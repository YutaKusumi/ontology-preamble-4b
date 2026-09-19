# -*- coding: utf-8 -*-
"""layers_B.py v1 —— 段階 B の**副位置の読み**（層ごとの分離・層別射影差・記述・裁定 D132・2026-09-19）。

正本 `descriptive_families.B_desc_layer.definition_D132` に従う（**データを見る前に登録した読み方**）:
  反証の場面（`B_desc_layer.scenario`）の無操作の二腕（`B_desc_layer.arms`＝O-Ncold と Osec-Ncold）の試行について、候補の各層で、
  副位置の活性（`activation_storage.response_mean`・走行器が npz に置く）を、**同じ層の (6b) の方向**（`B_desc_layer.direction`＝loaded・
  主位置から作った方向・単位ベクトルにする）に射影する。層ごとに、二腕の射影の**平均の差**・**標準化した差**（二腕を合わせた標準偏差で割る）・
  **AUC**（Osec-Ncold の試行より O-Ncold の試行の射影が大きい確率・同点は半分）を記述として出す。**目安は置かない・p を印字しない。**
  方向は抽出場面の主位置から作り、射影する活性は反証の場面の応答から取るので、同じ標本で方向を作って分離を測る循環は無い。
(6a)（静的）の分離は副位置で測れない（登録された走行に無操作の O と Osec が同じ場面で揃わない・`B_desc_direction.static_separation_D132`）。
入力: 本走行（tag `stageB`）の記録と、各走行の置き場の `resp-<run_key>.npz`（鍵は trial_id・値は［候補の層の数, 隠れ次元］の fp16）・
      方向の npz（`tools/direction_B.py` の `directions.npz`・鍵は `<名>__<層の割合>`）。
出力: records/B/layers-B-<日付>.{md,json}（既存は --force なしでは上書きしない）。報告の組み立て器が必須として読む。
用法: python tools/layers_B.py --directions results/dirB/directions.npz [--root <results>] [--allow-dry] [--force]
      python tools/layers_B.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO


def auc(a, b):
    """P(a > b) + 0.5 P(a = b)（Mann–Whitney の U を nA・nB で割った値・順位で数える）。"""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if not len(a) or not len(b):
        return None
    allv = np.concatenate([a, b])
    order = allv.argsort(kind='mergesort')
    ranks = np.empty(len(allv))
    sv = allv[order]
    i = 0
    while i < len(sv):                       # 同点は平均順位
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    ra = ranks[:len(a)].sum()
    u = ra - len(a) * (len(a) + 1) / 2.0
    return float(u / (len(a) * len(b)))


def separation(pa, pb):
    """平均の差・標準化した差（二腕を合わせた標準偏差）・AUC。記述のみ。"""
    pa, pb = np.asarray(pa, dtype=float), np.asarray(pb, dtype=float)
    na, nb = len(pa), len(pb)
    if na < 2 or nb < 2:
        return {'n_A': na, 'n_B': nb, 'mean_diff': None, 'smd': None, 'auc': None}
    d = float(pa.mean() - pb.mean())
    sp = float(np.sqrt(((na - 1) * pa.var(ddof=1) + (nb - 1) * pb.var(ddof=1)) / (na + nb - 2)))
    return {'n_A': na, 'n_B': nb, 'mean_A': float(pa.mean()), 'mean_B': float(pb.mean()), 'mean_diff': d,
            'smd': (d / sp) if sp > 0 else None, 'auc': auc(pa, pb)}


def load_resp(rec, trial_rows):
    """走行の置き場の resp npz から、試行ごとの副位置の活性を読む（無い試行は数えて返す）。"""
    arrs, missing = {}, 0
    npz = {}
    for r in trial_rows:
        p = r.get('resp_mean_path')
        if not p:
            missing += 1
            continue
        fn, key = p.split('#', 1)
        if fn not in npz:
            fp = os.path.join(rec['dir'], fn)
            npz[fn] = np.load(fp) if os.path.exists(fp) else None
        z = npz[fn]
        if z is None or key not in z.files:
            missing += 1
            continue
        arrs[r['trial_id']] = np.asarray(z[key], dtype=np.float32)
    return arrs, missing


def analyse(T, dirs, root=None, allow_dry=False):
    L = T['descriptive_families']['B_desc_layer']
    sc, (armA, armB), dname = L['scenario'], L['arms'], L['direction']
    ratios = list(T['selection']['candidates']['layers'])
    idx = runs_B.index_runs(T, T['tags']['main'], root, allow_dry=allow_dry)
    proj = {armA: {r: [] for r in ratios}, armB: {r: [] for r in ratios}}
    counts = {armA: {'ok': 0, 'no_resp': 0}, armB: {'ok': 0, 'no_resp': 0}}
    for key, recs in idx.items():
        for rec in recs:
            if (rec['manifest'].get('scenario')) != sc:
                continue
            rows = [r for r in runs_B.iter_jsonl(rec['trials_path'], ('trial_id', 'arm', 'status', 'resp_mean_path'))
                    if r['arm'] in (armA, armB) and r['status'] == 'ok']
            arrs, _ = load_resp(rec, rows)
            for r in rows:
                a = arrs.get(r['trial_id'])
                if a is None:
                    counts[r['arm']]['no_resp'] += 1
                    continue
                if a.shape[0] != len(ratios):
                    raise SystemExit('副位置の活性の層の数（%d）が候補の層の数（%d）と違う: %s' % (a.shape[0], len(ratios), r['trial_id']))
                counts[r['arm']]['ok'] += 1
                for li, ratio in enumerate(ratios):
                    u = dirs[(dname, float(ratio))]
                    u = u / float(np.linalg.norm(u))
                    proj[r['arm']][ratio].append(float(np.dot(a[li], u)))
    rows_out = []
    for ratio in ratios:
        s = separation(proj[armA][ratio], proj[armB][ratio])
        rows_out.append(dict(layer=ratio, **s))
    return {'scenario': sc, 'arm_A': armA, 'arm_B': armB, 'direction': dname, 'rows': rows_out, 'counts': counts}


def _selftest():
    rng = np.random.default_rng(11)
    # AUC: 既知の値（完全分離・完全一致・同点）
    assert auc([3, 4, 5], [0, 1, 2]) == 1.0 and auc([0, 1, 2], [3, 4, 5]) == 0.0
    assert abs(auc([1, 1], [1, 1]) - 0.5) < 1e-12
    # 正規の二群: AUC は Φ(d/√2) の近く（d は標準化した差）
    a, b = rng.normal(1.0, 1.0, 4000), rng.normal(0.0, 1.0, 4000)
    from scipy.stats import norm, mannwhitneyu
    s = separation(a, b)
    assert abs(s['auc'] - norm.cdf(1.0 / np.sqrt(2))) < 0.02, s
    assert abs(s['smd'] - 1.0) < 0.06, s
    # **別の実装**（scipy の Mann–Whitney）と照らす
    u = mannwhitneyu(a[:300], b[:300], alternative='two-sided').statistic
    assert abs(auc(a[:300], b[:300]) - u / (300 * 300)) < 1e-12, 'AUC が scipy の U と違う'
    print('[layers_B selftest] AUC（既知の値・同点・scipy の U と一致）・標準化した差: すべて通った')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--directions', default=None, help='tools/direction_B.py の directions.npz')
    ap.add_argument('--root', default=None)
    ap.add_argument('--contrasts', default=None)
    ap.add_argument('--out', default=None)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--allow-dry', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    if not a.directions:
        sys.exit('--directions（tools/direction_B.py の directions.npz）が要る')
    T = runs_B.load_T(a.contrasts)
    z = np.load(a.directions)
    dirs = {(k.split('__')[0], float(k.split('__')[1])): z[k] for k in z.files}
    R = analyse(T, dirs, a.root, a.allow_dry)
    now = datetime.datetime.now(datetime.timezone.utc)
    jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
    out_md = a.out or os.path.join(REPO, 'records', 'B', 'layers-B-%s.md' % jst.strftime('%Y-%m-%d'))
    out_json = os.path.splitext(out_md)[0] + '.json'
    if not a.force:
        for p in (out_md, out_json):
            if os.path.exists(p):
                sys.exit('既にある（--force で上書き）: %s' % p)
    REC = dict({'kind': 'layers_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'directions_sha16': runs_B.sha16_file(a.directions),
                'definition': T['descriptive_families']['B_desc_layer']['definition_D132']}, **R)
    json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    L = ['# 段階 B 副位置の読み（層ごとの分離・記述・機械生成・`tools/layers_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
         '- 正本 SHA16 %s・方向の npz SHA16 %s。場面 %s・%s 対 %s・方向 %s（主位置から作った・単位ベクトル）。'
         % (REC['contrasts_sha16'], REC['directions_sha16'], R['scenario'], R['arm_A'], R['arm_B'], R['direction']),
         '- **記述であり、目安も p も置かない**（裁定 D132）。(6a) の分離は副位置で測れない（`B_desc_direction.static_separation_D132`）。',
         '- 副位置の活性を読めた試行: %s（%s）・%s（%s）。読めなかった試行（応答が空など）: %s・%s。'
         % (R['arm_A'], R['counts'][R['arm_A']]['ok'], R['arm_B'], R['counts'][R['arm_B']]['ok'],
            R['counts'][R['arm_A']]['no_resp'], R['counts'][R['arm_B']]['no_resp']), '',
         '| 層（全層に対する深さの割合） | n A／B | 射影の平均 A | 射影の平均 B | 平均の差 | 標準化した差 | AUC |', '|---|---|---|---|---|---|---|']
    f = lambda x: '—' if x is None else ('%.4g' % x)
    for r in R['rows']:
        L.append('| %s | %s／%s | %s | %s | %s | %s | %s |' % (r['layer'], r['n_A'], r['n_B'], f(r.get('mean_A')), f(r.get('mean_B')),
                                                          f(r['mean_diff']), f(r['smd']), f(r['auc'])))
    L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
    print('[layers_B] %s / %s' % (out_md, out_json))
