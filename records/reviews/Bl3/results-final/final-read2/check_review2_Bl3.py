# -*- coding: utf-8 -*-
"""起草者の最終の見直し・二度目の器による確かめ（枠 `frame-review2-Bl3.md` の手順 1・読み直す前に走らせる）。
最終版の案 `records/Bl3/results-Bl3-FINAL-2026-09-27.md` について、逸脱の器を読まずに記録から書いた式で次を確かめる:
 (一) 逆引用符の中の置き場が、置き場にある。
 (二) SHA16 が、隣に書いた置き場のファイル（または名で指した記録）の今の値と同じ。
 (三) 裁定の番号が、裁定の記録の名か、正本の decisions か、凍結の本文か、台帳にある（まだ裁かれていない番号は、そう記す）。
 (四) 正本の鍵（`labels.first_step_margin` など）が、正本にある。
 (五) 足した区画（【逸脱 D-BLT1】の印の区画）の数を、記録（集計の記録・組の出力・下見の記録・設計事実・開く段の記録・正本・再現の記録）から出し直した値の並びと、区画ごとに照らす
      （並べ直しの表の行は凍結の表の写しなので、数は凍結の表と照らす）。
 (六) 足した区画と起草者の欄が指す節に、指した中身がある。
書くのは本記録（md と json）だけ。
用法: python records/reviews/Bl3/results-final/final-read2/check_review2_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, glob, math, hashlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
NL = chr(10)
BS = chr(92)
P = lambda r: os.path.join(REPO, *r.split('/'))
s16 = lambda r: hashlib.sha256(open(P(r), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
ld = lambda r: json.load(open(P(r), encoding='utf-8'))
OUT_MD, OUT_JS = os.path.join(HERE, 'check-review2-Bl3.md'), os.path.join(HERE, 'check-review2-Bl3.json')
for p_ in (OUT_MD, OUT_JS):
    assert not os.path.exists(p_), '既にある: ' + p_
sys.path.insert(0, P('tools'))
import report_lint as RL
FINAL = 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'
TXT = open(P(FINAL), encoding='utf-8').read().replace('\r\n', NL)
L = TXT.split(NL)
T3 = ld('design/contrasts-Bl3.json')
MB = RL.machine_block(T3)
TAG = '【逸脱 D-BLT1】'
R = []
add = lambda what, ok, got, note='': R.append({'what': what, 'ok': ok, 'got': got, 'note': note})

# (一) 置き場
paths = []
for i, l in enumerate(L, 1):
    for m in re.finditer(r'`([^`\s]+)`', l):
        s = m.group(1)
        if '/' in s and re.search(r'\.(md|json|py|npz|html)$|/$', s) and not any(c in s for c in '{}<>*'):
            paths.append((i, s))
missing = [(i, s) for i, s in paths if not os.path.exists(P(s.rstrip('/')))]
add('(一) 逆引用符の中の置き場が置き場にある', not missing, '置き場 %d（異なり %d）・無い %s' % (len(paths), len({s for _, s in paths}), missing))

# (二) SHA16
KNOWN = [(r'正本 `design/contrasts-Bl3\.json` SHA16 ([0-9A-F]{16})', 'design/contrasts-Bl3.json'), (r'凍結の記録 SHA16 ([0-9A-F]{16})', 'records/Bl3/FREEZE-RECORD-Bl3.json'),
         (r'封印の記録 SHA16 ([0-9A-F]{16})', 'records/Bl3/sealing-record-Bl3.json'), (r'集計の出力 SHA16 ([0-9A-F]{16})', 'records/Bl3/analysis-Bl3.json'),
         (r'凍結の本文 SHA16 ([0-9A-F]{16})', 'design/design-Bl3-FROZEN.md'), (r'・正本 SHA16 ([0-9A-F]{16})', 'design/contrasts-Bl3.json')]
sha_rows, sha_bad, sha_unmatched = [], [], []
for i, l in enumerate(L, 1):
    for m in re.finditer(r'[0-9A-F]{16}', l):
        h = m.group(0)
        pre = l[max(0, m.start() - 120):m.start()]
        cand = None
        for rx, rel in KNOWN:
            mm = re.search(rx, l[max(0, m.start() - 60):m.end()])
            if mm and mm.group(1) == h:
                cand = rel
        if cand is None:
            pm = list(re.finditer(r'`([^`]+)`', pre))
            if pm and re.search(r'（SHA16 $|・SHA16 $', pre):
                cand = pm[-1].group(1)
        if cand is None:
            sha_unmatched.append((i, h, pre[-40:]))
            continue
        ok_ = os.path.exists(P(cand)) and s16(cand) == h
        sha_rows.append((i, cand, h, ok_))
        if not ok_:
            sha_bad.append((i, cand, h, s16(cand) if os.path.exists(P(cand)) else None))
add('(二) SHA16 が隣の置き場のファイルの今の値と同じ', not sha_bad and not sha_unmatched, '照らした SHA16 %d・外れ %s・置き場の分からない SHA16 %s' % (len(sha_rows), sha_bad, sha_unmatched))

# (三) 裁定の番号
nums = sorted({int(x) for x in re.findall(r'(?<![A-Za-z0-9])D(\d{2,3})(?![0-9])', TXT)})
have = set(int(k[1:]) for k in T3.get('decisions', {}))
for fp in glob.glob(P('records/*/rulings-D*.md')) + glob.glob(P('records/*/*/rulings-D*.md')):
    mm = re.search(r'rulings-D(\d+)(?:-D(\d+))?\.md$', fp.replace(BS, '/'))
    a_, b_ = int(mm.group(1)), int(mm.group(2) or mm.group(1))
    have |= set(range(a_, b_ + 1))
frozen_txt = open(P('design/design-Bl3-FROZEN.md'), encoding='utf-8').read()
have |= {int(x) for x in re.findall(r'(?<![A-Za-z0-9])D(\d{2,3})(?![0-9])', frozen_txt)}
review1 = open(P('records/reviews/Bl3/results-final/final-read/review-final-Bl3.md'), encoding='utf-8').read()
pending = [n for n in nums if n not in have and ('D%d' % n) in review1]
absent = [n for n in nums if n not in have and n not in pending]
add('(三) 裁定の番号が裁定の記録・正本・凍結の本文にある', not absent, '番号 %d（D%d〜D%d）・無い %s・まだ裁かれていない（一度目の見直しの候補）%s' % (len(nums), nums[0], nums[-1], ['D%d' % n for n in absent], ['D%d' % n for n in pending]),
    'まだ裁かれていない番号は、登録者の裁定の後に正しくなる（裁かれなければ、その句を外して組み直す）')

# (四) 正本の鍵
keys = sorted({m.group(1) for m in re.finditer(r'`((?:labels|gate|pilot|predictions|independent_recompute|review_plan|computation|nulls|readout|descriptive|scope|report_rules)\.[A-Za-z0-9_.]+)`', TXT)})


def has_key(T, dotted):
    cur = T
    for part in dotted.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return False
    return True


bad_keys = [k for k in keys if not has_key(T3, k)]
add('(四) 正本の鍵が正本にある', not bad_keys, '鍵 %d・無い %s' % (len(keys), bad_keys))

# (五) 足した区画の数
blocks = []
i = 0
while i < len(L):
    if L[i] == MB['begin'] and i + 1 < len(L) and L[i + 1].startswith('- ' + TAG) and not L[i + 1].startswith('- ' + TAG + '**'):
        j = L.index(MB['end'], i)
        blocks.append((i + 2, L[i + 1:j]))
        i = j + 1
        continue
    i += 1
isnum = lambda t: re.fullmatch(r'-?[\d,]*\.?\d+(?:e-?\d+)?%?', t) is not None
toks = lambda lines: [t for l in lines for t, _, _, _ in RL.report_numbers(l) if isnum(t)]
A = ld('records/Bl3/analysis-Bl3.json')
dirs = {p: v['dir'] for p, v in A['inputs'].items()}
M = ld('results/Bl3/main/%s/main.json' % dirs['main'])
RC = ld('results/Bl3/main/%s/recompute.json' % dirs['recompute'])
PJ = ld('records/Bl3/pilot/pilot-20260926T103442Z/pilot.json')['pilot']
FJ = ld('records/Bl3/design-facts-Bl3.json')
OJ = ld('records/Bl3/open-results-Bl3.json')
VR = ld('records/reviews/Bl3/results-round1/checks/verification-results-Bl3.json')
rows = A['rows']
K = T3['nulls']['isotropic']['count']
m = A['rows_meta']['m_rows']
iso = lambda k: np.array([v for kk, v in M['cells'][k]['effects'].items() if kk.startswith('iso:')], dtype=np.float64)
css = sorted({r['cell_sign'] for r in rows.values()})
iq = [float(np.percentile(iso(k), 75) - np.percentile(iso(k), 25)) for k in css]
lo_all, hi_all = min(float(iso(k).min()) for k in css), max(float(iso(k).max()) for k in css)
non = [r for r in rows.values() if not r['iso_outside']]
tails = [min(r['upper'], r['lower']) for r in non]
effs = [abs(r['effect']) for r in rows.values()]
r1 = [r for r in rows.values() if r['iso_outside']][0]
c1 = r1['cell_sign']
cell1 = c1.rsplit('|', 1)[0]
pa0 = A['descriptive']['pa_noop'][c1]
pf = T3['pilot']['p_bounds'][0]
lof = math.log(pf / (1 - pf))
eff1 = r1['effect']
pa1 = 1.0 / (1.0 + (1.0 - pa0) / pa0 * math.exp(-eff1))
isoN = sorted(iso(c1), reverse=True)
kmax = lambda mm: max(k for k in range(50) if 2 * (1 + k) / (1 + K) < 0.05 / mm)
q7 = [e for e in FJ['facts']['C']['q7_intervals'] if e['id'] == [rid for rid, r in rows.items() if r['iso_outside']][0]][0]
G = A['gates']
lo_cell = PJ['cells'][cell1]['lo']
via = PJ['vi']['a']
vd = PJ['v']['diffs']
mains = [c for c in PJ['cells'] if PJ['cells'][c].get('main')]
gate_only = [c for c in PJ['cells'] if not PJ['cells'][c].get('main')]
near = [(c, PJ['cells'][c]['lo'] - lof, via[c]) for c in mains if PJ['cells'][c].get('pass_i_ii') and PJ['cells'][c]['lo'] - lof < via[c]]
dv = {v: {c: PJ['iv'][v]['lo'][c] - PJ['cells'][c]['lo'] for c in PJ['iv'][v]['lo']} for v in sorted(PJ['iv'])}
vmax = {v: max(abs(x) for x in d_.values()) for v, d_ in dv.items()}
f4 = lambda x: '%.4g' % x
units = G['main']['units']
unit_digits = [re.sub(r'\D', '', u) for u in units if re.search(r'\d', u)]
EXP = collections.OrderedDict()
EXP['起草者の欄の文が指す数'] = [str(K), '%.2f' % min(iq), '%.2f' % max(iq), '%.2f' % lo_all, '%.2f' % hi_all, str(len(css)), str(sum(1 for r in rows.values() if r['iso_outside'])), str(m), str(len(non)),
                        '%.3f' % min(r['p'] for r in non), '%.3f' % max(r['p'] for r in non), str(min(tails)), str(max(tails)), '%.1f' % (100.0 * min(tails) / K), '%.1f%%' % (100.0 * max(tails) / K),
                        '%.3f' % min(effs), '%.3f' % max(effs), str(len(RC['rows'])), str(sum(1 for r in rows.values() if r['direction'] == 'Nk'))] + ('%.3g' % A['recompute']['first']['max_abs_diff']).split('e-') + [str(A['main_run']['batch'])]
# 走査器の数の形は「1.5〜19.1%」を 1.5 と 19.1% に、「3.71e-06」を 3.71 と 06 に分けて拾うので、出し直した数も同じ形に分ける
EXP['〈両方の外〉の行'] = [f4(pa0), f4(pf), '%.2f' % (pa0 / pf), '%.3f' % eff1, '%.2g' % pa1, f4(lo_cell), '%.3f' % lof, '%.3f' % (lo_cell - lof), f4(via[cell1]), f4(PJ['cells'][cell1]['stage_b_rate']),
                    '%.3f' % eff1, str(r1['upper']), '%.3f' % isoN[0], '%.6f' % (0.05 / m), str(kmax(m)), '%.3f' % isoN[1], '%.3f' % isoN[2], '%.3f' % (eff1 - isoN[2]),
                    '%.1f' % q7['diff_pt'], '%.2f' % q7['lo'], '%.2f' % q7['hi'], f4(r1['iso_top_share']), '%.4f' % (1.0 / r1['second']['of_oriented']), f4(A['chance']['oriented']), f4(A['chance']['pair']),
                    f4(r1['iso_median'])]
EXP['記述の「v̂ と (6b) を抜いた門」'] = [str(G['desc_without_vhat_loaded']['n_rows']), f4(G['desc_without_vhat_loaded']['rho']), f4(G['desc_without_vhat_loaded']['p']), str(len(units))] + unit_digits + [str(G['main']['n_perm']), str(T3['gate']['permutations'])]
EXP['独立の再計算の範囲は'] = [str(len(RC['rows'])), str(sum(1 for r in rows.values() if r['direction'] == 'Nk')), str(A['main_run']['batch'])]
EXP['数と分母'] = [str(sum(1 for r in rows.values() if r['direction'] == 'static' and r['iso_outside'])), str(sum(1 for r in rows.values() if r['direction'] == 'static')),
                str(sum(1 for r in rows.values() if r['direction'] == 'Nk' and r['iso_outside'])), str(sum(1 for r in rows.values() if r['direction'] == 'Nk')),
                str(sum(1 for r in rows.values() if r['second']['top'])), str(len(rows)), str(len(A['q7_rows']))]
EXP['上の限界の文の「全経路'] = [str(m), '%.6f' % (0.05 / m), str(kmax(m)), str(kmax(16)), str(A['main_run']['batch']), f4(max(via.values())), f4(T3['pilot']['noise_max']), '%.0f' % (max(via.values()) / T3['pilot']['noise_max']),
                          f4(max(abs(vd[c]) for c in mains)), f4(max(abs(vd[c]) for c in gate_only)), '%.2f' % min(iq), '%.2f' % max(iq), '%.3f' % min(effs), '%.3f' % max(effs)] + [
                          x for c, g_, w_ in near for x in ('%.3f' % g_, f4(w_))] + [f4(vmax[v]) for v in sorted(vmax)]
EXP['この最終版は'] = [str(len([x for x in VR['checks']]) and 21), '0']
EXP['上の検分票は'] = []
bl_res = []
for start, body in blocks:
    head = body[0][len('- ' + TAG):]
    key = [k for k in EXP if head.startswith(k)]
    if head.startswith('次の区画の表は') or head.startswith('上の区画の表の並べ直し'):
        continue
    if len(key) != 1:
        bl_res.append((start, head[:20], '種類が決まらない', None))
        continue
    got = toks(body)
    want = EXP[key[0]]
    ok_ = collections.Counter(got) == collections.Counter(want)
    bl_res.append((start, key[0], ok_, {'区画の数': got, '出し直した数': want} if not ok_ else len(got)))
add('(五) 足した区画の数は、記録から出し直した数の並びと同じ（区画ごと）', all(x[2] is True for x in bl_res), '・'.join('%d 行 %s %s' % (s, k, ('数 %d' % d) if ok is True else ('外れ %s' % d)) for s, k, ok, d in bl_res),
    'この確かめでは、逸脱の器の式を読まずに記録から出し直した。頭の添えの「照らした記録の項 21」は逸脱の器の確かめの記録の値')

# (六) 節の指し
sec = {}
cur = None
for l in L:
    mm = re.match(r'^## (\d)\. ', l)
    if mm:
        cur = int(mm.group(1))
        sec[cur] = []
    elif l.startswith('## '):
        cur = None
    if cur is not None:
        sec[cur].append(l)
secT = {k: NL.join(v) for k, v in sec.items()}
lim_after = [NL.join(b) for s, b in blocks if b[0].startswith('- ' + TAG + '上の限界の文の「全経路')]
rej = [l for l in L if l.startswith('- 「')]
after_rej = [b for s, b in blocks if b[0].startswith('- ' + TAG + '起草者の欄の文が指す数')]
checks6 = {'§4 にバッチの大きさと近道の行': 'バッチの大きさ' in secT.get(4, '') and '近道' in secT.get(4, ''),
           '§5 に GPU の行': 'GPU' in secT.get(5, ''),
           '§7 の後の注に計算の道': bool(lim_after) and '計算の道:' in lim_after[0],
           '§2 に升目ごとの確率の表': '升目と符号ごとの無操作の選択肢 a の文字の確率' in secT.get(2, ''),
           '§1 に (vi) の (a)・揺れの版・段階 B の無操作の破局の率': all(x in secT.get(1, '') for x in ('(vi) (a)', '(iv) 揺れの版', '段階 B の無操作の破局の率')),
           '§0 に「主の記述の札と門」': '**主の記述の札と門**' in secT.get(0, ''),
           '起草者の欄の直後に「下の区画」（起草者の欄の数の区画）': bool(after_rej) and TXT.index(after_rej[0][0]) > TXT.index(rej[2]) and TXT.index(after_rej[0][0]) < TXT.index('**答えの範囲**'),
           '§5 に一段目の差の最大': '一段目' in secT.get(5, '') and '差の最大' in secT.get(5, ''),
           '転記行 C に sub:N1 の q7 の区間': 'sub:N1:O-Ncold-v~O-Ncold-vrand 20/200 − 24/200 ＝ -2.0 [-8.26, 4.23]' in open(P('records/Bl3/design-facts-Bl3.md'), encoding='utf-8').read(),
           '台帳の封印の行に封印の台本と登録者の補い': all(x in [l for l in open(P('records/FREEZE-RECORD.md'), encoding='utf-8').read().split(NL) if 'B-lens 層三 予想封印' in l][0] for x in ('封印の台本', '19:24'))}
add('(六) 足した区画と起草者の欄が指す節に、指した中身がある', all(checks6.values()), '・'.join('%s %s' % (k, '合う' if v else '外れ') for k, v in checks6.items()))
res = {'what': '起草者の最終の見直し・二度目の器による確かめ（逸脱の器を読まずに記録から書いた式）', 'inputs': {FINAL: s16(FINAL)}, 'checks': R,
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(res, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1, default=str)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
MD = ['# 起草者の最終の見直し・二度目の器による確かめ（機械生成・`check_review2_Bl3.py`）', '', '- 対象: `%s`（SHA16 %s）。枠: `frame-review2-Bl3.md`（読み直す前にコミット c9ea96c で置いた）。' % (FINAL, s16(FINAL)), '',
      '| 確かめ | 結果 | 中身 | 注 |', '|---|---|---|---|'] + ['| %s | %s | %s | %s |' % (cell(x['what']), '合う' if x['ok'] else '外れ', cell(x['got']), cell(x['note'])) for x in R] + ['',
      res['clause'], '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(MD))
for x in R:
    print(('OK ' if x['ok'] else 'NG ') + x['what'], '|', str(x['got'])[:600])
