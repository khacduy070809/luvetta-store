import re, html, json
SRC='/home/claude/theme/extracted/'
KEEP=['display','flex-direction','flex-wrap','justify-content','align-items','gap','grid-template-columns','width','max-width','min-width','height','min-height','max-height','aspect-ratio','padding','margin','font-family','font-size','font-weight','font-style','line-height','letter-spacing','text-transform','text-align','color','background','background-color','border','border-top','border-bottom','border-radius','box-shadow','object-fit','position','opacity','animation','overflow','white-space','scroll-snap-type','text-decoration']
def clean_sel(s):
    s=re.sub(r'#LVID\s*','',s); s=s.replace('LVID','')
    s=' '.join(s.split()); return s.strip() or ':root'
def parse_css(css):
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
    css=re.sub(r'\{\{.*?\}\}','LVID',css,flags=re.S); css=re.sub(r'\{%.*?%\}','',css,flags=re.S)
    out=[]; i=0
    # handle @media blocks and keyframes
    pos=0
    tokens=[]
    def rules(block, media=None):
        for m in re.finditer(r'([^{}]+)\{([^{}]*)\}',block):
            sel=clean_sel(m.group(1)); body=m.group(2)
            props=[]
            for d in body.split(';'):
                if ':' not in d: continue
                k,v=d.split(':',1); k=k.strip().lower(); v=' '.join(v.split())
                if k in KEEP and '{{' not in v: props.append(f'{k}: {v}')
            if props: tokens.append((media,sel,props))
    # extract media blocks
    rest=css
    for mm in re.finditer(r'@media([^{]+)\{((?:[^{}]*\{[^{}]*\})*)\s*\}',css):
        rules(mm.group(2), ' '.join(mm.group(1).split()))
    rest=re.sub(r'@media([^{]+)\{((?:[^{}]*\{[^{}]*\})*)\s*\}','',css)
    kf=re.findall(r'@keyframes\s+([\w-]+)',rest)
    rest=re.sub(r'@keyframes[^{]+\{((?:[^{}]*\{[^{}]*\})*)\s*\}','',rest)
    rules(rest)
    return tokens,kf
def visible_text(code):
    c=re.sub(r'{%-?\s*comment\s*-?%}.*?{%-?\s*endcomment\s*-?%}','',code,flags=re.S)
    c=re.sub(r'<(style|script)[^>]*>.*?</\1>','',c,flags=re.S|re.I)
    c=re.sub(r'<!--.*?-->','',c,flags=re.S)
    c=re.sub(r'<svg.*?</svg>','',c,flags=re.S|re.I)
    c=re.sub(r'{%.*?%}','',c,flags=re.S); c=re.sub(r'{{.*?}}','',c,flags=re.S)
    c=re.sub(r'<(br)\s*/?>','\n',c)
    c=re.sub(r'</?(p|h[1-6]|li|div|section|span|button|a|label|option|summary|strong|em|b)\b[^>]*>',lambda m:'\n' if m.group(0)[1]!='/' and m.group(1) in('p','h1','h2','h3','h4','li','div','section','button','label','option','summary') else ' ',c)
    c=re.sub(r'<[^>]+>',' ',c)
    lines=[html.unescape(' '.join(l.split())) for l in c.split('\n')]
    out=[];
    for l in lines:
        if l and (not out or out[-1]!=l): out.append(l)
    return out
def assets(code):
    urls=re.findall(r'https://cdn\.shopify\.com/[^\s"\')]+',code)
    alts=re.findall(r'alt="([^"{}]+)"',code)
    return list(dict.fromkeys(urls)), list(dict.fromkeys(alts))
def spec(fn):
    code=open(SRC+fn).read()
    css=' '.join(re.findall(r'<style[^>]*>(.*?)</style>',code,flags=re.S))
    toks,kf=parse_css(css)
    base=[t for t in toks if not t[0]]; med={}
    for m,s,p in toks:
        if m: med.setdefault(m,[]).append((s,p))
    txt=visible_text(code); urls,alts=assets(code)
    return dict(base=base,media=med,kf=kf,text=txt,urls=urls,alts=alts,len=len(code))
if __name__=='__main__':
    for f in ['01','02','03','04','05','06','07','08','10','11','12']:
        s=spec(f+'.liquid')
        b=sum(len('; '.join(p))+len(sel) for _,sel,p in s['base']); m=sum(sum(len('; '.join(p))+len(x) for x,p in v) for v in s['media'].values())
        print(f, 'code',s['len'],'base css chars',b,'media chars',m,'text lines',len(s['text']),'urls',len(s['urls']))
