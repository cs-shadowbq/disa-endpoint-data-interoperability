# XLS Extractor

A Python CLI tool for intelligently extracting Excel sheets to JSON and Markdown formats.

## Features

- **Smart Detection**: Automatically identifies documentation vs. structured data sheets
- **JSON Export**: Converts tabular data with headers into structured JSON
- **Markdown Export**: Extracts text-based documentation sheets as Markdown
- **Manual Override**: Force specific sheets to use a particular format
- **Batch Processing**: Process multiple Excel files simultaneously
- **Rich CLI**: Beautiful terminal interface with progress indicators and tables

## Installation

### Requirements

- Python 3.8+
- Dependencies: `openpyxl`, `rich`

### Install via pip

```bash
pip install -e .
```

## Quick Start

```bash
# Extract all sheets from a file
xls-extractor data.xlsx

# Specify output directory
xls-extractor data.xlsx --output-dir ./extracted

# Force specific sheets as Markdown
xls-extractor data.xlsx --markdown-sheets "README" "Notes"

# Process multiple files
xls-extractor file1.xlsx file2.xlsx file3.xlsx
```

## How It Works

### Automatic Sheet Detection

The tool analyzes each sheet to determine the best extraction format:

**Documentation Sheets → Markdown**
- Single-column text content
- ≥80% of rows use only the first column
- No clear tabular structure
- Example: README pages, notes, instructions

**Structured Data Sheets → JSON**
- Multiple columns with headers
- First row contains column names
- Consistent data rows below headers
- Example: Tables, lists, inventories

### Output Examples

**JSON Output** (`SheetName.json`):
```json
{
  "SheetName": [
    {
      "Name": "Alice",
      "Age": 30,
      "City": "NYC"
    },
    {
      "Name": "Bob",
      "Age": 25,
      "City": "LA"
    }
  ]
}
```

**Markdown Output** (`Documentation.md`):
```markdown
# Documentation

Introduction

This is a documentation sheet.

It contains text-based content.
```

## CLI Options

```
usage: xls-extractor [-h] [-o OUTPUT_DIR] [-m MARKDOWN_SHEETS [MARKDOWN_SHEETS ...]] [-v] files [files ...]

Extract Excel sheets to JSON and Markdown

positional arguments:
  files                           Excel file(s) to process (.xlsx or .xls)

optional arguments:
  -h, --help                      show this help message and exit
  -o, --output-dir OUTPUT_DIR     Output directory (default: json/)
  -m, --markdown-sheets [...]     Sheet names to force as Markdown
  -v, --version                   show program's version number and exit
```

## Architecture

### Design Principles

The tool follows **SOLID principles** and uses a **modular, testable architecture**:

- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible via interfaces without modifying core code
- **Liskov Substitution**: Writers and extractors are interchangeable
- **Interface Segregation**: Focused, minimal interfaces
- **Dependency Inversion**: Depends on abstractions, not implementations

### Module Structure

```
xls_extractor/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
├── interfaces.py        # Abstract base classes (SheetDetector, SheetWriter, SheetExtractor)
├── detectors.py         # Sheet type detection (DocumentationSheetDetector)
├── extractors.py        # Extraction implementations (JSONExtractor, MarkdownExtractor)
├── writers.py           # Output writers (JSONWriter, MarkdownWriter)
└── processor.py         # Excel file processor (ExcelProcessor)
```

### Class Diagram

```
┌─────────────────┐
│ SheetDetector   │ (Interface)
└─────────────────┘
        △
        │
        │ implements
        │
┌─────────────────────────────┐
│ DocumentationSheetDetector  │
└─────────────────────────────┘

┌─────────────────┐
│ SheetWriter     │ (Interface)
└─────────────────┘
        △
        │
        ├─── JSONWriter
        └─── MarkdownWriter

┌─────────────────┐
│ SheetExtractor  │ (Abstract)
└─────────────────┘
        △
        │
        ├─── JSONExtractor
        └─── MarkdownExtractor

┌─────────────────┐
│ ExcelProcessor  │ (Orchestrator)
└─────────────────┘
```

## Extending the Tool

### Adding a New Output Format

1. **Create a Writer**:
```python
from xls_extractor.interfaces import SheetWriter

class CSVWriter(SheetWriter):
    def write(self, data, output_path, sheet_name):
        # Implementation
        pass
```

2. **Create an Extractor**:
```python
from xls_extractor.interfaces import SheetExtractor

class CSVExtractor(SheetExtractor):
    def __init__(self, writer):
        super().__init__(writer)
    
    def extract(self, sheet_data, sheet_name, output_dir):
        # Implementation
        pass
    
    def can_handle(self, sheet_data):
        # Detection logic
        return True
```

3. **Register in Processor**:
```python
self.csv_extractor = CSVExtractor(CSVWriter())
```

### Adding a New Detector

```python
from xls_extractor.interfaces import SheetDetector

class CustomDetector(SheetDetector):
    def is_documentation_sheet(self, sheet_data):
        # Custom detection logic
        return False
```

## Testing

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=xls_extractor --cov-report=html

# Specific test file
pytest tests/test_extractors.py

# Verbose output
pytest -v
```

### Test Coverage

The project maintains >90% test coverage across:
- Sheet detection logic
- Extraction algorithms
- File writing
- Excel processing
- Error handling

### Example Test

```python
def test_extracts_structured_data(tmp_path):
    extractor = JSONExtractor(JSONWriter())
    
    sheet_data = [
        ["Name", "Age"],
        ["Alice", 30],
        ["Bob", 25]
    ]
    
    extractor.extract(sheet_data, "Users", tmp_path)
    
    output_file = tmp_path / "Users.json"
    assert output_file.exists()
```

## API Usage

### Programmatic Usage

```python
from pathlib import Path
from xls_extractor.processor import ExcelProcessor

# Create processor
processor = ExcelProcessor(
    output_dir=Path("./output"),
    force_markdown_sheets=["README", "Notes"]
)

# Process file
results = processor.process_file(Path("data.xlsx"))

# Check results
print(f"Processed: {results['sheets_processed']}")
print(f"Failed: {results['sheets_failed']}")
```

### Custom Extraction

```python
from xls_extractor.extractors import JSONExtractor
from xls_extractor.writers import JSONWriter
from pathlib import Path

# Create extractor
extractor = JSONExtractor(JSONWriter())

# Extract sheet data
sheet_data = [
    ["Column1", "Column2"],
    ["Value1", "Value2"]
]

extractor.extract(sheet_data, "MySheet", Path("./output"))
```

## Performance

- **Memory Efficient**: Streams data using openpyxl's `iter_rows()`
- **Fast Processing**: Processes typical sheets in milliseconds
- **Batch Friendly**: Handles multiple files without memory issues

## Limitations

- Currently supports `.xlsx` and `.xls` formats only
- Auto-detection may misclassify edge cases (use `--markdown-sheets` to override)
- Formula results only (not the formulas themselves)
- Merged cells are treated as separate cells

## Troubleshooting

### Sheet Not Detected Correctly

Use `--markdown-sheets` to force specific sheets:
```bash
xls-extractor file.xlsx --markdown-sheets "SheetName"
```

### Missing Dependencies

Install all dependencies:
```bash
pip install openpyxl rich
```

### Permission Errors

Ensure output directory is writable:
```bash
chmod 755 json/
```

## Contributing

We welcome contributions! Please:

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass (`pytest`)
5. Run linting (`ruff check src/`)

## License

[Add license information]

## Version History

- **0.1.0** (Initial Release)
  - Automatic sheet type detection
  - JSON and Markdown extraction
  - CLI with rich formatting
  - Comprehensive test suite
