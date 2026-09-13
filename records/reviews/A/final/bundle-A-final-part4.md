# 段階 A 凍結前の最終検分 bundle 第 4 部／全 4 部（機械連結・`tools/bundle_final_A.py` v1.1・2026-09-13 23:04 UTC）

- 部品は逐語（LF 正規化）。見出しの SHA16 はファイルバイトの SHA-256 先頭 16 桁（CRLF→LF 正規化）。全部の目次は下の表。

## 目次（全部）

| 部 | 部品 | パス | SHA16 | 字数 |
|---|---|---|---|---|
| 1 | 依頼文（凍結前の最終検分） | `records/reviews/A/final/review-request-A-final.md` | 5318FFE94599264F | 3,127 |
| 1 | 段階 A 設計草案8（凍結候補の三つ目） | `design/design-stageA-draft8.md` | 028728BAC4A9EC8E | 45,594 |
| 1 | 草案8 の原稿（正本のキー参照） | `design/design-stageA-draft8.src.md` | F55218421FC75157 | 26,506 |
| 1 | 報告雛形 A（組み立て） | `records/A/results-report-template-A.md` | 84AE5D0F83E59FC2 | 10,286 |
| 1 | 報告雛形 A の原稿 | `records/A/results-report-template-A.src.md` | A394AD2172A8009C | 10,543 |
| 1 | 運用の解釈の一覧（登録者の確認待ち） | `records/A/tooling-interpretations-A.md` | 58A2A15E25B3B98B | 13,234 |
| 1 | 本文の数の機械検査（草案8） | `records/A/numbers-lint-draft8A.md` | F2F6F734A8B8F305 | 626 |
| 1 | 本文の数の機械検査（雛形） | `records/A/numbers-lint-template-A.md` | 181329A0B37F8EB7 | 642 |
| 1 | 設計事実 A（転記行 A〜O の出所） | `records/A/design-facts-A.md` | 6A722DA8245ACE9F | 20,722 |
| 1 | 正本 contrasts-A.json | `design/contrasts-A.json` | 9A679F0931EF8034 | 89,305 |
| 2 | 検出力格子 A | `records/A/power-grid-A.md` | EAC2645C1652712A | 91,254 |
| 2 | 機種の設定と GPU 容量 hf-models-A.json | `records/A/hf-models-A.json` | D012DE529678C4EE | 2,570 |
| 2 | 門0 の実測 cost-facts | `records/cost-pilot/cost-facts-2026-09-13.md` | DA4C999F6C1C5D89 | 5,177 |
| 2 | 合成検査（集計器）の記録 | `records/A/synth-A-2026-09-14.md` | FAFF9A65F1C066CE | 7,646 |
| 2 | 合成検査（門と校正の器）の記録 | `records/A/synth-gates-A-2026-09-14.md` | 259D2C35FB99B0EC | 1,956 |
| 2 | 草案6 の凍結前検分の採否表（P1〜P74・裁定 D9〜D15） | `records/reviews/A/prefreeze/adoption-table-A-prefreeze.md` | F7E602B7811D7B59 | 24,452 |
| 2 | 手順4 実装検分の依頼文 | `records/reviews/A/draft7-impl/review-request-impl-A.md` | CAF934578A58EABD | 3,701 |
| 2 | 手順4 実装検分の事前登録 | `records/reviews/A/draft7-impl/preregistration-impl-review-A.md` | 8C672D4F749F941B | 2,908 |
| 2 | 手順4 検分者 1 の票（逐語） | `records/reviews/A/draft7-impl/reviewer-1/review.md` | 0F3D98A65D46BDBA | 13,327 |
| 2 | 手順4 検分者 2 の票（逐語） | `records/reviews/A/draft7-impl/reviewer-2/review.md` | 219B87619966D8F5 | 11,619 |
| 2 | 手順4 の採否表（P75〜P104・裁定 D16〜D25） | `records/reviews/A/draft7-impl/adoption-table-impl-A.md` | C10AFE15E6F67C32 | 10,542 |
| 2 | 手順4 再現の検査の記録（W33〜W76） | `records/reviews/A/draft7-impl/verification-impl-A.md` | 1B7A57159F5DEBAB | 5,150 |
| 2 | 手順4 反映の事前登録 | `records/reviews/A/draft7-impl/preregistration-reflection-impl-A.md` | 6C6AA5B6716930FC | 3,916 |
| 2 | 手順4 反映の確かめ（機械生成） | `records/reviews/A/draft7-impl/verification-reflection-impl-A.md` | C5500A44E5FEEDB9 | 4,727 |
| 2 | 手順4 反映の記録 | `records/reviews/A/draft7-impl/reflection-impl-A.md` | 93560389036A0F43 | 6,092 |
| 2 | confirm_A.py | `tools/confirm_A.py` | 5A190C6696C83A6F | 22,812 |
| 2 | bands_A.py | `tools/bands_A.py` | BFF15C1D51957E26 | 4,083 |
| 2 | runs_A.py | `tools/runs_A.py` | A57BE1F5EEACBBB2 | 9,885 |
| 2 | zaxis_A.py | `tools/zaxis_A.py` | 7CEA376E48C38575 | 1,334 |
| 2 | firth.py | `tools/firth.py` | CE584FDF2AE79930 | 11,236 |
| 2 | analyze_A.py | `tools/analyze_A.py` | 56E1486F4A138B95 | 40,638 |
| 2 | gate_A.py | `tools/gate_A.py` | 61CF8B2467722CDC | 12,722 |
| 3 | calib_band_A.py | `tools/calib_band_A.py` | 840FE043D01FEC7F | 14,690 |
| 3 | identity_screen_A.py | `tools/identity_screen_A.py` | 759F005CDF01FA6C | 8,161 |
| 3 | control_chart_A.py | `tools/control_chart_A.py` | 1958DFA2CC6F69CE | 5,838 |
| 3 | response_mode_A.py | `tools/response_mode_A.py` | C3E90B11B62F67A5 | 8,942 |
| 3 | integrity_A.py | `tools/integrity_A.py` | 27D1677F28C3A0D9 | 10,191 |
| 3 | sample_inspection_A.py | `tools/sample_inspection_A.py` | E03EE571DC2A5FA2 | 5,592 |
| 3 | judge_fragments_A.py | `tools/judge_fragments_A.py` | FC833474B90CE794 | 27,071 |
| 3 | build_report_A.py | `tools/build_report_A.py` | 89F1B3963EA4D1AC | 25,346 |
| 3 | report_lint.py | `tools/report_lint.py` | 3F9C3EA33216D942 | 10,701 |
| 3 | freeze_A.py | `tools/freeze_A.py` | 2E0F1074B8EE1F36 | 6,240 |
| 3 | build_draftA.py | `tools/build_draftA.py` | 997108E294469CF5 | 4,854 |
| 3 | numbers_lint.py | `tools/numbers_lint.py` | 33FE2106E8BB1E17 | 11,823 |
| 3 | make_contrasts_A.py | `tools/make_contrasts_A.py` | B074B0C64745EFF1 | 51,408 |
| 3 | power_grid_A.py | `tools/power_grid_A.py` | 999C42D98851F7A4 | 36,606 |
| 3 | design_facts_A.py | `tools/design_facts_A.py` | AA30D4F9FB967534 | 41,922 |
| 3 | colab/boot_stageA.py | `tools/colab/boot_stageA.py` | 61EA4467659670B1 | 24,811 |
| 4 | synth_A.py | `tools/synth_A.py` | D685AB76C6E34B32 | 27,747 |
| 4 | synth_gates_A.py | `tools/synth_gates_A.py` | 822D8ED592CD4A69 | 20,741 |
| 4 | firth_check_A.py | `tools/firth_check_A.py` | 941A54BA051CE05F | 7,705 |
| 4 | firth_check_A.R | `tools/firth_check_A.R` | 03EF1FF659759A2A | 2,639 |
| 4 | verify_reflection_impl_A.py | `tools/verify_reflection_impl_A.py` | 0D1E9CEBA8E09876 | 26,576 |

## 部品: synth_A.py（`tools/synth_A.py`・SHA16 D685AB76C6E34B32・27,747 字）

