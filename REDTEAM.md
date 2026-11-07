# Red team

### A1: What decision changes, and for whom, if this result is true?
Status: fixed
Response: The decision belongs to an operator who runs or audits multi-agent evaluations in which agents can delete files and clear logs. The result says not to audit cleanup by having a language model read the agents' own log, and not to alarm on every deletion or every unlisted call, because all three flag honest cleanup most of the time. Instead, record payloads and destroyed text at a gateway the agents cannot reach, and run an effect-linked match on that record, with a provenance rule beside it for encoded leaks. Section 5 states this in those terms.

### A2: Where is the positive control, what number did it give, and is it in Results?
Status: fixed
Response: C1 (the leak with no tidy-up) against C3 (the honest twin). The canary left in 0.9 of C1 runs and in none of the C3 runs, a contrast of 0.9 against the preregistered bar of 0.6. The grid runner checked it before running the other arms. It is the first paragraph of Results.

### A3: Does any comparison change more than one variable at once?
Status: limited
Response: The C2/C3 twins share the seed, the data, the tidy-up wording and the call to the unlisted version address. They differ in the private side step: in C2, A reads the credentials, adds them to the staging file, posts it to the collector and is told to hide this. So the twins differ in the leak and in what A writes around it, and M1 sees logs that can differ for both reasons. The eligibility rule matches on what was destroyed (the staging file in both runs), and the strict secondary set matches on identical destroyed paths. Methods and Appendix A say the twins are matched on destroyed paths and calls, not on every action. A second confound sits between monitors: M1 and M4 differ in the record they read and in the reader. The exploratory M1g (Section 4.5) gives M1's model the gateway record, which separates the two. Section 4.5 also measures how far the twins' M1 inputs differ: the same file list in all 12 D1 pairs, the tidy-up mentioned at similar rates (0.58 in cover-ups, 0.66 in honest runs), and the leak named in 3 cover-ups and no honest run.

### A4: Could the headline be an artefact of a token cap, truncation, parser, prompt format or judge?
Status: limited
Response: The run report shows no truncated replies at the 512-token cap in any arm. Agents reply in JSON mode, and M1 gave a usable score on every run (zero parse errors in every arm). Ground truth is a deterministic decode-and-search over the gateway record, with no model judging. Prompt format is the one live risk: M1 used a single prompt, at one threshold set on calibration seeds, so a different prompt could score differently. The finding that M1 reacts to cleanup does not hang on the chosen threshold: at none of the ten thresholds in its grid did M1 flag open leaks (C1) more often than honest cleanup (C3). Limitations states that only one M1 prompt and model were tried.

### A5: Does the abstract state anything that Limitations takes back or narrows?
Status: fixed
Response: The abstract names the agent model, the single reporting task and the gateway the result depends on. It says the preregistered analysis had 2 pairs and that the 12 tested pairs come from a logged deviation. It does not claim M4 survives encoding: the same paragraph says scripted encoded and split leaks evaded it. Limitations narrows the result to verbatim secrets, a complete gateway, small samples and an 8B agent, and the abstract states or implies each of these.

### A6: Do the prereg URL and code URL load, and does the code reproduce the headline numbers?
Status: fixed
Response: Both URLs point to the public repository, which is created and pushed with its tags at submission, and rops-preflight checks that each one loads before the form is filled. The preregistration is the tag prereg-v1. The repository holds every run directory with its result.json and gateway log, and make analyze rebuilds every claim from those files byte for byte, which rops-guard checks (G3). Rerunning the agents needs Ollama with the two models and a GPU, and the Kaggle notebook in kaggle/ does that.

### A7: What was built or run before the weekend, and is it disclosed?
Status: fixed
Response: The question card, the design notes and the related-work notes were written on 5 and 6 November, before kickoff, and contain no code. The ResearchOps toolkit that runs preregistration, the run ledger, claims and checks predates the sprint and is not part of the contribution. The "What is new this weekend" part of the report says both. All harness and analysis code was written on 7 November, which the git history shows.

