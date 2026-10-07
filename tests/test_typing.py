"""Consumer typing contract, checked with basedpyright when it is available."""

from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def test_consumer_typing_contract(require_tool):
    require_tool("basedpyright")
    completed = subprocess.run(
        ["basedpyright", "-p", str(HERE / "typing")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout
    assert "0 errors, 0 warnings" in completed.stdout, completed.stdout


def test_the_library_itself_type_checks_without_warnings(require_tool):
    """The library passes basedpyright's default (recommended) mode with no warnings."""
    require_tool("basedpyright")
    root = HERE.parent
    completed = subprocess.run(
        ["basedpyright"], cwd=root, capture_output=True, text=True, check=False
    )
    assert "0 errors, 0 warnings" in completed.stdout, completed.stdout


def test_the_type_checking_mode_is_not_relaxed():
    project = tomllib.loads(
        (HERE.parent / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert "typeCheckingMode" not in project["tool"]["basedpyright"]


def test_consumer_typing_contract_under_mypy(require_tool):
    """mypy rejects exactly the lines marked ``# pyright: ignore`` and nothing else.

    In particular it accepts every ``name @= value`` line of a class body
    (the result of ``@=`` is typed as the descriptor itself).
    """
    require_tool("mypy")
    fixtures = HERE / "typing"
    completed = subprocess.run(
        ["mypy", "--python-version", "3.11", "--show-error-codes", "consumer.py"],
        cwd=fixtures,
        capture_output=True,
        text=True,
        check=False,
    )
    reported = {
        int(line)
        for line in re.findall(
            r"^consumer\.py:(\d+): error", completed.stdout, re.MULTILINE
        )
    }
    source = (fixtures / "consumer.py").read_text(encoding="utf-8").splitlines()
    expected = {
        n
        for n, text in enumerate(source, 1)
        if text.rstrip().endswith("# pyright: ignore")
    }
    assert reported == expected, completed.stdout


def test_the_library_itself_type_checks_under_mypy(require_tool):
    require_tool("mypy")
    root = HERE.parent
    completed = subprocess.run(
        ["mypy", "--python-version", "3.11", "src/shikumi_contrace"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout
