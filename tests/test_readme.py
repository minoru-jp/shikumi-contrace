"""The README examples run, and they type-check against the real implementation.

The examples are the code blocks of the Japanese canonical README
(``devdocs/canonical_documents/README.md``). They are the ``test_target_field``
fields of its canonical source.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "devdocs" / "canonical_documents" / "README.md"

_FENCE = re.compile(r"^```(\w+)\n(.*?)^```", re.DOTALL | re.MULTILINE)


def blocks(language: str) -> list[str]:
    text = CANONICAL.read_text(encoding="utf-8")
    return [m.group(2) for m in _FENCE.finditer(text) if m.group(1) == language]


def example_files() -> dict[str, str]:
    boundary, subject, contract, implementation, test = blocks("python")[:5]
    return {
        "contract/__init__.py": "",
        "contract/ports/__init__.py": "",
        "contract/ports/reservation.py": boundary,
        "contract/inventory.py": subject,
        "contract/inventory_contract.py": contract,
        "inventory_service.py": implementation,
        "test_inventory.py": test,
    }


def write_examples(root: Path) -> None:
    for name, source in example_files().items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")


def test_the_complete_example_is_the_first_five_python_blocks():
    examples = blocks("python")[:5]
    assert len(examples) == 5
    assert examples[0].startswith("# contract/ports/reservation.py")
    assert examples[1].startswith("# contract/inventory.py")
    assert examples[2].startswith("# contract/inventory_contract.py")
    assert examples[3].startswith("# inventory_service.py")
    assert examples[4].startswith("# test_inventory.py")


def test_the_readme_examples_pass_under_pytest(tmp_path):
    write_examples(tmp_path)
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "2 passed" in completed.stdout


def test_the_readme_examples_satisfy_the_checks(tmp_path):
    # The examples follow the rules they describe: the value shape lives in
    # `ports`, which the check finds from the contract that refers to it.
    write_examples(tmp_path)
    code = (
        "import sys, test_inventory; from shikumi_contrace.checking import check; "
        "found = check(test_modules=[test_inventory]); print(found); sys.exit(1 if found else 0)"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_the_readme_examples_type_check(tmp_path, require_tool):
    require_tool("basedpyright")
    write_examples(tmp_path)
    (tmp_path / "pyrightconfig.json").write_text(
        '{"include": ["."], "typeCheckingMode": "standard", "pythonVersion": "3.11",'
        f' "extraPaths": ["{(ROOT / "src").as_posix()}"]}}',
        encoding="utf-8",
    )
    completed = subprocess.run(
        ["basedpyright", "-p", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout
    assert "0 errors" in completed.stdout, completed.stdout


def test_contract_and_implementation_do_not_know_each_other():
    contract = example_files()["contract/inventory_contract.py"]
    implementation = example_files()["inventory_service.py"]
    assert "inventory_service" not in contract
    assert "contract.inventory" not in implementation
    assert "shikumi_contrace" not in implementation
