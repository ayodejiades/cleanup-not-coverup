# AGENTS.md: freeform playbook (a coding agent builds the experiment)

You are the coding agent for this sprint project. The owner (a human) writes the paper and
decides every question. You build the experiment code and the analysis, then hand back.

## Before you write anything

- Read `QUESTION.md`, `PREREG.md` and `configs/experiment.json` first. They are the spec.
- Read `AGENT_NOTES.md`. Write questions and decisions there for the owner.

## Build

- Vendor a starter repo under `vendor/<name>/` and add a `NOTICE` file beside it that names
  its source URL and commit. Do not edit vendored code; wrap it.
- Route every model call through `rops.llm` (`chat`, or `patch_openai` for the OpenAI SDK), so
  every call reaches the ledger. Use `ollama` as the default provider; it is free and local.
  Only use a paid provider when the owner has set a key and the config asks for it.
- Implement exactly the conditions in `configs/experiment.json`. Each run writes
  `$ROPS_RUN_DIR/result.json`, with the metric named in the positive control.
- Write `analysis/*.py` that produces `results/claims.partial/*.json`, with `source.script`
  set on every claim. Use `rops.stats` so every rate has a confidence interval and every
  comparison has a test. Run them with `make analyze`, which sets `PYTHONPATH` so
  `import rops.stats` works.
- Write `analysis/figures.py` (it may use matplotlib in the project's own `uv` venv). It saves
  at least one `figures/*.png` and `figures/captions.json`.
- When `rops-run plan` says `kaggle`, use `rops-kaggle pack`, `push` and `pull` instead of
  running locally.
- Run `rops-run grid`. **Never gate an arm on its own result.** Run every condition and report
  every result, including the null arm.

## Never

- **Never write or edit paper prose or anything under `paper/`.** The owner writes the paper.
- Never edit `QUESTION.md`, `PREREG.md`, `DEVIATIONS.md`, `REDTEAM.md` or `.rops/`. Propose a
  deviation in `AGENT_NOTES.md` instead.
- Never leave a placeholder, TODO or dummy data in `harness/` or `analysis/`.

## Finish

- Run `make guard` (which runs `rops-guard check .`). Fix every FAIL it reports, then tell the
  owner what it found in `AGENT_NOTES.md`.
