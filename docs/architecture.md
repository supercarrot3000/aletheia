# Architecture and public corpus contract

## Canonical knowledge

Git-tracked UTF-8 Markdown and JSON are the initial source of truth. Assign stable public IDs independent of filenames. Ideas retain their full available narrative, author/attribution where consented, date or date range, provenance, corrections, related questions, and access/rights status. Never confuse a source narrative with facts that it purports to establish. Store new interpretations as separate records that reference idea IDs and precise sections. Corrections append or supersede with explicit history; do not silently rewrite. Keep public citations or source locators; never include private system URLs or IDs. A generated local search index or SQLite graph is disposable and rebuilt from Git.

Record types: idea, source, question, definition, premise, claim, argument, objection, countermodel, proof, test, tranche and receipt. Each argument lists its exact dependencies and inference rule or warrant. Each claim has epistemic type, status, scope/profile, provenance, objections and reversal conditions. Source records distinguish primary text, paraphrase and interpretation, licence and provenance. For Scripture keep exact reference, translation/edition, context and disputed readings; no unauthorised translation dumps. A proof carries a statement-to-formula mapping and the logic/axiom ledger. A receipt binds hashes of input revision, definitions, sources, policy, solver version and tests. Verification is a vector, not a truth score.

## Tranche workflow

1. Select a question, freeze inputs and declare the applicable profile and alternative premises.
2. Retrieve related ideas, arguments, objections, prior tests and sources; distinguish cross-domain analogies from evidence.
3. Propose claims and arguments in a branch; retain competing accounts and failures.
4. Check structural/provenance constraints and formal statements; reject circular support, missing bridge premises, inconsistencies and stale receipts. Search for countermodels; a bounded search with none is not a proof.
5. Independently check semantic fidelity, scriptural context, evidence quality and defeaters. Use different reviewer context/provider when feasible; agreement alone is not evidence.
6. Publish a tranche report and dimension-specific receipts. A PR can preserve an unresolved hypothesis, but must not falsely promote it as verified.
7. Add discovered errors as regression candidates, separately reviewed. Reverify dependent claims after premise/definition/source changes.

## Verification roadmap

Start with deterministic corpus lint, reference and dependency checks, propositional countermodels and receipt hashes. Next add source anchors, logic-specific proof adapters (Lean, Isabelle/HOL and Nitpick, SMT where appropriate), independent formalisation review, provenance audit, held-out mutation tests and a provider-neutral runner. Do not attempt to encode all theology into a single logic. Benchmark detection, false rejection, unknown outcomes and cost. Do not allow research agents to alter protected gate policy in their own acceptance run.

## Public project governance

The theological starting profile can be explicitly Christian and Scripture-grounded; alternate interpretations and non-theistic comparison models remain legitimate objects of investigation. A contributor need not personally affirm any profile to investigate its entailments. Neither the maintainer nor an AI is exempt from evidential scrutiny. The software uses MIT and the original corpus and prose use CC BY 4.0. Third-party works retain their existing rights. See the [licensing guide](../LICENSING.md).

## Implemented local milestone

The schema-version-one index links the Markdown documents and JSON collections. [The formal collection](../corpus/arguments.json) adds typed profiles, definitions, premises, objections and arguments for the divine-simplicity comparison. The existing claims and questions stay in their original collections. A formal argument points to a research claim and question, and its encoded conclusion may be a conjecture under challenge. `depends_on` records research context, while only `premise_refs` supply assumptions to the checker. Keep the semantic mapping, hypotheses and competing accounts in the corpus.

[Local commands](../runner/README.md) provide readable record lookup, deterministic question packets, and independent replay against a trusted copy. Receipts identify indexed and protected input files by SHA-256 and bind the trusted verifier files, fixture outcomes, argument results and Lean toolchain. They are reproducibility artifacts. A trusted copy must be retained separately to establish policy authority. These hashes cover the local input surface and do not represent a full Git tree, toolchain binary attestation or an independent approval signature.

The [roadmap](roadmap.md) records the original audit, the first milestone's acceptance criteria and the remaining work. In particular, the Python hosted workflow remains a same-tree regression check pending protected-branch integration.
