#!/usr/bin/env python3
"""Kiểm tra một khối code Custom Liquid trước khi dán vào Shopify.

Cách dùng:  python check_liquid.py <file.liquid> [--limit 10000]
In ra: số ký tự, số byte UTF-8, và các cảnh báo thường gặp.
Mã thoát 0 = đạt, 1 = có lỗi chặn (vượt giới hạn hoặc lỗi nghiêm trọng).
"""
import argparse, re, sys

def check(code, limit):
    errors, warnings = [], []
    n_chars, n_bytes = len(code), len(code.encode('utf-8'))
    if limit and n_chars > limit:
        errors.append(f"Vượt giới hạn: {n_chars} ký tự > {limit}.")
    if re.search(r'section\.settings', code):
        errors.append("Dùng section.settings — khối Custom Liquid không có settings nên giá trị luôn rỗng.")
    if re.search(r'{%-?\s*schema', code):
        errors.append("Có {% schema %} — không dùng được trong khối Custom Liquid.")
    if re.search(r'\balert\s*\(', code):
        warnings.append("Có alert() — nên hiện thông báo trong giao diện thay vì hộp thoại.")
    if 'DecompressionStream' in code:
        warnings.append("Dùng DecompressionStream — có thể không chạy trên mọi trình duyệt.")
    # cả section bị bọc trong {% if %} ngay ngoài cùng (dễ làm section biến mất)
    body = re.sub(r'<style[\s\S]*?</style>|<script[\s\S]*?</script>|{%-?\s*comment[\s\S]*?endcomment\s*-?%}', '', code)
    body = re.sub(r'{%-?\s*(assign|capture)[\s\S]*?%}', '', body).strip()
    if re.match(r'^{%-?\s*(if|unless)\b', body) and re.search(r'{%-?\s*end(if|unless)\s*-?%}\s*$', body):
        warnings.append("Toàn bộ HTML nằm trong một {% if/unless %} ngoài cùng — kiểm tra section có thể bị ẩn khi biến trống.")
    for tag in ('div', 'section', 'style', 'script'):
        o = len(re.findall(rf'<{tag}\b', code, re.I)); c = len(re.findall(rf'</{tag}>', code, re.I))
        if o != c:
            warnings.append(f"Số thẻ <{tag}> mở ({o}) và đóng ({c}) không khớp.")
    for a, b in (('if', 'endif'), ('for', 'endfor'), ('unless', 'endunless'), ('form', 'endform')):
        o = len(re.findall(rf'{{%-?\s*{a}\b', code)); c = len(re.findall(rf'{{%-?\s*{b}\b', code))
        if o != c:
            errors.append(f"Số {{% {a} %}} ({o}) và {{% {b} %}} ({c}) không khớp.")
    ids = re.findall(r'\bid="([A-Za-z][\w-]*)"', code)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        warnings.append("ID cố định bị trùng: " + ", ".join(dup))
    return n_chars, n_bytes, errors, warnings

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('file'); ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    code = open(a.file, encoding='utf-8').read()
    n, b, errs, warns = check(code, a.limit)
    print(f"Ký tự: {n} | Byte UTF-8: {b}" + (f" | Giới hạn: {a.limit}" if a.limit else ""))
    for e in errs: print("LỖI:", e)
    for w in warns: print("CẢNH BÁO:", w)
    print("KẾT QUẢ:", "ĐẠT" if not errs else "CHƯA ĐẠT")
    sys.exit(1 if errs else 0)
