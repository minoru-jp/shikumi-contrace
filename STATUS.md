# shikumi-contrace Project Status

Describes the current state of `shikumi-contrace` and notices about the future from the current point of view.
Past state changes are not retained; user-facing changes that actually occurred are the responsibility of the CHANGELOG.
The specification contains only what has been decided; what has not been decided is recorded in the notices (`NOTICE_NNN`) of this document.

## STATUS_001

The first public release, version `0.1.0`, is now available. The core, the reading API, the checking API and the optional pytest integration are implemented, and the tests pass on Python 3.11 and 3.12. Type checking is confirmed with basedpyright and mypy. The English public documents are published.

title: Development stage

## STATUS_002

The supported Python range is planned to be `>=3.11`. This is because Shikumi, which it builds on, requires 3.11 or later.

title: Supported Python

## STATUS_003

The design of `shikumi-contrace` is described in the specification (`docs/specification/`). The specification is the standard for the implementation, and the implementation follows what the specification says. When the specification and the implementation disagree, the description in the specification is reviewed first, not the implementation.

title: Design and implementation

## STATUS_004

`shikumi-contrace` was started as a new project under a different name because its design philosophy differs from that of the old `speclike` (0.0.x published on PyPI). The public names, features and change history of `speclike` are not carried over.

title: Relationship to speclike

## STATUS_005

Documents are managed with `shikumi-devdoc`. The canonical sources are in `devdocs/canonical_sources/`, and the Japanese canonical documents generated from them are in `devdocs/canonical_documents/`. The English public documents (`README.md`, `STATUS.md`, `CHANGELOG.md`, `docs/`) are translations of the Japanese canonical documents and keep the same structure as them.

title: Documentation system

## STATUS_006

The Shikumi it builds on is required to be the current version (0.2.4) or later, with no upper bound. Shikumi is in the 0.2 series and its public API may change, but this is coordinated between Shikumi and `shikumi-contrace`.

title: Shikumi version requirement

## STATUS_007

`shikumi-contrace` depends on the current version (0.1.0) or later of metamk, re-exports `metamk.Mk` under the name `Phase`, and re-exports `phase_of` under the same name. There is no upper bound. The behavior of `Phase` follows `metamk.Mk`.

title: metamk requirement and re-export

## STATUS_008

The repository `minoru-jp/shikumi-contrace` will be newly created, and the old `speclike` will be archived after a pointer to `shikumi-contrace` is added to its README. The license is MIT.

title: Repository and license

## NOTICE_014

Between the first public release of the new design and 1.0, the public API may be changed without notice.

title: API stability before 1.0

kind: General

condition: Until the first major version is released.
