# -*- coding: utf-8 -*-
# write_freeze_record_main.py : 人の立場の三つの腕の本番の事前登録の凍結の記録を書く（一度だけ・SHA-256 は道具で数える）
import os, sys, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
OUT = os.path.join(W, '13-FREEZE-RECORD-main.md')
FILES = [
    ('事前登録（本文）', '10-prereg-main-draft-v0.md'),
    ('草案と器の対応表', '12-kit-correspondence-v0.md'),
    ('kit v2（Colab に上げる zip）', 'kit-main-v2/kit-stance-main-v2.zip'),
    ('kit v2 の設定', 'kit-main-v2/kit-stance-main-v2/run-config.json'),
    ('Colab の器 v1', 'tools/boot_stance_main_v1.py'),
    ('較正の決め・族・判定の道具 v1', 'tools/stance_eval_v1.py'),
    ('自己試験 v1', 'tools/selftest_stance_v1.py'),
    ('検出力の道具', 'tools/power_stance_v0.py'),
    ('kit を組む道具 v2', 'tools/make_kit_main_v2.py'),
    ('立場の 18 の文', 'arms/arms-stance-v0.json'),
    ('先行研究の下調べ（一次の読みの追記つき）', 'notes/lit-survey-v0.md'),
    ('予行の記録', 'results/rehearse-main-v1.md'),
    ('予行の env の zip', 'results/out-env-v1.zip'),
    ('系統外の検分の依頼文', 'reviews/gemini-1/request.txt'),
    ('系統外の検分の答え', 'reviews/gemini-1/answer-page-text.txt'),
    ('系統外の検分の採否', 'reviews/gemini-1/response-v0.md'),
    ('系統外の検分の送りの記録', 'reviews/gemini-1/send-record.md'),
]
if os.path.exists(OUT):
    print('STOP exists', OUT); raise SystemExit(1)
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
rows = []
for what, rel in FILES:
    p = os.path.join(W, *rel.split('/'))
    b = open(p, 'rb').read()
    rows.append('| %s | `%s` | %d | %s |' % (what, rel, len(b), hashlib.sha256(b).hexdigest().upper()))
NL = chr(10)
L = ['# 人の立場の三つの腕：本番の事前登録の凍結の記録（%s 日本時間・南無弥勒如来）' % now, '',
     '本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。', '',
     '- 決め：登録者の決め（2026-11-05 22:2x・質問フォーム）「凍結して、較正と本番を夜間の間に続ける」。',
     '- 夜の間の扱い（同じ質問フォーム）：',
     '  - (a) 較正で「伺う」の印が出た場面は使わずに進める。',
     '  - (b) 本番の途中でランタイムが失われたら止めて朝に伺う。',
     '  - (c) 今夜の計算ユニットの上限は 15。',
     '  - 本文 §0 に同じ字で書いた。',
     '- 凍結の時点：較正の前・本番の値は無い。予行の答え（封の側）は下ろしていない。',
     '- この後の変更は逸脱として、番号・理由・登録者の承認（夜の間は (a)〜(c) の範囲だけ）とともに記録する。', '',
     '| 何 | ファイル（作業の置き場からの道） | バイト | SHA-256 |', '|---|---|---|---|'] + rows + [
     '', '- 論文の公開の置き場の凍結物（送りの道具・場面の素材・パーサ・拒否の規則・語彙・判定の関数）の SHA-256 は、kit v2 の run-config.json と `tools/stance_eval_v1.py` の PIN に書いてある。', '']
with open(OUT, 'x', encoding='utf-8', newline=NL) as f:
    f.write(NL.join(L))
print('書いた', OUT, 'SHA-256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest().upper(), 'rows', len(rows))
