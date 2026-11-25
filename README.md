# Luvetta Shop — Hệ sinh thái thương mại điện tử ứng dụng AI

Bài tập lớn: xây dựng cửa hàng Shopify **luvetta.store** (Dainty Heart Initial Necklace — dây chuyền tim trơn và chữ cái A–Z, Gold/Silver, khách hàng Mỹ) cùng hệ thống AI hỗ trợ bán hàng và vận hành.

## Sơ đồ hệ sinh thái

```
Nội dung (Claude viết kịch bản/prompt → Flow dựng video → CapCut)
        │
        ▼
Facebook / Instagram @luvet.ta  ──►  luvetta.store (Shopify)
        ▲                               │
        │                               ├─ Luvetta Gift Assistant (AI agent trên web, thêm giỏ hàng)
   Muse agent (đăng bài, email,         ├─ Đơn hàng → email xác nhận (Shopify)
   báo cáo — có cổng duyệt)             └─ Dữ liệu → Google Sheets → Looker Studio dashboard
```

## Cấu trúc repo

| Thư mục | Nội dung |
|---|---|
| [`theme/`](theme/) | Code theme Shopify (Liquid, sections Custom Liquid, snippet chatbot) |
| [`ai-agent/`](ai-agent/) | **Luvetta Gift Assistant**: Cloudflare Worker + Workers AI, khung chat, system prompt, nhật ký test |
| [`ai-skills/`](ai-skills/) | 13 AI skill chuẩn Agent Skills (`SKILL.md`), kèm script kiểm tra; `packaged/` là file `.skill` để cài |
| [`muse-agent/`](muse-agent/) | Cấu hình agent Muse: skills, prompts, scripts, workflows (do Muse đóng gói) |
| [`prompts/`](prompts/) | Bộ prompt dựng section (v3), prompt pack Muse, mẫu email |
| [`data/`](data/) | Dữ liệu Shopify đã ẩn danh, file nguồn cho Looker Studio, dashboard PDF |
| [`docs/`](docs/) | Ảnh chụp minh chứng |

## Các thành phần chính

### 1. Website Shopify
- Theme tùy biến bằng các section Custom Liquid (trust bar, story, bundle Buy 2 Get 1, review, guarantee…).
- Prompt dựng từng section: `prompts/sections-v3/`.

### 2. AI agent trên website — Luvetta Gift Assistant
- Kiến trúc: khung chat (snippet Liquid) → Cloudflare Worker (giữ system prompt) → Workers AI `llama-3.3-70b-instruct-fp8-fast`.
- Công cụ (function calling): `check_options`, `add_to_cart`, `view_cart`, `get_store_info`.
- Luôn hỏi xác nhận trước khi thêm vào giỏ. Hướng dẫn cài: [`ai-agent/README.md`](ai-agent/README.md).

### 3. AI skills
13 skill: section builder, liquid debug, code optimizer, test data, bundle builder, gift agent, copywriter, product image, ad video, social content, competitor research, brand identity, ads strategy.
Cài vào Claude: Settings → Capabilities → Skills → Upload file trong `ai-skills/packaged/`. Agent khác hỗ trợ chuẩn Agent Skills: chép thư mục vào thư mục skills của agent.

### 4. Agent vận hành Muse
Đăng video từ Google Drive, email sau đặt hàng, phân loại hộp thư, báo cáo tuần — mọi bài đăng/email đều qua cổng duyệt `DUYỆT / SỬA / TỪ CHỐI`. Xem `muse-agent/` và `prompts/muse-prompt-pack-v1.txt`.

### 5. Dữ liệu & dashboard
- Google Sheets nguồn → Looker Studio (cập nhật khi Sheets thay đổi, làm mới ~15 phút).
- Dashboard PDF tông be kem: `data/dashboard/`.

## Bảo mật dữ liệu
Repo **không** chứa token, khóa API, mật khẩu hay thông tin cá nhân khách hàng. Khóa API (nếu dùng) đặt trong biến môi trường Cloudflare. Email khách đã được che; đơn #1003 là đơn test.

## Công cụ AI đã dùng
Claude (code, prompt, skill, dashboard), ChatGPT, Gemini/Flow (video), Muse (vận hành), Cloudflare Workers AI (chatbot).
