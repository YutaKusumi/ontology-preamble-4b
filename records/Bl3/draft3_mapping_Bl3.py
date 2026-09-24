# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の草案3 の対応の記録を書く: 設計の巡・二巡目（最終検分）の採否表の各行（P667〜P698）を、草案3 のどこで受けたか。
- 採否表の行（採否・票・所見・案）は採否表から器が読む（打ち直さない）。受けた所（正本の鍵・草案3 の節・設計事実の鍵・草案3 の文の字句・露出の記録の字句）は起草者が並べ、器がその実在を確かめる。
- 近道の許容の下限（裁定 D219 の「下限は G2 の案の値」）は、正本の値を書式で文字列にし、G2 の票の逐語にその文字列があることを器が確かめる。
- 一つでも見つからなければ終了コードを立てる（受けたと書いたのに実物が無い型を捕まえる）。
出力: records/Bl3/draft3-mapping-Bl3.md
用法: python records/Bl3/draft3_mapping_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
AT = 'records/reviews/Bl3/design-round2/adoption-table-Bl3-design-r2.md'
G2 = 'records/reviews/Bl3/design-round2/gemini-2/review.md'
EX = 'records/Bl3/exposure-before-seal-Bl3.md'
T3 = json.load(open(j('design', 'contrasts-Bl3.json'), encoding='utf-8'))
FJ = json.load(open(j('records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
D3 = open(j('design', 'design-Bl3-draft3.md'), encoding='utf-8').read()
G2T = open(j(*G2.split('/')), encoding='utf-8').read()
EXT = open(j(*EX.split('/')), encoding='utf-8').read()
assert T3['version'].startswith('draft3')
rows = {}
for l in open(j(*AT.split('/')), encoding='utf-8'):
    m = re.match(r'^\| (P6\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|', l)
    if m:
        rows[m.group(1)] = {'votes': m.group(2).strip(), 'gist': m.group(3).strip(), 'kind': m.group(5).strip()}
assert min(rows) == 'P667' and max(rows) == 'P698' and len(rows) == int(max(rows)[1:]) - int(min(rows)[1:]) + 1, (len(rows), min(rows), max(rows))
# 受けた所: 正本の鍵（c:）・草案3 の節（s:）・設計事実の鍵（f:）・草案3 の字句（t:）・露出の記録の字句（r:）・正本の値が G2 の票の逐語にあるか（g:）。変えない行は「—」と理由
MAP = {
    'P667': ['—: 是認（半分にとどまった直しは下の行で受けた）'],
    'P668': ['—: 是認（変えない）'],
    'P669': ['—: 是認（除いた二つの出所は §15 に書いた）', 's:15', 't:二巡目の採否表 P669'],
    'P670': ['—: 是認（足りない印字は P681・P688・P689・P692 で受けた）'],
    'P671': ['c:decisions.D219', 'c:independent_recompute.what', 'c:independent_recompute.new_paths', 'c:independent_recompute.stages.first', 'c:independent_recompute.stages.second',
             'c:independent_recompute.tol_stage1', 'c:independent_recompute.agreement', 'c:independent_recompute.print', 'c:independent_recompute.on_mismatch', 's:12',
             'f:E.passes_recompute', 'f:E.tokens_recompute', 't:札の一致'],
    'P672': ['c:pilot.cache_tol_rule', 'c:pilot.cache_tol_factor', 'c:pilot.cache_tol_floor', 'c:pilot.noise_max', 'g:pilot.cache_tol_floor', 's:4', 't:上限 `pilot.noise_max` で頭打ちにした値'],
    'P673': ['c:decisions.D221', 'c:pilot.order', 'c:pilot.checks.vi.path', 'c:pilot.checks.vi.a', 'c:pilot.checks.vi.b', 'c:pilot.checks.vi.floor_rule', 'c:pilot.checks.vi.measures',
             'c:pilot.repeat_n', 'c:pilot.decision.rule', 'c:pilot.decision.q1_map', 'c:reading_rules', 'c:limits', 's:4', 's:9', 's:10', 'f:E.passes_noise_a', 'f:E.passes_noise_b',
             't:数値が定まらず測れなかった'],
    'P674': ['c:readout.primary.batching', 'f:E.batch_fill_main', 's:3', 's:6', 't:最後のバッチを零のベクトルで埋めて同じ形にし'],
    'P675': ['c:computation.steered_cache_check.rule', 'f:E.passes_cache', 's:12', 't:二つの道の効き目の差の絶対値の最大'],
    'P676': ['c:nulls.storage.rule', 'c:computation.self_checks.logit', 'c:computation.self_checks.layer', 'c:computation.self_checks.on_fail', 'c:computation.logit_tol', 'c:computation.layer_tol',
             'c:descriptive.layerwise.capture', 'f:D.npz_directions', 's:2', 's:8', 's:12', 't:二重の正規化を捕まえる'],
    'P677': ['c:decisions.D222', 'c:pilot.decision.tool_error.what', 'c:pilot.decision.tool_error.on_error', 'c:pilot.decision.tool_error.on_suspicion', 'c:pilot.decision.tool_error.decide',
             'c:pilot.decision.tool_error.rerun', 'c:computation.main_freeze_check', 'c:report_rules.template', 's:4', 's:12', 't:逸脱の台帳に記した器の差分だけ'],
    'P678': ['c:pilot.checks.iii', 'c:pilot.iii_sentences.positive', 'c:pilot.iii_sentences.not_positive', 'c:pilot.iii_sentences.undefined', 's:4', 't:同じ値は平均の順位',
             't:読み取りの値を段階 B の行動の率の代わりに読まない'],
    'P679': ['c:gate.dropped', 's:7', 't:残った単位の数の階乗'],
    'P680': ['c:decisions.D223', 'c:report_rules.template', 'c:limits', 's:10', 's:12', 't:床の近くの升目'],
    'P681': ['c:decisions.D220', 'c:readout.variants.V3', 'c:readout.variants.rule', 'c:readout.primary.copy_cue', 'c:pilot.checks.iv', 'c:reading_rules', 'c:print_strings.reading_never_ban', 'c:limits',
             'f:A.v3_head_same', 'f:A.outputs_with_v3_key', 's:3', 's:4', 's:9', 's:10', 't:揺れの版の値', 't:割り方の各片'],
    'P682': ['c:labels.second.ranks', 'c:limits', 's:5', 's:10', 't:行に不利な側'],
    'P683': ['c:labels.second.iso_top_share', 's:5', 't:行の偶然の目安ではない'],
    'P684': ['c:labels.side_rule', 's:5', 's:9', 't:下の四分位と上の四分位の間'],
    'P685': ['c:gate.descriptive_rule', 's:7', 's:9', 't:記述の門には型を当てない'],
    'P686': ['c:labels.print_rule', 's:5', 't:中心からどちらの側に離れたかを言わないので'],
    'P687': ['c:predictions.q7_rule', 'f:C.q7_intervals', 's:6', 's:11', 't:数えられる行が残らなければ採点しない', 't:区間が零を含み q7 で該当なしになる行'],
    'P688': ['c:gate.style_note', 'c:gate.style_hold_pt', 'f:C.style_share_pt', 's:6', 's:7', 't:閾値の値だけを借り', 't:門の行すべての JSON 直答の割合の差'],
    'P689': ['f:D.seeds_taken_n', 'f:E.batch', 's:6', 't:のどれとも重ならない', 't:同じ値であることを器が確かめた'],
    'P690': ['s:15', 't:器で見る前は、知る前ではなかった', 't:二巡目の事実の確かめ K476'],
    'P691': ['c:decisions.D218', 'c:numbering.rulings_next', 'r:## 扱いの決定（登録者裁定 D217）', '—: C2-R18 の言い直しは採否表の行に置いた（第一巡の採否表は書き換えない）'],
    'P692': ['c:cost.note', 'c:cost.colab_units_high', 'f:E.tokens_recompute', 'f:E.passes_secondary_noop', 's:14', 't:二段にした独立の再計算'],
    'P693': ['c:limits', 's:10', 't:段階 B で生成したトークンの並びと違うことがある'],
    'P694': ['c:review_plan.synthetic', 'c:review_plan.impl.focus', 's:12', 't:bf16 相当の揺れを入れた合成の模型', 't:合成データの確かめを検分者が実際に走らせ'],
    'P695': ['c:decisions.D218', 'c:decisions.D219', 'c:decisions.D220', 'c:decisions.D221', 'c:decisions.D222', 'c:decisions.D223', 'c:numbering.rulings_next',
             'c:inputs.files.rulings_D218', 'c:inputs.files.rulings_D219_D223', 'c:inputs.files.design_r2_adoption', 'c:inputs.files.design_r2_verification', 'c:drafter_values', 's:16'],
    'P696': ['—: 記録に置く（事実の言い直しは採否表の行・草案は変えない）'],
    'P697': ['—: 是認（既にある決まり）', 'c:predictions.free'],
    'P698': ['r:## 設計の巡・二巡目の票（最終検分）', 's:15', 't:露出の記録の二巡目の段'],
}
assert set(MAP) == set(rows), sorted(set(rows) ^ set(MAP))
assert T3['numbering']['rulings_next'] == 'D%d' % (max(int(k[1:]) for k in T3['decisions']) + 1), '次の裁定の番号が台帳の続きでない'


def canon_get(path):
    x = T3
    for k in path.split('.'):
        if isinstance(x, dict) and k in x:
            x = x[k]
        else:
            return None, False
    return x, True


def facts_has(path):
    row, key = path.split('.', 1)
    return row in FJ['facts'] and key in FJ['facts'][row]


def g2_has(path):
    v, ok = canon_get(path)
    return ok and ('%g' % v) in G2T


secs = set(re.findall(r'^## (\d+)\.', D3, flags=re.M))
out, bad = [], []
for p in sorted(MAP):
    checks = []
    for it in MAP[p]:
        kind, val = it.split(':', 1)
        ok = {'c': lambda v: canon_get(v)[1], 's': lambda v: v in secs, 'f': lambda v: facts_has(v), 't': lambda v: v in D3, 'r': lambda v: v in EXT, 'g': lambda v: g2_has(v), '—': lambda v: True}[kind](val)
        label = {'c': lambda v: '正本 `%s`' % v, 's': lambda v: '草案3 §%s' % v, 'f': lambda v: '設計事実 `%s`' % v, 't': lambda v: '草案3 の字句「%s」' % v.replace('|', '｜'),
                 'r': lambda v: '露出の記録の字句「%s」' % v, 'g': lambda v: '正本 `%s` の値（%g）が G2 の票にある' % (v, canon_get(v)[0]), '—': lambda v: v.strip()}[kind](val)
        checks.append((label, ok))
        if not ok:
            bad.append((p, label))
    r = rows[p]
    out.append('| %s | %s | %s | %s | %s |' % (p, r['votes'], r['kind'], '・'.join(l for l, _ in checks), '全て在る' if all(o for _, o in checks) else '**無いものがある**'))
L = ['# B-lens 層三の草案3 の対応の記録（機械で確かめた・`records/Bl3/draft3_mapping_Bl3.py`）', '',
     '- 採否表: `%s`（SHA16 %s）の行 %s〜%s。採否・票・所見・案は採否表から器が読んだ。' % (AT, s16(AT), min(rows), max(rows)),
     '- 受けた所: 正本 `design/contrasts-Bl3.json`（SHA16 %s・版 %s）・草案3 `design/design-Bl3-draft3.md`（SHA16 %s）・設計事実 `records/Bl3/design-facts-Bl3.json`（SHA16 %s）・露出の記録 `%s`（SHA16 %s）・G2 の票 `%s`（SHA16 %s）。受けた所は起草者が並べ、器がその実在を確かめた（中身の当否は確かめていない）。' % (
         s16('design/contrasts-Bl3.json'), T3['version'], s16('design/design-Bl3-draft3.md'), s16('records/Bl3/design-facts-Bl3.json'), EX, s16(EX), G2, s16(G2)),
     '- 次の裁定の番号（正本 `numbering.rulings_next`）が、正本の台帳の最後の番号の続きであることも器が確かめた。',
     '- 見つからなかったもの: %d 件。' % len(bad), '',
     '| 採否 | 票・所見 | 案 | 草案3 で受けた所 | 実在 |', '|---|---|---|---|---|'] + out + [
     '', '- 限界: この記録は、受けた所が在ることを確かめる。受け方が所見を取り違えていないか、半分しか直していないかは確かめない。二巡目は最終検分なので、この後に設計の巡は無く（裁定 D218）、受け方の当否は登録者の確認と器の実装の検分で見る。',
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'draft3-mapping-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('wrote draft3-mapping-Bl3.md | rows', len(out), '| missing', len(bad), bad[:5])
sys.exit(1 if bad else 0)
