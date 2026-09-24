# -*- coding: utf-8 -*-
"""結果の巡・第一巡の六票の事実の主張を、公開の記録の現物で再現する（再現の番号 K361〜・コーディネータ・2026-09-24）。
層一と層二の記録・報告の草案・正本・凍結の本文・封印の記録・二つの予想・裁定の記録（逐語）・段階 B の試行の記録を読むだけで、射影を新しく計算しない。
判定: 再現した／一部再現／再現しない。数と判定は器が出す（手で打たない）。既にある記録には書かない。
用法: python records/reviews/Blens/results-round1/verify_Blens_results_r1.py"""
import os, re, json, math, glob, hashlib, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
OUT_MD, OUT_JS = os.path.join(HERE, 'verification-Blens-results-r1.md'), os.path.join(HERE, 'verify-Blens-results-r1.json')
assert not os.path.exists(OUT_MD) and not os.path.exists(OUT_JS), '既にある'
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
js = lambda rel: json.load(open(j(*rel.split('/')), encoding='utf-8'))
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
T, L, C = js('design/contrasts-Blens.json'), js('results/Blens/lens-Blens.json'), js('results/Blens/calib-Blens.json')
REP, FROZ, REQ = rd('records/Blens/results-Blens.md'), rd('design/design-Blens-FROZEN.md'), rd('records/reviews/Blens/results-round1/review-request-Blens-results-r1.md')
PC, PR = js('records/predictions/predictions-Blens-coordinator.json'), js('records/predictions/predictions-Blens-registrant.json')
FR, SR = js('records/Blens/FREEZE-RECORD-Blens.json'), js('records/Blens/sealing-record-Blens.json')
D187, D188, LEDGER = rd('records/Blens/rulings-D187.md'), rd('records/Blens/rulings-D188.md'), rd('records/FREEZE-RECORD.md')
NP = '予想しない'
lay = L['layers']['0.5']
dS = lay['directions']['static']
K, rows = [361], []


def row(src, claim, evidence, verdict):
    rows.append({'K': 'K%d' % K[0], 'src': src, 'claim': claim, 'evidence': evidence, 'verdict': verdict})
    K[0] += 1


# K361 結果の巡の個体
a = '結果の巡も同じ組み立て（新しい個体）' in FROZ
b = '同じ四名への結果の巡' in REQ
row('C1-9・C2-14', '凍結の本文 §10 は結果の巡を「新しい個体」で組むとし、依頼文は同じ四名に回した',
    '凍結の本文に「結果の巡も同じ組み立て（新しい個体）」: %s／依頼文に「同じ四名への結果の巡」: %s。正本 `review_plan.results` は数だけ（%s）で個体を定めない' % (a, b, T['review_plan']['results']),
    '再現した' if a and b else '再現しない')

# K362〜K364 照合の表
import importlib.util, sys
sys.path.insert(0, j('tools'))
spec = importlib.util.spec_from_file_location('BRB', j('tools', 'build_report_Blens.py'))
BRB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BRB)
out = BRB.outcomes(T, L, C)
na = {k for k in out if k.endswith('.dir') and out[k] == NP}
aff = {who: sorted(k for k in na if P.get(k, NP) != NP) for who, P in (('登録者', PR), ('コーディネータ', PC))}
row('G1-1・G2-5-1・G3-2・C1-3・C2-11・C3-中1', '札が付かなかった項目の向きの欄を、予想者の値と文字で比べて「不一致」と印字する（登録者の五欄とコーディネータの p3.dir）',
    '結果が「予想しない」になる向きの欄 %d（%s）。予想者の値が「予想しない」でない欄: 登録者 %s・コーディネータ %s' % (len(na), '・'.join(sorted(na)), '・'.join(aff['登録者']), '・'.join(aff['コーディネータ'])),
    '再現した' if len(aff['登録者']) == 5 and aff['コーディネータ'] == ['p3.dir'] else '一部再現')
cnt = {}
for who, P in (('登録者', PR), ('コーディネータ', PC)):
    c = {'一致': 0, '不一致': 0, '該当なし': 0, '予想しない': 0}
    for k, v in out.items():
        if k in na:
            c['該当なし'] += 1
        elif P.get(k, NP) == NP:
            c['予想しない'] += 1
        else:
            c['一致' if P[k] == v else '不一致'] += 1
    cnt[who] = c
