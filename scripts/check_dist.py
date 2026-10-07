"""Build and verify the shikumi-contrace release distributions.

Used by CI and by the release workflow; it can also be run locally::

    python -m pip install -e ".[dist]"
    python scripts/check_dist.py

What it does, in order:

1. (release only) checks that the release tag is ``v<project version>``;
2. checks that the CHANGELOG has an entry for the project version (and,
   for a release, that the entry has a release date);
3. builds one wheel and one sdist;
4. inspects both archives (exact wheel contents, metadata, sdist contents);
5. runs ``twine check --strict`` on them;
6. installs each artifact into a fresh virtual environment, runs ``pip check``
   and a smoke test from a neutral directory (so the source tree is not used):
   first without pytest (the core must work without it), then with the
   ``pytest`` extra (the optional pytest integration must work).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import venv
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

# The wheel must contain exactly these package files (plus .dist-info). Adding a
# module to the package therefore requires updating this list on purpose.
EXPECTED_WHEEL_PACKAGE_FILES = {
    "shikumi_contrace/__init__.py",
    "shikumi_contrace/_descriptors.py",
    "shikumi_contrace/_model.py",
    "shikumi_contrace/_shikumi.py",
    "shikumi_contrace/_structure.py",
    "shikumi_contrace/_vocabulary.py",
    "shikumi_contrace/checking.py",
    "shikumi_contrace/pytest.py",
    "shikumi_contrace/py.typed",
    "shikumi_contrace/reading.py",
}

# The runtime requirements are exactly these; everything else is an extra.
EXPECTED_RUNTIME_REQUIREMENTS = {"shikumi>=0.2.4", "metamk>=0.1.0"}

REQUIRED_SDIST_PATHS = {
    "src/shikumi_contrace/__init__.py",
    "src/shikumi_contrace/_descriptors.py",
    "src/shikumi_contrace/_model.py",
    "src/shikumi_contrace/_shikumi.py",
    "src/shikumi_contrace/_structure.py",
    "src/shikumi_contrace/_vocabulary.py",
    "src/shikumi_contrace/checking.py",
    "src/shikumi_contrace/pytest.py",
    "src/shikumi_contrace/py.typed",
    "src/shikumi_contrace/reading.py",
    "tests/test_checking.py",
    "tests/test_documents.py",
    "tests/test_readme.py",
    "devdocs/canonical_sources/readme.py",
    "devdocs/canonical_documents/README.md",
    "docs/glossary.md",
    "docs/specification/INDEX.md",
    "README.md",
    "STATUS.md",
    "CHANGELOG.md",
    "LICENSE",
    "pyproject.toml",
    "scripts/check_dist.py",
    "scripts/render_canonical_docs.py",
}

FORBIDDEN_ARCHIVE_PARTS = {
    ".github",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
}

# Run without pytest installed: the core must not need it (PYT_006).
CORE_SMOKE_TEST = r"""
import importlib.util
import sys
from importlib.resources import files
from pathlib import Path
from typing import Protocol

import shikumi_contrace
import metamk
from shikumi_contrace import INV, PRE, Phase, binds, kind, member, note, phase_of, subject, upholds
from shikumi_contrace.checking import check
from shikumi_contrace.reading import clauses_of, relations_of

assert files("shikumi_contrace").joinpath("py.typed").is_file(), "py.typed is missing"
assert importlib.util.find_spec("pytest") is None, "pytest must not be installed here"
assert "pytest" not in sys.modules
assert Phase is metamk.Mk and phase_of is metamk.phase_of


class Spec(Protocol):
    def run(self) -> int: ...


class Impl:
    def run(self) -> int:
        return 1


class Contract:
    subject @= Spec

    class Stable:
        '''The state does not change.'''

        kind @= INV

    class run:
        member @= Spec.run

        class Positive:
            '''The result is positive.'''

            kind @= PRE
            note @= "a note"


@binds[Spec](Impl)
class Suite:
    @upholds(Contract.Stable, Contract.run.Positive)
    def test_x(self): ...


assert [c.path for c in clauses_of(Contract)] == ["Stable", "run.Positive"]
assert [r.clause for r in relations_of(Suite.test_x)] == [
    Contract.Stable,
    Contract.run.Positive,
]
assert check(test_modules=[]) == []

