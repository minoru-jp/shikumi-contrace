"""Checks for the documentation system.

* The Japanese canonical documents under ``devdocs/canonical_documents/`` are in
  sync with the canonical sources (nobody edited a generated file by hand).
* The English public documents (``README.md``, ``STATUS.md``, ``CHANGELOG.md`` and
  ``docs/``) have the same structure as the Japanese canonical documents they are
  translated from, and contain no Japanese text.
"""

from __future__ import annotations

import filecmp
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "devdocs" / "canonical_documents"
CONTEXT_FILE = ROOT / "devdocs" / "config" / "context.json"

# canonical document -> published document
PUBLISHED = {
    "README.md": "README.md",
    "STATUS.md": "STATUS.md",
    "changelog/CHANGELOG.md": "CHANGELOG.md",
    "GLOSSARY.md": "docs/glossary.md",
    **{
        f"specification/{path.name}": f"docs/specification/{path.name}"
        for path in sorted((CANONICAL / "specification").glob("*.md"))
    },
}

# In these documents the section headings are identifiers (STATUS_001, AIM_001,
# V0_1_0, ...) and must not be translated. The H1 title of every document is
# translated, and so are the headings of README.md and the glossary.
IDENTITY_HEADING_DOCUMENTS = {
    "STATUS.md",
    "changelog/CHANGELOG.md",
    *(name for name in PUBLISHED if name.startswith("specification/")),
}

_JAPANESE = re.compile(r"[\u3000-\u9fff\uff00-\uffef]")


# --- Canonical documents are in sync with the canonical sources ------------


def test_canonical_documents_are_in_sync_with_their_sources(tmp_path, require_tool):
    require_tool("shikumi-devdoc")
    completed = subprocess.run(
        [sys.executable, "scripts/render_canonical_docs.py", "--output", str(tmp_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    mismatches = _tree_differences(tmp_path, CANONICAL)
    assert not mismatches, (
        f"{mismatches} are out of date. Regenerate them from their canonical sources."
    )


def _tree_differences(generated: Path, committed: Path) -> list[str]:
    comparison = filecmp.dircmp(generated, committed)
    found = comparison.left_only + comparison.right_only + comparison.diff_files
    for name in comparison.subdirs:
        found += [
            f"{name}/{x}" for x in _tree_differences(generated / name, committed / name)
        ]
    return found


# --- English documents have the same structure as the Japanese ones --------


def _body(path: Path) -> str:
    """A document without the generation header of canonical documents."""
    return re.sub(
        r"\A<!--.*?-->\s*", "", path.read_text(encoding="utf-8"), flags=re.DOTALL
    )


@dataclass
class Section:
    """Structure of one Markdown section (wording is deliberately not kept)."""

    level: int
    heading: str = field(default="", compare=False)
    paragraphs: int = 0
    bullets: int = 0
    table_rows: int = 0
    metadata: list[str] = field(default_factory=list)
    code_blocks: list[str] = field(default_factory=list)


_METADATA = re.compile(
    r"^(title|kind|condition|version|released on): |^(Added|Changed|Removed):$"
)


def _outline(text: str) -> list[Section]:
    sections = [Section(level=0)]
    in_code, code_lines, in_paragraph = False, [], False
    for line in text.splitlines():
        section = sections[-1]
        if line.startswith("```"):
            if in_code:
                section.code_blocks.append("\n".join(code_lines))
                code_lines = []
            in_code, in_paragraph = not in_code, False
        elif in_code:
            code_lines.append(line)
        elif heading := re.match(r"^(#+) ", line):
            sections.append(
                Section(level=len(heading.group(1)), heading=line[heading.end() :])
            )
            in_paragraph = False
        elif not line.strip():
            in_paragraph = False
        elif line.startswith("|"):
            section.table_rows += 1
            in_paragraph = False
        elif line.startswith("- "):
            section.bullets += 1
            in_paragraph = False
        elif metadata := _METADATA.match(line):
            section.metadata.append(metadata.group(0))
            in_paragraph = False
        elif line.startswith(">") and not line.startswith("> [!"):
            continue  # continuation of the NOTE admonition
        elif not in_paragraph:
            section.paragraphs += 1
            in_paragraph = True
    return sections


def _inline_code(text: str) -> set[str]:
    without_blocks = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return set(re.findall(r"`([^`\n]+)`", without_blocks))


def _urls(text: str) -> set[str]:
    return set(re.findall(r"\]\((https?://[^)]+)\)", text))


def test_every_canonical_document_has_a_published_translation():
    assert set(PUBLISHED) == {
        str(path.relative_to(CANONICAL)).replace("\\", "/")
        for path in CANONICAL.rglob("*.md")
    }
    for published in PUBLISHED.values():
        assert (ROOT / published).is_file(), published


def test_there_are_no_published_documents_without_a_canonical_source():
    found = {
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in (ROOT / "docs").rglob("*.md")
    }
    assert found == {v for v in PUBLISHED.values() if v.startswith("docs/")}


@pytest.mark.parametrize("canonical", sorted(PUBLISHED))
def test_english_document_has_the_structure_of_the_japanese_one(canonical):
    japanese = _body(CANONICAL / canonical)
    english = (ROOT / PUBLISHED[canonical]).read_text(encoding="utf-8")

    ja_outline, en_outline = _outline(japanese), _outline(english)
    assert len(ja_outline) == len(en_outline), "number of sections differs"
    for index, (ja, en) in enumerate(zip(ja_outline, en_outline, strict=True)):
        assert ja == en, f"section #{index} differs in structure"
        if canonical in IDENTITY_HEADING_DOCUMENTS and ja.level >= 2:
            assert ja.heading == en.heading, f"section #{index} heading was changed"

    assert _inline_code(japanese) == _inline_code(english)
    assert _urls(japanese) == _urls(english)


@pytest.mark.parametrize("canonical", sorted(PUBLISHED))
def test_published_documents_contain_no_japanese(canonical):
    english = (ROOT / PUBLISHED[canonical]).read_text(encoding="utf-8")
    found = [line for line in english.splitlines() if _JAPANESE.search(line)]
    assert not found, found[:3]


def test_no_generation_header_leaks_into_published_documents():
    for published in PUBLISHED.values():
        text = (ROOT / published).read_text(encoding="utf-8")
        assert "<!--" not in text, published
        assert "shikumi-devdoc:translation-metadata" not in text, published


def test_generation_header_is_present_in_canonical_documents():
    for canonical in PUBLISHED:
        assert (CANONICAL / canonical).read_text(encoding="utf-8").startswith("<!--")


def test_the_published_readme_examples_are_the_canonical_ones():
    def python_blocks(path: Path) -> list[str]:
        text = path.read_text(encoding="utf-8")
        return [
            m.group(2)
            for m in re.finditer(
                r"^```(\w+)\n(.*?)^```", text, re.MULTILINE | re.DOTALL
            )
            if m.group(1) == "python"
        ]

    published = python_blocks(ROOT / "README.md")
    assert len(published) >= 5
    assert published == python_blocks(CANONICAL / "README.md")


# --- The realization context must agree with pyproject.toml ----------------


def test_realization_context_matches_pyproject():
    """context.json supplies the name and Python range shown in the documents."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    context = json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))["project"]
    assert context["name"] == project["name"]
    assert context["requires-python"] == project["requires-python"]
