# -*- coding: utf-8 -*-
# audit_prose_count_v0.py : 全試行で「JSON だけの答え」を数える事後の記述（登録者の決め・2026-11-06 21:3x・判定は変えない）
#   第二の登録の tools/audit_prose_count_bs_v0.py の写し。開く道具を第一の登録の audit_open_v1.py に替えただけ。
#   凍結の開く道具の関数をそのまま使い、読み手に渡す写しと同じ手順（写し返しを除く → JSON を伏せる）で、散文の字数を試行ごとに数える。
#   答えの本文は画面にもファイルにも出さない。出すのは条件ごとの数だけ。抜き出しの 371 の長さと一致することを照らす。
# 使い方: python -I audit_prose_count_v0.py <config-open-v1.json> <出す json>
import sys, os, json, importlib.util, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('audit_open_v1', os.path.join(HERE, 'audit_open_v1.py'))
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
cfg_p, out_p = sys.argv[1:3]
if os.path.exists(out_p):
    raise SystemExit('STOP 既にある')
c = O.load_config(cfg_p)
prel, psha = c['parser']
if O.sha_lf(O.P(c, prel)) != psha:
    raise SystemExit('STOP パーサの SHA')
parser = O.load_parser(O.P(c, prel))
stance = O.load_stance(c)
counts = {}
per_trial = {}
for sc, (zrel, zsha) in sorted(c['zips'].items()):
    zp = O.P(c, zrel)
    if O.sha_bytes(open(zp, 'rb').read()) != zsha:
        raise SystemExit('STOP zip の SHA ' + sc)
    rk, tr, rw = O.read_sealed(zp, sc)
    raw_by = {x['trial_id']: x for x in rw}
    for r in tr:
        if r.get('status') != 'ok':
            continue
        arm = r['arm']
        ft = O.final_text(raw_by[r['trial_id']].get('raw_output'))
        un, _ = O.strip_echo(ft, stance.get(arm, []))
        masked = O.mask_json(un, parser._JB)
        n = len(masked.replace(O.MARK, '').strip())
        per_trial[r['trial_id']] = n
        k = counts.setdefault(sc, {}).setdefault(arm, collections.Counter())
        k['n'] += 1
        cat = O.parser_category(r)
        k['json_only' if n == 0 else 'with_prose'] += 1
        k[('json_only_' if n == 0 else 'with_prose_') + cat] += 1
# 抜き出しの 371 と照らす
key = json.load(open(O.P(c, c['out'] + '/partC-key.json'), encoding='utf-8'))
sheet = {json.loads(l)['code']: json.loads(l) for l in open(O.P(c, c['out'] + '/partC-sheet.jsonl'), encoding='utf-8') if l.strip()}
bad = [k['code'] for k in key if per_trial[k['trial_id']] != len(sheet[k['code']]['answer_masked'].replace(O.MARK, '').strip())]
if bad:
    raise SystemExit('STOP 抜き出しの長さと合わない %d' % len(bad))
out = {sc: {arm: dict(v) for arm, v in arms.items()} for sc, arms in counts.items()}
tot = collections.Counter()
for sc, arms in counts.items():
    for v in arms.values():
        tot.update(v)
with open(out_p, 'x', encoding='utf-8', newline='\n') as f:
    json.dump({'by_condition': out, 'total': dict(tot), 'sample_check_items': len(key)}, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('total', dict(tot))
for sc in sorted(counts):
    s = collections.Counter()
    for v in counts[sc].values():
        s.update(v)
    print(sc, 'json_only', s['json_only'], '/', s['n'], {a: counts[sc][a]['json_only'] for a in counts[sc]})
print('sample check OK', len(key))
