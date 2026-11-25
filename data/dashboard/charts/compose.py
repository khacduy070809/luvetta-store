from PIL import Image, ImageDraw, ImageFont
BG='#F5E6DC'; CARD='#FFF7F3'; TX='#5F4B43'; MU='#9A8478'; GOLD='#B88E63'; LINE='#E6D2C3'; WARN='#B07A4F'
W,H=3200,3150
c=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(c)
F=lambda s,b=False,serif=False: ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVu{'Serif' if serif else 'Sans'}{'-Bold' if b else ''}.ttf",s)
d.text((120,90),'Luvetta Shop — Dashboard dữ liệu website',font=F(78,True,True),fill=TX)
d.text((120,200),'luvetta.store · Shopify Analytics · 01/10 – 18/11/2026',font=F(36),fill=MU)
d.text((W-120,200),'Little details, big meaning. ♡',font=F(36,False,True),fill=GOLD,anchor='ra')
d.line((120,270,W-120,270),fill=GOLD,width=4)
def card(x,y,w,h,r=36,fill=CARD): d.rounded_rectangle((x,y,x+w,y+h),r,fill=fill,outline=LINE,width=3)
kp=[('Phiên truy cập T11','284','T10: 119 · ▲ 139%'),('Khách truy cập T11','236','T10: 119'),('Lượt xem trang T11','541','T10: 127'),('Tỷ lệ thêm vào giỏ','10,6%','30 phiên có thêm giỏ'),('Tỷ lệ chuyển đổi','1,4%','4 phiên mua'),('Đơn · Doanh thu','4 · $20','1 test · 3 cần xác minh')]
cw=(W-240-5*40)//6
for i,(a,b,s) in enumerate(kp):
    x=120+i*(cw+40); card(x,320,cw,300)
    d.text((x+40,360),a,font=F(30),fill=MU); d.text((x+40,415),b,font=F(84,False,True),fill=TX); d.text((x+40,545),s,font=F(27),fill=GOLD if '▲' in s else MU)
def put(fn,x,y,w,h):
    card(x,y,w,h); im=Image.open(fn).convert('RGB'); pad=36
    r=min((w-2*pad)/im.width,(h-2*pad)/im.height); im=im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
    c.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))
put('1_daily_sessions.png',120,670,1940,820); put('2_month_compare.png',2100,670,980,820)
put('3_funnel.png',120,1530,1000,720); put('6_variants.png',1160,1530,900,720); put('7_donuts.png',2100,1530,980,720)
put('4_bounce.png',120,2290,1300,720); put('5_duration.png',1460,2290,900,720)
x,y,w,h=2400,2290,680,720; card(x,y,w,h,fill='#EFD9CB')
d.text((x+40,y+40),'Dữ liệu còn thiếu',font=F(40,True,True),fill=TX)
yy=y+120
for t in ['• Nguồn truy cập (FB, IG,','   vào thẳng)','• Insights Facebook Page','• Insights Instagram @luvet.ta','• Thiết bị, quốc gia','• Giỏ hàng bỏ dở','• Lượt dùng chatbot AI']:
    d.text((x+40,yy),t,font=F(30),fill=TX); yy+=60
d.text((x+40,y+h-90),'Đơn T11 chưa giao hàng.',font=F(26),fill=WARN)
d.text((120,H-80),'Nguồn: Shopify Analytics export · Email khách đã ẩn · Đơn #1003 là đơn test',font=F(26),fill=MU)
c.save('Luvetta_Dashboard_be_kem.png',optimize=True); c.resize((1600,1575)).save('/tmp/prev.png')
