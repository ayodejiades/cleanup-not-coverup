# Sprint notes: Swarm Alignment Hackathon

Read from every tab of https://apartresearch.com/sprints/swarm-alignment-2026 (Overview,
Resources, Guidelines, Schedule), the report template and the prize terms, on Thu 5 Nov 2026.
Paraphrased; the page is the source of truth.

## Rules that change what you do

- **Abstract 150–250 words.** Both the Guidelines and the template say so. `.rops/sprint.json`
  has `abstract_max_words: 250`. Intake had defaulted to 150.
- **8 pages max, not counting references and appendices.** The template recommends about 4.
- **Required appendix: "Limitations and Dual-Use / Ethical Considerations".** The template does
  not have this section. Add it yourself. It must say what the result does not establish, and
  any way the setup or findings could make multi-agent operations easier to run or harder to
  detect.
- **The template's sections:** Introduction (with a contributions list), Related Work, Methods,
  Results, Discussion and Limitations (with Future Work), Conclusion, Code and Data, Author
  Contributions, References, Appendix, LLM Usage Statement. The template asks that the final
  version be written mainly by the team.
- **AI use is allowed.** Made-up results or references can disqualify a project. A judge can
  decline to score a report that is too unclear to follow.
- **Prior work** is allowed, but only the weekend's work is judged, and every submission is
  screened for prior work. Mark any code written before the sprint as preexisting, in both the
  README and the report. This applies to `traceturn` and to the Collusion harness.
- **Resubmitting:** submit again with the same title before the deadline. Up to two projects per
  person.
- **Projects stay hidden until after judging** (infohazard policy). The confirmation email is
  your receipt, so check that it carries the right PDF.
- **Prize terms:** the terms page says 30% is withheld for citizens of countries with no US tax
  treaty. It doesn't name Nigeria. That Nigeria has no such treaty is from general knowledge,
  not the page, so check it on the IRS treaty list linked from the terms. Prizes are paid by
  SWIFT transfer, and the prize form is due within a week of being sent.

## Times (Lagos, UTC+1)

| When | What |
|---|---|
| Thu 5 Nov 23:00 | Talk: Grant Fleming (AE Studio), "Novel Risks From Adversarially Optimized Agent Swarms" |
| Already recorded | Adaption workshop; John Kitaoka (MATS / UK AISI), "Open Problems in Securing Systems Against AI Agent Swarms" |
| Fri 6 Nov 13:00 | Sprint opens (00:00 AoE). Don't run planned conditions before this |
| Fri 6 Nov 14:30 | Logistics talk |
| Fri 6 Nov 18:00 | H0 in `docs/HOURS.md` |
| Fri 6 Nov 20:00 | Rowan Howard-Jones, "To Catch a Swarm" |
| Fri 6 Nov 21:15 | Elias Stengel-Eskin, "The Emergence of Agent Languages" |
| Fri 6 Nov 22:30 | Kickoff keynote, Judd Rosenblatt; logistics talk at 23:30 |
| Sat 7 Nov 14:00 | Justin Shenk (also a judge), "Modeling Agent Swarms: A Field Guide" |
| Sat 7 Nov 20:00 | Jurgis Kemeklis, "Mitigating Insider Threats from AIs with AI Control" |
| **Mon 9 Nov 12:59** | **Deadline** (Sun 8 Nov 23:59 AoE) |

## Data and tools named on the page

- METR / Redwood investigation of the Hugging Face incident: metr.org/hugging-face-incident-report-aug-2026.pdf
- Swarm Traces: swarmtraces.org (a redacted dataset of 80,000+ reconstructed attack payloads)
- AI Village transcripts: huggingface.co/datasets/aidigestorg/ai-village (traceturn already parses these)
- Transluce agent activity logs: transluce.org/agent-activity
- swarms.wiki: a directory of datasets, environments and incident trackers
- Concordia (google-deepmind/concordia): the only starter repo. `Ajay150313/agentsre`, which
  intake also picked up, is a judge's own library, so I removed it from `starter_repos`.
- Earlier Apart multi-agent sprints: the Multi-Agent Safety Hackathon (2024) and the
  Multi-Agent Security Research Sprint (Feb 2024).

## Reading list per track (Resources tab)

- **General:** Hammond et al. 2025 (multi-agent risks); Tomašev et al. 2025 (distributional AGI
  safety); Chan et al. 2025 (infrastructure for agents); Dafoe et al. 2020; Conitzer & Oesterheld 2023.
- **Track 1:** Park et al. 2023; Akata et al. 2025; Gandhi et al. 2023; CRUX (Kapoor et al. 2026); GovSim (Piatti et al. 2024).
- **Track 2:** Prompt Infection (Lee & Tiwari 2024); task splitting to evade filters (Jones et al.
  2025); coordination to resist shutdown (Agrawal et al. 2026); Tilli 2026; Jørgensen et al. 2025.
