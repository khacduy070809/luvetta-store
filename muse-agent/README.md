# Muse agent — cấu hình vận hành Luvetta

Thư mục này do **Muse** đóng gói (skills/, prompts/, scripts/, workflows/, evidence/).
Bản thân Muse (model + runtime của Meta) không nằm trong repo; ở đây chỉ có cấu hình, quy trình và code nhóm xây trên nền Muse.

Prompt pack tham chiếu: [`../prompts/muse-prompt-pack-v1.txt`](../prompts/muse-prompt-pack-v1.txt)

## Nội dung đã đóng gói

| Mục | Nội dung |
|---|---|
| [`skills/luvetta-shop-operations/SKILL.md`](skills/luvetta-shop-operations/SKILL.md) | Skill vận hành shop: nguyên tắc cứng, quy trình đăng bài / email / báo cáo |
| [`prompts/PROMPT_PACK.md`](prompts/PROMPT_PACK.md) | Prompt Engineering Pack v1.0 (8 module) — bản đặc tả vận hành đầy đủ |
| [`prompts/EMAIL_TEMPLATE_THANKYOU.md`](prompts/EMAIL_TEMPLATE_THANKYOU.md) | Mẫu email cảm ơn sau đặt hàng (qua cổng DUYỆT) |
| [`workflows/WORKFLOWS.md`](workflows/WORKFLOWS.md) | Lịch đăng 4 khung/ngày, cổng dedupe, đăng đồng bộ Business Suite, quy trình email + báo cáo tuần |
| [`scripts/dedupe_check.py`](scripts/dedupe_check.py) | Kiểm tra trùng video với danh sách đã đăng |
| [`scripts/fingerprint_compare.py`](scripts/fingerprint_compare.py) | Fingerprint video (thời lượng + aHash frame 30%/70%) và so khớp Hamming |
| [`scripts/stage_pool.py`](scripts/stage_pool.py) | Chuẩn bị kho video chờ đăng |
| [`evidence/VIDEO_INVENTORY.md`](evidence/VIDEO_INVENTORY.md) | Bản đồ dedupe + nhật ký các video đã đăng (link FB/IG công khai; ID thư mục Drive đã che) |

Dữ liệu không đưa vào repo: email/tên khách hàng, hàng đợi vận hành (queue), token và thông tin thanh toán.
