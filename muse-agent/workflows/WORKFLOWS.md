# Workflows — Luvetta auto-post & email

## 1. Đăng video tự động (FB Page "Luvetta" + Instagram @luvet.ta)

- **Lịch:** 4 khung/ngày — 09:00 / 13:00 / 16:00 / 20:00 (Asia/Ho_Chi_Minh).
- **Nguồn video:** thư mục Drive do chủ shop chỉ định, gồm 4 thư mục con theo thành viên team. Agent không di chuyển file trong thư mục dùng chung này.
- **Cổng duy nhất = dedupe** (quyết định của chủ shop, thay cho cổng duyệt từng video):
  1. Fingerprint từng file: thời lượng + aHash 16×16 của frame tại 30% và 70% (xem `../scripts/fingerprint_compare.py`).
  2. So với toàn bộ bài đã đăng trên @luvet.ta. TRÙNG khi: lệch thời lượng ≤ 2s VÀ khoảng cách Hamming tốt nhất ≤ 45.
  3. Trước mỗi lần đăng, kiểm tra lại danh sách IG trực tiếp; file trùng → bỏ qua, lấy file kế tiếp.
- **Kênh đăng:** Meta Business Suite composer, chọn CẢ HAI đích ("Luvetta và luvet.ta") để đăng đồng bộ FB + IG trong một bài. Caption dùng chung = thân caption Facebook (bỏ dòng hashtag cuối) + dòng trống + dòng hashtag của caption Instagram.
- **Quy tắc lấp slot:** nếu video dự kiến của một slot đã bị đăng sớm, đẩy video khác lên lấp slot đúng giờ thay vì để trống.
- **Hết kho video:** lần chạy kế tiếp quét Drive tìm file mới (fingerprint + dedupe + viết caption theo Module 03 của prompt pack + xếp hàng). Không có file mới → dừng lịch đăng và báo chủ shop.
- **Sự cố:** nếu Business Suite bị kẹt xử lý media hoặc đòi đăng nhập/xác minh → ghi nhận PUBLISH_FAILED, báo chủ shop, KHÔNG tự đổi kênh đăng; slot sau tự nhặt lại item.

## 2. Email sau đặt hàng (có cổng duyệt)

- Mẫu đứng: `../prompts/EMAIL_TEMPLATE_THANKYOU.md` — tiêu đề `Your little "[Letter]" is on its way ♡`.
- Quy trình gọn: (1) báo cáo ngắn gồm khách + đơn; (2) gửi bản nháp đã điền tên/mẫu; (3) chỉ gửi khi chủ shop trả lời `DUYỆT <mã item> <phiên bản>`. Lệnh `SỬA` = sửa theo ghi chú rồi trình lại; `TỪ CHỐI` = hủy item.
- Địa chỉ email khách lấy từ Shopify (email thông báo của Shopify không chứa email khách).

## 3. Báo cáo tuần

- Thứ Hai 09:00 ICT: kéo mới đơn hàng + ShopifyQL analytics (sessions/visitors/conversion/funnel), trạng thái kho video và đăng bài, hóa đơn/billing nếu có cảnh báo, các item chờ duyệt.
- Không trình bày số liệu cũ như số của tuần hiện tại.

## 4. Phân loại hộp thư (Gmail của shop)

- Đơn hàng/thanh toán/bảo mật từ Shopify, Meta, Google: đọc và tóm tắt cho chủ shop.
- Email chào mời kiểu "store owner" từ người lạ: phân loại SPAM_OR_SUSPICIOUS, để nguyên trong inbox, không trả lời, không chuyển spam (theo quyết định của chủ shop).
- Cảnh báo bảo mật liên quan tới chính thao tác liên kết tài khoản của chủ shop: không bấm "This wasn't me" (có thể hủy liên kết Page ↔ Instagram và làm hỏng đăng đồng bộ).
