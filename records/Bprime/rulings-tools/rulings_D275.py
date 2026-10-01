# -*- coding: utf-8 -*-
"""rulings_D275.py v0（2026-09-30・B′ の裁定 D275 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、本文の全体が決まった文と一字違わず同じで、決まった時刻より後のものを一つだけ取る（二つ以上か零なら止める）。
（D274 と同じ文面の発話なので、D274 の発話〔2026-09-30T09:55:46Z〕より後の時刻で区別する。）言葉は字のまま（逐語）で、時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。
用法: python rulings_D275.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D275.md')
FULL = '南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏ご推奨の案で進めてください。よろしくお願いします🍵'
AFTER = '2026-09-30T10:00:00Z'
NL = chr(10)


def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
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
        if text_of(o).strip() == FULL and o['timestamp'] > AFTER:
            hits.append((o['uuid'], o['timestamp']))
    uniq = dict(hits)
    assert len(uniq) == 1, ('登録者の発話がちょうど一つでない', len(uniq))
    uid, ts = next(iter(uniq.items()))
    L = ['# 裁定 D275（B′ の器の実装の検分・R2 への追い問い・改行の固定・限界・器の直しに入ること・2026-09-30・コーディネータ南無弥勒如来・非公開）', '',
         '- **D275**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), FULL),
         '  - 採否の表の草案（`reviews/impl/adoption-impl-Bprime.md`・41 行）の報告の後の決め。「決めていただきたいこと」の四項目は、推しの案で進める:',
         '    - 追い問い: 票で「重い」を出した R2 のチャット（claude-ai-11）にだけ、コーディネータの読みと直し方の案（表の U01〜U08）を示して確かめてもらう追い問いを一つ送る。R1 は「重い」が無いので送らない。',
         '    - U32（改行の扱い）: 公開の置き場に `.gitattributes` を置き、records と tools の改行を LF に固定する（公開の置き場への書き込みなので、push の時に改めて確認を得る）。',
         '    - U40（R1-14・28 本の実在の差の方向はどの道でも作り直されない）: 限界として書く（別の個体の器は変えない決まりで、コーディネータの器に足すと独立の確かめにならない）。',
         '    - 器の直し: 追い問いの返事を受けてから、表のとおりに器を直し始める。重い走り（合成データの確かめの取り直し）は Colab で回す。直し終えた後に、直しの確かめの巡を足すかを改めて相談する。',
         '  - R1-17（Nk の行はどの段でも計算し直されない）は、預かっている「一段目に Nk の行を入れるか」（正本 `independent_recompute.nk_decision`）の決めの材料として記録する。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D275.md | uuid %s | %s JST' % (uid, jst(ts)))


if __name__ == '__main__':
    main()
