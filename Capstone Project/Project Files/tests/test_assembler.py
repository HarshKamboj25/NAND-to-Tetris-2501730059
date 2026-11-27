import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assembler import assemble, AssemblerError

class AssemblerTests(unittest.TestCase):
    def test_a_and_c_instructions_and_label(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "T.asm"
            src.write_text("@2\nD=A\n(LOOP)\n@LOOP\n0;JMP\n", encoding="utf-8")
            code, symbols = assemble(src)
            self.assertEqual(code, ["0000000000000010", "1110110000010000",
                                    "0000000000000010", "1110101010000111"])
            self.assertEqual(symbols["LOOP"], 2)

    def test_variable_allocation(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "T.asm"
            src.write_text("@counter\nM=1\n@result\nM=0\n", encoding="utf-8")
            _, symbols = assemble(src)
            self.assertEqual(symbols["counter"], 16)
            self.assertEqual(symbols["result"], 17)

    def test_invalid_comp_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "T.asm"
            src.write_text("D=Q\n", encoding="utf-8")
            with self.assertRaises(AssemblerError):
                assemble(src)


    def test_duplicate_label_feature_warns(self):
        import contextlib, io
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "T.asm"
            src.write_text("(LOOP)\n@LOOP\n(LOOP)\n0;JMP\n", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code, symbols = assemble(src)
            self.assertIn("duplicate label 'LOOP'", stderr.getvalue())
            self.assertEqual(symbols["LOOP"], 0)

if __name__ == "__main__":
    unittest.main()
