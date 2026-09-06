# -*- coding: utf-8 -*-
"""compare_predictions.py —— 封印済み予想（第2版・SHA EA169F11…）と本走行の実測を機械照合する。
柵: 予想の的中は O の妥当性や前置きの推奨の根拠に転用しない（凍結 §13）。照合は記録であり評価ではない。
帯: 5%以下／5%超20%以下／20%超50%以下／50%超80%以下／80%超（閉区間・全分母の率）。S3 は拠出量帯（0–2／3–5／6–8／9–12）。段0 は最大差（pt）帯。
"""
import os, json, glob, hashlib, datetime
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = os.path.join(REPO, 'records', 'predictions', 'predictions-registrant-2026-09-05-v2.json')
b = open(PRED, 'rb').read(); SHA = hashlib.sha256(b).hexdigest().upper(); P = json.loads(b)


def band(r):
    if r is None:
        return '—'
    return '5%以下' if r <= 0.05 else '5%超20%以下' if r <= 0.20 else '20%超50%以下' if r <= 0.50 else '50%超80%以下' if r <= 0.80 else '80%超'


def band_amt(x):
    return '0–2' if x <= 2 else '3–5' if x <= 5 else '6–8' if x <= 8 else '9–12'


def band_pt(x):
    return '0–3pt' if x <= 3 else '4–8pt' if x <= 8 else '9–15pt' if x <= 15 else '16pt超'


def cells(tag, sub):
    fs = [f for f in glob.glob(os.path.join(REPO, 'results', tag, '*', 'cells.json')) if sub in os.path.basename(os.path.dirname(f))]
    return json.load(open(fs[0], encoding='utf-8'))['cells'] if fs else None


rows = []


def add(section, key, actual_desc, actual_band):
    pred = P.get(key, '（未記入）'); hit = (pred == actual_band) if actual_band != '—' else None
    rows.append((section, key, pred, actual_desc, actual_band, '一致' if hit else ('不一致' if hit is False else '—')))


# 段I
ARMS = ['N', 'Onull', 'O', 'Osec', 'Lneg', 'Nk', 'Nai', 'Nlib']
for sc in ('S1', 'S4', 'SK', 'N1', 'N2'):
    c = cells('stage1', '__%s__' % sc)
    for a in ARMS:
        x = c[a]; r = x['catastrophe_rate_all']; add('段I %s' % sc, 's1.%s.%s' % (sc, a), '%d/%d=%.3f' % (x['catastrophe'], x['n_ok'], r), band(r))
    dirn = 'O＜Onull（Oが低い）' if c['O']['catastrophe_rate_all'] < c['Onull']['catastrophe_rate_all'] else ('O＞Onull（Oが高い）' if c['O']['catastrophe_rate_all'] > c['Onull']['catastrophe_rate_all'] else '差なし')
    add('段I %s' % sc, 's1.%s.dir' % sc, dirn, dirn)
c = cells('stage1', '__S2__')
for a in ARMS:
    r = c[a]['s2_direct_rate']; add('段I S2 direct率', 's1b.S2 direct率.%s' % a, '%.2f' % r, band(r))
c = cells('stage1', '__S3__')
for a in ARMS:
    m = c[a]['s3_amount_mean']; add('段I S3 拠出量', 's1b.S3 拠出量.%s' % a, '%.2f' % m, band_amt(m))
# 段II
for sysname, label in (('none', '素'), ('neutral', '中立'), ('a2', 'A2'), ('a2prime', 'A2′'), ('lneg-sys', 'Lneg-sys')):
    c = cells('stage2', '__%s__' % sysname)
    for a in ('N', 'O'):
        x = c[a]; r = x['catastrophe_rate_all']; add('段II %s' % label, 's2.%s.%s' % (label, a), '%d/%d=%.3f' % (x['catastrophe'], x['n_ok'], r), band(r))
    dirn = 'O＜Onull（Oが低い）' if c['O']['catastrophe_rate_all'] < c['Onull']['catastrophe_rate_all'] else 'O＞Onull（Oが高い）'
    add('段II %s' % label, 's2.%s.dir' % label, dirn, dirn)
    ref = sum(x['refuse'] for x in c.values()) / sum(x['n_ok'] for x in c.values())
    add('段II %s' % label, 's2.%s.refuse' % label, '全腕 refuse 率 %.2f' % ref, 'refuseが過半' if ref > 0.5 else 'refuseは少数')
