# shikumi-contrace Specification

| Document | Summary |
| --- | --- |
| [Purpose and Scope](aim.md) | The purpose of shikumi-contrace, and what is out of scope. |
| [Structure of a Contract](contract.md) | The entities that make up a contract (subject type, members, clauses), and the rules for their positions. |
| [Independence of Contracts](independence.md) | The rules for keeping a contract an independent asset that depends on neither tests nor implementations, and the direction of dependencies. |
| [Declarations on the Test Side](test_side.md) | The declarations that relate a test to the clauses of a contract, annotations, and bindings. |
| [Descriptors and Syntax](syntax.md) | The names and syntax of the descriptors used on the contract side and the test side, including the syntax of bindings. |
| [Reading Information](reading.md) | An API, independent of any test runner, that reads the information declared on contracts and tests, to trace the correspondence between clauses and tests. |
| [Names and Placement of the Public API](api.md) | Where the public API is placed, and the names of the reading, checking and pytest integration APIs. |
| [Vocabulary](vocab.md) | Providing a standard vocabulary, not obstructing custom vocabulary, and not rejecting unknown vocabulary. |
| [Standard Vocabulary](standard_vocabulary.md) | The standard clause kinds, violation behaviors, relation words and annotation words, and their meanings. |
| [Specification Body and Validation](regulation.md) | The validation rules that check the structure and independence of contracts, how the ranges that limit references are determined, and the nature and limits of the checks. |
| [pytest Integration (Optional)](pytest_integration.md) | What to observe when providing the pytest integration as an optional integration: separation from the core, how diagnostics are reported, how information is held, and the range of features provided. |
