"""Command-line interface for XLS Extractor."""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from . import __version__
from .processor import ExcelProcessor


console = Console()


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Extract Excel sheets to JSON and Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all sheets from a file
  xls-extractor input.xlsx

  # Specify custom output directory
  xls-extractor input.xlsx --output-dir ./output

  # Force specific sheets to be extracted as Markdown
  xls-extractor input.xlsx --markdown-sheets "README" "Notes"

  # Include hidden columns in extraction
  xls-extractor input.xlsx --include-hidden

  # Extract formulas instead of values
  xls-extractor input.xlsx --extract-mode formulas

  # Process multiple files
  xls-extractor file1.xlsx file2.xlsx file3.xlsx
        """,
    )

    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Excel file(s) to process (.xlsx or .xls)",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("json"),
        help="Output directory for extracted data (default: json/)",
    )

    parser.add_argument(
        "-m",
        "--markdown-sheets",
        nargs="+",
        default=[],
        help="Sheet names to force as Markdown (space-separated)",
    )

    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden columns in extraction (default: False)",
    )

    parser.add_argument(
        "--extract-mode",
        choices=["values", "formulas"],
        default="values",
        help="Extract cell values or formulas (default: values)",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"xls-extractor {__version__}",
    )

    return parser


def validate_files(files: list[Path]) -> list[Path]:
    """
    Validate input files exist and are Excel files.

    Args:
        files: List of file paths

    Returns:
        List of valid file paths

    Raises:
        SystemExit: If any file is invalid
    """
    valid_files = []
    errors = []

    for file in files:
        if not file.exists():
            errors.append(f"File not found: {file}")
        elif not file.is_file():
            errors.append(f"Not a file: {file}")
        elif file.suffix.lower() not in [".xlsx", ".xls"]:
            errors.append(f"Not an Excel file: {file}")
        else:
            valid_files.append(file)

    if errors:
        console.print("[red]Errors:[/red]")
        for error in errors:
            console.print(f"  • {error}")
        sys.exit(1)

    return valid_files


def display_results(results: dict) -> None:
    """
    Display processing results in a formatted table.

    Args:
        results: Dictionary with processing results
    """
    table = Table(title=f"Results: {Path(results['file']).name}")

    table.add_column("Status", style="cyan")
    table.add_column("Sheet Name", style="magenta")
    table.add_column("Details", style="green")

    for sheet in results["sheets_processed"]:
        table.add_row("✓", sheet, "Extracted successfully")

    for failure in results["sheets_failed"]:
        table.add_row("✗", failure["sheet"], f"Error: {failure['error']}", style="red")

    console.print(table)


def main() -> int:
    """
    Main entry point for CLI.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Display header
    console.print(
        Panel.fit(
            f"[bold cyan]XLS Extractor[/bold cyan] v{__version__}\n"
            "[dim]Extract Excel sheets to JSON and Markdown[/dim]",
            border_style="cyan",
        )
    )

    # Validate files
    valid_files = validate_files(args.files)

    if not valid_files:
        console.print("[red]No valid files to process[/red]")
        return 1

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Process files
    processor = ExcelProcessor(
        output_dir=args.output_dir,
        force_markdown_sheets=args.markdown_sheets,
        include_hidden=args.include_hidden,
        extract_mode=args.extract_mode,
    )

    all_success = True

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for file in valid_files:
            task = progress.add_task(f"Processing {file.name}...", total=None)

            try:
                results = processor.process_file(file)
                progress.remove_task(task)
                display_results(results)

                if results["sheets_failed"]:
                    all_success = False

            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]Failed to process {file.name}: {e}[/red]")
                all_success = False

    # Summary
    console.print()
    if all_success:
        console.print(
            f"[green]✓ All files processed successfully![/green]\n"
            f"[dim]Output directory: {args.output_dir.absolute()}[/dim]"
        )
        return 0
    else:
        console.print("[yellow]⚠ Some sheets failed to process[/yellow]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
