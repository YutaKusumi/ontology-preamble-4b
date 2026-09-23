# -*- coding: utf-8 -*-
"""凍結の記録の逸脱台帳に D-B6 を足し、D-B5 の行に旗の改め（v2）を追記し、裁定 D158〜D160 の記録を書く（登録者の言葉は会話の記録から機械で切り出す）。
足すだけ——`frozen` の区画と D-B1〜D-B4 の行は一字も変えない（前後で確かめる）。D-B5 の行は末尾に追記の一文を足すだけ（元の文は残す）。
用法: python records/B/deviations/ledger_devB6.py <会話の記録 jsonl>"""
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
        if '7c45651' in t and '最終検分である旨' in t and len(t) < 800:
            words, uuid, ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '裁定の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
appr = '登録者裁定（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」）' % (jst, uuid, words.replace(NL, ' '))

FREC = json.load(open(j('records', 'B', 'deviations', 'flag-record-B-2026-09-23.json'), encoding='utf-8'))
for k, f in (('devB1', 'records/B/results-report-B-devB1.md'), ('frozen', 'records/B/results-report-B-frozen.md')):
    assert s16(f) == FREC['reports'][k]['flagged_sha16'], k
tool = s16('records/B/deviations/flag_reports_B.py')
D6 = ('D-B6', '2026-09-23',
      '**凍結した集計器の機械の報告に旗の段を足した（登録者裁定 D159）**。`records/B/results-report-B-frozen.md` を単体で引くと、頭の要約の「判定不能（品質床）」の本数が品質床に落ちたと読まれる（公開前検分・第二巡・再現 K281）。'
      '凍結した組み立て器は変えず、器 `records/B/deviations/flag_reports_B.py` v2（SHA16 %s）が題の直後・機械の区画の外に旗の段を一つ足した。旗を除いた本文は組み立て器の出力（SHA16 %s）と一字も違わないことを器が確かめている（旗を足した後の SHA16 %s・記録 `records/B/deviations/flag-record-B-2026-09-23.json`）。'
      '機械の区画とその記録は変わらず、凍結した走査器は違反なしで通った。' % (tool, FREC['reports']['frozen']['builder_output_sha16'], FREC['reports']['frozen']['flagged_sha16']),
      '報告（機械の報告の一本の・区画の外の一段）。データ・集計・札・機械の区画は変わらない')
D5_ADD = ('**追記（2026-09-23・登録者裁定 D159）**: 旗の段を同じ器の v2（`flag_reports_B.py`・SHA16 %s）で改めた——内訳（事前登録の確証と逸脱の下の札の本数・漢数字）・連れの二本の指し方・数え上げの範囲を足した（第二巡・再現 K280）。'
          '旗を除いた本文の同一性（SHA16 %s）は保った。改めた後の SHA16 %s。' % (tool, FREC['reports']['devB1']['builder_output_sha16'], FREC['reports']['devB1']['flagged_sha16']))

mdp, jsp = j('records', 'B', 'FREEZE-RECORD-B.md'), j('records', 'B', 'FREEZE-RECORD-B.json')
F = json.load(open(jsp, encoding='utf-8'))
frozen_before = json.dumps(F['frozen'], sort_keys=True, ensure_ascii=False)
first4 = json.dumps(F['deviations'][:4], sort_keys=True, ensure_ascii=False)
assert [d['no'] for d in F['deviations']] == ['D-B1', 'D-B2', 'D-B3', 'D-B4', 'D-B5']
d5_old = F['deviations'][4]['what']
F['deviations'][4]['what'] = d5_old + ' ' + D5_ADD
n, d, w, sc = D6
F['deviations'].append({'no': n, 'date': d, 'what': w, 'scope': sc, 'approval': appr})
assert json.dumps(F['frozen'], sort_keys=True, ensure_ascii=False) == frozen_before
assert json.dumps(F['deviations'][:4], sort_keys=True, ensure_ascii=False) == first4
assert F['deviations'][4]['what'].startswith(d5_old)
md = open(mdp, encoding='utf-8').read()
rows = [l for l in md.split(NL) if l.startswith('| D-B5 |')]
assert len(rows) == 1
cells = rows[0].split(' | ')
assert len(cells) == 5 and d5_old in cells[2]
cells[2] = cells[2] + ' ' + D5_ADD
row5 = ' | '.join(cells)
row6 = '| %s | %s | %s | %s | %s |' % (n, d, w, sc, appr)
md2 = md.replace(rows[0] + NL, row5 + NL + row6 + NL)
assert md2.count(D5_ADD) == 1 and md2.count(row6) == 1 and md2.replace(row5 + NL + row6 + NL, rows[0] + NL) == md
json.dump(F, open(jsp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
open(mdp, 'w', encoding='utf-8', newline=NL).write(md2)

R = ['# 登録者裁定 D158〜D160（2026-09-23・公開前検分・第二巡の整理を受けて）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst, words.replace(NL, ' ')),
     '- 「ご推奨」の中身は `adoption-table-results-r2.md` §2（採否の案 P472〜P487）と §3（裁定の候補の三件）。', '',
     '| 裁定 | 中身 |', '|---|---|',
     '| D158 | 採否の案 P472〜P487 を採る。**事後の計算の見せ方は甲**（D155 の再裁定）——表紙の事後の区画を「範囲（三本の最小〜最大）・一番近い一本との差・その両側 Fisher・三本の等質性の χ²・下限つきの方向を単位にした形（一列）」にし、順位の下限の一文を頭に置く。形一・形二は記録のファイルに残し、表紙からは外す。事後の計算は札を作らず、札を取り下げない |',
     '| D159 | 凍結した集計器の機械の報告にも、同じ器の型で旗の段を足す（逸脱 D-B6）。逸脱の下の報告の旗は内訳・連れの指し方・範囲を足して改める（D-B5 の追記） |',
     '| D160 | 草案3 の差分だけを、新しい個体の**系統外**一票に見せる。**依頼文に、これが最終の検分であることを書く**（検分の繰り返しを避けるため・登録者の指示）。範囲と票数は登録者が決める |', '',
     '- 記帳: `records/B/FREEZE-RECORD-B.{md,json}` の逸脱台帳の D-B6 と D-B5 の追記（器 `records/B/deviations/ledger_devB6.py`・`frozen` の区画と D-B1〜D-B4 は前後で同一）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
rp = j('records', 'reviews', 'B', 'results', 'round2', 'rulings-D158-D160.md')
assert not os.path.exists(rp)
open(rp, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('ledger: D-B6 appended, D-B5 annotated; approval:', appr[:120])