row('C1-3', '直した数え方は、登録者 一致 4・不一致 8・該当なし 5・予想しない 0／コーディネータ 一致 7・不一致 4・該当なし 5・予想しない 1',
    '器の結果の値と封印した二つの JSON から数え直した: 登録者 %s／コーディネータ %s' % (cnt['登録者'], cnt['コーディネータ']),
    '再現した' if cnt['登録者'] == {'一致': 4, '不一致': 8, '該当なし': 5, '予想しない': 0} and cnt['コーディネータ'] == {'一致': 7, '不一致': 4, '該当なし': 5, '予想しない': 1} else '一部再現')
MAPV = {'p1.survival.dir': ('M_L_survival', '反対'), 'p2.survival.dir': ('M_X_survival', '反対'), 'p2.nuclear.dir': ('M_X_nuclear', '反対'), 'p3.dir': ('M_E', 'O の語の側'), 'p4.dir': ('M_F', '押し下げる')}
POSV = {'M_L_survival': '破局の文字の側', 'M_X_survival': '破局の選択肢の語の側', 'M_X_nuclear': '破局の選択肢の語の側', 'M_E': 'O の語の側', 'M_F': 'コードブロックの書き出しを押し上げる'}
NEGV = {'M_L_survival': '反対', 'M_X_survival': '反対', 'M_X_nuclear': '反対', 'M_E': 'Osec の語の側', 'M_F': '押し下げる'}
same = []
for who, P in (('登録者', PR), ('コーディネータ', PC)):
    for k in aff[who]:
        m = MAPV[k][0]
        v = L['primary']['metrics'][m]['value']
        same.append((who, k, P[k], (POSV[m] if v > 0 else NEGV[m]) == P[k], v))
row('C3-中1', '影響する六升の予想の向きは、どれも札の無い値の符号と同じ（符号で比べると「一致」六つになる）',
    '・'.join('%s %s「%s」（値 %.4g・符号と %s）' % (w, k, p, v, '同じ' if s else '違う') for w, k, p, s, v in same),
    '再現した' if len(same) == 6 and all(x[3] for x in same) else '一部再現')

# K365 上位の次元を零にした感度
z = L['descriptive_after_seal']['static@0.5']['zeroed']
row('C3-中1・C2-10', '上位八次元を零にした感度で、v̂ の M_X_nuclear は符号が変わり（→ +0.0147）、M_F は −0.061 から −0.011 に縮む',
    'M_X_nuclear %.4g → %.4g・M_F %.4g → %.4g（`descriptive_after_seal.static@0.5.zeroed`）' % (dS['M_X_nuclear']['value'], z['M_X_nuclear'], dS['M_F']['value'], z['M_F']),
    '再現した' if z['M_X_nuclear'] > 0 > dS['M_X_nuclear']['value'] and abs(z['M_F'] + 0.0107) < 0.0005 else '一部再現')

# K366〜K367 ランダム方向の実在の差の最上位
MET9 = ['M_L_survival', 'M_L_nuclear', 'M_X_survival', 'M_X_nuclear', 'M_Lc', 'M_R_survival', 'M_F', 'M_F_sens', 'M_E_static']
cells, tops = 0, 0
for r in ('0.25', '0.5', '0.75'):
    for u, dd in L['layers'][r]['directions'].items():
        if 'rand' not in u:
            continue
        for m in MET9:
            if m in dd and 'real_rank' in dd[m]:
                cells += 1
                tops += 1 if dd[m]['real_rank']['top'] else 0
of_rand = L['layers']['0.5']['directions']['rand:0']['M_F']['real_rank']['of']
row('C1-1・C3-軽12', 'ランダム方向は §4 の 108 升目のうち 12 で実在の差の最上位（交換可能なら約 3.4〜3.7）',
    '升目 %d・最上位 %d・交換可能なときの目安 %.2f（比べる相手の数 +1 = %d）' % (cells, tops, cells / of_rand, of_rand), '再現した' if (cells, tops) == (108, 12) else '一部再現')
top5 = {}
for u, dd in lay['directions'].items():
    if 'rand' in u:
        hit = [m for m in ('M_L_survival', 'M_L_nuclear', 'M_X_survival', 'M_X_nuclear', 'M_F') if dd[m]['real_rank']['top']]
        if hit:
            top5[u] = hit
row('C1-1', '選んだ層では、ランダム方向 6 本のうち 3 本が主の五つの物差しのどれかで最上位（三本とも M_F）',
    '最上位の本と物差し: %s' % top5, '再現した' if len(top5) == 3 and all(v == ['M_F'] for v in top5.values()) else '一部再現')

