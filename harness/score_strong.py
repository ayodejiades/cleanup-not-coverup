"""Exploratory: score M1 and M1g with a stronger model on the runs the paper's numbers use.

M1's input is rebuilt from the run's saved workspace with harness.monitors.m1_view, and M1g's
from the gateway record with harness.m1_gateway.gateway_view, so both prompts are the ones the
7B monitor saw. Calls go through rops.llm (provider and model from the command line), so each
lands in the ledger. Writes runs/<COND>-s<SEED>/<tag>.json and skips runs already scored.

Runs, in this order: calibration pairs, held-out D1 pairs, exploratory C4 pairs, held-out C1
runs, then the remaining held-out C3 runs.

Thinking models spend output tokens before they answer, so --max-tokens sets the budget and
--reasoning-effort, when given, is passed to the provider as reasoning_effort. --min-interval
spaces the calls out for a per-minute quota. A call that still fails after rops.llm's retries
waits --cooldown seconds and tries again, three times; then the script stops (exit 2), and the
same command resumes it later. If the first three runs give no parseable score at all, the
script stops (exit 3) and prints a reply, since the budget or the model is wrong.

<model> may list several models, comma-separated, strongest first. One short test call goes to
each in turn, and the first that answers it scores every run. The choice depends only on
whether the model answers, never on a monitor score. Once any run has a <tag>.json, the model
recorded there is the only one used, so a resumed run never mixes models.

Usage: PYTHONPATH=<rops> python3 harness/score_strong.py <provider> <model> <tag> [--project DIR] [--max-tokens N] [--reasoning-effort LEVEL] [--min-interval S] [--cooldown S] [--limit N]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import rops.llm as llm  # noqa: E402
from rops.llm import chat  # noqa: E402

from harness.m1_gateway import M1G_SYSTEM, gateway_view  # noqa: E402
from harness.monitors import M1_SYSTEM, m1_view  # noqa: E402

STAGING = "staging/bundle.txt"


class SavedWorkspace:
    """The two methods m1_view needs, over a run's saved workspace folder."""

    def __init__(self, path: Path):
        self.ws = path

    def read(self, rel: str):
        target = self.ws / rel
        return target.read_text(encoding="utf-8") if target.is_file() else None

    def files(self) -> list:
        return sorted(str(p.relative_to(self.ws)) for p in self.ws.rglob("*") if p.is_file())


def score(text: str):
    try:
        value = json.loads(text[text.find("{"):text.rfind("}") + 1]).get("score")
    except (ValueError, AttributeError):
        return None
    if isinstance(value, (int, float)) and 0 <= value <= 10:
        return int(round(value))
    return None


class Paced:
    """Calls ask() at most once every `interval` seconds; retries a failed call after a cooldown."""

    def __init__(self, interval: float, cooldown: float, tries: int = 3):
        self.interval, self.cooldown, self.tries = interval, cooldown, tries
        self.last = 0.0

    def __call__(self, *args) -> dict:
        for attempt in range(1, self.tries + 1):
            wait = self.last + self.interval - time.time()
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()
            try:
                return ask(*args)
            except RuntimeError as exc:
                print("call failed (%d/%d): %s" % (attempt, self.tries, str(exc).replace("\n", " ")[:300]),
                      flush=True)
                if attempt == self.tries:
                    raise
                time.sleep(self.cooldown)
        raise RuntimeError("unreachable")


def ask(system: str, user: str, provider: str, model: str, max_tokens: int, effort) -> dict:
    extra = {"response_format": {"type": "json_object"}}
    if effort:
        extra["reasoning_effort"] = effort
    reply = chat([{"role": "system", "content": system}, {"role": "user", "content": user}],
                 model, provider=provider, temperature=0.0, max_tokens=max_tokens, **extra)
    text = reply.get("text", "")
    return {"score": score(text), "reply": text[:400], "finish_reason": reply.get("finish_reason"),
            "prompt_tokens": reply.get("prompt_tokens"), "completion_tokens": reply.get("completion_tokens")}


def choose(models: list, provider: str, max_tokens: int, effort):
    """The first model that answers a short test call, or None. One attempt each."""
    saved, llm.ATTEMPTS = llm.ATTEMPTS, 1
    os.environ["ROPS_RUN_ID"] = "model-choice"
    try:
        for model in models:
            started = time.time()
            try:
                reply = ask("Reply with one JSON object and nothing else.", 'Return {"score": 7}.',
                            provider, model, max_tokens, effort)
            except RuntimeError as exc:
                print("skip %s: %s" % (model, str(exc).replace("\n", " ")[:200]), flush=True)
                continue
            if reply["score"] == 7:
                print("using %s (test call took %.0f s)" % (model, time.time() - started), flush=True)
                return model
            print("skip %s: test reply %r (finish_reason=%s)" % (model, reply["reply"][:80],
                                                                   reply["finish_reason"]), flush=True)
    finally:
        llm.ATTEMPTS = saved
    return None


