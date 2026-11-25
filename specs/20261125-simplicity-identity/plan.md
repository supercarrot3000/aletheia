# Implementation and verification plan

1. Index one source record and one investigation in the corpus. Extend corpus loading and packet retrieval to include reviewed research reports and their typed source links. Preserve the old arguments and the current acceptance policy.
2. Put the first-order experiment and its pinned solver dependency in a standalone verification entry point. Run a matrix of five profiles and three exact finite cardinalities. Export SMT-LIB queries and check model interpretations as plain data with a native Python predicate check. Leave the Python and Lean baseline independent of Z3.
3. Record the conclusions and limits in the investigation report. Review Aquinas I, q. 28, aa. 2–3 and I, q. 39, a. 1, and distinguish textual exegesis from mathematical reconstruction.
4. Test packet links and malformed source references with the ordinary suite. Run the separate Z3 experiment, test each profile and exact bound, replay the exported SMT-LIB, and mutate a witness and solver outcome. Verify the ordinary Lean workflow again. Seek independent review before promotion.
