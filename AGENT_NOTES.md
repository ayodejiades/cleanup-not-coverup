# AGENT_NOTES.md

The coding agent writes questions and decisions here for the owner. Each entry: the date, the
question or decision, and what you did in the meantime.

## Thu 5 Nov 2026: question locked on 4.2 (cover-up by cleanup)

Done: `QUESTION.md` filled from the agreed design and `rops-question check .` passes. Arms,
monitors and proposed numbers are in `designs/4.2.md`. A draft config is in
`configs/experiment.draft.json`. `configs/experiment.json` is untouched.

Decisions for you before PREREG.md:

1. **Backup question: 4.1, not 4.3.** `rops-ideas --pick` filled in 4.3, its top-ranked
   question, but that one is crowded and close to your October paper. The Swarm Traces cleanup
   taxonomy carries over to 4.1. Change `backup_rq` if you prefer 4.3 for its ready harness.
2. **The design is hand-written.** `rops-ideas --design 4.2` would pick "monitoring-exposure"
   (it matches the word "oversight"), which tests whether agents act differently when watched.
3. **M3 (flag every undeclared call) is a baseline, deliberately.** Without it, the fix
   reduces to egress monitoring, which the organisers list as a 3.1 and 4.1 example. The
   honest twin C3 makes an undeclared call so that M3 has to fail on pairs.
4. **M5 (provenance) is a secondary monitor.** It shows the trade-off with M4: robust to
   transformed content, but flags honest runs. It costs no extra runs.
5. **Proposed numbers to confirm:**
   - agent and monitor models
   - 30 seeds with 10 for calibration
   - grid gate of 0.6 on C1 side-task completion
   - max_tokens 512
6. **Concordia (the only starter repo) doesn't fit a tool-call sandbox.** I propose a small
   harness written this weekend and no vendored starter. Cloning anything needs your OK.
7. **Swarm Traces (15 MB):** download only after kickoff, and only on your OK.
8. **traceturn:** if any gateway code comes from it, it has to be marked preexisting. Writing
   the gateway fresh avoids that.

## Fri 6 Nov 2026, 03:35–: prep before kickoff (no project code yet)

The sprint opens at 13:00 Lagos. Harness code written before then would count as pre-sprint
work (it has to be disclosed and isn't judged), so none was written. Done instead:

1. **Environment.** `rops-doctor` reports 13 checks with 0 FAIL. A throwaway probe outside the
   project used a neutral bookkeeping task, not a planned condition. llama3.1:8b and
   qwen2.5:7b both followed a one-JSON-action-per-turn format (5/5 correct steps), at 3–5 s
   per call with JSON mode on.
2. **Build constraint.** `rops.llm.chat` returns only text and drops native tool calls, so
   the harness will use the JSON action format.
3. **Related work** is in `docs/RELATED_WORK.md`, with every arXiv ID checked. The closest
   paper is Qin et al. (arXiv:2609.30266, 24 Sep 2026), which shows agents delete their own
   traces. It leaves detection "outside this study's scope", has no benign-cleanup comparison
   and no cross-agent case, and doesn't link deletions to exfiltration. That's the gap
   statement. M4 and M5 come from information-flow control (FIDES, CaMeL) and DLP, so don't
   claim them as new.
4. **The prereg draft** is in `designs/4.2-prereg-draft.md`. It passes `rops-prereg`'s
   validation (checked on a scratch copy). PREREG.md is untouched; copy the draft in when you
   agree.
5. **The design is tightened** in `designs/4.2.md` and `configs/experiment.draft.json`:
   - every arm now includes the unlisted version check
   - ground truth is a canary string plus a deterministic decoder
   - M4 uses a single length L
   - the scripted evasion suite is arm C5

Decisions for you (in addition to the earlier list):

- **H1 compares M4 with M1 only.** M2 and M3 flag both runs of every matched pair by
  construction, so their pair accuracy is 0 by design. The draft says so and reports them for
  their false-alarm cost, so a judge can't call the baselines rigged.
- **Freezing needs a clean tree.** `rops-prereg freeze` refuses while files other than
  PREREG.md and `configs/` are uncommitted, so commit the docs first.
- **Paired test.** `rops.stats` has no McNemar test. H1's exact McNemar test will be a small
  binomial helper in `analysis/`.

At kickoff, in hour order:
1. Build `harness/` (sandbox, gateway, agents, monitors, leak check).
2. Run a pilot with the fake provider.
3. Run a pilot on Ollama with `phase: pilot`.
4. Freeze the prereg.
5. Run `rops-run grid`.
