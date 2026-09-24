# -*- coding: utf-8 -*-
"""make_predictions_form_Bl3.py v1 —— B-lens 層三（Bl3）の予想の書式（HTML・単一ファイル・押しボタンで一つ選ぶ・ブラウザの中で JSON と SHA-256 を作る・2026-09-25）。

正本 `design/contrasts-Bl3.json` の `predictions.items`（七つの項目・裁定 D148・D209・D210・D217）を、押しボタンの欄に組む（B-lens の書式の型）。
正本の項目は鍵と選択肢を持つので、器は欄を作らず、正本の鍵と選択肢をそのまま使う。q1 の選択肢は正本 `pilot.decision.q1_map` の鍵と同じであることを確かめる。
初めは「予想しない」が選ばれている。情報状態は自由記述の欄に書く（正本 `predictions.free`・封印の前の露出の記録を読んだことを書く・項目ごとの印は付けない）。
確かさの欄は置かない（正本に無い）。引かれている結論の一行の欄は B-lens の書式の型のまま置く（予想の欄に数えない）。
SHA-256 の JS は V′ 様式 v0.5 から逐語で流用し、様式の名・プログラム・正本の版・保存の名の四つだけを置き換える（B-lens と同じ流用・`make_predictions_form_B` の型）。
用法: python tools/make_predictions_form_Bl3.py [--force] ／ --selftest
柵: 本様式のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, html, argparse
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import make_predictions_form_B as FB

VERSION = 'v1'
FORM_VERSION = 'v1'
OUT = os.path.join(REPO, 'records', 'predictions', 'predictions-form-Bl3-v1.html')
NP = '予想しない'
FENCE = '本様式のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
esc = lambda s: html.escape(str(s), quote=True)
OTHER = ['free', 'info.coi', 'who', 'date']


def load_T():
    return json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))


def meta(T):
    return {'form': 'predictions-form %s (Bl3)' % FORM_VERSION, 'program': 'ontology-preamble-4b/Bl3', 'contrasts': T['version'], 'download': 'predictions-Bl3.json'}


def js_block(T):
    TB = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
    src = open(os.path.join(REPO, TB['predictions']['js_source']), encoding='utf-8').read()
    js = re.search(r'<script>.*?</script>', src, re.S).group(0)
    assert js.count(FB.V5_META) == 1 and js.count(FB.V5_DL) == 1, 'V′ 様式 v0.5 の JS の置き換える文字列が一つずつでない'
    M = meta(T)
    return js.replace(FB.V5_META, "form:'%s',program:'%s',contrasts:'%s'" % (M['form'], M['program'], M['contrasts'])).replace(FB.V5_DL, M['download'])


def items(T):
    return T['predictions']['items']


def prediction_keys(T):
    return [it['key'] for it in items(T)]


def check_canon(T):
    """正本の項目の形の確かめ（鍵が重ならない・選択肢がある・「予想しない」を選択肢に持たない・q1 の選択肢が下見の決めの対応の鍵と同じ）。"""
    its = items(T)
    keys = [it['key'] for it in its]
    assert len(keys) == len(set(keys)) and all(it.get('ask') and it.get('options') for it in its), '正本の項目の鍵が重なるか、問いか選択肢が無い'
    assert all(NP not in it['options'] and len(it['options']) == len(set(it['options'])) for it in its), '選択肢に「予想しない」があるか、重なっている'
    q1 = [it for it in its if it['key'] == 'q1.pilot'][0]
    assert q1['options'] == list(T['pilot']['decision']['q1_map']), ('q1 の選択肢が下見の決めの対応の鍵と違う', q1['options'], list(T['pilot']['decision']['q1_map']))
    return keys


def build(T):
    P = T['predictions']
    check_canon(T)
    Q = T['pilot']['decision']['q1_map']
    H = ['<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>予想の書式 %s（B-lens 層三・正本 %s）</title>' % (esc(FORM_VERSION), esc(T['version'])),
         '<style>body{font-family:sans-serif;max-width:1100px;margin:1em auto;padding:0 1em;line-height:1.6;color:#222}'
         'h1{font-size:1.35em}h2{font-size:1.1em;border-bottom:2px solid #ccc;margin-top:1.5em}.box{border:1px solid #ccc;background:#fafafa;padding:.6em 1em;margin:.6em 0}'
         'table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:4px 6px;vertical-align:top}th{background:#f0f0f0;text-align:left}'
         '.q{display:flex;flex-wrap:wrap;gap:4px}.opt{border:1px solid #888;background:#fff;border-radius:14px;padding:3px 10px;cursor:pointer;font-size:13px}'
         '.opt:hover{background:#eef}.opt.on{background:#2b5fb4;color:#fff;border-color:#2b5fb4}.btn{font-size:15px;padding:6px 14px;margin:4px 6px 4px 0;cursor:pointer}'
         '#hash{font-family:monospace;font-size:15px;background:#ffd;padding:4px}pre{background:#f6f6f6;padding:6px;max-height:320px;overflow:auto;font-size:12px}.muted{color:#666;font-size:12px}</style></head><body>',
         '<h1>予想の書式 %s——B-lens 層三（足した方向の全経路の効き目を、等方のランダム方向と実在の差の方向と比べる）</h1>' % esc(FORM_VERSION),
         '<div class="box"><b>使い方</b>: 各欄の選択肢を<b>一度押すと選ばれます</b>（青いものが選ばれた値）。分からない欄は初めの「%s」のままで構いません。'
         '最後に「封印する」を押すと、JSON と SHA-256 が下に出ます。<b>SHA-256 をチャットに貼り、JSON を保存して添付してください</b>（「JSON をダウンロード」）。<br>'
         '<b>封印の順</b>: %s。<br><b>時</b>: %s。<br><b>止まったとき</b>: %s。<br><b>情報状態</b>: %s。</div>' % (
             esc(NP), FB.md(P['order']), FB.md(P['when']), FB.md(P['if_stopped']), FB.md(P['free'])),
         '<p class="muted">正本 %s・書式 %s・器 tools/make_predictions_form_Bl3.py %s。予想した欄: <b id="cnt">0</b></p>' % (esc(T['version']), esc(FORM_VERSION), VERSION)]
    H.append('<h2>用語</h2><table>')
    for term, text in (('読み取り（甲）', T['readout']['primary']['rule'] + '。' + T['readout']['primary']['quantity']), ('等方の外', T['labels']['iso_outside']['rule']),
                       ('二つ目の札', T['labels']['second']['rule']), ('札の言い方', T['labels']['print_rule']), ('下見の決め', T['pilot']['decision']['rule']),
                       ('門', T['gate']['test'] + '。' + T['gate']['push']), ('v̂ を抜いた門', T['gate']['without_vhat']), ('門が判定不能のとき', P['gate_rule']),
                       ('q7 の決まり', P['q7_rule'])):
        H.append('<tr><th>%s</th><td>%s</td></tr>' % (esc(term), FB.md(text)))
    H.append('<tr><th>q1 の選択肢と下見の決め</th><td>%s</td></tr>' % '<br>'.join('%s: %s' % (esc(k), FB.md(v)) for k, v in Q.items()))
    H.append('</table><h2>予想の項目（%d）</h2><table><tr><th>鍵</th><th>項目（正本の文）</th><th>欄</th></tr>' % len(items(T)))
    for it in items(T):
        H.append('<tr><td><code>%s</code></td><td>%s</td><td>%s</td></tr>' % (esc(it['key']), FB.md(it['ask']), FB.pills(it['key'], it['options'], NP, pred=True)))
    H.append('</table><h2>情報状態と予想者（予想の欄に数えない）</h2><table>')
    H.append('<tr><td>情報状態（封印の前に見たもの・封印の前の露出の記録 <code>records/Bl3/exposure-before-seal-Bl3.md</code> を読んだこと）</td>'
             '<td><textarea data-k="free" rows="5" cols="90"></textarea></td></tr>')
    H.append('<tr><td>引かれている結論（利益相反・一行）</td><td><input data-k="info.coi" size="90"></td></tr>')
    H.append('<tr><td>予想者</td><td>%s</td></tr>' % FB.pills('who', ['登録者', 'コーディネータ'], '登録者'))
    H.append('<tr><td>日付</td><td><input data-k="date" size="20" placeholder="例: 2026-09-26"></td></tr></table>')
    H.append('<h2>封印</h2><button class="btn" onclick="gen()">封印する（JSON と SHA-256 を作る）</button><button class="btn" onclick="dl()">JSON をダウンロード</button>'
             '<p>SHA-256: <span id="hash"></span></p><pre id="out"></pre>')
    H.append(js_block(T))
    H.append(FB.PILL_JS % NP)
    H.append('<p class="muted">%s</p></body></html>' % esc(FENCE))
    return '\n'.join(H)


class _Keys(HTMLParser):
    def __init__(self):
        super().__init__()
        self.keys, self.opts, self._cur = [], {}, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'data-k' in a:
            self.keys.append(a['data-k'])
            self._cur = a['data-k'] if a.get('type') == 'hidden' else None
            if self._cur:
                self.opts[self._cur] = []
        if tag == 'button' and 'data-v' in a and self._cur:
            self.opts[self._cur].append(a['data-v'])


def read_form(h):
    """書式の HTML から、欄の鍵と押しボタンの選択肢を読む（封印の器が同じ鍵・同じ選択肢だけを受けるため）。"""
    p = _Keys()
    p.feed(h)
    return p.keys, p.opts


def check(T, h):
    keys, opts = read_form(h)
    assert len(keys) == len(set(keys)), '欄の鍵が重なっている'
    for k in prediction_keys(T) + OTHER:
        assert k in keys, ('欄が無い', k)
    assert set(keys) == set(prediction_keys(T) + OTHER), ('書式に余計な欄がある', sorted(set(keys) - set(prediction_keys(T) + OTHER)))
    for it in items(T):
        assert opts[it['key']] == it['options'], ('選択肢が違う', it['key'], opts.get(it['key']))
    M = meta(T)
    assert FB.V5_META not in h and ("form:'%s'" % M['form']) in h and M['download'] in h, 'JS の置き換えが無い'
    assert h.count('function gen(') == 1 and h.count('function sha256hex(') == 1, 'JS が足りない'
    return {'keys': len(keys), 'prediction_fields': len(prediction_keys(T))}


def _selftest():
    T = load_T()
    h = build(T)
    r = check(T, h)
    broken = h.replace('data-k="q4.gate"', 'data-x="dropped"', 1)
    try:
        check(T, broken)
        raise AssertionError('欄を落とした様式を通した')
    except AssertionError as e:
        assert '通した' not in str(e), e
    T2 = json.loads(json.dumps(T))
    T2['predictions']['items'][0]['options'] = ['続ける', '止める']
    try:
        check_canon(T2)
        raise AssertionError('q1 の選択肢が下見の決めと違う正本を通した')
    except AssertionError as e:
        assert '通した' not in str(e), e
    print('[make_predictions_form_Bl3] 自己検査 OK（欄 %d・予想の欄 %d）' % (r['keys'], r['prediction_fields']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    T = load_T()
    if os.path.exists(OUT) and not a.force:
        sys.exit('既にある（--force で上書き）: %s' % OUT)
    h = build(T)
    r = check(T, h)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(h)
    print('[make_predictions_form_Bl3] %s（欄 %d・予想の欄 %d）' % (os.path.relpath(OUT, REPO), r['keys'], r['prediction_fields']))
