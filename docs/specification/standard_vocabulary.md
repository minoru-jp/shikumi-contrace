# Standard Vocabulary

Defines the words that shikumi-contrace provides as standard. Words are values of a small number of open information types (clause kinds, violation behaviors, relations, annotations), and a custom vocabulary can be made with the same generators. The identifiers of the standard words are in English, and their Japanese names are given alongside in parentheses in the Japanese version of this document.

## STD_001

The standard clause kind `PRE` (precondition) represents a clause of a precondition.

title: Clause kind: PRE

level: MUST

detail: The rules for the position where it is placed are defined in the specification of the structure of a contract.

related: [CTR_009](contract.md#ctr_009)

## STD_002

The standard clause kind `POST` (postcondition) represents a clause of a postcondition.

title: Clause kind: POST

level: MUST

detail: The rules for the position where it is placed are defined in the specification of the structure of a contract.

related: [CTR_009](contract.md#ctr_009)

## STD_003

The standard clause kind `INV` (invariant) represents a clause of an invariant.

title: Clause kind: INV

level: MUST

detail: The rules for the position where it is placed are defined in the specification of the structure of a contract.

related: [CTR_009](contract.md#ctr_009)

## STD_004

The standard violation behavior `OUT_OF_SCOPE` (out of contract) expresses that the clause makes no promise about the behavior of a call that does not satisfy the precondition.

title: Violation behavior: OUT_OF_SCOPE

level: MUST

detail: It does not mean that an upstream layer necessarily checks the condition, or that the implementation does nothing. It only leaves the behavior of a violating call outside the promise of this clause.

related: [CTR_016](contract.md#ctr_016)

## STD_005

The standard violation behavior `REJECTED` (reject) expresses that the clause promises that the implementation does not accept a call that does not satisfy the precondition as a normal success.

title: Violation behavior: REJECTED

level: MUST

detail: The mechanism of rejection is not prescribed. It may be an exception, a failure-valued return, a protocol response, or another mechanism; no particular guard clause or test syntax is required.

related: [CTR_016](contract.md#ctr_016)

## STD_010

The standard relation word `upholds` (keep) expresses that a test checks, in a situation where the clause is in effect, that the clause is kept and holds.

title: Relation word: upholds

level: MUST

detail: For a precondition, it checks that an input that satisfies the condition (including boundaries) is accepted; for a postcondition, that the postcondition holds; for an invariant, that the invariant is preserved.

related: [VOC_001](vocab.md#voc_001)

## STD_011

The standard relation word `violates` (break) expresses that a test creates a situation in which the clause is deliberately broken and checks the behavior at that time.

title: Relation word: violates

level: MUST

detail: It is mainly used for preconditions. It is not normally used for postconditions and invariants.

related: [VOC_001](vocab.md#voc_001)

## STD_012

A standard relation word **MUST** express only the stance of a test toward a clause. It **MUST NOT** express the kind of the clause.

title: Relation words express only the stance

level: MUST NOT

detail: The kind of a clause is held by the clause itself. Repeating it in a relation word would mean maintaining the same information in two places. Users who need a word that includes the kind (for example `preserves`) can define it as a custom vocabulary.

related: [VOC_001](vocab.md#voc_001)

## STD_013

The combinations of the standard relation words and the clause kinds are used as follows.

| Clause kind | `upholds` | `violates` |
| --- | --- | --- |
| `PRE` | An input that satisfies the condition (including boundaries) is accepted | The behavior on violation is checked with a call that breaks the condition |
| `POST` | The postcondition holds | Not normally used |
| `INV` | The invariant is preserved | Not normally used |

title: How relation words combine with clause kinds

level: INFORMATIVE

detail: Diagnosing combinations that are not normally used is defined in the validation rules (REG_019).

related: [VOC_001](vocab.md#voc_001)

## STD_020

The standard annotation word `note` (supplement) expresses a supplement in general. It is the default annotation word.

title: Annotation word: note

level: MUST

detail: Aspect: explanation. Main positions: all.

related: [VOC_001](vocab.md#voc_001)

## STD_021

The standard annotation word `rationale` (reason) expresses the reason a promise exists.

title: Annotation word: rationale

level: MUST

detail: Aspect: explanation. Main positions: contract, member, clause. It is the information most easily lost when a contract is carried over to another implementation.

related: [VOC_001](vocab.md#voc_001)

## STD_022

The standard annotation word `caution` (caution) expresses a point that is easy to misunderstand and a point where a violation has a large impact.

title: Annotation word: caution

level: MUST

detail: Aspect: explanation. Main positions: all. It tells in advance the pitfalls to watch for when making changes.

related: [VOC_001](vocab.md#voc_001)

## STD_023

The standard annotation word `example` (example) expresses a concrete example of an input and its result.

title: Annotation word: example

level: MUST

detail: Aspect: explanation. Main positions: clause. It makes the meaning of a clause statement concrete. It is desirable to check with a test that the example does not drift from the actual behavior.

related: [VOC_001](vocab.md#voc_001)

## STD_024

The standard annotation word `source` (source) expresses a reference to something upstream, such as a requirement, an issue or an RFC.

title: Annotation word: source

level: MUST

detail: Aspect: explanation. Main positions: contract, clause, test.

related: [VOC_001](vocab.md#voc_001)

## STD_025

The standard annotation word `assumption` (premise) expresses what the contract does not guarantee and takes as a premise. For example, that it is used from a single thread.

title: Annotation word: assumption

level: MUST

detail: Aspect: explanation. Main positions: contract, member. It becomes a list of premises to re-confirm when the contract is carried over to another environment.

related: [VOC_001](vocab.md#voc_001)

## STD_026

The standard annotation word `security` (security) is a marker that shows that something concerns a property that must be protected (security).

title: Annotation word: security

level: MUST

detail: Aspect: domain. Main positions: contract, member, clause, test. It shows what must always be carried over in a rebuild and what must be checked before a change that weakens a clause. Its absence does not guarantee that something is unrelated to safety. It is desirable not to write concrete attack procedures in the text of an annotation. The text is optional.

related: [VOC_001](vocab.md#voc_001)

## STD_027

The standard annotation word `performance` (performance) is a marker that shows that something concerns constraints of time or space.

title: Annotation word: performance

level: MUST

detail: Aspect: domain. Main positions: clause, test.

related: [VOC_001](vocab.md#voc_001)

## STD_028

The standard annotation word `concurrency` (concurrency) is a marker that shows that something concerns concurrency or atomicity.

title: Annotation word: concurrency

level: MUST

detail: Aspect: domain. Main positions: clause, test. It shows places that are easy to break and hard to check.

related: [VOC_001](vocab.md#voc_001)

## STD_029

The standard annotation word `critical` (critical) is a marker that shows that a violation has a large impact.

title: Annotation word: critical

level: MUST

detail: Aspect: severity. Main positions: clause, test. It shows the priority of a failure and what must be checked before a change that weakens it. The text is optional.

related: [VOC_001](vocab.md#voc_001)

## STD_030

The standard annotation word `todo` (pending) shows that something is not yet addressed or is temporary.

title: Annotation word: todo

level: MUST

detail: Aspect: status. Main positions: all.

related: [VOC_001](vocab.md#voc_001)

## STD_031

The standard annotation word `provisional` (provisional) shows that the content itself is not yet settled.

title: Annotation word: provisional

level: MUST

detail: Aspect: status. Main positions: contract, member, clause. It distinguishes clauses from those that may be fixed. `todo` expresses that there is something left to do, and `provisional` expresses that the content is not yet settled.

related: [VOC_001](vocab.md#voc_001)

## STD_032

The standard annotation word `legacy` (compatibility) shows behavior that is kept for the sake of compatibility. It is not necessarily a desirable design.

title: Annotation word: legacy

level: MUST

detail: Aspect: status. Main positions: clause, test. It shows what must be judged, at a rebuild, whether to carry over, and prevents it from being treated as something to tidy up.

related: [VOC_001](vocab.md#voc_001)

## STD_033

The standard annotation word `deprecated` (scheduled for removal) shows that removal has been decided.

title: Annotation word: deprecated

level: MUST

detail: Aspect: status. Main positions: clause, test. It shows what is not carried over at a rebuild. `legacy` is something to judge whether to carry over, and `deprecated` is something not carried over.

related: [VOC_001](vocab.md#voc_001)

## STD_034

The standard annotation word `manual` (manual check) shows a clause that is checked not by an automated test but manually or by another means.

title: Annotation word: manual

level: MUST

detail: Aspect: verification. Main positions: clause. It distinguishes a clause that intentionally has no automated test from a test that was forgotten.

related: [VOC_001](vocab.md#voc_001)

## STD_035

The standard annotation word `boundary` (boundary) shows a test that deals with boundary values.

title: Annotation word: boundary

level: MUST

detail: Aspect: verification. Main positions: test.

related: [VOC_001](vocab.md#voc_001)

## STD_036

The standard annotation word `regression` (regression) shows a test that prevents the recurrence of a past defect.

title: Annotation word: regression

level: MUST

detail: Aspect: verification. Main positions: test. It tells people who change things later, and LLMs, that this is not a test that may be deleted.

related: [VOC_001](vocab.md#voc_001)

## STD_040

The text of an annotation **MUST** be optional. An annotation word whose meaning is sufficient with the word alone, such as `security` or `critical`, **MUST** be attachable without text.

title: The text of an annotation is optional

level: MUST

related: [VOC_001](vocab.md#voc_001)

## STD_041

A standard annotation word **MUST** be attachable to any of a contract, a member, a clause and a test. The main positions given for each word are a guideline, not a restriction.

title: Annotation words are not restricted by position

level: MUST

related: [VOC_001](vocab.md#voc_001)

## STD_042

The identifiers of the standard vocabulary are in English. Their names in Japanese are given alongside in each item of the Japanese version of this document. The names of a custom vocabulary may be in any language.

title: Identifiers of the standard vocabulary are in English

level: MUST

related: [VOC_001](vocab.md#voc_001)
