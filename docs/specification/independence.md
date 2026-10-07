# Independence of Contracts

Defines the rules for carrying only the contract away as an independent asset when the design or the implementation is rebuilt from scratch. Tight coupling between contracts and tests is prevented by structure.

## IND_001

A contract **MUST** be placed in a module or package separate from tests and implementations, that is, in a contract asset. This holds even when the contract is small.

title: Contracts live in a separate contract asset

level: MUST

detail: So that only the contract can be carried away as an independent asset when, after the design and implementation have progressed to some extent, a dead end is reached or a decision is made to rebuild from scratch.

related: [CTR_001](contract.md#ctr_001)

## IND_002

A contract asset **MUST NOT** hold references to tests. This holds whether the reference takes the form of a module, a class, a function or a value.

title: A contract asset does not refer to tests

level: MUST NOT

detail: By defining, structurally, that a contract cannot refer to tests, tight coupling between contracts and tests is prevented. The correspondence from a contract to tests is held by the test side as relations.

## IND_003

A contract asset **MUST NOT** hold references to implementations. This holds whether the reference takes the form of a module, a class, a function or a value.

title: A contract asset does not refer to implementations

level: MUST NOT

detail: To prevent a contract from becoming impossible to import when the implementation is lost in a rebuild from scratch. Instead of the types of an implementation, a contract uses structural types it defines itself.

related: [CTR_003](contract.md#ctr_003)

## IND_004

A contract asset **SHOULD** keep its runtime dependencies small so that it can be loaded where the contract is carried to. The part of shikumi-contrace that a contract asset imports **SHOULD** be limited to the core. shikumi-contrace does not enforce this guidance.

title: Guidance: keep the runtime dependencies of a contract asset small

level: INFORMATIVE

detail: If a library that the contract depends on is absent where the contract is carried to, the contract cannot be loaded. Types of third-party libraries can avoid runtime imports by appearing only inside type annotations. Concretely, the evaluation of annotations is deferred (`from __future__ import annotations`) and the import of the types is placed inside `if TYPE_CHECKING:`. Even with this style, a type checker can check the real types. However, to check types, that library must be in an environment visible to the type checker.

## IND_005

shikumi-contrace **MUST NOT** impose requirements that constrain how an implementation is written, such as an implementation importing a contract or shikumi-contrace, or inheriting from a type of a contract.

title: Contracts do not shape the implementation

level: MUST NOT

detail: A contract remains a concept for use in tests. The existence of a contract must not affect the design of the implementation.

related: [AIM_001](aim.md#aim_001)

## IND_006

An implementation **MUST** conform to the subject type by structural subtyping, not by inheritance by name.

title: Conformance is structural

level: MUST

related: [CTR_003](contract.md#ctr_003)

## IND_007

The binding that ties the subject type of a contract to an implementation **MUST** be placed on the test side.

title: Binding is held by the test side

level: MUST

detail: A contract and an implementation do not know each other, so only a test can know both.

## IND_008

The direction of dependencies is as follows. A test depends on both the contract and the implementation, and the contract and the implementation do not know each other.

```text
test ──▶ contract asset
  └─────▶ implementation

contract asset ──▶ (depends on neither tests nor implementations)
```

title: Direction of dependencies

level: INFORMATIVE

## IND_009

shikumi-contrace **MUST NOT** restrict a contract asset from depending on anything other than tests and implementations.

title: Dependencies other than tests and implementations are not restricted

level: MUST NOT

detail: Restrictions are limited to the boundaries of packages declared by the user (references from a contract asset to tests and implementations). Restricting other dependencies would become an unexpected pitfall for users, since not all use cases can be anticipated. A classification such as standard library versus third-party library is not used as a basis for restriction either.

## IND_010

The shapes of values that a contract and an implementation share, that is, the boundary types, **MUST** be placed in a package named `ports`. `ports` is placed directly inside the package of the contract asset. The name of the package of the contract asset is arbitrary.

title: Boundary types live in a package named ports, directly inside the contract asset

level: MUST

related: [CTR_003](contract.md#ctr_003)

detail: The arguments of the methods of a subject type are contravariant, so when an implementation receives them with its own concrete class, it cannot accept the whole range that the contract promised, and the type checker rejects it. Instead of the implementation writing the same shape twice with a Protocol of its own, the boundary types are shared. The layout is a `ports/` package directly inside `contract/` (the contract asset; the name is arbitrary), with Protocols and data written in the modules inside `ports/`. It has to be a package so that the structure stays the same whether the project is small or large. The name is fixed to `ports` so that derivation and checking can find the boundary types without configuration (REG_012, REG_027). It is placed directly inside the package of the contract asset so that the contract can be carried away as a single directory, and the range can be declared with a single root. This rule assumes the use in which the contract is written first and the implementation is built afterwards; whether an implementation imports from `ports` is up to the implementation (IND_005).

## IND_011

A contract module **MUST NOT** define a Protocol that is not the subject type of any contract. The shapes of values are placed in `ports`.

title: A contract module defines no Protocol other than subject types

level: MUST NOT

related: [CTR_003](contract.md#ctr_003)

detail: The only Protocols that may be placed in a contract module are the subject types of contracts. A generic subject type (such as `Inventory[R]`) is also a subject type. The shapes of values that appear in the arguments and return values of methods (`Reservation`, `Order` and the like) are not subject types, so they are placed in `ports`. Only Protocols are detected; placing a data type such as a dataclass in a contract module is not detected.

## IND_012

The modules inside `ports` **MUST** define only Protocols and data (dataclasses, NamedTuples, TypedDicts, Enums). Type aliases, type variables and constants may also be placed there. Contracts, functions and any other classes **MUST NOT** be defined in them. The `__init__` of `ports` itself holds no definitions and may only re-export what the modules inside define.

title: The boundary types hold only Protocols and data, defined in modules

level: MUST

related: [CTR_003](contract.md#ctr_003)

detail: Boundary types are for sharing shapes and have no behavior. Methods that a dataclass has are allowed as part of the data type. Classes other than those listed, such as exception classes, are placed on the implementation side or outside the contract. Definitions are not placed in `__init__` so that there is one place for them, and a reader can find the contents of `ports` by following the modules.

## IND_013

`ports` **MUST NOT** refer to contracts, shikumi-contrace, tests or implementations. The `__init__` of a parent package on the way to importing `ports` (including the `__init__` of the package of the contract asset) **MUST NOT** import contracts or shikumi-contrace.

title: The boundary types refer to no contract, no shikumi-contrace, no test and no implementation

level: MUST NOT

detail: References to tests and implementations are covered as they are by the rules of the contract asset (IND_002, IND_003). References to contracts and shikumi-contrace are prohibited so that, when an implementation imports from `ports`, neither a contract nor shikumi-contrace is dragged along (IND_005). Importing `contract/ports/` runs `contract/__init__.py` first, so the `__init__.py` of the contract asset is kept empty, or at least does not import contracts.

## IND_014

For the boundary types, the following is desirable. Make them depend only on the standard library (IND_004). Whether an implementation imports from the boundary types is up to the implementation, and shikumi-contrace neither requires nor forbids it (IND_005, IND_009). If it does, `ports` is carried along when the contract is carried away.

title: Guidance: depend only on the standard library, and carry ports along

level: INFORMATIVE

detail: An opaque handle that is only handed out by one method and taken back by another can be expressed without sharing, by a generic subject type (SYN_027). When a contract is laid over an existing implementation, the implementation cannot be changed, so the argument types on the contract side are designed to be wide. That the dependency on the standard library is not checked follows from IND_009.

## IND_015

The package that holds `ports` directly, that is, the package of the contract asset, **MUST NOT** contain tests or implementations.

title: The package that holds ports contains no test and no implementation

level: MUST NOT

detail: A contract asset is placed apart from tests and implementations (IND_001). This rule applies that principle to the package that holds `ports` directly. `ports` cannot be placed directly inside the package of a whole project in which implementations also live. Even when the contracts are divided among several sub-packages, it is fine as long as `ports` is directly inside the package of the contract asset. The same rule applies whether the ranges are declared or derived. Derivation uses only the ranges the tests declared, so an implementation that is not bound is overlooked (there is no false detection).
