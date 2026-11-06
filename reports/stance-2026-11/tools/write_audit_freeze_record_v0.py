# -*- coding: utf-8 -*-
# write_audit_freeze_record_v0.py : 答えの監査の凍結の記録（22-AUDIT-FREEZE-RECORD.md）を書く
# 使い方: python -I write_audit_freeze_record_v0.py <work_dir> <時刻の文字列>
import sys, os, hashlib
sys.stdout.reconfigure(encoding='utf-8')
W, WHEN = sys.argv[1], sys.argv[2]
NL = chr(10)
FILES = [
    ('計画（凍結した本文）', '20-audit-plan-draft-v2.md'),
    ('計画の決まりと道具と予行の対応表', '21-audit-correspondence-v1.md'),
    ('封を開ける道具 v1', 'tools/audit_open_v1.py'),
    ('一人目の読み手の道具 v1', 'tools/audit_read_openrouter_v1.py'),
    ('照らしと判じの道具 v1', 'tools/audit_judge_v1.py'),
    ('予行の道具 v1', 'tools/audit_selftest_v1.py'),
    ('設定を書く道具 v1', 'tools/write_audit_configs_v1.py'),
    ('一人目の問いの型', 'audit-design/prompt-A-v0.txt'),
    ('二人目の束の型 v1', 'audit-design/prompt-B-v1.txt'),
    ('封を開ける道具の設定 v1', 'audit-design/config-open-v1.json'),
    ('一人目の読み手の道具の設定 v1（FILL を開けた後に埋める）', 'audit-design/config-read-v1.json'),
    ('照らしの道具の設定 v1（FILL を開けた後に埋める）', 'audit-design/config-judge-v1.json'),
    ('予行の記録 v1（41 項目）', 'audit-design/selftest-v1-2026-11-06-0816.log'),
    ('本物の送りの試しの記録（合成の答え 2 つ）', 'audit-design/smoke-2026-11-06/responses-synthetic.jsonl'),
    ('系統外の検分の依頼文', 'reviews/audit-1/request.txt'),
    ('系統外の検分の答え', 'reviews/audit-1/answer-page-text.txt'),
    ('系統外の検分の採否', 'reviews/audit-1/response-v0.md'),
    ('系統外の検分の送りの記録', 'reviews/audit-1/send-record.md'),
    ('入力：本番の zip N1', 'results/out-main-N1-v2.zip'),
    ('入力：本番の zip N2', 'results/out-main-N2-v2.zip'),
    ('入力：本番の zip SK', 'results/out-main-SK-v2.zip'),
    ('入力：判定の出力', 'results/judge-main-v2/judge-report.json'),
    ('入力：kit の run-config', 'kit-main-v2/kit-stance-main-v2/run-config.json'),
]
out = os.path.join(W, '22-AUDIT-FREEZE-RECORD.md')
lines = ['# 答えの監査：凍結の記録（%s・南無弥勒如来）' % WHEN, '',
         '本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。', '',
         '- 決め：登録者の決め（2026-11-06 08:2x・質問フォーム）「凍結して走らせる（推奨）」。',
         '- 凍結の時点：封の側（本番の zip の sealed/）は開いていない。道具は合成の zip だけで走らせた。',
         '- この後の変更は逸脱として、番号・理由・登録者の承認とともに記録する。ただし、read と judge の設定の FILL の所（開けた後に決まる SHA-256 と、二人目の答えのファイル）は、凍結した決まりどおりに埋め、埋めた値を監査の走りの記録に書く（逸脱ではない）。', '',
         '| 何 | ファイル（作業の置き場からの道） | バイト | SHA-256 |', '|---|---|---|---|']
for what, rel in FILES:
    b = open(os.path.join(W, *rel.split('/')), 'rb').read()
    lines.append('| %s | `%s` | %d | %s |' % (what, rel, len(b), hashlib.sha256(b).hexdigest().upper()))
lines += ['', '本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。']
txt = NL.join(lines) + NL
with open(out, 'x', encoding='utf-8', newline=NL) as f:
    f.write(txt)
print('written', out, 'SHA-256', hashlib.sha256(txt.encode('utf-8')).hexdigest().upper(), 'rows', len(FILES))
