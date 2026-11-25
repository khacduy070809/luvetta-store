# Test log — Luvetta Gift Assistant

Môi trường: luvetta.store (theme chính Shrine PRO, ID 167968375030) và theme nháp "Copy of…" (ID 168926314742).
Server: Cloudflare Worker `luvetta-agent` v1.3, model `@cf/meta/llama-3.3-70b-instruct-fp8-fast`.

| # | Ngày | Khách nhắn | Agent làm gì | Kết quả |
|---|---|---|---|---|
| 1 | 17/11 | (bản Gemini) "Help me pick a gift" | Lỗi `User location is not supported` — Worker chạy qua máy chủ Hồng Kông | Lỗi → chuyển sang Workers AI |
| 2 | 17/11 | "I need a gift for my girlfriend Sarah" | Không trả lời — sai handle sản phẩm (`dainty-heart-initial-necklace`) | Lỗi → sửa handle thành `tiny-heart-initial-necklace-gold-silver` |
| 3 | 17/11 | (test server) "I need a gift for my girlfriend Sarah" | Gọi `check_options` lặp lại, không đọc được kết quả công cụ | Lỗi → server v1.3 đổi định dạng kết quả công cụ |
| 4 | 17/11 | (test server) "Gold please" | Thêm S/Gold vào giỏ KHÔNG hỏi lại xác nhận | Lỗi prompt → căn cứ viết v2 |
| 5 | 17/11 | (test server) "Is it real gold?" | Gọi `get_store_info(materials)`, trả lời không đoán, mời xem chính sách | Đạt |
| 6 | 17/11 | Theme nháp: Sarah → "Gold please" → "yes" | Gợi ý chữ S, hỏi màu, hỏi xác nhận, thêm S/Gold vào giỏ thật ($5.00) | Đạt |
| 7 | 17/11 | Web chính: "Hi! I want a necklace for my mom, her name is Emma" → "Silver please" → "yes" | Gợi ý chữ E, xác nhận, thêm E/Silver vào giỏ; nhắc giỏ đã có S/Gold (tổng $10.00) | Đạt |

Lỗi còn lại cho v2: agent gọi sản phẩm là "Dainty Heart Initial Necklace" trong khi tên trên Shopify là "Tiny Heart & Initial Necklace".
