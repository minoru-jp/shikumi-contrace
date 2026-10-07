"""Shared pytest fixtures."""

from __future__ import annotations

import os
import shutil
import sys
import textwrap
from collections.abc import Callable, Iterator
from pathlib import Path
from types import ModuleType

import pytest

pytest_plugins = ["pytester"]


@pytest.fixture
def require_tool() -> Callable[[str], None]:
    """Make a test depend on an external command.

    On a developer machine a missing tool skips the test. On CI (the ``CI``
    environment variable is set) a missing tool is a failure, so a check can
    never be silently skipped there.
    """

    def require(name: str) -> None:
        if shutil.which(name) is not None:
            return
        if os.environ.get("CI"):
            pytest.fail(f"{name} is required on CI but was not found")
        pytest.skip(f"{name} is not installed")

    return require


class Project:
    """A throw-away source tree whose modules can be written and imported."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def write(self, files: dict[str, str]) -> None:
        for relative, source in files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(textwrap.dedent(source), encoding="utf-8")
            for parent in path.relative_to(self.root).parents:
                if str(parent) != ".":
                    init = self.root / parent / "__init__.py"
                    if not init.exists():
                        init.write_text("", encoding="utf-8")

    def load(self, name: str) -> ModuleType:
        import importlib

        return importlib.import_module(name)


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Project]:
    """A temporary project on ``sys.path``; its modules are forgotten afterwards."""
    before = set(sys.modules)
    monkeypatch.syspath_prepend(str(tmp_path))
    import importlib

    importlib.invalidate_caches()
    yield Project(tmp_path)
    for name in set(sys.modules) - before:
        module = sys.modules.get(name)
        origin = getattr(module, "__file__", None) or ""
        if str(tmp_path) in origin:
            del sys.modules[name]
