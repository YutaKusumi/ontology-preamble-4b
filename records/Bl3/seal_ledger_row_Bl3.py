# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の予想の封印の台帳の一行（`records/FREEZE-RECORD.md`）を書く（B-lens の封印の行の型）。封印の器 `tools/seal_Bl3.py` は台帳を書かないので、この器が足す。
時刻は会話の記録（コーディネータが SHA を伝えた返信・登録者が SHA を貼った発言）と、登録者の予想の JSON のファイルの更新の時刻から、機械で切り出す（手で打たない）。
登録者の発言の頭には添付の手元の道筋があるので、言葉は写さず時刻だけを書く。置き場・SHA・予想した欄の数は封印の記録から読む。既に行があれば書かない。
封印の後に登録者が会話で、情報状態の欄に露出の記録の旨を記すよう求めたとき（裁定 D217）は、その言葉を会話の記録から逐語で切り出して行に足す（予想の JSON は変えない）。
用法: python records/Bl3/seal_ledger_row_Bl3.py <会話の記録 jsonl> <登録者の予想の JSON（ダウンロードしたもの）>
柵: 本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
LEDGER = os.path.join(REPO, 'records', 'FREEZE-RECORD.md')
SEAL = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
TAG = 'B-lens 層三 予想封印'
JST = datetime.timezone(datetime.timedelta(hours=9))
jst = lambda ts: datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(JST).strftime('%Y-%m-%d %H:%M')
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
led = open(LEDGER, encoding='utf-8').read()
assert TAG not in led, '台帳に既に封印の行がある'
R = json.load(open(SEAL, encoding='utf-8'))
PC, PR = R['predictions']['coordinator'], R['predictions']['registrant']
A, U = [], []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'assistant' and isinstance(c, list):
        if any(isinstance(x, dict) and x.get('type') == 'text' and PC['sha256'] in x.get('text', '') for x in c):
            A.append(o.get('timestamp'))
    elif o.get('type') == 'user' and 'toolUseResult' not in o:
        t = c if isinstance(c, str) else ''.join(y.get('text', '') for y in (c or []) if isinstance(y, dict) and y.get('type') == 'text')
        if PR['sha256'] in t:
            U.append(o.get('timestamp'))
assert A and len(U) == 1, ('時刻が一つに決まらない', len(A), len(U))
t_c, t_r = jst(min(A)), jst(U[0])
rj = open(sys.argv[2], 'rb').read()
assert hashlib.sha256(rj).hexdigest().upper() == PR['sha256'], '登録者の予想の JSON が封印の記録と違う'
t_file = datetime.datetime.fromtimestamp(os.path.getmtime(sys.argv[2]), JST).strftime('%Y-%m-%d %H:%M')
reg = json.loads(rj.decode('utf-8'))
free_r = str(reg.get('free') or '')
names_exposure = any(x in free_r for x in ('露出', 'exposure-before-seal', 'X1'))
hm = lambda s: s.split(' ')[1]
# 封印の後の登録者の言葉（裁定 D217 の旨・予想の JSON は封印したまま）
W = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str) and '露出の記録 X1〜X4' in c and '記載してください' in c and o.get('timestamp') > U[0]:
        W.append((o.get('timestamp'), c))
assert len(W) <= 1, ('封印の後の言葉が一つに決まらない', len(W))
d217 = ''
if W:
    t_w, c_w = W[0]
    a0, a1 = c_w.find('裁定 D217'), c_w.find('記載してください。')
    assert a0 >= 0 and a1 > a0
    cut = c_w[a0:a1 + len('記載してください。')]
    tg, sr = 'pasted' + '_content', 'system' + '-reminder'
    assert not any(x in cut for x in ('<' + tg, '</' + tg, '<' + sr, sr + '>', 'Users')), '印か手元の道筋が入っている'
    d217 = '封印の後の %s に、登録者は会話で「%s」と書いた（予想の JSON は封印したまま変えていない）。' % (hm(jst(t_w)), cut)
assert t_c[:10] == t_r[:10] == t_file[:10]
row = ('| %s | **%s（コーディネータが先・登録者・裁定 D148 の順）**（下見の前の凍結の後・下見の前・裁定 D210）: コーディネータの予想 %s（SHA-256 %s）を封印し、%s の返信で SHA だけを伝えた。'
       'その後に登録者が書式で作った予想（ファイルの更新 %s）を、%s にチャットで受けた SHA-256 %s と突き合わせて %s に写した。封印の記録 %s。封印の器は `tools/seal_Bl3.py` %s。'
       'コーディネータの予想の値は、封印の台本（道具の呼び出しの中身）に選択肢の番号と考え方の文として出た（封印の前に開かないよう登録者に伝えた）。'
       'コーディネータは封印の前に、正本の情報状態に加えて、段階 B の集計の記録の確証の族の行・段階 B の標本化の設定・B-lens の報告の要約を読み直した（予想の自由記述に記した）。%s'
       '予想した欄: コーディネータ %d・登録者 %d。 | %s・%s・records/Bl3/sealing-record-Bl3.json | コーディネータ %s・登録者 %s・封印の記録 %s | '
       '的中は独立の確認ではなく、誰の判断の重みも変えない（段階 B と同じ）。Colab の起動器の相 pilot と相 main は、封印の記録が無ければ走らない |'
       % (t_c[:10], TAG, PC['path'], PC['sha256'], hm(t_c), hm(t_file), hm(t_r), PR['sha256'], PR['path'], 'records/Bl3/sealing-record-Bl3.json', R['version'],
          '' if names_exposure else '登録者の情報状態の欄は、B-lens 層三に至る一連の検証を承知していると書き、露出の記録の名は挙げていない（露出の記録には、登録者が設計の巡の票を会話に貼るときに X1〜X4 の文を読んだことが書いてある）。' + d217,
          PC['n_predicted'], PR['n_predicted'], PC['path'], PR['path'], s16(os.path.join(REPO, PC['path'])), s16(os.path.join(REPO, PR['path'])), s16(SEAL)))
for bad in ('AppData', 'Users', 'Downloads'):
    assert bad not in row, '手元の道筋が入る'
open(LEDGER, 'a', encoding='utf-8', newline=NL).write(('' if led.endswith(NL) else NL) + row + NL)
print('ledger row appended | coordinator told', t_c, '| registrant file', t_file, '| registrant sha in chat', t_r, '| names exposure record', names_exposure, '| D217 words after the seal', bool(d217))
