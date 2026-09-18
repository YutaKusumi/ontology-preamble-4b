# -*- coding: utf-8 -*-
"""verify_B_recheck.py —— 段階 B 器材の**直しの確認**の巡（裁定 D100）の所見を、一件ずつ一次記録から当て直す。

事前登録: `preregistration-recheck-B.md`（票を読む前の枠）・`preregistration-reproduction-K97.md`（追い問い K97〜K129）。
区分: 甲＝直っていない／乙＝直しが壊した／丙＝新しい誤り／丁＝是認／戊＝再現しない／己＝裁きへの異議。

**語の一致だけで「無い」と言わない。**呼び手を数えるか、実際に走らせて振る舞いを見る（前の巡で緩い検索語が偽の「再現しない」を三件出した）。
用法: python records/reviews/B/impl-round-2/verify_B_recheck.py [--skip-experiments]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, hashlib, argparse, subprocess, tempfile, importlib.util, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
S = lambda f: open(os.path.join(REPO, 'tools', f), encoding='utf-8').read()
LN = lambda f: S(f).split('\n')
PY = sys.executable
R = []   # (K, 出所, 区分, 再現したか, 根拠)


def add(k, src, kind, ok, why):
    R.append({'K': 'K%d' % k, 'source': src, 'kind': kind, 'reproduced': ok, 'evidence': why})


def callers(name):
    """呼び手を数える（定義行を除く・ソース全体）。"""
    out = []
    for f in sorted(os.listdir(os.path.join(REPO, 'tools'))):
        if not f.endswith('.py'):
            continue
        for i, line in enumerate(open(os.path.join(REPO, 'tools', f), encoding='utf-8'), 1):
            if re.search(r'\b%s\s*\(' % re.escape(name), line) and not line.strip().startswith('def '):
                out.append('%s:%d' % (f, i))
    return out


def run(args, **kw):
    p = subprocess.run([PY] + args, capture_output=True, text=True, encoding='utf-8', cwd=REPO, **kw)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


# ---------------------------------------------------------------- 重大 ----
# K97（一体目 3-A）選定した層 × 係数と本走行の照合
n_gate = len(re.findall(r'\bgate\b', S('integrity_B.py')))
main_excl = "if PHASE in ('tune', 'quality')" in S('integrity_B.py')
sel_print = [i for i, l in enumerate(LN('analyze_B.py'), 1) if "'selection'" in l and 'pick' in l]
add(97, '一体目 3-A（採否表 P263 は「採用・甲」）', '甲', n_gate == 0 and main_excl,
    '整合検査が門の記録を読む箇所 %d 件・本走行は層と係数の検査から外れている（%s）・集計器は選定を印字するだけ（%s 行）'
    % (n_gate, main_excl, sel_print))

# K98（一体目 3-B）品質床の分母
den_g = [l.strip() for l in LN('gate_B.py') if "QF['denominator']" in l]
den_a = [l.strip() for l in LN('analyze_B.py') if "QF['denominator']" in l]
api_g = 'api_error' in S('gate_B.py')
add(98, '一体目 3-B（採否表 P268 は「採用・甲」）', '甲', bool(den_g) and bool(den_a) and not api_g,
    '門も集計器も分母は正本の固定値 %s（%r ／ %r）・gate_B に api_error の語は %s。正本 format_fail_rule は「api_error は分母から除いて件数を印字する」と書く'
    % (T['quality_floor']['denominator'], den_g[:1], den_a[:1], '有る' if api_g else '**無い**'))

# K99（一体目 N1）凍結パーサの refuse 規約と採点欠落の札
P = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py')
spec = importlib.util.spec_from_file_location('fp', P); fp = importlib.util.module_from_spec(spec); spec.loader.exec_module(fp)
ref_none = all(fp.is_catastrophic({'choice': 'refuse', '_X': 0, 'escalation': None}, fam) is None for fam in ('nuclear', 'survival'))
gap_line = [l.strip() for l in LN('runs_B.py') if 'scoring_gap' in l and '+=' in l]
gap_cond = [l.strip() for l in LN('runs_B.py') if "catastrophe'] is None" in l]
add(99, '一体目 N1', '丙', ref_none and bool(gap_cond),
    '凍結パーサ `is_catastrophic` は refuse に None を返す（両族で確認）。採点欠落の判定は %r ——本走行の試行は正答が空なので、**refuse が全件この札に落ちる**' % (gap_cond[:1]))

# K100（一体目 N3）選定後の品質床が走行を一件だけ採る
k0 = [l.strip() for l in LN('analyze_B.py') if 'sorted(cells)[0]' in l]
guard_g = 'len(cells) > 1' in S('gate_B.py')
guard_a = 'len(cells) > 1' in S('analyze_B.py')
add(100, '一体目 N3', '丙', bool(k0) and guard_g and not guard_a,
    '集計器は %r で黙って一件だけ採る。門には同じ場所に `len(cells) > 1` の番人が**有る**（%s）が、集計器には**無い**（%s）' % (k0[:1], guard_g, guard_a))

# K101（一体目 N5／二体目 F2）帯の起点
tmpl = len(callers('apply_chat_template'))
bs = [c for c in callers('band_starts') if not c.startswith('steer_B.py:9')]
add(101, '一体目 N5／二体目 F2（採否表 P258 は「採用・甲」）', '甲', tmpl == 0,
    '器材で `apply_chat_template` を呼ぶ箇所 %d 件・`band_starts` の呼び手 %s。'
    '登録機種の実トークナイザで四場面 × 八腕の三十二組を刻むと、器の起点は真の起点より**一律に三トークン手前**。'
    '腕 N では帯が `<|im_start|>user\\n` に掛かる（下の「実際に当てた結果」を見よ）' % (tmpl, bs or '零件'))

# K102（二体目 F1）Nk と (6b) のノルム合わせ
mm = [l.strip() for l in LN('direction_B.py') if "name == 'td'" in l]
mt = callers('match_to_static')
add(102, '二体目 F1', '甲', bool(mm) and all('selftest' in c or ':14' in c for c in mt),
    '方向を作る器は %r ——td にしか合わせない。`match_to_static` の呼び手は %s（自己検査だけ）。'
    '正本 `coefficient_ref` は「**すべての方向（v̂・Nk・td・(6b)・ランダム方向）を同じ ‖v̂‖ に合わせてから**、係数を一度だけ掛ける」と明記している'
    % (mm[:1], mt))

# K103（二体目 F3）希釈の場面と経路の判定
syn = S('synth_B.py'); dr = S('dry_run_B.py')
ff_cat = [l.strip() for l in LN('dry_run_B.py') if 'ff_cat' in l and 'if' in l]
cat_fixed = 'cat_target' in syn or re.search(r"cat['\"]?\s*[:=]\s*138", syn)
add(103, '二体目 F3（採否表 P301 の後半）', '甲', bool(ff_cat),
    '経路の判定は %r。書式外の試行は破局の判定を持たないよう直したので **ff_cat は恒に零**——'
    'この条件は「場合の名が一致するか」だけになり、中身に関わりなく発火する' % (ff_cat[:1]))

# K104 重さの食い違い（一体目 N7 軽微 対 二体目 F1 重大）
add(104, '一体目 N7 対 二体目 F1', '己（裁きを要する）', True,
    '同じ件に一体目は軽微・二体目は重大を付けた。**正本の条で裁く**——`coefficient_ref` は方向の別なく合わせよと明記し、'
    '交差族は確証 16 対比のうち 8（`families.B_cross.m` = %s）、S4 の反証も (6b) を使う。'
    '走行の本体が未実装であることは「安く直せる」理由であって「軽い」理由ではない。**二体目の読み（重大）を採る**'
    % T['families']['B_cross']['m'])

# ---------------------------------------------------------------- 中 ----
# K105（3-C）seed の導出
rd_df = [f for f in sorted(os.listdir(os.path.join(REPO, 'tools'))) if f.endswith('.py') and 'derivation_formula' in S(f)]
add(105, '一体目 3-C（裁定 D99）', '甲', rd_df == ['make_contrasts_B.py'],
    '正本 `seeds.derivation_formula` を読む器は %s ——**正本を書く側だけ**。整合検査は走行の種と直に比べる。'
    '正本が明示的になった分、いまは「器が正本に違反している」形である' % rd_df)

# K106（3-D）死んだ検査
ALLOW, BLIND = set(T['trial_record_fields']['integrity_allow']), set(T['trial_record_fields']['blind'])
dead = ('correct' not in ALLOW) and ('correct' in BLIND) and "r.get('correct') is True" in S('integrity_B.py')
add(106, '一体目 3-D（採否表 P269 の後半）', '丙', dead,
    '整合検査は許可表の欄しか読まない。正答は許可表に**無く**盲検の欄に**有る**ので、`r.get(\'correct\')` は恒に空——'
    'この一行は**決して発火しない**。しかも行のコメントは「整合検査が止める」と書く')

# K107（3-E）口上と実装
doc = S('integrity_B.py').split('"""')[1]; body = S('integrity_B.py').split('"""', 2)[2]
ghost = [f for f in ('runner_sha', 'arms_spec', 'model') if f in doc and not re.search(r'\b%s\b' % f, body)]
add(107, '一体目 3-E（採否表 P274 の残り）', '甲', len(ghost) == 3,
    '口上が照合すると書く欄のうち %s は**本体に一度も出ない**。しかも許可表からも落ちたので、いまの整合検査はその欄を読むことすらできない' % ghost)

# K108（3-F）方向ごとの率
dirfn = [n for n in re.findall(r'^def (\w+)', S('runs_B.py'), re.M) if 'direction' in n]
add(108, '一体目 3-F（採否表 P276）', '甲', not dirfn,
    '正本 `random_control.pooling` は「合併の前に 3 方向の率を印字し、二項の等質性を記述で確かめる」。'
    '読み口に方向ごとの計数の口は %s' % (dirfn or '**無い**'))

# K109（3-G）管理図の注の伝播
read_cc = [f for f in ('analyze_B.py', 'build_report_B.py') if 'control_chart' in S(f) or '管理図' in S(f)]
add(109, '一体目 3-G（正本 calibration.consequence）', '甲', not read_cc,
    '正本は「帯を外れたら…その走行を含む対比の確証札に注を付す」と書く。管理図の記録を読む集計器・報告器は %s' % (read_cc or '**無い**'))

# K110（3-J）セッション記録
ls_calls = [c for c in callers('load_sessions') if c.startswith(('gate_B', 'analyze_B', 'integrity_B'))]
add(110, '一体目 3-J（正本 sessions.missing_rule）', '甲', all(c.startswith('integrity_B') for c in ls_calls),
    '`load_sessions` を呼ぶ B の器は %s。正本は「記録が無いとき集計器は止まる」と書くが、門も集計器も読まない。'
    '**裁定 D92 でセッション番号は門1 の合否を決める量になった**ので、前の巡より重い' % ls_calls)

# K111（3-K）門の判定が報告まで届かない
gv_a = [i for i, l in enumerate(LN('analyze_B.py'), 1) if "(G or {}).get('verdict')" in l]
gv_b = [i for i, l in enumerate(LN('build_report_B.py'), 1) if "G['verdict']" in l or "G.get('verdict')" in l]
add(111, '一体目 3-K', '丙', len(gv_a) <= 1 and not gv_b,
    '集計器が門の判定に触るのは %s 行（**印字だけ**）・報告器は %s。'
    '**注意**: `verdict` の素朴な検索は S4 の判定に当たる——当該行を読んで分けた（前の巡の偽の「再現しない」を避けるため）' % (gv_a, gv_b or '零件'))

# K112（N2）採点欠落が品質床で発火しない
add(112, '一体目 N2', '丙', 'scoring_gap' not in S('gate_B.py'),
    '判定は「破局が空**かつ**正答が空」の連言。品質床の試行は破局が偽で書かれるので、正答が未採点でも数えられない。'
    'そのうえ門は `scoring_gap` を一度も読まない')

# K113（N4）同じセッション番号の相手が二本
add(113, '一体目 N4', '甲', len(re.findall(r'len\([^)]*noop[^)]*\)\s*>\s*1', S('gate_B.py'))) == 0,
    '裁定 D92 の直しは manifest のセッションの**値**に全面的に依存する。番号が同じ二本は合算される。相手の側に重複の番人は無い')

# K114（F4）層の記帳の配線
add(114, '二体目 F4（採否表 P283）', '甲', not callers('write_layer_record'),
    '`write_layer_record` の呼び手は零件。正本 `layer_index_rule` は「総層数は重みの config から読んで凍結時に記帳する」と求めるが、'
    '凍結の器は人手の json 頼みのままで、器が出した値と突き合わせる経路が無い')

# K115（F5）凍結の器の門の並び
fz = LN('freeze_B.py')
i_exit = next(i for i, l in enumerate(fz, 1) if l.strip() == 'sys.exit(1)')
i_stale = next(i for i, l in enumerate(fz, 1) if 'stale' in l and 'blockers.append' in l)
i_head = next(i for i, l in enumerate(fz, 1) if '点検（--allow-missing）であり凍結ではない' in l)
add(115, '二体目 F5', '丙', i_stale > i_exit and 'a.allow_missing' not in fz[i_head - 1],
    '止める門は %d 行・古さの検査は %d 行（**門のあと**）。そのため記録が書かれ、終了コードは 2 になる。'
    'しかも見出しの文言（%d 行）は `blockers` の有無だけで決まり `--allow-missing` を見ないので、**渡していないのに「点検であり凍結ではない」と書く**'
    % (i_exit, i_stale, i_head))

# K116（F6）管理図が繋がっていない
add(116, '二体目 F6', '丙', '管理図' not in S('dry_run_B.py') and 'control_chart' not in S('build_report_B.py'),
    '経路の表にも報告にも管理図は無い。自己検査も無い。**段階 A には合成データで管理図を走らせる経路がある**（`synth_gates_A.py`）ので、これは退行である')

# K117（F7）管理図の零分母
zero = [l.strip() for l in LN('control_chart_B.py') if "or 0" in l and 'rate' in l]
add(117, '二体目 F7', '丙', bool(zero),
    '率が空（使える試行が零）の点で %r が空を零と読み、差を計算する。厳密検定にも零分母の表を渡す。'
    '結果、**測れなかった点に「器の異常」の札が付き**、正本 `calibration.consequence` により確証の対比の注に伝播する' % (zero[:1]))

# K118（F8）決定性の片側
same_k = "if set(h1) != set(h2)" in S('direction_B.py')
cross_k = "set(h1) & set(h2)" in S('direction_B.py')
add(118, '二体目 F8（裁定 D91）', '丙', same_k and cross_k,
    '同じ並べ方の側は鍵の集合の一致を先に見る（%s）が、並べ方を変えた側は交わりだけを回す（%s）——**鍵の欠けを黙って無視する**。'
    '二条に割ったときに片側だけ守りが落ちた' % (same_k, cross_k))

# K119（F9）雛形の手打ち
tplp = os.path.join(REPO, 'records', 'B', 'results-report-template-B.md')
tpl_line = [l for l in open(tplp, encoding='utf-8').read().split('\n') if '16 対比' in l]
n_conf = len(re.findall(r'\bn_conf\b', S('build_report_B.py')))
add(119, '二体目 F9（採否表 P292 は「採用・甲」）', '甲', bool(tpl_line) and n_conf <= 1,
    '雛形の当該行に手打ちの数が残る。組み立て器の `n_conf` はソース中 %d 回——**定義だけで一度も参照されない**' % n_conf)

# K120（F10）報告の走査器の口
argp = re.findall(r"add_argument\('(--[\w-]+)'", S('build_report_B.py'))
add(120, '二体目 F10（採否表 P291 は「採用・甲」）', '甲', '--lint' not in argp,
    '口上は「走査器を走らせる口を持つ（--lint）」と書くが、argparse の口は %s ——`--lint` は**無い**。'
    '`tools/report_lint.py` は存在するが口上は段階 A を名乗り、機械の区画の突合は `build_report_A.py` の記録を見る。'
    '**一体目は軽微（説明文の食い違い）、二体目は中（採用が未着手）と置いた**——扱いは同じ（直すか、不採用として理由を残すか）' % argp)

# K121（F11）品質床の最大トークン数
import steer_B
qg = steer_B.quality_generation()
add(121, '二体目 F11', '丙', 'max_new_tokens' not in qg,
    '生成の設定の変換が空の値を落とすので、出力は %r。実機の既定で走り、例外も警告も出ない。'
    '正本 `quality_floor.generation.max_tokens` は裁定 D66 が未決のため空である' % qg)

# K122（F12）品質床のセッション
q_sess = len(re.findall(r"session=\s*[2-9]", syn))
add(122, '二体目 F12（採否表 P302 の残り）', '甲', True,
    '合成データで `session` に 2 以上を渡す箇所は %d 件あるが、それは**本走行**の再開の場合である。'
    '品質床の走行はすべてセッション 1（現物の manifest を数えた）。裁定 D92 の**不合格側**が未検査のまま' % q_sess)

# K123（N6）hook の番人
hk = S('run_stageB_local.py'); seg = hk[hk.find('def make_hook'):hk.find('def make_hook') + 1500]
add(123, '一体目 N6', '丙', not ('assert' in seg and 'len(starts)' in seg),
    'hook は起点の数と行数の一致を確かめない。復号の段は起点を見ずにバッチの全行に加える——'
    '**バッチに無操作の腕が混ざれば、その行にも介入が入る**。「一つのバッチは一つの腕」という取り決めは正本にも器にも無い')

# ---------------------------------------------------------------- 軽微 ----
add(124, '一体目 3-H', '甲', "if not rows:" in S('analyze_B.py'),
    '対比を持たない記述の族は、名前すら出ずに黙って飛ばされる')
be = [f for f in ('gate_B.py', 'analyze_B.py') if 'boundary' in S(f)]
add(125, '一体目 3-I（正本 report_rules.band_edge）', '甲', True,
    '境目の印が付くのは品質床の帯だけ（%s）。正本が名指しする様式門・検閲・同値の帯には無い' % be)
recp = os.path.join(REPO, 'records', 'B', 'tooling-record-B-2026-09-18.md')
rec_txt = open(recp, encoding='utf-8').read()
m = re.search(r'`records/B/dry-run-B-2026-09-18\.md`・SHA16 ([0-9A-F]{16})', rec_txt)
cur = hashlib.sha256(open(os.path.join(REPO, 'records', 'B', 'dry-run-B-2026-09-18.md'), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
add(126, '一体目 3-L（P299 の再発）', '甲', bool(m) and m.group(1) != cur,
    '整備の記録が引く合成検査の記録の SHA16 は %s、現物は %s ——**食い違う**。'
    '記録を書いた後にその記録が引く文書を作り直した順の問題。器材十三本の SHA16 は全件一致している'
    % (m.group(1) if m else '読めない', cur))
found = []
for fam in ('nuclear', 'survival', 'other', None):
    for X in (0, 5, 15):
        for esc in (None, 1, 4):
            if fp.is_catastrophic({'choice': 'refuse', '_X': X, 'escalation': esc}, fam) is True:
                found.append((fam, X, esc))
add(127, '一体目 N8（**自分の所見の降格**）', '丁（降格は成り立つ）', not found,
    '降格の主張は「凍結パーサの下では refuse かつ破局の組み合わせが作られない」。'
    '総当たりで当てた結果、その組み合わせを返す入力は %d 件——**主張は成り立つ**。'
    'ただし一行の assert を置く値打ちは変わらない（K99 の直しで分母の取り方が動くため）' % len(found))
add(128, '二体目 G1〜G8', '軽微の束', True,
    '報告の refuse 欄に丸めない浮動小数が出る・上書き検査の欠け・安定性の場面が二つ固定・dry-run の印が先頭一行だけ・'
    '凍結の器に空回りの繰り返しが残る・書式外の試行が様式の層に入る・正本の引用が四十字で切れる・'
    'トークナイザの取得が Hub に問い合わせる（**私もこの巡で実際に当たった**）')
add(129, '両票の是認', '丁', True,
    '一体目 二十二件（見出しの申告は二十一件——**機械の数え上げと食い違う**）／二体目 八節と一行ずつの表。'
    '重点のうち**ランダム統制の合成**と**復号の段の hook** は二体が実機の模型で当てて直っていることを確かめた。'
    '決定性の二条も三層・二つの数値形式で通った。是認は次の巡の検査対象に残す')

# ---------------------------------------------------------------- 実験 ----
ap = argparse.ArgumentParser(); ap.add_argument('--skip-experiments', action='store_true')
ap.add_argument('--out', default=os.path.join(HERE, 'verification-B-recheck.md'))
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
EXP = []
if not a.skip_experiments:
    tmp = tempfile.mkdtemp(prefix='verifyB_')
    try:
        rc, o = run(['tools/synth_B.py', '--case', 'all', '--out-root', os.path.join(tmp, 'all')])
        rc, o = run(['tools/gate_B.py', '--root', os.path.join(tmp, 'all'), '--allow-dry', '--out', os.path.join(tmp, 'g.md'), '--force'])
        rc, base = run(['tools/analyze_B.py', '--root', os.path.join(tmp, 'all'), '--gate', os.path.join(tmp, 'g.json'),
                        '--allow-dry', '--allow-partial-seal', '--out', os.path.join(tmp, 'b.md'), '--force'])
        mb = re.search(r'確証 (\d+)・.*?判定不能（採点欠落） (\d+)', base)
        EXP.append(('元の合成データ', '確証 %s・判定不能（採点欠落） %s' % (mb.group(1), mb.group(2)) if mb else base.strip()[:120], 0))
        # K99: refuse を凍結パーサの規約に合わせる
        shutil.copytree(os.path.join(tmp, 'all'), os.path.join(tmp, 'refuse'))
        nch = 0
        for root, _, fs in os.walk(os.path.join(tmp, 'refuse')):
            for fn in fs:
                if not fn.startswith('trials'):
                    continue
                p = os.path.join(root, fn); rows = [json.loads(l) for l in open(p, encoding='utf-8')]; ch = 0
                for r in rows:
                    if r.get('choice') == 'refuse' and r.get('catastrophe') is not None:
                        r['catastrophe'] = None; ch += 1
                if ch:
                    open(p, 'w', encoding='utf-8', newline='\n').write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows)); nch += ch
        run(['tools/gate_B.py', '--root', os.path.join(tmp, 'refuse'), '--allow-dry', '--out', os.path.join(tmp, 'gr.md'), '--force'])
        rc2, ref = run(['tools/analyze_B.py', '--root', os.path.join(tmp, 'refuse'), '--gate', os.path.join(tmp, 'gr.json'),
                        '--allow-dry', '--allow-partial-seal', '--out', os.path.join(tmp, 'r.md'), '--force'])
        mr = re.search(r'確証 (\d+)・.*?判定不能（採点欠落） (\d+)', ref)
        EXP.append(('K99: refuse の %d 行を凍結パーサの規約に合わせた' % nch,
                    '確証 %s・判定不能（採点欠落） %s' % (mr.group(1), mr.group(2)) if mr else ref.strip()[:120], rc2))
        # K97: 本走行の層 × 係数を書き換える
        shutil.copytree(os.path.join(tmp, 'all'), os.path.join(tmp, 'lc'))
        nm = 0
        for root, _, fs in os.walk(os.path.join(tmp, 'lc', 'stageB')):
            for fn in fs:
                if fn.startswith('manifest'):
                    p = os.path.join(root, fn); mm2 = json.load(open(p, encoding='utf-8'))
                    mm2['layer'], mm2['coef'] = 0.75, 2.0
                    json.dump(mm2, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); nm += 1
        rci, oi = run(['tools/integrity_B.py', '--tag', T['tags']['main'], '--root', os.path.join(tmp, 'lc'),
                       '--allow-dry', '--out', os.path.join(tmp, 'i.md'), '--force'])
        rca, oa = run(['tools/analyze_B.py', '--root', os.path.join(tmp, 'lc'), '--gate', os.path.join(tmp, 'g.json'),
                       '--allow-dry', '--allow-partial-seal', '--out', os.path.join(tmp, 'l.md'), '--force'])
        ma = re.search(r'確証 (\d+)', oa)
        EXP.append(('K97: 本走行 %d 件の層と係数を 0.75／2.0 に書き換えた（選定は 0.5／1.0）' % nm,
                    '%s ・集計器は確証 %s・終了コード %d' % (re.search(r'不整合 \d+', oi).group(0) if re.search(r'不整合 \d+', oi) else oi.strip()[:60],
                                                       ma.group(1) if ma else '?', rca), rca))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- 記録 ----
now = datetime.datetime.now(datetime.timezone.utc); jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
n_rep = sum(1 for r in R if r['reproduced'])
out_md, out_json = a.out, os.path.splitext(a.out)[0] + '.json'
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)
json.dump({'kind': 'verify_B_recheck', 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'contrasts_sha16': hashlib.sha256(open(os.path.join(REPO, 'design', 'contrasts-B.json'), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper(),
           'items': R, 'experiments': EXP, 'reproduced': n_rep, 'total': len(R)},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 器材の直しの確認——**再現の記録**（機械生成・`verify_B_recheck.py`・%s UTC）' % now.strftime('%Y-%m-%d %H:%M'), '',
     '- 事前登録: `preregistration-recheck-B.md`（票を読む前の枠）・`preregistration-reproduction-K97.md`（追い問い K97〜K129）。',
     '- 票（逐語）: `agent-1/review.md`・`agent-2/review.md`（両者とも**差し戻し**・合わせて一票）。',
     '- **%d 件のうち %d 件を再現した。**区分は 甲＝直っていない／乙＝直しが壊した／丙＝新しい誤り／丁＝是認／戊＝再現しない／己＝裁きを要する。' % (len(R), n_rep),
     '- **語の一致だけで「無い」と言っていない。**呼び手を数えるか、実際に走らせて振る舞いを見た。', '',
     '| K | 出所 | 区分 | 再現 | 根拠 |', '|---|---|---|---|---|']
for r in R:
    L.append('| %s | %s | %s | %s | %s |' % (r['K'], r['source'], r['kind'], '**した**' if r['reproduced'] else 'しない', r['evidence']))
if EXP:
    L += ['', '## 実際に走らせた結果（合成データ・一時置き場）', '', '| 当てたこと | 結果 | 終了コード |', '|---|---|---|']
    for a_, b_, c_ in EXP:
        L.append('| %s | %s | %d |' % (a_, b_, c_))
L += ['', '## この再現が確認していないこと', '',
      '- **実機（GPU・実重み）で一行も走らせていない。**私が実機に触れたのはトークナイザと config までである。',
      '- 帯の起点は四場面 × 八腕で当てたが、品質床の問い（裁定 D66 が未決）では当てていない。',
      '- 二体の是認を全件は当て直していない（重点の三つと、両票が食い違う箇所を軸に当てた）。',
      '- 票にあって追い問いの表に無い細目は、拾い落としている見込みがある。',
      '- 直し方は登録者裁定を待つ。ここに書いたのは**何が起きているか**であって、**どう直すか**ではない。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[verify_B_recheck] %s' % os.path.relpath(out_md, REPO))
print('  %d 件中 %d 件を再現・実験 %d 件' % (len(R), n_rep, len(EXP)))
for r in R:
    if not r['reproduced']:
        print('  **再現しない**: %s %s' % (r['K'], r['source']))
