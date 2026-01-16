"""Sheet type detection logic."""

from typing import Any, List

from .interfaces import SheetDetector


class DocumentationSheetDetector(SheetDetector):
    """Detects if a sheet is a documentation/text sheet."""

    def __init__(self, single_column_threshold: float = 0.8, empty_cell_threshold: float = 0.5):
        """
        Initialize detector.

        Args:
            single_column_threshold: Ratio of rows with only first column filled (0.0-1.0)
            empty_cell_threshold: Max ratio of empty cells allowed (0.0-1.0)
        """
        self.single_column_threshold = single_column_threshold
        self.empty_cell_threshold = empty_cell_threshold

    def is_documentation_sheet(self, sheet_data: List[List[Any]]) -> bool:
        """
        Determine if a sheet is a documentation sheet.

        A documentation sheet typically has:
        - Most rows use only the first column
        - Text content rather than tabular data
        - No clear header row pattern

        Args:
            sheet_data: 2D list of cell values

        Returns:
            True if sheet appears to be documentation
        """
        if not sheet_data or len(sheet_data) < 2:
            return False

        non_empty_rows = [row for row in sheet_data if any(cell for cell in row)]
        if not non_empty_rows:
            return False

        # Count rows where only first column has content
        single_column_rows = 0
        for row in non_empty_rows:
            if not row:
                continue
            # Check if first cell has content and rest are empty
            first_cell = row[0] if row else None
            rest_empty = all(not cell for cell in row[1:]) if len(row) > 1 else True

            if first_cell and rest_empty:
                single_column_rows += 1

        # Calculate ratio
        single_column_ratio = single_column_rows / len(non_empty_rows)

        # Check if it looks like structured data (has multiple non-empty columns consistently)
        multi_column_rows = 0
        for row in non_empty_rows:
            non_empty_cells = sum(1 for cell in row if cell)
            if non_empty_cells > 2:  # More than 2 columns have data
                multi_column_rows += 1

        multi_column_ratio = multi_column_rows / len(non_empty_rows)

        # Documentation sheet if high single-column ratio OR low multi-column ratio
        return single_column_ratio >= self.single_column_threshold or multi_column_ratio < 0.3
