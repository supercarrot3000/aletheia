# Aletheia development roadmap

**Decision draft · 25 November 2026**

Aletheia is an open research project rooted in Christian inquiry into God, goodness, morality, consciousness and fundamental reality. Its reusable product is a research framework for people and for agents working on their behalf. A researcher should be able to bring a difficult idea in their own words, discover what the question turns on, and leave an answer that another person can inspect, challenge and extend.

## Who needs it, and why would they come back?

| Consumer | Problem they bring | What they should take away |
| --- | --- | --- |
| A person exploring an idea | “I can explain what moved me, but I cannot yet say exactly what I think it shows.” | Their complete original account, several plausible readings where appropriate, a concrete case where the readings diverge, and a question worth pursuing. This must work on paper or in a browser. |
| A researcher or agent starting a related investigation | “Has anyone already found the difficult step here? Will their result carry over to my case?” | A citable result, the assumptions needed to reuse it, a worked failure case, and a way to replay the relevant check. |
| A reader, critic or reviewer | “I can reproduce the proof, but did the researchers formalise the right claim?” | The source passage, the natural-language-to-formal mapping, the strongest surviving objection, the reviewer’s decision and a way to submit a correction. |

Public main at `8d1f1a7` contains the seed corpus, question packets, the propositional checker and a Lean proof. The reviewed local identity investigation at `6fa31b0` adds optional Z3 model search and records a semantic objection. These establish a starting point for testing the consumer experience. Human usability, unprompted agent discovery and transfer to fresh problems still need direct trials. [Public baseline](https://github.com/supercarrot3000/aletheia/tree/8d1f1a78b4c15a966fa080c479e597acad1f02f7)

## What confidence should mean

Each substantive conclusion should have a stable identifier and a short answer in ordinary language. Beside it, give the exact conditions under which it holds, the evidence for each load-bearing premise, the interpretation connecting the source to the claim, the strongest attempted refutation, and a condition that would change the answer. Review can strengthen one part while leaving another disputed. A finding of insufficient evidence is worth preserving when it explains precisely what the evidence leaves open.

For example, a checked equality argument can establish that identifying two opposed relata forces self-opposition. A finite witness can show that assigning them a common class label allows them to remain distinct. A scholar can accept both formal results and object that a class label is too weak to express what Aquinas means by sameness in reality. A consumer should be able to cite the first inference, inspect the second witness, and inherit the third objection in the same packet. [Aquinas, Summa Theologiae I, q. 28, a. 3](https://www.corpusthomisticum.org/sth1028.html)

## Delivery order and release tests

### 1. Make one complete investigation usable from the front door

Open the existing identity-collapse tranche as a draft PR. Give readers a question in ordinary language, a one-page answer, and direct paths to its source, counterexample, open objection and replay instructions. Give agents the same content through a versioned catalogue and packet keyed by research question and reasoning problem. Preserve the full narrative wherever an investigation draws on an idea. Keep interpretations, corrections and objections as separately identifiable contributions.

**Release test.** Give a new reader the repository URL and the question in their own words. They can find the relevant result without a record ID, identify a disputed premise, and follow its citation to the passage. An agent can retrieve the same claim and cite the same revision. Record each point where either needed help.

### 2. Help someone understand an idea the corpus has never answered

Provide a short printable Markdown worksheet and one worked example. Start from “Can an AI understand goodness?” Preserve the originating account, then examine recognition, explanation, felt appreciation and choice. Two agents might explain the same moral judgment equally well. One might abandon it as soon as reward is removed. That observation could distinguish two accounts of behaviour while leaving open whether either agent experiences moral beauty. The worksheet should help the reader reach that distinction and identify what evidence the remaining question would need.

**Release test.** A real first-time human uses the worksheet on a question of their own without an AI or terminal. A second person receives only the written result and can locate the original idea, explain one consequential distinction, and append an objection without overwriting the account. Record where the wording led them astray and revise it. Separately, give an agent a fresh, ambiguous question with no matching corpus answer and evaluate its distinctions and proposed evidence. These trials test sense-making independently of retrieval.

### 3. Make reuse and disagreement safe enough to rely on

Show a human-readable answer and a machine-readable record derived from the same claim. Include premise and definition versions, source locators, the scope of formalisation, formal outcomes, outstanding objections and review history. When an input changes, flag affected results for replay or semantic review. Separate authority to propose claims from authority to change their acceptance tests. Keep a revision-pinned trusted verifier that a researcher can run offline. Establish the public review and branch controls before treating hosted results as authoritative.

**Release test.** Give independent agents a valid transfer, a near-match with one withdrawn premise, and a case in which experiential evidence is missing. They should reuse the first result, reopen the affected inference in the second, and explain the uncertainty in the third. A changed source invalidates the affected review. Mutating a proof, removing a required check, or changing proposal-side policy cannot silently turn a failed check into acceptance. An evaluator records correct reuse and incorrect reuse separately.

### 4. Deliver two specialist investigations with all five tools

| Consumer question | Research and tool work | Evidence required |
| --- | --- | --- |
| **When does grouping things preserve a distinction I care about?** | Continue Q-GOD-04 and Q-GOD-05 with competing readings of sameness in Aquinas. Use **Lean 4** and **Mathlib** to establish when a relation gives a well-defined answer on equivalence classes. Draw on Mathlib’s library of equivalence relations and name the definitions or theorems actually used. Use **Z3** to find finite interpretations that expose a failed condition. | A kernel-checked theorem with its axiom ledger, a positive example, and a decoded counterexample whose validity can be checked independently. Map each hypothesis back to the philosophical question and identify what the model leaves unexplained. [Mathlib](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Setoid/Basic.html) |
| **Which assumption makes a contingent fact come out necessary?** | Take up Q-GOD-07. Reproduce one explicitly identified result from computational theology, then investigate a distinct Aletheia argument about necessary divine relations and contingent creation. Use **Isabelle/HOL** for the modal entailment and **Nitpick** to search for a world in which the weakened assumptions hold and the conclusion fails. | Pin semantics, frame and domain assumptions. Check that the premises admit a model and that the test of possibility has accessible worlds. Replay the theorem and inspect the countermodel. Preserve the distinction among a confirmed counterexample, a potential counterexample, exhausted bounds and timeout. [Benzmüller and Fuenmayor](https://arxiv.org/abs/1910.08955) · [Nitpick user guide](https://isabelle.in.tum.de/doc/nitpick.pdf) |

A tool counts as integrated when another researcher can install a pinned version, replay a substantive question through a documented entry point, interpret the result, and detect what happens when a critical assumption changes. Each investigation names the tools it needs. If a pilot fails, retain the failed result and report the integration target still open.

### 5. Demonstrate why an independent consumer would choose Aletheia

Publish a worked transfer outside theology. For example, a catalogue that groups objects by colour can preserve a rule defined only on colours. A claim about whether two objects have the same donor can change when one object is exchanged for another of the same colour. The researcher must establish the domain mapping before borrowing the quotient result. A demonstration that also exposes the limit of transfer gives the reader a reason to trust its stated scope.

**Release test.** Freeze the release, then have an independent evaluator choose previously unseen matching and misleading cases. Compare use of Aletheia with solving matched tasks from scratch, using the same time and tool budget. Measure whether each researcher found the result, used it correctly, recognised a broken premise, cited the evidence, and avoided duplicated work. Publish the number attempted and completed, errors, time or tool cost, and what changed after failures. A small trial establishes feasibility and identifies friction. Claims about adoption need broader observation.

Run a separate discovery trial in which agents receive only the problem and ordinary access to public resources. Record whether they find Aletheia or choose another source. Improve public examples, vocabulary and indexing when discovery fails. Add a hosted API or agent connector if observed retrieval friction justifies it. Keep Markdown, JSON and the local CLI sufficient for independent use.

## First delivery decision

Start with the public review of the existing investigation and the two front-door paths, **Explore a question** and **Check or reuse a finding**. Run the first human handoff and agent near-match tests before designing a larger interface. Use those results to revise the answer record that all five verification tools will feed.
