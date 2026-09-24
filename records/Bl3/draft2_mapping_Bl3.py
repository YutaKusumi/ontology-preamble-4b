# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の草案2 の対応の記録を書く: 設計の巡・第一巡の採否表の各行（P620〜P666）を、草案2 のどこで受けたか。
- 採否表の行（採否・票・所見・案）は採否表から器が読む（打ち直さない）。受けた所（正本の鍵・草案2 の節・設計事実の鍵・草案2 の文の字句）は起草者が並べ、器がその実在を確かめる。
- 一つでも見つからなければ終了コードを立てる（受けたと書いたのに実物が無い型を捕まえる）。
出力: records/Bl3/draft2-mapping-Bl3.md
用法: python records/Bl3/draft2_mapping_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
AT = 'records/reviews/Bl3/design-round1/adoption-table-Bl3-design-r1.md'
T3 = json.load(open(j('design', 'contrasts-Bl3.json'), encoding='utf-8'))
FJ = json.load(open(j('records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
D2 = open(j('design', 'design-Bl3-draft2.md'), encoding='utf-8').read()
assert T3['version'].startswith('draft2')
rows = {}
for l in open(j(*AT.split('/')), encoding='utf-8'):
    m = re.match(r'^\| (P6\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|', l)
    if m:
        rows[m.group(1)] = {'votes': m.group(2).strip(), 'gist': m.group(3).strip(), 'kind': m.group(5).strip()}
assert len(rows) == 47 and min(rows) == 'P620' and max(rows) == 'P666', (len(rows), min(rows), max(rows))
# 受けた所: 正本の鍵（c:）・草案2 の節（s:）・設計事実の鍵（f:）・草案2 の字句（t:）。変えない行は「—」と理由
MAP = {
    'P620': ['c:readout.primary.copy_cue', 'c:readout.variants.V3', 'c:scope.not_answered', 'c:limits', 's:3', 's:4', 's:10', 'f:B.cells', 't:雛形との重なり'],
    'P621': ['c:scope.full_path', 'c:scope.not_answered', 'c:limits', 'c:report_rules.template', 's:0', 's:1', 's:10', 's:12'],
    'P622': ['c:readout.primary.band_why', 's:3'],
    'P623': ['c:readout.primary.quantity', 'c:readout.primary.a_vs_catastrophe', 'c:scope.question', 's:0', 's:3'],
    'P624': ['f:A.refuse_next', 's:6', 't:refuse を選んだ出力'],
    'P625': ['c:readout.primary.precision', 'c:readout.primary.place', 'c:readout.primary.batching', 'c:readout.primary.batch', 'c:readout.primary.order_seed', 'c:pilot.checks.vi', 's:3', 's:4'],
    'P626': ['c:descriptive.mass', 's:8'],
    'P627': ['c:gate.attenuation', 'c:gate.descriptive_gates', 's:7', 's:10'],
    'P628': ['c:pilot.mass_min', 'c:pilot.p_bounds', 'c:pilot.cache_tol_rule', 'c:pilot.iii_sentences', 's:4', 's:15'],
    'P629': ['c:pilot.decision.gate_only', 'c:pilot.decision.drop_effects', 'c:pilot.decision.family', 'c:pilot.decision.q1_map', 'c:pilot.decision.tool_error', 'c:pilot.decision.report', 'c:gate.dropped', 's:4', 's:7', 's:9', 't:下見で一部を外した'],
    'P630': ['c:computation.steered_cache_check', 'c:computation.before_seal', 's:12'],
    'P631': ['c:computation.main_freeze_check', 'c:predictions.free', 's:11', 's:12'],
    'P632': ['c:nulls.isotropic.count', 'c:labels.p_min', 'c:labels.first_step_margin', 's:5', 'f:E.passes_main'],
    'P633': ['c:nulls.storage.dtype', 'c:nulls.storage.rule', 's:2'],
    'P634': ['c:nulls.real.chance_second_pair', 'c:nulls.real.chance_note', 'c:labels.second.ranks', 'c:labels.second.iso_rate', 's:5', 's:15'],
    'P635': ['c:labels.second.rule', 'c:labels.second.center_why', 's:5'],
    'P636': ['c:gate.push_center', 's:7'],
    'P637': ['c:gate.push', 'c:gate.call', 'c:labels.second.call', 'c:review_plan.synthetic', 's:5', 's:7', 's:12'],
    'P638': ['c:gate.descriptive_gates', 'c:gate.rows_without_vhat_loaded', 'c:gate.permutations_without_vhat_loaded', 'f:C.rows_without_vhat_loaded', 's:7'],
    'P639': ['f:D.cos_iso_b3_max', 's:6', 't:等方の方向と段階 B の三本の余弦'],
    'P640': ['c:scope.not_answered', 'c:limits', 's:0', 's:10', 't:活性の共分散に沿う帰無'],
    'P641': ['—: 不採用（門は条件として置く）。検出力の文は `gate.power_note` のまま', 'c:gate.power_note'],
    'P642': ['c:gate.descriptive_gates', 'c:gate.style_hold_pt', 'f:C.style_rows', 's:7'],
    'P643': ['c:descriptive.layerwise.values', 'c:descriptive.layerwise.capture', 'c:descriptive.layerwise.note_no_reading', 'c:descriptive.layerwise.place', 'c:print_strings.added_ban', 's:8', 's:9'],
    'P644': ['c:readout.secondary.band', 's:3'],
    'P645': ['c:reading_rules', 's:9', 't:最上位は順位で、検定ではない'],
    'P646': ['c:labels.side_rule', 's:5', 's:9', 't:零を越えて中央値と反対の向き'],
    'P647': ['c:reading_rules', 's:9', 't:外でない行', 't:下見で一部を外した'],
    'P648': ['c:reading_rules', 's:9', 't:方向に固有の効き目は言えない'],
    'P649': ['c:predictions.items', 'c:predictions.q7_rule', 's:11'],
    'P650': ['c:report_rules.template', 's:12'],
    'P651': ['c:independent_recompute.who', 'c:independent_recompute.how', 'c:independent_recompute.tol', 'c:independent_recompute.on_mismatch', 's:12'],
    'P652': ['c:review_plan.synthetic', 's:12', 't:向きの足し分に要る全ての升目・符号・方向の組の突き合わせ'],
    'P653': ['c:review_plan.synthetic', 'c:review_plan.impl.focus', 's:12'],
    'P654': ['c:cost.note', 'f:E.passes_recompute', 'f:E.passes_cache', 's:14'],
    'P655': ['—: 不採用（段階 B の生の出力の記録にトークンの並びの欄が無い）'],
    'P656': ['c:scope.reach', 's:1'],
    'P657': ['c:numbering.rulings_next', 'c:decisions.D210', 'c:decisions.D217', 'c:inputs.files.rulings_D210', 'c:inputs.files.rulings_D211_D217', 'c:drafter_values', 's:16'],
    'P658': ['s:15', 't:会話の記録の時刻で確かめた'],
    'P659': ['—: 是認（変えない）'],
    'P660': ['c:pilot.decision.after_stop', 's:4'],
    'P661': ['—: 是認（変えない）'],
    'P662': ['—: 是認（絞り方は P643 で受けた）'],
    'P663': ['—: 是認（変えない）'],
    'P664': ['—: 是認（偶然の目安の直しは P634 で受けた）'],
    'P665': ['—: 是認（変えない）'],
    'P666': ['c:predictions.free', 's:11', 's:15', 't:exposure-before-seal-Bl3.md'],
}
assert set(MAP) == set(rows), sorted(set(rows) ^ set(MAP))


def canon_has(path):
    x = T3
    for k in path.split('.'):
        if isinstance(x, dict) and k in x:
            x = x[k]
        else:
            return False
    return True


def facts_has(path):
    row, key = path.split('.', 1)
    return row in FJ['facts'] and key in FJ['facts'][row]


secs = set(re.findall(r'^## (\d+)\.', D2, flags=re.M))
out, bad = [], []
for p in sorted(MAP):
    checks = []
    for it in MAP[p]:
        kind, val = it.split(':', 1)
        ok = {'c': lambda v: canon_has(v), 's': lambda v: v in secs, 'f': lambda v: facts_has(v), 't': lambda v: v in D2, '—': lambda v: True}[kind](val)
        label = {'c': '正本 `%s`' % val, 's': '草案2 §%s' % val, 'f': '設計事実 `%s`' % val, 't': '草案2 の字句「%s」' % val, '—': val.strip()}[kind]
        checks.append((label, ok))
        if not ok:
            bad.append((p, label))
    r = rows[p]
    out.append('| %s | %s | %s | %s | %s |' % (p, r['votes'], r['kind'], '・'.join(l for l, _ in checks), '全て在る' if all(o for _, o in checks) else '**無いものがある**'))
L = ['# B-lens 層三の草案2 の対応の記録（機械で確かめた・`records/Bl3/draft2_mapping_Bl3.py`）', '',
     '- 採否表: `%s`（SHA16 %s）の行 P620〜P666。採否・票・所見・案は採否表から器が読んだ。' % (AT, s16(AT)),
     '- 受けた所: 正本 `design/contrasts-Bl3.json`（SHA16 %s・版 %s）・草案2 `design/design-Bl3-draft2.md`（SHA16 %s）・設計事実 `records/Bl3/design-facts-Bl3.json`（SHA16 %s）。受けた所は起草者が並べ、器がその実在を確かめた（中身の当否は確かめていない）。' % (
         s16('design/contrasts-Bl3.json'), T3['version'], s16('design/design-Bl3-draft2.md'), s16('records/Bl3/design-facts-Bl3.json')),
     '- 見つからなかったもの: %d 件。' % len(bad), '',
     '| 採否 | 票・所見 | 案 | 草案2 で受けた所 | 実在 |', '|---|---|---|---|---|'] + out + [
     '', '- 限界: この記録は、受けた所が在ることを確かめる。受け方が所見を取り違えていないか、半分しか直していないかは確かめない（設計の巡・二巡目で諮る）。',
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'draft2-mapping-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('wrote draft2-mapping-Bl3.md | rows', len(out), '| missing', len(bad), bad[:5])
sys.exit(1 if bad else 0)
