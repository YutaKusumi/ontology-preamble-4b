# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D178 の記録を書く（設計の巡の第二巡・凍結前の最終検分・2026-09-23）。
登録者の言葉は会話の記録から機械で切り出す。既にあるファイルには書かない。
用法: python records/Blens/rulings_D178.py <会話の記録 jsonl>"""
import os, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
words = rec_uuid = rec_ts = None
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'user':
        continue
    c = (o.get('message') or {}).get('content')
    texts = [c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']
    for t in texts:
        if '凍結前の最終検分' in t and 'ef4a72c' in t and '先程の四名' in t and len(t) < 600:
            words, rec_uuid, rec_ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '裁定の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(rec_ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')

R = ['# 登録者裁定 D178（2026-09-23・B-lens の設計の巡の第二巡・凍結前の最終検分）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (rec_uuid, jst, words.replace(NL, ' ')),
     '', '| 裁定 | 中身 |', '|---|---|',
     '| D178 | **設計の巡の第二巡を置き、凍結前の最終検分とする**。検分者は第一巡と同じ四名（Gemini 3.8 Flash 二名・claude.ai の Claude Opus 5.5 二名）。第一巡は四票とも条件つき可で差し戻しが無かったので、第二巡を凍結の前の最後の検分とし、その旨を依頼文に書く。これは裁定 D166 の順（設計の巡は一巡）に、登録者が一巡を足したもの。この巡の後は、裁定・草案3・器と合成データ・凍結へ進み、設計の巡をもう一度は置かない（裁定 D160 の型）。対象は草案2（コミット ef4a72c）。 |', '',
     '## 注（事実のみ）', '',
     '- 草案2 の §10 の「設計の巡は一巡で済んだ」と §12 の「草案2 は外の目を通らずに器と凍結へ進む（裁定 D166）」は、この裁定の前に書いた文である。草案2 は書き換えず、依頼文でこの点を知らせ、草案3 で改める。',
     '- 採用済みの手順（計画案 v2.0 §8-補・内部・非公開）の六番は、結果の検分で二巡目以降を新規の個体とする決まりで、設計の検分には当てはまらない。同じ個体は、自分の第一巡の所見が正しく直ったかを確かめられる。一方で、第一巡で見たものに寄りやすく、第一巡で見落とした所をまた見落とす見込みがある。',
     '- 同じ六番の「合も採否表に載せて次の巡に渡す」に当たるものとして、第一巡の四票の是認と総括の抜き書きを、器で切り出して第二巡の束に入れる（`records/reviews/Blens/design-round2/round1-approvals-extract.md`）。',
     '- 番号: この巡の再現は K326 から、採否は P528 から、次の裁定は D179 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
out = os.path.join(HERE, 'rulings-D178.md')
assert not os.path.exists(out), '既にある: ' + out
open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', out, '|', jst, rec_uuid)
