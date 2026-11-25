# Lỗi đã gặp ở Luvetta

| Hiện tượng | Nguyên nhân | Cách sửa |
|---|---|---|
| Section dán vào không hiện gì | Toàn bộ HTML bọc trong `{% if %}` với biến đang trống (ví dụ trust bar chờ `review_rating`, `community_url`) | Bỏ `{% if %}` ngoài cùng hoặc cho nội dung mặc định luôn hiện; chỉ ẩn riêng phần thiếu dữ liệu |
| Giá trị luôn rỗng | Dùng `section.settings` trong khối Custom Liquid | Khai báo bằng `{% assign %}` ở đầu code |
| Review hiện trong Theme Editor nhưng không hiện ngoài web | Dữ liệu chỉ có trong mảng mẫu/điều kiện design mode, hoặc review metafield chưa `approved: true` | Kiểm tra nguồn dữ liệu và trường `approved` |
| Review mẫu hiện trên web thật | Mảng `fallbackReviews` không bọc `{% if request.design_mode %}` | Bọc mảng mẫu, ngoài storefront dùng mảng rỗng → "No reviews yet" |
| Không dán được / bị cắt | Code > 10.000 ký tự cho một khối Custom Liquid | Rút gọn, giữ chức năng; kiểm tra bằng check_liquid.py --limit 10000 |
| Chạy trên Chrome, lỗi Safari cũ | Dùng `DecompressionStream` | Bỏ nén, dùng JSON thường |
| Agent chat không trả lời | Sai product handle (`/products/<handle>.js` trả 404) | Handle đúng: `tiny-heart-initial-necklace-gold-silver` |
| Lightbox không đóng bằng phím | Thiếu xử lý `Escape` | Thêm keydown Escape |