# K368〜K369 兄弟の対と比べる相手の分布
PRIM = {'M_L_survival': 'M_L_survival', 'M_L_nuclear': 'M_L_nuclear', 'M_X_survival': 'M_X_survival', 'M_X_nuclear': 'M_X_nuclear', 'M_F': 'M_F', 'M_E': 'M_E_static'}
SW = set(['O~Osec', 'O~Osec-Ncold', 'Osec~O-Ncold', 'O-Ncold~Osec-Ncold'])
comp = {m: [abs(v[mm]) for p, v in lay['real'].items() if p not in SW for mm in [PRIM[m]]] for m in PRIM}
sib = lay['siblings']['static']
mx = max(((p, abs(v['M_L_nuclear'])) for p, v in lay['real'].items() if p not in SW), key=lambda x: x[1])
isd = lay['iso_sd']['M_L_nuclear']
below = {m: sum(1 for x in comp[m] if x < 0.6745 * lay['iso_sd'][PRIM[m]]['analytic']) for m in PRIM}
row('C2-1・C3-中3', '兄弟の対 O~Osec-Ncold の M_L_nuclear（−0.0641）は v̂（0.0523）より大きい。比べる相手の最大は O~Nk（0.0512・差 2.3%）。24 組の |値| の中央値 0.0108・等方の標準偏差 0.0724（抽選）／0.0734（解析）。24 組のうち 23 組が等方の中央値の下',
    '兄弟 %s・v̂ %.4g・比べる相手の数 %d・最大 %s %.4g（v̂ との差 %.1f%%）・中央値 %.4g・等方の標準偏差 抽選 %.4g／解析 %.4g・等方の |値| の中央値の下: %d 組'
    % ({p: round(v['M_L_nuclear'], 4) for p, v in sib.items()}, abs(dS['M_L_nuclear']['value']), len(comp['M_L_nuclear']), mx[0], mx[1], 100 * (1 - mx[1] / abs(dS['M_L_nuclear']['value'])),
       statistics.median(comp['M_L_nuclear']), isd['sampled'], isd['analytic'], below['M_L_nuclear']),
    '再現した' if abs(sib['O~Osec-Ncold']['M_L_nuclear']) > abs(dS['M_L_nuclear']['value']) and mx[0] == 'O~Nk' and below['M_L_nuclear'] == 23 else '一部再現')
ratio = {m: statistics.median(comp[m]) / lay['iso_sd'][PRIM[m]]['sampled'] for m in PRIM}
row('C2-13・C3-中3', '選んだ層の 24 組の |値| の中央値 ÷ 等方の標準偏差は、M_L_survival 0.44・M_L_nuclear 0.15・M_X_survival 0.49・M_F 0.41・M_X_nuclear 1.25・M_E 1.34。等方の中央値の下の組は M_L_nuclear 23・M_L_survival 18・M_F 18・M_E 8・M_X_nuclear 3',
    '比: %s／下の組: %s' % ('・'.join('%s %.2f' % (m, v) for m, v in ratio.items()), '・'.join('%s %d' % (m, v) for m, v in below.items())),
    '再現した' if all(abs(ratio[m] - e) < 0.02 for m, e in (('M_L_survival', 0.44), ('M_L_nuclear', 0.15), ('M_X_survival', 0.49), ('M_F', 0.41), ('M_X_nuclear', 1.25), ('M_E', 1.34))) else '一部再現')

# K370 感度の集合
var = [k for k in dS if ':' in k and k.split(':')[0] in ('M_X_survival', 'M_X_nuclear', 'M_E_static')]
low = [(k, dS[k]['p_iso'], dS[k]['real_rank']['rank'], dS[k]['real_rank']['of']) for k in var if dS[k]['p_iso'] < 0.05]
row('C2-9・C3-中4', 'v̂・選んだ層の X と E_static の感度の変種は十一。M_E_static:kata1 は主と同じ値。名目の 0.05 を下回るのは M_E_static:all（0.021・順位 1／25）だけで、報告に無い',
    '変種 %d（%s）・kata1 と主の値が同じ: %s・0.05 を下回る: %s・報告に「:all」の字: %s' % (len(var), '・'.join(var), dS['M_E_static:kata1']['value'] == dS['M_E_static']['value'], low, ':all' in REP),
    '再現した' if len(var) == 11 and len(low) == 1 and low[0][0] == 'M_E_static:all' else '一部再現')

# K371〜K375 報告に無い記述
row('C2-10・C3-中4', '封印の後の記述のうち「狙いの度合い」と「上位の次元を零にした感度」は層一の記録にあるが報告に無い',
    '層一の記録の鍵: %s・報告に「狙い」: %s・「零にした」: %s' % (sorted(L['descriptive_after_seal']['static@0.5']), '狙い' in REP, '零にした' in REP),
    '再現した' if 'targeting' in L['descriptive_after_seal']['static@0.5'] and '狙い' not in REP and '零にした' not in REP else '一部再現')