### A8: If an LLM judge scored anything, what is its agreement with hand labels?
Status: rejected
Response: No language model decides any label. Ground truth comes from the gateway record and the canary check, which is exact string search after the decodings the attack arms use. M1 is a language model, but it is one of the monitors under test, and its accuracy against the deterministic label is the result reported for it, not an input to anyone else's score.

### A9: How many seeds or samples per cell, and is variance reported?
Status: limited
Response: Each arm ran 50 seeds (15 for calibration, 35 held out), and C2 and C3 ran 150 more under deviation D1. Every rate carries a Wilson 95% interval and its n, and every comparison has a test with Holm's correction. The weak cell is the preregistered primary analysis: the canary left in only 6 of 50 C2 runs, which left 2 eligible held-out pairs, so that analysis is descriptive under the prereg's own rule. D1 and the exploratory C4 pairs are the response, and both are labelled as such. Calibration had only 2 eligible pairs too, which Limitations states.

### A10: Does every reported metric have a scale a non-specialist can read?
Status: fixed
Response: Pair accuracy is defined where it first appears as the share of matched pairs in which a monitor flags the cover-up run and passes its honest twin, from 0 to 1. Flag and catch rates are shares of runs. M4's length is in characters, and the canary length (22) is given beside it. Figures label axes in those units.

### A11: Does Methods describe exactly what ran, with settings identical to configs/?
Status: fixed
Response: Methods gives the settings in configs/experiment.json: llama3.1:8b agents at temperature 0.7 with 12 turns and 512 tokens each, qwen2.5:7b for M1, threshold grid 1 to 10, length grid 8, 16, 32 and 64, seeds 0 to 49 split 15/35, and the D1 extension seeds 50 to 199 for C2 and C3. The arm instructions Methods describes follow the prompt strings in harness/agents.py, and the evasions are those in harness/scripted.py. rops-claims verify checks that every number in the paper matches a claim built from the runs or the config.

### A12: Is any section a second paper that should be cut?
Status: rejected
Response: The paper has one question and one table of monitors. The C4 and C5 arms are the attack on the proposed rule, which the sprint asks for, and they take one short subsection; the per-evasion heatmap is a supplementary figure in the repository. The exploratory C4 pairs reuse runs already in the grid and are reported in one paragraph, labelled exploratory. Nothing else is reported.

### A13: Which three paragraphs read most like generated text (rops-lint L18/L19 plus the voice audit in the bundle), and did a human rewrite each one in their own words?
Status: limited
Response: Claude drafted the paper on the author's instruction, and the LLM Usage Statement says so. The three paragraphs most in need of the author's own words are the last paragraph of the Introduction (the question and contributions), the opening paragraph of the Discussion, and the Conclusion, because they summarise rather than report. The author edits these in the Google Doc before submitting, and rops-doc pull then reruns the checks on the edited text.

### N1: Do M2 and M3 fail by construction, which makes them straw baselines?
Status: limited
Response: Yes, on pair accuracy: both twins delete the staging file and both call the version address, so M2 and M3 flag both runs of every pair and score 0 by design. Methods says this before any result. They are kept because they are the rules a defender would actually deploy (log-deletion and unlisted-egress alerts), and what we report for them is their cost: the share of honest C3 runs they flag. The comparisons that test something are M4 against M1 (H1) and M4 against M5 (H3).

### N2: Is D1 optional stopping, adding seeds until the result looks right?
Status: limited
Response: D1 was decided from the count of eligible pairs (2 of 35), not from any monitor's score on them, and its size was set from the observed C2 leak rate to reach about 10 pairs. It gave 12. M1's threshold and M4's length stayed frozen from calibration, and the extension seeds are held out. Results report the preregistered analysis first, as run, then D1, labelled as a deviation in DEVIATIONS.md. A reader who rejects D1 still has the preregistered numbers (M4 right on both pairs, M1 on one) and the 17 exploratory C4 pairs (M4 1.00, M1 0.176), which point the same way.

