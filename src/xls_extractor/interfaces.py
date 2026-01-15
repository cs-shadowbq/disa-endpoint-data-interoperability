"""Base interfaces and abstract classes for extractors."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List


class SheetDetector(ABC):
    """Interface for detecting sheet types."""

    @abstractmethod
    def is_documentation_sheet(self, sheet_data: List[List[Any]]) -> bool:
        """Determine if a sheet is a documentation sheet."""
        pass


class SheetWriter(ABC):
    """Interface for writing extracted sheet data."""

    @abstractmethod
    def write(self, data: Any, output_path: Path, sheet_name: str) -> None:
        """Write extracted data to file."""
        pass


class SheetExtractor(ABC):
    """Base class for sheet extraction."""

    def __init__(self, writer: SheetWriter):
        """Initialize extractor with a writer."""
        self.writer = writer

    @abstractmethod
    def extract(self, sheet_data: List[List[Any]], sheet_name: str, output_dir: Path) -> None:
        """Extract and write sheet data."""
        pass

    @abstractmethod
    def can_handle(self, sheet_data: List[List[Any]]) -> bool:
        """Check if this extractor can handle the given sheet."""
        pass
