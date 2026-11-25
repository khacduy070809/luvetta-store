"""Chạy thử các script đi kèm skill và kiểm tra cú pháp script của Muse."""
import json
import py_compile
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK_LIQUID = ROOT / "ai-skills/luvetta-section-builder/scripts/check_liquid.py"
MAKE_REVIEWS = ROOT / "ai-skills/luvetta-test-data/scripts/make_sample_reviews.py"

GOOD = """<style>.lv-box{padding:16px}</style>
<div class="lv-box"><h2>A Little Heart. A Letter That's Yours.</h2></div>
"""
BAD = """<div class="lv-box">{{ section.settings.title }}</div>
{% schema %}{"name":"x"}{% endschema %}
"""


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, timeout=60)


class TestCheckLiquid(unittest.TestCase):
    def _check(self, code):
        with tempfile.NamedTemporaryFile("w", suffix=".liquid", delete=False, encoding="utf-8") as f:
            f.write(code)
        return run(CHECK_LIQUID, f.name)

    def test_code_dung_thi_dat(self):
        self.assertEqual(self._check(GOOD).returncode, 0)

    def test_bat_loi_section_settings_va_schema(self):
        r = self._check(BAD)
        self.assertEqual(r.returncode, 1)
        self.assertIn("section.settings", r.stdout + r.stderr)

    def test_cac_ban_sao_check_liquid_giong_nhau(self):
        copies = sorted(ROOT.glob("ai-skills/*/scripts/check_liquid.py"))
        self.assertGreaterEqual(len(copies), 2)
        first = copies[0].read_bytes()
        for c in copies[1:]:
            with self.subTest(file=str(c.relative_to(ROOT))):
                self.assertEqual(c.read_bytes(), first)


class TestMakeSampleReviews(unittest.TestCase):
    def test_sinh_dung_so_luong_va_chua_duyet(self):
        r = run(MAKE_REVIEWS, "--count", "5", "--seed", "1", "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual(len(data), 5)
        self.assertTrue(all(item["approved"] is False for item in data))

    def test_ban_js_chi_hien_trong_theme_editor(self):
        r = run(MAKE_REVIEWS, "--count", "3")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("request.design_mode", r.stdout)


class TestPythonSyntax(unittest.TestCase):
    def test_moi_file_python_bien_dich_duoc(self):
        files = [p for p in ROOT.rglob("*.py") if ".git" not in p.parts and "theme" not in p.parts]
        self.assertTrue(files)
        for p in files:
            with self.subTest(file=str(p.relative_to(ROOT))):
                py_compile.compile(str(p), doraise=True, cfile=tempfile.mktemp())


if __name__ == "__main__":
    unittest.main()
