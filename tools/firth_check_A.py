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