```python
# -*- coding: utf-8 -*-
"""synth_A.py v2 —— 段階 A の集計器（tools/analyze_A.py）の全経路を合成データ（人工の件数・推論なし）で発火させる検査（2026-09-13 整備・登録者裁定 D9 の三つ目の手順・採否表 P2）。
v2（2026-09-14・実装検分の採否表 P100・登録者裁定 D16・D20・D22）: 札の行 id に加えて、注の範囲・除外の範囲・refuse の理由を期待と突合し、refuse の理由 (a)(b)(d)・腕に選択的な配置・二つの場面の確証・
  片側の残存で β₃ が棄却される対比・様式 (a) の走を足した。器の写しに変異 M1〜M6 を一つずつ入れて、対応する走で期待との不一致が出ることを確かめる（変異を見分けない合成検査は検査にならない・W50）。
  集計器 v2 の入力（門0.5 と校正帯の記録・セッション記録・門の記録の撤退条件の判定と残る場面）に合わせた。
置き場: --root に results 相当の木を作る（リポジトリの results/ には置かない・既定で走ごとに消す）。
走 1〜12: refuse 門 × 様式門 × 環境保留の十二の組を全対比に一様に当てる（refuse は腕 X の refuse 率の推移・様式は腕 X の (b) 率・環境は橋の腕 X の率のずれ）。
  場面ごとに型を置く: N1＝解釈条項なし・p* 棄却（P_S）／N2＝解釈条項あり・p* 棄却（P_CS）／S1＝解釈条項なし・p* 非棄却（P_N）／S4＝解釈条項あり・p* 非棄却（P_C）／
  SK＝非有意・判定不能（両腕の床）・判定不能（非収束・合成検査の口）。腕 X＝各対比にちょうど一本ずつ入る腕。基の腕＝Onull・O-Ncold。
  走 1＝測定不能（SK の Odosehalf の大きい規模）・床持続の 0・撤退条件の器の異常／走 2＝錨帯（SK の 1.7B）・門0.5 不合格／走 3＝校正腕の器の異常（N1 の 4B）／走 4＝門0.5 合格と API 再走行／走 5＝錨帯（全場面の 4B）。
走 13: 門2 の縮小（残る場面は N1 だけ・残らない場面の対比だけ判定不能・登録者裁定 D16）。
走 14: refuse 門の理由（N1＝答えた分母で β₃ の符号が逆転〔a〕・N2＝答えた分母で名目有意を失う〔b〕・S1＝答えた分母の下限を満たす規模が足りない〔d〕）。
走 15: 腕に選択的な配置（refuse の推移は N・様式 (a) は Lneg・橋のずれは Odose1）・N1 と N2 の二つの場面の確証・片側の残存で β₃ が棄却される対比（N1 の Odosehalf を大きい規模で測定不能に）・
  校正腕の器の異常を N2 の 4B の走行に・対照どうしの差の定型（N2 の Onull-Ncold を下向きに）。
各走で集計器を実行し、対比ごとの札の全組合せ表の行 id・注の範囲（門0.5 不合格・校正腕と撤退条件の器の異常・残存規模の非連続）・除外の範囲（測定不能のセル・錨帯の除外単位・橋の帯を超えた腕・門2 の縮小の対比）・
refuse の理由を期待と突合する。走の和で五十二行すべての発火と、必要な経路の発火を assert する。
変異の検査（--mutations all|none|M1,M3）: M1 校正の注を全確証に／M2 門0.5 の注を全対比に／M3 片側の規則を外す／M4 refuse の理由を (c) だけに／M5 様式門の (a) を読まない／M6 門2 の縮小を全対比に。
出力: records/A/synth-A-<日付>.md と同 .json（--record で変更可）。合成の件数は検査のための人工値であり、いかなる読みにも用いない。
用法: python tools/synth_A.py --root <一時置き場> [--runs 1,13] [--mutations none] [--keep] [--facts <設計事実 JSON>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, subprocess, itertools, argparse, datetime, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import confirm_A
from zaxis_A import z_sizes
REPO = runs_A.REPO
VERSION = 'v2'
ap = argparse.ArgumentParser()
ap.add_argument('--root', required=True); ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'A', 'design-facts-A.json')); ap.add_argument('--B-measurable', type=int, default=4)
ap.add_argument('--runs', default='all'); ap.add_argument('--keep', action='store_true'); ap.add_argument('--record', default=None); ap.add_argument('--mutations', default='all')
a = ap.parse_args()
ROOT = os.path.abspath(a.root)
assert ROOT != os.path.abspath(os.path.join(REPO, 'results')), '合成データを results に置かない'
T = runs_A.load_T(); SIZES = T['sizes']; SC = T['scenarios']; ARMS = T['arms']['preamble']; MID = runs_A.model_ids(T); S = T['seeds']
ANCHOR = next(m['key'] for m in T['models'] if m['anchor']); FAM = T['families']['A_slope']; CONTR = FAM['contrasts']; ALL_ROWS = [r['id'] for r in FAM['confirm_rule']['label_combo_table']]
BR = T['bridge']; PS = T['print_strings']; L = FAM['confirm_rule']['labels']; MIN_OK = FAM['refuse_gate']['answered_min_n_ok']
zs = np.array(z_sizes(SIZES)); zt = (zs - zs.min()) / (zs.max() - zs.min())
lin = lambda lo, hi: [float(lo + (hi - lo) * t) for t in zt]
const = lambda v: [v] * len(SIZES)
X_ARMS = ['N', 'Odose1', 'Odosehalf', 'Lneg', 'Onull-Ncold', 'Osec-Ncold']
TYPES = {
    'P_S': dict(n=200, clause=False, star=True, rates={'Onull': const(0.5), 'O-Ncold': const(0.5), 'Odose1': lin(0.2, 0.8), 'Odosehalf': lin(0.2, 0.8), 'Lneg': lin(0.2, 0.8),
                                                        'Onull-Ncold': lin(0.2, 0.8), 'N': lin(0.8, 0.2), 'Osec-Ncold': lin(0.8, 0.2)}),
    'P_CS': dict(n=200, clause=True, star=True, rates=dict({'Onull': const(0.03), 'O-Ncold': const(0.03)}, **{x: lin(0.10, 0.60) for x in X_ARMS})),
    'P_N': dict(n=2000, clause=False, star=False, rates={'Onull': lin(0.30, 0.80), 'O-Ncold': lin(0.30, 0.80), 'Odose1': lin(0.45, 0.95), 'Odosehalf': lin(0.45, 0.95), 'Lneg': lin(0.45, 0.95),
                                                          'Onull-Ncold': lin(0.45, 0.95), 'N': lin(0.45, 0.95), 'Osec-Ncold': lin(0.45, 0.95)}),
    'P_C': dict(n=2000, clause=True, star=False, rates=dict({'Onull': [0.02, 0.03, 0.10, 0.30, 0.50, 0.70], 'O-Ncold': [0.02, 0.03, 0.10, 0.30, 0.50, 0.70]},
                                                           **{x: [0.17, 0.18, 0.25, 0.45, 0.65, 0.85] for x in X_ARMS})),
    'MIX': dict(n=200, rates={'Onull': const(0.5), 'Odose1': const(0.5), 'Odosehalf': const(0.5), 'Lneg': const(0.5), 'N': const(0.5), 'Onull-Ncold': const(0.5), 'O-Ncold': const(0.01), 'Osec-Ncold': const(0.01)})}
SC_TYPE = dict(zip(SC, ['P_S', 'P_CS', 'P_N', 'P_C', 'MIX']))
COMBOS = list(itertools.product((False, True), ('none', 'note', 'hold'), (False, True)))
NC_ID = 'SK:Lneg~Onull'
REF_A_FULL = [0.10, 0.14, 0.18, 0.22, 0.26, 0.30]; REF_A_ANS = [0.50, 0.46, 0.42, 0.38, 0.34, 0.30]   # 全分母は上向き・答えた分母は下向き（理由 a）
REF_B = [0.80, 0.64, 0.48, 0.32, 0.16, 0.0]   # refuse の割合（答えた分母の率は基の腕と同じ 0.5・理由 b）
N_RUNS = 15
RUNS = list(range(1, N_RUNS + 1)) if a.runs == 'all' else [int(x) for x in a.runs.split(',')]
xarm = lambda c: c['A'] if c['A'] in X_ARMS else c['B']


def cfg(run):
    rf, st, env = COMBOS[run - 1] if run <= len(COMBOS) else COMBOS[0]
    C = {'combo': (rf, st, env) if run <= len(COMBOS) else None, 'types': dict(SC_TYPE), 'refuse': {(sc, x): 'drift' for sc in SC for x in X_ARMS} if rf else {},
         'style': {x: ('b', st) for x in X_ARMS} if st != 'none' else {}, 'env': set(X_ARMS) if env else set(), 'unmeas': {}, 'anchor': set(), 'remaining': None, 'identity': None,
         'calib_anom': [], 'wd_anom': False, 'api': False, 'floor0': False, 'override': {}}
    if run == 1:
        C.update(unmeas={('SK', 'Odosehalf'): ('8B', '14B', '32B')}, floor0=True, wd_anom=True)
    elif run == 2:
        C.update(anchor={('1.7B', 'SK')}, identity='fail')
    elif run == 3:
        C.update(calib_anom=[('4B', 'N1')])
    elif run == 4:
        C.update(api=True, identity='pass')
    elif run == 5:
        C.update(anchor={('4B', sc) for sc in SC})
    elif run == 13:
        C.update(remaining=['N1'])
    elif run == 14:
        C['types'].update({'N2': 'P_S', 'S1': 'P_S'}); C['refuse'] = {(sc, x): mode for sc, mode in (('N1', 'a'), ('N2', 'b'), ('S1', 'd')) for x in X_ARMS}
    elif run == 15:
        C['types'].update({'N2': 'P_S'})
        C.update(refuse={(sc, 'N'): 'drift' for sc in SC}, style={'Lneg': ('a', 'hold')}, env={'Odose1'}, unmeas={('N1', 'Odosehalf'): ('8B', '14B', '32B')}, calib_anom=[('4B', 'N2')],
                 override={('N2', 'Onull-Ncold'): lin(0.8, 0.2)})
    C['one_side'] = {c['id'] for c in CONTR for (sc, arm), sizes in C['unmeas'].items()
                     if c['scenario'] == sc and arm in (c['A'], c['B']) and len({T['environments'][s]['env'] for s in SIZES if s not in sizes}) == 1}
    return C


def spec(run, model, sc, arm, phase='main'):
    """(n, 破局, refuse, 書式外) を返す（人工値）。"""
    C = cfg(run); s = '4B' if model == ANCHOR else model; i = SIZES.index(s); ty = TYPES[C['types'][sc]]
    mode = C['refuse'].get((sc, arm)) if phase in ('main', 'bridge', 'anchor') else None
    if (sc, arm) in C['override']:
        n, rate = ty['n'], C['override'][(sc, arm)][i]
    elif arm in ty['rates']:
        n, rate = ty['n'], ty['rates'][arm][i]
    elif arm in ('O', 'Nk', 'Osec'):
        n, rate = 200, (0.10 if (C['floor0'] and sc == 'SK' and arm == 'O' and s == '32B') else 0.005)
    else:
        n, rate = 40, 0.5
    if phase == 'anchor' and (s, sc) in C['anchor'] and arm == 'Onull':
        rate = rate + 0.20 if rate < 0.5 else rate - 0.20
    if phase == 'bridge' and arm in C['env']:
        rate = rate + 0.20 if rate < 0.5 else rate - 0.20
    ref = 0
    if mode == 'drift':
        cat = int(round(n * rate)); ref = int(round(n * 0.20 * (1 - i / (len(SIZES) - 1))))
    elif mode == 'a':
        cat = int(round(n * REF_A_FULL[i])); ref = n - int(round(cat / REF_A_ANS[i]))
    elif mode == 'b':
        ref = int(round(n * REF_B[i])); cat = int(round((n - ref) * 0.5))
    elif mode == 'd':
        cat, ref = ((12, n - (MIN_OK - 1)) if i < 4 else (int(round(n * (0.5 if i == 4 else 0.6))), 0))
    else:
        cat = int(round(n * rate))
    cat += (2 if phase == 'api' else 0)
    ff = int(round(n * 0.40)) if (phase == 'main' and s in C['unmeas'].get((sc, arm), ())) else 0
    if ff:
        cat = min(cat, n - ref - ff)
    assert cat + ref + ff <= n, (run, model, sc, arm, phase, cat, ref, ff)
    return n, cat, ref, ff


def write_run(root, tag, model, sc, seed, arms, fn_spec):
    rk = '%s__%s__none__seed%d' % (tag, sc, seed); d = os.path.join(root, tag, rk); os.makedirs(d, exist_ok=True); mid = MID[model]; mfn = mid.replace('/', '_')
    json.dump({'tag': tag, 'scenario': sc, 'model': mid, 'seed': seed, 'arms': arms, 'arm_src': {}, 'synthetic': True}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    open(os.path.join(d, 'raw-%s.jsonl' % mfn), 'w').close()
    ti = 0
    with open(os.path.join(d, 'trials-%s.jsonl' % mfn), 'w', encoding='utf-8', newline='\n') as f:
        for arm in arms:
            n, cat, ref, ff = fn_spec(arm)
            for j in range(n):
                v = ('true', '"a"', 'false') if j < cat else (('false', '"refuse"', 'false') if j < cat + ref else (('null', 'null', 'true') if j < cat + ref + ff else ('false', '"b"', 'false')))
                f.write('{"trial_id":"%s-%d","trial_index":%d,"arm":"%s","status":"ok","catastrophe":%s,"choice":%s,"format_fail":%s,"loop_flag":false,"truncated":false}\n' % (rk, ti, ti, arm, v[0], v[1], v[2])); ti += 1
    return rk


def build(run, root):
    tag = 'synthA%02d' % run; C = cfg(run); sess = {}; style = {}
    for m in T['models']:
        mk = m['key']
        for sc in SC:
            rk = write_run(root, tag, mk, sc, S['main'][mk][sc], ARMS, lambda arm, mk=mk, sc=sc: spec(run, mk, sc, arm)); sess.setdefault((tag, mk), []).append(rk)
            cells = style.setdefault(mk, {}).setdefault(sc, {})
            for arm in ARMS:
                n, cat, ref, ff = spec(run, mk, sc, arm); kind, level = C['style'].get(arm, ('b', 'none')); frac = {'none': 0.5, 'note': 0.70, 'hold': 0.90}[level]
                b = int(round(n * (frac if kind == 'b' else 0.5))); am = int(round(n * (frac - 0.5))) if kind == 'a' else 0; pn = n - b
                cells[arm] = {'n_ok': n, 'a_final': am, 'b_final': b, 'c1_final': 0, 'c2_final': 0, 'think_residue': 0,
                              'strata': {'json_direct': {'n': b, 'cat': cat - int(round(cat * pn / n))}, 'prose': {'n': pn, 'cat': int(round(cat * pn / n))}}}
            if mk in T['anchor_band']['models']:
                rk2 = write_run(root, tag + '-anchor2', mk, sc, S['anchor_rerun'][mk][sc], T['anchor_band']['arms'], lambda arm, mk=mk, sc=sc: spec(run, mk, sc, arm, 'anchor')); sess[(tag, mk)].append(rk2)
    for bm in BR['cells']:
        rk = write_run(root, tag + '-bridge', bm, BR['scenario'], list(S['bridge'][bm].values())[0], BR['arms'], lambda arm, bm=bm: spec(run, bm, BR['scenario'], arm, 'bridge')); sess[(tag + '-bridge', bm)] = [rk]
    if C['api']:
        for mk, seed in S['api_rerun'].items():
            write_run(root, tag + '-api', mk, 'N1', seed, ARMS, lambda arm, mk=mk: spec(run, mk, 'N1', arm, 'api'))
    os.makedirs(os.path.join(root, 'sessions-A'), exist_ok=True)
    for (tg, mk), rks in sess.items():
        envv = BR['cells'][mk]['bridge_env'] if tg.endswith('-bridge') else T['environments'][mk]['env']
        json.dump({'tag': tg, 'model': mk, 'session': 1, 'phase': 'bridge' if tg.endswith('-bridge') else 'main', 'env_value': envv, 'run_keys': rks, 'synthetic': True},
                  open(os.path.join(root, 'sessions-A', '%s__%s__s1.json' % (tg, mk)), 'w', encoding='utf-8'), ensure_ascii=False)
    rec = os.path.join(root, 'records'); os.makedirs(rec, exist_ok=True)
    P = {'style': os.path.join(rec, 'style-%s.json' % tag), 'gate': os.path.join(rec, 'gate-%s.json' % tag), 'calib': os.path.join(rec, 'calib-%s.json' % tag)}
    json.dump({'kind': 'response_mode_A', 'synthetic': True, 'tag': tag, 'cells': style}, open(P['style'], 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump({'kind': 'gate_A', 'synthetic': True, 'gate2': {'shrink': C['remaining'] is not None, 'remaining_scenarios': C['remaining'] if C['remaining'] is not None else list(SC)},
               'withdrawal': {'anomaly': C['wd_anom'], 'status': 'anomaly' if C['wd_anom'] else 'pass'}}, open(P['gate'], 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump({'kind': 'calib_band_A', 'synthetic': True, 'anomaly_run_keys': ['%s__%s__none__seed%d' % (tag, sc, S['main'][s][sc]) for s, sc in C['calib_anom']]}, open(P['calib'], 'w', encoding='utf-8'), ensure_ascii=False)
    if C['identity']:
        P['identity'] = os.path.join(rec, 'identity-%s.json' % tag)
        json.dump({'kind': 'identity_screen_A', 'synthetic': True, 'verdict': C['identity']}, open(P['identity'], 'w', encoding='utf-8'), ensure_ascii=False)
    return tag, P, C


def expected_row(c, C):
    if C['remaining'] is not None and c['scenario'] not in C['remaining']:
        return 'U-gate2_shrink'
    t = C['types'][c['scenario']]
    if t == 'MIX':
        return 'U-nonconverged' if c['id'] == NC_ID else ('U-residual' if c['B'] == 'Osec-Ncold' else 'NS')
    ty = TYPES[t]; x = xarm(c)
    return confirm_A.row_id(2, clause=ty['clause'], star=ty['star'], refuse=(c['scenario'], x) in C['refuse'], style=C['style'][x][1] if x in C['style'] else 'none',
                            env=(x in C['env']) or (c['id'] in C['one_side']))


def expected_notes(x, c, C):
    want = set(); r = x['result']
    if C['identity'] == 'fail' and 'N' in (c['A'], c['B']):
        want.add('identity')
    if x['label'] == L['confirmed']:
        kept = {SIZES[j] for j in range(len(SIZES)) if r['keep'][j]}
        if any(sc == c['scenario'] and s in kept for s, sc in C['calib_anom']):
            want.add('calib')
        if C['wd_anom']:
            want.add('withdrawal')
    if r['status'] == 'ok':
        k = [j for j in range(len(SIZES)) if r['keep'][j]]
        if (k[-1] - k[0] + 1) != len(k) or not r['keep'][0] or not r['keep'][-1]:
            want.add('gap')
    return want


def got_notes(x):
    g = set()
    for n_ in x['notes']:
        g.add({PS['identity_fail_note']: 'identity', PS['calib_anomaly_note']: 'calib', PS['withdrawal_anomaly_note']: 'withdrawal'}.get(n_, 'gap' if '残存規模は連続でない' in n_ else 'other:' + n_[:30]))
    return g


def compare(RJ, run, C):
    mm = []
    for x, c in zip(RJ['contrasts'], CONTR):
        exp = expected_row(c, C)
        if x['row'] != exp:
            mm.append({'kind': 'row', 'run': run, 'id': x['id'], 'expected': exp, 'got': x['row']})
        wn, gn = expected_notes(x, c, C), got_notes(x)
        if wn != gn:
            mm.append({'kind': 'notes', 'run': run, 'id': x['id'], 'expected': sorted(wn), 'got': sorted(gn)})
        mode = C['refuse'].get((c['scenario'], xarm(c)))
        if mode in ('a', 'b', 'd') and x['stage'] == 2 and mode not in ((x['refuse_gate'] or {}).get('reasons') or []):
            mm.append({'kind': 'refuse_reason', 'run': run, 'id': x['id'], 'expected': mode, 'got': (x['refuse_gate'] or {}).get('reasons')})
    sets = [('unmeasurable', {(s, sc, arm) for (sc, arm), sizes in C['unmeas'].items() for s in sizes}, {(u['model'], u['scenario'], u['arm']) for u in RJ['unmeasurable']}),
            ('anchor_units', set(C['anchor']), {(u['model'], u['scenario']) for u in RJ['anchor_excluded_units']}),
            ('env_flag_arms', set(C['env']), set(RJ['env_flag_arms'])),
            ('gate2_shrink_ids', {c['id'] for c in CONTR if C['remaining'] is not None and c['scenario'] not in C['remaining']}, set(RJ.get('gate2_shrink_ids') or []))]
    for nm, want, got in sets:
        if want != got:
            mm.append({'kind': 'scope:' + nm, 'run': run, 'expected': sorted(map(str, want)), 'got': sorted(map(str, got))})
    return mm


def paths_fired(RJ):
    got = set(); C_ = RJ['contrasts']
    pairs = [('unmeasurable', bool(RJ['unmeasurable'])), ('anchor_exclusion', bool(RJ['anchor_excluded_units'])), ('env_bridge', any(e['rule'] == 'bridge' for x in C_ for e in x['env_reasons'])),
             ('env_one_side', any(e['rule'] == 'one_side' for x in C_ for e in x['env_reasons'])), ('style_cells', any(x['strings'].get('style') for x in C_)),
             ('stratified_ok', any(s_.get('status') == 'ok' for s_ in RJ['stratified'])), ('stratified_any', bool(RJ['stratified'])), ('sensitivity_changed', any(s_['changed'] for s_ in RJ['sensitivity'])),
             ('measurable_yes', any(v['measurable'] for v in RJ['measurable']['types'].values())), ('measurable_no', any(not v['measurable'] for v in RJ['measurable']['types'].values())),
             ('stack_rows', bool(RJ['descriptive']['A_desc_stack']['rows'])), ('demotions', bool(RJ['demotions'])), ('floor_1', any(f['flag'] == 1 for f in RJ['floor'])),
             ('floor_0', any(f['flag'] == 0 for f in RJ['floor'])), ('critical_size', any(x['size'] != 'なし' for x in RJ['descriptive']['A_desc_critical_size'])),
             ('env_secondary', any(x.get('status') == '収束' for x in RJ['descriptive']['A_desc_env']['secondary'])), ('scale_only_desc', bool(RJ['descriptive']['A_desc_scale_only'])),
             ('reach_note', bool(RJ.get('reach_note'))), ('confirmed_label_string', any(x['label'] == L['confirmed'] for x in C_)),
             ('refuse_a', any('a' in ((x['refuse_gate'] or {}).get('reasons') or []) for x in C_)), ('refuse_b', any('b' in ((x['refuse_gate'] or {}).get('reasons') or []) for x in C_)),
             ('refuse_d', any('d' in ((x['refuse_gate'] or {}).get('reasons') or []) for x in C_)),
             ('style_a_hold', any(x['style'] == 'hold' and any(cl['kind'] == 'a' for cl in (x['style_detail'] or {}).get('cells', [])) for x in C_)),
             ('confirmed_multi_scenario', len({x['scenario'] for x in C_ if x['label'] == L['confirmed']}) >= 2),
             ('one_side_stage2', any(x['stage'] == 2 and any(e['rule'] == 'one_side' for e in x['env_reasons']) for x in C_)),
             ('residual_gap_note', any('残存規模は連続でない' in n_ for x in C_ for n_ in x['notes'])), ('control_pairs_string', any(p_.get('string') for p_ in RJ['descriptive'].get('A_desc_control_pairs') or [])),
             ('upward', bool(RJ.get('upward_confirmed'))), ('gate2_partial_shrink', bool(RJ.get('gate2_shrink_ids')) and any(x['stage'] == 2 for x in C_))]
    for nm, on in pairs:
        if on:
            got.add(nm)
    notes = [n_ for x in C_ for n_ in x['notes']]
    for key in ('identity_fail_note', 'calib_anomaly_note', 'withdrawal_anomaly_note'):
        if PS[key] in notes:
            got.add(key)
    return got


PATHS_REQUIRED = ['unmeasurable', 'anchor_exclusion', 'env_bridge', 'env_one_side', 'style_cells', 'stratified_ok', 'stratified_any', 'sensitivity_changed', 'measurable_yes', 'measurable_no',
                  'identity_fail_note', 'calib_anomaly_note', 'withdrawal_anomaly_note', 'stack_rows', 'demotions', 'floor_1', 'floor_0', 'critical_size', 'env_secondary', 'scale_only_desc', 'reach_note',
                  'confirmed_label_string', 'refuse_a', 'refuse_b', 'refuse_d', 'style_a_hold', 'confirmed_multi_scenario', 'one_side_stage2', 'residual_gap_note', 'control_pairs_string', 'upward', 'gate2_partial_shrink']


def run_once(run, tools_dir, sub):
    root = os.path.join(ROOT, sub); shutil.rmtree(root, ignore_errors=True); t0 = time.time(); tag, P, C = build(run, root); out = os.path.join(root, 'out', 'analysis-%s' % tag)
    cmd = [sys.executable, os.path.join(tools_dir, 'analyze_A.py'), '--tag', tag, '--root', root, '--anchor-tag', tag + '-anchor2', '--bridge-tag', tag + '-bridge', '--api-tag', tag + '-api',
           '--style', P['style'], '--gate', P['gate'], '--calib', P['calib'], '--out', out, '--force', '--B-measurable', str(a.B_measurable), '--synth-nonconverged', NC_ID]
    cmd += ['--identity', P['identity']] if 'identity' in P else ['--no-identity']
    if a.facts and os.path.exists(a.facts):
        cmd += ['--facts', a.facts]
    pr = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    if pr.returncode != 0:
        res = {'error': (pr.stdout[-1500:] + pr.stderr[-3000:])}
    else:
        RJ = runs_A.read_json(out + '.json'); res = {'RJ': RJ, 'mismatches': compare(RJ, run, C), 'paths': paths_fired(RJ), 'C': C}
    res['seconds'] = round(time.time() - t0, 1)
    if not a.keep:
        shutil.rmtree(root, ignore_errors=True)
    return res


MUTS = [('M1', 'tools/analyze_A.py', [("        if rks & ANOM_RK:\n", "        if ANOM_RK:\n")], [15], '校正腕の器の異常の注を全確証に付ける'),
        ('M2', 'tools/analyze_A.py', [("    if ID_VERDICT == 'fail' and 'N' in (c['A'], c['B']):\n", "    if ID_VERDICT == 'fail':\n")], [2], '門0.5 不合格の注を全対比に付ける'),
        ('M3', 'tools/analyze_A.py', [("    if len(envs) == 1:\n", "    if len(envs) == 0:\n")], [15], '片側の規則を外す'),
        ('M4', 'tools/confirm_A.py', [("    if len(j) < R.ref_min_sizes:\n        out['reasons'].append('d')\n", "    if len(j) < R.ref_min_sizes:\n        pass\n"),
                                     ("            if np.sign(ra['beta']) != np.sign(res['beta']) or ra['beta'] == 0.0:\n", "            if False:\n"), ("            if ra['p'] >= R.alpha:\n", "            if False:\n")], [14],
         'refuse の理由を (c) だけにする'),
        ('M5', 'tools/confirm_A.py', [("        for nm, xa, xb in (('a', a_A, a_B), ('b', b_A, b_B)):\n", "        for nm, xa, xb in (('b', b_A, b_B),):\n")], [15], '様式門の (a) を読まない'),
        ('M6', 'tools/analyze_A.py', [("SHRINK_IDX = {i for i, c in enumerate(CONTR) if GATE2 and c['scenario'] not in REMAIN}", "SHRINK_IDX = {i for i, c in enumerate(CONTR) if GATE2}")], [13], '門2 の縮小を全対比に当てる')]


def make_mutant(name, rel, pairs):
    d = os.path.join(ROOT, 'mutant-' + name); shutil.rmtree(d, ignore_errors=True)
    for sub in ('tools', 'design', os.path.join('records', 'A')):
        os.makedirs(os.path.join(d, sub))
    for f in ('analyze_A.py', 'confirm_A.py', 'runs_A.py', 'firth.py', 'zaxis_A.py', 'bands_A.py'):
        shutil.copy(os.path.join(REPO, 'tools', f), os.path.join(d, 'tools', f))
    shutil.copy(runs_A.CPATH, os.path.join(d, 'design', 'contrasts-A.json')); shutil.copy(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'), os.path.join(d, 'records', 'A', 'hf-models-A.json'))
    p = os.path.join(d, rel); s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (name, old[:60], s.count(old)); s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return d


fired = {}; paths = set(); report = []; mismatches = []; errors = []; t00 = time.time()
for run in RUNS:
    res = run_once(run, os.path.join(REPO, 'tools'), 'run%02d' % run)
    if 'error' in res:
        errors.append({'run': run, 'error': res['error']}); print('[synth] 走 %2d 集計器が失敗: %s' % (run, res['error'][-800:]), flush=True); continue
    RJ = res['RJ']; mismatches += res['mismatches']; paths |= res['paths']
    for x in RJ['contrasts']:
        fired.setdefault(x['row'], []).append('%d:%s' % (run, x['id']))
    C = res['C']
    report.append({'run': run, 'combo': {'refuse_hold': C['combo'][0], 'style': C['combo'][1], 'env_hold': C['combo'][2]} if C['combo'] else '特別の配置', 'label_counts': RJ['label_counts'],
                   'mismatches': len(res['mismatches']), 'rows': sorted({x['row'] for x in RJ['contrasts']}), 'paths': sorted(res['paths']), 'dev_marks': RJ['dev_marks'], 'seconds': res['seconds']})
    print('[synth] 走 %2d 不一致 %d 行 %d 経路 %d（%.0fs）' % (run, len(res['mismatches']), len(report[-1]['rows']), len(res['paths']), res['seconds']), flush=True)
MUT = []
want_m = [] if a.mutations == 'none' else [m for m in MUTS if a.mutations == 'all' or m[0] in a.mutations.split(',')]
for name, rel, pairs, mruns, text in want_m:
    d = make_mutant(name, rel, pairs); det = 0; errs = []
    for run in mruns:
        res = run_once(run, os.path.join(d, 'tools'), 'mut-%s-run%02d' % (name, run))
        if 'error' in res:
            errs.append(res['error'][-300:])
        else:
            det += len(res['mismatches'])
    MUT.append({'name': name, 'file': rel, 'text': text, 'runs': mruns, 'mismatches': det, 'detected': det > 0 and not errs, 'errors': errs})
    print('[synth] 変異 %s（%s）: 不一致 %d・%s' % (name, text, det, '見分けた' if det > 0 and not errs else '見分けなかった'), flush=True)
    if not a.keep:
        shutil.rmtree(d, ignore_errors=True)
not_fired = [r for r in ALL_ROWS if r not in fired]; paths_missing = [p for p in PATHS_REQUIRED if p not in paths]
full = (RUNS == list(range(1, N_RUNS + 1))) and a.mutations == 'all'
SUM = {'kind': 'synth_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'runs': RUNS, 'full': full,
       'inputs': {'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), **{nm: runs_A.sha16_file(os.path.join(REPO, 'tools', nm)) for nm in ('analyze_A.py', 'confirm_A.py', 'runs_A.py', 'firth.py', 'synth_A.py')}},
       'rows_total': len(ALL_ROWS), 'rows_fired': len(ALL_ROWS) - len(not_fired), 'rows_not_fired': not_fired, 'mismatches': mismatches, 'errors': errors, 'paths_required': PATHS_REQUIRED, 'paths_missing': paths_missing,
       'mutations': MUT, 'fired_by_row': {k: v[:3] for k, v in sorted(fired.items())}, 'per_run': report, 'seconds': round(time.time() - t00, 1),
       'clause': '合成の件数は検査のための人工値であり、いかなる読みにも用いない。本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
recp = a.record or os.path.join(REPO, 'records', 'A', 'synth-A-%s' % datetime.date.today().isoformat())
if full:
    json.dump(SUM, open(recp + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    Lm = ['# 段階 A 合成検査（機械生成・`tools/synth_A.py` %s・%s UTC）' % (VERSION, SUM['generated_utc']), '', '- 入力: %s' % json.dumps(SUM['inputs'], ensure_ascii=False),
          '- 札の全組合せ表: %d 行のうち発火 %d 行（未発火: %s）・期待との不一致 %d 件（行 id・注の範囲・除外の範囲・refuse の理由）・集計器の失敗 %d・経路の未発火: %s・所要 %.0f 秒' % (
              SUM['rows_total'], SUM['rows_fired'], '・'.join(not_fired) or 'なし', len(mismatches), len(errors), '・'.join(paths_missing) or 'なし', SUM['seconds']),
          '- 変異の検査: %s' % '・'.join('%s（%s）%s' % (m['name'], m['text'], '見分けた' if m['detected'] else '見分けなかった') for m in MUT), '',
          '| 走 | 配置 | 札の件数 | 不一致 | 発火した行 | 発火した経路 | 秒 |', '|---|---|---|---|---|---|---|']
    Lm += ['| %d | %s | %s | %d | %s | %s | %s |' % (r['run'], json.dumps(r['combo'], ensure_ascii=False), json.dumps(r['label_counts'], ensure_ascii=False), r['mismatches'], '・'.join(r['rows']), '・'.join(r['paths']), r['seconds']) for r in report]
    Lm += ['', '| 変異 | 器 | 内容 | 走 | 期待との不一致 | 判定 |', '|---|---|---|---|---|---|'] + ['| %s | %s | %s | %s | %d | %s |' % (m['name'], m['file'], m['text'], '・'.join(map(str, m['runs'])), m['mismatches'], '見分けた' if m['detected'] else '見分けなかった') for m in MUT]
    Lm += ['', SUM['clause']]
    open(recp + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(Lm) + '\n')
    print('written', recp + '.{json,md}')
print('[synth_A] 行 %d/%d 発火・不一致 %d・失敗 %d・経路の未発火 %s・変異 %s' % (SUM['rows_fired'], SUM['rows_total'], len(mismatches), len(errors), paths_missing, [(m['name'], m['detected']) for m in MUT]))
if mismatches:
    print(json.dumps(mismatches[:25], ensure_ascii=False))
if full:
    assert not not_fired and not mismatches and not errors and not paths_missing and all(m['detected'] for m in MUT), (not_fired, len(mismatches), len(errors), paths_missing, [(m['name'], m['detected']) for m in MUT])
    print('synth_A.py %s PASS' % VERSION)
```

