# -*- coding: utf-8 -*-
"""make_bundle_final_Bprime.py v0（2026-10-01・B′ の最終検分の束を組む・結果の巡の `make_bundle_results_Bprime.py` の型・コーディネータ南無弥勒如来）。
束は一つの md（`bundle/bundle-final-Bprime-all-in-one.md`）と索引（`bundle/bundle-index.md`）と、grok に送る発話（`grok/grok-final-message.md`・頭の一文と束）。
元のファイルはバイトのまま読み、索引に置き場と SHA16 と字数を並べる。JSON と長い記録は五つの逆引用符の囲いで包む。起草者の欄の結果の巡で見た版は、公開の置き場のコミット b4dd234 の版を git から読む。
結果の巡の二票は入れない（採否の表が要旨を書いている・層三の最終検分の束と同じ）。書く物は一度だけ（既にあれば止める）。
用法: python make_bundle_final_Bprime.py [--dry <書き出す置き場>]（--dry は手元と GitHub の一致を照らさず、決めた置き場に書く試し・依頼文はその置き場の request-final-Bprime.md を読む）
柵: 本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, sys, json, hashlib, subprocess, argparse, difflib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
FENCE = '`' * 5
CALM = '時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。'
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
ap = argparse.ArgumentParser()
ap.add_argument('--dry')
a = ap.parse_args()
BASE = a.dry or HERE
OUT = os.path.join(BASE, 'bundle', 'bundle-final-Bprime-all-in-one.md')
IDX = os.path.join(BASE, 'bundle', 'bundle-index.md')
MSG = os.path.join(BASE, 'grok', 'grok-final-message.md')
REQ = os.path.join(BASE, 'request-final-Bprime.md')
git = lambda *c: subprocess.run(['git', '-C', PUB] + list(c), capture_output=True).stdout
head = git('rev-parse', 'HEAD').decode().strip()
remote = git('rev-parse', 'origin/main').decode().strip()
if not a.dry:
    assert head == remote, '公開の置き場の手元と GitHub が違う'
idx = []


def text_of(b, label, rel):
    t = b.decode('utf-8')
    assert FENCE not in t, ('囲いの字が中にある', rel)
    idx.append((label, rel, s16b(b), len(t)))
    return t


def src(path, label):
    rel = os.path.relpath(path, PUB).replace(os.sep, '/') if path.startswith(PUB) else os.path.basename(path)
    return text_of(open(path, 'rb').read(), label, rel)


def block(path, label, lang=''):
    t = src(path, label)
    return '### %s（`%s`・SHA16 %s）\n\n%s%s\n%s\n%s\n' % (label, idx[-1][1], idx[-1][2], FENCE, lang, t.rstrip('\n'), FENCE)


def jblock(obj, label, note):
    t = json.dumps(obj, ensure_ascii=False, indent=1, default=str)
    assert FENCE not in t
    idx.append((label, note, s16b(t.encode('utf-8')), len(t)))
    return '### %s（%s・この写しの SHA16 %s）\n\n%sjson\n%s\n%s\n' % (label, note, idx[-1][2], FENCE, t, FENCE)


def gblock(commit, rel, label, lang=''):
    b = git('show', '%s:%s' % (commit, rel))
    assert b, (commit, rel)
    t = text_of(b, label, '%s（コミット %s の版）' % (rel, commit))
    return '### %s（`%s`・コミット %s の版・SHA16 %s）\n\n%s%s\n%s\n%s\n' % (label, rel, commit, idx[-1][2], FENCE, lang, t.rstrip('\n'), FENCE)


P = lambda *x: os.path.join(PUB, *x)
parts = ['# B′ の最終検分の束（一つの md・コミット %s の時点で組んだ）\n\n- 組み立ての器: `make_bundle_final_Bprime.py` v0（コーディネータ）。部は七つ。各部の元のファイルの置き場と SHA16 は索引（この束の終わり）に並べる。\n'
         '- JSON と長い記録は五つの逆引用符の囲いで包んだ。中身はバイトのまま（改行は LF）。\n' % head[:7]]
parts.append('## 第一部 依頼文\n\n' + src(REQ, '依頼文'))
parts.append('\n'.join(['## 第二部 報告の草案の二つ目（全文）と確かめの記録と逸脱の器\n',
                        block(P('records', 'Bprime', 'results-Bprime-draft2.md'), '報告の草案の二つ目', 'markdown'),
                        block(P('records', 'Bprime', 'results-Bprime-draft2-checks.json'), '草案の二つ目の確かめの記録', 'json'),
                        block(P('tools', 'build_report_Bprime_devBPT1.py'), '逸脱の器（D-BPT1）', 'python')]))
fz = open(P('records', 'Bprime', 'results-Bprime.md'), 'rb').read()
idx.append(('凍結した組み立ての器の出力（起草者の欄を直した版で組み直したもの・差分の元）', 'records/Bprime/results-Bprime.md', s16b(fz), len(fz.decode('utf-8'))))
dl = list(difflib.unified_diff(fz.decode('utf-8').split('\n'), open(P('records', 'Bprime', 'results-Bprime-draft2.md'), encoding='utf-8').read().split('\n'),
                               'records/Bprime/results-Bprime.md', 'records/Bprime/results-Bprime-draft2.md', n=1, lineterm=''))
dt = '\n'.join(dl)
assert FENCE not in dt
idx.append(('凍結の報告と草案の二つ目の機械の差分', 'difflib.unified_diff（前後一行）', s16b(dt.encode('utf-8')), len(dt)))
parts.append('\n'.join(['## 第三部 凍結した器の出力と草案の二つ目の違いと、起草者の欄の二つの版\n',
                        '### 凍結の報告（`records/Bprime/results-Bprime.md`・SHA16 %s）と草案の二つ目の機械の差分（difflib の unified_diff・前後一行・この写しの SHA16 %s）\n\n'
                        '凍結の報告の全文は、草案の二つ目から印の区画を除き、見出しと状態の行を戻したものと同じ（逸脱の器が確かめた・第二部の確かめの記録）。\n\n%sdiff\n%s\n%s\n' % (s16b(fz), idx[-1][2], FENCE, dt, FENCE),
                        block(P('records', 'Bprime', 'results-draft', 'rejected-lines-Bprime.md'), '起草者の欄（直した版・--rejected で渡した）', 'markdown'),
                        gblock('b4dd234', 'records/Bprime/results-draft/rejected-lines-Bprime.md', '起草者の欄（結果の巡で見た版）', 'markdown')]))
parts.append('\n'.join(['## 第四部 結果の巡の後の記録\n',
                        block(P('records', 'reviews', 'Bprime', 'results', 'adoption-table-results-Bprime.md'), '結果の巡の採否の表', 'markdown'),
                        block(P('records', 'reviews', 'Bprime', 'results', 'repro-results-Bprime.json'), '結果の巡の再現の記録', 'json'),
                        block(P('records', 'Bprime', 'rulings-D284.md'), '裁定 D284 の記録', 'markdown')]))
ld = lambda p: json.load(open(p, encoding='utf-8'))
FR = ld(P('records', 'Bprime', 'FREEZE-RECORD-Bprime.json'))
CL = ld(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'))
AN = ld(P('records', 'Bprime', 'analysis-Bprime.json'))
fr_x = {'kind': FR['kind'], 'stage': FR['stage'], 'frozen_jst': FR['frozen_jst'], 'deviation_rule': FR['deviation_rule'], 'deviations': FR['deviations'],
        'frozen_sha16（design の二つ）': {k: v for k, v in FR['frozen_sha16'].items() if k.startswith('design/')}, 'prefreeze.g': FR['prefreeze']['g'],
        'checks.colab_check': FR['checks']['colab_check'], 'main_freeze': {k: v for k, v in FR['main_freeze'].items() if k not in ('added', 'pilot_attempts', 'pilot')},
        'main_freeze_sha16': FR['main_freeze_sha16'], '（注）': 'main_freeze の added（抽出の転記行など）・pilot_attempts・pilot（読み取りの下見の記録と同じ中身）と、ほかの節は写していない'}
ext = {k: v for k, v in CL['external'].items() if k != 'rows'}
ext['rows（数）'] = len(CL['external']['rows'])
cl_x = {'kind': CL['kind'], 'version': CL['version'], 'closed_jst': CL['closed_jst'], 'session': CL['session'], 'start_record': CL['start_record'], 'end_record': CL['end_record'],
        'external': ext, 'iii_status': CL['iii_status'], '（注）': 'digests・summaries・fixed・row_C・bundle などは写していない（転記行 C は閉じた記録の md の表にある）'}
an_x = {'version': AN['version'], 'dry': AN['dry'], 'pilot_attempts[-1].cells': AN['pilot_attempts'][-1]['cells'], 'pilot_attempts[-1].decision': AN['pilot_attempts'][-1]['decision'],
        'pilot_attempts[-1].iii': AN['pilot_attempts'][-1]['iii'], 'predictions_truth': AN['predictions_truth'], '（注）': '集計の出力のほかの節は写していない'}
sh = lambda *x: s16b(open(P(*x), 'rb').read())
p5 = ['## 第五部 注が指す記録の機械の写し\n',
      jblock(fr_x, '凍結の記録の抜き出し（逸脱の台帳・下見の前の凍結の g・G4 の確かめ・本の凍結の節）', '`records/Bprime/FREEZE-RECORD-Bprime.json`（SHA16 %s）から機械で抜き出し' % sh('records', 'Bprime', 'FREEZE-RECORD-Bprime.json')),
      block(P('records', 'Bprime', 'pilot', 'pilot-Bprime.json'), '読み取りの下見の記録', 'json'),
      block(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.md'), '行動の下見の閉じた記録（md）', 'markdown'),
      jblock(cl_x, '行動の下見の閉じた記録の抜き出し', '`records/Bprime/behavior/behavior-closed-Bprime.json`（SHA16 %s）から機械で抜き出し' % sh('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json')),
      jblock(an_x, '集計の出力（段 stopped）の抜き出し', '`records/Bprime/analysis-Bprime.json`（SHA16 %s）から機械で抜き出し' % sh('records', 'Bprime', 'analysis-Bprime.json'))]
for fn in sorted(os.listdir(P('records', 'Bprime', 'runs'))):
    p5.append(block(P('records', 'Bprime', 'runs', fn), '走行の記録 %s' % fn, 'json'))
p5.append(block(P('records', 'Bprime', 'prefreeze-Bprime-2026-10-01-colab', 'provenance.json'), '下見の前の凍結を走らせた所の記録', 'json'))
parts.append('\n'.join(p5))
parts.append('## 第六部 凍結の本文（全文）\n\n' + block(P('design', 'design-Bprime-FROZEN.md'), '凍結の本文', 'markdown'))
parts.append('## 第七部 正本（全文）\n\n' + block(P('design', 'contrasts-Bprime.json'), '正本', 'json'))
body = '\n\n'.join(parts)
ix = ['# 束の索引（B′ の最終検分・コミット %s）' % head[:7], '', '| 何 | 元の置き場 | SHA16 | 字数 |', '|---|---|---|---|']
ix += ['| %s | %s | %s | %d |' % (a_, b_, c_, d_) for a_, b_, c_, d_ in idx]
ix += ['', '- 公開の置き場に置いてあるが束に入れなかったもの: 結果の巡の二票（`records/reviews/Bprime/results/votes/`）・結果の巡の束・合成データの確かめの記録・器の本文・設計の巡と器の検分の票。',
       '- まだ公開していないもの（最終版と一緒に公開する予定・採否の W22）: 系統外の模型による採点の束と返事・行動の下見の生成と採点の出力の全文・Colab の走りの進みの記録とセッションの記録・凍結の後の器の段の記録。', '',
       '本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
full = body + '\n\n' + '\n'.join(ix)
msg = CALM + 'この発話は、B′ の結果の報告の最終検分（最終の系統外の一票）の依頼です。第一部が依頼文で、第二部から第七部が束です（束の索引は終わりにあります）。依頼文のとおりに検分してください。\n\n' + full
for p_ in (OUT, IDX, MSG):
    assert not os.path.exists(p_), p_
    os.makedirs(os.path.dirname(p_), exist_ok=True)
open(OUT, 'w', encoding='utf-8', newline='\n').write(full)
open(IDX, 'w', encoding='utf-8', newline='\n').write('\n'.join(ix))
open(MSG, 'w', encoding='utf-8', newline='\n').write(msg)
print('束', len(full), '字', len(full.encode('utf-8')), 'バイト', s16b(full.encode('utf-8')), '| 発話', len(msg), '字', s16b(msg.encode('utf-8')), '| 索引', len(idx), '項 | コミット', head[:7])
