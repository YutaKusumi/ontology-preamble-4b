# -*- coding: utf-8 -*-
"""compare_predictions_F.py —— 段階 F の封印予想（様式 v0.7・登録者とコーディネータの各 JSON）と本走行の機械判定（analyze_F の JSON）を照合する。
柵（凍結 §0・§2.8）: 的中は独立の確認ではなく誰の判断の重みも変えない。照合は記録であり評価ではない。U 腕の帯は既測の自動入力（照合するが的中に数えず別枠）。
照合規則（本器で固定・結果を見てから変えない）:
- 帯（f.<sc>.<arm>）: 第一走行の全分母率 r を閉区間で帯に写す。U 腕（自動入力）は別枠「既測の写し」。
- 向き（f.<sc>.dir.<A~B>）: 第一走行の機械判定で、確証かつ + → 「A が B より高い」、確証かつ − → 「A が B より低い」、非有意 → 「差なし（区別できない）」。門・撤退降格・保留は「照合不能」。
- 添え札（f.<sc>.tag.<A~B>）: 第一走行の添え札の四値（門・降格の対比も添え札は付くので照合する）。
- T2 対 T（f.<sc>.t2t.<A~B>）: 記述族の差 |Δ|≥5pt を向き・未満を差なしと写す（記述・検定なし・照合のみ）。
- 全体: confirmed_band＝第一走行の確証本数（24 本中）／replicated_share＝①／確証本数／mass_style_hold＝いずれかの場面で一斉保留／up_tag_band＝判定された対比のうち「上昇あり」の本数。
- 「予想しない」は照合しない。手直し欄（preset_edits）は別枠で併記する。
用法: python tools/compare_predictions_F.py --pred records/predictions/predictions-<who>-F-<date>.json --results records/F/results-F-stageF1-stageF2.json
出力: records/F/predictions-check-F-<who>.md と同 .json。"""
import os, json, hashlib, datetime, collections, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--pred', required=True); ap.add_argument('--results', required=True); ap.add_argument('--who', default=None); a = ap.parse_args()
b = open(a.pred, 'rb').read(); SHA = hashlib.sha256(b).hexdigest().upper(); P = json.loads(b); R = json.load(open(a.results, encoding='utf-8'))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8')); who = a.who or P.get('who', '不明')
edits = set(P.get('preset_edits') or []) if not isinstance(P.get('preset_edits'), str) else set(json.loads(P['preset_edits']))


def band(r):
    return '5%以下' if r <= 0.05 else '5%超20%以下' if r <= 0.20 else '20%超50%以下' if r <= 0.50 else '50%超80%以下' if r <= 0.80 else '80%超'


rate = {}
for lab, v in R['first'].items():
    rate[(v['scenario'], v['A'])] = (v['a'], v['na']); rate[(v['scenario'], v['B'])] = (v['b'], v['nb'])
