theory Anderson_Reference
  imports Main
begin

text \<open>Independent transcription of the premises in Benzmüller and Fuenmayor,
  arXiv:1910.08955v2, section 5, Figure 5. Target: the countermodel to
  modal collapse (line 20). The quantifier over propositions is higher-order.\<close>

typedecl world
typedecl individual

type_synonym mprop = "world \<Rightarrow> bool"
type_synonym property = "individual \<Rightarrow> mprop"

definition box :: "('w \<Rightarrow> 'w \<Rightarrow> bool) \<Rightarrow> ('w \<Rightarrow> bool) \<Rightarrow> 'w \<Rightarrow> bool" where
  "box r p w \<longleftrightarrow> (\<forall>v. r w v \<longrightarrow> p v)"

definition actual_some :: "(individual \<Rightarrow> mprop) \<Rightarrow> property \<Rightarrow> mprop" where
  "actual_some e p w \<longleftrightarrow> (\<exists>x. e x w \<and> p x w)"

definition entails :: "(world \<Rightarrow> world \<Rightarrow> bool) \<Rightarrow> (individual \<Rightarrow> mprop) \<Rightarrow>
    property \<Rightarrow> property \<Rightarrow> mprop" where
  "entails r e p q w \<longleftrightarrow> box r (\<lambda>v. \<forall>x. e x v \<longrightarrow> p x v \<longrightarrow> q x v) w"

definition godlike :: "(world \<Rightarrow> world \<Rightarrow> bool) \<Rightarrow> (property \<Rightarrow> mprop) \<Rightarrow> property" where
  "godlike r pos x w \<longleftrightarrow> (\<forall>p. pos p w \<longleftrightarrow> box r (p x) w)"

definition essence :: "(world \<Rightarrow> world \<Rightarrow> bool) \<Rightarrow> (individual \<Rightarrow> mprop) \<Rightarrow>
    property \<Rightarrow> individual \<Rightarrow> mprop" where
  "essence r e q x w \<longleftrightarrow> (\<forall>p. box r (p x) w \<longleftrightarrow> entails r e q p w)"

definition necessary_existence :: "(world \<Rightarrow> world \<Rightarrow> bool) \<Rightarrow>
    (individual \<Rightarrow> mprop) \<Rightarrow> property" where
  "necessary_existence r e x w \<longleftrightarrow> (\<forall>q. essence r e q x w \<longrightarrow> box r (actual_some e q) w)"

definition anderson :: "(world \<Rightarrow> world \<Rightarrow> bool) \<Rightarrow>
    (individual \<Rightarrow> mprop) \<Rightarrow> (property \<Rightarrow> mprop) \<Rightarrow> bool" where
  "anderson r e pos \<longleftrightarrow> symp r \<and>
    (\<forall>w p. pos (\<lambda>x v. \<not> p x v) w \<longrightarrow> \<not> pos p w) \<and>
    (\<forall>w p q. pos p w \<and> entails r e p q w \<longrightarrow> pos q w) \<and>
    (\<forall>w. pos (godlike r pos) w) \<and>
    (\<forall>w p. pos p w \<longrightarrow> box r (pos p) w) \<and>
    (\<forall>w. pos (necessary_existence r e) w)"

lemma reference_modal_collapse:
  "anderson r e pos \<Longrightarrow> \<forall>p w. p w \<longrightarrow> box r p w"
  nitpick [card world = 2, card individual = 1, timeout = 45, expect = genuine]
  oops

end
