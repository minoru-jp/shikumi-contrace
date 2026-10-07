"""The optional pytest integration (PYT_005-PYT_016, API_008-API_010)."""

from __future__ import annotations

import importlib.util

import pytest

CONTRACT = '''
from typing import Protocol
from shikumi_contrace import POST, PRE, kind, member, subject

class Spec(Protocol):
    def get(self, key: str) -> object: ...

class Contract:
    subject @= Spec

    class get:
        member @= Spec.get

        class Keys:
            """Keys are strings."""
            kind @= PRE

        class Found:
            """A stored key is found."""
            kind @= POST
'''

LEAKY_CONTRACT = (
    CONTRACT
    + """
from impl_pkg.service import Service as _Leak
"""
)

SERVICE = """
class Service:
    def get(self, key: str) -> object: ...
"""

TESTS = """
from shikumi_contrace import binds, boundary, note, upholds
from contract_pkg.contract import Spec, Contract as C
from impl_pkg.service import Service

@binds[Spec](Service)
class TestGet:
    @upholds(C.get.Keys)
    @boundary
    @note("empty key")
    def test_fails(self):
        assert False, "boom"

    @upholds(C.get.Found)
    def test_passes(self):
        pass

def test_plain_failure():
    assert False, "plain"
"""


@pytest.fixture
def files(pytester):
    pytester.makepyfile(
        **{
            "contract_pkg/__init__": "",
            "contract_pkg/contract": CONTRACT,
            "impl_pkg/__init__": "",
            "impl_pkg/service": SERVICE,
            "test_it": TESTS,
        }
    )
    pytester.makeconftest('pytest_plugins = ["shikumi_contrace.pytest"]\n')
    return pytester


def run(pytester, *args):
    return pytester.runpytest_subprocess(*args)


def test_a_failed_test_shows_its_contract_information(files):  # PYT_011
    out = run(files).stdout.str()
    section = out.split("- contrace -")[1].split("test_plain_failure")[0]
    # The order of the lines is not specified (NOTICE_024); each line must be there.
    assert "upholds" in section and "[pre] Keys are strings." in section
    assert "note: empty key" in section
    assert "boundary" in section
    assert "implementation: impl_pkg.service.Service" in section


def test_a_test_without_declarations_gets_nothing_added(files):  # PYT_011
    result = run(files)
    out = result.stdout.str()
    plain = out.split("test_plain_failure")[1]
    assert "contrace" not in plain.split("short test summary")[0]


def test_a_passing_test_shows_nothing(files):
    result = run(files, "-k", "test_passes")
    assert "contrace" not in result.stdout.str().replace("shikumi_contrace.pytest", "")


def test_the_check_runs_only_when_chosen(files):  # PYT_012
    files.makepyfile(**{"contract_pkg/contract": LEAKY_CONTRACT})
    quiet = run(files, "-k", "test_passes")
    assert "ContraceWarning" not in quiet.stdout.str()
    chosen = run(files, "-k", "test_passes", "--contrace-check")
    chosen.stdout.fnmatch_lines(["*ContraceWarning*refers to implementations*"])


def test_findings_are_reported_as_warnings(files):  # PYT_007
    files.makepyfile(**{"contract_pkg/contract": LEAKY_CONTRACT})
    result = run(files, "-k", "test_passes", "--contrace-check")
    result.assert_outcomes(passed=1, warnings=1)


def test_a_warning_filter_turns_findings_into_errors(files):  # PYT_007, API_010
    files.makepyfile(**{"contract_pkg/contract": LEAKY_CONTRACT})
    result = run(
        files,
        "--contrace-check",
        "-W",
        "error::shikumi_contrace.checking.ContraceWarning",
    )
    assert result.ret != 0
    out = result.stdout.str() + result.stderr.str()
    assert "INTERNALERROR" not in out  # a plain error, not a pytest crash
    assert "contrace finding treated as an error" in out


def test_ranges_can_be_declared_in_the_ini_file(files):  # REG_014, API_009
    files.makepyfile(**{"contract_pkg/contract": LEAKY_CONTRACT})
    files.makeini(
        """
        [pytest]
        contrace_contract_assets =
            contract_pkg
        contrace_tests =
            test_it
        contrace_implementations =
            impl_pkg
        """
    )
    result = run(files, "-k", "test_passes", "--contrace-check")
    result.stdout.fnmatch_lines(["*ContraceWarning*refers to implementations*"])


@pytest.mark.skipif(
    importlib.util.find_spec("xdist") is None, reason="pytest-xdist is not installed"
)
def test_under_xdist_findings_are_not_duplicated(files):  # PYT_013
    files.makepyfile(**{"contract_pkg/contract": LEAKY_CONTRACT})
    serial = run(files, "-k", "test_passes", "--contrace-check")
    parallel = run(files, "-k", "test_passes", "--contrace-check", "-n", "2")
    serial.assert_outcomes(passed=1, warnings=1)
    parallel.assert_outcomes(passed=1, warnings=1)


@pytest.mark.skipif(
    importlib.util.find_spec("xdist") is None, reason="pytest-xdist is not installed"
)
def test_under_xdist_the_failure_display_still_works(files):  # PYT_011
    result = run(files, "-n", "2")
    result.stdout.fnmatch_lines(["*- contrace -*", "*upholds*"])


def test_the_integration_is_not_active_unless_registered(pytester):  # PYT_016
    pytester.makepyfile(
        """
        def test_fails():
            assert False
        """
    )
    result = pytester.runpytest_subprocess("--contrace-check")
    assert result.ret != 0
    result.stderr.fnmatch_lines(["*unrecognized arguments: --contrace-check*"])
