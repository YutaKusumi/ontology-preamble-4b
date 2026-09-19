# -*- coding: utf-8 -*-
"""bundle_B_final.py v2 —— 段階 B **最後の系統外への検分**の依頼文と束を機械で作る（裁定 D131・2026-09-19）。

裁定 D131: 設計を直して草案12B を起こし、走行器と抽出器の本体を書き、小さな模型で端から端まで通してから、
**もう一度系統の外へ出す。そしてその巡を最後にする**（検分のループを避けるため）。

依頼文は**開示の欄を先頭に置く**（正本 `disclosure`・裁定 D117）。v2 では、開示の五項目の中身を**正本 `disclosure.items` から読む**
（草案12B も同じ出所から束縛する・前は依頼文の器の中に起草者が書き、草案には規則しか無かった）。項目が一つでも欠ければ止まる。
**束の前の点検（2026-09-19）**で、採否表で「採用」とした直しの多くが現物の器に入っていなかったことが分かった。
その監査の記録（直す前・直した後）と、点検で見つけた穴の記録を束に入れ、依頼文の「不利なこと」の節に先に書く。
束は貼り付けて読める形に分け、各部の冒頭に入力の SHA16 を置く。器材のソースは**逐語**で入れる（手で写さない）。
状態の数（監査・経路・変異・端から端まで・凍結の器の止まり方）は、**記録と器の出力から機械で読む**（手で打たない）。
用法: python tools/bundle_B_final.py [--outdir records/reviews/B/final-round] [--force]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse, datetime, subprocess, tempfile, shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda *p: hashlib.sha256(open(os.path.join(REPO, *p), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
VERSION = 'v2'

ap = argparse.ArgumentParser()
ap.add_argument('--outdir', default=os.path.join(REPO, 'records', 'reviews', 'B', 'final-round'))
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
if os.path.exists(os.path.join(a.outdir, 'final-request-B.md')) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % a.outdir)
os.makedirs(a.outdir, exist_ok=True)

T = json.loads(rd('design', 'contrasts-B.json'))
TOOLS = ['rules_B.py', 'runs_B.py', 'gate_B.py', 'analyze_B.py', 'layers_B.py', 'integrity_B.py', 'sample_inspection_B.py', 'direction_B.py',
         'steer_B.py', 'run_stageB_local.py', 'control_chart_B.py', 'synth_B.py', 'dry_run_B.py', 'mutation_B.py', 'endtoend_B.py',
         'build_report_B.py', 'freeze_B.py', 'make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py']


def latest(prefix, ext='.md'):
    """records/B/ の中で、いちばん新しい日付の記録を**機械で選ぶ**（日付が変わっても古い名前を引かない）。"""
    fs = sorted(f for f in os.listdir(os.path.join(REPO, 'records', 'B')) if f.startswith(prefix) and f.endswith(ext))
    assert fs, '記録が無い: %s' % prefix
    return 'records/B/' + fs[-1]


ER = 'records/reviews/B/external-round/'
DOCS = {'draft': 'design/design-stageB-draft12.md', 'canon': 'design/contrasts-B.json',
        'facts': 'records/B/design-facts-B.md', 'record': 'records/B/tooling-record-B-2026-09-18.md',
        'sweep': 'records/B/prebundle-sweep-2026-09-19.md',
        'dry': latest('dry-run-B-'), 'mutation': latest('mutation-B-'), 'endtoend': latest('endtoend-B-'),
        'template': 'records/B/results-report-template-B.md',
        'audit_prereg': ER + 'preregistration-fix-audit-B-external.md',
        'audit_before': ER + 'verification-fixes-B-external-before.md', 'audit_after': ER + 'verification-fixes-B-external-after.md'}
PREV = {'adoption': ER + 'adoption-table-B-external.md', 'rulings': ER + 'rulings-D117-D131.md',
        'verification': ER + 'verification-B-external.md', 'design_q': ER + 'design-questions-D118-D129.md'}
for k, v in list(DOCS.items()) + list(PREV.items()):
    assert os.path.exists(os.path.join(REPO, *v.split('/'))), ('束に入れる記録が無い', k, v)

# ---- 開示（正本 disclosure.items・裁定 D117・欠ければ止まる） ----
FIELDS = T['disclosure']['fields']
DISCLOSURE = T['disclosure'].get('items') or {}
missing = [f for f in FIELDS if not DISCLOSURE.get(f)]
assert not missing, ('開示の項目が欠けている（正本 disclosure.items・裁定 D117）', missing)

# ---- 状態の数（記録と器の出力から機械で読む） ----
V = json.loads(rd(*(PREV['verification'].replace('.md', '.json')).split('/')))
MU = json.loads(rd(*DOCS['mutation'].replace('.md', '.json').split('/')))
E2E = json.loads(rd(*DOCS['endtoend'].replace('.md', '.json').split('/')))
AB = json.loads(rd(*DOCS['audit_before'].replace('.md', '.json').split('/')))
AA = json.loads(rd(*DOCS['audit_after'].replace('.md', '.json').split('/')))
NG = '直っていない'
ab_ng = [r for r in AB['rows'] if r['status'] == NG]
ab_ng_p = [r for r in ab_ng if r['P'].startswith('P')]
aa_ng = [r for r in AA['rows'] if r['status'] == NG]
aa_wait = [r for r in AA['rows'] if r['status'] == '登録者の裁定待ち']
dry_txt = rd(*DOCS['dry'].split('/'))
m_dry = re.search(r'発火しなかった経路 (\d+) 件', dry_txt)
dry_unfired = int(m_dry.group(1)) if m_dry else None
# 凍結の器を**束の外の置き場**で走らせ、何で止まるかを読む（公開の置き場に記録を残さない）
_fd = tempfile.mkdtemp(prefix='freezeB_')
try:
    subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'freeze_B.py'), '--draft', DOCS['draft'], '--allow-missing', '--force',
                    '--out', os.path.join(_fd, 'F.md')], capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    FR = json.load(open(os.path.join(_fd, 'F.json'), encoding='utf-8')) if os.path.exists(os.path.join(_fd, 'F.json')) else {}
finally:
    shutil.rmtree(_fd, ignore_errors=True)
blockers = FR.get('blockers') or []

L = []
add = L.append
add('# 段階 B の検分の依頼（**系統の外へ・最後の一回**・裁定 D131・%s 日本時間）' % jst.strftime('%Y-%m-%d %H:%M'))
add('')
add('- 依頼者: 南無弥勒如来（コーディネータ・起草者・器材も書いた・Claude Opus 5）／登録者: 楠見優太（この依頼文と資料を登録者が各位に渡します）。')
add('- 検分していただく方: **系統外（Gemini ほか）を二名以上**と、**claude.ai の Claude**。')
add('  claude.ai の票は起草者と同一系列なので、**これまでのエージェントと claude.ai の検分と合わせて一票**として数えます（裁定 D59）。**系統外の票だけが、独立の目です。**')
add('- **これが最後の外の目です。**登録者は検分のループを避けるため、この巡を最後にすると決めています（裁定 D131）。'
    'ここで捕まらなかったものは、**独立の目に検べられないまま凍結されます**。')
add('- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b')
add('- **データはまだ一つもありません。**')
add('')
add('## 0. 開示（先に全部書きます・正本 `disclosure.items`・裁定 D117）')
add('')
add('前の系統外の巡で、私は「発火しなかった経路 零」と書きながら、**走行器と抽出器の本体が無いことを依頼文に一言も書きませんでした**。'
    '四票すべてがそこを最初に挙げました。**同じことをしないために、以下を先に書きます。**この五項目は正本に一度だけ置き、草案12B も同じ出所から組んでいます。')
add('')
for f in FIELDS:
    add('### %s' % f)
    add('')
    for x in DISCLOSURE[f]:
        add('- %s' % x)
    add('')
add('## 1. 前の巡で何があり、何を直したか')
add('')
add('- **前の系統外の巡**（`%s`）: claude.ai 二名・Gemini 二名、**四票とも差し戻し**。'
    '追い問い %d 件のうち %d 件を再現しました（再現しなかった一件は理由と当てた行を記録に残しました）。'
    % (ER, V['total'], V['reproduced']))
add('- 採否表 P337〜P383・登録者裁定 D117〜D131（草案12B の §5-7 に承認の逐語）。')
add('- **設計を四つ変えました**（`%s` に、数で決めた理由があります）:' % PREV['design_q'])
add('  - **S4 の反証**: 「下がらなかった（封印は当たり）」を、検出力で帰無を受け入れる規則から**同等性の規則**に改めました（裁定 D118）。区間は Newcombe。')
add('  - **確証の統制**: 等方のランダム方向は確証の相手のまま保ち、**td を全場面に広げて**「同じだけ動いた」の数の基準を置きました。'
    '共分散から引く統制は、**私の当初案でしたが取り下げました**（誠実に推定できないため・裁定 D123）。')
add('  - **介入の帯**: **主位置（プロンプトの最終トークン）から EOS まで**に狭めました。抽出した場所と加える場所を一致させるためです。'
    'バッチの組み方も初めて登録しました（裁定 D124）。')
add('  - **品質床の多重性**: 補正ではなく、**課題の正答率の下限を引き上げて**解きました（裁定 D129）。')
add('- **走行器と抽出器の本体を書き、小さな模型で端から端まで通しました**（`%s`・%d 件中 落ちた検査 %d 件）。'
    % (DOCS['endtoend'], E2E['total'], E2E['failed']))
add('- **自己検査の検査を足しました**——直す前の誤りを入れ直して、検査が落ちることを確かめます（`%s`・%d 件中 捕まえられなかった変異 %d 件）。'
    % (DOCS['mutation'], MU['total'], MU['missed']))
add('- **束の前の点検と直しの監査**（2026-09-19・`%s`）と、そこから上がった**登録者裁定 D132**（副位置の保存と読み方をいま登録し、各選択肢の対数尤度は在庫へ・草案12B の §5-8）。'
    % DOCS['sweep'])
add('')
add('## 2. 不利なことを先に（起草者の申し送り）')
add('')
add('- **この束を組む直前まで、採否表で「採用」とした直しの多くが、現物の器に入っていませんでした。**'
    '採用した直しを現物の器で一件ずつ当て直す監査（枠は監査の前に登録・`%s`）で、**直す前は %d 件が「直っていない」**でした'
    '（採否表の行 %d 件と、束の前の点検で見つけた穴 %d 件）。その中には、**S4 の同等性の規則（裁定 D118）が正本と草案の文にしか無く、集計器は検出力の規則のままだった**件が含まれます。'
    '整備の記録には「改めた」と書いていました。**前の巡で捕まった型（「採用」と書いたのに現物が変わっていない）を、そのまま繰り返していました。**'
    % (DOCS['audit_prereg'], len(ab_ng), len(ab_ng_p), len(ab_ng) - len(ab_ng_p)))
add('- **「直っていない」の倒れる向きの多くは、起草者の引力と同じ側でした**（封印が当たりやすい・特異性を書きやすい・門が閉じにくい・様式門が黙って効かない）。')
add('- **合成データは通り、本物の出力では違う結果になる型**が、今回もありました（走行器が様式・言及の欄を空で書き、集計器は空を「該当なし」と数えていた——様式門が実データでは一度も掛からない形）。'
    'refuse の規約・封印の語彙・種の単位に続いて、**同じ型の四度目**です。')
add('- **ランダム方向の腕（確証のすべての対比の相手）が、走行器で走らない形でした。**端から端までの検査が無操作と静的方向の二腕しか走らせていなかったので、気づきませんでした。')
add('- **報告の組み立て器は、合成データでも一度も走っていませんでした**（走査器の口は、正本に必要な鍵が無くて通らなかった）。抽出器は主位置の活性そのものを保存していませんでした。合成データによる検査に管理図の経路はありませんでした。')
add('- **私の検査の器にも誤りがありました**: 監査の器は三度、誤った「直っていない」を出しました（直す前に二度は鍵の取り違え、直した後に一度は検査の前提の誤り——いずれも出力を別名で残しました）。'
    '変異の器は、実トークナイザの置き場を渡し忘れると、自己検査が「飛ばした」で通るのを「守りが無い」と誤って記録しました。'
    '端から端までの検査は一度、時間切れで止められたのに、パイプの終了コードで「通った」に見えました（走らせ直して確かめました）。')
add('- 直した後の監査（`%s`）は「直っていない」%d 件・登録者の裁定待ち %d 件です。**ただし、監査の器も、直した器も、私が書きました。**'
    % (DOCS['audit_after'], len(aa_ng), len(aa_wait)))
add('- **「対処した」と書いてあることを対処の証拠にしないでください。「検査が通った」を正しく測った証拠にしないでください。**'
    '変異の一覧も、合成データの壊れ方も、監査の項目も、**私が選んだもの**です。')
add('')
add('## 3. 見ていただきたいこと')
add('')
add('**(a) 設計の四つの変更は正しいか**（S4 の同等性・td の拡張と共分散統制の取り下げ・帯の縮小・品質床の下限）。'
    'とくに、**取り下げた二つの案**（共分散の統制・多重性の補正）を取り下げてよかったか。')
add('**(b) 前の巡の所見は本当に直っているか**——採否表 `%s` の各行を、**現物のソースで**確かめてください。直した後の監査の表（`%s`）も、私の自己申告です。'
    % (PREV['adoption'], DOCS['audit_after']))
add('**(c) 判定の規則の器 `tools/rules_B.py`**——S4 の三分岐（同等性・Newcombe・床の規則・検閲）、td の特異性（**水準は `1 − alpha_upper` で、確証の各族より緩い＝特異性を書ける側に倒れやすい**・正本の登録どおり）、'
    '等質性の注、refuse 門（答えた分母と読めた分母・符号の積）、品質床の api_error の門（選定の段では記録の不在と同じに扱い、門は incomplete）。')
add('**(d) 走行器と抽出器の本体**——**抽出した層と介入する層が同じか**、**ランダム方向の行ごとの割り当て**、**書式外のときの再生成が凍結走行器と同じ手順か**、'
    '**様式・言及・refuse の分類・ループが段階 A の凍結した関数と同じものか**、**種の区切りが再開でずれないか**、**副位置の活性の取り方**（生成と同じ hook を掛けたまま一度だけ順伝播）。')
add('**(e) 裁定 D132 の読み方**（副位置の活性を同じ層の (6b) の方向に射影し、平均の差・標準化した差・AUC を記述で出す・目安を置かない）——循環が無いという私の主張は正しいか、別の読み方のほうが良いか。')
add('**(f) まだ下りていない登録者の裁定**（品質床の課題・同一性選別に Osec-Ncold を足すか・S4 の効き目を絶対値のままにするか）について、凍結の前に決めておくべきことはあるか。')
add('**(g) 私が見落としている型**——Claude 系の検分は何巡重ねても相関した目です。系統外の方にしか見えないものがあるはずです。')
add('')
add('## 4. いまの状態（機械の出力）')
add('')
add('| 何 | 置き場 | SHA16 |')
add('|---|---|---|')
for k, rel in sorted(DOCS.items()):
    add('| %s | `%s` | %s |' % (k, rel, s16(*rel.split('/'))))
for t in TOOLS:
    add('| 器材 | `tools/%s` | %s |' % (t, s16('tools', t)))
add('')
add('- 正本 %s。確証の族 %s 対比。本走行は腕 × 場面で n=%s。規模は転記行 A。' % (T['version'], T['m_total'], T['n_main']))
add('- 合成データによる検査: 発火しなかった経路 %s 件（`%s`）。変異: %d 件中 捕まえられなかった変異 %d 件。端から端まで: %d 件中 落ちた検査 %d 件。'
    % (dry_unfired, DOCS['dry'], MU['total'], MU['missed'], E2E['total'], E2E['failed']))
add('- 直しの監査: 直す前 %d 行のうち「直っていない」%d 件 → 直した後 %d 行のうち「直っていない」%d 件・登録者の裁定待ち %d 件。'
    % (len(AB['rows']), len(ab_ng), len(AA['rows']), len(aa_ng), len(aa_wait)))
add('- 凍結の器は、いま **%d 件で止まります**——%s。いずれもこの段では正しい状態です（凍結時に記帳する値と封印予想は、データを見る前・凍結のときに入れる）。'
    % (len(blockers), '／'.join(b[:60] for b in blockers)))
add('')
add('## 5. 資料の並び')
add('')
add('- `final-request-B.md`（この依頼文）・`bundle-index.md`（索引）')
add('- `part1.md` 設計草案12B（全文）・`part2.md` 正本と転記行・`part3.md` 束の前の点検と直しの監査の記録')
add('- `part4.md`〜 器材のソース（逐語）')
add('- 前の巡の記録（公開の置き場）: `%s`（票・採否表・裁定・再現・設計の問いの検討）' % ER)
add('')
add('## 6. 検分の作法（お願い）')
add('')
add('- 所見ごとに「置き場・行（または節）・何が起きるか・直し方・重さ（重大／中／軽微）」でお願いします。')
add('- **是認（問題なし）も同じ形で書いてください。**見逃しの記録は指摘の記録と同じ値打ちがあります。')
add('- 分母・基底率・出典の行を必ず添えてください。')
add('- 最後に**「この検分が確認していないこと」を一項目以上**書いてください。')
add('- **読了の申告は検査ではありません。**具体的な追い問いで確かめます。')
add('- 判定は **差し戻し／条件つき可／可** のいずれかで、理由を添えてください。')
add('')
add('## 7. 柵')
add('')
add('- 本依頼と資料のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。')
add('- 破局率を上げる操作の再現手順は、資料のいかなる箇所にも書いていません。')
add('')
req = '\n'.join(L)
open(os.path.join(a.outdir, 'final-request-B.md'), 'w', encoding='utf-8', newline='\n').write(req)

# ---- 資料の束 ----
parts = [('part1.md', '設計草案12B（全文・SHA16 %s）' % s16(*DOCS['draft'].split('/')), rd(*DOCS['draft'].split('/'))),
         ('part2.md', '正本（JSON 全文・SHA16 %s）と転記行（SHA16 %s）' % (s16(*DOCS['canon'].split('/')), s16(*DOCS['facts'].split('/'))),
          '```json\n' + json.dumps(T, ensure_ascii=False, indent=1) + '\n```\n\n' + rd(*DOCS['facts'].split('/'))),
         ('part3.md', '束の前の点検と直しの監査の記録（枠・直す前・直した後・点検の記録）',
          '\n\n---\n\n'.join('## `%s`（SHA16 %s）\n\n%s' % (DOCS[k], s16(*DOCS[k].split('/')), rd(*DOCS[k].split('/')))
                             for k in ('audit_prereg', 'audit_before', 'audit_after', 'sweep')))]
cur, size, n = [], 0, 4
for t in TOOLS:
    src = rd('tools', t)
    blk = '\n'.join(['## `tools/%s`（SHA16 %s・%d 行）' % (t, s16('tools', t), src.count('\n')), '', '```python', src.rstrip('\n'), '```', ''])
    if size + len(blk) > 60000 and cur:
        parts.append(('part%d.md' % n, '器材のソース（逐語）', '\n'.join(cur)))
        n += 1
        cur, size = [], 0
    cur.append(blk)
    size += len(blk)
if cur:
    parts.append(('part%d.md' % n, '器材のソース（逐語）', '\n'.join(cur)))
for fn in os.listdir(a.outdir):                          # 前に組んだ束の余りの部を残さない
    if re.fullmatch(r'part\d+\.md', fn) and fn not in {p[0] for p in parts}:
        os.remove(os.path.join(a.outdir, fn))
idx = ['# 段階 B 最後の系統外への検分・資料の束（索引・機械生成・`tools/bundle_B_final.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
       '- 依頼文: `final-request-B.md`（SHA16 %s）' % hashlib.sha256(req.encode('utf-8')).hexdigest()[:16].upper(), '',
       '| 部 | 中身 | 文字数 |', '|---|---|---|']
for fn, title, body in parts:
    open(os.path.join(a.outdir, fn), 'w', encoding='utf-8', newline='\n').write('# %s（機械生成・%s UTC）\n\n' % (title, now.strftime('%Y-%m-%d %H:%M')) + body)
    idx.append('| `%s` | %s | %s |' % (fn, title, format(len(body), ',')))
idx += ['', '公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b', '',
        '本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(a.outdir, 'bundle-index.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(idx))
print('[bundle_B_final] %s' % os.path.relpath(a.outdir, REPO))
print('  依頼文 %s 字・資料 %d 部（%s）' % (format(len(req), ','), len(parts), '・'.join(format(len(b), ',') for _, _, b in parts)))
print('  開示の項目 %d／%d（正本 disclosure.items）・凍結の器の止まり %d 件・監査 直す前 %d → 直した後 %d（直っていない）'
      % (len([f for f in FIELDS if DISCLOSURE.get(f)]), len(FIELDS), len(blockers), len(ab_ng), len(aa_ng)))