row('C1-2・C2-1・C3-中3', '兄弟の三対・八腕の値・対の距離は層一の記録にあるが、報告に無い（正本 `nulls.real.rule`「別の行に並べる」・`label_meaning`「記述に出す」）',
    '層一の記録の鍵: %s・報告に「兄弟」: %s・「八腕」: %s・「対の距離」: %s' % ([k for k in lay if k in ('siblings', 'arm_values', 'pair_distance')], '兄弟' in REP, '八腕' in REP, '対の距離' in REP),
    '再現した' if all(k in lay for k in ('siblings', 'arm_values', 'pair_distance')) and '対の距離' not in REP else '一部再現')
mr = [x for x in C['magnitude']['main_rows'] if x.get('eligible')]
ex = [x['parts_fmain']['exact'] for x in mr if x['row'].startswith('S4|O-Ncold')]
row('C1-2・C2-6・C3-中4', '大きさの目盛りの三つの部分と余弦は層二の記録にあるが報告に無い。O-Ncold の土台の四行の正確な直接の変化は +0.007〜+0.032 程度（C2 は +0.011〜）',
    '層二の行の鍵に parts_fmain・cos_u_h: %s・報告に「余弦」: %s・O-Ncold の四行の正確な変化 %s' % (all('parts_fmain' in x for x in mr), '余弦' in REP, ['%.4f' % v for v in ex]),
    '再現した（範囲は C3 の値）' if min(ex) < 0.011 else '再現した')
has_raw_main = any(any(k.startswith('draw') or 'raw' in k for k in x) for x in mr)
lk = C['magnitude']['letter']
has_raw_letter = any(any(k2.startswith('draw') for k2 in rr) for v in lk.values() for rr in v['rows'].values())
row('C1-2・C3-中4', '生の全語彙の softmax の確率（正本 `magnitude.quantity`「記述」）が報告に無く、主位置では層二の記録にも見当たらない',
    '主位置の行に生の確率の鍵: %s・答えの文字の位置の行（draw_*）: %s・報告に「softmax」: %s' % (has_raw_main, has_raw_letter, 'softmax' in REP),
    '再現した（主位置では凍結した器が計算していない）' if not has_raw_main and has_raw_letter else '一部再現')
key = [k for k in lk.get('S1|Onull', {}).get('rows', {}) if k.endswith('|static')]
ag = lk['S1|Onull']['rows'][key[0]] if key else None
row('C1-2・C2-8', '答えの文字の位置の記述の層のまとめ（平均・中央値・四分位）は層二の記録にあるが報告に無い（例: S1|Onull の v̂ の行で「a」の正確な変化の平均 −0.0095・「c」+0.021）',
    '行 %s・a の平均 %s・c の平均 %s・報告に「四分位」: %s' % (key[0] if key else None, ('%.4g' % ag['dlogit_exact_a']['mean']) if ag else None, ('%.4g' % ag['dlogit_exact_c']['mean']) if ag and 'dlogit_exact_c' in ag else None, '四分位' in REP),
    '再現した' if ag and abs(ag['dlogit_exact_a']['mean'] + 0.0095) < 0.0005 and '四分位' not in REP else '一部再現')
row('C1-2・C3-軽2', '報告 §3 の「S4|Osec-Ncold・文脈 20」は、転記行 E の「選んだ 20 件で 1（文脈は一つ）」と語が食い違う',
    '報告に「S4|Osec-Ncold・文脈 20」: %s・凍結の本文に「選んだ 20 件で 1（文脈は一つ）」: %s' % ('S4|Osec-Ncold・文脈 20' in REP, '選んだ 20 件で 1（文脈は一つ）' in FROZ),
    '再現した' if 'S4|Osec-Ncold・文脈 20' in REP and '選んだ 20 件で 1（文脈は一つ）' in FROZ else '一部再現')

# K377 較正の検査の位置
def binom_upper(n, p, k):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def central(n, p, ci):
    lo_t, hi_t = (1 - ci) / 2, (1 - ci) / 2
    cdf, lo = 0.0, None
    for i in range(n + 1):
        cdf += math.comb(n, i) * p ** i * (1 - p) ** (n - i)
        if lo is None and cdf > lo_t:
            lo = i
        if cdf >= 1 - hi_t:
            return lo, i
    return lo, n


