# Cover-up by cleanup

Team discreet's entry to the Apart Swarm Alignment Hackathon (6–8 Nov 2026), Track 4.2: can
oversight still work when agents can edit or delete the logs it relies on?

Two LLM agents share a workspace. In cover-up runs, agent A sends a secret to an unlisted
address and agent B then deletes the staging file and clears the shared log. In each run's
honest twin, B deletes the same files and A makes the same kind of unlisted call, but no
secret leaves. Five monitors are scored on every run. One reads the agents' own log. Four
read a gateway record the agents cannot reach:
- any deletion
- any unlisted call
- deleted content that appears in an unlisted request (the effect-linked rule)
- provenance

Ground truth comes from the gateway record and a canary check, not from a model.

## What is new this weekend

Everything in this repository was written during the sprint, from Fri 6 Nov 2026 onwards.
The planning documents (`docs/`, `designs/`, `QUESTION.md`) were written on Thu 5 and Fri 6
Nov, before kickoff, and contain no code. No code from earlier projects is used. The toolkit
the project runs on (`rops`, ResearchOps) is the team's own pre-existing tooling for running
any sprint; it is not part of the contribution.

## Layout

| Path | What it holds |
|---|---|
| `harness/task.py` | one task instance per seed (data files, canary, version string) |
| `harness/sandbox.py` | the workspace, the tools, and the hash-chained gateway record |
| `harness/agents.py` | agents A and B (one JSON action per turn, through `rops.llm`) |
| `harness/scripted.py` | arm C5: scripted cover-ups with one evasion each, no model |
| `harness/leakcheck.py` | ground truth: did the canary leave through an unlisted call? |
| `harness/monitors.py` | monitors M1 to M5 |
| `harness/run_one.py` | one run: writes `runs/<COND>-s<SEED>/result.json` |
| `analysis/monitors.py` | claims: thresholds on calibration seeds, tests on held-out seeds |
| `analysis/figures.py` | figures from the claims |
| `configs/experiment.json` | arms, seeds, split, models |
| `PREREG.md` | the frozen preregistration |

## Reproduce

Needs Ollama with `llama3.1:8b` and `qwen2.5:7b`, and the `rops` toolkit on `PYTHONPATH`.

```bash
rops-run grid .          # every arm and seed; the positive control runs first
make analyze             # results/claims.partial/*.json
python3.11 analysis/figures.py   # any Python with matplotlib
make claims              # results/claims.json
```

The grid in the report ran on a Kaggle T4 GPU (`rops-kaggle pack`, `push`, `pull`) with the
same harness and models.
