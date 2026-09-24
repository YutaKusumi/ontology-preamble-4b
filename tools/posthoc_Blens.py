# -*- coding: utf-8 -*-
"""posthoc_Blens.py v1 —— B-lens の事後の計算（逸脱 D-BL4・登録者裁定 D192・2026-09-24）。札を新しく作らず、付いた札と読みの比を変えない。

凍結した層二の器 `tools/blens_calib.py` が計算していなかった、正本の記述の二つを出す:
  1. 主位置の生の全語彙の softmax の確率（正本 `magnitude.quantity`「生の全語彙の softmax の確率は記述」）: 大きさの目盛りの行ごとに、
     直接の経路だけを土台に足す前と後の「```」（転記行 B の主）の確率を、温度も切り詰めも掛けずに出す。
     凍結した芯の関数 `blens_core.direct_path` と、層二と同じ入力（Colab の相 extract の残差・升目ごとの一件目・選んだ層の方向・B の係数と腕の符号）を使い、
     同じ出口の値に B の標本化の変換を当てた確率が、層二の記録の値と一致することを先に確かめる（一致しなければ止める）。
  2. 異なる文の頭の数（正本 `magnitude.aggregate`「異なる文の頭の数を印字する」）: 層ごとに、選んだ出力の、答えの文字より前の出力のトークンの並びの種類の数
     （転記行 E の「文字の前の並びの種類」と同じ数え方）。段階 B の生の出力を手元のトークナイザで割り直し、答えの文字を覆うトークンの位置が
     Colab の相 extract の記録（`cover`）と一致することを先に確かめる（一致しなければ止める）。
封印の前には走らない（凍結の記録と封印の記録）。
出力: results/Blens/posthoc-Blens.json（--force が無ければ上書きしない）。
用法: python tools/posthoc_Blens.py --colab-dir <相 extract の出力の置き場> [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, argparse, datetime, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C
import blens_lens as BL

VERSION = 'v1'
NL = chr(10)
OUT = os.path.join(REPO, 'results', 'Blens', 'posthoc-Blens.json')
CAL = os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json')
CH = re.compile(r'"choice"\s*:\s*"(a|b|c|d|refuse)"')
base_arm = lambda arm: re.split(r'[+\-]v', arm)[0]


def softmax(z):
    z = np.asarray(z, dtype=np.float64)
    e = np.exp(z - z.max())
    return e / e.sum()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--colab-dir', required=True)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    BL.require_sealed(TL)
    if os.path.exists(OUT) and not a.force:
        raise SystemExit('既にある: %s' % OUT)
    FJ = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
    CK = json.load(open(os.path.join(a.colab_dir, 'check.json'), encoding='utf-8'))
    if CK['selected_sha16'] != FJ['facts']['E']['selected_sha16'] or CK.get('dry'):
        raise SystemExit('Colab の出力の選んだ試行が設計の事実と違うか、DRY の出力（止める）')
    CALJ = json.load(open(CAL, encoding='utf-8'))
    Z = np.load(os.path.join(a.colab_dir, 'h.npz'))
    SAMP, coef, eps = TL['inputs']['sampling_B'], TL['layers']['coef_applied'], float(CK['rms_norm_eps'])
    SJ = json.load(open(BL.SETS, encoding='utf-8'))
    fmain = int(SJ['sets']['F']['main'])
    sel = BL.rkey(TL['primary']['ratio'])
    import steer_B
    D = np.load(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'))
    dirs = collections.OrderedDict((u, D['%s__%s' % (u, sel)].astype(np.float64)) for u in ('static', 'loaded', 'Nk', 'td'))
    for i, v in enumerate(steer_B.random_directions(D['static__%s' % sel], 'main', float(sel))):
        dirs['rand:%d' % i] = np.asarray(v, dtype=np.float64)
    W = BL.Weights(BL.SNAP, TL['inputs']['model']['vocab_size'])
    units = list(dirs)
    ZU = W.delta_full(np.array([dirs[u] for u in units], dtype=np.float32)).astype(np.float64)
    first = collections.OrderedDict()
    for k, c in enumerate(CK['contexts']):
        first.setdefault((c['scenario'], c['arm']), k)
    ZH = W.delta_full(np.asarray(Z['h_main'], dtype=np.float32)[list(first.values())]).astype(np.float64)
    zh = {key: ZH[:, j] for j, key in enumerate(first)}
    hm = {key: np.asarray(Z['h_main'][k], dtype=np.float64) for key, k in first.items()}
    # 1. 主位置の生の softmax（層二の行ごと・変換の後の確率が層二の記録と一致することを先に確かめる）
    rows, mism = [], []
    for x in CALJ['magnitude']['main_rows']:
        if 'pT_before' not in x:
            continue
        sc, arm, unit = x['row'].split('|')
        key = (sc, base_arm(arm))
        dp = C.direct_path(zh[key], ZU[:, units.index(unit)], hm[key], dirs[unit], x['sign'] * coef, eps)
        tb = C.transform(dp['before'], SAMP['temperature'], SAMP['top_k'], SAMP['top_p'])[fmain]
        ta = C.transform(dp['after'], SAMP['temperature'], SAMP['top_k'], SAMP['top_p'])[fmain]
        if abs(tb - x['pT_before']) > 1e-9 or abs(ta - x['pT_after']) > 1e-9:
            mism.append((x['row'], tb, x['pT_before'], ta, x['pT_after']))
        rb, ra = softmax(dp['before'])[fmain], softmax(dp['after'])[fmain]
        rows.append({'row': x['row'], 'eligible': x['eligible'], 'raw_before': float(rb), 'raw_after': float(ra), 'raw_diff': float(ra - rb),
                     'pT_before': x['pT_before'], 'pT_after': x['pT_after'], 'obs_diff': x['obs_diff']})
    if mism:
        raise SystemExit('変換の後の確率が層二の記録と一致しない（止める・登録者に相談）: %s' % mism[:3])
    # 2. 異なる文の頭の数（層ごと・Colab の cover と一致することを先に確かめる）
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(BL.SNAP)
    by_tid = {c['trial_id']: c for c in CK['contexts']}
    heads, cmis = {}, []
    for stratum, ids_ in FJ['facts']['E']['selected'].items():
        sc, arm, style = stratum.split('|')
        d = os.path.join(REPO, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
        raw = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
        prefs = []
        for tid in ids_:
            enc = tok(raw[tid]['final'], add_special_tokens=False, return_offsets_mapping=True)
            pos = list(CH.finditer(raw[tid]['final']))[-1].start(1)
            c0 = [q for q, (s0, s1) in enumerate(enc['offset_mapping']) if s0 <= pos < s1][0]
            if by_tid[tid]['cover'] != c0:
                cmis.append((tid, c0, by_tid[tid]['cover']))
            prefs.append(tuple(enc['input_ids'][:c0]))
        heads[stratum] = {'n_outputs': len(ids_), 'distinct_heads': len(set(prefs)), 'prefix_len_min': min(len(p) for p in prefs), 'prefix_len_max': max(len(p) for p in prefs)}
    if cmis:
        raise SystemExit('答えの文字を覆うトークンの位置が Colab の記録と一致しない（止める・登録者に相談）: %s' % cmis[:3])
    res = {'kind': 'blens_posthoc', 'version': VERSION, 'deviation': 'D-BL4', 'ruling': 'D192', 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
           'raw_softmax_main': rows, 'distinct_heads': heads,
           'checks': {'pT_reproduced_rows': len(rows), 'cover_reproduced': sum(len(v) for v in FJ['facts']['E']['selected'].values())},
           'inputs': {'calib_sha16': BL.sha16f(CAL), 'colab_check_sha16': BL.sha16f(os.path.join(a.colab_dir, 'check.json')), 'h_npz_sha16': BL.sha16f(os.path.join(a.colab_dir, 'h.npz'))},
           'note': '事後の区画の記述。札を新しく作らず、付いた札と読みの比を変えない（逸脱 D-BL4・裁定 D192）',
           'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print('wrote', os.path.relpath(OUT, REPO), '| rows', len(rows), '| strata', len(heads))


if __name__ == '__main__':
    main()
