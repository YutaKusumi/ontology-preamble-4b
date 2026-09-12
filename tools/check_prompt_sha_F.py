# -*- coding: utf-8 -*-
"""check_prompt_sha_F.py —— 走行の trials から各腕の prompt_sha を、盤の腕本文（arms/panelF・arms/panel）と凍結場面（arms/frozen-from-ryokai-os/app-scenarios.json）から `user_message` と同じ規則
（`rd(arm) + "\\n\\n" + SCEN_TEXT + INST`・N は `SCEN_TEXT + INST`）で再構成して突合し、T・T2 腕の user 文が META で始まることを assert する（凍結 §2.6「付記の位置の検査」）。
用法: python tools/check_prompt_sha_F.py --tag dryF --root results/_dryrun"""
import os, sys, json, glob, hashlib, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--root', default=None); ap.add_argument('--compare-m', action='store_true', help='U 腕（N・Ncold・O-Ncold）の prompt_sha を M 第一走行 stageM1 の同名腕の trials と突合する'); a = ap.parse_args()
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8')); META = T['metas']
D = json.load(open(os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8')); SCJ = {x['question_id']: x for x in D['scenarios']}
sha16 = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
rd = lambda p: open(p, encoding='utf-8').read().replace('\r\n', '\n').strip()
def arm_text(name):
    if name == 'N':
        return None
    for d in ('panel', 'panelF'):
        p = os.path.join(REPO, 'arms', d, name + '.md')
        if os.path.isfile(p):
            return rd(p)
    sys.exit('盤に無い腕 %s' % name)
bad = 0; seen = {}
for d in sorted(glob.glob(os.path.join(a.root or os.path.join(REPO, 'results', a.tag), a.tag + '__*'))):
    m = json.load(open(os.path.join(d, 'manifest.json'), encoding='utf-8')); sc = SCJ[m['scenario']]; ST, INST = sc['text'], D['json_instruction'][sc['family']]
    for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8'):
        if not l.strip():
            continue
        r = json.loads(l); t = arm_text(r['arm']); um = (t + '\n\n' + ST + INST) if t else (ST + INST); s = sha16(um)
        mk = 'T2' if r['arm'].startswith('T2-') else 'T' if r['arm'].startswith('T-') else None
        ok = (s == r['prompt_sha']) and (mk is None or um.startswith(META[mk] + '\n\n')) and (mk is not None or not (um.startswith(META['T'] + '\n\n') or um.startswith(META['T2'] + '\n\n')))   # D-26: 場面文自体が「これは」で始まる S4 で誤警報したため META の逐語で判定
        seen.setdefault((m['scenario'], r['arm']), [0, 0]); seen[(m['scenario'], r['arm'])][0 if ok else 1] += 1; bad += (not ok)
if a.compare_m:
    mshas = {}
    for md in glob.glob(os.path.join(REPO, 'results', 'stageM1', 'stageM1__*__none__*')):
        msc = os.path.basename(md).split('__')[1]
        for l in open(glob.glob(os.path.join(md, 'trials-*.jsonl'))[0], encoding='utf-8'):
            if l.strip():
                r = json.loads(l)
                if r['arm'] in ('N', 'Ncold', 'O-Ncold'):
                    mshas.setdefault((msc, r['arm']), set()).add(r['prompt_sha'])
    fshas = {}
    for d in sorted(glob.glob(os.path.join(a.root or os.path.join(REPO, 'results', a.tag), a.tag + '__*'))):
        m = json.load(open(os.path.join(d, 'manifest.json'), encoding='utf-8'))
        for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8'):
            if l.strip():
                r = json.loads(l)
                if r['arm'] in ('N', 'Ncold', 'O-Ncold'):
                    fshas.setdefault((m['scenario'], r['arm']), set()).add(r['prompt_sha'])
    for k in sorted(fshas):
        ok = (k in mshas) and fshas[k] == mshas[k]; bad += (not ok)
        print('M 突合 %s %-8s F %s / M %s %s' % (k[0], k[1], sorted(fshas[k]), sorted(mshas.get(k, {'—'})), 'MATCH' if ok else 'MISMATCH'))
for k, v in sorted(seen.items()):
    print('%s %-12s 一致 %d 不一致 %d' % (k[0], k[1], v[0], v[1]))
print('[check_prompt_sha_F] %s（%d 試行・不一致 %d・T/T2 腕は META で始まる・U 腕は META で始まらない）' % ('MATCH' if bad == 0 else 'MISMATCH', sum(sum(v) for v in seen.values()), bad)); sys.exit(0 if bad == 0 else 1)
