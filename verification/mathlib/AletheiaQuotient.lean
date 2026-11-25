import Mathlib.Order.Setoid.Basic

set_option warningAsError true

namespace Aletheia

universe u v

variable {Item : Type u} {Category : Type v}

abbrev categoryOf (classify : Item → Category) (item : Item) :
    Quotient (Setoid.ker classify) :=
  Quotient.mk _ item

/-- A relation is defined on the classes exactly when changing representatives
    in either argument preserves its truth. -/
theorem relation_descends_iff (classify : Item → Category) (rel : Item → Item → Prop) :
    (∃ lifted : Quotient (Setoid.ker classify) → Quotient (Setoid.ker classify) → Prop,
        ∀ x y, lifted (categoryOf classify x) (categoryOf classify y) ↔ rel x y) ↔
    ∀ x x' y y', classify x = classify x' → classify y = classify y' →
      (rel x y ↔ rel x' y') := by
  constructor
  · rintro ⟨lifted, agrees⟩ x x' y y' hx hy
    have hx' : categoryOf classify x = categoryOf classify x' :=
      Quotient.sound ((Setoid.ker_def).2 hx)
    have hy' : categoryOf classify y = categoryOf classify y' :=
      Quotient.sound ((Setoid.ker_def).2 hy)
    rw [← agrees x y, ← agrees x' y', hx', hy']
  · intro invariant
    let pair := Setoid.prod (Setoid.ker classify) (Setoid.ker classify)
    let onPair : Quotient pair → Prop :=
      Quotient.lift (fun xy : Item × Item => rel xy.1 xy.2)
        (fun x y h => propext (invariant x.1 y.1 x.2 y.2 h.1 h.2))
    let combine := Setoid.prodQuotientEquiv (Setoid.ker classify) (Setoid.ker classify)
    exact ⟨fun x y => onPair (combine (x, y)), fun _ _ => Iff.rfl⟩

/-- An irreflexive relation cannot descend if it relates two items in one class. -/
theorem opposed_pair_prevents_descent (classify : Item → Category)
    (rel : Item → Item → Prop) (irreflexive : ∀ x, ¬ rel x x)
    {x y : Item} (same : classify x = classify y) (opposed : rel x y) :
    ¬ ∃ lifted : Quotient (Setoid.ker classify) → Quotient (Setoid.ker classify) → Prop,
        ∀ a b, lifted (categoryOf classify a) (categoryOf classify b) ↔ rel a b := by
  intro existsLift
  have invariant := (relation_descends_iff classify rel).1 existsLift
  exact irreflexive x ((invariant x x y x rfl same.symm).1 opposed)

abbrev colour (_ : Bool) : Unit := ()
def sameColour (x y : Bool) : Prop := colour x = colour y
def differentDonors (x y : Bool) : Prop := x ≠ y

theorem same_colour_descends :
    ∃ lifted : Quotient (Setoid.ker colour) → Quotient (Setoid.ker colour) → Prop,
      ∀ a b, lifted (categoryOf colour a) (categoryOf colour b) ↔ sameColour a b := by
  apply (relation_descends_iff colour sameColour).2
  intro x x' y y' hx hy
  unfold sameColour
  rw [hx, hy]

theorem different_donors_fails :
    ¬ ∃ lifted : Quotient (Setoid.ker colour) → Quotient (Setoid.ker colour) → Prop,
      ∀ a b, lifted (categoryOf colour a) (categoryOf colour b) ↔ differentDonors a b :=
  opposed_pair_prevents_descent colour differentDonors (fun _ h => h rfl)
    (x := false) (y := true) rfl Bool.noConfusion

end Aletheia

#print axioms Aletheia.relation_descends_iff
#print axioms Aletheia.opposed_pair_prevents_descent
#print axioms Aletheia.same_colour_descends
#print axioms Aletheia.different_donors_fails
