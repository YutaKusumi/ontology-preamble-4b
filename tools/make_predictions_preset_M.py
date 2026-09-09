# -*- coding: utf-8 -*-
"""make_predictions_preset_M.py —— 登録者予想様式 v0.6 の「下見から自動入力」プリセットを、下見（prelim・登録外・n=40）の cells.json から機械生成する。
登録者の申告「私の予想は下見の結果をそのまま反映したもの」を、手入力なしで様式に載せるための器。値は下見の破局率をそのまま帯に写し、向きは同じ下見の率差から機械的に決める
（|差| が 10 pt〔4/40〕以上なら高い／低い・未満なら差なし・片方でも下見に無ければ「予想しない」）。下見に対応する腕が無い項目は「予想しない」のまま。
参照腕のうち下見に無い Onull-Ncold・N・sysN は V′ 本走行の実測を用いる（出所を明記）。出所（走行タグ・腕・k/n）はすべて JSON に記録し、様式の JSON にも埋め込む。
下見の対応（M の腕 → 下見の腕）は本ファイルの MAP が正本。異なる走行の腕を並べた対比は走行差を含む（下見メモの注意そのまま）。
出力: records/predictions/preset-prelim-M.json
"""
import os, json, glob
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8')); SC = list(T['scenarios'])
BANDS = ['5%以下', '5%超20%以下', '20%超50%以下', '50%超80%以下', '80%超']


def band(r):
    return BANDS[0] if r <= 0.05 else BANDS[1] if r <= 0.20 else BANDS[2] if r <= 0.50 else BANDS[3] if r <= 0.80 else BANDS[4]


def cnt_band(k40):
    return '0 件' if k40 == 0 else '4〜19 件' if k40 == 1 else '20 件以上'


# M の腕 → (下見タグ, 下見の腕)。None は下見に無い。
MAP = {'Nk-Ncold': ('prelim-neutral', 'Nk-Ncold'), 'O-Ncold': ('prelim-neutral', 'O-Ncold'), 'Ncold': ('prelim-namuamidabutsu', 'Ncold'), 'sysNone-Ncold': ('prelim-namuamidabutsu', 'Ncold'),
       'KanF1TS-Ncold': ('prelim-neutral', 'L1KanS-Ncold'), 'KanF1TK-Ncold': ('prelim-neutral', 'L1KanM-Ncold'), 'KanF1PS-Ncold': ('prelim-neutral', 'L1KanPR-Ncold'), 'KanF1PK-Ncold': ('prelim-neutral', 'L1KanPK-Ncold'), 'KanF1NJ-Ncold': ('prelim-neutral', 'L1KanNJ-Ncold'),
       'sysLAmi': ('prelim-OAmidaLong-sys', 'Ncold'), 'sysLKan': ('prelim-OKanzeonLong-sys', 'Ncold')}
for X in ('Dai', 'Ami', 'Mir'):
    MAP['%sF1T0-Ncold' % X] = ('prelim-oneline', 'L1%s-Ncold' % X); MAP['%sF1TK-Ncold' % X] = ('prelim-oneline2', 'L1%sM-Ncold' % X); MAP['%sF1TS-Ncold' % X] = ('prelim-oneline3', 'L1%sS-Ncold' % X)
for X in ('Dai', 'Ami', 'Kan', 'Mir'):
    MAP['%sF2T0-Ncold' % X] = ('prelim-oneline', 'L2%s-Ncold' % X); MAP['%sF3T0-Ncold' % X] = ('prelim-oneline', 'L3%s-Ncold' % X)
VP = {'Onull-Ncold': 'Onull-Ncold', 'N': 'N', 'sysN': 'N'}   # V′ 実測を用いる参照腕
cells = {}
for f in glob.glob(os.path.join(REPO, 'results', 'prelim-*', '*', 'cells.json')):
    d = json.load(open(f, encoding='utf-8')); cells.setdefault(os.path.basename(os.path.dirname(os.path.dirname(f))), {}).setdefault(d['manifest']['scenario'], {}).update(d['cells'])
values, sources, rates = {}, {}, {}
for sc in SC:
    for arm, (tag, pa) in MAP.items():
        x = cells.get(tag, {}).get(sc, {}).get(pa)
        if not x or not x['n_ok']:
            continue
        r = x['catastrophe'] / x['n_ok']; rates[(sc, arm)] = r; values['m.%s.%s' % (sc, arm)] = band(r); sources['m.%s.%s' % (sc, arm)] = '%s/%s %d/%d' % (tag, pa, x['catastrophe'], x['n_ok'])
    for arm, va in VP.items():
        k = T['scenarios'][sc]['vprime_stageVp'][va]; r = k / 400; rates[(sc, arm)] = r; values['m.%s.%s' % (sc, arm)] = band(r); sources['m.%s.%s' % (sc, arm)] = 'V′ stageVp/%s %d/400' % (va, k)
    for arm in ('sysLAmi', 'sysLKan'):
        x = cells.get(MAP[arm][0], {}).get(sc, {}).get('Ncold')
        if x:
            values['m.%s.cnt.%s' % (sc, arm)] = cnt_band(x['catastrophe']); sources['m.%s.cnt.%s' % (sc, arm)] = '%s/Ncold %d/%d（×10 を件数帯に写す）' % (MAP[arm][0], x['catastrophe'], x['n_ok'])
    for F in T['families'].values():
        for c in F['contrasts']:
            if c['scenario'] != sc:
                continue
            ra, rb = rates.get((sc, c['A'])), rates.get((sc, c['B']))
            if ra is None or rb is None:
                continue
            d = ra - rb; v = 'A が B より高い' if d >= 0.10 else 'A が B より低い' if d <= -0.10 else '差なし（区別できない）'
            k = 'm.%s.dir.%s~%s' % (sc, c['A'], c['B']); values[k] = v; sources[k] = '%s − %s = %+.3f（下見・走行差を含む）' % (sources['m.%s.%s' % (sc, c['A'])], sources['m.%s.%s' % (sc, c['B'])], d)
out = {'preset': 'prelim-auto-2026-09-09', 'rule': '帯＝下見の破局率をそのまま写す（5%以下／5%超20%以下／20%超50%以下／50%超80%以下／80%超）。向き＝同じ下見の率差 |Δ|≥10pt で高い／低い・未満は差なし・片方でも無ければ予想しない。件数帯＝下見の k/40 を ×10 で写す。参照腕の Onull-Ncold・N・sysN は V′ 実測。下見に無い腕（MS・MK・NJ2・F4・PS/PK の Kan 以外・-PS/-MS/-T0/-noC・sysO・sysOnull）は予想しない。',
       'note': '下見は登録外・n=40・証拠に数えない（設計 §0-4）。異なる走行の腕を並べた向きは走行差を含む。KanF1PS の下見は om 表記時代の無意味列（oh āvosik llāmā）であり本追補の PS（oṃ āhovis klālā）とは別文字列。的中・外れは誰の判断の重みも変えない。',
       'values': values, 'sources': sources, 'map': {k: list(v) for k, v in MAP.items()}, 'vprime_refs': VP}
p = os.path.join(REPO, 'records', 'predictions', 'preset-prelim-M.json')
json.dump(out, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('written', p, 'values', len(values), 'bands', sum(1 for k in values if '.dir.' not in k and '.cnt.' not in k), 'dirs', sum(1 for k in values if '.dir.' in k), 'cnt', sum(1 for k in values if '.cnt.' in k))
