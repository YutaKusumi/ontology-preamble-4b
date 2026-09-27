# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D247〜D250 の記録を書く（最終の系統外の検分の二票の採否の案の裁定）。
登録者の言葉は会話の記録から、裁定の候補の文は公開した採否の案（コミット 1135b35 の `records/reviews/Bl3/results-final/adoption-final-Bl3.md` の §4）から、機械で切り出す（手で打たない）。
採られた案: すべて推奨の案。既にある記録には書かない。
用法: python records/Bl3/rulings_D247_D250.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D247-D250.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True)
ADOPT, C_AD = 'records/reviews/Bl3/results-final/adoption-final-Bl3.md', '1135b35'
U = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        U.append((o.get('uuid'), o.get('timestamp'), c))
hits = [m for m in U if 'D247〜D250 については、ご推奨の案の通りで進めてください' in m[2]]
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, ts, words = hits[0]
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>', 'AppData', 'Users', 'Temp'):
    assert bad not in words, '登録者の言葉に印か道筋が入っている'
raw = git('show', '%s:%s' % (C_AD, ADOPT)).stdout
assert raw, '採否の案がコミットに無い'
ad = raw.decode('utf-8')
s16 = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
L = ad.split(NL)
i0 = [i for i, l in enumerate(L) if l.startswith('- **D247（')]
i1 = [i for i, l in enumerate(L) if l.startswith('- 利益相反の記録:')]
assert len(i0) == 1 and len(i1) == 1 and i0[0] < i1[0], (i0, i1)
cand = L[i0[0]:i1[0] + 1]
assert [l[:9] for l in cand if l.startswith('- **D')] == ['- **D247（', '- **D248（', '- **D249（', '- **D250（'], cand
new1 = [l for l in L if l.startswith('- D248 の甲（')]
assert len(new1) == 1
ps = re.findall(r'^\| (P\d+) \|', ad, re.M)
rl = git('reflog', 'show', 'refs/remotes/origin/main', '--date=iso').stdout.decode('utf-8')
m_push = re.search(r'^1135b35 refs/remotes/origin/main@\{(\S+ \S+) \+0900\}: update by push', rl, re.M)
assert m_push and m_push.group(1) > jst(ts), 'push の時刻が登録者の言葉の後に無い'
R = ['# 登録者裁定 D247〜D250（%s・B-lens 層三・最終の系統外の検分の二票の採否の案）' % jst(ts)[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), words.strip().replace(NL, ' ')),
     '- 採られた案: すべて推奨の案（D247 は甲／D248 は甲／D249 は甲／D250 は甲）。候補の文は、公開した採否の案（コミット %s の `%s`・SHA16 %s）の §4 にあり、下に逐語で置く。' % (C_AD, ADOPT, s16), '',
     '## 裁定の候補（逐語・採否の案の §4）', ''] + cand + ['',
     '## 裁定', '',
     '- **D247**: 最終の系統外の検分の二票（F1・F2）を、ともに最終検分とし、所見は和集合で受ける。正本 `review_plan.final.external` と枠は一票としたので、逸脱 D-BLT2 として台帳に記す（B-lens の D-BL5 の型）。',
     '- **D248**: 起草者の欄の一行目を、採否の案の案の文（D248 の甲）のとおり直す（計算の道の指す先を分かる形にし、但し書きを、動いた分の二つの分を札が分けていない形にする）。F1 の案の文の「分離できない」は採らない。',
     '- **D249**: 逸脱の器を v2 にし、`--final` で最終版を組む。検分を受けた草案の二つ目のファイルは書き換えず、最終版との違いが決めた行だけであることを器が確かめる（裁定 D243 の見出しと状態の行の直しの範囲）。',
     '- **D250**: 採否の案のほかの行（B と C）を案のとおりとする。', '',
     '## 注（事実のみ）', '',
     '- 同じ言葉で、登録者は 1135b35（最終の検分の票の逐語・確かめ・採否の案）の push を許した。push は %s（手元の remote の追跡の参照の reflog）。' % m_push.group(1),
     '- 起草者の欄の一行目の新しい文は、採否の案の「%s」の行にある。' % new1[0][:14],
     '- 採否の案の番号は %s〜%s。' % (ps[0], ps[-1]),
     '- D247〜D250 は下見の前の凍結の後の裁定なので、凍結した正本の `decisions` には入らない。',
     '- 番号: 次の裁定は D251 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| words', jst(ts), uuid, '| adoption', C_AD, s16, '| candidates', len(cand), 'lines | push', m_push.group(1))
