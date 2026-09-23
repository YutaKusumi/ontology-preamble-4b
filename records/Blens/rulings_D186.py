# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D186 の記録を書く（凍結の前の登録者の最終の確かめ・2026-09-23）。
登録者の言葉は会話の記録から機械で切り出す。§13 の値は正本から写す（手で打たない）。既にあるファイルには書かない。
用法: python records/Blens/rulings_D186.py <会話の記録 jsonl>"""
import os, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
COMMIT = '567c74e'
words = rec_uuid = rec_ts = None
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
        if '登録者最終確認を行いました' in t and COMMIT in t and len(t) < 600:
            words, rec_uuid, rec_ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '裁定の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(rec_ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
show = lambda rel: subprocess.run(['git', 'show', '%s:%s' % (COMMIT, rel)], cwd=REPO, capture_output=True, check=True).stdout
s16 = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
draft_b, canon_b = show('design/design-Blens-draft3.md'), show('design/contrasts-Blens.json')
T = json.loads(canon_b.decode('utf-8'))
MG, WS = T['magnitude'], T['nulls']['word_side']
vals = [('大きさの目盛りの下限（観測の変化の二標本の z の絶対値）', '%g（連続性の補正 %g）' % (MG['lower_bound']['z_min'], MG['lower_bound']['continuity'])),
        ('語の側の帰無', '抽選 %s 回・種 %d・ノルムの帯 %d・水準 %g・薄い層を合わせる倍率 %d' % ('{:,}'.format(WS['draws']), WS['seed'], WS['norm_bands'], WS['alpha'], WS['merge_factor'])),
        ('logits の突き合わせの許容', '%g' % MG['logit_check']['atol']),
        ('等方の帰無の自己検査の許容（相対の差）', '%g' % T['nulls']['isotropic']['analytic_tol']),
        ('封印の後の記述の上位の次元の数', '%d' % T['descriptive_after_seal']['top_dims']),
        ('較正の検査の区間', '%g' % MG['calibration_check']['ci']),
        ('境目の近くの行を印字する帯', '%g〜%g' % tuple(MG['near_band'])),
        ('大きさの目盛りで層ごとに選ぶ件数', '%d' % MG['per_cell']),
        ('読みの比', '%g' % MG['reading_ratio']),
        ('門の行動の量の連続性の補正', '%g' % T['calibration']['continuity']),
        ('主の札の水準・門の水準', '%g・%g' % (T['primary']['alpha'], T['calibration']['alpha'])),
        ('語の一覧の上位と下位の数', '%d' % T['projection']['top_k']),
        ('様式の感度の集合の上位の数', '%d' % T['token_sets']['F_top'])]
R = ['# 登録者裁定 D186（2026-09-23・B-lens の凍結の前の登録者の最終の確かめ）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (rec_uuid, jst, words.replace(NL, ' ')),
     '', '| 裁定 | 中身 |', '|---|---|',
     '| D186 | **草案3（コミット %s・`design/design-Blens-draft3.md` SHA16 %s・正本 `design/contrasts-Blens.json` SHA16 %s）と、§13 の起草者が置いた値を、今のまま確かめた**。器・合成データ・凍結・封印の順に進める。 |' % (COMMIT, s16(draft_b), s16(canon_b)), '',
     '## 確かめた値（§13・正本から機械で写した）', '', '| 値 | 置いた値 |', '|---|---|']
R += ['| %s | %s |' % kv for kv in vals]
R += ['', '## 注（事実のみ）', '',
      '- 同じ言葉で、コミット %s の push の許可があった（push 済み）。' % COMMIT,
      '- 凍結はこの後、器と合成データの確かめの後に行う。凍結の本文は、草案3 の原稿から題名と凍結の一行だけを変えて組む（段階 A・B と同じ型）。',
      '- この確かめの後、凍結までに草案3 の文や正本を変える必要が出たときは、止めて登録者に相談する（登録者の決まり）。凍結の後の変更は、逸脱として台帳に記す。',
      '- 番号: 次の裁定は D187 から（正本の `numbering.rulings_next` は草案3 の時点の値のまま）。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
out = os.path.join(HERE, 'rulings-D186.md')
assert not os.path.exists(out), '既にある: ' + out
open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', out, '|', jst, rec_uuid)
