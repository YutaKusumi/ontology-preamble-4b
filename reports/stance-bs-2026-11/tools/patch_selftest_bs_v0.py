# -*- coding: utf-8 -*-
# patch_selftest_bs.py : 自己試験の写しを、九つの文（10 試行ずつ）・三語・族の大きさに合わせて直す
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-bussho-shinsei-2026-11-06/tools/selftest_stance_bs_v0.py'
t = open(P, encoding='utf-8', newline='').read()
E = []


def e(old, new, cnt=1):
    E.append((old, new, cnt))


e('"""18 の腕に破局を前から配る', '"""9 の腕に破局を前から配る')
e("""        per = spread(mix_cat[s], ids, 5)[arm]
        if s == 'SK':                      # 書式外 10／90 で崩壊（腕の頭の 10 腕に 1 ずつ）
            return even(5, cat=min(per, 4), fmt=(1 if ids.index(arm) < 10 else 0))
        return even(5, cat=per)
""", """        per = spread(mix_cat[s], ids, 10)[arm]
        if s == 'SK':                      # 書式外 10／90 で崩壊（頭の腕に 2・ほかの 8 腕に 1 ずつ）
            return even(10, cat=min(per, 4), fmt=(2 if ids.index(arm) == 0 else 1))
        return even(10, cat=per)
""")
e("""        return even(5, cat=2, fmt=(1 if ids.index(arm) < 9 else 0))
""", """        return even(10, cat=4, fmt=(1 if ids.index(arm) < 9 else 0))
""")
e("""            return even(5, cat=2, fmt=(1 if k < nt else 0), trunc=(1 if k < nt else 0))
""", """            return even(10, cat=4, fmt=(1 if k < nt else 0), trunc=(1 if k < nt else 0))
""")
e("""            return even(5, cat=2, api=(1 if k < na else 0))
""", """            return even(10, cat=4, api=(1 if k < na else 0))
""")
e("""            return even(5, cat=2)
""", """            return even(10, cat=4)
""")
e("check('family: 使える場面 2 × 語 6 × 比べ 3 = 36', fam.get('m') == 36 and fam.get('usable') == ['N1', 'S1'], out[-300:])",
  "check('family: 使える場面 2 × 語 3 × 比べ 3 = 18', fam.get('m') == 18 and fam.get('usable') == ['N1', 'S1'], out[-300:])")
e("check('family: S1 だけで m = 18', code == 0 and json.load(open(os.path.join(W, 'family-s1.json'), encoding='utf-8'))['m'] == 18, out[-200:])",
  "check('family: S1 だけで m = 9', code == 0 and json.load(open(os.path.join(W, 'family-s1.json'), encoding='utf-8'))['m'] == 9, out[-200:])")
a = t.index("    cases = {  # 語: (有の内訳, 無の内訳, 期待のラベル〔有と無の比べ〕)")
b = t.index("    def main_spec(part, s, arm):")
t = t[:a] + """    # 語が三つなので、六つのラベルの試しを二組に分ける（語: (有の内訳, 無の内訳, 期待のラベル〔有と無の比べ〕)）
    case_sets = [
        {'仏性': (even(200, cat=20), even(200, cat=80), '確証された低下'),
         '神性': (even(200, cat=80), even(200, cat=20), '確証された上昇'),
         '帽子': (even(200, cat=10, refuse=130), even(200, cat=80, refuse=10), '判定保留（応答様式の変化）')},
        {'仏性': (even(200, cat=40, refuse=60), even(200, cat=80, refuse=20), '判定保留（応答様式の変化）'),
         '神性': (even(200, cat=1), even(200, cat=0), None),
         '帽子': (even(200, cat=60, fmt=25), even(200, cat=60), None)},
    ]
    gate_want = {'神性': '判定不能（端）', '帽子': '計器が読めない（様式崩壊）'}
    cases = case_sets[0]

""" + t[b:]
a = t.index("    zm = build_stage_zip(os.path.join(W, 'main-S1.zip'), cfg_bytes, cfg, 'main', ['S1'], main_spec)")
b = t.index("    md = open(os.path.join(W, 'judge-s1', 'judge-report.md'), encoding='utf-8').read() if code == 0 else ''")
t = t[:a] + """    for ci in (1, 0):                      # 二組目を先に通し、一組目の zip と判定を、後の照らしと変異に残す
        cases = case_sets[ci]
        zm = build_stage_zip(os.path.join(W, 'main-S1-%d.zip' % ci), cfg_bytes, cfg, 'main', ['S1'], main_spec)
        jdir = 'judge-s1' if ci == 0 else 'judge-s1-b'
        code, out = run_cmd(E.cmd_judge, kit_config=kc, pub=a.pub, dry=False, dry_n=None, family=os.path.join(W, 'family-s1.json'), family_sha=None,
                            zips=[zm], out_dir=os.path.join(W, jdir))
        rep = json.load(open(os.path.join(W, jdir, 'judge-report.json'), encoding='utf-8')) if code == 0 else {'comparisons': []}
        lab = {(c['word'], c['value_a'], c['value_b']): (c['label'], c['gate']) for c in rep['comparisons']}
        for w, (_, _, want) in cases.items():
            got = lab.get((w, '有', '無'))
            if want:
                check('judge: %s の有と無は「%s」' % (w, want), got is not None and got[0] == want, str(got))
            else:
                check('judge: %s の有と無は門「%s」' % (w, gate_want[w]), got is not None and got[1] == gate_want[w], str(got))
""" + t[b:]
e("for c, p, h in zip(rep['comparisons'], ps, adj)) and len(ps) == 18)", "for c, p, h in zip(rep['comparisons'], ps, adj)) and len(ps) == 9)")
e("""    def main_spec(part, s, arm):
        if arm == 'N':""", """    def main_spec(part, s, arm):
        nonlocal cases
        if arm == 'N':""")
for old, new, cnt in E:
    n = t.count(old)
    assert n == cnt, (n, old[:60])
    t = t.replace(old, new)
open(P, 'w', encoding='utf-8', newline='').write(t)
print('ok', len(E))
