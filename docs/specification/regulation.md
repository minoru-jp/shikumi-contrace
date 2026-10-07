# Specification Body and Validation

Defines the validation rules provided when shikumi-contrace is built as a Shikumi specification body, and the nature of its checks. A check only returns diagnostics and does not rewrite contracts or tests.

## REG_001

The declarations of shikumi-contrace for contracts and tests **MUST** be defined as a specification body composed of Shikumi's information types, descriptors and validation rules.

title: The specification body is composed of information types, descriptors and validation rules

level: MUST

related: [AIM_007](aim.md#aim_007)

## REG_002

Validation **MUST** be based on the runtime state that holds after Python has run. It **MUST NOT** analyze source code statically.

title: Validation is based on the runtime state after execution

level: MUST

detail: The targets of a check are the namespaces of modules and packages after import, and the attributes of classes. Imports performed lazily inside the body of a function, and the inner values of lists and the like, are not checked. Checks are run only on trusted Python code. Code that runs at import time runs with ordinary privileges.

## REG_003

shikumi-contrace **MUST** provide a validation rule that checks whether a contract asset refers to tests or implementations. A violation is reported as a diagnostic.

title: A rule checks the independence of a contract asset

level: MUST

related: [IND_002](independence.md#ind_002)

detail: The ranges of what is regarded as tests and what as implementations are defined in the way ranges are determined (REG_011 to REG_017).

## REG_004

shikumi-contrace **MUST** provide a validation rule that checks whether the standard clause kinds are placed in their defined positions.

title: A rule checks the positions of standard clause kinds

level: MUST

related: [CTR_009](contract.md#ctr_009)

## REG_005

shikumi-contrace **SHOULD** provide a validation rule that checks whether the class name of a member matches the name of the member it refers to. A contract that has both a declaration of the subject type and a declaration of a member is not subject to it.

title: A rule checks the names of member classes

level: SHOULD

related: [CTR_008](contract.md#ctr_008)

## REG_006

A validation rule **MUST** only return diagnostics. It **MUST NOT** rewrite or correct the content of contracts or tests.

title: Validation reports only

level: MUST NOT

## REG_007

A validation rule **MUST NOT** emit a diagnostic on the grounds that a vocabulary is not included in the standard vocabulary.

title: No validation rule rejects unknown vocabulary

level: MUST NOT

related: [VOC_004](vocab.md#voc_004)

## REG_008

Users **MAY** add their own validation rules.

title: Users may add their own validation rules

level: MAY

## REG_009

The severity of diagnostics is not fixed per validation rule. When the pytest integration reports diagnostics, it reports them as pytest warnings, and the severity is decided by the user.

title: Severity is delegated to the user

level: MUST

related: [PYT_007](pytest_integration.md#pyt_007)

## REG_010

shikumi-contrace **SHOULD** provide a validation rule that checks whether a test that has a relation holds, on itself or on the class it belongs to, a binding to the subject type of the contract the clause belongs to. It reports as diagnostics the case in which it does not, and the case in which the subject type of the binding does not match that of the contract.

title: A rule checks that related tests are bound to the contract's subject type

level: SHOULD

detail: The contract a clause belongs to is followed from the class that encloses the class of the clause. The subject type of a contract is obtained from the declaration of the subject type of the contract.

related: [IND_007](independence.md#ind_007)

## REG_011

The ranges of contract assets, tests and implementations are expressed as module paths (prefixes separated by dots). Unless the user declares them, a range is derived from the declarations of the tests; if the user declares them, only the declarations are used. The union of a derived range and a declared range is not used.

title: Ranges are module paths; declared ranges replace derived ones

level: MUST

detail: If there are declarations, only the declarations; if not, derivation. This keeps the explanation simple and avoids unexpected results.

related: [IND_002](independence.md#ind_002)

## REG_012

When there are no declarations, the range of contract assets is derived from the modules of the clauses that the tests with relations relate to and from the modules of contracts on which those contracts depend directly or transitively through contract dependencies. The range of tests is derived from the modules of the tests with relations, and the range of implementations from the modules of the implementations that the tests bind. However, when deriving, modules of the Python standard library (including `builtins`) are excluded from the range of implementations. The targets of the check are the derived contract-asset modules. The `ports` (boundary types) that the contract modules refer to are also included in the range of contract assets.

title: Ranges are derived from the declarations in the tests

level: MUST

detail: Derivation covers only what the tests declared, the contracts on which those contracts depend, and the `ports` that the contracts refer to, so there may be oversights but no false detections. When `ports` appears in a qualified module path, it is treated as boundary types on the contract-asset side only if the referring contract module is also under the parent package of that `ports`. Merely having `ports` in the module path of an unrelated dependency package does not cause that package to be derived into the contract asset. A top-level `ports` remains a candidate so that invalid placement can be diagnosed. Excluding the standard library applies only to derivation. Without it, when an implementation is a class of the standard library, merely using `str` in a contract would be falsely detected. A range declared by the user is not judged by whether it is in the standard library.

related: [SYN_015](syntax.md#syn_015)

## REG_013

A derived range of implementations is only the module where the implementation is defined. References to anything other than the defining module, such as the package that re-exports it, are not detected by derivation. When a wider check is wanted, declare the ranges.

title: A derived implementation range is the defining module only

level: INFORMATIVE

## REG_014

shikumi-contrace **MUST** provide a means for users to declare the ranges of contract assets, tests and implementations. When the range of contract assets is declared, all modules under it are checked.

title: Users can declare the three ranges

level: MUST

detail: Contracts that no test cites (orphaned contracts) are also checked. The names and syntax of the declarations are defined in the specification of the names and placement of the public API.

## REG_015

When ranges overlap, the longest matching range takes precedence. A reference for which the range of contract assets matches longest is allowed.

title: The longest matching range wins

level: MUST

detail: To handle the layout in which a contract asset is placed inside the same top-level package as the implementation. For example, if the range of implementations is declared as `myproj` and the range of contract assets as `myproj.contracts`, references inside the contract asset are allowed, and a reference to `myproj.service` is diagnosed as a reference to an implementation.

## REG_016

shikumi-contrace **MUST NOT** provide a means to place the declaration of ranges inside a contract asset.

title: Range declarations are not placed inside a contract asset

level: MUST NOT

detail: If the names of the packages of tests or implementations were written inside a contract asset, the contract would know them even as strings, which goes against the purpose of independence.

related: [IND_001](independence.md#ind_001)

## REG_017

shikumi-contrace **MUST NOT** assume the kind or the layout of implementations (the structure of packages, names, whether they are re-exported). It learns the location of an implementation only from a binding or from the user's declarations.

title: The layout of implementations is not assumed

level: MUST NOT

related: [IND_005](independence.md#ind_005)

## REG_018

shikumi-contrace **SHOULD** limit its dependence on Shikumi's public API to a small number of names and gather it in one place internally.

title: Dependence on Shikumi's public API is kept small and in one place

level: SHOULD

detail: The public API of Shikumi used in the prototype was covered by seven: `Cardinality`, `ClassBinding`, `InformationType`, `attach_information`, `class_binding`, `information_of` and `record_descriptor_use`. Gathering the dependence in one place prepares for changes to Shikumi's public API and for future replacement.

## REG_019

shikumi-contrace **SHOULD** provide a validation rule that checks combinations of a standard relation word and a standard clause kind that are not normally used (`violates` on a postcondition or an invariant). The diagnostics are reported as warnings. A custom vocabulary is not subject to this rule.

title: A rule checks unusual combinations of standard words

level: SHOULD

detail: The targets are limited to combinations among the standard vocabulary. No diagnostic is emitted on the grounds that a vocabulary is not included in the standard vocabulary (VOC_004). The combinations are those that the specification of the standard vocabulary (STD_013) says are not normally used.

## REG_020

shikumi-contrace **MUST** provide a validation rule that checks that a contract dependency declaration is placed in a contract class body, that its target is a contract, and that the dependency relationship is acyclic. Violations are reported as diagnostics.

title: A rule checks contract dependencies and rejects cycles

level: MUST

related: [CTR_014](contract.md#ctr_014), [CTR_015](contract.md#ctr_015), [SYN_025](syntax.md#syn_025)

detail: Ordinary `depends_on` declarations accept only references to class objects that already exist, which makes cycles difficult to create. Validation also checks runtime states created through low-level Shikumi APIs and confirms that no cycle exists. Validation does not automatically retire or rewrite anything (REG_006).

## REG_021

shikumi-contrace **MUST** provide a validation rule that checks that a violation-behavior declaration is placed on a precondition clause. A violation is reported as a diagnostic.

title: A rule checks the position of precondition violation behavior

level: MUST

related: [CTR_016](contract.md#ctr_016), [SYN_026](syntax.md#syn_026)

## REG_022

shikumi-contrace **MUST NOT** inspect the syntax of a test body, the presence of exception checks, or a particular rejection mechanism on the grounds of a declared violation behavior. It also **MUST NOT** emit a diagnostic merely because a `REJECTED` clause has no related violation test, or because an `OUT_OF_SCOPE` clause has one.

title: Validation does not infer test shape from violation behavior

level: MUST NOT

related: [AIM_016](aim.md#aim_016)

## REG_023

shikumi-contrace **MUST** provide a validation rule that checks that `ports` contains no contract, defines no function or class other than Protocols and data, and that the `__init__` of `ports` itself holds no definitions. A violation is reported as a diagnostic.

title: A rule checks that the boundary types hold only Protocols and data

level: MUST

related: [IND_012](independence.md#ind_012)

detail: The diagnostic codes are `ports-contract` (it contains a contract), `ports-behavior` (it defines a function, or a class that is neither data nor a Protocol) and `ports-definition-in-init` (the `__init__` of `ports` holds a definition). What is recognized as data is a dataclass, a NamedTuple, a TypedDict and an Enum.

## REG_024

shikumi-contrace **MUST** provide a validation rule that checks that `ports` does not refer to a contract or to shikumi-contrace, and that the `__init__` of a parent package on the way to importing `ports` does not import a contract or shikumi-contrace. A violation is reported as a diagnostic.

title: A rule checks that the boundary types do not drag a contract along

level: MUST

related: [IND_013](independence.md#ind_013)

detail: The diagnostic codes are `ports-reference` (a reference from `ports` itself) and `ports-parent` (an import in the `__init__` of a parent package). The parent packages include the package of the contract asset. The check of parent packages reads the import statements in the source of `__init__`. References to tests and implementations are detected by the existing rule (`independence`), because `ports` is in the range of contract assets.

## REG_025

When the user declares the ranges, and a `ports` that a contract module refers to is not in the declared range of contract assets, shikumi-contrace **MUST** report it as a diagnostic.

title: A declared range that leaves out the boundary types is reported

level: MUST

related: [IND_010](independence.md#ind_010)

detail: A declared range replaces a derived range (REG_011), so `ports` is not included automatically. If it is left out, `ports` escapes the check. Which `ports` is treated as boundary types on the contract-asset side follows the same rule as REG_012; an unrelated dependency package named `ports` is not included. The diagnostic code is `ports-undeclared`.

## REG_026

shikumi-contrace **MUST** provide a validation rule that checks that a contract module does not define a Protocol that is not the subject type of any contract. A violation is reported as a diagnostic.

title: A rule checks that value shapes are not defined in contract modules

level: MUST

related: [IND_011](independence.md#ind_011)

detail: The diagnostic code is `shape-outside-ports`. Only Protocols defined directly in the module are targeted. Data types such as dataclasses are not.

## REG_027

shikumi-contrace **MUST** express the structure of the package that holds `ports` directly, that is, that `ports` is a package whose direct children are only modules, as a Shikumi structure specification, and **MUST** check conformance to it. The structure specification is published as `CONTRACT_ASSET_STRUCTURE`. A violation is reported as a diagnostic.

title: The structure of the contract asset is a Shikumi structure specification

level: MUST

related: [IND_010](independence.md#ind_010)

detail: A Shikumi structure specification is written relative to its root and has no name for the root itself. For this reason the name of the package of the contract asset is arbitrary, and `ports` is the only fixed name. The other children directly below the root are modules or sub-packages of any name. `ports` is not required, because a contract that has no shapes of values needs no `ports`. A structure specification deals only with topology, so what is inside a module (the kind of definitions, references) is outside its scope (IND_012, IND_013). The diagnostic code is `ports-structure`, and it includes the message of Shikumi's structure diagnostic. The published specification can be passed as it is to Shikumi's own validation (`structure_specification` of `validate`).

## REG_028

shikumi-contrace **MUST** report as a diagnostic the case in which the package that holds `ports` directly contains a test or an implementation, and the case in which `ports` is outside any package (at the top level).

title: A rule checks that ports is placed directly inside a contract asset

level: MUST

related: [IND_015](independence.md#ind_015)

detail: The diagnostic code is `ports-placement`. The ranges of tests and implementations are the declared ones or the derived ones. Derivation uses only the ranges the tests declared, so an implementation that is not bound is overlooked. That is the direction of oversight, not of false detection.
