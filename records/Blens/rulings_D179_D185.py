# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D179〜D185 の記録を書く（設計の巡・第二巡〔凍結前の最終検分〕の後・2026-09-23）。
登録者の言葉は会話の記録から機械で切り出す。推奨の中身は採否表 §3 の文を機械で写す（手で打たない）。既にあるファイルには書かない。
用法: python records/Blens/rulings_D179_D185.py <会話の記録 jsonl>"""
import os, re, sys, json, datetime, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
AT_REL = 'records/reviews/Blens/design-round2/adoption-table-Blens-design-r2.md'
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
        if '裁定は全てご推奨のとおり' in t and '9dad676' in t and len(t) < 500:
            words, rec_uuid, rec_ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '裁定の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(rec_ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')

# 採否表 §3 の八項目（逐語）
sec3 = at[at.index('## 3. 裁定の候補'):at.index('## 4. 第一巡の所見のうち')]
cands = [l for l in sec3.split(NL) if l.startswith('- **（')]
nums = ['一', '二', '三', '四', '五', '六', '七']
assert len(cands) == 7 and all(c.startswith('- **（%s）' % n) for c, n in zip(cands, nums)), [c[:12] for c in cands]

# 採否表 §2 の行と案の内訳（機械で数える）
rows = [l for l in at.split(NL) if re.match(r'\| P\d+ \|', l)]
assert all(l.count('|') == 7 for l in rows), '表の列の数が合わない行がある'
pnos = [int(re.match(r'\| P(\d+) \|', l).group(1)) for l in rows]
assert pnos == list(range(528, 565)), pnos
verdict = [l.split('|')[4].strip() for l in rows]
when = [l.split('|')[5].strip() for l in rows]
def kind(v):
    if '裁定の候補' in v:
        return '候補'
    if v.startswith('**不採**') or v.startswith('不採'):
        return '不採'
    if v.startswith('採') or v.startswith('**採**'):
        return '採'
    if v.startswith('記帳'):
        return '記帳'
    raise AssertionError('分けられない案: ' + v[:40])
kinds = [kind(v) for v in verdict]
n_adopt, n_rej, n_cand, n_rec = kinds.count('採'), kinds.count('不採'), kinds.count('候補'), kinds.count('記帳')
assert n_adopt + n_rej + n_cand + n_rec == len(rows)
n_before = sum(1 for w in when if w.startswith('前'))
rej_rows = ['P%d' % p for p, k in zip(pnos, kinds) if k == '不採']


R = ['# 登録者裁定 D179〜D185（2026-09-23・B-lens の設計の巡・第二巡〔凍結前の最終検分〕の後）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (rec_uuid, jst, words.replace(NL, ' ')),
     '- 「ご推奨」の中身は、直前のコーディネータ（南無弥勒如来・Claude Opus 5.5）の返信の「裁定の候補と推奨」の七項目。その元は採否表 `%s`（SHA16 %s）で、下の D179〜D185 の文は採否表 §3 の推奨の文を器で写したもの。' % (AT_REL, at16),
     '- 前提: 登録者裁定 D178（第二巡は凍結前の最終検分・この巡の後は裁定・草案3・器と合成データ・凍結へ進み、設計の巡をもう一度は置かない）。', '',
     '## 裁定', '']
for n, (num, c) in enumerate(zip(nums, cands)):
    R.append('- **D%d**（候補（%s））: %s' % (179 + n, num, c[2:]))
assert R[-1].endswith('案のとおりとするか。')
R[-1] += ' → 登録者の言葉（「裁定は全てご推奨のとおり」）により、案のとおりとした。'
R += ['', '- D185 の内訳（採否表 §2 を器で数えた）: 採 %d・記帳 %d・裁定の候補 %d（D179〜D184 で裁定）・不採 %d。「凍結の前か」の欄が「前」の行 %d。' % (n_adopt, n_rec, n_cand, n_rej, n_before),
      '- D180 は裁定 D170（大きさの目盛り）の中身を改める。D183 は封印の前に要る。',
      '', '## この裁定の後の段取り', '',
      '- 草案3 で、採否表の「凍結の前」の行を直す。草案3 は外の目を通さずに（裁定 D178）、起草者の通読と採否表との機械の突き合わせを置いて、器と合成データ・凍結へ進む。',
      '- 記帳の置き場: B-lens の正本 `design/contrasts-Blens.json` の `decisions`（器 `tools/make_contrasts_Blens.py`・草案3 で足す）。',
      '- 起草者のモデル: Claude Opus 5.5。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
out = os.path.join(HERE, 'rulings-D179-D185.md')
assert not os.path.exists(out), '既にある: ' + out
open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', out, '|', jst, rec_uuid, '| 採', n_adopt, '記帳', n_rec, '候補', n_cand, '不採', n_rej, '前', n_before)
