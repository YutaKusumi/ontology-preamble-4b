# -*- coding: utf-8 -*-
"""bprime_core.py v0 —— B′ の計算の芯（numpy だけ・重みも試行も読まない・2026-09-30・コーディネータ南無弥勒如来）。

正本 `design/contrasts-Bprime.json` の決まりのうち、B′ で足した計算を、重みや試行を読まない純粋な関数に置く。札の計算と下見の決め（割合と裾・Holm・効き目の側・
二つ目の札・等方の最上位の割合・(vi) の分岐・(i)(ii) の升目の決め・較正の文・下見のやり直しの流れ・バッチの組み方）は、層三の凍結の芯 `bl3_core`（公開の置き場の版）を
読み取りだけで呼ぶ（同じ式を二度書かない）。走らせる器・集計の器・報告の組み立ての器・合成データの器が、同じ関数を呼ぶ。

置くもの（正本の鍵）:
  - 出口の値の自己検査の許容（`computation.self_checks.logit`）: bf16 の刻み・tol(z)＝k × u(z)・k の測り方と assert（z₀ の切り替え）・三つの道の判定（合・否・見分ける力無し）。
  - 床の余白の印（`floor_margin.mark`）。
  - 全体の要約の数と文（`reading.summary`）と、その assert。
  - 率の区間（`behavior_pilot.rate.interval`）: 連続性の補正なしの Wilson のスコアの区間。
  - 書き出しの根の件数（`behavior_pilot.root_counts`）: (a) 文字列と番号の件数・(b) 頭の振り分け（八つの区分）と続きの振り分け・(c) コードブロックの数・(d) 頭の七つ・(e) 次の番号・定型の文の選び方。
  - 「採点できなかった」割合の上限（`behavior_pilot.scoring.unscorable`）。
  - 封印の後の止め（`computation.stops`）: G4 の日の数え方・暦の期限。
  - 本の凍結で足してよい鍵の確かめ（`computation.main_freeze.allowed_keys`）。
  - 報告の走査（`scan`）: 決まった文字列の行の一字違わない一致・自由の文の禁止の語と「層三」「Qwen」と数と「区別でき」の走査。
用法: python tools/bprime_core.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, math, json, datetime
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.environ.get('OP4B_PUBLIC_REPO', 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b')
sys.path.insert(0, os.path.join(PUB, 'tools'))
import bl3_core as K3                                                   # 層三の凍結の芯（読むだけ・呼ぶだけ）

VERSION = 'v0.1'        # v0.1（2026-09-30）: (b) の頭の振り分けの起点を外から渡せるようにした（凍結の採点の器が読む塊の中の鍵・所見 K6）。前の版は `prev/bprime_core-v0.py`
KEY = '"choice"'
FENCE = '```'
SIDES = ('stronger', 'weaker', 'opposite', 'sign_only')
CLASSES = ('主', 'V1', 'V2', 'V3', '囲いあり候補外', '囲いなし候補外', '鍵あり値の頭が候補外', '鍵なし')


class ToolError(Exception):
    """凍結した確かめが機械で落ちた（器の誤り）。"""


# ---------------- 出口の値の自己検査の許容 ----------------
def ulp_bf16(x):
    """bf16 の刻み: |x| を bf16 で表したときの隣り合う二つの数の間隔（正の有限の値だけ・零は ToolError）。"""
    a = np.abs(np.asarray(x, dtype=np.float64))
    if np.any(~np.isfinite(a)) or np.any(a <= 0):
        raise ToolError('bf16 の刻みは正の有限の値にだけ定まる')
    return np.power(2.0, np.floor(np.log2(a)) - 7)


def u_of(z, z0):
    """u(z)＝|z| と z₀ の大きい方の bf16 の刻み（正本 `computation.self_checks.logit.tol_form`）。"""
    return ulp_bf16(np.maximum(np.abs(np.asarray(z, dtype=np.float64)), float(z0)))


def measure_k(diffs, zs, z0, factor):
    """k＝〈差 ÷ u(z)〉の最大の倍率倍。diffs: 模型の出口と float32 で当て直した値（softcap あり）の差の絶対値・zs: 模型の出口の値。"""
    d = np.abs(np.asarray(diffs, dtype=np.float64))
    return float(factor * np.max(d / u_of(zs, z0)))


def k_with_asserts(diffs, zs, L):
    """正本 `computation.self_checks.logit`（L）の測り方と assert: |z| ≥ big_z の行が足りれば z₀、足りなければ z₀ の切り替え。戻り値: {'z0','k','big_rows','fallback'}。
    assert が落ちたら ToolError（凍結しない・登録者に上げる）。"""
    A = L['measure']['asserts']
    zs = np.asarray(zs, dtype=np.float64)
    big = int(np.sum(np.abs(zs) >= A['big_z']))
    if big >= A['big_z_rows_min']:
        z0, kmax, fb = L['z0'], A['k_max'], False
    else:
        z0, kmax, fb = L['z0_fallback'], A['k_max_fallback'], True
    k = measure_k(diffs, zs, z0, L['tolerance_factor'])
    if not k <= kmax:
        raise ToolError('許容の k が上限を超えた（k=%.4g・上限 %s・z₀=%s）' % (k, kmax, z0))
    return {'z0': z0, 'k': k, 'big_rows': big, 'fallback': fb}


def softcap(r, cap):
    return cap * np.tanh(np.asarray(r, dtype=np.float64) / cap)


def logit_self_check(z_model, z_on, z_off, z_dbl, k, z0, disc):
    """一つの位置の三つの道の判定（正本 `computation.self_checks.logit.rule`）。
    z_model: 模型の出口の値（bf16 を float64 にしたもの）・z_on: softcap あり・z_off: softcap なし（softcap の前の値）・z_dbl: 正規化の二重（softcap あり）。
    「あり」は掛けたすべての行で |z_model − z_on| ≤ tol。「なし」「二重」は、見込みの差（なし: |z_off − z_on|・二重: |z_dbl − z_on|）が tol の disc 倍を超える行だけに掛け、
    その行の中の最大の |z_model − 間違った道| が tol を超えることを求める。見分けに使える行が無い道は「見分ける力無し」。
    戻り値: {'on': bool, 'off': 'pass'|'fail'|'none', 'dbl': …, 'state': '合'|'否'|'見分ける力無し'}。"""
    zm = np.asarray(z_model, dtype=np.float64)
    tol = k * u_of(zm, z0)
    out = {'on': bool(np.all(np.abs(zm - np.asarray(z_on)) <= tol))}
    for name, wrong in (('off', z_off), ('dbl', z_dbl)):
        wrong = np.asarray(wrong, dtype=np.float64)
        use = np.abs(wrong - np.asarray(z_on, dtype=np.float64)) > disc * tol
        if not np.any(use):
            out[name] = 'none'
        else:
            out[name] = 'pass' if bool(np.max(np.abs(zm[use] - wrong[use]) - tol[use]) > 0) else 'fail'
    if not out['on'] or 'fail' in (out['off'], out['dbl']):
        out['state'] = '否'
    elif 'none' in (out['off'], out['dbl']):
        out['state'] = '見分ける力無し'
    else:
        out['state'] = '合'
    return out


# ---------------- 床の余白の印 ----------------
def logit(p):
    return float(math.log(p / (1.0 - p)))


def floor_mark(lo_noop, p_bounds, vi_a_cell, vi_b_max):
    """床の余白の印（正本 `floor_margin.mark`）: 床と天井からの余白の近い方が〈その升目の (vi) の (a) の値と (vi) の (b) の升目の間の最大の、大きい方〉より小さいとき印。"""
    lo_f, hi_f = logit(p_bounds[0]), logit(p_bounds[1])
    margin = min(float(lo_noop) - lo_f, hi_f - float(lo_noop))
    target = max(float(vi_a_cell), float(vi_b_max))
    return {'mark': bool(margin < target), 'margin': margin, 'target': target}


# ---------------- 全体の要約 ----------------
def summary_numbers(rows):
    """rows: 残った主の行 [{'direction': 'static'|'Nk', 'iso_outside', 'second', 'mark', 'side'}]（side は等方の外の行だけ）。
    戻り値: 要約の数（正本 `reading.summary` の〔〕）。assert（`reading.summary.asserts`）が落ちたら ToolError。"""
    n = len(rows)
    iso = [r for r in rows if r['iso_outside']]
    non = [r for r in rows if not r['iso_outside']]
    k = len(iso)
    a1 = sum(1 for r in iso if not r['mark'] and r['direction'] == 'static')
    a2 = sum(1 for r in iso if not r['mark'] and r['direction'] == 'Nk')
    b1 = sum(1 for r in iso if r['mark'] and r['direction'] == 'static')
    b2 = sum(1 for r in iso if r['mark'] and r['direction'] == 'Nk')
    m = b1 + b2
    j = sum(1 for r in iso if r['second'])
    s = {x: sum(1 for r in iso if r.get('side') == x) for x in SIDES}
    j0 = sum(1 for r in non if r['second'])
    N = {'n': n, 'k': k, 'k0': k - m, 'm': m, 'a1': a1, 'a2': a2, 'b1': b1, 'b2': b2, 'j': j, 'j0': j0, 'n−k': n - k,
         's1': s['stronger'], 's2': s['weaker'], 's3': s['opposite'], 's4': s['sign_only']}
    ok = (a1 + a2 + b1 + b2 == k and m == b1 + b2 and j <= k and N['s1'] + N['s2'] + N['s3'] + N['s4'] == k and j0 <= n - k
          and all(r['direction'] in ('static', 'Nk') for r in rows))
    if not ok:
        raise ToolError('要約の数の assert が落ちた: %s' % N)
    return N


def fill(template, values):
    """〔名〕を値で埋める（名が無ければ ToolError・埋めた後に〔〕が残れば ToolError）。"""
    def rep(mo):
        key = mo.group(1)
        if key not in values:
            raise ToolError('埋める値が無い: %s' % key)
        return str(values[key])
    out = re.sub(r'〔([^〔〕]+)〕', rep, template)
    if '〔' in out or '〕' in out:
        raise ToolError('埋め残しがある')
    return out


def summary_sentences(S, N):
    """要約の文（正本 `reading.summary`・S）。k が 1 以上なら三つの文、零なら零のときの文と三つ目の文。"""
    if N['k'] >= 1:
        return [fill(t, N) for t in S['k_pos']]
    return [fill(S['k_zero_first'], N), fill(S['k_pos'][2], N)]


# ---------------- 率の区間 ----------------
def wilson(k, n, z):
    """Wilson のスコアの区間（連続性の補正なし）。n が零なら (None, None)。"""
    if n == 0:
        return (None, None)
    p = k / n
    den = 1 + z * z / n
    cen = (p + z * z / (2 * n)) / den
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, cen - hw), min(1.0, cen + hw))


# ---------------- 書き出しの根の件数 ----------------
def variant_strings(prefix):
    """揺れの版の文字列（層三の転記行 A の定義）: V1＝コードブロックの行を除く・V2＝選択の鍵の前に改行と字下げ・V3＝選択の鍵の後の空白を除く。"""
    first_nl = prefix.index('\n') + 1
    v1 = prefix[first_nl:]
    v2 = prefix.replace('{' + KEY, '{\n  ' + KEY, 1)
    v3 = prefix.replace(KEY + ': "', KEY + ':"', 1)
    if len({prefix, v1, v2, v3}) != 4:
        raise ToolError('揺れの版の文字列が主と重なる')
    return {'主': prefix, 'V1': v1, 'V2': v2, 'V3': v3}


def subseq_positions(seq, sub):
    """seq の中に sub が並びとして現れる位置（始まりの添字）の並び。"""
    n, m = len(seq), len(sub)
    return [i for i in range(0, n - m + 1) if list(seq[i:i + m]) == list(sub)]


def opening_fences(text):
    """生成した部分の頭から数えて奇数番目の '```' の位置（開く囲い）。"""
    pos, out, i = [], [], 0
    while True:
        j = text.find(FENCE, i)
        if j < 0:
            break
        pos.append(j)
        i = j + len(FENCE)
    return [p for q, p in enumerate(pos) if q % 2 == 0]


def block_fence(text, ki):
    """鍵を含むブロックの開く囲い（器の段の所見 K1）: 鍵の手前の '```' の数が奇数のとき、その最後の '```'（鍵は開いたブロックの中）。偶数なら None（鍵はどのブロックの中にも無い）。
    正本の「奇数番目の '```'」を字のとおりに当てると、鍵より前で閉じた別のブロックの開く囲いを拾うので、三巡目の直し（A7-17）の狙いに合わせてこう定める。"""
    before, i = [], 0
    while True:
        j = text.find(FENCE, i)
        if j < 0 or j >= ki:
            break
        before.append(j)
        i = j + len(FENCE)
    return before[-1] if len(before) % 2 == 1 else None


def classify_head(text, strings, window, ki=None):
    """(b) 頭の振り分け（正本 `behavior_pilot.root_counts.b`）。strings: variant_strings の戻り値。
    ki: 起点にする鍵の位置（凍結の採点の器が読む塊の中の鍵・`bprime_behavior.scorer_key` が決める・器の段の所見 K6）。None なら本文の最後の鍵。
    戻り値: {'class': 八つのどれか, 'head_end': 頭の終わりの位置か None, 'n_keys': 鍵の数, 'cont': 続きの振り分けか None}。"""
    n_keys = text.count(KEY)
    if n_keys == 0:
        return {'class': '鍵なし', 'head_end': None, 'n_keys': 0, 'cont': None}
    if ki is None:
        ki = text.rfind(KEY)
    elif not (0 <= ki and text.startswith(KEY, ki)):
        raise ToolError('起点の位置に選択の鍵が無い')
    ke = ki + len(KEY)
    if text.startswith(': "', ke):
        he = ke + 3
    elif text.startswith(':"', ke):
        he = ke + 2
    else:
        return {'class': '鍵あり値の頭が候補外', 'head_end': None, 'n_keys': n_keys, 'cont': None}
    fence = block_fence(text, ki)
    if fence is not None and ki - window <= fence:
        head = text[fence:he]
        cls = next((c for c in ('主', 'V2', 'V3') if head == strings[c]), '囲いあり候補外')
    else:
        cls = 'V1' if (ki >= 1 and text[ki - 1] == '{' and text[ki - 1:he] == strings['V1']) else '囲いなし候補外'
    return {'class': cls, 'head_end': he, 'n_keys': n_keys, 'cont': continuation(text[he:])}


def continuation(rest):
    """頭の後の続き（正本 `behavior_pilot.root_counts.b.continuation`）: 答えの形・雛形の写しの形・切れた・候補外。"""
    m = re.match(r'(refuse|[a-z])', rest)
    if not m:
        return '切れた' if rest == '' or 'refuse'.startswith(rest) else '候補外'
    after = rest[m.end():]
    if after == '':
        return '切れた'
    if not after.startswith('"'):
        return '候補外' if not ('refuse'.startswith(rest) and m.group(1) == 'r') else '切れた'
    if after[1:2] == '':
        return '切れた'
    return '雛形の写しの形' if after[1:2] == '|' else '答えの形'


def code_blocks(text):
    """(c) JSON のコードブロックの数（開く囲いの後が json の札のもの）と、閉じていないブロックの有無。"""
    opens = opening_fences(text)
    n_fence = text.count(FENCE)
    n_json = sum(1 for p in opens if text[p + len(FENCE):p + len(FENCE) + 4].lower() == 'json')
    return {'n_json': n_json, 'bucket': '一' if n_json == 1 else ('二' if n_json == 2 else ('三以上' if n_json >= 3 else '零')), 'unclosed': bool(n_fence % 2 == 1)}


def head_cut(text, strings):
    """頭の途中で切れた（生成した部分が、最後の開く囲いから始まる候補の頭の真の途中で終わる）。"""
    opens = opening_fences(text)
    tail = text[opens[-1]:] if opens else text
    return any(len(tail) < len(s) and s.startswith(tail) and len(tail) > 0 for s in strings.values())


def root_counts_one(text, gen_ids, prefix_ids, strings, set_head_ids, window, ki=None):
    """一つの応答の (a)〜(e)。gen_ids は `<channel|>` の直後から生成したトークンの番号（止める印の手前まで）。ki は (b) の起点（classify_head と同じ）。"""
    pos = subseq_positions(gen_ids, prefix_ids)
    b = classify_head(text, strings, window, ki=ki)
    if pos:
        nxt_i = pos[-1] + len(prefix_ids)
        e = 'none' if nxt_i >= len(gen_ids) else ('set' if gen_ids[nxt_i] in set_head_ids else 'other')
    else:
        e = None
    return {'a_str': strings['主'] in text, 'a_tok': bool(pos), 'b': b, 'c': code_blocks(text), 'c_head_cut': head_cut(text, strings),
            'd': list(gen_ids[:len(prefix_ids)]) == list(prefix_ids), 'e': e}


def root_counts_cell(items, window):
    """升目の件数の集計（分母は試行の全件）。items: root_counts_one の戻り値の並び。(a) の番号の件数が文字列の件数を上回ったら、その欄だけ器の誤りの印。"""
    n = len(items)
    a_str = sum(1 for x in items if x['a_str'])
    a_tok = sum(1 for x in items if x['a_tok'])
    cls = {c: sum(1 for x in items if x['b']['class'] == c) for c in CLASSES}
    if sum(cls.values()) != n:
        raise ToolError('頭の振り分けの和が分母と違う')
    cont = {}
    for x in items:
        key = x['b']['cont'] if x['b']['cont'] is not None else '続きは数えない'
        cont[key] = cont.get(key, 0) + 1
    e = {}
    for x in items:
        if x['e'] is not None:
            e[x['e']] = e.get(x['e'], 0) + 1
    return {'n': n, 'a_str': a_str, 'a_tok': a_tok, 'a_tok_error': bool(a_tok > a_str), 'classes': cls, 'cont': cont,
            'multi_key': sum(1 for x in items if x['b']['n_keys'] >= 2), 'c_json': {k: sum(1 for x in items if x['c']['bucket'] == k) for k in ('零', '一', '二', '三以上')},
            'c_unclosed': sum(1 for x in items if x['c']['unclosed']), 'c_head_cut': sum(1 for x in items if x['c_head_cut']),
            'd': sum(1 for x in items if x['d']), 'e': e}


def root_sentence_choice(cell):
    """定型の文の選び方（正本 `fixed_sentences.root_counts.choose`）: one・two・three のちょうど一つと、four を置くか。"""
    main = 'two' if cell['d'] > 0 else ('three' if cell['a_str'] > 0 else 'one')
    return {'main': main, 'four': bool(cell['a_str'] != cell['a_tok'] and not cell['a_tok_error'])}


# ---------------- 採点できなかった割合 ----------------
def unscorable_exceeds(counts, U):
    """主の八升目のどれかで「採点できなかった」件数が `count_min` 以上（割合が `max_share` を超える）なら真。counts: 升目 → (件数, 分母)。"""
    bad = []
    for c, (k, n) in counts.items():
        over_share = k / n > U['max_share'] if n else True
        over_count = k >= U['count_min']
        if over_share != over_count and n == 40:
            raise ToolError('割合と件数の決まりが食い違う: %s %s/%s' % (c, k, n))
        if over_share:
            bad.append(c)
    return {'exceeds': bool(bad), 'cells': sorted(bad)}


# ---------------- 封印の後の止め ----------------
def jst_date(ts):
    """日本時間の時刻（'YYYY-MM-DD HH:MM[:SS]' か ISO の文字列）→ 日本時間の暦日（date）。"""
    t = ts.replace('T', ' ')[:19]
    fmt = '%Y-%m-%d %H:%M:%S' if len(t) >= 19 else '%Y-%m-%d %H:%M'
    return datetime.datetime.strptime(t, fmt).date()


def g4_days(attempts, seal_jst):
    """G4 の日の数え方（正本 `computation.stops.g4.rule`）。attempts: [{'time_jst','success'}]（封印の後の試みの記録）。
    起点は封印の後の最初の失敗。数えるのは、起点の日から、試みを記録しその日に G4 が一度も割り当てられなかった日本時間の暦日だけ。段をまたいで通算し、数え直さない。"""
    seal = jst_date(seal_jst)
    after = sorted([a for a in attempts if jst_date(a['time_jst']) >= seal], key=lambda a: a['time_jst'])
    fails = [a for a in after if not a['success']]
    if not fails:
        return {'days': 0, 'dates': []}
    start = jst_date(fails[0]['time_jst'])
    by_date = {}
    for a in after:
        d = jst_date(a['time_jst'])
        if d >= start:
            by_date.setdefault(d, []).append(a['success'])
    dates = sorted(d for d, v in by_date.items() if not any(v))
    return {'days': len(dates), 'dates': [d.isoformat() for d in dates]}


def calendar_closed(seal_jst, now_jst, days, done):
    """暦の期限（正本 `computation.stops.calendar`）: 封印の日（日本時間）を 0 日目として、days 日目の日本時間の暦日の終わりまでに本の計算と独立の再計算を終えなかったら閉じる。"""
    if done:
        return False
    return (jst_date(now_jst) - jst_date(seal_jst)).days > int(days)


# ---------------- 本の凍結で足してよい鍵 ----------------
def main_freeze_keys_ok(added_keys, allowed):
    """足した鍵が一覧の内か（正本 `computation.main_freeze.allowed_keys`）。allowed: 段 → 鍵の名の並び。戻り値: 一覧の外の鍵の並び（空なら通る）。"""
    ok = set()
    for v in allowed.values():
        if isinstance(v, list):
            ok |= set(v)
    return sorted(k for k in added_keys if k not in ok)


# ---------------- 報告の走査 ----------------
NUM = re.compile(r'(?<![A-Za-z0-9_.,])[−\-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?')


def fixed_line_ok(line, template, values):
    """決まった文字列から組んだ行が、〔〕を埋めた正本の文字列と一字違わず一致するか。"""
    try:
        return line == fill(template, values)
    except ToolError:
        return False


def free_text_hits(line, bans, allowed_numbers, masks=()):
    """自由の文の走査: 禁止の語・「層三」「Qwen」・置いてよい数の外の数・「区別でき」の当たりを並べる（空なら通る）。"""
    hits = [('ban', w) for w in bans if w in line]
    for w in ('層三', 'Qwen', '区別でき'):
        if w in line:
            hits.append(('word', w))
    t = line
    for rx in masks:
        t = rx.sub(lambda mo: ' ' * len(mo.group(0)), t)
    for mo in NUM.finditer(t):
        tok = mo.group(0)
        if tok not in allowed_numbers:
            hits.append(('number', tok))
    return hits


# ---------------- 自己検査（合成の値） ----------------
def _bf16(x):
    x = np.asarray(x, dtype=np.float32)
    b = x.view(np.uint32).astype(np.uint64)
    r = ((b + 0x7FFF + ((b >> 16) & 1)) >> 16) << 16
    return r.astype(np.uint32).view(np.float32)


def _selftest():
    CT = json.load(open(os.path.join(os.path.dirname(HERE), 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    L = CT['computation']['self_checks']['logit']
    n_ok = 0
    # 1. 刻みと許容の床
    assert ulp_bf16(4.0) == 2.0 ** -5 and ulp_bf16(1.0) == 2.0 ** -7 and ulp_bf16(20.0) == 2.0 ** -3
    assert float(u_of(0.0, 4)) == 2.0 ** -5 and float(u_of(-30.0, 4)) == 2.0 ** -3
    try:
        ulp_bf16(0.0); raise AssertionError('零で止まらない')
    except ToolError:
        pass
    n_ok += 1
    # 2. bf16 の丸めを模した道: 正しい実装が「あり」を通り、抜けと二重が落ちる（T04・合成データ）。床の無い形では k が大きく膨らむ
    rng = np.random.default_rng(20260930)
    D, V, cap = 512, 4000, 30.0
    W = _bf16(rng.standard_normal((V, D)).astype(np.float32) * 0.09)
    w = (rng.standard_normal(D) * 0.3).astype(np.float32)
    rms = lambda x: x / np.sqrt(np.mean(x.astype(np.float32) ** 2) + 1e-6) * (1 + w)
    diffs, zs, trips = [], [], []
    for t in range(40):
        h = _bf16(rng.standard_normal(D).astype(np.float32) * 3.0)
        if t % 2 == 1:
            h = h + _bf16((W[t % 5] * 40.0).astype(np.float32))
        hn = _bf16(rms(h))
        zr = _bf16(W.astype(np.float32) @ hn.astype(np.float32))
        zm = _bf16(_bf16(np.tanh(_bf16(zr / cap))) * cap).astype(np.float64)
        r32 = (W.astype(np.float32) @ rms(h).astype(np.float32)).astype(np.float64)
        z_on = softcap(r32, cap)
        hn2 = rms(rms(h).astype(np.float32))
        z_dbl = softcap((W.astype(np.float32) @ hn2.astype(np.float32)).astype(np.float64), cap)
        diffs.append(np.abs(zm - z_on)); zs.append(zm); trips.append((zm, z_on, r32, z_dbl))
    d_all, z_all = np.concatenate(diffs), np.concatenate(zs)
    k_nofloor = float(2 * np.max(d_all / ulp_bf16(np.maximum(np.abs(z_all), 1e-30))))
    kk = k_with_asserts(d_all, z_all, L)
    assert k_nofloor > 10 * kk['k'], ('床の無い形の k が膨らまない', k_nofloor, kk)
    states = [logit_self_check(zm, z_on, r32, z_dbl, kk['k'], kk['z0'], L['discrimination_factor']) for zm, z_on, r32, z_dbl in trips]
    assert all(s['on'] for s in states), '正しい実装が「あり」で落ちた'
    assert any(s['off'] == 'pass' for s in states) and not any(s['off'] == 'fail' for s in states), ('抜けを見分けられない', [s['off'] for s in states])
    assert not any(s['dbl'] == 'fail' for s in states)
    # 誤った実装（softcap の抜け）を正しい道と取り違えると「あり」が落ちる
    zm, z_on, r32, z_dbl = trips[1]
    bad = logit_self_check(zm, r32, r32, z_dbl, kk['k'], kk['z0'], L['discrimination_factor'])
    assert not bad['on'] and bad['state'] == '否'
    # 小さい値だけの位置では見分ける力が無い（止めずに印字する側）
    small = np.linspace(-2, 2, 50)
    s = logit_self_check(small, small, small + 1e-9, small, kk['k'], kk['z0'], L['discrimination_factor'])
    assert s['state'] == '見分ける力無し'
    n_ok += 1
    # 3. k の assert と切り替え
    A = L['measure']['asserts']
    z_small = np.full(100, 2.0)
    fb = k_with_asserts(np.full(100, 1e-4), z_small, L)
    assert fb['fallback'] and fb['z0'] == L['z0_fallback']
    try:
        k_with_asserts(np.full(100, 10.0), np.full(100, 20.0), L); raise AssertionError('k の上限で止まらない')
    except ToolError:
        pass
    n_ok += 1
    # 4. 床の余白の印（層三の最終版の二つの升目の数・負の例・ちょうど同じ）
    FM = CT['pilot']['p_bounds']
    r1 = floor_mark(-8.783, FM, 0.6899, 0.0)
    assert r1['mark'] and abs(r1['margin'] - 0.4270) < 1e-3
    r2 = floor_mark(-5.0, FM, 0.6899, 0.0)
    assert not r2['mark']
    lo_eq = logit(FM[0]) + 0.5
    assert not floor_mark(lo_eq, FM, 0.5, 0.2)['mark'] and floor_mark(lo_eq, FM, 0.5000001, 0.2)['mark']
    n_ok += 1
    # 5. 要約の数と文
    S = CT['reading']['summary']
    rows = [{'direction': 'static', 'iso_outside': True, 'second': True, 'mark': True, 'side': 'sign_only'},
            {'direction': 'Nk', 'iso_outside': True, 'second': False, 'mark': False, 'side': 'stronger'},
            {'direction': 'static', 'iso_outside': False, 'second': True, 'mark': False},
            {'direction': 'Nk', 'iso_outside': False, 'second': False, 'mark': False}]
    N = summary_numbers(rows)
    assert (N['n'], N['k'], N['k0'], N['m'], N['a1'], N['a2'], N['b1'], N['b2'], N['j'], N['j0'], N['s1'], N['s4']) == (4, 2, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1)
    sen = summary_sentences(S, N)
    assert len(sen) == 3 and '〔' not in ''.join(sen)
    N0 = summary_numbers([dict(r, iso_outside=False, side=None) for r in rows])
    sen0 = summary_sentences(S, N0)
    assert len(sen0) == 2 and sen0[0].startswith('どの主の行でも')
    try:
        summary_numbers([{'direction': 'loaded', 'iso_outside': False, 'second': False, 'mark': False}]); raise AssertionError('方向の assert が落ちない')
    except ToolError:
        pass
    n_ok += 1
    # 6. Wilson（公開の置き場の器 `confirm_A.wilson` と同じ式で、丸めの前の値を比べる）
    lo, hi = wilson(12, 40, CT['behavior_pilot']['rate']['interval']['z'])
    p = 12 / 40; zc = CT['behavior_pilot']['rate']['interval']['z']; den = 1 + zc * zc / 40
    assert abs(lo - ((p + zc * zc / 80) / den - zc * math.sqrt(p * (1 - p) / 40 + zc * zc / 6400) / den)) < 1e-12 and wilson(0, 0, zc) == (None, None)
    n_ok += 1
    # 7. 書き出しの根の件数（合成の応答）
    st = variant_strings(CT['readout']['primary']['prefix_text'])
    assert st['V1'] == '{"choice": "' and st['V2'] == '```json\n{\n  "choice": "' and st['V3'] == '```json\n{"choice":"'
    W64 = CT['behavior_pilot']['root_counts']['b']['window_chars']
    cases = {
        '推論の後の JSON': ('理由は…です。\n```json\n{"choice": "b", "amount": 0}\n```', '主', '答えの形'),
        '字下げした JSON': ('考え…\n```json\n{\n  "choice": "c"}\n```', 'V2', '答えの形'),
        '空白の無い鍵': ('```json\n{"choice":"a","amount":3}\n```', 'V3', '答えの形'),
        'V1 の形だけ': ('答え: {"choice": "b"}', 'V1', '答えの形'),
        '言語の札が大文字': ('```JSON\n{"choice": "b"}\n```', '囲いあり候補外', '答えの形'),
        'choice が二番目の鍵': ('```json\n{"amount": 0, "choice": "b"}\n```', '囲いあり候補外', '答えの形'),
        '雛形の写し': ('```json\n{"choice": "a"|"b"|"c"|"refuse"}\n```', '主', '雛形の写しの形'),
        '頭の途中の打ち切り': ('```json\n{"choi', '鍵なし', None),
        '値の手前で切れた': ('```json\n{"choice": "', '主', '切れた'),
        '鍵の後が候補外': ('```json\n{"choice" = "b"}\n```', '鍵あり値の頭が候補外', None),
        '閉じる囲いが手前にある（V1 の形）': ('```json\n{"x": 1}\n```\n{"choice": "b"}', 'V1', '答えの形'),
        '閉じる囲いが手前にある（候補外）': ('```json\n{"x": 1}\n```\n{ "choice": "b"}', '囲いなし候補外', '答えの形'),
        '鍵が開いたブロックの中で囲いが遠い（V1 の形）': ('```json\n' + ' ' * 70 + '{"choice": "b"}', 'V1', '答えの形'),
        '鍵が開いたブロックの中で囲いが遠い（候補外）': ('```json\n' + ' ' * 70 + '{ "choice": "b"}', '囲いなし候補外', '答えの形'),
        'コードブロック二つ・鍵が二度': ('```json\n{"choice": "a"}\n```\n後で直す\n```json\n{"choice": "c"}\n```', '主', '答えの形'),
        '鍵なし': ('答えは (b) です。', '鍵なし', None),
    }
    for name, (txt, want, cont) in cases.items():
        got = classify_head(txt, st, W64)
        assert got['class'] == want and got['cont'] == cont, (name, got)
    assert classify_head('```json\n{"choice": "a"}\n```\n```json\n{"choice": "c"}\n```', st, W64)['n_keys'] == 2
    assert head_cut('```json\n{"choi', st) and not head_cut('```json\n{"choice": "b"}', st)
    assert code_blocks('```json\n{}\n```\n```json\n{}')['unclosed'] and code_blocks('```json\n{}\n```')['bucket'] == '一'
    pid = CT['readout']['primary']['prefix_ids']
    one = root_counts_one('```json\n{"choice": "b"}', pid + [236763, 5], pid, st, {236746, 236763, 236755, 1811}, W64)
    assert one['a_str'] and one['a_tok'] and one['d'] and one['e'] == 'set'
    two = root_counts_one('前置き```json\n{"choice": "b"}', [9, 9] + pid + [7], pid, st, {236746}, W64)
    assert two['a_tok'] and not two['d'] and two['e'] == 'other'
    three = root_counts_one('```json\n{"choice": "', pid, pid, st, {236746}, W64)
    assert three['e'] == 'none'
    cell = root_counts_cell([one, two, three], W64)
    assert cell['n'] == 3 and cell['d'] == 2 and cell['a_tok'] == 3 and not cell['a_tok_error']
    assert root_sentence_choice(cell)['main'] == 'two'
    assert root_sentence_choice(dict(cell, d=0))['main'] == 'three' and root_sentence_choice(dict(cell, d=0, a_str=0, a_tok=0))['main'] == 'one'
    assert root_sentence_choice(dict(cell, a_tok=2))['four']
    n_ok += 1
    # 8. 採点できなかった割合
    U = CT['behavior_pilot']['scoring']['unscorable']
    assert not unscorable_exceeds({'N1|O-Ncold': (4, 40)}, U)['exceeds'] and unscorable_exceeds({'N1|O-Ncold': (5, 40)}, U)['exceeds']
    n_ok += 1
    # 9. G4 の日の数え方と暦の期限
    seal = '2026-10-10 12:00'
    att = [{'time_jst': '2026-10-11 09:00', 'success': True}, {'time_jst': '2026-10-12 09:00', 'success': False}, {'time_jst': '2026-10-12 21:00', 'success': True},
           {'time_jst': '2026-10-13 10:00', 'success': False}, {'time_jst': '2026-10-13 22:00', 'success': False}, {'time_jst': '2026-10-15 10:00', 'success': False}]
    g = g4_days(att, seal)
    assert g['days'] == 2 and g['dates'] == ['2026-10-13', '2026-10-15'], g
    CAL = CT['computation']['stops']['calendar']['days']
    assert not calendar_closed(seal, '2026-12-09 23:59', CAL, False) and calendar_closed(seal, '2026-12-10 00:01', CAL, False) and not calendar_closed(seal, '2027-01-01 00:00', CAL, True)
    n_ok += 1
    # 10. 本の凍結の鍵と走査
    allowed = CT['computation']['main_freeze']['allowed_keys']
    assert main_freeze_keys_ok(['転記行 D', '機械の決定'], allowed) == [] and main_freeze_keys_ok(['効き目'], allowed) == ['効き目']
    bans = CT['print_strings']['added_ban_bprime'] + CT['print_strings']['free_text_ban_bprime']
    assert free_text_hits('Gemma の方が区別できた行がより多い', bans, set()) and not free_text_hits('結果は表のとおり。', bans, set())
    assert ('number', '12') in free_text_hits('12 行だった', [], set()) and not free_text_hits('12 行だった', [], {'12'})
    t0 = CT['fixed_sentences']['root_counts']['two']
    assert fixed_line_ok(fill(t0, {'升目': 'N1|O-Ncold', '件数': 3}), t0, {'升目': 'N1|O-Ncold', '件数': 3}) and not fixed_line_ok('ちがう', t0, {'升目': 'x', '件数': 1})
    n_ok += 1
    # 11. 凍結の芯を呼ぶ所（層三の関数がそのまま使えること）
    d = K3.vi_decision(0.02, 0.001, CT['pilot']['noise_max'], CT['readout']['primary']['batch'])
    assert d['batch'] == 1 and not d['stop']
    assert K3.iii_sentence(0.3) == 'positive' and K3.iii_sentence(float('nan')) == 'undefined'
    n_ok += 1
    print('bprime_core.py %s SELFTEST PASS（%d 群・床の無い形の k %.1f・床つきの k %.3f・z₀ %s）' % (VERSION, n_ok, k_nofloor, kk['k'], kk['z0']))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    print(__doc__)
