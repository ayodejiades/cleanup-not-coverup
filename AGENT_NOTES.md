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
