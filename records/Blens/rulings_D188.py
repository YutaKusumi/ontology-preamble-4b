# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D188 の記録を書き、凍結の後の逸脱 D-BL1 を凍結の記録の逸脱台帳に記す（封印の器の直し・2026-09-24）。
登録者の言葉と、裁定の前にコーディネータが示した案は、会話の記録から機械で切り出す。直す前後の器の SHA16・差・自己検査の出力・直す前の器が新しい場合で止まること・
コーディネータの予想の下書きの SHA-256 が裁定の前にチャットで伝えた値と同じことを、機械で取って確かめる。数と SHA は手で打たない。既にある記録には書かない。
用法: python records/Blens/rulings_D188.py <会話の記録 jsonl> <コーディネータの予想の下書き（封印の器に渡す値の JSON）>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, difflib, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
FREEZE_COMMIT = '5eb187b'
TOOL = 'tools/seal_Blens.py'
OUT = os.path.join(HERE, 'rulings-D188.md')
FR_JSON = os.path.join(HERE, 'FREEZE-RECORD-Blens.json')
FR_MD = os.path.join(HERE, 'FREEZE-RECORD-Blens.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
transcript, draft = sys.argv[1], sys.argv[2]
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
show = lambda c, rel: subprocess.run(['git', 'show', '%s:%s' % (c, rel)], cwd=REPO, capture_output=True, check=True).stdout
env = dict(os.environ, PYTHONIOENCODING='utf-8')

# ---- 会話の記録から: 登録者の言葉と、コーディネータが示した案
words = opts = None
for line in open(transcript, encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    t = o.get('type')
    if t not in ('user', 'assistant'):
        continue
    c = (o.get('message') or {}).get('content')
    texts = [c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']
    for s in texts:
        if t == 'user' and len(s) < 600 and '封印の器' in s and '甲でお願いします' in s:
            words = (s.strip(), o.get('uuid'), o.get('timestamp'))
        if t == 'assistant' and 'D-BL1' in s and '甲（推奨）' in s and '封印の器' in s:
            opts = (s, o.get('uuid'), o.get('timestamp'))
assert words and opts, '会話の記録から言葉か案が見つからない'
assert opts[2] < words[2], '案が裁定より後にある'

# ---- 予想の下書きの SHA-256 が、裁定の前にチャットで伝えた値と同じ
announced = re.findall(r'SHA-256 は `([0-9a-f]{64})`', opts[0])
assert len(announced) == 1, announced
draft_sha = sha256b(open(draft, 'rb').read())
assert draft_sha == announced[0].upper(), ('予想の下書きが、チャットで伝えた後に変わっている', draft_sha, announced[0])

# ---- 直す前後の器・差・自己検査
before_b = show(FREEZE_COMMIT, TOOL)
after_b = open(os.path.join(REPO, *TOOL.split('/')), 'rb').read()
FR = json.load(open(FR_JSON, encoding='utf-8'))
assert FR['frozen_sha16'][TOOL] == s16b(before_b), '凍結の記録の SHA16 と凍結のコミットの器が違う'
diff = list(difflib.unified_diff(before_b.decode('utf-8').split(NL), after_b.decode('utf-8').replace('\r\n', NL).split(NL),
                                 '%s（凍結・%s）' % (TOOL, FREEZE_COMMIT), '%s（逸脱 D-BL1 の後）' % TOOL, n=1, lineterm=''))
st = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'seal_Blens.py'), '--selftest'], cwd=REPO, capture_output=True, text=True, encoding='utf-8', env=env)
assert st.returncode == 0, st.stderr[-800:]
selftest_line = [l for l in st.stdout.splitlines() if '自己検査 OK' in l][-1]
MUT = r'''
import sys, json, importlib.util
sys.path.insert(0, sys.argv[2])
spec = importlib.util.spec_from_file_location('seal_v1', sys.argv[1]); S1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(S1)
import make_predictions_form_Blens as FORM
T, keys, opts, M = S1.form_spec()
vals = {k: opts[k][0] for k in opts}
for p, fs in FORM.FIELDS:
    for k, o, _ in fs:
        if k.endswith('.label'):
            vals[k] = '両方'
vals.update({'who': 'コーディネータ', 'info.coi': 'x', 'free': '', 'date': '2026-09-24'})
v4 = dict(vals)
for fam in ('survival', 'nuclear'):
    v4['p1.%s.label' % fam], v4['p1.%s.dir' % fam] = '付かない', FORM.NP
v5 = {k: FORM.NP for k in FORM.prediction_keys()}
v5.update({'p1.survival.label': '両方', 'p1.survival.dir': '反対', 'p6.gate': '通らない', 'info.read_votes': '一部', 'info.read_facts': '見た', 'who': '登録者', 'info.coi': '', 'free': '', 'date': '2026-09-24'})
out = {}
for name, v, role, full in (('coordinator', v4, 'coordinator', True), ('registrant', v5, 'registrant', False)):
    try:
        S1.validate(v, keys, opts, role, full=full); out[name] = 'passed'
    except SystemExit as e:
        out[name] = 'stopped: ' + str(e)
print(json.dumps(out, ensure_ascii=False))
'''
with tempfile.TemporaryDirectory() as td:
    v1 = os.path.join(td, 'seal_Blens_v1.py')
    open(v1, 'wb').write(before_b)
    mp = os.path.join(td, 'mut.py')
    open(mp, 'w', encoding='utf-8').write(MUT)
    mr = subprocess.run([sys.executable, mp, v1, os.path.join(REPO, 'tools')], cwd=REPO, capture_output=True, text=True, encoding='utf-8', env=env)
    assert mr.returncode == 0, mr.stderr[-800:]
    mut = json.loads(mr.stdout.strip().splitlines()[-1])
