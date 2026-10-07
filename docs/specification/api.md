# Names and Placement of the Public API

Defines where the public API is placed and the names of the reading API, the checking API and the pytest integration. The names for writing contracts and tests (descriptors, words, binding) are defined in the specification of descriptors and syntax.

## API_001

The public API of the core is placed in `shikumi_contrace` (the top level), `shikumi_contrace.reading` and `shikumi_contrace.checking`, and the pytest integration is placed in `shikumi_contrace.pytest`.

title: Public APIs are placed in four locations

level: MUST

## API_002

The top-level `shikumi_contrace` holds the names for writing contracts and tests, laid out flat. They are the descriptors (`subject`, `member`, `kind`, `depends_on`, `on_violation`), the values of the clause kinds (`PRE`, `POST`, `INV`), the standard violation behaviors (`OUT_OF_SCOPE`, `REJECTED`), relation words, annotation words, `binds`, the generator of custom vocabulary `define`, and the re-exports of metamk (`Phase`, `phase_of`; `Phase` is an alias of `metamk.Mk`).

title: The top level holds the names for writing contracts and tests

level: MUST

detail: A descriptor in the `@=` form is imported and used as a bare name (SYN_011), so the names for writing are laid out flat at the top level.

related: [SYN_011](syntax.md#syn_011)

## API_003

The reading API is placed in `shikumi_contrace.reading` and the checking API in `shikumi_contrace.checking`, and neither is placed at the top level.

title: Reading and checking APIs are not placed at the top level

level: MUST

detail: All that code which writes contracts and tests needs is the names for writing. Mixing the names for reading and checking into the top level would increase the risk of collisions with users' names and the number of names. It also fits a contract asset importing only the minimum necessary names (IND_004).

related: [RDG_001](reading.md#rdg_001)

## API_004

`shikumi_contrace.reading` provides the following functions. The names are aligned with the `*_of` form of Shikumi's `information_of`.

| Name | Role |
| --- | --- |
| `relations_of(test)` | The relations of a test (relation words and clauses) |
| `annotations_of(obj)` | Annotations (words and texts) |
| `bindings_of(obj)` | Bindings (subject types and implementations) |
| `clauses_of(contract)` | The list of the clauses of a contract (kinds, violation behaviors, clause statements, annotations) |
| `dependencies_of(contract)` | Reads the contracts directly depended on by the contract, in written order |
| `dependents_of(contract, within=...)` | Looks up, within a specified range, the contracts that directly depend on the contract |
| `tests_of(clause, within=...)` | Looks up, from a clause, the tests related to it |
| `untested_clauses(contract, within=...)` | The list of clauses that no test with a relation is related to |

title: Names of the reading API

level: MUST

detail: `within` is given the objects that form the range of the lookup or the list. `tests_of` and `untested_clauses` receive tests; `dependents_of` receives modules or classes containing contracts (RDG_004, RDG_010). `untested_clauses` does not infer whether a clause ought to have a test from its meaning; it only looks at whether a recorded relation exists (RDG_005).

related: [RDG_002](reading.md#rdg_002), [RDG_010](reading.md#rdg_010)

## API_005

`shikumi_contrace.reading` provides `Relation`, `Annotation`, `Binding` and `Clause` as the types of reading results. Reading that follows `__wrapped__` (RDG_007) is built into all the functions of API_004.

title: Result types of the reading API

level: MUST

related: [RDG_007](reading.md#rdg_007)

## API_006

`shikumi_contrace.checking` provides `check(...)`, which runs checks and returns a list of diagnostics (`list[Diagnostic]`), the type of a diagnostic `Diagnostic` (code, message, subject), `ContraceWarning`, the category of warning with which the pytest integration reports diagnostics, and `CONTRACT_ASSET_STRUCTURE`, the structure specification of a contract asset. If the list is empty, there is no violation.

title: Names of the checking API

level: MUST

detail: The type returned by `check` is shikumi-contrace's own, and Shikumi's validation result type is not exposed in the public API. `CONTRACT_ASSET_STRUCTURE` is a value of a Shikumi type, and the only name published so that it can be passed to Shikumi's own validation (REG_027).

related: [REG_018](regulation.md#reg_018)

## API_007

`check` receives ranges either as declarations (`contract_assets`, `tests`, `implementations`: lists of module-path strings) or as the source of a derivation (`test_modules`: a list of test modules). When any one of the three declarations is given, no derivation is used, and the ranges of the roles not given are empty.

title: How check receives the ranges

level: MUST

detail: This applies the rule that, if there are declarations, only the declarations are used (REG_011), also to partial declarations.

related: [REG_011](regulation.md#reg_011)

## API_008

The pytest integration is registered explicitly by the user, writing `pytest_plugins = ["shikumi_contrace.pytest"]`.

title: The pytest integration is registered explicitly

level: MUST

detail: It was confirmed that, even if the package contains a module named `pytest.py`, the real pytest is loaded by an absolute import and works.

related: [PYT_005](pytest_integration.md#pyt_005)

## API_009

Validation at collection time is chosen with the option `--contrace-check`. The declarations of ranges are written in the pytest settings (ini) as `contrace_contract_assets`, `contrace_tests` and `contrace_implementations`, one module path per line.

title: The option and the settings of the pytest integration

level: MUST

detail: The three keys of the settings correspond to the three declarations of `check`.

related: [PYT_012](pytest_integration.md#pyt_012)

## API_010

To escalate diagnostics from warnings to errors, use pytest's warning filters (`-W error::shikumi_contrace.checking.ContraceWarning`, or `filterwarnings` in the settings).

title: Escalating diagnostics to errors

level: INFORMATIVE

related: [PYT_007](pytest_integration.md#pyt_007)
