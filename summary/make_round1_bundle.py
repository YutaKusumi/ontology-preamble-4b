# -*- coding: utf-8 -*-
"""make_round1_bundle.py v0（2026-10-02・中間総括の検分の一巡目の依頼文と束を組む・コーディネータ南無弥勒如来）。
束は一つの md（`reviews/round1/bundle-round1-all-in-one.md`）。元のファイルはバイトのまま読み、索引に置き場と SHA16 と字数を並べる。各段の最終版の §0 は、見出し「## 0.」の行から次の「## 」の行の前までを器で切り出す。
書く物は一度だけ（既にあれば止める）。用法: python make_round1_bundle.py
柵: 本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
RD = os.path.join(HERE, 'reviews', 'round1')
NL = chr(10)
FENCE = '`' * 5
CALM = '時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。'
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
    t = b.decode('utf-8')
    assert FENCE not in t, rel
    idx.append((label, rel, s16b(b), len(t)))
    return '### %s（`%s`・SHA16 %s）\n\n%s%s\n%s\n%s\n' % (label, rel, idx[-1][2], FENCE, lang, t.rstrip('\n'), FENCE)


def sec0(rel, label):
    t = open(os.path.join(PUB, *rel.split('/')), encoding='utf-8').read()
    L = t.split(NL)
    i = [n for n, l in enumerate(L) if l.startswith('## 0.')]
    assert len(i) == 1, (rel, len(i))
    j = [n for n in range(i[0] + 1, len(L)) if L[n].startswith('## ')]
    seg = NL.join(L[i[0]:j[0]] if j else L[i[0]:])
    assert FENCE not in seg
    idx.append(('§0 ' + label, '%s の %d〜%d 行' % (rel, i[0] + 1, (j[0] if j else len(L))), s16b(seg.encode('utf-8')), len(seg)))
    return '### §0 %s（`%s` の %d〜%d 行・この写しの SHA16 %s）\n\n%smarkdown\n%s\n%s\n' % (label, rel, i[0] + 1, (j[0] if j else len(L)), idx[-1][2], FENCE, seg, FENCE)


DRAFT = os.path.join(HERE, 'summary-interim-draft1-2026-10-02.md')
FRAME = os.path.join(HERE, '00-frame-interim-summary-2026-10-02.md')
req = NL.join([
    '# 中間総括（草案1）の検分のお願い（一巡目）',
    '',
    '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／%s。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d'),
    '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束はコミット %s の時点の記録から組みました。草案と枠と計算の器はまだ公開していない内部の文書です）。' % head[:7],
    '- **これは何か**: Qwen3-4B-Instruct を発端として 2026-09-05 から 2026-10-01 までに凍結・公開した九つの段（4B の最初の登録・追補 V′・追補 M・段階 F・段階 A・段階 B・B-lens・層三・B′）の、中間総括の草案1 です。'
    '登録の外の案内図で、新しい証拠を足さず、凍結した結果を読み直しません。内部で作り、完成したら公開します。検分は要る回数を行いますが、巡は二巡と最終の一票までを上限にしています。',
    '- **新しい計算**: 起草の途中で、既に公開した記録だけから計算できる記述を二つ足しました（動く幅の地図・段階 C の対称性の記述）。どちらも登録の外の記述で、札を付けず、検定もしません。定義は値を計算する前に枠に書きました。',
    '- **系統**: 票の頭に、あなたの系統（起草者と同じ Claude 系か、系統外か）と機種を書いてください。票を何票に数えるかは、呼び出しの出所（使った画面と、画面に出た機種の名）で決めます。',
    '- **開示**: Gemini は Google の模型で、B′ の調べる相手（Gemma）の作り手と同じ事業者です。この重なりは採否の表に書きます。',
    '- **束の中身**: 第一部 この依頼文／第二部 草案1（全文）と引用の照らしの記録／第三部 枠（起草と計算と検分の前に書いた）／第四部 新しい計算の器と出力（全文）／第五部 九つの段の最終版の §0（全文・器で切り出した）。最終版の全文は公開の置き場にあります（第五部の見出しに置き場）。',
    '- **褒めるのではなく、公開の前に崩すつもりで読んでください。** とくに、§2 の引用の選びに偏り（不利な文の落とし・有利な文の強調）がないか、段をまたぐ言い方が引用の範囲を越えていないか、新しい計算の定義と計算と読みの決まりに誤りがないかを見てください。',
    '',
    '## 1. 伺いたいこと',
    '',
    '1. **引用の選び（§2）**: 第五部の各段の §0 の全文と比べて、答えの引き方に偏りはないか。足りない文・要らない文はどれか。',
    '2. **段をまたぐ言い方（§0・§3.1・§4・§6）**: 引用の範囲を越えた言い過ぎ・言い足りなさはないか。各段の最終版の言い方と食い違う所はないか。',
    '3. **新しい計算（§3.2・§3.3・第四部）**: 定義（率・分母・閾値・Firth の当てはめ）の当否と、計算の誤り。読みの決まり（札を付けない・対称だったとは読まない・段階 A と V′ を横断しない・機種の安全さの比べにしない）が守られているか。器と別の方法で検算できる所があれば検算してください。',
    '4. **柵（§5）と書き方**: 機種の比べの書き方・両用性の柵・意識などの柵に、抜けや緩みはないか。',
    '5. **段階 C・D・E の要件（§6）**: 総括から出る要件として妥当か。足りないもの・言い過ぎのものはどれか（推奨は求めません）。',
    '6. **枠とのずれ（第三部）**: 草案が枠の構成と書き方の決まりと計算の定義に反している所はないか。',
    '7. **総合**: 公開に向けて直すもの（重さつき）と、記録に置けば足りるものに分けてください。',
    '',
    '## 2. お願い',
    '',
    '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
    '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と節、または公開の置き場のファイル）を付けてください。',
    '- 起草者は、ほとんどの段の器と報告を書いた当人で、段をまたいで筋の通った物語にまとめる側に引かれます。逆に、測れなかった所を増やして小さく見せる側にも引かれます。登録者は、追補と段階の多くで用いた前置き（O と長文招請）の著者・実践者です。どちらも利害の当事者です。',
    '',
    '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。',
    ''])
os.makedirs(RD, exist_ok=True)
REQ = os.path.join(RD, 'request-round1.md')
OUT = os.path.join(RD, 'bundle-round1-all-in-one.md')
IDX = os.path.join(RD, 'bundle-round1-index.md')
for p_ in (REQ, OUT, IDX):
    assert not os.path.exists(p_), p_
open(REQ, 'w', encoding='utf-8', newline=NL).write(req)
parts = ['# 中間総括の検分の束（一巡目・一つの md・公開の置き場のコミット %s の時点）\n\n- 組み立ての器: `summary/make_round1_bundle.py` v0（コーディネータ）。部は五つ。各部の元のファイルの置き場と SHA16 は索引（この束の終わり）に並べる。\n'
         '- JSON と長い記録は五つの逆引用符の囲いで包んだ。中身はバイトのまま（改行は LF）。\n' % head[:7]]
parts.append('## 第一部 依頼文\n\n' + req)
parts.append('## 第二部 草案1 と引用の照らしの記録\n\n' + block(DRAFT, '中間総括の草案1', 'summary/summary-interim-draft1-2026-10-02.md（内部）', 'markdown') + '\n'
             + block(os.path.join(HERE, 'summary-interim-draft1-checks.json'), '引用の照らしの記録', 'summary/summary-interim-draft1-checks.json（内部）', 'json'))
parts.append('## 第三部 枠\n\n' + block(FRAME, '枠（起草と計算と検分の前に書いた）', 'summary/00-frame-interim-summary-2026-10-02.md（内部）', 'markdown'))
parts.append('## 第四部 新しい計算の器と出力\n\n' + block(os.path.join(HERE, 'calc_interim.py'), '計算の器', 'summary/calc_interim.py（内部）', 'python') + '\n'
             + block(os.path.join(HERE, 'calc', 'calc-interim.md'), '計算の出力（表）', 'summary/calc/calc-interim.md（内部）', 'markdown'))
parts.append('## 第五部 九つの段の最終版の §0（全文・器で切り出した）\n\n' + '\n'.join(sec0(rel, label) for label, rel in FIN))
body = '\n\n'.join(parts)
ix = ['# 束の索引（中間総括の検分の一巡目・公開の置き場のコミット %s）' % head[:7], '', '| 何 | 元の置き場 | SHA16 | 字数 |', '|---|---|---|---|']
ix += ['| %s | %s | %s | %d |' % (a, b, c, d) for a, b, c, d in idx]
ix += ['', '本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
full = body + '\n\n' + '\n'.join(ix)
open(OUT, 'w', encoding='utf-8', newline=NL).write(full)
open(IDX, 'w', encoding='utf-8', newline=NL).write('\n'.join(ix))
print('依頼文', s16b(req.encode('utf-8')), len(req), '字 | 束', s16b(full.encode('utf-8')), len(full), '字', len(full.encode('utf-8')), 'バイト | 索引', len(idx), '項 | コミット', head[:7])