# 段VI
c = cells('stage6', '')
for key, arm in (('O1', 'Odose1'), ('Oh', 'Odosehalf'), ('L1', 'Lnegdose1'), ('Lh', 'Lnegdosehalf')):
    x = c[arm]; r = x['catastrophe_rate_all']; add('段VI', 's6.%s' % key, '%d/%d=%.3f' % (x['catastrophe'], x['n_ok'], r), band(r))
o1, oh, of = c['Odose1']['catastrophe_rate_all'], c['Odosehalf']['catastrophe_rate_all'], c['O']['catastrophe_rate_all']
shape = '単調（長いほど効く）' if o1 >= oh >= of else '非単調'
add('段VI', 's6.shape', 'O 一文 %.3f／半分 %.3f／全文 %.3f' % (o1, oh, of), shape)
# 段V
c = cells('stage5', '')
for key, arm in (('N（対照）', 'N'), ('Nstr（戦略家）', 'Nstr'), ('Ncold（冷徹・弱）', 'Ncold'), ('NcoldS（損得のみ・中）', 'NcoldS'), ('Ncold3（容赦なく勝敗のみ・強）', 'Ncold3'), ('Nwin（勝利至上）', 'Nwin'),
                 ('O（対照）', 'O'), ('Onull（対照）', 'Onull'), ('O-sec（対照）', 'Osec'), ('O＋Ncold', 'O-Ncold'), ('Ncold＋O', 'Ncold-O'), ('Onull＋Ncold', 'Onull-Ncold'), ('O-sec＋Ncold', 'Osec-Ncold'), ('G-hard（直接指示・記述専用）', 'G-hard')):
    x = c[arm]; r = x['catastrophe_rate_all']; add('段V', 's5.%s' % key, '%d/%d=%.3f' % (x['catastrophe'], x['n_ok'], r), band(r))
# 段III
cp = cells('stage3', 'pressure'); cn = cells('stage3', 'neutral')
for key, arm in (('N', 'N'), ('Onull', 'Onull'), ('O', 'O'), ('O-sec', 'Osec'), ('Lneg', 'Lneg')):
    for cond, c in (('pressure', cp), ('neutral', cn)):
        x = c[arm]; r = x['transition_rate']; add('段III', 's3.%s.%s' % (key, cond), '転向 %d/%d=%s' % (x['transition'], x['denominator'], r), band(r) if r is not None else '—')
    rp, rn = cp[arm]['transition_rate'], cn[arm]['transition_rate']
    d = '—' if (rp is None or rn is None) else ('圧力の方が高い' if rp > rn else '中立の方が高い' if rn > rp else '差はない')
    add('段III', 's3.%s.dir' % key, d, d)
# 段0（揃った回数で暫定）
sp = {'N': [], 'Onull': [], 'O': []}
for r_ in range(1, 7):
    c = cells('stage0-r%d' % r_, '')
    if c:
        for a in sp:
            sp[a].append(c[a]['catastrophe_rate_all'])
for a in sp:
    if sp[a]:
        d = 100 * (max(sp[a]) - min(sp[a])); add('段0（%d回・暫定）' % len(sp[a]), 's0.%s_spread' % a, '%.1fpt' % d, band_pt(d))

out = ['# 封印予想（第2版・SHA-256 %s…）と実測の照合 —— %s' % (SHA[:16], datetime.date.today().isoformat()), '',
       '柵（凍結 §13）: 予想の的中を O の妥当性・前置きの推奨・登録者の判断力の証拠に転用しない。本表は記録であり評価ではない。確信度と情報状態（COI「O が効いてほしい」・下見「読んだ」）は予想 JSON のとおり。', '',
       '| 段 | 鍵 | 予想 | 実測 | 実測の帯 | 照合 |', '|---|---|---|---|---|---|']
for r in rows:
    out.append('| %s | %s | %s | %s | %s | %s |' % r)
n = sum(1 for r in rows if r[5] in ('一致', '不一致')); h = sum(1 for r in rows if r[5] == '一致')
out.append(''); out.append('照合可能 %d 項目のうち一致 %d（%.0f%%）。不一致の内訳は本表を読む（帯の境界近傍と方向の逆転を分けて読むこと）。' % (n, h, 100 * h / n if n else 0))
os.makedirs(os.path.join(REPO, 'records', 'results'), exist_ok=True)
p = os.path.join(REPO, 'records', 'results', 'prediction-comparison-%s.md' % datetime.date.today().isoformat())
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n'); print('written', p, n, h)
