# -*- coding: utf-8 -*-
"""make_predictions_form_B.py v1 —— 段階 B の予想様式 v0.9（HTML・単一ファイル・**押しボタンで一つ選ぶ**・ブラウザの中で JSON と SHA-256 を生成）を、
正本 `design/contrasts-B.json` の `predictions`（登録者裁定 D148・2026-09-19・段階 A の裁定 D47 の型）から機械生成する。
欄: 確証の対比ごとの向き（封印の値と同じ三つ）・S4 の反証・確証の本数の帯・門1（ここまでが予想の欄）と、情報状態・v̂ の出どころを読んだか・COI・自由記述・予想者・日付。
用語の説明（`predictions.glossary`）と場面の説明（`predictions.scenario_notes`）を様式の頭に載せる。自動入力は置かない（`predictions.preset`）。
**選び方**: 各欄の選択肢を押しボタンで並べ、一度押すと選ばれる（隠した入力の欄に値が入る）。初めは「予想しない」が選ばれている。
SHA-256 の JS は V′ 様式 v0.5（`predictions.js_source`）から逐語で流用し、様式の名・プログラム・正本の版・保存の名の四つだけを置き換える（段階 A・F・M と同じ流用）。
JS は `data-k` を持つ要素の値を集めるので、押しボタンの値は隠した入力の欄（`data-k`）に書く。
用法: python tools/make_predictions_form_B.py [--force]（出力は正本 `predictions.form`・既存は --force が無ければ上書きしない）／ --selftest
柵: 本様式のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, html, argparse
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

REPO = runs_B.REPO
VERSION = 'v1'
V5_META = "form:'predictions-form v0.5 (Vprime)',program:'ontology-preamble-4b/Vprime',contrasts:'draft7-2026-09-07'"
V5_DL = 'predictions-Vprime-registrant.json'
FENCE = '本様式のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
esc = lambda s: html.escape(str(s), quote=True)


def md(s):
    """正本の文を HTML にする（エスケープの後に、**太字** を <b>、`コード` を <code> にする・ほかの書式は持ち込まない）。"""
    t = esc(s)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t.replace('**', '').replace('`', '')
FAMILY_LABEL = {'B_sub': '減算族', 'B_add': '加算族', 'B_cross': '交差族'}


def meta(T):
    P = T['predictions']
    return {'form': 'predictions-form %s (B)' % P['form_version'], 'program': 'ontology-preamble-4b/B', 'contrasts': T['version'],
            'download': 'predictions-B.json'}


def js_block(T):
    P = T['predictions']
    src = open(os.path.join(REPO, P['js_source']), encoding='utf-8').read()
    js = re.search(r'<script>.*?</script>', src, re.S).group(0)
    assert js.count(V5_META) == 1 and js.count(V5_DL) == 1, 'V′ 様式 v0.5 の JS の置き換える文字列が一つずつでない'
    M = meta(T)
    return js.replace(V5_META, "form:'%s',program:'%s',contrasts:'%s'" % (M['form'], M['program'], M['contrasts'])).replace(V5_DL, M['download'])


PILL_JS = """<script>
document.addEventListener('click',function(ev){const b=ev.target.closest('button.opt');if(!b)return;const q=b.closest('.q');
q.querySelectorAll('button.opt').forEach(x=>x.classList.remove('on'));b.classList.add('on');q.querySelector('input[type=hidden]').value=b.dataset.v;count();});
function count(){let n=0,t=0;document.querySelectorAll('.q.pred input[type=hidden]').forEach(e=>{t++;if(e.value!=='%s')n++;});document.getElementById('cnt').textContent=n+' / '+t;}
document.addEventListener('DOMContentLoaded',count);
</script>"""


def pills(key, options, default, glosses=None, pred=False):
    """押しボタンの一群（一度押すと選ばれる）。値は隠した入力の欄（data-k）に入る。"""
    g = glosses or {}
    bs = ''.join('<button type="button" class="opt%s" data-v="%s"%s>%s</button>' % (
        ' on' if o == default else '', esc(o), (' title="%s"' % esc(g[o])) if o in g else '', esc(o)) for o in options)
    return '<div class="q%s"><input type="hidden" data-k="%s" value="%s">%s</div>' % (' pred' if pred else '', esc(key), esc(default), bs)


def arm_words(arm):
    """腕の名を、書式の読み手に向けた短い言葉にする（例: O-Ncold-v → O-Ncold から v̂ を引いた腕）。"""
    base = re.split(r'[+\-]v', arm)[0]
    if '+v' in arm or '-v' in arm:
        sign = '足した' if '+v' in arm else '引いた'
        tail = arm.split('+v')[-1] if '+v' in arm else arm.split('-v')[-1]
        what = {'': 'v̂（O の方向）', 'rand': 'ランダム方向', 'Nk': 'Nk の方向', 'td': '腕対の差の方向', '6b': '負荷下の方向 (6b)'}[tail]
        return '%s に%sを%s腕' % (base, what, sign) if sign == '足した' else '%s から%sを%s腕' % (base, what, sign)
    return '%s（無操作）' % base


def build(T):
    P = T['predictions']
    F = P['fields']
    NP = P['not_predicted']
    DG = F['direction'].get('glosses') or {}
    H = ['<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>予想フォーム %s（段階 B・機構層・正本 %s）</title>' % (esc(P['form_version']), esc(T['version'])),
         '<style>body{font-family:sans-serif;max-width:1100px;margin:1em auto;padding:0 1em;line-height:1.6;color:#222}'
         'h1{font-size:1.4em}h2{font-size:1.15em;border-bottom:2px solid #ccc;margin-top:1.6em}h3{font-size:1em;margin:1em 0 .3em}'
         '.box{border:1px solid #ccc;background:#fafafa;padding:.6em 1em;margin:.6em 0}dt{font-weight:bold;margin-top:.4em}dd{margin:0 0 .3em 1.2em}'
         'table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:4px 6px;vertical-align:top}th{background:#f0f0f0;text-align:left}'
         '.q{display:flex;flex-wrap:wrap;gap:4px}.opt{border:1px solid #888;background:#fff;border-radius:14px;padding:3px 10px;cursor:pointer;font-size:13px}'
         '.opt:hover{background:#eef}.opt.on{background:#2b5fb4;color:#fff;border-color:#2b5fb4}'
         '.btn{font-size:15px;padding:6px 14px;margin:4px 6px 4px 0;cursor:pointer}#hash{font-family:monospace;font-size:15px;background:#ffd;padding:4px}'
         'pre{background:#f6f6f6;padding:6px;max-height:320px;overflow:auto;font-size:12px}.muted{color:#666;font-size:12px}</style></head><body>',
         '<h1>予想フォーム %s——段階 B（機構層・Qwen3-4B-Instruct-2507・O の枠組みに対応する方向の加減で、破局的選択率は動くか）</h1>' % esc(P['form_version']),
         '<div class="box"><b>使い方</b>: 各欄の選択肢を<b>一度押すと選ばれます</b>（青く光ったものが選ばれた値）。分からない欄は初めの「%s」のままで構いません。'
         '自動入力: %s。最後に「封印する」を押すと、JSON と SHA-256 が下に出ます。<b>SHA-256 をチャットに貼り、JSON を保存して添付してください</b>（「JSON をダウンロード」）。<br>'
         '<b>封印の順</b>: %s。<br><b>独立の決まり</b>: %s。<br><b>時機</b>: %s。<br><b>柵</b>: %s。</div>'
         % (esc(NP), md(P['preset']), md(P['order']), md(P['independence']), md(P['timing']), md(P['fence'])),
         '<p class="muted">正本 %s・様式 %s・器 tools/make_predictions_form_B.py %s。予想した欄: <b id="cnt">0</b></p>' % (esc(T['version']), esc(P['form_version']), VERSION)]
    # 用語と場面の説明
    H.append('<h2>用語の説明</h2><dl>')
    for term, text in P['glossary']:
        H.append('<dt>%s</dt><dd>%s</dd>' % (esc(term), md(text)))
    H.append('</dl><h2>場面の説明</h2><dl>')
    for sc in T['scenarios']:
        H.append('<dt>%s</dt><dd>%s</dd>' % (esc(sc), md(P['scenario_notes'][sc])))
    H.append('</dl>')
    # 情報状態
    H.append('<h2>情報状態（予想の欄に数えない）</h2><table><tr><th>記録</th><th>読んだか</th></tr>')
    for it in F['info']['items']:
        H.append('<tr><td>%s</td><td>%s</td></tr>' % (md(it['text']), pills(it['key'], F['info']['options'], F['info']['options'][-1])))
    V = F['vhat_floor_ack']
    H.append('<tr><td>%s</td><td>%s</td></tr></table>' % (md(V['text']), pills(V['key'], V['options'], V['options'][0])))
    coi = next(x for x in F['text'] if x['key'] == 'info.coi')
    H.append('<p>%s<br><input data-k="info.coi" size="100" placeholder="例: O の方向で破局率が下がってほしい／何も動かないでほしい など"></p>' % esc(coi['text']))
    # 向き
    n_dir = 0
    H.append('<h2>向き（確証の対比ごと・%d 本）</h2><p class="muted">A の腕の破局率が、B の腕（ランダム方向の腕）に比べてどう動くか。%s</p>'
             % (sum(len(Fm['contrasts']) for Fm in T['families'].values()), esc('／'.join('%s＝%s' % (k, v) for k, v in DG.items()))))
    for fk, Fm in T['families'].items():
        H.append('<h3>%s——%s</h3><table><tr><th>場面</th><th>A（介入の腕） 対 B（相手）</th><th>予想</th></tr>' % (esc(FAMILY_LABEL.get(fk, fk)), md(Fm['question'])))
        for c in Fm['contrasts']:
            H.append('<tr><td>%s</td><td>%s<br><span class="muted">A: %s／B: %s</span></td><td>%s</td></tr>' % (
                esc(c['scenario']), esc('%s 対 %s' % (c['A'], c['B'])), esc(arm_words(c['A'])), esc(arm_words(c['B'])),
                pills(F['direction']['key_prefix'] + c['id'], F['direction']['options'], NP, DG, pred=True)))
            n_dir += 1
        H.append('</table>')
    # S4
    S4 = T['descriptive_families']['B_desc_S4']
    H.append('<h2>S4 の反証</h2><p>%s</p><p class="muted">%s</p>%s' % (md(F['s4']['what']), md(S4['question']),
                                                                     pills(F['s4']['key'], F['s4']['options'], NP, DG, pred=True)))
    # 全体
    CB = F['confirmed_band']
    band_opts = [NP] + [('%d %s' % (a, CB['unit'])) if a == b else ('%d〜%d %s' % (a, b, CB['unit'])) for a, b in CB['edges']]
    H.append('<h2>全体</h2><table><tr><td>%s</td><td>%s</td></tr><tr><td>%s</td><td>%s</td></tr></table>' % (
        md(CB['what']), pills(CB['key'], band_opts, NP, pred=True), md(F['gate1']['what']), pills(F['gate1']['key'], F['gate1']['options'], NP, pred=True)))
    # 予想者・自由記述・日付
    free = next(x for x in F['text'] if x['key'] == 'free')
    date = next(x for x in F['text'] if x['key'] == 'date')
    H.append('<h2>予想者と記述</h2><table><tr><td>予想者</td><td>%s</td></tr>' % pills(F['who']['key'], F['who']['options'], F['who']['options'][0]))
    H.append('<tr><td>%s</td><td><textarea data-k="free" rows="4" cols="90"></textarea></td></tr>' % esc(free['text']))
    H.append('<tr><td>%s</td><td><input data-k="date" size="20" placeholder="例: 2026-09-20"></td></tr></table>' % esc(date['text']))
    # 封印
    H.append('<h2>封印</h2><button class="btn" onclick="gen()">封印する（JSON と SHA-256 を作る）</button><button class="btn" onclick="dl()">JSON をダウンロード</button>'
             '<p>SHA-256: <span id="hash"></span></p><pre id="out"></pre>')
    H.append(js_block(T))
    H.append(PILL_JS % NP)
    H.append('<p class="muted">%s</p></body></html>' % esc(FENCE))
    return '\n'.join(H), n_dir


class _Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.keys, self.stack, self.bad = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'data-k' in a:
            self.keys.append(a['data-k'])
        if tag not in ('input', 'meta', 'br'):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ('input', 'meta', 'br'):
            return
        if not self.stack or self.stack[-1] != tag:
            self.bad.append((tag, self.stack[-3:]))
        else:
            self.stack.pop()


def check(T, h, n_dir):
    """様式を組み直さずに、出来上がった HTML を読んで確かめる（欄の数・鍵の重なり・選択肢・JS の置き換え・閉じ忘れ）。"""
    P = T['predictions']
    F = P['fields']
    c = _Check()
    c.feed(h)
    keys = c.keys
    assert len(keys) == len(set(keys)), '欄の鍵が重なっている'
    conf = [x['id'] for Fm in T['families'].values() for x in Fm['contrasts']]
    dir_keys = [k for k in keys if k.startswith(F['direction']['key_prefix'])]
    assert sorted(dir_keys) == sorted(F['direction']['key_prefix'] + i for i in conf) and n_dir == len(conf), '向きの欄が確証の対比と合わない'
    pred_keys = dir_keys + [F['s4']['key'], F['confirmed_band']['key'], F['gate1']['key']]
    assert len(pred_keys) == P['n_prediction_fields'] and all(k in keys for k in pred_keys), '予想の欄の数が正本と違う'
    for k in [x['key'] for x in F['info']['items']] + [F['vhat_floor_ack']['key'], 'info.coi', 'free', 'date', F['who']['key']]:
        assert k in keys, ('欄が無い', k)
    assert not c.bad and not [t for t in c.stack if t not in ('html', 'body')], ('閉じ忘れ', c.bad[:3], c.stack[-3:])
    M = meta(T)
    assert V5_META not in h and V5_DL not in h and ("form:'%s'" % M['form']) in h and M['download'] in h, 'JS の置き換えが無い'
    assert h.count('function gen(') == 1 and h.count('function sha256hex(') == 1 and 'button.opt' in h, 'JS が足りない'
    for sv in F['direction']['options']:
        assert ('data-v="%s"' % esc(sv)) in h, ('選択肢が無い', sv)
    return {'keys': len(keys), 'prediction_fields': len(pred_keys)}


def _selftest():
    T = runs_B.load_T()
    h, n = build(T)
    r = check(T, h, n)
    # 恒真にしない: 向きの欄を一つ落とした様式は落ちる／JS の置き換えを忘れた様式は落ちる
    first = T['predictions']['fields']['direction']['key_prefix'] + T['families']['B_sub']['contrasts'][0]['id']
    broken = h.replace('data-k="%s"' % esc(first), 'data-x="dropped"', 1)
    try:
        check(T, broken, n)
        raise AssertionError('欄を落とした様式を通した')
    except AssertionError as e:
        assert '欄を落とした様式を通した' not in str(e), e
    try:
        check(T, h.replace("form:'%s'" % meta(T)['form'], V5_META, 1), n)
        raise AssertionError('JS の置き換えを忘れた様式を通した')
    except AssertionError as e:
        assert '忘れた様式を通した' not in str(e), e
    assert arm_words('O-Ncold-v') == 'O-Ncold からv̂（O の方向）を引いた腕' and arm_words('Onull+vrand') == 'Onull にランダム方向を足した腕', arm_words('O-Ncold-v')
    assert '**' not in h and '`' not in h.split('<script>')[0], '正本の文の書式の記号が残っている'
    assert md('**a** と `b`') == '<b>a</b> と <code>b</code>', md('**a** と `b`')
    print('[make_predictions_form_B selftest] 欄 %d（予想の欄 %d）・鍵の重なり無し・向きの欄は確証の対比と一致・JS の置き換え・閉じ忘れ無し・落とした様式を止める: 通った' % (r['keys'], r['prediction_fields']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    T = runs_B.load_T()
    out = os.path.join(REPO, *T['predictions']['form'].split('/'))
    if os.path.exists(out) and not a.force:
        sys.exit('既にある（--force で上書き）: %s' % out)
    h, n = build(T)
    r = check(T, h, n)
    open(out, 'w', encoding='utf-8', newline='\n').write(h)
    print('[make_predictions_form_B] %s（欄 %d・予想の欄 %d・SHA16 %s）' % (os.path.relpath(out, REPO), r['keys'], r['prediction_fields'], runs_B.sha16_file(out)))
