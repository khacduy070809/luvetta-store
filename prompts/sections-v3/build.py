from gen import spec
import re
N={
'01':dict(t='1. Trust bar (dưới header)',role='lập trình viên Shopify chuyên Custom Liquid',task='Viết thanh trust bar nằm ngay dưới header, hiển thị trên mọi trang.',
 lay=['Một hàng căn giữa: cụm trái = 5 sao + điểm + số review; vạch ngăn dọc 1px; cụm phải = câu cộng đồng + link in đậm gạch chân.','Link lấy từ biến Liquid community_url khai báo ở dòng đầu, mở tab mới, rel="noopener noreferrer".','Thanh LUÔN hiển thị, không bọc trong {% if %}.'],tech=[]),
'02':dict(t='2. Story — Image with text (trang chủ)',role='lập trình viên Shopify chuyên Custom Liquid',task='Viết section kể chuyện sản phẩm: chữ bên trái, ảnh dọc 9:16 bên phải.',
 lay=['Nền section #FFF7F3, khung 2 cột căn giữa.','Cột trái: tiêu đề 2 dòng (dòng 2 là <span> màu #B47E70), 8 đoạn văn, đoạn cuối in đậm.','Cột phải: ảnh 9:16 bo góc, có bóng đổ nhẹ, loading="lazy", width 720 height 1280.','ID section ghép: \'heart-story-\' | append: section.id | append: \'-\' | append: block.id; mọi CSS viết dưới #ID đó.'],tech=[]),
'03':dict(t='3. 4-image showcase + lightbox',role='lập trình viên Shopify chuyên Custom Liquid và JavaScript thuần',task='Viết section 4 ảnh phong cách sản phẩm, bấm ảnh để xem toàn màn hình.',
 lay=['4 thẻ ảnh cùng hàng; mỗi thẻ: ảnh phủ kín, lớp phủ gradient tối ở đáy chứa nhãn nhỏ viết hoa + tiêu đề serif trắng, nút ⤢ ở góc.','Lightbox: nền tối phủ toàn màn hình, ảnh lớn ở giữa, nút ✕ góc trên phải, nút ❮ ❯ hai bên, bộ đếm "1 / 4" và chú thích theo tiêu đề thẻ.','ID gallery ghép: \'heart-gallery-\' | append: section.id | append: \'-\' | append: block.id.'],
 tech=['JS trong IIFE, "use strict"; tìm gallery theo ID; gắn data-gallery-initialized="true" để không khởi tạo 2 lần.','Gom mảng ảnh từ các thẻ (src, alt, tiêu đề); mở lightbox tại ảnh được bấm, lưu phần tử đang focus để trả focus khi đóng.','Điều khiển: nút trước/sau (vòng lặp), phím ←/→, phím Escape, vuốt trái/phải (touchstart/touchend, ngưỡng ~50px), bấm nền tối để đóng; khoá cuộn trang khi mở.']),
'04':dict(t='5. Product info (khối lợi ích)',role='lập trình viên Shopify chuyên Custom Liquid',task='Viết khối giới thiệu lợi ích đặt trong cột mua hàng của trang sản phẩm, dưới tiêu đề và giá.',
 lay=['Câu trích dẫn in nghiêng ở đầu.','4 dòng lợi ích dạng lưới 2 cột (icon emoji 24px | chữ), tiêu đề lợi ích in đậm 800, theo sau là dấu – và mô tả.','Dòng CTA cuối: vòng tròn 32px nền #F9E8E3 chứa trái tim SVG 16px màu #C98D85 nhấp nháy (animation 1.4s lặp vô hạn) + chữ in đậm.'],tech=[]),
'05':dict(t='6. Bundle selector (Single / Buy 2 Get 1 Free)',role='lập trình viên Shopify chuyên Custom Liquid, AJAX Cart API và JavaScript thuần',task='Viết bộ chọn gói và chọn chữ/màu, đặt ngay trên nút ADD TO CART gốc của theme.',
 lay=['STEP 1: 2 thẻ gói cạnh nhau. Thẻ SINGLE NECKLACE có nhãn STANDARD, giá = giá biến thể mặc định ({{ bn_default.price | money }}). Thẻ BUY 2, GET 1 FREE có nhãn BEST VALUE ★, giá = 2 × giá. Thẻ đang chọn viền #C7947B nền hồng nhạt.','STEP 2: tab NECKLACE 1 / NECKLACE 2 / FREE GIFT 🎁 (chỉ hiện khi chọn gói 3); lưới 26 ô chữ A–Z (7 cột); 2 nút màu Gold/Silver có chấm tròn màu.','Thông báo lỗi chữ đỏ #AF3030 khi chưa chọn đủ; không dùng alert().'],
 tech=['Dựng bảng biến thể từ {{ product.variants | json }}: option1 = chữ, option2 = màu → variant id thật.','Gói 1: cập nhật input name="id" của form sản phẩm gốc theo lựa chọn, giữ nút ADD TO CART và Shop Pay gốc.','Gói 3: chặn submit form gốc, gửi 3 dòng qua fetch(\'/cart/add.js\') với items:[{id,quantity:1}×3], sau đó chuyển tới /cart; ẩn nút Shop Pay (.shopify-payment-button) khi đang chọn gói 3.','Ghi chú trong code: cần tạo discount tự động Buy X Get Y trong Shopify; code giao diện không tự tạo ưu đãi.']),
'06':dict(t='7. Guarantee badge (30 ngày)',role='lập trình viên Shopify và thiết kế icon SVG',task='Viết hộp cam kết hoàn tiền đặt dưới nút mua.',
 lay=['Hộp ngang: huy hiệu SVG 48px bên trái, nội dung bên phải.','Huy hiệu SVG viewBox 0 0 100 100: ngôi sao răng cưa 24 cánh màu #C99578 viền #A8745B; vòng tròn trong r=34 viền #FFF8F1; chữ "30" lớn, "DAY", "GUARANTEE" màu trắng.'],tech=[]),
'07':dict(t='8. See it in action (video)',role='lập trình viên Shopify chuyên Custom Liquid và JavaScript thuần',task='Viết carousel 3 video dọc cho trang sản phẩm.',
 lay=['Tiêu đề "See it in action" màu cam gradient (#EA7317 → #F5A94A), dưới là nhãn bo tròn viền cam có icon trái tim hồng #E1306C và chữ "Always a theme you\'ll love".','Hàng video cuộn ngang (scroll-snap-type: x mandatory), mỗi thẻ khung dọc bo góc, video autoplay muted loop playsinline, nút Play/Pause tròn góc dưới trái.','Dưới hàng video là thanh tiến trình kéo được (draggable progress bar) đồng bộ với vị trí cuộn.'],
 tech=['Nút Play/Pause đổi icon theo trạng thái video.','Kéo thanh tiến trình → cuộn danh sách tương ứng; cuộn danh sách → cập nhật thanh.','Phím ←/→ chuyển video khi danh sách đang focus.']),
'08':dict(t='9. Customer Reviews',role='lập trình viên Shopify chuyên Liquid, metafield và JavaScript thuần',task='Viết widget đánh giá khách hàng cho trang sản phẩm.',
 lay=['Tiêu đề "Customer Reviews" căn giữa; dưới là điểm trung bình lớn + sao + "Based on N reviews" + nút "Write A Review" bo tròn nền #B47E70.','Thanh công cụ một hàng: ô "Search reviews", select All ratings/5→1 stars, ô tích "With media", "Sort by:" (Highest rating, Lowest rating, Most recent, Most helpful).','Mỗi review: avatar tròn chữ cái đầu nền #F8EAE3, tên, sao + tiêu đề in đậm, ngày bên phải (dd/mm/yyyy), nội dung, "Read more" khi dài, ảnh thumbnail bo góc nếu có, "Was this review helpful? 👍 n 👎 n".','Phân trang dạng nút tròn: ‹ 1 2 … 4 ›, trang hiện tại nền #B47E70; 5 review mỗi trang.'],
 tech=['Dữ liệu: product.metafields.custom.customer_reviews (JSON mảng: name, rating, title, body, date, images[], helpful). Không có dữ liệu → "No reviews yet" và "—".','Lọc, tìm, sắp xếp, phân trang làm phía trình duyệt; nút Helpful chỉ tăng bộ đếm trên trình duyệt.','Form "Write a review" (ẩn, mở bằng nút) dùng {% form \'contact\', id: \'LuvettaReviewForm\' %}: chọn sao, Name, Email, Review title, Your review, nút Cancel / Submit Review; sau khi gửi hiện "Thank you! Your message has been sent."']),
'10':dict(t='10. Guarantee + Add to cart',role='lập trình viên Shopify chuyên Custom Liquid',task='Viết khối cam kết 30 ngày cuối trang sản phẩm, có nút thêm vào giỏ.',
 lay=['Section nền #FFF7F3, nội dung căn giữa, rộng tối đa ~680px.','Icon khiên có dấu ✓ viền vàng #C39762 trong vòng tròn.','Tiêu đề serif lớn: "30-Day Money-Back" màu #B47E70 + "Guarantee" màu #56392F.','Đoạn mô tả, nút ADD TO CART ♡ bo tròn full-pill nền #B47E70 chữ trắng, hàng 3 điểm tin cậy có dấu ✓ vàng, câu kết nhỏ, link "View our refund policy" gạch chân.'],
 tech=['Nút gửi form /cart/add với variant đang chọn ({{ product.selected_or_first_available_variant.id }}), quantity 1.']),
'11':dict(t='11. About Us',role='lập trình viên Shopify và copywriter thương hiệu',task='Viết toàn bộ trang About Us (nội dung + code) cho template page.',
 lay=['Nền #FFF7F3, cột nội dung căn giữa rộng tối đa ~600px.','Tiêu đề trang "ABOUT US" serif đậm màu #56392F, dưới là đường kẻ mảnh – ♡ – đường kẻ màu #C39762.','8 phần + Join Us; mỗi phần: tiêu đề serif, các đoạn ngắn, câu kết màu #B47E70 in đậm; giữa các phần là đường kẻ mảnh #EAD7C9.','Phần Our Commitment có phụ đề serif màu #B47E70 "Personal Jewelry, Meaningful Choices".','Không có newsletter, không có footer trong section.'],tech=[]),
'12':dict(t='4. Footer',role='lập trình viên Shopify chuyên Custom Liquid',task='Viết footer thương hiệu thay footer mặc định.',
 lay=['Nền #FFF7F3; 3 cột: cột 1 icon trái tim trong vòng tròn viền #C39762 + khối chữ; cột 2 Quick Links; cột 3 newsletter.','Câu "Made to feel personal. ♡" in nghiêng serif màu #B47E70.','Newsletter: ô email viền #EAD7C9, nút "Sign Me Up ♡" full-width nền #B47E70; dòng chú thích nhỏ.','Hàng dưới: đường kẻ, icon phương thức thanh toán thật của shop (shop.enabled_payment_types | payment_type_svg_tag), dòng "© {{ \'now\' | date: \'%Y\' }}, {{ shop.name }}. Made with ♡".'],
 tech=['Link chính sách lấy từ shop.privacy_policy.url, shop.refund_policy.url, shop.terms_of_service.url, shop.shipping_policy.url; Search → routes.search_url.','Newsletter dùng {% form \'customer\' %} với input hidden contact[tags] = newsletter; form.posted_successfully? → hiện "Thank you for joining! / So happy to have you here. ♡"; lỗi hiện màu đỏ #A0443B.'])}