- **Track 3:** A2A (Google 2025); IDs for AI systems (Chan et al. 2024); Kirchenbauer et al. 2023;
  Sun et al. 2023; Haupt et al. 2022; Tennenholtz 2004.
- **Track 4:** Secret Collusion (Motwani et al. 2024); multi-agent interpretability for collusion
  (Rose et al. 2026); AI Control (Greenblatt et al. 2024); failure attribution (Zhang et al. 2025);
  Riedl 2026; CaMeLs (Foerster et al. 2026).

## Example projects the organisers suggest, mapped to the questions

The organisers suggested these, so expect other teams to run them. A suggested project is a
crowding risk, not a novelty signal.

| Q | Suggested example (paraphrased) |
|---|---|
| 1.1 | Red-team agents try to escape a no-internet sandbox; close what works; publish a checklist. Also: do read-only allowlists combine into writes? Do agents build covert channels unprompted? |
| 1.2 | Ten agents from three "companies" share one paid API on a fixed budget; seeded rerun script |
| 1.3 | The same scenario on a frontier model and on 2–3 small ones; find where outcomes stop matching |
| 2.1 | 20–50 agents with an unannounced shared folder: do they find it, talk, and split up work? |
| 2.2 | Split a refused task into harmless pieces across a pipeline. "Refusal shopping": a coordinator asks a second worker after the first refuses |
| 2.3 | One compromised agent in chain, star and fully connected networks. A shared-memory benchmark comparing source attribution with independent verification. Spread of selfish behaviour |
| 2.4 | N copies with a majority vote, a fraction compromised: does redundancy help, or do copies fail together? |
| 3.1 | Compare ID schemes for agents that rename themselves. Identity and audit trail moved to the gateway |
| 3.2 | A2A attacks (impersonation, overstated permissions) and one fix. Enforcement inside vs outside the protocol. Privilege escalation through delegation |
| 3.3 | A reputation system attacked by a ring of agents rating each other up. A whistleblower channel attacked with false reports |
| 3.4 | Strategy-proof mechanisms. A swarm runtime with Lean-typed messages |
| 4.1 | Forensics on Swarm Traces (who talked to whom, how information spread, could it have been flagged early). A monitor that sees only network egress and tool calls |
| 4.2 | (No direct example.) Close: the gateway-side audit trail (3.1). "Did it actually happen?": check each worker's "done" claim against the database before the next worker acts |
| 4.3 | **"Catch the cartel"**: two pricing agents that can talk; some runs told to collude; a monitor sees only a sample of messages and prices. Also: a sanctioned, logged channel as a control for covert ones |
| 4.4 | Replicas as a monitor; copies colluding with no channel (Schelling points); split-up attacks; research sabotage split across commits; approval laundering; can a swarm recruit its monitor? |
| Track 4 | "Whose fault was it?": plant a worker, reference or grader error; does a diagnostic name the source, say "insufficient evidence" when it should, and avoid blaming anyone in runs with nothing planted? |

## Crowding check (past entries)

The two earlier multi-agent sprints don't publish their projects ("Projects from this Sprint
are not published on the site"), so the only past entries available are the first 200 from
the AI Collusion sprint (23–25 Oct 2026), fetched into `~/researchops/corpus/`. No placements
are out yet. The "Prior entries" column in `IDEAS.md` counts any entry sharing two keywords
with the question. On a corpus that is all about collusion, that matches almost everything,
so I counted with topic phrases instead:

| Topic | Entries (of 200) |
|---|---|
| 4.3 partial-view, covert-channel or steganography monitor | 4, including "Evaluating Partial Message Monitoring of LLM Trading Agents", which is close to 4.3 itself |
| Any LLM collusion monitor (4.3 / 4.4) | 56 |
| 4.4 control protocols, trusted vs untrusted | 2 (the 2026 AI Control Hackathon wasn't fetched) |
| 4.2 tampered, deleted or spoofed logs | **0** |
| 4.1 forensics on real logs | 2 (the AI Swarm Dynamics Hackathon, where traceturn came from, is not on Apart and wasn't fetched) |
| 2.3 spread from a compromised agent | 4 |
| 2.2 task splitting past refusals | 2 |
| 1.1 sandbox escape or containment | 5 |
| 3.x identity, reputation, protocol | 7 |

## Overlap with your own past work (disclose any you build on)

- **4.3 "Catch the cartel"** is close to your Collusion entry (*Parallel conduct is not
  agreement*, 23–25 Oct): the same double auction, detectors, and no-channel decoys. Reusing
  that harness lowers setup risk. Only a partial-view monitor would be new this weekend.
- **4.1 on AI Village** is what `traceturn` already does. The new part would have to be
  Swarm Traces data or a new method.
- **"Did it actually happen?" and "Whose fault was it?"** fit traceturn's claim-versus-observation
  logic and your decoy and false-positive habits, without reusing its code.
