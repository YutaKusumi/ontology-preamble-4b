# -*- coding: utf-8 -*-
"""pc1_crosscheck.py —— PC1: 前置き本文・system文・圧力文・環境帰結文に、各シナリオの誘因語彙(丙 incentive-lexicon.json の algorithm)が混入していないかの交差検査。
再現: python tools/pc1_crosscheck.py  → records/pc1-crosscheck.md を生成（対象一覧・チャネル別ヒット・除外適用後）。監査一巡目の指摘(③#17・②D-1)を受け、コーディネータの非再現な先行検査を置き換える。"""
import json, re, os, glob, unicodedata, hashlib, datetime
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEX_PATH = os.environ.get('OP4B_LEXICON', os.path.join(REPO, 'arms/materials-draft/hei/incentive-lexicon-v2.json'))
LEX = json.load(open(LEX_PATH, encoding='utf-8'))
def norm(t): t = unicodedata.normalize('NFKC', t); return re.sub(r'[ \t\r]', '', t)
def rd(p): return open(p, encoding='utf-8').read().replace('\r\n', '\n').strip()
def sha(p): return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
targets = {}
def env_block(path):
    t = rd(path); m = re.search(r'<<<ENV-BLOCK-BEGIN>>>(.*?)<<<ENV-BLOCK-END>>>', t, re.S)
    return m.group(1).strip() if m else None
for p in ['arms/frozen-from-ryokai-os/armsE/preamble-O.md', 'arms/frozen-from-ryokai-os/armsE/preamble-Onull.md', 'arms/frozen-from-ryokai-os/armsE/preamble-Lneg.md', 'arms/frozen-from-ryokai-os/armsE/preamble-Om.md',
          'arms/frozen-from-ryokai-os/arms/A2-on-full.md', 'arms/frozen-from-ryokai-os/arms/A2-prime-on-full-3.1.md'] + sorted(os.path.relpath(x, REPO).replace(os.sep,'/') for x in glob.glob(os.path.join(REPO,'arms/panel/*.md'))) + sorted(os.path.relpath(x, REPO).replace(os.sep,'/') for x in glob.glob(os.path.join(REPO,'arms/materials-draft/otsu/T2-*.md'))) + sorted(os.path.relpath(x, REPO).replace(os.sep,'/') for x in glob.glob(os.path.join(REPO,'arms/materials-draft/ko/*-dose-*.md'))) + sorted(os.path.relpath(x, REPO).replace(os.sep,'/') for x in glob.glob(os.path.join(REPO,'arms/materials-draft/hei/env-frozen-texts*.md'))):
    fp = os.path.join(REPO, p)
    if os.path.isfile(fp): targets[p] = rd(fp)
spec = os.path.join(REPO, 'arms/materials-draft/hei/agent-env-spec-v2.md')
if os.path.isfile(spec):
    eb = env_block(spec)
    targets['arms/materials-draft/hei/agent-env-spec-v2.md [ENV-BLOCK のみ]'] = eb if eb else '(ENV-BLOCK 未検出)'
out = ['# PC1 交差検査（機械・再現可能）', '生成: %s／語彙: %s／対象 %d 文書' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), sha(LEX_PATH), len(targets)), '',
       '| 文書 | シナリオ | チャネル(群) | ヒット断片 |', '|---|---|---|---|']
nhit = 0
for doc, text in targets.items():
    t0 = norm(text)
    for sc, e in LEX['scenarios'].items():
        t = t0
        for ex in e.get('exclude_spans', []): t = re.sub(ex['regex'] if isinstance(ex, dict) else ex, '', t)
        for name, spec in e['channels'].items():
            grp = 'core' if name in e.get('core', []) else 'extended' if name in e.get('extended', []) else 'shared' if name in e.get('shared_nuclear', []) else 'aux'
            frags = []
            for pt in spec['patterns']:
                for m in re.finditer(pt, t): frags.append(m.group(0))
            if frags:
                nhit += 1; out.append('| %s | %s | %s (%s) | %s |' % (doc, sc, name, grp, '／'.join(sorted(set(frags))[:4])))
assert len(targets) >= 20, '対象文書が %d 件しか集まっていない（作業ディレクトリ依存の疑い）' % len(targets)
out.append(''); out.append('ヒット行数: %d（core のみを数え直すと %d）' % (nhit, sum(1 for l in out if '(core)' in l)))
out.append('対象＝モデルに送られる文言のみ（前置き・system・圧力/続行文・用量版・環境の凍結文言 env-frozen-texts*.md）。仕様書の散文は対象外（説明文の自己ヒットを避けるため・監査二巡目G3）。')
out.append('注: 表が事実の全て（ハードコードの注記は置かない・監査二巡目③R2-#4）。core の行のみが誘因言及率の主指標に影響し、_bare/extended/aux は別列。')
open(os.path.join(REPO, 'records/pc1-crosscheck.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
