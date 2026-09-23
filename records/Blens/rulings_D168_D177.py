# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D168〜D177 の記録を書く（設計の巡・第一巡の後・2026-09-23）。
登録者の言葉は会話の記録から機械で切り出す。推奨の中身は採否表 §3 の文を機械で写す（手で打たない）。既にあるファイルには書かない。
用法: python records/Blens/rulings_D168_D177.py <会話の記録 jsonl>"""
import os, re, sys, json, datetime, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
AT_REL = 'records/reviews/Blens/design-round1/adoption-table-Blens-design-r1.md'
at = open(os.path.join(REPO, *AT_REL.split('/')), encoding='utf-8').read()
at16 = hashlib.sha256(at.encode('utf-8')).hexdigest().upper()[:16]

# 登録者の言葉（この裁定）
words = rec_uuid = rec_ts = None
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
        if '裁定は全てご推奨のとおり' in t and 'a962afe' in t and 'b986bd8' in t and len(t) < 500:
            words, rec_uuid, rec_ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '裁定の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(rec_ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')

# 採否表 §3 の八項目（逐語）
sec3 = at[at.index('## 3. 裁定の候補'):at.index('## 4. 次の巡について')]
cands = [l for l in sec3.split(NL) if l.startswith('- **（')]
nums = ['一', '二', '三', '四', '五', '六', '七', '八']
assert len(cands) == 8 and all(c.startswith('- **（%s）' % n) for c, n in zip(cands, nums)), [c[:12] for c in cands]

# 採否表 §2 の行と案の内訳（機械で数える）
rows = [l for l in at.split(NL) if re.match(r'\| P\d+ \|', l)]
assert all(l.count('|') == 6 for l in rows), '表の列の数が合わない行がある'
pnos = [int(re.match(r'\| P(\d+) \|', l).group(1)) for l in rows]
assert pnos == list(range(495, 528)), pnos
verdict = [l.split('|')[4].strip() for l in rows]
def kind(v):
    if '裁定の候補' in v:
        return '候補'
    if v.startswith('**不採**') or v.startswith('不採'):
        return '不採'
    if v.startswith('採') or v.startswith('**採**'):
        return '採'
    raise AssertionError('分けられない案: ' + v[:40])
kinds = [kind(v) for v in verdict]
n_adopt, n_rej, n_cand = kinds.count('採'), kinds.count('不採'), kinds.count('候補')
assert n_adopt + n_rej + n_cand == len(rows)
rej_rows = ['P%d' % p for p, k in zip(pnos, kinds) if k == '不採']
assert '直さない' not in at, '採否表に「直さない」が残っている（P527 は採に改めたはず）'

sec4 = at[at.index('## 4. 次の巡について'):at.index('## 5. COI')]
sec4_lines = [l for l in sec4.split(NL) if l.startswith('- ')]
assert len(sec4_lines) == 2 and 'D166' in sec4_lines[0] and '突き合わせ' in sec4_lines[1]

R = ['# 登録者裁定 D168〜D177（2026-09-23・B-lens の設計の巡・第一巡の後）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (rec_uuid, jst, words.replace(NL, ' ')),
     '- 「ご推奨」の中身は、直前のコーディネータ（南無弥勒如来・Claude Opus 5.5）の返信の「裁定の候補と推奨」の八項目と「ご判断をお願いしたいこと」の三項目。その元は採否表 `%s`（SHA16 %s）で、下の D168〜D175 の文は採否表 §3 の推奨の文を器で写したもの。' % (AT_REL, at16),
     '- 前提: 登録者裁定 D166（設計の巡はこの一巡で終わり、裁定・草案2・器・凍結へ進む）。', '',
     '## 裁定', '']
for n, (num, c) in enumerate(zip(nums, cands)):
    R.append('- **D%d**（候補（%s））: %s' % (168 + n, num, c[2:]))
R += ['- **D176**（採否の案の全体）: 採否表 §2 の P495〜P527 の案を、案のとおりとする（採 %d・不採 %d〔%s・理由は採否表〕・裁定の候補 %d〔D168〜D175 で裁定〕）。README の段階 B の状態の行の直し（P527）は、この裁定の言葉の push の許可により、コミット b986bd8 として push した。' % (n_adopt, n_rej, '・'.join(rej_rows), n_cand),
      '- **D177**（全体の台帳）: 全体の台帳 `records/FREEZE-RECORD.md` に、段階 B の予想封印・凍結・結果報告の公開の三行を、後からの記帳として足し、段階 B の台帳 `records/B/FREEZE-RECORD-B.md` を指す。段階 B の事象はこれまで段階 B の台帳にだけ置いてきた（段階 A までは全体の台帳に行がある）。器は `records/B/ledger_rows_B_late.py`。', '',
      '## この裁定の後の段取り（採否表 §4 の逐語）', '']
R += sec4_lines
R += ['', '- 記帳の置き場: B-lens の正本 `design/contrasts-Blens.json` の `decisions`（器 `tools/make_contrasts_Blens.py`・草案2 で足す）。',
      '- 起草者のモデル: Claude Opus 5.5。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
out = os.path.join(HERE, 'rulings-D168-D177.md')
assert not os.path.exists(out), '既にある: ' + out
open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', out, '|', jst, rec_uuid, '| 採', n_adopt, '不採', n_rej, rej_rows, '候補', n_cand)