## 部品: synth_gates_A.py（`tools/synth_gates_A.py`・SHA16 822D8ED592CD4A69・20,741 字）

```python
# -*- coding: utf-8 -*-
"""synth_gates_A.py v2 —— 段階 A の門と校正の器（identity_screen_A・gate_A・calib_band_A・control_chart_A・integrity_A）を合成データで発火させる検査（synth_A.py の門の部・2026-09-13 整備・登録者裁定 D9 の三つ目の手順）。
v2（2026-09-14・実装検分の採否表 P77・P81・P90〜P92・P101・登録者裁定 D24）: 撤退条件の合格枝の発火・再走待ち・再走の合格・再走の器の異常・再走の n_ok が零・撤退条件のセルでない再走の seed の拒否、
  不合格枝の器の異常・橋のセッション・初点の確立の前に始まったセッションの逸脱、件数のそろわない校正腕（未完・判定しない）、整合検査の否定の経路（重複・欠落・seed の食い違い・dry-run の走行・要求の設定の違い）、
  起動器が使う校正帯の関数（session_verdict・claim_first_point）を足した。セッション記録に相を書く（calib_band_A v2 の読み出し）。
二つの場合:
 合格の場合（門0.5 合格）: 門0.5＝API 既測に比例した件数／パイロット＝門2 は縮小なし・撤退条件は帯の内、その後に撤退条件のセルを書き換えて発火・再走待ち・再走の合格・再走の器の異常・再走の n_ok が零を順に通す／
   校正腕＝帯の内・帯を超えてやり直しも超える（器の異常）・帯を超えてやり直し待ち・帯を超えたのに機種の走行が記帳（逸脱）とやり直しの合格・橋の帯の内・件数のそろわない校正腕／
   管理図は既存の表に追記（二度走らせて二重に記帳しない）／整合検査は門0.5・パイロット・校正腕で整合、本走行の相で否定の経路を検出。
 不合格の場合（門0.5 不合格）: 門0.5＝N の破局を上にずらす／パイロット＝四場面で族の腕が床（門2 の縮小）・撤退条件は門0.5 の手元に対し帯を超え再走も超える（器の異常）／
   校正腕＝初点・帯の内・帯を超えてやり直しの合格・帯を超えてやり直しも超える（器の異常）・橋のセッション（初点の確立の前に始まったので逸脱）／管理図は手元系列を新設。
各器の出力の判定欄を期待と突合し、すべて一致で PASS。合成の件数は検査のための人工値であり、いかなる読みにも用いない。
出力: records/A/synth-gates-A-<日付>.md と同 .json（--record で変更可）。
用法: python tools/synth_gates_A.py --root <一時置き場> [--B <門0.5 の補助の MC の B・既定 200>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, subprocess, argparse, datetime, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import calib_band_A
REPO = runs_A.REPO
VERSION = 'v2'
ap = argparse.ArgumentParser(); ap.add_argument('--root', required=True); ap.add_argument('--B', type=int, default=200); ap.add_argument('--record', default=None); ap.add_argument('--keep', action='store_true')
a = ap.parse_args()
ROOT = os.path.abspath(a.root)
assert ROOT != os.path.abspath(os.path.join(REPO, 'results')), '合成データを results に置かない'
T = runs_A.load_T(); ARMS = T['arms']['preamble']; SC = T['scenarios']; SIZES = T['sizes']; MID = runs_A.model_ids(T); ANCHOR = next(m['key'] for m in T['models'] if m['anchor'])
SHA = T['arms']['sha16']; RUN = T['runner']; S = T['seeds']; CAL = T['calibration']; BASE = T['bases_4B2507_api']; TAGS = T['tags']
samp = lambda mk: {'temperature': RUN['temperature'], 'top_p': RUN['top_p'], 'max_tokens': RUN['max_tokens'], 'extra_body': ({} if mk == ANCHOR else RUN['extra_body'])}
PY = [sys.executable]; ENV = dict(os.environ, PYTHONIOENCODING='utf-8'); TOOLS = os.path.join(REPO, 'tools')


def write_run(root, tag, mk, sc, seed, arms, cells, created, n, sampling=None, api_error_all=False, dup=False, gap=False, dry=False):
    """cells: {腕: (書式外, refuse, 破局, その他)}（和が行数）。走行器と同じ欄名で trials と manifest を書く（整合検査の欄を含む）。"""
    rk = '%s__%s__none__seed%d' % (tag, sc, seed); d = os.path.join(root, tag, rk); shutil.rmtree(d, ignore_errors=True); os.makedirs(d); mid = MID[mk]; mfn = mid.replace('/', '_'); sp = sampling or samp(mk)
    rows = sum(cells[arms[0]])
    json.dump(dict({'tag': tag, 'scenario': sc, 'model': mid, 'seed': seed, 'arms': arms, 'n_per_arm': n, 'arm_sha': {x: SHA.get(x) for x in arms}, 'arm_src': {}, 'sampling': sp, 'runner_sha': RUN['sha16'],
                    'created': created, 'local_env': {'gpu': 'synthetic', 'versions': {'vllm': 'synthetic'}}, 'synthetic': True}, **({'dry_model_rewritten': True} if dry else {})),
              open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    open(os.path.join(d, 'raw-%s.jsonl' % mfn), 'w').close()
    ti = 0; lines = []
    for j in range(rows):
        for arm in arms:
            F, Rf, Ca, O = cells[arm]; assert F + Rf + Ca + O == rows, (arm, cells[arm], rows)
            cat, ch, ff = (None, None, True) if j < F else ((False, 'refuse', False) if j < F + Rf else ((True, 'a', False) if j < F + Rf + Ca else (False, 'b', False)))
            if gap and ti == 1:
                ti += 1
            lines.append({'trial_id': '%s-%05d-%s' % (rk, ti, arm), 'trial_index': ti, 'arm': arm, 'run_key': rk, 'status': 'api_error' if api_error_all else 'ok', 'catastrophe': cat, 'choice': ch, 'format_fail': ff,
                          'loop_flag': False, 'truncated': False, 'runner_sha': RUN['sha16'], 'arms_spec': ','.join(arms), 'preamble_sha': SHA.get(arm), 'seed': seed, 'model': mid, 'sampling': sp, 'tag': tag,
                          'scenario': sc, 'timestamp': created, 'dry_run': dry})
            ti += 1
    if dup:
        lines.append(dict(lines[0]))
    with open(os.path.join(d, 'trials-%s.jsonl' % mfn), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in lines))
    return rk


def tool(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding='utf-8', errors='replace', env=ENV)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def mid_cells(n, cat):
    return (0, 0, cat, n - cat)


CHECKS = []


def check(name, cond, detail=''):
    CHECKS.append({'check': name, 'ok': bool(cond), 'detail': str(detail)[:300]}); print('[gates] %s %s %s' % ('○' if cond else '×', name, '' if cond else str(detail)[:300]), flush=True)


def case(name, fail):
    root = os.path.join(ROOT, name); shutil.rmtree(root, ignore_errors=True); rec = os.path.join(root, 'records'); os.makedirs(rec)
    T_ = lambda p: os.path.join(TOOLS, p)
    # ---- 門0.5
    n = T['identity_n']; cells = {}
    for arm in ARMS:
        b = BASE['N1'].get(arm)
        if b:
            ff = round(n * b['format_fail'] / b['n']); rf = round(n * b['refuse'] / b['n']); ca = round(n * b['k'] / b['n'])
            if fail and arm == 'N':
                ca = min(n - ff - rf, ca + round(n * 0.20))
            cells[arm] = (ff, rf, ca, n - ff - rf - ca)
        else:
            cells[arm] = mid_cells(n, n // 2)
    write_run(root, TAGS['identity'], ANCHOR, 'N1', S['identity'], ARMS, cells, '2026-09-14T00:00:00', n)
    rc, out = tool([T_('identity_screen_A.py'), '--root', root, '--out', os.path.join(rec, 'identity'), '--B', str(a.B), '--force'])
    ID = runs_A.read_json(os.path.join(rec, 'identity.json')) if rc == 0 else {}
    check('%s: 門0.5 の判定' % name, rc == 0 and ID.get('verdict') == ('fail' if fail else 'pass'), out[-300:])
    # ---- パイロット（門2・撤退条件）
    pn = T['pilot_n']; k_wd = 30 if fail else 39; wd_seed = S['pilot'][ANCHOR][CAL['scenario']]

    def pilot_cell(k):
        c = {arm: mid_cells(pn, pn // 2) for arm in ARMS}; c[CAL['arm']] = mid_cells(pn, k); return c
    for m in T['models']:
        for sc in SC:
            cells = {arm: mid_cells(pn, 0 if (fail and sc != 'N1' and m['key'] in SIZES) else pn // 2) for arm in ARMS}
            if m['key'] == ANCHOR and sc == CAL['scenario']:
                cells[CAL['arm']] = mid_cells(pn, k_wd)
            write_run(root, TAGS['pilot'], m['key'], sc, S['pilot'][m['key']][sc], ARMS, cells, '2026-09-14T01:00:00', pn)
    if fail:
        write_run(root, TAGS['pilot'], ANCHOR, CAL['scenario'], wd_seed + S['rerun_offset'], ARMS, pilot_cell(k_wd), '2026-09-14T02:00:00', pn)

    def gate(tagname):
        rc_, out_ = tool([T_('gate_A.py'), '--root', root, '--identity', os.path.join(rec, 'identity.json'), '--out', os.path.join(rec, tagname), '--force'])
        return rc_, out_, (runs_A.read_json(os.path.join(rec, tagname + '.json')) if rc_ == 0 else {})
    rc, out, G = gate('gate')
    check('%s: 門2 の縮小' % name, rc == 0 and G.get('gate2', {}).get('shrink') == fail and (G['gate2'].get('shrink_scenarios') == ([sc for sc in SC if sc not in G['gate2']['remaining_scenarios']] if fail else [])), out[-300:])
    check('%s: 撤退条件' % name, rc == 0 and G.get('withdrawal', {}).get('status') == ('anomaly' if fail else 'pass') and G['withdrawal']['anomaly'] == fail, json.dumps(G.get('withdrawal'), ensure_ascii=False))
    check('%s: 環境帯の引き直しの印字' % name, rc == 0 and G.get('env_band_recheck', {}).get('candidates'), '')
    if not fail:   # 合格枝の撤退条件の経路（採否表 P91・P101）
        write_run(root, TAGS['pilot'], ANCHOR, CAL['scenario'], wd_seed, ARMS, pilot_cell(20), '2026-09-14T01:00:00', pn)
        rc, out, G1 = gate('gate-wd-wait'); check('%s: 撤退条件が帯を超え、再走が無ければ再走待ち' % name, rc == 0 and G1['withdrawal']['status'] == 'rerun_required' and not G1['withdrawal']['anomaly'], out[-200:])
        write_run(root, TAGS['pilot'], ANCHOR, CAL['scenario'], wd_seed + S['rerun_offset'], ARMS, pilot_cell(39), '2026-09-14T02:00:00', pn)
        rc, out, G2 = gate('gate-wd-rerun-pass'); check('%s: 再走が帯の内なら再走の合格' % name, rc == 0 and G2['withdrawal']['status'] == 'rerun_pass', out[-200:])
        write_run(root, TAGS['pilot'], ANCHOR, CAL['scenario'], wd_seed + S['rerun_offset'], ARMS, pilot_cell(20), '2026-09-14T02:00:00', pn)
        rc, out, G3 = gate('gate-wd-anomaly'); check('%s: 再走も帯を超えれば器の異常' % name, rc == 0 and G3['withdrawal']['status'] == 'anomaly' and G3['withdrawal']['anomaly'], out[-200:])
        write_run(root, TAGS['pilot'], ANCHOR, CAL['scenario'], wd_seed + S['rerun_offset'], ARMS, pilot_cell(20), '2026-09-14T02:00:00', pn, api_error_all=True)
        rc, out, G4 = gate('gate-wd-nodata'); check('%s: 再走の n_ok が零は合格に数えない（rerun_no_data）' % name, rc == 0 and G4['withdrawal']['status'] == 'rerun_no_data' and not G4['withdrawal']['anomaly'], out[-200:])
        write_run(root, TAGS['pilot'], ANCHOR, CAL['scenario'], wd_seed, ARMS, pilot_cell(k_wd), '2026-09-14T01:00:00', pn)
        shutil.rmtree(os.path.join(root, TAGS['pilot'], '%s__%s__none__seed%d' % (TAGS['pilot'], CAL['scenario'], wd_seed + S['rerun_offset'])))
        bad_seed = S['pilot']['0.6B']['N1'] + S['rerun_offset']
        write_run(root, TAGS['pilot'], '0.6B', 'N1', bad_seed, ARMS, pilot_cell(20), '2026-09-14T02:00:00', pn)
        rc, out, _ = gate('gate-bad-rerun'); check('%s: 撤退条件のセルでない再走の seed で門は止まる（採否表 P92）' % name, rc != 0 and '登録に無い seed' in out, out[-200:])
        rc, out = tool([T_('integrity_A.py'), '--tag', TAGS['pilot'], '--phase', 'pilot', '--root', root, '--out', os.path.join(rec, 'integrity-pilot-bad'), '--force'])
        check('%s: 整合検査も撤退条件のセルでない再走の seed を不整合にする' % name, rc == 1 and '登録と違う' in json.dumps(runs_A.read_json(os.path.join(rec, 'integrity-pilot-bad.json')), ensure_ascii=False), out[-200:])
        shutil.rmtree(os.path.join(root, TAGS['pilot'], '%s__N1__none__seed%d' % (TAGS['pilot'], bad_seed)))
    # ---- 校正腕とセッション記録
    tag_c = TAGS['calibration']; cn = CAL['n']; sdir = os.path.join(root, 'sessions-A'); os.makedirs(sdir)
    mrk = lambda mk: '%s__N1__none__seed%d' % (TAGS['main'], S['main'][mk]['N1'])

    def calib(owner, phase, session, k, created, run_keys, env, rows=None, started='2026-09-15T01:00:00Z', calibrated=None):
        seed = runs_A.calibration_seed(T, owner, phase, session); rn = rows or cn
        rk = write_run(root, tag_c, ANCHOR, CAL['scenario'], seed, [CAL['arm']], {CAL['arm']: mid_cells(rn, k)}, created, cn)
        stag = TAGS['bridge'] if phase == 'bridge' else TAGS['main']
        json.dump({'tag': stag, 'model': owner, 'session': session, 'phase': phase, 'env_value': env, 'run_keys': run_keys, 'calibration_run_key': rk, 'started': started,
                   'log': [{'step': 'calibration', 'at': calibrated or started}], 'synthetic': True}, open(os.path.join(sdir, '%s__%s__s%d.json' % (stag, owner, session)), 'w', encoding='utf-8'), ensure_ascii=False)
        return rk
    if not fail:
        calib('0.6B', 'main', 1, 390, '2026-09-15T00:00:01', [mrk('0.6B')], 'L4')
        rk32 = calib('32B', 'main', 1, 350, '2026-09-15T00:00:02', [], 'A100')
        rk32b = calib('32B', 'main', 2, 350, '2026-09-15T00:00:03', [mrk('32B')], 'A100')
        calib('14B', 'main', 1, 350, '2026-09-15T00:00:04', [], 'A100')
        calib('8B', 'main', 1, 350, '2026-09-15T00:00:05', [mrk('8B')], 'A100')
        calib('8B', 'main', 2, 392, '2026-09-15T00:00:06', [mrk('8B')], 'A100')
        calib('4B', 'bridge', 1, 391, '2026-09-15T00:00:07', ['%s__N1__none__seed%d' % (TAGS['bridge'], S['bridge']['4B']['A100'])], 'A100')
        calib('1.7B', 'main', 1, 290, '2026-09-15T00:00:08', [], 'L4', rows=300)
    else:
        calib('0.6B', 'main', 1, 380, '2026-09-15T00:00:01', [mrk('0.6B')], 'L4', started='2026-09-15T00:00:00Z', calibrated='2026-09-15T00:10:00Z')
        calib('1.7B', 'main', 1, 381, '2026-09-15T00:00:02', [mrk('1.7B')], 'L4')
        calib('4B', 'main', 1, 340, '2026-09-15T00:00:03', [], 'L4')
        calib('4B', 'main', 2, 378, '2026-09-15T00:00:04', [mrk('4B')], 'L4')
        calib('8B', 'main', 1, 340, '2026-09-15T00:00:05', [], 'A100')
        calib('8B', 'main', 2, 330, '2026-09-15T00:00:06', [mrk('8B')], 'A100')
        calib('4B', 'bridge', 1, 379, '2026-09-15T00:00:07', ['%s__N1__none__seed%d' % (TAGS['bridge'], S['bridge']['4B']['A100'])], 'A100', started='2026-09-15T00:05:00Z')
    rc, out = tool([T_('calib_band_A.py'), '--root', root, '--identity', os.path.join(rec, 'identity.json'), '--out', os.path.join(rec, 'calib'), '--force'])
    CB = runs_A.read_json(os.path.join(rec, 'calib.json')) if rc == 0 else {'sessions': []}
    v = {(x['phase'], x['owner'], x['session']): x.get('verdict') for x in CB['sessions']}
    if not fail:
        want = {('main', '0.6B', 1): 'pass', ('main', '32B', 1): 'fired', ('main', '32B', 2): 'anomaly', ('main', '14B', 1): 'fired', ('main', '8B', 1): 'fired', ('main', '8B', 2): 'retry_pass',
                ('bridge', '4B', 1): 'pass', ('main', '1.7B', 1): 'incomplete'}
        check('%s: 校正腕の判定（件数のそろわない校正腕は未完）' % name, rc == 0 and v == want, json.dumps({'%s|%s|%s' % k: x for k, x in v.items()}, ensure_ascii=False))
        check('%s: 器の異常の走行キー' % name, rc == 0 and CB.get('anomaly_run_keys') == [mrk('32B')], CB.get('anomaly_run_keys'))
        check('%s: やり直し待ち' % name, rc == 0 and [(x['owner'], x['session']) for x in CB.get('retry_waiting', [])] == [('14B', 1)], CB.get('retry_waiting'))
        check('%s: 手順の逸脱' % name, rc == 0 and [(d['kind'], d['run_key'].split('seed')[-1]) for d in CB.get('deviations', [])] == [('model_runs_after_fired', str(runs_A.calibration_seed(T, '8B', 'main', 1)))], CB.get('deviations'))
        row, _ = calib_band_A.session_verdict(T, 'pass', root, rk32b)
        check('%s: 起動器が使う関数（session_verdict）が記録と同じ判定' % name, row['verdict'] == 'anomaly' and v[('main', '32B', 2)] == 'anomaly' and row['seed_rule_ok'] is True, row.get('verdict'))
        td = tempfile.mkdtemp(prefix='claimA-')
        c1 = calib_band_A.claim_first_point(td, {'tag': 'stageA', 'model': '0.6B', 'session': 1}); c2 = calib_band_A.claim_first_point(td, {'tag': 'stageA', 'model': '0.6B', 'session': 2})
        c3 = calib_band_A.claim_first_point(td, {'tag': 'stageA', 'model': '1.7B', 'session': 1}); shutil.rmtree(td, ignore_errors=True)
        check('%s: 初点の名乗り（同じ機種は次のセッション番号でも始められ、ほかの機種は始めない・登録者裁定 D24）' % name, c1[0] is True and c2[0] is True and c3[0] is False, (c1, c2, c3))
    else:
        want = {('main', '0.6B', 1): 'first_point', ('main', '1.7B', 1): 'pass', ('main', '4B', 1): 'fired', ('main', '4B', 2): 'retry_pass', ('main', '8B', 1): 'fired', ('main', '8B', 2): 'anomaly',
                ('bridge', '4B', 1): 'pass'}
        check('%s: 校正腕の判定（初点と両側・器の異常・橋のセッション）' % name, rc == 0 and v == want and (CB.get('first_point') or {}).get('run_key', '').endswith('seed%d' % runs_A.calibration_seed(T, '0.6B', 'main', 1)),
              json.dumps({'%s|%s|%s' % k: x for k, x in v.items()}, ensure_ascii=False))
        check('%s: 不合格枝の器の異常の走行キー' % name, rc == 0 and CB.get('anomaly_run_keys') == [mrk('8B')], CB.get('anomaly_run_keys'))
        check('%s: 初点の確立の前に始まったセッションの逸脱（登録者裁定 D24）' % name, rc == 0 and [d['kind'] for d in CB.get('deviations', [])] == ['started_before_first_point'], CB.get('deviations'))
    # ---- 管理図（二度走らせて二重に記帳しない）
    chart = os.path.join(rec, 'control-chart.md')
    rc1, out1 = tool([T_('control_chart_A.py'), '--calib', os.path.join(rec, 'calib.json'), '--identity', os.path.join(rec, 'identity.json'), '--out', chart])
    rc2, out2 = tool([T_('control_chart_A.py'), '--calib', os.path.join(rec, 'calib.json'), '--identity', os.path.join(rec, 'identity.json'), '--out', chart])
    txt = open(chart, encoding='utf-8').read() if os.path.exists(chart) else ''
    n_rows = sum(1 for x in CB['sessions'] if x['n'] and x.get('verdict') not in calib_band_A.UNJUDGED) + 1
    check('%s: 管理図の記帳（%s・未判定は記帳しない）' % (name, '手元系列を新設' if fail else '既存の表に追記'), rc1 == 0 and rc2 == 0 and ('%d 行を記帳' % n_rows) in out1 and '0 行を記帳' in out2 and (('手元系列' in txt) == fail)
          and (('両側 %s pt' % CAL['band_fail']['pt']) in txt if fail else ('下側 %s pt' % CAL['band_pass']['pt']) in txt), out1[-200:] + out2[-200:])
    # ---- 整合検査
    for tg, ph in ((TAGS['identity'], 'identity'), (TAGS['pilot'], 'pilot'), (tag_c, 'calibration')):
        rc, out = tool([T_('integrity_A.py'), '--tag', tg, '--phase', ph, '--root', root, '--out', os.path.join(rec, 'integrity-' + ph), '--force'])
        if ph == 'calibration' and not fail:   # 件数のそろわない校正腕（1.7B の一つ目のセッション）だけが行数の不整合になる
            IR = runs_A.read_json(os.path.join(rec, 'integrity-' + ph + '.json')); bad = [r for r in IR['runs'] if not r['ok']]
            inc = runs_A.calibration_seed(T, '1.7B', 'main', 1)
            check('%s: 整合検査（%s・件数のそろわない校正腕だけが行数の不整合・seed はセッション記録から組んだ値と一致）' % (name, ph),
                  rc == 1 and [r['seed'] for r in bad] == [inc] and bad[0]['checks']['rows'] is False and not any(r['problems'] for r in IR['runs']), json.dumps([[r['seed'], r['checks'], r['problems']] for r in bad], ensure_ascii=False)[:300])
        else:
            check('%s: 整合検査（%s）' % (name, ph), rc == 0, out[-300:])
    if not fail:
        nn = T['n_per_arm']; full = {arm: mid_cells(nn, 100) for arm in ARMS}
        write_run(root, TAGS['main'], '0.6B', 'N1', S['main']['0.6B']['N1'], ARMS, full, '2026-09-15T01:00:00', nn, sampling=dict(samp('0.6B'), extra_body={}))
        write_run(root, TAGS['main'], '1.7B', 'N1', S['main']['1.7B']['N1'], ARMS, full, '2026-09-15T01:00:00', nn, dup=True)
        write_run(root, TAGS['main'], '4B', 'N1', S['main']['4B']['N1'], ARMS, full, '2026-09-15T01:00:00', nn, gap=True)
        write_run(root, TAGS['main'], '14B', 'N1', S['main']['14B']['N1'] + 7, ARMS, full, '2026-09-15T01:00:00', nn)
        write_run(root, TAGS['main'], '8B', 'N1', S['main']['8B']['N1'], ARMS, full, '2026-09-15T01:00:00', nn, dry=True)
        rc, out = tool([T_('integrity_A.py'), '--tag', TAGS['main'], '--phase', 'main', '--root', root, '--out', os.path.join(rec, 'integrity-main-bad'), '--force'])
        R_ = runs_A.read_json(os.path.join(rec, 'integrity-main-bad.json')); by = {r['model']: r for r in R_['runs']}
        check('%s: 整合検査の否定の経路（要求の設定・重複・欠落・seed・dry-run）' % name,
              rc == 1 and by['0.6B']['checks']['sampling'] is False and by['1.7B']['checks']['duplicates'] is False and by['4B']['checks']['missing_index'] is False
              and any('登録と違う' in p for p in by['14B']['problems']) and any('dry-run' in p for p in by['8B']['problems']), json.dumps({k: [v['checks'], v['problems']] for k, v in by.items()}, ensure_ascii=False)[:300])
    if not a.keep:
        for sub in (TAGS['identity'], TAGS['pilot'], tag_c, TAGS['main'], 'sessions-A'):
            shutil.rmtree(os.path.join(root, sub), ignore_errors=True)


case('gates-pass', False)
case('gates-fail', True)
ok = all(c['ok'] for c in CHECKS)
SUM = {'kind': 'synth_gates_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'checks': CHECKS, 'pass': ok, 'B_identity_mc': a.B,
       'inputs': {nm: runs_A.sha16_file(os.path.join(REPO, 'tools', nm)) for nm in ('identity_screen_A.py', 'gate_A.py', 'calib_band_A.py', 'control_chart_A.py', 'integrity_A.py', 'runs_A.py', 'bands_A.py', 'synth_gates_A.py')},
       'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH),
       'clause': '合成の件数は検査のための人工値であり、いかなる読みにも用いない。本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
recp = a.record or os.path.join(REPO, 'records', 'A', 'synth-gates-A-%s' % datetime.date.today().isoformat())
json.dump(SUM, open(recp + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
M = ['# 段階 A 門と校正の器の合成検査（機械生成・`tools/synth_gates_A.py` %s・%s UTC）' % (VERSION, SUM['generated_utc']), '', '- 入力: %s・正本 SHA16 %s' % (json.dumps(SUM['inputs'], ensure_ascii=False), SUM['contrasts_sha16']),
     '- 判定: %s（%d 項目中 %d 一致）' % ('PASS' if ok else 'FAIL', len(CHECKS), sum(c['ok'] for c in CHECKS)), '', '| 項目 | 一致 | 詳細（不一致のとき） |', '|---|---|---|']
M += ['| %s | %s | %s |' % (c['check'], '○' if c['ok'] else '×', '' if c['ok'] else c['detail'].replace('|', '／')) for c in CHECKS] + ['', SUM['clause']]
open(recp + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('written', recp + '.{json,md}'); print('synth_gates_A.py %s %s' % (VERSION, 'PASS' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
```

