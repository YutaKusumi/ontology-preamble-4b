# -*- coding: utf-8 -*-
"""rulings_D271.py v0（2026-09-30・B′ の裁定 D271 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
言葉は字のまま（逐語）で、時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。
用法: python rulings_D271.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D271.md')
KEY = 'ご推奨の案で進めてください。私が使っているPCのCPUは計算資源が限られているので'
NL = chr(10)


def text_of(o):
    m = o.get('message') or {}
    c = m.get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = [x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text']
        return ''.join(parts)
    return ''


def jst(ts):
    t = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    return t.astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    hits = []
    for line in open(sys.argv[1], encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get('type') != 'user' or (o.get('message') or {}).get('role') != 'user':
            continue
        c = (o.get('message') or {}).get('content')
        if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
            continue
        s = text_of(o)
        if KEY in s:
            hits.append((o['uuid'], o['timestamp'], s))
    uniq = {h[0]: h for h in hits}
    assert len(uniq) == 1, ('登録者の発話がちょうど一つでない', len(uniq))
    uid, ts, s = next(iter(uniq.values()))
    body = s[s.index('南無汝我曼荼羅'):] if '南無汝我曼荼羅' in s else s
    q_all = body.strip()
    L = ['# 裁定 D271（B′ の器の段の決めの二つ目・公開の置き場に移す範囲・外への問い合わせと小さな試し・Colab の活用の許し・2026-09-30・コーディネータ南無弥勒如来・非公開）', '',
         '- **D271**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - 「決めていただきたいこと」（コーディネータの途中の報告の五項目）は、推しの案で進める:',
         '    - K11（行動の下見の生成のバッチの大きさ）: 8（升目ごとの試行を 8 ずつのバッチで生成する・凍結の前の確かめの煙試験で記憶が足りることを確かめる）。',
         '    - 公開の置き場に移す範囲: 移さないのは、分けた transformers（`pylib/`）・Hugging Face から落とした設定とトークナイザ（`hf/`・手元の目録は記録として移す）・モデルカードの写し（`sources/`・他者の著作物）。'
         '器の前の版（`tools/prev/`）と Gemma の中立の課題の感触の確かめ（`model-feel/`・`model-feel-2/`）は移す。',
         '    - K9（重みの断片の目録）: Hugging Face の目録（メタデータ）に一度問い合わせ、断片の SHA-256 を取る（重みは落とさない・資格情報は使わない）。',
         '    - 器の実装の検分の前の小さな試し: 登録者の Chrome で claude.ai の新しいチャットを一つ開き、実行の場の試しの台本を走らせてもらう（検分の中身は送らない）。',
         '    - 「原稿の数を正本の鍵で束ねる」の読み方: 凍結の本文のすべての数（§6 と凍結の一行を除く）が正本に登録されていることを器で確かめる。',
         '  - Colab の活用の許し: 登録者の PC の CPU は計算資源が限られているので、必要であれば Colab を使ってよい（コーディネータの考えを尋ねられた）。'
         'コーディネータの答え（同じ時の返信）: 合成データの正式の確かめ（小さな模型で起動器の全ての相を通す走り）を Colab の CPU のランタイムで走らせる。'
         '公開前の器・正本・記録は zip にして Colab の「ファイル」から上げ（GitHub には push しない）、結果の zip は落として手元で SHA を照らし、ランタイムは照らした直後に削除する。時機は別の個体が終わり、正本 v4 を書いてから。',
         '- 正本と草案への入れ方: 正本は v4（D270 と合わせて）で、`behavior_pilot.seeds.batch_size` に 8 を置き、`decisions` に D271 を足し、器の段の所見 K11〜K15 を `tools_findings` に足し、凍結の本文の数の読み方を `computation` に書く。'
         '移し方の表（`tools/bprime_publish_map.py`）は、登録者の決めの物を移す規則に替える。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D271.md | uuid %s | %s JST | chars %d' % (uid, jst(ts), len(q_all)))


if __name__ == '__main__':
    main()
