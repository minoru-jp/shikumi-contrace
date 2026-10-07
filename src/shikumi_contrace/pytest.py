"""The optional pytest integration (specification PYT_001-PYT_016, API_008-API_010).

Register it explicitly: ``pytest_plugins = ["shikumi_contrace.pytest"]``. It does two
things and nothing else:

* it shows the contract information of a failed test in its output;
* with ``--contrace-check`` it checks contract assets at collection time and
  reports the findings as :class:`shikumi_contrace.checking.ContraceWarning`.

The module is named ``pytest`` inside the package; the absolute import below
still finds the real pytest.
"""

from __future__ import annotations

import warnings
from collections.abc import Generator, Mapping
from types import ModuleType
from typing import cast

import pytest

from shikumi_contrace._model import KIND, attr_of, infos_on
from shikumi_contrace.checking import ContraceWarning, check
from shikumi_contrace.reading import annotations_of, bindings_of, relations_of


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("contrace")
    group.addoption(
        "--contrace-check",
        action="store_true",
        default=False,
        help="check contract assets at collection time and report findings as warnings",
    )
    parser.addini(
        "contrace_contract_assets",
        type="linelist",
        help="module paths of the contract assets (one per line)",
    )
    parser.addini(
        "contrace_tests",
        type="linelist",
        help="module paths of the tests (one per line)",
    )
    parser.addini(
        "contrace_implementations",
        type="linelist",
        help="module paths of the implementations (one per line)",
    )


def _raw_option(config: pytest.Config, name: str) -> object | None:
    return cast(
        "object | None", config.getoption(name)
    )  # pytest types getoption() as `Any`


def _raw_ini(config: pytest.Config, name: str) -> object | None:
    return cast("object | None", config.getini(name))  # pytest types getini() as `Any`


def _flag(config: pytest.Config, name: str) -> bool:
    return _raw_option(config, name) is True


def _ini_lines(config: pytest.Config, name: str) -> list[str] | None:
    value = _raw_ini(config, name)
    if not isinstance(value, list):
        return None
    lines = [str(line) for line in cast("list[object]", value)]
    return lines or None


def _worker_id(config: pytest.Config) -> str | None:
    """The pytest-xdist worker id, or None when xdist is not running (PYT_013)."""
    worker_input = attr_of(config, "workerinput")
    if not isinstance(worker_input, Mapping):
        return None
    worker = cast("Mapping[str, object]", worker_input).get("workerid")
    return worker if isinstance(worker, str) else None


def _implementation_label(implementation: object) -> str:
    label = attr_of(implementation, "__qualname__") or attr_of(
        implementation, "__name__"
    )
    module = attr_of(implementation, "__module__")
    text = label if isinstance(label, str) else repr(implementation)
    return f"{module}.{text}" if isinstance(module, str) else text


def _lines_for(item: pytest.Item) -> list[str]:
    function = attr_of(item, "function")
    owner = attr_of(item, "cls")
    if function is None:
        return []
    lines: list[str] = []
    for relation in relations_of(function):
        kinds = infos_on(relation.clause, KIND)
        kind = kinds[0].name if kinds else "?"
        statement = (relation.clause.__doc__ or "").strip().splitlines()
        summary = statement[0] if statement else relation.clause.__qualname__
        lines.append(f"  {relation.word.name:<9}[{kind}] {summary}")
    for annotation in annotations_of(function):
        lines.append(
            f"  {annotation.word.name}: {annotation.text}"
            if annotation.text
            else f"  {annotation.word.name}"
        )
    # The class actually collected (a subclass may bind its own implementation) first.
    bindings = list(bindings_of(owner)) if isinstance(owner, type) else []
    bindings += [b for b in bindings_of(function) if b not in bindings]
    for binding in bindings:
        lines.append(
            f"  implementation: {_implementation_label(binding.implementation)}"
        )
    return lines


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    report = yield
    if report.when == "call" and report.failed:
        lines = _lines_for(item)
        if lines:  # tests without contract declarations are left alone (PYT_011)
            report.sections.append(("contrace", "\n".join(lines)))
    return report


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if not _flag(config, "--contrace-check"):
        return
    if _worker_id(config) not in (None, "gw0"):
        return  # under pytest-xdist, one worker checks for all (PYT_013)

    modules = [
        module
        for module in (attr_of(item, "module") for item in items)
        if isinstance(module, ModuleType)
    ]
    assets = _ini_lines(config, "contrace_contract_assets")
    tests = _ini_lines(config, "contrace_tests")
    implementations = _ini_lines(config, "contrace_implementations")
    if assets or tests or implementations:
        findings = check(
            contract_assets=assets, tests=tests, implementations=implementations
        )
    else:
        findings = check(test_modules=sorted(set(modules), key=lambda m: m.__name__))
    for finding in findings:
        try:
            warnings.warn(ContraceWarning(finding.message), stacklevel=1)
        except ContraceWarning as error:  # promoted to an error by a warning filter
            raise pytest.UsageError(
                f"contrace finding treated as an error: {error}"
            ) from None
