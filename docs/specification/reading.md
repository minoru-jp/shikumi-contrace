# Reading Information

Defines the API that reads declared information so that the correspondence between clauses and tests can be traced. Because the pytest integration is kept to the necessary minimum, narrowing down and listing can be written by users with this API. The names of the API are defined in the specification of the names and placement of the public API.

## RDG_001

The core **MUST** provide an API that reads the information declared on contracts and tests. This API **MUST NOT** depend on any specific test runner.

title: A reading API independent of any test runner

level: MUST

related: [AIM_003](aim.md#aim_003)

## RDG_002

The reading API **MUST** be able to read the relations a test has (relation words and clauses), annotations and bindings.

title: Reading what a test declares

level: MUST

detail: A binding attached to a test class can also be read as a binding of the tests in that class (SYN_018). Resolving the class from the object of a function is done by `__qualname__` and is limited to classes at module level. From a method of an instance, the class of the instance can be followed, so a class defined inside a function can also be read. From the function object of a class defined inside a function, it cannot be followed. The pytest integration reads directly from the collected class, so it is not affected.

## RDG_003

The reading API **MUST** be able to read, from a contract, the list of clauses it has (including kinds, violation behaviors, clause statements and annotations).

title: Reading the clauses of a contract

level: MUST

## RDG_004

The reading API **MUST** be able to look up, from a clause, the tests related to that clause. The lookup is done within the range of tests the user passes.

title: Looking up the tests related to a clause

level: MUST

related: [AIM_001](aim.md#aim_001)

## RDG_005

The reading API **MUST** be able to list the clauses that no test with a relation is related to.

title: Listing clauses that no test is related to

level: MUST

detail: This list reports only whether a recorded relation exists. It does not infer whether a clause ought to have a test from the clause kind, violation behavior, or any other meaning.

related: [AIM_001](aim.md#aim_001)

## RDG_006

The reading API **MUST** only read information. It **MUST NOT** rewrite the content of contracts or tests.

title: The reading API only reads

level: MUST NOT

## RDG_007

For a function wrapped by a decorator, the reading API **MUST** follow the chain of `__wrapped__` and also read the information attached to the inner function. When information is attached to both the outer and the inner function, both are returned.

title: The reading API follows the __wrapped__ chain

level: MUST

detail: Information is attached to the identity of an object. If a declaration is inside another decorator (such as one that uses `functools.wraps`, or `mock.patch`), the information is attached to the inner function and not to the outer wrapper function. Without following the chain, such declarations would be overlooked.

## RDG_008

Test functions and methods are not treated as Shikumi entities. The information of a test is read directly from the objects of functions and methods.

title: Test functions are read directly, not as Shikumi entities

level: INFORMATIVE

detail: The standard structure of Shikumi treats classes as entities and does not treat functions and methods as entities. The validation framework of Shikumi is used for validating the contract side (classes), but the information of the test side is read with the reading API. Validation rules that concern the test side (such as REG_010) can also be implemented using the reading API.

## RDG_009

The reading API **MUST** return information in the order it was written. Information attached to the same target by decorators is returned from top to bottom, and information attached by `@=` in the body of a class is returned after the information attached by decorators, in the order written. Information of an outer wrapper is returned before that of the inner function.

title: Information is returned in the order it was written

level: MUST

detail: Decorators are applied from the bottom, so the order in which the attached information is held is the reverse of the order written (SYN_014). The reading API absorbs this.

## RDG_010

The reading API must be able to read, in written order, the contracts on which a contract directly depends. It must also be able to look up, within a range supplied by the user, the contracts that directly depend on a given contract. The reverse relationship is not stored; it is derived from the declared directional contract dependencies.

title: Reading contract dependencies in both directions

level: MUST

related: [AIM_003](aim.md#aim_003)
