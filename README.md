<div align="center">

# LUVETTA SHOP — Hệ sinh thái thương mại điện tử ứng dụng AI

### Shopify · AI Agent · AI Skills · Prompt Engineering · Data Dashboard

**Bài tập lớn môn Phân tích Web** · Giảng viên: Thầy Noah · Học viện Công nghệ Bưu chính Viễn thông (PTIT)

[![Kiểm thử](https://github.com/khacduy070809/luvetta-store/actions/workflows/tests.yml/badge.svg)](https://github.com/khacduy070809/luvetta-store/actions/workflows/tests.yml)
[![Website](https://img.shields.io/badge/Website-luvetta.store-B47E70)](https://luvetta.store)
![Shopify](https://img.shields.io/badge/Shopify-Liquid-7AB55C?logo=shopify&logoColor=white)
![Cloudflare Workers AI](https://img.shields.io/badge/Cloudflare-Workers_AI-F38020?logo=cloudflare&logoColor=white)
![Agent Skills](https://img.shields.io/badge/AI_Skills-14-56392F)
![Ngôn ngữ](https://img.shields.io/badge/Tài_liệu-Tiếng_Việt-16a34a)

</div>

---

## Thành viên nhóm

| STT | Họ và tên | Mã sinh viên | Phụ trách |
|---|---|---|---|
| 1 | _(cập nhật)_ | | |
| 2 | _(cập nhật)_ | | |
| 3 | _(cập nhật)_ | | |
| 4 | _(cập nhật)_ | | |

## Mục lục

1. [Giới thiệu](#1-giới-thiệu)
2. [Sơ đồ hệ sinh thái](#2-sơ-đồ-hệ-sinh-thái)
3. [Cấu trúc repo](#3-cấu-trúc-repo)
4. [Các thành phần chính](#4-các-thành-phần-chính)
5. [Kiểm thử tự động](#5-kiểm-thử-tự-động)
6. [Bảo mật dữ liệu](#6-bảo-mật-dữ-liệu)
7. [Công cụ AI đã dùng](#7-công-cụ-ai-đã-dùng)

## 1. Giới thiệu

Bài tập lớn: xây dựng cửa hàng Shopify **luvetta.store** (Dainty Heart Initial Necklace — dây chuyền tim trơn và chữ cái A–Z, Gold/Silver, khách hàng Mỹ) cùng hệ thống AI hỗ trợ bán hàng và vận hành. Nhận diện thương hiệu: [`docs/brand/Luvetta_Brand_Identity.pdf`](docs/brand/Luvetta_Brand_Identity.pdf).

## 2. Sơ đồ hệ sinh thái

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

## 3. Cấu trúc repo

| Thư mục | Nội dung |
|---|---|
| [`theme/`](theme/) | Code theme Shopify (Liquid, sections Custom Liquid, snippet chatbot) |
| [`ai-agent/`](ai-agent/) | **Luvetta Gift Assistant**: Cloudflare Worker + Workers AI, khung chat, system prompt, nhật ký test |
| [`ai-skills/`](ai-skills/) | 13 AI skill chuẩn Agent Skills (`SKILL.md`), kèm script kiểm tra; `packaged/` là file `.skill` để cài |
| [`muse-agent/`](muse-agent/) | Cấu hình agent Muse: skills, prompts, scripts, workflows (do Muse đóng gói) |
| [`prompts/`](prompts/) | Bộ prompt dựng section (v3), prompt pack Muse, mẫu email |
| [`data/`](data/) | Dữ liệu Shopify đã ẩn danh, file nguồn cho Looker Studio, dashboard PDF |
| [`docs/`](docs/) | Ảnh chụp minh chứng, tài liệu nhận diện thương hiệu (PDF) |
| [`tests/`](tests/) | Kiểm thử tự động cho skill, chatbot, script và dữ liệu |

## 4. Các thành phần chính

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

## 5. Kiểm thử tự động

27 bài test chạy tự động trên GitHub Actions mỗi lần đẩy code (huy hiệu **Kiểm thử** ở đầu trang):
- **AI skills**: đúng chuẩn Agent Skills, file tham chiếu tồn tại, có bản đóng gói.
- **Chatbot**: chạy `worker.js` với AI giả lập — chặn website lạ, đúng system prompt và 4 công cụ, chống gọi công cụ lặp, xử lý hết hạn mức.
- **Script**: chạy thật `check_liquid.py`, `make_sample_reviews.py`; mọi file Python biên dịch được.
- **Dữ liệu**: email khách đã che, số liệu khớp giữa các file, repo không chứa token.

Chạy trên máy: `python -m unittest discover -s tests -v` và `node --test tests/worker.test.mjs`. Chi tiết: [`tests/README.md`](tests/README.md).

## 6. Bảo mật dữ liệu
Repo **không** chứa token, khóa API, mật khẩu hay thông tin cá nhân khách hàng. Khóa API (nếu dùng) đặt trong biến môi trường Cloudflare. Email khách đã được che; đơn #1003 là đơn test.

## 7. Công cụ AI đã dùng
Claude (code, prompt, skill, dashboard), ChatGPT, Gemini/Flow (video), Muse (vận hành), Cloudflare Workers AI (chatbot).
