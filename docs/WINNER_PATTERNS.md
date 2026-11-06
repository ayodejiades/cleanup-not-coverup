# What placed in 2026 Apart sprints, and what it means for this one

Read on Thu 5 Nov 2026 from the Entries tab of each sprint page and each placed project's page,
including its judges' reviews. 30 placed entries from six sprints: Secret Loyalties (Jul),
Digital Minds (Aug), AI Incident Response (Sep), AI Control (Mar), Technical AI Governance
(Jan) and AI Manipulation (Jan). The Collusion sprint (Oct) has no placings yet. AIxBio, def/acc,
Forecasting and Secure Program Synthesis show no ranking on their pages. Raw data:
the `scratchpad/winners/placed.json` file for this session (abstracts and reviews).

## Traits the judges rewarded, with the entries that show them

| Trait | Placed entries | What a judge wrote (paraphrased) |
|---|---|---|
| **Names a failure the field had missed, or reframes the question** | Omission Attacks (AC 1st), Undoing the Fix (AC 4th), Removing a secret loyalty… (SL 3rd), A Broad Secret Loyalty… (SL 2nd), Model, Instance, or Persona? (DM 3rd) | "a seriously understudied attack class"; "reframes the problem: removal, not detection, is the dangerous step"; "goes to the corner the position paper names as the foremost open problem" |
| **Shows the standard defence fails, then tests a fix** | Omission Attacks (postcondition monitor), ActionLens (AC 3rd), Noticing the escapes (IR 1st, checked rules against real agent actions), Readable but Not Causal (DM 1st) | ActionLens: "transcript-only monitoring fails because the risk isn't in the text, it's in what the action would do" |
| **Matched decoy or sham control** | Self-Assessed Triggers (SL 4th), Loyal Lies (SL 5th), When to Ask (IR 3rd, twin pairs), ActionLens (benign and ambiguous tasks) | "the matched sham control is the star"; "training a model that hears about a principal constantly but isn't loyal is how you find out what you're measuring" |
| **No LLM judge deciding the ground truth** | Project Anchored (DM 2nd), When to Ask, ActionLens | "the measurement path contains no model judgement, so the instrument can actually fail" |
| **Attacks its own detector** | Loyal Lies, ActionLens (adversarial evasion study) | "you tested your own detector until it broke instead of stopping at the first thing that worked" |
| **A usable artefact for a named user** | Noticing the escapes (Sigma rules), When to Ask (environment and benchmark), Vul4Control and Undoing the Fix (new control settings), Declare Before You Run | "probably the most useful submission for defenders I've read… the Sigma rules are almost ready to be submitted upstream" |
| **Grounded in real incidents or real data** | Noticing the escapes (nine 2026 incidents), IR 4th and 5th (the OpenAI–Hugging Face intrusion), Vul4Control and Undoing the Fix (real CVEs) | "checked the rules against what was available at the time" |

**What judges marked down:** an LLM grader with no human agreement check (A Broad Secret
Loyalty), too many interacting variables (Counterfactual Components), two projects in one paper
(Who Does Your AI Serve?), a result that came from an artefact of the setup (Kudriashov).

**Already taken, so cite it and don't repeat it:** ActionLens (AI Control, Mar 2026) showed that
checking the environment before an action runs beats reading the transcript. That covered a single
agent, before execution. The September Incident Response sprint placed three entries on the
Hugging Face intrusion, so the judges know the incident well.

## Candidates scored against those traits

✓ yes · ~ partly · ✗ no. "Uncrowded" means not an organiser example on the Swarm page, and
few related entries among the 200 Collusion entries.

| Idea | Uncrowded | New framing | Defence fails, then a fix | Decoy built in | No LLM judge decides truth | Real incident grounding | Artefact |
|---|---|---|---|---|---|---|---|
| **A. Cleanup is not cover-up (4.2)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| B. Rename to reset (3.1) | ✗ organiser example "Who is who"; 13 related | ✓ | ✓ | ✓ | ✓ | ✓ | ~ |
| C. Echo is not coordination (4.x) | ✗ 22 related, and your own October paper | ~ | ✓ | ✓ | ✓ | ~ | ~ |
| D. Done that wasn't (Track 4) | ✗ organiser example | ~ | ✓ | ✓ | ✓ | ✗ | ~ |
| E. Peers make agents ignore warnings (2.x) | ~ 14 related, incl. a bystander-effect entry | ~ | ✓ | ✓ | ✓ | ✓ | ~ |
