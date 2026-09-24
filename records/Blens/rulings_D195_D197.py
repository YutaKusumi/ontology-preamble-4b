# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D195〜D197 の記録を書き、逸脱 D-BL5（最終検分の票の数）と、逸脱 D-BL3 の更新（組み立ての器 v2・報告の最終版）を
凍結の記録の逸脱台帳に記す（2026-09-24・最終検分の後）。
登録者の言葉と、裁定の前にコーディネータが示した案は、会話の記録から機械で切り出す（手で打たない）。器と出力の SHA16 は器が計算する。
台帳に記す前と後に、逸脱の下の組み立ての器で草案の二つ目と最終版を組み直し、置き場のファイルと同じことを確かめる。既にある記録には書かない。
用法: python records/Blens/rulings_D195_D197.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
P = lambda r: os.path.join(REPO, *r.split('/'))
s16 = lambda r: hashlib.sha256(open(P(r), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
OUT = os.path.join(HERE, 'rulings-D195-D197.md')
FR_JSON, FR_MD = os.path.join(HERE, 'FREEZE-RECORD-Blens.json'), os.path.join(HERE, 'FREEZE-RECORD-Blens.md')
BUILDER = 'tools/build_report_Blens_devBL3.py'
FINAL = 'records/Blens/results-Blens-FINAL-2026-09-24.md'
ADOPT = 'records/reviews/Blens/results-final/adoption-table-Blens-results-final.md'
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')


def rebuild_same():
    """逸脱の下の組み立ての器で、草案の二つ目と最終版を組み直し、置き場のファイルと同じこと（器は書かない）を確かめる。"""
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    for args in ([], ['--final']):
        r = subprocess.run([sys.executable, P(BUILDER)] + args, cwd=REPO, capture_output=True, env=env)
        out = r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')
        if r.returncode != 0 or '既にある出力と同じ（書かない）' not in out or '走査の違反 0' not in out:
            raise SystemExit('組み直しが置き場と同じにならない（止める）: %s %s' % (args, out.strip()[-300:]))
        if args and '草案の二つ目と同じ（作り直し）' not in out:
            raise SystemExit('最終版の組み直しで、草案の二つ目の確かめが出ていない（止める）')


MSGS = []                                   # (種類, uuid, 時刻, 文)
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    t = o.get('type')
    c = (o.get('message') or {}).get('content')
    items = [{'type': 'text', 'text': c}] if isinstance(c, str) else [x for x in (c or []) if isinstance(x, dict)]
    for x in items:
        if x.get('type') == 'text' and t in ('user', 'assistant'):
            MSGS.append((t, o.get('uuid'), o.get('timestamp'), x.get('text') or ''))
ruling = [m for m in MSGS if m[0] == 'user' and len(m[3]) < 800 and '裁定は推奨どおりで' in m[3] and 'c8ab5ac' in m[3]]
assert len(ruling) == 1, len(ruling)
ruling = ruling[0]
opts = [m for m in MSGS if m[0] == 'assistant' and '**D195**' in m[3] and '**D196**' in m[3] and '**D197**' in m[3] and m[2] < ruling[2]]
assert opts, '裁定の前の案が見つからない'
opts = opts[-1]
words = ruling[3].strip().replace(NL, ' ')
approval = lambda d: '登録者裁定 %s（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」）' % (d, jst(ruling[2]), ruling[1], words)
day = jst(ruling[2]).split(' ')[0]

rebuild_same()                                                    # 台帳に記す前
FR = json.load(open(FR_JSON, encoding='utf-8'))
assert [d['no'] for d in FR['deviations']] == ['D-BL1', 'D-BL2', 'D-BL3', 'D-BL4'], [d['no'] for d in FR['deviations']]
d3 = [d for d in FR['deviations'] if d['no'] == 'D-BL3'][0]
assert 'updates' not in d3
v1 = [f['sha16'] for f in d3['files'] if f['path'] == BUILDER][0]
assert v1 != s16(BUILDER), '器が v1 のまま'
lint_n = int(re.search(r'- 違反 (\d+)', open(P(FINAL.replace('.md', '-lint.md')), encoding='utf-8').read()).group(1))
assert lint_n == 0, lint_n
upd = {'date': day,
       'what': ('**報告の最終版の組み立て（器 v2）**。最終検分の二票の所見（採否表 `%s` の区分（三）の行 P605〜P609）を受け、逸脱の下の器 `%s` を v2（SHA16 %s・v1 は SHA16 %s）に改めた。'
                '`--final` で最終版 `%s`（SHA16 %s・走査の違反 %d）を組む。足した行は、§0 の §1 への参照・§3 の大きさの目盛りの表の並べ直し（行の名の縦棒を字にした・列と値は凍結の器の出力のまま）・'
                '§8 の一致の注と登録者の予想のファイルの時刻の注（時刻は露出の記録から器が読む）・§9 の門の限界の句。v2 は、草案の二つ目を同じ走りで作り直して置き場と同じことと、'
                '草案の二つ目から改めた行が決めた行（見出し・状態・冒頭の添え・§9 の門の限界の箇条・検分票）だけであることを確かめる。`--final` が無ければ、出力は v1 と同じ（草案の二つ目）')
               % (ADOPT, BUILDER, s16(BUILDER), v1, FINAL, s16(FINAL), lint_n),
       'scope': '報告の表し方だけ（札・門・大きさの目盛りの判定と、凍結した器の出力と、草案の二つ目は変えない）',
       'approval': approval('D196'),
       'files': [{'path': BUILDER, 'sha16_v1': v1, 'sha16_v2': s16(BUILDER)}] + [{'path': p_, 'sha16': s16(p_)} for p_ in (FINAL, FINAL.replace('.md', '-machine.json'), FINAL.replace('.md', '-lint.md'))]}
dev5 = {'no': 'D-BL5', 'date': day,
        'what': ('**最終検分の票の数**。正本 `review_plan.final.external` と凍結の本文 §10 は、最終を系統外の一票とした。登録者は、最終検分（登録者裁定 D194）を新しい Gemini 3.8 Flash の二名に依頼し、'
                 '二票になった（F1・F2・どちらも条件つき可）。二票をともに最終検分とし、所見は和集合で受けた。票の置き場は `records/reviews/Blens/results-final/gemini-final-1/` と `gemini-final-2/` に分けた'
                 '（枠 `frame-Blens-results-final.md` の §2 は一つの置き場とした）。記録 `records/Blens/rulings-D195-D197.md`・採否表 `%s`') % ADOPT,
        'scope': '最終検分の組み立てだけ（同じ機種の二票は、会話が別でも相関しうるので、独立の重みを二倍には数えない）。報告の札と数は変えない',
        'approval': approval('D195')}
d3['updates'] = [upd]
FR['deviations'].append(dev5)
json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = open(FR_MD, encoding='utf-8').read()
cell = lambda s: s.replace('|', '｜')
a3 = [l for l in md.split(NL) if l.startswith('| D-BL3 |')]
a4 = [l for l in md.split(NL) if l.startswith('| D-BL4 |')]
assert len(a3) == 1 and len(a4) == 1
md = md.replace(a3[0], a3[0] + NL + '| D-BL3（更新・器 v2） | %s | %s | %s | %s |' % (upd['date'], cell(upd['what']), upd['scope'], cell(upd['approval'])), 1)
md = md.replace(a4[0], a4[0] + NL + '| %s | %s | %s | %s | %s |' % (dev5['no'], dev5['date'], cell(dev5['what']), dev5['scope'], cell(dev5['approval'])), 1)
open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md)
rebuild_same()                                                    # 台帳に記した後（最終版は台帳に依らない）

RUL = [('D195', '最終検分は、登録者が依頼した新しい Gemini 3.8 Flash の二票（F1・F2）とする。二票の所見は和集合で受ける。正本 `review_plan.final.external` と凍結の本文 §10 の「系統外の一票」を二票にしたことを、逸脱 D-BL5 として台帳に記す（報告の札と数は変えない）'),
       ('D196', '最終検分の採否表（`%s`）の区分（三）の行（P605〜P609・P609 の §9 の門の限界の句は推奨どおり入れる）を、逸脱の下の組み立ての器 v2（D-BL3 の更新・`--final`）で最終版 `%s` に入れる。'
                '区分（一）の行は案のとおり記録に置く。最終版の後に検分の巡を置かない（D194）。逸脱台帳の D-BL3 に、v2 の器と最終版を足す' % (ADOPT, FINAL)),
       ('D197', '最終版の公開（GitHub への push）は、登録者が最終版を確かめた後とする')]
R = ['# 登録者裁定 D195〜D197（2026-09-24・最終検分の後）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (ruling[1], jst(ruling[2]), words), '',
     '| 裁定 | 中身 |', '|---|---|'] + ['| %s | %s |' % kv for kv in RUL] + [
     '', '## 裁定の前にコーディネータが示した案（逐語・会話の記録 uuid `%s`・%s 日本時間）' % (opts[1], jst(opts[2])), '', '````text', opts[3].rstrip(), '````', '',
     '## 注（事実のみ）', '',
     '- 採否表: `%s`。再現の表: 同じ置き場の `verification-Blens-results-final.md`。二票: 同じ置き場の `gemini-final-1/review.md`・`gemini-final-2/review.md`。' % ADOPT,
     '- 登録者の許可を受けて、二票・再現の表・採否表のコミット c8ab5ac を push した。',
     '- 逸脱 D-BL5 と、D-BL3 の更新（器 v2・最終版）を凍結の記録の逸脱台帳に記した（器と出力の SHA16 は器が計算した）。台帳に記す前と後に、器で草案の二つ目と最終版を組み直し、置き場のファイルと同じことを確かめた。',
     '- 最終版 `%s`（SHA16 %s）の公開は、登録者の最終確認の後（D197）。' % (FINAL, s16(FINAL)),
     '- 番号: 次の裁定は D198 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '|', jst(ruling[2]), ruling[1], '| options', jst(opts[2]), opts[1], '| D-BL5 + D-BL3 update ledgered | FINAL', s16(FINAL), '| builder v2', s16(BUILDER), 'v1', v1)
