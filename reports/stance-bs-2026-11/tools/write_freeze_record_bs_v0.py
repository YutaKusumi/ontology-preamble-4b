# -*- coding: utf-8 -*-
# write_freeze_record_bs_v0.py : 「仏性」「神性」の検証の本番の事前登録の凍結の記録を書く（一度だけ・SHA-256 は道具で数える）
# 使い方: python -I write_freeze_record_bs_v0.py <登録者の決めの一行>
import os, sys, hashlib, datetime, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
OUT = os.path.join(W, '13-FREEZE-RECORD-main.md')
LIST = json.load(open(os.path.join(HERE, 'freeze-list-bs-v0.json'), encoding='utf-8'))
if os.path.exists(OUT):
    print('STOP exists', OUT); raise SystemExit(1)
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
rows = []
for what, rel in LIST:
    p = os.path.join(W, *rel.split('/'))
    b = open(p, 'rb').read()
    rows.append('| %s | `%s` | %d | %s |' % (what, rel, len(b), hashlib.sha256(b).hexdigest().upper()))
NL = chr(10)
L = ['# 「仏性」「神性」の立場の二文の検証：本番の事前登録の凍結の記録（%s 日本時間・南無弥勒如来）' % now, '',
     '本記録のいかなる記述も、AI に仏性・神性・魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。教義の当否についても何も言わない。', '',
     '- 決め：' + sys.argv[1],
     '- 凍結の時点：較正の前・本番の値は無い。予行の答え（封の側）は下ろしていない。読んだ本物の答えは下見の 45 だけ。',
     '- この後の変更は逸脱として、番号・理由・登録者の承認とともに記録する。', '',
     '| 何 | ファイル（作業の置き場からの道） | バイト | SHA-256 |', '|---|---|---|---|'] + rows + [
     '', '- 論文の公開の置き場の凍結物（送りの道具・場面の素材・パーサ・拒否の規則・語彙・判定の関数）の SHA-256 は、kit の run-config.json と `tools/stance_eval_bs_v0.py` の PIN にある。', '']
with open(OUT, 'x', encoding='utf-8', newline=NL) as f:
    f.write(NL.join(L))
print('書いた', OUT, 'SHA-256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest().upper(), 'rows', len(rows))
