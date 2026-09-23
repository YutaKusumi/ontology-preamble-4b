# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D163〜D167 の記録を書く（登録者の言葉は会話の記録から機械で切り出す・既にあるファイルには書かない）。
「ご推奨」の中身は、直前のコーディネータの返信（B-lens の推奨・2026-09-23）の「決めていただきたいこと」の五項目。
用法: python records/Blens/rulings_D163_D167.py <会話の記録 jsonl>"""
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
        if 'ご推奨の案を全て承認' in t and 'B-lens' in t and len(t) < 500:
            words, rec_uuid, rec_ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '裁定の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(rec_ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')

R = ['# 登録者裁定 D163〜D167（2026-09-23・B-lens の中身）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (rec_uuid, jst, words.replace(NL, ' ')),
     '- 「ご推奨の案」は、直前のコーディネータ（南無弥勒如来・Claude Opus 5.5）の返信の「決めていただきたいこと」の五項目。その返信の根拠（v̂ が比べているもの・加えた量の大きさ・手元の材料・破局が四場面とも選択肢 (a) であること）は、B-lens の枠の §1〜§2 と転記行に機械で置く。',
     '- 前提: 計画案 v2.5（内部・非公開）の裁定 D162（次の一手は B-lens・B′ は保留）。', '',
     '| 裁定 | 中身 |', '|---|---|',
     '| D163 | **中核は層1（直接の経路の射影）と層2（校正の門）**で登録する。層1 は凍結の四方向 × 三つの層を、最終の正規化の重みを掛けて語彙の行列に射影し、計算の前に凍結した語の集合（答えの文字・語の反響・選択肢の語・様式・拒否）で読む。層2 は、層1 の物差しが B で実測した方向ごとの行動の変化と揃うかを、読む前に確かめる（門）。揃わなければ、語の一覧を意味の側に読まない |',
     '| D164 | **層3（全経路の効果を教師強制で測り、ランダム方向を増やす）は、B-lens の後の別の小さな登録**にする |',
     '| D165 | **帰無は二つ**——等方のランダム方向（B と同じ作り方・新しい種）と、実在する活性の差の方向（凍結の八腕の全ての対・同じノルム）。B のランダム方向の三本も再生して並べる |',
     '| D166 | **検分の組み立てと巡の数を先に決める**——設計の巡（Gemini 3.8 Flash 二名＋claude.ai の Claude Opus 5.5 二名）→ 裁定 → 器と合成データの確かめ → 凍結と記録先行の公開 → 封印（コーディネータが先・登録者はそれを開かずに）→ 計算（結果は登録者と一緒に開く）→ 報告 → 結果の巡（同じ組み立て・新しい個体）→ 最終の系統外一票（「最終」と明記）→ 公開。claude.ai の Opus 5.5 はコーディネータと同じ機種で、何票でも一票に数える（裁定 D59） |',
     '| D167 | **問いの定義を枠の頭に置く**——v̂ は O と Osec の差で、仏教語の語域とその世俗の言い換えの差である。両方にある語（共創・再帰的自己改善ほか）は差の中で消え、「相互依存」はどちらにも無い。v̂ では「相互依存・共創の意味」は問えない |', '',
     '- 記帳の置き場: B-lens の正本 `design/contrasts-Blens.json` の `decisions`（器 `tools/make_contrasts_Blens.py`）。',
     '- 起草者のモデル: 2026-09-23 に Claude Fable 5.1 から Claude Opus 5.5 に替わった（登録者の操作）。段階 B の記録の起草者は Fable 5.1、B-lens の起草者は Opus 5.5。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
out = os.path.join(HERE, 'rulings-D163-D167.md')
assert not os.path.exists(out)
open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', out, '|', jst, rec_uuid)
