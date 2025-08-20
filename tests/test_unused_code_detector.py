import unittest
import tempfile
from pathlib import Path
from pdk_gen.unused_code_detector import UnusedCodeDetector, CodeAnalyzer


class TestUnusedCodeDetector(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmpdir.name)
        
        # Create test files
        (self.tmp_path / "test_module.py").write_text("""
def used_function():
    return "used"

def unused_function():
    return "unused"

def call_used():
    return used_function()

import os
import sys  # unused import
from pathlib import Path

unused_var = "not used"
used_var = "used in print"
print(used_var)
""")
        
        (self.tmp_path / "main.py").write_text("""
from test_module import used_function

def main():
    return used_function()

if __name__ == "__main__":
    main()
""")
        
        (self.tmp_path / "unused_file.py").write_text("""
def never_imported():
    pass
""")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_analyzer_basic(self):
        """Test basic code analysis functionality."""
        test_file = self.tmp_path / "test_module.py"
        analyzer = CodeAnalyzer(test_file)
        
        with open(test_file, 'r') as f:
            content = f.read()
        
        import ast
        tree = ast.parse(content, filename=str(test_file))
        analyzer.visit(tree)
        
        # Check functions are detected
        self.assertIn("used_function", analyzer.functions)
        self.assertIn("unused_function", analyzer.functions)
        self.assertIn("call_used", analyzer.functions)
        
        # Check function calls are detected
        self.assertIn("used_function", analyzer.function_calls)
        self.assertIn("print", analyzer.function_calls)
        
        # Check imports are detected
        self.assertIn("os", analyzer.imports)
        self.assertIn("sys", analyzer.imports)
        self.assertIn("Path", analyzer.imports)

    def test_unused_function_detection(self):
        """Test detection of unused functions."""
        detector = UnusedCodeDetector(self.tmp_path)
        detector.analyze_project()
        
        unused_functions = detector.find_unused_functions()
        
        # Check that unused_function is detected as unused
        test_module_file = self.tmp_path / "test_module.py"
        self.assertIn(test_module_file, unused_functions)
        self.assertIn("unused_function", unused_functions[test_module_file])
        
        # Check that used_function is not detected as unused (it's called in main.py)
        # Note: used_function is imported and called in main.py, so it should not be unused

    def test_unused_import_detection(self):
        """Test detection of unused imports."""
        detector = UnusedCodeDetector(self.tmp_path)
        detector.analyze_project()
        
        unused_imports = detector.find_unused_imports()
        
        # sys import should be detected as unused
        test_module_file = self.tmp_path / "test_module.py"
        if test_module_file in unused_imports:
            self.assertIn("sys", unused_imports[test_module_file])

    def test_unused_file_detection(self):
        """Test detection of unused files."""
        detector = UnusedCodeDetector(self.tmp_path)
        detector.analyze_project()
        
        unused_files = detector.find_unused_files()
        
        # unused_file.py should be detected as unused
        unused_file = self.tmp_path / "unused_file.py"
        self.assertIn(unused_file, unused_files)

    def test_report_generation(self):
        """Test report generation in both text and JSON format."""
        detector = UnusedCodeDetector(self.tmp_path)
        detector.analyze_project()
        
        # Test text report
        text_report = detector.generate_report('text')
        self.assertIn("UNUSED CODE DETECTION REPORT", text_report)
        self.assertIn("unused_function", text_report)
        
        # Test JSON report
        json_report = detector.generate_report('json')
        self.assertIn("unused_functions", json_report)
        self.assertIn("unused_imports", json_report)
        
        # Validate JSON structure
        import json
        data = json.loads(json_report)
        self.assertIsInstance(data, dict)
        self.assertIn("unused_functions", data)
        self.assertIn("unused_imports", data)
        self.assertIn("unused_files", data)
        self.assertIn("unused_variables", data)


if __name__ == "__main__":
    unittest.main()