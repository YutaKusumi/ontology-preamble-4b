# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D189〜D193 の記録と、封印の前の露出の記録を書き、逸脱 D-BL2（結果の巡の組み立て）を凍結の記録の逸脱台帳に記す（2026-09-24）。
登録者の言葉・申告と、裁定の前にコーディネータが示した案、露出の文は、会話の記録と置き場の記録から機械で切り出す（手で打たない）。
Colab のユニットの数は、登録者の発言から機械で読み、器の記録（JSON）にする（報告の費用の行に使う）。既にある記録には書かない。
用法: python records/Blens/rulings_D189_D193.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D189-D193.md')
EXPO = os.path.join(HERE, 'sealing-exposures-Blens.md')
UNITS = os.path.join(HERE, 'colab-units-Blens.json')
FR_JSON, FR_MD = os.path.join(HERE, 'FREEZE-RECORD-Blens.json'), os.path.join(HERE, 'FREEZE-RECORD-Blens.md')
for p in (OUT, EXPO, UNITS):
    assert not os.path.exists(p), '既にある: ' + p
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
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
        elif x.get('type') == 'tool_result':
            cc = x.get('content')
            MSGS.append(('tool_result', o.get('uuid'), o.get('timestamp'), cc if isinstance(cc, str) else ' '.join(y.get('text', '') for y in (cc or []) if isinstance(y, dict))))
ruling = [m for m in MSGS if m[0] == 'user' and len(m[3]) < 800 and 'ご推奨の案を承認' in m[3] and '629.98' in m[3]]
assert len(ruling) == 1, len(ruling)
ruling = ruling[0]
opts = [m for m in MSGS if m[0] == 'assistant' and '**D189**' in m[3] and '**D193**' in m[3] and 'ご申告' in m[3] and m[2] < ruling[2]]
assert opts, '裁定の前の案が見つからない'
opts = opts[-1]
words = ruling[3].strip()
stmt = words[words.index('私の登録者としての申告ですが'):words.index('影響していません。') + len('影響していません。')]
# ユニットの数（登録者の発言から・時刻の順）
units = []
for t, u, ts, s in MSGS:
    if t == 'user' and len(s) < 800:
        for mm in re.finditer(r'ユニット数は、?\s*([0-9]+\.[0-9]+)', s):
            units.append({'uuid': u, 'jst': jst(ts), 'value': float(mm.group(1))})
units = [x for x in units if x['jst'] >= '2026-09-24']       # B-lens の Colab の段は 2026-09-24 だけ
units.sort(key=lambda x: x['jst'])
seen, U = set(), []
for x in units:
    if x['uuid'] not in seen:
        seen.add(x['uuid'])
        U.append(x)
