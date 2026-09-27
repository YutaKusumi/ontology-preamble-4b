# -*- coding: utf-8 -*-
"""層三の層ごとの差分の表（登録外の記述・公開の後）を、非公開の置き場から公開の置き場に置く（登録者「今回の層ごとの記録は、登録外の記述として公開の置き場にも置いてください」2026-09-27）。
- 枠 `frame-layerwise-Bl3.md` と控え `frame-stamp.txt` は、一字違わず写す（枠の SHA16 が控えの値と同じことを確かめる）。
- 表の台本 `layerwise_Bl3.py` は、置き場の道筋だけを相対に改めたものを置き、ここで走らせて出した表と JSON が、非公開の置き場の表と JSON とバイトで同じことを確かめる。
- 登録者の言葉は会話の記録から機械で切り出す（手で打たない）。案内 `README.md` を一度だけ書く。
用法: python records/Bl3/post-publication/layerwise/publish_layerwise_Bl3.py <非公開の置き場の layerwise の folder> <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, shutil, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
NL = chr(10)
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16 = lambda p: s16b(open(p, 'rb').read())
SRC = sys.argv[1]
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
OUT_IDX = os.path.join(HERE, 'README.md')
assert not os.path.exists(OUT_IDX), '既にある（一度だけ）'
# 枠と控え
for n in ('frame-layerwise-Bl3.md', 'frame-stamp.txt'):
    assert not os.path.exists(os.path.join(HERE, n))
    shutil.copyfile(os.path.join(SRC, n), os.path.join(HERE, n))
stamp = open(os.path.join(HERE, 'frame-stamp.txt'), encoding='utf-8').read()
assert s16(os.path.join(HERE, 'frame-layerwise-Bl3.md')) in stamp, '枠の SHA16 が控えと違う（止める）'
# 台本（道筋だけ相対に）
code = open(os.path.join(SRC, 'layerwise_Bl3.py'), encoding='utf-8').read()
hit = re.findall(r"^REPO = '[A-Za-z]:/[^']*'$", code, flags=re.M)
assert len(hit) == 1, '置き場の道筋の行が一つに決まらない（止める）'
code = code.replace(hit[0], "REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))   # 公開の置き場では、置き場からの相対（非公開の置き場で走らせた版との違いはこの一行だけ）")
assert not re.search(r"[A-Za-z]:/", code), '台本に道筋が残る（止める）'
open(os.path.join(HERE, 'layerwise_Bl3.py'), 'w', encoding='utf-8', newline=NL).write(code)
r = subprocess.run([sys.executable, os.path.join(HERE, 'layerwise_Bl3.py')], cwd=REPO, capture_output=True, text=True, encoding='utf-8')
assert r.returncode == 0, r.stderr[-500:]
same = {n: s16(os.path.join(HERE, n)) == s16(os.path.join(SRC, n)) for n in ('layerwise-Bl3.md', 'layerwise-Bl3.json')}
assert all(same.values()), ('公開の置き場で出した表が、非公開の置き場の表と違う（止める）', same)
# 登録者の言葉
U = []
for line in open(sys.argv[2], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str) and '今回の層ごとの記録は、登録外の記述として公開の置き場にも置いてください' in c:
        U.append((o.get('uuid'), o.get('timestamp'), c))
assert len(U) == 1, len(U)
uuid, ts, words = U[0]
seg = re.search(r'今回の層ごとの記録は、登録外の記述として公開の置き場にも置いてください。', words).group(0)
A = os.path.join(REPO, 'records', 'Bl3', 'analysis-Bl3.json')
L = ['# 層三の層ごとの差分の表（登録外の記述・層三の公開の後・2026-09-27）', '',
     '- 性格: **登録外の記述**。層三の登録（凍結の本文・正本・最終版 `records/Bl3/results-Bl3-FINAL-2026-09-27.md`）の外に置く。札・読みの型・報告の文は変えない。層三の凍結した記述（正本 `descriptive.layerwise`・裁定 D203・D208）の値を、表に並べただけである。',
     '- 経緯: 登録者が系統外（Gemini）との対話で出た「各層の軌道分解」を、取得してあるデータで行うよう求め、コーディネータが非公開の置き場で行った。登録者の言葉（逐語の一文・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), seg),
     '- 値の出所: `records/Bl3/analysis-Bl3.json`（SHA16 %s）の `layerwise`（選んだ第 17 層の後の第 18〜35 層・等方は層ごとの中央値と 95%% の中央の区間だけ）。' % s16(A),
     '- 置き方: 枠 `frame-layerwise-Bl3.md` は、値を見る前に非公開の置き場で書いたもので、一字違わず写した（題の「非公開」は書いたときの状態・時刻とハッシュは `frame-stamp.txt`・SHA16 %s）。表の台本 `layerwise_Bl3.py` は、置き場の道筋の一行だけを相対に改め、ここで走らせて出した表 `layerwise-Bl3.md`（SHA16 %s）と値 `layerwise-Bl3.json`（SHA16 %s）が、非公開の置き場で出したものとバイトで同じことを確かめた（`publish_layerwise_Bl3.py`）。' % (
         s16(os.path.join(HERE, 'frame-layerwise-Bl3.md')), s16(os.path.join(HERE, 'layerwise-Bl3.md')), s16(os.path.join(HERE, 'layerwise-Bl3.json'))),
     '- 読みの決まり（枠に先に書いた）: どの層も「効き目が生まれた層」「転換層」と呼ばない。区間の内か外かは記述で、検定ではない。途中の層の残差を最終の正規化と語彙の行列に当てた値は、その層で模型が使う量と同じである保証が無い（正本の注）。この表は、後の層の部品ごとの差し替え（計画の ③）の根拠にしない。',
     '- 会話で示した図は置いていない（値は表と JSON にある）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_IDX, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('placed | frame', s16(os.path.join(HERE, 'frame-layerwise-Bl3.md')), '| md', s16(os.path.join(HERE, 'layerwise-Bl3.md')), '| json', s16(os.path.join(HERE, 'layerwise-Bl3.json')), '| same as internal', same, '| words', jst(ts), uuid)
