"""Kiểm tra 13 AI skill (ai-skills/) và skill của Muse đúng chuẩn Agent Skills.

Chạy:  python -m unittest discover -s tests -v
"""
import json
import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "ai-skills"
PACKAGED = SKILLS / "packaged"
SKILL_DIRS = sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())
MUSE_SKILLS = sorted((ROOT / "muse-agent" / "skills").glob("*/SKILL.md"))


def frontmatter(md_path):
    text = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, val = line.split(":", 1)
        val = val.strip()
        if val.startswith('"'):
            val = json.loads(val)
        meta[key.strip()] = val
    return meta, text[m.end():]


class TestAiSkills(unittest.TestCase):
    def test_so_luong_skill(self):
        # Yêu cầu BTL: 7–10 skill trở lên
        self.assertGreaterEqual(len(SKILL_DIRS), 7)

    def test_frontmatter_hop_le(self):
        for d in SKILL_DIRS:
            with self.subTest(skill=d.name):
                meta, body = frontmatter(d / "SKILL.md")
                self.assertIsNotNone(meta, "thiếu khối frontmatter ---")
                self.assertEqual(meta.get("name"), d.name, "name phải trùng tên thư mục")
                self.assertRegex(meta["name"], r"^[a-z0-9-]{1,64}$")
                desc = meta.get("description", "")
                self.assertTrue(20 <= len(desc) <= 1024, f"description dài {len(desc)} ký tự")
                self.assertNotIn("<", desc)
                self.assertGreater(len(body.strip()), 200, "thân SKILL.md quá ngắn")

    def test_file_tham_chieu_ton_tai(self):
        # Mọi đường dẫn references/, scripts/, assets/ nhắc trong SKILL.md phải có thật
        for d in SKILL_DIRS:
            text = (d / "SKILL.md").read_text(encoding="utf-8")
            for rel in set(re.findall(r"((?:references|scripts|assets)/[\w.\-/]+\.\w+)", text)):
                with self.subTest(skill=d.name, file=rel):
                    self.assertTrue((d / rel).is_file(), f"{rel} không tồn tại")

    def test_ban_dong_goi_day_du(self):
        for d in SKILL_DIRS:
            with self.subTest(skill=d.name):
                pkg = PACKAGED / f"{d.name}.skill"
                self.assertTrue(pkg.is_file(), "thiếu file .skill trong packaged/")
                with zipfile.ZipFile(pkg) as z:
                    names = z.namelist()
                self.assertIn(f"{d.name}/SKILL.md", names)


class TestMuseSkill(unittest.TestCase):
    def test_muse_skill_co_frontmatter(self):
        self.assertTrue(MUSE_SKILLS, "chưa có skill nào trong muse-agent/skills/")
        for md in MUSE_SKILLS:
            with self.subTest(skill=md.parent.name):
                meta, _ = frontmatter(md)
                self.assertIsNotNone(meta)
                self.assertTrue(meta.get("name"))
                self.assertTrue(meta.get("description"))


if __name__ == "__main__":
    unittest.main()
