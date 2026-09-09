# -*- coding: utf-8 -*-
"""synth_M.py v1 —— 追補 M の集計器（analyze_M.py）の全経路を合成データ（人工値・API 不使用）で発火させる検査。
results/_synth/<tag>__<sc>__synth__seedN/cells.json（人工の破局・refuse・答えた分母）、records/M/style-<tag>.json（人工の様式率・層）、records/M/gate-<tag>.json（人工の門）を書き、
analyze_M.py を第一走行 synthM1・第二走行 synthM2 で実行できる形にする。発火させる経路（凍結前の検査項目）:
 確証（上向き・下向き）／非有意／門降格（床・天井）／refuse 転位の保留／様式転位の保留（>30pt）／様式差の注（15〜30pt）／層別（両腕 n≥30）と層別不能／
 固有の札 三段（梵転写のみ・カナのみ・両表記）／M-b 配線（枠付け語に固有・束の差・F4 とは異なる）／M-c 配線（固有・無意味列のみ・-T0 のみ）／連続性 5pt 帯の発火／drift (i)(iii) の発火／
 複製六札（①〜⑥・第一走行保留の札なし）／反証条件 (i)(ii)(iii)（synthNull で発火）／一斉保留の第一の所見（synthStyle）／system_sha 突合の不一致停止（synthBad）。
用法: python tools/synth_M.py && python tools/analyze_M.py --tag synthM1 --tag2 synthM2 --gate records/M/gate-synthM1.json
"""
import os, json, shutil, random
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8')); n = T['n_per_arm']; SC = list(T['scenarios'])
LM = json.load(open(os.path.join(REPO, 'arms', 'panelM', 'SHA-LEDGER-M.json'), encoding='utf-8'))
ALL = T['arms']['preamble'] + [d['name'] for d in T['arms']['system']]
SYS_SHA = {d['name']: (None if d['system'] == 'none' else {'O': 'F3EE60C33F825575', 'Onull': '2123B3CD8586E7DF'}.get(d['system']) or LM['system'][os.path.splitext(d['system'])[0]]) for d in T['arms']['system']}
ROOT = os.path.join(REPO, 'results', '_synth'); shutil.rmtree(ROOT, ignore_errors=True); os.makedirs(ROOT)


def cell(k, ref=0, ff=0, ans_rate=None, sysname=None):
    ans = n - ref - ff
    return {'n': n, 'n_ok': n, 'api_error': 0, 'catastrophe': k, 'catastrophe_n_all': n, 'catastrophe_rate_all': round(k / n, 4), 'refuse': ref, 'format_fail': ff, 'catastrophe_n_answered': ans,
            'catastrophe_rate_answered': (round(ans_rate, 4) if ans_rate is not None else round(k / ans, 4)) if ans else None, 'system_sha': SYS_SHA.get(sysname) if sysname else None}


def style(a, b, jn=None, jc=None, pn=None, pc=None, n_ok=n):
    st = {'json_direct': {'n': jn if jn is not None else 0, 'catastrophe': jc or 0}, 'prose': {'n': pn if pn is not None else n_ok, 'catastrophe': pc or 0}}
    return {'n_ok': n_ok, 'a_rate_final': a, 'b_rate_final': b, 'a_rate_first': a, 'b_rate_first': b, 'strata_final': st}


