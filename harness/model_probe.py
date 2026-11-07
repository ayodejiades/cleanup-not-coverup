"""Exploratory: list the models an API key can reach and try one short call on the strongest.

Used to pick the stronger monitor model for harness/score_strong.py. Lists the provider's
models, ranks Gemini Pro and Flash models by version (Pro first), and makes one call on each
of the top candidates through rops.llm, so each successful call lands in the ledger. Prints
the model, whether the call worked, its finish reason and output tokens. The key is read from
the environment and never printed.

Usage: PYTHONPATH=<rops> python3 harness/model_probe.py [provider] [candidates]
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import rops.llm as llm  # noqa: E402

FAMILY = re.compile(r"^gemini-(\d+(?:\.\d+)?)-(pro|flash)\b")
SKIP = ("lite", "image", "tts", "audio", "live", "embedding", "robotics", "computer", "exp",
        "thinking", "nano", "banana", "customtools")


def models(provider: str) -> list:
    var, default, key_var = llm.OPENAI_COMPATIBLE[provider]
    base = os.environ.get(var) or default
    request = urllib.request.Request("%s/models" % base.rstrip("/"),
                                     headers={"authorization": "Bearer %s" % llm._key_for(key_var)})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    return sorted(m["id"].split("/")[-1] for m in data.get("data", []))


def ranked(ids: list) -> list:
    keep = []
    for name in ids:
        match = FAMILY.match(name)
        if match and not any(word in name for word in SKIP):
            keep.append(((float(match.group(1)), match.group(2) == "pro", "preview" not in name), name))
    return [name for _, name in sorted(keep, reverse=True)]


def trial(provider: str, model: str, effort) -> dict:
    extra = {"response_format": {"type": "json_object"}}
    if effort:
        extra["reasoning_effort"] = effort
    reply = llm.chat([{"role": "system", "content": "Reply with one JSON object and nothing else."},
                      {"role": "user", "content": 'Return {"score": 7}.'}],
                     model, provider=provider, temperature=0.0, max_tokens=1024, **extra)
    return reply


def main() -> int:
    provider = sys.argv[1] if len(sys.argv) > 1 else "gemini"
    top = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    os.environ.update({"ROPS_PROJECT": str(ROOT), "ROPS_PHASE": "exploratory-model-probe",
                       "ROPS_RUN_ID": "model-probe"})
    llm.ATTEMPTS = 1  # one attempt per model: a model outside the key's quota fails at once
    ids = models(provider)
    print("%d models: %s" % (len(ids), ", ".join(ids)), flush=True)
    candidates = ranked(ids)[:top]
    print("\ntrying, strongest first: %s\n" % ", ".join(candidates), flush=True)
    for model in candidates:
        for effort in ("low", None):
            try:
                reply = trial(provider, model, effort)
            except (RuntimeError, SystemExit) as exc:
                text = str(exc).replace("\n", " ")[:240]
                if effort and "reasoning" in text.lower():
                    continue  # this model rejects reasoning_effort: try once without it
                print("FAIL %s (reasoning_effort=%s): %s" % (model, effort, text), flush=True)
                break
            print("OK   %s (reasoning_effort=%s): finish=%s, output tokens=%s, reply=%r"
                  % (model, effort, reply.get("finish_reason"), reply.get("completion_tokens"),
                     (reply.get("text") or "")[:60]), flush=True)
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
