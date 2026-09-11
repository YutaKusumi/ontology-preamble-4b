# -*- coding: utf-8 -*-
"""make_predictions_form_F.py —— 段階 F の予想様式 v0.7（HTML・単一ファイル・ブラウザ内で JSON と SHA-256 を生成・登録者とコーディネータの双方が封印）を `design/contrasts-F.json` から機械生成する。
v0.6（M）からの変更: 対象を 24 対比の向き（三値）・T／T2 腕 24 セルの帯・添え札の向き（24・四値）・T2 対 T の向き（12・記述）・確証本数の帯・複製割合の帯・一斉保留の三値・「上昇あり」の対比数の帯・COI 自記欄に組み替え。
U 腕 12 セルの帯は既測（M 第一走行）から自動入力（`make_predictions_preset_F.py`）。下見は置かない。SHA-256 の JS は V′ 様式 v0.5 から逐語で流用（M と同じ）。
"""
import os, json, re
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8')); MT = T['mention_tag']
V5 = open(os.path.join(REPO, 'records', 'predictions', 'predictions-form-Vprime-v0.5.html'), encoding='utf-8').read()
JS = re.search(r'<script>.*?</script>', V5, re.S).group(0)
JS = JS.replace("form:'predictions-form v0.5 (Vprime)',program:'ontology-preamble-4b/Vprime',contrasts:'draft7-2026-09-07'", "form:'predictions-form v0.7 (F)',program:'ontology-preamble-4b/F',contrasts:'%s'" % T['version']).replace('predictions-Vprime-registrant.json', 'predictions-F.json')
JS = JS.replace('for(const k of keys)sorted[k]=o[k];', 'for(const k of keys)sorted[k]=o[k];sorted.preset_applied=presetApplied?PRESET.preset:null;sorted.preset_rule=presetApplied?PRESET.rule:null;sorted.preset_note=presetApplied?PRESET.note:null;sorted.preset_edits=presetApplied?keys.filter(k=>PRESET.values[k]!==undefined&&o[k]!==PRESET.values[k]):null;sorted.preset_sources=presetApplied?PRESET.sources:null;')
assert 'preset_applied' in JS and "v0.7 (F)" in JS
BANDS = ['予想しない', '5%以下', '5%超20%以下', '20%超50%以下', '50%超80%以下', '80%超']; DIR3 = ['予想しない', 'A が B より高い', 'A が B より低い', '差なし（区別できない）']; TAG = ['予想しない'] + MT['labels']


def sel(k, opts):
    return "<select data-k='%s'>%s</select>" % (k, ''.join('<option>%s</option>' % o for o in opts))


META = T['metas']
H = ['<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>予想フォーム v0.7（段階 F・検査認識の付記・contrasts %s）</title>' % T['version'],
     '<style>body{font-family:sans-serif;max-width:1200px;margin:1em auto;padding:0 1em}table{border-collapse:collapse;font-size:12px}td,th{border:1px solid #999;padding:2px 4px}select{font-size:11px}.box{border:1px solid #ccc;padding:.5em;margin:.5em 0;background:#fafafa}.btn{margin:.5em .5em .5em 0}</style></head><body>',
     '<h1>予想フォーム v0.7——段階 F（Qwen3-4B-Instruct-2507・場面冒頭の検査認識の付記）</h1>',
     '<div class="box"><b>使い方</b>: 帯は第一走行の破局率（全分母・n=400・閉区間: 5%以下／5%超20%以下／20%超50%以下／50%超80%以下／80%超）。向きは確証対比ごとに三値（A が B より高い／低い／差なし）。添え札は (c2) の処置腕 対 U の四値（上昇あり／上昇なし／低下／復唱のみ）。T2 対 T は記述（向き三値）。分からない項目は「予想しない」のまま。登録者とコーディネータの双方が封印する（予想者欄で区別）。最後に「生成」で JSON と SHA-256 を出し、SHA-256 をチャットに貼付して封印する。的中・外れは誰の判断の重みも変えない（予想的中の非転用）。向きは正本 JSON のみが定め、封印予想を事後の向きの根拠に引かない。<br>',
     '<b>腕</b>: U＝付記なし（N＝前置きなし／Ncold／O-Ncold・V′・M と同一バイト）。T＝「%s」／T2＝「%s」を user 文の冒頭（前置きの前）に置く。T-X・T2-X の X は N・Ncold・O-Ncold。system 型は置かない。</div>' % (META['T'], META['T2']),
     '<h2>情報状態</h2><p>本プログラム結果の読了 %s　追補 V′ 結果報告の読了 %s　追補 M 結果報告の読了 %s　段階 F 凍結文書の読了 %s</p><p>COI（自由記述・望む方向を先に書く）<input data-k="info.coi" size="90" placeholder="例: 付記で下がってほしい／動かないでほしい／上昇なしが多くあってほしい など"></p>' % (sel('info.main_read', ['読了', '未読']), sel('info.vprime_read', ['読了', '未読']), sel('info.m_read', ['読了', '未読']), sel('info.f_read', ['読了', '未読']))]
