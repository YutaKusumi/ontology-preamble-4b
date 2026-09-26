# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の本の凍結の登録者の言葉と、下見と本の計算の zip のダウンロードの許しを、会話の記録から機械で切り出して記録にする（手で打たない）。
- 本の凍結の言葉: 登録者の言葉の全文を逐語で置き、本の凍結の記録に渡す部分（「本の凍結の準備が整いました」から「凍結をしてください」まで）を機械で切り出す。
- 本の計算の zip のダウンロードの許し: 同じ言葉の終わりの文と、その後の登録者の訂正の言葉（「承認に対します」を「承認いたします」に改めた）を逐語で置く。
- 下見の zip のダウンロードの許し: 封印の後の言葉（裁定 D217 の旨の言葉と同じ発言）の中の文を逐語で置く。
既にある記録には書かない。本の凍結の器に渡す部分は、一時の置き場の words.txt にも書く（引数に手で打たない）。
用法: python records/Bl3/freeze_words_main_Bl3.py <会話の記録 jsonl> <words.txt の置き場>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
OUT = os.path.join(HERE, 'main-freeze-words-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
U = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        U.append((o.get('uuid'), o.get('timestamp'), c))


def one(pred, what):
    h = [m for m in U if pred(m[2])]
    assert len(h) == 1, ('一つに決まらない', what, len(h))
    return h[0]


def cut(t, a, b):
    i = t.index(a)
    j = t.index(b, i) + len(b)
    return t[i:j]
m_fz = one(lambda t: '本の凍結の準備が整いました' in t and '凍結をしてください' in t, '本の凍結の言葉')
m_fix = one(lambda t: '承認いたしますので' in t and '訂正いたします' in t, '訂正の言葉')
m_pl = one(lambda t: 'zip のダウンロードも許可します' in t and '露出の記録 X1〜X4' in t, '下見の zip の許し')
assert m_pl[1] < m_fz[1] < m_fix[1], '言葉の順が思ったものと違う'
words = cut(m_fz[2], '本の凍結の準備が整いました', '凍結をしてください')
dl_orig = cut(m_fz[2], 'なお、本の計算の zip のダウンロード', 'お願いします。')
dl_pilot = cut(m_pl[2], 'fbb8271 の push と下見をお願いします', 'zip のダウンロードも許可します')
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for m in (m_fz, m_fix, m_pl):
    for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>', 'Users'):
        assert bad not in m[2], '貼り付けの印か系統の印か手元の道筋が入っている'
flat = lambda t: t.strip().replace(NL, ' ')
R = ['# B-lens 層三の本の凍結の登録者の言葉と、下見と本の計算の zip のダウンロードの許し（機械生成・`freeze_words_main_Bl3.py`）', '',
     '## 本の凍結の言葉', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (m_fz[0], jst(m_fz[1]), flat(m_fz[2])),
     '- 本の凍結の記録に渡す部分（上の言葉から機械で切り出した・「本の凍結の準備が整いました」から「凍結をしてください」まで）: 「%s」' % words, '',
     '## 本の計算の zip のダウンロードの許し', '',
     '- 上の言葉の終わりの文（逐語）: 「%s」' % dl_orig,
     '- 登録者の訂正（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (m_fix[0], jst(m_fix[1]), flat(m_fix[2])),
     '- 採った形: 本の計算の三つの組（本の計算・独立の再計算・乙）の zip を、コーディネータが Colab のランタイムから落とす（訂正の言葉のとおり「承認いたします」と読む）。', '',
     '## 下見の zip のダウンロードの許し', '',
     '- 登録者の言葉の中の文（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (m_pl[0], jst(m_pl[1]), dl_pilot), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
open(sys.argv[2], 'w', encoding='utf-8', newline=NL).write(words)
print('wrote', os.path.basename(OUT), '| main freeze words', jst(m_fz[1]), m_fz[0], '| correction', jst(m_fix[1]), '| pilot zip words', jst(m_pl[1]), '| words chars', len(words))
