# shikumi-contrace Changelog

Records the change history of `shikumi-contrace` by version. `shikumi-contrace` is a new project separate from `speclike`, and the change history of `speclike` is not carried over.

## V0_1_0

The first public release.

version: 0.1.0

released on: 2026-10-07

Added:

- Added the descriptors `subject`, `member` and `kind` that describe a contract, and the standard clause kinds `PRE`, `POST` and `INV`.
- Added the relation words `upholds` and `violates` that relate a test to a clause, and 17 standard annotation words. Annotation words can be written both with `@=` in a class body and as decorators.
- Added the binding `binds[Subject](Impl)` that ties the subject type of a contract to an implementation. A type checker can check that the implementation conforms. The subject type may be a generic class given type arguments (`Inventory[Reservation]`).
- Added `define`, the generators for custom vocabulary.
- Re-exported metamk's `Mk` under the name `Phase`, and `phase_of` under the same name.
- Added the reading API `shikumi_contrace.reading`. `untested_clauses` lists clauses that have no test with a recorded relation.
- Added `depends_on` for describing directional dependencies between contracts, and `dependencies_of` and `dependents_of` for forward and reverse lookup. Validation checks misplaced dependencies, dependencies on non-contract classes, and dependency cycles.
- Added the rule that the shapes of values shared by a contract and an implementation (boundary types) are placed in the `ports` package directly inside the contract asset, and its checks. The structure (`ports` is a package whose direct children are modules) is checked with the Shikumi structure specification `CONTRACT_ASSET_STRUCTURE`. Validation also reports a `ports` that contains a contract or a function, a `ports` whose `__init__` holds definitions, a `ports` that refers to a contract or to `shikumi-contrace`, a parent package whose `__init__` imports them, a package that holds `ports` and also contains a test or an implementation, a `ports` that is left out of a declared range, and a contract module that defines a Protocol that is not a subject type.
- Added `on_violation` for describing how a precondition treats violating calls, with the standard values `OUT_OF_SCOPE` and `REJECTED`. It does not infer or enforce the implementation mechanism or the shape of test code.
- Added the checking API `shikumi_contrace.checking`. It checks the independence of contract assets, the positions of clauses, the names of members, bindings, and combinations of the standard vocabulary that are not normally used.
- Added the optional pytest integration `shikumi_contrace.pytest`. It provides the display of contract information in the output of failed tests, and validation at collection time only when chosen.
