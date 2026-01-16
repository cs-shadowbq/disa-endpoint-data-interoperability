"""Tests for sheet detectors."""

import pytest

from xls_extractor.detectors import DocumentationSheetDetector


class TestDocumentationSheetDetector:
    """Test DocumentationSheetDetector class."""

    def test_detects_single_column_documentation(self):
        """Test detection of single-column documentation sheets."""
        detector = DocumentationSheetDetector()

        sheet_data = [
            ["Introduction"],
            ["This is a documentation sheet."],
            ["It has multiple lines of text."],
            ["All in the first column."],
            [""],
            ["Another paragraph."],
        ]

        assert detector.is_documentation_sheet(sheet_data) is True

    def test_detects_multi_column_structured_data(self):
        """Test detection of multi-column structured data."""
        detector = DocumentationSheetDetector()

        sheet_data = [
            ["Name", "Age", "City"],
            ["Alice", 30, "NYC"],
            ["Bob", 25, "LA"],
            ["Charlie", 35, "Chicago"],
        ]

        assert detector.is_documentation_sheet(sheet_data) is False

    def test_handles_empty_sheet(self):
        """Test handling of empty sheets."""
        detector = DocumentationSheetDetector()

        assert detector.is_documentation_sheet([]) is False
        assert detector.is_documentation_sheet([[]]) is False
        assert detector.is_documentation_sheet([[""], [""], [""]]) is False

    def test_handles_single_row(self):
        """Test handling of single-row sheets."""
        detector = DocumentationSheetDetector()

        sheet_data = [["Just one row"]]
        assert detector.is_documentation_sheet(sheet_data) is False

    def test_custom_thresholds(self):
        """Test custom detection thresholds."""
        detector = DocumentationSheetDetector(single_column_threshold=0.5)

        # 50% single column, 50% multi-column
        sheet_data = [
            ["Text only"],
            ["More text"],
            ["Name", "Value", "Notes"],
            ["Item", "100", "Some notes"],
        ]

        assert detector.is_documentation_sheet(sheet_data) is True

    def test_mixed_content_with_sparse_data(self):
        """Test sheet with mixed single and sparse multi-column content."""
        detector = DocumentationSheetDetector()

        sheet_data = [
            ["Title"],
            ["Description text here"],
            ["", "", ""],
            ["Another line", ""],
            ["More text"],
        ]

        assert detector.is_documentation_sheet(sheet_data) is True