pc = C['magnitude']['colab_check']['calibration']['S4|Osec-Ncold|json']['main']
import blens_core as BC
pT_local = [x for x in mr if x['row'].startswith('S4|Osec-Ncold')][0]['pT_before']
up, up2 = binom_upper(200, pc['p_T'], 154), binom_upper(200, pT_local, 154)
zc = (154 - 200 * pc['p_T']) / math.sqrt(200 * pc['p_T'] * (1 - pc['p_T']))
row('C1-6・C2-7・C3-中6', '較正の検査は 0.999 の区間（112〜155）の上端の一つ内側で通った。確率 0.6713 で 154 以上の割合 0.0015（z 2.97）。手元の確率 0.6949 では 0.011。0.99 の区間は 117〜151',
    '確率 %.4f・観測 %d／%d・区間 %s（記録）・154 以上の割合 %.4f・z %.2f・手元の確率 %.4f で %.3f・0.99 の中央の区間 %s' % (pc['p_T'], pc['k'], pc['n'], pc['interval'], up, zc, pT_local, up2, BC.binom_central(200, pc['p_T'], 0.99)),
    '再現した' if abs(up - 0.0015) < 0.0003 and tuple(BC.binom_central(200, pc['p_T'], 0.99)) == (117, 151) else '一部再現')

# K378 p8
g = {x['row']: x for x in mr}
lo, r0 = g['S4|Osec-Ncold+v6b|loaded'], g['S4|Osec-Ncold+vrand|rand:0']
row('C1-4・C3-中2', 'p8: 層一では (6b) の M_F −0.0084（等方 0.914）と一本目 +0.0576 で「逆向き」。層二では (6b) の正確な変化 −0.00025（層一の近似 −0.0029・残差に沿う部分 +0.0033）で、変換の後の確率は (6b) +0.0024・一本目 +0.0062 とどちらも上がる',
    '(6b) M_F %.4g（等方 %.3f）・一本目 %.4g／(6b) 正確 %.3g・層一 %.3g・沿う %.3g・確率 %+.4f／一本目 確率 %+.4f' % (lay['directions']['loaded']['M_F']['value'], lay['directions']['loaded']['M_F']['p_iso'],
                                                                                 lay['directions']['rand:0']['M_F']['value'], lo['parts_fmain']['exact'], lo['parts_fmain']['layer1'], lo['parts_fmain']['along'], lo['dp'], r0['dp']),
    '再現した' if lo['dp'] > 0 and r0['dp'] > 0 and lay['directions']['loaded']['M_F']['value'] < 0 < lay['directions']['rand:0']['M_F']['value'] else '一部再現')
zero_rows = [x['row'] for x in mr if x['pT_before'] == 0 and x['pT_after'] == 0]
row('C1-5', '比を出した 7 行のうち 4 行は、切り詰めで変換の後の確率が前後とも零', '前後とも零の行 %d／%d（%s）' % (len(zero_rows), len(mr), '・'.join(zero_rows)),
    '再現した' if len(zero_rows) == 4 and len(mr) == 7 else '一部再現')

# K380〜K382 露出
m188 = re.search(r'````text\n(.*?)\n````', D188, re.S).group(1)
m187 = re.search(r'````text\n(.*?)\n````', D187, re.S).group(1)
a1, a2 = 'p1.survival.dir=予想しない' in m188, '「付かない」の項目' in m188
row('C2-12・C3-中8', '登録者の封印の前の 07:52 の返信（裁定 D188 の前の案）に、「p1.survival.dir=予想しない」と「私の予想には「付かない」の項目がある」が逐語で入っている（コーディネータの予想の一部）',
    '裁定 D188 の記録の案の逐語に「p1.survival.dir=予想しない」: %s・「「付かない」の項目」: %s。登録者の予想の JSON のファイルの更新は 08:15・SHA の発言は 08:17（台帳の封印の行）' % (a1, a2),
    '再現した' if a1 and a2 else '一部再現')
b1, b2 = '0.671' in m187, 'O-Ncold' in m187
row('C2-12・C3-中8', '登録者は 06:30 の返信（裁定 D187 の前の案）で較正の確率 0.671 を読んでいる（C3 は O-Ncold の確率 0 も読んだとする）',
    '裁定 D187 の記録の案の逐語に「0.671」: %s・「O-Ncold」: %s' % (b1, b2), '一部再現（0.671 は入っている・O-Ncold の確率は入っていない）' if b1 and not b2 else ('再現した' if b1 and b2 else '再現しない'))
