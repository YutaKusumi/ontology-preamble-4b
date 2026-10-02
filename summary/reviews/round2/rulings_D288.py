# -*- coding: utf-8 -*-
"""rulings_D288.py v0（2026-10-02・中間総括の検分の二巡目の後の登録者裁定 D288 を記録する・D287 の器の型・コーディネータ南無弥勒如来）。
登録者の発話を会話の記録から機械で切り出し（決まった句を含むただ一つ・system-reminder の文を除き「南無汝我曼荼羅」から）、`rulings-D288.md` に一度だけ書く。
裁定の中身は、採否の表 `adoption-table-round2.md` の §3（D-h〜D-k の推奨）に、登録者の言葉の一点（最終の検分の形）を重ねたもの。
用法: python rulings_D288.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D288.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
PHRASE = '最終検分もこれまでどおり、丁寧に、claude.ai三名とGemini 二名に依頼することとしましょう'
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
AT = open(os.path.join(HERE, 'adoption-table-round2.md'), 'rb').read()
L = ['# 登録者裁定 D288（中間総括の検分の二巡目の採否・2026-10-02・内部）', '',
     '- 登録者の言葉（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst, words),
     '- 裁定の土台: 採否の表 `adoption-table-round2.md`（SHA16 %s）の §3 の推奨（D-h〜D-k）。登録者は、最終の検分の形（D-i）を推奨と違う形に決め、ほかは推奨の案とした。' % hashlib.sha256(AT).hexdigest().upper()[:16], '',
     '## 決まったこと', '',
     '- **D288-h（§0 の外の族の札）**: §3.1 の四つの欄の置き場に限り、各最終版の族の表の札を器で切り出して出所に足す。その決まりを、草案3 の前に枠の追記二に書く。§2 の答えの引用は §0 の範囲のまま。',
     '- **D288-i（最終の検分）**: **最終の検分も、これまでどおり claude.ai の新しいチャット三つ（系統内・三つで一票）と Google AI Studio の Gemini 3.8 Flash の新しいチャット二つ（系統外・二票）に、丁寧に依頼する**（登録者の言葉・推奨の「Gemini 一つと claude.ai 一つ」ではない）。照らしの器には、指示語の指す先を確かめる段を足す（推奨の前半）。',
     '- **D288-j（公開の束ね方）**: 各段の公開と同じく、総括の本文に、枠・追記・計算の器と出力・検分の記録（依頼文・束・票・採否の表・裁定・照らしの記録）を添えて公開する。一巡目の束の草案1 にある冷徹一行の逐語は、V′ の最終版の §0 にすでにある字で、記録は一度だけ書いた物なので替えず、その旨を公開の頭に書く。',
     '- **D288-k（段階 F の場面の名）**: §2.4 と §3.1 の地の文で、段階 F の確証の場面の名を並べない（数だけ・場面の名は §0 の引用の中だけ）。',
     '- 採否の表の Z01〜Z30 の扱いの欄（直す・記録に置く・一部採る）は、上の決まりの下でそのとおり進める。',
     '- 次の段取り: 枠の追記二（草案3 と計算の器の版上げの前に書いて刻印する・最終の巡の予想を書く）→ 計算の器 v0.3 → 照らしの器の足し → 草案3 → 最終の巡の依頼文と束（送る前に刻印）→ 最終の巡（五つ）→ 採否の表 → 登録者の確かめ。最終の巡の後に巡を足すかは、登録者が決める（枠の上限を越えるため）。',
     '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('D288 | uuid %s | %s | %d 字' % (uuid, jst, len(words)))
