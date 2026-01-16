"""Tests for writers."""

import json
from pathlib import Path

import pytest

from xls_extractor.writers import JSONWriter, MarkdownWriter


class TestJSONWriter:
    """Test JSONWriter class."""

    def test_writes_json_file(self, tmp_path):
        """Test writing JSON data to file."""
        writer = JSONWriter()
        data = {"test_sheet": [{"name": "Alice", "age": 30}]}

        writer.write(data, tmp_path, "test_sheet")

        output_file = tmp_path / "test_sheet.json"
        assert output_file.exists()

        with open(output_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        assert loaded_data == data

    def test_sanitizes_filenames(self, tmp_path):
        """Test filename sanitization."""
        writer = JSONWriter()
        data = {"test": "data"}

        writer.write(data, tmp_path, "sheet:with*invalid?chars")

        # Should replace invalid characters with underscores
        output_file = tmp_path / "sheet_with_invalid_chars.json"
        assert output_file.exists()

    def test_creates_output_directory(self, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        writer = JSONWriter()
        output_dir = tmp_path / "subdir" / "nested"
        data = {"test": "data"}

        writer.write(data, output_dir, "test")

        assert output_dir.exists()
        assert (output_dir / "test.json").exists()


class TestMarkdownWriter:
    """Test MarkdownWriter class."""

    def test_writes_markdown_file(self, tmp_path):
        """Test writing Markdown data to file."""
        writer = MarkdownWriter()
        data = ["Line 1", "Line 2", "Line 3"]

        writer.write(data, tmp_path, "test_sheet")

        output_file = tmp_path / "test_sheet.md"
        assert output_file.exists()

        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()

        assert "# test_sheet" in content
        assert "Line 1" in content
        assert "Line 2" in content
        assert "Line 3" in content

    def test_sanitizes_filenames(self, tmp_path):
        """Test filename sanitization."""
        writer = MarkdownWriter()
        data = ["test"]

        writer.write(data, tmp_path, "sheet/with\\invalid:chars")

        # Should replace invalid characters with underscores
        output_file = tmp_path / "sheet_with_invalid_chars.md"
        assert output_file.exists()

    def test_handles_empty_lines(self, tmp_path):
        """Test handling of empty lines in data."""
        writer = MarkdownWriter()
        data = ["Line 1", "", "Line 2", None, "Line 3"]

        writer.write(data, tmp_path, "test")

        output_file = tmp_path / "test.md"
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Empty lines should be skipped
        assert "Line 1" in content
        assert "Line 2" in content
        assert "Line 3" in content

    def test_creates_output_directory(self, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        writer = MarkdownWriter()
        output_dir = tmp_path / "subdir" / "nested"
        data = ["test"]

        writer.write(data, output_dir, "test")

        assert output_dir.exists()
        assert (output_dir / "test.md").exists()
