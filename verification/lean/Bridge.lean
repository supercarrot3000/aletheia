set_option warningAsError true

theorem simplicityBridge (simple composite relational : Prop)
    (isSimple : simple) (excludesComposition : simple → ¬ composite)
    (relationalImpliesComposite : relational → composite) : ¬ relational :=
  fun isRelational => excludesComposition isSimple (relationalImpliesComposite isRelational)

#print axioms simplicityBridge
