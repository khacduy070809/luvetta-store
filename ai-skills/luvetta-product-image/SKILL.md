---
name: luvetta-product-image
description: "Viết prompt tạo ảnh (và kiểm tra ảnh) sản phẩm Dainty Heart Initial Necklace của Luvetta đúng thiết kế hai mặt rời: ảnh UGC, banner, ảnh đeo cổ, mở hộp quà, flat lay. Dùng mỗi khi người dùng cần ảnh sản phẩm cho website, quảng cáo hay mạng xã hội, hoặc gửi ảnh AI để hỏi có đúng sản phẩm không."
---

# Luvetta Product Image

Lỗi phổ biến nhất của AI tạo ảnh với sản phẩm này là **khắc chữ vào trong trái tim** hoặc gộp tim và chữ thành một mặt. Skill này tồn tại để chặn lỗi đó. Đọc `references/luvetta-brand.md` trước.

## Quy trình
1. Hỏi (nếu thiếu): mục đích (web/ads/social), tỉ lệ khung (9:16, 1:1, 4:5, 16:9), chữ cái, màu Gold/Silver, bối cảnh, có lộ mặt người mẫu không.
2. Viết prompt tiếng Anh theo mẫu dưới. Nếu công cụ tạo ảnh có sẵn trong phiên, tạo ảnh; nếu không, trả prompt để người dùng dán vào ChatGPT/Gemini.
3. Kiểm tra mỗi ảnh theo checklist; ảnh sai → nêu lỗi cụ thể và bổ sung điều cấm tương ứng vào prompt, tạo lại.

## Mẫu prompt
```text
Photo-realistic [UGC / product / lifestyle] photo, [aspect ratio].
A dainty [Gold/Silver] necklace with TWO separate tiny charms side by side on the same thin chain:
a plain polished heart with no engraving on the LEFT, and a separate capital letter "[X]" on the RIGHT.
Charms are small and delicate (about 1 cm). Scene: [scene]. Natural soft light, warm cream tones (#FFF7F3, #F8EAE3).
[If no face: frame from mid-neck down only — no chin, mouth, nose or eyes.]
DO NOT: put the letter inside the heart, engrave the heart, merge heart and letter into one pendant,
add gems/diamonds/pearls, double chain, oversized charms, extra text or logos.
```

## Checklist cho mỗi ảnh
- Hai mặt rời, tim trơn bên trái, chữ đúng ký tự bên phải
- Kích thước thanh mảnh, không quá khổ
- Không lỗi tay/ngón, không chữ méo
- Không logo/thương hiệu bên thứ ba
- Ghi chú cho người dùng: ảnh AI không được dùng như ảnh khách hàng thật

## Đầu ra
Prompt (khối text) + danh sách ảnh đã kiểm tra kèm Đạt/Lỗi và lý do.
