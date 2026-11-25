# Aletheia

Aletheia investigates the nature of God, goodness, morality, consciousness and fundamental reality. It grew out of Christian inquiry about the character of God and how human and artificial intelligence might come to understand goodness. Its purpose is to discover what is true. That includes finding errors in its own arguments, testing rival explanations and preserving questions that remain unresolved.

People and AI agents can inherit the same material, recover how a conclusion was reached and challenge the steps for themselves. Aletheia welcomes scrutiny from any philosophical or religious starting point. A proof establishes what follows from its stated assumptions in its chosen logic. Assessing the truth of those assumptions, the fidelity of a theological interpretation and the character of lived experience requires other kinds of inquiry.

## Start with a question

- Work through an idea on paper or in a browser. [Explore a question](docs/research/explore.md)
- Find an answer, its evidence and the objection that remains. [Check or reuse a finding](docs/research/findings.md) · [Machine-readable catalogue](docs/research/findings.json)

## Start with the research

- [The Purple Man and Alice Springs](corpus/ideas/purple-man.md) preserves the full available recollection and the contributor's clarifications. The original playwright’s identity remains open, and their work helped inspire this project. [Provenance record](corpus/sources/purple-man-origin.json) · [Acknowledgement](ACKNOWLEDGEMENTS.md)
- [Nature of God and fundamental reality](corpus/programmes/nature-of-god.md) introduces the divine-simplicity question. The local demonstration tests whether excluding composition also excludes real relational distinction. The [identity-collapse investigation](corpus/investigations/simplicity-identity.md) traces a sharper objection to Aquinas and compares finite models of the competing assumptions.
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

- **Implemented in the local milestone.** [Lean 4](https://lean-lang.org/doc/reference/latest/Introduction/) checks the exact encoded bridge theorem with its logical kernel and exposes its axiom dependencies.
- [Mathlib](https://mathlib.org/) supplies the equivalence relations and product of quotients used in the checked grouping theorem. [Replay](verification/README.md#mathlib-grouping-theorem)
- [Isabelle/HOL](https://isabelle.in.tum.de/) checks the modal bridge theorem. [Nitpick](https://isabelle.in.tum.de/doc/nitpick.pdf) finds countermodels to the actual-world bridge and the published Anderson reference. [Modal investigation](corpus/investigations/modal-creation.md)
- **Implemented for the optional finite-model experiment.** [Z3](https://microsoft.github.io/z3guide/docs/logic/basiccommands/) finds finite interpretations of common essence and opposition and compares them with stronger identity assumptions. The [investigation](corpus/investigations/simplicity-identity.md#replay) includes the replay command.

Christoph Benzmüller and colleagues provide a precedent for computational theology that exposes the consequences of competing axioms. Benzmüller and Bruno Woltzenlogel Paleo formalised variants of Gödel’s ontological argument with higher-order provers. Benzmüller and David Fuenmayor examined positive properties and modal collapse in related variants. [Formalisation of Gödel’s argument](https://arxiv.org/abs/1308.4526) · [Analysis of modal collapse](https://arxiv.org/abs/1910.08955)

## Project status

This is Aletheia's initial open-source research release. The software uses MIT and the original corpus and prose use CC BY 4.0. The [licensing guide](LICENSING.md) describes the scope of each licence. The [audit and roadmap](docs/roadmap.md) and [architecture](docs/architecture.md) describe the implemented workflow and later stages.
