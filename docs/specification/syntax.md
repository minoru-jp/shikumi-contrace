# Descriptors and Syntax

Defines the names and syntax of the descriptors used on the contract side and on the test side. The `@=` form is used inside a class body, and decorators are used just before their target. Words are imported and used as bare names.

## SYN_001

Declarations in the `@=` form are written inside a class body. Declarations in the decorator form are written just before a function, a method or a class.

title: The @= form goes in class bodies; the decorator form goes before the target

level: MUST

detail: A test function or method has no body, so declarations on the test side are written in the decorator form.

## SYN_002

The subject type is declared with the descriptor `subject`, written as `subject @= <subject>` in the body of the contract class.

title: Writing the subject type: subject

level: MUST

related: [CTR_002](contract.md#ctr_002)

## SYN_003

Which element of the subject type a member represents is declared with the descriptor `member`, written as `member @= <member>` in the body of the member's class. When the subject type is a callable type, it can also be written in the body of the contract (CTR_012).

title: Writing the member: member

level: MUST

related: [CTR_007](contract.md#ctr_007)

## SYN_004

The clause kind is declared with the descriptor `kind`, written as `kind @= <kind>` in the body of the clause's class.

title: Writing the clause kind: kind

level: MUST

related: [CTR_004](contract.md#ctr_004)

## SYN_005

The values of the standard clause kinds (`PRE`, `POST`, `INV`) are upper-case identifiers, and descriptors, relation words and annotation words are lower-case identifiers.

title: Values are upper-case; descriptors and words are lower-case

level: MUST

detail: So that a value and the descriptor used to write it can be told apart by the shape of the name.

## SYN_006

An annotation word **MUST** work in both forms with a single word: the `@=` form in a class body (`rationale @= "text"`) and the decorator form (`@rationale("text")`, or `@critical` without text). Whichever form is used, the information attached is the same.

title: An annotation word can be written in both forms

level: MUST

detail: On the contract side too, the text may be written in the decorator form. There are several ways to write it, but the result is the same, so it is not a way to write something wrongly.

related: [STD_041](standard_vocabulary.md#std_041)

## SYN_007

An annotation word without text (such as `security` or `critical`) is written as a bare decorator `@<word>` just before its target. A form that writes only a tag, without text, inside a class body is not provided.

title: A tag without text is a bare decorator

level: MUST

detail: The way of writing tags is aligned between the contract side and the test side. The `@=` form in a class body is used for annotations that have text.

related: [STD_040](standard_vocabulary.md#std_040)

## SYN_008

A relation word is written in the decorator form, just before a test function or method. As in `@upholds(<clause>, ...)`, several clauses can be given in one declaration.

title: Writing relation words: decorators taking clauses

level: MUST

related: [TST_002](test_side.md#tst_002)

## SYN_009

The clause given to a relation word **MUST** be a reference to the class of the contract itself. If something that is not a class, such as a string, is given, a `TypeError` is raised at the time the decorator is applied. Whether the given class is a clause is not checked when the decorator is applied.

title: A relation word takes clause classes, not strings

level: MUST

related: [TST_002](test_side.md#tst_002)

## SYN_010

A relation word is attached to a test function or method. If it is attached to a test class, a `TypeError` is raised at the time the decorator is applied.

title: Relation words are for test functions and methods

level: MUST

detail: The meaning of attaching it to a class (such as applying it to all tests in the class) is not defined for the time being. To avoid a state in which nothing happens silently, it is made an error. The meaning will be defined when the need is confirmed.

## SYN_011

A descriptor or a word in the `@=` form **MUST** be imported and used as a bare name. An `@=` that goes through attribute access (for example `c.note @= "text"`) **MUST NOT** be used, because it overwrites the descriptor held by the module.

title: Use bare names for the @= form

level: MUST

detail: The decorator form may be written through a namespace (`@c.note("text")`). When the name of a word collides with a user's variable name, import it under an alias.

## SYN_012

shikumi-contrace **MUST** provide generators with which users create the relation words, annotation words, clause kinds and violation behaviors of a custom vocabulary (`define.relation(name)`, `define.annotation(name)`, `define.kind(name)`, `define.violation(name)`). The standard vocabulary is created with the same generators.

title: Generators create custom and standard words alike

level: MUST

detail: A generated word is bound to a variable of the same name, as in `flaky = define.annotation("flaky")`. The variable name and the string coincide, but the name of the word does not depend on the variable name. The name of the generators is `define` rather than `words`, so that it is unlikely to collide with a user's variable names.

## SYN_013

Descriptors and words **MUST** have type annotations with which a type checker can check, distinguishing them, the form with text (`@note("text")`), the form without text (`@security`), and the `@=` form.

title: Type annotations distinguish the forms

level: MUST

detail: The type variable that represents the target of a decorator is constrained to functions, methods and classes. Without the constraint, the form with text is mistaken for the form that receives the target.

## SYN_014

The order in which information attached in the decorator form is held is the order of application (the reverse of the order written). The order in which information attached in the `@=` form is held is the order written.

title: Order in which information is held

level: INFORMATIVE

detail: The reading API absorbs this difference and returns information in the order written (RDG_009).

## SYN_015

A binding is written as the decorator `@binds[<subject>](<implementation>, ...)`, just before a test class or a function or method.

title: Writing the binding: binds

level: MUST

related: [IND_007](independence.md#ind_007)

## SYN_016

`binds` **MUST** be given the subject type as a type argument. If the type argument is omitted, a `TypeError` is raised at the time the decorator is applied.

title: binds takes the subject type as a type argument

level: MUST

detail: Without the type argument, a type checker cannot check the conformance of the implementation. A way of writing that looks as if it checks but does not actually check is not provided.

## SYN_017

`binds` can be given one or more implementations. An implementation is either something that produces the subject type (a class, or a function that returns one) or the subject type itself (a function, a module, an object). Whether construction needs arguments does not matter.

title: binds takes implementations: factories or objects

level: MUST

detail: For a contract about a single function, the function itself is given; for a contract about a collection of functions, the module itself is given. Whether an implementation produces the thing or is the thing is not distinguished at run time.

related: [CTR_012](contract.md#ctr_012)

## SYN_018

A binding applies to the target it is attached to. When attached to a test class, it applies to the tests in that class. When a binding is attached to both the class and a function or method in it, both apply. A binding for a whole module is not provided for the time being.

title: A binding applies to the decorated target

level: MUST

detail: Unlike a relation word (SYN_010), a binding can be attached to a test class. A binding is a declaration of which implementation a test is for, and the class is the natural unit.

## SYN_019

The type annotations of `binds` **MUST** be such that a type checker can detect that an implementation does not conform to the subject type.

title: A non-conforming implementation is detected by the type checker

level: MUST

detail: When the contract is carried away and the implementation is rebuilt, whether the new implementation conforms to the subject type can be known before running. The check of conformance was confirmed with basedpyright and mypy. The same holds when the implementation is a function, a module, a generic function or an overloaded function.

## SYN_020

A binding is a declaration, not an enforcement. shikumi-contrace does not verify whether a test actually uses the implementation it is bound to.

title: A binding is a declaration, not an enforcement

level: INFORMATIVE

## SYN_021

A descriptor in the `@=` form **MUST** check its value at the time `@=` is evaluated. It **MUST NOT** raise an exception in the processing that runs when the class is created.

title: Values of @= descriptors are checked when @= is evaluated

level: MUST

detail: On Python 3.11, an exception raised in the processing that runs when the class is created is wrapped in `RuntimeError`, which makes the cause hard to see. On Python 3.12 and later, the original exception is raised as it is.

## SYN_022

Users can import metamk's `Mk` under the name `Phase`, and `phase_of` under the same name, from `shikumi_contrace`.

title: metamk phase names can be imported from shikumi_contrace

level: MUST

detail: For example, `from shikumi_contrace import Phase` can be written. `Phase` refers to the same object as `from metamk import Mk`.

## SYN_023

A re-export **SHOULD** expose its public name with an explicit alias or with `__all__`.

title: Re-exports are written in the explicit form

level: SHOULD

detail: For example, write `from metamk import Mk as Phase`. Some type checkers do not treat a re-export without an explicit form as a public name (such as mypy with `--no-implicit-reexport`).

## SYN_024

A descriptor in the `@=` form **MUST** annotate the type of the result of `@=` as the type of the descriptor itself.

title: The result of @= is annotated as the descriptor itself

level: MUST

detail: `name @= value` in a class body is an assignment to the name `name`, and mypy reports an error on every line if the type of the result differs from the type of `name`. If the result is annotated as the type of the descriptor itself (`Self`), both basedpyright and mypy accept it. At run time, what is returned is a temporary binding that Shikumi removes when the class is created.

## SYN_025

A contract dependency is written with the `depends_on` descriptor as `depends_on @= <contract>` in the class body of the dependent contract. The dependency must be a reference to the other contract class itself, not a string. Multiple dependencies are written by repeating `depends_on @= ...` in the desired order.

title: Writing contract dependencies: depends_on

level: MUST

related: [CTR_014](contract.md#ctr_014)

detail: Because only references to class objects are accepted, ordinary declarations do not create forward references to contracts that have not yet been defined. Cycles are also reported by validation.

## SYN_026

A violation behavior is written with the `on_violation` descriptor as `on_violation @= <behavior>` in the class body of a precondition clause. The standard values are `OUT_OF_SCOPE` and `REJECTED`. A custom violation behavior is created with `define.violation(<name>)`.

title: Writing precondition violation behavior: on_violation

level: MUST

related: [CTR_016](contract.md#ctr_016)

detail: `on_violation` does not specify the implementation mechanism used on violation. Even `REJECTED` does not imply raising an exception or using `pytest.raises`.

## SYN_027

The type argument of `binds` can be the class of the subject type itself, or a generic class given type arguments (`Subject[Handle]`). What the binding records is the class before the type arguments were given (`Subject`). On the contract side, the class without type arguments is written as `subject @= Subject`.

title: binds accepts a generic subject given type arguments

level: MUST

related: [IND_006](independence.md#ind_006)

detail: When an implementation returns a value of its own type and another method takes that value (for example `reserve`, which returns a reservation, and `release`, which takes one), a contract can state "what was handed out is what is taken back" with a generic Protocol whose type is a type variable, without bringing the type of the implementation into the contract. Writing `@binds[Inventory[Reservation]](Impl)` in the binding makes the type checker check conformance including the type arguments (confirmed with basedpyright and mypy). The type arguments exist only for type checking and are not recorded in the binding. Reading returns the class before the type arguments were given. A generic class without type arguments is also accepted at run time; depending on the settings of the type checker, it may warn about the missing type arguments. Type arguments can be given only to a class. A union (`A | B`), `Annotated` and the like are not accepted as a subject type and raise `TypeError` (SYN_016).
