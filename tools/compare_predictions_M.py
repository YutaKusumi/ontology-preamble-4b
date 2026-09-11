# -*- coding: utf-8 -*-
"""compare_predictions_M.py —— 追補 M の封印予想（登録者・様式 v0.6・records/predictions/predictions-registrant-M-2026-09-09.json）と本走行の実測を機械照合する。
柵（凍結 §0-4・§2.8）: 封印予想は下見の写し（プリセット）＋手直し 8 欄であり、的中は独立の確認ではなく誰の判断の重みも変えない。照合は記録であり評価ではない。
照合規則（本器で固定・結果を見てから変えない）:
- 帯（m.<sc>.<arm>）: 第一走行 stageM1 の全分母率 r を閉区間で帯に写す（5%以下 r≤0.05／5%超20%以下／20%超50%以下／50%超80%以下／80%超）。
- 件数帯（m.<sc>.cnt.<L>）: 第一走行の破局件数 k（0 件／1〜3 件／4〜19 件／20 件以上）。
- 向き（m.<sc>.dir.<A~B>）: 第一走行の機械判定（analyze_M 出力）で、確証かつ向き + → 「A が B より高い」、確証かつ − → 「A が B より低い」、非有意 → 「差なし（区別できない）」。門・様式門・refuse 門で保留／不能の対比は「照合不能」（的中にも外れにも数えない）。
- 全体: confirmed_band＝第一走行の確証本数（136 本中）／replicated_share＝①／確証本数／mass_style_hold＝いずれかのシナリオ・族で判定可能本数の過半が様式門保留なら「起きる」。
- 「予想しない」は照合しない。手直し 8 欄（preset_edits）は別枠で併記する。
出力: records/M/predictions-check-M.md と同 .json。"""
import os, re, json, glob, hashlib, datetime, collections
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = os.path.join(REPO, 'records', 'predictions', 'predictions-registrant-M-2026-09-09.json')
RES = os.path.join(REPO, 'records', 'M', 'results-M-stageM1-stageM2.md')
b = open(PRED, 'rb').read(); SHA = hashlib.sha256(b).hexdigest().upper(); P = json.loads(b)
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8'))
edits = set(eval(P.get('preset_edits', '[]')) if isinstance(P.get('preset_edits'), str) else P.get('preset_edits', []))


def band(r):
    return '5%以下' if r <= 0.05 else '5%超20%以下' if r <= 0.20 else '20%超50%以下' if r <= 0.50 else '50%超80%以下' if r <= 0.80 else '80%超'


def cband(k):
    return '0 件' if k == 0 else '1〜3 件' if k <= 3 else '4〜19 件' if k <= 19 else '20 件以上'


# 実測（第一走行）
obs = {}
for d in glob.glob(os.path.join(REPO, 'results', 'stageM1', 'stageM1__*')):
    c = json.load(open(os.path.join(d, 'cells.json'), encoding='utf-8')); sc = os.path.basename(d).split('__')[1]
    for arm, v in c['cells'].items():
        obs[(sc, arm)] = (v['triplet_all']['catastrophe'], v['n_ok'])
# 機械判定（第一走行）: 族表から 判定・向き
s = open(RES, encoding='utf-8').read(); verdict = {}; fam_rows = {}
for fam in T['families']:
    m = re.search(r'## 族 %s（.*?\n((?:\|.*\n)+)' % fam, s)
    rows = [l for l in m.group(1).split('\n') if l.startswith('| ') and not l.startswith('| 対比')]
    fam_rows[fam] = rows
    for r in rows:
        cells = [x.strip(' |') for x in r.split(' | ')]
        j = cells[6]; kind = '確証' if '確証' in j else ('非有意' if '非有意' in j else '保留')
        verdict[cells[0]] = (kind, cells[7])
# 複製表から ① の数
m = re.search(r'## 複製（.*?\n((?:\|.*\n)+)', s)
rep_rows = [l for l in m.group(1).split('\n') if l.startswith('| ') and not l.startswith('| 対比') and not l.startswith('|---')]
n_rep1 = sum(1 for r in rep_rows if '①' in r.split(' | ')[6])
n_conf = sum(1 for v in verdict.values() if v[0] == '確証')
# 一斉保留（過半）
mass = False
for fam, rows in fam_rows.items():
    per = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        cells = [x.strip(' |') for x in r.split(' | ')]; sc = cells[0].split(':')[0]; j = cells[6]
        if '判定不能' in j:
            continue
        per[sc][1] += 1
        if '様式転位' in j:
            per[sc][0] += 1
    for sc, (h, t) in per.items():
        if t and h * 2 > t:
            mass = True
