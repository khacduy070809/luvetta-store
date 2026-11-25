---
name: luvetta-liquid-debug
description: "Tìm và sửa lỗi code Shopify Custom Liquid của Luvetta Shop (section không hiện, hiện trong Theme Editor nhưng không hiện ngoài web, vỡ mobile, quá 10.000 ký tự), và tái dựng prompt có cấu trúc từ code đã chạy. Dùng khi người dùng gửi code Liquid kèm mô tả lỗi, ảnh chụp section bị sai, hoặc muốn 'viết lại prompt từ code này' cho báo cáo."
---

# Luvetta Liquid Debug & Reverse Prompt

Hai chế độ: **Sửa lỗi** (có code + hiện tượng) hoặc **Tái dựng prompt** (có code chạy đúng, cần prompt để tái tạo/ghi báo cáo). Hỏi lại nếu không rõ người dùng cần chế độ nào.

Đọc `references/luvetta-brand.md` trước. Danh sách lỗi đã từng gặp ở Luvetta nằm trong `references/known-issues.md` — đối chiếu đầu tiên vì phần lớn lỗi lặp lại.

## Chế độ 1 — Sửa lỗi
1. Lưu code ra file, chạy `python scripts/check_liquid.py <file>` để bắt lỗi cấu trúc nhanh.
2. Đối chiếu hiện tượng với `known-issues.md`; nếu không khớp, đọc code tìm nguyên nhân gốc.
3. Trả lời theo mẫu:
   - **Nguyên nhân** (1–3 câu, chỉ rõ dòng/đoạn).
   - **Cách sửa**: đoạn code đã sửa tối thiểu, hoặc code thay thế hoàn chỉnh nếu người dùng yêu cầu.
   - **Kiểm tra lại**: kết quả check_liquid sau khi sửa + việc người dùng cần làm (Save, xem tab ẩn danh...).
4. Giữ nguyên mọi chức năng không liên quan đến lỗi.

## Chế độ 2 — Tái dựng prompt từ code
Trích từ code và viết prompt theo đúng khung:
```
VAI TRÒ / BỐI CẢNH (dán hồ sơ thương hiệu) / NHIỆM VỤ
BỐ CỤC & HÀNH VI
NỘI DUNG CHỮ (nguyên văn, đúng thứ tự)
ẢNH / VIDEO (URL)
THÔNG SỐ GIAO DIỆN (tên class + giá trị CSS chính)
RESPONSIVE (từng @media)
YÊU CẦU KỸ THUẬT
TỰ KIỂM TRA / ĐỊNH DẠNG TRẢ VỀ
```
Ghi chú cho người dùng: đây là prompt **tái dựng từ code cuối**, không phải prompt gốc đã gõ — khi đưa vào báo cáo cần ghi rõ như vậy.