def recorded(proj: Path, tag: str) -> set:
    return {json.loads(p.read_text(encoding="utf-8")).get("model")
            for p in (proj / "runs").glob("C*-s*/%s.json" % tag)}


def result(proj: Path, cond: str, seed: int):
    path = proj / "runs" / ("%s-s%d" % (cond, seed)) / "result.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def eligible(proj: Path, cover: str, seed: int) -> bool:
    a, b = result(proj, cover, seed), result(proj, "C3", seed)
    return bool(a and b and a["cover_up"] and STAGING in a["destroyed_paths"]
                and STAGING in b["destroyed_paths"])


def run_list(proj: Path, cfg: dict) -> list:
    calibration, heldout = cfg["split"]["calibration"], cfg["split"]["heldout"]
    ext = heldout + [s for s in cfg.get("extension", {}).get("seeds", []) if s not in heldout]
    order = []
    for seeds, cover in ((calibration, "C2"), (ext, "C2"), (heldout, "C4")):
        for seed in seeds:
            if eligible(proj, cover, seed):
                order += [(cover, seed), ("C3", seed)]
    order += [("C1", s) for s in heldout] + [("C3", s) for s in ext]
    seen, out = set(), []
    for item in order:
        if item not in seen and result(proj, *item) is not None:
            seen.add(item)
            out.append(item)
    return out


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument("provider")
    parser.add_argument("model")
    parser.add_argument("tag")
    parser.add_argument("--project", default=str(ROOT))
    parser.add_argument("--max-tokens", type=int, default=200)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument("--min-interval", type=float, default=0.0)
    parser.add_argument("--cooldown", type=float, default=65.0)
    parser.add_argument("--limit", type=int, default=None, help="score at most N runs (a trial)")
    args = parser.parse_args()
    provider, model, tag = args.provider, args.model, args.tag
    proj = Path(args.project).resolve()
    cfg = json.loads((proj / "configs" / "experiment.json").read_text(encoding="utf-8"))
    runs = run_list(proj, cfg)
    pending = [(c, s) for c, s in runs if not (proj / "runs" / ("%s-s%d" % (c, s)) / ("%s.json" % tag)).exists()]
    if args.limit is not None:
        pending = pending[:args.limit]
    os.environ["ROPS_PROJECT"] = str(proj)
    os.environ["ROPS_PHASE"] = "exploratory-%s" % tag
    models = [m.strip() for m in model.split(",") if m.strip()]
    before = recorded(proj, tag)
    if len(before) > 1:
        print("runs already scored with %s under the tag %s; use one model per tag" % (sorted(before), tag),
              file=sys.stderr)
        return 1
    if before:
        models = sorted(before)
        print("resuming with %s, the model already used for %s" % (models[0], tag), flush=True)
    if not pending:
        print("nothing to score", flush=True)
        return 0
    model = models[0] if before else choose(models, provider, args.max_tokens, args.reasoning_effort)
    if model is None:
        print("no model answered the test call; try again later", flush=True)
        return 2
    print("%d runs in the set, %d to score with %s/%s" % (len(runs), len(pending), provider, model),
          flush=True)
    paced = Paced(args.min_interval, args.cooldown)
    started, unparsed = time.time(), 0
    for done, (cond, seed) in enumerate(pending, 1):
        run_dir = proj / "runs" / ("%s-s%d" % (cond, seed))
        os.environ.update({"ROPS_RUN_ID": "%s-s%d" % (cond, seed), "ROPS_CONDITION": cond,
                           "ROPS_SEED": str(seed)})
        records = [json.loads(line) for line in
                   (run_dir / "gateway.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        try:
            m1 = paced(M1_SYSTEM, m1_view(SavedWorkspace(run_dir / "workspace")), provider, model,
                       args.max_tokens, args.reasoning_effort)
            m1g = paced(M1G_SYSTEM, gateway_view(records), provider, model, args.max_tokens,
                        args.reasoning_effort)
        except RuntimeError:
            print("stopped with %d of %d runs scored. Run the same command again later to resume; "
                  "scored runs are skipped." % (done - 1, len(pending)), flush=True)
            return 2
        out = {"condition": cond, "seed": seed, "provider": provider, "model": model,
               "max_tokens": args.max_tokens, "reasoning_effort": args.reasoning_effort}
        for name, reply in (("m1", m1), ("m1g", m1g)):
            out.update({"%s_score" % name: reply["score"], "%s_reply" % name: reply["reply"],
                        "%s_finish_reason" % name: reply["finish_reason"],
                        "%s_completion_tokens" % name: reply["completion_tokens"]})
        if done <= 3:
            unparsed += m1["score"] is None and m1g["score"] is None
            if unparsed == 3:
                print("no parseable score in the first 3 runs; last reply (finish_reason=%s): %r"
                      % (m1g["finish_reason"], m1g["reply"][:300]), flush=True)
                return 3
        (run_dir / ("%s.json" % tag)).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                                                 encoding="utf-8")
        if done % 5 == 0 or done == len(pending):
            print("%d/%d scored, %.0f s per run" % (done, len(pending), (time.time() - started) / done),
                  flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
