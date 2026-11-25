"""Kiểm tra dữ liệu trong data/: khớp số liệu và không lộ thông tin khách hàng."""
import csv
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "data" / "shopify-export"


def rows(name):
    with open(EXPORT / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestShopifyData(unittest.TestCase):
    def test_email_khach_da_duoc_che(self):
        for r in rows("orders.csv"):
            with self.subTest(order=r["order"]):
                email = r["customer_email_masked"]
                self.assertRegex(email, r"^.\*{3}@[\w.-]+$|example\.com$")

    def test_khong_co_cot_ten_dia_chi_dien_thoai(self):
        for name in ("orders.csv", "daily.csv", "variants.csv"):
            header = " ".join(rows(name)[0].keys()).lower()
            for bad in ("name", "address", "phone", "zip"):
                with self.subTest(file=name, col=bad):
                    self.assertNotIn(bad, header.replace("customer_email_masked", ""))

    def test_tong_doanh_thu_bien_the_khop_don_hang(self):
        orders = sum(float(r["total_usd"]) for r in rows("orders.csv"))
        variants = sum(float(r["sales_usd"]) for r in rows("variants.csv"))
        self.assertAlmostEqual(orders, variants, places=2)

    def test_so_luong_ban_khop_don_hang(self):
        units = sum(int(r["units"]) for r in rows("variants.csv"))
        purchased = sum(int(r["products_purchased"] or 0) for r in rows("daily.csv"))
        self.assertEqual(units, purchased)

    def test_ngay_lien_tuc_khong_trung(self):
        dates = [r["date"] for r in rows("daily.csv")]
        self.assertEqual(len(dates), len(set(dates)))
        self.assertEqual(dates, sorted(dates))


class TestKhongLoBiMat(unittest.TestCase):
    PATTERNS = [
        r"sk-[A-Za-z0-9]{20,}",            # OpenAI
        r"AIza[0-9A-Za-z_\-]{35}",         # Google API key
        r"ghp_[A-Za-z0-9]{30,}",           # GitHub token
        r"shpat_[a-f0-9]{32}",             # Shopify admin token
        r"[0-9]{9,10}:AA[A-Za-z0-9_\-]{33}",  # Telegram bot token
    ]

    def test_repo_khong_chua_token(self):
        rx = re.compile("|".join(self.PATTERNS))
        for p in ROOT.rglob("*"):
            if not p.is_file() or ".git" in p.parts or p.suffix.lower() in {".png", ".jpg", ".pdf", ".xlsx", ".skill", ".zip"}:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            with self.subTest(file=str(p.relative_to(ROOT))):
                self.assertIsNone(rx.search(text))


if __name__ == "__main__":
    unittest.main()