assert [x['value'] for x in U] == [630.56, 630.33, 630.12, 629.98], [x['value'] for x in U]
steps = [('一度目の凍結の前の確かめ（相 check・止めた）', U[0], U[1]), ('二度目の凍結の前の確かめ（相 check）', U[1], U[2]), ('相 extract', U[2], U[3])]
UJ = {'kind': 'blens_colab_units', 'readings': U, 'steps': [{'step': s, 'before': a['value'], 'after': b['value'], 'used': round(a['value'] - b['value'], 2)} for s, a, b in steps],
      'total_used': round(U[0]['value'] - U[-1]['value'], 2), 'source': '登録者がチャットに書いた Colab のユニットの数（会話の記録から機械で読んだ）',
      'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
# 露出の文（会話の記録と置き場の記録から）
m187 = [m for m in MSGS if m[0] == 'assistant' and '問題一' in m[3] and '問題二' in m[3] and '私の推奨は A です' in m[3]][-1]
s_0671 = [l for l in m187[3].split(NL) if '0.671' in l][0].strip()
s_file = [l for l in m187[3].split(NL) if 'predictions-Blens.json' in l][0].strip()
m188 = [m for m in MSGS if m[0] == 'assistant' and 'D-BL1' in m[3] and '甲（推奨）' in m[3] and '封印の器' in m[3]][-1]
s_dir = [l for l in m188[3].split(NL) if 'p1.survival.dir=予想しない' in l][0].strip()
s_na = [l for l in m188[3].split(NL) if '「付かない」の項目' in l][0].strip()
tool = [m for m in MSGS if m[0] == 'tool_result' and 'p6.gate = 通らない' in m[3] and 'p1.survival.label = 付かない' in m[3]]
assert len(tool) == 1
PC = json.load(open(os.path.join(REPO, 'records', 'predictions', 'predictions-Blens-coordinator.json'), encoding='utf-8'))
s_free = PC['free'].split('。')[0] + '。'
LED = open(os.path.join(REPO, 'records', 'FREEZE-RECORD.md'), encoding='utf-8').read()
row_seal = [l for l in LED.split(NL) if 'B-lens 予想封印' in l][0]
reg_file = re.search(r'ファイルの更新 (\d\d:\d\d)', row_seal).group(1)
reg_sha = re.search(r'(\d\d:\d\d) にチャットで受けた SHA-256', row_seal).group(1)
coord_seal = re.search(r'(\d\d:\d\d) にチャットで SHA だけを伝えた', row_seal).group(1)

E = ['# B-lens の予想の封印の前の露出の記録（機械生成・`records/Blens/rulings_D189_D193.py`・裁定 D190・2026-09-24）', '',
     '- 裁定 D148 の順（コーディネータが先に封印して SHA だけを伝え、登録者はコーディネータの予想を開かずに封印する）に関わる出来事を、時刻の順に一つの記録にまとめた。文は会話の記録と置き場の記録から機械で切り出した。',
     '- この記録は評価ではない。予想の照合は記録であり評価ではない（報告 §8）。', '',
     '| 時刻（日本時間） | 向き | 出来事 | 逐語（機械で切り出した） |', '|---|---|---|---|',
     '| %s | コーディネータ → 登録者 | 一度目の Colab の確かめの報告で、較正の検査の確率（無操作の模型・射影ではない）を伝えた | %s |' % (jst(m187[2]), s_0671.replace('|', '｜')),
     '| %s | 登録者の置き場 → コーディネータ | コーディネータが、登録者の Downloads に予想の JSON の名のファイルがあるのを見た（開いていない） | %s |' % (jst(m187[2]), s_file.replace('|', '｜')),
     '| %s | コーディネータの出力 | コーディネータの予想の値（鍵と値の一覧）が、準備の途中のツールの出力に出た（会話の記録 uuid `%s`） | （値の一覧・封印の記録の JSON と同じ中身） |' % (jst(tool[0][2]), tool[0][1]),
     '| %s | コーディネータ → 登録者 | 封印の器が止まった報告で、コーディネータの予想の一部（p1.survival の向きの欄が「予想しない」＝その札の予想が「付かない」・「付かない」の項目がある）を伝えた。コーディネータはこれを露出と気づかなかった（結果の巡の票 C2・C3 が指摘） | %s ／ %s |'
     % (jst(m188[2]), s_dir.replace('|', '｜'), s_na.replace('|', '｜')),
     '| 封印の前 | コーディネータ | コーディネータは封印の前に、凍結の前の Colab の確かめの出力を見た（コーディネータの予想の自由記述） | %s |' % s_free.replace('|', '｜'),
     '| %s | コーディネータ → 登録者 | コーディネータが封印し、SHA だけを伝えた（全体の台帳の封印の行） | — |' % coord_seal,
     '| %s・%s | 登録者 | 登録者の予想の JSON のファイルの更新 %s・チャットで SHA-256 を伝えた %s（全体の台帳の封印の行） | — |' % (reg_file, reg_sha, reg_file, reg_sha), '',
     '## 登録者の申告（逐語・会話の記録 uuid `%s`・%s 日本時間）' % (ruling[1], jst(ruling[2])), '', '「%s」' % stmt.replace(NL, ' '), '',
     '## 注（事実のみ）', '',
     '- 登録者は、予想が 2026-09-23 の時点で固まっていたと申告した。コーディネータの本日の報告（06:30・07:52）と準備の途中のツールの出力（開いていない）は、予想に触れていないと申告した。',
     '- ファイルの更新の時刻（%s）は、書式から JSON を保存した時刻で、予想が固まった時刻とは別である。前の版のファイルの SHA は取っていないので、中身が同じかは器では確かめられない（登録者の申告に依る）。' % reg_file,
     '- コーディネータの予想は、登録者の予想の JSON を見る前に封印した（登録者の JSON はその後に写した）。', '',
     '## 検分票', '',
     '- 対象: 封印の前の露出の全て（コーディネータが気づいたものと、結果の巡の票が見つけたもの）。',
     '- 段階: 結果の後（結果の巡の後の記録）。',
     '- 敵対的検分: コーディネータが見落とした 07:52 の露出を、見落としとして書いた。',
     '- 本検分が確認していないこと: 登録者の予想の中身がいつ固まったか（申告に依る）。会話の外で起きたこと。', '',
     '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']

RUL = [('D189', '結果の巡の組み立ての逸脱（D-BL2）を記帳する。凍結の本文 §10 は結果の巡を「新しい個体」で組むとしたが、依頼文は同じ四名に宛てた（起草者の誤り）。登録者が各系統に新しい個体を一人ずつ足した（G3・C3）。独立の重みは G3 に置き、G1・G2 は同じ個体の二巡目、C1〜C3 は一票として数える。最終の系統外の一票は、新しい個体（Gemini の新しい会話）とし、「最終」と明記する'),
       ('D190', '封印の前の露出を時刻つきで一つの記録にまとめる（`records/Blens/sealing-exposures-Blens.md`）。登録者の申告を逐語で入れる'),
       ('D191', '報告の直しは、凍結した組み立ての器の出力（`records/Blens/results-Blens.md`）を残したまま、逸脱の下の組み立ての器（D-BL3・凍結した器を読み込み、印を付けた区画を足す）で報告の草案2 を組む。採否表の区分（三）の行はこの器で行う'),
       ('D192', '主位置の生の全語彙の softmax の確率と、異なる文の頭の数（凍結した層二の器が計算していない・採否表 P582・P583）を、事後の区画で計算する（D-BL4）。札・読みの比は変えない'),
       ('D193', '結果の巡・第一巡の採否表（P565〜P603）の案を、案のとおりとする')]
R = ['# 登録者裁定 D189〜D193（2026-09-24・結果の巡・第一巡の後）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (ruling[1], jst(ruling[2]), words.replace(NL, ' ')), '',
     '| 裁定 | 中身 |', '|---|---|'] + ['| %s | %s |' % kv for kv in RUL] + [
     '', '## Colab のユニット（登録者の発言から機械で読んだ・`records/Blens/colab-units-Blens.json`）', '', '| 段 | 前 | 後 | 使った数 |', '|---|---|---|---|']
R += ['| %s | %.2f | %.2f | %.2f |' % (s['step'], s['before'], s['after'], s['used']) for s in UJ['steps']]
R += ['', '- 合計 %.2f。' % UJ['total_used'], '',
      '## 裁定の前にコーディネータが示した案（逐語・会話の記録 uuid `%s`・%s 日本時間）' % (opts[1], jst(opts[2])), '', '````text', opts[3].rstrip(), '````', '',
      '## 注（事実のみ）', '',
      '- 採否表: `records/reviews/Blens/results-round1/adoption-table-Blens-results-r1.md`。再現の表: 同じ置き場の `verification-Blens-results-r1.md`。',
      '- 逸脱 D-BL2 を凍結の記録の逸脱台帳に記した。D-BL3 と D-BL4 は、器を作ったときに記す。',
      '- 番号: 次の裁定は D194 から。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']

# 逸脱 D-BL2 を凍結の記録に記す
FR = json.load(open(FR_JSON, encoding='utf-8'))
assert not any(d.get('no') == 'D-BL2' for d in FR['deviations'])
dev = {'no': 'D-BL2', 'date': jst(ruling[2]).split(' ')[0],
       'what': '**結果の巡の組み立て**。凍結の本文 §10 は結果の巡を「新しい個体」で組むとしたが（正本 `review_plan.results` は数だけを定める）、コーディネータの依頼文は設計の巡と同じ四名に宛てた。登録者が Gemini と claude.ai に新しい個体を一人ずつ足し、六票になった（G3・C3 が新しい個体）。票の C1・C2 が指摘した。記録 `records/Blens/rulings-D189-D193.md`',
       'scope': '結果の巡の独立の重み（G1・G2 は同じ個体の二巡目・C1〜C3 は一票）。最終の系統外の一票は新しい個体とする。報告の札と数は変えない',
       'approval': '登録者裁定 D189（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」）' % (jst(ruling[2]), ruling[1], words.replace(NL, ' '))}
FR['deviations'].append(dev)
json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = open(FR_MD, encoding='utf-8').read()
anchor = [l for l in md.split(NL) if l.startswith('| D-BL1 |')][0]
md = md.replace(anchor, anchor + NL + '| %s | %s | %s | %s | %s |' % (dev['no'], dev['date'], dev['what'].replace('|', '｜'), dev['scope'], dev['approval'].replace('|', '｜')), 1)
open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md)
json.dump(UJ, open(UNITS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
open(EXPO, 'w', encoding='utf-8', newline=NL).write(NL.join(E))
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), os.path.basename(EXPO), os.path.basename(UNITS), '| units', [s['used'] for s in UJ['steps']], '| D-BL2 ledgered')
