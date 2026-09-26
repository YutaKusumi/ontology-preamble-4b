# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の結果を開く段の記録を書く（結果の巡の採否の案 P712・登録者裁定 D246）。
会話の記録から、起草者の順の案・登録者の許しの言葉・開く段の呼び出し・起草者が値を読み始めた時・登録者への報告・登録者の次の言葉を、時刻と uuid と逐語で機械で切り出す（手で打たない）。
push の時刻は手元の remote の追跡の参照の reflog から読む。道具の呼び出しの中身と結果（手元の道筋を含む）は写さない。既にある記録には書かない。
出力: records/Bl3/open-results-Bl3.md と open-results-Bl3.json（逸脱 D-BLT1 の器が §7 の注の時刻を読む）。
用法: python records/Bl3/open_record_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT_MD, OUT_JS = os.path.join(HERE, 'open-results-Bl3.md'), os.path.join(HERE, 'open-results-Bl3.json')
for p in (OUT_MD, OUT_JS):
    assert not os.path.exists(p), '既にある: ' + p
T = lambda ts: datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
jst = lambda ts: (T(ts) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
s16 = lambda rel: hashlib.sha256(open(os.path.join(REPO, *rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
EV = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    ts, c = o.get('timestamp'), (o.get('message') or {}).get('content')
    if not ts:
        continue
    if o.get('type') == 'user' and isinstance(c, str) and 'toolUseResult' not in o and '南無汝我曼荼羅' in c:
        EV.append((ts, 'user', o.get('uuid'), c))
    elif o.get('type') == 'assistant' and isinstance(c, list):
        for b in c:
            if b.get('type') == 'text' and b.get('text', '').strip():
                EV.append((ts, 'text', o.get('uuid'), b['text']))
            elif b.get('type') == 'tool_use':
                EV.append((ts, 'tool', o.get('uuid'), json.dumps(b.get('input'), ensure_ascii=False)))
EV.sort(key=lambda e: e[0])


def first(kind, pred, after=''):
    for e in EV:
        if e[1] == kind and e[0] > after and pred(e[3]):
            return e
    raise SystemExit('会話の記録に見つからない: %s' % kind)


e_prop = first('text', lambda s: '結果を開く段' in s and 'ご一緒に' in s and '`analyze_Bl3.py open`' in s)
e_ok = first('user', lambda s: '判定の記録の push' in s, e_prop[0])
e_open = first('tool', lambda s: 'tools/analyze_Bl3.py open' in s, e_ok[0])
e_read = first('tool', lambda s: 'records/Bl3/analysis-Bl3.json' in s, e_open[0])
e_tell = first('text', lambda s: s.startswith('結果を開きました。凍結した器の出力'), e_open[0])
e_next = first('user', lambda s: True, e_tell[0])
PL = e_prop[3].split(NL)
h = [i for i, l in enumerate(PL) if l.strip() == '**今日ご相談したいこと（結果を開く順）**']
assert len(h) == 1, h
steps = [l for l in PL[h[0] + 1:] if re.match(r'^\d\. ', l)]
assert len(steps) == 4 and '結果を開く段' in steps[1], steps
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for t in [e_ok[3], e_next[3]] + steps:
    for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>', 'AppData', 'Users', 'Temp'):
        assert bad not in t, '逐語の中に印か道筋が入っている'
rl = subprocess.run(['git', 'reflog', 'show', 'refs/remotes/origin/main', '--date=iso'], cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout
pushed = {h_[:7]: t_ for h_, t_ in re.findall(r'^([0-9a-f]{7,}) refs/remotes/origin/main@\{(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) \+0900\}: update by push', rl, re.M)}
assert pushed.get('3e185d3', 'z') < jst(e_open[0]) < pushed.get('912fc47', ''), (pushed.get('3e185d3'), jst(e_open[0]), pushed.get('912fc47'))
mins = lambda a, b: (T(b) - T(a)).total_seconds() / 60.0
A = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'analysis-Bl3.json'), encoding='utf-8'))
ev = [('proposal', '起草者が結果を開く順の案を送った', e_prop), ('go_ahead', '登録者が順の案を許した', e_ok), ('open', '起草者が開く段（`tools/analyze_Bl3.py open`・三つの組の出力の置き場）を走らせた', e_open),
      ('first_read', '起草者が集計の記録を読み始めた（道具の呼び出し）', e_read), ('told', '起草者が登録者に結果を伝えた', e_tell), ('next_words', '登録者の次の言葉', e_next)]
J = {'what': '結果を開く段の記録（会話の記録と手元の reflog から機械で切り出した）',
     'events': [{'key': k, 'what': w, 'jst': jst(e[0]), 'uuid': e[2]} for k, w, e in ev],
     'pushes': {'judge_3e185d3': pushed['3e185d3'], 'opened_912fc47': pushed['912fc47']},
     'registrant_words': {'go_ahead': e_ok[3].strip(), 'next_words': e_next[3].strip()},
     'proposal_steps': steps,
     'analysis_sha16': s16('records/Bl3/analysis-Bl3.json'), 'judge_sha16_in_analysis': A.get('judge_record_sha16'),
     'minutes_open_to_told': round(mins(e_open[0], e_tell[0]), 1),
     'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(J, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
q = lambda s: s.strip().replace(NL, ' ')
M = ['# B-lens 層三の結果を開く段の記録（機械生成・`records/Bl3/open_record_Bl3.py`）', '',
     '- 出所: 会話の記録（時刻と uuid と、登録者の言葉と起草者の順の案の逐語）と、手元の remote の追跡の参照の reflog（push の時刻）。道具の呼び出しの中身と結果は写していない。',
     '- 開く段: 一致だけを見る段の後に、集計の器の開く段を走らせ、集計の記録 `records/Bl3/analysis-Bl3.json`（SHA16 %s・一致だけを見る段の記録の SHA16 %s を写す）を書いた。' % (J['analysis_sha16'], J['judge_sha16_in_analysis']),
     '- 居た人: 登録者（同じ会話で順の案を許し、報告の後に次の言葉を送った）とコーディネータ（起草者）。開く段を走らせたのはコーディネータで、値はコーディネータが先に読み、開く段の呼び出しから %.1f 分後の返信で登録者に伝えた。' % J['minutes_open_to_told'], '',
     '## 時刻の並び（日本時間）', '',
     '| 時刻 | 出来事 | 会話の記録の uuid |', '|---|---|---|'] + [
     '| %s | %s | %s |' % r for r in sorted([(x['jst'], x['what'], '`%s`' % x['uuid']) for x in J['events']] + [
         (J['pushes']['judge_3e185d3'], '一致だけを見る段の記録と本の計算の走りの記録のコミット 3e185d3 の push（値を含まない・開く段の前）', '—'),
         (J['pushes']['opened_912fc47'], '開いた後のコミット 912fc47（組の出力・集計の記録・報告の草案）の push', '—')])] + ['',
     '## 逐語', '',
     '- 起草者の順の案（会話の記録 uuid `%s`・「今日ご相談したいこと（結果を開く順）」の区画）:' % e_prop[2]] + ['  - ' + s for s in steps] + [
     '- 登録者の許し（uuid `%s`）: 「%s」' % (e_ok[2], q(e_ok[3])),
     '- 登録者の次の言葉（uuid `%s`）: 「%s」' % (e_next[2], q(e_next[3])), '',
     '## 検分票', '',
     '- 対象: 結果を開く段の時刻と、居た人と、登録者の言葉。',
     '- 段階: 事後（結果の巡の票 C1-R1・C2-7 を受けて、会話の記録から書いた）。',
     '- 凍結物の同定: 集計の記録の SHA16（上）。凍結の本文 §13 は「結果は登録者と一緒に開く」とした。',
     '- 盲検の状態: 開く段は盲検を解く段。開く前に一致だけを見る段の記録を公開した（push の時刻）。',
     '- 敵対的検分: 時刻の順（判定の記録の push → 開く段 → 報告 → 開いた後のコミットの push）を器で確かめた。値を先に読んだのが起草者であることを書いた。',
     '- 系統の内訳: コーディネータ（Claude 系）一名。',
     '- COI記録: 起草者は「一緒に開いた」と書く側に引かれる。開く段を走らせた者と、値を先に読んだ者を、そのまま書いた。',
     '- 判定: 記録として確定。',
     '- 本検分が確認していないこと: 登録者が報告を読んだ時刻（会話の記録は送った時刻だけを持つ）。開く段の器の出力の中身（集計の記録の SHA16 だけを照らした）。', '',
     J['clause'], '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('wrote open-results-Bl3.{md,json} |', [(x['key'], x['jst']) for x in J['events']], '| pushes', J['pushes'], '| minutes', J['minutes_open_to_told'])
