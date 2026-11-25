#!/usr/bin/env python3
"""Tạo review MẪU để test widget Customer Reviews của Luvetta.

Cách dùng:
  python make_sample_reviews.py --count 38 --format js   > sample.js    # mảng fallbackReviews (chỉ cho Theme Editor)
  python make_sample_reviews.py --count 10 --format json > sample.json  # cấu trúc metafield, approved=false

Dữ liệu là GIẢ, chỉ để kiểm thử giao diện. Không đưa lên website công khai như review thật.
"""
import argparse, json, random, datetime

NAMES = ["Emily R.", "Sophia L.", "Mia T.", "Olivia H.", "Hannah B.", "Ava K.", "Chloe M.", "Grace P.", "Lily S.", "Zoe W.", "Ella D.", "Nora J."]
TITLES = {5: ["Even prettier in person", "Exactly what I wanted", "Perfect birthday gift", "Lovely everyday piece"],
          4: ["Really cute", "Sweet and simple", "Nice gift"],
          3: ["Okay overall", "Smaller than expected"],
          2: ["Not quite for me"], 1: ["Didn't work out"]}
SHORT = ["Simple, dainty and so sweet.", "Cute little heart next to the letter.", "Looks lovely with a plain tee."]
LONG = ["I ordered the heart and initial necklace for myself and I love how delicate it looks. The little letter sits right next to the heart and it goes with almost everything I wear.",
        "Bought this for my sister with her initial and she was so happy. The tiny heart beside the letter is such a thoughtful detail, and it layers nicely with her other chains."]

def make(count, seed, fmt):
    rnd = random.Random(seed); out = []; start = datetime.date(2026, 11, 15)
    weights = [5] * 12 + [4] * 4 + [3] * 2 + [2, 1]
    for i in range(count):
        r = rnd.choice(weights)
        d = start - datetime.timedelta(days=i)
        item = {"name": NAMES[i % len(NAMES)], "rating": r, "title": rnd.choice(TITLES[r]),
                "text": rnd.choice(LONG if i % 3 == 0 else SHORT), "date": d.strftime("%d/%m/%Y"),
                "images": [] , "up": rnd.randint(0, 20), "down": rnd.randint(0, 2)}
        if fmt == "json":
            item = {"approved": False, **item}
        out.append(item)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=38); ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--format", choices=["js", "json"], default="js")
    a = ap.parse_args(); data = make(a.count, a.seed, a.format)
    if a.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("{% if request.design_mode %}{%- comment -%} DỮ LIỆU MẪU — chỉ hiện trong Theme Editor {%- endcomment -%}")
        print("const fallbackReviews = " + json.dumps(data, ensure_ascii=False, indent=2) + ";")
        print("{% else %}\nconst fallbackReviews = [];\n{% endif %}")