assert all(v.startswith('stopped: 書式に無い選択肢') for v in mut.values()), mut

# ---- 逸脱台帳（凍結の記録の JSON と md）
approval = '登録者裁定 D188（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」）' % (jst(words[2]), words[1], words[0].replace(NL, ' '))
what = ('**封印の器の直し**。凍結した封印の器 `%s`（v1・SHA16 %s）は、書式のボタンから選んでよい値の一覧を作るが、書式の「予想しない」はボタンでなく予想の欄の初めの値なので、'
        'どの欄の「予想しない」も止めていた。設計は、札が「付かない」の項目の向きの欄を「予想しない」のままにするよう求め、書式は選ばなかった欄に「予想しない」を書き出すので、'
        'コーディネータの封印も、選ばない欄のある登録者の封印も通らなかった（コーディネータの封印で見つけた・何も書かれていない）。v1 の自己検査は止まるべき場合を試していたが、別の理由で止まっていた。'
        '直した器 v2（SHA16 %s）は、予想の欄に限って「予想しない」を受ける。ほかの確かめ（鍵・予想者の欄・コーディネータの予想が埋まっているか）は変えない。'
        '自己検査に、通るべき場合・選ばない欄のある登録者の JSON・正しい理由で止まる場合・一時の置き場での端から端までの封印を足した（v1 は足した二つの場合で止まることを確かめた）。'
        '記録 `records/Blens/rulings-D188.md`') % (TOOL, s16b(before_b), s16b(after_b))
scope = '封印の手続きだけ（予想の項目・予想の書式・正本・語の集合・層一と層二の器・凍結の本文は変えない）'
dev = {'no': 'D-BL1', 'date': jst(words[2]).split(' ')[0], 'what': what, 'scope': scope, 'approval': approval,
       'files': [{'path': TOOL, 'sha16_frozen': s16b(before_b), 'sha16_after': s16b(after_b)}]}
if any(d.get('no') == 'D-BL1' for d in FR.get('deviations', [])):
    raise SystemExit('D-BL1 は凍結の記録に既にある')
FR.setdefault('deviations', []).append(dev)
json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = open(FR_MD, encoding='utf-8').read()
assert '## 逸脱台帳' not in md and 'D-BL1' not in md
clause = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
cut = md.rindex(clause)
ledger = ['## 逸脱台帳', '', '- ' + FR['deviation_rule'] + '。黙って直すことは、正しく直すことより悪い（記帳のない変更を禁じる）。', '',
          '| 番号 | 日付 | 何を・なぜ | 射程 | 承認 |', '|---|---|---|---|---|',
          '| %s | %s | %s | %s | %s |' % (dev['no'], dev['date'], dev['what'].replace('|', '｜'), dev['scope'], dev['approval'].replace('|', '｜')), '', '']
