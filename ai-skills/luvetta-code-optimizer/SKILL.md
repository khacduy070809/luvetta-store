---
name: luvetta-code-optimizer
description: "Rút gọn và tối ưu code Shopify Custom Liquid của Luvetta (đưa xuống dưới 10.000 ký tự, giữ nguyên chức năng), tối ưu tải ảnh/video, loại API trình duyệt kém tương thích. Dùng khi người dùng nói code quá dài, không dán vừa Custom Liquid, trang tải chậm, hoặc muốn 'rút gọn code này'."
---

# Luvetta Code Optimizer

Nguyên tắc số một: **rút gọn mà không mất chức năng**. Người dùng thường chỉ phát hiện thiếu chức năng sau khi đã dán lên web.

## Quy trình
1. Lưu code gốc ra file, chạy `python scripts/check_liquid.py <file> --limit 10000` để biết điểm xuất phát.
2. Liệt kê chức năng hiện có (tìm kiếm, lọc, sắp xếp, phân trang, lightbox, form...) và xác nhận với người dùng danh sách bắt buộc giữ.
3. Rút gọn theo thứ tự ít rủi ro → nhiều rủi ro: xóa comment/khoảng trắng thừa → gộp CSS trùng, rút tên class → dùng vòng lặp `{% for %}` thay HTML lặp → gom hàm JS trùng.
4. Không dùng `DecompressionStream` hay API mới chưa hỗ trợ rộng để "nén" code.
5. Chạy lại check_liquid đến khi ĐẠT; đối chiếu từng chức năng trong danh sách.
6. Ảnh: `loading="lazy"`, có width/height. Video: `muted playsinline`, `preload="metadata"`.

## Định dạng đầu ra
- Bảng: Trước (ký tự) | Sau (ký tự) | Giới hạn.
- Danh sách chức năng: Giữ ✓ / Bỏ (kèm lý do — chỉ bỏ khi người dùng đồng ý).
- Code thay thế hoàn chỉnh trong khối ```liquid.
- Ghi chú trung thực: "Đã kiểm tra tĩnh bằng script; cần thử trên Chrome, Safari và điện thoại trước khi coi là hoàn tất."
