# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D228〜D230 の記録を書く（器の段の三回目の区切りの後）。
登録者の言葉と、裁定の前にコーディネータが示した推奨の段は、会話の記録から機械で切り出す（手で打たない）。
採られた案: D228・D229 は抜き書きの各裁定の一つ目の案、D230 は二つ目の案（登録者の言葉「D230は、２の方向性で」）に、登録者の言葉の D230 の段（逐語・機械で切り出す）を添える。
既にある記録には書かない。
用法: python records/Bl3/rulings_D228_D230.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D228-D230.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
M = []
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
            M.append((t, o.get('uuid'), o.get('timestamp'), x.get('text') or ''))
one = lambda f: (lambda h: (h[0] if len(h) == 1 else (_ for _ in ()).throw(SystemExit('一つに決まらない: %d' % len(h)))))([m for m in M if f(m)])
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and 'D228〜D229はご推奨どおりで' in m[3])
H0, H1 = '## ご裁定をお願いしたいこと（一つ目が私の推奨）', '## 次に進む前のお願い'
rec = one(lambda m: m[0] == 'assistant' and H0 in m[3] and H1 in m[3] and all(d in m[3] for d in ('D228', 'D229', 'D230')) and m[2] < appr[2])
excerpt = rec[3][rec[3].index(H0):rec[3].index(H1)].rstrip()
ask = rec[3][rec[3].index(H1):].rstrip()


def option(d, k):
    """抜き書きの裁定 d の k 番目の案（字下げの改行は空白にした）。"""
    seg = excerpt[excerpt.index('**%s' % d):]
    nxt = [seg.find('- **D%d' % n) for n in range(int(d[1:]) + 1, int(d[1:]) + 3) if seg.find('- **D%d' % n) > 0]
    seg = seg[:min(nxt)] if nxt else seg
    m = re.search(r'^  %d\. (.+?)(?=^  %d\. |\n\n|\n\S|\Z)' % (k, k + 1), seg, flags=re.M | re.S)
    assert m, (d, k)
    return ' '.join(x.strip() for x in m.group(1).strip().split(NL))


taken = {'D228': option('D228', 1), 'D229': option('D229', 1), 'D230': option('D230', 2)}
w = appr[3]
i0, i1 = w.index('D230は'), w.index('私がお伺いしますよ。') + len('私がお伺いしますよ。')
d230_words = w[i0:i1].replace(NL, ' ')
pushed = git('rev-parse', '--short', 'origin/main')
cell = lambda s: str(s).replace('|', '｜')
R = ['# 登録者裁定 D228〜D230（%s・B-lens 層三・器の段の三回目の区切りの後）' % jst(appr[2])[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), w.strip().replace(NL, ' ')),
     '- 裁定の前にコーディネータが示した推奨の段と、同じ返信の「次に進む前のお願い」の段を下に逐語で置く（会話の記録 uuid `%s`・%s 日本時間）。' % (rec[1], jst(rec[2])),
     '- 前提: 器の段の記録 `records/Bl3/tools/tools-log-Bl3.md` の §8「登録者に上げること（三回目の区切り）」（T5・T6・T8。T7・T9 は報告）。', '',
     '| 裁定 | 採られた案（抜き書きから機械で切り出した・字下げの改行は空白にした） |', '|---|---|',
     '| D228 | 一つ目の案（ご推奨どおり）: %s |' % cell(taken['D228']),
     '| D229 | 一つ目の案（ご推奨どおり）: %s |' % cell(taken['D229']),
     '| D230 | 二つ目の案の方向: %s ／ 登録者の言葉の形（逐語）:「%s」 |' % (cell(taken['D230']), cell(d230_words)), '',
     '## 裁定の前にコーディネータが示した推奨（抜き書き・逐語）', '', '````text', excerpt, '````', '',
     '## 同じ返信の「次に進む前のお願い」（逐語）', '', '````text', ask, '````', '',
     '## 注（事実のみ）', '',
     '- 同じ言葉で、登録者は三つのコミット（0546a80・b354548・0bfc0c2）の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- D228 と D229 の中身は、器の段の三回目の区切りで既に器に入っている（凍結の本文の器 `tools/make_frozen_Bl3.py`・報告の組み立ての器 `tools/build_report_Bl3.py`）。',
     '- D230 は、正本 `review_plan` の巡には数えない意見伺いで、依頼文とバンドルはコーディネータが用意し、登録者が系統外（Gemini）二名と claude.ai の Claude Opus 5.5 二名に伺う。'
     '返ってきた意見は逐語で保全し、コーディネータが採否の案を組み、登録者が裁定する。claude.ai の二名はコーディネータと同じ系列で、何名でも一票に数える（裁定 D59 の数え方）。',
     '- 記帳の置き場: 正本の `decisions` への D228〜D230 の記帳は、下見の前の凍結の正本で行う（D226・D227 と同じ）。',
     '- 番号: 次の裁定は D231 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| recommendation', jst(rec[2]), rec[1], '| origin/main', pushed)
