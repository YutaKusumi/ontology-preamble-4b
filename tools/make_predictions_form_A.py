# -*- coding: utf-8 -*-
"""make_predictions_form_A.py v1 —— 段階 A の予想様式 v0.8（HTML・単一ファイル・ブラウザの中で JSON と SHA-256 を生成・登録者とコーディネータの双方が封印）を、
正本 `design/contrasts-A.json` の `predictions`（登録者裁定 D47・2026-09-15）から機械生成する。
欄: 確証の対比ごとの向き・床持続のセルの 0/1・確証の本数の帯・測れた効果種の数の帯（ここまでが予想の欄）と、情報状態・COI・自由記述・予想者・日付。自動入力は置かない。
SHA-256 の JS は V′ 様式 v0.5（`predictions.js_source`）から逐語で流用し、様式の名・プログラム・正本の版・保存の名の四つだけを置き換える（段階 F・M と同じ流用）。
用法: python tools/make_predictions_form_A.py [--force]（出力は正本 `predictions.form`・既存は --force が無ければ上書きしない）
柵: 本様式のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, html, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
FORM_NAME, PROGRAM, DL_NAME = 'predictions-form v0.8 (A)', 'ontology-preamble-4b/A', 'predictions-A.json'
V5_META = "form:'predictions-form v0.5 (Vprime)',program:'ontology-preamble-4b/Vprime',contrasts:'draft7-2026-09-07'"
V5_DL = 'predictions-Vprime-registrant.json'
FENCE = '本様式のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
esc = lambda s: html.escape(str(s), quote=True)


def js_block(T, P):
    src = open(os.path.join(REPO, P['js_source']), encoding='utf-8').read()
    js = re.search(r'<script>.*?</script>', src, re.S).group(0)
    assert js.count(V5_META) == 1 and js.count(V5_DL) == 1, 'V′ 様式 v0.5 の JS の置き換える文字列が一つずつでない'
    return js.replace(V5_META, "form:'%s',program:'%s',contrasts:'%s'" % (FORM_NAME, PROGRAM, T['version'])).replace(V5_DL, DL_NAME)


def sel(key, opts):
    return "<select data-k='%s'>%s</select>" % (esc(key), ''.join('<option>%s</option>' % esc(o) for o in opts))


def build(T):
    P = T['predictions']; F = P['fields']; CON = T['families']['A_slope']['contrasts']; FD = T['descriptive_families']['A_desc_floor']
    text_of = lambda k: next(x['text'] for x in F['text'] if x['key'] == k)
    CR = P['compare_rules']; n = {'向き': 0, '床持続': 0, '全体': 0, '情報状態': 0, '予想者': 0}
    H = ['<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>予想フォーム v0.8（段階 A・規模軸・正本 %s）</title>' % esc(T['version']),
         '<style>body{font-family:sans-serif;max-width:1200px;margin:1em auto;padding:0 1em}table{border-collapse:collapse;font-size:12px}td,th{border:1px solid #999;padding:2px 4px}select{font-size:11px}.box{border:1px solid #ccc;padding:.5em;margin:.5em 0;background:#fafafa}.btn{margin:.5em .5em .5em 0}</style></head><body>',
         '<h1>予想フォーム v0.8——段階 A（Qwen3 稠密系列の規模軸・枠組みへの感受性）</h1>',
         '<div class="box"><b>使い方</b>: 分からない欄は「%s」のまま残す。自動入力は置かない（%s）。予想者の欄で登録者とコーディネータを区別する。最後に「生成」で JSON と SHA-256 を出し、SHA-256 をチャットに貼り、JSON を保存して添付する。<br>'
         '<b>向き</b>（確証の対比 %d 本）: 機種の規模が大きいほど、A の破局率が B に比べて上がる側へ動くか・下がる側へ動くか・区別できないかを選ぶ。<br>'
         '<b>床持続</b>（%s × 場面・%d セル）: 全規模で破局率の上限（片側 %s）が censor.low（%s）未満になるかを選ぶ。<br>'
         '<b>全体</b>: %s の帯と、%s の帯。<br>'
         '<b>照合の規則</b>（照合の器に固定・結果を見てから変えない）: %s／%s／%s／%s。<br>'
         '<b>封印の順</b>: %s。%s。<br>'
         '<b>柵</b>: %s。</div>' % (esc(P['not_predicted']), esc(P['preset']), len(CON), esc('・'.join(FD['arms'])), len(FD['cells']), esc(FD['cp_level']), esc(T['censor']['low']),
                                  esc(F['confirmed_band']['what']), esc(F['measurable_band']['what']), esc(CR['direction']), esc(CR['floor']), esc(CR['confirmed_band']), esc(CR['measurable_band']),
                                  esc(P['order']), esc(P['independence']), esc(P['fence']))]
    H.append('<h2>情報状態（予想の欄に数えない）</h2><table><tr><th>記録</th><th>読んだか</th></tr>')
    for it in F['info']['items']:
        H.append('<tr><td>%s</td><td>%s</td></tr>' % (esc(it['text']), sel(it['key'], F['info']['options']))); n['情報状態'] += 1
    H.append('</table><p>%s <input data-k="info.coi" size="90" placeholder="例: 傾向が立ってほしい／床に留まってほしい など"></p>' % esc(text_of('info.coi')))
    H.append('<h2>向き（確証の対比ごと・%d 本）</h2>' % len(CON))
    for sc in T['scenarios']:
        H.append('<h3>場面 %s</h3><table><tr><th>対比（A 対 B）</th><th>効果種</th><th>向き</th></tr>' % esc(sc))
        for c in CON:
            if c['scenario'] == sc:
                H.append('<tr><td>%s 対 %s</td><td>%s</td><td>%s</td></tr>' % (esc(c['A']), esc(c['B']), esc(c['effect']), sel(F['direction']['key_prefix'] + c['id'], F['direction']['options']))); n['向き'] += 1
        H.append('</table>')
    cells = {(c['scenario'], c['arm']): c for c in FD['cells']}
    H.append('<h2>床持続（%s × 場面・0/1）</h2><table><tr><th>場面 \\ 腕</th>%s</tr>' % (esc('・'.join(FD['arms'])), ''.join('<th>%s</th>' % esc(x) for x in FD['arms'])))
    for sc in T['scenarios']:
        row = []
        for arm in FD['arms']:
            row.append('<td>%s</td>' % sel(F['floor']['key_prefix'] + cells[(sc, arm)]['id'], F['floor']['options'])); n['床持続'] += 1
        H.append('<tr><td>%s</td>%s</tr>' % (esc(sc), ''.join(row)))
    H.append('</table>')
    H.append('<h2>全体</h2><p>%s（%d 本中）の帯 %s　%s（%d 種中）の帯 %s</p>' % (esc(F['confirmed_band']['what']), len(CON), sel(F['confirmed_band']['key'], F['confirmed_band']['options']),
                                                                      esc(F['measurable_band']['what']), T['families']['A_slope']['effect_types'], sel(F['measurable_band']['key'], F['measurable_band']['options'])))
    n['全体'] += 2
    H.append('<h2>%s</h2><textarea rows="4" data-k="free" style="width:100%%"></textarea>' % esc(text_of('free')))
    H.append('<p><b>予想者</b> %s　<b>%s</b> <input data-k="date" size="12" placeholder="YYYY-MM-DD"></p>' % (sel(F['who']['key'], F['who']['options']), esc(text_of('date')))); n['予想者'] += 1
    H.append('<button class="btn" onclick="gen()">予想JSONを生成してハッシュを表示</button><button class="btn" onclick="dl()">JSONをダウンロード</button>')
    H.append('<p>SHA-256: <span id="hash">（未生成）</span></p><pre id="out" style="white-space:pre-wrap;font-size:11px"></pre>')
    H.append('<p style="font-size:11px">%s</p>' % FENCE)
    H.append(js_block(T, P) + '</body></html>')
    assert n['床持続'] == len(FD['cells']) and n['向き'] == len(CON), n
    assert n['向き'] + n['床持続'] + n['全体'] == P['n_prediction_fields'], (n, P['n_prediction_fields'])
    return '\n'.join(H) + '\n', n


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--force', action='store_true'); ap.add_argument('--contrasts', default=None); ap.add_argument('--out', default=None)
    a = ap.parse_args(); T = runs_A.load_T(a.contrasts); P = T['predictions']
    out = a.out or os.path.join(REPO, P['form'])
    if os.path.exists(out) and not a.force:
        sys.exit('既存の様式があるので上書きしない（--force）: %s' % out)
    text, n = build(T)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write(text)
    print('[make_predictions_form_A %s] written %s | 選択の欄 %s | 予想の欄 %d | SHA16 %s' % (VERSION, out, n, P['n_prediction_fields'], runs_A.sha16_file(out)))
