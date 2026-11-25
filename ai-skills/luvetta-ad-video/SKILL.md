---
name: luvetta-ad-video
description: "Viết kịch bản và prompt từng cảnh cho video quảng cáo dọc 9:16 của Luvetta (TikTok, Reels, Facebook Ads) giữ nhất quán nhân vật, sản phẩm, hộp quà, ánh sáng. Dùng khi người dùng muốn làm video UGC, video POV tặng quà, video phối đồ, hoặc cần prompt cho Veo/Grok/công cụ tạo video AI."
---

# Luvetta Ad Video

Skill này lo phần **kịch bản và prompt** (viết bằng Claude/ChatGPT); phần **dựng clip** do công cụ video AI người dùng chọn (Gemini Veo, Grok...). Đọc `references/luvetta-brand.md` trước.

## Quy trình
1. Hỏi: hướng video (Wear their initial / A gift that feels personal / Everyday styling / Choose your letter / Buy 2 Get 1 — chỉ khi ưu đãi chạy thật), thời lượng (15–30s), lộ mặt hay không, công cụ tạo video.
2. Viết **khối nhất quán** (CONSISTENCY BLOCK): nhân vật, trang phục, sản phẩm (hai mặt rời), đạo cụ, ánh sáng. Dán khối này vào ĐẦU mọi prompt cảnh — lý do: công cụ video tạo từng cảnh độc lập, thiếu khối này nhân vật và sản phẩm sẽ đổi giữa các cảnh.
3. Chia kịch bản 3–6 cảnh, mỗi cảnh 3–5 giây: hành động, góc máy, chuyển động camera, chữ trên màn hình.
4. Kiểm tra từng cảnh tạo ra: sản phẩm sai thiết kế → loại.

## Định dạng đầu ra
```
HƯỚNG VIDEO | THỜI LƯỢNG | HOOK (≤8 từ, chữ trên màn hình 2 giây đầu)
CONSISTENCY BLOCK: ...
| Cảnh | Giây | Hành động & góc máy | Prompt video (tiếng Anh) | Chữ trên màn hình |
CTA cuối: "Pick Your Initial & Make It Yours Today!"
```

## Quy tắc
- Sản phẩm: dây mảnh, tim trơn rời bên trái + chữ rời bên phải, ở MỌI cảnh.
- Không lộ mặt khi người dùng yêu cầu: khung từ giữa cổ trở xuống.
- Không dùng logo xe/thương hiệu khác khi chạy quảng cáo thật (chuỗi cảnh xe Mercedes ban đêm chỉ là bối cảnh sáng tạo nội bộ).
- Hộp quà trong video là đạo cụ, không ngầm hứa sản phẩm có hộp.
