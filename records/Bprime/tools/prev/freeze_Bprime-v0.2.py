# -*- coding: utf-8 -*-
"""freeze_Bprime.py v0.2 —— B′ の凍結の記帳（正本 `computation.main_freeze`・`predictions.when`・`computation.pre_freeze_checks`・草案10 §4.6・§12・
層三の `tools/freeze_Bl3.py` v4 の型・2026-09-30・コーディネータ南無弥勒如来）。

相:
  prefreeze  下見の前の凍結（封印の前）。確かめてから記帳する（外れたら止める・登録者に相談）:
    - 凍結の本文: `make_frozen_Bprime.py --check`（組み直しが凍結の本文と同じ）と、数の検査の記録の未登録が零。
    - 正本: `decisions` に裁定の記録（`records/Bprime/rulings-D*.md`）の番号がすべてあり、`numbering.rulings_next` がその次の番号。
      `inputs.files_public` の SHA16 が公開の置き場のファイルと同じ。`inputs.files_internal`（移した後は `inputs.files_bprime`）の SHA16 が、
      移し方の表（`bprime_publish_map`）で引いたファイルと同じ。
    - 転記行の記録（凍結の前の行）の正本と台帳の SHA16 が今と同じ。意味のない列の記録がある。重みの断片の目録（K9）に索引の断片がすべてある。
    - 等方の乱数 g: 凍結の関数と同じ引き方で手元で引き（`bprime_directions.iso_g`・次元は正本 `inputs.model_facts.hidden_size`）、SHA-256 を Colab の確かめの g と照らす。
    - 合成データの正式の記録（`records/Bprime/dry-run-Bprime-*.md` の最新）: 確かめがすべて期待どおりで、版の SHA16 の表が器の閉包と正本を覆い、今の版と同じ。
      三の部の四つの行（別の個体の二つの器の --selftest と --dry）が名で在り、期待どおり（二つの器の自己検査はここで代える・U06）。
    - 器の自己検査（`SELFTESTS`・移す器は例だけの閉じた検査・別の個体の二つの器は合成データの記録で代える）がすべて通る。予想の書式が組めて正本の版が同じ。封印はまだ無い（正本 `predictions.when`）。
    - Colab の相 check の出力（session.json と check.json）: DRY でない・すべての項目が通った・GPU が正本の GPU・版が正本 `inputs.versions` と文字列で同じ・
      重みの SHA-256 が目録と同じ・取り出したコミットの正本と器の SHA16 が今と同じ・g が手元と同じ。
    - 器の実装の検分の採否表がある（`records/reviews/Bprime/impl/adoption-table-*.md`・正本 `review_plan.impl`）。封印の前の露出の記録がある。
    - 器の閉包は、閉包の始めの器（`TOOLS`）がすべて見つかる形で取る（見つからなければ止める・置き場の取り違えを止める・U01）。器の SHA16 は閉包で取る（起動器と同じ関数・U08）。
    記帳: `records/Bprime/FREEZE-RECORD-Bprime.json`・`.md`（凍結物の SHA16・器の閉包・`prefreeze` の値〔g・k と z₀・注意の実装・決定性の設定・版のピン・行動の下見の生成のバッチ〕・確かめ）
    と、全体の台帳（`records/FREEZE-RECORD.md`）の一行。Colab の確かめの出力は `records/Bprime/colab-check-Bprime-session.json`・`colab-check-Bprime.json` に写す。
  main  本の凍結（決め〔機械〕の後・本の計算の前・T12）。確かめ（正本 `computation.main_freeze.checks` の八つ・v0.2 で七つ目と八つ目の形を直した）:
    - 正本の SHA16 が下見の前の凍結と同じ。凍結物の SHA16 の違いが逸脱の台帳の器の差分とつながる（`bl3_core.ledger_chain_bad`）。
    - 読み取りの下見の試み（`--pilot` の置き場の pilot-Bprime.json と session.json）: DRY でない・コミットが凍結と封印と行動の下見の閉じた記録と抽出の記録を含み、
      そのコミットの封印の記録と閉じた記録と抽出の記録が今の記録と同じ・試みの順が終わりの時刻の順・二つ以上なら台帳にやり直しの記帳・最後が器の誤りでない。
    - 凍結した決定木の器（`bl3_core.vi_decision`・`pass_i_ii`・`cells_decision`）を最後の試みの記録に当てて出し直した決定が、記録の決定と一致する。
    - 手元の方向の npz の SHA-256 が、公開した抽出の記録の SHA-256 と同じ。
    - 七つ目: 下見の前の凍結から動かせない器（閉包 − 除く器・`bprime_core.lock_bad`）の SHA16 が下見の前の凍結のまま（台帳に記しても通さない・U03）。
    - 八つ目: 段ごとの起動の記録と出力の SHA の記録の組（名にセッション）がそろい、下見の走行の数が試みの数と同じで、二つ以上の走行には台帳のやり直しの行がある（`bprime_core.runs_bad`・T13・U04）。
    - 足した鍵が正本 `computation.main_freeze.allowed_keys` の一覧の内で、本の凍結の節の実際の鍵と下見の記録の鍵が閉じた一覧の内（`main_freeze_structure_bad`・U11）。凍結の記録のほかの鍵は一字も変えない。
    記帳: 凍結の記録の `main_freeze`（許された鍵の値・下見の試みと最後の記録・凍結物の SHA16・台帳の行の数・登録者の言葉と時刻）と、その節の正準の SHA16（`main_freeze_sha16`・起動器と集計の器が照らす・U10）と、全体の台帳の一行。
用法: python tools/freeze_Bprime.py prefreeze --words "<登録者の逐語>" --when "<日時（日本時間）>" --colab-check <相 check の出力の置き場> [--behavior-batch <数・正本の値と照らす>] ／ prefreeze --check-only
      python tools/freeze_Bprime.py main --words "<登録者の逐語>" --when "<日時（日本時間）>" --pilot <相 pilot の出力の置き場> [<二つ目> …] --npz <手元の方向の npz> ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, ast, glob, json, shutil, hashlib, argparse, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_gemma as G                    # 凍結の器の置き場（公開の置き場の tools）を sys.path に足す
PUBLIC = G.REPO

VERSION = 'v0.2'        # v0.2（2026-09-30・器の実装の検分の後）: 閉包の始めの器が見つからなければ止める（U01）・器の SHA16 を閉包で取る（U08）・自己検査の一覧を直した（U06）・合成データの記録の三の部を名で照らす（U06）・相 check の評価の決定性と k を締めた（U52）・本の凍結の七つ目（U03）と八つ目（U04・U09）・本の凍結の鍵の照らし（U11）・本の凍結の節の SHA16（U10）。前の版は `prev/freeze_Bprime-v0.1.py`／v0.1（2026-09-30・D271）: 行動の下見の生成のバッチの大きさを正本 `behavior_pilot.seeds.batch_size` から取る（与えた値が違えば止める）。前の版は `prev/freeze_Bprime-v0.py`
NL = chr(10)
R_ = lambda *a: os.path.join(ROOT, *a)
FR_JSON = R_('records', 'Bprime', 'FREEZE-RECORD-Bprime.json')
FR_MD = R_('records', 'Bprime', 'FREEZE-RECORD-Bprime.md')
CC_SESSION = R_('records', 'Bprime', 'colab-check-Bprime-session.json')
CC_CHECK = R_('records', 'Bprime', 'colab-check-Bprime.json')
LEDGER_ALL = R_('records', 'FREEZE-RECORD.md')
SEAL = R_('records', 'Bprime', 'sealing-record-Bprime.json')
MANIFEST = R_('records', 'Bprime', 'MANIFEST-gemma-4-31B-it.json')
CLOSED = R_('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json')
EXTRACT = R_('records', 'Bprime', 'extract', 'extraction-record-Bprime.json')
RUNS = R_('records', 'Bprime', 'runs')
EXPOSURE = R_('records', 'Bprime', 'exposure-before-seal-Bprime.md')
TOOLS = ['tools/bprime_gemma.py', 'tools/bprime_core.py', 'tools/bprime_run.py', 'tools/bprime_cells.py', 'tools/bprime_directions.py', 'tools/bprime_behavior.py',
         'tools/bprime_facts.py', 'tools/bprime_meaningless.py', 'tools/bprime_external.py', 'tools/bprime_phases.py', 'tools/bprime_typo.py', 'tools/bprime_publish_map.py',
         'tools/bprime_numbers_lint.py', 'tools/analyze_Bprime.py', 'tools/build_report_Bprime.py', 'tools/sweep_Bprime.py', 'tools/close_behavior_Bprime.py',
         'tools/send_external_Bprime.py', 'tools/make_predictions_form_Bprime.py', 'tools/seal_Bprime.py', 'tools/make_frozen_Bprime.py', 'tools/freeze_Bprime.py',
         'tools/make_contrasts_Bprime.py', 'tools/colab/boot_bprime.py', 'tools/bprime_recompute_rewrite.py', 'tools/bprime_reextract.py', 'tools/g4_attempts_Bprime.py']
SELFTESTS = [(t, ['--selftest']) for t in ('tools/bprime_core.py', 'tools/bprime_typo.py', 'tools/bprime_directions.py', 'tools/bprime_behavior.py',
                                           'tools/bprime_external.py', 'tools/analyze_Bprime.py', 'tools/build_report_Bprime.py', 'tools/sweep_Bprime.py',
                                           'tools/close_behavior_Bprime.py', 'tools/send_external_Bprime.py', 'tools/make_predictions_form_Bprime.py', 'tools/seal_Bprime.py',
                                           'tools/make_frozen_Bprime.py', 'tools/freeze_Bprime.py', 'tools/g4_attempts_Bprime.py')] + [('tools/bprime_publish_map.py', ['--selftest-examples'])]
# 別の個体の二つの器（`bprime_recompute_rewrite.py`・`bprime_reextract.py`）は、器の置き場から二つ上を作業の置き場とみなす作りで、公開の置き場では自己検査が正本を見つけられない。
# 器の中は変えない決まりなので、自己検査はここで走らせず、合成データの正式の記録の三の部の四つの行（作業の置き場の形で走らせた --selftest と --dry）で代える（U06・R2-12）
INDEPENDENT_ROWS = ('bprime_recompute_rewrite.py --selftest', 'bprime_recompute_rewrite.py --dry', 'bprime_reextract.py --selftest', 'bprime_reextract.py --dry')
MAIN_FREEZE_TOP = ('frozen_jst', 'registrant_words', 'added', 'pilot_attempts', 'pilot', 'decision', 'sessions', 'frozen_sha16', 'tool_diffs_applied', 'seal', 'runs', 'lock',
                   'freeze_tool', 'deviations_n')
PILOT_KEYS = ('version', 'logit_check', 'vi', 'batch', 'floor', 'cells', 'iv', 'decision', 'iii', 'n_forward', 'behavior_state', 'chain', 'variants_used',
              'start_record_sha256', 'session', 'time_utc', 'clause', 'tool_error')
SESSION_KEYS = ('commit', 'gpu', 'versions', 'canon_sha16', 'finished', 'session_id', 'start_end')
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
DEVIATION_RULE = ('凍結の後の変更は、逸脱として番号・日付・理由・登録者の承認を台帳（この記録の deviations）に記す。器の差分は tool_diffs に置き場（path）・前（before）・後（after）の SHA16 を記す'
                  '（同じ置き場を二度直すときは、前の差分の後の SHA16 を次の差分の前に書く・路ごとにつなげて照らす）。下見のやり直しは kind pilot_rerun の行で記す。'
                  '台帳は後ろに足すだけで、前の行を書き換えない（正本 computation.main_freeze・層三の D222・D239 の型）')


def rel(p):
    for base in (ROOT, PUBLIC):
        r = os.path.relpath(p, base).replace(os.sep, '/')
        if not r.startswith('..'):
            return r
    return p.replace(os.sep, '/')


# 作業の置き場では、別の個体の二つの器は `tools/independent/` にある（移し方の表が公開の置き場の `tools/` に写す）。公開の置き場の名で引いたとき、
# 作業の置き場ではその実物を読む（同じバイト・どちらの置き場でも閉包に同じ器が入る・v0.2・U01）
WORKSPACE_ALIAS = {'tools/bprime_recompute_rewrite.py': 'tools/independent/bprime_recompute_rewrite.py', 'tools/bprime_reextract.py': 'tools/independent/bprime_reextract.py'}


def P(r):
    """置き場の道筋 → ファイル（B′ の置き場に無ければ、作業の置き場の読み替え〔WORKSPACE_ALIAS〕、公開の置き場の凍結の器と記録の順に引く）。"""
    a = os.path.join(ROOT, *r.split('/'))
    if os.path.exists(a) or os.path.abspath(ROOT) == os.path.abspath(PUBLIC):
        return a
    if r in WORKSPACE_ALIAS and os.path.exists(os.path.join(ROOT, *WORKSPACE_ALIAS[r].split('/'))):
        return os.path.join(ROOT, *WORKSPACE_ALIAS[r].split('/'))
    b = os.path.join(PUBLIC, *r.split('/'))
    return b if os.path.exists(b) else a


def sha16b(b):
    return hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def sha16f(p):
    with open(p, 'rb') as fh:
        return sha16b(fh.read())


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest().upper()


def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def import_closure(tools, strict=True):
    """器が import する（関数の中の import も含む）手元の器の閉包（B′ の器と公開の置き場の凍結の器）。
    strict: 閉包の始めの器（`tools`）が一つでも見つからなければ止める（v0.2・U01・前は黙って飛ばし、置き場の取り違えで器が閉包から落ちた）。"""
    miss = [t for t in tools if not os.path.exists(P(t))]
    if strict and miss:
        raise SystemExit('閉包の始めの器が置き場に無い（置き場の取り違え・U01）: %s' % miss)
    out, todo = set(), list(tools)
    while todo:
        t = todo.pop()
        if t in out or not os.path.exists(P(t)):
            continue
        out.add(t)
        with open(P(t), encoding='utf-8') as fh:
            tree = ast.parse(fh.read())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split('.')[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = [node.module.split('.')[0]]
            for n in names:
                for cand in ('tools/%s.py' % n, 'tools/colab/%s.py' % n):
                    if os.path.exists(P(cand)) and cand not in out:
                        todo.append(cand)
    return sorted(out)


def frozen_files(C):
    """凍結物（器の閉包を除く）: 正本・凍結の本文と草案・記録・書式・台帳・裁定・器の段の記録・器の実装の検分・読む記録（正本 `inputs.files_public`）。"""
    import make_frozen_Bprime as MFB
    files = ['design/contrasts-Bprime.json', 'design/design-Bprime-FROZEN.md', rel(MFB.SRC), 'records/Bprime/numbers-lint-FROZEN-Bprime.md', 'records/Bprime/frozen-diff-Bprime.md',
             'records/Bprime/facts-Bprime-pre.json', 'records/Bprime/facts-Bprime-pre.md', 'records/Bprime/meaningless-Bprime.json', 'records/Bprime/MANIFEST-gemma-4-31B-it.json',
             'records/predictions/predictions-form-Bprime-v1.html', 'tools/ledger-bprime.json', 'tools/ledger-bprime.md', 'records/Bprime/tools/tools-log-Bprime.md',
             'records/Bprime/tools/independent/instructions-rewrite-reextract-Bprime.txt', 'records/Bprime/tools/independent/rewrite-reextract-dev-Bprime.md',
             'records/Bprime/exposure-before-seal-Bprime.md', 'records/Bprime/publish-map-Bprime.json']          # 移し方の記録（凍結の本文の道筋を引く・正本 v5 `computation.frozen_text.publish_record`・U28）
    files += sorted(rel(p) for p in glob.glob(R_('records', 'Bprime', 'rulings-D*.md')))
    files += sorted(rel(p) for p in glob.glob(R_('records', 'reviews', 'Bprime', 'impl', '*.md')))
    files += [v['path'] for v in C['inputs']['files_public'].values()]
    out = []
    for f in files:
        if f not in out:
            out.append(f)
    return out


IMPL_NOTES = [                                                                  # 器の実装の検分の注（採否の表の注の行・器は変えない所・v0.2）
    ('U33', '相 check の出口の値の自己検査の「なし」「二重」の fail は作りの上で起きえない（見分けに使える行だけに掛ける）。この項目が確かめるのは、「あり」が通ることと、見分けに使える行があること（R1-03・R1-02 の残り）'),
    ('U35', '加減の層には集めるフックを置かない（集めるフックの順の確かめは作りの上で落ちえない・R1-06）'),
    ('U36', '最後の層の自己検査の差は作りの上で零になる（作りの上の一致の確かめ）。層の誤りは、効き目の比べと書き換えの道の歯で捕まる（R1-07）'),
    ('U37', '器は rsqrt、模型は冪で正規化の逆数を取る。差は float32 の刻みほどで許容の内（変えない・二つの道がそろって rsqrt・R1-08）'),
    ('U38', '(iii) の変換の値の元は器の float32 の出口の値で、generate の元（模型の bf16 を float32 にした値）と違う。記述だけの値（R1-10）'),
    ('U39', '凍結の解析器は量の欄の true を整数として通し、系統外への依頼の文は「整数」とだけ書く（一致の記述の注・凍結の器は変えない・R1-11）'),
    ('U47', '本の列は窓より短いので、実の重みの一段目は窓つきの mask の誤りを見ない。窓の誤りは、窓を列より短くした小さな模型の確かめで見る（G-06）'),
    ('U49', 'フックの道は float64、書き換えの道は float32 で logsumexp を取る。道の間でビットの一致は求めない（G-08）'),
]


def z_floor(k, z0, cap, disc, step=0.01):
    """測った k で、softcap の抜けの見込みの差（r − cap·tanh(r/cap)）が許容の disc 倍を超える出口の値（softcap の後）の下限（v0.2・U34・R1-05）。
    z を 0 から step ずつ上げ、初めて超える値を返す（cap に届くまで超えなければ None）。"""
    import math
    import bprime_core as Pc
    z = step
    while z < cap * (1 - 1e-9):
        r = cap * math.atanh(z / cap)
        if r - z > disc * k * float(Pc.u_of(z, z0)):
            return round(z, 2)
        z += step
    return None


def rulings_check(C, ruling_files):
    ruled = set()
    for fp in ruling_files:
        m_ = re.fullmatch(r'rulings-D(\d+)(?:-D(\d+))?\.md', os.path.basename(fp))
        if m_:
            ruled |= {'D%d' % i for i in range(int(m_.group(1)), int(m_.group(2) or m_.group(1)) + 1)}
    miss = sorted(ruled - set(C['decisions']), key=lambda x: int(x[1:]))
    nxt = ('D%d' % (max(int(x[1:]) for x in ruled) + 1)) if ruled else None
    bad = []
    if not ruled or miss:
        bad.append('正本の decisions に、裁定の記録の番号が無い: %s' % miss)
    if C['numbering']['rulings_next'] != nxt:
        bad.append('正本の次の裁定の番号 %s が、裁定の記録の次の番号 %s と違う' % (C['numbering']['rulings_next'], nxt))
    return {'rulings_recorded': len(ruled), 'missing_in_decisions': miss, 'rulings_next': C['numbering']['rulings_next'], 'rulings_next_expected': nxt}, bad


def inputs_check(C):
    """正本の入力のファイルの SHA16 が今と同じか（公開の置き場の凍結物と、B′ の置き場のファイル）。"""
    import bprime_publish_map as PM
    bad_pub = [k for k, v in C['inputs']['files_public'].items() if v.get('sha16') and (not os.path.exists(P(v['path'])) or sha16f(P(v['path'])) != v['sha16'])]
    key = 'files_bprime' if 'files_bprime' in C['inputs'] else 'files_internal'
    bad_bp = []
    for k, v in C['inputs'][key].items():
        pth = v['path']
        if key == 'files_internal':
            inside = os.path.join(ROOT, *pth[len('Bprime/'):].split('/')) if pth.startswith('Bprime/') else None
            pub = PM.public_path(pth)
            cand = [x for x in (inside, P(pub) if pub else None) if x and os.path.exists(x)]
        else:
            cand = [P(pth)] if os.path.exists(P(pth)) else []
        if not cand or sha16f(cand[0]) != v['sha16']:
            bad_bp.append(k)
    return {'public_checked': len(C['inputs']['files_public']), 'public_bad': bad_pub, 'bprime_key': key, 'bprime_checked': len(C['inputs'][key]), 'bprime_bad': bad_bp}, \
        (['正本 inputs.files_public の SHA16 と今のファイルが違う: %s' % bad_pub] if bad_pub else []) + (['正本 inputs.%s の SHA16 と今のファイルが違う: %s' % (key, bad_bp)] if bad_bp else [])


def g_local(C):
    import bprime_directions as BD
    I = C['nulls']['isotropic']
    g = BD.iso_g(I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'], C['inputs']['model_facts']['hidden_size'])
    return BD.g_record(g, I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'])


def dry_record_check(C, closure):
    dr = sorted(glob.glob(R_('records', 'Bprime', 'dry-run-Bprime-*.md')))
    if not dr:
        return None, ['合成データの正式の記録が無い（records/Bprime/dry-run-Bprime-<日付>.md）']
    with open(dr[-1], encoding='utf-8') as fh:
        txt = fh.read()
    m = re.search(r'確かめ: (\d+) のうち (\d+) が期待どおり', txt)
    res = {'path': rel(dr[-1]), 'checks': int(m.group(1)) if m else None, 'as_expected': int(m.group(2)) if m else None}
    bad = []
    if not m or m.group(1) != m.group(2) or '**期待と違う**' in txt:
        bad.append('合成データの正式の記録に期待と違う確かめがある')
    table = dict(re.findall(r'^\| ([^ |]+) \| ([0-9A-F]{16}) \|$', txt, flags=re.M))
    need = set(closure) | {'design/contrasts-Bprime.json', 'tools/ledger-bprime.json'}
    lack = sorted(need - set(table))
    differ = sorted(f for f, s16 in table.items() if not os.path.exists(P(f)) or sha16f(P(f)) != s16)
    res['sha_table'] = {'files': len(table), 'lack': lack, 'differ': differ}
    if lack:
        bad.append('合成データの正式の記録の版の SHA16 の表が、器の閉包と正本と台帳を覆わない: %s' % lack[:10])
    js = dr[-1][:-3] + '.json'
    rows = (load(js).get('rows') or []) if os.path.exists(js) else []
    got3 = {r['name']: bool(r.get('ok')) for r in rows if r.get('group') == '三'}
    miss3 = [n for n in INDEPENDENT_ROWS if not got3.get(n)]
    res['independent_rows'] = {n: got3.get(n) for n in INDEPENDENT_ROWS}
    if miss3:
        bad.append('合成データの正式の記録の三の部に、別の個体の二つの器の行が名で無いか、期待どおりでない（自己検査の代わり・U06）: %s' % miss3)
    if differ:
        bad.append('合成データの正式の記録を取った版と今の版が違う（取り直す）: %s' % differ[:10])
    return res, bad


def _determinism_ok(D):
    """決定性の設定の四つの値（v0.2・U52・前は空でなければ真）: tf32 の二つが偽・float32 の行列の精度が highest・注意の実装がある。"""
    D = D if isinstance(D, dict) else {}
    return D.get('allow_tf32_matmul') is False and D.get('allow_tf32_cudnn') is False and D.get('float32_matmul_precision') == 'highest' and bool(D.get('attn_implementation'))


def _logit_k_ok(it):
    """k の項目（v0.2・U52・前は鍵があるかだけ）: 項目が通った（pass が真）・k が有限の正の数・z₀ が整数。"""
    it = it if isinstance(it, dict) else {}
    k, z0 = it.get('k'), it.get('z0')
    return it.get('pass') is True and isinstance(k, (int, float)) and not isinstance(k, bool) and k == k and 0 < k < float('inf') and isinstance(z0, int) and not isinstance(z0, bool)


def colab_check_eval(C, S, CK, canon16, tool_sha, g_sha, manifest):
    """相 check の出力の確かめ（外れの名の並び）。"""
    V = C['inputs']['versions']
    man_files = (manifest or {}).get('files') or {}
    c = {'kind_check': S.get('kind') == 'bprime_colab_check', 'not_dry': S.get('dry') is False, 'all_pass': CK.get('all_pass') is True,
         'commit': bool(re.fullmatch(r'[0-9a-f]{40}', S.get('commit') or '')), 'gpu': C['inputs']['gpu']['name'] in str(S.get('gpu')),
         'versions': (S.get('versions') or {}).get('transformers') == V['transformers'] and (S.get('versions') or {}).get('torch') == V['torch'],
         'weights': bool(man_files) and {k: v for k, v in (S.get('weights_sha256') or {}).items()} == {k: r['sha256'].upper() for k, r in man_files.items()},
         'canon_at_commit': S.get('canon_sha16') == canon16, 'tools_at_commit': (S.get('tools_sha16') or {}) == tool_sha and bool(tool_sha),
         'g_same': ((CK.get('items') or {}).get('isotropic_g') or {}).get('g', {}).get('g_sha256') == g_sha,
         'logit_k': _logit_k_ok((CK.get('items') or {}).get('logit_tolerance_k')), 'determinism': _determinism_ok(CK.get('determinism'))}
    return c, [k for k, v in c.items() if not v]


def closure_sha_map():
    """器の SHA16 の表（閉包の置き場 → SHA16・起動器の session の `tools_sha16` と同じ関数・v0.2・U08・前は bprime_*.py と起動器だけで凍結の器を含まなかった）。"""
    return {pth: sha16f(P(pth)) for pth in import_closure(TOOLS)}


def prefreeze_checks(colab_dir=None, behavior_batch=None, run_selftests=True):
    import make_frozen_Bprime as MFB
    import make_predictions_form_Bprime as FORM
    C = load(R_('design', 'contrasts-Bprime.json'))
    res, bad = {}, []
    canon16 = sha16f(R_('design', 'contrasts-Bprime.json'))
    # 凍結の本文
    if not os.path.exists(MFB.FOUT):
        bad.append('凍結の本文が無い（make_frozen_Bprime を先に走らせる）')
    else:
        r = subprocess.run([sys.executable, P('tools/make_frozen_Bprime.py'), '--check'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT,
                           env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        res['frozen_text_rebuilt_same'] = r.returncode == 0
        if r.returncode != 0:
            bad.append('凍結の本文を組み直した本文が凍結の本文と違う')
        if not os.path.exists(MFB.LINT) or '未登録 0' not in open(MFB.LINT, encoding='utf-8').read():
            bad.append('凍結の本文の数の検査に未登録がある（または記録が無い）')
    # 正本
    res['canon'] = {'version': C['version'], 'sha16': canon16}
    r_, b_ = rulings_check(C, glob.glob(R_('records', 'Bprime', 'rulings-D*.md')))
    res['rulings'] = r_
    bad += b_
    r_, b_ = inputs_check(C)
    res['inputs'] = r_
    bad += b_
    # 転記行・意味のない列・目録
    FJ = load(R_('records', 'Bprime', 'facts-Bprime-pre.json'))
    if FJ.get('contract_sha16') != canon16 or FJ.get('ledger_sha16') != sha16f(R_('tools', 'ledger-bprime.json')):
        bad.append('転記行の記録の正本か台帳の SHA16 が今と違う（作り直す）')
    if not os.path.exists(R_('records', 'Bprime', 'meaningless-Bprime.json')):
        bad.append('意味のない列の記録が無い')
    manifest = load(MANIFEST) if os.path.exists(MANIFEST) else None
    if not manifest or not (manifest.get('files') or {}):
        bad.append('重みの断片の目録（records/Bprime/MANIFEST-gemma-4-31B-it.json）が無いか、断片が無い（K9）')
    else:
        shards = [k for k in manifest['files'] if k.endswith('.safetensors')]
        idx = manifest.get('index_shards') or []
        res['manifest'] = {'files': len(manifest['files']), 'shards': len(shards), 'index_shards': len(idx)}
        if not idx or sorted(idx) != sorted(shards):
            bad.append('重みの断片の目録の断片が、索引の断片とそろわない')
    if not os.path.exists(EXPOSURE):
        bad.append('封印の前の露出の記録が無い（records/Bprime/exposure-before-seal-Bprime.md・正本 predictions.exposure）')
    # 等方の乱数 g（手元）
    g = g_local(C)
    res['g_local'] = g
    # 合成データ・器の自己検査
    closure = import_closure(TOOLS)
    res['tools_closure_n'] = len(closure)
    res['dry_run'], b_ = dry_record_check(C, closure)
    bad += b_
    if run_selftests:
        st = {}
        for t, args in SELFTESTS:
            if t == 'tools/freeze_Bprime.py':
                continue
            r = subprocess.run([sys.executable, P(t)] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT,
                               env=dict(os.environ, PYTHONIOENCODING='utf-8'))
            st[t] = r.returncode == 0
        res['selftests'] = st
        bad += ['器の自己検査が落ちた: %s' % t for t, v in st.items() if not v]
    # 予想の書式・封印はまだ無い
    if not os.path.exists(FORM.OUT):
        bad.append('予想の書式が無い（make_predictions_form_Bprime を先に走らせる）')
    else:
        h = open(FORM.OUT, encoding='utf-8').read()
        res['form'] = FORM.check(C, h)
        if C['version'] not in h:
            bad.append('予想の書式の正本の版が今の正本と違う（組み直す）')
    for p in (R_('records', 'predictions', 'predictions-Bprime-coordinator.json'), R_('records', 'predictions', 'predictions-Bprime-registrant.json'), SEAL):
        if os.path.exists(p):
            bad.append('封印が凍結より先にある（正本 predictions.when と違う）: %s' % rel(p))
    impl = sorted(glob.glob(R_('records', 'reviews', 'Bprime', 'impl', 'adoption-table-*.md')))
    res['impl_review'] = [rel(x) for x in impl]
    if not impl:
        bad.append('器の実装の検分の採否表が無い（records/reviews/Bprime/impl/・正本 review_plan.impl）')
    # 行動の下見の生成のバッチ（正本 `behavior_pilot.seeds.batch_size`・K11・D271）
    tpc = int(C['behavior_pilot']['trials_per_cell'])
    bsz = int(C['behavior_pilot']['seeds']['batch_size'])
    res['behavior_batch'] = bsz
    if tpc % bsz:
        bad.append('正本の生成のバッチの大きさ %d が升目ごとの試行の数 %d を割り切らない' % (bsz, tpc))
    if behavior_batch is not None and int(behavior_batch) != bsz:
        bad.append('与えた生成のバッチの大きさ %s が正本の値 %d と違う' % (behavior_batch, bsz))
    # Colab の確かめ
    if colab_dir is not None:
        S = load(os.path.join(colab_dir, 'session.json'))
        CK = load(os.path.join(colab_dir, 'check.json'))
        c, fails = colab_check_eval(C, S, CK, canon16, closure_sha_map(), g['g_sha256'], manifest)
        res['colab_check'] = dict(c, commit_seen=S.get('commit'), gpu_name=S.get('gpu'), versions_seen=S.get('versions'))
        bad += ['Colab の確かめ: %s' % k for k in fails]
        res['prefreeze_values'] = {'logit_k': {k: CK['items']['logit_tolerance_k'][k] for k in ('k', 'z0')} if 'logit_k' not in fails else None,
                                   'determinism': CK.get('determinism'), 'attn_implementation': (CK.get('determinism') or {}).get('attn_implementation'),
                                   'pins': {k: v for k, v in (S.get('versions') or {}).items() if v}}
    return C, res, bad


def prefreeze(words, when, colab_dir, behavior_batch, force=False):
    C, res, bad = prefreeze_checks(colab_dir, behavior_batch)
    print(json.dumps({k: v for k, v in res.items() if k not in ('selftests',)}, ensure_ascii=False, indent=1, default=str)[:6000])
    if bad:
        raise SystemExit('下見の前の凍結の確かめが外れた（止める・登録者に相談）: %s' % bad)
    if colab_dir is None:
        print('[freeze_Bprime] 確かめだけ（Colab の確かめを除く）: 外れ無し')
        return
    if os.path.exists(FR_JSON) and not force:
        raise SystemExit('既にある: %s' % rel(FR_JSON))
    shutil.copyfile(os.path.join(colab_dir, 'session.json'), CC_SESSION)
    shutil.copyfile(os.path.join(colab_dir, 'check.json'), CC_CHECK)
    tools = import_closure(TOOLS)
    files = frozen_files(C) + [res['dry_run']['path'], rel(CC_SESSION), rel(CC_CHECK)]
    frozen = {r: sha16f(P(r)) for r in files + tools}
    pv = res['prefreeze_values']
    R = collections.OrderedDict([
        ('kind', 'bprime_freeze_record'), ('version', VERSION), ('stage', 'prefreeze'), ('frozen_jst', when), ('registrant_words', words),
        ('rulings', sorted((k for k in C['decisions'] if int(k[1:]) >= 255), key=lambda x: int(x[1:]))), ('frozen_sha16', frozen), ('tools_import_closure', tools),
        ('prefreeze', collections.OrderedDict([('g', res['g_local']), ('logit_k', pv['logit_k']), ('attn_implementation', pv['attn_implementation']),
                                               ('determinism', pv['determinism']), ('pins', pv['pins']), ('behavior_batch', int(res['behavior_batch'])),
                                               ('manifest_sha16', sha16f(MANIFEST))])),
        ('checks', res), ('deviation_rule', DEVIATION_RULE), ('deviations', []),
        ('next', '記録先行の公開（push）→ 予想の封印（コーディネータが先・SHA だけを伝える → 登録者）→ 相 extract と抽出の記録の公開 → 行動の下見と閉じた記録の公開 → 読み取りの下見 → '
                 '本の凍結 → 本の計算 → 独立の再計算と独立の再抽出 → 一致だけを見る段 → 結果を登録者と一緒に開く'),
        ('clause', CLAUSE)])
    with open(FR_JSON, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(R, fh, ensure_ascii=False, indent=1)
    md = ['# B′ の下見の前の凍結の記録（機械生成・`tools/freeze_Bprime.py` %s）' % VERSION, '',
          '- 凍結: %s（日本時間）・登録者の言葉は逐語で「%s」。' % (when, words),
          '- 本文: `design/design-Bprime-FROZEN.md`（SHA16 %s）・草案との差は `records/Bprime/frozen-diff-Bprime.md`。' % frozen['design/design-Bprime-FROZEN.md'],
          '- 正本: 版 %s（SHA16 %s）。等方の乱数 g: SHA-256 %s（種 %d・本数 %d・次元 %d・NumPy %s）。' % (C['version'], frozen['design/contrasts-Bprime.json'], R['prefreeze']['g']['g_sha256'],
                                                                                 R['prefreeze']['g']['seed'], R['prefreeze']['g']['count'], R['prefreeze']['g']['dim'], R['prefreeze']['g']['numpy']),
          '- Colab の確かめ（相 check・コミット %s・%s）: %s。' % (res['colab_check']['commit_seen'], res['colab_check']['gpu_name'],
                                                             '・'.join('%s %s' % (k, '合う' if v else '外れ') for k, v in res['colab_check'].items() if isinstance(v, bool))),
          '- 下見の前の値: k %s・z₀ %s・注意の実装 %s・行動の下見の生成のバッチ %d。' % (pv['logit_k']['k'], pv['logit_k']['z0'], pv['attn_implementation'], int(res['behavior_batch'])),
          '- 合成データ: `%s`（確かめ %s・期待どおり %s）。' % (res['dry_run']['path'], res['dry_run']['checks'], res['dry_run']['as_expected']),
          '- 次: ' + R['next'], '', '## 器の実装の検分の注（器は変えない所・採否の表の注の行）', '']
    Lg = C['computation']['self_checks']['logit']
    zf = z_floor(float(pv['logit_k']['k']), float(pv['logit_k']['z0']), float(C['inputs']['model_facts']['final_logit_softcapping']), float(Lg['discrimination_factor']))
    md += ['- U34: 測った k（%s・z₀ %s）では、softcap の抜けの見込みの差が許容の %s 倍を超えるのは、出口の値（softcap の後）の大きさが %s 以上の行（R1-05）。'
           % (pv['logit_k']['k'], pv['logit_k']['z0'], Lg['discrimination_factor'], zf if zf is not None else 'cap の内に無い')]
    md += ['- %s: %s。' % kv for kv in IMPL_NOTES]
    md += ['', '## 凍結物の SHA16', '', '| 置き場 | SHA16 |', '|---|---|'] + ['| `%s` | %s |' % kv for kv in sorted(frozen.items())] + ['', CLAUSE, '']
    with open(FR_MD, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(NL.join(md))
    row = ('| %s | **B′ 下見の前の凍結**（登録者「%s」%s 日本時間）: 草案を逐語複製した design/design-Bprime-FROZEN.md と、正本・器・等方の乱数 g の SHA を凍結した。'
           '凍結の記録 records/Bprime/FREEZE-RECORD-Bprime.json（凍結物 %d 件・器の閉包 %d）。封印はこの後（コーディネータが先）。 | design/design-Bprime-FROZEN.md | %s | 凍結の後の変更は逸脱として台帳に記す |'
           % (when.split(' ')[0], words, when, len(frozen), len(tools), frozen['design/design-Bprime-FROZEN.md']))
    led = open(LEDGER_ALL, encoding='utf-8').read() if os.path.exists(LEDGER_ALL) else ''
    if 'B′ 下見の前の凍結' not in led:
        with open(LEDGER_ALL, 'a', encoding='utf-8', newline=NL) as fh:
            fh.write(('' if (not led or led.endswith(NL)) else NL) + row + NL)
    print('[freeze_Bprime] 下見の前の凍結を記帳した: %s・%s（凍結物 %d）' % (rel(FR_JSON), rel(FR_MD), len(frozen)))


# ---------------- 本の凍結 ----------------
def git(*args):
    return subprocess.run(['git', '-C', ROOT] + list(args), capture_output=True)


def in_commit(commit, path):
    return git('cat-file', '-e', '%s:%s' % (commit, path)).returncode == 0


def at_commit_sha16(commit, path):
    r = git('show', '%s:%s' % (commit, path))
    return sha16b(r.stdout) if r.returncode == 0 else None


def decision_rebuild(C, rec):
    """凍結した決定木の器を下見の記録に当てて、決定を出し直す（T12）。戻り値: (出し直した決定の要約, 記録の決定の要約)。"""
    import bl3_core as K
    PL = C['pilot']
    sa = max(float(v) for v in rec['vi']['a'].values())
    sb = max(float(v) for v in rec['vi']['b'].values())
    vi = K.vi_decision(sa, sb, PL['noise_max'], C['readout']['primary']['batch'])
    if vi['stop']:
        mine = {'stop': True, 'reason': 'vi_b', 'q1': '止める'}
        theirs = {k: (rec.get('decision') or {}).get(k) for k in ('stop', 'reason', 'q1')}
        return mine, theirs
    ok = {c: K.pass_i_ii(v['mass'], v['pa'], PL['mass_min'], PL['p_bounds']) for c, v in rec['cells'].items()}
    cd = K.cells_decision(ok, {}, PL['decision']['cells_min_pass'])
    mine = {'batch': vi['batch'], 'floor': vi['floor'], 'pass_i_ii': ok, 'decision': cd}
    theirs = {'batch': rec.get('batch'), 'floor': rec.get('floor'), 'pass_i_ii': {c: v['pass_i_ii'] for c, v in rec['cells'].items()}, 'decision': rec.get('decision')}
    return mine, theirs


def runs_count_bad(stages=('extract', 'behavior', 'pilot'), attempts=None, deviations=None):
    """段ごとの起動の記録と出力の SHA の記録（名にセッション・T13・v0.2・U04・U09）: 芯の `runs_table` と `runs_bad`（報告の側と同じ関数）で照らす。"""
    import bprime_core as Pc_
    names = {fn: sha256f(os.path.join(RUNS, fn)) for fn in (os.listdir(RUNS) if os.path.isdir(RUNS) else []) if fn.endswith('.json')}
    try:
        table = Pc_.runs_table(names)
    except Pc_.ToolError as e_:
        return {'table': None}, ['起動の記録の置き場に決まりの外の名がある（T13）: %s' % e_]
    bad = Pc_.runs_bad(table, stages, attempts or {}, Pc_.reruns_of(deviations))
    return {'table': table}, bad


def main_freeze_content(C, atts, sessions, EX, CL, now_sha, FR, res, when, words):
    last = atts[-1]
    content = collections.OrderedDict([
        ('extraction', collections.OrderedDict([('転記行 D', EX['row_D']), ('npz の SHA', EX['npz_sha256']), ('係数', EX['coefficient']), ('g との一致の合否', EX['g_match'])])),
        ('behavior_pilot', collections.OrderedDict([('採点の器の SHA', CL['digests']['scorer_sha16'] if CL.get('digests') else None),
                                                    ('採点の出力の SHA', CL['digests']['scores_sha256'] if CL.get('digests') else None),
                                                    ('生成したトークンの番号の列の SHA', CL['digests']['gen_ids_sha256'] if CL.get('digests') else None),
                                                    ('転記行 C', {'closed_record_sha16': sha16f(CLOSED), 'tool_error': CL.get('tool_error')})])),
        ('readout_pilot', collections.OrderedDict([('(i)〜(iv) と (vi) の (a)(b) の値', {k: last.get(k) for k in ('cells', 'iv', 'vi')}),
                                                   ('(iii) の選んだ文と値と除いた升目の数', last.get('iii')), ('外した升目と理由', (last.get('decision') or {}).get('dropped')),
                                                   ('機械の決定', last.get('decision')), ('本の計算のバッチの大きさ', last.get('batch')),
                                                   ('出口の値の自己検査の合否と見分ける力の有無', last.get('logit_check')),
                                                   ('読み取りの下見の起動の記録と出力の SHA', [s.get('start_end') for s in sessions])])),
        ('tool_diffs', [d for d in (FR.get('deviations') or []) if d.get('tool_diffs')])])
    added = [k for grp in ('extraction', 'behavior_pilot', 'readout_pilot') for k in content[grp]]
    return content, added


def main_freeze_checks(FR, pilot_dirs, npz_path):
    import bl3_core as K
    import bprime_core as Pc
    C = load(R_('design', 'contrasts-Bprime.json'))
    bad, res = [], {}
    frozen = FR['frozen_sha16']
    canon = 'design/contrasts-Bprime.json'
    if sha16f(P(canon)) != frozen[canon]:
        bad.append('正本の SHA16 が下見の前の凍結から変わった（正本を変える直しは本の凍結の決まりの外・登録者に上げる）')
    now_sha = {pth: (sha16f(P(pth)) if os.path.exists(P(pth)) else None) for pth in frozen}
    bad += ['凍結物の SHA16 の違いが逸脱の台帳の器の差分と合わない: %s' % x for x in K.ledger_chain_bad(frozen, now_sha, FR.get('deviations') or [])]
    res['changed'] = sorted(p for p in frozen if now_sha[p] != frozen[p])
    closure_now = import_closure(TOOLS)
    lock = Pc.lock_bad(FR.get('tools_import_closure') or [], frozen, closure_now, {pth: (sha16f(P(pth)) if os.path.exists(P(pth)) else None) for pth in closure_now})
    res['lock'] = {'excluded': sorted(Pc.LOCK_EXCLUDED), 'bad': lock}
    bad += lock
    for p, what in ((CLOSED, '行動の下見の閉じた記録'), (EXTRACT, '抽出の記録'), (SEAL, '封印の記録')):
        if not os.path.exists(p):
            bad.append('%s が無い（%s）' % (what, rel(p)))
    if bad:
        return None, None, None, None, None, res, bad
    EX, CL, SR = load(EXTRACT), load(CLOSED), load(SEAL)
    if npz_path is None or not os.path.exists(npz_path) or sha256f(npz_path) != EX.get('npz_sha256'):
        bad.append('手元の方向の npz が無いか、SHA-256 が公開した抽出の記録と違う')
    atts, sessions, fin = [], [], []
    for d in pilot_dirs:
        PJ = load(os.path.join(d, 'pilot-Bprime.json'))
        S = load(os.path.join(d, 'session.json'))
        if S.get('dry') or S.get('kind') != 'bprime_colab_pilot':
            bad.append('読み取りの下見の試みの出力が DRY か、相 pilot の出力でない: %s' % d)
        c = S.get('commit') or ''
        need_in = ('records/Bprime/FREEZE-RECORD-Bprime.json', 'records/Bprime/sealing-record-Bprime.json', 'records/Bprime/behavior/behavior-closed-Bprime.json',
                   'records/Bprime/extract/extraction-record-Bprime.json')
        if not (re.fullmatch(r'[0-9a-f]{40}', c) and all(in_commit(c, x) for x in need_in)):
            bad.append('読み取りの下見の試みのコミットが、凍結と封印と閉じた記録と抽出の記録を含むコミットでない: %s' % c)
        elif any(at_commit_sha16(c, x) != sha16f(R_(*x.split('/'))) for x in need_in[1:]):
            bad.append('読み取りの下見の試みのコミットの封印か閉じた記録か抽出の記録が、今の記録と違う: %s' % c)
        else:
            try:
                FRc = json.loads(git('show', '%s:records/Bprime/FREEZE-RECORD-Bprime.json' % c).stdout.decode('utf-8'))
            except Exception:
                FRc = {}
            if FRc.get('frozen_sha16') != frozen or FRc.get('prefreeze') != FR.get('prefreeze'):
                bad.append('読み取りの下見の試みのコミットの凍結の記録の凍結物か下見の前の値が、今の凍結の記録と違う: %s' % c)
        if S.get('canon_sha16') != frozen.get(canon):
            bad.append('読み取りの下見の試みの正本の SHA16 が凍結の記録と違う: %s' % d)
        ends = sorted(glob.glob(os.path.join(d, 'end-pilot*.json')))
        starts = sorted(glob.glob(os.path.join(d, 'start-pilot*.json')))
        se = {'start': (os.path.basename(starts[0]), sha256f(starts[0])) if starts else None, 'end': (os.path.basename(ends[0]), sha256f(ends[0])) if ends else None}
        if ends:
            E = load(ends[0])
            if E.get('outputs_sha256', {}).get('pilot-Bprime.json') != sha256f(os.path.join(d, 'pilot-Bprime.json')):
                bad.append('読み取りの下見の記録の SHA-256 が出力の SHA の記録と違う: %s' % d)
        else:
            bad.append('読み取りの下見の出力の SHA の記録が無い: %s' % d)
        atts.append(PJ)
        fin.append(S.get('finished') or '')
        sessions.append(dict({k: S.get(k) for k in ('commit', 'gpu', 'versions', 'canon_sha16', 'finished', 'session_id')}, start_end=se))
    if fin != sorted(fin) or not all(fin):
        bad.append('読み取りの下見の試みの与えた順が、終わりの時刻の順と違う（または時刻が無い）: %s' % fin)
    reruns = [x for x in FR.get('deviations') or [] if x.get('kind') == 'pilot_rerun']
    if len(atts) >= 2 and len(reruns) < len(atts) - 1:
        bad.append('読み取りの下見の試みが二つ以上あるのに、逸脱の台帳にやり直しの記帳（kind pilot_rerun）が足りない: 試み %d・記帳 %d' % (len(atts), len(reruns)))
    if not atts:
        bad.append('読み取りの下見の試みが無い')
    elif atts[-1].get('tool_error'):
        bad.append('最後の読み取りの下見の試みが器の誤り（本の凍結の前に登録者の裁定を仰ぐ）')
    else:
        mine, theirs = decision_rebuild(C, atts[-1])
        res['decision_rebuild_same'] = json.dumps(mine, sort_keys=True, ensure_ascii=False) == json.dumps(theirs, sort_keys=True, ensure_ascii=False)
        if not res['decision_rebuild_same']:
            bad.append('凍結した決定木の器で出し直した決定が、読み取りの下見の記録の決定と違う（T12）')
    res['runs'], b_ = runs_count_bad(('extract', 'behavior', 'pilot'), {'pilot': len(pilot_dirs)}, FR.get('deviations'))
    bad += b_
    res['n_attempts'] = len(atts)
    res['seal'] = {'record_sha16': sha16f(SEAL), 'predictions_sha256': {r: (sha256f(R_(*v['path'].split('/'))) if os.path.exists(R_(*v['path'].split('/'))) else None)
                                                                         for r, v in (SR.get('predictions') or {}).items()}}
    for r_, v in (SR.get('predictions') or {}).items():
        if res['seal']['predictions_sha256'][r_] != v.get('sha256'):
            bad.append('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % r_)
    return atts, sessions, EX, CL, now_sha, res, bad


def main_freeze_structure_bad(section, allowed):
    """本の凍結の節の実際の鍵の照らし（正本 `computation.main_freeze`「これら以外の鍵が増えたら止める」・v0.2・U11・前は器が書いた名そのものを照らして落ちようがなかった）。"""
    bad = []
    out_top = sorted(set(section) - set(MAIN_FREEZE_TOP))
    if out_top:
        bad.append('本の凍結の節の鍵が閉じた一覧の外: %s' % out_top)
    added = section.get('added') or {}
    for grp, keys in added.items():
        if grp not in allowed:
            bad.append('足した組が正本の一覧の外: %s' % grp)
        elif isinstance(allowed[grp], list) and sorted(set(keys) - set(allowed[grp])):
            bad.append('足した鍵が正本の一覧の外（%s）: %s' % (grp, sorted(set(keys) - set(allowed[grp]))))
    for i, rec in enumerate(list(section.get('pilot_attempts') or []) + [section.get('pilot') or {}]):
        o = sorted(set(rec) - set(PILOT_KEYS))
        if o:
            bad.append('下見の記録の鍵が閉じた一覧の外（%d）: %s' % (i, o))
    for sss in section.get('sessions') or []:
        o = sorted(set(sss) - set(SESSION_KEYS))
        if o:
            bad.append('下見の試みの session の鍵が閉じた一覧の外: %s' % o)
    return bad


def main_freeze(words, when, pilot_dirs, npz_path):
    import bprime_core as Pc
    FR = load(FR_JSON)
    if 'main_freeze' in FR:
        raise SystemExit('本の凍結は既にある')
    C = load(R_('design', 'contrasts-Bprime.json'))
    atts, sessions, EX, CL, now_sha, res, bad = main_freeze_checks(FR, pilot_dirs, npz_path)
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str)[:4000])
    if bad:
        raise SystemExit('本の凍結の確かめが外れた（止める・登録者に相談）: %s' % bad)
    content, added = main_freeze_content(C, atts, sessions, EX, CL, now_sha, FR, res, when, words)
    outside = Pc.main_freeze_keys_ok(added, C['computation']['main_freeze']['allowed_keys'])
    if outside:
        raise SystemExit('本の凍結に足す鍵が正本の一覧の外: %s' % outside)
    before = json.loads(json.dumps(FR))
    FR['main_freeze'] = collections.OrderedDict([
        ('frozen_jst', when), ('registrant_words', words), ('added', content), ('pilot_attempts', atts), ('pilot', atts[-1]), ('decision', atts[-1].get('decision')),
        ('sessions', sessions), ('frozen_sha16', now_sha), ('tool_diffs_applied', res['changed']), ('seal', res['seal']), ('runs', res['runs']), ('lock', res['lock']),
        ('freeze_tool', 'tools/freeze_Bprime.py %s' % VERSION), ('deviations_n', len(FR.get('deviations') or []))])
    sb = main_freeze_structure_bad(FR['main_freeze'], C['computation']['main_freeze']['allowed_keys'])
    if sb:
        raise SystemExit('本の凍結の節の鍵が閉じた一覧の外（止める・U11）: %s' % sb)
    FR['main_freeze_sha16'] = Pc.main_freeze_sha16(FR)                 # 本の凍結の節の正準の SHA16（起動器と集計の器が同じ関数で照らす・v0.2・U10）
    assert all(FR[k] == before[k] for k in before), '本の凍結でほかの鍵が変わった'
    assert set(FR) - set(before) == {'main_freeze', 'main_freeze_sha16'}
    with open(FR_JSON, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(FR, fh, ensure_ascii=False, indent=1)
    dec = atts[-1].get('decision') or {}
    add = ['', '## 本の凍結（読み取りの下見の記録と機械の決定を足した・正本 computation.main_freeze）', '',
           '- 本の凍結: %s（日本時間）・登録者の言葉は逐語で「%s」。' % (when, words),
           '- 読み取りの下見の試み %d・最後の試みの機械の決定: %s（外した升目: %s）・本の計算のバッチの大きさ %s。' % (len(atts), dec.get('q1'), '・'.join(dec.get('dropped') or []) or 'なし', atts[-1].get('batch')),
           '- 凍結物の SHA16 の違い（逸脱の台帳の器の差分と一致）: %s。' % ('・'.join(res['changed']) or '無し'), '', CLAUSE, '']
    md = open(FR_MD, encoding='utf-8').read().rstrip(NL)
    if md.endswith(CLAUSE):
        md = md[: -len(CLAUSE)].rstrip(NL)
    with open(FR_MD, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(md + NL + NL.join(add))
    row = ('| %s | **B′ 本の凍結**（登録者「%s」%s 日本時間）: 読み取りの下見の記録と機械の決定（%s）を凍結の記録に足した。器の差分 %d（逸脱の台帳と一致）。 | records/Bprime/FREEZE-RECORD-Bprime.json | %s | 以後の変更は逸脱として台帳に記す |'
           % (when.split(' ')[0], words, when, dec.get('q1'), len(res['changed']), sha16f(FR_JSON)))
    led = open(LEDGER_ALL, encoding='utf-8').read() if os.path.exists(LEDGER_ALL) else ''
    if 'B′ 本の凍結' not in led:
        with open(LEDGER_ALL, 'a', encoding='utf-8', newline=NL) as fh:
            fh.write(('' if (not led or led.endswith(NL)) else NL) + row + NL)
    print('[freeze_Bprime] 本の凍結を記帳した: %s（読み取りの下見の試み %d）' % (rel(FR_JSON), len(atts)))


# ---------------- 自己検査（純な関数と止まるべき形・全体は合成データの正式の確かめで走らせる） ----------------
def _selftest():
    import tempfile
    import bl3_core as K
    import bprime_core as Pc
    C = load(R_('design', 'contrasts-Bprime.json'))
    ok = []
    with tempfile.TemporaryDirectory() as td:
        # 裁定の記録の番号と正本
        names = [os.path.join(td, 'rulings-D%d.md' % i) for i in range(255, 256 + (int(C['numbering']['rulings_next'][1:]) - 256))]
        info, b_ = rulings_check(C, names)
        ok.append(('裁定の記録と正本の番号がそろう', not b_ and info['rulings_next_expected'] == C['numbering']['rulings_next']))
        info2, b2 = rulings_check(C, names + [os.path.join(td, 'rulings-D%d.md' % (int(C['numbering']['rulings_next'][1:])))])
        ok.append(('正本に無い裁定の記録で止まる', bool(b2)))
    # 等方の乱数 g の記録（手元で引く・二度で同じ）
    g1, g2 = g_local(C), g_local(C)
    ok.append(('g を二度引いて同じ SHA', g1['g_sha256'] == g2['g_sha256'] and g1['dim'] == C['inputs']['model_facts']['hidden_size'] and g1['count'] == C['nulls']['isotropic']['count']))
    # Colab の確かめの照らし
    tool_sha = closure_sha_map()
    canon16 = sha16f(R_('design', 'contrasts-Bprime.json'))
    man = {'files': {'model-00001-of-00002.safetensors': {'sha256': 'ab' * 32}, 'config.json': {'sha256': 'cd' * 32}}}
    S = {'kind': 'bprime_colab_check', 'dry': False, 'commit': 'a' * 40, 'gpu': C['inputs']['gpu']['name'], 'versions': {'transformers': C['inputs']['versions']['transformers'],
         'torch': C['inputs']['versions']['torch'], 'numpy': 'x'}, 'weights_sha256': {k: v['sha256'].upper() for k, v in man['files'].items()}, 'canon_sha16': canon16, 'tools_sha16': tool_sha}
    CK = {'all_pass': True, 'items': {'isotropic_g': {'g': {'g_sha256': g1['g_sha256']}}, 'logit_tolerance_k': {'pass': True, 'k': 2.0, 'z0': 4}},
          'determinism': {'allow_tf32_matmul': False, 'allow_tf32_cudnn': False, 'float32_matmul_precision': 'highest', 'attn_implementation': 'sdpa'}}
    c, fails = colab_check_eval(C, S, CK, canon16, tool_sha, g1['g_sha256'], man)
    ok.append(('Colab の確かめがそろう形で外れ無し', not fails))
    for mut, name in ((lambda s, k: s.update(dry=True), 'DRY'), (lambda s, k: s.update(gpu='NVIDIA L4'), 'GPU'), (lambda s, k: k['items']['isotropic_g']['g'].update(g_sha256='0'), 'g'),
                      (lambda s, k: s['weights_sha256'].update({'config.json': '0'}), '重み'), (lambda s, k: s.update(canon_sha16='0'), '正本'), (lambda s, k: k.update(all_pass=False), '項目'),
                      (lambda s, k: k['determinism'].update(allow_tf32_matmul=True), '決定性の値'), (lambda s, k: k['items']['logit_tolerance_k'].update(**{'pass': False}), 'k の項目の合否'),
                      (lambda s, k: s['tools_sha16'].update({'tools/bprime_core.py': '0'}), '器の SHA（閉包）')):
        S2, CK2 = json.loads(json.dumps(S)), json.loads(json.dumps(CK))
        mut(S2, CK2)
        ok.append(('Colab の確かめの外れ（%s）で止まる' % name, bool(colab_check_eval(C, S2, CK2, canon16, tool_sha, g1['g_sha256'], man)[1])))
    # 決定の出し直し（合成の下見の記録）
    cells = ['%s|%s' % tuple(x) for x in C['cells_main']]
    PL = C['pilot']
    good = {c_: {'lo': 0.0, 'pa': 0.4, 'mass': 0.95, 'pass_i_ii': K.pass_i_ii(0.95, 0.4, PL['mass_min'], PL['p_bounds'])} for c_ in cells}
    vi = K.vi_decision(0.002, 0.001, PL['noise_max'], C['readout']['primary']['batch'])
    rec = {'vi': {'a': {c_: 0.002 for c_ in cells}, 'b': {c_: 0.001 for c_ in cells}}, 'cells': good, 'batch': vi['batch'], 'floor': vi['floor'],
           'decision': K.cells_decision({c_: v['pass_i_ii'] for c_, v in good.items()}, {}, PL['decision']['cells_min_pass'])}
    m1, t1 = decision_rebuild(C, rec)
    ok.append(('決定の出し直しが記録と同じ', json.dumps(m1, sort_keys=True) == json.dumps(t1, sort_keys=True)))
    rec_bad = json.loads(json.dumps(rec))
    rec_bad['decision']['dropped'] = [cells[0]]
    m2, t2 = decision_rebuild(C, rec_bad)
    ok.append(('書き換えた決定を捕まえる', json.dumps(m2, sort_keys=True) != json.dumps(t2, sort_keys=True)))
    # 本の凍結に足す鍵が正本の一覧の内
    EX = {'row_D': {}, 'npz_sha256': 'X', 'coefficient': 1.0, 'g_match': True}
    CL = {'digests': {'scorer_sha16': {}, 'scores_sha256': 'S', 'gen_ids_sha256': 'G'}, 'tool_error': False}
    global CLOSED
    keep = CLOSED
    with tempfile.TemporaryDirectory() as td:
        CLOSED = os.path.join(td, 'closed.json')
        with open(CLOSED, 'w', encoding='utf-8') as fh:
            fh.write('{}')
        content, added = main_freeze_content(C, [dict(rec, iii={'rho': 0.1}, logit_check={'states': {}})], [{'start_end': None}], EX, CL, {}, {'deviations': []}, {}, 'x', 'y')
    CLOSED = keep
    ok.append(('本の凍結に足す鍵がすべて正本の一覧の内', Pc.main_freeze_keys_ok(added, C['computation']['main_freeze']['allowed_keys']) == [] and len(added) == 15))
    # 本の凍結の節の鍵の照らし（v0.2・U11）: 器が実際に書く形は通り、外の鍵を一つ足すと止まる
    allowed = C['computation']['main_freeze']['allowed_keys']
    sec = collections.OrderedDict([(k_, None) for k_ in MAIN_FREEZE_TOP])
    sec.update(added=content, pilot_attempts=[{'version': 'x', 'cells': {}, 'decision': {}}], pilot={'version': 'x'}, sessions=[{'commit': 'c', 'start_end': None}])
    ok.append(('本の凍結の節の鍵が閉じた一覧の内', main_freeze_structure_bad(sec, allowed) == []))
    for mut, name in ((lambda d: d.update(extra=1), '節の外の鍵'), (lambda d: d['pilot'].update(effects={}), '下見の記録の外の鍵'),
                      (lambda d: d['added']['extraction'].update({'効き目': 1}), '足した組の外の鍵'), (lambda d: d['sessions'][0].update(values=1), 'session の外の鍵')):
        d2 = json.loads(json.dumps(sec, ensure_ascii=False))
        mut(d2)
        ok.append(('本の凍結の鍵の照らしが止まる（%s）' % name, bool(main_freeze_structure_bad(d2, allowed))))
    # 七つ目（下見の前の凍結から動かせない器）と節の SHA16（v0.2・U03・U10）
    cl = import_closure(TOOLS)
    shas = {x: sha16f(P(x)) for x in cl}
    ok.append(('動かせない器が同じなら通る', Pc.lock_bad(cl, shas, cl, dict(shas)) == []))
    ok.append(('集計の器の SHA が違えば台帳に記しても止まる', bool(Pc.lock_bad(cl, shas, cl, dict(shas, **{'tools/analyze_Bprime.py': '0' * 16})))))
    ok.append(('除く器（フックの付け外しの範囲）の SHA の違いは七つ目では止めない', Pc.lock_bad(cl, shas, cl, dict(shas, **{'tools/bprime_run.py': '0' * 16})) == []))
    ok.append(('本の凍結の節の SHA16 が節の正準の JSON から出る', Pc.main_freeze_sha16({'main_freeze': sec}) == Pc.canon_sha16(sec)))
    ok.append(('錠の除く器が正本 v5 の一覧と同じ（U03）', dict(Pc.LOCK_EXCLUDED) == dict(C['computation']['main_freeze'].get('lock_excluded') or {})))
    ok.append(('測った k での出口の値の下限（票の数と同じ・小数一桁・U34）', [round(z_floor(k_, 4, 30.0, 3), 1) for k_ in (5.78, 4.63, 16, 64)] == [13.7, 12.8, 21.9, 28.2]))
    ok.append(('移し方の記録が凍結物に入る（U28）', 'records/Bprime/publish-map-Bprime.json' in frozen_files(C)))
    # 閉包の始めの器が見つからなければ止まる（v0.2・U01）
    try:
        import_closure(TOOLS + ['tools/no_such_tool_Bprime.py'])
        ok.append(('閉包の始めの器が無ければ止まる', False))
    except SystemExit:
        ok.append(('閉包の始めの器が無ければ止まる', True))
    bad = [n for n, v in ok if not v]
    assert not bad, bad
    print('freeze_Bprime.py %s SELFTEST PASS（%d 項目・器の閉包 %d・凍結物の型 %d・全体の走りは合成データの正式の確かめで見る）' % (VERSION, len(ok), len(import_closure(TOOLS)), len(frozen_files(C))))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if '--selftest' in sys.argv:
        return _selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['prefreeze', 'main'])
    ap.add_argument('--words')
    ap.add_argument('--when')
    ap.add_argument('--colab-check')
    ap.add_argument('--behavior-batch', type=int)
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--pilot', nargs='*')
    ap.add_argument('--npz')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if a.stage == 'prefreeze':
        if a.check_only:
            return prefreeze(None, None, None, a.behavior_batch)
        if not (a.words and a.when and a.colab_check):
            raise SystemExit('--words・--when・--colab-check が要る（生成のバッチの大きさは正本から取る・与えれば照らす）')
        return prefreeze(a.words, a.when, a.colab_check, a.behavior_batch, a.force)
    if not (a.words and a.when and a.pilot and a.npz):
        raise SystemExit('--words・--when・--pilot・--npz が要る')
    main_freeze(a.words, a.when, a.pilot, a.npz)


if __name__ == '__main__':
    main()
