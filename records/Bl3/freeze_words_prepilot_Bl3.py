# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の下見の前の凍結の登録者の言葉と、Colab の相 check の前後の登録者の言葉とユニットの読みを、会話の記録から機械で切り出して記録にする（手で打たない）。
- 凍結の言葉: 登録者の言葉の全文を逐語で置き、凍結の一行と凍結の記録に渡す部分（「凍結に当たり申し上げます」から「凍結をよろしくお願いします」まで）を機械で切り出す。
- 相 check の前の言葉: Colab のユニットの残りとプラン・GPU の見解の問い・相 check の時（一つの言葉）と、GPU を L4 に決めた言葉。
- 相 check の後のユニットの読み: コーディネータが Colab の画面の文を機械で読んだ道具の出力（会話の記録の道具の結果）から切り出す。
既にある記録には書かない。凍結の器と凍結の本文の器に渡す部分は、一時の置き場の words.txt にも書く（引数に手で打たない）。
用法: python records/Bl3/freeze_words_prepilot_Bl3.py <会話の記録 jsonl> <words.txt の置き場>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
OUT = os.path.join(HERE, 'prepilot-freeze-words-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
U, T = [], []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        U.append((o.get('uuid'), o.get('timestamp'), c))
    elif o.get('type') == 'user' and isinstance(c, list):
        for x in c:
            if isinstance(x, dict) and x.get('type') == 'tool_result':
                cc = x.get('content')
                txt = cc if isinstance(cc, str) else ''.join(y.get('text', '') for y in (cc or []) if isinstance(y, dict))
                T.append((o.get('uuid'), o.get('timestamp'), txt))


def one(pred, what):
    h = [m for m in U if pred(m[2])]
    assert len(h) == 1, ('一つに決まらない', what, len(h))
    return h[0]
m_units = one(lambda t: 'Colab Pro+' in t and '相 check は今日の夕方' in t, '相 check の前の言葉')
m_l4 = one(lambda t: 'GPU は L4 でお願いします' in t, 'GPU の言葉')
m_fz = one(lambda t: '凍結に当たり申し上げます' in t and 'ベストを尽くしたと判断します' in t, '凍結の言葉')
t = m_fz[2]
a0, a1 = t.index('凍結に当たり申し上げます'), t.index('凍結をよろしくお願いします') + len('凍結をよろしくお願いします')
words = t[a0:a1]
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for m in (m_units, m_l4, m_fz):
    for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
        assert bad not in m[2], '貼り付けの印か系統の印が入っている'
assert re.search(r'\d', words) is None, '凍結の一行に入る言葉に数字がある'
rd = [x for x in T if '利用可能なコンピューティング ユニット数' in x[2]]
assert rd, 'ユニットの読みの道具の結果が無い'
j_ = json.loads(rd[-1][2][rd[-1][2].index('{'):rd[-1][2].rindex('}') + 1])
R = ['# B-lens 層三の下見の前の凍結の登録者の言葉と、Colab の相 check の前後の言葉とユニットの読み（機械生成・`freeze_words_prepilot_Bl3.py`）', '',
     '## 凍結の言葉', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (m_fz[0], jst(m_fz[1]), m_fz[2].strip().replace(NL, ' ')),
     '- 凍結の一行と凍結の記録に渡す部分（上の言葉から機械で切り出した・「凍結に当たり申し上げます」から「凍結をよろしくお願いします」まで）: 「%s」' % words, '',
     '## 相 check の前の言葉（GPU と時）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (m_units[0], jst(m_units[1]), m_units[2].strip().replace(NL, ' ')),
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (m_l4[0], jst(m_l4[1]), m_l4[2].strip().replace(NL, ' ')),
     '- 採った形: Colab の GPU は L4（相 check・下見・本の計算のすべて・下見と本の計算は同じ GPU の型で走らせる）。相 check はこの日の夕方に行った。', '',
     '## 相 check の後の Colab のユニットの読み（コーディネータが Colab の画面の文を機械で読んだ道具の出力）', '',
     '- 読んだ時（協定世界時）: %s' % j_.get('at'),
     '- 読んだ文: %s' % '／'.join('「%s」' % x for x in j_.get('found') or []),
     '- 相 check の前のユニットの残りは、上の相 check の前の言葉にある値（登録者の読み）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
open(sys.argv[2], 'w', encoding='utf-8', newline=NL).write(words)
print('wrote', os.path.basename(OUT), '| freeze words', jst(m_fz[1]), m_fz[0], '| units read at', j_.get('at'), '| words chars', len(words))
