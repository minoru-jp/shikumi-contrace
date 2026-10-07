# Purpose and Scope

Defines what shikumi-contrace exists for and what it does not aim at. The other specifications are read in the light of the purpose given in this document.

## AIM_001

The purpose of shikumi-contrace is to describe the promises of a piece of functionality as a contract, as an asset independent of the implementation and the tests, and to tie tests to the clauses of the contract, so that it can be traced which tests exist for which clause and which clause each test concerns. A contract does not affect the design of the implementation, and it can be carried over even when the design or the implementation is rebuilt from scratch.

title: Purpose: contracts as independent assets, traced by tests

level: INFORMATIVE

detail: The content of a contract (preconditions, postconditions, invariants) cannot be checked by types. Checking it is left to tests, so being able to trace the correspondence between clauses and tests becomes important.

## AIM_003

The core of shikumi-contrace **MUST NOT** depend on any specific test runner. Features specific to pytest are provided as an optional integration, kept to the necessary minimum.

title: Independent of any test runner; pytest support is optional

level: MUST

detail: The pytest integration is not placed at the center of shikumi-contrace. Without it, describing contracts, relating tests to them, and checking remain usable.

## AIM_004

shikumi-contrace **MUST** assume both humans and LLMs as writers and readers of its declarations.

title: Humans and LLMs as both writers and readers

level: MUST

detail: Assuming them as writers means requiring declarations that an LLM can write without mistakes. Assuming them as readers means requiring declarations that an LLM can read without misreading. A custom notation is not introduced merely because it is easier for humans to write.

## AIM_005

shikumi-contrace **MUST** be able to describe contracts based on preconditions, postconditions and invariants.

title: Expressing contracts of pre-conditions, post-conditions and invariants

level: MUST

detail: A contract here means Design by Contract: defining behavior by preconditions, postconditions and invariants. It does not mean verifying API contracts between services.

## AIM_006

shikumi-contrace **MUST** provide a standard vocabulary without obstructing custom vocabulary. The more free the vocabulary is, the better; this is a design principle.

title: Open vocabulary as a design principle

level: MUST

## AIM_007

shikumi-contrace **MUST** be built as a Shikumi specification body.

title: Built as a Shikumi specification body

level: MUST

detail: That Shikumi suits describing and validating contract information was confirmed with prototypes (Python 3.11 and 3.12). The Shikumi version it builds on is the current version (0.2.4) or later, with no upper bound.

## AIM_008

Structuring the inside of a test body (the separation of preparation, the call to the target, and verification) is not the responsibility of shikumi-contrace itself. shikumi-contrace re-exports the library metamk for that purpose.

title: Structuring the inside of a test body belongs to metamk, which is re-exported

level: INFORMATIVE

detail: The meaning and specification of the phases belong to metamk. shikumi-contrace deals with the contract side and with the relations between tests and contracts.

## AIM_009

Mechanisms for reusing test logic are not a goal of shikumi-contrace.

title: Non-goal: reusing test logic

level: INFORMATIVE

detail: Reusing test logic can be done with the standard mechanisms of the test runner, such as pytest's parametrize and fixtures. shikumi-contrace provides nothing that replaces them.

## AIM_010

Mechanisms that gather parameters, skips, expected exceptions and the like into the declarations of contracts and tests, and a custom notation for declaring parameters, are not goals of shikumi-contrace.

title: Non-goal: aggregating test-runner features into declarations

level: INFORMATIVE

detail: These can be done with the standard mechanisms of the test runner (PYT_004).

## AIM_011

Generating contracts or tests automatically, and deriving tests from contracts mechanically, are not goals of shikumi-contrace.

title: Non-goal: generating or deriving tests mechanically

level: INFORMATIVE

## AIM_012

Overlaying test results on the structure of a contract and displaying them (a contract view) is outside the scope of shikumi-contrace.

title: Non-goal: a contract view of test results

level: INFORMATIVE

detail: No feature is provided that lists the structure of a contract and shows test results per clause. Under parallel execution (pytest-xdist), collection happens on the workers, so overlaying results on the structure of a contract would also need additional design.

## AIM_013

Arrange / Act / Assert is sometimes recommended as the structure of a test, but it is only one example of a structure. It is neither a design principle nor a constraint of shikumi-contrace, and shikumi-contrace does not prescribe the structure of a test body.

title: Arrange / Act / Assert is one recommended structure, not a constraint

level: INFORMATIVE

## AIM_014

shikumi-contrace **MUST** depend on metamk, **MUST** re-export metamk's `Mk` under the name `Phase`, and **MUST** re-export `phase_of` under the same name. `Phase` **MUST** be the same object as metamk's `Mk`, and `phase_of` **MUST** be the same object as metamk's `phase_of`.

title: shikumi-contrace depends on metamk and re-exports its phase API

level: MUST

detail: The version of metamk is the current version (0.1.0) or later, with no upper bound. metamk has no dependencies and does not depend on pytest, so it does not undermine the fact that the core does not depend on a specific test runner (AIM_003).

## AIM_015

shikumi-contrace **MUST NOT** change the meaning of `Phase` or `phase_of`. The specification and maintenance of phases belong to metamk.

title: The meaning of the re-exported phase API is not changed by shikumi-contrace

level: MUST NOT

detail: `Phase` changes only the name to fit the shikumi-contrace context. Its behavior is identical to `metamk.Mk`.

## AIM_016

shikumi-contrace **MUST NOT** infer how a test body should be written from the meaning declared in a contract. It **MUST NOT** require a particular exception check, guard clause, test-runner-specific construct, or similar mechanism merely because of contract information.

title: Non-goal: inferring the shape of test code from contract meaning

level: MUST NOT

detail: A contract keeps semantic information for humans and LLMs to read as design intent. For example, `REJECTED` does not mean that a violation is represented by an exception. Unless another declaration fixes it, the implementation mechanism may be an exception, a failure-valued return, an HTTP response, or something else.
