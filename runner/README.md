# Run a local research tranche

The current interface produces a reproducible handoff for a human or an AI working in another tool. Start with the corpus and agent contract. A published or remote service is unnecessary.

## Prepare an input

```sh
python3 -IB aletheia.py packet Q-GOD-03 > question.json
```

The packet includes the question, applicable programme text, relevant claims and arguments, referenced definitions, premises and objections, and complete linked idea narratives and source records. It carries hashes of the indexed corpus inputs and verifier assets. Build from those inputs and return a proposed corpus tree for review. Record source locators, assumptions, rival readings and attempted refutations. Preserve evidence of failures and keep objections open where they remain unresolved.

## Verify independently

Keep an operator-controlled copy of the reviewed project. Assemble the proposed corpus and acknowledgement in a separate, stable directory that proposal authors cannot change during the run. Use the trusted copy's script by absolute path.

```sh
python3 -IB /path/to/trusted/aletheia.py verify --candidate /path/to/proposal > receipt.json
python3 -IB /path/to/trusted/aletheia.py replay receipt.json --candidate /path/to/proposal
```

For this local milestone the candidate supplies indexed corpus files and the acknowledgement as data. The trusted copy supplies policy, regression fixtures, proof, compiler pin and checker code. The verifier freezes the Purple Man artifacts and the simplicity exemplar against the trusted baseline. Policy or protected-record changes require a separately reviewed update of that baseline. The operator controls the trusted directory, installed Lean, Python and the execution environment.

An accepted run means the local structural and formal checks completed. Review the specific logical result, premise support, semantic mapping and any defeaters before using a conclusion. A proposal may legitimately add a refuted argument or inconsistent premise set as a recorded failure. This interface has no automatic merge or claim promotion. With no Git metadata in the supplied draft, replay identifies indexed input bytes by content hashes. Protected hosted checks, reviewed Git revisions, durable attempt logs and provider adapters are planned in the [roadmap](../docs/roadmap.md).
