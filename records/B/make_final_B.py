# -*- coding: utf-8 -*-
"""make_final_B.py —— 段階 B の結果報告の最終版 `records/B/results-B-FINAL-2026-09-23.md` を、草案5（最終案・`results-B.md`）の逐語の写しとして作る。
変えるのは題の行の「草案5（最終案）」→「最終版」と、登録者の最終確認の一行（数を含むので機械の区画に置く）を足すことだけ（登録者の言葉は会話の記録から機械で切り出す）。段階 A の最終版と同じ型。
用法: python records/B/make_final_B.py <会話の記録 jsonl>"""
import os, sys, json, hashlib, datetime, subprocess

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import report_lint as RL
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda t: hashlib.sha256(t.encode('utf-8')).hexdigest().upper()[:16]

words, uuid, ts = None, None, None
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
        if '最善のことを尽くした' in t and 'f62f0fe' in t and len(t) < 600:
            words, uuid, ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '最終確認の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')

src = open(j('records', 'B', 'results-B.md'), encoding='utf-8').read()
lines = src.split(NL)
assert lines[0].startswith('# 段階 B 結果報告（表紙・草案5（最終案））')
lines[0] = lines[0].replace('草案5（最終案）', '最終版')
status = ('- 状態: **最終版**（登録者最終確認 %s 日本時間・会話の記録 uuid `%s`・逐語「%s」）。草案5（最終案・`results-B.md`・SHA16 %s）の逐語の写しで、題の行とこの一行のほかは一字も変えていない。'
          '以後の変更は凍結の記録の逸脱台帳（D-B7 から）に記帳する。' % (jst, uuid, words.replace(NL, ' '), s16(src)))
assert lines[1] == '' and lines[2].startswith('- 起草:')
MB = RL.machine_block(json.load(open(j('design', 'contrasts-B.json'), encoding='utf-8')))
out_lines = lines[:3] + [MB['begin'], status, MB['end']] + lines[3:]      # 数（時刻・uuid・SHA16・逐語の中の数）を含むので機械の区画に置く
text = NL.join(out_lines)
# 写しの確かめ: 題の行と足した一行を除けば同一
assert NL.join([out_lines[0].replace('最終版', '草案5（最終案）')] + out_lines[1:3] + out_lines[6:]) == src
out = j('records', 'B', 'results-B-FINAL-2026-09-23.md')
assert not os.path.exists(out), '最終版は既にある（上書きしない）'
open(out, 'w', encoding='utf-8', newline=NL).write(text)
T = json.load(open(j('design', 'contrasts-B.json'), encoding='utf-8'))
RL.write_sidecar(out, text, T, 'records/B/make_final_B.py')
rc = subprocess.run([sys.executable, j('tools', 'report_lint.py'), out, '--contrasts', j('design', 'contrasts-B.json'), '--out', j('records', 'B', 'results-B-FINAL-2026-09-23-lint.md')],
                    env=dict(os.environ, PYTHONUTF8='1')).returncode
print('FINAL', s16(text), 'lint rc', rc, '| confirmation', jst, uuid)
sys.exit(rc)