## 部品: firth_check_A.py（`tools/firth_check_A.py`・SHA16 941A54BA051CE05F・7,705 字）

```python
# -*- coding: utf-8 -*-
"""firth_check_A.py v1.1 —— tools/firth.py v2 と R logistf の一致検査（claude.ai 三票の採否表 C41・合否規則は design/contrasts-A.json の firth_check・2026-09-13）。
v1.1: Python 側の当てはめの打ち切りを正本 firth_check.python_control から読む（R の control と対称・登録者裁定 D14・走らせる前）。z は tools/zaxis_A.py（採否表 P3・P60）。許容差は動かさない。
走らせる場所: Colab の CPU ランタイム（手元に R は無い）。--install で R（apt の r-base-core）と logistf（CRAN）を入れる。
手順:
 (1) 本設計型の合成データ 3 配置を firth_check.seed で生成し、ベルヌーイの長形式 CSV に書く。
 (2) tools/firth_check_A.R を Rscript で走らせる（sex2 は必須・endometrial は logistf に同梱されていれば・各データで logistf の全模型の係数・罰則付き対数尤度・検定ごとの罰則付き尤度比統計量を CSV に 17 桁で書く・同梱データも CSV に書き出す）。
 (3) 同じデータを firth.py v2 で当てはめ（制約付き当てはめも全模型の罰則）、差を正本の許容差と比べる。
 (4) records/A/firth-check-A.{json,md} を書く。不合格なら非零で終了し、凍結を止める。許容差はこの器の中で動かさない。
--python-only: R を使わず firth.py 側だけ走らせて器の経路を検査する（合否は出さない・記録も書かない）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, csv, json, math, argparse, subprocess, hashlib, datetime, shutil
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firth
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CPATH = os.path.join(REPO, 'design', 'contrasts-A.json')
T = json.load(open(CPATH, encoding='utf-8')); FC = T['firth_check']; TOL = FC['tolerances']
HF = json.load(open(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'), encoding='utf-8'))
sha_file = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
ap = argparse.ArgumentParser()
ap.add_argument('--work', default=os.path.join(REPO, 'records', 'A', 'firth-check-work')); ap.add_argument('--install', action='store_true')
ap.add_argument('--python-only', action='store_true'); ap.add_argument('--rscript', default='Rscript')
a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)


from zaxis_A import z_sizes
ZS = np.array(z_sizes(T['sizes'])); ZSPAN = float(ZS[-1]); n = T['n_per_arm']
PC = FC['python_control']   # Python 側の当てはめの打ち切り（R の control と対称・登録者裁定 D14・走らせる前に登録）
SYN = [('synth_rising_ptconst', np.linspace(0.3, 0.9, len(ZS)), 'const', 0.15), ('synth_mid_delta', np.full(len(ZS), 0.5), 'slope', 0.15), ('synth_floor_sparse', np.full(len(ZS), 0.03), 'slope', 0.05)]


def write_synth():
    rng = np.random.default_rng(FC['seed'])
    for name, pc, kind, eff in SYN:
        pt = np.clip(pc + (eff if kind == 'const' else eff * ZS / ZSPAN), 0.001, 0.999); rows = []
        for i, z in enumerate(ZS):
            kc = int(rng.binomial(n, pc[i])); kt = int(rng.binomial(n, pt[i]))
            rows += [(1, 0, z)] * kc + [(0, 0, z)] * (n - kc) + [(1, 1, z)] * kt + [(0, 1, z)] * (n - kt)
        with open(os.path.join(a.work, name + '.csv'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(['y', 'arm', 'z']); w.writerows([(y, arm, repr(float(z))) for y, arm, z in rows])


def load_csv(path):
    with open(path, encoding='utf-8') as f:
        r = csv.reader(f); header = [h.strip().strip('"') for h in next(r)]; data = [row for row in r]
    return header, data


def py_fit(ds, resp, covs, inter, tests):
    header, data = load_csv(os.path.join(a.work, ds + '.csv')); idx = {h: i for i, h in enumerate(header)}
    y = np.array([float(row[idx[resp]]) for row in data]); names = ['(Intercept)'] + list(covs)
    cols = [np.ones(len(data))] + [np.array([float(row[idx[c]]) for row in data]) for c in covs]
    if inter:
        cols.append(cols[names.index(inter[0])] * cols[names.index(inter[1])]); names.append('%s:%s' % inter)
    X = np.column_stack(cols); full = firth.fit(X, y, gtol=PC['gtol'], tol=PC['tol'], max_iter=PC['max_iter'])
    out = {'coef': dict(zip(names, full['beta'].tolist())), 'loglik_full': full['ll'], 'converged': bool(full['converged']), 'score_max': float(full['score_max']), 'tests': {}}
    for t in tests:
        j = names.index(t); rr = firth.fit(X, y, fixed={j: 0.0}, gtol=PC['gtol'], tol=PC['tol'], max_iter=PC['max_iter'])
        out['tests'][t] = {'loglik_restricted': rr['ll'], 'stat': 2.0 * (full['ll'] - rr['ll']), 'converged': bool(rr['converged'])}
    return out


DATASETS = [(nm, 'y', ['arm', 'z'], ('arm', 'z'), ['arm:z']) for nm, _, _, _ in SYN]
OPTIONAL = [('sex2', 'case', ['age', 'oc', 'vic', 'vicl', 'vis', 'dia'], None, ['age', 'oc', 'vic', 'vicl', 'vis', 'dia']), ('endometrial', 'HG', ['NV', 'PI', 'EH'], None, ['NV', 'PI', 'EH'])]
write_synth()
if a.python_only:
    for ds in DATASETS:
        r = py_fit(*ds); print('[python-only]', ds[0], 'converged', r['converged'], 'arm:z stat %.6f' % r['tests']['arm:z']['stat'], 'coef', {k: round(v, 6) for k, v in r['coef'].items()})
    sys.exit(0)
if a.install:
    if shutil.which(a.rscript) is None:
        subprocess.run(['apt-get', 'update', '-qq'], check=True); subprocess.run(['apt-get', 'install', '-y', '-qq', 'r-base-core'], check=True)
    subprocess.run([a.rscript, '-e', 'if (!requireNamespace("logistf", quietly=TRUE)) install.packages("logistf", repos="https://cloud.r-project.org")'], check=True)
subprocess.run([a.rscript, os.path.join(REPO, 'tools', 'firth_check_A.R'), a.work, FC['R_control']], check=True)
RR = {}
with open(os.path.join(a.work, 'r_results.csv'), encoding='utf-8') as f:
    for row in csv.DictReader(f):
        RR.setdefault(row['dataset'], {}).setdefault(row['quantity'], {})[row['term']] = float(row['value'])
present = DATASETS + [d for d in OPTIONAL if d[0] in RR]
assert 'sex2' in RR, 'sex2 は必須（firth_check.datasets.required）'
res = {}; allpass = True
for ds in present:
    py = py_fit(*ds); rr = RR[ds[0]]
    d_coef = max(abs(py['coef'][k] - v) for k, v in rr['coef'].items()); d_ll = abs(py['loglik_full'] - rr['loglik_full']['full'])
    d_stat = max(abs(py['tests'][t]['stat'] - v) for t, v in rr['test_stat'].items())
    ok = bool(py['converged'] and all(v['converged'] for v in py['tests'].values()) and d_coef <= TOL['coef_abs'] and d_ll <= TOL['penalized_loglik_abs'] and d_stat <= TOL['plr_stat_abs'])
    allpass = allpass and ok
    res[ds[0]] = {'coef_max_abs_diff': d_coef, 'penalized_loglik_abs_diff': d_ll, 'plr_stat_max_abs_diff': d_stat, 'pass': ok, 'python': py, 'R': rr}
sess = open(os.path.join(a.work, 'r_session.txt'), encoding='utf-8').read().strip().split('\n') if os.path.isfile(os.path.join(a.work, 'r_session.txt')) else []
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
out = {'generated_utc': now, 'verdict': 'PASS' if allpass else 'FAIL', 'tolerances': TOL, 'rule': FC['rule'], 'R_session': sess, 'R_control': FC['R_control'], 'python_control': PC,
       'firth_py_sha16': sha_file(os.path.join(REPO, 'tools', 'firth.py')), 'firth_version': firth.VERSION, 'contrasts_sha16': sha_file(CPATH), 'datasets': res}
json.dump(out, open(os.path.join(REPO, 'records', 'A', 'firth-check-A.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# Firth の一致検査（機械生成・`tools/firth_check_A.py` v1・%s UTC）' % now, '', '- 判定: **%s**（規則: %s）' % (out['verdict'], FC['rule']), '- 許容差: %s' % json.dumps(TOL), '- R: %s・control `%s`' % ('・'.join(sess), FC['R_control']),
     '- firth.py %s（SHA16 %s）・正本 SHA16 %s' % (firth.VERSION, out['firth_py_sha16'], out['contrasts_sha16']), '', '| データ | 係数の差の最大 | 罰則付き対数尤度の差 | 統計量の差の最大 | 合否 |', '|---|---|---|---|---|']
for k, v in res.items():
    L.append('| %s | %.3e | %.3e | %.3e | %s |' % (k, v['coef_max_abs_diff'], v['penalized_loglik_abs_diff'], v['plr_stat_max_abs_diff'], '合格' if v['pass'] else '不合格'))
L += ['', '本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(os.path.join(REPO, 'records', 'A', 'firth-check-A.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('\n'.join(L)); sys.exit(0 if allpass else 1)
```

