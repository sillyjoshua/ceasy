import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ceasy import CeasyError, compile_source

class CeasyTests(unittest.TestCase):
    def test_print_string(self):
        output = compile_source('print("Hello");')
        self.assertIn('printf("%s\\n", "Hello");', output)

    def test_integer_variable(self):
        output = compile_source('let score = 42;\nprint(score);')
        self.assertIn('int score = 42;', output)
        self.assertIn('printf("%d\\n", score);', output)

    def test_decimal_variable(self):
        output = compile_source('let ratio = 3.14;\nprint(ratio);')
        self.assertIn('double ratio = 3.14;', output)
        self.assertIn('printf("%f\\n", ratio);', output)

    def test_unknown_variable_fails(self):
        with self.assertRaises(CeasyError):
            compile_source('print(missing);')

    def test_duplicate_declaration_fails(self):
        with self.assertRaises(CeasyError):
            compile_source('let x = 1;\nlet x = 2;')

if __name__ == '__main__':
    unittest.main()