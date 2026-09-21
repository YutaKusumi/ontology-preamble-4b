# -*- coding: utf-8 -*-
"""凍結の記録の逸脱台帳に D-B1〜D-B4 を記帳し、裁定 D151〜D154 の記録を書く（登録者の言葉は会話の記録から機械で切り出す）。
**足すだけ**——凍結の記録のほかの行・欄は一字も変えない（`frozen` の区画の同一性を前後で確かめる）。
用法: python records/B/deviations/ledger_devB.py <会話の記録 jsonl>"""
import os, sys, json, hashlib, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]

# ---- 登録者の言葉（逐語・機械で切り出す） ----
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
        if 'D151〜D154' in t and 'ご推奨のとおり' in t and len(t) < 600:
            words, uuid, ts = t.strip(), o.get('uuid'), o.get('timestamp')
assert words, '裁定の言葉が見つからない'
jst = (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
appr = '登録者裁定（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」）' % (jst, uuid, words.replace(NL, ' '))

ENTRIES = [
    ('D-B1', '2026-09-22',
     '**集計器の食い違いの直し（登録者裁定 D151・乙′）**。凍結した集計器 `tools/analyze_B.py`（SHA16 %s・**変えない**）は、選定後の品質床で確証族の二つの土台の腕（O-Ncold-v・Onull+v）にも選定後の段の走行を求め、'
     '凍結した起動器は正本 `quality_floor.run_order`（「(ii)…残りの介入の腕」）に従ってこの二腕を外すので、減算族と加算族の 8 対比が「判定不能（品質床）」になった（床に落ちたのではなく、走行の記録が無い）。'
     '逸脱の下の集計器 `tools/analyze_B_devB1.py`（SHA16 %s）を、生成器 `tools/make_analyze_B_devB1.py`（SHA16 %s）で凍結した器から機械で作った（差分 `records/B/deviations/D-B1-analyze_B.diff`・SHA16 %s）。'
     '違いは、選定後の段の走行が無い土台の腕の床を、門の記録 `records/B/gate-B-2026-09-21.json`（SHA16 %s・**確証の率を開く前**の記録）の・選定の段の・選ばれた層 × 係数の行で読むことと、その印だけ。'
     '検定・族・Holm・閾値は変えない。合成データでの回帰の確かめ（`records/B/deviations/regress_devB1.py`）と、同じ型の食い違いの掃き出し（`records/B/deviations/sweep-readers-writers-2026-09-22.md`・既知の一件のほか 0 件）を**走らせる前に**済ませた。'
     '逸脱の下の集計器は**一回だけ**走らせ、凍結した器の出力 `records/B/analysis-B-2026-09-22.*` と並べて公開する。直した側の確証の札は「確証（逸脱 D-B1 の下）」と印を付け、事前登録の確証と同じ身分を持たない。'
     '**直すという決定は、起草者と登録者が率と p を見た後になされた**（伺いの四票には率と p を伏せた・`records/reviews/B/incident-qpost-round/`）。'
     % (s16('tools/analyze_B.py'), s16('tools/analyze_B_devB1.py'), s16('tools/make_analyze_B_devB1.py'), s16('records/B/deviations/D-B1-analyze_B.diff'), s16('records/B/gate-B-2026-09-21.json')),
     '集計（札）——減算族・加算族の 8 対比と、それに依る数え上げ・特異性・予想の照合。データ・正本・凍結した器は変えない'),
    ('D-B2', '2026-09-22',
     '**選定後の品質床 (ii) を、本走行の前に判定しなかった**（採否表 P439・再現 K225）。正本 `quality_floor.run_order` は「(ii) は本走行の入力になるので、本走行を始める前に判定を終える」と定めるが、'
     '(ii) を本走行の前に判定する器が無かった——`tools/gate_B.py` は選定の段しか読まず、走行の段取り `records/B/run-plan-B.md` の段 6 の「`gate_B` を再度通して post の行を得る」は実現しない文だった。'
     'コーディネータは選定後の段の整合検査（不整合 0）だけで本走行を起動した（2026-09-21）。(ii) の判定は本走行の後、集計器の中で行われ、走行のあった 11 腕はすべて合格（無操作との差は下限の内側）。'
     '判定の時期が登録と違うことを記帳する。段取りの文は直さず、この行で訂正する。',
     '手順（判定の時期）。データと判定の中身は変わらない'),
    ('D-B3', '2026-09-22',
     '**選定後の段のセッション番号**（採否表 P449・再現 K233）。正本 `sessions.number_rule` は「ランタイムを新しく起動するたびに一つ進める」。品質床の相は、選定の段を調整走行と同じランタイムで（番号 1）、'
     '選定後の段を**新しいランタイム**で走らせたが、コーディネータは番号を 1 のままにした。走行キーは `…__post__…__s1`、セッション記録 `results/sessions-B/stageB-quality__s1.json` は二つのランタイムを一つに束ねている'
     '（選定の段だけの版はコミット ee9bc61 にある）。無操作の相手の引き当ては段の中で閉じるので判定は動かない。GPU と版は二つのランタイムで同じ（セッション記録）。',
     '記録（セッション番号）。データと判定は変わらない'),
    ('D-B4', '2026-09-22',
     '**率盲検の外の露出**。起動器 `tools/colab/boot_stageB.py` は、本走行でもセルごとの件数（破局・refuse を含む）を出力に印字する——登録した率盲検の外の経路（走行の段取り §5）に無い。'
     'コーディネータは出力を畳んで進捗を Drive の置き場の名で見たが、Colab のページの再読込で出力が二度展開され、画面写しに件数の欄の一部が映った（`records/B/main-run-B.md` §1）。登録者も同じタブを見うる状態だった。'
     '値は控えず、使っていない。集計は凍結した器と逸脱 D-B1 の下の器が機械で行った。',
     '率盲検（集計の前の露出）。データ・判定は変わらない'),
]

# ---- 凍結の記録に足す ----
mdp, jsp = j('records', 'B', 'FREEZE-RECORD-B.md'), j('records', 'B', 'FREEZE-RECORD-B.json')
F = json.load(open(jsp, encoding='utf-8'))
frozen_before = json.dumps(F['frozen'], sort_keys=True, ensure_ascii=False)
assert F['deviations'] == [], '既に記帳がある（足す前に確かめる）'
F['deviations'] = [{'no': n, 'date': d, 'what': w, 'scope': sc, 'approval': appr} for n, d, w, sc in ENTRIES]
assert json.dumps(F['frozen'], sort_keys=True, ensure_ascii=False) == frozen_before
json.dump(F, open(jsp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = open(mdp, encoding='utf-8').read()
anchor = '- （凍結の後に足す）' + NL
assert md.count(anchor) == 1
table = ['', '| 番号 | 日付 | 何を・なぜ | 射程 | 承認 |', '|---|---|---|---|---|'] + ['| %s | %s | %s | %s | %s |' % (n, d, w, sc, appr) for n, d, w, sc in ENTRIES]
md2 = md.replace(anchor, anchor + NL.join(table) + NL)
assert md2.replace(NL.join(table) + NL, '') == md          # 足しただけであること
open(mdp, 'w', encoding='utf-8', newline=NL).write(md2)

# ---- 裁定の記録 ----
R = ['# 登録者裁定 D151〜D154（2026-09-22・選定後の品質床の食い違いの扱い）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst, words.replace(NL, ' ')),
     '- 「ご推奨」の中身は `adoption-table-qpost.md` §3（四票の整理の後にコーディネータが出した案）。コーディネータの推奨は自分の引かれる向きと重なっていた（同 §4）。', '',
     '| 裁定 | 中身 |', '|---|---|',
     '| D151 | **乙′**——逸脱として記帳し（D-B1）、同じ型の食い違いを掃き出してから、最小の直し（二つの土台の腕の選定後の床を、門の記録の選定の段の・選ばれた組の行で読む）の集計器を一回だけ走らせ、凍結した器の出力と機械で突き合わせ、報告は**両方を同じ重さで並べる**。直した側の確証の札は「確証（逸脱 D-B1 の下）」と印を付け、要約で印の無い「確証」を使わず、直した札だけから新しい集計を作らない。丙（足りないセルを今から走らせる）は採らない |',
     '| D152 | 封印予想の照合（一度だけ）は、一つの座で、凍結した器の出力と逸脱の下の出力の両方に続けて当て、どちらも別名で残して公開する（後でどちらかを選べる形にしない）。道の選び方が起草者と登録者の的中数を動かすことを COI に書く |',
     '| D153 | 凍結の記録の逸脱台帳に D-B1（集計器の直し）・D-B2（(ii) を本走行の前に判定しなかった・段取りの段 6 の文の誤り）・D-B3（選定後の段のセッション番号）・D-B4（率盲検の外の露出）を記帳する |',
     '| D154 | 副位置の活性 `resp-*.npz`（調整走行・本走行）は Drive と手元に置いたまま、SHA-256 の一覧を記録に足す（公開の置き場には足さない・正本 `activation_storage` の `place` の型） |', '',
     '- 記帳: `records/B/FREEZE-RECORD-B.{md,json}` の逸脱台帳（`records/B/deviations/ledger_devB.py` が足した・`frozen` の区画は前後で同一）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
rp = j('records', 'reviews', 'B', 'incident-qpost-round', 'rulings-D151-D154.md')
assert not os.path.exists(rp)
open(rp, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('ledger: %d entries; approval: %s' % (len(ENTRIES), appr[:120]))