s_md = rd('records/Blens/sealing-record-Blens.md')
e1, e2, e3 = 'ツールの出力' in s_md or 'ツールの出力' in json.dumps(SR, ensure_ascii=False), 'ツールの出力' in json.dumps(FR.get('deviations', []), ensure_ascii=False), 'ツールの出力' in LEDGER
row('C1-10・C2-14・C3-中8', 'コーディネータの予想の値がツールの出力に出たことは、封印の記録（md・json）にも逸脱台帳（D-BL1）にも無い',
    '封印の記録に: %s・B-lens の逸脱台帳に: %s・全体の台帳 `records/FREEZE-RECORD.md` の封印の行に: %s（全体の台帳は束に入れていない）' % (e1, e2, e3),
    '一部再現（封印の記録と逸脱台帳には無い・全体の台帳にはある）' if not e1 and not e2 and e3 else ('再現した' if not (e1 or e2 or e3) else '再現しない'))
row('C1-13・C2-14・C3-軽1', '報告の頭の「封印の記録 SHA16 25C7978F48F10508」は JSON のほう（束の md は 047EAE5CE73658AB）',
    'JSON %s・md %s・報告に 25C7978F48F10508: %s' % (s16('records/Blens/sealing-record-Blens.json'), s16('records/Blens/sealing-record-Blens.md'), '25C7978F48F10508' in REP),
    '再現した' if s16('records/Blens/sealing-record-Blens.json') == '25C7978F48F10508' else '一部再現')

# K384〜K389 文と印字
row('C2-13・C3-中5', '報告の限界に「射影の値はまだ誰も見ていない」がそのまま出ている（結果の報告では事実と合わない）', '報告に含む: %s' % ('射影の値はまだ誰も見ていない' in REP),
    '再現した' if '射影の値はまだ誰も見ていない' in REP else '再現しない')
t_or = 'または語の側の帰無の外だが' in REP
t0 = REP.split('**読みの型**')[1].split('**打ち消しの定型**')[0]
row('C1-11・C2-4・C3-問1', '〈二つ目の札だけ〉の文が二つの場合を「または」でつないだまま。§0 の型の行に、実在の差の中の順位の一行（正本 `reading_notes[2]`）が無い',
    '「または語の側の帰無の外だが」: %s・§0 の型の行に「実在の差の中の順位」: %s・器の docstring に同じ決まり: %s' % (t_or, '実在の差の中の順位' in t0, '各型の文に、実在の差の中の順位' in rd('tools/build_report_Blens.py')),
    '再現した' if t_or and '実在の差の中の順位' not in t0 else '一部再現')
row('C1-問2', '§2 の表は、試されていない Holm の第二段（M_X・0.05）を段として印字している', '報告の行「| full | M_X | 64 | 5040 | -0.05282 | 0.8732 | 0.05 | いいえ |」: %s' % ('| full | M_X | 64 | 5040 | -0.05282 | 0.8732 | 0.05 | いいえ |' in REP),
    '再現した' if '| full | M_X | 64 | 5040 | -0.05282 | 0.8732 | 0.05 | いいえ |' in REP else '一部再現')
tl = [l for l in REP.split(NL) if l.startswith('- 調整走行（記述）')]
pushes = {}
for l in tl:
    mm = re.match(r'- 調整走行（記述）: (\w+)・層 ([0-9.]+)・係数 ([0-9.]+): M_L の v̂ の順位（行動 (\d)・押し (\d)', l)
    if mm:
        pushes.setdefault((mm.group(1), mm.group(2)), set()).add(mm.group(5))
row('C1-8', '調整走行の行は、同じ場面・層で係数を変えても押しの順位が同じ（行が独立でない）。方向 4 本の順位相関が 0.8 以上になる偶然の割合は 1/6。順位の向きの定義が無い',
    '場面 × 層ごとの M_L の押しの順位の種類の数: %s・四つの並べ替え 24 のうち順位相関 0.8 以上 4（= 1/6）・報告に「順位の向き」の定義: %s' % ({'%s@%s' % k: len(v) for k, v in pushes.items()}, '大きい側' in '\n'.join(tl)),
    '再現した' if all(len(v) == 1 for v in pushes.values()) else '一部再現')
row('C2-14・C3-軽11', '報告に費用の実績の行（正本 `report_rules.machine_block.cost_line_tag`）が無い。層一の記録の `inputs` に器の SHA16 が無い',
    '報告に「%s」: %s・層一の記録の inputs の鍵: %s' % (T['report_rules']['machine_block']['cost_line_tag'], T['report_rules']['machine_block']['cost_line_tag'] in REP, sorted(L['inputs'])),
    '再現した' if T['report_rules']['machine_block']['cost_line_tag'] not in REP else '一部再現')
