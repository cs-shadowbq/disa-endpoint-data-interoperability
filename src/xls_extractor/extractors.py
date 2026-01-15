"""Concrete extractor implementations."""

from pathlib import Path
from typing import Any, List

from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from .interfaces import SheetExtractor, SheetWriter
from .detectors import DocumentationSheetDetector
from .symbol_font import decode_symbol_font, is_symbol_font


class MarkdownExtractor(SheetExtractor):
    """Extracts documentation sheets as Markdown."""

    def __init__(self, writer: SheetWriter, detector: DocumentationSheetDetector = None):
        """
        Initialize Markdown extractor.

        Args:
            writer: Writer to use for output
            detector: Detector to identify documentation sheets
        """
        super().__init__(writer)
        self.detector = detector or DocumentationSheetDetector()

    def extract(self, sheet_data: List[List[Any]], sheet_name: str, output_dir: Path) -> None:
        """
        Extract documentation sheet as Markdown (without formatting).

        Args:
            sheet_data: 2D list of cell values
            sheet_name: Name of the sheet
            output_dir: Directory to write output to
        """
        # Extract text from first column
        lines = []
        for row in sheet_data:
            if row and row[0]:  # Only process rows with content in first column
                content = str(row[0]).strip()
                if content:
                    lines.append(content)

        self.writer.write(lines, output_dir, sheet_name)

    def extract_with_formatting(self, sheet: Worksheet, sheet_name: str, output_dir: Path) -> None:
        """
        Extract documentation sheet as Markdown with formatting preserved.

        Args:
            sheet: Worksheet object with cell formatting
            sheet_name: Name of the sheet
            output_dir: Directory to write output to
        """
        lines = []
        for row in sheet.iter_rows():
            if not row:
                continue

            # Get first cell in row
            cell = row[0]
            if not cell or cell.value is None:
                continue

            content = str(cell.value).strip()
            if not content:
                continue

            # Decode Symbol font if needed (converts Greek letters back to Latin)
            if is_symbol_font(cell.font):
                content = decode_symbol_font(content)

            # Check formatting and apply markdown headers
            formatted_content = self._apply_markdown_formatting(cell, content)
            lines.append(formatted_content)

        self.writer.write(lines, output_dir, sheet_name)

    def _apply_markdown_formatting(self, cell: Cell, content: str) -> str:
        """
        Apply markdown formatting based on Excel cell formatting.

        Args:
            cell: Excel cell object
            content: Cell content text

        Returns:
            Content with appropriate markdown formatting
        """
        if not cell.font:
            return content

        # Check if text starts with number followed by period (e.g., "1. ", "2. ")
        # This is a numbered list item and should be #### heading
        if content and len(content) >= 3:
            if content[0].isdigit() and content[1] == '.':
                return f"#### {content}"

        # Don't apply other heading formatting if text starts with a number
        if content and content[0].isdigit():
            return content

        # Check if cell has mixed formatting (rich text)
        if self._has_mixed_formatting(cell):
            return content

        is_bold = cell.font.bold if cell.font.bold is not None else False
        is_underlined = cell.font.underline is not None and cell.font.underline != "none"

        # Bold AND underlined -> ## subtitle
        if is_bold and is_underlined:
            return f"## {content}"
        # Just bold -> ### subtitle
        elif is_bold:
            return f"### {content}"
        # Regular text
        else:
            return content

    def _has_mixed_formatting(self, cell: Cell) -> bool:
        """
        Check if a cell has mixed formatting (some text bold, some not).

        Args:
            cell: Excel cell object

        Returns:
            True if cell has mixed formatting (rich text with varying styles)
        """
        # If the cell value is a rich text object (list of tuples/objects)
        # it means different parts have different formatting
        try:
            # In openpyxl, rich text cells have their value as a list
            if isinstance(cell.value, list):
                return True
            # Check if there's an internal value that's a list (rich text)
            if hasattr(cell, '_value') and isinstance(cell._value, list):
                return True
        except (AttributeError, TypeError):
            pass

        return False

    def can_handle(self, sheet_data: List[List[Any]]) -> bool:
        """Check if this extractor can handle the sheet."""
        return self.detector.is_documentation_sheet(sheet_data)


class JSONExtractor(SheetExtractor):
    """Extracts structured sheets as JSON."""

    def __init__(self, writer: SheetWriter, header_row_index: int = 0):
        """
        Initialize JSON extractor.

        Args:
            writer: Writer to use for output
            header_row_index: Index of header row (default: 0)
        """
        super().__init__(writer)
        self.header_row_index = header_row_index

    def extract(self, sheet_data: List[List[Any]], sheet_name: str, output_dir: Path) -> None:
        """
        Extract structured sheet as JSON.

        Args:
            sheet_data: 2D list of cell values
            sheet_name: Name of the sheet
            output_dir: Directory to write output to
        """
        if not sheet_data or len(sheet_data) < 2:
            # Empty or single-row sheet
            data = {sheet_name: []}
            self.writer.write(data, output_dir, sheet_name)
            return

        # Get header row
        header_row = sheet_data[self.header_row_index]
        headers = [self._clean_header(cell) for cell in header_row]

        # Get data rows
        data_rows = sheet_data[self.header_row_index + 1:]

        # Convert to list of dictionaries
        records = []
        for row in data_rows:
            # Skip empty rows
            if not any(cell for cell in row):
                continue

            record = {}
            for i, header in enumerate(headers):
                if header:  # Only include non-empty headers
                    value = row[i] if i < len(row) else None
                    record[header] = self._clean_value(value)

            if record:  # Only add non-empty records
                records.append(record)

        # Wrap in sheet name
        data = {sheet_name: records}
        self.writer.write(data, output_dir, sheet_name)

    def can_handle(self, sheet_data: List[List[Any]]) -> bool:
        """Check if this extractor can handle the sheet."""
        # JSONExtractor is the default fallback, so it can handle anything
        # that looks like structured data
        if not sheet_data or len(sheet_data) < 2:
            return True

        # Check if first row looks like headers (mostly non-empty)
        first_row = sheet_data[0]
        non_empty = sum(1 for cell in first_row if cell)
        return non_empty >= 2  # At least 2 columns with headers

    @staticmethod
    def _clean_header(value: Any) -> str:
        """Clean header value."""
        if value is None:
            return ""
        header = str(value).strip()
        # Replace spaces with underscores for easier JSON access
        header = header.replace(" ", "_")
        return header

    def _clean_value(self, value: Any, cell: Cell = None) -> Any:
        """Clean cell value and convert Symbol font if needed."""
        if value is None:
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            # Convert Symbol font if cell provided and uses Symbol font
            if cell and is_symbol_font(cell.font):
                cleaned = decode_symbol_font(cleaned)
            return cleaned
        return value
