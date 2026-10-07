# Declarations on the Test Side

Defines the declarations with which a test states, just before the test, what it does to which clause of a contract. The statement of a clause is written once on the contract side, and tests refer to it.

## TST_001

A test **MUST** be an ordinary function or method collected by the test runner. shikumi-contrace does not change the shape of a test.

title: Tests remain ordinary tests of the test runner

level: MUST

related: [AIM_003](aim.md#aim_003)

## TST_002

A test **MUST** be able to declare, just before the test, its relation to the clauses of a contract. The relation **MUST** point to the target clause by a reference to the entity of the contract itself. It **MUST NOT** point by a string.

title: A test declares its relation to clauses, by reference

level: MUST

related: [CTR_004](contract.md#ctr_004)

## TST_003

One test **MAY** be related to several clauses.

title: One test may relate to several clauses

level: MAY

detail: In tests based on contracts, one run may check both the rejection of a violation of a precondition and the preservation of an invariant at the same time.

## TST_004

A relation **MUST** be accompanied by a relation word that expresses the stance of the test toward the clause. The standard relation words are `upholds` (keep) and `violates` (break).

title: A relation carries a relation word

level: MUST

detail: The meaning of the standard relation words is defined in the specification of the standard vocabulary.

## TST_005

An annotation **MAY** be attached to a test.

title: Notes may be attached to a test

level: MAY

detail: It is used to tell people who later read the test, and LLMs, the reason for a decision, the intent of a boundary, and cautions that cannot be read from the clause or the test name.

## TST_006

A clause statement **SHOULD** be written once on the contract side and not repeated on the test side. A test name **SHOULD** express the concrete behavior the test checks.

title: Clause statements are not repeated on the test side

level: SHOULD

detail: When a test name and a clause name overlap, the same sentence has to be maintained in two places. The statement of a clause is placed in the contract, and the concrete behavior in the test name, separately.

related: [CTR_011](contract.md#ctr_011)

## TST_007

The binding that ties the subject type of a contract to an implementation **MUST** be written on the test side.

title: Bindings are written on the test side

level: MUST

related: [IND_007](independence.md#ind_007)

detail: The syntax of a binding is defined in the specification of descriptors and syntax.

## TST_008

The structure inside the body of a test is outside the scope of this specification, and shikumi-contrace does not prescribe it.

title: The inside of a test body is out of scope

level: INFORMATIVE

related: [AIM_008](aim.md#aim_008)
