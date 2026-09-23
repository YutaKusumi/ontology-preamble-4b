# -*- coding: utf-8 -*-
"""全体の台帳 records/FREEZE-RECORD.md に、段階 B の予想封印・凍結・結果報告の公開の三行を後から記帳する（登録者裁定 D177・2026-09-23）。
値は段階 B の凍結の記録・予想の JSON・git・README・会話の記録から器で取る（手で打たない）。行が既にあれば止まる（足すのは一度だけ）。
用法: python records/B/ledger_rows_B_late.py <会話の記録 jsonl>"""
import os, re, sys, json, hashlib, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
P = lambda rel: os.path.join(REPO, *rel.split('/'))
rd = lambda rel: open(P(rel), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(P(rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s256 = lambda rel: hashlib.sha256(open(P(rel), 'rb').read()).hexdigest().upper()
git = lambda *a: subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, check=True).stdout.decode('utf-8').strip()

LED = 'records/FREEZE-RECORD.md'
led = rd(LED)
for mark in ('**段階 B 予想封印', '**段階 B 凍結**', '**段階 B 結果報告 公開**'):
    assert mark not in led, '既に行がある: ' + mark
assert led.endswith('|' + NL), '台帳の末尾が表の行でない'
assert re.search(r'^\| 2026-09-17 \| \*\*段階 A 結果報告 公開\*\*', led.split(NL)[-2]), '台帳の最後の行が段階 A の公開の行でない'

# 会話の記録から登録者の言葉
def find(pred):
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
            if pred(t):
                return t.strip(), o.get('uuid'), o.get('timestamp')
    raise AssertionError('言葉が見つからない')
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
fz_t, fz_u, fz_ts = find(lambda t: '凍結とそれに伴う段取りを進めてください' in t and len(t) < 800)
pb_t, pb_u, pb_ts = find(lambda t: '草案5を確認いたしまして' in t and 'f62f0fe' in t and len(t) < 800)
fz_q = re.search(r'登録者確認を行いました。.*?凍結とそれに伴う段取りを進めてください。', fz_t).group(0)
pb_q = re.search(r'草案5を確認いたしまして、.*?判断いたします。', pb_t).group(0)
assert jst(fz_ts) == '2026-09-20 18:44' and jst(pb_ts) == '2026-09-23 13:57', (jst(fz_ts), jst(pb_ts))

# 段階 B の凍結の記録
FRB_REL = 'records/B/FREEZE-RECORD-B.md'
frb = rd(FRB_REL)
frz_time = re.search(r'凍結の時刻: (.+?)。凍結した。', frb).group(1)
frozen16, canon16 = s16('design/design-stageB-FROZEN.md'), s16('design/contrasts-B.json')
assert frozen16 == '8B3D54E4500B46FF' and canon16 == 'EF0DF4295B68F949', (frozen16, canon16)
assert re.search(r'`tools/freeze_B\.py` v13', frb)

# 封印（値は凍結の記録に記帳された値と、ファイルから計算した値の両方で確かめる）
REG, COO, SEAL = 'records/predictions/predictions-registrant-B-2026-09-19.json', 'records/predictions/predictions-coordinator-B-2026-09-19.json', 'records/B/seal-B.json'
reg256, coo256, seal256 = s256(REG), s256(COO), s256(SEAL)
for v in (reg256, coo256, seal256):
    assert v in frb, '凍結の記録の値と合わない: ' + v
assert '**順の注**' in frb and '登録者の予想はコーディネータの予想を見ずに封印されたので独立である' in frb
seal_commit = git('log', '--format=%h', '--diff-filter=A', '--', SEAL)
assert seal_commit == '2c1ff7f', seal_commit
assert 'predictions sealed' in git('log', '-1', '--format=%s', seal_commit)
assert os.path.exists(P('records/predictions/sealing-record-B-2026-09-19.md'))

# 凍結のコミット
frz_commit = git('log', '--format=%h', '--diff-filter=A', '--', 'design/design-stageB-FROZEN.md')
assert frz_commit == 'aea6c52' and git('log', '-1', '--format=%s', frz_commit).startswith('stage B: frozen'), frz_commit
assert '(aea6c52)' in git('log', '-1', '--format=%s', 'b52ea11')
readme = rd('README.md')
assert '22fbd64' in readme and 'make_frozen_B.py' in readme
git('cat-file', '-e', '22fbd64^{commit}')

# 公開
FIN = 'records/B/results-B-FINAL-2026-09-23.md'
fin16 = s16(FIN)
tag_commit = git('rev-parse', '--short', 'release-B-2026-09-23^{commit}')
assert tag_commit == '4d13197', tag_commit
res_line = [l for l in readme.split(NL) if l.startswith('- **結果（2026-09-22〜23・公開')]
assert len(res_line) == 1
for frag in ('第一巡・第二巡とも系統外二票・系統内二票・全票「条件つき可」', '裁定 D151〜D160', '第三巡は最終の系統外一票・「条件つき可」', '逸脱台帳 D-B1〜D-B6'):
    assert frag in res_line[0], frag
assert os.path.exists(P('records/B/make_final_B.py'))

late = '**後からの記帳**（2026-09-23・登録者裁定 D177）。段階 B の事象は段階 B の台帳 %s に置いてきた' % FRB_REL
rows = [
    '| 2026-09-19 | **段階 B 予想封印（登録者とコーディネータ・裁定 D148）**（凍結の前・データ生成前）: 登録者の予想 %s（SHA-256 %s）とコーディネータの予想 %s（SHA-256 %s）を保全し、起草者の封印 %s（SHA-256 %s）をコーディネータの予想から作った（コミット %s）。**順は裁定 D148 と逆**——登録者が先に封印して JSON を送り、コーディネータはそれを見た後に封印した。登録者の予想は独立で、コーディネータの予想は独立でない。経緯は records/predictions/sealing-record-B-2026-09-19.md、記帳は %s の「封印予想」「登録者とコーディネータの予想」の節。的中は独立の確認ではなく、誰の判断の重みも変えない。 | %s・%s・%s | 登録者 %s・コーディネータ %s・封印 %s | %s |' % (
        REG, reg256, COO, coo256, SEAL, seal256, seal_commit, FRB_REL, REG, COO, SEAL, reg256[:16], coo256[:16], seal256[:16], late),
    '| 2026-09-20 | **段階 B 凍結**（登録者「%s」%s 日本時間）: 草案13B の原稿（コミット 22fbd64）を design/design-stageB-FROZEN.md に逐語複製（題名と凍結の一行のみ改める・差は器 tools/make_frozen_B.py で確かめた）。正本 design/contrasts-B.json・凍結の記録 %s（tools/freeze_B.py v13・凍結の時刻 %s）。凍結のコミット %s・走行の段取りにそのコミットを入れたコミット b52ea11。記録先行公開。以後の変更は段階 B の台帳の逸脱台帳（D-B1〜）に記帳する。 | design/design-stageB-FROZEN.md・design/contrasts-B.json・%s | 凍結本文 %s・正本 %s | %s |' % (
        fz_q, jst(fz_ts), FRB_REL, frz_time, frz_commit, FRB_REL, frozen16, canon16, late),
    '| 2026-09-23 | **段階 B 結果報告 公開**（登録者最終確認「%s」%s 日本時間）: 草案5（records/B/results-B.md）を %s に逐語複製（題と状態の一行のほかは同一・器 records/B/make_final_B.py）。二つの集計の出力（凍結した集計器・逸脱 D-B1 の下）を同じ重さで並べる。公開前検分は第一巡・第二巡（各 系統外二票・系統内二票・全票「条件つき可」）と第三巡（最終の系統外一票・「条件つき可」）と起草者の最終の見直し。裁定 D151〜D160。逸脱 D-B1〜D-B6（段階 B の台帳）。README に導線・タグ release-B-2026-09-23（コミット %s）。 | %s・records/B/・README.md | 最終版 %s | %s |' % (
        pb_q, jst(pb_ts), FIN, tag_commit, FIN, fin16, late),
]
for r in rows:
    assert r.count('|') == 6, r[:60]
open(P(LED), 'w', encoding='utf-8', newline=NL).write(led + NL.join(rows) + NL)
print('appended', len(rows), 'rows |', LED, s16(LED))