root = Path(r"__SOURCE_ROOT__").resolve()
installed_from = Path(shikumi_contrace.__file__).resolve()
assert root not in installed_from.parents, f"imported from the source tree: {installed_from}"
print("core smoke test passed:", installed_from)
"""

# Run with the `pytest` extra: the integration is registered explicitly.
PYTEST_PROJECT_FILES = {
    "conftest.py": 'pytest_plugins = ["shikumi_contrace.pytest"]\n',
    "test_it.py": '''
from typing import Protocol

from shikumi_contrace import PRE, binds, kind, member, subject, upholds


class Spec(Protocol):
    def run(self) -> int: ...


class Impl:
    def run(self) -> int:
        return 1


class Contract:
    subject @= Spec

    class run:
        member @= Spec.run

        class Positive:
            """The result is positive."""

            kind @= PRE


@binds[Spec](Impl)
class TestIt:
    @upholds(Contract.run.Positive)
    def test_fails(self):
        assert False, "boom"

    def test_plain(self):
        pass
''',
}


def _fail(message: str) -> None:
    raise SystemExit(f"check_dist: {message}")


def _run(
    args: list[str | os.PathLike[str]],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    command = [os.fspath(arg) for arg in args]
    print("+", " ".join(command), flush=True)
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=not capture,
        capture_output=capture,
        text=True,
    )


def _project() -> dict[str, object]:
    with (ROOT / "pyproject.toml").open("rb") as file:
        return tomllib.load(file)["project"]


# --- 1 / 2: release tag and changelog --------------------------------------


def check_release_tag(tag: str, version: str) -> None:
    expected = f"v{version}"
    if tag != expected:
        _fail(
            f"release tag {tag!r} does not match project version {version!r}; "
            f"expected {expected!r}"
        )
    print(f"release tag {tag} matches project version {version}")


def check_changelog(version: str, *, require_release_date: bool) -> None:
    """The CHANGELOG must have an entry for ``version``.

    When publishing a release the entry must also carry its release date
    (``released on: YYYY-MM-DD``). Normal CI does not require the date, so that
    the entry for the next version can be started before it is released.
    """
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    sections = re.split(r"^## ", changelog, flags=re.MULTILINE)
    entry = next(
        (
            section
            for section in sections
            if re.search(rf"^version: {re.escape(version)}$", section, re.MULTILINE)
        ),
        None,
    )
    if entry is None:
        _fail(f"CHANGELOG.md has no entry for version {version}")
    if require_release_date and not re.search(
        r"^released on: \d{4}-\d{2}-\d{2}$", entry, re.MULTILINE
    ):
        _fail(
            f"the CHANGELOG.md entry for version {version} has no release date "
            "('released on: YYYY-MM-DD')"
        )


# --- 3: build --------------------------------------------------------------


def _build() -> tuple[Path, Path]:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    _run([sys.executable, "-m", "build", "--outdir", DIST])
    wheels = sorted(DIST.glob("*.whl"))
    sdists = sorted(DIST.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        _fail(f"expected one wheel and one sdist, found {wheels=} {sdists=}")
    return wheels[0], sdists[0]


# --- 4: archive inspection -------------------------------------------------


def _assert_no_forbidden_parts(names: list[str], *, archive: Path) -> None:
    bad = [n for n in names if FORBIDDEN_ARCHIVE_PARTS.intersection(Path(n).parts)]
    if bad:
        _fail(f"forbidden paths in {archive.name}: {bad[:20]}")


def check_wheel(wheel: Path, project: dict[str, object]) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        _assert_no_forbidden_parts(names, archive=wheel)

        package_files = {n for n in names if ".dist-info/" not in n}
        if package_files != EXPECTED_WHEEL_PACKAGE_FILES:
            _fail(
                f"unexpected wheel contents in {wheel.name}: "
                f"extra={sorted(package_files - EXPECTED_WHEEL_PACKAGE_FILES)} "
                f"missing={sorted(EXPECTED_WHEEL_PACKAGE_FILES - package_files)}"
            )
        if not any(n.endswith(".dist-info/licenses/LICENSE") for n in names):
            _fail(f"LICENSE is not included in {wheel.name}")

        metadata_names = [n for n in names if n.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            _fail(f"expected one METADATA in {wheel.name}, found {metadata_names}")
        metadata = archive.read(metadata_names[0]).decode("utf-8")

    fields: dict[str, list[str]] = {}
    for line in metadata.split("\n\n", 1)[0].splitlines():
        key, _, value = line.partition(": ")
        fields.setdefault(key, []).append(value)

    expectations = {
        "Name": [project["name"]],
        "Version": [project["version"]],
        "Requires-Python": [project["requires-python"]],
        "License-Expression": ["MIT"],
    }
    for key, expected in expectations.items():
        if fields.get(key) != expected:
            _fail(f"metadata {key}: expected {expected}, found {fields.get(key)}")

    # Only the declared runtime dependencies may be required; the rest are extras.
    runtime = {r for r in fields.get("Requires-Dist", []) if "extra ==" not in r}
    if runtime != EXPECTED_RUNTIME_REQUIREMENTS:
        _fail(
            f"unexpected runtime dependencies: {sorted(runtime)}; "
            f"expected {sorted(EXPECTED_RUNTIME_REQUIREMENTS)}"
        )
    if "pytest" not in fields.get("Provides-Extra", []):
        _fail("the 'pytest' extra is missing from the metadata")


def check_sdist(sdist: Path) -> None:
    with tarfile.open(sdist, "r:gz") as archive:
        names = archive.getnames()
    _assert_no_forbidden_parts(names, archive=sdist)
    # Every sdist member lives under one top-level directory (shikumi_contrace-<version>/).
    # Compare the paths below it exactly: matching only on a suffix would let
    # devdocs/canonical_documents/README.md stand in for a missing README.md.
    relative_paths = {name.split("/", 1)[1] for name in names if "/" in name}
    missing = sorted(REQUIRED_SDIST_PATHS - relative_paths)
    if missing:
        _fail(f"missing required paths in {sdist.name}: {missing}")


# --- 5: twine --------------------------------------------------------------


def check_metadata_with_twine(wheel: Path, sdist: Path) -> None:
    _run([sys.executable, "-m", "twine", "check", "--strict", wheel, sdist])


# --- 6: installed smoke tests ----------------------------------------------


def _venv_python(directory: Path) -> Path:
    bin_dir = directory / ("Scripts" if os.name == "nt" else "bin")
    return bin_dir / ("python.exe" if os.name == "nt" else "python")


def _clean_environment() -> dict[str, str]:
    # No PYTHONPATH, so that the installed package, not the source tree, is imported.
    return {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}


def install_and_smoke_test(artifact: Path, *, work: Path, label: str) -> None:
    environment = work / f"{label}-env"
    venv.EnvBuilder(with_pip=True).create(environment)
    python = _venv_python(environment)

    # 1) the core, without pytest
    _run([python, "-m", "pip", "install", artifact], cwd=work)
    _run([python, "-m", "pip", "check"], cwd=work)
    _run(
        [python, "-c", CORE_SMOKE_TEST.replace("__SOURCE_ROOT__", str(ROOT))],
        cwd=work,
        env=_clean_environment(),
    )

    # 2) the optional pytest integration, with the `pytest` extra
    _run([python, "-m", "pip", "install", f"{artifact}[pytest]"], cwd=work)
    _run([python, "-m", "pip", "check"], cwd=work)
    project = work / f"{label}-pytest-project"
    project.mkdir()
    for name, source in PYTEST_PROJECT_FILES.items():
        (project / name).write_text(source, encoding="utf-8")
    result = _run(
        [python, "-m", "pytest", "-p", "no:cacheprovider", "-q"],
        cwd=project,
        env=_clean_environment(),
        capture=True,
    )
    print(result.stdout)
    if result.returncode != 1:  # exactly one test fails on purpose
        _fail(f"the pytest smoke test ended with exit code {result.returncode}")
    for expected in ("- contrace -", "upholds", "[pre] The result is positive."):
        if expected not in result.stdout:
            _fail(f"the pytest integration did not show {expected!r}")
    if "1 failed, 1 passed" not in result.stdout:
        _fail("the pytest smoke test did not end with '1 failed, 1 passed'")
    print("pytest integration smoke test passed")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build and verify the shikumi-contrace release distributions."
    )
    parser.add_argument(
        "--release-tag",
        help="Git tag of the release being published; must be v<project version>.",
    )
    parser.add_argument(
        "--archive-only",
        action="store_true",
        help="Inspect the built archives without installing them.",
    )
    args = parser.parse_args()

    project = _project()
    version = str(project["version"])

    if args.release_tag is not None:
        check_release_tag(args.release_tag, version)
    check_changelog(version, require_release_date=args.release_tag is not None)

    wheel, sdist = _build()
    check_wheel(wheel, project)
    check_sdist(sdist)
    check_metadata_with_twine(wheel, sdist)

    if not args.archive_only:
        with tempfile.TemporaryDirectory(prefix="shikumi-contrace-dist-check-") as temp:
            work = Path(temp)
            install_and_smoke_test(wheel, work=work, label="wheel")
            install_and_smoke_test(sdist, work=work, label="sdist")

    print(f"release distributions verified: {wheel.name}, {sdist.name}")


if __name__ == "__main__":
    main()
