---
name: luvetta-gift-agent
description: "Triển khai, cấu hình, kiểm thử và cải tiến Luvetta Gift Assistant — chatbot AI agent tư vấn quà và thêm dây chuyền vào giỏ trên luvetta.store (Cloudflare Worker + Workers AI + snippet Liquid). Dùng khi người dùng muốn cài lại chatbot, sửa system prompt, thêm công cụ, debug chatbot không trả lời, hoặc chạy kịch bản test cho agent."
---

# Luvetta Gift Assistant (AI agent)

Kiến trúc: khung chat (`assets/luvetta-agent.liquid`, snippet render trước `</body>` trong `layout/theme.liquid`) → server Cloudflare Worker (`assets/worker.js`, giữ system prompt) → Workers AI (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`). Công cụ chạy trên trình duyệt khách: `check_options`, `add_to_cart`, `view_cart`, `get_store_info`.

Tài liệu: `references/system-prompt-v1.md` (prompt + 9 kịch bản test), `references/test-log.md` (kết quả test thật), `references/luvetta-brand.md`.

## Việc thường gặp
**Cài lại từ đầu**
1. Cloudflare → Workers & Pages → Create → Hello World → dán `assets/worker.js` → Deploy.
2. Settings → Bindings → Workers AI, tên biến `AI`. Variables: `ALLOWED_ORIGINS` = `https://luvetta.store,https://www.luvetta.store,https://gpwyyp-dq.myshopify.com`.
3. Mở URL Worker: phải thấy `"ai_binding":true`.
4. Shopify → Edit code → snippets → tạo `luvetta-agent.liquid` từ `assets/` (sửa `endpoint`), thêm `{% render 'luvetta-agent' %}` trước `</body>`.

**Debug "chat không trả lời"** — kiểm tra theo thứ tự: URL Worker GET có `ai_binding:true`? → origin trang có trong ALLOWED_ORIGINS? → `/products/<productHandle>.js` trả 200? → bật `debug: true` trong CONFIG để thấy từng bước công cụ trong khung chat.

**Chạy kiểm thử** — chạy 9 kịch bản trong system-prompt-v1.md, ghi thêm dòng vào test-log.md (ngày, câu khách, agent làm gì, Đạt/Lỗi).

## Trạng thái hiện tại (trung thực)
- Đã chạy thật trên luvetta.store; test log: 7 lần (3 đạt, 4 phát hiện lỗi). Chưa chạy đủ 9 kịch bản.
- `bundleActive: false`; storeInfo (chất liệu, ship, đổi trả) trống → agent đưa link chính sách thay vì trả lời.
- Hỏi xác nhận trước khi thêm giỏ hiện chỉ dựa vào system prompt (test #4 từng bỏ qua).

## Đề xuất V2 (chưa triển khai)
1. Chốt xác nhận bằng code: công cụ `propose_cart` hiện thẻ sản phẩm + nút Confirm; chỉ khi khách bấm, JavaScript mới gọi `/cart/add.js`; AI không gọi thêm giỏ trực tiếp.
2. Thống nhất tên sản phẩm trong system prompt với tên trên Shopify.
3. Điền storeInfo đã xác minh; chỉ bật bundleActive khi discount chạy thật.
