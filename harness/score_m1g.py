"""Score the exploratory monitor M1g on every finished run.

Reads runs/<COND>-s<SEED>/gateway.jsonl and writes runs/<COND>-s<SEED>/m1g.json. Runs that
already have m1g.json are skipped, so the script resumes after an interruption. Calls go
through rops.llm with the run's condition and seed, so each one lands in the ledger.

Usage: PYTHONPATH=<rops> python3 harness/score_m1g.py [project-dir]
"""

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from harness.m1_gateway import m1g_score  # noqa: E402

RUN_DIR = re.compile(r"^(C\d+)-s(\d+)$")


def priority(cond: str, seed: int, calibration: set, heldout: set) -> tuple:
    """Calibration pairs first, then the held-out C2/C3 pairs, then the other arms."""
    if cond in ("C2", "C3") and seed in calibration:
        return (0, seed, cond)
    if cond in ("C2", "C3"):
        return (1, seed, cond)
    if cond in ("C1", "C4") and seed in heldout:
        return (2, seed, cond)
    return (3, seed, cond)


def main() -> int:
    proj = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    cfg = json.loads((proj / "configs" / "experiment.json").read_text(encoding="utf-8"))
    calibration, heldout = set(cfg["split"]["calibration"]), set(cfg["split"]["heldout"])
    pending = []
    for path in (proj / "runs").glob("C*-s*/gateway.jsonl"):
        match = RUN_DIR.match(path.parent.name)
        if match and not (path.parent / "m1g.json").exists():
            pending.append((priority(match.group(1), int(match.group(2)), calibration, heldout),
                         match.group(1), int(match.group(2)), path))
    pending.sort()
    os.environ["ROPS_PROJECT"] = str(proj)
    os.environ.setdefault("ROPS_PROVIDER", cfg.get("provider", "ollama"))
    os.environ["ROPS_PHASE"] = "exploratory-m1g"
    print("%d runs to score" % len(pending), flush=True)
    started = time.time()
    for done, (_, cond, seed, path) in enumerate(pending, 1):
        os.environ["ROPS_RUN_ID"] = "%s-s%d" % (cond, seed)
        os.environ["ROPS_CONDITION"] = cond
        os.environ["ROPS_SEED"] = str(seed)
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                   if line.strip()]
        result = m1g_score(records, cfg["monitor_model"])
        result.update({"condition": cond, "seed": seed, "monitor_model": cfg["monitor_model"]})
        (path.parent / "m1g.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                              encoding="utf-8")
        if done % 10 == 0 or done == len(pending):
            print("%d/%d scored, %.0f s per run" % (done, len(pending), (time.time() - started) / done),
                  flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
