# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D194 の記録を書く（最終の系統外の一票を最終検分とし、依頼文に明記する・2026-09-24）。
登録者の言葉は会話の記録から機械で切り出す（手で打たない）。既にあるファイルには書かない。
用法: python records/Blens/rulings_D194.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D194.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
hit = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'user':
        continue
    c = (o.get('message') or {}).get('content')
    texts = [c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']
    for t in texts:
        if len(t) < 800 and '最終検分' in t and 'a59924f' in t:
            hit.append((t.strip(), o.get('uuid'), o.get('timestamp')))
assert len(hit) == 1, len(hit)
words, uuid, ts = hit[0]
R = ['# 登録者裁定 D194（2026-09-24・最終の系統外の一票を最終検分とする）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), words.replace(NL, ' ')), '',
     '| 裁定 | 中身 |', '|---|---|',
     '| D194 | 結果の巡の二巡目にあたる、新しい Gemini 3.8 Flash の会話の一票（裁定 D189 の最終の系統外の一票）を**最終検分**とし、依頼文に「最終検分」と明記する。'
     'この票の所見は裁定で受けて報告を直し、そのまま公開へ進む。この後に検分の巡を置かない（検分のループを避ける・結果の巡・第一巡で差し戻しは零）。 |', '',
     '## 注（事実のみ）', '',
     '- 正本 `review_plan` の順（結果の巡 → 最終の系統外の一票〔「最終」と明記〕→ 公開）と、「この順のほかに巡を置かない」（`no_more`）に沿う。',
     '- 依頼文と束は `records/reviews/Blens/results-final/make_bundle_Blens_results_final.py` で組み直した。枠 `frame-Blens-results-final.md` には、票の前に追記した。',
     '- 番号: この票の採否の裁定は D195 から（再現は K398 から・採否は P604 から）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', OUT, '|', jst(ts), uuid)
