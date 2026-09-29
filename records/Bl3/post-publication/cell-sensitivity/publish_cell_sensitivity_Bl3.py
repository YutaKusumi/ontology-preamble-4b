# -*- coding: utf-8 -*-
"""層三の升目ごとの揺れの広さ（登録外の記述・公開の後）を、非公開の置き場から公開の置き場に置く（登録者「公開の置き場にも置いてください」2026-09-29）。
- 枠 `frame-cell-sensitivity-Bl3.md` と控え `frame-stamp.txt` は、一字違わず写す（枠の SHA16 が控えの値と同じことを確かめる）。
- 台本 `cell_sensitivity_Bl3.py` は、置き場の道筋だけを相対に改めたものを置き、ここで走らせて出した表と JSON が、非公開の置き場の表と JSON とバイトで同じことを確かめる（台本の違いは一行だけであることも確かめる）。
- 登録者の言葉と、元の問いの文（コーディネータの答え）は、会話の記録から機械で切り出す（手で打たない）。枠の問いの文との違いを機械で確かめて開示する。案内 `README.md` を一度だけ書く。
用法: python records/Bl3/post-publication/cell-sensitivity/publish_cell_sensitivity_Bl3.py <非公開の置き場の cell-sensitivity の folder> <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, shutil, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
NL = chr(10)
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16 = lambda p: s16b(open(p, 'rb').read())
SRC, LOG = sys.argv[1], sys.argv[2]
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
H = lambda n: os.path.join(HERE, n)
OUT_IDX = H('README.md')
assert not os.path.exists(OUT_IDX), '既にある（一度だけ）'
FR, ST, SC, MD, JS = 'frame-cell-sensitivity-Bl3.md', 'frame-stamp.txt', 'cell_sensitivity_Bl3.py', 'cell-sensitivity-Bl3.md', 'cell-sensitivity-Bl3.json'
for n in (FR, ST, SC, MD, JS):
    assert not os.path.exists(H(n)), n
# 枠と控え
for n in (FR, ST):
    shutil.copyfile(os.path.join(SRC, n), H(n))
stamp = open(H(ST), encoding='utf-8').read()
assert s16(H(FR)) in stamp, '枠の SHA16 が控えと違う（止める）'
frame = open(H(FR), encoding='utf-8').read()
# 台本（道筋だけ相対に）
code0 = open(os.path.join(SRC, SC), encoding='utf-8').read()
hit = re.findall(r"^REPO = '[A-Za-z]:/[^']*'$", code0, flags=re.M)
assert len(hit) == 1, '置き場の道筋の行が一つに決まらない（止める）'
code = code0.replace(hit[0], "REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))   # 公開の置き場では、置き場からの相対（非公開の置き場で走らせた版との違いはこの一行だけ）")
assert not re.search(r"[A-Za-z]:/", code), '台本に道筋が残る（止める）'
a_, b_ = code0.split(NL), code.split(NL)
assert len(a_) == len(b_) and sum(1 for x, y in zip(a_, b_) if x != y) == 1, '台本の違いが一行でない（止める）'
open(H(SC), 'w', encoding='utf-8', newline=NL).write(code)
r = subprocess.run([sys.executable, H(SC)], cwd=REPO, capture_output=True, text=True, encoding='utf-8', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
assert r.returncode == 0, r.stderr[-800:]
same = {n: s16(H(n)) == s16(os.path.join(SRC, n)) for n in (MD, JS)}
assert all(same.values()), ('公開の置き場で出した表が、非公開の置き場の表と違う（止める）', same)
J = json.load(open(H(JS), encoding='utf-8'))
for k, v in J['source'].items():
    assert s16(os.path.join(REPO, *k.split('/'))) == v, ('値の出所の SHA16 が今の置き場と違う（止める）', k)


# 会話の記録から、登録者の言葉と元の問いの文を切り出す
def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return ''


U_place, U_req, A_q = {}, {}, {}
for line in open(LOG, encoding='utf-8'):
    if '公開の置き場にも置いてください' not in line and '立ちうる問い' not in line:
        continue
    try:
        o = json.loads(line)
    except Exception:
        continue
    t, s = o.get('type'), text_of(o)
    if t == 'user' and 'toolUseResult' not in o and not s.startswith('This session is being continued'):
        if '新たな共創の種になりますね。公開の置き場にも置いてください' in s:
            U_place[o['uuid']] = (o['timestamp'], s)
        if '」の「立ちうる問い」を登録外の' in s:
            U_req[o['uuid']] = (o['timestamp'], s)
    if t == 'assistant' and '## 4. 機根——' in s and '立ちうる問い：どの文脈で' in s:
        A_q[o['uuid']] = (o['timestamp'], s)
assert len(U_place) == 1 and len(U_req) == 1 and len(A_q) == 1, (len(U_place), len(U_req), len(A_q))
(u_place, (ts_place, s_place)), = U_place.items()
(u_req, (ts_req, s_req)), = U_req.items()
(u_q, (ts_q, s_q)), = A_q.items()
seg_place = re.search('公開の置き場にも置いてください', s_place).group(0)
heading = re.search('## 4[.] (機根——[^' + NL + ']*)', s_q).group(1)
question = re.search('立ちうる問い：(どの文脈で[^。]*?のか)。', s_q).group(1)
assert ('「%s」' % heading) in frame, '喩えの名が枠と元の文で違う（止める）'
fq = re.search('の立ちうる問い「([^」]*)」', frame).group(1)
assert fq != question and fq.replace('（升目）', '') == question, ('枠の問いの文と元の文の違いが、見つけたものと違う（止める）', fq, question)
MODEL = 'Qwen3-4B-Instruct-2507'
assert MODEL in frame
L = ['# 層三の升目ごとの揺れの広さ（登録外の記述・層三の公開の後・2026-09-29）', '',
     '- 性格: **登録外の記述**。層三の登録（凍結の本文・正本・最終版 `records/Bl3/results-Bl3-FINAL-2026-09-27.md`）の外に置く。札・読みの型・報告の文は変えない。層三の記録にある値（最後の層の、等方のランダム方向と実在の差の方向の効き目・層ごとの等方の区間・下見の升目の値）を並べただけで、新しい計算はしていない。',
     '- 経緯: 登録者が、空海の『秘密曼荼羅十住心論』の視点からのインスピレーションを問い、コーディネータが仮説としていくつかを挙げた。その一つ「%s」の立ちうる問い「%s」（元の文・コーディネータの答え・会話の記録 uuid `%s`・%s 日本時間）を、登録者が登録外として調べるよう求め（会話の記録 uuid `%s`・%s 日本時間）、コーディネータが非公開の置き場で行った。登録者は報告を受けた後、公開の置き場に置くことを求めた。登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (
         heading, question, u_q, jst(ts_q), u_req, jst(ts_req), u_place, jst(ts_place), seg_place),
     '- 呼び名: 「機根」は問いを生んだ喩えで、記録では中立に「升目ごとの揺れの広さ」と呼ぶ。模型に能力や心の性質を帰さない（枠の頭）。',
     '- 値の出所: ' + '・'.join('`%s`（SHA16 %s）' % (k, v) for k, v in J['source'].items()) + '。',
     '- 置き方: 枠 `%s` は、値を見る前に非公開の置き場で書いたもので、一字違わず写した（題の「非公開」は書いたときの状態・時刻とハッシュは `%s`・SHA16 %s）。台本 `%s` は、置き場の道筋の一行だけを相対に改め、ここで走らせて出した表 `%s`（SHA16 %s）と値 `%s`（SHA16 %s）が、非公開の置き場で出したものとバイトで同じことを確かめた（`publish_cell_sensitivity_Bl3.py`）。' % (
         FR, ST, s16(H(FR)), SC, MD, s16(H(MD)), JS, s16(H(JS))),
     '- 枠について開示すること:',
     '  - 枠の頭の依頼の行で、問いの文を鉤括弧に入れたとき、起草者が元の文に無い「（升目）」を補った（逐語の決まりに反する）。枠は控えのハッシュのまま写したので、直していない。元の文は、上の経緯の鉤括弧の中のとおり（会話の記録から機械で切り出した）。公開の置き場に置く段で、起草者が元の文と照らして見つけた。',
     '  - 枠からのずれ一つ（等方の効き目がある升目と符号は %d・± の組は %d）は、表の頭に開示した。' % (len(J['cellsigns_with_iso']), len(J['pairs'])),
     '- 読みの決まり（枠に先に書いた）: 記述であり、検定ではない（升目は少ない）。唯一の等方の外の行を、升目の区間が狭いから「見かけ」だったとも、狭い升目だから「特別」だったとも読まない。途中の層の値は、その層で模型が使う量と同じである保証が無く、どの層も「転換層」と呼ばない。模型の性質の言葉を結果の記述に使わない。',
     '- 範囲: この記録は %s だけの記述で、機種の間の違いについては何も言わない。' % MODEL,
     '- 表・枠の予想との照らし・記述・検分票（確認していないことを含む）は `%s` にある。' % MD, '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_IDX, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('placed | frame', s16(H(FR)), '| md', s16(H(MD)), '| json', s16(H(JS)), '| same as internal', same,
      '| place', jst(ts_place), u_place, '| request', jst(ts_req), u_req, '| question', jst(ts_q), u_q)
