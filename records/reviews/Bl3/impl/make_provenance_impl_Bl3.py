# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の器の実装の検分の票の出所の記録を書く（枠 `frame-impl-Bl3.md` §2）。数と SHA と逐語は器の出力から機械で入れる（手で打たない）。
- 票の置き場・字数・バイト・SHA-256・SHA16（LF にそろえた）・機種の欄・終わりの通知との同じか（`<札>/meta.json`）。
- 使った量（トークン・時間）と、起動の前の申告（`permission-impl-Bl3.md` の申告の段）を並べる。
- 検分者の作業場で追跡しているファイルの変化（git status と git diff）。
- コーディネータが起動の後に検分者へ送った知らせ（会話の記録の SendMessage の呼び出しから逐語で切り出す・検分者の内部の番号は書かない）。
既にある記録には書かない。
用法: python records/reviews/Bl3/impl/make_provenance_impl_Bl3.py <会話の記録 jsonl> <R1 の内部の番号> <R2 の内部の番号> <R1 の作業場> <R2 の作業場>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'provenance-impl-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
sess, ref = sys.argv[1], {'R1': sys.argv[2], 'R2': sys.argv[3]}
wt = {'R1': sys.argv[4], 'R2': sys.argv[5]}
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
rows, msgs = [], {'R1': [], 'R2': []}
for line in open(sess, encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'assistant':
        continue
    for c in (o.get('message') or {}).get('content') or []:
        if isinstance(c, dict) and c.get('type') == 'tool_use' and c.get('name') == 'SendMessage':
            to = (c.get('input') or {}).get('to')
            for tag, r in ref.items():
                if to == r:
                    msgs[tag].append((o.get('timestamp'), c['input'].get('message') or ''))
perm = open(os.path.join(HERE, 'permission-impl-Bl3.md'), encoding='utf-8').read()
decl = [l.strip() for l in perm.split(NL) if '費用の見込み' in l or '体数と機種' in l]
L = ['# 器の実装の検分（二体）の票の出所（機械生成・`make_provenance_impl_Bl3.py`・%s）' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), '',
     '- 検分者: 系統内の新しい個体二体（R1・R2）。コーディネータと同じ系列なので、二体で一つに数える（裁定 D59）。二体の一致は独立の確かめではない。',
     '- 保全の仕方: 票の本文は、検分者の会話の記録の最後の本文から機械で切り出した（`save_vote_impl_Bl3.py`）。会話の記録に届いた終わりの通知の本文（XML の文字の置き換えを戻したもの）と突き合わせた。',
     '- 票は書き換えない。所見の採否は、コーディネータが検分の版の一次の実物で再現してから決める（枠 §2・確かめの記録 `checks/`）。',
     '- 起動の前の申告（`permission-impl-Bl3.md` の申告の段から機械で拾った行）: %s' % ' ／ '.join(decl), '',
     '| 札 | 担当 | 置き場 | 字数 | バイト | SHA-256 | SHA16（LF） | 機種の欄 | 通知の本文と | 使ったトークン | 道具の呼び出し | 時間（分） |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for tag in ('R1', 'R2'):
    d = os.path.join(HERE, tag.lower())
    M = json.load(open(os.path.join(d, 'meta.json'), encoding='utf-8'))
    b = open(os.path.join(d, 'review.md'), 'rb').read()
    u = M.get('usage') or {}
    L.append('| %s | %s | `%s/review.md` | %d | %d | %s | %s | %s | %s | %s | %s | %s |' % (
        tag, M['role'], tag.lower(), M['body_chars'], len(b), sha256b(b), sha256b(b.replace(b'\r\n', b'\n'))[:16], '・'.join(M['models']), '同じ' if M['notification_body_same'] else '違う',
        u.get('subagent_tokens'), u.get('tool_uses'), round(u['duration_ms'] / 60000) if u.get('duration_ms') else None))
COPIED = [('R1', 'r1/dry-run-R1.md', '合成データの確かめの記録（検分者が走らせた・採否表 P694）'), ('R1', 'r1/preregistration-R1.txt', '検分者の事前登録（判定の規則・予想・COI）'),
          ('R2', 'r2/dry-run-R2.md', '合成データの確かめの記録（検分者が走らせた・採否表 P694）'), ('R2', 'r2/prereg-R2.txt', '検分者の事前登録（判定表・予想・COI）')]
L += ['', '## 検分者の一時の置き場から写した記録（バイトのまま・正本 review_plan.impl.focus の「その記録を残す」）', '', '| 札 | 置き場 | 何か | バイト | SHA-256 |', '|---|---|---|---|---|']
for tag, rp, what in COPIED:
    b_ = open(os.path.join(HERE, *rp.split('/')), 'rb').read()
    L.append('| %s | `%s` | %s | %d | %s |' % (tag, rp, what, len(b_), sha256b(b_)))
L += ['', '- 検分者の一時の置き場の残り（試しの台本・試しの出力・起動器の DRY の出力）は写していない（票に置き場の名が書かれている・一時の置き場は後で消えうる）。']
L += ['', '## 検分者の作業場（票を受け取った後に確かめた）', '']
for tag in ('R1', 'R2'):
    head = subprocess.run(['git', '-C', wt[tag], 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
    st = subprocess.run(['git', '-C', wt[tag], 'status', '--porcelain', '--untracked-files=all'], capture_output=True, text=True).stdout.strip().split(NL)
    df = subprocess.run(['git', '-C', wt[tag], 'diff', '--stat'], capture_output=True, text=True).stdout.strip()
    L.append('- %s: 作業場のコミット %s・追跡しているファイルの差分 %s・追跡の外のファイル %s' % (tag, head, '無し' if not df else df.split(NL)[-1], '・'.join('`%s`' % x[3:] for x in st if x.startswith('??')) or '無し'))
L += ['', '## コーディネータが起動の後に検分者へ送った知らせ（逐語・会話の記録の SendMessage の呼び出しから）', '']
for tag in ('R1', 'R2'):
    for ts, m in msgs[tag]:
        L += ['- %s へ（%s 日本時間）:' % (tag, jst(ts)), '', '````text', m, '````', '']
L += ['## 注（事実のみ）', '',
      '- 検分者の作業場は、ローカルの依頼のコミット c1a759c ではなく push 済みの 87ce664 から作られ、依頼文は作業場に無かった。起動の直後に、二体へ `git show c1a759c:…` で依頼文を読むよう知らせた（上の一つ目の知らせ）。二体とも票の冒頭に、依頼文を読む前にしたことを書いている。',
      '- R2 へ二つ目の知らせで「起動器の DRY が止まっているように見える」と伝えたのは、コーディネータの読み違いだった。R2 の票によれば、R2 が外の走りを遅くしないよう優先度を下げて走らせていたためで、塞がってはいなかった（R2 は止めも走らせ直しもしていない）。',
      '- 二体とも、使った量が起動の前の申告（一体あたりのトークンと時間）を超えた。同じ機械でコーディネータの正式の合成データの記録と並べて走らせたため、合成データの確かめの走りが長くなった。',
      '- 二体の一時の置き場は、同じ一時の置き場の根の下（r1・r2）にあった。二体とも、もう一体の置き場は開いていないと票に書いている（申告）。',
      '- 起動の時に、検分者の文脈には利用者の記憶の索引（計画の工程の要約を含む）が環境から入っていた（R1 の票の開示）。R1 は git の履歴で枠のコミットの件名の一行を見たと開示している（中身は開いていないと申告）。R2 は器の段の記録（§10〜§12・正式の記録の予想を含む）を読んだと開示している。',
      '- 検分者の内部の番号は、この記録に書かない（検分者の会話の記録を探すためだけに使った）。',
      '- 二体の票の本文の終わりには、検分者の一時の置き場の道筋（利用者の名と会話の番号を含む）が書かれている。票は逐語で保全するので、そのまま残した（秘密の値ではない）。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('[make_provenance_impl_Bl3] wrote %s（知らせ R1 %d・R2 %d）' % (os.path.relpath(OUT, REPO), len(msgs['R1']), len(msgs['R2'])))