for sc in T['scenarios']:
    H.append('<h2>%s</h2><h3>破局率の帯（第一走行・全分母・U 腕は既測から自動入力）</h3><table><tr><th>土台 \\ 付記</th><th>U（既測・自動）</th><th>T</th><th>T2</th></tr>' % sc)
    for b in T['bases']:
        H.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (b, sel('f.%s.%s' % (sc, b), BANDS), sel('f.%s.T-%s' % (sc, b), BANDS), sel('f.%s.T2-%s' % (sc, b), BANDS)))
    H.append('</table><h3>向き（確証対比・三値）と添え札（四値）</h3><table><tr><th>対比（A 対 B）</th><th>向き（破局率）</th><th>添え札（(c2) 言及）</th><th>重複</th></tr>')
    for c in T['families']['F']['contrasts']:
        if c['scenario'] == sc:
            H.append('<tr><td>%s 対 %s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c['A'], c['B'], sel('f.%s.dir.%s~%s' % (sc, c['A'], c['B']), DIR3), sel('f.%s.tag.%s~%s' % (sc, c['A'], c['B']), TAG), '重複（付記と場面文）' if c.get('duplicate') else ''))
    H.append('</table><h3>T2 対 T（記述・向き三値）</h3><table><tr><th>対比</th><th>向き</th></tr>')
    for c in T['descriptive_families']['F_desc_t2_vs_t']['contrasts']:
        if c['scenario'] == sc:
            H.append('<tr><td>%s 対 %s</td><td>%s</td></tr>' % (c['A'], c['B'], sel('f.%s.t2t.%s~%s' % (sc, c['A'], c['B']), DIR3)))
    H.append('</table>')
H.append('<h2>全体</h2><p>第一走行の確証本数（24 本中）の帯 %s　そのうち第二走行で複製される割合の帯 %s　様式門による一斉保留（いずれかの場面で判定可能の過半）%s　添え札「上昇あり」の対比数（24 中）の帯 %s</p>' % (sel('f.all.confirmed_band', ['予想しない', '0 本', '1〜3 本', '4〜8 本', '9〜16 本', '17〜24 本']), sel('f.all.replicated_share', ['予想しない', '0〜25%', '25%超50%以下', '50%超75%以下', '75%超']), sel('f.all.mass_style_hold', ['予想しない', '起きる', '起きない']), sel('f.all.up_tag_band', ['予想しない', '0 本', '1〜2 本', '3〜6 本', '7〜12 本', '13〜24 本'])))
H.append('<h2>自由記述</h2><textarea rows="4" data-k="free" style="width:100%"></textarea>')
H.append('<p><b>予想者</b> %s　<b>日付</b> <input data-k="date" size="12" placeholder="YYYY-MM-DD"></p>' % sel('who', ['登録者', 'コーディネータ']))
PRESET = json.load(open(os.path.join(REPO, 'records', 'predictions', 'preset-M1-F.json'), encoding='utf-8'))
H.append('<div class="box"><b>既測から自動入力</b>: U 腕 12 セルの帯を M 第一走行の実測（公開済み・同一バイトの U 腕）から写す（`tools/make_predictions_preset_F.py`・出所は生成 JSON の preset_sources に全項目記録）。T・T2・向き・添え札・T2 対 T・全体欄は自動入力しない（既測なし・下見は置かない）。自動入力の後に手で直した項目は preset_edits として JSON に残る。<br><button class="btn" onclick="preset()">既測から自動入力する（%d 項目）</button> <span id="preset_state">（未適用）</span></div>' % len(PRESET['values']))
H.append('<button class="btn" onclick="gen()">予想JSONを生成してハッシュを表示</button><button class="btn" onclick="dl()">JSONをダウンロード</button>')
H.append('<script>const PRESET=%s;let presetApplied=false;function preset(){let n=0;for(const k in PRESET.values){const e=document.querySelector("[data-k=\'"+k+"\']");if(e){e.value=PRESET.values[k];n++;}}presetApplied=true;document.getElementById("preset_state").textContent="適用済み（"+n+" 項目・"+PRESET.preset+"）";}</script>' % json.dumps({'preset': PRESET['preset'], 'values': PRESET['values'], 'sources': PRESET['sources'], 'rule': PRESET['rule'], 'note': PRESET['note']}, ensure_ascii=False))
H.append('<p>SHA-256: <span id="hash">（未生成）</span></p><pre id="out" style="white-space:pre-wrap;font-size:11px"></pre>')
H.append('<p style="font-size:11px">本様式のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。</p>')
H.append(JS + '</body></html>')
p = os.path.join(REPO, 'records', 'predictions', 'predictions-form-F-v0.7.html')
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(H) + '\n')
n_sel = sum(h.count('<select') for h in H); print('written', p, 'selects', n_sel)
