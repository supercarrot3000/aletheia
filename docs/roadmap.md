# Audit and implementation roadmap

## Starting state

The supplied directory was a plain tree without Git metadata. All four starter tests passed under Python 3.12.3. Seven fixture cases covered reversal, missing premises, an added bridge, contradictory premises and a valid control. The checker correctly tests premise satisfiability separately from entailment. Keep it as a small exhaustive reference implementation.

The starter tests check identity uniqueness and selected file and reference links. An existing ID of the wrong type can satisfy a claim reference, and file checks do not confine indexed paths. Definitions and premises are absent as explicit data. The fixture verdicts can drift from claim prose, and the runner does not produce a repeatable input or record. The proposed CI runs the same tree that supplies the acceptance tests. It is a useful regression check and gives no independent authority when a proposal can change it.

The corpus's strongest properties are preserved narrative, explicit provisional status, rival hypotheses and conditions for revision. Its claim provenance and warrant granularity vary. Treat even a correctly checked toy argument as a question about the representation until its mapping has independent review. In particular, a Boolean valuation of three symbols cannot answer whether the corresponding state is metaphysically possible.

## 1. Local research and verification

Deliver the [milestone specification](../specs/20261125-replayable-research/spec.md). Use a canonical corpus file for the first typed argument family, an offline packet and receipts. Reuse the exhaustive checker for a small model and Lean core for the bridge entailment. Freeze the verified exemplar and Purple Man attribution in independent replay. Accept when the seed, both expected formal outcomes, targeted mutations, candidate isolation and replay all exercise their local entry points.


Local verification on 25 November 2026 passed all 16 tests with Lean 4.35.0 enabled. The gap witness assigns true to simplicity and relational distinction and false to composition. The added bridge gives a Lean theorem with an empty axiom ledger. Tests also exercise stale replay, candidate-side policy substitution, altered controls, malformed inputs, a reversed implication implementation and a Lean proof placeholder. The three Purple Man artifacts match their starting hashes. Semantic review of the encoding remains open.

## 2. Independent review and provenance

Add migrated stable source anchors, versioned definitions, profile-aware premise provenance and structured objections across the corpus. Add claim-specific human review records for semantic fidelity, evidence, rival interpretations and reversal conditions. Retain withdrawn hypotheses and negative findings. Accept when a reader can follow a source-to-claim chain without private records, an edited definition identifies results that need replay, and an unresolved objection prevents the corresponding review dimension from being promoted.

In a reviewed Git repository, run required checks from a protected verifier revision and gate-owned execution environment. Give the proposer write access to proposals and give a separate role control of policy, protected tests and review records. Accept when changing candidate verifier files, fixtures or required statuses cannot change the acceptance decision and CI records the exact protected revision. Test this before relying on merge enforcement.

## 3. Specialist verification pilots

- Z3 for a bounded first-order or arithmetic exercise beyond the current checker. Pin the solver and timeout, query premise satisfiability independently of premises plus negated conclusion, save the query and verify concrete models with an independent evaluator where feasible. Accept only with known valid, refutable, inconsistent and unknown controls that remain distinguishable. Treat an SMT unsatisfiability result as solver evidence within the declared logic and resource policy.
- Lean and Mathlib for a focused argument that benefits from a maintained mathematical library. Pin toolchain and dependencies, check the exact theorem type and transitive axiom ledger, and test that placeholders and changed statements fail the independent gate. Select Mathlib imports by theorem requirements.
- Isabelle/HOL with Nitpick for a modal or higher-order pilot. First reproduce a published computational theology example, subject to upstream terms, then encode one Aletheia comparison with explicit frame conditions and quantifier semantics. Accept when a known finite model, a bounded no-model result, a timeout and a kernel-checked theorem are saved as distinct outcomes with bounds and provenance. Treat each translation as a separate semantic review obligation.

Prefer upstream libraries and interchange standards within each logic. Benchmark detection, false rejections, unknown outcomes and cost on reviewed controls. Require held-out adversarial mutations for changed automation in addition to transparent regression cases.

## 4. Repeatable research and publication review

Extend packets into versioned tranche proposals, attempt logs, countermodel artifacts, review decisions and receipt histories. Keep model interaction behind a provider-neutral interface. Accept when two independent operators can generate the same research inputs offline, submit their proposals with different tools, and reproduce formal checks for the same pinned inputs. Record model-generated outputs as research artifacts and preserve all reviewed objections and failures.

The initial publication uses MIT for software and CC BY 4.0 for original corpus material, including the contributor's recollection. Preserve provenance and third-party rights when reviewing future additions. Continue the Purple Man identification as an open provenance question.