n_conf = sum(1 for v in R['first'].values() if v['status'] == 'confirmed'); n_rep1 = sum(1 for v in R.get('replication', {}).values() if v['label'].startswith('①'))
mass = any(v['mass'] for v in R['mass_hold'].values()); k_up = R['falsification']['k_up']
C = collections.Counter(); det = []
for k, v in P.items():
    if not k.startswith('f.'):
        continue
    parts = k.split('.'); edited = '手直し' if k in edits else ('自動入力' if k in (P.get('preset_sources') or {}) else '手入力')
    if v == '予想しない':
        C['予想しない'] += 1; continue
    if parts[1] == 'all':
        if parts[2] == 'confirmed_band':
            act = '0 本' if n_conf == 0 else '1〜3 本' if n_conf <= 3 else '4〜8 本' if n_conf <= 8 else '9〜16 本' if n_conf <= 16 else '17〜24 本'; actual = '%d 本' % n_conf
        elif parts[2] == 'replicated_share':
            sh = n_rep1 / n_conf if n_conf else None; act = '—' if sh is None else ('0〜25%' if sh <= 0.25 else '25%超50%以下' if sh <= 0.50 else '50%超75%以下' if sh <= 0.75 else '75%超'); actual = '①%d／確証%d' % (n_rep1, n_conf)
        elif parts[2] == 'mass_style_hold':
            act = '起きる' if mass else '起きない'; actual = act
        else:
            act = '0 本' if k_up == 0 else '1〜2 本' if k_up <= 2 else '3〜6 本' if k_up <= 6 else '7〜12 本' if k_up <= 12 else '13〜24 本'; actual = '%d 本' % k_up
        res = '的中' if act == v else '外れ'; C['全体・' + res] += 1; det.append(('全体', k, v, actual + '→' + act, res, edited)); continue
    sc = parts[1]
    if parts[2] == 'dir':
        cid = sc + ':' + parts[3]; f = R['first'].get(cid)
        if not f or f['status'] not in ('confirmed', 'ns'):
            res = '照合不能'; act = (f or {}).get('status', '不明')
        elif f['status'] == 'confirmed':
            act = 'A が B より高い' if f['sign'] > 0 else 'A が B より低い'; res = '的中' if act == v else '外れ'
        else:
            act = '差なし（区別できない）'; res = '的中' if act == v else '外れ'
        C['向き・' + res] += 1; det.append(('向き', k, v, act, res, edited)); continue
    if parts[2] == 'tag':
        cid = sc + ':' + parts[3]; f = R['first'].get(cid); act = ((f or {}).get('tag') or {}).get('label', '—')
        res = '照合不能' if act == '—' else ('的中' if act == v else '外れ'); C['添え札・' + res] += 1; det.append(('添え札', k, v, act, res, edited)); continue
    if parts[2] == 't2t':
        A, B = parts[3].split('~'); ra = rate.get((sc, A)); rb = rate.get((sc, B))
        if not ra or not rb:
            res = '照合不能'; act = '—'
        else:
            d = ra[0] / ra[1] - rb[0] / rb[1]; act = 'A が B より高い' if d >= 0.05 else 'A が B より低い' if d <= -0.05 else '差なし（区別できない）'; res = '的中' if act == v else '外れ'
        C['T2対T（記述）・' + res] += 1; det.append(('T2対T（記述）', k, v, act, res, edited)); continue
    arm = parts[2]; x = rate.get((sc, arm))
    if not x:
        C['帯・照合不能'] += 1; det.append(('帯', k, v, '—', '照合不能', edited)); continue
    act = band(x[0] / x[1]); res = '的中' if act == v else '外れ'; kind = '帯（U・既測の写し）' if arm in T['bases'] else '帯'
    C[kind + '・' + res] += 1; det.append((kind, k, v, '%d/%d %.3f→%s' % (x[0], x[1], x[0] / x[1], act), res, edited))
stamp = datetime.date.today().isoformat()
out = ['# 段階 F 封印予想の照合（%s・機械生成 %s）' % (who, stamp), '', '- 予想: `%s`（SHA-256 %s・プリセット %s・手直し %d 欄・COI 自記「%s」）' % (os.path.relpath(a.pred, REPO).replace('\\', '/'), SHA, P.get('preset_applied'), len(edits), P.get('info.coi', '')),
       '- 実測: `%s`（第一走行の機械判定・第二走行の複製 ①）。照合規則は本器の冒頭に固定。' % os.path.relpath(a.results, REPO).replace('\\', '/'),
       '- **柵**: 的中は独立の確認ではなく誰の判断の重みも変えない。U 腕の帯は既測の自動入力であり別枠。照合は記録であり評価ではない。', '', '## 集計', '| 種別 | 的中 | 外れ | 照合不能 |', '|---|---|---|---|']
for kind in ('帯', '帯（U・既測の写し）', '向き', '添え札', 'T2対T（記述）', '全体'):
    out.append('| %s | %d | %d | %d |' % (kind, C[kind + '・的中'], C[kind + '・外れ'], C[kind + '・照合不能']))
out.append('| 予想しない | %d | | |' % C['予想しない'])
out += ['', '## 外れ・照合不能の一覧', '| 種別 | 欄 | 予想 | 実測 | 結果 | 入力 |', '|---|---|---|---|---|---|'] + ['| %s | %s | %s | %s | %s | %s |' % x for x in det if x[4] != '的中']
out += ['', '## 全体欄', '| 欄 | 予想 | 実測 | 結果 |', '|---|---|---|---|'] + ['| %s | %s | %s | %s |' % (x[1], x[2], x[3], x[4]) for x in det if x[0] == '全体']
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
p = os.path.join(REPO, 'records', 'F', 'predictions-check-F-%s' % who); os.makedirs(os.path.dirname(p), exist_ok=True)
open(p + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump({'who': who, 'sha256': SHA, 'counts': dict(C), 'detail': det, 'n_conf': n_conf, 'n_rep1': n_rep1, 'mass_style_hold': mass, 'k_up': k_up}, open(p + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', p + '.md', dict(C))
