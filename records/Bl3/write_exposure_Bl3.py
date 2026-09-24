# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の封印の前の露出の記録を書く（B-lens の裁定 D190 の型・時刻つき・一つの記録）。
設計の巡・第一巡の票のうち、層三の結果の見込みに当たる文（封印する予想の項目に触れうるもの）を、逐語保全した票のファイルから機械で切り出す（手で打たない）。
票が届いた時刻は、会話の記録（票を含む登録者の発言）から取る。既にある記録には書かない。
用法: python records/Bl3/write_exposure_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'exposure-before-seal-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
R1 = os.path.join(REPO, 'records', 'reviews', 'Bl3', 'design-round1')
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
got = None
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
        if 'Geminiさん（一人目）' in t and 'Claudeさん（二人目）' in t and 'B-lens 層三の枠（草案1）' in t:
            got = (o.get('uuid'), o.get('timestamp'))
assert got, '票を含む登録者の発言が見つからない'
# 見込みに当たる文の在り処（票のファイルの中の一意の字句で所を決め、その行を器が切り出す）
SPOTS = [('gemini-1', '引き倒されて', '所見 1-1', '下見で続けられるか（q1）と、読み取りの形（下見の (i)(ii)）'),
         ('gemini-1', '確率が極めて高く設定', '所見 5-2', '門を通るか（q4・q5）'),
         ('gemini-1', '半ば確定', '所見 5-2', '門を通るか（q4・q5）'),
         ('gemini-2', '可能性は現実的', '伺い 2 の答え', '下見で続けられるか（q1）と、床と天井（下見の (ii)）')]
rows = []
for d, key, where, items in SPOTS:
    p = os.path.join(R1, d, 'review.md')
    L = open(p, encoding='utf-8').read().split(NL)
    hit = [i for i, l in enumerate(L) if key in l]
    assert len(hit) == 1, (d, key, len(hit))
    rows.append((d, hit[0] + 1, where, items, L[hit[0]].strip(), s16(p)))
cell = lambda s: str(s).replace('|', '｜')
R = ['# B-lens 層三の封印の前の露出の記録（B-lens の裁定 D190 の型・時刻つき）', '',
     '- 何の記録か: 層三の予想（正本の `predictions.items`）を封印する前に、登録者とコーディネータの目に触れた、層三の結果の見込みに当たる文の記録。封印の前に登録者とコーディネータが見たものは、ここに時刻つきで足していく。',
     '- 見込みの文の出所: 設計の巡・第一巡の票。依頼文は「結果の見込みを書かないでください」と頼んでいた（`records/reviews/Bl3/design-round1/review-request-Bl3-design.md`）。',
     '- 票が届いた時刻: %s 日本時間（登録者が四票を会話に貼った発言・会話の記録 uuid `%s`）。登録者は票を受け取って貼る時に、コーディネータは票を整理する時に、下の文を読んだ。' % (jst(got[1]), got[0]),
     '- 全経路の効き目の値: 四票とも、計算していないと書いている（各票の「確認していないこと」）。下の文は値の計算ではなく、見込みの文である。票の中の仮の数の例（「もし〜なら」の形）は、見込みに数えていない。', '',
     '## 露出の一覧（票の文は、逐語保全した票のファイルから器が切り出した行）', '',
     '| 番号 | 票（ファイルの SHA16） | 行 | 所見 | 触れうる予想の項目 | 切り出した行 |', '|---|---|---|---|---|---|'] + [
     '| X%d | `%s/review.md`（%s） | %d | %s | %s | %s |' % (i + 1, d, sh, n, where, items, cell(txt)) for i, (d, n, where, items, txt, sh) in enumerate(rows)] + [
     '', '## 扱い（登録者の裁定を待つ）', '',
     '- この露出をどう扱うか（予想の自由記述の欄に「封印の前に設計の巡の票の見込みの文を読んだ」と書く・項目ごとに印を付ける、など）は、登録者が決める。',
     '- コーディネータは、封印が済むまで、これらの文への賛否や、自分の見込みを返信に書かない。',
     '- Claude 系の二票には、層三の結果の見込みに当たる文は見当たらなかった（コーディネータの通読・機械の検査ではない）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| rows', len(rows), '| votes at', jst(got[1]))
