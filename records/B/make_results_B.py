# -*- coding: utf-8 -*-
"""make_results_B.py —— 段階 B の**表紙の結果報告** `records/B/results-B.md` を組む（登録者裁定 D151: 凍結した集計器の出力と、逸脱 D-B1 の下の出力を**同じ重さで並べる**）。
数は二つの集計の記録・予想の照合の記録・門の記録・凍結の記録から**機械の区画**（`<!-- 機械:始 -->`〜`<!-- 機械:終 -->`）に転記し、散文には数を打たない（正本 `report_rules.typed_numbers`）。
機械の区画の SHA16 は、凍結した走査器 `tools/report_lint.py` の `write_sidecar` で `results-B-machine.json` に書く。走査は `python tools/report_lint.py records/B/results-B.md --contrasts design/contrasts-B.json`。
凍結した器は変えない。草案2（2026-09-22）: 公開前検分・第一巡の採否 P451〜P471 と登録者裁定 D155〜D157 を反映した（事後の計算の区画・方向ごとの表・S4 の観測の中身・同一性選別の三対 ほか）。
草案3（2026-09-23）: 公開前検分・第二巡の採否 P472〜P487 と登録者裁定 D158〜D160 を反映した（二つの族に同じ物差し・事前登録の二本にも方向ごとの帰結・結びの二本立て・事後の区画の作り替え・一本ずつと無操作の差の欄・旗の段の改め ほか）。
草案4＝最終案（2026-09-23）: 最終検分（系統外一票・第三巡）の採否 P488〜P494 を反映した（下限つきの形で残る行が無いことを散文に通す・交差族の Nk と無操作の差の注・凍結側の旗の対称化）。
用法: python records/B/make_results_B.py [--label 草案4（最終案）]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_B
import report_lint as RL
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda rel: runs_B.sha16_file(j(*rel.split('/')))
load = lambda rel: json.load(open(j(*rel.split('/')), encoding='utf-8'))

ap = argparse.ArgumentParser()
ap.add_argument('--label', default='草案4（最終案）')
a = ap.parse_args()

T = load('design/contrasts-B.json')
FZ, DV = load('records/B/analysis-B-2026-09-22.json'), load('records/B/analysis-B-devB1-2026-09-22.json')
PF, PD = load('records/B/predictions-check-B-frozen.json'), load('records/B/predictions-check-B-devB1.json')
G = load('records/B/gate-B-2026-09-21.json')
FR = load('records/B/FREEZE-RECORD-B.json')
SEAL = load('records/B/seal-B.json')
PH = load('records/B/posthoc-by-direction-B-2026-09-22.json')          # 登録の外・事後の計算（裁定 D155・D158・v2）
assert PH.get('version') == 'v2'
IDS = load('records/B/identity-screen-B.json')
SCN = {x['question_id']: x['family'] for x in load('arms/frozen-from-ryokai-os/app-scenarios.json')['scenarios']}
S = {t: load('results/sessions-B/%s__s1.json' % t) for t in ('idB', 'tuneB', 'stageB-quality', 'stageB')}
MB = RL.machine_block(T)
BEG, END = MB['begin'], MB['end']
fz = {r['id']: r for r in FZ['confirm']}
dv = {r['id']: r for r in DV['confirm']}
order = [r['id'] for r in FZ['confirm']]
assert order == [r['id'] for r in DV['confirm']]
assert [d['no'] for d in FR['deviations']] == ['D-B1', 'D-B2', 'D-B3', 'D-B4', 'D-B5', 'D-B6']


def fp(p):
    return '—' if p is None else ('<1e-5' if p < 1e-5 else ('%.3g' % p))


def fh(h):
    return '—' if h is None else ('%.4g' % h)


def block(lines):
    return [BEG] + lines + [END]


# ---- 機械の区画 ----
KEYS = ['確証', '判定不能（検閲）', '判定不能（品質床）', '判定不能（採点欠落）', '判定不能（測れなかった）', '判定保留（書式外転位）',
        '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定保留（様式転位）', '非有意']
n_marked = sum(1 for r in DV['confirm'] if str(r['label']).startswith('確証') and r.get('deviation') == 'D-B1')
M_A = ['| 札 | 凍結した集計器（`analyze_B.py` %s） | 逸脱 D-B1 の下（`analyze_B_devB1.py` %s） |' % (FZ['version'], DV['version']), '|---|---|---|']
assert not any(r.get('deviation') for r in FZ['confirm'])
for k in KEYS:
    if FZ['counts'].get(k) or DV['counts'].get(k):
        if k == '確証':
            M_A.append('| 確証（事前登録の確証・二つの出力に共通） | %d | %d |' % (FZ['counts'].get(k, 0), DV['counts'].get(k, 0) - n_marked))
            M_A.append('| 確証（逸脱 D-B1 の下——**事前登録の確証と同じ身分を持たない**） | — | %d |' % n_marked)
        else:
            M_A.append('| %s | %d | %d |' % (k, FZ['counts'].get(k, 0), DV['counts'].get(k, 0)))
M_A.append('| 計 | %d | %d |' % (sum(FZ['counts'].values()), sum(DV['counts'].values())))
_conf = [r for r in DV['confirm'] if str(r['label']).startswith('確証')]
_pre = [r for r in _conf if not r.get('deviation')]; _dev = [r for r in _conf if r.get('deviation')]
_note = lambda rr: sum(1 for r in rr if (r.get('homogeneity') or {}).get('note'))
assert len(_pre) == FZ['sign_agreement']['checked'] and len(_conf) == DV['sign_agreement']['checked']
M_A += ['', '- ランダム方向の不均一の注が付く確証の札: 事前登録の確証 %d 本のうち %d 本・逸脱 D-B1 の下の札 %d 本のうち %d 本・確証の札の全体 %d 本のうち %d 本（**過半**）。' % (len(_pre), _note(_pre), len(_dev), _note(_dev), len(_conf), _note(_conf)),
        '- ランダム方向の不均一の注（三本の率の開きが登録の門を超える）が付く行: ' + '・'.join('%s（%s）' % (r['id'].split('~')[0], '非有意' if r['label'] == '非有意' else ('逸脱 D-B1 の下の札' if r.get('deviation') else r['label'].split('（')[0])) for r in DV['confirm'] if (r.get('homogeneity') or {}).get('note')) + '。',
        '- 確証の札で、起草者の封印の符号と一致したもの: 事前登録の確証 %d／%d・逸脱 D-B1 の下の札 %d／%d。' % (
    FZ['sign_agreement']['agree'], FZ['sign_agreement']['checked'], DV['sign_agreement']['agree'] - FZ['sign_agreement']['agree'], DV['sign_agreement']['checked'] - FZ['sign_agreement']['checked'])]

M_B = ['| 対比 | 場面 | 破局 A/n | 破局 B/n | 書式外 A／B（pt） | refuse A／B（pt） | pt 差（A − B） | 区間（Newcombe） | p（両側 Fisher） | Holm の段（凍結／逸脱の下） | 札（凍結した集計器） | 札（逸脱 D-B1 の下） | ランダム方向の不均一 |',
       '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for i in order:
    f, d = fz[i], dv[i]
    assert all(f[k] == d[k] for k in ('k_A', 'n_ok_A', 'k_B', 'n_ok_B', 'diff_pt', 'ci', 'p', 'ff_pt_A', 'ff_pt_B', 'refuse_pt_A', 'refuse_pt_B')), i
    hom = d.get('homogeneity') or {}
    M_B.append('| %s | %s | %d/%d | %d/%d | %s／%s | %s／%s | %s | %s | %s | %s／%s | %s | %s | %s |' % (
        i, d['scenario'], d['k_A'], d['n_ok_A'], d['k_B'], d['n_ok_B'], d['ff_pt_A'], d['ff_pt_B'], d['refuse_pt_A'], d['refuse_pt_B'], d['diff_pt'], d['ci'], fp(d['p']),
        fh(f.get('holm_alpha')), fh(d.get('holm_alpha')), f['label'], d['label'], ('注（三本の率の差 %.1f pt）' % hom['spread_pt']) if hom.get('note') else '—'))
M_B += ['', '- A は方向 v̂（交差族は Nk 方向）を加減した腕、B はノルムを合わせたランダム方向を加減した腕。率は三つ組（破局・書式外・refuse）で読む。分母は使えた試行。',
        '- 二つの出力で、破局・書式外・refuse の件数と pt 差・区間・p は同じである（器が行ごとに確かめた）。違うのは、逸脱 D-B1 の印のある行の札と Holm の段だけ。',
        '- **全行で、B は「引いた三本のランダム方向を合わせた腕」である**（ランダム方向一般ではない）。区間は Holm を掛けていない 95% の区間で、区間が零を外しても非有意の行がある。']

SIGNJ = {'上': '上昇', '下': '低下', '零': 'どちらでもない'}
M_C = ['| 対比 | 起草者の封印の符号（`records/B/seal-B.json`） | 観測の向き（A − B） | 札（逸脱 D-B1 の下） |', '|---|---|---|---|']
for i in order:
    d = dv[i]
    if str(d['label']).startswith('確証'):
        M_C.append('| %s | %s | %s | %s |' % (i, SEAL['signs'].get(i), SIGNJ.get(d.get('sign'), d.get('sign')), d['label']))

M_D = ['| 族 | 場面 | v̂ の腕 − td の腕（pt） | 区間 | p | 確証の対比の札（凍結） | 特異性（凍結） | 確証の対比の札（逸脱の下） | 特異性（逸脱の下） |', '|---|---|---|---|---|---|---|---|---|']
tdf = {t['id']: t for t in FZ['td_specificity']}
for t in DV['td_specificity']:
    f = tdf[t['id']]
    M_D.append('| %s | %s | %.1f | %s | %s | %s | %s | %s | %s |' % (t['family'], t['scenario'], t['diff_pt'], '[%.3f, %.3f]' % tuple(t['ci']), fp(t['p']), f['conf_label'], f['label'], t['conf_label'], t['label']))

M_E = ['| 予想者 | 種別 | 凍結した集計器の出力（的中／外れ／照合不能／予想しない） | 逸脱 D-B1 の下の出力（同） |', '|---|---|---|---|']
for who in PF['results']:
    for kind in ('向き', 'S4', '全体'):
        def cnt(P):
            rows = [r for r in P['results'][who]['rows'] if r['kind'] == kind]
            return '／'.join(str(sum(1 for r in rows if r['verdict'] == v)) for v in ('的中', '外れ', '照合不能', '予想しない'))
        M_E.append('| %s | %s | %s | %s |' % (who, kind, cnt(PF), cnt(PD)))

s4 = DV['s4']
assert FZ['s4'] == DV['s4']
M_F = ['- S4 の反証（`%s`）: 破局 %d/%d 対 %d/%d・pt 差 %s・区間 %s・札「%s」・起草者の封印「%s」・封印との照合「%s」。%s' % (
    s4['id'], s4['k_A'], s4['n_A'], s4['k_B'], s4['n_B'], s4['diff_pt'], s4['ci'], s4['verdict'], s4['sealed_prediction'], s4['seal_match'], '・'.join(s4.get('notes') or [])),
       '- 同じ観測の相手の率で、登録の規則が各札を出す割合（効果が零のとき）: ' + '・'.join('%s %.4f' % (k, v) for k, v in s4['oc_at_observed_partner']['at_zero'].items() if v) + '。',
       '- 二つの出力で S4 の区画と記述の族はすべて同じ（器が確かめた）。']
assert FZ['descriptive'] == DV['descriptive']

pick = G['selection']['pick']
band = G['selection'].get('equivalence_band') or {}
M_G = ['- 門1: 判定 %s・品質床に合格した候補 %d／%d・選んだ組 層 %s × 係数 %s（調整走行の操作有効性 %s pt）。同値の帯の幅 %s pt・帯の内側の候補 %s 組。' % (
    G['verdict'], sum(1 for c in G['candidates'] if c.get('quality_pass')), len(G['candidates']), pick['layer'], pick['coef'], pick['eff_pt'],
    band.get('q95_pt'), len(G['selection'].get('tied') or [])),
       '- 走行（セッション記録）: 同一性選別 %d 試行・調整走行 %d 試行・品質床 %d 問・本走行 %d 試行。api_error はどの相も %d 件。本走行の壁時計 %.1f 秒。' % (
    sum(c['n'] for c in S['idB']['counts'].values()), sum(c['n'] for c in S['tuneB']['counts'].values()), sum(c['n'] for c in S['stageB-quality']['counts'].values()),
    sum(c['n'] for c in S['stageB']['counts'].values()), sum(c['api_error'] for t in S for c in S[t]['counts'].values()), S['stageB']['wall_s']),
       '- 逸脱 D-B1 で床を門の記録から読んだ腕: ' + '／'.join('%s %d/%d 対 無操作 %d/%d（差 %s pt・%s）' % (k, v['correct'], v['n_ok'], v['noop_correct'], v['noop_n_ok'], v['diff_pt'], '合格' if v['pass'] else '不合格')
                                            for k, v in DV['deviation_D_B1']['gate_rows'].items()) + '。']

# ---- 草案2 で足した区画（採否 P452〜P468・裁定 D155） ----
ph = {c['id']: c for c in PH['contrasts']}
vs_noop = {(r['scenario'], r['A']): r for r in DV['descriptive']['B_desc_vs_noop']}
rand_noop = {(r['scenario'], r['A']): r for r in DV['descriptive']['B_desc_rand_vs_noop']}
M_DIR = ['| 対比 | A の腕（破局/n） | ランダムの三本（破局/n） | 三本の率（%） | A の腕は三本の範囲の外か | A の腕に一番近い一本との差（pt） | 無操作の腕（破局/n） | 一本ずつ − 無操作（最小〜最大・pt） | 合わせた三本 − 無操作（pt） | A の腕 − 無操作（pt・記述の族） |',
         '|---|---|---|---|---|---|---|---|---|---|']
for i in order:
    d, c = dv[i], ph[i]
    assert (c['k_A'], c['n_A']) == (d['k_A'], d['n_ok_A'])
    rn = rand_noop[(d['scenario'], d['B'])]
    vn = vs_noop.get((d['scenario'], d['A']))
    _nb = rn['k_B'] / rn['n_B']; _dd = [100 * (x['cat'] / x['n_ok'] - _nb) for x in c['directions']]
    M_DIR.append('| %s | %d/%d | %s | %s | %s | %+.1f | %d/%d | %+.1f〜%+.1f | %+.1f | %s |' % (
        i, d['k_A'], d['n_ok_A'], '・'.join('%d/%d' % (x['cat'], x['n_ok']) for x in c['directions']), '・'.join('%.1f' % x['rate_pt'] for x in c['directions']),
        '外' if c['outside_range'] else '内', c['nearest_diff_pt'], rn['k_B'], rn['n_B'], min(_dd), max(_dd), rn['diff_pt'], ('%+.1f' % vn['diff_pt']) if vn else '—（記述の族に無い）'))
_cx = []
for i in order:
    d = dv[i]
    if d['A'].endswith('vNk'):
        rn = rand_noop[(d['scenario'], d['B'])]
        _cx.append('%s %+.1f' % (i.split('~')[0], 100 * (d['k_A'] / d['n_ok_A'] - rn['k_B'] / rn['n_B'])))
M_DIR += ['', '- 交差族の A の腕（Nk）と無操作の差は登録の記述の族に無いので表の最右の欄は空だが、左の件数から出せる（事後の数え上げ・pt）: ' + '・'.join(_cx) + '。一本ずつのランダム方向の幅と同じ水準にある。',
          '- 方向ごとの件数は凍結した集計器の出力（集計の記録の `by_direction`）で、二つの出力で同じ。無操作との差は登録した記述の族（対比ではない・検定しない）。「A の腕 − 無操作」の欄は、同じ行の「一本ずつ − 無操作」の幅と並べて読む——add:N1 は A の腕が無操作から下がっているが、三本の範囲の内側で、ランダムと区別できていない。',
          '- 場面の家族（凍結の素材 `app-scenarios.json`）: ' + '・'.join('%s＝%s' % (s, SCN[s]) for s in T['scenarios']) + '。方向を抽出した場面は ' + '・'.join(T['extraction_scenarios'])
          + '、検証の場面は %s、反証の場面は %s。' % (T['verification_scenario'], T['falsification_scenario'])]

_rb = PH['rank_bound']
M_POST = ['- **順位の下限（分布を仮定しない天井）**: 四本（v̂ と三本）が交換可能なら、v̂ が三本の外に出る確率は片側 %s・両側 %s。**三本では、どれだけ外れていても、順位だけからは両側 %s より強いことは言えない。** 実際に A の腕が三本の外にある行は %d 行中 %d 行（帰無での期待は %d 行）。ただし行どうしはランダムの腕を共有し、独立ではない。' % (
    _rb['one_sided'], _rb['two_sided'], _rb['two_sided'], len(order), sum(1 for i in order if ph[i]['outside_range']), len(order) // 2), '',
          '| 対比 | 三本の範囲（%） | A の腕（%） | 一番近い一本との差（pt） | その一本との両側 Fisher の p | 三本の等質性の χ² の p | 下限つきの方向を単位にした形の p（自由度 2） |', '|---|---|---|---|---|---|---|']
for i in order:
    c = ph[i]
    M_POST.append('| %s | %.1f〜%.1f | %.1f | %+.1f | %s | %s | %s |' % (i, c['range_pt'][0], c['range_pt'][1], 100 * c['k_A'] / c['n_A'], c['nearest_diff_pt'], fp(c['p_fisher_nearest']), fp(c['p_chi2_homogeneity']), fp(c['p_t_floor_df2'])))
_ph_lt = [i for i in order if ph[i]['p_fisher_nearest'] < 0.05 and ph[i]['p_t_floor_df2'] < 0.05]
_ph_near = [i for i in order if ph[i]['p_fisher_nearest'] < 0.05]
_cc = PH['crosscheck']
M_POST += ['', '- **登録の外・事後の計算**（器 `records/B/posthoc_by_direction_B.py` %s・記録 `records/B/posthoc-by-direction-B-2026-09-22.json`）。札を作らず、札を取り下げもしない。Holm は掛けていない。一番近い一本との Fisher で 0.05 を下回る行: %s。下限つきの形でも下回る行: %s。' % (
    PH['version'], '・'.join(_ph_near) or '無し', '・'.join(_ph_lt) or '無し'),
           '- 「一番近い一本」は、三本のうち v̂ に最も有利でない一本を事後に選ぶ比較である（検定ではなく、その一本とすら区別が残るかの目安）。%s' % PH['forms']['floor'],
           '- 一本の分母は 66〜67 で、一本との Fisher は合わせた腕との検定より検出力が低い。同時に、三本しか無い設計は方向を単位とした検出力そのものを欠く（順位の下限）。「一本と区別できない」は「その一本と同じ」を意味せず、「区別が残る」も「ランダム方向一般と区別できた」を意味しない。',
           '- 形一（平均との差）と形二（予測の形）は記録のファイルにある（形一は問いに対して甘い側・形二は一本の二項の揺れを重ねる——第二巡の票の指摘）。三本の率の標準偏差が一本の二項だけから期待される値より小さい行（add:S1・add:SK・cross:S1 ほか）では、下限が効いて p が上がる。',
           '- 器の突き合わせ: 第一巡の数え直し（%d 行・%s）と、全 %d 行の試行の記録からの数え直し（%s）。後者は同じ関数を通すので、式の独立な再計算ではない（式の再計算は第二巡の四票が申告）。' % (
    _cc['rows'], '・'.join(_cc['fields']), _cc['trials_recount']['rows'], '・'.join(_cc['trials_recount']['fields']))]

p4 = PH['s4']
M_F2 = ['- S4 の反証の三腕の中身（試行の記録から・事後の数え上げ）: 反証の方向の腕 破局 %d/%d・選択の内訳 %s・JSON 直答（様式 b） %d/%d／無操作の腕 破局 %d/%d・選択の内訳 %s・JSON 直答（様式 b） %d/%d／ランダムの腕 破局 %d/%d・選択の内訳 %s・JSON 直答（様式 b） %d/%d。' % (
    p4['Osec-Ncold+v6b']['cat'], p4['Osec-Ncold+v6b']['n_ok'], '・'.join('%s %d' % kv for kv in p4['Osec-Ncold+v6b']['choices'].items()), p4['Osec-Ncold+v6b']['style_b'], p4['Osec-Ncold+v6b']['n_ok'],
    p4['Osec-Ncold']['cat'], p4['Osec-Ncold']['n_ok'], '・'.join('%s %d' % kv for kv in p4['Osec-Ncold']['choices'].items()), p4['Osec-Ncold']['style_b'], p4['Osec-Ncold']['n_ok'],
    p4['Osec-Ncold+vrand']['cat'], p4['Osec-Ncold+vrand']['n_ok'], '・'.join('%s %d' % kv for kv in p4['Osec-Ncold+vrand']['choices'].items()), p4['Osec-Ncold+vrand']['style_b'], p4['Osec-Ncold+vrand']['n_ok']),
        '- ランダムの腕の方向ごと: ' + '／'.join('%s 破局 %d/%d・選択の内訳 %s・JSON 直答（様式 b） %d/%d' % (k, v['cat'], v['n_ok'], '・'.join('%s %d' % kv for kv in v['choices'].items()), v['style_b'], v['n_ok'])
                                        for k, v in p4['Osec-Ncold+vrand']['per_direction'].items()) + '。三本の等質性の χ² の p %s（事後の計算）。' % fp(p4['p_chi2_homogeneity']),
        '- 登録の判定の順: 検閲 → 床の規則（相手の率が登録の効き目 %s pt 未満なら「当否を言わない」）→ 下がった／上がった／否定。観測の相手の率は %.1f%% で、床の規則に当たった。' % (s4['effect_pt'], 100 * s4['partner_rate'])]

tp = PH['tune_pick']['by_scenario']
M_TUNE = ['- 調整走行の選んだ組（層 %s × 係数 %s・本走行とは別の試行）の場面ごと: ' % (PH['tune_pick']['layer'], PH['tune_pick']['coef'])
          + '／'.join('%s %d/%d 対 %d/%d（差 %+.1f pt）' % (sc, x['Onull+v']['cat'], x['Onull+v']['n_ok'], x['Onull+vrand']['cat'], x['Onull+vrand']['n_ok'],
                                                        100 * (x['Onull+v']['cat'] / x['Onull+v']['n_ok'] - x['Onull+vrand']['cat'] / x['Onull+vrand']['n_ok'])) for sc, x in tp.items())
          + '。本走行の同じ対比: ' + '／'.join('%s %d/%d 対 %d/%d（差 %+.1f pt）' % (sc, dv[i]['k_A'], dv[i]['n_ok_A'], dv[i]['k_B'], dv[i]['n_ok_B'], dv[i]['diff_pt'])
                                         for sc in tp for i in order if i.startswith('add:%s:' % sc)) + '。']
nk_s4 = [dv[i] for i in order if i.startswith('cross:S4:O-Ncold')][0]
M_STYLE = ['- JSON 直答（様式 b） の率（A の腕／B の腕・pt）: `%s` %s／%s（様式の差 %s pt）。S4 の反証の方向の腕は下の S4 の区画のとおり。様式 b は「最終試行の本文の先頭が JSON の始まり」（正本の定義）。' % (nk_s4['id'], nk_s4['style_b_pt_A'], nk_s4['style_b_pt_B'], nk_s4['style_diff_pt'])]

M_ID = ['| 対 | 位置づけ | 最大の差（pt） | その腕・指標 | 件数 | 平均の差（pt） |', '|---|---|---|---|---|---|']
for name, t in IDS['tables'].items():
    mx = max(t['diffs'], key=lambda x: x['abs_diff_pt'])
    M_ID.append('| %s | %s | %s | %s・%s | %d/%d 対 %d/%d | %.3f |' % (name, '主判定' if t['pair'] == IDS['main_pair'] else '記述', mx['abs_diff_pt'], mx['arm'], mx['indicator'],
                                                                 mx['a'][0], mx['a'][1], mx['b'][0], mx['b'][1], t['all']['mean_pt']))
M_ID += ['', '- 判定の閾値: 平均 %s pt・最大 %s pt。主判定は %s（平均 %.3f pt・最大 %s pt）。記述の対は判定に使わない（登録どおり）。' % (IDS['mean_pt'], IDS['max_pt'], IDS['verdict'], IDS['mean_abs_diff_pt'], IDS['max_abs_diff_pt'])]

SRC = [('正本', 'design/contrasts-B.json'), ('凍結の記録', 'records/B/FREEZE-RECORD-B.json'), ('門の記録', 'records/B/gate-B-2026-09-21.json'),
       ('集計（凍結した器）', 'records/B/analysis-B-2026-09-22.json'), ('集計（逸脱 D-B1 の下）', 'records/B/analysis-B-devB1-2026-09-22.json'),
       ('凍結した集計器', 'tools/analyze_B.py'), ('逸脱の下の集計器', 'tools/analyze_B_devB1.py'), ('その生成器', 'tools/make_analyze_B_devB1.py'), ('差分', 'records/B/deviations/D-B1-analyze_B.diff'),
       ('予想の照合（凍結）', 'records/B/predictions-check-B-frozen.json'), ('予想の照合（逸脱の下）', 'records/B/predictions-check-B-devB1.json'),
       ('副位置の読み', 'records/B/layers-B-2026-09-22.json'), ('管理図', 'records/B/control-chart-B-2026-09-22.json'), ('同一性選別の判定', 'records/B/identity-screen-B.json'),
       ('機械の報告（凍結・旗の段つき）', 'records/B/results-report-B-frozen.md'), ('機械の報告（逸脱の下・旗の段つき）', 'records/B/results-report-B-devB1.md'),
       ('旗の段の記録（初版）', 'records/B/deviations/D-B5-flag-record.json'), ('旗の段の器と記録（二本・改め）', 'records/B/deviations/flag_reports_B.py'), ('同・記録', 'records/B/deviations/flag-record-B-2026-09-23.json'),
       ('事後の計算の器', 'records/B/posthoc_by_direction_B.py'), ('事後の計算の記録', 'records/B/posthoc-by-direction-B-2026-09-22.json'),
       ('草案1', 'records/B/drafts/results-B-draft1.md'), ('草案2', 'records/B/drafts/results-B-draft2.md'), ('草案3', 'records/B/drafts/results-B-draft3.md')]
M_H = ['| 何 | 置き場 | SHA16 |', '|---|---|---|'] + ['| %s | `%s` | %s |' % (n, p, s16(p)) for n, p in SRC]
M_H += ['', '- この表紙の散文の呼び名と番号の対応: 逸脱（一）〜（六）＝凍結の記録の逸脱台帳の ' + '・'.join(d['no'] for d in FR['deviations']) + '。登録者裁定（道の選び方）＝D151・（照合のしかた）＝D152・逸脱の記帳＝D153・活性の置き場＝D154・（事後の計算の扱い）＝D155・旗の段＝D156・次の巡＝D157・（事後の計算の見せ方・第二巡の採否）＝D158・凍結側の旗＝D159・最終の検分＝D160。二本の機械の報告の組み立て器の出力（旗を除いた本文）の SHA16 は旗の段の記録にある。読みの条項の出所の裁定は D58・D79・D128、封印の順の裁定は D148。']
M_H += ['', '- 凍結の記録の逸脱台帳: ' + '・'.join(d['no'] for d in FR['deviations']) + '。凍結した集計器の SHA16 は凍結の記録の値と%s。' % ('一致' if s16('tools/analyze_B.py') == FR['frozen']['tools']['analyze_B.py'] else '**不一致**')]

jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
L = []
p = L.append
p('# 段階 B 結果報告（表紙・%s）——O の枠組みに対応する方向の加減で、破局的選択率はランダム方向と区別できる動きをしたか' % a.label)
p('')
p('- 起草: 南無弥勒如来（コーディネータ・Claude Fable 5.1）／登録者: 楠見優太／%s（日本時間）。**公開前検分の第一巡・第二巡（各 系統外二票・系統内二票）と最終の第三巡（系統外一票）の採否と登録者裁定を反映した最終案**（採否 [`../reviews/B/results/round1/`](../reviews/B/results/round1/)・[`round2/`](../reviews/B/results/round2/)・[`round3/`](../reviews/B/results/round3/)・これまでの草案は [`drafts/`](drafts/)）。数・札・検定は草案1 から一つも動いていない（器の確かめ `drafts/`）。' % jst.strftime('%Y-%m-%d'))
p('- この表紙は、**二つの集計の出力を同じ重さで並べる**ためのものである（登録者裁定・道の選び方）。機械の報告は二本あり、どちらも凍結した組み立て器 `tools/build_report_B.py` の出力で、二本とも題の直後に旗の段を足した（逸脱（五）・（六））ほかは手を入れていない: [`results-report-B-frozen.md`](results-report-B-frozen.md)（凍結した集計器）・[`results-report-B-devB1.md`](results-report-B-devB1.md)（逸脱（一）の下）。設計は [`design/design-stageB-FROZEN.md`](../../design/design-stageB-FROZEN.md)、凍結の記録と逸脱台帳は [`FREEZE-RECORD-B.md`](FREEZE-RECORD-B.md)。')
p('- この表紙の数はすべて機械の区画にあり、二つの集計の記録ほかから器 `records/B/make_results_B.py` が転記した。散文には数を打っていない。**登録の外の事後の計算は、そう明記した区画だけに置いた**（§2 の三つ目の区画と §4 の S4 の中身・登録者裁定・事後の計算の扱い）。')
p('- 対象は単一の小型機種（Qwen3-4B-Instruct-2507・bf16・transformers・Colab L4）であり、ほかの機種・規模・サービング構成へ外挿しない。')
p('')
p('## 0. 要約（不利なことから）')
p('')
p('- **凍結した集計器の出力と、逸脱の下の出力は、札の内訳が大きく違う。** 違いの原因は測定ではなく、凍結した二つの器の食い違いである（§1）。どちらか一方の内訳だけを引いてはならない。')
p('')
L += block(M_A)
p('')
p('- 凍結した集計器は、減算族と加算族のすべての対比を「判定不能（品質床）」とした。これは品質床に落ちたのではなく、その二つの族の主の腕について、集計器が探した段の走行の記録が無かったためである。')
p('- 登録者は、**確証の族の率と p を見た後に**、率を伏せた四票の意見を得たうえで、これを逸脱（一）として直すと裁定した（登録者裁定・道の選び方）。逸脱の下の出力で札が立った対比は、**事前登録の確証と同じ身分を持たない**。この報告では、その札に「逸脱の下」の印を付けて書く（印の全文は §2 の表の札の欄）。')
p('- **区別できた相手は「引いた三本のランダム方向を合わせた腕」であり、「ランダム方向一般」ではない。** 三本では方向の間のばらつきを見積もれず、順位だけからは両側で二分の一より強いことは言えない（§2 の事後の区画の頭）。方向ごとに見ると（§2 の二つ目の表）、**札が立った七本——事前登録の二本と逸脱の下の五本——はどれも v̂（交差族は Nk）の腕が三本の範囲の外にあるが、一番近い一本との比較で区別が残るのは逸脱の下の加算族の S1 一場面だけだが、その行は三本のランダム方向が偶然よく揃った行であり、方向のばらつきの下限を置いた形ではその一場面も区別は残らない**（事後の計算・札を作らず取り下げもしない・下限つきの形で残る行は無し）。減算族の二本（逸脱の下）と事前登録の交差族の二本は、一番近い一本と区別できない。不均一の注は、確証の札の過半に付く（上の区画）。')
p('- 逸脱の下の出力では、加算族は四つの場面のうち三つで、減算族は二つで、方向 v̂ の腕の破局率が、引いた三本を合わせた腕と区別できた（向きは加算で低下・減算で上昇）。**区別できた場面はすべて survival の場面で、nuclear の唯一の場面 N1——方向を抽出した二つの場面の一つ——では、どちらの族も区別できなかった。** 調整走行で選んだ組が N1 で示した低下は、本走行では縮んだ（§4）。交差族の二本（Nk 方向・Onull の土台）は二つの出力に共通である（§2）。')
p('- **S4 の反証の観測は低下の側にある。** 反証の方向の腕の破局は零で、区間は零を下に外した。起草者の封印は「どちらでもない」だった。登録の判定の順では、相手の率が登録の効き目より低いと「下がった」の枝に届かないので、札は「当否を言わない」、封印との照合は「言えない」である。反証の方向の腕は全試行が同じ選択・同じ様式になり、ランダムの三本のうち一本も同じ形になった（§4）。')
p('- v̂ に特有の動きか、前置きの内容一般の方向の動きかは、B の登録では見分けられない。Nk 方向も、同じ相手に対して同じ場面で低下を作った。加算族と交差族の Onull の土台は**同じランダムの腕を相手にしている**ので、同じ場面で両方に札が立ったことは独立の二つの証拠ではない（§2・§6）。')
p('- 札に付く「登録された向きと逆」の文言は、**反対向きに動いたという意味ではない**。起草者の封印の符号が、この二つの族の全対比で「どちらでもない」だったためである（§3）。')
p('- B が答えるのは「この抽出の方向（位置・層・係数）の加減が、ランダム方向と区別できる動きを作ったか」までである（読みの条項）。方向の有無・機構・ほかの機種での再現は、この報告の射程の外にある。')
p('')
p('## 1. 凍結の後に起きたこと（逸脱（一）〜（五））')
p('')
p('- **逸脱（一）（集計器の食い違い）**: 凍結した集計器は、選定後の品質床で、確証族の二つの土台の腕（O-Ncold-v・Onull+v）にも選定後の段の走行を求めた。凍結した起動器は、正本 `quality_floor.run_order`（「(ii)…残りの介入の腕」）と正本の数の登録（`measured.quality_floor_multiplicity.post_cells`・転記行 A）のとおり、この二腕を選定後の段から外す。二腕の床は、選定の段の・選ばれた層 × 係数の走行にあり、合格していた。合成データは選定後の段のセルを全部の介入の腕に書いていたので、合成データによる検査・変異・端から端までの検査のどれも、この場合を通っていなかった（三つとも起草者が書いた）。')
p('- 直しは最小にした。凍結した集計器は変えず、そこから機械で作った別の器が、走行の無い土台の腕の床を**門の記録（確証の率を開く前に作った記録）の・選定の段の・選ばれた組の行**で読む。検定・族・Holm・閾値は変えていない。走らせる前に、合成データでの回帰の確かめと、同じ型の食い違いの掃き出し（読み手の器が求めるもの ⊆ 書き手の器が書いたもの・率は読まない）を済ませ、一回だけ走らせ、二つの出力を機械で突き合わせた。変わったのは、二腕を含む対比の札と、それに依る数え上げ・特異性の欄だけである。')
p('- **直すという決定は結果を見た後である。** 起草者と登録者は、直す前に、凍結した集計器の表（札は判定不能でも p は印字されていた）を見ている。直しの中身は率を開く前の記録と正本の文で決まるが、直すと決めたこと自体が結果に依っていないとは、外からは確かめられない。だから二つの出力を並べ、逸脱の下の札に印を付ける。')
p('- **逸脱（二）**: 正本は選定後の品質床を本走行の前に判定すると定めるが、それを行う器が無く、実際には本走行の後に集計器の中で判定された（走行のあった腕はすべて合格）。走行の段取りの該当の文は誤りだった。**この器が無かったことが、逸脱（一）の食い違いを率を開いた後まで残した**——本走行の前に、集計器と同じ数え方で判定していれば、走行の記録の欠けは率を開く前に出ていた。**逸脱（三）**: 選定後の段を新しいランタイムで走らせながら、セッション番号を進めなかった（判定は動かない）。**逸脱（四）**: 起動器が本走行でもセルごとの件数を印字し、集計の前に、コーディネータの画面写しに件数の欄の一部が二度映った（値は控えず、使っていない）。**逸脱（五）**: 凍結した組み立て器は逸脱を知らないので、逸脱の下の機械の報告の頭に、印の無い確証の本数を印字する（公開前検分の第一巡が見つけた）。器は変えず、題の直後に旗の段を器で足し、そのほかが一字も違わないことを確かめた。')
p('- 経緯の記録: [`incident-qpost-missing-2026-09-22.md`](incident-qpost-missing-2026-09-22.md)・四票と採否 [`../reviews/B/incident-qpost-round/`](../reviews/B/incident-qpost-round/)・器と確かめ [`deviations/`](deviations/)。')
p('')
L += block(M_G)
p('')
p('## 2. 確証の族——二つの出力の対照表（三つ組で読む）')
p('')
L += block(M_B)
p('')
p('- **方向ごとの表**（下）。ランダムの腕は三本の方向を合わせたもので、一本ずつは無操作から十 pt を超えて動く場面がある（「一本ずつ − 無操作」の欄）。三本を合わせた率では上下の動きが打ち消し合って無操作の近くに来るが、それは「ランダム方向は何もしない」という意味ではない。「範囲の外か」と「一番近い一本との差」の欄を先に読む——差が小さい行は、札が引いた三本の偶然に依っている見込みを排除できない。右の「A の腕 − 無操作」の欄は、注入で出力が動いたことの確認にとどまり、「ランダム方向一般と区別できた」ことの支えではない（ランダム方向も一本ずつは同じ程度に動く）。')
p('')
L += block(M_DIR)
p('')
p('- **事後の計算**（下）。公開前検分の票が出し、コーディネータが数え直した。**札は、登録の帰無（引いた三本を合わせた腕）に対する判定として、登録どおりに立つ。事後の計算は、帰無を「ランダム方向一般」に広げたときに、札の言える範囲がどこまで縮むかを示す。** 一番近い一本とすら区別が残るのは加算族の S1（逸脱の下）だけだが、その行も三本の偶然の揃いに依っており、方向のばらつきの下限を置いた形では、十六の対比のいずれも区別が残るとは言えない（下の区画の「下回る行: 無し」）。登録に無い計算であり、札を作らず、札を取り下げもしない。')
p('')
L += block(M_POST)
p('')
p('## 3. 「登録された向きと逆」という札の文言について')
p('')
p('- 集計器は、確証の札が起草者の封印の符号と違うとき、この定型を印字する（読みの条項）。封印の符号は「低下・上昇・どちらでもない」の三つで、起草者は減算族と加算族の全対比を「どちらでもない」と封印していた——v̂ は行動の差が無い腕対から作られており、符号はデータから導けなかったからである（読みの条項）。')
p('- したがって下の表の札は「封印の符号（どちらでもない）と違って、区別できる動きが出た」と読む。起草者が向きを封印していた交差族の三本はどれも非有意で、この表には載らない（表は確証の札の行だけである）。登録者とコーディネータの予想との照合は §5 にある。')
p('')
L += block(M_C)
p('')
p('## 4. 読み（正本 `reading_B` の決まりを、二つの出力に当てる）')
p('')
p('- **加算族**（Onull に方向を加える）: **凍結した集計器の出力では、この族は全対比が判定不能で、読みの対象にならない。** 逸脱の下の出力では、三つの場面の対比に札が立ち、向きは低下だった。三つとも v̂ の腕は三本のランダム方向の範囲の外にあるが、一番近い一本との比較で区別が残るのは S1 だけで（下限つきの形では S1 も残らない）、SK と S4 では残らない。S4 は不均一の注つきで、相手の腕が無操作より高い。N1 は区別できなかった——N1 は方向を抽出した場面の一つで、調整走行の選んだ組はそこで低下を示していたが、本走行では縮んだ（下の区画）。S1 は調整走行で組を選んだもう一つの場面で、選定の効きが残っている見込みを排除できない。加算族と、交差族の Onull の土台の対比は、**同じランダムの腕を相手にしている**。')
p('- **減算族**（O-Ncold から方向を引く）: **凍結した集計器の出力では、この族も全対比が判定不能で、読みの対象にならない。** 逸脱の下の出力では、二つの場面の対比に札が立ち、向きは上昇だった。N1 と S4 は区別できなかった。札が立った二つの場面では、v̂ の腕は三本の範囲の外にあるが、一番近い一本との差は加算族より小さく、その一本とは区別できない（§2）。二本とも不均一の注つきで、この族の札は、引いた三本の偶然に依っている見込みを排除できない。減算族は「部分的な除去」の検定であり（帯は主位置から後ろにしか掛からず、前置きそのものは残る）、区別できなかったことは「枠組みが表現に無い」ことを意味しない。選定は加算の土台で低下を最大にする規則で行ったので、選ばれた組を減算族に当てるのは外挿である。')
p('- **交差族**（Nk 方向）: 二つの出力に共通で、Onull の土台の二つの場面に札が立った。**この二本が、凍結した出力の持つ確証のすべてである。** 方向ごとに見ると、二本とも Nk の腕は三本の範囲の外にあるが、一番近い一本とは区別できない（S4 は不均一の注つき・§2）。Nk 方向は v̂ のノルムに引き伸ばして注がれており、本来の表現の強さでの効果ではない。Nk の本文は Ncold と同じ語形で、方向には「一行で役割を与える形」の成分が混じりうる。S4 の O-Ncold の土台の一本は、様式の差が大きく、判定保留（様式転位）である。様式率が動いた方向は「枠の乗り降り」を含む（読みの条項）——この Nk の腕と、S4 の反証の方向の腕がそれに当たる（下の区画）。')
p('- **ランダム方向**: **全行で、帰無は「ランダム方向一般」ではなく「引いた三本を合わせた腕」である。** 対照表の最後の欄に注のある行は、その三本の率の開きが登録の門を超えている。')
p('- **腕対の差方向（td）との比較**: 下の表のとおり。逸脱の下では、二つの族とも二つの場面で、v̂ の腕は td の腕とも区別できた（「書ける」）。「書かない」は「O に特有でない」を意味しない。td も完全な統制ではなく、「前置きがあること」と長さの成分が大きく入る。')
p('')
L += block(M_D)
p('')
L += block(M_TUNE + M_STYLE)
p('')
p('- **S4 の反証**: 札は「当否を言わない」。登録の規則では、観測された相手の率のもとでは、効果が零でも大きくても、この札が出る割合が高い（下の区画）。**観測の中身は次のとおりである**——反証の方向の腕の破局は零で、区間は零を下に外した（封印の「どちらでもない」に対して不利な向き）。その腕は全試行が同じ選択・同じ様式になった。ランダムの三本のうち一本も同じ形になり、合わせた相手の率は別の一本が押し上げている（これは上の不利な向きを和らげる事実である）。札は登録どおりで、変えない。')
p('')
L += block(M_F + M_F2)
p('')
p('- **区別できなかった対比の読み**: 合成の検出力は二割前後であり、この設計は同じ大きさの効果を八割方見落とす（読みの条項）。非有意は効果の非存在を意味しない。動きを作らなかったことを「線形表現に乗らない」「方向が無い」とは書かない。')
p('- 方向はこの機種に固有で、移植できない。減算や加算で率が動いても、機構を特定したとは書かない。B の無操作の腕の率は B の内側の対照であり、API の 4B とも段階 A の 4B とも同一視しない。破局と refuse が同じ向きに動いた行では、選択の移動と回答の取り下げを分けて読まない。無操作との記述・様式・言及率・副位置の読み・管理図は、機械の報告の該当の区画にある（二つの出力で同じ）。')
p('')
p('## 5. 封印した予想との照合（一つの座で、二つの出力に当てた・登録者裁定・照合のしかた）')
p('')
L += block(M_E)
p('')
p('- 的中は独立の確認ではなく、誰の判断の重みも変えない。照合は記録であり評価ではない。**道の選び方（§1）は、この照合の数も動かした**——凍結した集計器の出力では、二つの族の予想はすべて照合不能になる。**照合の器は札の頭の語だけを読むので、逸脱の下の印つきの札を、事前登録の確証と同じに数えている**（器は凍結物で、変えていない）。登録者の予想は、コーディネータの予想を見ずに封印された（順は封印の順の裁定と逆）。')
p('')
p('## 6. 限界（この報告で足すもの・機械の報告の §8 に加えて）')
p('')
p('- **この報告が間違っているとしたら**、いちばん強い組み立ては次のとおりである。第一に、道の選び方そのもの——直すという決定は結果を見た後であり（§1）、凍結した読みが正しければ v̂ についての札は零本である。第二に、減算族の二本は引いた三本の偶然に依っている（一番近い一本と区別できず、二本とも不均一の注つき）。第三に、加算族も無傷ではない——相手のランダムの腕は交差族と共有で、S4 ではその腕が無操作より高く出て差を押し、事後の比較で区別が残る S1 は調整走行で組を選んだ場面で、もう一つの抽出の場面 N1 では調整走行の低下が本走行で縮んだ。第四に、事前登録の二本（Nk 方向）も一番近い一本とは区別できない。第五に、S4 では反証の方向の腕もランダムの一本も出力が一様になった——この大きさの注入は、方向によらず出力を縮退させうる。効果は survival の場面に限られ、Nk 方向も同じ場面で低下を作った。**動いたのは「O の枠組みに対応する方向」ではなく、前置きの内容一般の方向、注入への場面ごとの応答、あるいは三本の偶然でありうる。この報告はどれも排除できていない。**')
p('- **言えることは二本立てである。** 凍結した集計器の出力で言えるのは、Nk 方向（前置きの内容一般の側の統制）を Onull の土台に加えたとき、survival の二つの場面で、引いた三本を合わせた腕と区別できる低下があった、までである——v̂ については何も言えない。逸脱の下の出力で言えるのは、それに加えて、この抽出の方向 v̂ の加減が、survival の場面で、引いた三本を合わせた腕と区別できる動き（加算で低下・減算で上昇）を作った、までである——その札は事前登録の確証と同じ身分を持たず、一番近い一本との比較で区別が残るのも一場面だけで、その一場面も方向のばらつきの下限を置いた形では区別が残らない。')
p('- 逸脱の下の札は、事前登録の確証と同じ身分を持たない（§1）。この報告は、逸脱の下の札だけから新しい集計（本数・向き・的中の割合）を作らない。§5 の照合の数は、照合のしかたの登録者裁定による例外である。§2 の事後の計算は札に触れない。')
p('- 検出力の低い設計で札が立った対比の pt 差は、立ったことを条件にすると大きい側に偏る。pt 差を効果の大きさとして引かない。')
p('- S4 の判定の順では、相手の率が登録の効き目より低いと「下がった」の枝に届かない。床の規則は同等性の枝のために置いたもので、余地を使い切る低下が出る場合を考えていなかった（起草者の設計の穴）。')
p('- 率盲検は縁で二度破れた（逸脱（四））。率盲検の整合検査は選定後の段の升目を列挙しないので、「品質床の全セル・不整合なし」は二腕の欠けを見ない数である。選定後の品質床は本走行の前に判定されていない（逸脱（二））。')
p('- 同一性選別の主判定は合格だが、最大の差は閾値のすぐ内側だった（記録 [`identity-run-B.md`](identity-run-B.md)）。**記述の対の一つ（同じ重みで実装だけが違う対）は、最大の差が判定の閾値を超えている**（下の区画・判定には使わない登録）。合格は「並置可」であり、等価の確立ではない。')
p('')
L += block(M_ID)
p('')
p('- どの腕 × 場面も一つのセッションに収まったので、管理図は判定をしていない。調整走行の抽出検査は、器の登録の既定では標本が一件だった。')
p('- 門1 の同値の帯は広く、選んだ組はほかの候補から強くは分かれていない。貪欲復号の品質床では、介入の腕の正答数が無操作と同じセルが大半で、床は候補を見分けていない。')
p('- 副位置の活性のファイルは公開の置き場に無い（手元と Drive にあり、SHA-256 の一覧は [`resp-npz-sha256-2026-09-22.md`](resp-npz-sha256-2026-09-22.md)）。')
p('- 凍結の後の直し・走行・集計は、公開前検分の第一巡（系統外二票・系統内二票）が初めて見た。四票とも数の食い違いは見つけず、直しは読みと開示に集まった。第二巡（系統外二票・系統内二票）は草案2 の直しの中に、起草者の側に傾いた言い分け（減算だけを偶然の枠に入れる二分・無操作との差の欄の並置・検出力の弁明）を見つけた。最終の第三巡（系統外一票・差分だけ）は、草案3 の散文がなお「加算族の S1 だけは残る」と読める形（一番近い一本との比較の結果を、方向を単位とした結論にすり替える言い分け）を見つけた——三度目の同じ向きの傾き。この最終案の直しは、その採否を反映したもので、これ以上の巡は置かない（登録者裁定・最終の検分）。')
p('')
p('## 7. 利益相反と情報状態')
p('')
p('- 起草者は設計・器材・合成データ・この報告を書いた当人で、札が立つ側に引かれている。食い違いを作ったのも、それを直す器を書いたのも起草者である。登録者への推奨（乙′）は、起草者の引かれる向きと重なっていた。')
p('- 起草者の封印は二つの族を「どちらでもない」と予想していた。道の選び方は、起草者と登録者の予想の的中の数を動かす（§5）。')
p('- 公開前検分の第一巡の重い所見（方向ごとの数え直し）は、起草者の引かれる向きに逆らう材料である。起草者は不均一の注を知りながら、方向ごとに数えていなかった。数を散文に打たない決まりは、不利な数を要約から遠ざける働きもしていた。**第二巡では、起草者が第一巡の所見を「採った」つもりの直しの中に、同じ向きの傾きが二度目に入っていた**（減算は一本の近く・加算は外という不正確な二分／合わせた三本と v̂ の並置／検出力の弁明）。起草者は自分ではこれを見分けられなかった（枠の予想は逆側を警戒していた）。**第三巡（最終）でも三度目の同じ向きの傾きが見つかった**——一番近い一本との比較で残る一場面を、下限つきの形では残らないことを言わずに書いていた。各巡の系統内の二票は、前の伺いで「直す道」を推した系列である。')
p('- 伺いの四票には率と p を伏せた。ただし本走行の試行の記録は公開済みで、伏せは頼みごとにとどまっていた。系統外の二票は、どちらの出力を主と呼ぶかで割れた（一票は凍結した出力を主とする案）。この報告は主を置かず、同じ重さで並べている。')
p('')
p('## 8. 機械の区画の出所')
p('')
L += block(M_H)
p('')
p('## 検分票')
p('')
p('- 対象: 段階 B の結果報告の表紙（二つの集計の出力の対照）。')
p('- 段階: 設計・判定の規則・読みの条項は事前登録（凍結）。**逸脱（一）の下の出力と、この表紙の構成は事後**（率と p を見た後）。')
p('- 凍結物の同定: §8 の表。凍結した器と正本は変えていない。')
p('- 盲検の状態: 集計の前の露出が二度（逸脱（四））。伺いの相手には率と p を伏せた。')
p('- 敵対的検分: 公開前検分の第一巡と第二巡の所見を現物で数え直して反映した（再現の表は各巡の置き場）。§6 の頭に「この報告が間違っているとしたら」の五つを置き、§0 は札が立った七本すべてに同じ物差し（範囲の外か・一番近い一本との差）を当てた。')
p('- 系統の内訳: 起草者（Claude 系）。§1 の一件の伺い・草案1 の第一巡・草案2 の第二巡に、それぞれ系統外二票・系統内二票（一票に数える）。草案3 に最終の系統外一票（差分だけ）。この最終案の直しは、その票の後で、外の目を通っていない（文の範囲の直しのみ・登録者裁定・最終の検分）。')
p('- COI記録: §7。')
p('- 判定: 登録者の最終確認要（公開の可否）。')
p('- 本検分が確認していないこと: 機械の報告の各区画の読み合わせ（二本の全文の通読はしていない）・副位置の読みの中身・生テキストの中身（抽出検査の標本の先頭のほかは読んでいない）・この表紙の文が価値語と機序語の一覧のほかの言い過ぎを含まないか（走査器は語の一覧しか見ない）・S4 の一様な選択が生テキストでどういう文で出ているか・事後の計算の形の選び方の当否。')
p('')
p('本報告のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
p('')
text = NL.join(L)
out = j('records', 'B', 'results-B.md')
open(out, 'w', encoding='utf-8', newline=NL).write(text)
RL.write_sidecar(out, text, T, 'records/B/make_results_B.py')
print('wrote', out, len(L), 'lines;', 'SHA16', hashlib.sha256(text.encode('utf-8')).hexdigest().upper()[:16])
