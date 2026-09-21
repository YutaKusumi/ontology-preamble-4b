# -*- coding: utf-8 -*-
"""逸脱 D-B1 の集計器の回帰の確かめ（**合成データだけ**・実データには触れない）。
(1) 合成の場合 all（選定後の段の走行が全部の介入の腕にある）では、凍結した集計器と逸脱の下の集計器の出力が、版・題・時刻と `deviation_D_B1` の欄のほか**一致**すること。
(2) 同じ合成データから二つの土台の腕の選定後の走行を外すと、凍結した集計器は 8 対比を「判定不能（品質床）」にし、逸脱の下の集計器は門の記録の選定の段の行で読んで札を出し、
    **変わるのは、その二腕を含む対比の行と、その族の Holm の欄だけ**であること。
用法: python records/B/deviations/regress_devB1.py   （リポジトリの直下で・results/_synth/devB1* を作って消す）"""
import os, sys, json, shutil, subprocess

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
PY = sys.executable
ENV = dict(os.environ, PYTHONUTF8='1')


def run(args):
    r = subprocess.run([PY] + args, cwd=REPO, capture_output=True, text=True, encoding='utf-8', env=ENV)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def analyze(tool, root, name):
    out = os.path.join(root, name + '.md')
    cmd = [tool, '--gate', os.path.join(root, 'gate-B.json'), '--root', root, '--allow-dry', '--out', out, '--force']
    seal = os.path.join(root, 'seal-B.json')
    if os.path.exists(os.path.join(REPO, seal)):
        cmd += ['--seal', seal, '--allow-partial-seal']
    rc, o = run(cmd)
    assert rc == 0, (tool, rc, o[-600:])
    return json.load(open(os.path.join(REPO, root, name + '.json'), encoding='utf-8'))


def strip(rec):
    r = json.loads(json.dumps(rec))
    for k in ('version', 'generated_utc', 'deviation_D_B1'):
        r.pop(k, None)
    return r


def rows_by_id(rec):
    return {r['id']: r for r in rec['confirm']}


root = os.path.join('results', '_synth', 'devB1')
shutil.rmtree(os.path.join(REPO, root), ignore_errors=True)
rc, o = run(['tools/synth_B.py', '--case', 'all', '--out-root', root]); assert rc == 0, o[-400:]
rc, o = run(['tools/gate_B.py', '--root', root, '--allow-dry', '--out', os.path.join(root, 'gate-B.md'), '--force']); assert rc in (0, 2), o[-400:]
G = json.load(open(os.path.join(REPO, root, 'gate-B.json'), encoding='utf-8'))
assert G['verdict'] == 'open', G['verdict']

# (1) 全部の腕に選定後の走行がある場合: 一致
F1 = analyze('tools/analyze_B.py', root, 'analysis-frozen')
D1 = analyze('tools/analyze_B_devB1.py', root, 'analysis-devB1')
assert strip(F1) == strip(D1), '（1）で食い違った'
assert D1['deviation_D_B1']['arms'] == [], D1['deviation_D_B1']
print('(1) 選定後の走行が全腕にある合成データ: 二つの出力は版・題・時刻のほか一致（逸脱の枝は発火 0 腕）')

# (2) 二つの土台の腕の選定後の走行を外す
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
qtag = T['tags']['quality']
base_arms = ['O-Ncold-v', 'Onull+v']
removed = []
qdir = os.path.join(REPO, root, qtag)
for d in sorted(os.listdir(qdir)):
    if '__post__' in d and any(d.split('__post__')[1].split('__')[0] == a or d.endswith('__post__' + a) or ('__post__' + a + '__') in d for a in base_arms):
        if 'noop' in d:
            continue
        shutil.rmtree(os.path.join(qdir, d)); removed.append(d)
assert len(removed) == 2, removed
F2 = analyze('tools/analyze_B.py', root, 'analysis-frozen-2')
D2 = analyze('tools/analyze_B_devB1.py', root, 'analysis-devB1-2')
fr, dr = rows_by_id(F2), rows_by_id(D2)
touched = sorted(i for i in fr if fr[i].get('A') in base_arms or fr[i].get('B') in base_arms)
assert len(touched) == 8, touched
f1 = rows_by_id(F1)
# 凍結した器: 二腕を含む対比は「判定不能（品質床）」になる——ただし、先に立つ別の札（検閲・保留）がある行はその札のまま
assert all(fr[i]['label'] in ('判定不能（品質床）', f1[i]['label']) for i in touched), [fr[i]['label'] for i in touched]
n_qf = sum(1 for i in touched if fr[i]['label'] == '判定不能（品質床）' and f1[i]['label'] != '判定不能（品質床）')
assert n_qf >= 1, '走行を外しても品質床の札が一つも立たない'
assert all(dr[i].get('deviation') == 'D-B1' for i in touched), [dr[i].get('deviation') for i in touched]
assert sorted(D2['deviation_D_B1']['arms']) == sorted(base_arms)
# 二腕を含まない対比の行は一字も変わらない
other = [i for i in fr if i not in touched]
assert all(fr[i] == dr[i] for i in other), [i for i in other if fr[i] != dr[i]]
# 逸脱の下の 8 行は、走行を外す前（(1) の凍結した器）の札と同じ中身になる（印と注と欄のほか）
for i in touched:
    a, b = dict(rows_by_id(F1)[i]), dict(dr[i])
    lab_a, lab_b = a.pop('label'), b.pop('label')
    b.pop('deviation'); nb = [n for n in b.pop('notes', []) if '逸脱 D-B1' not in n]; na = a.pop('notes', [])
    assert a == b and na == nb, (i, {k: (a.get(k), b.get(k)) for k in a if a.get(k) != b.get(k)})
    assert lab_b == lab_a or (lab_a.startswith('確証') and lab_b.startswith('確証') and '逸脱 D-B1 の下' in lab_b), (lab_a, lab_b)
# 確証の族の外で変わってよいのは、選定後の品質床の区画と数え上げだけ
f2, d2 = strip(F2), strip(D2)
diff_keys = sorted(k for k in f2 if f2[k] != d2[k])
print('(2) 二腕の選定後の走行を外した合成データ: 凍結した器は二腕を含む %d 対比のうち %d 対比を新たに判定不能（品質床）に・逸脱の下の器は門の記録で読んで、走行を外す前と同じ札を出した' % (len(touched), n_qf))
print('    二腕を含まない %d 対比の行は一致・逸脱の下の 8 行は「走行を外す前の凍結した器の行」と印のほか一致' % len(other))
print('    記録の欄で食い違ったもの:', diff_keys)
allowed = {'confirm', 'counts', 'quality_post', 'sign_agreement', 'td_specificity', 's4'}
assert set(diff_keys) <= allowed, set(diff_keys) - allowed
shutil.rmtree(os.path.join(REPO, root), ignore_errors=True)
print('回帰の確かめ: 通った')
