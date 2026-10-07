"""正本ソース（devdocs/canonical_sources/）から正本（devdocs/canonical_documents/）を生成する。

リポジトリのルートで実行する::

    python scripts/render_canonical_docs.py

正本は生成物である。直接編集せず、正本ソースを変更して再生成する。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVDOCS = ROOT / "devdocs"
CONTEXT = json.dumps(
    json.loads((DEVDOCS / "config" / "context.json").read_text(encoding="utf-8"))
)
NOTICE = str(DEVDOCS / "config" / "notice.toml")
DEFAULT_OUT = DEVDOCS / "canonical_documents"
SRC = "devdocs.canonical_sources"


def run(*args: str) -> None:
    command = [
        "shikumi-devdoc",
        "render",
        *args,
        "--notice",
        NOTICE,
        "--translation-source",
    ]
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True, env={**_env()})


def _env() -> dict[str, str]:
    import os

    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT) + (
        (":" + env["PYTHONPATH"]) if env.get("PYTHONPATH") else ""
    )
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help="directory to write the canonical documents to",
    )
    out = parser.parse_args().output.resolve()
    run("glossary", f"{SRC}.vocabulary", "-o", str(out / "GLOSSARY.md"))
    run("document", f"{SRC}.readme", "-o", str(out), "--context", CONTEXT)
    run("document", f"{SRC}.status", "-o", str(out), "--context", CONTEXT)
    run("document", f"{SRC}.changelog", "-o", str(out / "changelog"))
    run("document", f"{SRC}.specification", "-o", str(out / "specification"))
    run(
        "index",
        f"{SRC}.specification",
        "-o",
        str(out / "specification"),
        "--index-title",
        "shikumi-contrace 仕様書",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
