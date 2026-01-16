"""Writers for different output formats."""

import json
from pathlib import Path
from typing import Any

from .interfaces import SheetWriter


class JSONWriter(SheetWriter):
    """Writes data as JSON."""

    def write(self, data: Any, output_path: Path, sheet_name: str) -> None:
        """
        Write data to JSON file.

        Args:
            data: Data to write
            output_path: Directory to write to
            sheet_name: Name of the sheet (used for filename)
        """
        output_path.mkdir(parents=True, exist_ok=True)
        output_file = output_path / f"{self._sanitize_filename(sheet_name)}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Sanitize filename by replacing invalid characters."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, "_")
        return name.strip()


class MarkdownWriter(SheetWriter):
    """Writes data as Markdown."""

    def write(self, data: Any, output_path: Path, sheet_name: str) -> None:
        """
        Write data to Markdown file.

        Args:
            data: Data to write (list of strings)
            output_path: Directory to write to
            sheet_name: Name of the sheet (used for filename)
        """
        output_path.mkdir(parents=True, exist_ok=True)
        output_file = output_path / f"{self._sanitize_filename(sheet_name)}.md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {sheet_name}\n\n")
            if isinstance(data, list):
                for line in data:
                    if line:  # Only write non-empty lines
                        f.write(f"{line}\n\n")
            else:
                f.write(str(data))

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Sanitize filename by replacing invalid characters."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, "_")
        return name.strip()
