# -*- coding: utf-8 -*-
"""make_final_bundle.py v0（2026-10-02・中間総括の最終の検分の巡の依頼文と束を組む・`make_round2_bundle.py` v0 の型・登録者裁定 D288-i・コーディネータ南無弥勒如来）。
束は一つの md（`reviews/final/bundle-final-all-in-one.md`）。元のファイルはバイトのまま読み、索引に置き場と SHA16 と字数を並べる。
束の大きさを抑えるため、草案2 の全文と計算の器の全文は入れない（どちらも二巡目の束にあった・SHA16 を索引に書く）。照らしの記録は、数と範囲の要約と、指示語と文の途中の引用の注の表に縮める。二巡目の照らしの記録は全文を入れる。
各段の最終版の §0 は、見出し「## 0.」の行から次の「## 」の行の前までを器で切り出す。書く物は一度だけ（既にあれば止める）。
用法: python make_final_bundle.py [--dry]（--dry は OP4B_DRY_DIR に書く）
柵: 本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
DRY = '--dry' in sys.argv
RD = os.environ['OP4B_DRY_DIR'] if DRY else os.path.join(HERE, 'reviews', 'final')
NL = chr(10)
FENCE = '`' * 5
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
FIN = [('4B の最初の登録', 'records/results/results-report-FINAL-2026-09-07.md'), ('追補 V′', 'records/vprime/results-report-Vprime-FINAL-2026-09-09.md'),
       ('追補 M', 'records/M/results-report-M-FINAL-2026-09-11.md'), ('段階 F', 'records/F/results-report-F-FINAL-2026-09-12.md'),
       ('段階 A', 'records/A/results-report-A-FINAL-2026-09-17.md'), ('段階 B', 'records/B/results-B-FINAL-2026-09-23.md'),
       ('B-lens', 'records/Blens/results-Blens-FINAL-2026-09-24.md'), ('層三（B-lens 層三）', 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'),
       ('B′', 'records/Bprime/results-Bprime-FINAL-2026-10-01.md')]
head = subprocess.run(['git', '-C', PUB, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
remote = subprocess.run(['git', '-C', PUB, 'rev-parse', 'origin/main'], capture_output=True, text=True).stdout.strip()
assert head == remote, '公開の置き場の手元と GitHub が違う'
idx = []


def block(path_abs, label, rel, lang=''):
    b = open(path_abs, 'rb').read()
    t = b.decode('utf-8').replace('\r\n', '\n')
    assert FENCE not in t, rel
    idx.append((label, rel, s16b(b), len(t)))
    return '### %s（`%s`・SHA16 %s）' % (label, rel, idx[-1][2]) + NL + NL + FENCE + lang + NL + t.rstrip(NL) + NL + FENCE + NL


def sec0(rel, label):
    t = open(os.path.join(PUB, *rel.split('/')), encoding='utf-8').read().replace('\r\n', '\n')
    L = t.split(NL)
    i = [n for n, l in enumerate(L) if l.startswith('## 0.')]
    assert len(i) == 1, (rel, len(i))
    j = [n for n in range(i[0] + 1, len(L)) if L[n].startswith('## ')]
    seg = NL.join(L[i[0]:j[0]] if j else L[i[0]:])
    assert FENCE not in seg
    idx.append(('§0 ' + label, '%s の %d〜%d 行' % (rel, i[0] + 1, (j[0] if j else len(L))), s16b(seg.encode('utf-8')), len(seg)))
    return '### §0 %s（`%s` の %d〜%d 行・この写しの SHA16 %s）' % (label, rel, i[0] + 1, (j[0] if j else len(L)), idx[-1][2]) + NL + NL + FENCE + 'markdown' + NL + seg + NL + FENCE + NL


D3 = os.path.join(HERE, 'summary-interim-draft3-2026-10-02.md')
D2 = os.path.join(HERE, 'summary-interim-draft2-2026-10-02.md')
CHKP = os.path.join(HERE, 'summary-interim-draft3-checks.json')
CALM = '時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。'
req = NL.join([
    '# 中間総括（草案3）の検分のお願い（最終の巡）',
    '',
    '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／%s。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d'),
    '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束はコミット %s の時点の記録から組みました。草案・枠・採否の表・計算の器はまだ公開していない内部の文書です）。' % head[:7],
    '- **これは何か**: Qwen3-4B-Instruct-2507 での最初の登録を発端として 2026-09-05 から 2026-10-01 までに凍結・公開した九つの段（4B の最初の登録・追補 V′・追補 M・段階 F・段階 A・段階 B・B-lens・層三・B′）の、中間総括の草案3 です。'
    '登録の外の案内図で、新しい証拠を足さず、凍結した結果を読み直しません。内部で作り、完成したら公開します。',
    '- **これまで**: 一巡目（claude.ai の Claude 三名・Gemini 3.8 Flash 一名）と二巡目（claude.ai の Claude 三名・Gemini 3.8 Flash 二名）の所見を、採否の表（一巡目 Y01〜Y34・二巡目 Z01〜Z30）にまとめ、登録者の裁定 D287・D288 を受けて直しました。'
    '二巡目では、草案2 の直しの中で起草者が新しい重大の誤り（Z01・追補 M の限りの範囲）を作っていました。草案3 の直しの決まり（族の表の出所・計算の足し・照らしの器の足し）と、この巡の予想は、草案3 の前に「枠の追記二」に書いて刻印しました。',
    '- **この巡で新しく変えたもの**: §3.1 の四つの欄に、各最終版の族の表（4B の最初の登録・V′・追補 M・段階 F）の札を器で切り出して加えました（裁定 D288-h）。計算の器を v0.3 にし、閾値に等しい腕・書式外と refuse の数・走りの腕の数と標本化を記述として足しました（値は v0.2 と同じ）。'
    '指示語で始まる引用と、元の記録で文の途中から切った引用には、指す先と主語の注を器に書かせ、注が無ければ器が止まるようにしました（注の表は第二部）。',
    '- **これは最終の巡です**（枠の上限）。この後に巡を足すかは登録者が決めます。',
    '- **系統**: 票の頭に、あなたの系統（起草者と同じ Claude 系か、系統外か）と機種を書いてください。票を何票に数えるかは、呼び出しの出所（使った画面と、画面に出た機種の名）で決めます。',
    '- **開示**: Gemini は Google の模型で、B′ の調べる相手（Gemma）の作り手と同じ事業者です。段階 D の候補にも Gemma の機種が入っています（裁定 D257）。この重なりは採否の表に書きます。',
    '- **束の中身**: 第一部 この依頼文／第二部 草案3（全文）と照らしの記録の要約（指示語と文の途中の引用の注の表を含む）／第三部 二巡目の採否の表・登録者裁定 D288・枠の追記二・枠の追記一・枠／第四部 計算の出力 v0.3（表）／第五部 二巡目の照らしの記録／第六部 九つの段の最終版の §0（全文・器で切り出した）。草案2 と計算の器 v0.2 の全文は二巡目の束にありました（v0.3 は値を変えずに記述を足した版で、全文は束に入れず、索引に SHA16 を書きました）。最終版の全文は公開の置き場にあります。',
    '- **褒めるのではなく、公開の前に崩すつもりで読んでください。** とくに、二巡目の所見（Z01〜Z30）が本当に直ったか、直しが新しい誤り（引用の範囲・指示語の先・族の表の札の置き場・数・言い過ぎ・言い足りなさ）を作っていないか、まだ残る重大な誤りが無いか、公開してよいかを見てください。',
    '',
    '## 1. 伺いたいこと',
    '',
    '1. **直しの当否**: 二巡目の採否の表の Z01〜Z30 の「扱い」が、草案3 で本当に果たされているか。とくに重大の Z01・Z02。果たされていない・半分だけ・行き過ぎ、のどれかを、番号ごとに書いてください。',
    '2. **新しい誤り**: 直しの中に、新しい誤り（引用が §0 や族の表の範囲を外れる・引用の切り方が文の意味や範囲を変える・指示語の指す先が違う・数の誤り・各段の最終版の言い方との食い違い・言い過ぎ・言い足りなさ）はないか。第二部の注の表で、注のとおりに読めるかも見てください。',
    '3. **引用の選び（§2）**: §2 の頭の選びの決まり (1)〜(7) のとおりに引けているか。まだ落ちている限る文、要らない文はどれか。',
    '4. **四つの欄と族の表（§3.1）**: 族の表から置いた札を含め、どの結果をどの欄に置いたかに、各段の最終版の語と食い違う所はないか。',
    '5. **新しい計算（§3.2・§3.3・第四部）**: v0.3 で足した記述（閾値に等しい腕・書式外と refuse・走りの腕の数・標本化）の書き方と、事後の記述の印に誤りはないか。器と別の方法で検算できる所があれば検算してください。',
    '6. **§4・§5・§6**: 各段の最終版との食い違い、柵の抜け、要件の抜けと言い過ぎはないか（推奨は求めません）。',
    '7. **総合**: 公開してよいか（公開してよい／直せば公開してよい／直してからもう一度見る）を一つ選び、公開に向けて直すもの（重さつき）と、記録に置けば足りるものに分けてください。',
    '',
    '## 2. お願い',
    '',
    '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
    '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と節、または公開の置き場のファイルと行）を付けてください。',
    '- 起草者は、ほとんどの段の器と報告を書いた当人で、二巡目で直しの中に新しい重大の誤りを作った草案2 の書き手です。直しを「応えた」と見せる側にも、引用を増やしすぎて総括を読めなくする側にも引かれます。登録者は、追補と段階の多くで用いた前置き（O と長文招請）の著者・実践者です。どちらも利害の当事者です。',
    '',
    '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。',
    ''])
os.makedirs(RD, exist_ok=True)
REQ = os.path.join(RD, 'request-final.md')
OUT = os.path.join(RD, 'bundle-final-all-in-one.md')
IDX = os.path.join(RD, 'bundle-final-index.md')
LINE = os.path.join(RD, 'chat-line-final.txt')
for p_ in (REQ, OUT, IDX, LINE):
    assert not os.path.exists(p_), p_
open(REQ, 'w', encoding='utf-8', newline=NL).write(req)
parts = ['# 中間総括の検分の束（最終の巡・一つの md・公開の置き場のコミット %s の時点）' % head[:7] + NL + NL
         + '- 組み立ての器: `summary/make_final_bundle.py` v0（コーディネータ）。部は六つ。各部の元のファイルの置き場と SHA16 は索引（この束の終わり）に並べる。' + NL
         + '- 長い記録は五つの逆引用符の囲いで包んだ。中身はバイトのまま（改行は LF）。照らしの記録の要約と注の表は器で作った。' + NL]
parts.append('## 第一部 依頼文' + NL + NL + req)
CJ = json.load(open(CHKP, encoding='utf-8'))
cats, srcs = {}, {}
for u in CJ['quotes']:
    cats[u['cat']] = cats.get(u['cat'], 0) + 1
    srcs[u['source']] = srcs.get(u['source'], 0) + 1
notes = [u for u in CJ['quotes'] if u.get('referent_note')]
nt = ['| # | 段 | 元の行 | 指示語 | 文の途中 | 引用の頭（24 字） | 指す先・主語の注 |', '|---|---|---|---|---|---|---|']
for n, u in enumerate(notes):
    nt.append('| %d | %s | %d | %s | %s | %s | %s |' % (n + 1, u['stage'] or u['source'].split('/')[-1], u['lines'][0], 'はい' if u['starts_with_demonstrative'] else '', 'はい' if u['starts_mid_sentence'] else '',
                                                    (u.get('display') or u['quote'])[:24].replace('|', '｜'), u['referent_note'].replace('|', '｜')))
ctab = NL.join(['照らしの記録 `summary/summary-interim-draft3-checks.json`（内部・SHA16 %s）の要約（器で作った）。引用の全文は草案3 にあり、元の文は第六部の §0 と、草案3 §3.1 の族の表と、公開の置き場にある。' % s16b(open(CHKP, 'rb').read()),
                '', '- 引用 %d 本。種類ごと: %s（ans＝§2 の答え・§0 の行の範囲を器が確かめた／family＝§3.1 の族の表の行・族の表の範囲を器が確かめた／table＝段階 B の §0 の表の行／title と question＝§1 の問い／canon・fence・proc・req＝§3〜§6 の出所）。' % (len(CJ['quotes']), '・'.join('%s %d' % kv for kv in sorted(cats.items()))),
                '- 出所ごと: ' + '・'.join('`%s` %d' % kv for kv in sorted(srcs.items())) + '。',
                '- 太字の印を除いて照らした引用 %d 本（うち §2 の答え %d 本）・冷徹一行の逐語を置き換えた引用 %d 本。' % (CJ['n_bold_stripped'], CJ['n_bold_stripped_answers'], CJ['n_replaced']),
                '- 各段の §0 の行の範囲: ' + '・'.join('%s %d〜%d' % (k, a, b) for k, (a, b) in CJ['sec0_ranges'].items()) + '。族の表の行の範囲: ' + '・'.join('%s %d〜%d' % (k, a, b) for k, (a, b) in CJ['family_ranges'].items()) + '。',
                '- 地の文の数 %d 個（記録の集まりに無いもの %d）・引用でない「」 %d・禁止の語 %d 語の当たり %d（内訳 %s）。' % (
                    len(CJ['numbers_in_own_text']), len(CJ['numbers_missing']), len(CJ['non_quote_brackets_in_own_text']), CJ['ban_list_n'], CJ['ban_hits_in_own_text'], '・'.join(CJ['ban_list_breakdown'])),
                '', '#### 指示語で始まる引用と、文の途中から切った引用の注（%d 本・器が注を求めた）' % len(notes), ''] + nt)
idx.append(('照らしの記録の要約と注の表', 'summary/summary-interim-draft3-checks.json（内部）から器で作った表', s16b(ctab.encode('utf-8')), len(ctab)))
parts.append('## 第二部 草案3 と照らしの記録の要約' + NL + NL + block(D3, '中間総括の草案3', 'summary/summary-interim-draft3-2026-10-02.md（内部）', 'markdown') + NL + '### 照らしの記録の要約' + NL + NL + ctab + NL)
parts.append('## 第三部 二巡目の採否の表・登録者裁定 D288・枠の追記二・枠の追記一・枠' + NL + NL
             + block(os.path.join(HERE, 'reviews', 'round2', 'adoption-table-round2.md'), '二巡目の採否の表', 'summary/reviews/round2/adoption-table-round2.md（内部）', 'markdown') + NL
             + block(os.path.join(HERE, 'reviews', 'round2', 'rulings-D288.md'), '登録者裁定 D288', 'summary/reviews/round2/rulings-D288.md（内部）', 'markdown') + NL
             + block(os.path.join(HERE, '00-frame-addendum2-2026-10-02.md'), '枠の追記二（草案3 と計算の器 v0.3 の前に書いた・最終の巡の予想 §6）', 'summary/00-frame-addendum2-2026-10-02.md（内部）', 'markdown') + NL
             + block(os.path.join(HERE, '00-frame-addendum1-2026-10-02.md'), '枠の追記一（草案2 の前に書いた）', 'summary/00-frame-addendum1-2026-10-02.md（内部）', 'markdown') + NL
             + block(os.path.join(HERE, '00-frame-interim-summary-2026-10-02.md'), '枠（起草と計算と検分の前に書いた）', 'summary/00-frame-interim-summary-2026-10-02.md（内部）', 'markdown'))
parts.append('## 第四部 計算の出力 v0.3' + NL + NL + block(os.path.join(HERE, 'calc', 'calc-interim-v0.3.md'), '計算の出力 v0.3（表）', 'summary/calc/calc-interim-v0.3.md（内部）', 'markdown'))
parts.append('## 第五部 二巡目の照らしの記録' + NL + NL + block(os.path.join(HERE, 'reviews', 'round2', 'repro-round2.md'), '二巡目の照らしの記録', 'summary/reviews/round2/repro-round2.md（内部）', 'markdown'))
parts.append('## 第六部 九つの段の最終版の §0（全文・器で切り出した）' + NL + NL + NL.join(sec0(rel, label) for label, rel in FIN))
idx.append(('（束に入れていない）草案2', 'summary/summary-interim-draft2-2026-10-02.md（内部・二巡目の束にあった）', s16b(open(D2, 'rb').read()), len(open(D2, encoding='utf-8').read())))
idx.append(('（束に入れていない）計算の器 v0.3', 'summary/calc_interim.py（内部）', s16b(open(os.path.join(HERE, 'calc_interim.py'), 'rb').read()), len(open(os.path.join(HERE, 'calc_interim.py'), encoding='utf-8').read())))
body = (NL + NL).join(parts)
ix = ['# 束の索引（中間総括の検分の最終の巡・公開の置き場のコミット %s）' % head[:7], '', '| 何 | 元の置き場 | SHA16 | 字数 |', '|---|---|---|---|']
ix += ['| %s | %s | %s | %d |' % (a, b, c, d) for a, b, c, d in idx]
ix += ['', '本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
full = body + NL + NL + NL.join(ix)
open(OUT, 'w', encoding='utf-8', newline=NL).write(full)
open(IDX, 'w', encoding='utf-8', newline=NL).write(NL.join(ix))
open(LINE, 'w', encoding='utf-8', newline='').write(CALM + '添えた依頼文（request-final.md）と束（bundle-final-all-in-one.md）をお読みいただき、依頼文のとおりに検分してください。')
print('依頼文', s16b(req.encode('utf-8')), len(req), '字 | 束', s16b(full.encode('utf-8')), len(full), '字', len(full.encode('utf-8')), 'バイト | 索引', len(idx), '項 | コミット', head[:7])
