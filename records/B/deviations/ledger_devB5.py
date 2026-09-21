# -*- coding: utf-8 -*-
"""凍結の記録の逸脱台帳に D-B5 を足し、裁定 D155〜D157 の記録を書く（登録者の言葉は会話の記録から機械で切り出す）。
**足すだけ**——台帳のほかの行と、凍結の記録の `frozen` の区画は一字も変えない（前後で確かめる）。
用法: python records/B/deviations/ledger_devB5.py <会話の記録 jsonl>"""
import os, sys, json, hashlib, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]

words, uuid, ts = None, None, None
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
        if '裁定は三件ともご推奨のとおり' in t and len(t) < 600:
            words, uuid, ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '裁定の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
appr = '登録者裁定（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」）' % (jst, uuid, words.replace(NL, ' '))

FREC = json.load(open(j('records', 'B', 'deviations', 'D-B5-flag-record.json'), encoding='utf-8'))
assert s16('records/B/results-report-B-devB1.md') == FREC['flagged_sha16']
ENTRY = ('D-B5', '2026-09-22',
         '**逸脱の下の機械の報告に旗の段を足した（登録者裁定 D156）**。凍結した組み立て器 `tools/build_report_B.py`（**変えない**）は逸脱を知らないので、'
         '`records/B/results-report-B-devB1.md` の頭の機械の区画に、印の無い確証の本数を印字していた（公開前検分・第一巡・再現 K254）。'
         '器 `records/B/deviations/flag_devB1_report.py`（SHA16 %s）が、題の直後・機械の区画の外に旗の段を一つ足した。'
         '旗を除いた本文は組み立て器の出力（SHA16 %s）と一字も違わないことを器が確かめている（旗を足した後の SHA16 %s・記録 `records/B/deviations/D-B5-flag-record.json`）。'
         '機械の区画とその記録は変わらず、凍結した走査器は違反なしで通った。凍結した集計器の報告 `results-report-B-frozen.md` には触れていない。'
         % (s16('records/B/deviations/flag_devB1_report.py'), FREC['builder_output_sha16'], FREC['flagged_sha16']),
         '報告（機械の報告の一本の・区画の外の一段）。データ・集計・札・機械の区画は変わらない')

mdp, jsp = j('records', 'B', 'FREEZE-RECORD-B.md'), j('records', 'B', 'FREEZE-RECORD-B.json')
F = json.load(open(jsp, encoding='utf-8'))
frozen_before = json.dumps(F['frozen'], sort_keys=True, ensure_ascii=False)
dev_before = json.dumps(F['deviations'], sort_keys=True, ensure_ascii=False)
assert [d['no'] for d in F['deviations']] == ['D-B1', 'D-B2', 'D-B3', 'D-B4'], '台帳の並びが思ったものと違う'
n, d, w, sc = ENTRY
F['deviations'].append({'no': n, 'date': d, 'what': w, 'scope': sc, 'approval': appr})
assert json.dumps(F['frozen'], sort_keys=True, ensure_ascii=False) == frozen_before
assert json.dumps(F['deviations'][:4], sort_keys=True, ensure_ascii=False) == dev_before
md = open(mdp, encoding='utf-8').read()
rows = [l for l in md.split(NL) if l.startswith('| D-B4 |')]
assert len(rows) == 1
row = '| %s | %s | %s | %s | %s |' % (n, d, w, sc, appr)
md2 = md.replace(rows[0] + NL, rows[0] + NL + row + NL)
assert md2.replace(row + NL, '') == md
json.dump(F, open(jsp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
open(mdp, 'w', encoding='utf-8', newline=NL).write(md2)

R = ['# 登録者裁定 D155〜D157（2026-09-22・公開前検分・第一巡の整理を受けて）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst, words.replace(NL, ' ')),
     '- 「ご推奨」の中身は `adoption-table-results-r1.md` §2（採否の案 P451〜P471）と §3（裁定の候補の三件）。', '',
     '| 裁定 | 中身 |', '|---|---|',
     '| D155 | 採否の案 P451〜P471 を採る。**事後の計算を表紙に載せる（甲）**——方向ごとの率（凍結した集計器の出力）に加えて、一番近い一本との Fisher と、方向を単位にした t（二つの形）を「登録の外・事後・札を作らない」と明記した区画に載せ、その後ろに v の腕と無操作の差（記述の族）を並べる。事後の計算は札を作らず、札を取り下げもしない |',
     '| D156 | 逸脱の下の機械の報告の題の直後（機械の区画の外）に、器で旗の段を足す。そのほかが一字も変わらないことを器が確かめ、凍結の記録の逸脱台帳に D-B5 として記帳する。表紙の「手を入れていない」は改める |',
     '| D157 | 草案2 の後の巡は、草案2 の差分と新しい区画だけを、新しい個体の系統外の一票に見せる（段階 A の最終検分と同じ型）。範囲と票数は登録者が決める |', '',
     '- 記帳: `records/B/FREEZE-RECORD-B.{md,json}` の逸脱台帳の D-B5（器 `records/B/deviations/ledger_devB5.py` が足した・`frozen` の区画と前の四行は前後で同一）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
rp = j('records', 'reviews', 'B', 'results', 'round1', 'rulings-D155-D157.md')
assert not os.path.exists(rp)
open(rp, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('ledger: D-B5 appended; approval:', appr[:140])
