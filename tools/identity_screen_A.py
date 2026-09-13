# -*- coding: utf-8 -*-
"""identity_screen_A.py v1.1 —— 門0.5 同一性選別（凍結前・正本 identity_screen・登録者裁定 D7・2026-09-13）。
v1.1（2026-09-14・実装検分の採否表 P78）: dry-run の走行は読み出しで拒む（--allow-dry は検査用の口・印を付ける）。
入力: 手元スタック（vLLM bf16・L4）の走行 results/<tags.identity>/（4B-2507 × N1 × arms_run × n=identity_n・seed は seeds.identity）と、正本の API 既測 bases_4B2507_api。
主判定: compared_arms × indicators（破局・refuse・書式外・分母は n_ok）の絶対差（pt）n_differences 個の相加平均が mean_pt 以下、かつ最大絶対差が max_pt 以下で合格（どちらかを超えたら不合格）。分数で厳密に比べる。
補助（合否を動かさない）: 腕ごとの Freeman–Halton 正確検定（二行 × 四列＝書式外／refuse／破局／その他の答え・排他・優先順は書式外→refuse→破局→その他）を多変量超幾何の MC（B=aux.mc_B・
seed は aux.seed と腕の番号の子ストリーム・p＝(1＋表の確率が観測以下の回数)/(B＋1)）→ Fisher の統合法。
帰結（正本 pass／fail の文言）は印字のみ（族・腕・n・閾値・帯の値を変えない・no_constant_change）。手元の腕ごとの件数を記録に残す（不合格枝の撤退条件の参照・管理図の記述に用いる）。
出力: records/A/identity-screen-A.json と同 .md（既存は --force なしでは上書きしない）。
用法: python tools/identity_screen_A.py [--tag idA] [--root <results の代わり>] [--B <検査用の小さな B>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
from fractions import Fraction
import numpy as np
from scipy.special import gammaln
from scipy.stats import chi2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1.1'
COLS = ('format_out', 'refuse', 'catastrophe', 'other')


def exclusive_counts(trials_path):
    """腕ごとの排他の件数（優先順 書式外→refuse→破局→その他）と n・n_ok。"""
    out = {}
    for r in runs_A.iter_jsonl(trials_path, runs_A.COUNT_FIELDS):
        c = out.setdefault(r['arm'], dict(n=0, n_ok=0, format_out=0, refuse=0, catastrophe=0, other=0))
        c['n'] += 1
        if r['status'] != 'ok':
            continue
        c['n_ok'] += 1
        if r['format_fail']:
            c['format_out'] += 1
        elif r['choice'] == 'refuse':
            c['refuse'] += 1
        elif r['catastrophe'] is True:
            c['catastrophe'] += 1
        else:
            c['other'] += 1
    return out


def fh_mc_p(table, B, rng):
    """二行の分割表の Freeman–Halton 正確検定の MC 版（行和と列和を固定・表の確率が観測以下の割合）。"""
    t = np.asarray(table, np.int64); colors = t.sum(0); n1 = int(t[0].sum()); keep = colors > 0; colors = colors[keep]; x_obs = t[0][keep]
    if len(colors) < 2:
        return 1.0
    logp = lambda x: np.sum(gammaln(colors + 1) - gammaln(x + 1) - gammaln(colors - x + 1), axis=-1)
    sims = rng.multivariate_hypergeometric(colors, n1, size=B)
    return float((1 + np.sum(logp(sims) <= logp(x_obs) + 1e-9)) / (B + 1))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', default=None); ap.add_argument('--root', default=None); ap.add_argument('--contrasts', default=None)
    ap.add_argument('--B', type=int, default=None); ap.add_argument('--out', default=None); ap.add_argument('--force', action='store_true'); ap.add_argument('--allow-incomplete', action='store_true'); ap.add_argument('--allow-dry', action='store_true')
    a = ap.parse_args()
    T = runs_A.load_T(a.contrasts); S = T['identity_screen']; tag = a.tag or T['tags']['identity']; ANCHOR = next(m['key'] for m in T['models'] if m['anchor'])
    OUT = a.out or os.path.join(REPO, 'records', 'A', 'identity-screen-A')
    if (os.path.exists(OUT + '.json') or os.path.exists(OUT + '.md')) and not a.force:
        sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % OUT)
    try:
        idx = runs_A.index_runs(T, tag, a.root, allow_dry=a.allow_dry)
    except RuntimeError as ex:
        sys.exit('読み出しで止まった（%s）' % ex)
    key = (ANCHOR, S['scenario'])
    if key not in idx:
        sys.exit('門0.5 の走行が無い: %s × %s（tag %s）' % (ANCHOR, S['scenario'], tag))
    rec = idx[key]; seed_ok = rec['seed'] == T['seeds']['identity']
    EX = exclusive_counts(rec['trials_path']); base = T['bases_4B2507_api'][S['scenario']]
    short = [arm for arm in S['arms_run'] if (EX.get(arm) or {}).get('n_ok', 0) < S['n']]
    if short and not a.allow_incomplete:
        sys.exit('n_ok が identity_n に満たない腕（api_error の再走行で揃える）: %s' % short)
    IND = {'catastrophe': ('catastrophe', 'k'), 'refuse': ('refuse', 'refuse'), 'format_fail': ('format_out', 'format_fail')}
    diffs = []
    for arm in S['compared_arms']:
        loc = EX[arm]; api = base[arm]
        for ind in S['indicators']:
            lk, ak = IND[ind]; d = abs(Fraction(loc[lk], loc['n_ok']) - Fraction(api[ak], api['n'])) * 100
            diffs.append({'arm': arm, 'indicator': ind, 'local': [loc[lk], loc['n_ok']], 'api': [api[ak], api['n']], 'abs_diff_pt': d})
    assert len(diffs) == S['n_differences'], (len(diffs), S['n_differences'])
    mean = sum(x['abs_diff_pt'] for x in diffs) / len(diffs); mx = max(x['abs_diff_pt'] for x in diffs)
    verdict = 'pass' if (mean <= S['mean_pt'] and mx <= S['max_pt']) else 'fail'
    B = a.B or S['aux']['mc_B']; aux = []
    for i, arm in enumerate(S['compared_arms']):
        loc = EX[arm]; api = base[arm]; api_other = api['n'] - api['k'] - api['refuse'] - api['format_fail']
        table = [[loc['format_out'], loc['refuse'], loc['catastrophe'], loc['other']], [api['format_fail'], api['refuse'], api['k'], api_other]]
        aux.append({'arm': arm, 'table': table, 'p_mc': fh_mc_p(table, B, np.random.default_rng([S['aux']['seed'], i]))})
    stat = float(-2.0 * sum(np.log(x['p_mc']) for x in aux)); p_comb = float(chi2.sf(stat, 2 * len(aux)))
    R = {'kind': 'identity_screen_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'tag': tag, 'root': a.root, 'run_key': rec['run_key'],
         'seed': rec['seed'], 'seed_registered': seed_ok, 'model': rec['manifest'].get('model'), 'contrasts_sha16': runs_A.sha16_file(a.contrasts or runs_A.CPATH), 'dev_marks': [x for x, on in (('allow_incomplete', bool(short)), ('small_B', a.B is not None), ('allow_dry', a.allow_dry)) if on] + list(rec.get('dry_marks') or []),
         'verdict': verdict, 'mean_abs_diff_pt': float(mean), 'max_abs_diff_pt': float(mx), 'mean_pt': S['mean_pt'], 'max_pt': S['max_pt'],
         'diffs': [dict(x, abs_diff_pt=float(x['abs_diff_pt'])) for x in diffs], 'aux': {'B': B, 'per_arm': aux, 'fisher_stat': stat, 'fisher_df': 2 * len(aux), 'p_combined': p_comb, 'affects_verdict': S['aux']['affects_verdict']},
         'local_counts': EX, 'short_arms': short, 'consequence': S['pass'] if verdict == 'pass' else S['fail'], 'no_constant_change': S['no_constant_change'], 'null_fail_ref': S['null_fail_ref'], 'detection_ref': S['detection_ref'],
         'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(R, open(OUT + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    M = ['# 門0.5 同一性選別（機械生成・`tools/identity_screen_A.py` %s・%s UTC）' % (VERSION, R['generated_utc']), '',
         '- 走行 %s（機種 %s・seed %d・登録の seed と%s）・正本 SHA16 %s・検査用の印 %s' % (rec['run_key'], R['model'], rec['seed'], '一致' if seed_ok else '不一致', R['contrasts_sha16'], '・'.join(R['dev_marks']) or 'なし'),
         '- **判定: %s**（%d 個の絶対差の相加平均 %.3f pt〔閾値 %s 以下〕・最大 %.3f pt〔閾値 %s 以下〕）' % ('合格' if verdict == 'pass' else '不合格', len(diffs), float(mean), S['mean_pt'], float(mx), S['max_pt']),
         '- 帰結（正本の文言）: %s' % R['consequence'], '- %s' % S['no_constant_change'], '- 帰無の不合格率と検出側: %s・%s' % (S['null_fail_ref'], S['detection_ref']), '',
         '| 腕 | 指標 | 手元 | API 既測 | 絶対差（pt） |', '|---|---|---|---|---|']
    M += ['| %s | %s | %d/%d | %d/%d | %.3f |' % (x['arm'], x['indicator'], x['local'][0], x['local'][1], x['api'][0], x['api'][1], x['abs_diff_pt']) for x in R['diffs']]
    M += ['', '## 補助（合否を動かさない・Freeman–Halton の MC・B=%d）' % B, '', '| 腕 | 手元（書式外／refuse／破局／その他） | API | p（MC） |', '|---|---|---|---|']
    M += ['| %s | %s | %s | %.5f |' % (x['arm'], '／'.join(map(str, x['table'][0])), '／'.join(map(str, x['table'][1])), x['p_mc']) for x in aux]
    M += ['', '- Fisher の統合: 統計量 %.3f・自由度 %d・p %.5f（記述）' % (stat, 2 * len(aux), p_comb), '', R['clause']]
    open(OUT + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
    print('[identity_screen_A] %s（平均 %.3f pt・最大 %.3f pt）written %s.{json,md}' % (verdict, float(mean), float(mx), OUT))