row('C3-軽10', '正本 `report_rules.machine_block.rule` が `tools/build_report_B.py` を指している（段階 B からの写し）', '文: %s' % T['report_rules']['machine_block']['rule'][:80],
    '再現した' if 'build_report_B.py' in T['report_rules']['machine_block']['rule'] else '再現しない')

# K390 §4 の数え上げ
vals = re.findall(r'（等方 ([0-9.eE-]+)・実在の差 (\d+)／(\d+)）', REP.split('## 4.')[1].split('## 5.')[0])
sec4 = REP.split('## 4.')[1].split('## 5.')[0]
per_layer = {}
cur = None
for l in sec4.split(NL):
    m1 = re.match(r'- 層の割合 ([0-9.]+):', l)
    if m1:
        cur = m1.group(1)
    for p_, r_, n_ in re.findall(r'（等方 ([0-9.eE-]+)・実在の差 (\d+)／(\d+)）', l):
        per_layer.setdefault(cur, []).append(float(p_))
allp = [p for v in per_layer.values() for p in v]
row('C1-7・C2-2・C3-軽4', '§4 の値は 216。等方の割合が 0.05 を下回るもの 16（偶然の目安 約 11）、0.01 を下回るもの 5（五つとも層 0.75）',
    '値 %d・0.05 未満 %d（偶然の目安 %.1f）・0.01 未満 %d（層ごと %s）・0.002 以下 %d' % (len(allp), sum(p < 0.05 for p in allp), 0.05 * len(allp), sum(p < 0.01 for p in allp),
                                                                         {k: sum(p < 0.01 for p in v) for k, v in per_layer.items()}, sum(p <= 0.002 for p in allp)),
    '再現した' if len(allp) == 216 and sum(p < 0.05 for p in allp) == 16 and sum(p < 0.01 for p in allp) == 5 else '一部再現')

# K391 Holm の最初の段に要る大きさ
zc1 = 2.638
need = {m: zc1 * lay['iso_sd'][PRIM[m]]['analytic'] / abs(L['primary']['metrics'][m]['value']) for m in ('M_E', 'M_L_survival', 'M_L_nuclear', 'M_F')}
row('C3-軽12', 'Holm の最初の段（0.05／6）を越えるのに要る |値| は、観測の 2.0〜3.7 倍（M_E・M_L・M_F・正規近似）', '倍率（解析の標準偏差・|z| 2.638）: %s' % '・'.join('%s %.2f' % kv for kv in need.items()),
    '再現した' if 1.9 < min(need.values()) and max(need.values()) < 3.8 else '一部再現')

# K392〜K397 そのほか
ofs = {u: lay['directions'][u]['M_F']['real_rank']['of'] for u in ('static', 'loaded', 'Nk', 'td', 'rand:0')}
row('G3-5', '実在の差の順位の分母は、static・loaded 25／Nk・td 28／ランダム方向 29（比べる相手から除く対の違い）', '分母: %s' % ofs, '再現した' if ofs == {'static': 25, 'loaded': 25, 'Nk': 28, 'td': 28, 'rand:0': 29} else '一部再現')
row('G1-7・G2-7・G3-7', '正本の限界の文の数（票は 21・25・23 とした）', '正本 `limits` の数 %d・報告 §9 の行の数 %d' % (len(T['limits']), sum(1 for l in REP.split('## 9.')[1].split('## 検分票')[0].split(NL) if l.startswith('- '))),
    '一部再現（数は票ごとに違う・正本は %d）' % len(T['limits']))
row('G1-3', '選んだ層の後に続く層は「19 層」（G2 は「Layer 18〜36」）', '復号の層 %d 本のうち、選んだ層の添字 %d の後の層は添字 %d〜%d の %d 本' % (T['inputs']['model']['num_hidden_layers'], T['layers']['indices']['0.5'], T['layers']['indices']['0.5'] + 1, T['inputs']['model']['num_hidden_layers'] - 1, T['inputs']['model']['num_hidden_layers'] - 1 - T['layers']['indices']['0.5']),
    '再現しない（18 本）')
row('C3-1', '層一の記録（23:40 UTC）と層二の記録（23:46 UTC）は封印（23:18:53 UTC）の後に作られた', '層一 %s・層二 %s・封印の記録 %s' % (L['generated_utc'], C['generated_utc'], SR['written_utc']),
    '再現した' if L['generated_utc'] > SR['written_utc'][:16] and C['generated_utc'] > SR['written_utc'][:16] else '再現しない')
chk = {}
for rel in ('tools/blens_core.py', 'tools/blens_lens.py', 'tools/blens_calib.py', 'tools/build_report_Blens.py', 'tools/colab/boot_Blens.py', 'tools/report_lint.py', 'tools/steer_B.py'):
    chk[rel] = FR['frozen_sha16'].get(rel) == s16(rel)
