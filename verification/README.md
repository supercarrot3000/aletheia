# Verification

The local verifier reads the indexed Markdown and JSON corpus, checks typed references and argument dependency cycles, runs trusted regression fixtures, and checks each encoded argument. JSON keys must be unique and indexed paths must stay within the corpus. Argument dependency edges give context and guide packet retrieval. Formal entailment uses the formulas of the argument's explicit premise references.

The standard-library reference checker exhaustively enumerates assignments for `var`, `not`, `and` and `implies`, up to 16 variables. It distinguishes a countermodel, entailment with satisfiable premises, and inconsistent premises. Exceeding the bound fails replay. A countermodel gives a concrete valuation that satisfies every premise and falsifies the conclusion.

For the simplicity bridge control, the verifier renders the exact encoded proposition in Lean's `Prop`, checks a core Lean proof against it, and requires an empty axiom ledger. The argument records spell out the encoding and assumptions. The Lean proof and the propositional countermodel concern the chosen encoding. The receipt keeps semantic review pending. For the trust boundary and command line, see the [runner handoff](../runner/README.md).

Run the structural, regression and targeted mutation tests with Python, or add the environment variable to include the Lean integration tests.

```sh
python3 -B -m unittest discover -s verification/tests -v
ALETHEIA_TEST_LEAN=1 python3 -B -m unittest discover -s verification/tests -v
```

The draft GitHub workflow exercises the Python suite in the proposed tree. The independent local replay uses a separately retained baseline. Hosted enforcement is a later stage.

## Optional finite-model experiment

The [identity-collapse investigation](../corpus/investigations/simplicity-identity.md) uses a pinned Z3 version for finite first-order model search. It has its own replay command and regressions. The regular verifier and Lean proof remain independent of that installation.

## Mathlib grouping theorem

Use the pinned Lean toolchain and the checked-in Lake manifest. From the repository root:

```sh
cd verification/mathlib
lake exe cache get Mathlib.Order.Setoid.Basic
lake env lean AletheiaQuotient.lean
```

The replay prints the axiom ledger for the general theorem, the obstruction, and both catalogue examples. Mathlib supplies the kernel equivalence relation and product quotient construction. [Finding and transfer cases](../docs/research/findings.md#when-does-grouping-preserve-a-relationship)

## Isabelle/HOL and Nitpick

The modal investigation includes a published reference problem and a separate research question. It explains the exact domains, proof obligations and countermodel expectations. [Install and replay](../corpus/investigations/modal-creation.md#replay)
