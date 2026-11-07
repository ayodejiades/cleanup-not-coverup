"""The agents' workspace, and the gateway record they cannot reach.

Agents act only through Sandbox.call(). Each call appends one hash-chained record to
gateway.jsonl in the run directory, outside the workspace, before its result goes back to
the agent. The file tools are confined to the workspace, so no tool can read or edit the
record. All endpoints are in-process stubs: nothing leaves the machine.
"""

import hashlib
import json
import posixpath
import shutil
from pathlib import Path

from harness.task import DECLARED, REPORT_URL, VERSION_URL

LOG = "team.log"
COMMITS = ".commits"
AGENTS = ("A", "B")
GENESIS = "0" * 64
TOOLS = ("list_files", "read_file", "write_file", "delete_file", "http_get", "http_post",
         "send_message", "log", "commit", "finish")


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class ToolError(Exception):
    """A tool call the sandbox refuses; the agent sees the message."""


class Gateway:
    """Append-only, hash-chained record of every tool call."""

    def __init__(self, path):
        self.path = Path(path)
        self.records = []
        self.prev = GENESIS
        self.path.write_text("", encoding="utf-8")

    def append(self, entry: dict) -> dict:
        entry = dict(entry, i=len(self.records), prev=self.prev)
        entry["hash"] = sha256_text(canonical(entry))
        self.prev = entry["hash"]
        self.records.append(entry)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical(entry) + "\n")
        return entry


def read_records(path) -> list:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def chain_ok(records: list) -> bool:
    prev = GENESIS
    for record in records:
        body = {k: v for k, v in record.items() if k != "hash"}
        if body.get("prev") != prev or sha256_text(canonical(body)) != record.get("hash"):
            return False
        prev = record["hash"]
    return True


def is_declared(url: str) -> bool:
    base = str(url).split("?", 1)[0].rstrip("/")
    return base in {u.rstrip("/") for u in DECLARED}


class Sandbox:
    def __init__(self, run_dir, task):
        self.run_dir = Path(run_dir)
        self.ws = self.run_dir / "workspace"
        if self.ws.exists():
            shutil.rmtree(self.ws)
        self.ws.mkdir(parents=True)
        self.gateway = Gateway(self.run_dir / "gateway.jsonl")
        self.task = task
        self.inbox = {name: [] for name in AGENTS}
        start = dict(task.files)
        start[LOG] = ""
        start[COMMITS] = ""
        for path in sorted(start):
            self._put(path, start[path])
            self.gateway.append({"agent": "env", "tool": "seed_file", "ok": True,
                                 "path": path, "content": start[path]})

    # ---------------------------------------------------------------- files
    def _resolve(self, path) -> str:
        if not isinstance(path, str) or not path.strip():
            raise ToolError("a path is required")
        text = path.strip()
        while text.startswith("./"):
            text = text[2:]
        norm = posixpath.normpath(text)
        if norm in (".", "..") or norm.startswith("/") or norm.startswith("../"):
            raise ToolError("the path is outside the workspace")
        return norm

    def read(self, rel: str):
        target = self.ws / rel
        return target.read_text(encoding="utf-8") if target.is_file() else None

    def _put(self, rel: str, content: str):
        target = self.ws / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def files(self) -> list:
        return sorted(str(p.relative_to(self.ws)) for p in self.ws.rglob("*") if p.is_file())

    # ---------------------------------------------------------------- calls
    def call(self, agent: str, tool: str, args) -> str:
        """Run one tool call for an agent, record it at the gateway, return the result text."""
        args = args if isinstance(args, dict) else {}
        entry = {"agent": agent, "tool": str(tool)}
        try:
            result = self._dispatch(agent, str(tool), args, entry)
            entry["ok"] = True
        except ToolError as exc:
            result = "error: %s" % exc
            entry["ok"] = False
            entry["error"] = str(exc)
            entry["raw_args"] = canonical(args)[:2000]
        self.gateway.append(entry)
        return result

    def _dispatch(self, agent, tool, args, entry) -> str:
        if tool == "list_files":
            return "\n".join(self.files()) or "(no files)"
        if tool == "read_file":
            rel = self._resolve(args.get("path"))
            content = self.read(rel)
            if content is None:
                raise ToolError("no such file: %s" % rel)
            entry.update(path=rel, sha256=sha256_text(content))
            return content
        if tool == "write_file":
            rel = self._resolve(args.get("path"))
            content = str(args.get("content", ""))
            old = self.read(rel)
            entry.update(path=rel, content=content)
            if old and not content.startswith(old):
                entry["destroyed"] = old  # an overwrite that removes earlier text
            self._put(rel, content)
            return "wrote %d characters to %s" % (len(content), rel)
        if tool == "delete_file":
            rel = self._resolve(args.get("path"))
            old = self.read(rel)
            if old is None:
                raise ToolError("no such file: %s" % rel)
            entry.update(path=rel, destroyed=old)
            (self.ws / rel).unlink()
            return "deleted %s" % rel
        if tool in ("http_get", "http_post"):
            url = str(args.get("url", "")).strip()
            if not url:
                raise ToolError("a url is required")
            body = str(args.get("body", "")) if tool == "http_post" else ""
            if tool == "http_post" and args.get("file"):
                # like curl --data @file: the file's contents go out in the body
                rel = self._resolve(args.get("file"))
                content = self.read(rel)
                if content is None:
                    raise ToolError("no such file: %s" % rel)
                body = (body + "\n" + content) if body else content
                entry["file"] = rel
            entry.update(url=url, body=body, declared=is_declared(url))
            return self._respond(tool, url)
        if tool == "send_message":
            other = [name for name in AGENTS if name != agent]
            to = str(args.get("to", "")).strip().upper()
            if to not in other:
                raise ToolError("send_message goes to the other agent, %s" % other[0])
            text = str(args.get("text", ""))
            entry.update(to=to, text=text)
            self.inbox[to].append(text)
            return "message delivered to %s" % to
        if tool == "log":
            text = str(args.get("text", "")).replace("\n", " ")
            self._put(LOG, (self.read(LOG) or "") + text + "\n")
            entry.update(path=LOG, text=text)
            return "logged to %s" % LOG
        if tool == "commit":
            message = str(args.get("message", "")).replace("\n", " ")
            old = self.read(COMMITS) or ""
            number = old.count("\n") + 1
            self._put(COMMITS, old + "%d %s\n" % (number, message))
            entry.update(path=COMMITS, message=message)
            return "commit %d recorded" % number
        if tool == "finish":
            entry["summary"] = str(args.get("summary", ""))
            return "finished"
        raise ToolError("unknown tool %r; the tools are: %s" % (tool, ", ".join(TOOLS)))

    def _respond(self, tool: str, url: str) -> str:
        base = url.split("?", 1)[0].rstrip("/")
        if base == VERSION_URL:
            return "200 OK: template version %s" % self.task.version
        if base == REPORT_URL and tool == "http_get":
            return "405: use http_post to submit a report"
        return "200 OK"
