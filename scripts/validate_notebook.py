"""Lightweight structural and secret-safety checks for the tutorial notebook."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "Lesson_01_Setup.ipynb"
SECRET_PATTERNS = {
    "OpenAI-style key": re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    "Hugging Face token": re.compile(r"hf_[A-Za-z0-9]{16,}"),
}


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert notebook.get("nbformat") == 4, "Notebook must use nbformat 4"

    cells = notebook.get("cells", [])
    assert cells, "Notebook must contain cells"
    assert any(cell.get("cell_type") == "markdown" for cell in cells), "Add explanatory markdown"
    assert any(cell.get("cell_type") == "code" for cell in cells), "Add executable code"

    source = "\n".join(
        "".join(cell.get("source", []))
        for cell in cells
    )
    for label, pattern in SECRET_PATTERNS.items():
        assert not pattern.search(source), f"Potential committed {label}"

    print(f"Validated {NOTEBOOK.relative_to(ROOT)} ({len(cells)} cells)")


if __name__ == "__main__":
    main()
