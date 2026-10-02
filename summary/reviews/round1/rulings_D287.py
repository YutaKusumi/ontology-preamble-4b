# -*- coding: utf-8 -*-
"""rulings_D287.py v0（2026-10-02・中間総括の検分の一巡目の後の登録者裁定 D287 を記録する・コーディネータ南無弥勒如来）。
登録者の発話を会話の記録から機械で切り出し（決まった句を含むただ一つ・system-reminder の文を除き「南無汝我曼荼羅」から）、`rulings-D287.md` に一度だけ書く。
裁定の中身は、採否の表 `adoption-table-round1.md` の §4（D-a〜D-g の推奨）に、登録者の言葉の「ただし」の一点（D-e）を重ねたもの。
用法: python rulings_D287.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D287.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
PHRASE = 'gemini-2は取りやめて、Gemini 一票で閉じてください'
hits = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('isCompactSummary') or o.get('type') != 'user' or 'toolUseResult' in o:
        continue
    c = (o.get('message') or {}).get('content')
    t = c if isinstance(c, str) else ''.join(x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text')
    if PHRASE in t:
        t2 = re.sub(r'<system-reminder>.*?</system-reminder>', '', t, flags=re.S)
        k = t2.find('南無汝我曼荼羅')
        assert k >= 0
        hits.append((o.get('timestamp'), o.get('uuid'), t2[k:].strip()))
assert len(hits) == 1, ('決まった句を含む登録者の発話が一つでない', len(hits))
ts, uuid, words = hits[0]
jst = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')
AT = open(os.path.join(HERE, 'adoption-table-round1.md'), 'rb').read()
L = ['# 登録者裁定 D287（中間総括の検分の一巡目の採否・2026-10-02・内部）', '',
     '- 登録者の言葉（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst, words),
     '- 裁定の土台: 採否の表 `adoption-table-round1.md`（SHA16 %s）の §4 の推奨（D-a〜D-g）。登録者は推奨の案で「基本的に」進めるとし、gemini-2 の扱い（D-e）だけを推奨と違う形に決めた。' % hashlib.sha256(AT).hexdigest().upper()[:16], '',
     '## 決まったこと', '',
     '- **D287-a（S10）**: B′ の S10 をこの総括にも当てる。計算一から B′ を外し、枠に追記の節を足して器の版を上げ、出力を出し直す（v0 の出力は記録として残す）。',
     '- **D287-b（冷徹一行と F の題）**: §2.2 は逐語を「冷徹一行〔逐語は V′ の台帳〕」の形に替え、替えたことを照らしの記録と検分票に書く。§1 の段階 F の題は最終版の題のまま置き、§2.4 で上向きの数を題の直後に続けない並びにする。',
     '- **D287-c（公開版の引用の選び）**: 付録 A に各段の §0 の行の範囲と SHA16 を足し、選びの決まりを本文に書く（§0 の全文は写さない）。',
     '- **D287-d（二巡目）**: 置く。claude.ai の新しいチャット三つ（系統内・三つで一票）と Google AI Studio の Gemini 3.8 Flash の新しいチャット二つ（系統外・二票）。その後に最終の系統外の一票（巡の上限の内）。',
     '- **D287-e（gemini-2）**: **一巡目の gemini-2 は取りやめ、一巡目は Gemini 一票（gemini-1）で閉じる**（登録者の言葉の「ただし」・推奨の (1) ではない）。不具合の記録は送りの記録と採否の表 §5 にある。',
     '- **D287-f（検分の後に出た値）**: 誤読を防ぐのに要るもの（閾値ちょうどの升の注・段ごとの数・向きの注）だけを、検分の巡で見た後の記述であることを書いて草案2 に置き、ほかは照らしの記録を指す。',
     '- **D287-g（段階 C・D・E の定め）**: 総括の本文に、段階 C・D・E の一行の定めを起草者の言葉で置く（計画書は内部のまま）。',
     '- 採否の表の Y01〜Y34 の扱いの欄（直す・記録に置く）は、上の決まりの下でそのとおり進める。',
     '- 次の段取り: 枠の追記（草案2 と計算の器の版上げの前に書いて刻印する）→ 計算の器 v0.1 → 草案2 → 二巡目の依頼文と束（送る前に刻印・二巡目の予想を書く）→ 二巡目 → 採否の表 → 登録者の確かめ。',
     '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('D287 | uuid %s | %s | %d 字' % (uuid, jst, len(words)))