def write_run(tag, sc, cells, styles):
    d = os.path.join(ROOT, '%s__%s__synth__seed0' % (tag, sc)); os.makedirs(d, exist_ok=True)
    json.dump({'run_key': os.path.basename(d), 'manifest': {'scenario': sc, 'arms': list(cells), 'tag': tag}, 'integrity_ok': True, 'cells': cells}, open(os.path.join(d, 'cells.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return styles


def base_cells(sc, run=1):
    """既定: 全腕を V′ Nk-Ncold 相当の水準に置き、シナリオごとに人工の差を入れる。"""
    vp = T['scenarios'][sc]['vprime_stageVp']; nk = vp['Nk-Ncold']; C = {}; S = {}
    for a in ALL:
        k = nk if a not in ('O-Ncold', 'Onull-Ncold', 'Ncold', 'N') else vp[a]
        if a.startswith('sys'):
            k = vp['O-Ncold']
        C[a] = cell(k, sysname=a if a.startswith('sys') else None); S[a] = style(0.9, 0.1, jn=40, jc=int(k * 0.1), pn=360, pc=int(k * 0.9))
    return C, S


# ---- 第一走行 synthM1
styles1 = {}; styles2 = {}
for sc in SC:
    C, S = base_cells(sc); C2, S2 = base_cells(sc)
    vp = T['scenarios'][sc]['vprime_stageVp']
    if sc == 'N1':   # 床からの上向き: Kan TS 上がる・PS も上がる・MS は上がらない → 段 (1) 立たない（TS~MS 非確証）／Ami は四本立つ（両表記に固有）
        C['KanF1TS-Ncold'] = cell(60); C['KanF1PS-Ncold'] = cell(55); C['KanF1MS-Ncold'] = cell(58); C['KanF1TK-Ncold'] = cell(10); C['KanF1PK-Ncold'] = cell(9); C['KanF1MK-Ncold'] = cell(8)
        C['AmiF1TS-Ncold'] = cell(70); C['AmiF1PS-Ncold'] = cell(10); C['AmiF1MS-Ncold'] = cell(9); C['AmiF1TK-Ncold'] = cell(65); C['AmiF1PK-Ncold'] = cell(8); C['AmiF1MK-Ncold'] = cell(7); C['AmiF1T0-Ncold'] = cell(8)
        # M-b: Dai F2 は F1 と F4 の両方と差（枠付け語に固有）／Ami F2 は F1 とのみ差（束）／Kan F3 は F4 とのみ差
        C['DaiF1T0-Ncold'] = cell(8); C['DaiF2T0-Ncold'] = cell(120); C['DaiF3T0-Ncold'] = cell(9); C['DaiF4T0-Ncold'] = cell(10)
        C['AmiF2T0-Ncold'] = cell(90); C['AmiF4T0-Ncold'] = cell(85); C['KanF3T0-Ncold'] = cell(8); C['KanF4T0-Ncold'] = cell(70)   # Kan F3: F4 とのみ差（F1 とは区別できない）
        # refuse 転位: Mir F2 は全分母で上がるが答えた分母では逆
        C['MirF1T0-Ncold'] = cell(8, ref=0); C['MirF2T0-Ncold'] = cell(60, ref=200, ans_rate=0.02)
        # 様式転位: Kan F2 は F1 と 40pt の様式差（保留）・Ami F3 は 20pt（注）
        C['KanF2T0-Ncold'] = cell(70); S['KanF2T0-Ncold'] = style(0.5, 0.5, jn=200, jc=50, pn=200, pc=20); C['AmiF3T0-Ncold'] = cell(75); S['AmiF3T0-Ncold'] = style(0.7, 0.3, jn=120, jc=40, pn=280, pc=35)
        # M-c: LAmi は PS・MS とも差（固有）／LKan は PS とのみ差
        C['sysLAmi'] = cell(5, sysname='sysLAmi'); C['sysLAmi-PS'] = cell(70, sysname='sysLAmi-PS'); C['sysLAmi-MS'] = cell(72, sysname='sysLAmi-MS'); C['sysLAmi-T0'] = cell(60, sysname='sysLAmi-T0')
        C['sysLKan'] = cell(5, sysname='sysLKan'); C['sysLKan-PS'] = cell(70, sysname='sysLKan-PS'); C['sysLKan-MS'] = cell(7, sysname='sysLKan-MS'); C['sysLKan-T0'] = cell(6, sysname='sysLKan-T0')
        # 第二走行: Ami TS は複製（①）／Kan TS は非有意（②）／Dai F2 は反転（③）／Ami F2 は保留（drift iii 発火のため参照腕を動かす）／sysLAmi-PS は複製
        C2['AmiF1TS-Ncold'] = cell(68); C2['AmiF1PS-Ncold'] = cell(9); C2['AmiF1MS-Ncold'] = cell(10); C2['AmiF1TK-Ncold'] = cell(66); C2['AmiF1PK-Ncold'] = cell(8); C2['AmiF1MK-Ncold'] = cell(7); C2['AmiF1T0-Ncold'] = cell(8)
        C2['KanF1TS-Ncold'] = cell(20); C2['KanF1PS-Ncold'] = cell(15); C2['DaiF2T0-Ncold'] = cell(0); C2['DaiF1T0-Ncold'] = cell(60)
        C2['sysLAmi'] = cell(5, sysname='sysLAmi'); C2['sysLAmi-PS'] = cell(70, sysname='sysLAmi-PS'); C2['sysLAmi-MS'] = cell(72, sysname='sysLAmi-MS')
        C2['MirF3T0-Ncold'] = cell(90)   # ⑤ 第二走行のみ有意
    if sc == 'S1':   # 天井からの下向き: Kan TS・PS・MS が下がる（両表記の段 (2) だけ立つように TK 側のみ）／門: 両腕天井（Dai TS 対 Dai PS）
        C['KanF1TK-Ncold'] = cell(300); C['KanF1PK-Ncold'] = cell(385); C['KanF1MK-Ncold'] = cell(386)
        C['sysLAmi'] = cell(50, sysname='sysLAmi'); C['sysLAmi-T0'] = cell(120, sysname='sysLAmi-T0'); C['sysLAmi-PS'] = cell(52, sysname='sysLAmi-PS'); C['sysLAmi-MS'] = cell(51, sysname='sysLAmi-MS')
        # 連続性 5pt 帯発火（Nk-Ncold が V′ 387 から 340 へ）・drift (i) 発火（O-Ncold と Ncold もずらす）
        C['Nk-Ncold'] = cell(340); C['O-Ncold'] = cell(200); C['Ncold'] = cell(350)
        C2['Nk-Ncold'] = cell(387); C2['KanF1TK-Ncold'] = cell(300)
    if sc == 'S4':   # 全腕天井→門で全降格・層別不能（json 層 n<30）
        for a in ALL:
            S[a] = style(0.0, 1.0, jn=5, jc=5, pn=395, pc=395)
    if sc == 'SK':   # 一斉保留（様式門）: 全対比で A・B の様式差 >30pt
        for i, a in enumerate(ALL):
            S[a] = style(0.95 if i % 2 == 0 else 0.5, 0.05 if i % 2 == 0 else 0.6, jn=200, jc=100, pn=200, pc=100)
            C[a] = cell(300 + (i % 2) * 60, sysname=a if a.startswith('sys') else None)
    styles1[sc] = S; styles2[sc] = S2
    write_run('synthM1', sc, C, S); write_run('synthM2', sc, C2, S2)
os.makedirs(os.path.join(REPO, 'records', 'M'), exist_ok=True)
json.dump({'tag': 'synthM1', 'runs': styles1, 'synthetic': True}, open(os.path.join(REPO, 'records', 'M', 'style-synthM1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'tag': 'synthM2', 'runs': styles2, 'synthetic': True}, open(os.path.join(REPO, 'records', 'M', 'style-synthM2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 門（人工）: S4 は全降格（天井）・他は GO
G = {'tag': 'synthM1', 'synthetic': True, 'results': {}}
for F in T['families'].values():
    for c in F['contrasts']:
        G['results'][c['id']] = {'status': 'downgraded_ceiling', 'reason': '天井（両腕とも ≥39）'} if c['scenario'] == 'S4' else {'status': 'go'}
json.dump(G, open(os.path.join(REPO, 'records', 'M', 'gate-synthM1.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# synthNull: 全腕同率（反証条件 (i)(ii)(iii) の発火）
for sc in SC:
    C, S = base_cells(sc); write_run('synthNull', sc, C, S)
json.dump({'tag': 'synthNull', 'runs': {sc: base_cells(sc)[1] for sc in SC}, 'synthetic': True}, open(os.path.join(REPO, 'records', 'M', 'style-synthNull.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
GN = {'tag': 'synthNull', 'synthetic': True, 'results': {c['id']: {'status': 'go'} for F in T['families'].values() for c in F['contrasts']}}
json.dump(GN, open(os.path.join(REPO, 'records', 'M', 'gate-synthNull.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# synthBad: system_sha 不一致（集計器が停止すること）
C, S = base_cells('N1'); C['sysLAmi']['system_sha'] = 'DEADBEEFDEADBEEF'; write_run('synthBad', 'N1', C, S)
json.dump({'tag': 'synthBad', 'runs': {'N1': S}}, open(os.path.join(REPO, 'records', 'M', 'style-synthBad.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('synthetic runs written under results/_synth（synthM1・synthM2・synthNull・synthBad）')
