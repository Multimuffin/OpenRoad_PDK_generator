#!/usr/bin/env python3
"""
Unused Code Detector for PDK Generator

This module analyzes the PDK Generator codebase to detect potentially unused code including:
- Unused functions and methods
- Unused imports  
- Unused files/modules
- Dead code paths

Usage:
    python -m pdk_gen.unused_code_detector [--path PATH] [--json]
"""

import ast
import json
from pathlib import Path
from typing import Dict, Set, List, Optional
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class CodeAnalyzer(ast.NodeVisitor):
    """AST visitor to extract functions, classes, and imports from Python files."""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.module_name = self._get_module_name(filepath)
        self.imports = set()  # All imports in this file
        self.from_imports = defaultdict(set)  # from X import Y mappings
        self.functions = set()  # Function names defined in this file  
        self.classes = set()  # Class names defined in this file
        self.function_calls = set()  # Function names called in this file
        self.attribute_access = set()  # Attribute access like obj.method
        self.variables = set()  # Variables assigned in this file
        self.variable_usage = set()  # Variables used/referenced in this file
        
    def _get_module_name(self, filepath: Path) -> str:
        """Convert file path to module name."""
        # Assume we're analyzing from the project root
        try:
            relative = filepath.relative_to(Path.cwd())
            parts = list(relative.parts[:-1]) + [relative.stem]
            if parts[-1] == '__init__':
                parts = parts[:-1]
            return '.'.join(parts)
        except ValueError:
            # If path is not relative to cwd, use absolute path parts
            parts = list(filepath.parts)
            if parts[-1].endswith('.py'):
                parts[-1] = parts[-1][:-3]
            if parts[-1] == '__init__':
                parts = parts[:-1]
            return '.'.join(parts)
    
    def visit_Import(self, node):
        """Handle 'import x' statements."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.add(name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Handle 'from x import y' statements."""
        module = node.module or ''
        for alias in node.names:
            imported_name = alias.asname if alias.asname else alias.name
            self.from_imports[module].add(imported_name)
            # Also add to general imports for easier lookup
            self.imports.add(imported_name)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Handle function definitions."""
        self.functions.add(node.name)
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Handle async function definitions.""" 
        self.functions.add(node.name)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Handle class definitions."""
        self.classes.add(node.name)
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Handle function calls."""
        if isinstance(node.func, ast.Name):
            self.function_calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # For method calls like obj.method()
            self.attribute_access.add(node.func.attr)
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Handle variable names and references."""
        if isinstance(node.ctx, ast.Store):
            self.variables.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.variable_usage.add(node.id)
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """Handle attribute access like obj.attr."""
        if isinstance(node.ctx, ast.Load):
            self.attribute_access.add(node.attr)
        self.generic_visit(node)


class UnusedCodeDetector:
    """Main class for detecting unused code in the PDK Generator project."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.analyzers: Dict[Path, CodeAnalyzer] = {}
        self.entry_points = set()
        
    def analyze_file(self, filepath: Path) -> Optional[CodeAnalyzer]:
        """Analyze a single Python file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(filepath))
            analyzer = CodeAnalyzer(filepath)
            analyzer.visit(tree)
            return analyzer
            
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.warning(f"Could not parse {filepath}: {e}")
            return None
    
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project."""
        python_files = []
        for pattern in ['**/*.py']:
            python_files.extend(self.project_path.glob(pattern))
        return [f for f in python_files if not any(part.startswith('.') for part in f.parts)]
    
    def analyze_project(self):
        """Analyze all Python files in the project."""
        python_files = self.find_python_files()
        
        for filepath in python_files:
            analyzer = self.analyze_file(filepath)
            if analyzer:
                self.analyzers[filepath] = analyzer
        
        # Identify entry points (files with if __name__ == "__main__" or CLI commands)
        self._identify_entry_points()
    
    def _identify_entry_points(self):
        """Identify entry points like CLI commands and main scripts."""
        # Known entry points from setup.py
        entry_points = {
            'pdk_gen.cli:main',
            'pdk_gen.setup_config:run_setup'
        }
        
        for entry in entry_points:
            module_path, func_name = entry.split(':')
            module_parts = tuple(module_path.split('.'))  # Convert to tuple for hashing
            self.entry_points.add((module_parts, func_name))
        
        # Also check for files with if __name__ == "__main__"
        for filepath, analyzer in self.analyzers.items():
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    if 'if __name__ == "__main__"' in content:
                        self.entry_points.add((tuple(filepath.parts), '__main__'))
            except:
                pass
    
    def find_unused_functions(self) -> Dict[str, Set[str]]:
        """Find functions that are defined but never called."""
        all_function_calls = set()
        all_attribute_calls = set()
        defined_functions = {}
        
        # Collect all function calls and definitions
        for filepath, analyzer in self.analyzers.items():
            all_function_calls.update(analyzer.function_calls)
            all_attribute_calls.update(analyzer.attribute_access)
            
            for func_name in analyzer.functions:
                defined_functions[f"{analyzer.module_name}:{func_name}"] = filepath
        
        # Find unused functions
        unused = {}
        for func_key, filepath in defined_functions.items():
            module_name, func_name = func_key.split(':', 1)
            
            # Skip if it's an entry point
            is_entry_point = any(
                func_name == entry_func for entry_parts, entry_func in self.entry_points
            )
            
            # Skip special methods and test methods
            if (func_name.startswith('__') and func_name.endswith('__') or
                func_name.startswith('test_') or
                func_name in ['setUp', 'tearDown'] or  # unittest methods
                func_name.startswith('visit_')):  # AST visitor methods
                continue
                
            # Skip if function is called anywhere or used as method
            if (func_name in all_function_calls or 
                func_name in all_attribute_calls or 
                is_entry_point):
                continue
            
            if filepath not in unused:
                unused[filepath] = set()
            unused[filepath].add(func_name)
        
        return unused
    
    def find_unused_imports(self) -> Dict[str, Set[str]]:
        """Find imports that are imported but never used."""
        unused = {}
        
        for filepath, analyzer in self.analyzers.items():
            unused_imports = set()
            
            # Check regular imports
            for import_name in analyzer.imports:
                if (import_name not in analyzer.function_calls and
                    import_name not in analyzer.variable_usage and
                    import_name not in analyzer.attribute_access):
                    unused_imports.add(import_name)
            
            if unused_imports:
                unused[filepath] = unused_imports
        
        return unused
    
    def find_unused_files(self) -> Set[Path]:
        """Find Python files that are never imported."""
        imported_modules = set()
        
        # Collect all imported modules
        for analyzer in self.analyzers.values():
            for module in analyzer.from_imports.keys():
                if module:  # Skip empty module names
                    imported_modules.add(module)
            
            # Also check for direct module imports
            for import_name in analyzer.imports:
                if '.' in import_name:
                    imported_modules.add(import_name)
        
        # Find files that are never imported
        unused_files = set()
        for filepath, analyzer in self.analyzers.items():
            module_name = analyzer.module_name
            
            # Skip entry points, test files, setup files, and our detector
            if (filepath.name.startswith('test_') or 
                filepath.name == '__init__.py' or
                filepath.name == 'setup.py' or
                filepath.name == 'unused_code_detector.py' or  # Skip our own detector
                any(entry_parts for entry_parts, _ in self.entry_points if 
                    analyzer.module_name.endswith('.'.join(entry_parts[-2:])))):
                continue
            
            # Check if this module is imported anywhere
            is_imported = any(
                module_name.endswith(imported) or imported.endswith(module_name.split('.')[-1])
                for imported in imported_modules
            )
            
            if not is_imported:
                unused_files.add(filepath)
        
        return unused_files
    
    def find_unused_variables(self) -> Dict[str, Set[str]]:
        """Find variables that are defined but never used."""
        unused = {}
        
        for filepath, analyzer in self.analyzers.items():
            unused_vars = set()
            
            for var_name in analyzer.variables:
                # Skip special variables and constants
                if (var_name.startswith('_') or 
                    var_name.isupper() or 
                    var_name in analyzer.variable_usage):
                    continue
                
                unused_vars.add(var_name)
            
            if unused_vars:
                unused[filepath] = unused_vars
        
        return unused
    
    def generate_report(self, output_format='text') -> str:
        """Generate a comprehensive unused code report."""
        unused_functions = self.find_unused_functions()
        unused_imports = self.find_unused_imports()
        unused_files = self.find_unused_files()
        unused_variables = self.find_unused_variables()
        
        if output_format == 'json':
            return json.dumps({
                'unused_functions': {str(k): list(v) for k, v in unused_functions.items()},
                'unused_imports': {str(k): list(v) for k, v in unused_imports.items()},
                'unused_files': [str(f) for f in unused_files],
                'unused_variables': {str(k): list(v) for k, v in unused_variables.items()}
            }, indent=2)
        
        # Text format
        report = []
        report.append("=" * 60)
        report.append("UNUSED CODE DETECTION REPORT")
        report.append("=" * 60)
        
        # Unused functions
        if unused_functions:
            report.append("\n🔍 UNUSED FUNCTIONS:")
            for filepath, functions in unused_functions.items():
                report.append(f"\n  📄 {filepath}:")
                for func in sorted(functions):
                    report.append(f"    - {func}()")
        else:
            report.append("\n✅ No unused functions found")
        
        # Unused imports
        if unused_imports:
            report.append("\n\n📦 UNUSED IMPORTS:")
            for filepath, imports in unused_imports.items():
                report.append(f"\n  📄 {filepath}:")
                for imp in sorted(imports):
                    report.append(f"    - {imp}")
        else:
            report.append("\n\n✅ No unused imports found")
        
        # Unused files
        if unused_files:
            report.append("\n\n📁 UNUSED FILES:")
            for filepath in sorted(unused_files):
                report.append(f"  - {filepath}")
        else:
            report.append("\n\n✅ No unused files found")
        
        # Unused variables
        if unused_variables:
            report.append("\n\n🔤 UNUSED VARIABLES:")
            for filepath, variables in unused_variables.items():
                report.append(f"\n  📄 {filepath}:")
                for var in sorted(variables):
                    report.append(f"    - {var}")
        else:
            report.append("\n\n✅ No unused variables found")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)


def main():
    """CLI interface for the unused code detector."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Detect unused code in PDK Generator')
    parser.add_argument('--path', type=Path, default=Path.cwd(), 
                       help='Path to analyze (default: current directory)')
    parser.add_argument('--json', action='store_true',
                       help='Output results in JSON format')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format='%(levelname)s: %(message)s'
    )
    
    # Run analysis
    detector = UnusedCodeDetector(args.path)
    detector.analyze_project()
    
    # Generate and print report
    output_format = 'json' if args.json else 'text'
    report = detector.generate_report(output_format)
    print(report)


if __name__ == '__main__':
    main()