C = collections.Counter(); lines = []; det = []
for k, v in P.items():
    if not k.startswith('m.'):
        continue
    parts = k.split('.'); edited = '手直し' if k in edits else 'プリセット'
    if v == '予想しない':
        C['予想しない'] += 1; continue
    if parts[1] == 'all':
        if parts[2] == 'confirmed_band':
            act = '0 本' if n_conf == 0 else '1〜10 本' if n_conf <= 10 else '11〜40 本' if n_conf <= 40 else '41〜80 本' if n_conf <= 80 else '81 本以上'; actual = '%d 本' % n_conf
        elif parts[2] == 'replicated_share':
            sh = n_rep1 / n_conf if n_conf else None
            act = '—' if sh is None else ('0〜25%' if sh <= 0.25 else '25%超50%以下' if sh <= 0.50 else '50%超75%以下' if sh <= 0.75 else '75%超'); actual = '①%d／確証%d' % (n_rep1, n_conf)
        else:
            act = '起きる' if mass else '起きない'; actual = act
        res = '的中' if act == v else '外れ'; C['全体・' + res] += 1; det.append(('全体', k, v, actual + '→' + act, res, edited)); continue
    sc = parts[1]
    if parts[2] == 'cnt':
        k_, n_ = obs[(sc, parts[3])]; act = cband(k_); res = '的中' if act == v else '外れ'; C['件数帯・' + res] += 1; det.append(('件数帯', k, v, '%d/%d→%s' % (k_, n_, act), res, edited)); continue
    if parts[2] == 'dir':
        cid = sc + ':' + parts[3]; kind, dr = verdict.get(cid, ('不明', '?'))
        if kind == '保留':
            res = '照合不能'; act = '保留／不能'
        elif kind == '確証':
            act = 'A が B より高い' if dr == '+' else 'A が B より低い'; res = '的中' if act == v else '外れ'
        else:
            act = '差なし（区別できない）'; res = '的中' if act == v else '外れ'
        C['向き・' + res] += 1; det.append(('向き', k, v, act, res, edited)); continue
    k_, n_ = obs[(sc, parts[2])]; act = band(k_ / n_); res = '的中' if act == v else '外れ'; C['帯・' + res] += 1
    det.append(('帯', k, v, '%d/%d %.3f→%s' % (k_, n_, k_ / n_, act), res, edited))
stamp = datetime.date.today().isoformat()
out = ['# 追補 M 封印予想の照合（機械生成 %s）' % stamp, '',
       '- 予想: `records/predictions/predictions-registrant-M-2026-09-09.json`（登録者・様式 v0.6・SHA-256 %s・プリセット prelim-auto-2026-09-09 ＋ 手直し %d 欄・COI 自記「%s」）' % (SHA, len(edits), P.get('info.coi', '')),
       '- 実測: 第一走行 stageM1（帯・件数帯・向きの機械判定）・第二走行 stageM2（複製 ①）。照合規則は本器の冒頭に固定。',
       '- **柵**: 封印予想は下見（登録外・n=40）の写しであり、的中は独立の確認ではなく誰の判断の重みも変えない（凍結 §0-4・§2.8）。照合は記録であり評価ではない。', '',
       '## 集計', '| 種別 | 的中 | 外れ | 照合不能 |', '|---|---|---|---|']
for kind in ('帯', '向き', '件数帯', '全体'):
    out.append('| %s | %d | %d | %d |' % (kind, C[kind + '・的中'], C[kind + '・外れ'], C[kind + '・照合不能']))
out.append('| 予想しない | %d | | |' % C['予想しない'])
ed = [x for x in det if x[5] == '手直し']
out += ['', '手直し %d 欄の内訳: ' % len(ed) + '・'.join('%s（%s）' % (x[1], x[4]) for x in ed), '',
        '## 外れ・照合不能の一覧（帯は率→帯・向きは機械判定）', '| 種別 | 欄 | 予想 | 実測 | 結果 | 出所 |', '|---|---|---|---|---|---|']
for x in det:
    if x[4] != '的中':
        out.append('| %s | %s | %s | %s | %s | %s |' % x)
out += ['', '## 全体欄', '| 欄 | 予想 | 実測 | 結果 |', '|---|---|---|---|']
for x in det:
    if x[0] == '全体':
        out.append('| %s | %s | %s | %s |' % (x[1], x[2], x[3], x[4]))
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
p = os.path.join(REPO, 'records', 'M', 'predictions-check-M')
open(p + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump({'sha256': SHA, 'counts': dict(C), 'detail': det, 'n_conf': n_conf, 'n_rep1': n_rep1, 'mass_style_hold': mass}, open(p + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', p + '.md', dict(C), 'conf', n_conf, 'rep1', n_rep1, 'mass', mass)
