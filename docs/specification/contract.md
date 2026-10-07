# Structure of a Contract

Defines the structure used when a contract is written as nested classes: a subject type, members and clauses. Shikumi handles granularity only down to the class, so clauses per method are also expressed with classes.

## CTR_001

A contract **MUST** be written as a Python class that contains the declaration of a subject type and clauses.

title: A contract is a class

level: MUST

related: [AIM_001](aim.md#aim_001)

## CTR_002

A contract **MUST** name its one subject type by a reference to the type itself. It **MUST NOT** name it by a string.

title: A contract names one subject type by reference

level: MUST

detail: Naming the subject type by a string generalizes the contract more than necessary and makes it impossible to navigate from the IDE. A contract is written with the type kept.

## CTR_003

A type defined by a contract **MUST** be a structural type (Protocol). A concrete class such as a dataclass **MUST NOT** be placed in a contract.

title: Types defined by a contract are structural

level: MUST

detail: So that an implementation can conform structurally, keeping its own types, without importing the contract. A type that represents a value is also expressed as a structural type that has the required attributes as read-only properties.

related: [AIM_001](aim.md#aim_001)

## CTR_004

A clause **MUST** be written as a class nested in a contract or a member, and the docstring of the class **MUST** be the clause statement. One clause states one promise in one sentence.

title: A clause is a nested class whose docstring is the clause statement

level: MUST

## CTR_005

A clause about the subject type as a whole **MUST** be placed directly under the contract.

title: Clauses about the whole subject type sit directly under the contract

level: MUST

## CTR_006

A member **MUST** be written as a nested class directly under the contract, representing a method of the subject type or the like, and the clauses about that member **MUST** be placed inside the member's class. If the subject type is a callable type, CTR_012 **MAY** be followed instead.

title: A member is a nested class that holds the clauses of one method

level: MUST

detail: Shikumi does not treat a method, which is finer than a class, as an entity. So clauses per method are also expressed through a class that represents the method.

## CTR_007

A member **MUST** specify which member of the subject type it represents, as a reference to that member of the subject type.

title: A member refers to the member of the subject type

level: MUST

## CTR_008

The class name of a member **SHOULD** match the name of the member of the subject type it refers to. A mismatch is diagnosed. However, a contract that has both a declaration of the subject type and a declaration of a member (CTR_012) is not subject to this rule.

title: Member class names follow the referred member names

level: SHOULD

detail: It serves as insurance for detecting a drift that occurs when only the referred name changes in an IDE rename.

## CTR_009

The standard precondition and postcondition **MUST** be placed directly under an entity that represents a member (a member class, or a contract that has `member` by CTR_012). The standard invariant **MUST** be placed directly under a contract that has a declaration of the subject type. A different position is diagnosed. The clause kinds of the custom vocabulary are not subject to this positional rule.

title: Standard clause kinds have fixed positions

level: MUST

detail: Positions are given roles, while the words put in them are not restricted. The positional rule applies only to the standard vocabulary and does not obstruct the custom vocabulary. When a contract has both a declaration of the subject type and a declaration of a member, a precondition, a postcondition and an invariant can all be placed directly under the contract.

## CTR_010

An annotation **MAY** be attached to any of a contract, a member and a clause.

title: Notes may be attached to a contract, a member, or a clause

level: MAY

## CTR_011

A clause statement **SHOULD** be written so that its meaning is clear from that clause alone. A way of writing that cannot be understood without reading other clauses or tests is avoided.

title: A clause statement is readable on its own

level: SHOULD

## CTR_012

When the subject type is a callable type, that is, a Protocol that has only `__call__`, the contract class itself **MAY** represent that `__call__`. To do so, `member @= <subject>.__call__` is written in the body of the contract in addition to the declaration of the subject type. A member class is then unnecessary, and clauses of preconditions and postconditions can be placed directly under the contract.

title: A contract may itself stand for the single member of a callable subject type

level: MAY

detail: A contract about a single function is written with a Protocol that has only `__call__` (a callback protocol) as the subject type. No new descriptor is needed.

## CTR_013

A contract about a collection of functions (a module) is written with an ordinary subject type that has methods, and the module is bound as the implementation.

title: A contract for a module of functions uses an ordinary subject type

level: INFORMATIVE

detail: The syntax for binding a module is defined in the specification of descriptors and syntax.

## CTR_014

A contract may have contract dependencies on one or more other contracts. If `B` depends on `A`, a change or retirement of `A` means that the validity or continued relevance of `B` needs to be re-evaluated.

title: A contract may depend on other contracts

level: MAY

detail: A dependency is not a logical implication; it is a directional relationship for tracing the impact of changes. Changing or retiring the dependency does not automatically change or retire the dependent contract. A contract may have multiple dependencies.

## CTR_015

Contract dependencies must be acyclic. This prohibits not only direct mutual dependencies, but also dependencies that return to their origin through multiple contracts.

title: Contract dependencies are acyclic

level: MUST

## CTR_016

A precondition clause **MAY** have a violation behavior. The violation behavior expresses how far that clause itself includes, in its promise, calls that do not satisfy the precondition.

title: A precondition may declare how violation is treated

level: MAY

detail: Omitting a violation behavior is not the same as writing `OUT_OF_SCOPE`. Omission means that this information about behavior on violation has not been declared.
