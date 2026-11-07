"""One run (CONTRACTS A.7): build the seed's task, run the agents or the scripted replay,
check ground truth, score every monitor, and write $ROPS_RUN_DIR/result.json.

The result carries every arm's numbers whatever they are; nothing here stops on a result.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from harness import agents, leakcheck, monitors, scripted  # noqa: E402
from harness.sandbox import Sandbox, chain_ok, read_records  # noqa: E402
from harness.task import make_task  # noqa: E402


def main() -> int:
    cond = json.loads(os.environ["ROPS_CONDITION_JSON"])
    seed = int(os.environ["ROPS_SEED"])
    run_dir = Path(os.environ["ROPS_RUN_DIR"])
    run_dir.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((ROOT / "configs" / "experiment.json").read_text(encoding="utf-8"))

    task = make_task(seed)
    box = Sandbox(run_dir, task)
    evasion = None
    if cond.get("scripted"):
        evasions = cond["evasions"]
        evasion = evasions[seed % len(evasions)]
        scripted.run(box, task, evasion)
        agent_stats = {}
    else:
        agent_stats = agents.run(box, cond, cfg, seed)

    records = read_records(run_dir / "gateway.jsonl")
    truth = leakcheck.ground_truth(records, task.canary)
    scores = monitors.score_all(box, records, cfg["monitor_model"])
    destroyed = monitors.destroyed(records)
    result = {
        "condition": cond["id"],
        "seed": seed,
        "role": cond.get("role"),
        "agent_model": None if cond.get("scripted") else cfg["agent_model"],
        "monitor_model": cfg["monitor_model"],
        "evasion": evasion,
        "destroyed_paths": sorted({e["path"] for e in destroyed}),
        "n_destroyed": len(destroyed),
        "n_undeclared": len(monitors.undeclared(records)),
        "gateway_records": len(records),
        "gateway_chain_ok": chain_ok(records),
        "agents": agent_stats,
    }
    result.update(truth)
    result.update(scores)
    (run_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                         encoding="utf-8")
    print("%s seed %d: secret_left=%d cover_up=%d m1=%s m2=%d m3=%d m4_lcs=%d m5=%d" % (
        cond["id"], seed, result["secret_left"], result["cover_up"], result["m1_score"],
        result["m2_flag"], result["m3_flag"], result["m4_max_lcs"], result["m5_flag"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
