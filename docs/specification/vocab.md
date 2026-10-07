# Vocabulary

Defines, for vocabulary such as clause kinds, the words of relations and the words of annotations, what shikumi-contrace provides and what it leaves to users. The more free the vocabulary is, the better. Variations in spelling are accepted as part of expressiveness.

## VOC_001

shikumi-contrace **MUST** provide a standard vocabulary. The standard vocabulary includes clause kinds, violation behaviors, relation words and annotation words.

title: A standard vocabulary is provided

level: MUST

detail: The standard words and their meanings are defined in the specification of the standard vocabulary.

related: [AIM_006](aim.md#aim_006)

## VOC_002

shikumi-contrace **MUST NOT** obstruct users from defining and using a custom vocabulary.

title: Custom vocabulary is not obstructed

level: MUST NOT

related: [AIM_006](aim.md#aim_006)

## VOC_003

A custom vocabulary **MUST** be usable in the same positions and with the same notation as the standard vocabulary.

title: Custom vocabulary is used the same way as the standard one

level: MUST

## VOC_004

shikumi-contrace **MUST NOT** emit a diagnostic on the grounds that a vocabulary is not included in the standard vocabulary. It **MUST NOT** reject an unknown vocabulary.

title: Unknown vocabulary is not rejected

level: MUST NOT

detail: Rejection here includes not only errors but also warnings. Diagnostics about the handling of vocabulary are emitted only by validation rules that users have added as their own rules.

## VOC_005

shikumi-contrace **MUST NOT** unify or reject variations in the spelling of vocabulary.

title: Variations in spelling are accepted

level: MUST NOT

detail: Variations in spelling are something that is natural. Being able to write the same meaning with different words raises expressiveness.

## VOC_006

Users **MAY** define, outside shikumi-contrace, validation rules that restrict vocabulary as their own rules. By default, shikumi-contrace does not restrict vocabulary.

title: Restricting vocabulary is the user's choice

level: MAY

## VOC_007

The rules VOC_002 to VOC_005 apply in the same way to the vocabulary of annotations.

title: Note vocabulary follows the same rules

level: MUST

## VOC_008

Vocabulary **MUST** be represented as values of the open information types that shikumi-contrace defines (clause kinds, violation behaviors, relations, annotations). Both the standard vocabulary and a custom vocabulary **MUST** be values created with the same generators, and there **MUST NOT** be a need to register an information type in order to use a custom vocabulary.

title: Vocabulary is represented as values of open information types

level: MUST

detail: If words had to be registered as information types, words without registration would not appear in the semantic view, and the freedom of vocabulary would be lost in practice. If words are values, the number of information types that are recognized can be kept small regardless of the number of words.

## VOC_009

A custom vocabulary **MUST** appear in the semantic view alongside the standard vocabulary.

title: Custom vocabulary appears in the semantic view like the standard one

level: MUST

## VOC_010

When a project wants to leave a violation behavior deliberately undecided, it **MAY** define a custom violation behavior (for example `UNDECIDED = define.violation("undecided")`) and use it. Omitting the violation behavior means that it is not declared, and can be told apart from a deliberate deferral.

title: Guidance: marking violation behavior as deliberately undecided

level: INFORMATIVE

detail: Four states of violation behavior can be told apart when reading. `REJECTED` promises that a violating call is not accepted as a normal success. `OUT_OF_SCOPE` leaves the behavior on violation outside the promise. A word of the project (such as `UNDECIDED`) expresses that it is deliberately undecided. Omission expresses that nothing is declared (possibly forgotten). In reading, the preconditions whose `on_violation` is omitted can be listed by filtering `clauses_of`. A project that does not allow omission can check this filter in its own tests, as its own rule (VOC_006). shikumi-contrace does not diagnose omission. Omission is a legitimate way of writing, and diagnosing it would make the declaration effectively mandatory (REG_022). If many projects come to need the same word, adding it to the standard words will be considered.
