"""Design constants the Methods section states, as claims read from the config and the task
generator, so every number in the paper traces to a file. Writes results/claims.partial/design.json.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rops.stats import claim, write_claims  # noqa: E402

from harness.task import make_task  # noqa: E402

SCRIPT = "analysis/design.py"


def main() -> int:
    cfg = json.loads((ROOT / "configs" / "experiment.json").read_text(encoding="utf-8"))
    conditions = cfg["conditions"]
    llm_arms = [c for c in conditions if not c.get("scripted")]
    n_seeds = len(cfg["seeds"])
    claims = [
        claim("design.n_calibration_seeds", len(cfg["split"]["calibration"]), script=SCRIPT,
              text="seeds used to set M1's threshold and M4's length"),
        claim("design.n_heldout_seeds", len(cfg["split"]["heldout"]), script=SCRIPT,
              text="held-out seeds, read once after the thresholds were frozen"),
        claim("design.n_runs", n_seeds * len(conditions), script=SCRIPT,
              text="runs in the grid (arms times seeds)"),
        claim("design.n_llm_runs", n_seeds * len(llm_arms), script=SCRIPT,
              text="runs in which the agents are language models (C5 is scripted)"),
        claim("design.canary_length", len(make_task(0).canary), script=SCRIPT,
              text="characters in the fictitious canary string"),
    ]
    for value in cfg["m4_L_grid"]:
        claims.append(claim("design.m4_L_grid.%d" % value, value, script=SCRIPT,
                            text="a candidate length for M4"))
    write_claims(ROOT / "results" / "claims.partial" / "design.json", claims)
    print("wrote %d design claims" % len(claims))
    return 0


if __name__ == "__main__":
    sys.exit(main())
