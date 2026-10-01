# -*- coding: utf-8 -*-
# 逸脱の台帳の行（D-BPT1 の案）と起草者の欄の新しい版を、凍結した組み立ての器の build と scan に直に通して、走査の当たりを見る（何も書かない・試し）。
import io, os, sys, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
BP = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime'
sys.path.insert(0, os.path.join(PUB, 'tools'))
import build_report_Bprime as BR
RECS = os.path.join(PUB, 'records', 'Bprime')
ld = lambda p: json.load(open(p, encoding='utf-8'))
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
C = ld(os.path.join(PUB, 'design', 'contrasts-Bprime.json'))
FR, SR, A = ld(os.path.join(RECS, 'FREEZE-RECORD-Bprime.json')), ld(os.path.join(RECS, 'sealing-record-Bprime.json')), ld(os.path.join(RECS, 'analysis-Bprime.json'))
preds = {role: ld(BR.REPO_ROOT_FOR(SR, role)) for role in ('registrant', 'coordinator')}
closed = ld(os.path.join(RECS, 'behavior', 'behavior-closed-Bprime.json'))
facts = ld(os.path.join(RECS, 'facts-Bprime-pre.json'))
import bprime_gemma as G_
bl3 = BR.bl3_values(C, G_.REPO)
meta = {'canon': s16(os.path.join(PUB, 'design', 'contrasts-Bprime.json')), 'freeze': 'TEST', 'seal': s16(os.path.join(RECS, 'sealing-record-Bprime.json')), 'analysis': s16(os.path.join(RECS, 'analysis-Bprime.json')), 'judge': A.get('judge_record_sha16')}
rej = open(os.path.join(BP, 'records', 'Bprime', 'results-draft', 'rejected-lines-Bprime.md'), encoding='utf-8').read()
dev = json.load(open(sys.argv[1], encoding='utf-8')) if len(sys.argv) > 1 else None
D = BR.build(C, A, preds, meta, closed, facts, bl3, deviations=[dev] if dev else [], rejected=rej, runs_dir=os.path.join(RECS, 'runs'), FR=FR)
hits = BR.scan(C, D.lines)
print('lines', len(D.lines), 'hits', len(hits))
for h in hits:
    print(json.dumps(h, ensure_ascii=False))
