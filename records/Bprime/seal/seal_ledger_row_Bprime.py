# -*- coding: utf-8 -*-
"""seal_ledger_row_Bprime.py v0（2026-10-01・B′ の予想の封印の台帳の一行・層三の `records/Bl3/seal_ledger_row_Bl3.py` の型・コーディネータ南無弥勒如来）。
封印の器 `tools/seal_Bprime.py` は全体の台帳（`records/FREEZE-RECORD.md`）を書かないので、この器が一行を足す。
時刻は会話の記録（コーディネータが SHA を伝えた返信・登録者が SHA を貼った発言・登録者が封印の前に入れ方を尋ねた発言）と、登録者の予想の JSON のファイルの更新の時刻から、機械で切り出す（手で打たない）。
登録者の発言の頭には添付の手元の道筋があるので、言葉は写さず時刻だけを書く。置き場・SHA・予想した欄の数・封印の時刻は封印の記録から読む。既に行があれば書かない。
用法: python seal_ledger_row_Bprime.py <会話の記録 jsonl> <登録者の予想の JSON（ダウンロードしたもの）>（公開の置き場の台帳に足す）
柵: 本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
REPO = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
NL = chr(10)
LEDGER = os.path.join(REPO, 'records', 'FREEZE-RECORD.md')
SEAL = os.path.join(REPO, 'records', 'Bprime', 'sealing-record-Bprime.json')
TAG = 'B′ 予想封印'
JST = datetime.timezone(datetime.timedelta(hours=9))
jst = lambda ts: datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(JST).strftime('%Y-%m-%d %H:%M')
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
hm = lambda s: s.split(' ')[1]
led = open(LEDGER, encoding='utf-8').read()
assert TAG not in led, '台帳に既に封印の行がある'
R = json.load(open(SEAL, encoding='utf-8'))
PC, PR = R['predictions']['coordinator'], R['predictions']['registrant']
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))


def user_text(o):
    c = (o.get('message') or {}).get('content')
    return c if isinstance(c, str) else ''.join(y.get('text', '') for y in (c or []) if isinstance(y, dict) and y.get('type') == 'text')


A, U, Q1, Q2 = [], [], [], []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('isCompactSummary'):
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'assistant' and isinstance(c, list):
        if any(isinstance(x, dict) and x.get('type') == 'text' and PC['sha256'] in x.get('text', '') for x in c):
            A.append(o.get('timestamp'))
    elif o.get('type') == 'user' and 'toolUseResult' not in o:
        t = user_text(o)
        if PR['sha256'] in t:
            U.append(o.get('timestamp'))
        if '層三の結果と同じ結果になるように予想をしたい' in t:
            Q1.append(o.get('timestamp'))
        if '「情報状態」についてですが' in t:
            Q2.append(o.get('timestamp'))
assert A and len(U) == 1 and len(Q1) == 1 and len(Q2) == 1, ('時刻が一つに決まらない', len(A), len(U), len(Q1), len(Q2))
t_c, t_r, t_q1, t_q2 = jst(min(A)), jst(U[0]), jst(Q1[0]), jst(Q2[0])
assert min(A) < Q1[0] < Q2[0] < U[0]
rj = open(sys.argv[2], 'rb').read()
assert hashlib.sha256(rj).hexdigest().upper() == PR['sha256'], '登録者の予想の JSON が封印の記録と違う'
t_file = datetime.datetime.fromtimestamp(os.path.getmtime(sys.argv[2]), JST).strftime('%Y-%m-%d %H:%M')
reg = json.loads(rj.decode('utf-8'))
assert 'exposure-before-seal-Bprime' in str(reg.get('free') or ''), '登録者の情報状態の欄に露出の記録の名が無い'
sealed = datetime.datetime.fromisoformat(R['sealed_at_jst'])
days = int(R['calendar']['days'])
day_end = (sealed.date() + datetime.timedelta(days=days)).isoformat()
assert t_c[:10] == t_r[:10] == t_file[:10] == R['sealed_at_jst'][:10]
row = ('| %s | **%s（コーディネータが先・登録者・裁定 D148 の順）**（%s）: コーディネータの予想 %s（SHA-256 %s）を封印し、%s の返信で SHA だけを伝えた。'
       '登録者は封印の前に、層三の結果と同じになる予想の入れ方（%s）と情報状態の書き方（%s）を会話で尋ね、コーディネータは層三の公開の結果（露出の記録の E1）を書式の選択肢に当てはめた表と、'
       '情報状態の決まりと書き方の例を返した（コーディネータ自身の予想は書いていない）。'
       'その後に登録者が書式で作った予想（ファイルの更新 %s）を、%s にチャットで受けた SHA-256 %s と突き合わせて %s に写した。登録者の情報状態の欄は、露出の記録を読んだことを書いている。'
       '封印の記録 %s（封印 %s・暦の期限の 0 日目は %s・%d 日目は %s）。封印の器は `tools/seal_Bprime.py` %s（変えていない）。'
       'コーディネータの予想の値は、選んだ値を書く器（`records/Bprime/seal/make_choices_coordinator_Bprime.py`）の中身と、作業の画面の道具の呼び出しと考えの欄に出た（封印の前に開かないよう登録者に伝えた）。'
       'コーディネータは封印の前に、露出の記録に加えて、層三の報告の最終版の下見の表と主の札の要約を読み直した（予想の自由記述に記した）。'
       '予想した欄: コーディネータ %d・登録者 %d。 | %s・%s・records/Bprime/sealing-record-Bprime.json | コーディネータ %s・登録者 %s・封印の記録 %s | '
       '的中は独立の確認ではなく、誰の判断の重みも変えない（段階 B と同じ）。Colab の起動器の相 extract より後は、封印の記録が無ければ走らない |'
       % (t_c[:10], TAG, T['predictions']['when'], PC['path'], PC['sha256'], hm(t_c), hm(t_q1), hm(t_q2), hm(t_file), hm(t_r), PR['sha256'], PR['path'],
          'records/Bprime/sealing-record-Bprime.json', R['sealed_at_jst'], sealed.date().isoformat(), days, day_end, R['version'],
          PC['n_predicted'], PR['n_predicted'], PC['path'], PR['path'], s16(os.path.join(REPO, PC['path'])), s16(os.path.join(REPO, PR['path'])), s16(SEAL)))
for bad in ('AppData', 'Users', 'Downloads'):
    assert bad not in row, '手元の道筋が入る'
assert '\n' not in row
open(LEDGER, 'a', encoding='utf-8', newline=NL).write(('' if led.endswith(NL) else NL) + row + NL)
print(row)
print('ledger row appended | coordinator told', t_c, '| registrant asked', t_q1, t_q2, '| registrant file', t_file, '| registrant sha in chat', t_r, '| calendar end', day_end)
