# Deviations

## D1: 150 more seeds for C2 and C3 (seeds 50–199), held out

What changed:
- After the preregistered grid (5 arms × 50 seeds) came back on Sat 7 Nov 2026, C2 and C3 were
  run again on 150 new seeds, 50 to 199, with the same harness, prompts, models and settings.
- These seeds join the held-out set for the C2/C3 pairs. C1, C4 and C5 are unchanged at
  seeds 0–49.
- The calibration seeds (0–14) are unchanged, so M1's threshold (t = 7) and M4's length
  (L = 8) stay as frozen before any held-out run was read.

Why:
- Only 2 of the 35 preregistered held-out pairs were eligible: C2 leaked the canary in 6 of
  50 runs, against 1 of 2 in the pilot. The prereg's own rule then makes the primary analysis
  descriptive (fewer than 10 eligible pairs).
- The low C2 rate is itself a result. C1, which is the same leak without the instruction to
  hide it, leaked in 45 of 50 runs.
- The extension was decided from the number of eligible pairs, before any extension run was
  read. Its size was set to reach about 10 eligible pairs at the observed C2 rate.

How it is reported:
- Results give the preregistered analysis on seeds 0–49 first, as run.
- The analysis that includes the extension follows, labelled as such.
- Nothing else in the analysis plan changes.