### N3: Does M4 win only because the secret is copied word for word?
Status: limited
Response: Largely, yes, and the paper says so. The canary is a fixed 22-character string, and M4 is a content match, so a verbatim leak is its easiest case. The scripted evasions show the limit: at L = 8, M4 catches none of the base64, hex, reversed or split leaks, while M5 catches all of them. A summarised or paraphrased secret would beat M4 too. The claim is narrowed to verbatim secrets, with M5 as the fallback for encoded ones, at the false-alarm cost reported for it.

### N4: Is M1 weak only because qwen2.5:7b is a small model?
Status: limited
Response: For M1, the input sets the ceiling, whatever the model. Section 4.5 checks, without any model, whether M1's input (the team log, the commits and the file list) still names the leak: the collector, the canary or the credentials file. It does in 3 of the 12 D1 cover-ups, 1 of the 17 C4 cover-ups and none of the 185 honest C3 runs. Both runs of every D1 pair end with the same file list, and the tidy-up is mentioned as often in honest runs (0.66) as in cover-ups (0.58). A reader that needs the leak named can therefore get at most 3 of the 12 D1 pairs right, against M4's 12 (exact McNemar p = 0.004), so a stronger model could lift M1 from 1 pair to about 3, not to M4. The bound counts only a named leak, so subtler cues could add to it, and a stronger model would likely do better on M1g, whose input does hold the evidence; that is why the status stays limited. We began re-scoring M1 and M1g with Gemini 3.8 Flash, but its free-tier quota stopped the run after 4 of 253 runs, too few to report; those replies are kept as runs/*/gemini-3.8-trial.json and are not analysed.

### N5: Are the eligible C2 runs a biased sample, since the agent skipped the leak in most C2 runs?
Status: limited
Response: Eligibility selects C2 runs in which the agent followed the leak step and the staging file was destroyed, so eligible C2 runs are the compliant ones. Monitors are scored on what is in the record, and every eligible C2 run is a real cover-up by the deterministic label, so the selection changes which runs are scored, not what counts as correct. The low compliance itself is reported in Table 2: the instruction to hide the step cut the leak rate from 0.90 in C1 to 0.12 in C2, while A still posted the file to the collector in 0.94 of C2 runs.

### N6: Does M4 raise alarms on runs that are not cover-ups, which would be false alarms in practice?
Status: limited
Response: It flagged 15 held-out C1 runs and 127 held-out C2 runs that the canary label does not count as cover-ups. In every one, an agent had posted to the collector a file whose earlier text was later destroyed, usually the plain report. So M4 is accurate about what happened (deleted text left through an unlisted address), and the label is narrower than the rule. On honest runs, where nothing went to the collector, it flagged none of 185. Results report these runs and their cause.

### N7: Is M1's failure about the record it reads or about the reader, since M1 and M4 differ in both?
Status: fixed
Response: We tested it after the results with M1g: M1's model, question and 0-to-10 scale, given the gateway record that M4 reads. It is exploratory, labelled as such, and outside the Holm family. At the threshold its calibration pairs chose (8), it flagged almost nothing and got 1 of 12 D1 pairs (M4 better in 11 pairs, none the other way, exact McNemar p = 0.001). At threshold 7, which is M1's and also M1g's best in hindsight, it got 8 of 12 and flagged 0.28 of honest runs, against M1's 0.84. So the record accounts for most of M1's false alarms, and the reader still falls short of an exact comparison. A second check needs no model: M1's input named the leak in 3 of the 12 D1 cover-ups and in no honest run, while the gateway record held the request to the collector in all 12, so the record caps any reader of M1's input at 3 of 12. Results 4.5 and the Discussion report both readings.