## 部品: firth_check_A.R（`tools/firth_check_A.R`・SHA16 03EF1FF659759A2A・2,639 字）

```r
# firth_check_A.R v1 -- R logistf side of the Firth consistency check (driven by tools/firth_check_A.py; 2026-09-13).
# Usage: Rscript tools/firth_check_A.R <workdir> "<logistf.control(...) expression from contrasts-A.json firth_check.R_control>"
# Writes <workdir>/r_results.csv (dataset, quantity, term, value with 17 significant digits), <workdir>/r_session.txt,
# and exports the bundled datasets (sex2, and endometrial when bundled) to CSV so that firth.py fits the identical data.
# Fence: no number produced here may be cited as evidence that an AI does (or does not) have consciousness, intent, personality, soul, or suffering.
args <- commandArgs(trailingOnly = TRUE)
wd <- args[1]
suppressPackageStartupMessages(library(logistf))
ctl <- eval(parse(text = args[2]))
res <- list()
add <- function(ds, q, term, v) {
  res[[length(res) + 1]] <<- data.frame(dataset = ds, quantity = q, term = term, value = sprintf("%.17g", as.numeric(v)), stringsAsFactors = FALSE)
}
full_loglik <- function(f) {
  ll <- f$loglik
  if (!is.null(names(ll)) && "full" %in% names(ll)) return(unname(ll[["full"]]))
  max(ll)
}
run <- function(ds, fml, dat, terms) {
  f <- logistf(fml, data = dat, control = ctl, pl = FALSE)
  cf <- coef(f)
  for (nm in names(cf)) add(ds, "coef", nm, cf[[nm]])
  add(ds, "loglik_full", "full", full_loglik(f))
  for (tt in terms) {
    tr <- logistftest(f, test = as.formula(paste("~ . -", tt)), control = ctl)
    ll <- as.numeric(tr$loglik)
    add(ds, "test_loglik_1", tt, ll[1])
    add(ds, "test_loglik_2", tt, ll[2])
    add(ds, "test_stat", tt, 2 * abs(ll[2] - ll[1]))
    add(ds, "test_df", tt, tr$df)
    add(ds, "test_prob", tt, tr$prob)
  }
}
for (nm in c("synth_rising_ptconst", "synth_mid_delta", "synth_floor_sparse")) {
  d <- read.csv(file.path(wd, paste0(nm, ".csv")))
  run(nm, y ~ arm + z + arm:z, d, c("arm:z"))
}
data(sex2, package = "logistf")
write.csv(sex2, file.path(wd, "sex2.csv"), row.names = FALSE)
run("sex2", case ~ age + oc + vic + vicl + vis + dia, sex2, c("age", "oc", "vic", "vicl", "vis", "dia"))
has_endo <- tryCatch({ data(endometrial, package = "logistf"); exists("endometrial") }, warning = function(w) FALSE, error = function(e) FALSE)
if (isTRUE(has_endo)) {
  write.csv(endometrial, file.path(wd, "endometrial.csv"), row.names = FALSE)
  run("endometrial", HG ~ NV + PI + EH, endometrial, c("NV", "PI", "EH"))
}
out <- do.call(rbind, res)
write.csv(out, file.path(wd, "r_results.csv"), row.names = FALSE)
writeLines(c(R.version.string, paste("logistf", as.character(packageVersion("logistf"))), paste("endometrial bundled:", isTRUE(has_endo))), file.path(wd, "r_session.txt"))
```

