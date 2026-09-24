# -*- coding: utf-8 -*-
"""B-lens の登録者最終確認と登録者裁定 D198・D199 を記録し、最終版を組み直し、逸脱 D-BL3 の二つ目の更新（組み立ての器 v3）を台帳に記す（2026-09-24）。
登録者の言葉と、裁定の前にコーディネータが示した案は、会話の記録から機械で切り出す（手で打たない）。器と出力の SHA16 は器が計算する。
順: 登録者が確かめた案（置き場の最終版のファイル）の SHA16 を記録 → 確認の記録を書く → 最終版を組み直す → 案との違いが状態の一行だけであることを確かめる →
    草案の二つ目が変わらないことを確かめる → 台帳に記す → 台帳に記した後も最終版が変わらないことを確かめる → 裁定の記録を書く。既にある記録には書かない。
用法: python records/Blens/rulings_D198_D199.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
P = lambda r: os.path.join(REPO, *r.split('/'))
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16 = lambda r: s16b(open(P(r), 'rb').read())
OUT = os.path.join(HERE, 'rulings-D198-D199.md')
CONFIRM = 'records/Blens/final-confirmation-Blens.json'
FR_JSON, FR_MD = os.path.join(HERE, 'FREEZE-RECORD-Blens.json'), os.path.join(HERE, 'FREEZE-RECORD-Blens.md')
BUILDER = 'tools/build_report_Blens_devBL3.py'
FINAL = 'records/Blens/results-Blens-FINAL-2026-09-24.md'
REVIEW = 'records/reviews/Blens/results-final/final-read/review-final-Blens.md'
PROPOSAL_REPORTED = '122BC016BA5D737A'                   # 登録者に示した案の SHA16（コーディネータの報告の値・器の値と突き合わせる）
for p in (OUT, P(CONFIRM)):
    assert not os.path.exists(p), '既にある: ' + p
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
env = dict(os.environ, PYTHONIOENCODING='utf-8')


def build(args):
    r = subprocess.run([sys.executable, P(BUILDER)] + args, cwd=REPO, capture_output=True, env=env)
    out = r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')
    if r.returncode != 0 or '走査の違反 0' not in out:
        raise SystemExit('組み立ての器が止まった（止める）: %s %s' % (args, out.strip()[-300:]))
    return out


MSGS = []
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
conf = [m for m in MSGS if m[0] == 'user' and len(m[3]) < 800 and '登録者最終確認を行いました' in m[3] and 'ご推奨の案を全て承認' in m[3]]
assert len(conf) == 1, len(conf)
conf = conf[0]
opts = [m for m in MSGS if m[0] == 'assistant' and '**D198**' in m[3] and '**D199**' in m[3] and '**D200**' in m[3] and m[2] < conf[2]]
assert opts, '裁定の前の案が見つからない'
opts = opts[-1]
words = conf[3].strip().replace(NL, ' ')
approval = lambda d: '登録者裁定 %s（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」）' % (d, jst(conf[2]), conf[1], words)
day = jst(conf[2]).split(' ')[0]
push_ins = [m for m in MSGS if m[0] == 'user' and len(m[3]) < 800 and '最終版の見直しを' in m[3] and m[2] < conf[2]]
assert len(push_ins) == 1, len(push_ins)
prev = re.search(r'`%s` の (\w+) の版（' % re.escape(FINAL), open(P(REVIEW), encoding='utf-8').read()).group(1)
assert ('%s の push' % prev) in push_ins[0][3], '見直しの記録の版と、push の指示の版が違う'
Q_ALL = 'ご推奨の案を全て承認します'
assert Q_ALL in words

# 1) 登録者が確かめた案
prop = open(P(FINAL), 'rb').read().replace(b'\r\n', b'\n')
prop_sha = s16b(prop)
assert prop_sha == PROPOSAL_REPORTED, ('置き場の最終版が、登録者に示した案と違う（止める）', prop_sha)
out0 = build(['--final'])
assert '既にある出力と同じ（書かない）' in out0, '確認の記録の前の器が、案を作り直せない（止める）'
# 2) 確認の記録
CF = {'kind': 'blens_final_confirmation', 'uuid': conf[1], 'jst': jst(conf[2]), 'words': words, 'proposal_sha16': prop_sha, 'proposal_path': FINAL,
      'source': '登録者の発言（会話の記録から機械で切り出した）', 'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(CF, open(P(CONFIRM), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
# 3) 最終版を組み直す
build(['--final', '--force'])
new = open(P(FINAL), 'rb').read().replace(b'\r\n', b'\n')
pl, nl_ = prop.decode('utf-8').split(NL), new.decode('utf-8').split(NL)
diff = [i for i in range(max(len(pl), len(nl_))) if i >= len(pl) or i >= len(nl_) or pl[i] != nl_[i]]
if len(pl) != len(nl_) or len(diff) != 1 or not pl[diff[0]].startswith('- 状態: ') or words not in nl_[diff[0]] or prop_sha not in nl_[diff[0]]:
    raise SystemExit('組み直した最終版と案の違いが、状態の一行だけでない（止める）: %s' % diff)
status_line_no = diff[0] + 1
# 4) 草案の二つ目は変わらない
assert '既にある出力と同じ（書かない）' in build([]), '草案の二つ目が変わった（止める）'
# 5) 台帳
FR = json.load(open(FR_JSON, encoding='utf-8'))
d3 = [d for d in FR['deviations'] if d['no'] == 'D-BL3'][0]
assert len(d3.get('updates', [])) == 1, '台帳の D-BL3 の更新の数が想定と違う'
v2 = [f['sha16_v2'] for f in d3['updates'][0]['files'] if f['path'] == BUILDER][0]
assert v2 != s16(BUILDER), '器が v2 のまま'
lint_n = int(re.search(r'- 違反 (\d+)', open(P(FINAL.replace('.md', '-lint.md')), encoding='utf-8').read()).group(1))
assert lint_n == 0
upd = {'date': day,
       'what': ('**報告の最終版の組み立て（器 v3）**。起草者の最終の見直し（`%s`）の所見 F-A〜F-F を受け、逸脱の下の器 `%s` を v3（SHA16 %s・v2 は SHA16 %s）に改めた。'
                '状態を機械の区画に移し、登録者最終確認の記録 `%s` から確認の逐語と時刻と、確かめた案の SHA16 を書く（F-A）。冒頭の凍結の後の逸脱の一覧（台帳から読む）と検分票の D-BL2 の一句（F-B）・'
                '§3 の答えの文字の位置の二つの行の言い回し（F-C・F-C2）・検分票の区画の頭の添え（F-D）・§3 の並べ直しの表の見出しの理由の句（F-E）・§0 の〈門を通らない〉の添え（F-F）。'
                '最終版 `%s`（SHA16 %s・走査の違反 %d）は、登録者が確かめた案（SHA16 %s）と状態の一行（%d 行目）のほか同じ（器が確かめた）。草案の二つ目の出力は v1・v2 と同じ')
               % (REVIEW, BUILDER, s16(BUILDER), v2, CONFIRM, FINAL, s16(FINAL), lint_n, prop_sha, status_line_no),
       'scope': '報告の表し方だけ（札・門・大きさの目盛りの判定と、凍結した器の出力と、草案の二つ目は変えない）',
       'approval': approval('D198'),
       'files': [{'path': BUILDER, 'sha16_v2': v2, 'sha16_v3': s16(BUILDER)}] + [{'path': p_, 'sha16': s16(p_)} for p_ in (FINAL, FINAL.replace('.md', '-machine.json'), FINAL.replace('.md', '-lint.md'), CONFIRM)]}
d3['updates'].append(upd)
json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = open(FR_MD, encoding='utf-8').read()
a = [l for l in md.split(NL) if l.startswith('| D-BL3（更新・器 v2） |')]
assert len(a) == 1
cell = lambda s: s.replace('|', '｜')
md = md.replace(a[0], a[0] + NL + '| D-BL3（更新・器 v3） | %s | %s | %s | %s |' % (upd['date'], cell(upd['what']), upd['scope'], cell(upd['approval'])), 1)
open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md)
# 6) 台帳に記した後も最終版は変わらない
assert '既にある出力と同じ（書かない）' in build(['--final']), '台帳に記した後、最終版が変わった（止める）'
# 7) 裁定の記録
RUL = [('D198', '起草者の最終の見直し（`%s`）の所見のうち、F-A〜F-D と任意の F-E・F-F を、逸脱の下の組み立ての器 v3（D-BL3 の二つ目の更新）で最終版に入れる。F-G は記録だけ。台帳の D-BL3 に v3 の器と最終版を足す' % REVIEW),
       ('D199', '%s の版は、登録者の指示（会話の記録 uuid `%s`・%s 日本時間）で、登録者最終確認の前に push した。これで裁定 D197 の順（確かめの後に push）を登録者が改めた。'
                '登録者最終確認の後に、確認の逐語と時刻を最終版の状態の区画に入れて組み直し、その版をもって公開を終える（段階 B の最終版の型）' % (prev, push_ins[0][1], jst(push_ins[0][2])))]
R = ['# 登録者最終確認と登録者裁定 D198・D199（2026-09-24・起草者の最終の見直しの後）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (conf[1], jst(conf[2]), words), '',
     '| 裁定 | 中身 |', '|---|---|'] + ['| %s | %s |' % kv for kv in RUL] + [
     '', '## 確認の記録（`%s`）' % CONFIRM, '',
     '- 登録者が確かめた案: `%s`（SHA16 %s・コーディネータが示した案の値と一致）。' % (FINAL, prop_sha),
     '- 組み直した最終版: SHA16 %s・走査の違反 %d。案との違いは状態の一行（%d 行目）だけ（器が確かめた）。草案の二つ目は変わらない（器が確かめた）。' % (s16(FINAL), lint_n, status_line_no), '',
     '## 裁定の前にコーディネータが示した案（逐語・会話の記録 uuid `%s`・%s 日本時間）' % (opts[1], jst(opts[2])), '', '````text', opts[3].rstrip(), '````', '',
     '## 注（事実のみ）', '',
     '- 案の D200（README の案内の一行と、公開の後のタグ）には、コーディネータが推奨を書いていなかった。登録者の「%s」が D200 に及ぶかは、push の許可を伺うときに登録者に確かめ、その裁定は別の記録に書く。' % Q_ALL,
     '- 逸脱 D-BL3 の二つ目の更新（器 v3・最終版）を、凍結の記録の逸脱台帳に記した。台帳に記した後も、最終版は変わらない（器が確かめた）。',
     '- 番号: 次の裁定は D200 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '|', jst(conf[2]), conf[1], '| options', jst(opts[2]), opts[1], '| proposal', prop_sha, '| FINAL', s16(FINAL), 'status line', status_line_no, '| builder v3', s16(BUILDER), 'v2', v2)
