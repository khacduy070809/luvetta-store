---
name: luvetta-bundle-builder
description: "Xây hoặc sửa bộ chọn gói Single / Buy 2 Get 1 Free cho sản phẩm dây chuyền Luvetta trên Shopify: 3 chiếc chọn chữ và màu độc lập, dùng variant ID thật, thêm giỏ qua /cart/add.js, giữ nút Add to Cart và Shop Pay gốc, cấu hình discount Buy X Get Y. Dùng khi người dùng nói về bundle, mua 2 tặng 1, gói combo, tăng giá trị đơn hàng."
---

# Luvetta Bundle Builder

Đọc `references/luvetta-brand.md`. Sản phẩm có 52 biến thể: Option1 = Initial (A–Z), Option2 = Color (Gold/Silver), giá $5.00 mỗi biến thể.

## Quy trình
1. Xác nhận với người dùng: discount Buy X Get Y đã tạo trong Shopify chưa (code giao diện KHÔNG tự tạo ưu đãi — đây là hiểu lầm hay gặp).
2. Viết code bộ chọn (Custom Liquid trong block của main-product) theo đặc tả dưới; kiểm tra bằng `python scripts/check_liquid.py <file>`.
3. Hướng dẫn tạo discount: Discounts → Create → Buy X get Y → Customer buys: 2 sản phẩm Tiny Heart & Initial Necklace → Customer gets: 1 cùng sản phẩm, 100% off → Automatic.
4. Checklist kiểm thử với người dùng: giỏ đúng 3 biến thể đã chọn, tổng sau discount $10.00, mobile không vỡ.

## Đặc tả giao diện & logic
- STEP 1 — CHOOSE YOUR PACKAGE: thẻ SINGLE NECKLACE (nhãn STANDARD, giá `{{ product.selected_or_first_available_variant.price | money }}`) và thẻ BUY 2, GET 1 FREE (nhãn BEST VALUE ★, "🎁 1 necklace FREE").
- STEP 2 — CHOOSE YOUR INITIAL & COLOR: tab NECKLACE 1 / NECKLACE 2 / FREE GIFT 🎁 (chỉ khi gói 3); lưới 26 ô chữ (7 cột); nút màu Gold/Silver.
- Map (chữ, màu) → variant id từ `{{ product.variants | json }}`.
- Gói 1: cập nhật input `name="id"` của form gốc → nút ADD TO CART và Shop Pay gốc hoạt động bình thường.
- Gói 3: chặn submit form gốc, `fetch('/cart/add.js', {items:[{id,quantity:1}×3]})`, rồi chuyển tới `/cart`; ẩn `.shopify-payment-button` khi chọn gói 3 (Shop Pay sẽ bỏ qua logic thêm 3 dòng).
- Lỗi chưa chọn đủ: chữ đỏ dưới bộ chọn, không dùng `alert()`.

## Quy tắc
- Không tạo nút mua trùng lặp.
- Không quảng cáo "Buy 2 Get 1 Free" khi discount chưa bật thật.
