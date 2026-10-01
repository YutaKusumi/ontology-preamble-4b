# -*- coding: utf-8 -*-
"""make_bundle_results_Bprime.py v0（2026-10-01・B′ の結果の巡の束を組む・層三の `records/reviews/Bl3/results-round1/make_bundle_results_Bl3.py` の型・コーディネータ南無弥勒如来）。
束は一つの md（`bundle/bundle-results-Bprime-all-in-one.md`）と索引（`bundle/bundle-index.md`）。元のファイルはバイトのまま読み、索引に置き場と SHA16 と字数を並べる。
JSON と長い記録は五つの逆引用符の囲いで包む（中の三つの逆引用符で囲いが切れないように）。器の段の記録は、凍結の後の行（「凍結と G4 の確かめと、下見の前の凍結の止まり」から）だけを写す。
書く物は一度だけ（既にあれば止める）。用法: python make_bundle_results_Bprime.py
柵: 本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, sys, json, hashlib, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
BP = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime'
OUT = os.path.join(HERE, 'bundle', 'bundle-results-Bprime-all-in-one.md')
IDX = os.path.join(HERE, 'bundle', 'bundle-index.md')
FENCE = '`' * 5
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
head = subprocess.run(['git', '-C', PUB, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
idx = []


def src(path, label):
    b = open(path, 'rb').read()
    t = b.decode('utf-8')
    assert FENCE not in t, ('囲いの字が中にある', path)
    rel = os.path.relpath(path, PUB).replace(os.sep, '/') if path.startswith(PUB) else ('（作業の置き場）' + os.path.relpath(path, BP).replace(os.sep, '/'))
    idx.append((label, rel, s16b(b), len(t)))
    return t


def block(path, label, lang=''):
    t = src(path, label)
    rel = idx[-1][1]
    return '### %s（`%s`・SHA16 %s）\n\n%s%s\n%s\n%s\n' % (label, rel, idx[-1][2], FENCE, lang, t.rstrip('\n'), FENCE)


def jblock(obj, label, note):
    t = json.dumps(obj, ensure_ascii=False, indent=1)
    assert FENCE not in t
    idx.append((label, note, s16b(t.encode('utf-8')), len(t)))
    return '### %s（%s・この写しの SHA16 %s）\n\n%sjson\n%s\n%s\n' % (label, note, idx[-1][2], FENCE, t, FENCE)


P = lambda *a: os.path.join(PUB, *a)
parts = []
parts.append('# B′ の結果の巡の束（一つの md・コミット %s の時点で組んだ）\n\n- 組み立ての器: `make_bundle_results_Bprime.py` v0（コーディネータ）。部は六つ。各部の元のファイルの置き場と SHA16 は索引（この束の終わり）に並べる。\n'
             '- JSON と長い記録は五つの逆引用符の囲いで包んだ。中身はバイトのまま（改行は LF）。\n' % head[:7])
parts.append('## 第一部 依頼文\n\n' + src(os.path.join(HERE, 'request-results-Bprime.md'), '依頼文'))
parts.append('## 第二部 報告の草案（全文）と起草者の欄の元の文\n\n' + block(P('records', 'Bprime', 'results-Bprime.md'), '報告の草案', 'markdown')
             + '\n' + block(P('records', 'Bprime', 'results-draft', 'rejected-lines-Bprime.md'), '起草者の欄の元の文（--rejected で渡した）', 'markdown'))
FR = json.load(open(P('records', 'Bprime', 'FREEZE-RECORD-Bprime.json'), encoding='utf-8'))
mf = {k: v for k, v in FR['main_freeze'].items() if k not in ('pilot_attempts', 'pilot')}
mf['（注）'] = 'pilot_attempts と pilot は読み取りの下見の記録（この部の初めのブロック）と同じ中身なので写していない'
p3 = ['## 第三部 止めた記録の機械の写し\n',
      block(P('records', 'Bprime', 'pilot', 'pilot-Bprime.json'), '読み取りの下見の記録', 'json'),
      block(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.md'), '行動の下見の閉じた記録（md）', 'markdown'),
      block(P('records', 'Bprime', 'analysis-Bprime.json'), '集計の出力（段 stopped）', 'json'),
      jblock({'main_freeze': mf, 'main_freeze_sha16': FR['main_freeze_sha16'], 'deviations': FR.get('deviations'), 'stage': FR.get('stage')}, '凍結の記録の本の凍結の節', '`records/Bprime/FREEZE-RECORD-Bprime.json` から機械で抜き出し'),
      block(P('records', 'Bprime', 'extract', 'extraction-record-Bprime.json'), '抽出の記録', 'json')]
for fn in sorted(os.listdir(P('records', 'Bprime', 'runs'))):
    p3.append(block(P('records', 'Bprime', 'runs', fn), '走行の記録 %s' % fn, 'json'))
p3 += [block(P('records', 'Bprime', 'sealing-record-Bprime.md'), '封印の記録（md）', 'markdown'),
       block(P('records', 'predictions', 'predictions-Bprime-coordinator.json'), 'コーディネータの予想', 'json'),
       block(P('records', 'predictions', 'predictions-Bprime-registrant.json'), '登録者の予想', 'json'),
       block(P('records', 'Bprime', 'exposure-before-seal-Bprime.md'), '封印の前の露出の記録', 'markdown'),
       block(P('records', 'Bprime', 'g4', 'g4-attempts-Bprime.jsonl'), 'G4 の試みの記録', 'json')]
parts.append('\n'.join(p3))
parts.append('## 第四部 凍結の本文（全文）\n\n' + block(P('design', 'design-Bprime-FROZEN.md'), '凍結の本文', 'markdown'))
parts.append('## 第五部 正本（全文）\n\n' + block(P('design', 'contrasts-Bprime.json'), '正本', 'json'))
led = open(P('records', 'FREEZE-RECORD.md'), encoding='utf-8').read().split('\n')
rows = [l for l in led if l.startswith('| ') and '**B′' in l]
assert len(rows) == 3, len(rows)
tl = open(os.path.join(BP, 'tools', 'tools-log-Bprime.md'), encoding='utf-8').read().split('\n')
i0 = [i for i, l in enumerate(tl) if l.startswith('- **凍結と G4 の確かめと、下見の前の凍結の止まり')]
i1 = [i for i, l in enumerate(tl) if l.startswith('## この記録が確認していないこと')]
assert len(i0) == 1 and len(i1) == 1 and i0[0] < i1[0]
tl_after = '\n'.join(tl[i0[0]:i1[0]]).strip('\n')
assert FENCE not in tl_after
idx.append(('器の段の記録の凍結の後の行', '（作業の置き場）tools/tools-log-Bprime.md の %d〜%d 行' % (i0[0] + 1, i1[0]), s16b(tl_after.encode('utf-8')), len(tl_after)))
p6 = ['## 第六部 凍結の後の記録\n',
      '### 全体の台帳の B′ の行（`records/FREEZE-RECORD.md` から機械で抜き出し）\n\n' + '\n'.join(rows) + '\n',
      block(P('records', 'Bprime', 'prefreeze-Bprime-2026-10-01-colab', 'provenance.json'), '下見の前の凍結を走らせた所の記録', 'json'),
      '### 器の段の記録の凍結の後の行（作業の置き場・公開の写しは凍結物なので、この束で初めて出す・%s）\n\n%smarkdown\n%s\n%s\n' % (idx[-1][1], FENCE, tl_after, FENCE)]
parts.append('\n'.join(p6))
body = '\n\n'.join(parts)
ix = ['# 束の索引（B′ の結果の巡・コミット %s）' % head[:7], '', '| 何 | 元の置き場 | SHA16 | 字数 |', '|---|---|---|---|']
ix += ['| %s | %s | %s | %d |' % (a, b, c, d) for a, b, c, d in idx]
ix += ['', '- 公開の置き場に置いてあるが束に入れなかったもの: 合成データの確かめの記録・器の本文・設計の巡と器の検分の票（`records/reviews/Bprime/`）。', '- まだ公開していないもの（結果の段で公開する予定）: 系統外の模型による採点の束（Gemma の応答 40 件・升目を伏せた形）と grok の返事・行動の下見の生成の全文・Colab の走りの進みの記録。', '',
       '本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
full = body + '\n\n' + '\n'.join(ix)
for p_ in (OUT, IDX):
    assert not os.path.exists(p_), p_
open(OUT, 'w', encoding='utf-8', newline='\n').write(full)
open(IDX, 'w', encoding='utf-8', newline='\n').write('\n'.join(ix))
print('束', os.path.basename(OUT), len(full), '字', len(full.encode('utf-8')), 'バイト', s16b(full.encode('utf-8')))
print('索引', len(idx), '項')
