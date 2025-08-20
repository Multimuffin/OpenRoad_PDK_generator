# Unused Code Detection

This document describes the unused code detection functionality that has been added to the PDK Generator project.

## Overview

The unused code detector is a static analysis tool that identifies potentially unused code in the PDK Generator codebase, including:

- **Unused functions and methods**: Functions that are defined but never called
- **Unused imports**: Import statements for modules/symbols that are never used
- **Unused files/modules**: Python files that are never imported by other modules
- **Unused variables**: Variables that are assigned but never referenced

## Usage

### Command Line Interface

The unused code detector can be run using the `pdk-unused` command:

```bash
# Analyze the entire project
pdk-unused

# Analyze a specific directory  
pdk-unused --path pdk_gen

# Generate JSON output
pdk-unused --json

# Enable verbose logging
pdk-unused --verbose
```

### Programmatic Usage

```python
from pdk_gen.unused_code_detector import UnusedCodeDetector
from pathlib import Path

# Create detector instance
detector = UnusedCodeDetector(Path("./pdk_gen"))

# Analyze the code
detector.analyze_project()

# Generate report
report = detector.generate_report('text')
print(report)

# Get specific unused items
unused_functions = detector.find_unused_functions()
unused_imports = detector.find_unused_imports()
unused_files = detector.find_unused_files()
unused_variables = detector.find_unused_variables()
```

## Features

### Smart Analysis

The detector uses AST (Abstract Syntax Tree) parsing to analyze Python code and build a comprehensive usage graph. It understands:

- Function definitions and calls
- Import statements and usage
- Variable assignments and references
- Class definitions and method calls
- Attribute access patterns

### False Positive Filtering

The detector includes intelligent filtering to reduce false positives:

- **Entry Points**: Functions used as CLI commands or main scripts are never marked as unused
- **Special Methods**: Python magic methods (`__init__`, `__str__`, etc.) are excluded
- **Test Methods**: unittest methods (`test_*`, `setUp`, `tearDown`) are excluded
- **Framework Methods**: AST visitor methods (`visit_*`) and other framework callbacks are excluded
- **Test Files**: Files starting with `test_` are excluded from unused file detection

### Multiple Output Formats

- **Text Format**: Human-readable report with organized sections
- **JSON Format**: Machine-readable output for integration with other tools

## Example Output

```
============================================================
UNUSED CODE DETECTION REPORT
============================================================

🔍 UNUSED FUNCTIONS:

  📄 pdk_gen/file_finder.py:
    - find_lib_files_by_corner()
    - list_subdirs()

  📄 pdk_gen/dir_utils.py:
    - create_named_dir()

📦 UNUSED IMPORTS:

  📄 pdk_gen/config_updater.py:
    - scripts

📁 UNUSED FILES:
  - pdk_gen/resource_utils.py

🔤 UNUSED VARIABLES:

  📄 pdk_gen/config_updater.py:
    - scripts

============================================================
```

## Current Findings

As of the current analysis, the detector has identified the following unused code in the PDK Generator:

### Unused Functions
- `pdk_gen/config_updater_dongbu.py`: `_find_first()` - Helper method that's defined but never called
- `pdk_gen/file_finder.py`: `find_lib_files_by_corner()`, `list_subdirs()` - Utility functions with commented imports
- `pdk_gen/dir_utils.py`: `create_named_dir()` - Directory creation utility that's never used
- `pdk_gen/config_updater.py`: `_find_first()` - Duplicate helper method

### Unused Files
- `pdk_gen/resource_utils.py` - Contains functions that are duplicated in `symlink_utils.py`

### Unused Variables
- `pdk_gen/config_updater.py`: `scripts` - Variable assigned but never used

## Integration

The unused code detector is integrated into the PDK Generator package as:

1. **CLI Command**: `pdk-unused` for standalone usage
2. **Python Module**: `pdk_gen.unused_code_detector` for programmatic access
3. **Test Suite**: Comprehensive tests in `tests/test_unused_code_detector.py`

## Limitations

- **Dynamic Imports**: Code that is imported using `importlib` or similar dynamic mechanisms may not be detected
- **String-based References**: Functions called via string names or `getattr()` may be missed
- **External Usage**: The detector only analyzes the current project and cannot detect usage from external packages
- **Comment Dependencies**: Some imports may be needed for type hints in comments or documentation

## Maintenance

The unused code detector should be run periodically as part of code maintenance to:

1. Identify and remove dead code
2. Clean up unused imports
3. Detect duplicate functionality
4. Improve code quality and maintainability

Regular usage helps keep the codebase clean and reduces maintenance overhead.