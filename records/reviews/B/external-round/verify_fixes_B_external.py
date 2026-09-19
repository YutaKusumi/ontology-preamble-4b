# -*- coding: utf-8 -*-
"""verify_fixes_B_external.py —— 系統の外への検分（裁定 D117〜D131）で「採用」とした直しが、**現物の器で効いているか**を当て直す。

枠（判定の基準・予想・利益相反）は、この器を書く前に `preregistration-fix-audit-B-external.md` に置いた。
**器の振る舞いの件は、文の証拠で「直っている」にしない。**正本と草案に書いてあっても、器が同じ振る舞いをしなければ「直っていない」。
二度走らせる——直す前（`--label before`）と直した後（`--label after`）。直す前の結果も消さずに残す。

判定: 直っている（振る舞い）／直っている（配線）／直っている（文）／直っていない／登録者の裁定待ち。
**直す前の走行（三回目）の後に変えた検査**（基準は動かさず、見方を強めるか誤反応を除くだけ・出力の末尾にも印字する）:
  - P357: 「古い式の文が正本に残っていないか」で見ていたが、正本は**履歴として古い式を引用する**ので誤って反応する。
    「新しい式（試行の記録に書く種はバッチの種・引き直しの種）が正本にあるか」で見る形に改めた。
  - P361・P376: 文の有無で見ていたのを、**壊した入力で器を走らせて止まるか**で見る形に強めた。
  - X6〜X10: 直している途中で見つけた件を行として足した（直す前の監査の表には無い）。
用法: python records/reviews/B/external-round/verify_fixes_B_external.py --label before|after [--force] [--skip-live]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, argparse, subprocess, tempfile, importlib, datetime, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
TOOLS = os.path.join(REPO, 'tools')
sys.path.insert(0, TOOLS)
PY = sys.executable
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
S = lambda f: open(os.path.join(TOOLS, f), encoding='utf-8').read() if os.path.exists(os.path.join(TOOLS, f)) else ''
DRAFT_PATH = os.path.join(REPO, 'design', 'design-stageB-draft12.md')
DRAFT = open(DRAFT_PATH, encoding='utf-8').read()

OK_B, OK_W, OK_T = '直っている（振る舞い）', '直っている（配線）', '直っている（文）'
NG, WAIT = '直っていない', '登録者の裁定待ち'
R = []


def add(p, k, d, what, status, evidence):
    R.append({'P': p, 'K': k, 'D': d, 'what': what, 'status': status, 'evidence': evidence})


def check(p, k, d, what, fn):
    try:
        st, ev = fn()
    except Exception as e:                                  # 器が無い・呼べない・壊れている——いずれも「直っていない」
        st, ev = NG, '確かめる途中で止まった: %s: %s' % (type(e).__name__, str(e)[:300])
    add(p, k, d, what, st, ev)


def callers(name, files=None):
    out = []
    for f in sorted(files or os.listdir(TOOLS)):
        if not f.endswith('.py'):
            continue
        for i, line in enumerate(S(f).split('\n'), 1):
            if re.search(r'\b%s\s*\(' % re.escape(name), line) and not line.strip().startswith('def '):
                out.append('%s:%d' % (f, i))
    return out


def rules():
    """判定の規則を置く器（直すときに足す）。無ければ ImportError で「直っていない」に倒れる。"""
    importlib.invalidate_caches()
    if 'rules_B' in sys.modules:
        del sys.modules['rules_B']
    return importlib.import_module('rules_B')


def run(args, cwd=None, env=None):
    p = subprocess.run([PY] + args, capture_output=True, text=True, encoding='utf-8', cwd=cwd or REPO,
                       env=dict(os.environ, PYTHONIOENCODING='utf-8', **(env or {})))
    return p.returncode, (p.stdout or '') + (p.stderr or '')


ap = argparse.ArgumentParser()
ap.add_argument('--label', required=True, choices=['before', 'after'])
ap.add_argument('--force', action='store_true')
ap.add_argument('--skip-live', action='store_true', help='合成データを作って器を走らせる検査を飛ばす（飛ばしたら印字する）')
a = ap.parse_args()
OUT = os.path.join(HERE, 'verification-fixes-B-external-%s.md' % a.label)
if os.path.exists(OUT) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % OUT)


# ============================================================ P337 D117 ====
def p337():
    body = 'def run_cell' in S('run_stageB_local.py') and 'def main_position_activation' in S('direction_B.py')
    fields = T['disclosure']['fields']
    in_draft = [f for f in fields if f in DRAFT]
    items = (T['disclosure'].get('items') or {})
    listed = [f for f in fields if items.get(f)]
    if not body:
        return NG, '走行器か抽出器の本体が無い'
    if len(in_draft) < len(fields) or len(listed) < len(fields):
        return NG, ('本体は書いた。**しかし開示の五項目の列挙が草案に無い**（草案に現れる項目 %d／%d・正本に中身がある項目 %d／%d）。'
                    '正本は「依頼文と草案の両方に必ず列挙する」と定めている' % (len(in_draft), len(fields), len(listed), len(fields)))
    return OK_T, '本体は書いた。開示の五項目は正本 `disclosure.items` に一つの出所として置き、草案がそれを束縛する（%d／%d）' % (len(in_draft), len(fields))
check('P337', 'K130', 'D117', '本体を書く・開示の欄を草案と依頼文の両方に列挙する', p337)


# ============================================================ P338 D118 ====
def p338():
    src = S('analyze_B.py')
    if 'power >= pmin' in src:
        return NG, '集計器の S4 の判定は `elif power >= pmin:` で「下がらなかった」を出す——**検出力の規則のまま**。区間も `wald_ci`'
    r = rules()
    T3 = T['descriptive_families']['B_desc_S4']['three_way']
    eff = T3['effect_pt']
    # 同等性の規則: 区間が零を含み、(ランダム − (6b)) の片側 95% 上限が効き目以上なら「当否を言わない」
    # 相手 0.1725・n=200 の近傍で、区間が零を含み上限が効き目以上になる組を探す
    n = 200
    case_undecided = case_notdrop = None
    for kB in range(30, 40):
        for kA in range(kB - 20, kB + 1):
            v = r.s4_verdict(kA, n, kB, n, T)
            if v['verdict'] == '当否を言わない' and case_undecided is None and v['upper_one_sided_pt'] >= eff:
                case_undecided = (kA, kB, v)
            if v['verdict'].startswith('下がらなかった') and case_notdrop is None:
                case_notdrop = (kA, kB, v)
    if case_undecided is None or case_notdrop is None:
        return NG, '三分岐の (iii) の二つの枝を再現できない（%s・%s）' % (case_undecided, case_notdrop)
    if not case_notdrop[2]['upper_one_sided_pt'] < eff:
        return NG, '「下がらなかった」の組で片側上限が効き目未満でない: %s' % (case_notdrop,)
    if not callers('s4_verdict', ['analyze_B.py']):
        return NG, '規則の関数はあるが、**集計器が呼んでいない**'
    if 'wald_ci' in src:
        return NG, '集計器にまだ Wald の区間が残っている'
    return OK_B, ('片側上限が効き目以上の組（(6b) %d・ランダム %d／%d）は「当否を言わない」、未満の組（%d・%d）は「下がらなかった」。'
                  '集計器は `rules_B.s4_verdict` を呼ぶ。区間は Newcombe' % (case_undecided[0], case_undecided[1], n, case_notdrop[0], case_notdrop[1]))
check('P338', 'K131', 'D118', 'S4 の「下がらなかった」を同等性の規則で決める・区間を Wald から改める', p338)


# ============================================================ P339 D119 ====
def p339():
    c = callers('equivalence_band')
    ok = any(x.startswith('design_facts_B.py') for x in c) and any(x.startswith('gate_B.py') for x in c)
    return (OK_W if ok else NG), '同値の帯の共有の関数の呼び手: %s' % '・'.join(c)
check('P339', 'K132', 'D119', '転記行 C を門と同じ模擬で出す', p339)


# ============================================================ P340 D120 ====
def p340():
    q = T['quality_floor']
    keys = [k for k in ('input', 'apply_band', 'scoring') if q.get(k)]
    import steer_B
    g = steer_B.quality_generation()
    ok = len(keys) == 3 and g.get('max_new_tokens') == q['generation']['max_tokens']
    return (OK_B if ok else NG), '正本の欄 %s・品質床の生成の最大トークン数 %s（正本 %s）' % ('・'.join(keys), g.get('max_new_tokens'), q['generation']['max_tokens'])
check('P340', 'K133', 'D120', '品質床の四欄を決めて正本に登録する', p340)
add('P340', 'K133', 'D66', '品質床の課題そのものの選定', WAIT, '裁定 D66（登録者が選ぶ）。下限 `quality_floor.base_min` は実測の正答率を見てから凍結する')


# ============================================================ P341 D121 ====
def p341():
    a_ = 'SIGN_VALUES' in S('analyze_B.py') and 'sign_values' in S('analyze_B.py') + S('freeze_B.py')
    f_ = 'sign_values' in S('freeze_B.py') or 'SIGN_VALUES' in S('freeze_B.py')
    return (OK_W if (a_ and f_) else NG), '集計器の列挙の検査 %s・凍結の器の列挙の検査 %s' % ('有り' if a_ else '**無し**', '有り' if f_ else '**無し**')
check('P341', 'K134', 'D121', '封印の符号を列挙型にし、両方の器で検べる', p341)


# ============================================================ P342〜P344 D122 ====
def mut_record():
    """変異の記録（`tools/mutation_B.py` の出力）。行は `rows`、各行の `caught` は捕まえた器の一覧・`missed` は捕まえなかった器の一覧。
    **一回目の監査はここで鍵を `items` と取り違え、四件を誤って「直っていない」とした**（監査の器の誤り・記録に残す）。"""
    fs = sorted(f for f in os.listdir(os.path.join(REPO, 'records', 'B')) if f.startswith('mutation-B-') and f.endswith('.json'))
    m = json.load(open(os.path.join(REPO, 'records', 'B', fs[-1]), encoding='utf-8'))
    assert isinstance(m.get('rows'), list) and m['rows'], '変異の記録に行が無い: %s' % fs[-1]
    return m, fs[-1]


def _caught(x):
    """自己検査の変異は `caught`／`missed`（器の一覧）で、合成データを通す変異は `changed`（出力が変わったか）で記録される。
    **二回目の監査はこの別を見落とし、合成データを通す変異を二件とも「捕まえなかった」と読んだ**（監査の器の誤り・記録に残す）。"""
    if x.get('pipeline'):
        return x.get('changed') is True
    return bool(x.get('caught')) and not x.get('missed')


def mut_caught(m, word):
    hit = [x for x in m['rows'] if word in x.get('name', '')]
    return hit, bool(hit) and all(_caught(x) for x in hit)


def p342():
    m, fn = mut_record()
    hit, ok = mut_caught(m, '帯の起点')
    return (OK_B if ok else NG), '変異の記録 `%s`: 帯の起点の変異 %d 件・すべて捕まえた %s' % (fn, len(hit), ok)
check('P342', 'K135', 'D122', '帯の起点の自己検査を独立の正解と照らす', p342)


def p343():
    m, fn = mut_record()
    hit, ok = mut_caught(m, 'ノルム')
    return (OK_B if ok else NG), '変異の記録 `%s`: ノルムの変異 %d 件・すべて捕まえた %s' % (fn, len(hit), ok)
check('P343', 'K136', 'D122', '自己検査を変異で落ちるところまで作る', p343)


def p344():
    said = '飛ばした' in S('steer_B.py')
    strict = [f for f in ('steer_B.py', 'direction_B.py', 'run_stageB_local.py') if 'OP4B_REQUIRE_FULL_SELFTEST' in S(f)]
    if not said:
        return NG, '飛ばしたことを印字しない'
    if len(strict) < 3:
        return NG, '「飛ばした」は印字する。**しかし実機の段で飛ばしを失敗に倒す口が無い**（持つ器: %s）' % ('・'.join(strict) or 'なし')
    return OK_W, '三つの器とも、`OP4B_REQUIRE_FULL_SELFTEST=1` のとき飛ばしを失敗に倒す'
check('P344', 'K137', 'D122', '飛ばしたら印字し、実機の段では失敗に倒す', p344)


def p345():
    src = S('run_stageB_local.py')
    meta = 'hook.op4b' in src or "hook.meta" in src
    allset = 'assert_hooks_exactly' in src
    if not (meta and allset):
        return NG, 'hook に腕・方向・係数・バッチ番号を持たせていない（%s）／全層の hook の集合を期待と照らしていない（%s）' % (meta, allset)
    return OK_W, 'hook は腕・方向・係数・バッチ番号を持ち、生成の直前に全層の hook の集合を期待と照らす（振る舞いは端から端までの検査）'
check('P345', 'K138', 'D122', 'hook に腕・方向・係数・バッチ番号を持たせ、登録の集合を確かめる', p345)


# ============================================================ P346 D123 ====
def p346():
    by = T['arms']['by_scenario']
    td_all = all(any('vtd' in x for x in by[sc]) for sc in T['scenarios'])
    if not td_all:
        return NG, 'td が全場面に無い'
    if 'td_specificity' not in S('rules_B.py'):
        return NG, 'td を全場面に広げたが、**「同じだけ動いた」の数の基準を判定する器が無い**（集計器・規則の器に実装が零件）'
    r = rules()
    same = r.td_specificity(40, 200, 42, 200, T)       # 差がほぼ零 → 区間が零を含む → 書かない
    diff = r.td_specificity(10, 200, 60, 200, T)       # 大きな差 → 書ける
    if not (same['write_specificity'] is False and diff['write_specificity'] is True):
        return NG, '数の基準の二つの枝が再現しない: %s / %s' % (same, diff)
    if not callers('td_specificity', ['analyze_B.py']):
        return NG, '規則の関数はあるが、**集計器が呼んでいない**'
    return OK_B, 'td は全場面にある。v と td の差の区間が零を含めば「特異性を書かない」、外せば「書ける」（両方の枝を当てた）。集計器が呼ぶ'
check('P346', 'K139', 'D123', 'td を全場面に広げ、「同じだけ動いた」の数の基準を置く', p346)


# ============================================================ P347 D124 ====
def p347():
    import steer_B
    band_ok = 'len(ids) - 1' in S('steer_B.py')
    stale = [k for k in ('prompt_assembly', 'chat_template') if '場面の本文」の開始位置' in str(T['runner'].get(k)) or '場面の本文が始まる位置」として引く' in str(T['runner'].get(k))]
    stale_doc = [f for f in ('run_stageB_local.py',) if '場面本文の開始位置から EOS まで' in S(f)]
    if not band_ok:
        return NG, '帯の起点が主位置でない'
    if stale or stale_doc:
        return NG, '器の帯は主位置から。**しかし正本（%s）と器の口上（%s）に「場面本文の開始から」が残る**' % ('・'.join(stale) or 'なし', '・'.join(stale_doc) or 'なし')
    return OK_B, '帯は主位置から EOS まで（steer_B の自己検査と端から端までの検査）。正本と口上の古い文は無い'
check('P347', 'K140', 'D124', '帯を主位置から EOS までに狭める・バッチの組み方を登録する', p347)


# ============================================================ P348 D125 ====
def p348():
    src = S('analyze_B.py')
    ok = "not (r.get('fired') or [])" in src
    m, fn = mut_record()
    hit, caught = mut_caught(m, 'Holm')
    return (OK_B if (ok and caught) else NG), '順位は門の当たった対比を全部外す（様式門を含む）・変異「様式門を Holm の順位に戻す」を捕まえた %s（`%s`）' % (caught, fn)
check('P348', 'K141', 'D125', '様式門の保留も Holm の順位から外す', p348)


# ============================================================ P349 D126 ====
def p349():
    m, fn = mut_record()
    hit, caught = mut_caught(m, 'セッション')
    g ='load_sessions' in S('gate_B.py') and 'load_sessions' in S('analyze_B.py')
    return (OK_B if (caught and g) else NG), '門と集計器が読む %s・変異「セッション記録の検査を本走行だけに戻す」を捕まえた %s（`%s`）' % (g, caught, fn)
check('P349', 'K142', 'D126', 'セッション記録の検査を全相と門に広げる', p349)


# ============================================================ P350 D127 ====
def p350():
    src = S('control_chart_B.py')
    judge_line = [l.strip() for l in src.split('\n') if l.strip().startswith('out = ')]
    uses_p = any('pval' in l or 'p <' in l for l in judge_line)
    if not uses_p:
        return NG, '管理図の判定は `%s` だけで、**厳密検定の p 値を判定に使わない**（正本は「二標本・両側・厳密」）' % (judge_line[:1] or ['?'])[0]
    return OK_B, '管理図の判定: `%s`' % judge_line[0]
check('P350', 'K143', 'D127', '管理図の判定を「差が帯を超え、かつ厳密検定が有意」にする', p350)


# ============================================================ P351〜 D128（文） ====
RD = T.get('reading_D128') or {}
def d128(key, want_word=None):
    def f():
        v = RD.get(key)
        bound = ('{{reading_D128/%s}}' % key) in open(os.path.join(REPO, 'design', 'design-stageB-draft12.src.md'), encoding='utf-8').read()
        ok = bool(v) and bound and (want_word is None or want_word in v)
        return (OK_T if ok else NG), '正本 `reading_D128.%s` %s・草案の束縛 %s' % (key, '有り' if v else '**無し**', '有り' if bound else '**無し**')
    return f
check('P351', 'K144', 'D128', '読み条項: Nk の効果は規格化した強さでのもの', d128('nk_normalised'))


def p352():
    f1 = d128('power_in_lead')()
    tpl = open(os.path.join(REPO, 'records', 'B', 'results-report-template-B.src.md'), encoding='utf-8').read()
    sec = lambda a_, b_: tpl.split(a_)[1].split(b_)[0] if a_ in tpl else ''
    lead = '見落とし' in sec('## 0.', '## 1.')
    lim = '見落とし' in sec('## 8.', '## 9.')
    if f1[0] != OK_T:
        return f1
    return (OK_T if (lead and lim) else NG), f1[1] + '・報告の雛形の冒頭（§0）に %s・限界（§8）に %s' % ('有り' if lead else '**無し**', '有り' if lim else '**無し**')
check('P352', 'K145', 'D128', '報告の冒頭の定型と限界の欄に、見落としの割合そのものを置く', p352)


def p353():
    return (OK_T if T['quality_floor']['base_min'] == 0.85 else NG), '正本 `quality_floor.base_min` = %s' % T['quality_floor']['base_min']
check('P353', 'K146', 'D129', '品質床の正答率の下限を引き上げる', p353)


def p354():
    f1 = d128('vhat_from_floor_pair')()
    s0 = DRAFT.split('## 1.')[0]
    in0 = '床' in s0 and ('v̂' in s0 or '抽出元' in s0)
    seal = 'floor' in json.dumps(T.get('seal_format'), ensure_ascii=False) or '床' in json.dumps(T.get('seal_format'), ensure_ascii=False)
    if f1[0] != OK_T:
        return f1
    return (OK_T if (in0 and seal) else NG), f1[1] + '・草案 §0 に %s・封印の情報状態の欄に %s' % ('有り' if in0 else '**無し**', '有り' if seal else '**無し**')
check('P354', 'K147', 'D128', 'v̂ の抽出元が床であることを §0 と封印の情報状態に書く', p354)


def p355():
    rule = (T['random_control'].get('homogeneity_rule') or '')
    if 'homogeneity' not in S('rules_B.py'):
        return NG, '正本に閾値と札の文はある。**判定する器が無い**（集計器・規則の器に実装が零件）'
    r = rules()
    thr = T['random_control']['homogeneity_max_spread_pt']
    lo = r.homogeneity([(20, 100), (22, 100), (24, 100)], T)
    hi = r.homogeneity([(10, 100), (22, 100), (40, 100)], T)
    edge = r.homogeneity([(10, 100), (10 + int(thr), 100), (12, 100)], T)
    if not (lo['note'] is False and hi['note'] is True and edge['note'] is False):
        return NG, '三つの枝（内側・外側・境目ちょうど）が再現しない: %s / %s / %s' % (lo, hi, edge)
    if not callers('homogeneity', ['analyze_B.py']):
        return NG, '規則の関数はあるが、**集計器が呼んでいない**'
    return OK_B, '差 %g pt 超で注・境目ちょうどは注にしない（三つの枝を当てた）。集計器が呼ぶ' % thr
check('P355', 'K148', 'D127', '三方向の等質性の閾値と、崩れたときの札', p355)


def p356():
    src = S('direction_B.py')
    ok = 'h_norm_main' in src and 'h_norm' in json.dumps(T.get('activation_storage'), ensure_ascii=False) + json.dumps(T.get('selection'), ensure_ascii=False)
    return (OK_W if ok else NG), ('抽出器が主位置の ‖h‖ と ‖v̂‖／‖h‖ を層ごとに記帳する' if ok else
                                  '‖v̂‖／帯の位置の ‖h‖ を層ごとに**記帳する器も条も無い**')
check('P356', 'K149', 'D127', '‖v̂‖／‖h‖ を層ごとに記帳し、調整走行の前に登録者に見せる', p356)


def p357():
    c = callers('recorded_seed')
    ok = any(x.startswith('run_stageB_local.py') for x in c) and any(x.startswith('integrity_B.py') for x in c) and any(x.startswith('synth_B.py') for x in c)
    _f = T['seeds'].get('derivation_formula', '')
    # 新しい式があるかで見る（正本は履歴として古い式を引用するので、古い文の有無では誤って反応する・直す前の走行の後に改めた）
    stale = not ('試行の記録に書く種は、その試行が属するバッチの種' in _f and 'retry_seed' in _f)
    if not ok:
        return NG, '書く側と検べる側が同じ関数を呼んでいない: %s' % c
    if stale:
        return NG, '器は「バッチの種」を書き、整合検査も同じ関数で組み直す。**しかし正本 `seeds.derivation_formula` は「試行の種」のまま**'
    return OK_B, '書く側（走行器・合成）と検べる側（整合検査）が `runs_B.recorded_seed` を呼ぶ。正本の式もバッチの種'
check('P357', 'K150', 'D127', '種の単位をバッチにし、試行単位の再現は主張しない', p357)


def p358():
    ge = T['runner'].get('generation_explicit') or {}
    ok = bool(ge) and 'not_applicable' in ge and 'generation_explicit' in S('run_stageB_local.py')
    return (OK_W if ok else NG), '正本 `runner.generation_explicit` を走行器が明示で渡す（受け取らない鍵は not_applicable）'
check('P358', 'K151', 'D127', '標本化の設定を正本に登録し、明示で渡す', p358)
add('P359', 'K152', 'D122', '直しの確認の器を、振る舞いと書き換えの照合に分ける', OK_W,
    '前の巡の器（`verify_fixes_B_recheck.py`）は記録として残し、**この器で置き換えた**——判定を「振る舞い／配線／文」に分け、器の振る舞いの件は文の証拠で直っているにしない')


def p360():
    ok = 'partner_duplicate' in S('gate_B.py') or 'n > items' in S('gate_B.py') or "> T['quality_floor']['items']" in S('gate_B.py')
    return (OK_W if ok else NG), '門が品質床の相手の重複を止める'
check('P360', 'K153', 'D126', '品質床の鍵に走行が二本以上あれば止める', p360)


def p361():
    g = '_gap_tune' in S('gate_B.py')
    if not g:
        return NG, '門が調整走行の升目の欠けを見ない'
    if a.skip_live:
        return NG, '**振る舞いを見ていない**（--skip-live）'
    # **壊した入力で当てる**: 合成データの本走行から、登録された一つの腕の行を消して整合検査を走らせる（直す前の走行の後に強めた）
    d = tempfile.mkdtemp(prefix='audit_p361_')
    try:
        rc, out = run(['tools/synth_B.py', '--case', 'all', '--out-root', d])
        # **どのセッションにも行が残らない腕を消す**。直した後の一回目の走行は、二つのセッションに分けて置いた腕を一方からだけ消し、
        # 残りの行を整合検査が「連番でない」として捕まえた——登録の升目の欠けの検査を当てたことにならなかった（監査の器の誤り・記録に残した）。
        fs = sorted(__import__('glob').glob(os.path.join(d, 'stageB', '*', 'trials-*.jsonl')))
        by_f = {f_: [json.loads(l) for l in open(f_, encoding='utf-8') if l.strip()] for f_ in fs}
        arm_files = {}
        for f_, rows_ in by_f.items():
            for r_ in rows_:
                arm_files.setdefault((r_['scenario'], r_['arm']), set()).add(f_)
        sc_d, drop = next(k for k, v in sorted(arm_files.items()) if len(v) == 1)
        for f_, rows_ in by_f.items():
            open(f_, 'w', encoding='utf-8', newline='\n').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows_
                                                                       if not (r['scenario'] == sc_d and r['arm'] == drop)))
        rc, out = run(['tools/integrity_B.py', '--tag', 'stageB', '--root', d, '--allow-dry', '--out', os.path.join(d, 'i.md'), '--force'])
        probs = json.load(open(os.path.join(d, 'i.json'), encoding='utf-8')).get('problems', [])
    finally:
        shutil.rmtree(d, ignore_errors=True)
    hit = [p for p in probs if '登録の升目' in p]
    return (OK_B if hit else NG), ('腕 %s の行を消すと、整合検査が「%s」と止める' % (drop, hit[0][:60]) if hit else '腕 %s の行を消しても、整合検査が欠けを言わない' % drop)
check('P361', 'K154', 'D126', '相ごとに登録の升目を列挙し、欠けを不整合にする', p361)


def p362():
    mf = T['runner'].get('manifest_fields') or {}
    common = mf.get('common', [])
    need = [k for k in ('dtype', 'order', 'transformers_version') if k not in common]
    if need:
        return NG, 'manifest の共通の欄に **%s が無い**（版・dtype・並べ方を欄に入れる直しが入っていない）' % '・'.join(need)
    return OK_W, 'manifest の共通の欄に dtype・並べ方・transformers の版がある'
check('P362', 'K155', 'D126', '版・dtype・並べ方を manifest の欄に入れ、空を不整合にする', p362)


def p363():
    ok = "r.get('choice') not in (None, 'refuse') and r['catastrophe'] is None" in S('runs_B.py')
    return (OK_W if ok else NG), '選択があるのに破局の判定が空の試行を採点欠落に数える'
check('P363', 'K156', 'D126', '「choice が refuse でも空でもないなら catastrophe は真か偽」を確かめる', p363)
check('P364', 'K157', 'D128', '読み条項: 反証は (6b) についてのもの', d128('falsification_scope'))
check('P365', 'K158', 'D128', '読み条項: 減算族は部分的な除去の検定', d128('partial_removal'))


def p366():
    q = T['quality_floor']
    named = bool(q.get('denominator_name'))
    if 'api_error_gate' not in S('rules_B.py'):
        return NG, '分母の名は正本に置いた（%s）。**api_error の差の門を判定する器が無い**（門は api_error を列に出すだけ）' % named
    r = rules()
    thr = q['api_error_gate_pt']
    hold = r.api_error_gate({'n': 100, 'api_error': 20}, {'n': 100, 'api_error': 5}, T)
    keep = r.api_error_gate({'n': 100, 'api_error': 5}, {'n': 100, 'api_error': 5}, T)
    edge = r.api_error_gate({'n': 100, 'api_error': 5 + int(thr)}, {'n': 100, 'api_error': 5}, T)
    if not (hold is True and keep is False and edge is False):
        return NG, '三つの枝が再現しない: %s / %s / %s' % (hold, keep, edge)
    if not callers('api_error_gate', ['gate_B.py']):
        return NG, '規則の関数はあるが、**門が呼んでいない**'
    return OK_B, 'api_error の率の差が %g pt 超のセルは品質床を判定しない（三つの枝を当てた）。門が呼ぶ' % thr
check('P366', 'K159', 'D127', '品質床の分母の名を改め、api_error の差に門を置く', p366)


def p367():
    src = S('analyze_B.py')
    if "aa, ab = na - A['refuse'], nb - B['refuse']" in src and 'refuse_gate' not in src:
        return NG, 'refuse 門の「答えた分母」は `na - A[\'refuse\']` で、**書式外を含んだまま**'
    r = rules()
    A = {'cat': 20, 'n_ok': 200, 'refuse': 10, 'ff': 60}
    B = {'cat': 50, 'n_ok': 200, 'refuse': 10, 'ff': 2}
    g = r.refuse_gate(A, B, T)
    ok = g['readable']['n_A'] == 200 - 10 - 60 and g['readable']['n_B'] == 200 - 10 - 2
    if not ok:
        return NG, '読めた分母が n_ok − refuse − 書式外 になっていない: %s' % g.get('readable')
    if not callers('refuse_gate', ['analyze_B.py']):
        return NG, '規則の関数はあるが、**集計器が呼んでいない**'
    return OK_B, '答えた分母（n_ok − refuse）と読めた分母（さらに書式外を除く）の両方で当てる。集計器が呼ぶ'
check('P367', 'K160', 'D127', 'refuse 門を、読めた分母（書式外も除く）でも当てる', p367)


def p368():
    src = S('analyze_B.py')
    if "same = (d2 > 0) == (row['diff_pt'] > 0)" in src:
        return NG, '同方向の判定は `(d2 > 0) == (diff > 0)` のままで、答えた分母の差が零のとき**偽どうしで同方向と誤判定**する'
    r = rules()
    ok = r.same_direction(0.0, -0.1) is False and r.same_direction(-0.2, -0.1) is True and r.same_direction(0.2, -0.1) is False
    return (OK_B if ok else NG), '符号の積で決める（零は同方向にしない・三つの枝を当てた）'
check('P368', 'K161', 'D130', '同方向の判定を符号の積で書き直す', p368)


def p369():
    src = S('sample_inspection_B.py')
    ok = 'by_cell' in src and 'セッションを跨いで' in src
    return (OK_W if ok else NG), ('抽出検査はセル（場面 × 腕）で束ねてから引く' if ok else
                                  '抽出検査は**走行ごと × 腕**でセルを作る——セッションに分かれたセルは、その数に比例して高い確率で引かれる')
check('P369', 'K162', 'D130', 'セル単位に束ねてから標本を引く', p369)


def p370():
    rec = sorted(f for f in os.listdir(os.path.join(REPO, 'records', 'B')) if f.startswith('dry-run-B-'))[-1]
    txt = open(os.path.join(REPO, 'records', 'B', rec), encoding='utf-8').read()
    ok = '上がった（封印は当たり）' in txt
    return (OK_B if ok else NG), '合成データによる検査の記録 `%s` に S4 の「上がった」の経路 %s' % (rec, '有り' if ok else '**無し**')
check('P370', 'K163', 'D130', '経路の表に S4 の「上がった」を足す', p370)


def p371():
    ok = '七腕' in json.dumps(T['identity_screen'], ensure_ascii=False)
    return (OK_T if ok else NG), '正本に「B の八腕のうち選別で比べたのは七腕」と印字する'
check('P371', 'K164', 'D130', '同一性選別の腕の数を正しく印字する', p371)
add('P371', 'K164', 'D130', 'Osec-Ncold を選別の比較に足すか', WAIT, '正本 `identity_screen.b_panel_arms_compared`: 「足すか、七腕である旨を印字するかを凍結の前に決める」')


def p372():
    bad = []
    head = DRAFT.split('\n## 0.')[0]
    status_line = next((l for l in head.split('\n') if l.startswith('- 状態:')), '')
    if '草案12B' not in status_line or '草案10B' in status_line:
        bad.append('状態の行が古い（「%s」）' % status_line[6:30])
    if 'boot_stageB' in DRAFT:
        bad.append('実在しない器 `boot_stageB.py` の名がある')
    if '二体に見せ（裁定 D100）' in head:
        bad.append('次の段取りが裁定 D100 のころのまま')
    return (NG if bad else OK_T), ('・'.join(bad) if bad else '前書き・器の名・次の段取りは現在の状態に合う')
check('P372', 'K165', 'D130', '草案の組み立ての傷（前書き・重複・句点・実在しない器の名）', p372)


def p373():
    src = S('design_facts_B.py')
    ok = 'paired' in src or '対の見方' in src
    return (OK_B if ok else NG), ('転記行 E は対の比較（不一致の割合ごと）でも出す' if ok else
                                 '転記行 E は二標本の値だけで、「対にして読むより保守側」と**注を足しただけ**（出し直していない）')
check('P373', 'K166', 'D130', '転記行 E を対の比較で出し直す', p373)


def p374():
    ok = '降格した対比も順位に含める' not in S('analyze_B.py')
    return (OK_T if ok else NG), 'Holm の段の古い注釈 %s' % ('は無い' if ok else 'が残る')
check('P374', 'K167', 'D130', '古い注釈を消す', p374)
check('P375', 'K168', 'D128', '読み条項を Nk−N と td にも及ぼす', d128('td_not_clean'))


def p376():
    # 数の走査器 numbers_lint.py は**段階 A の凍結した器**なので、検査は B の組み立て器 build_draftB.py に置いた（直す前の走行の後に見方を改めた）
    if 'LED' not in S('build_draftB.py'):
        return NG, '草案の組み立て器に「台帳に無い裁定番号を止める」検査が無い'
    if a.skip_live:
        return NG, '**振る舞いを見ていない**（--skip-live）'
    d = tempfile.mkdtemp(prefix='audit_p376_')
    try:
        src = os.path.join(d, 'x.src.md')
        open(src, 'w', encoding='utf-8', newline='\n').write('# 見本\n\n裁定 D9999 を引く。\n')
        rc, out = run(['tools/build_draftB.py', '--kind', 'template', '--src', src, '--out', os.path.join(d, 'x.md'),
                       '--label', '見本', '--lint-report', os.path.join(d, 'l.md')])
    finally:
        shutil.rmtree(d, ignore_errors=True)
    stopped = rc != 0 and '台帳' in out
    return (OK_B if stopped else NG), ('台帳に無い番号を引く原稿で組み立て器が止まる' if stopped else '台帳に無い番号を引いても組み立て器が止まらない（%s）' % out[-80:])
check('P376', 'K169', 'D130', '裁定の台帳を埋め、台帳に無い裁定番号を止める検査を足す', p376)


def p377():
    order = T['gate_order']['order']
    has = any('測れなかった' in x for x in order)
    reads = "T['gate_order']['order']" in S('analyze_B.py') or 'gate_order(' in S('analyze_B.py')
    if not (has and reads):
        return NG, '正本の並びに「測れなかった」%s・集計器が正本の並びを読む %s（いまは手書きの並び）' % ('有り' if has else '**無し**', reads)
    return OK_W, '正本の並びに「測れなかった」があり、集計器は正本の並びを読む'
check('P377', 'K170', 'D130', '門の並びを正本から読む・「測れなかった」を足す', p377)


def p378():
    rule = T['seeds'].get('cell_index_rule', '')
    ok = '混合基数' in rule or '逃げ道' in rule or 'cell_index' in rule
    return (OK_T if ok else NG), ('正本がセルの番号の式（混合基数と逃げ道）を書く' if ok else
                                 '正本は「登録順の添字」とだけ書き、器の**混合基数と +997 の逃げ道**を書いていない')
check('P378', 'K171', 'D130', 'セルの番号の式を正本に正確に書く', p378)


def p379():
    src = S('analyze_B.py')
    if 'wald_ci' in src:
        return NG, '札は厳密検定、印字の区間は **Wald** のまま（食い違いうる旨の印字も無い）'
    return OK_B, '区間は Newcombe に揃え、札（厳密検定）と区間が食い違いうる旨を印字する'
check('P379', 'K172', 'D130', '区間を揃えるか、食い違いうる旨を印字する', p379)


def p380():
    ok = '_bad_arms' in S('analyze_B.py')
    return (OK_W if ok else NG), '管理図の注は、異常のあった腕を含む対比だけに付ける'
check('P380', 'K173', 'D130', '管理図の注を、異常のあった走行を含む対比だけに付ける', p380)


def p381():
    src = S('analyze_B.py')
    ok = '--allow-not-open' in src and '--allow-unbound' in src
    return (OK_W if ok else NG), '検査用の口は門の判定（--allow-not-open）と束縛（--allow-unbound）で分かれている'
check('P381', 'K174', 'D130', '検査用の口を、門の判定と束縛で分ける', p381)


def p382():
    ok = bool(T['selection'].get('batch_composition'))
    return (OK_T if ok else NG), '正本 `selection.batch_composition` に登録した'
check('P382', 'K175', 'D124', 'バッチの組み方を正本に登録する', p382)


# ============================================================ 束の前の点検で見つけた穴 ====
def x1():
    src = S('run_stageB_local.py')
    ok = 'direction_of' in src and 'random_directions' in src
    return (OK_W if ok else NG), ('走行器がランダム方向を試行ごとに割り当て、行ごとの方向で掛ける' if ok else
                                 '走行器は `dirs[(kind, 層)]` を引くだけで、**ランダム方向（三本・試行ごとの割り当て）の処理が無い**——呼ぶと鍵が無くて止まる')
check('X1', '—', 'D117', 'ランダム方向の腕を走らせる', x1)


def x2():
    src = S('run_stageB_local.py')
    bad = [f for f in ('style_a=None', 'style_b=None', 'mention=None', 'loop_flag=False', 'truncated=False', 'refuse_class=None') if f in src]
    return (NG if bad else OK_W), ('走行器が次を固定の空で書く: %s——集計器は空を「該当なし」と数えるので、**様式門は実データでは黙って効かない**' % '・'.join(bad)
                                   if bad else '走行器は段階 A の凍結した関数で様式・言及・ループ・打ち切り・refuse の分類を書く')
check('X2', '—', 'D117', '様式 (a)(b)・言及・ループ・打ち切り・refuse の分類を書く', x2)


def x3():
    src = S('run_stageB_local.py')
    ok = "'raws'" in src or 'raws_out' in src
    return (OK_W if ok else NG), ('走行器が生テキストを返し、置き場に書く' if ok else '走行器は生テキストを作るが**返さない**——raw の置き場の本文が空になる')
check('X3', '—', 'D117', '生テキストを保存する', x3)


def x4():
    tr = T['trial_record']
    ll = any('対数尤度' in x for x in tr)
    store = 'resp_mean' in S('run_stageB_local.py') and 'capture_resp_mean' in S('run_stageB_local.py')
    reg = bool((T['descriptive_families'].get('B_desc_layer') or {}).get('definition_D132'))
    if ll or not store or not reg:
        return NG, '対数尤度が試行の記録に残る %s・副位置の保存 %s・読み方の登録 %s' % (ll, store, reg)
    return OK_W, '対数尤度は在庫へ降ろした。副位置は走行器が保存し、読み方は正本に登録した（裁定 D132）'
check('X4', '—', 'D132', '副位置の保存と読み方の登録・対数尤度を在庫へ', x4)


def x5():
    bad = []
    if '検出力が足りないときは「**当否を言わない**」' in DRAFT or '区間が零を含み、かつ検出力が足りないとき' in DRAFT:
        bad.append('§1 の S4 が検出力の規則のまま')
    if '場面本文の開始位置から EOS まで' in DRAFT:
        bad.append('§2.3 の帯の起点が古い')
    if '「場面の本文」の開始位置である' in DRAFT:
        bad.append('§2.8 の帯の起点が古い')
    if 'そのため順位からは外さない' in DRAFT:
        bad.append('§2.4 の様式門と Holm が裁定 D125 と逆')
    if '**まだ決めていないこと**（器材の段で埋め' in DRAFT:
        bad.append('§2.5 の「まだ決めていないこと」に裁定 D120 で決めた欄が残る')
    if '走行器の本体（バッチ生成の繰り返し・再開・記録の書き出し）は骨組みである' in DRAFT:
        bad.append('§7 の検分票が「走行器の本体は骨組み」のまま')
    return (NG if bad else OK_T), ('・'.join(bad) if bad else '草案に、後の裁定で取って代わられた文は見当たらない（この器が探した六つの型について）')
check('X5', '—', 'D130', '草案の古い記述（後の裁定で取って代わられた文）', x5)


# ============================================================ 直している途中で見つけた件（監査の後） ====
def x6():
    if a.skip_live:
        return NG, '**振る舞いを見ていない**（--skip-live）'
    fs = sorted(f for f in os.listdir(os.path.join(REPO, 'records', 'B')) if f.startswith('dry-run-B-') and f.endswith('.md'))
    txt = open(os.path.join(REPO, 'records', 'B', fs[-1]), encoding='utf-8').read()
    line = [l for l in txt.split('\n') if l.startswith('| 報告の組み立て（全区画・走査器）')]
    ok = bool(line) and '発火せず' not in line[0]
    return (OK_B if ok else NG), '合成データによる検査の記録 `%s` で、報告の組み立て（全区画・段階 A の走査器）の経路 %s' % (fs[-1], '発火' if ok else '**不発**')
check('X6', '—', 'D112', '報告の組み立てが一度も走らず、走査器の口が通らなかった（監査の後に見つけた）', x6)


def x7():
    ok = 'main_position_activations.npz' in S('direction_B.py') and 'activations_npz_sha256' in S('direction_B.py')
    return (OK_W if ok else NG), ('抽出器が主位置の活性そのもの（二度分）を保存し、SHA を記帳する' if ok else '抽出器は方向だけを保存し、活性を残さない')
check('X7', '—', 'D91', '抽出器が主位置の活性を保存していなかった（監査の後に見つけた）', x7)


def x8():
    fs = sorted(f for f in os.listdir(os.path.join(REPO, 'records', 'B')) if f.startswith('dry-run-B-') and f.endswith('.md'))
    txt = open(os.path.join(REPO, 'records', 'B', fs[-1]), encoding='utf-8').read()
    want = ('管理図: 帯の外かつ有意', '管理図: 帯の外だが有意でない', '管理図: 帯の内側', '管理図の注が対比に付く')
    rows = {w: [l for l in txt.split('\n') if l.startswith('| ' + w)] for w in want}
    ok = all(v and '発火せず' not in v[0] for v in rows.values())
    return (OK_B if ok else NG), '管理図の四つの経路: %s' % '・'.join('%s %s' % (w, '発火' if (v and '発火せず' not in v[0]) else '**不発**') for w, v in rows.items())
check('X8', '—', 'D110', '合成データによる検査に管理図の経路が一つも無かった（監査の後に見つけた）', x8)


def x9():
    ok = "OP4B_REQUIRE_FULL_SELFTEST='1'" in S('mutation_B.py')
    return (OK_W if ok else NG), ('変異の器は飛ばしを失敗に倒して自己検査を走らせる（置き場が無ければ最初に止まる）' if ok else
                                  '変異の器は、自己検査が「飛ばした」で通るのを「守りが無い」と誤って記録しうる')
check('X9', '—', 'D122', '変異の器が、実トークナイザの置き場が無いとき誤った結果を出した（監査の後に見つけた）', x9)


def x10():
    F = json.load(open(os.path.join(REPO, 'records', 'B', 'design-facts-B.json'), encoding='utf-8'))['facts']
    n = F['I']['data']['prompt_vectors']
    want = len(T['arms']['panel']) * len(T['extraction_scenarios']) * len(T['selection']['candidates']['layers'])
    return (OK_B if n == want else NG), '転記行 I の主位置の本数 %d（前置きの腕 × 抽出場面 × 候補の層 ＝ %d）' % (n, want)
check('X10', '—', 'D130', '転記行 I が主位置の本数を全場面で数えていた（監査の後に見つけた）', x10)


# ============================================================ 出力 ====
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
cnt = {}
for r in R:
    cnt[r['status']] = cnt.get(r['status'], 0) + 1
L = ['# 段階 B 系統の外への検分の直しの監査（**%s**・%s 日本時間）' % ('直す前' if a.label == 'before' else '直した後', jst.strftime('%Y-%m-%d %H:%M')), '',
     '- 器: `verify_fixes_B_external.py`（枠は `preregistration-fix-audit-B-external.md`・**監査の前に登録した**）。',
     '- 正本 SHA16 %s・草案12B SHA16 %s。' % (
         __import__('hashlib').sha256(open(os.path.join(REPO, 'design', 'contrasts-B.json'), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper(),
         __import__('hashlib').sha256(open(DRAFT_PATH, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()),
     '- 数: ' + '・'.join('%s %d' % (k, cnt.get(k, 0)) for k in (OK_B, OK_W, OK_T, NG, WAIT)) + '（全 %d 行）。' % len(R), '',
     '| P | K | 裁定 | 何を | 判定 | 証拠 |', '|---|---|---|---|---|---|']
for r in R:
    st = ('**%s**' % r['status']) if r['status'] == NG else r['status']
    L.append('| %s | %s | %s | %s | %s | %s |' % (r['P'], r['K'], r['D'], r['what'], st, r['evidence'].replace('|', '／')))
L += ['', '## 直す前の走行の後に変えた検査（基準は動かしていない）', '',
      '- P357: 古い式の文の有無で見ていたのを、新しい式が正本にあるかで見る形に改めた（正本は履歴として古い式を引用するので、古い文の有無では誤って反応する）。',
      '- P361・P376: 文の有無で見ていたのを、壊した入力で器を走らせて止まるかで見る形に強めた。P376 は、数の走査器が段階 A の凍結した器なので、検査を B の組み立て器に置いたことに合わせた。',
      '- X6〜X10: 直している途中で見つけた件を行として足した。',
      '- 直す前の走行の一回目と二回目は、**監査の器の誤り**（変異の記録の鍵の取り違え）で四件と二件を誤って「直っていない」とした。どちらの出力も別名で残した。',
      '- **直した後の走行の一回目も、監査の器の誤り**で P361 を誤って「直っていない」とした（二つのセッションに分けて置いた腕を一方からだけ消した）。出力を別名で残し、どのセッションにも行が残らない腕を消す形に直した。', '',
      '## この監査が確認していないこと', '',
      '- 監査の器そのものの正しさ。器が欠陥を見落とす形で書かれている可能性は、この表では確かめていない（直した件の変異を `tools/mutation_B.py` に足して一部だけ確かめる）。',
      '- 「配線」「文」の判定は、呼び手の有無や鍵の有無を見たもので、**振る舞いの正しさまでは見ていない**。',
      '- 採否表の外の欠陥（誰も挙げていない型）。**最後の系統外の巡に委ねる。**',
      '- 実機（GPU・実重み）では一行も走らせていない。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
json.dump({'kind': 'verify_fixes_B_external', 'label': a.label, 'generated_utc': now.strftime('%Y-%m-%d %H:%M'), 'counts': cnt, 'rows': R},
          open(os.path.splitext(OUT)[0] + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('[verify_fixes_B_external] %s | %s' % (OUT, '・'.join('%s %d' % (k, cnt.get(k, 0)) for k in (OK_B, OK_W, OK_T, NG, WAIT))))
for r in R:
    if r['status'] == NG:
        print('  %-5s %-5s %s' % (r['P'], r['D'], r['what']))
