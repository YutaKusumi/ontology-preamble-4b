# -*- coding: utf-8 -*-
"""bundle_B_final.py v3 —— 段階 B **最後の系統外への検分**の依頼文と束を機械で作る（裁定 D131・2026-09-19）。

裁定 D131: 設計を直して草案12B を起こし、走行器と抽出器の本体を書き、小さな模型で端から端まで通してから、
**もう一度系統の外へ出す。そしてその巡を最後にする**（検分のループを避けるため）。

依頼文は**開示の欄を先頭に置く**（正本 `disclosure`・裁定 D117）。開示の五項目の中身は**正本 `disclosure.items` から読む**
（草案12B も同じ出所から束縛する）。項目が一つでも欠ければ止まる。
v3（2026-09-19）での変更:
- **束に、依頼文が頼む検分に要る記録をすべて入れる**（v2 までは前の巡の採否表・裁定の文・設計の問いの検討が束に無く、
  問い (a)(b) を束だけでは検べられなかった）。**採否表の引用の照合の記録**も入れる。
- 部を**必読**と**参照**に分け、索引と依頼文に「どの問いに要るか」を印字する（束の全体は前の巡の二倍を超え、文脈に一度に入らない方がいる）。
- 器材の一覧を `tools/` の現物と突き合わせ、**束に入れない器を名指しで決める**（黙って漏らさない）。
- 状態の数（前の巡の票の数・再現・監査・経路・変異・端から端まで・引用の照合・凍結の器の止まり方）は、**記録と器の出力から機械で読む**（手で打たない）。
束は貼り付けて読める形に分け、各部の冒頭に入力の SHA16 を置く。器材のソースは**逐語**で入れる（手で写さない）。
用法: python tools/bundle_B_final.py [--outdir records/reviews/B/final-round] [--force]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, glob, json, hashlib, argparse, datetime, subprocess, tempfile, shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda *p: hashlib.sha256(open(os.path.join(REPO, *p), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
VERSION = 'v3'
PART_MAX = 60000     # 一つの部の字数の上限の目安（貼り付けて読めるように・数の結果は変えない）

ap = argparse.ArgumentParser()
ap.add_argument('--outdir', default=os.path.join(REPO, 'records', 'reviews', 'B', 'final-round'))
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
if os.path.exists(os.path.join(a.outdir, 'final-request-B.md')) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % a.outdir)
os.makedirs(a.outdir, exist_ok=True)

T = json.loads(rd('design', 'contrasts-B.json'))

# ---- 器材: 必読（問い (b)〜(e) の中心）と参照。現物の一覧と突き合わせる ----
CORE_TOOLS = ['rules_B.py', 'analyze_B.py', 'gate_B.py', 'layers_B.py', 'runs_B.py', 'steer_B.py', 'run_stageB_local.py', 'direction_B.py']
REF_TOOLS = ['integrity_B.py', 'sample_inspection_B.py', 'control_chart_B.py', 'freeze_B.py', 'build_report_B.py', 'citations_B.py',
             'synth_B.py', 'dry_run_B.py', 'mutation_B.py', 'endtoend_B.py', 'make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py']
NOT_IN_BUNDLE = {'bundle_B_final.py': 'この依頼文と束を組む器そのもの（実験の器材ではない）'}
TOOLS = CORE_TOOLS + REF_TOOLS
_have = {os.path.basename(f) for f in glob.glob(os.path.join(REPO, 'tools', '*_B.py'))} | {'build_draftB.py'}
_left = sorted(_have - set(TOOLS) - set(NOT_IN_BUNDLE))
assert not _left, ('束の一覧にも除外の一覧にも無い器がある（黙って漏らさない）', _left)
assert len(set(TOOLS)) == len(TOOLS)


def latest(prefix, ext='.md'):
    """records/B/ の中で、日付だけを名に持つ記録の**いちばん新しいもの**を機械で選ぶ（別名で残した記録を拾わない）。"""
    pat = re.compile(r'^%s\d{4}-\d{2}-\d{2}%s$' % (re.escape(prefix), re.escape(ext)))
    fs = sorted(f for f in os.listdir(os.path.join(REPO, 'records', 'B')) if pat.match(f))
    assert fs, '記録が無い: %s' % prefix
    return 'records/B/' + fs[-1]


ER = 'records/reviews/B/external-round/'
DOCS = {'draft': 'design/design-stageB-draft12.md', 'canon': 'design/contrasts-B.json',
        'facts': 'records/B/design-facts-B.md', 'record': 'records/B/tooling-record-B-2026-09-18.md',
        'sweep': 'records/B/prebundle-sweep-2026-09-19.md', 'citation': 'records/B/citation-check-2026-09-19.md',
        'dry': latest('dry-run-B-'), 'mutation': latest('mutation-B-'), 'endtoend': latest('endtoend-B-'),
        'mutation_run1': 'records/B/mutation-B-2026-09-19-run1-conflated-selftest.md',
        'template': 'records/B/results-report-template-B.md',
        'audit_prereg': ER + 'preregistration-fix-audit-B-external.md',
        'audit_before': ER + 'verification-fixes-B-external-before.md', 'audit_after': ER + 'verification-fixes-B-external-after.md'}
PREV = {'adoption': ER + 'adoption-table-B-external.md', 'rulings': ER + 'rulings-D117-D131.md',
        'verification': ER + 'verification-B-external.md', 'design_q': ER + 'design-questions-D118-D129.md',
        'provenance': ER + 'provenance.md'}
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
MU1 = json.loads(rd(*DOCS['mutation_run1'].replace('.md', '.json').split('/')))
E2E = json.loads(rd(*DOCS['endtoend'].replace('.md', '.json').split('/')))
AB = json.loads(rd(*DOCS['audit_before'].replace('.md', '.json').split('/')))
AA = json.loads(rd(*DOCS['audit_after'].replace('.md', '.json').split('/')))
CIT = json.loads(rd(*DOCS['citation'].replace('.md', '.json').split('/')))
NG = '直っていない'
ab_ng = [r for r in AB['rows'] if r['status'] == NG]
ab_ng_p = [r for r in ab_ng if r['P'].startswith('P')]
aa_ng = [r for r in AA['rows'] if r['status'] == NG]
aa_wait = [r for r in AA['rows'] if r['status'] == '登録者の裁定待ち']
dry_txt = rd(*DOCS['dry'].split('/'))
m_dry = re.search(r'発火しなかった経路 (\d+) 件', dry_txt)
dry_unfired = int(m_dry.group(1)) if m_dry else None
# 前の巡の票（出所の記録の表から数える）
_prov = [l for l in rd(*PREV['provenance'].split('/')).split('\n') if re.match(r'^\| `[\w-]+/review\.md` \|', l)]
n_votes = len(_prov)
n_ext = sum('**系統外**' in l for l in _prov)
n_int = sum('系統内' in l for l in _prov)
n_back = sum('**差し戻し**' in l for l in _prov)
assert n_votes and n_ext + n_int == n_votes, ('出所の記録の表が読めない', n_votes, n_ext, n_int)
# 引用の照合（いまの器で、いまの正本・文書・器材に当てる）
import citations_B
CV, CT = citations_B.check_all(REPO)
cit_items = len(CIT['items'])
cit_occ = sum(e['count'] for e in CIT['items'])
cit_lab = sum('出所の札' in e['kind'] for e in CIT['items'])
cit_lab_up = sum(1 for e in CIT['items'] if '出所の札' in e['kind'] and '系統外の検分' in e['old'] and '系統内の検分' in e['new'])
# 凍結の器を**束の外の置き場**で走らせ、何で止まるかを読む（公開の置き場に記録を残さない）
_fd = tempfile.mkdtemp(prefix='freezeB_')
try:
    subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'freeze_B.py'), '--draft', DOCS['draft'], '--allow-missing', '--force',
                    '--out', os.path.join(_fd, 'F.md')], capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    FR = json.load(open(os.path.join(_fd, 'F.json'), encoding='utf-8')) if os.path.exists(os.path.join(_fd, 'F.json')) else {}
finally:
    shutil.rmtree(_fd, ignore_errors=True)
assert FR, '凍結の器の記録が読めない（器が落ちた）'
blockers = FR.get('blockers') or []
TW = T['descriptive_families']['B_desc_S4']['three_way']

# ---- 資料の部（必読・参照）: (名, 中身, 必読か, 関わる問い, 本文) ----
def doc_block(key, table):
    rel = table[key]
    return '## `%s`（SHA16 %s）\n\n%s' % (rel, s16(*rel.split('/')), rd(*rel.split('/')))


parts = [('設計草案12B（全文・SHA16 %s）' % s16(*DOCS['draft'].split('/')), True, '(a)(c)(e)(f)(g)', rd(*DOCS['draft'].split('/'))),
         ('正本（JSON 全文・SHA16 %s）と転記行（SHA16 %s）' % (s16(*DOCS['canon'].split('/')), s16(*DOCS['facts'].split('/'))), True, '(a)〜(g)',
          '```json\n' + json.dumps(T, ensure_ascii=False, indent=1) + '\n```\n\n' + rd(*DOCS['facts'].split('/'))),
         ('前の巡の採否表・登録者裁定の文・設計の問いの検討／直しの監査（枠・直した後）／採否表の引用の照合の記録', True, '(a)(b)(g)',
          '\n\n---\n\n'.join([doc_block(k, PREV) for k in ('adoption', 'rulings', 'design_q')] +
                             [doc_block(k, DOCS) for k in ('audit_prereg', 'audit_after', 'citation')]))]


def pack(names, title, must, qs):
    """器材のソースを逐語で部に詰める（部の字数の上限の目安を超えたら次の部へ）。"""
    out, cur, size = [], [], 0
    for t in names:
        src = rd('tools', t)
        blk = '\n'.join(['## `tools/%s`（SHA16 %s・%d 行）' % (t, s16('tools', t), src.count('\n')), '', '```python', src.rstrip('\n'), '```', ''])
        if size + len(blk) > PART_MAX and cur:
            out.append((title, must, qs, '\n'.join(cur)))
            cur, size = [], 0
        cur.append(blk)
        size += len(blk)
    if cur:
        out.append((title, must, qs, '\n'.join(cur)))
    return out


parts += pack(CORE_TOOLS, '器材のソース（逐語・核）', True, '(b)(c)(d)(e)')
REF_DOCS = [('audit_before', DOCS), ('sweep', DOCS), ('verification', PREV), ('template', DOCS), ('record', DOCS),
            ('dry', DOCS), ('mutation', DOCS), ('mutation_run1', DOCS), ('endtoend', DOCS)]
_cur, _size = [], 0
for k, tb in REF_DOCS:
    blk = doc_block(k, tb)
    if _size + len(blk) > PART_MAX and _cur:
        parts.append(('参照の記録（直す前の監査・点検・前の巡の再現・報告の雛形・整備・合成データ・変異・端から端まで）', False, '(b)(g)', '\n\n---\n\n'.join(_cur)))
        _cur, _size = [], 0
    _cur.append(blk)
    _size += len(blk)
if _cur:
    parts.append(('参照の記録（直す前の監査・点検・前の巡の再現・報告の雛形・整備・合成データ・変異・端から端まで）', False, '(b)(g)', '\n\n---\n\n'.join(_cur)))
parts += pack(REF_TOOLS, '器材のソース（逐語・参照）', False, '(b)(g)')
parts = [('part%d.md' % (i + 1),) + p for i, p in enumerate(parts)]
n_must = sum(1 for p in parts if p[2])
chars_must = sum(len(p[4]) for p in parts if p[2])
chars_all = sum(len(p[4]) for p in parts)

# ---- 依頼文 ----
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
add('- **段階 B のデータはまだ一つもありません**（段階 A の結果は公開済みです）。')
add('- **資料は %d 部あり、うち必読が %d 部です**（全体 %s 字・必読 %s 字）。文脈に一度に入らないときは必読の部を先に読み、**読んだ部を票の冒頭に書いてください**（§5・§6）。'
    % (len(parts), n_must, format(chars_all, ','), format(chars_must, ',')))
add('')
add('## 0. 開示（先に全部書きます・正本 `disclosure.items`・裁定 D117）')
add('')
add('前の系統外の巡で、私は「発火しなかった経路 零」と書きながら、**走行器と抽出器の本体が無いことを依頼文に一言も書きませんでした**。'
    '%d 票すべてがそこを最初に挙げました。**同じことをしないために、以下を先に書きます。**この五項目は正本に一度だけ置き、草案12B も同じ出所から組んでいます。' % n_votes)
add('')
for f in FIELDS:
    add('### %s' % f)
    add('')
    for x in DISCLOSURE[f]:
        add('- %s' % x)
    add('')
add('## 1. 前の巡で何があり、何を直したか')
add('')
add('- **前の系統外の巡**（`%s`）: 系統外 %d 名・系統内（claude.ai）%d 名、**%d 票のうち差し戻し %d 票**。'
    '追い問い %d 件のうち %d 件を再現しました（再現しなかった %d 件は理由と当てた行を記録に残しました）。'
    % (ER, n_ext, n_int, n_votes, n_back, V['total'], V['reproduced'], V['total'] - V['reproduced']))
add('- 採否表 P337〜P383・登録者裁定 D117〜D131（草案12B の §5-7 に承認の逐語）。**採否表・裁定の文・設計の問いの検討は、束の必読の部に入れました。**')
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
add('- **採否表の引用の照合**（2026-09-19・`%s`）と、照合の器 `tools/citations_B.py`。' % DOCS['citation'])
add('')
add('## 2. 不利なことを先に（起草者の申し送り）')
add('')
add('- **この束を組む直前まで、採否表で「採用」とした直しの多くが、現物の器に入っていませんでした。**'
    '採用した直しを現物の器で一件ずつ当て直す監査（枠は監査の前に登録・`%s`）で、**直す前は %d 件が「直っていない」**でした'
    '（採否表の行 %d 件と、束の前の点検で見つけた穴 %d 件）。その中には、**S4 の同等性の規則（裁定 D118）が正本と草案の文にしか無く、集計器は検出力の規則のままだった**件が含まれます。'
    '整備の記録には「改めた」と書いていました。**前の巡で捕まった型（「採用」と書いたのに現物が変わっていない）を、そのまま繰り返していました。**'
    % (DOCS['audit_prereg'], len(ab_ng), len(ab_ng_p), len(ab_ng) - len(ab_ng_p)))
add('- **「直っていない」の倒れる向きの多くは、起草者の引力と同じ側でした**（封印が当たりやすい・特異性を書きやすい・門が閉じにくい・様式門が黙って効かない）。')
add('- **正本と器材の注に手で打った採否表の番号が、別の行を指していました**（依頼文を書く途中で気づいた・**事後の点検**・`%s`）。'
    '直した項 %d（出現 %d 箇所）。うち**出所の札の誤り %d 項**——系統内（claude.ai）だけが挙げた所見に「系統外の検分」の札を付けたものが %d 項あり、**独立の票の記録を水増しする向き**でした。'
    '足した照合の器は、直す前の版に当てると **%d 項のうち %d 項しか捕まえません**（裁定の番号も出所の札も添えていない引用は照らせない）。**残りは私が読んで直したもので、直した先の行の選び方も私の判断です。**'
    % (DOCS['citation'], cit_items, cit_occ, cit_lab, cit_lab_up, cit_items, CIT['caught_by_checker_before']))
add('- **照合の器の自己検査にも欠けがありました**——一つの試験の文に二つの食い違いを混ぜていたので、片方の照合を外しても他方で落ち、守りを試せていませんでした。'
    '変異の器が捕まえ（一回目 %d 件中 %d 件を捕まえられなかった・出力は `%s`）、直しました。'
    % (MU1['total'], MU1['missed'], DOCS['mutation_run1']))
add('- **合成データは通り、本物の出力では違う結果になる型**が、今回もありました（走行器が様式・言及の欄を空で書き、集計器は空を「該当なし」と数えていた——様式門が実データでは一度も掛からない形）。'
    'refuse の規約・封印の語彙・種の単位に続いて、**同じ型の四度目**です。')
add('- **ランダム方向の腕（確証のすべての対比の相手）が、走行器で走らない形でした。**端から端までの検査が無操作と静的方向の二腕しか走らせていなかったので、気づきませんでした。')
add('- **報告の組み立て器は、合成データでも一度も走っていませんでした**（走査器の口は、正本に必要な鍵が無くて通らなかった）。抽出器は主位置の活性そのものを保存していませんでした。合成データによる検査に管理図の経路はありませんでした。')
add('- **私の検査の器にも誤りがありました**: 監査の器は三度、誤った「直っていない」を出しました（直す前に二度は鍵の取り違え、直した後に一度は検査の前提の誤り——いずれも出力を別名で残しました）。'
    '変異の器は、実トークナイザの置き場を渡し忘れると、自己検査が「飛ばした」で通るのを「守りが無い」と誤って記録しました。'
    '端から端までの検査は一度、時間切れで止められたのに、パイプの終了コードで「通った」に見えました（走らせ直して確かめました）。')
add('- 直した後の監査（`%s`）は「直っていない」%d 件・登録者の裁定待ち %d 件です。**この監査は、採否表の引用を直す前の正本で走らせたものです**（監査が見た器の振る舞いは、引用の直しで変わっていません）。'
    '**ただし、監査の器も、直した器も、照合の器も、私が書きました。**'
    % (DOCS['audit_after'], len(aa_ng), len(aa_wait)))
add('- **「対処した」と書いてあることを対処の証拠にしないでください。「検査が通った」を正しく測った証拠にしないでください。**'
    '変異の一覧も、合成データの壊れ方も、監査の項目も、直した先の採否表の行も、**私が選んだもの**です。')
add('')
add('## 3. 見ていただきたいこと')
add('')
add('**(a) 設計の四つの変更は正しいか**（S4 の同等性・td の拡張と共分散統制の取り下げ・帯の縮小・品質床の下限）。'
    'とくに、**取り下げた二つの案**（共分散の統制・多重性の補正）を取り下げてよかったか。')
add('**(b) 前の巡の所見は本当に直っているか**——採否表 `%s` の各行を、**現物のソースで**確かめてください。直した後の監査の表（`%s`）も、採否表の引用の照合の記録（`%s`）も、私の自己申告です。'
    '**正本と器材の注が引く「採否表 P…」が、その行の所見を指しているか**も、見ていただけると助かります（照合の器は中身を見ません）。'
    % (PREV['adoption'], DOCS['audit_after'], DOCS['citation']))
add('**(c) 判定の規則の器 `tools/rules_B.py`**——S4 の三分岐（同等性・Newcombe・床の規則・検閲）、td の特異性（**水準は `1 − alpha_upper` で、確証の各族より緩い＝特異性を書ける側に倒れやすい**・正本の登録どおり）、'
    '等質性の注、refuse 門（答えた分母と読めた分母・符号の積）、品質床の api_error の門（選定の段では記録の不在と同じに扱い、門は incomplete）。')
add('**(d) 走行器と抽出器の本体**——**抽出した層と介入する層が同じか**、**ランダム方向の行ごとの割り当て**、**書式外のときの再生成が凍結走行器と同じ手順か**、'
    '**様式・言及・refuse の分類・ループが段階 A の凍結した関数と同じものか**、**種の区切りが再開でずれないか**、**副位置の活性の取り方**（生成と同じ hook を掛けたまま一度だけ順伝播）。')
add('**(e) 裁定 D132 の読み方**（副位置の活性を同じ層の (6b) の方向に射影し、平均の差・標準化した差・AUC を記述で出す・目安を置かない）——循環が無いという私の主張は正しいか、別の読み方のほうが良いか。')
add('**(f) まだ下りていない登録者の裁定**——凍結の前に決めておくべきことはあるか、決め方に偏りは無いか（草案 §5-補 に列挙）:')
add('  - 品質床の課題の選定（裁定 D66）と、無操作の実測の正答率を見てからの下限の凍結（正本 `quality_floor.base_min`・いまの登録値 %s・草案 §2.5）。' % T['quality_floor']['base_min'])
add('  - 同一性選別の比較に Osec-Ncold を足すか、七腕である旨を印字するか（正本 `identity_screen.b_panel_arms_compared`）。')
add('  - S4 の効き目をいまの絶対値（%s pt）のまま置くか、相対で置き直すか（正本 `descriptive_families.B_desc_S4.three_way.effect_pt_caveat`）。' % TW['effect_pt'])
add('**(g) 私が見落としている型**——Claude 系の検分は何巡重ねても相関した目です。系統外の方にしか見えないものがあるはずです。')
add('')
add('## 4. いまの状態（機械の出力）')
add('')
add('| 何 | 置き場 | SHA16 |')
add('|---|---|---|')
for k, rel in sorted(list(DOCS.items()) + list(PREV.items())):
    add('| %s | `%s` | %s |' % (k, rel, s16(*rel.split('/'))))
for t in TOOLS:
    add('| 器材 | `tools/%s` | %s |' % (t, s16('tools', t)))
add('')
add('- 正本 %s。確証の族 %s 対比。本走行は腕 × 場面で n=%s。規模は転記行 A。' % (T['version'], T['m_total'], T['n_main']))
add('- 合成データによる検査: 発火しなかった経路 %s 件（`%s`）。変異: %d 件中 捕まえられなかった変異 %d 件。端から端まで: %d 件中 落ちた検査 %d 件。'
    % (dry_unfired, DOCS['dry'], MU['total'], MU['missed'], E2E['total'], E2E['failed']))
add('- 直しの監査: 直す前 %d 行のうち「直っていない」%d 件 → 直した後 %d 行のうち「直っていない」%d 件・登録者の裁定待ち %d 件。'
    % (len(AB['rows']), len(ab_ng), len(AA['rows']), len(aa_ng), len(aa_wait)))
add('- 採否表の引用の照合（いまの器で、いまの正本・草案・雛形・器材に当てた）: 引用 %d・裁定の照合 %d・出所の札の照合 %d・**違反 %d**。'
    % (CT['cit'], CT['d'], CT['label'], len(CV)))
add('- 凍結の器は、いま **%d 件で止まります**——%s。いずれもこの段では正しい状態です（凍結時に記帳する値と封印予想は、データを見る前・凍結のときに入れる）。'
    % (len(blockers), '／'.join(b if len(b) <= 80 else b[:80] + '…' for b in blockers)))
add('- 束に入れない器: %s。' % '・'.join('`tools/%s`（%s）' % (k, v) for k, v in NOT_IN_BUNDLE.items()))
add('')
add('## 5. 資料の並び')
add('')
add('- `final-request-B.md`（この依頼文）・`bundle-index.md`（索引）')
add('')
add('| 部 | 中身 | 必読か | 関わる問い | 字数 |')
add('|---|---|---|---|---|')
for fn, title, must, qs, body in parts:
    add('| `%s` | %s | %s | %s | %s |' % (fn, title, '**必読**' if must else '参照', qs, format(len(body), ',')))
add('')
add('- 前の巡の票（逐語）と出所の記録は、公開の置き場の `%s` にあります（束には入れていません）。' % ER)
add('')
add('## 6. 検分の作法（お願い）')
add('')
add('- **読んだ部を、票の冒頭に書いてください。**文脈に入り切らないときは必読の部を先に読み、**読まなかった部については、是認も差し戻しも書かないでください。**')
add('- 所見ごとに「置き場・行（または節）・何が起きるか・直し方・重さ（重大／中／軽微）」でお願いします。')
add('- **是認（問題なし）も同じ形で書いてください。**見逃しの記録は指摘の記録と同じ値打ちがあります。')
add('- 分母・基底率・出典の行を必ず添えてください。')
add('- 最後に**「この検分が確認していないこと」を一項目以上**書いてください。')
add('- **読了の申告は検査ではありません。**具体的な追い問いで確かめます。')
add('- 公開の置き場の `prelim/` と `results/prelim-*`（登録外の下見）は開かないでください。')
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
for fn in os.listdir(a.outdir):                          # 前に組んだ束の余りの部を残さない
    if re.fullmatch(r'part\d+\.md', fn) and fn not in {p[0] for p in parts}:
        os.remove(os.path.join(a.outdir, fn))
idx = ['# 段階 B 最後の系統外への検分・資料の束（索引・機械生成・`tools/bundle_B_final.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
       '- 依頼文: `final-request-B.md`（SHA16 %s）' % hashlib.sha256(req.encode('utf-8')).hexdigest()[:16].upper(),
       '- 部 %d（必読 %d）・全体 %s 字・必読 %s 字' % (len(parts), n_must, format(chars_all, ','), format(chars_must, ',')), '',
       '| 部 | 中身 | 必読か | 関わる問い | 字数 |', '|---|---|---|---|---|']
for fn, title, must, qs, body in parts:
    head = '# %s（%s・関わる問い %s・機械生成・%s UTC）\n\n' % (title, '必読' if must else '参照', qs, now.strftime('%Y-%m-%d %H:%M'))
    open(os.path.join(a.outdir, fn), 'w', encoding='utf-8', newline='\n').write(head + body)
    idx.append('| `%s` | %s | %s | %s | %s |' % (fn, title, '**必読**' if must else '参照', qs, format(len(body), ',')))
idx += ['', '公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b', '',
        '本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(a.outdir, 'bundle-index.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(idx))
print('[bundle_B_final %s] %s' % (VERSION, os.path.relpath(a.outdir, REPO)))
print('  依頼文 %s 字・資料 %d 部（必読 %d・%s 字／全体 %s 字）' % (format(len(req), ','), len(parts), n_must, format(chars_must, ','), format(chars_all, ',')))
print('  開示の項目 %d／%d・凍結の器の止まり %d 件・監査 直す前 %d → 直した後 %d（直っていない）・引用の照合の違反 %d'
      % (len([f for f in FIELDS if DISCLOSURE.get(f)]), len(FIELDS), len(blockers), len(ab_ng), len(aa_ng), len(CV)))