ORDER=['01','02','03','12','04','05','06','07','08','10','11']
def merge(lines):
    out=[]
    for l in lines:
        if out and l and (l[0].islower() or out[-1].endswith(',')) : out[-1]+=' '+l
        else: out.append(l)
    return [x for x in out if x not in ('—','.','© ,')]
def css_lines(rules):
    seen={}; 
    for sel,p in rules: seen.setdefault(sel,[]); seen[sel]+= [x for x in p if x not in seen[sel]]
    return [f'{s} {{ {"; ".join(p)} }}' for s,p in seen.items()]
def build(f):
    n=N[f]; s=spec(f+'.liquid')
    o=[f'VAI TRÒ: Bạn là {n["role"]}.','BỐI CẢNH: [BỐI CẢNH CHUNG]',f'NHIỆM VỤ: {n["task"]}','','BỐ CỤC & HÀNH VI:']+['- '+x for x in n['lay']]
    o+=['','NỘI DUNG CHỮ (dùng NGUYÊN VĂN, đúng thứ tự xuất hiện):']+['- '+x for x in merge(s['text'])]
    if s['urls']:
        o+=['','ẢNH / VIDEO (dùng đúng URL):']+['- '+u for u in s['urls']]
    o+=['','THÔNG SỐ GIAO DIỆN (dùng ĐÚNG tên class và giá trị dưới đây; được thêm thuộc tính phụ nếu cần):']+css_lines([(a,b) for _,a,b in s['base']])
    if s['kf']: o+=['Animation: @keyframes '+', '.join(s['kf'])]
    if s['media']:
        o+=['','RESPONSIVE:']
        for m,rs in s['media'].items(): o+=[f'@media {m}:']+['  '+x for x in css_lines(rs)]
    o+=['','YÊU CẦU KỸ THUẬT:']+['- '+x for x in n['tech']]+['- Không dùng thư viện ngoài; CSS và JS nằm gọn trong một khối, mọi class có prefix riêng như trên để không đụng CSS của theme.','- Chỉ dùng Liquid chạy được trong khối Custom Liquid (không dùng section.settings, không cần {% schema %}).','- Section phải hiển thị ngay khi dán code.','','TỰ KIỂM TRA trước khi trả lời: đối chiếu từng mục NỘI DUNG CHỮ và THÔNG SỐ GIAO DIỆN ở trên, không bỏ sót, không đổi chữ, không đổi màu.','ĐỊNH DẠNG TRẢ VỀ: một khối code hoàn chỉnh để dán vào Custom Liquid, không giải thích dài.']
    return n['t'],'\n'.join(o)
if __name__=='__main__':
    tot=0
    for f in ORDER:
        t,p=build(f); tot+=len(p); open(f'p{f}.txt','w').write(p); print(t,len(p))
    print('total',tot)
