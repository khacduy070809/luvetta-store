---
name: luvetta-shop-operations
description: Vận hành hằng ngày cho Luvetta Shop (luvetta.store) — đăng video Facebook Page + Instagram, email sau đặt hàng qua cổng duyệt, phân loại hộp thư Gmail, báo cáo tuần. Dùng khi cần đăng bài, soạn email khách, kiểm tra kho video hoặc tổng hợp số liệu shop.
---

# Luvetta Shop — Operations

Shopify store bán MỘT sản phẩm cho khách Mỹ: **Dainty Heart Initial Necklace** — mặt tim trơn + một mặt chữ cái viết hoa RIÊNG (A–Z) đặt cạnh nhau trên cùng một dây mảnh. "Gold"/"Silver" là tên màu, không phải tuyên bố chất liệu. Không bao giờ viết "initial engraved on a heart".

## Nguyên tắc cứng

- Không bịa thông tin về chất liệu, chống nước, vận chuyển, đổi trả, giảm giá hay đánh giá. Trường dữ liệu chưa được chủ shop cung cấp = không nhắc tới.
- Caption và email khách viết bằng tiếng Anh Mỹ; trao đổi với chủ shop bằng tiếng Việt.
- Video do team sản xuất; agent chỉ đọc, viết caption và đăng — không tự tạo/sửa video.
- Không bao giờ đăng lại video đã có trên Instagram @luvet.ta (kiểm tra dedupe trước mỗi lần đăng).
- Email gửi ra ngoài luôn cần chủ shop duyệt đích danh (lệnh DUYỆT / SỬA / TỪ CHỐI kèm mã item + phiên bản).

## Quy trình chính

1. **Đăng video** — xem `../../workflows/WORKFLOWS.md` (4 khung giờ/ngày, dedupe là cổng duy nhất cho video, đăng đồng bộ qua Meta Business Suite).
2. **Email sau đặt hàng** — dùng mẫu trong `../../prompts/EMAIL_TEMPLATE_THANKYOU.md`; quy trình duyệt gọn: báo cáo ngắn (khách + đơn) → bản nháp đã điền tên → chủ shop DUYỆT mới gửi.
3. **Phân loại hộp thư** — email chào mời "store owner" không rõ nguồn = SPAM_OR_SUSPICIOUS; để nguyên trong inbox theo quyết định của chủ shop, không trả lời.
4. **Báo cáo tuần** — thứ Hai 09:00 ICT: đơn hàng/doanh thu (Shopify), lưu lượng (ShopifyQL), trạng thái đăng bài/kho video, các việc còn mở. Luôn kéo số liệu mới, không dùng lại số cũ.

## Tài liệu tham chiếu

- Prompt pack đầy đủ (8 module): `../../prompts/PROMPT_PACK.md`
- Script dedupe + fingerprint video: `../../scripts/`
- Nhật ký đăng bài & bản đồ dedupe: `../../evidence/VIDEO_INVENTORY.md`
