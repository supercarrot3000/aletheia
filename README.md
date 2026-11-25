# Aletheia

Aletheia investigates the nature of God, goodness, morality, consciousness and fundamental reality. It grew out of Christian inquiry about the character of God and how human and artificial intelligence might come to understand goodness. Its purpose is to discover what is true. That includes finding errors in its own arguments, testing rival explanations and preserving questions that remain unresolved.

People and AI agents can inherit the same material, recover how a conclusion was reached and challenge the steps for themselves. Aletheia welcomes scrutiny from any philosophical or religious starting point. A proof establishes what follows from its stated assumptions in its chosen logic. Assessing the truth of those assumptions, the fidelity of a theological interpretation and the character of lived experience requires other kinds of inquiry.

## Explore a question or check a finding

- Work through a difficult idea on paper or in a browser. The worksheet helps you preserve the original account, compare plausible readings and find where they lead to different answers. [Explore a question](docs/research/explore.md)
- Find a conclusion, its assumptions, its evidence and the objection it leaves open. [Check or reuse a finding](docs/research/findings.md) · [Machine-readable catalogue](docs/research/findings.json)
- Start with identity collapse. Two things that are each literally identical to the same thing are identical to each other. A finite model shows how two opposed things can share a class label. Whether that captures Aquinas’s account of shared essence remains open. [Identity investigation](corpus/investigations/simplicity-identity.md)

The research checks include a theorem about when grouping preserves a relationship and a modal investigation about when necessary relations would make creation necessary. [Verification and replay](verification/README.md)

## Research programmes

- [The Purple Man and Alice Springs](corpus/ideas/purple-man.md) preserves the full available recollection and the contributor's clarifications. The original playwright’s identity remains open, and their work helped inspire this project. [Provenance record](corpus/sources/purple-man-origin.json) · [Acknowledgement](ACKNOWLEDGEMENTS.md)
- [Nature of God and fundamental reality](corpus/programmes/nature-of-god.md) introduces the divine-simplicity question. The local demonstration tests whether excluding composition also excludes real relational distinction.
- [Moral True North](corpus/programmes/moral-true-north.md), [Moral beauty](corpus/programmes/moral-beauty.md) and [Moral discovery](corpus/programmes/moral-discovery.md) record hypotheses, competing readings and questions for further work.

## Run locally

Use Python 3.10 or newer. For formal replay, install Elan and the Lean version pinned in [lean-toolchain](lean-toolchain). Once the toolchain is installed, the commands need no service or model credentials.

```sh
python3 -IB aletheia.py show IDEA-001
python3 -IB aletheia.py packet Q-GOD-03 > question.json
python3 -IB aletheia.py verify > receipt.json
python3 -IB aletheia.py replay receipt.json
ALETHEIA_TEST_LEAN=1 python3 -B -m unittest discover -s verification/tests -v
```

The receipt reports a countermodel for the missing-bridge argument and a Lean-checked entailment with the explicit bridge. The corpus keeps the semantic objection open. See the [runner handoff](runner/README.md) for independent proposal replay and the [verification guide](verification/README.md) for the result vocabulary.

## Standing on the shoulders of established research

**All five verification tools have been integrated and tested.** Each investigation links to its assumptions, checked result and replay instructions.

| Tool | Verified use | Where to replay it |
| --- | --- | --- |
| Lean 4 | Checks the bridge proof and exposes its axiom dependencies. | [Replay the bridge proof](#run-locally) |
| Mathlib | Supplies the quotient machinery for the checked theorem about when grouping preserves a relationship. | [Mathlib replay](verification/README.md#mathlib-grouping-theorem) |
| Z3 | Replays 15 finite queries comparing identity, common essence and opposition. | [Z3 replay](corpus/investigations/simplicity-identity.md#replay) |
| Isabelle/HOL | Checks the modal bridge theorem and the explicit interpretations for necessary relations and contingent creation. | [Isabelle replay](corpus/investigations/modal-creation.md#replay) |
| Nitpick | Finds two-world counterexamples for the Aletheia creation argument and the published Anderson reference. | [Nitpick replay](corpus/investigations/modal-creation.md#replay) |

Christoph Benzmüller and colleagues provide a precedent for computational theology that exposes the consequences of competing axioms. Benzmüller and Bruno Woltzenlogel Paleo formalised variants of Gödel’s ontological argument with higher-order provers. Benzmüller and David Fuenmayor examined positive properties and modal collapse in related variants. [Formalisation of Gödel’s argument](https://arxiv.org/abs/1308.4526) · [Analysis of modal collapse](https://arxiv.org/abs/1910.08955)

## Project status

The software uses MIT and the original corpus and prose use CC BY 4.0. The [licensing guide](LICENSING.md) describes the scope of each licence. The [consumer roadmap](docs/consumer-roadmap.md) and [architecture](docs/architecture.md) describe the implemented workflow and later stages.
