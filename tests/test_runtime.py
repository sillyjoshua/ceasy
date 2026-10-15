import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ceasy_runtime import SecretValue, eval_expr, load_secrets, run_file, RuntimeErrorCeasy

class RuntimeTests(unittest.TestCase):
    def test_python_style_module_calls(self):
        import math
        self.assertEqual(eval_expr("math.sqrt(81)", {"math": math}), 9)

    def test_secret_values_are_redacted_when_printed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "demo.ceasy"
            source.write_text('let token = secret("API_KEY");\nprint(token);\nprint("key=" + token);\n', encoding="utf-8")
            source.with_suffix(".cesecret").write_text(json.dumps({"API_KEY": "very-private-value"}), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                run_file(source)
            self.assertNotIn("very-private-value", output.getvalue())
            self.assertEqual(output.getvalue().count("[secret]"), 2)

    def test_import_statement_and_from_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "imports.ceasy"
            source.write_text('import random;\nfrom math import sqrt;\nlet roll = random.randint(1, 6);\nprint(roll);\nprint(sqrt(81));\n', encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                run_file(source)
            lines = output.getvalue().splitlines()
            self.assertTrue(lines[0].isdigit())
            self.assertEqual(lines[1], "9.0")

    def test_missing_secret_has_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "demo.ceasy"
            source.write_text('print(secret("MISSING"));\n', encoding="utf-8")
            with self.assertRaises(RuntimeErrorCeasy):
                run_file(source)

if __name__ == "__main__":
    unittest.main()
