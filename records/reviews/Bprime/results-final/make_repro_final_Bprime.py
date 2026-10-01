# -*- coding: utf-8 -*-
"""make_repro_final_Bprime.py v0.1（2026-10-01・v0.1: 凍結した器の状態の型の照らしを、見つかった鍵の集まりで比べる形に直した〔v0 は型の名の定義と呼び出しの二か所を数えて「合わない」と出した・照らしの書き方の誤りで、器の中身は同じ〕・v0 の台本と出力は prev/ に置いた・B′ の最終検分の票〔grok-4.7〕の事実の主張を、公開の置き場の一次の記録で再現する・結果の巡の `make_repro_results_Bprime.py` の型・コーディネータ南無弥勒如来）。
票の「検算したこと」と所見 X01〜X06 の事実の主張を、記録・正本・報告の草案の二つ目・確かめの記録から機械で照らし、項ごとに値と合否を `repro-final-Bprime.json` に書く（一度だけ）。
採否の表は数を打ち直さず、この記録の鍵を指す。用法: python make_repro_final_Bprime.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json, math, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
OUT = os.path.join(HERE, 'repro-final-Bprime.json')
P = lambda *a: os.path.join(PUB, *a)
ld = lambda *a: json.load(open(P(*a), encoding='utf-8'))
s16 = lambda *a: hashlib.sha256(open(P(*a), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
C = ld('design', 'contrasts-Bprime.json')
PJ = ld('records', 'Bprime', 'pilot', 'pilot-Bprime.json')
FR = ld('records', 'Bprime', 'FREEZE-RECORD-Bprime.json')
CL = ld('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json')
AN = ld('records', 'Bprime', 'analysis-Bprime.json')
CK = ld('records', 'Bprime', 'results-Bprime-draft2-checks.json')
PV = ld('records', 'Bprime', 'prefreeze-Bprime-2026-10-01-colab', 'provenance.json')
RR = ld('records', 'reviews', 'Bprime', 'results', 'repro-results-Bprime.json')
D2 = open(P('records', 'Bprime', 'results-Bprime-draft2.md'), encoding='utf-8').read()
FZ = open(P('records', 'Bprime', 'results-Bprime.md'), encoding='utf-8').read()
ADOPT = open(P('records', 'reviews', 'Bprime', 'results', 'adoption-table-results-Bprime.md'), encoding='utf-8').read()
lo_b, hi_b = C['pilot']['p_bounds']
cells = PJ['cells']
runs = {r['phase']: r for r in FR['main_freeze']['runs']['table']}
st = {ph: ld('records', 'Bprime', 'runs', r['start']['file']) for ph, r in runs.items()}
out = {}


def put(k, got, ok, claim):
    out[k] = {'claim': claim, 'got': got, 'ok': bool(ok)}


floor_c = sorted(c for c, v in cells.items() if v['pa'] < lo_b)
ceil_c = sorted(c for c, v in cells.items() if v['pa'] > hi_b)
in_c = sorted(c for c, v in cells.items() if lo_b <= v['pa'] <= hi_b)
put('cells_split', {'floor': floor_c, 'ceiling': ceil_c, 'inside': in_c}, floor_c == ['N1|O-Ncold', 'N1|Onull'] and ceil_c == ['S1|O-Ncold', 'S4|O-Ncold', 'SK|O-Ncold']
    and in_c == ['S1|Onull', 'S4|Onull', 'SK|Onull'], '外は N1 の二つ（床）と O-Ncold の S1・S4・SK（天井）、内は S*|Onull の三つ')
put('pass_equals_inside', sorted(c for c, v in cells.items() if v['pass_i_ii']), sorted(c for c, v in cells.items() if v['pass_i_ii']) == in_c, '内の三つが (i)(ii) を満たした')
put('logodds_bound', {'repro_results': RR['p_bounds_logodds'], 'from_canon': math.log(hi_b / (1 - hi_b))}, abs(RR['p_bounds_logodds'] - math.log(hi_b / (1 - hi_b))) < 1e-12, '対数オッズの境は 9.21024…')
put('SK_Onull_pa', cells['SK|Onull']['pa'], cells['SK|Onull']['pa'] < hi_b and '| SK\\|Onull | 8.917 | 0.9999 |' in FZ, 'SK|Onull の記録は天井の内（0.9998659…）・表示は天井と同じ字')
put('mass_not_one', {c: v['mass'] for c, v in cells.items()}, all(v['mass'] != 1.0 for v in cells.values()), '質量は八つともちょうど一ではない')
sg = {c: abs(1 / (1 + math.exp(-v['lo'])) - v['pa']) for c, v in cells.items()}
put('sigmoid_lo_pa_maxabs', max(sg.values()), max(sg.values()) < 1e-9, '対数オッズと集合の中の確率の対応は sigmoid（床側・内・天井側の三点で検算）')
put('vi', {'a_max': PJ['vi']['decision']['spread_a'], 'b_max': PJ['vi']['decision']['spread_b'], 'noise_max': C['pilot']['noise_max'], 'vi_decision': PJ['vi']['decision']},
    PJ['vi']['decision']['spread_a'] > C['pilot']['noise_max'] and PJ['vi']['decision']['spread_b'] == 0 and PJ['vi']['decision']['stop'] is False and PJ['vi']['decision']['batch'] == 1,
    '(vi) の (a) の最大は上限を超え、(b) は零・(vi) の記録は stop false・batch 1（X06）')
put('decision', PJ['decision'], PJ['decision']['stop'] is True and PJ['decision']['reason'] == 'i_ii' and PJ['decision']['n_pass'] == 3 and PJ['decision']['n_main'] == 8, '決定は止める・理由 i_ii・通過 3／8')
put('logit_check', {'states': PJ['logit_check']['states'], 'no_discrimination': PJ['logit_check']['no_discrimination']},
    all(v == '合' for v in PJ['logit_check']['states'].values()) and not PJ['logit_check']['no_discrimination'], '自己検査は八升目とも「合」・見分ける力の無い位置は空')
rc = {ph: st[ph]['commit'] for ph in runs}
tab = {ph: [x for x in FZ.split('\n') if x.startswith('| %s | ' % ph)][0].rstrip(' |').split(' ')[-1] for ph in runs}
ps = [o for o in FR['main_freeze']['sessions'] if o['start_end']['start'][0] == runs['pilot']['start']['file']][0]
put('run_commits', {'table': tab, 'start_records': rc, 'behavior_session_commit': CL['session']['commit'], 'pilot_main_freeze_session_commit': ps['commit']},
    tab == rc and CL['session']['commit'] != rc['behavior'] and ps['commit'] != rc['pilot'], '走行の表のコミットは起動の記録の commit と一致し、行動の下見の session.commit と読み取りの下見の main_freeze.sessions のコミットとは違う')
put('closed_before_pilot', {'closed_jst': CL['closed_jst'], 'start_pilot_jst': st['pilot']['time_jst'], 'closed_sha16': s16('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'),
                            'start_pilot_closed_record_sha16': st['pilot'].get('closed_record_sha16')},
    CL['closed_jst'] < st['pilot']['time_jst'] and st['pilot'].get('closed_record_sha16') == s16('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'), '閉じた時刻は読み取りの下見の起動より前・閉じた記録の SHA16 は起動の記録の closed_record_sha16 と一致')
g = FR['prefreeze']['g']['g_sha256']
put('g_sha', {'freeze_record': g, 'in_provenance': g in json.dumps(PV, ensure_ascii=False), 'colab_check_g_same': FR['checks']['colab_check']['g_same']},
    g in json.dumps(PV, ensure_ascii=False) and FR['checks']['colab_check']['g_same'] is True, 'g の SHA は凍結の記録と出所の記録と G4 の確かめ（g_same）で一致')
neg = C['negation_templates']
put('negation_verbatim', {'first_in_draft2': D2.count('  - ' + neg[0]), 'fourth_in_draft2': D2.count('  - ' + neg[3])}, D2.count('  - ' + neg[0]) == 2 and D2.count('  - ' + neg[3]) == 1,
    '打ち消しの定型の写しは正本と一字違わず同じ（§1 に一つ目と四つ目・§6 に一つ目）')
put('facts_count', len(CK['checks']['facts']), len(CK['checks']['facts']) == 68, '確かめの記録の facts は 68 項')
put('V2_SK_Onull_diff', PJ['iv']['V2']['lo']['SK|Onull'] - cells['SK|Onull']['lo'], abs(PJ['iv']['V2']['lo']['SK|Onull'] - cells['SK|Onull']['lo']) > C['pilot']['variant_flag'] and PJ['iv']['V2']['flags']['SK|Onull'] is True,
    'V2 の SK|Onull の差は表示「1」・記録 1.00033…・印「はい」（X04）')
put('wilson_40_upper', RR['wilson_40_of_40'], RR['wilson_40_of_40'][1] > 1.0 and '0.9124〜1' in FZ, 'Wilson の上端の表示「1」と再現の記録のごくわずかな超過（X04）')
put('adoption_secret_unchecked', '進みの記録に秘密が無いことは、まだ機械で確かめていない' in ADOPT, '進みの記録に秘密が無いことは、まだ機械で確かめていない' in ADOPT, '採否の表は秘密の確かめを「まだ機械で確かめていない」と書いた（X02）')
st_line = [x for x in D2.split('\n') if x.startswith('- 状態: ')]
put('draft2_status_and_sheet', {'status': st_line, 'sheet_line': [x for x in D2.split('\n') if '最終の系統外の一票はこの後' in x]},
    st_line == ['- 状態: **報告の草案の二つ目**（結果の巡の後・最終の系統外の一票の前）。'] and any('最終の系統外の一票はこの後' in x for x in D2.split('\n')), '状態の行は「最終の系統外の一票の前」・検分票は「最終の系統外の一票はこの後」（X01）')
BRsrc = open(P('tools', 'build_report_Bprime.py'), encoding='utf-8').read()
tmpl = C['report_rules']['template']
put('frozen_builder_status_types', {'canon_template_line': [x for x in tmpl if '登録者最終確認の前と後' in x], 'builder_status_keys': sorted(set(re.findall(r"\('(status_\w+)'", BRsrc)))},
    any('登録者最終確認の前と後の二つの型' in x for x in tmpl) and set(re.findall(r"\('(status_\w+)'", BRsrc)) == {'status_draft'},
    '（コーディネータの照らし）正本は状態を登録者最終確認の前と後の二つの型と定めるが、凍結した組み立ての器が持つ状態の型は草案の型だけ')
assert not os.path.exists(OUT), OUT
res = {'kind': 'bprime_final_vote_repro', 'tool': 'make_repro_final_Bprime.py v0.1', 'vote': 'votes/grok-4.7/response.md', 'checks': out,
       'n': len(out), 'n_ok': sum(1 for v in out.values() if v['ok']),
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
print('再現 %d 項のうち合 %d' % (res['n'], res['n_ok']))
for k, v in out.items():
    if not v['ok']:
        print('合わない:', k, json.dumps(v['got'], ensure_ascii=False)[:200])
