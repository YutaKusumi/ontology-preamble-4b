# -*- coding: utf-8 -*-
"""make_predictions_preset_F.py —— 予想様式 v0.7 の「U 腕を既測から自動入力」プリセットを `design/contrasts-F.json`（base_M1＝追補 M 第一走行の U 腕の実測・公開済み）から機械生成する。
自動入力するのは U 腕 12 セル（N・Ncold・O-Ncold × 4 場面）の破局率の帯だけ。T・T2 腕・向き・添え札・T2 対 T・全体欄には既測が無く自動入力しない（言及率には既測が無い・凍結 §2.8）。
出力: records/predictions/preset-M1-F.json（出所は各項目に記録し様式の JSON にも埋め込む）。的中・外れは誰の判断の重みも変えない。"""
import os, json
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8'))
BANDS = ['5%以下', '5%超20%以下', '20%超50%以下', '50%超80%以下', '80%超']


def band(r):
    return BANDS[0] if r <= 0.05 else BANDS[1] if r <= 0.20 else BANDS[2] if r <= 0.50 else BANDS[3] if r <= 0.80 else BANDS[4]


values, sources = {}, {}
for sc in T['scenarios']:
    for b in T['bases']:
        x = T['scenarios'][sc]['base_M1'][b]; r = x['catastrophe'] / x['n_ok']
        values['f.%s.%s' % (sc, b)] = band(r); sources['f.%s.%s' % (sc, b)] = 'M 第一走行 stageM1/%s %d/%d（公開済み・同一バイトの U 腕）' % (b, x['catastrophe'], x['n_ok'])
out = {'preset': 'M1-U-auto-2026-09-11', 'rule': 'U 腕 12 セルの帯＝M 第一走行の実測破局率をそのまま帯に写す（5%以下／5%超20%以下／20%超50%以下／50%超80%以下／80%超）。T・T2 腕・向き・添え札・T2 対 T・全体欄は自動入力しない（既測なし）。',
       'note': '既測の U 腕は本段の対照と同一バイト。的中・外れは誰の判断の重みも変えない。自動入力の後に手で直した項目は preset_edits として JSON に残る。', 'values': values, 'sources': sources}
p = os.path.join(REPO, 'records', 'predictions', 'preset-M1-F.json'); os.makedirs(os.path.dirname(p), exist_ok=True)
json.dump(out, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1); print('written', p, 'values', len(values))
