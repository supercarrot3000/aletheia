# Identity collapse and relative opposition in divine simplicity

Research record INV-SIMPLICITY-IDENTITY. Questions Q-GOD-02, Q-GOD-03 and Q-GOD-04. Semantic and theological review remains open.

## The argument in its source

The seed exercise asks whether excluding composition entails excluding real relational distinction. Its propositional countermodel shows why an extra premise is needed. Aquinas supplies a sharper challenge in *Summa Theologiae* I, q. 28, a. 3, arg. 1. If paternity is the same in reality as the divine essence, and filiation is the same in reality as that very essence, it seems that paternity and filiation must be identical. If those two sameness statements are unrestricted equality on a single domain, the inference is valid by symmetry and transitivity. Real opposition would then apply to identical relata. [Primary text and locators](../sources/aquinas-summa-identity.json)

Aquinas's reply distinguishes sameness in reality from sameness in account or intelligibility. He appeals to the different respects expressed by action and being acted upon, and attributes real distinction to relative opposition while maintaining simplicity in the absolute essence. The account of persons in I, q. 39, a. 1 invokes subsistent relations. A formal reconstruction has to explain how that position secures the unity of essence and why the distinctions are real. Relabelling the same problem as a different type of identity would leave those obligations intact. [Primary Latin text, I, qq. 28 and 39](https://www.corpusthomisticum.org/sth1028.html)

## Representations under test

Let `p` and `f` denote paternity and filiation as modeled relata. Each relatum maps to an essence class. Two relata have a common essence class when their images are equal. Opposition is a symmetric, irreflexive relation. The background asserts that `p` and `f` have the same image. This is a deliberately weak representation of the source's stronger sameness-in-reality language. The symmetry and irreflexivity conditions specify the test's opposition predicate.

- **Common essence.** Require opposition between `p` and `f` and allow relata with the same image to differ.
- **Unrestricted identity.** Add `p = f`. Here the same-domain identity objection is represented by its immediate consequence, since identifying both with one object entails that equation.
- **Replacement in either argument of opposition.** Test the two positions separately. For any `x` and `y` with the same essence image, replacing `x` by `y` in the chosen position must preserve the truth of opposition against any third argument.
- **Control.** Require both replacement rules and drop the assertion that `p` and `f` are opposed. This tests whether the rules themselves are consistent.

The replacement test matters even if sameness of essence is represented by a class projection. Assuming replacement in the first position takes opposition of `p` to `f` to opposition of `f` to itself. Replacement in the second position instead produces opposition of `p` to itself. Either clashes with irreflexivity. This argument works at any domain size and can be inspected directly. Given symmetry, the two replacement rules are equivalent. Running each on its own makes the exact failure in the model explicit. The solver is for repeatable witness discovery and comparison against the alternate premises. It searches the finite interpretations and gives a concrete witness that a researcher can challenge. [Z3 solver interface](https://microsoft.github.io/z3guide/programming/Z3%20Python/Introduction/)

## Finite results

Z3 checked five profiles at each exact relatum-domain size. The essence sort has as many available labels as relata, so it can represent every partition of the modeled relata. Unused labels are allowed. Each reported model is checked by a separate Python test of the decoded interpretation.

| Profile | One relatum | Two relata | Three relata |
| --- | --- | --- | --- |
| Common essence with opposition | Unsatisfiable | Model | Model |
| Unrestricted identity with opposition | Unsatisfiable | Unsatisfiable | Unsatisfiable |
| First-position replacement with opposition | Unsatisfiable | Unsatisfiable | Unsatisfiable |
| Second-position replacement with opposition | Unsatisfiable | Unsatisfiable | Unsatisfiable |
| Both replacements, without an asserted opposed pair | Model | Model | Model |

A smallest witness in the searched range has two different relata assigned to the same essence label, with opposition between them in both directions and neither self-opposed. At size one an irreflexive relation supplies no pair. The size-three witness establishes only that the weak formal constraints admit such a domain. It makes no claim about three divine persons or the full inventory of relations. The solver results concern the exact finite encodings. The general contradiction for identity and replacement follows from the direct argument above.

## Replay

From the project root, use a virtual environment for the optional model finder.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r verification/experiments/requirements-z3.txt
.venv/bin/python -IB verification/experiments/simplicity_identity.py > simplicity-receipt.json
.venv/bin/python -B -m unittest discover -s verification/experiments -v
```

The receipt contains every SMT-LIB query, exact bounds, solver version, timeout and checked witness. A timeout or unknown result is distinct from an unsatisfiable result. The original corpus and Lean verification commands have no Z3 dependency. Model names can differ on another run. The profile outcomes and the validity of the returned interpretations are the reproducible observations.

## What remains open

The common-essence reconstruction owes a principled reason why substitution fails in opposition while its account of common essence remains strong enough for divine simplicity. A critic may argue that multiple relata mapped to one essence class merely share a classification, or that real relata add an ontological commitment tantamount to composition. Aquinas's distinctions among senses of composition in I, q. 3, a. 7 and his account of subsistent relation in I, q. 39, a. 1 set the terms of the next review. An argument that the source requires substitution in either position would overturn this reading's claim to semantic fidelity. An independently defended alternative that preserves the source's stronger sameness claim would supersede the projection model. [Primary text on simplicity](https://www.corpusthomisticum.org/sth1003.html) · [Primary text on relation and person](https://www.corpusthomisticum.org/sth1028.html)
