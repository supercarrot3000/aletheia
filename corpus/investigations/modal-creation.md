# Necessary relations and contingent creation

Q-GOD-07 asks whether a necessary divine relation can coexist with contingent creation. Let D say that the relation holds at a world and C say that creation occurs there. In this investigation, necessity means truth at every world accessible from the point of evaluation. The symbols D and C are propositions about worlds. The model leaves the nature of the relation and of creation to further interpretation.

## Two readings of the bridge

If D is necessary and the implication from D to C is also necessary, C must be necessary. Isabelle/HOL proves this for arbitrary accessibility. The bridge has content. It would mean that every world which admits the divine relation also admits creation.

If that implication holds at the actual world, creation can still vary. Nitpick searches an exact two-world domain with reflexive, symmetric and transitive accessibility. A separate theorem checks an explicit interpretation. D holds at both mutually accessible worlds, C holds at the actual world, and C fails at the other world. A second checked interpretation shows that the stronger premises can be satisfied together.

## Published reference result

Benzmüller and Fuenmayor report a countermodel to full modal collapse in Anderson’s variant of Gödel’s argument. Our independent Isabelle transcription follows their Figure 5, with actualist existence, a symmetric frame, intensional properties and higher-order quantification over propositions. The exact scope is two worlds and one individual, as reported for line 20. It checks the same countermodel outcome. The reference uses a much richer set of assumptions than the separate bridge argument for Q-GOD-07. [Primary paper, §5 and Figure 5](https://arxiv.org/html/1910.08955)

## Replay

Install the Isabelle2025-2 distribution, put its executable on the command path and run from the repository root.

```sh
isabelle version
isabelle build -D verification/isabelle
isabelle build_log -v Aletheia
```

Where the experiment expects a countermodel, Nitpick must report a genuine one at the specified bound. A one-world control exhausts its scope without a counterexample. A potential counterexample or timeout fails these expectations. The Isabelle theorems separately check the general entailment and the two concrete interpretations. [Official pinned distribution](https://isabelle.in.tum.de/website-Isabelle2025-2/) · [Nitpick manual](https://isabelle.in.tum.de/doc/nitpick.pdf)
