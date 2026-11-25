theory Creation
  imports Anderson_Reference
begin

text \<open>Any accessibility relation is allowed in the proof. The countermodel
  search is restricted to a reflexive, symmetric and transitive frame.\<close>

theorem necessary_bridge:
  assumes "box r divine actual" and "box r (\<lambda>w. divine w \<longrightarrow> created w) actual"
  shows "box r created actual"
  using assms unfolding box_def by blast

lemma actual_bridge_counterexample:
  assumes "reflp r" "symp r" "transp r"
    and "box r divine actual" "divine actual \<longrightarrow> created actual" "divine actual"
  shows "box r created actual"
  using assms
  nitpick [card 'a = 1, timeout = 45, expect = none]
  nitpick [card 'a = 2, timeout = 45, expect = genuine]
  oops

text \<open>The following explicit interpretation checks that the weaker premises
  are jointly satisfiable, and that there is a reachable world where creation
  fails. Both worlds are mutually accessible.\<close>

theorem explicit_two_world_witness:
  "reflp (\<lambda>(_::bool) (_::bool). True) \<and>
   symp (\<lambda>(_::bool) (_::bool). True) \<and>
   transp (\<lambda>(_::bool) (_::bool). True) \<and>
   box (\<lambda>_ _. True) (\<lambda>_. True) True \<and>
   ((\<lambda>_::bool. True) True \<longrightarrow> id True) \<and>
   (\<lambda>_::bool. True) True \<and>
   \<not> box (\<lambda>_ _. True) id True"
  unfolding reflp_def symp_def transp_def box_def by auto

text \<open>The stronger assumptions are consistent as well. In a one-world
  interpretation both propositions can hold.\<close>

theorem strong_premises_possible:
  "box (\<lambda>(_::unit) (_::unit). True) (\<lambda>_. True) () \<and>
   box (\<lambda>_ _. True) (\<lambda>_. True \<longrightarrow> True) ()"
  unfolding box_def by simp

end
