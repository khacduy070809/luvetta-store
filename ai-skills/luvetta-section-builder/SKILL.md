---
name: luvetta-section-builder
description: "Viết hoặc dựng lại section Shopify Custom Liquid cho Luvetta Shop đúng nhận diện thương hiệu (màu, chữ, responsive). Dùng skill này mỗi khi người dùng muốn thêm, sửa, làm lại một khối giao diện trên store Luvetta — hero, story, gallery, review, footer, About Us, video, bundle — hoặc dán code vào Custom Liquid, kể cả khi họ chỉ gửi ảnh mẫu và nói 'làm giống thế này'."
---

# Luvetta Section Builder

Mục tiêu: trả về MỘT khối code Custom Liquid dán vào Shopify là chạy ngay, đúng thương hiệu Luvetta, không vỡ giao diện điện thoại.

## Trước khi làm
1. Đọc `references/luvetta-brand.md` (thương hiệu, thiết kế sản phẩm, bảng màu, điều không được khẳng định).
2. Nếu người dùng muốn **dựng lại một section đang có** của Luvetta (Trust bar, Story, 4-image showcase, Footer, Product info, Bundle selector, Guarantee badge, See it in action, Customer Reviews, Guarantee + Add to cart, About Us), mở `references/luvetta-sections-spec.txt` và dùng đúng phần thông số của section đó: chữ nguyên văn, tên class, giá trị CSS, responsive.

## Quy trình
1. **Làm rõ yêu cầu** (hỏi ngắn gọn nếu thiếu): section đặt ở đâu, nội dung chữ đã chốt, ảnh/video (URL Shopify CDN), có giới hạn ký tự không.
2. **Viết code** theo các quy tắc dưới.
3. **Tự kiểm tra**: lưu code ra file rồi chạy `python scripts/check_liquid.py <file> --limit 10000` (bỏ `--limit` nếu người dùng không yêu cầu). Sửa đến khi KẾT QUẢ: ĐẠT và xử lý mọi CẢNH BÁO hợp lý.
4. **Trả kết quả** theo định dạng đầu ra.

## Quy tắc (và lý do)
- Dùng bảng màu trong hồ sơ thương hiệu; chữ khách nhìn thấy bằng tiếng Anh Mỹ. Lý do: giữ nhận diện nhất quán giữa các section.
- Mọi class có prefix riêng; ID ghép `'tên-' | append: section.id | append: '-' | append: block.id`. Lý do: không đụng CSS theme và dùng section nhiều lần trên một trang không xung đột.
- KHÔNG dùng `section.settings` hay `{% schema %}`: khối Custom Liquid không có settings, giá trị sẽ luôn rỗng.
- KHÔNG bọc toàn bộ section trong `{% if %}` phụ thuộc biến có thể trống: section sẽ biến mất mà người dùng không biết vì sao (lỗi đã gặp ở Trust bar).
- CSS + JS nằm gọn trong khối, JS trong IIFE, không thư viện ngoài, không `alert()`.
- Không tạo nút mua trùng với nút ADD TO CART / Shop Pay gốc của theme.
- Không bịa thông tin sản phẩm (chất liệu, ship, hoàn tiền, số review) — nếu cần, để chỗ trống và hỏi người dùng.
- Khi rút gọn/sửa code cũ: giữ nguyên mọi chức năng đang có và trả code thay thế hoàn chỉnh, không trả đoạn vá lẻ.
- Responsive: kiểm tra bố cục ở ≤749px và màn 360px.

## Định dạng đầu ra
1. Một dòng tóm tắt section làm gì.
2. Một khối code ```liquid hoàn chỉnh.
3. Kết quả `check_liquid.py` (số ký tự + ĐẠT).
4. Tối đa 3 dòng hướng dẫn: dán vào đâu, chỗ nào cần sửa chữ/link.

## Ví dụ
Người dùng: "Làm cho mình thanh trust bar dưới header, shop chưa có review."
→ Thanh luôn hiển thị với "♡ Personalized initials A–Z · Gold or Silver" | "Made to feel personal.", không có sao/số review, link mạng xã hội là biến tùy chọn (trống thì chỉ ẩn link).
