# -*- coding: utf-8 -*-
"""rulings_D289.py v0（2026-10-02・中間総括の検分の最終の巡の後の登録者裁定 D289 を記録する・D288 の器の型・コーディネータ南無弥勒如来）。
登録者の発話を会話の記録から機械で切り出し（決まった句を含むただ一つ・system-reminder の文を除き「南無汝我曼荼羅」から）、`rulings-D289.md` に一度だけ書く。
裁定の中身は、採否の表 `adoption-table-final.md` の §3（D289-a〜D289-d の推奨）を、登録者がそのまま採ったもの。gemini-5 の置き場の扱いは登録者の言葉による。
用法: python rulings_D289.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D289.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
PHRASE = 'チャットセクションの記録がすぐに表示されないことがありますが'
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
AT = open(os.path.join(HERE, 'adoption-table-final.md'), 'rb').read()
L = ['# 登録者裁定 D289（中間総括の検分の最終の巡の採否・2026-10-02・内部）', '',
     '- 登録者の言葉（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間・改行は元のまま）: 「%s」' % (uuid, jst, words),
     '- 裁定の土台: 採否の表 `adoption-table-final.md`（SHA16 %s）の §3 の推奨（D289-a〜D289-d）。登録者は推奨の案をそのまま採った。' % hashlib.sha256(AT).hexdigest().upper()[:16], '',
     '## 決まったこと', '',
     '- **D289-a（Q03・族の表の注の行）**: 各族の表の直下に、その最終版が表に付けた語の注と読みの限りの行を、表と同じく器で切り出して置く（D288-h を表の隣の注と限りの行まで広げる）。§3.1 の「範囲は §2 に引いた限りの文のとおり」の句は、§0 から入った札に限ると書き直す。',
     '- **D289-b（Q15・計画書の出所）**: §6 の段階 C の定めの出所を、非公開の内部の計画書と書き、計画書の字は引かない。',
     '- **D289-c（Q22・追補 M の断面の数）**: 追補 M でも、札 ① のうち様式門で過半が保留された断面にある本数を、両向きで、族と場面の組の数で書く（対比の id は並べない）。同じ箇所に、どちらの向きも登録者の封印の COI 自記に有利な向きに読まれうることを書く。',
     '- **D289-d（閉じ方）**: 最終の巡の後に検分の巡を足さない。(1) 広げた照らしの器（段ごとの欄の和・引用の中の指示語と頭の接続の語・数・引用・禁止の語）を通し、(2) 直した行だけの前後の差分を、出所の最終版の行と並べて器で作り、登録者が目で見て、(3) 登録者の最終確認で公開（D288-j の束ね方）に進む。',
     '- **gemini-5 の置き場（受け取りの記録）**: 登録者の言葉のとおり、AI Studio の履歴の表示は待たず、受け取って SHA-256 を照らした票の本文を記録として受け取る（結果を記録として受け取る）。',
     '- 採否の表の Q01〜Q31 の扱いの欄（直す・記録に置く・公開の時に直す・直さない）は、上の決まりの下でそのとおり進める。',
     '- 次の段取り: 枠の追記三（草案4 と計算の器 v0.4 の前に書いて刻印する）→ 計算の器 v0.4 → 照らしの器の広げ → 草案4 → 差分の資料 → 登録者の確かめ → 登録者の最終確認 → 公開の束（D288-j）→ push とタグ（そのつど登録者の許し）。',
     '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('D289 | uuid %s | %s | %d 字' % (uuid, jst, len(words)))
