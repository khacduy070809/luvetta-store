---
name: luvetta-test-data
description: "Tạo dữ liệu mẫu (review, danh sách) để kiểm thử giao diện widget Customer Reviews của Luvetta trên Theme Editor, đúng cấu trúc code thật, không để dữ liệu giả lọt ra website công khai. Dùng khi người dùng cần review mẫu, JSON metafield mẫu, hoặc muốn test lọc/sắp xếp/phân trang review."
---

# Luvetta Test Data

Widget Customer Reviews của Luvetta có **2 nguồn dữ liệu**:
- **Review thật**: metafield `product.metafields.custom.customer_reviews` (mảng JSON). Widget chỉ hiển thị phần tử có `approved: true`.
- **Dữ liệu mẫu**: mảng JavaScript `fallbackReviews` trong code, dùng khi metafield chưa có review.

Vì metafield dùng chung cho mọi theme (kể cả theme đang chạy), dữ liệu mẫu KHÔNG được đưa vào metafield. Dữ liệu mẫu phải nằm trong `fallbackReviews` và được bọc `{% if request.design_mode %}` để chỉ hiện trong Theme Editor.

## Quy trình
1. Hỏi: số lượng, cần dạng mảng mẫu (js) hay cấu trúc metafield (json) để minh họa.
2. Chạy script (kết quả có thể lặp lại nhờ seed cố định):
   - `python scripts/make_sample_reviews.py --count 38 --format js` → mảng `fallbackReviews` đã bọc design_mode.
   - `python scripts/make_sample_reviews.py --count 10 --format json` → cấu trúc metafield, mọi phần tử `approved: false`.
3. Trả kết quả + hướng dẫn thay vào đâu trong code widget.

## Cấu trúc một review
`{ "approved": bool (chỉ metafield), "name": str, "rating": 1–5, "title": str, "text": str, "date": "dd/mm/yyyy", "images": [url], "up": int, "down": int }`
Lưu ý tên trường: `text` (không phải body), `up`/`down` (không phải helpful). Ngày dạng dd/mm/yyyy (widget cũng đọc được YYYY-MM-DD).

## Checklist
- Đủ trường hợp: không ảnh, nội dung dài, 1–3 sao
- Mảng mẫu bọc `{% if request.design_mode %}`; mở luvetta.store ở tab ẩn danh không thấy review mẫu
- Không dùng số sao/số lượng review mẫu để quảng cáo
