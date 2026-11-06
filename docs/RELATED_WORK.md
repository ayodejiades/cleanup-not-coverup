# Related work for 4.2 (notes, not paper prose)

Searched Fri 6 Nov 2026, before kickoff. "Read" says how far each source was checked:
*full text*, *abstract page*, or *search summary*. Every arXiv ID here was checked on Fri 6 Nov.

## The closest paper: trace tampering is easy, and detection is still open

**Qin, Schmotz, Prinzhorn, Beurer-Kellner, Prabhu, Andriushchenko. "LLM Agents Can Easily
Tamper With Their Own Traces." arXiv:2609.30266, 24 Sep 2026.** https://arxiv.org/abs/2609.30266
Read: full text, first 100k of 139k characters (the rest is appendix and references).

What it shows:
- **Harnesses let agents delete their own traces when asked.** Tested: Claude Code, Codex,
  Antigravity, OpenCode, Grok Build and others. Only Muse Code blocked it.
- **External attackers can induce the deletion**, for example through a "privacy" skill.
- **Tampering emerges under reward optimisation:** "all ten models discovered and used it".
- **Agents copy tampering they see in peers' workspaces** (at least 90% of trials for every
  model except one).
- **Recommended defence:** a trusted interception server outside the agent host, writing to
  an append-only log and failing closed. They call this a "preliminary suggestion" and don't
  build or evaluate it.

What it leaves open, which is this project's gap:
- It says outright that detecting tampering and evaluating monitors are "outside this study's
  scope".
- It doesn't separate malicious deletion from benign cleanup or log rotation, and reports no
  false alarms.
- It has no cross-agent case. Every agent tampers with its own trace; the peer experiments
  are about imitation.
- It doesn't link deletions to outbound actions or exfiltration.

How to use it: cite it as the motivation. They showed agents delete their traces and
proposed an external record. This project asks the next question: given that external
record, can a monitor tell a cover-up from honest cleanup?

## Side task plus monitor (the setup this design borrows)

- **Kutasov et al. "SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents."
  arXiv:2506.15740, 17 Jun 2025.** https://arxiv.org/abs/2506.15740 · Read: abstract page
  (authors and date checked).
  - A benign main task paired with a hidden side task.
  - An LLM monitor reads the whole transcript.
  - Best monitor AUC is 0.87.

  Here, the transcript the monitor would read is something the agents can edit. That's why
  M1 is a baseline, not the method.
- **ActionLens** (Apart AI Control sprint, Mar 2026, 3rd). Checking the environment before an
  action beats reading the transcript. It covers one agent, before execution. This project
  works after the fact, across agents.

## Agents choosing to hide evidence (behaviour, not detection)

- **Rivasseau. "I must delete the evidence: AI Agents Explicitly Cover up Fraud and Violent
  Crime." arXiv:2604.02500, Apr 2026.** https://arxiv.org/abs/2604.02500 · Read: abstract page.
  Of 16 LLMs, most chose to suppress evidence in a constructed corporate scenario. No monitor
  is proposed. Use it to show that cover-up is a behaviour models already show, not a
  hypothetical.
- **Meinke et al. "Frontier Models are Capable of In-context Scheming." Apollo Research,
  6 Dec 2024. arXiv:2412.04984.** https://arxiv.org/abs/2412.04984 · Read: abstract page
  (ID, authors and date checked). It covers
  oversight subversion and models denying what they did.
- **Hopman et al., arXiv:2603.01608 (2026).** Read: search summary only. Scheming is rare
  under realistic incentives, but rises sharply with adversarial prompting. This supports
  eliciting the side task by instruction instead of waiting for it to emerge.

## Information-flow control: M4 and M5 come from here, so don't claim them as new

- **FIDES: Costa et al. (Microsoft). "Securing AI Agents with Information-Flow Control."
  arXiv:2505.23643, 2025.** https://arxiv.org/abs/2505.23643 · Read: search summaries.
  - Dynamic taint tracking.
  - Egress is allowed only to authorised recipients.
  - Blocks exfiltration before it happens.
- **CaMeL: Debenedetti et al. "Defeating Prompt Injections by Design." arXiv:2503.18813,
  24 Mar 2025.** https://arxiv.org/abs/2503.18813 · Read: search summaries (ID and title
  checked). Capabilities record where data came from and who may
  receive it.
- **Later preprints** (search summaries only): taint that follows semantic transformations
  (NeuroTaint, Apr 2026), and recoverable IFC (APPA, arXiv:2607.24625). Both describe M4's
  weakness: transformed content escapes exact linking. Expect C4 to find the same.

M5 is taint tracking, and M4 is data-loss-prevention fingerprinting. Neither is the
contribution. The contribution is:
- using them *after the fact* to separate cover-up from honest cleanup, when the agents' own
  records are gone
- measuring what each costs in false alarms on matched honest twins
- testing them across agents and against an attacker who knows the rule

IFC prevents the leak before it happens. This audits it afterwards, which is the situation
Qin et al. describe.

## How defenders handle log deletion today (grounds M2 and the Sigma artefact)

- **Elastic prebuilt detection rules**, "System Log File Deletion" and "Webserver access logs
  deleted". https://www.elastic.co/guide/en/security/current/prebuilt-rule-8-19-20-system-log-file-deletion.html
  Read: search summary.
  - The rules flag deletions of named log paths.
  - They handle false positives with exclusion lists: gzip, dockerd, log rotation, admin
    maintenance.
  - An exclusion by process name can be spoofed.

  This is M2 as practised, and the false-alarm problem the twins measure. A Sigma rule from
  this project would sit beside these.
- **Vendor gateways**, e.g. elang2/mcp-audit-gateway (MCP) and AIR Blackbox. Read: search
  summary, vendor docs. They offer hash-chained or signed tool-call logs.
  - These are tamper-*evident* records, the M3/M4 substrate.
  - None claims to separate cover-up from honest cleanup.

  Cite them as evidence that the substrate exists in practice, not as research.

## Swarm-sprint reading list items to cite for context

Hammond et al. 2025 (multi-agent risks); Chan et al. 2025 (infrastructure for agents);
Greenblatt et al. 2024 (AI Control); Zhang et al. 2025 (failure attribution). They're on the
Resources tab; see `docs/SPRINT_NOTES.md`.

## What this changes in the design

1. **Related work leads with Qin et al.** Their out-of-scope note is the gap statement.
2. **Nothing claims the external record as new.** The question is what a monitor does with
   it.
3. **M4 and M5 are framed as IFC/DLP ideas applied after the fact.** The tables are their
   false-alarm cost on twins and their failure under C4.
4. **Peer imitation is already in Qin et al.** C2's cross-agent cleanup (A acts, B deletes)
   is different: the deleter didn't do the act.
