# -*- coding: utf-8 -*-
"""make_predictions_form_Blens.py v1 —— B-lens の予想の書式（HTML・単一ファイル・押しボタンで一つ選ぶ・ブラウザの中で JSON と SHA-256 を作る・2026-09-23）。

正本 `design/contrasts-Blens.json` の `predictions`（裁定 D148 の順・裁定 D172・D183）の八つの項目を、押しボタンの欄に組む（段階 B の書式の型・正本 §8）。
欄（鍵）は器が決め、各項目の選択肢の字が、正本の項目の文にあることを器で確かめる（向き・門・比・S4 の選択肢。札の選択肢は第一項の文にある）。
各項目に確かさ（正本 `predictions.confidence_levels`）の欄を置く。初めは「予想しない」が選ばれている。
SHA-256 の JS は V′ 様式 v0.5 から逐語で流用し、様式の名・プログラム・正本の版・保存の名の四つだけを置き換える（段階 A・B と同じ流用・`make_predictions_form_B` の型）。
用法: python tools/make_predictions_form_Blens.py [--force] ／ --selftest
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
OUT = os.path.join(REPO, 'records', 'predictions', 'predictions-form-Blens-v1.html')
NP = '予想しない'
LABELS = ['付かない', '等方の外だけ', '二つ目の札だけ', '両方']
FENCE = '本様式のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
esc = lambda s: html.escape(str(s), quote=True)
# 項目（正本 predictions.items の順）→ 欄。欄は (鍵, 選択肢, 選択肢を正本の項目の文で確かめるか)
FIELDS = [
    ('p1', [('p1.survival.label', LABELS, True), ('p1.survival.dir', ['破局の文字の側', '反対'], True), ('p1.nuclear.label', LABELS, True), ('p1.nuclear.dir', ['破局の文字の側', '反対'], True)]),
    ('p2', [('p2.survival.label', LABELS, False), ('p2.survival.dir', ['破局の選択肢の語の側', '反対'], True), ('p2.nuclear.label', LABELS, False), ('p2.nuclear.dir', ['破局の選択肢の語の側', '反対'], True)]),
    ('p3', [('p3.label', LABELS, False), ('p3.dir', ['O の語の側', 'Osec の語の側'], True)]),
    ('p4', [('p4.label', LABELS, False), ('p4.dir', ['コードブロックの書き出しを押し上げる', '押し下げる'], True)]),
    ('p5', [('p5.answer', ['大きい', '大きくない'], False)]),
    ('p6', [('p6.gate', ['通らない', 'M_L で通る', 'M_X で通る', '両方'], True), ('p6.without_vhat', ['通る', '通らない'], False)]),
    ('p7', [('p7.answer', ['無い', '一部', '全部'], True)]),
    ('p8', [('p8.answer', ['同じ向き', '逆向き'], True)]),
]
FIELD_LABEL = {'survival.label': 'survival の札', 'survival.dir': 'survival の向き（札が付くなら）', 'nuclear.label': 'nuclear の札', 'nuclear.dir': 'nuclear の向き（札が付くなら）',
               'label': '札', 'dir': '向き（札が付くなら）', 'answer': '答え', 'gate': '方向を単位にした門', 'without_vhat': 'v̂ を抜いた門'}
INFO = [('info.read_votes', '設計の巡の二巡の八票とその整理（再現の表・採否表）を読んだか', ['読んだ', '一部', '読んでいない']),
        ('info.read_facts', '草案の設計の事実（§6 の転記行）を見たか', ['見た', '一部', '見ていない'])]


def load_T():
    return json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))


def meta(T):
    return {'form': 'predictions-form %s (Blens)' % FORM_VERSION, 'program': 'ontology-preamble-4b/Blens', 'contrasts': T['version'], 'download': 'predictions-Blens.json'}


def js_block(T):
    TB = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
    src = open(os.path.join(REPO, TB['predictions']['js_source']), encoding='utf-8').read()
    js = re.search(r'<script>.*?</script>', src, re.S).group(0)
    assert js.count(FB.V5_META) == 1 and js.count(FB.V5_DL) == 1, 'V′ 様式 v0.5 の JS の置き換える文字列が一つずつでない'
    M = meta(T)
    return js.replace(FB.V5_META, "form:'%s',program:'%s',contrasts:'%s'" % (M['form'], M['program'], M['contrasts'])).replace(FB.V5_DL, M['download'])


def prediction_keys():
    return [k for _, fs in FIELDS for k, _, _ in fs] + ['%s.conf' % p for p, _ in FIELDS]


def check_options_in_canon(T):
    """選択肢の字が正本の項目の文にあること（器が欄を勝手に作らないための突き合わせ）。"""
    items = T['predictions']['items']
    assert len(items) == len(FIELDS), ('正本の項目の数と欄の項目の数が違う', len(items), len(FIELDS))
    for (p, fs), text in zip(FIELDS, items):
        for k, opts, strict in fs:
            if strict:
                for o in opts:
                    assert o in text, ('選択肢の字が正本の項目の文に無い', k, o)
    assert '大きいか' in items[4] and '通るか' in items[5] and all(x in T['predictions']['confidence_levels'] for x in ('高', '中', '低'))


def build(T):
    P = T['predictions']
    check_options_in_canon(T)
    H = ['<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>予想の書式 %s（B-lens・正本 %s）</title>' % (esc(FORM_VERSION), esc(T['version'])),
         '<style>body{font-family:sans-serif;max-width:1100px;margin:1em auto;padding:0 1em;line-height:1.6;color:#222}'
         'h1{font-size:1.35em}h2{font-size:1.1em;border-bottom:2px solid #ccc;margin-top:1.5em}.box{border:1px solid #ccc;background:#fafafa;padding:.6em 1em;margin:.6em 0}'
         'table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:4px 6px;vertical-align:top}th{background:#f0f0f0;text-align:left}'
         '.q{display:flex;flex-wrap:wrap;gap:4px}.opt{border:1px solid #888;background:#fff;border-radius:14px;padding:3px 10px;cursor:pointer;font-size:13px}'
         '.opt:hover{background:#eef}.opt.on{background:#2b5fb4;color:#fff;border-color:#2b5fb4}.btn{font-size:15px;padding:6px 14px;margin:4px 6px 4px 0;cursor:pointer}'
         '#hash{font-family:monospace;font-size:15px;background:#ffd;padding:4px}pre{background:#f6f6f6;padding:6px;max-height:320px;overflow:auto;font-size:12px}.muted{color:#666;font-size:12px}</style></head><body>',
         '<h1>予想の書式 %s——B-lens（凍結した方向の直接の経路を語彙に射影し、段階 B の行動で校正する）</h1>' % esc(FORM_VERSION),
         '<div class="box"><b>使い方</b>: 各欄の選択肢を<b>一度押すと選ばれます</b>（青いものが選ばれた値）。分からない欄は初めの「%s」のままで構いません。'
         '最後に「封印する」を押すと、JSON と SHA-256 が下に出ます。<b>SHA-256 をチャットに貼り、JSON を保存して添付してください</b>（「JSON をダウンロード」）。<br>'
         '<b>封印の順</b>: %s。<br><b>情報状態</b>: %s。</div>' % (esc(NP), FB.md(P['order']), FB.md(P['information_state'])),
         '<p class="muted">正本 %s・書式 %s・器 tools/make_predictions_form_Blens.py %s。予想した欄: <b id="cnt">0</b></p>' % (esc(T['version']), esc(FORM_VERSION), VERSION)]
    H.append('<h2>用語</h2><table>')
    for term, text in (('等方の外', T['primary']['label_isotropic']), ('二つ目の札', T['primary']['label_second']), ('札の言い方', T['primary']['print_rule']),
                       ('M_L', T['metrics']['M_L']), ('M_X', T['metrics']['M_X']), ('M_E', T['metrics']['M_E']), ('M_F', T['metrics']['M_F']),
                       ('門', T['calibration']['gate']), ('v̂ を抜いた門', T['calibration']['gate_without_vhat']), ('読みの比', T['magnitude']['reading'])):
        H.append('<tr><th>%s</th><td>%s</td></tr>' % (esc(term), FB.md(text)))
    H.append('</table><h2>予想の項目（%d）</h2><table><tr><th>項目（正本の文）</th><th>欄</th></tr>' % len(FIELDS))
    for (p, fs), text in zip(FIELDS, P['items']):
        cells = ''.join('<div><span class="muted">%s</span>%s</div>' % (esc(FIELD_LABEL[k.split('.', 1)[1]]), FB.pills(k, opts, NP, pred=True)) for k, opts, _ in fs)
        cells += '<div><span class="muted">確かさ</span>%s</div>' % FB.pills('%s.conf' % p, P['confidence_levels'], NP, pred=True)
        H.append('<tr><td>%s</td><td>%s</td></tr>' % (FB.md(text), cells))
    H.append('</table><h2>情報状態と予想者（予想の欄に数えない）</h2><table>')
    for k, text, opts in INFO:
        H.append('<tr><td>%s</td><td>%s</td></tr>' % (esc(text), FB.pills(k, opts, opts[-1])))
    H.append('<tr><td>予想者</td><td>%s</td></tr>' % FB.pills('who', ['登録者', 'コーディネータ'], '登録者'))
    H.append('<tr><td>引かれている結論（利益相反・一行）</td><td><input data-k="info.coi" size="90"></td></tr>')
    H.append('<tr><td>自由記述</td><td><textarea data-k="free" rows="4" cols="90"></textarea></td></tr>')
    H.append('<tr><td>日付</td><td><input data-k="date" size="20" placeholder="例: 2026-09-24"></td></tr></table>')
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
    for k in prediction_keys() + [x[0] for x in INFO] + ['who', 'info.coi', 'free', 'date']:
        assert k in keys, ('欄が無い', k)
    for p, fs in FIELDS:
        for k, o, _ in fs:
            assert opts[k] == o, ('選択肢が違う', k, opts.get(k))
    M = meta(T)
    assert FB.V5_META not in h and ("form:'%s'" % M['form']) in h and M['download'] in h, 'JS の置き換えが無い'
    assert h.count('function gen(') == 1 and h.count('function sha256hex(') == 1, 'JS が足りない'
    return {'keys': len(keys), 'prediction_fields': len(prediction_keys())}


def _selftest():
    T = load_T()
    h = build(T)
    r = check(T, h)
    broken = h.replace('data-k="p6.gate"', 'data-x="dropped"', 1)
    try:
        check(T, broken)
        raise AssertionError('欄を落とした様式を通した')
    except AssertionError as e:
        assert '通した' not in str(e), e
    T2 = json.loads(json.dumps(T))
    T2['predictions']['items'][7] = T2['predictions']['items'][7].replace('逆向き', '反対の向き')
    try:
        check_options_in_canon(T2)
        raise AssertionError('正本に無い選択肢を通した')
    except AssertionError as e:
        assert '通した' not in str(e), e
    print('[make_predictions_form_Blens] 自己検査 OK（欄 %d・予想の欄 %d）' % (r['keys'], r['prediction_fields']))


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
    print('[make_predictions_form_Blens] %s（欄 %d・予想の欄 %d）' % (os.path.relpath(OUT, REPO), r['keys'], r['prediction_fields']))
