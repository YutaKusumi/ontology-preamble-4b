# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の器の直しの確かめ（登録者裁定 D238・正本 `review_plan.impl_recheck`）の依頼文と束を組む（意見伺いの束の器 `records/reviews/Bl3/opinions-tools/make_bundle_Bl3_opinions_tools.py` の型）。
束の部: 第一部 依頼文／第二部 採否の案と裁定／第三部 二体の票と起草者の再現の記録／第四部 検分の版からの差分／第五部 正本 v8（全文）と設計の事実と凍結の本文との差の記録／
第六部 直した器の全文（走らせる器）／第七部 直した器の全文（集計・報告・封印・凍結・正本の生成器は差分だけ）／第八部 合成データの器と正式の記録と試しの九度目の記録と器の段の記録。
入力は、束の入力がそろったコミット（`--src`・正式の記録を足したコミット）から読む。器と正本は、直しを入れたコミット（`FIXED`）と同じ中身であることを確かめる。
正式の記録は、確かめがすべて期待どおりで、記録の末尾の版の SHA16 の表が束に入れる器と正本と同じことを確かめる。器（.py）と正本（.json）の行の頭に、そのファイルの行番号を付ける。
束が長いときは、ファイルの境で分けた版も作る（中身は一通版と同じ）。`--test` は正式の記録の代わりに試しの九度目の記録を置き、一時の置き場に書く（大きさを測るため・記録にしない）。
用法: python records/reviews/Bl3/fixcheck/make_bundle_fixcheck_Bl3.py --src <コミット> [--test <一時の置き場>]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, argparse, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
NL = chr(10)
REVIEW = '87ce664'                      # 器の実装の検分の版
FIXED = 'a8ac5ad'                       # 直しを入れたコミット（裁定 D236 の直し・正本 v8）
ap = argparse.ArgumentParser()
ap.add_argument('--src', required=True, help='束の入力がそろったコミット（正式の記録を足したコミット）')
ap.add_argument('--test', default=None, help='正式の記録の代わりに試しの九度目の記録を置き、この一時の置き場に書く')
a = ap.parse_args()
SRC = a.src
git = lambda *x: subprocess.run(['git'] + list(x), cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout.strip()
at = lambda c, rel: subprocess.run(['git', 'show', '%s:%s' % (c, rel)], cwd=REPO, capture_output=True, check=True).stdout
rd = lambda rel: at(SRC, rel).decode('utf-8')
s16 = lambda rel: hashlib.sha256(at(SRC, rel).replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
anc = lambda x, y: subprocess.run(['git', 'merge-base', '--is-ancestor', x, y], cwd=REPO).returncode == 0
assert anc(REVIEW, FIXED) and anc(FIXED, SRC), '検分の版 → 直しのコミット → 束の入力のコミットの順になっていない'
T3 = json.loads(rd('design/contrasts-Bl3.json'))
FJ = json.loads(rd('records/Bl3/design-facts-Bl3.json'))
assert T3['version'] == 'draft3-r4-2026-09-25', T3['version']
assert FJ['contrasts_sha16'] == s16('design/contrasts-Bl3.json'), '設計の事実が正本から作られていない'
assert T3['numbering']['rulings_next'] == 'D239'

RUN_TOOLS = ['tools/bl3_core.py', 'tools/bl3_run.py', 'tools/colab/boot_Bl3.py']
POST_TOOLS = ['tools/analyze_Bl3.py', 'tools/sweep_Bl3.py', 'tools/build_report_Bl3.py', 'tools/seal_Bl3.py', 'tools/make_frozen_Bl3.py', 'tools/freeze_Bl3.py', 'tools/make_contrasts_Bl3.py']
CANON = ['design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'records/Bl3/frozen-diff-Bl3.md']
DIFF_FILES = RUN_TOOLS + POST_TOOLS + ['tools/dry_run_Bl3.py'] + CANON
changed = git('diff', '--name-only', REVIEW, SRC, '--', 'tools', 'design', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'records/Bl3/frozen-diff-Bl3.md').split(NL)
assert sorted(changed) == sorted(DIFF_FILES), '検分の版から変わった器と正本が見込みと違う: %s' % sorted(set(changed) ^ set(DIFF_FILES))
for rel in DIFF_FILES:
    assert at(SRC, rel) == at(FIXED, rel), '器か正本が直しのコミットと違う: %s' % rel

if a.test:
    DRY_REC = 'records/Bl3/tools/trials/dry-trial-9-Bl3.md'                   # 大きさを測るための代わり（記録にしない）
else:
    recs = sorted(p for p in git('ls-tree', '-r', '--name-only', SRC, 'records/Bl3/').split(NL) if re.fullmatch(r'records/Bl3/dry-run-Bl3-[0-9-]+\.md', p))
    assert recs, '束の入力のコミットに合成データの正式の記録が無い'
    DRY_REC = recs[-1]
    txt = rd(DRY_REC)
    m = re.search(r'確かめ: (\d+) のうち (\d+) が期待どおり', txt)
    assert m and m.group(1) == m.group(2) and '**期待と違う**' not in txt, '正式の記録に期待と違う確かめがある'
    n_iso = re.search(r'等方の方向の本数: (\d+)（正本 (\d+)）', txt)
    assert n_iso and int(n_iso.group(1)) == T3['nulls']['isotropic']['count'], '正式の記録の等方の本数が正本と違う'
    assert '起動器の三つの相' in txt
    table = dict(re.findall(r'^\| ([^ |]+) \| ([0-9A-F]{16}) \|$', txt, flags=re.M))
    differ = sorted(f for f in DIFF_FILES if f in table and table[f] != s16(f))
    lack = sorted(f for f in DIFF_FILES if f != 'records/Bl3/frozen-diff-Bl3.md' and f not in table)
    assert not differ and not lack, '正式の記録の版の SHA16 の表が束の器と違う: %s／表に無い: %s' % (differ, lack)

PARTS = [
    ('第二部 採否の案と裁定', ['records/reviews/Bl3/impl/adoption-table-impl-Bl3.md', 'records/Bl3/rulings-D236-D237.md', 'records/Bl3/rulings-D238.md']),
    ('第三部 二体の票（逐語）と、起草者の再現の記録と、票を得た経緯', ['records/reviews/Bl3/impl/r1/review.md', 'records/reviews/Bl3/impl/r2/review.md',
                                              'records/reviews/Bl3/impl/checks/verification-impl-r1-Bl3.md', 'records/reviews/Bl3/impl/checks/verification-impl-r2-Bl3.md',
                                              'records/reviews/Bl3/impl/provenance-impl-Bl3.md']),
    ('第四部 検分の版 %s からの差分（git diff）' % REVIEW, ['DIFF:' + f for f in DIFF_FILES]),
    ('第五部 正本 v8（全文）と設計の事実と、凍結の本文と草案3 の差の記録', ['design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'records/Bl3/frozen-diff-Bl3.md']),
    ('第六部 直した器の全文（走らせる器: 核・フックの道と読み取りと本の計算と乙・Colab の起動器）', RUN_TOOLS),
    ('第七部 直した器の全文（集計・掃き出し・報告の組み立て・封印・凍結の本文・凍結の記帳）', POST_TOOLS[:-1]),                  # 正本の生成器は差分だけ（生成した正本は第五部に全文）
    ('第八部 合成データの器と、合成データの正式の記録と、試しの九度目の記録と、器の段の記録', ['tools/dry_run_Bl3.py', DRY_REC] + (['records/Bl3/tools/trials/dry-trial-9-Bl3.md'] if not a.test else []) + ['records/Bl3/tools/tools-log-Bl3.md']),
]
UNCHANGED = ['tools/bl3_directions.py', 'tools/bl3_recompute_rewrite.py', 'tools/make_predictions_form_Bl3.py', 'tools/bl3_facts.py', 'tools/build_draft_Bl3.py', 'tools/report_lint.py']
for f in UNCHANGED:
    assert at(SRC, f) == at(REVIEW, f), '変えていないはずの器が変わっている: %s' % f

REQ = ['# B-lens 層三の器の直しの確かめのお願い（下見の前の凍結の前・登録者裁定 D238）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-25。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （器の実装の検分の版はコミット %s、直した器と正本はコミット %s、束はコミット %s の中身から組みました。`prelim/` と `results/prelim-*` は開かないでください）。' % (REVIEW, FIXED, SRC),
       '- **これは器の直しの確かめの巡です。** 層三の器は、系統内の新しい個体二体（Claude Opus 5.5）の実装の検分を受け、起草者が所見 29 件（R1 7 件・R2 22 件）をすべて検分の版で再現してから、26 の直しを入れました（登録者裁定 D236）。'
       '直しが大きくなったので、登録者は、直した器を系統外の二名と claude.ai の二名に見ていただく巡を一つ足すと決めました（裁定 D238）。**直しを書いたのも、直しを確かめたのも、起草者一人です。** 凍結の後に器や正本を直すと逸脱になるので、凍結の前に外の目で見ていただきたいのです。',
       '- **お願い: 本物の模型で全経路の効き目を計算しないでください。** 予想の封印がまだです（封印は下見の前の凍結の後です）。式や手順の検算と、乱数の模型の上の確かめ（本物の重みを使わないもの）は歓迎します。',
       '- **お願い: 結果の見込み（どの行に札が付くか・門を通るかなど）を書かないでください。** 書かれていたら、封印の前の露出として記録します。',
       '- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）と機種を書いてください。claude.ai の Claude Opus 5.5 は起草者と同じ機種です。',
       '- **束の中身**: 第一部 依頼文／第二部 採否の案と裁定／第三部 二体の票（逐語）と、起草者の再現の記録と、票を得た経緯／第四部 検分の版 %s からの差分（git diff）／第五部 正本 v8（全文）と設計の事実と、凍結の本文と草案3 の差の記録／' % REVIEW +
       '第六部 直した器の全文（走らせる器）／第七部 直した器の全文（集計・掃き出し・報告の組み立て・封印・凍結の本文・凍結の記帳）／第八部 合成データの器と、合成データの正式の記録と、試しの九度目の記録と、器の段の記録。'
       '器（.py）と正本（.json）の行の頭の番号は、そのファイルの行番号です。長いので、ファイルの境で分けた版もあります（中身は一通版と同じ）。',
       '- **束に入れていないもの**: 検分の版から変えていない器（%s・段階 B と B-lens の凍結した関数など）と、枠（草案3）と、再現の器（`records/reviews/Bl3/impl/checks/`）は、公開のコミットで読めます。'
       '正本の生成器 `tools/make_contrasts_Bl3.py` は、差分（第四部）だけを入れました（生成した正本 v8 の全文は第五部にあり、生成器の全文は公開のコミットで読めます）。' % '・'.join('`%s`' % f for f in UNCHANGED),
       '- **既に分かっている点**: 第八部の器の段の記録（§13〜§15 と検分票）と、第二部の採否の案の B の表にあります。同じ点に気づいたら、「記録にある点」と一言添えてください（新しい点と分けて数えます）。', '',
       '## 1. 伺いたいこと', '',
       '1. **直しが所見を閉じたか**: 第二部の採否の案の A の表の直しの一つずつについて、第三部の所見（R1・R2 の札）と第四部の差分を並べて、所見が閉じたか。閉じ方が所見の言う形と違う所（別の形で閉じた・一部だけ閉じた）はないか。',
       '2. **直しが入れた新しい誤り**: 足した照らしと止め（下見の前の凍結・本の凍結・一致だけを見る段と結果を開く段・報告の組み立て・起動器の止め方と持ち出し）に、次の三つの形がないか。とくに、封印と凍結と結果を開く段の結びつき（照らす SHA がどこから来て、いつ照らすか）を見てください。',
       '   - 正しい流れでも止まる（厳しすぎる）',
       '   - 何も捕まえない（照らす相手が同じものから作られている・必ず通る）',
       '   - 止まるべき所で止まらない',
       '3. **器の決め**: 第二部の採否の案の B の表で「変えない」とした器の決めのうち、凍結の前に直すべきものはないか。',
       '4. **合成データの正式の記録**: 第八部の正式の記録の確かめの一つずつが、名のとおりのものを確かめているか。確かめの側が器と同じ誤りを共有していないか、答えの分かる合成が答えを器から借りていないか。',
       '5. **判定**: 最後に、次の三つから一つを選んでください。',
       '   - 「このまま下見の前の凍結の段に進めてよい」',
       '   - 「凍結の前に直すものがある（直した後の確かめは起草者の合成データの記録で足りる）」',
       '   - 「直しが大きく、もう一度外の目が要る」', '',
       '## 2. お願い', '',
       '- 一つの所見ごとに、重さ（重い・中くらい・軽い）と、根拠の置き場（束の部とファイルと行番号、または正本の鍵）と、確かめ方を付けてください。',
       '- 凍結の前に直すべきものと、記録（限界・報告の注）に置けば足りるものを分けてください。',
       '- 問題が無いと見た所も、どこを見てそう判断したかを書いてください（問題なしの判断も記録して、次の確かめに使います）。',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。「全部読んだ」ではなく、どのファイルのどの関数を読んだかで書いてください。',
       '- 起草者（コーディネータ）は器と直しの書き手で、「直した・通った」と読む側に引かれます。登録者は層三の問いを立てた当人です。どちらも利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']


def numbered(text):
    lines = text.rstrip(NL).split(NL)
    w = len(str(len(lines)))
    return NL.join('%*d | %s' % (w, i, l) for i, l in enumerate(lines, 1))


LOCAL = re.compile(r'[A-Za-z]:[\\/]Users[\\/][^\\/`\s]+[\\/]AppData[\\/]Local[\\/]Temp[\\/]claude[\\/][^\\/`\s]+[\\/][0-9a-f-]{36}[\\/]scratchpad')


def sanitize(text):
    """束の写しの中だけ、手元の一時の置き場の道筋を決まった言い方に置き換える（元のファイルは変えない・SHA16 は元のファイルのもの）。置き換えた後に手元の道筋が残れば止める。"""
    out, n = LOCAL.subn('〈手元の一時の置き場〉', text)
    assert not re.search(r'[A-Za-z]:[\\/]Users[\\/]|/c/Users/|AppData', out), '束の写しに手元の道筋が残る'
    return out, n


def diff_of(rel):
    d = subprocess.run(['git', 'diff', '--no-color', '--no-ext-diff', REVIEW, SRC, '--', rel], cwd=REPO, capture_output=True, check=True).stdout.decode('utf-8')
    assert d.strip(), rel
    return d


items, idx = [], ['# 束の索引（B-lens 層三の器の直しの確かめ・下見の前の凍結の前・登録者裁定 D238）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|', '| 第一部 依頼文 | 依頼文 | — |']
items.append(('第一部 依頼文', 'REQ', NL.join(['', '=' * 20 + ' 第一部 依頼文 ' + '=' * 20, ''] + REQ)))
for title, files in PARTS:
    for k, rel in enumerate(files):
        head = ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, ''] if k == 0 else ['']
        if rel.startswith('DIFF:'):
            f = rel[5:]
            body = diff_of(f)
            body, n = sanitize(body)
            assert n == 0, f
            block = ['<<< 始: `%s` の差分（%s → %s・git diff・囲みは四つの backtick） >>>' % (f, REVIEW, SRC), '````diff', body.rstrip(NL), '````', '<<< 終: `%s` の差分 >>>' % f]
            items.append((title, rel, NL.join(head + block)))
            idx.append('| %s | `%s` の差分 | — |' % (title, f))
            continue
        body, n = sanitize(rd(rel))
        note = '・束の写しでは手元の一時の置き場の道筋 %d か所を〈手元の一時の置き場〉に置き換えた（元のファイルは変えていない・SHA16 は元のファイルのもの）' % n if n else ''
        if rel.endswith(('.py', '.json')):
            assert n == 0, rel
            block = ['<<< 始: `%s`（SHA16 %s・行の頭の番号はこのファイルの行番号） >>>' % (rel, s16(rel)), '```', numbered(body), '```', '<<< 終: `%s` >>>' % rel]
        else:
            block = ['<<< 始: `%s`（SHA16 %s%s） >>>' % (rel, s16(rel), note), body.rstrip(NL), '<<< 終: `%s` >>>' % rel]
        items.append((title, rel, NL.join(head + block)))
        idx.append('| %s | `%s` | %s |' % (title, rel, s16(rel)))
text = NL.join(b for _, _, b in items) + NL
OUT = os.path.abspath(a.test) if a.test else HERE
os.makedirs(OUT, exist_ok=True)
for fn in ('request-fixcheck-Bl3.md', 'bundle-fixcheck-Bl3-all-in-one.md', 'bundle-index.md'):
    assert a.test or not os.path.exists(os.path.join(OUT, fn)), '既にある: ' + fn                  # 記録は一度だけ書く
open(os.path.join(OUT, 'request-fixcheck-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
bp = os.path.join(OUT, 'bundle-fixcheck-Bl3-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(bp, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-fixcheck-Bl3-all-in-one.md`: %d 字・SHA16 %s（入力のコミット %s・直した器と正本のコミット %s・検分の版 %s）。' % (len(text), h, SRC, FIXED, REVIEW)]
LIMIT = 110000                                             # 一度に貼る長さの目安（字）。これを超えるときはファイルの境で分けた版も作る
groups = [items]
if len(text) > LIMIT:
    groups, cur = [], []
    for it in items:
        if cur and sum(len(x[2]) for x in cur) + len(it[2]) > LIMIT:
            groups.append(cur)
            cur = []
        cur.append(it)
    groups.append(cur)
    for k, g in enumerate(groups, 1):
        head_line = '（B-lens 層三の器の直しの確かめの束・分けた版 %d／%d・中身は一通版と同じ）' % (k, len(groups))
        body = head_line + NL + NL.join(b for _, _, b in g) + NL
        fp = os.path.join(OUT, 'bundle-fixcheck-Bl3-part%d.md' % k)
        assert a.test or not os.path.exists(fp), '既にある: ' + fp
        open(fp, 'w', encoding='utf-8', newline=NL).write(body)
        idx.append('- 分けた版 %d／%d `bundle-fixcheck-Bl3-part%d.md`: %s・%d 字・SHA16 %s。' % (
            k, len(groups), k, '・'.join(('依頼文' if rel == 'REQ' else (rel[5:] + ' の差分') if rel.startswith('DIFF:') else rel) for _, rel, _ in g), len(body),
            hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper()[:16]))
idx += ['- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(OUT, 'bundle-index.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
pushed = all(anc(c, 'origin/main') for c in (REVIEW, FIXED, SRC))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字 | items', len(items), '| parts', len(groups), '| 正式の記録', DRY_REC,
      '| 公開済み' if pushed else '| まだ公開していないコミットがある（渡す前に push する）')