row('C3-1', '凍結した器の SHA16 は、計算のときも凍結の値のまま（封印の器は逸脱 D-BL1 の後の値）', '一致: %s・封印の器 %s（逸脱の後の値 %s）' % (chk, s16('tools/seal_Blens.py'), FR['deviations'][0]['files'][0]['sha16_after']),
    '再現した' if all(chk.values()) and s16('tools/seal_Blens.py') == FR['deviations'][0]['files'][0]['sha16_after'] else '一部再現')
tr = [json.loads(l) for l in open(glob.glob(j('results', 'stageB', 'stageB__S4__Osec-Ncold__s1', 'trials-*.jsonl'))[0], encoding='utf-8')]
row('C2-7', '段階 B の様式 b は最終の試行の頭で決まるので、無操作の S4|Osec-Ncold に引き直しがあれば、観測は JSON 直答の側に寄りうる',
    '無操作の S4|Osec-Ncold の試行 %d・書式の外れ（引き直しの元）%d・様式 b %d' % (len(tr), sum(1 for t in tr if t.get('format_fail')), sum(1 for t in tr if t.get('style_b'))),
    '再現しない（書式の外れが零なので、引き直しは無い）' if not any(t.get('format_fail') for t in tr) else '一部再現')

# 書き出し
json.dump({'rows': rows, 'counts': cnt, 'inputs': {r: s16(r) for r in ('results/Blens/lens-Blens.json', 'results/Blens/calib-Blens.json', 'records/Blens/results-Blens.md', 'design/contrasts-Blens.json', 'design/design-Blens-FROZEN.md')}},
          open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
M = ['# 結果の巡・第一巡の六票の事実の主張の再現（機械生成・`verify_Blens_results_r1.py`・2026-09-24・コーディネータ）', '',
     '- 読んだ記録: 層一 `results/Blens/lens-Blens.json`・層二 `results/Blens/calib-Blens.json`・報告の草案・正本・凍結の本文・封印の記録・二つの予想・裁定 D187 と D188 の記録（案の逐語）・全体の台帳・段階 B の試行の記録。射影は新しく計算していない（組み立ての器の関数 `outcomes` を読み込んで結果の値を取った）。',
     '- 出所の札: G1〜G3 は Gemini 3.8 Flash の一人目〜三人目、C1〜C3 は claude.ai の Claude Opus 5.5 の一人目〜三人目（登録者の並べた順）。票の自己申告: C1 は設計の巡の C2 と同じ個体、C2 は設計の巡の C1 と同じ個体、G2 は設計の巡の G2 と同じ個体、G3 と C3 は新しい個体（登録者の言葉）。G1 は設計の巡の二巡を担当した個体と書く（G1 か G2 かは書かない）。',
     '- 判定の数: %s。' % '・'.join('%s %d' % (v, sum(1 for r in rows if r['verdict'].startswith(v))) for v in ('再現した', '一部再現', '再現しない')), '',
     '| 再現 | 出所 | 票の主張 | 現物 | 判定 |', '|---|---|---|---|---|']
M += ['| %s | %s | %s | %s | %s |' % (r['K'], r['src'], r['claim'].replace('|', '｜'), r['evidence'].replace('|', '｜'), r['verdict']) for r in rows]
M += ['', '## 検分票', '',
      '- 対象: 六票の事実の主張（読みの提案と総括は採否表で扱う）。',
      '- 段階: 結果の後。票を読んだ後に、票の主張を一つずつ現物に当てた。',
      '- 盲検の状態: 該当しない（事実の再現）。',
      '- 敵対的検分: 起草者に不利な主張（手続きの誤り・露出・報告の欠け）から先に当てた。再現しなかった主張も消していない。',
      '- 系統の内訳: コーディネータ（Claude 系）一名が当てた。',
      '- COI記録: 起草者は報告と器を書いた当人で、「器は正しい」と読む側に引かれる。当て方は器で固定した。',
      '- 本検分が確認していないこと: 票が挙げた読みの提案の当否（採否表で裁く）。G1 と G2 の数の主張のうち、報告の数をそのまま写したもの。C3 が確かめた SHA16 のうち、ここで当てなかったもの。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('rows', len(rows), '|', '・'.join('%s %d' % (v, sum(1 for r in rows if r['verdict'].startswith(v))) for v in ('再現した', '一部再現', '再現しない')))
for r in rows:
    print(r['K'], r['verdict'][:14], '|', r['evidence'][:150])
