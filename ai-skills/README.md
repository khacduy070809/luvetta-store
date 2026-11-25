# Luvetta AI Skills (bản cho AI agent tự chạy)

13 skill theo chuẩn Agent Skills (mỗi thư mục có SKILL.md + YAML frontmatter `name`/`description`).
Mỗi skill tự đủ: có sẵn `references/luvetta-brand.md`, không phụ thuộc file ngoài.

| # | Skill | Script/tài nguyên chạy được |
|---|---|---|
| 1 | luvetta-brand-identity | — |
| 2 | luvetta-copywriter | — |
| 3 | luvetta-product-image | — |
| 4 | luvetta-ad-video | — |
| 5 | luvetta-section-builder | scripts/check_liquid.py, references/luvetta-sections-spec.txt |
| 6 | luvetta-liquid-debug | scripts/check_liquid.py, references/known-issues.md |
| 7 | luvetta-code-optimizer | scripts/check_liquid.py |
| 8 | luvetta-test-data | scripts/make_sample_reviews.py |
| 9 | luvetta-bundle-builder | scripts/check_liquid.py |
| 10 | luvetta-gift-agent | assets/worker.js, assets/luvetta-agent.liquid, references/system-prompt-v1.md, references/test-log.md |
| 11 | luvetta-social-content | — |
| 12 | luvetta-competitor-research | — |
| 13 | luvetta-ads-strategy (đề xuất, chưa chạy ads thật) | — |

## Cách nạp
- Claude (claude.ai / app): Settings → Capabilities → Skills → Upload, chọn từng file `.skill`/.zip trong thư mục `dist`.
- Claude Code: chép các thư mục vào `~/.claude/skills/` (hoặc `.claude/skills/` trong project).
- Agent khác: đọc SKILL.md làm hướng dẫn; script cần Python 3, không cần thư viện ngoài.

## Lệnh test nhanh
python luvetta-test-data/scripts/make_sample_reviews.py --count 5 --format json
python luvetta-section-builder/scripts/check_liquid.py luvetta-gift-agent/assets/luvetta-agent.liquid
