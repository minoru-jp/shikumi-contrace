# pytest Integration (Optional)

The core of shikumi-contrace does not depend on a specific test runner. This document defines what shikumi-contrace observes when providing features for pytest as an optional integration, and the range of features the integration provides. The integration is kept to the necessary minimum, and everything else is done with the reading API of the core.

## PYT_001

Collection and execution of tests are done by the test runner (pytest). shikumi-contrace **MUST NOT** implement them on its own.

title: Collection and execution belong to the test runner

level: MUST NOT

related: [AIM_003](aim.md#aim_003)

## PYT_002

shikumi-contrace **MUST NOT** generate or rewrite test functions or test classes by means such as metaclasses or rewriting class names.

title: Tests are not synthesized or rewritten

level: MUST NOT

## PYT_003

shikumi-contrace **MUST NOT** change the name, signature or definition location of a test function as seen by the test runner.

title: Names, signatures and locations of tests are preserved

level: MUST NOT

detail: So that the output of the test runner, the IDE and tracebacks point to the actual definition location.

## PYT_004

shikumi-contrace **MUST** coexist with the standard mechanisms of pytest (parametrize, fixtures, marks, skip and so on). It **MUST NOT** provide mechanisms that replace them.

title: Coexistence with the standard mechanisms of pytest

level: MUST

related: [AIM_009](aim.md#aim_009)

## PYT_005

The pytest integration **MUST** be optional. Even without the pytest integration, describing contracts, relating tests and validation **MUST** remain usable.

title: The pytest integration is optional

level: MUST

related: [AIM_003](aim.md#aim_003)

detail: The form of introduction is defined in PYT_016.

## PYT_006

The core **MUST NOT** import pytest. Processing that depends on pytest **MUST** be placed only in the pytest integration.

title: The core does not import pytest

level: MUST

related: [IND_004](independence.md#ind_004)

detail: A contract asset imports the core of shikumi-contrace. If the core imported pytest, the contract asset would depend on pytest, and it would become harder to carry the contract away as an independent asset.

## PYT_007

Diagnostics reported by the pytest integration **MUST** be reported as pytest warnings. The severity of diagnostics **MUST** be decidable by the user with pytest's warning filters (`-W` or `filterwarnings`).

title: Diagnostics are reported as pytest warnings

level: MUST

detail: Emitting diagnostics as warnings means that, by default, the run is not stopped, and users can escalate them to errors when needed. When a setting that treats warnings as errors is given, the run ends not with an internal pytest error but with an ordinary error that shows the content of the diagnostic.

## PYT_008

shikumi-contrace **MUST** hold the information of contracts and tests on objects as Shikumi information.

title: Information is held as Shikumi information

level: MUST

## PYT_009

The pytest integration **MUST** read, from the tests collected by pytest, the information attached by the core. For that purpose it **MUST NOT** change the definition location, name or signature of test functions or methods. How information is read follows the reading API (including RDG_007).

title: The integration reads information from collected tests

level: MUST

related: [RDG_007](reading.md#rdg_007)

## PYT_010

The features the pytest integration provides **SHOULD** be limited to the necessary minimum, such as displaying contract information. The features provided are defined in PYT_011 to PYT_013.

title: The integration is kept to the necessary minimum

level: SHOULD

detail: A contract view (overlaying test results on the structure of a contract and displaying them) is outside the scope.

related: [AIM_003](aim.md#aim_003)

## PYT_011

The pytest integration **MUST** show, in the output of a failed test, the clauses (kinds and clause statements) the test related to, annotations, and the implementations it bound. This display is always enabled, and **MUST NOT** add anything to the output of a test that has no contract declarations.

title: Contract information is shown in the output of failed tests

level: MUST

detail: A binding attached to a test class is also shown. It is also shown under parallel execution. The display is one line each, in the order of relations, annotations and bindings. Relations and annotations are arranged in the order written (RDG_009). For a clause statement, the first line is shown.

related: [AIM_003](aim.md#aim_003)

## PYT_012

The pytest integration **MUST** provide a feature that runs validation at collection time and reports diagnostics. Diagnostics are reported according to PYT_007. This feature **MUST** operate only when the user chooses it.

title: Validation at collection time runs only when the user chooses it

level: MUST

detail: To avoid warnings appearing in existing tests merely because the integration was introduced. The same validation can also be called from an ordinary test, using the API of the core. The name of the means of choosing it is defined in the specification of the names and placement of the public API. If validation is not chosen, the guarantee does not work, so for continuous validation it is desirable to always choose it in the settings.

related: [AIM_003](aim.md#aim_003)

## PYT_013

Under parallel execution (pytest-xdist), validation at collection time **MUST** be run and reported by only one worker. Diagnostics **MUST NOT** be reported in duplicate as many times as there are workers.

title: Under parallel execution, validation runs in a single worker

level: MUST

detail: Every worker collects all the tests, so one worker is enough to validate. This behavior depends on information that pytest-xdist passes to workers. The target is limited to pytest-xdist. The behavior with other parallel execution plugins is not specified.

## PYT_014

An option for narrowing down tests by clause kind or the like is not provided as standard.

title: No built-in option for filtering tests by contract information

level: INFORMATIVE

detail: pytest's `-m` cannot narrow down by the arguments of a mark. Users can write the narrowing in `conftest.py` using the reading API of the core.

## PYT_015

The pytest integration does not provide a feature that records the information of contracts and tests as `pytest.mark`.

title: Information is not recorded as pytest marks

level: INFORMATIVE

detail: Because vocabulary is free, the kinds of marks would increase without limit, and it also goes badly with `--strict-markers`. Narrowing down by arguments cannot be done with `-m` either. Users who need it can attach pytest's standard marks themselves.

## PYT_016

The pytest integration **MUST** be installable as an additional dependency. Registration with pytest **MUST** be made explicitly by the user. Merely installing it **MUST NOT** change the behavior of pytest.

title: The pytest integration is an optional extra with explicit registration

level: MUST

detail: For example, install it with `pip install shikumi-contrace[pytest]`, and the user writes the registration in `conftest.py` or the like. If it were registered automatically, the behavior of pytest would change even in an environment where shikumi-contrace was installed only for another purpose.

related: [AIM_003](aim.md#aim_003)
