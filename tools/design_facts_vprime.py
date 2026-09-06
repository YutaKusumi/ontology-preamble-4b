# -*- coding: utf-8 -*-
"""design_facts_vprime.py —— 追補 V′ の設計事実（腕数・試行数・対比数・被覆・費用時間の概算・反証条件の発火確率・盤の未使用腕・--arms）を
`design/contrasts-Vprime.json` と盤台帳から機械生成する。本文（草案／凍結文書）はこの出力を転記するだけで、散文中に手計算の数を書かない（三巡目検器身高2・高3・高5／破器身 H1）。
出力: records/design-facts-Vprime.md と同 .json（上書き＝正本の現状を映す。凍結時の値は FREEZE-RECORD に写す）。
"""
import os, sys, json, math, hashlib, datetime
from scipy.stats import binom
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-Vprime.json'), encoding='utf-8'))
L = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8'))
n = T['n_per_arm']; SC = list(T['scenarios']); arms = T['arms']['singles'] + T['arms']['combos']
# 概算の係数（出所: 本プログラム本走行 41,540 試行の実績比からのコーディネータ概算・約 1.0 秒/試行・約 $0.0001/試行。実績ではない）
SEC_PER_TRIAL, USD_PER_TRIAL = 1.0, 0.0001
fams = T['families']; dfams = T.get('descriptive_families', {})
allc = [(f, c) for f, F in list(fams.items()) + list(dfams.items()) for c in F['contrasts']]
ids = [c['id'] for f, c in allc]
dup = sorted({i for i in ids if ids.count(i) > 1})
used = {c[k] for f, c in allc for k in ('A', 'B')}
unlinked = [a for a in arms if a not in used]
panel_unused = sorted(a for a in L if a not in arms and a not in ('O', 'Onull'))
not_in_ledger = [a for a in arms if a not in L and a not in ('N', 'O', 'Onull')]
trials_main = len(SC) * len(arms) * n; trials_pilot = len(SC) * len(arms) * T['gate_counts']['pilot_n']
s = ','.join(arms); arms_sha = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
conf_n = sum(len(F['contrasts']) for F in fams.values()); desc_n = sum(len(F['contrasts']) for F in dfams.values())
measured = sum(1 for F in fams.values() for c in F['contrasts'] if c.get('base_B_main') is not None)
assumed = conf_n - measured
fp = fams['Vprime_b']['falsification']['firing_probability']
# 発火確率の再計算（JSON の埋め込み値と一致することを検査）
thr = {sc: T['scenarios'][sc]['onull_base_main'] for sc in SC}
for pk, row in fp['rows'].items():
    p = float(pk)
    for k, v in row.items():
        t = 0.20 if k == 'old_0.20' else thr[k]
        w = float(binom.sf(math.ceil(t * n) - 1, n, p))
        assert abs(w - v) <= 1e-12 * max(1.0, abs(v)) or (v == 0 and w == 0), (pk, k, v, w)
facts = {'contrasts_version': T['version'], 'when': datetime.date.today().isoformat(), 'scenarios': SC, 'arms_total': len(arms), 'singles': len(T['arms']['singles']), 'combos': len(T['arms']['combos']),
         'n_per_arm': n, 'trials_main': trials_main, 'trials_pilot': trials_pilot, 'est_hours_main': trials_main * SEC_PER_TRIAL / 3600, 'est_usd_main': trials_main * USD_PER_TRIAL,
         'confirmatory_contrasts': conf_n, 'confirmatory_by_family': {f: F['m'] for f, F in fams.items()}, 'confirmatory_measured_base': measured, 'confirmatory_assumed_base': assumed,
         'descriptive_contrasts': desc_n, 'descriptive_by_family': {f: len(F['contrasts']) for f, F in dfams.items()}, 'duplicate_ids': dup, 'arms_without_contrast': unlinked,
         'panel_unused': panel_unused, 'arms_not_in_ledger': not_in_ledger, 'arms_string_sha16': arms_sha, 'arms_string_len': len(s), 'fwer_max': 1 - 0.95 ** len(fams)}
for f, F in fams.items():
    assert F['m'] == len(F['contrasts']), (f, F['m'], len(F['contrasts']))
if dup or unlinked or not_in_ledger:
    print('[facts] 整合エラー: dup=%s unlinked=%s not_in_ledger=%s' % (dup, unlinked, not_in_ledger)); sys.exit(2)
fpt = fams['Vprime_b']['falsification'].get('firing_probability_text', '')
out = ['# 追補 V′ 設計事実（機械生成・contrasts %s・%s）' % (T['version'], facts['when']), '',
       '**転記行 A（規模）**: %d シナリオ × %d 腕（単独 %d＋組合せ %d）× %d ＝ %s 試行（概算 ≈$%.1f・約 %.1f 時間・係数は本プログラム実績比のコーディネータ概算）。パイロット %d/腕 ＝ %s 試行。' % (len(SC), len(arms), facts['singles'], facts['combos'], n, format(trials_main, ','), facts['est_usd_main'], facts['est_hours_main'], T['gate_counts']['pilot_n'], format(trials_pilot, ',')),
       '**転記行 B（対比）**: 確証 %d 本（%s）・記述 %d 本（%s）・id は全族を通じて一意（重複 %d）・登録された対比を持たない腕 %d。' % (conf_n, '・'.join('%s m=%d' % kv for kv in facts['confirmatory_by_family'].items()), desc_n, '・'.join('%s %d' % kv for kv in facts['descriptive_by_family'].items()), len(dup), len(unlinked)),
       '**転記行 C（検出力の被覆）**: 確証 %d 本のうち実測基底 %d 本（V′a）・仮定基底 %d 本（V′b %d・V′c %d・N1:Ncold~Nstr 1）。仮定基底の対比の検出力は走行前に確定できず、検出域の申告に用いない。' % (conf_n, measured, assumed, fams['Vprime_b']['m'], fams['Vprime_c']['m']),
       '**転記行 D（全体 FWER）**: 確証族 %d・最大 1−0.95^%d ≈ %.3f。' % (len(fams), len(fams), facts['fwer_max']),
       '**転記行 E（反証条件の発火確率）**: %s' % fpt,
       '**転記行 F（盤の未使用腕）**: %s（走行は --arms の一行 SHA16 %s・%d 腕・%d 字のみ）。' % ('・'.join(panel_unused), arms_sha, len(arms), len(s)), '',
       '## 発火確率表（規則 1・n=%d・%s）' % (n, fp['method']), '| O-Ncold 真値 | 旧 0.20 | ' + ' | '.join(SC) + ' |', '|---|---|' + '---|' * len(SC)]
for pk, row in fp['rows'].items():
    out.append('| %s | %.2e | %s |' % (pk, row['old_0.20'], ' | '.join('%.2e' % row[sc] for sc in SC)))
out += ['', '## --arms（正本から生成・手打ち禁止）', '```', s, '```', '', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(os.path.join(REPO, 'records', 'design-facts-Vprime.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump(facts, open(os.path.join(REPO, 'records', 'design-facts-Vprime.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('\n'.join(out[2:8]))
