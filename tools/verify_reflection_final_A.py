# -*- coding: utf-8 -*-
"""verify_reflection_final_A.py v1 —— 凍結前の最終検分の反映（採否表 P105〜P153・登録者裁定 D26〜D35）が直ったことを機械で確かめ、
records/reviews/A/final/verification-reflection-final-A.{md,json} を書く（2026-09-14）。
直った条件は事前登録（records/reviews/A/final/preregistration-reflection-final-A.md の S1〜S14・T1〜T14・G1〜G3・F1〜F6・R1〜R4・反映の前に記した）。
本器は次を走らせる: 正本の文字列とキーの突合／共有関数と検査器の自己検査／合成検査と門と校正の合成検査の記録／合成の走行の上の否定の経路（集計器・組み立て器・走査器）／
凍結器の実験（リポジトリの写しの木・results と .git を除く）／格子 v3.3 と v3.2（コミット 150dab4）の節ごとの数値の突合／設計事実・草案9・雛形・README の文字列と数の検査の記録。
リポジトリの results/ と records の現物は変えない（写しの木と一時置き場で走らせる）。
用法: python tools/verify_reflection_final_A.py --work <リポジトリの外の一時置き場>
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, shutil, subprocess, datetime, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
BASE_COMMIT = '150dab464f6b28314528a87c2fbb106d329bf7de'   # 凍結前の最終検分の記録のコミット（格子 v3.2 を持つ・公開済み）
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
ap = argparse.ArgumentParser(); ap.add_argument('--work', required=True)
ap.add_argument('--synth', default='records/A/synth-A-2026-09-14b.json'); ap.add_argument('--synth-gates', default='records/A/synth-gates-A-2026-09-14b.json')
ap.add_argument('--draft', default='design/design-stageA-draft9.md'); ap.add_argument('--out', default=os.path.join(REPO, 'records', 'reviews', 'A', 'final', 'verification-reflection-final-A'))
a = ap.parse_args()
WORK = os.path.abspath(a.work)
try:
    inside = os.path.commonpath([os.path.realpath(WORK), os.path.realpath(REPO)]) == os.path.realpath(REPO)
except ValueError:
    inside = False
assert not inside, '一時置き場をリポジトリの中に置かない'
shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK)
T = runs_A.load_T(); PY = sys.executable; ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
FAM = T['families']['A_slope']; ME = T['reading_selection']['measurable_effect_type']; PS = T['print_strings']; TI = T['tooling_interpretations']
ROWS = []; EXTRA = {}; T0 = time.time()


def R(cond, item, text, method, ok, detail=''):
    ROWS.append({'cond': cond, 'item': item, 'condition': text, 'method': method, 'ok': bool(ok), 'detail': str(detail)[:600]})
    print('[verify] %s %s（%s）%s' % ('○' if ok else '×', cond, item, '' if ok else str(detail)[:400]), flush=True)


def run(args, timeout=5400, cwd=None):
    p = subprocess.run([PY] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', env=ENV, timeout=timeout, cwd=cwd)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


SRC = lambda rel: open(os.path.join(REPO, rel), encoding='utf-8').read().replace('\r\n', '\n')
tool = lambda name: os.path.join(REPO, 'tools', name)
has = lambda s, *ws: all(w in (s or '') for w in ws)
lacks = lambda s, *ws: [w for w in ws if w not in (s or '')]

# ---- 1-A. 正本（S1〜S14）
R('S1', 'D26 (a)', '運用の解釈の状態が項 24・25 の確認（裁定 D26）と、全項の確認を凍結確認の直前に受けることを書く', '正本の文字列',
  has(TI['status'], 'calibration.incomplete_rule', 'sessions.commit_rule', '登録者裁定 D26', '凍結確認の直前'), lacks(TI['status'], 'calibration.incomplete_rule', 'sessions.commit_rule', '登録者裁定 D26', '凍結確認の直前'))
CR = T['calibration'].get('claim_release')
R('S2', 'D26 (b)・P144', '初点の名乗りの移し替えの文言（理由の記帳・退避・消さない・並行のランタイム）が正本にあり、一覧の項に入る', '正本の文字列とキー',
  has(CR, '理由を記帳', '退避してから別の機種で名乗る', '消さない', '並行のランタイムを同時に起こさない') and 'calibration.claim_release' in TI['items'], CR)
EC = T['judge_validity']['extract'].get('echo')
R('S3', 'D26 (d)・P141', '断片の復唱の測定（最長共通部分の字数を鍵の側・採点の後に分布・閾値なし）が正本にあり、一覧の項に入る', '正本の文字列とキー',
  has(EC, '最長共通部分の字数', '対応表（鍵）の側', '分布', '閾値を置かない') and 'judge_validity.extract.echo' in TI['items'], EC)
R('S4', 'D27', 'B_per_contrast が 10,000・区間の規則・境界の規則（またげば測れなかった）がある', '正本の値と文字列',
  ME.get('B_per_contrast') == 10000 and has(ME.get('interval'), '区間', 'デルタ法') and has(ME.get('boundary_rule'), 'またぐ', '測れなかった'), {k: ME.get(k) for k in ('B_per_contrast', 'ci_level', 'interval', 'boundary_rule')})
R('S5', 'D28', '両向きを計算し、両向きとも測れた向きの効果種を測れたとする規則がある', '正本の値と文字列',
  ME.get('directions') == 'both' and has(ME.get('directions_rule'), '逆向き', '両向きとも測れた向きである効果種'), ME.get('directions_rule'))
FACTS = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'design-facts-A.json')); FD = FACTS['facts']
R('S6', 'D29', '場面ごとの被覆の規則・下限のキー（転記行 D の区切りと同じ値）・選択規則の読みの範囲の文言がある', '正本の文字列とキー・設計事実',
  has(ME.get('coverage'), '測れた対比', 'blind_below', 'id') and ME.get('blind_below') == FD['D']['data'].get('blind_threshold') and '測れた対比の場面について書き' in T['reading_selection']['text'] and '{blind}' in PS.get('measurable_coverage', ''),
  {'blind_below': ME.get('blind_below'), 'facts_D_blind_threshold': FD['D']['data'].get('blind_threshold')})
R('S7', 'D30', 'rule が Δ に観測効果量を使わない・d0 は実測・門の前の札 D1 の初段・確率の意味を書き分ける', '正本の文字列',
  has(ME.get('rule'), '観測された効果量を使わない', '水準差 d0 は実測', '札 D1 の初段', '全場面に Δ があるときの確率', '場面ごとに別の走行の標本'),
  lacks(ME.get('rule'), '観測された効果量を使わない', '水準差 d0 は実測', '札 D1 の初段', '全場面に Δ があるときの確率', '場面ごとに別の走行の標本'))
R('S8', 'D31', '区間の被覆の断りが正本の区間の欄と print_strings にある', '正本の文字列',
  has(FAM['confirm_rule']['pt_slope'].get('interval_coverage'), '同時被覆を主張しない', '上限として読まない') and has(PS.get('interval_note'), '同時被覆を主張しない', '上限として読まない'), PS.get('interval_note'))
SI = T['sample_inspection']
R('S9', 'D32', '抽出検査の正本が、鍵と機械分類の集計をリポジトリの外に・封印を目視の前に・標本に機械分類を印字しない・目視の分類の後に一致を記録、と書く', '正本の文字列',
  has(SI.get('content'), '伏せているのは機種・場面・腕', '標本に印字せず', '目視の記録に書いた後') and has(SI.get('record'), '公開リポジトリの外', '封印', '目視の前にコミット', '-agreement.json') and has(SI.get('key_rule'), 'リポジトリの中なら止まる', 'SHA-256'),
  {k: SI.get(k) for k in ('content', 'record', 'key_rule')})
FC = T['firth_check']
R('S10', 'D33', 'failure_options に四つの手があり、一覧に無い手と許容差を後から動かす手は採らないと書く', '正本の値',
  len(FC.get('failure_options') or []) == 4 and has(FC.get('failure_path'), '一覧に無い手', '許容差'), FC.get('failure_path'))
R('S11', 'D34', '時間貸しの見積もりと上限額の記帳・上限での停止・上界の分を停止規則の参照から除く、が正本にある', '正本の文字列',
  has(T['cost'].get('rental_rule'), '見積もり', '上限額', '止めて再裁定') and has(T['cost']['stop_rule'].get('rental_adjust'), '除いて比べる', '転記行 F'), {'rental_rule': T['cost'].get('rental_rule'), 'rental_adjust': T['cost']['stop_rule'].get('rental_adjust')})
bad_eff = [c['id'] for c in FAM['contrasts'] if c.get('effect') != c['id'].split(':', 1)[1]]; ids = FAM.get('effect_type_ids') or []
R('S12', 'P127', '各対比の effect が id の後半と一致し、effect_type_ids が七つで、生成器の integrity が不一致を assert する', '正本のキーと生成器',
  not bad_eff and len(ids) == FAM['effect_types'] == 7 and set(c['effect'] for c in FAM['contrasts']) == set(ids) and "'effect_mismatch'" in SRC('tools/make_contrasts_A.py'), {'bad': bad_eff, 'effect_type_ids': ids})


def resolve(path, prev):
    def get(p):
        v = T
        for seg in p.split('.'):
            if not isinstance(v, dict) or seg not in v:
                return None
            v = v[seg]
        return v
    cands = [path] + (['.'.join(prev.split('.')[:i]) + '.' + path for i in range(len(prev.split('.')) - 1, 0, -1)] if prev else [])
    for c in cands:
        if get(c) not in (None, '', [], {}):
            return c
    return None


miss = []; DEC = T.get('registrant_decisions_D26_D35') or {'items': []}
for it in DEC['items']:
    num, body = it.split(' ', 1)
    if num == 'D35':
        continue   # 草案の §0 を指す（R1 で確かめる）
    prev = None
    for seg in re.sub(r'（.*?）', '', body).split('・'):
        full = resolve(seg.strip(), prev)
        if full is None:
            miss.append((num, seg))
        else:
            prev = full
R('S13', '—', 'registrant_decisions_D26_D35 の各裁定が正本のキーを指し、版は draft9-2026-09-14・生成器は v2.5', '正本',
  len(DEC['items']) == 10 and not miss and T.get('version') == 'draft9-2026-09-14' and T.get('generator') == 'tools/make_contrasts_A.py v2.5', {'missing': miss, 'version': T.get('version'), 'generator': T.get('generator')})
L9 = SRC('records/A/numbers-lint-draft9A.md') if os.path.exists(os.path.join(REPO, 'records', 'A', 'numbers-lint-draft9A.md')) else ''
gen_ok = {nm: ('生成器の文字列リテラル検査（`tools/%s`）: 構造でない数 0' % nm) in L9 for nm in ('make_contrasts_A.py', 'design_facts_A.py', 'power_grid_A.py', 'confirm_A.py', 'build_draftA.py')}
R('S14', 'P121', '数の検査の生成器の検査で、正本と転記行と本文に文字列を書く五つの器の構造でない数が零・格子の器が切り詰めの上下限を共有関数から読む', '草案9 の数の検査の記録と格子の器の原稿',
  all(gen_ok.values()) and '違反の合計: 0' in L9 and 'from confirm_A import RATE_CLIP' in SRC('tools/power_grid_A.py'), gen_ok)

# ---- 1-B. 器材（T1〜T14）
rc, out = run([tool('confirm_A.py'), '--selftest']); EXTRA['confirm_selftest_tail'] = out[-600:]
R('T1', 'P130', '門2 の縮小と非収束が重なった対比の rules に理由を二つとも並べ、行 id と札を変えない', '確証の共通関数の自己検査（項 8）', rc == 0 and 'SELFTEST PASS' in out and '8 v1.3' in out and 'P130' in out, out[-300:])
CF = SRC('tools/confirm_A.py')
R('T2', 'P132', '模擬の名目は β₃ も pt 差の傾きも p<α・初段は p≤α/m', '確証の共通関数の自己検査（項 7）と原稿',
  rc == 0 and '7 v1.3' in out and "Rn = r['p_beta'] < R.alpha" in CF and "pt_nom = r['p_pt'] < R.alpha and r['same']" in CF, out[-300:])
rc9, out9 = run([tool('sample_inspection_A.py'), 'selftest'])
R('T9', 'D32', '抽出検査の器: 鍵の置き場がリポジトリの中なら止まる・封印の記録・標本に機械分類を印字しない・一致の採点で SHA-256 が封印と合わなければ止まる', '抽出検査の器の自己検査（四項）',
  rc9 == 0 and 'SELFTEST PASS' in out9 and all(('%d %s' % (i, w)) in out9 for i, w in ((1, 'extract'), (2, 'extract'), (3, 'score'), (4, 'score'))), out9[-300:])
rc10, out10 = run([tool('judge_fragments_A.py'), 'selftest'])
R('T10', 'P141', '断片の抽出が最長共通部分の字数（自分の腕・ほかの腕の最大）を鍵に置き、採点がその分布を記述する', '判定器の自己検査（項 4b・6b）', rc10 == 0 and 'SELFTEST PASS' in out10 and '4b v2.1' in out10 and '6b v2.1' in out10, out10[-300:])
import numbers_lint
rc13, out13 = run([tool('numbers_lint.py'), '--selftest'])
R('T13', 'P126', '数の検査の限界の欄に docstring と自己検査の関数の中の文字列を検査しない旨がある', '数の検査の原稿と記録',
  rc13 == 0 and has(numbers_lint.LIMIT, 'docstring', '_selftest') and numbers_lint.LIMIT in L9, numbers_lint.LIMIT[-120:])
rcl, outl = run([tool('report_lint.py'), '--selftest'])
EXTRA['report_lint_selftest_tail'] = outl[-400:]
SA = runs_A.read_json(os.path.join(REPO, a.synth)); SAmd = SRC(a.synth[:-5] + '.md'); muts = {m['name']: m for m in SA.get('mutations', [])}; paths = {p for r in SA.get('per_run', []) for p in r['paths']}
SY = SRC('tools/synth_A.py')
R('T7', 'P135・P136', '合成検査が期待の札（正本 stage2_first_match から組む）と期待の keep（配置から組む）を突合し、変異 M1〜M10 のすべてが不一致を出す・M8 を見分ける配置がある', '合成検査 v2.1 の記録と原稿',
  SA.get('version') == 'v2.1' and SA.get('full') and not SA.get('mismatches') and not SA.get('rows_not_fired') and not SA.get('paths_missing') and not SA.get('errors')
  and sorted(muts) == sorted('M%d' % i for i in range(1, 11)) and all(m['detected'] for m in muts.values())
  and has(SY, 'def expected_label(row):', 'def expected_keep(run, c, C):', "FIRST_MATCH = FAM['confirm_rule']['label_stages']['stage2_first_match']", "'kind': 'label'", "'kind': 'keep'", '0.84] for x in X_ARMS')
  and {'measurable_both_directions', 'gate2_partial_shrink'} <= paths,
  {n: (m.get('mismatches') if isinstance(m.get('mismatches'), int) else len(m.get('mismatches') or []), m.get('detected')) for n, m in sorted(muts.items(), key=lambda x: int(x[0][1:]))})
SG = runs_A.read_json(os.path.join(REPO, a.synth_gates)); SGmd = SRC(a.synth_gates[:-5] + '.md')
R('T8', 'P134・P137', '合成記録の見出しにファイル名の日付の基準・合成記録に限界の三行', '合成検査と門と校正の合成検査の記録',
  has(SAmd, 'ファイル名の日付は手元の日付〔日本時間〕', '- 限界: 札の全組合せ表（正本 label_combo_table）は判定関数', '- 限界: 期待の行 id の符号化', '- 限界: 本器は Firth の PPLRT') and 'ファイル名の日付は手元の日付〔日本時間〕' in SGmd,
  lacks(SAmd, 'ファイル名の日付は手元の日付〔日本時間〕', '- 限界: 札の全組合せ表（正本 label_combo_table）は判定関数', '- 限界: 期待の行 id の符号化', '- 限界: 本器は Firth の PPLRT'))
R('T12', 'D26 (b)', '校正帯の器に名乗りの退避の関数があり、門と校正の合成検査 v2.1 が退避の前に名乗れない・理由が無ければ止まる・退避の後に名乗れることを確かめる', '門と校正の合成検査の記録と原稿',
  SG.get('version') == 'v2.1' and SG.get('pass') and any('初点の名乗りの移し替え' in c['check'] and c['ok'] for c in SG.get('checks', [])) and 'def release_first_point(sdir, reason, by):' in SRC('tools/calib_band_A.py'),
  [c['check'] for c in SG.get('checks', []) if not c['ok']])
rct, outt = run([tool('tooling_interpretations_A.py'), '--out', os.path.join(WORK, 'ti.md')])
TIrec = SRC('records/A/tooling-interpretations-A.md'); TIgen = open(os.path.join(WORK, 'ti.md'), encoding='utf-8').read() if rct == 0 else ''
R('T14', 'P140・P106', '運用の解釈の記録の各項に向きの一行・COI に同じ向きの項・記録を正本から組み立てる器があり、組み立て直すと記録と一致する', '記録と器（一時置き場で組み立て直し）',
  rct == 0 and TIgen == TIrec and TIrec.count('\n- 向き: ') == len(TI['items']) == 30 and 'style_gate.applies_sizes・families.A_slope.interpretation_clause.count_after・families.A_slope.refuse_gate.denominator_detail は、いずれも' in TIrec,
  {'rebuild_equal': TIgen == TIrec, 'direction_lines': TIrec.count('\n- 向き: '), 'items': len(TI['items'])})

# ---- 合成の走 1 の置き場で: 集計の記録（T3）・否定の経路（T4・T5）・--gate（T6）・雛形の到達の表（R3 の一部）
import report_lint
SW = os.path.join(WORK, 'synth1'); rcs, outs = run([tool('synth_A.py'), '--root', SW, '--runs', '1', '--mutations', 'none', '--keep', '--record', os.path.join(WORK, 'synth1-rec')])
R('合成の走 1', '—', '合成の走 1（測定不能・床の持続・撤退条件の異常）が期待の行 id・札・keep・注と一致する（記録は一時置き場）', '合成検査（走 1 のみ）', rcs == 0 and '不一致 0' in outs, outs[-300:])
tag = 'synthA01'; root1 = os.path.join(SW, 'run01'); rec1 = os.path.join(root1, 'records'); ANP = os.path.join(root1, 'out', 'analysis-%s.json' % tag)
AN = runs_A.read_json(ANP) if os.path.exists(ANP) else {}; M_ = AN.get('measurable') or {}
types_ok = bool(M_.get('types')) and all(set(v['directions']) == {'room', 'opposite'} and all(len(d['ci']) == 2 and d['state'] in ('measured', 'crosses', 'below') for d in v['directions'].values())
                                         and {'measured_contrasts', 'blind_ids', 'reasons', 'n_contrasts'} <= set(v) for v in M_['types'].values())
per_ok = bool(M_.get('per_contrast')) and all('d0' in p and set(p['directions']) == {'room', 'opposite'} and all(('clause_rate_among_fit' in d) or ('reason' in d) for d in p['directions'].values()) for p in M_['per_contrast'])
R('T3', 'D27〜D29・P117', '集計が向きごとの確率と区間・両向きの判定と境界の判定・測れた対比の本数と下限未満の id・測れなかった理由（d0・札の率・解釈条項の発火率・4B の点の外れ）を返す', '確証の共通関数の自己検査（項 5・9）と合成の走 1 の集計の記録',
  rc == 0 and '9 v1.3' in out and types_ok and per_ok and M_.get('ci_level') == ME['ci_level'] and bool(M_.get('coverage')), {'types_ok': types_ok, 'per_ok': per_ok, 'ci_level': M_.get('ci_level'), 'coverage': (M_.get('coverage') or [])[:2]})
TPL = os.path.join(REPO, T['report_rules']['template']); TL = frozenset(open(TPL, encoding='utf-8').read().replace('\r\n', '\n').split('\n'))


def build(analysis, outp, extra=()):
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    rc_, o_ = run([tool('build_report_A.py'), '--draft', '1', '--analysis', analysis, '--out', outp, '--force'] + list(extra))
    txt_ = open(outp, encoding='utf-8').read() if os.path.exists(outp) else ''
    sp_ = report_lint.sidecar_path(outp); side_ = runs_A.read_json(sp_) if os.path.exists(sp_) else None
    return rc_, o_, txt_, side_


kinds = lambda txt_, side_, allow=False: sorted({v['kind'] for v in report_lint.lint(txt_, T, TL, sidecar=side_, allow_dev_marks=allow)})
BASEC = [tool('analyze_A.py'), '--tag', tag, '--root', root1, '--anchor-tag', tag + '-anchor2', '--bridge-tag', tag + '-bridge', '--api-tag', tag + '-api', '--style', os.path.join(rec1, 'style-%s.json' % tag),
         '--gate', os.path.join(rec1, 'gate-%s.json' % tag), '--calib', os.path.join(rec1, 'calib-%s.json' % tag), '--B-measurable', '4', '--synth-nonconverged', 'SK:Lneg~Onull', '--force']
idp = os.path.join(rec1, 'identity-%s.json' % tag); BASEC += (['--identity', idp] if os.path.exists(idp) else ['--no-identity'])
os.makedirs(os.path.join(WORK, 'nf1')); os.makedirs(os.path.join(WORK, 'nf2')); os.makedirs(os.path.join(WORK, 'nr'))
rc_a, o_a = run(BASEC + ['--facts', os.path.join(WORK, 'no-such-design-facts.json'), '--out', os.path.join(WORK, 'nf1', 'analysis-%s' % tag)])
rc_b, o_b = run(BASEC + ['--no-facts', '--out', os.path.join(WORK, 'nf2', 'analysis-%s' % tag)]); NF = os.path.join(WORK, 'nf2', 'analysis-%s.json' % tag); A2 = runs_A.read_json(NF) if rc_b == 0 and os.path.exists(NF) else {}
rcb2, ob2, tb2, sb2 = build(NF, os.path.join(WORK, 'nf2', 'report.md')) if A2 else (None, '', '', None)
A3 = dict(AN, reach_note=None, dev_marks=[m for m in (AN.get('dev_marks') or []) if m != 'no_facts']); NR = os.path.join(WORK, 'nr', 'analysis-%s.json' % tag)
json.dump(A3, open(NR, 'w', encoding='utf-8'), ensure_ascii=False)
rcb3, ob3, tb3, sb3 = build(NR, os.path.join(WORK, 'nr', 'report.md'))
k2 = kinds(tb2, sb2) if tb2 else []
R('T4', 'P128', '集計器は設計事実の記録が無ければ止まり、検査用の口 --no-facts だけが通して印を付ける・組み立て器は印が無いのに到達の見込みが欠ければ止まる・走査器は代わりの文字列を違反にする', '否定の経路の実験（合成の走 1 の置き場）',
  rc_a != 0 and '設計事実の記録が無い' in o_a and rc_b == 0 and 'no_facts' in (A2.get('dev_marks') or []) and A2.get('reach_note') is None
  and report_lint.FALLBACK_REACH in tb2 and '到達の見込みの記録なし' in k2 and rcb3 != 0 and '集計に到達の見込みの記録が無い' in ob3 and not os.path.exists(os.path.join(WORK, 'nr', 'report.md')),
  {'analyze_missing_facts_rc': rc_a, 'no_facts_rc': rc_b, 'no_facts_marks': A2.get('dev_marks'), 'report_nofacts_kinds': k2, 'builder_missing_reach_rc': rcb3, 'builder_tail': ob3.strip()[-160:]})
rcb4, ob4, tb4, sb4 = build(NF, os.path.join(WORK, 'nf2', 'report-allow.md'), ['--allow-dev-marks'])
k4 = kinds(tb4, sb4, allow=True) if tb4 else []
R('T5', 'P133', '走査器は集計の検査用の印が「なし」でない報告を違反にし、組み立て器の検査用の口は印を報告に残して走査に渡す', '走査器の自己検査（項 7）と合成の集計で組み立て器と走査器',
  rcl == 0 and '7 v2.1' in outl and '検査用の印' in k2 and '検査用の印' not in k4 and '検査用の口 --allow-dev-marks で組み立てた' in tb4 and '集計の検査用の印: ' in tb4,
  {'kinds_without_allow': k2, 'kinds_with_allow': k4})
gate_syn = os.path.join(rec1, 'gate-%s.json' % tag); GS = runs_A.read_json(gate_syn) if os.path.exists(gate_syn) else {}
GW = os.path.join(WORK, 'gates'); rcg, outg = run([tool('synth_gates_A.py'), '--root', GW, '--keep', '--record', os.path.join(WORK, 'gates-rec')]); gate_real = os.path.join(GW, 'gates-pass', 'records', 'gate.json')
rc6a, o6a, t6a, s6a = build(ANP, os.path.join(WORK, 'gate', 'report-synthgate.md'), ['--gate', gate_syn])
rc6b, o6b, t6b, s6b = build(ANP, os.path.join(WORK, 'gate', 'report-realgate.md'), ['--gate', gate_real]) if os.path.exists(gate_real) else (None, 'gate_A の出力が無い', '', None)
OKK = {'埋め残し', '検査用の印'}; k6a = kinds(t6a, s6a) if t6a else ['報告なし']; k6b = kinds(t6b, s6b) if t6b else ['報告なし']
R('T6', 'P129', '合成検査の門の記録が per_scenario と撤退条件の枝の欄を持ち、組み立て器が合成の門の記録でも gate_A の実物の出力でも --gate で通る（走査の違反は埋め残しと検査用の印だけ）', '実験（合成の走 1 の集計・門と校正の合成検査の置き場の gate_A の出力）',
  'per_scenario' in GS.get('gate2', {}) and 'branch' in GS.get('withdrawal', {}) and rcg == 0 and 'Traceback' not in o6a and 'Traceback' not in o6b and '門2（機械の転記）' in t6a and '門2（機械の転記）' in t6b and set(k6a) <= OKK and set(k6b) <= OKK,
  {'synthetic_gate_keys': sorted(GS.keys()), 'rc_synth_gate': rc6a, 'rc_real_gate': rc6b, 'kinds_synth_gate': k6a, 'kinds_real_gate': k6b, 'tail_a': o6a.strip()[-160:], 'tail_b': o6b.strip()[-160:]})
_, _, tn, sn = build(ANP, os.path.join(WORK, 'report', 'report.md'))
kn = kinds(tn, sn) if tn else ['報告なし']
R('T5（走査の型）', 'P128・P133', '合成の集計で組み立てた報告の走査の違反が埋め残しと検査用の印だけ（組み立て器が機械の区画の外に未登録の数を書かない）・--no-facts の集計を --allow-dev-marks で組んだ報告は埋め残しと到達の見込みの欠けだけ', '合成の集計で組み立て器と走査器',
  set(kn) <= OKK and set(k4) <= {'埋め残し', '到達の見込みの記録なし'}, {'normal': kn, 'allow_no_facts': k4})
ln_ = tn.split('\n'); hi = next((i for i, l in enumerate(ln_) if l.startswith('| 効果種 |')), None); reach_rows = []
if hi is not None:
    j = hi
    while j < len(ln_) and ln_[j].startswith('|'):
        reach_rows.append(ln_[j]); j += 1
cells = [l.count('|') - 1 for l in reach_rows]
EXTRA['report_reach_table_cells'] = cells

# ---- 1-B T11. 凍結器（写しの木）
FW = os.path.join(WORK, 'freeze-clone')
shutil.copytree(REPO, FW, ignore=lambda d, names: [n for n in names if n == '__pycache__' or (os.path.abspath(d) == os.path.abspath(REPO) and n in ('.git', 'results'))])
FZ = lambda *args_: run([os.path.join(FW, 'tools', 'freeze_A.py')] + list(args_), cwd=FW)
mf_glob = lambda: sorted(glob.glob(os.path.join(FW, 'records', 'freeze-A-*.json')))
rc_c0, o_c0 = run([tool('freeze_A.py'), '--check'])
for f in ('records/A/identity-screen-A.json', 'records/A/identity-screen-A.md', 'records/A/firth-check-A.json', 'records/A/firth-check-A.md'):
    p = os.path.join(FW, f)
    if not os.path.exists(p):
        open(p, 'w', encoding='utf-8', newline='\n').write('{"placeholder": "verify_reflection_final_A の写しの木の中だけの置き物"}\n' if f.endswith('.json') else '写しの木の中だけの置き物（verify_reflection_final_A）\n')
shutil.copyfile(os.path.join(FW, a.draft), os.path.join(FW, 'design', 'design-stageA-FROZEN.md')); shutil.copyfile(os.path.join(FW, a.draft[:-3] + '.src.md'), os.path.join(FW, 'design', 'design-stageA-FROZEN.src.md'))
rc_c1, o_c1 = FZ('--check')
rc_p, o_p = FZ('--design', 'design/design-stageA-FROZEN.md'); mfs = mf_glob(); MF = runs_A.read_json(mfs[-1]) if mfs else {}
rc_v, o_v = FZ('--verify', os.path.relpath(mfs[-1], FW)) if mfs else (None, '')
fp = os.path.join(FW, 'design', 'design-stageA-FROZEN.md'); keep_d = open(fp, encoding='utf-8').read()
tamp = re.sub(r'(`design/contrasts-A\.json`〔SHA16 )([0-9A-F]{16})(〕)', lambda m: m.group(1) + '0' * 16 + m.group(3), keep_d, count=1)
open(fp, 'w', encoding='utf-8', newline='\n').write(tamp); n0 = len(mf_glob()); rc_t, o_t = FZ('--design', 'design/design-stageA-FROZEN.md'); n1 = len(mf_glob()); open(fp, 'w', encoding='utf-8', newline='\n').write(keep_d)
bp = os.path.join(FW, 'tools', 'report_lint.py'); keep_b = open(bp, encoding='utf-8').read(); guard = "if __name__ == '__main__':"
open(bp, 'w', encoding='utf-8', newline='\n').write(keep_b.replace(guard, "if __name__ == '__main__' and '--selftest' in __import__('sys').argv:\n    __import__('sys').exit(3)\n" + guard, 1))
n2 = len(mf_glob()); rc_s, o_s = FZ('--design', 'design/design-stageA-FROZEN.md'); n3 = len(mf_glob()); open(bp, 'w', encoding='utf-8', newline='\n').write(keep_b)
import freeze_A
N6 = ['records/A/power-grid-A.json', 'records/A/design-facts-A.json', 'tools/run_preamble_local.py', 'tools/cost_facts.py', 'tools/response_mode_M.py', 'tools/response_mode_F.py']
fl = freeze_A.file_list('design/design-stageA-FROZEN.md')
R('T11', 'P107・P131・P110', '凍結器 v3: --check は欠けで終了コード 2・発行の前に自己検査を走らせて合否と器の SHA16 をマニフェストに書く・凍結本文の正本 SHA16 が現物と違えば発行しない・自己検査が通らなければ発行しない・対象一覧に器材の入力六つ', '実験（写しの木・置き物の門0.5 と Firth の記録・草案9 を凍結本文の名で置く）',
  rc_c0 == 2 and '発行はできない' in o_c0 and rc_c1 == 0 and rc_p == 0 and len(MF.get('selftests', [])) == len(freeze_A.SELFTESTS) and all(s['rc'] == 0 and len(s['sha16']) == 16 for s in MF.get('selftests', []))
  and MF.get('design_contrasts_sha16') == runs_A.sha16_file(runs_A.CPATH) and 'public_check' in MF and rc_v == 0 and tamp != keep_d and rc_t != 0 and '凍結本文に書かれた正本の SHA16' in o_t and n1 == n0
  and keep_b.count(guard) >= 1 and rc_s != 0 and '自己検査が通らない器' in o_s and 'report_lint.py' in o_s and n3 == n2 and all(x in fl for x in N6),
  {'check_repo_rc': rc_c0, 'check_clone_rc': rc_c1, 'publish_rc': rc_p, 'selftests': [(s['tool'], s['rc']) for s in MF.get('selftests', [])], 'verify_rc': rc_v, 'tamper_rc': rc_t, 'tamper_tail': o_t.strip()[-120:],
   'broken_selftest_rc': rc_s, 'broken_tail': o_s.strip()[-120:], 'six_inputs_in_scope': {x: x in fl for x in N6}})
EXTRA['freeze_clone'] = {'publish_tail': o_p.strip()[-200:], 'manifest_files': len(MF.get('files', {})), 'selftests': MF.get('selftests')}

# ---- 1-C. 格子（G1〜G3）
old = json.loads(subprocess.run(['git', '-C', REPO, 'show', '%s:records/A/power-grid-A.json' % BASE_COMMIT], capture_output=True).stdout.decode('utf-8'))
new = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'power-grid-A.json'))


def cmpv(n, o, path, out, rounded):
    if isinstance(o, dict):
        if not isinstance(n, dict):
            out.append((path, '型')); return
        for k in o:
            if k not in n:
                out.append(('%s.%s' % (path, k), '欠け')); continue
            cmpv(n[k], o[k], '%s.%s' % (path, k), out, rounded)
    elif isinstance(o, list):
        if not isinstance(n, list) or len(n) != len(o):
            out.append((path, '長さ')); return
        for i, (x, y) in enumerate(zip(n, o)):
            cmpv(x, y, '%s[%d]' % (path, i), out, rounded)
    elif rounded and isinstance(o, float) and isinstance(n, (int, float)) and not isinstance(n, bool):
        if not (n == o or any(round(n, d) == o for d in range(0, 13))):   # E は丸めの前の値を保存する（v3.2 の値が丸めの一つと一致すればよい・採否表 P123）
            out.append((path, '値', n, o))
    elif n != o:
        out.append((path, '値', n, o))


SKIP = {'version', 'generated_utc', 'inputs', 'elapsed_s'}; GD = {}
for k in old:
    if k in SKIP:
        continue
    d_ = []
    if k not in new:
        d_.append((k, '欠け'))
    else:
        cmpv(new[k], old[k], k, d_, rounded=(k == 'E'))
    GD[k] = d_
ndiff = sum(len(v) for v in GD.values()); EXTRA['grid_diff'] = {k: len(v) for k, v in GD.items()}; EXTRA['grid_diff_examples'] = [x for v in GD.values() for x in v][:10]
R('G1', 'P121・P132・P123', '格子 v3.3 の既存の節の数値が v3.2（コミット 150dab4）と差のある値零で一致する（E は丸めの前の値を保存し、丸めた値が一致すればよい・足した鍵は比べない）', '節ごとの数値の突合（機械）',
  new.get('version') == 'v3.3' and not new.get('quick') and old.get('version') == 'v3.2' and ndiff == 0, {'diff_per_section': EXTRA['grid_diff'], 'examples': EXTRA['grid_diff_examples']})
DRO = new.get('DR_opp') or []; room_keys = {(r['id'], r['ctrl_trend']) for r in new.get('DR', []) if r.get('delta_value') not in (0, 0.0)}; opp_keys = {(r['id'], r['ctrl_trend']) for r in DRO}
R('G2', 'D28', '格子に逆向きの節（既測基底の対比 × 三型 × 逆向き）があり、乱数は別の子ストリーム', '格子の記録',
  bool(DRO) and all(r.get('direction') == 'opposite' for r in DRO) and new['streams'].get('DR_opp') == 10 and list(new['streams'].values()).count(10) == 1 and new['B'].get('DR_opp') == new['B'].get('DR') and opp_keys == room_keys,
  {'rows': len(DRO), 'stream': new['streams'].get('DR_opp'), 'B': new['B'].get('DR_opp'), 'keys_equal_room': opp_keys == room_keys, 'n_room_keys': len(room_keys)})
G_ = new.get('G') or {}
R('G3', 'P122', '格子の G 節に 12 セルをまたいだ率（注・判定保留・独立の近似の注）がある', '格子の記録',
  G_.get('cells_per_contrast') == 2 * len(T['sizes']) and bool(G_.get('union_independent')) and '独立' in (G_.get('union_note') or ''), {k: G_.get(k) for k in ('cells_per_contrast', 'union_note')})

# ---- 1-C. 転記行（F1〜F6）
R('F0', '—', '設計事実 v3.3 が現行の正本と格子から検査用の印なしで作られた', '設計事実',
  FACTS.get('generator') == 'tools/design_facts_A.py v3.3' and not FACTS.get('dev_marks') and FACTS.get('contrasts_sha16') == runs_A.sha16_file(runs_A.CPATH) and FACTS.get('power_grid_json_sha16') == runs_A.sha16_file(os.path.join(REPO, 'records', 'A', 'power-grid-A.json')),
  {k: FACTS.get(k) for k in ('generator', 'dev_marks', 'contrasts_sha16', 'power_grid_json_sha16')})
R('F1', 'P125', '転記行 A に校正腕のセッション数の内訳（32B が 2）と下界のセッション数と試行数', '設計事実', has(FD['A']['text'], '複数のセッションの機種: 32B が 2', '下界のセッション数') and 'calibration_sessions' in FD['A']['data'], FD['A']['text'][:200])
FDt = FD['D']['text']
R('F2', 'P118・P120・D27〜D29', '転記行 D に測れた効果種の B と DR 節の B の対応・両向きの効果種ごとの到達と区間と測れた対比の本数・格子の解釈条項の発火率が除外を入れない配置の値である旨', '設計事実',
  has(FDt, '測れた効果種の B', 'DR_opp', '除外を入れない配置', '余地のある向き', '逆向き', '区間', '測れた対比') and FD['D']['data'].get('B_measurable') == ME['B_per_contrast'] and FD['D']['data'].get('B_DR') == new['B'].get('DR') and 'blind_all_trends_opposite' in FD['D']['data'],
  lacks(FDt, '測れた効果種の B', 'DR_opp', '除外を入れない配置', '余地のある向き', '逆向き', '区間', '測れた対比'))
R('F3', 'P123', '転記行 E を生値から一度で丸める（境界の実サイズ 0.0264・単一セル 0.996）', '設計事実', has(FD['E']['text'], '境界での実サイズ 0.0264', '単一セル 0.996'), FD['E']['text'][:200])
R('F4', 'D34', '転記行 F に時間貸しに移す機種を除いた上界とその停止規則の閾値', '設計事実', bool(FD['F']['data'].get('rental_adjust')) and has(FD['F']['text'], '32B を除いた上界 123.2 ユニット', '153.9 ユニット'), FD['F']['data'].get('rental_adjust'))
R('F5', 'P122', '転記行 G に 12 セルをまたいだ率', '設計事実', has(FD['G']['text'], 'セルのどれかが超える率', '独立を近似'), lacks(FD['G']['text'], 'セルのどれかが超える率', '独立を近似'))
R('F6', 'P124', '転記行 M で確証族の 8 腕の値が先、13 腕の値が括弧', '設計事実', bool(re.search(r'確証族に現れる \d+ 腕のいずれかが超える確率 [0-9.]+（全 \d+ 腕では [0-9.]+）', FD['M']['text'])), FD['M']['text'][:200])

# ---- 1-C. 草案9・雛形・README（R1〜R4）
D9S = SRC(a.draft[:-3] + '.src.md'); D9 = SRC(a.draft) if os.path.exists(os.path.join(REPO, a.draft)) else ''
R1W = ('率盲検の外の経路（採否表 P104・P138・裁定 D35）', '自分の起草物と器材の見落とし（草案8 と器材）', '(xvi) **測れた効果種（裁定 D11・D29）**', '測れた対比でない場面については傾向の不在を書かない',
       '(xvii) **区間の被覆（裁定 D31）**', '裁定 D27・D28', '裁定 D30', '`firth_check.failure_options`', '裁定 D12 (e)・D34', '`calibration.claim_release`', '`judge_validity.extract.echo`', '- D26 運用の解釈の項', '- D35 率盲検の外の経路')
R('R1', 'D26・D29〜D35', '草案9 の原稿に §0 の新しい項・読み条項 (xvi) の拡張と (xvii)・測れた効果種の文言・抽出検査・Firth の選べる手・時間貸し・初点の名乗りの移し替え・§5 の D26〜D35', '原稿の文字列', has(D9S, *R1W), lacks(D9S, *R1W))
m6 = re.search(r'`design/contrasts-A\.json`〔SHA16 ([0-9A-F]{16})〕・`records/A/power-grid-A\.json`〔SHA16 ([0-9A-F]{16})〕', D9)
R('R2', '—', '草案9 の組み立ての数の検査の違反が零・§6 の見出しの正本と格子の SHA16 が現物と一致', '数の検査の記録と組み立て',
  '違反の合計: 0' in L9 and '束縛検査（原稿 `design/design-stageA-draft9.src.md`）: 違反 0' in L9 and bool(m6) and m6.group(1) == runs_A.sha16_file(runs_A.CPATH) and m6.group(2) == runs_A.sha16_file(os.path.join(REPO, 'records', 'A', 'power-grid-A.json')) and '〔転記行 A〕' not in D9,
  {'lint_total_zero': '違反の合計: 0' in L9, 'section6': m6.groups() if m6 else None})
TS = SRC('records/A/results-report-template-A.src.md'); LT = SRC('records/A/numbers-lint-template-A.md') if os.path.exists(os.path.join(REPO, 'records', 'A', 'numbers-lint-template-A.md')) else ''
R3W = ('`print_strings.measurable_coverage`', '- 測れた対比の本数（効果種ごと', '余地のある向き／逆向き', '- 区間の被覆（`print_strings.interval_note`', '目視の分類と機械分類の一致', '- 断片の復唱（`judge_validity.extract.echo`', '(i)〜(xvii)',
       '走査器が違反も埋め残しも無しに終わること', '(xiii) の交絡')
R('R3', 'D29・D31・D32・P141・P145・P146', '雛形に §0-7 と §1 の測れた対比の欄・§4 の到達の表の両向きと区間の列・区間の被覆の断り・抽出検査の一致の行・断片の復唱の行があり、雛形の数の検査の違反が零・組み立て器の到達の表の列数が雛形の見出しと一致',
  '雛形の原稿と数の検査の記録と合成の集計での組み立て',
  has(TS, *R3W) and '違反の合計: 0' in LT and not freeze_A.frames_check(T) and bool(cells) and len(set(cells)) == 1 and cells[0] == 6 and any('~' in r_ for r_ in reach_rows[2:]) and PS['interval_note'] in tn and '解釈条項の発火' in tn,
  {'missing': lacks(TS, *R3W), 'template_lint_zero': '違反の合計: 0' in LT, 'frames': freeze_A.frames_check(T), 'reach_table_cells': cells})
RM = SRC('README.md'); R4W = ('設計草案9', '設計草案8', '設計草案7', 'records/reviews/A/draft7-impl/', 'records/reviews/A/final/adoption-table-A-final.md', 'P105〜P153', 'D26〜D35', '門0.5（Colab・起動器の最初の実機の走行）')
R('R4', 'P111', 'README に草案7・8、実装検分、最終検分、この反映、次の手順が載る', 'README', has(RM, *R4W), lacks(RM, *R4W))
R('P107（公開物）', 'P107', '凍結器が公開物をコミットと main の両方で照合できる', '凍結器の原稿', has(SRC('tools/freeze_A.py'), "a.commit == 'main'", '--verify-public', 'raw.githubusercontent.com'))

ok = all(r['ok'] for r in ROWS); secs = int(time.time() - T0)
PRE = os.path.join(REPO, 'records', 'reviews', 'A', 'final', 'preregistration-reflection-final-A.md')
RES = {'kind': 'verification_reflection_final_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'seconds': secs, 'pass': ok, 'rows': ROWS, 'extra': EXTRA,
       'inputs': {'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), 'power_grid_sha16': runs_A.sha16_file(os.path.join(REPO, 'records', 'A', 'power-grid-A.json')), 'design_facts_sha16': runs_A.sha16_file(os.path.join(REPO, 'records', 'A', 'design-facts-A.json')),
                  'grid_base_commit': BASE_COMMIT, 'synth_A': a.synth, 'synth_gates_A': a.synth_gates, 'draft': a.draft, 'preregistration_sha16': runs_A.sha16_file(PRE)}, 'clause': CLAUSE}
json.dump(RES, open(a.out + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
M = ['# 反映の確かめ（凍結前の最終検分の採否表 P105〜P153・登録者裁定 D26〜D35・機械生成・`tools/verify_reflection_final_A.py` %s・%s UTC・%d 秒）' % (VERSION, RES['generated_utc'], secs), '',
     '- 事前登録: `records/reviews/A/final/preregistration-reflection-final-A.md`（SHA16 %s・反映の前に記した・SHA-256 は `verify.log` の [prereg-reflection]）。' % RES['inputs']['preregistration_sha16'],
     '- 入力: 正本 SHA16 %s・格子 SHA16 %s（比べた v3.2 はコミット %s）・設計事実 SHA16 %s・合成検査の記録 `%s`・門と校正の合成検査の記録 `%s`・草案 `%s`。' % (
         RES['inputs']['contrasts_sha16'], RES['inputs']['power_grid_sha16'], BASE_COMMIT[:7], RES['inputs']['design_facts_sha16'], a.synth, a.synth_gates, a.draft),
     '- 判定: **%s**（%d 項目中 %d 項目が直った条件に一致）。' % ('すべて一致' if ok else '不一致あり', len(ROWS), sum(r['ok'] for r in ROWS)), '',
     '| 条件 | 項 | 直った条件 | 確かめ | 結果 | 詳細（不一致のとき） |', '|---|---|---|---|---|---|']
M += ['| %s | %s | %s | %s | %s | %s |' % (r['cond'], r['item'], r['condition'], r['method'], '一致' if r['ok'] else '**不一致**', '' if r['ok'] else r['detail'].replace('|', '／').replace('\n', ' ')) for r in ROWS]
M += ['', '## 格子の節ごとの差の数（v3.3 対 v3.2・G1）', '', '| 節 | 差のある値 |', '|---|---|'] + ['| %s | %d |' % (k, v) for k, v in EXTRA['grid_diff'].items()]
M += ['', '## 凍結器の写しの木の実験（T11）', '',
      '- 写しの木: リポジトリから results と .git を除いて写し、門0.5 と Firth の一致検査の記録を置き物で埋め、草案9 を凍結本文の名で置いた（写しの木の中だけ・リポジトリの現物は変えない）。',
      '- 発行したマニフェストの対象 %d ファイル・自己検査 %s。' % (EXTRA['freeze_clone']['manifest_files'], '・'.join('%s rc %d' % (s['tool'], s['rc']) for s in (EXTRA['freeze_clone']['selftests'] or []))),
      '- 否定の経路: 凍結本文の §6 の見出しの正本 SHA16 を零に書き換えると発行しない／写しの木の `report_lint.py` の自己検査を終了コード 3 で落とすと発行しない（どちらもマニフェストは増えない）。']
M += ['', '## 検分票', '', '- 対象: 採否表 P105〜P153 と登録者裁定 D26〜D35 の反映（正本 v2.5・器材・格子 v3.3・設計事実 v3.3・草案9・報告雛形・運用の解釈の一覧・README）。',
      '- 段階: 事前登録あり（`preregistration-reflection-final-A.md`・反映の前に SHA-256 を記帳）。確かめの器の個々の判定の書き方（どの文字列を探すか・どの実験を置くか）は、反映の実装の後に本器を書くときに決めた（事後）。',
      '- 凍結物の同定: 凍結走行器 v2.7・凍結パーサ・盤の台帳（写しの木で読むだけ）。格子 v3.2 はコミット 150dab4 の公開物と比べた。',
      '- 盲検の状態: 該当なし（率を見る前）。',
      '- 敵対的検分: 直った条件を否定の経路と変異で確かめた（設計事実の欠け・到達の見込みの欠け・検査用の印・凍結本文の SHA16 の書き換え・自己検査の失敗・合成検査の変異 M1〜M10）。格子は既存の節の数値を全件突合した。',
      '- 系統の内訳: 確かめはコーディネータ（Claude Opus 5）の器。この反映は系統外の目を通らない（この後に検分の巡を置かない・登録者決定）。',
      '- COI 記録: 反映を早く終えて門0.5 へ進みたい。印＝直った条件を先に書き、不一致を表の先頭の判定に出し、器と記録を公開する。',
      '- 判定: %s。' % ('反映を確かめた（門0.5 へ）' if ok else '不一致の項を直してから確かめ直す'),
      '- 本検分が確認していないこと: 合成の走行は本物の出力の分布を再現しない。起動器は Colab の実機で走らせていない。集計時の測れた効果種の計算の実時間（B=10,000・両向き）は測っていない（合成の走行は B=4）。'
      '抽出検査の封印と一致、判定器の断片の復唱の測定は、合成の走行と自己検査でしか通していない。凍結器の発行は写しの木の置き物の記録で試しただけで、門0.5 と Firth の一致検査の実物の記録では試していない。'
      '文字列の突合は、文言があることを確かめ、文言が設計として正しいかは確かめない。確かめの器の判定の書き方は事後に決めた。', '', CLAUSE]
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[verify_reflection_final_A] %s（%d/%d・%d 秒）written %s.{md,json}' % ('PASS' if ok else 'FAIL', sum(r['ok'] for r in ROWS), len(ROWS), secs, a.out))
sys.exit(0 if ok else 1)
