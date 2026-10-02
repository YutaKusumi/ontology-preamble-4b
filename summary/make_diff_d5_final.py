# -*- coding: utf-8 -*-
"""make_diff_d5_final.py v0（2026-10-02・中間総括の草案5 から最終版への差分の資料を作る・`make_diff_d4_d5.py` v0 を写し、前と後と照らしの記録を替え、最終確認の言葉の出所と、冷徹一行の逐語がある記録の数えを足した・登録者裁定 D290・コーディネータ南無弥勒如来）。
草案5 と最終版の行の差分を器で作り、変わった所ごとに、前の字（草案5）・後の字（最終版）と、後の字の中の引用の出所とその行の字を並べる。
引用の出所と行は、最終版の照らしの記録（`summary-interim-FINAL-2026-10-02-checks.json`）から読み、出所の行の字は公開の置き場の記録から器で切り出す（打たない）。
状態の行の登録者の言葉は、裁定 D290 の記録（`reviews/final/rulings-D290.md`）の行を出所として並べる。公開の頭の断りに挙げた記録は、ファイルごとに冷徹一行の逐語の数を器で数えて並べる（字は出さない）。
書く物: `diff-draft5-to-final-2026-10-02.md`（一度だけ）。--dry は OP4B_DRY_DIR に書き、最終版と照らしの記録も OP4B_DRY_DIR の物を読む。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, difflib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
NL = chr(10)
DRY = '--dry' in sys.argv
OUT = os.path.join(os.environ['OP4B_DRY_DIR'], 'diff-final-dry.md') if DRY else os.path.join(HERE, 'diff-draft5-to-final-2026-10-02.md')
assert DRY or not os.path.exists(OUT), '既にある（一度だけ）'
D5P = os.path.join(HERE, 'summary-interim-draft5-2026-10-02.md')
FP = os.path.join(os.environ['OP4B_DRY_DIR'], 'final-dry.md') if DRY else os.path.join(HERE, 'summary-interim-FINAL-2026-10-02.md')
FCP = os.path.join(os.environ['OP4B_DRY_DIR'], 'final-dry-checks.json') if DRY else os.path.join(HERE, 'summary-interim-FINAL-2026-10-02-checks.json')
D290P = os.path.join(HERE, 'reviews', 'final', 'rulings-D290.md')
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]
assert s16(D5P) == '63520DFDE8E11042', '草案5 の SHA が違う'
D5 = open(D5P, encoding='utf-8').read().split(NL)
FIN = open(FP, encoding='utf-8').read().split(NL)
CHK = json.load(open(FCP, encoding='utf-8'))
assert CHK['draft_sha16'] == s16(FP), '照らしの記録と最終版が合わない'
assert CHK['confirmation']['record_sha16'] == s16(D290P), '照らしの記録と D290 の記録が合わない'
TXT = {}


def src_lines(path):
    if path not in TXT:
        TXT[path] = open(os.path.join(PUB, *path.split('/')), encoding='utf-8').read().replace('\r\n', '\n').split(NL)
    return TXT[path]


# 冷徹一行の逐語は、出所の行を写すときも置き換える（逐語を資料に出さない・D287-b）
_tv = NL.join(src_lines('records/vprime/results-report-Vprime-FINAL-2026-09-09.md'))
_i = _tv.index('冷徹一行「')
COLD = _tv[_i + len('冷徹一行「'):_tv.index('」', _i + len('冷徹一行「'))]
hide = lambda s: s.replace('冷徹一行「' + COLD + '」', '冷徹一行〔逐語は V′ の台帳〕').replace(COLD, '〔冷徹一行の逐語は V′ の台帳〕')


def section_of(lines, j):
    for k in range(j, -1, -1):
        if lines[k].startswith('#'):
            return lines[k].lstrip('#').strip()
    return '（頭）'


def fence(lines):
    return ['```text'] + [hide(l) for l in lines] + ['```']


def cold_count(rel):
    p = os.path.join(HERE, *rel.split('/')[1:])
    t = open(p, encoding='utf-8').read()
    if p.endswith('.json'):
        t2 = json.dumps(json.load(open(p, encoding='utf-8')), ensure_ascii=False)
        return max(t.count(COLD), t2.count(COLD))
    return t.count(COLD)


D290L = open(D290P, encoding='utf-8').read().split(NL)
sm = difflib.SequenceMatcher(a=D5, b=FIN, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
quotes = CHK['quotes']
L = ['# 差分の資料（中間総括の草案5 → 最終版・器で作った・%s 日本時間）' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
     '- 何か: 草案5（`summary/summary-interim-draft5-2026-10-02.md`・SHA16 %s・登録者最終確認の対象）と最終版（`summary/summary-interim-FINAL-2026-10-02.md`・SHA16 %s）の行の差分。最終版は、草案5 の本文に公開の時の直しだけを入れた版（最終の巡の採否の表の Q30・裁定 D288-j と D290 の (1)〜(6)）。変わった所ごとに、前の字・後の字と、後の字の中の引用の出所と、その出所の行の字（器で切り出した）を並べる。' % (s16(D5P), s16(FP)),
     '- 最終版の器（`summary/build_summary_final.py`）は、草案5 から変わった行が裁定 D290 の (1)〜(6) の行だけであることを確かめてから書いた（照らしの記録の `changes_vs_draft5`）。冷徹一行の逐語は、出所の行を写すときも置き換えた。',
     '- 変わった所の数: %d（置き換え %d・足した %d・除いた %d）。最終版で変わったか足した行 %d・草案5 から除いた行 %d（検分票を含む）。' % (
         len(ops), sum(1 for o in ops if o[0] == 'replace'), sum(1 for o in ops if o[0] == 'insert'), sum(1 for o in ops if o[0] == 'delete'),
         sum(o[4] - o[3] for o in ops if o[0] in ('replace', 'insert')), sum(o[2] - o[1] for o in ops if o[0] == 'delete')), '']
TAGJ = {'replace': '置き換え', 'insert': '足した', 'delete': '除いた'}
conf_words = None
for l_ in D290L:
    if l_.startswith('- 登録者の言葉（会話の記録から機械で切り出した逐語'):
        conf_words = l_[l_.index('）: 「') + len('）: 「'):-1]
        conf_line = D290L.index(l_) + 1
assert conf_words and CHK['confirmation']['words_chars'] == len(conf_words)
for n_, (tag, i1, i2, j1, j2) in enumerate(ops, 1):
    sec = section_of(FIN, j1 if j1 < len(FIN) else len(FIN) - 1)
    L += ['## 差分 %d（%s・草案5 の %s・最終版の %s・小節: %s）' % (n_, TAGJ[tag], ('%d〜%d 行' % (i1 + 1, i2)) if i2 > i1 else 'なし', ('%d〜%d 行' % (j1 + 1, j2)) if j2 > j1 else 'なし', sec), '']
    if i2 > i1:
        L += ['前（草案5）:', ''] + fence(D5[i1:i2]) + ['']
    if j2 > j1:
        L += ['後（最終版）:', ''] + fence(FIN[j1:j2]) + ['']
        new_text = NL.join(FIN[j1:j2])
        seen = set()
        hits = []
        for q in quotes:
            shown = q['quote']
            if (q['cat'] in ('family', 'fnote', 'mapnote', 'table') and shown in new_text) or ('「' + shown + '」') in new_text:
                key = (q['source'], tuple(q['lines']))
                if key not in seen:
                    seen.add(key)
                    hits.append(q)
        if hits:
            L += ['後の字の中の引用の出所（%d）:' % len(hits), '']
            for q in hits:
                l0, l1 = q['lines']
                L.append('- `%s` の %s（%s）%s' % (q['source'], ('%d 行' % l0) if l0 == l1 else ('%d〜%d 行' % (l0, l1)), q['cat'], ('・注: ' + q['referent_note']) if q.get('referent_note') else ''))
                if q['cat'] != 'canon':
                    L += [''] + fence(src_lines(q['source'])[l0 - 1:l1]) + ['']
                else:
                    L += ['']
        if ('「' + conf_words + '」') in new_text:
            L += ['後の字の中の登録者の言葉の出所:', '', '- `summary/reviews/final/rulings-D290.md` の %d 行（会話の記録から機械で切り出した逐語）' % conf_line, ''] + fence([D290L[conf_line - 1]]) + ['']
        if '公開の頭の断り' in new_text:
            L += ['公開の頭の断りに挙げた記録の、冷徹一行の逐語の数（この器がファイルを読んで数えた・字は出さない）:', '']
            for rel in CHK['cold_line_files']:
                assert ('`%s`' % rel) in new_text, ('断りの行に無い記録', rel)
                L.append('- `%s`: %d' % (rel, cold_count(rel)))
            L.append('')
    L.append('')
L += ['本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
TEXT = NL.join(L)
assert COLD not in TEXT, '冷徹一行の逐語が資料に出た'
open(OUT, 'w', encoding='utf-8', newline=NL).write(TEXT)
print('wrote', OUT, '| 差分', len(ops), '|', len(TEXT), '字')