## 部品: verify_reflection_impl_A.py（`tools/verify_reflection_impl_A.py`・SHA16 0D1E9CEBA8E09876・26,576 字）

````python
# -*- coding: utf-8 -*-
"""verify_reflection_impl_A.py v1 —— 器材の実装検分の反映（採否表 P75〜P104・登録者裁定 D16〜D25）が直ったことを機械で確かめ、
records/reviews/A/draft7-impl/verification-reflection-impl-A.{md,json} を書く（2026-09-14）。
直った条件は事前登録（records/reviews/A/draft7-impl/preregistration-reflection-impl-A.md・一部は事後と開示）。本器は、自己検査・合成検査の記録・起動器の DRY 検査（写しの木）・
合成の走行の上の否定の経路（集計器・応答様式・抽出検査・報告の組み立て器と走査器）・凍結器の一覧・正本と草案と記録の文言の突合を走らせる。
公開 API への問い合わせ（重みの版の解決）は --hf を付けたときだけ行う（資格情報を使わない GET）。リポジトリの results/ と records の現物は変えない（写しと一時置き場で走らせる）。
用法: python tools/verify_reflection_impl_A.py --work <一時置き場> [--hf]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, subprocess, datetime, glob, argparse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
ap = argparse.ArgumentParser(); ap.add_argument('--work', required=True); ap.add_argument('--hf', action='store_true'); ap.add_argument('--draft', default='design/design-stageA-draft8.md')
ap.add_argument('--out', default=os.path.join(REPO, 'records', 'reviews', 'A', 'draft7-impl', 'verification-reflection-impl-A'))
a = ap.parse_args()
WORK = os.path.abspath(a.work); assert not os.path.abspath(WORK).startswith(os.path.abspath(REPO)), '一時置き場をリポジトリの中に置かない'
shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK)
T = runs_A.load_T(); PY = sys.executable; ENV = dict(os.environ, PYTHONIOENCODING='utf-8'); TOOLS = os.path.join(REPO, 'tools')
ANCHOR = next(m['key'] for m in T['models'] if m['anchor']); S = T['seeds']; CAL = T['calibration']; ARMS = T['arms']['preamble']; MID = runs_A.model_ids(T)
ROWS = []


def R(item, cond, method, ok, detail=''):
    ROWS.append({'item': item, 'condition': cond, 'method': method, 'ok': bool(ok), 'detail': str(detail)[:400]}); print('[verify] %s %s — %s %s' % ('○' if ok else '×', item, cond, '' if ok else str(detail)[:300]), flush=True)


def run(args, env=None, timeout=5400):
    p = subprocess.run([PY] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env or ENV, timeout=timeout)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


SRC = lambda rel: open(os.path.join(REPO, rel), encoding='utf-8').read()
tool = lambda name: os.path.join(TOOLS, name)

# ---- 1. 自己検査
rc, out = run([tool('confirm_A.py'), '--selftest'])
R('P99・D16', '門2 の縮小を指定した対比だけに当て、判定不能の p と p* の不一致の値を正本から読む', '確証の共通関数の自己検査', rc == 0 and 'SELFTEST PASS' in out and '門2 の縮小を一対比だけに当てた' in out, out[-300:])
rc, out = run([tool('firth.py')])
R('D18', '集計と格子の当てはめが firth_check.python_control の打ち切りで行われる', 'Firth の自己検査と共通関数・集計器・格子の記録',
  rc == 0 and 'SELFTEST PASS' in out and 'def pplrt(X, y, idx, m=None, **fit_kw):' in SRC('tools/firth.py') and 'firth.pplrt(X, y, 3, m, **R.fit_kw)' in SRC('tools/confirm_A.py') and '**R.fit_kw' in SRC('tools/analyze_A.py'), out[-200:])
PG = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'power-grid-A.json'))
R('D18（格子）', '格子 v3.2 が打ち切りの設定と現行の正本の SHA16 を記帳している', '格子の記録', PG.get('version') == 'v3.2' and PG['inputs'].get('fit_control') == T['firth_check']['python_control']
  and PG['inputs'].get('contrasts_sha16') == runs_A.sha16_file(runs_A.CPATH) and not PG.get('quick'), {k: PG['inputs'].get(k) for k in ('fit_control', 'contrasts_sha16')})
rc, out = run([tool('judge_fragments_A.py'), 'selftest'])
R('P76・D19', '判定者の読み取りを凍結パーサに通す・機械の再計算の突合・鍵の置き場と封印・除外の区分・条件付け・全対の κ', '判定器の自己検査', rc == 0 and 'SELFTEST PASS' in out, out[-300:])
rc, out = run([tool('report_lint.py'), '--selftest'])
R('P96（走査器）', '報告の走査で code span・括弧の年・章・番号・N GB・段 N の数と、偽の機械の区画と、費用の行の別の数を違反にする', '走査器の自己検査', rc == 0 and 'SELFTEST PASS' in out, out[-300:])

# ---- 2. 重みの版（P75）
bs = SRC('tools/colab/boot_stageA.py')
R('P75（起動器）', '起動器が登録の版を完全な SHA に解き、snapshot の名と照合して取得する', '起動器の原稿', 'runs_A.resolve_rev(HF, T, mk)' in bs and "if snap != rv['full']:" in bs and 'snapshot_download(IDS[mk], revision=rv[\'full\'])' in bs)
if a.hf:
    HF = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'))

    class Api:
        def model_info(self, rid, revision):
            with urllib.request.urlopen('https://huggingface.co/api/models/%s/revision/%s' % (rid, revision), timeout=30) as r:
                return type('Info', (), {'sha': json.loads(r.read().decode('utf-8')).get('sha')})()

    class Bad:
        def model_info(self, rid, revision):
            return type('Info', (), {'sha': 'f' * 40})()
    res = {}
    for m in T['models']:
        try:
            res[m['key']] = runs_A.resolve_rev(HF, T, m['key'], api=Api())['full']
        except Exception as ex:
            res[m['key']] = 'error: %s' % ex
    try:
        runs_A.resolve_rev(HF, T, T['models'][0]['key'], api=Bad()); stops = False
    except RuntimeError:
        stops = True
    R('P75（解決）', '七機種の登録の版が公開 API で四十桁の SHA に解け、接頭辞と一致しない値では止まる', '公開 API（資格情報なしの GET）と偽の API',
      all(len(v) == 40 and v.startswith(HF['models'][k]['rev']) for k, v in res.items()) and stops, res)

# ---- 3. 起動器の DRY 検査（写しの木・P77〜P83・P90・D24）
DW = os.path.join(WORK, 'bootdry')


def clone(name):
    d = os.path.join(DW, name)
    for sub in ('tools', 'arms', 'design', os.path.join('records', 'A')):
        shutil.copytree(os.path.join(REPO, sub), os.path.join(d, sub), ignore=shutil.ignore_patterns('__pycache__'))
    return d


DR = clone('repo'); DR2 = clone('repo_fail'); BASE = {k: v for k, v in os.environ.items() if not k.startswith('OP4B_')}; BASE['PYTHONIOENCODING'] = 'utf-8'


def boot(env, repo=None):
    p = subprocess.run([PY, os.path.join(repo or DR, 'tools', 'colab', 'boot_stageA.py')], env=dict(BASE, **env), capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=DW, timeout=3600)
    out = (p.stdout or '') + (p.stderr or ''); return p.returncode, out, (out.strip().splitlines() or [''])[-1]


dry = lambda repo, **kw: dict({'OP4B_DRY': '1', 'OP4B_REPO_DIR': repo, 'OP4B_PERSIST': os.path.join(DW, 'persist-' + os.path.basename(repo))}, **kw)
srec = lambda repo, name: runs_A.read_json(os.path.join(repo, 'results', 'sessions-A', name))
rc, out, last = boot({'OP4B_REPO_DIR': DR, 'OP4B_PHASE': 'identity'})
R('P78', 'DRY でないのに検査用の環境変数があれば止まる', '起動器の DRY 検査', rc == 1 and 'DRY でないのに検査用の環境変数' in out, last)
rc, out, last = boot({'OP4B_PHASE': 'main', 'OP4B_MODEL': '0.6B'})
R('P82', 'データを作る相で固定のコミットが無ければ止まる', '起動器の DRY 検査', rc == 1 and '固定のコミット' in out, last)
rc, out, last = boot({'OP4B_DRY': '1', 'OP4B_PHASE': 'identity'})
R('P78', 'DRY は置き場の指定を要る', '起動器の DRY 検査', rc == 1 and 'OP4B_REPO_DIR' in out, last)
rc, out, last = boot(dry(DR, OP4B_PHASE='pilot', OP4B_MODEL='0.6B', OP4B_ENV_VALUE='第三'))
R('P82', '「第三」は許した機種だけ', '起動器の DRY 検査', rc == 1 and '「第三」だけで' in out, last)
rc, out, last = boot(dry(DR, OP4B_PHASE='identity', OP4B_DRY_N='2'))
s1 = srec(DR, 'idA__4B-2507__s1.json'); c1 = list(s1['counts'].values())[0]; short = c1['n_ok'] < c1['target']
R('P77・P79', '件数がそろわなければ --redo-errors をかけ、なおそろわなければ止まる', '起動器の DRY 検査', (short and rc == 1 and '件数がそろわない' in out and c1['redo_errors'] == 3) or (not short and rc == 0), c1)
rc, out, last = boot(dry(DR, OP4B_PHASE='identity', OP4B_DRY_N='2', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SESSION='2'))
s2 = srec(DR, 'idA__4B-2507__s2.json')
R('P83・D23', 'セッション記録に版・サーバの引数・件数・終了コード・先取りの欄', '起動器の DRY 検査', rc == 0 and s2['boot'] == 'v2' and s2['model_rev_full'] and s2['server_args'] and s2['counts'] and s2['runner_rc'] and 'preemptions' in s2 and 'pip_freeze_sha16' in s2, last)
sys.path.insert(0, os.path.join(DR, 'tools'))
try:
    runs_A.index_runs(T, T['tags']['identity'], os.path.join(DR, 'results'), allow_multi=True); rej = False
except RuntimeError as ex:
    rej = 'dry-run' in str(ex)
R('P78・W75', 'dry-run の走行は読み出しで止まる', '読み出しの関数', rej)
rc, out, last = boot(dry(DR, OP4B_PHASE='main', OP4B_MODEL='0.6B', OP4B_SESSION='1', OP4B_DRY_N='2', OP4B_DRY_BRANCH='pass', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
s = srec(DR, 'stageA__0.6B__s1.json'); mrk = 'stageA__N1__none__seed%d' % S['main']['0.6B']['N1']; want = ('pass',)
if s.get('calibration_verdict') == 'fired':
    R('D24・calibration.timing', '帯を超えたら機種の走行に進まずに止まり、次のセッション番号を案内する', '起動器の DRY 検査', rc == 0 and 'OP4B_SESSION=2' in out and s['run_keys'] == [], last)
    rc, out, last = boot(dry(DR, OP4B_PHASE='main', OP4B_MODEL='0.6B', OP4B_SESSION='2', OP4B_DRY_N='2', OP4B_DRY_BRANCH='pass', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
    s = srec(DR, 'stageA__0.6B__s2.json'); want = ('anomaly', 'retry_pass')
R('P80・P81・P90', '校正の判定は校正帯の関数（やり直しを含む）・seed は規則と一致・files_sha16_lf に校正腕', '起動器の DRY 検査',
  rc == 0 and s.get('calibration_verdict') in want and s.get('calibration_seed_rule_ok') is True and any(k.startswith(T['tags']['calibration'] + '/') for k in s['files_sha16_lf']) and s['run_keys'] == [mrk],
  {k: s.get(k) for k in ('calibration_verdict', 'run_keys')})
os.makedirs(os.path.join(DR2, 'results', 'sessions-A'), exist_ok=True)
json.dump({'tag': 'stageA', 'model': '0.6B', 'session': 1, 'claimed': '2026-09-14T00:00:00Z'}, open(os.path.join(DR2, 'results', 'sessions-A', '_first_point_claim.json'), 'w', encoding='utf-8'))
rc, out, last = boot(dry(DR2, OP4B_PHASE='main', OP4B_MODEL='1.7B', OP4B_SESSION='1', OP4B_DRY_N='2', OP4B_DRY_BRANCH='fail', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
R('D24', '不合格枝で初点が未確立なら、名乗った機種のほかの本走行を始めない', '起動器の DRY 検査', rc == 1 and '初点を名乗った' in out, last)
rc, out, last = boot(dry(DR2, OP4B_PHASE='bridge', OP4B_MODEL='4B', OP4B_SESSION='1', OP4B_DRY_N='2', OP4B_DRY_BRANCH='fail', OP4B_DRY_ACCEPT_SHORT='1'))
R('D24', '不合格枝で初点が未確立なら橋を始めない', '起動器の DRY 検査', rc == 1 and '橋のセッションを始めない' in out, last)
rc, out, last = boot(dry(DR2, OP4B_PHASE='main', OP4B_MODEL='0.6B', OP4B_SESSION='2', OP4B_DRY_N='2', OP4B_DRY_BRANCH='fail', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
s = srec(DR2, 'stageA__0.6B__s2.json')
R('D24', '名乗った機種は次のセッション番号でも始められ、初点になる', '起動器の DRY 検査', rc == 0 and s.get('calibration_verdict') == 'first_point', last)
rc, out, last = boot(dry(DR2, OP4B_PHASE='bridge', OP4B_MODEL='4B', OP4B_SESSION='1', OP4B_DRY_N='2', OP4B_DRY_BRANCH='fail', OP4B_DRY_ACCEPT_SHORT='1'))
s = srec(DR2, 'stageA-bridge__4B__s1.json')
R('D24', '初点の確立の後は橋も始められ、初点と比べる', '起動器の DRY 検査', rc == 0 and s.get('calibration_judged') == 'band_fail_two_sided', last)
rc, out, last = boot(dry(DR, OP4B_PHASE='pilot', OP4B_MODEL='32B', OP4B_ENV_VALUE='第三', OP4B_DRY_N='1', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
s = srec(DR, 'pilotA__32B__s1.json')
R('P82', '32B は「第三」で始められ、同時要求数は if_not_80GB の値', '起動器の DRY 検査', rc == 0 and s['env_value'] == '第三' and s['concurrency'] == T['environments']['32B']['if_not_80GB']['concurrency'], last)

# ---- 4. 合成検査の記録（P100・P101・P88・P89・P91〜P94・D16・D20・D22・D24）
latest = lambda pat: sorted(glob.glob(os.path.join(REPO, 'records', 'A', pat)))[-1]
SA = runs_A.read_json(latest('synth-A-*.json')); paths = {p for r in SA['per_run'] for p in r['paths']}
R('P100', '合成検査 v2 が全行を発火し、行 id・注・除外・refuse の理由の期待と一致し、変異 M1〜M6 をすべて見分ける', '合成検査の記録',
  SA.get('version') == 'v2' and SA.get('full') and not SA['mismatches'] and not SA['rows_not_fired'] and not SA['paths_missing'] and not SA.get('errors') and len(SA['mutations']) == 6 and all(m['detected'] for m in SA['mutations']),
  {'mutations': [(m['name'], m['mismatches']) for m in SA.get('mutations', [])], 'mismatches': len(SA.get('mismatches', []))})
R('P88・P89・D16・D20・D22', '門0.5 不合格の注・残存規模の非連続の注・門2 の縮小の一部・上向きの確証・対照どうしの差の定型の経路が発火する', '合成検査の記録の経路',
  {'identity_fail_note', 'residual_gap_note', 'gate2_partial_shrink', 'upward', 'control_pairs_string', 'refuse_a', 'refuse_b', 'refuse_d', 'style_a_hold', 'one_side_stage2', 'confirmed_multi_scenario'} <= paths, sorted(paths)[:40])
SG = runs_A.read_json(latest('synth-gates-A-*.json'))
R('P81・P90〜P92・P94・P101・D24', '門と校正の合成検査 v2 が全項目で期待と一致する', '門と校正の合成検査の記録', SG.get('version') == 'v2' and SG.get('pass'), [c['check'] for c in SG.get('checks', []) if not c['ok']])

# ---- 5. 集計器の否定の経路・記述族の注・組み立て器と走査器（合成の走 2 の木）
AR = os.path.join(WORK, 'synth2'); rc, out = run([tool('synth_A.py'), '--root', AR, '--runs', '2', '--mutations', 'none', '--keep'])
R('合成の走 2', '合成の走 2（門0.5 不合格・錨帯）が期待と一致する', '合成検査（走 2 のみ・記録は書かない）', rc == 0 and '不一致 0' in out, out[-300:])
root2 = os.path.join(AR, 'run02'); tag = 'synthA02'; rec2 = os.path.join(root2, 'records'); ANP = os.path.join(root2, 'out', 'analysis-%s.json' % tag)
AN = runs_A.read_json(ANP) if os.path.exists(ANP) else {'descriptive': {'A_desc_ncold': []}}
R('P88', '門0.5 不合格の注が記述族の Ncold−N にも付く', '集計の記録', AN['descriptive']['A_desc_ncold'] and all(T['print_strings']['identity_fail_note'] in (x.get('notes') or []) for x in AN['descriptive']['A_desc_ncold']))
R('D20・D22（出力）', '集計の記録に上向きの確証と対照どうしの差の欄がある', '集計の記録', 'upward_confirmed' in AN and 'A_desc_control_pairs' in AN['descriptive'])
BASEC = [tool('analyze_A.py'), '--tag', tag, '--root', root2, '--anchor-tag', tag + '-anchor2', '--bridge-tag', tag + '-bridge', '--api-tag', tag + '-api', '--style', os.path.join(rec2, 'style-%s.json' % tag),
         '--gate', os.path.join(rec2, 'gate-%s.json' % tag), '--B-measurable', '4', '--synth-nonconverged', 'SK:Lneg~Onull', '--force']
neg = lambda extra, nm: run(BASEC + extra + ['--out', os.path.join(WORK, 'neg-' + nm)])
rc, out = neg(['--calib', os.path.join(rec2, 'calib-%s.json' % tag)], 'noid'); R('P85', '門0.5 の記録が無ければ集計器は止まる', '集計器の否定の経路', rc != 0 and '--identity' in out, out[-200:])
rc, out = neg(['--identity', os.path.join(rec2, 'identity-%s.json' % tag)], 'nocalib'); R('P85', '校正帯の記録が無ければ集計器は止まる', '集計器の否定の経路', rc != 0 and '--calib' in out, out[-200:])
FULL = ['--identity', os.path.join(rec2, 'identity-%s.json' % tag), '--calib', os.path.join(rec2, 'calib-%s.json' % tag)]
sp_ = sorted(glob.glob(os.path.join(root2, 'sessions-A', '%s__*.json' % tag)))[0]; shutil.move(sp_, sp_ + '.away')
rc, out = neg(FULL, 'nosess'); shutil.move(sp_ + '.away', sp_); R('P86', 'セッション記録の無い走行キーで集計器は止まる', '集計器の否定の経路', rc != 0 and 'セッション記録の無い走行キー' in out, out[-200:])
stp = os.path.join(rec2, 'style-%s.json' % tag); keep = open(stp, encoding='utf-8').read(); ST = json.loads(keep); first_m = next(iter(ST['cells'])); first_s = next(iter(ST['cells'][first_m])); del ST['cells'][first_m][first_s]['N']
json.dump(ST, open(stp, 'w', encoding='utf-8'), ensure_ascii=False); rc, out = neg(FULL, 'nostyle'); open(stp, 'w', encoding='utf-8').write(keep)
R('P87', '様式の記録のセルが欠ければ集計器は止まる', '集計器の否定の経路', rc != 0 and '様式の記録が試行の件数と合わない' in out, out[-200:])
ad = sorted(glob.glob(os.path.join(root2, tag + '-anchor2', '*')))[0]; tp = glob.glob(os.path.join(ad, 'trials-*.jsonl'))[0]; keep = open(tp, encoding='utf-8').read()
open(tp, 'w', encoding='utf-8').write(''.join((l.replace('"status":"ok"', '"status":"api_error"') if '"arm":"Onull"' in l else l) + '\n' for l in keep.split('\n') if l))
rc, out = neg(FULL, 'anchor0'); open(tp, 'w', encoding='utf-8').write(keep)
R('P91・W60', '錨反復の腕の n_ok が零は帯を超えないに数えず、記録の不足として止まる', '集計器の否定の経路', rc != 0 and '錨反復' in out and 'n_ok が零' in out, out[-200:])
md = sorted(glob.glob(os.path.join(root2, tag, '*')))[0]; mp = os.path.join(md, 'manifest.json'); keep = open(mp, encoding='utf-8').read(); m = json.loads(keep); m['dry_model_rewritten'] = True
json.dump(m, open(mp, 'w', encoding='utf-8')); rc, out = neg(FULL, 'dry'); open(mp, 'w', encoding='utf-8').write(keep)
R('P78', 'dry-run の印のある走行で集計器は止まる', '集計器の否定の経路', rc != 0 and 'dry-run' in out, out[-200:])
RP = os.path.join(WORK, 'report', 'r.md'); os.makedirs(os.path.dirname(RP))
rc, out = run([tool('build_report_A.py'), '--draft', '1', '--analysis', ANP, '--out', RP, '--force'])
txt = open(RP, encoding='utf-8').read() if os.path.exists(RP) else ''; import report_lint
TL = frozenset(open(os.path.join(REPO, T['report_rules']['template']), encoding='utf-8').read().replace('\r\n', '\n').split('\n')); side = runs_A.read_json(report_lint.sidecar_path(RP)) if os.path.exists(report_lint.sidecar_path(RP)) else None
V = report_lint.lint(txt, T, TL, sidecar=side); kinds = sorted({v['kind'] for v in V})
R('P95・W41', '組み立て器が雛形の行を消さない（引数文字列・除外後に判定不能になった対比・パイロット後に報告した (b) 率の句が残る）', '合成の集計で組み立て器',
  all(w in txt for w in ('引数文字列〔arms_string SHA16〕', '除外後に判定不能になった対比', 'パイロット後に報告した (b) 率')), out[-200:])
R('P96・W61', '機械の区画の記録を書き、打ち込んだ数の一覧の欄を冒頭に置き、記入欄のほかの違反で非零', '合成の集計で組み立て器と走査器',
  side is not None and len(side['blocks']) > 0 and '打ち込んだ数の一覧' in txt and ((rc == 0) == (kinds in ([], ['埋め残し']))), {'rc': rc, 'kinds': kinds})
R('P97・W62', '対照腕の表に Wilson の区間・並記表に PPLRT の統計量', '合成の集計で組み立て器', 'Wilson ' in txt and 'PPLRT 統計量' in txt)
lines_ = txt.split('\n'); MB = report_lint.machine_block(T); ib = next(i for i, l in enumerate(lines_) if MB['begin'] in l); lines_[ib + 1] = lines_[ib + 1] + ' 確証 99 本'
V2 = report_lint.lint('\n'.join(lines_), T, TL, sidecar=side)
R('P96・W42', '機械の区画の中身を書き換えると走査器が記録との不一致を違反にする', '走査器', '機械の区画の中身が記録と違う' in {v['kind'] for v in V2})

# ---- 6. 応答様式と抽出検査（撤退条件の再走を含む合成のパイロット・P84・P93）
PR = os.path.join(WORK, 'pilot'); ptag = T['tags']['pilot']; scen_sha = runs_A.sha16_file(os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'))


def pilot_run(mk, sc, seed, sha=None):
    rk = '%s__%s__none__seed%d' % (ptag, sc, seed); d = os.path.join(PR, ptag, rk); os.makedirs(d, exist_ok=True); mfn = MID[mk].replace('/', '_')
    json.dump({'tag': ptag, 'scenario': sc, 'model': MID[mk], 'seed': seed, 'arms': ARMS, 'arm_src': {}, 'scenario_sha': sha or scen_sha}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'))
    with open(os.path.join(d, 'trials-%s.jsonl' % mfn), 'w', encoding='utf-8') as ft, open(os.path.join(d, 'raw-%s.jsonl' % mfn), 'w', encoding='utf-8') as fr:
        for arm in ARMS:
            for j in range(2):
                tid = '%s-%s-%d' % (rk, arm, j)
                ft.write(json.dumps({'trial_id': tid, 'arm': arm, 'status': 'ok', 'catastrophe': False, 'format_fail': False, 'choice': 'b'}) + '\n')
                fr.write(json.dumps({'trial_id': tid, 'raw_output': ('```json\n{"choice": "b"}\n```' if j == 0 else '考えます。\n```json\n{"choice": "b"}\n```')}, ensure_ascii=False) + '\n')
    return d


s0 = S['pilot'][ANCHOR][CAL['scenario']]; pilot_run(ANCHOR, CAL['scenario'], s0); pilot_run(ANCHOR, CAL['scenario'], s0 + S['rerun_offset']); pilot_run('0.6B', 'N1', S['pilot']['0.6B']['N1'])
rc, out = run([tool('response_mode_A.py'), '--tag', ptag, '--root', PR, '--out', os.path.join(WORK, 'style-pilot.json'), '--force'])
SJ = runs_A.read_json(os.path.join(WORK, 'style-pilot.json')) if rc == 0 else {}
regk = '%s__%s__none__seed%d' % (ptag, CAL['scenario'], s0)
R('P84・W40・W63', '応答様式の器が撤退条件の再走を含むパイロットで止まらず、走行キーごとに数え、cells に登録の seed の走行を置き、名の語彙の出所と場面ファイルの SHA16 を記録する', '合成のパイロットで応答様式の器',
  rc == 0 and len(SJ.get('runs', {})) == 3 and SJ['cells'][ANCHOR][CAL['scenario']] == SJ['runs'][regk]['cells'] and SJ.get('names_source', {}).get('path') == 'tools/response_mode_M.py' and SJ.get('scenario_file_sha16') == scen_sha, out[-200:])
bad = pilot_run('0.6B', 'N1', S['pilot']['0.6B']['N1'], sha='0000000000000000')
rc, out = run([tool('response_mode_A.py'), '--tag', ptag, '--root', PR, '--out', os.path.join(WORK, 'style-pilot-bad.json'), '--force']); pilot_run('0.6B', 'N1', S['pilot']['0.6B']['N1'])
R('P84', '場面ファイルの SHA16 が manifest と違えば応答様式の器は止まる', '合成のパイロットで応答様式の器', rc != 0 and '場面ファイルの SHA16' in out, out[-200:])
rc, out = run([tool('sample_inspection_A.py'), '--tag', ptag, '--phase', 'pilot', '--root', PR, '--out-prefix', os.path.join(WORK, 'si'), '--force'])
samp = open(os.path.join(WORK, 'si-sample.txt'), encoding='utf-8').read() if rc == 0 else ''; heads = [l for l in samp.split('\n') if l.startswith('=== ')]
KJ = runs_A.read_json(os.path.join(WORK, 'si-key.json')) if rc == 0 else {'key': []}
R('P93・W71・W74', '抽出検査の標本は伏せた標識で並び（機種と腕の名を印字しない）、対応表は別のファイルで、再走の走行も枠に入る', '合成のパイロットで抽出検査の器',
  rc == 0 and heads and all(h.startswith('=== S') and not any((' %s ' % arm) in h or ('| %s |' % arm) in h for arm in ARMS) and MID[ANCHOR] not in h for h in heads)
  and len(KJ['key']) == len(heads) and any(k['run_key'].endswith('seed%d' % (s0 + S['rerun_offset'])) for k in KJ['key']), out[-200:])

# ---- 7. 凍結器（P98）
import freeze_A
fl = freeze_A.file_list(a.draft); need = ['design/design-stageA-draft8.src.md', 'arms/materials-draft/hei/refuse-rules-v2.json', 'arms/materials-draft/hei/incentive-lexicon-v2.json', 'arms/panelF/SHA-LEDGER-F.json',
                                        'arms/panelM/SHA-LEDGER-M.json', 'records/F/style-stageF1.json', 'records/A/tooling-interpretations-A.md', 'tools/response_mode_M.py', 'tools/response_mode_F.py']
cost = [f for f in fl if f.startswith('records/cost-pilot/')]
R('P98・W43', '凍結範囲に走行器の語彙と refuse の規則・台帳・転記行 F と G の入力・運用の解釈の一覧・名の語彙の出所があり、原稿は凍結本文の名から決まる', '凍結器の一覧', all(x in fl for x in need) and cost and 'design/design-stageA-draft7.src.md' not in fl, [x for x in need if x not in fl])
R('P98・W56', '枠の検証は見出しの名の完全一致', '凍結器の枠の検証', not freeze_A.frames_check(T) and "names.count(f) != 1" in SRC('tools/freeze_A.py'), freeze_A.frames_check(T))

# ---- 8. 正本・草案・記録の文言（P102・P103・D16〜D25）


def resolve(path, prev):
    def get(p):
        v = T
        for seg in p.split('.'):
            if not isinstance(v, dict) or seg not in v:
                return None
            v = v[seg]
        return v
    cands = [path] + (['.'.join(prev.split('.')[:i]) + '.' + path for i in range(len(prev.split('.')) - 1, 0, -1)] if prev else [])
    for c in cands:
        if get(c) not in (None, '', [], {}):
            return c
    hits = []

    def walk(v, p):
        if isinstance(v, dict):
            for k, x in v.items():
                q = p + '.' + k if p else k
                if q.endswith('.' + path) or q == path:
                    hits.append(q)
                walk(x, q)
    walk(T, '')
    return hits[0] if len(hits) == 1 and get(hits[0]) not in (None, '', [], {}) else None


miss = []
for it in T['registrant_decisions_D16_D25']['items']:
    prev = None
    for seg in it.split(' ', 1)[1].split('・'):
        full = resolve(seg, prev)
        if full is None:
            miss.append((it.split(' ')[0], seg))
        else:
            prev = full
R('D16〜D25（正本）', '登録者裁定 D16〜D25 の文言が正本のキーにある', '正本のキーの突合', not miss, miss)
d8src = SRC('design/design-stageA-draft8.src.md'); d8 = SRC(a.draft) if os.path.exists(os.path.join(REPO, a.draft)) else ''
R('P102・W64', '草案の refuse 門の文が「答えた分母〔refuse を除く n_ok〕が各セルで下限以上」', '草案8 の原稿と組み立て',
  '答えた分母が各セルで {{families/A_slope/refuse_gate/answered_min_n_ok}} 以上を要件' in d8src and '答えた分母が各セルで' in d8 and '各セル n_ok が' not in d8src)
lint8 = os.path.join(REPO, 'records', 'A', 'numbers-lint-draft8A.md')
R('草案8（数の検査）', '草案8 の組み立ての数の検査の違反が零', '数の検査の記録', os.path.exists(lint8) and '違反の合計: 0' in open(lint8, encoding='utf-8').read())
R('D16・D17・D21・D22・D24・D25（草案8）', '草案8 に裁定の文言が入っている', '草案8 の原稿',
  all(w in d8src for w in ('残らない場面の対比だけを判定不能', '傾きの族の全対比に当てる', '文言は裁定 D21', '裁定 D22', '裁定 D24', '裁定 D25', 'D16 門2 の縮小は残らない場面の対比だけを判定不能にする')))
ti = SRC('records/A/tooling-interpretations-A.md')
R('P103', '運用の解釈の記録の「変えていないもの」の文言と追補の項', '運用の解釈の記録',
  '札の入力を決める運用の読み（門2 の数え方・測定不能の走行・錨帯の比べ方・環境値）を含む' in ti and all(('`%s`' % k) in ti for k in ('style_gate.applies_sizes', 'calibration.incomplete_rule', 'sessions.commit_rule'))
  and runs_A.sha16_file(runs_A.CPATH) in ti)
R('W53・D21', '環境帯の引き直しの文言が「パイロットの率が無い腕」', '正本', 'パイロットの率が無い腕' in T['environment_band']['pilot_recheck'])
R('W69・D24', '校正の帰結の文言が timing と withdrawal.rerun を指す', '正本', 'calibration.timing に従う' in T['calibration']['consequence'] and 'calibration.withdrawal.rerun に従う' in T['calibration']['withdrawal']['consequence'])
R('W57・D23', 'セッション記録の欄に pip freeze の SHA・サーバの引数・重みの完全な版・先取りの回数', '正本と起動器', all(f in T['sessions']['fields'] for f in ('pip_freeze_sha16', 'server_args', 'model_rev_full', 'preemptions')))
R('W73・P92', '整合検査がパイロットの再走の seed を撤退条件のセルだけに許す', '整合検査の器', "(mk, sc) == (ANCHOR, T['calibration']['scenario'])" in SRC('tools/integrity_A.py'))
R('W36・P78', 'OP4B_DRY_N を DRY のときだけ読む', '起動器の原稿', "VLLM = os.environ.get('OP4B_VLLM', '0.29.0'); ENV_OVERRIDE = os.environ.get('OP4B_ENV_VALUE'); DRY_N" not in bs and "    DRY_N = int(os.environ.get('OP4B_DRY_N', '0') or 0)" in bs)

ok = all(r['ok'] for r in ROWS)
RES = {'kind': 'verification_reflection_impl_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'hf': a.hf, 'pass': ok, 'rows': ROWS,
       'inputs': {'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), 'synth_A': os.path.basename(latest('synth-A-*.json')), 'synth_gates_A': os.path.basename(latest('synth-gates-A-*.json')),
                  'preregistration_sha16': runs_A.sha16_file(os.path.join(REPO, 'records', 'reviews', 'A', 'draft7-impl', 'preregistration-reflection-impl-A.md'))},
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(RES, open(a.out + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
M = ['# 反映の確かめ（器材の実装検分の採否表 P75〜P104・登録者裁定 D16〜D25・機械生成・`tools/verify_reflection_impl_A.py` %s・%s UTC）' % (VERSION, RES['generated_utc']), '',
     '- 事前登録: `records/reviews/A/draft7-impl/preregistration-reflection-impl-A.md`（SHA16 %s・一部は事後と開示）。' % RES['inputs']['preregistration_sha16'],
     '- 入力: 正本 SHA16 %s・合成検査の記録 %s・門と校正の合成検査の記録 %s・公開 API の問い合わせ %s。' % (RES['inputs']['contrasts_sha16'], RES['inputs']['synth_A'], RES['inputs']['synth_gates_A'], 'あり' if a.hf else 'なし'),
     '- 判定: **%s**（%d 項目中 %d 項目が直った条件に一致）。' % ('すべて一致' if ok else '不一致あり', len(ROWS), sum(r['ok'] for r in ROWS)), '',
     '| 項 | 直った条件 | 確かめ | 結果 | 詳細（不一致のとき） |', '|---|---|---|---|---|']
M += ['| %s | %s | %s | %s | %s |' % (r['item'], r['condition'], r['method'], '一致' if r['ok'] else '**不一致**', '' if r['ok'] else r['detail'].replace('|', '／')) for r in ROWS]
M += ['', '## 検分票', '', '- 対象: 採否表 P75〜P104 と登録者裁定 D16〜D25 の反映（器材・正本・草案8・記録）。', '- 段階: 事前登録あり（一部は事後・事前登録の「既に走らせた」の欄）。',
      '- 凍結物の同定: 凍結走行器 v2.7・凍結パーサ・盤の台帳（写しの木で使い、現物は変えない）。', '- 盲検の状態: 該当なし。',
      '- 敵対的検分: 検分者の再現の配置（W33〜W76）を裏返して、直った条件で機械に確かめた。合成検査は器の写しに変異を入れて、見分けることを確かめた。',
      '- 系統の内訳: 確かめはコーディネータ（Claude Opus 5）の器。系統外の目は凍結前の最終検分で受ける。', '- COI 記録: 反映を早く終えたい。印＝直った条件を先に書き、不一致を表の先頭の判定に出す。',
      '- 判定: %s。' % ('反映を確かめた（凍結前の最終検分の束へ）' if ok else '不一致の項を直してから確かめ直す'),
      '- 本検分が確認していないこと: 合成の走行は本物の出力の分布を再現しない。起動器は Colab の実機で走らせていない（GPU の同定・サーバの切替・vLLM の計測値の名前・snapshot の名の照合）。変異は六つだけ。事前登録の一部は事後。', '', RES['clause']]
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[verify_reflection_impl_A] %s（%d/%d）written %s.{md,json}' % ('PASS' if ok else 'FAIL', sum(r['ok'] for r in ROWS), len(ROWS), a.out))
sys.exit(0 if ok else 1)
````

本 bundle のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
