# Kiểm thử tự động

Bộ test chạy tự động trên GitHub Actions mỗi lần đẩy code (xem tab **Actions** của repo).

| File | Kiểm tra gì |
|---|---|
| `test_skills.py` | 13 skill trong `ai-skills/` đúng chuẩn Agent Skills: frontmatter `name`/`description`, file tham chiếu tồn tại, có bản `.skill` đóng gói; skill của Muse có frontmatter |
| `test_scripts.py` | Chạy thật `check_liquid.py` (code đúng → đạt, code sai → báo lỗi), `make_sample_reviews.py` (đánh giá mẫu luôn `approved: false`, chỉ hiện trong Theme Editor); mọi file Python biên dịch được |
| `test_data.py` | Dữ liệu Shopify: email khách đã che, không có cột tên/địa chỉ/điện thoại, doanh thu và số lượng khớp nhau giữa các file; cả repo không chứa token/khóa API |
| `worker.test.mjs` | Chatbot `ai-agent/worker.js` với AI giả lập: chặn website lạ (CORS), gửi đúng system prompt và 4 công cụ, chuyển lệnh gọi công cụ, chống gọi công cụ lặp, báo lỗi khi hết hạn mức |

## Chạy trên máy

```bash
python -m unittest discover -s tests -v
node --test tests/worker.test.mjs
```

Cần Python 3.10+ và Node 22+. Chatbot được test bằng AI giả lập nên không cần tài khoản Cloudflare.
