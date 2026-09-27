# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D251〜D253 の記録を書く（起草者の最終の見直しの一度目と二度目の裁定の候補）。
登録者の言葉は会話の記録から、裁定の候補の文と所見の行は公開した見直しの記録（一度目はコミット 2d6dca6 の `records/reviews/Bl3/results-final/final-read/review-final-Bl3.md` の §3・
二度目はコミット 352cfa9 の `records/reviews/Bl3/results-final/final-read2/review2-final-Bl3.md` の §3 と §5）から、機械で切り出す（手で打たない）。
採られた案: すべて推奨の案（D252 は二度目の見直しの R-h で補った文）。既にある記録には書かない。
用法: python records/Bl3/rulings_D251_D253.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D251-D253.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True)
REV1, C1 = 'records/reviews/Bl3/results-final/final-read/review-final-Bl3.md', '2d6dca6'
REV2, C2 = 'records/reviews/Bl3/results-final/final-read2/review2-final-Bl3.md', '352cfa9'
U = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        U.append((o.get('uuid'), o.get('timestamp'), c))
hits = [m for m in U if 'D251〜D253 はご推奨の案で進めてください' in m[2]]
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, ts, words = hits[0]
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>', 'AppData', 'Users', 'Temp'):
    assert bad not in words, '登録者の言葉に印か道筋が入っている'


def at(commit, path):
    raw = git('show', '%s:%s' % (commit, path)).stdout
    assert raw, 'コミットに無い: %s %s' % (commit, path)
    return raw.decode('utf-8').replace('\r\n', NL).split(NL), hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


R1, s1 = at(C1, REV1)
R2, s2 = at(C2, REV2)
c1 = [l for l in R1 if l.startswith('- **D251（') or l.startswith('- **D252（')]
c2 = [l for l in R2 if l.startswith('- **D251（') or l.startswith('- **D252（') or l.startswith('- **D253（')]
assert [l[:9] for l in c1] == ['- **D251（', '- **D252（'] and [l[:9] for l in c2] == ['- **D251（', '- **D252（', '- **D253（'], (c1, c2)
hd = [i for i, l in enumerate(R2) if l.startswith('| 番号 | 重さ | 置き場（最終版の案の行）')]
assert len(hd) == 1
rows = [l for l in R2 if re.match(r'^\| R-[a-d] \|', l)]
assert [l[:5] for l in rows] == ['| R-a', '| R-b', '| R-c', '| R-d'], rows
rec = [l[:5] for l in R2 if re.match(r'^\| R-[e-i] \|', l)]
rl = git('reflog', 'show', 'refs/remotes/origin/main', '--date=iso').stdout.decode('utf-8')
m_push = re.search(r'^352cfa9 refs/remotes/origin/main@\{(\S+ \S+) \+0900\}: update by push', rl, re.M)
assert m_push and m_push.group(1) > jst(ts), 'push の時刻が登録者の言葉の後に無い'
R = ['# 登録者裁定 D251〜D253（%s・B-lens 層三・起草者の最終の見直しの一度目と二度目）' % jst(ts)[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), words.strip().replace(NL, ' ')),
     '- 採られた案: すべて推奨の案（D251 は甲／D252 は甲・二度目の見直しの R-h で補った文／D253 は甲）。候補の文は、公開した一度目の見直しの記録（コミット %s の `%s`・SHA16 %s）の §3 と、二度目の見直しの記録（コミット %s の `%s`・SHA16 %s）の §5 にあり、下に逐語で置く。' % (C1, REV1, s1, C2, REV2, s2), '',
     '## 裁定の候補（逐語）', '',
     '一度目の見直しの記録の §3:', ''] + c1 + ['', '二度目の見直しの記録の §5（こちらが採られた文・D252 は R-h で補った）:', ''] + c2 + ['',
     '## 直す所見（逐語・二度目の見直しの記録の §3 の表の行）', '', R2[hd[0]], R2[hd[0] + 1]] + rows + ['',
     '## 裁定', '',
     '- **D251**: 一度目の見直しの F-a の直し（〈両方の外〉の注の逆数の言い方）を最終版に入れる（逸脱の器 v2 の組み方で既に入っている）。R-d のうち D251 に伴う書き方の合わせも行う。',
     '- **D252**: 公開の仕上げは、二度目の見直しの記録の §5 の D252 の甲（R-h で補った文）のとおりとする。登録者最終確認の後に組み直した最終版と、確認していただいた案との違いが、状態の行と、頭の添えの一行目の置き場の報告の SHA16 だけであることを器で確かめる。タグの名の日付は公開の日（日本時間）。',
     '- **D253**: R-a・R-b・R-c・R-d を直す（逸脱の器を v3 に上げ、草案の二つ目との違いの決めた行に、直した行を足す）。%s は記録に置く（二度目の見直しの記録のまま）。直した最終版の案は、器の確かめと器とは別の確かめを通してから、登録者最終確認に出す。' % '・'.join(x[2:] for x in rec if x[2:] in ('R-e', 'R-f', 'R-g')), '',
     '## 注（事実のみ）', '',
     '- 同じ言葉で、登録者は c9ea96c（二度目の見直しの枠）と 352cfa9（二度目の見直しの記録と器の確かめ）の push を許した。push は %s（手元の remote の追跡の参照の reflog）。' % m_push.group(1),
     '- 二度目の見直しの記録の所見の番号は %s。R-h は D252 の補い、R-i は一度目の見直しの記録の COI の行の書き留め（一度目の記録は書き換えない）。' % '・'.join(['R-a', 'R-b', 'R-c', 'R-d'] + [x[2:] for x in rec]),
     '- D251〜D253 は下見の前の凍結の後の裁定なので、凍結した正本の `decisions` には入らない。台帳（`records/FREEZE-RECORD.md`）には行を足さない（裁定 D249 の器 v2 と同じく、逸脱 D-BLT1 の器の中の直しで、新しい逸脱ではない）。',
     '- 番号: 次の裁定は D254 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| words', jst(ts), uuid, '| rev1', C1, s1, '| rev2', C2, s2, '| rows', len(rows), '| push', m_push.group(1))
