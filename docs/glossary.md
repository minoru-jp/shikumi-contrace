# shikumi-contrace Glossary

Terms for the main concepts shared by the specification and documents of shikumi-contrace. Terms of Shikumi are not redefined.

## Contract

An entity (a class) that describes the promises of the behavior of one subject type as a set of clauses. It contains the declaration of the subject type, and clauses and members.

A contract is a concept for tests and does not affect the design of the implementation.

## Subject type

The type that the clauses of a contract are about. It is a structural type (Protocol) defined by the contract itself, not the class of the implementation itself. An implementation conforms to the subject type structurally, without importing the contract.

## Member

A nested class in a contract that represents an element of the subject type, such as a method, that is the target of individual clauses. Since the granularity Shikumi handles is down to the class, clauses per method are also expressed with classes. When the subject type is a callable type, the contract itself may represent the member.

## Clause

An entity in a contract that states one promise in one sentence. It is written as a class, and its docstring is the clause statement. Clauses about the subject type as a whole are placed directly under the contract, and clauses about a member are placed under that member.

## Clause kind

Information that shows which of a precondition, a postcondition, an invariant and so on a clause is. The precondition, the postcondition and the invariant are provided as the standard vocabulary, but users are not prevented from adding kinds of their own.

## Precondition

A condition that the caller of the target must satisfy before the call. The behavior of the target for a call that violates it can also be described as a clause of a precondition.

## Postcondition

A condition that the target guarantees after a call to it has succeeded.

## Invariant

A condition that the target keeps before and after calls. The invariant here is a kind of clause in a contract, and is a different concept from the invariant in the glossary of Shikumi, which the semantic system of Shikumi itself must keep.

## Annotation

Supplementary information attached to a clause of a contract or to a test. It tells humans and LLMs the reason for a decision, the intent of a boundary, cautions and the like. Whether it is used at run time or not, the fact that it is written has meaning in itself.

## Relation

A declaration that states what a test does to which clause of a contract. For example, relations such as checking the violation of a clause or checking that a clause holds are declared just before the test.

## Standard vocabulary

The vocabulary that shikumi-contrace provides. It includes clause kinds, violation behaviors, relation words and annotation words. The standard words and their meanings are defined in the specification of the standard vocabulary.

## Custom vocabulary

A vocabulary that users define and add. It consists of values created with the same generators as the standard vocabulary, and it can be used in the same positions as the standard vocabulary. shikumi-contrace does not reject a vocabulary because it is unknown, and no registration is needed to use it.

## Binding

Tying the subject type of a contract to an actual implementation, and the declaration of that. Since a contract and an implementation do not know each other, the binding is held by the test side.

## Implementation

The code under test. It may be a class, a function or a module. It does not import the contract, and it conforms structurally to the subject type of the contract.

## Conformance

That an implementation satisfies the structure that the subject type of a contract asks for (the signatures of methods, attributes and so on). It is by structural subtyping, not by inheritance by name.

## Contract asset

An independent module or package that contains contracts and the subject types the contracts define. It is placed separately from tests and implementations, and is the unit with which only the contract can be carried away, for example in a rebuild from scratch. A contract asset depends on neither tests nor implementations.

## Core

The part of shikumi-contrace that does not depend on a specific test runner. It includes the vocabulary, information types, descriptors, validation rules and the re-export of metamk, and it does not import pytest. It is desirable that the part of shikumi-contrace that a contract asset imports be limited to the core.

## pytest integration

The optional part of shikumi-contrace that depends on pytest. It reads the information attached by the core from the tests collected by pytest, and provides the necessary minimum of features, such as displaying contract information. Without installing it, the features of the core can be used.

## Relation word

A word that expresses what stance a test takes toward a clause. The standard relation words do not repeat the kind of the clause and express only the stance.

## Annotation word

A word that expresses the nature of an annotation. Words for aspects such as explanation, domain, severity, status and verification are provided as the standard vocabulary.

## Generator

A function that creates a relation word, annotation word, clause kind or violation behavior. The standard vocabulary and a custom vocabulary are both created with the same generators.

## Contract dependency

A directional relationship expressing that the continued relevance or validity of one contract presupposes the continued relevance or validity of another. When the dependency is changed or retired, the dependent contract becomes a subject for re-evaluation. It does not mean logical implication or automatic retirement when the dependency changes.

## Violation behavior

Information expressing how far a precondition clause promises behavior for a call that does not satisfy the precondition. By itself, it does not prescribe whether the implementation handles that call with an exception, a return value, a protocol response, or another mechanism.

## Boundary types

The shapes of values that a contract and an implementation want to share (Protocols and data types that appear in the arguments and return values of the methods of the subject type), placed in the `ports` package directly inside the contract asset. They are part of the contract asset, have no behavior, and refer to neither contracts nor shikumi-contrace. Whether an implementation imports them is up to the implementation.
