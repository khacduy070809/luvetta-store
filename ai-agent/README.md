# Luvetta Gift Assistant (AI agent trên luvetta.store)

| File | Vai trò |
|---|---|
| `worker.js` | Cloudflare Worker: giữ system prompt, gọi Workers AI, trả lời/khai báo công cụ |
| `luvetta-agent.liquid` | Khung chat trong theme (snippet), thực thi công cụ bằng AJAX Cart API của Shopify |
| `system-prompt-v1.md` | System prompt + 9 kịch bản test |
| `test-log.md` | Kết quả test thật trên website |

## Cài đặt
1. Cloudflare → Workers & Pages → Create → Hello World → dán `worker.js` → Deploy.
2. Settings → Bindings → **Workers AI**, tên biến `AI`.
3. Variables: `ALLOWED_ORIGINS` = `https://luvetta.store,https://www.luvetta.store,https://<store>.myshopify.com`.
4. (Tùy chọn) dùng Gemini: `PROVIDER=gemini` và secret `GEMINI_API_KEY` — **đặt trong Cloudflare, không ghi vào code**.
5. Shopify → Edit code → `snippets/luvetta-agent.liquid` (sửa `endpoint` thành URL Worker) → thêm `{% render 'luvetta-agent' %}` trước `</body>` trong `layout/theme.liquid`.
6. Kiểm tra: mở URL Worker, phải thấy `"ai_binding":true`.

## Giới hạn đã biết / hướng V2
- Bước xác nhận trước khi thêm giỏ hiện dựa vào prompt; V2: công cụ `propose_cart` + nút Confirm bằng code.
- `storeInfo` (chất liệu, ship, đổi trả) để trống cho tới khi xác minh.