open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md[:cut] + NL.join(ledger) + md[cut:])

# ---- 裁定の記録
R = ['# 登録者裁定 D188（2026-09-24・凍結の後の逸脱 D-BL1・封印の器の直し）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (words[1], jst(words[2]), words[0].replace(NL, ' ')), '',
     '| 裁定 | 中身 |', '|---|---|',
     '| D188 | 封印の器 `%s` を最小限だけ直す（予想の欄に限って「予想しない」を受ける・ほかの確かめは変えない・自己検査に見逃した場合を足す）。凍結の後の逸脱 D-BL1 として、凍結の記録の逸脱台帳に記す（下の「甲」）。 |' % TOOL, '',
     '## 裁定の前にコーディネータが示した案（逐語・会話の記録 uuid `%s`・%s 日本時間）' % (opts[1], jst(opts[2])), '',
     '````text', opts[0].rstrip(), '````', '',
     '## 直したもの（機械で取った差）', '',
     '- `%s`: SHA16 %s（凍結・コミット %s・凍結の記録の値と同じ）→ %s。' % (TOOL, s16b(before_b), FREEZE_COMMIT, s16b(after_b)),
     '- 直した器の自己検査の出力: 「%s」。' % selftest_line,
     '- 直す前の器（v1）に、自己検査に足した二つの場合を通した結果: コーディネータの予想（札が「付かない」の項目の向きの欄が「予想しない」）は「%s」・選ばない欄のある登録者の JSON は「%s」。'
     % (mut['coordinator'], mut['registrant']),
     '- 凍結の記録 `records/Blens/FREEZE-RECORD-Blens.json` に `deviations`（D-BL1）を足し、`records/Blens/FREEZE-RECORD-Blens.md` に逸脱台帳の節を足した。凍結物の SHA16 の一覧（`frozen_sha16`）は凍結の時の値のまま残す。',
     '', '````diff'] + diff + ['````', '',
     '## 注（事実のみ）', '',
     '- コーディネータの予想の下書き（封印の器に渡す値の JSON）の SHA-256 は %s で、裁定の前にチャットで伝えた値と同じ（器で突き合わせた）。この下書きをそのまま封印の器に渡す。' % draft_sha,
     '- 層一の器が射影の前に確かめる凍結物（正本・語の集合・層一の器と芯）に、封印の器は入っていない。',
     '- 登録者の予想の JSON は作り直さなくてよい（書式は変わっていない）。',
     '- 次: コミット → コーディネータの封印（SHA だけを伝える）→ 登録者の封印 → 封印の記録 → push の許可。番号: 次の裁定は D189 から。', '',
     '## 検分票', '',
     '- 対象: 封印の器の直し（逸脱 D-BL1）と、その記帳。',
     '- 段階: 凍結の後・封印の前（射影は一つも計算していない）。',
     '- 凍結物の同定: 凍結の記録 `records/Blens/FREEZE-RECORD-Blens.json` の `tools/seal_Blens.py` の SHA16 が、凍結のコミット %s の器と同じことを確かめてから直した。' % FREEZE_COMMIT,
     '- 盲検の状態: 該当しない（手続きの器）。',
     '- 敵対的検分: 直した器が、書式に無い値（予想の欄の外の「予想しない」を含む）をなお止めることを自己検査で確かめた。自己検査に足した場合で、直す前の器が止まり、直した器が通ることを確かめた（足した検査が穴を捕まえる）。',
     '- 系統の内訳: コーディネータ（Claude 系）だけで直した。外の目は通っていない。',
     '- COI記録: コーディネータは封印へ進む側に引かれている。直しは受ける値を広げる向きなので、受けるのを「予想しない」だけ・予想の欄だけに限り、ほかの確かめは一つも外していない。',
     '- 判定: 登録者の裁定どおりに直した。',
     '- 本検分が確認していないこと: 書式の中の JS が書き出す JSON と、封印の器が書く JSON の形の一致は、書式を作ったときの確かめ（器の自己検査）に依る（今回の直しは形に触れていない）。登録者の JSON が実際に通ることは、登録者の封印のときに確かめる。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', OUT, '|', jst(words[2]), words[1], '| draft', draft_sha[:16], '| tool', s16b(before_b), '->', s16b(after_b), '| mut', mut)
