# -*- coding: utf-8 -*-
"""器の直しの確かめ（登録者裁定 D238）の四名の票（G1・G2・C1・C2）の事実の主張を、束の入力のコミット（b77dd22・器と正本は直しのコミット a8ac5ad と同じ）で確かめる。
束の入力のコミットを一時の置き場に複製して（`git clone --shared`）、行を読み、振る舞いは一時の置き場でだけ再現する（実の重みを読まない・リポジトリの作業木に書かない）。
方向の記録（`results/Bl3/`・コミットに入っていない）は、作業木から一時の複製に写して使う。記録には一時の置き場の道筋を書かない（決まった言い方に置き換える）。
用法: python records/reviews/Bl3/fixcheck/checks/verify_fixcheck_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, glob, shutil, hashlib, tempfile, subprocess, importlib, collections, contextlib, io

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
SRC = 'b77dd22'
NL = chr(10)
OUT_DIR = os.environ.get('VERIFY_OUT') or HERE                  # 試しの走りだけ一時の置き場に書く（記録は一度だけ）
OUT_MD = os.path.join(OUT_DIR, 'verification-fixcheck-Bl3.md')
OUT_JS = os.path.join(OUT_DIR, 'verification-fixcheck-Bl3.json')
for p in (OUT_MD, OUT_JS):
    assert not os.path.exists(p), '既にある（一度だけ）: ' + p
TD = tempfile.mkdtemp(prefix='fixcheck-verify-')
CL = os.path.join(TD, 'clone')
subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', REPO, CL], check=True)
subprocess.run(['git', '-C', CL, 'checkout', '-q', SRC], check=True)
HEAD = subprocess.run(['git', '-C', CL, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
for f in ('results/Bl3/directions-Bl3.json', 'results/Bl3/directions-Bl3.npz'):
    os.makedirs(os.path.dirname(os.path.join(CL, f)), exist_ok=True)
    shutil.copyfile(os.path.join(REPO, f), os.path.join(CL, f))
sys.path.insert(0, os.path.join(CL, 'tools'))
sys.path.insert(0, os.path.join(CL, 'tools', 'colab'))
T = lambda rel: open(os.path.join(CL, *rel.split('/')), encoding='utf-8').read()
LINES = lambda rel: T(rel).split(NL)
clean = lambda s: str(s).replace(CL, '〈一時の複製〉').replace(CL.replace('\\', '/'), '〈一時の複製〉').replace(TD, '〈一時の置き場〉').replace(TD.replace('\\', '/'), '〈一時の置き場〉')
ROWS = []


def rec(no, claim, how, result, detail):
    ROWS.append({'no': no, 'claim': claim, 'how': how, 'result': result, 'detail': clean(detail)})
    print('[verify]', no, result, clean(detail)[:200])


def find(rel, pat):
    return [i + 1 for i, l in enumerate(LINES(rel)) if re.search(pat, l)]


def body_of(rel, fname):
    L = LINES(rel)
    s = [i for i, l in enumerate(L) if re.match(r'^def %s\(' % re.escape(fname), l)]
    assert len(s) == 1, (rel, fname)
    e = next((j for j in range(s[0] + 1, len(L)) if re.match(r'^(def |class |if __name__|[A-Z_]+ = )', L[j])), len(L))
    return s[0] + 1, NL.join(L[s[0]:e])


T3 = json.loads(T('design/contrasts-Bl3.json'))
FJ = json.loads(T('records/Bl3/design-facts-Bl3.json'))
DJ = json.load(open(os.path.join(CL, 'results/Bl3/directions-Bl3.json'), encoding='utf-8'))
pair_names = list(DJ['groups']['real']['names'])
os.environ['OP4B_REPO_DIR'] = CL
import analyze_Bl3 as AZ
import freeze_Bl3 as FZ
import bl3_core as K
assert os.path.abspath(AZ.REPO) == os.path.abspath(CL) and os.path.abspath(FZ.REPO) == os.path.abspath(CL), '一時の複製の器を読んでいない'

# ---------------- C2-1: 凍結の本文の器が正しい流れで止まり、本文に一時の道筋が入る ----------------
ln71 = LINES('tools/build_draft_Bl3.py')[70]
st = subprocess.run([sys.executable, 'tools/make_frozen_Bl3.py', '--selftest'], cwd=CL, capture_output=True, text=True, encoding='utf-8', errors='replace')
r = subprocess.run([sys.executable, 'tools/make_frozen_Bl3.py', '--words', '（確かめのための仮の言葉）', '--commit', 'deadbee', '--date', '2026-09-26 00:00'],
                   cwd=CL, capture_output=True, text=True, encoding='utf-8', errors='replace')
fout = os.path.join(CL, 'design', 'design-Bl3-FROZEN.md')
ftxt = open(fout, encoding='utf-8').read() if os.path.exists(fout) else ''
standin_lines = [l for l in ftxt.split(NL) if 'frozen-standin.src.md' in l]
outside = [l for l in standin_lines if '../' in l or '..\\' in l]
import make_frozen_Bl3 as MFB
a1, a2 = os.path.join(TD, 'b1.md'), os.path.join(TD, 'b2.md')
fsrc_ = os.path.join(CL, 'design', 'design-Bl3-FROZEN.src.md')
d12 = []
if os.path.exists(fsrc_):
    MFB.build_frozen(fsrc_, a1, os.path.join(TD, 'lint.md'))                  # 二度とも同じ数の検査の置き場（器の差だけを見る）
    MFB.build_frozen(fsrc_, a2, os.path.join(TD, 'lint.md'))
    d12 = [l for l in __import__('difflib').unified_diff(open(a1, encoding='utf-8').read().split(NL), open(a2, encoding='utf-8').read().split(NL), n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]
rec_sha = [m_.group(1) for l in standin_lines for m_ in [re.search(r'frozen-standin\.src\.md` SHA16 ([0-9A-F]{16})', l)] if m_]
real_sha = MFB.sha16f(fsrc_) if os.path.exists(fsrc_) else None
rec('C2-1', '凍結の本文の器は、代わりの行を置いた一時の原稿から組むので、組み立ての記録の行に一時の原稿の道筋と SHA16 が入り、組み直すたびに違う本文になって、正しい流れでも止まる',
    '組み立ての器の 71 行を読み、一時の複製で凍結の本文の器の自己検査と、仮の言葉での端から端まで（--words・--commit・--date）を走らせ、同じ凍結版の原稿を二度組んで比べた',
    '再現した' if (r.returncode != 0 and '凍結版の原稿を組み直した本文が、凍結の本文と違う' in (r.stdout + r.stderr) and standin_lines and len(d12) == 2 and rec_sha and rec_sha[0] != real_sha) else '再現しない',
    '組み立ての器の 71 行は原稿の道筋と SHA16 を書く（%s）・自己検査の終わりの値 %d・端から端までの終わりの値 %d（%s）・凍結の本文の中の代わりの原稿の道筋の行 %d（リポジトリの外を指す行 %d）・その行の原稿の SHA16 %s と凍結版の原稿の実の SHA16 %s・同じ手順で二度組んだ本文の差 %d 行（%s）' % (
        'rel(a.src), sha(a.src)' in ln71, st.returncode, r.returncode, [l for l in (r.stdout + r.stderr).split(NL) if '外れた' in l][:1], len(standin_lines), len(outside), rec_sha[:1], real_sha, len(d12),
        [re.sub(r'`[^`]*frozen-standin\.src\.md`', '`〈一時の原稿〉`', x)[:120] for x in d12]))

# ---------------- C2-2: 一致だけを見る段の後に凍結の記録へ台帳を足すと、結果を開く段が止まる ----------------
frp = os.path.join(TD, 'FR.json')
FRd = {'frozen_sha16': {}, 'main_freeze': {'frozen_sha16': {}}, 'deviations': []}
json.dump(FRd, open(frp, 'w', encoding='utf-8'), ensure_ascii=False)
AZ.FR_PATH = frp
files = {'main': {'dir': 'x', 'json_sha256': 'A' * 64, 'session_sha256': 'B' * 64}}
J = {'agree': True, 'first': True, 'second': True, 'inputs': files, 'freeze_record_sha16': AZ.sha16f(frp)}


def open_msg(FRx):
    try:
        AZ.open_checked(T3, FJ, {}, {'main': {'dry': False}}, files, J, [], pair_names, None, None, None, FR=FRx, judge_sha16='0' * 16, repo=CL)
        return 'SystemExit なし'
    except SystemExit as e_:
        return str(e_)
    except Exception as e_:
        return '%s: %s' % (type(e_).__name__, e_)
m_before = open_msg(FRd)
FRd['deviations'].append({'no': 'X', 'kind': 'recompute_values', 'note': '値だけが許容の外（札は同じ）・裁定 D234 の台帳の行（合成）'})
json.dump(FRd, open(frp, 'w', encoding='utf-8'), ensure_ascii=False)
m_after = open_msg(FRd)
rec('C2-2', '一致だけを見る段は凍結の記録のファイル全体の SHA16 を置き、結果を開く段はそれと今のファイル全体を照らすので、間に台帳の行を足すと開く段が止まる',
    '一時の凍結の記録を置いて一致だけを見る段の記録を合成し、台帳の行を足す前と後で結果を開く段の確かめに当てた（DRY でない組）',
    '再現した' if ('凍結の記録が一致だけを見る段の後に変わった' in m_after and '凍結の記録が一致だけを見る段の後に変わった' not in m_before) else '再現しない',
    '足す前: %s／足した後: %s' % (m_before[:80], m_after[:80]))
AZ.FR_PATH = os.path.join(CL, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')

# ---------------- G2-新1・C1-新1・C2-6: 起動器が書く組の SHA-256 を集計の器が読まない ----------------
readers = sorted(set(os.path.relpath(p, CL).replace(os.sep, '/') for p in glob.glob(os.path.join(CL, 'tools', '**', '*.py'), recursive=True) if 'part_sha256' in open(p, encoding='utf-8').read()))
dd = os.path.join(TD, 'out-main')
os.makedirs(dd)
json.dump({'dry': False, 'part_sha256': {'main': '0' * 64}}, open(os.path.join(dd, 'session.json'), 'w', encoding='utf-8'))
json.dump({'cells': {}}, open(os.path.join(dd, 'main.json'), 'w', encoding='utf-8'))
try:
    ps, ss, fs = AZ.load_outputs([dd])
    lo = '止まらなかった（読んだ組の SHA-256 %s…・session の記録 %s…）' % (fs['main']['json_sha256'][:8], '0' * 8)
except SystemExit as e_:
    lo = '止まった: %s' % e_
rec('G2-新1・C1-新1・C2-6', '起動器が session に書く組の出力の SHA-256（part_sha256）を、集計の器は読まず、手元のファイルから取り直すだけ',
    '束の入力のコミットの器で part_sha256 を読む器を探し、組の JSON と食い違う part_sha256 を持つ session を集計の器の読み込みに与えた',
    '再現した' if ('tools/analyze_Bl3.py' not in readers and lo.startswith('止まらなかった')) else '再現しない',
    'part_sha256 が出る器 %s・読み込み %s' % (readers, lo))

# ---------------- G1-2-1・G2-新2・C1-新2・C2-3: 報告の組み立ては一致だけを見る段の記録・DRY の印・読んだ出力を照らさない ----------------
l0, b_li = body_of('tools/build_report_Bl3.py', 'load_inputs')
l1, b_sf = body_of('tools/build_report_Bl3.py', 'sealed_and_frozen_bad')
sw = LINES('tools/sweep_Bl3.py')
rec('G1-2-1・G2-新2・C1-新2・C2-3', '報告の組み立ては、一致だけを見る段の記録（judge-Bl3.json）と、集計の記録の judge_record_sha16・inputs・dry を照らさない。掃き出しも judge_record_sha16 を求めず、DRY なら等方の本数を問わない',
    '報告の組み立ての load_inputs と sealed_and_frozen_bad の本体と、掃き出しの器の行を読んだ',
    '再現した' if (('judge' not in b_li and 'judge' not in b_sf and "'dry'" not in b_li and "'inputs'" not in b_li) and not any('judge_record' in l for l in sw)) else '再現しない',
    'load_inputs（%d 行から）に judge %s・dry %s・inputs %s／掃き出しの judge_record_sha16 %s・DRY で等方の本数を問わない行 %s' % (
        l0, 'judge' in b_li, "'dry'" in b_li, "'inputs'" in b_li, any('judge_record' in l for l in sw), [i + 1 for i, l in enumerate(sw) if "A.get('dry')" in l]))

# ---------------- C1-新2・C2-6: 一致だけを見る段が置く封印の SHA16 を結果を開く段が照らさない ----------------
l2, b_oc = body_of('tools/analyze_Bl3.py', 'open_checked')
l3, b_jd = body_of('tools/analyze_Bl3.py', 'judge')
rec('C1-新2・C2-6', '一致だけを見る段は封印の記録の SHA16（sealing_record_sha16）を置くが、結果を開く段は照らさない。報告の頭の封印の照らしは手元の三つのファイルの間だけ',
    '集計の器の judge と open_checked の本体・報告の組み立ての sealed_and_frozen_bad を読んだ',
    '再現した' if ('sealing_record_sha16' in b_jd and 'sealing_record_sha16' not in b_oc and 'git' not in b_sf) else '再現しない',
    'judge（%d 行から）が置く %s・open_checked（%d 行から）が照らす %s・報告の封印の照らしに git の錨 %s' % (l3, 'sealing_record_sha16' in b_jd, l2, 'sealing_record_sha16' in b_oc, 'git' in b_sf))

# ---------------- C1-新3・C2-12: 手元の本の凍結の下見の記録を、相 main の出力とコミットに結ばない ----------------
bt = T('tools/colab/boot_Bl3.py')
rec('C1-新3・C2-12', '一致だけを見る段と結果を開く段は、手元の凍結の記録の下見（外した升目・揺れの床）を使い、相 main の出力の外した升目とバッチ・session のコミットの凍結の記録・session の正本と npz を、凍結の記録と照らさない',
    '集計の器の judge と open_checked の本体を読み、相 main の出力の dropped・batch と session のコミットの凍結の記録を読む行を探した',
    '再現した' if (not re.search(r"\['main'\]\.get\('dropped'\)|\['main'\]\['dropped'\]|'batch'", b_jd + b_oc) and 'git' not in b_jd + b_oc and "FR['frozen_sha16']" not in b_jd) else '一部',
    '相 main の外した升目・バッチを照らす行 %s・git の行 %s・session の正本を凍結の記録と照らす行 %s（組の間の食い違いだけを見る STRICT_ENV）・起動器が session に書く使った下見の記録 %s・それを二つの段が読む %s' % (
        bool(re.search(r"\['main'\]\.get\('dropped'\)|\['main'\]\['dropped'\]|'batch'", b_jd + b_oc)), 'git' in b_jd + b_oc, "FR['frozen_sha16']" in b_jd,
        ['%d: %s' % (i + 1, l.strip()[:90]) for i, l in enumerate(bt.split(NL)) if "SESSION['pilot_used']" in l][:2], 'pilot_used' in b_jd + b_oc))

# ---------------- C1-新4: 照らす器の一覧が手書きで閉包と読む入力から漏れる ----------------
fc_tools = [f for f in AZ.FROZEN_CHECK if f.startswith('tools/')]
clo = FZ.import_closure(fc_tools)
miss_clo = sorted(set(clo) - set(AZ.FROZEN_CHECK))
ff = set(FZ.frozen_files(T3))
reads = {'records/B/analysis-B-2026-09-22.json': None, 'results/Blens/calib-Blens.json': None, 'records/Blens/design-facts-Blens.json': None}
trials = sorted(os.path.relpath(p, CL).replace(os.sep, '/') for p in glob.glob(os.path.join(CL, 'results', 'stageB', '*', 'trials-*.jsonl')))
rec('C1-新4', '二つの段と報告の頭で照らす器の一覧（FROZEN_CHECK）は手書きで、報告の走査が読む器（numbers_lint・runs_A）と、結果を開く段が読む入力（段階 B の集計・段階 B の試行・B-lens の較正・B-lens の設計事実）が入らない',
    '一覧の器の import の閉包を凍結の器の関数で計算し、結果を開く段が読むファイルが一覧と凍結物（下見の前の凍結の frozen_files）に入るかを見た',
    '再現した' if (miss_clo and all(f not in AZ.FROZEN_CHECK for f in list(reads) + trials)) else '再現しない',
    '閉包にあって一覧に無い器 %s・読む入力で一覧に無いもの %d／%d・そのうち凍結物に入るもの %s・凍結物に入らないもの %s と段階 B の試行 %d ファイル（凍結物に入るもの %d）' % (
        miss_clo, sum(1 for f in list(reads) + trials if f not in AZ.FROZEN_CHECK), len(reads) + len(trials), sorted(f for f in reads if f in ff), sorted(f for f in reads if f not in ff), len(trials), sum(1 for f in trials if f in ff)))

# ---------------- C1-新5: DRY でない枝が正式の記録で走らない ----------------
dr = T('tools/dry_run_Bl3.py')
rec_txt = T('records/Bl3/dry-run-Bl3-2026-09-25.md')
calls_judge = [m.group(0)[:60] for m in re.finditer(r'AZ\.judge\([^\n]*', dr)]
sess_dry = re.findall(r"'dry': (True|False)", dr)
rec('C1-新5', '正式の記録は、一致だけを見る段の DRY でない枝・結果を開く段の凍結の記録の照らし・台帳で許す差分の道・起動器の相 pilot と main の封印と凍結の照らし・報告の器の CLI（load_inputs）を走らせない',
    '合成データの器の judge の呼び方と session の DRY の印と、報告の器の呼び方（build か load_inputs か）と、起動器の DRY の枝を読んだ',
    '再現した' if ('load_inputs' not in dr and 'dry_no_gate' in bt and "'dry': False" not in dr) else '一部',
    '合成データの器の judge の呼び出し %d・session の DRY の印 %s・load_inputs の呼び出し %s・起動器の DRY は凍結と封印を見ない %s・正式の記録の五の行 %d' % (
        len(calls_judge), collections.Counter(sess_dry), 'load_inputs' in dr, 'dry_no_gate' in bt, sum(1 for l in rec_txt.split(NL) if l.startswith('| 五 |'))))

# ---------------- C1-新6・C2-11: 下見のやり直しと台帳 ----------------
bl, b_mf = body_of('tools/freeze_Bl3.py', 'main_freeze_checks')
_mdr = re.search(r"'deviation_rule': '([^']*)'", T('tools/freeze_Bl3.py'))
DEVRULE = _mdr.group(1) if _mdr else ''
rec('C1-新6・C2-11', '起動器の相 pilot は下見の前の凍結の SHA16 と台帳を見ずに照らすので、器を直した後の下見のやり直しは起動器で止まる。本の凍結の器は台帳の器の差分を路ごとに最後の一件しか持たず、同じファイルを二度直すと正しい流れでも止まる。kind pilot_rerun の書き方は凍結の記録の決まりの文に無い',
    '起動器の凍結の照らしの行・本の凍結の器の台帳の組み方・凍結の記録に書く deviation_rule の文を読んだ',
    '再現した' if ("FR['frozen_sha16']" in bt and "ledgered[td['path']] = td" in b_mf and "td.get('before') != want" in b_mf and DEVRULE and 'pilot_rerun' not in DEVRULE) else '一部',
    '起動器の相 pilot の照らしの相手 %s（台帳を読む行 %s）・本の凍結の台帳 %s・前の SHA16 を凍結の値と比べる %s・deviation_rule の文に pilot_rerun %s' % (
        [l.strip()[:90] for l in bt.split(NL) if "sha_map = FR['main_freeze']['frozen_sha16'] if PHASE == 'main' else FR['frozen_sha16']" in l][:1], 'deviations' in bt,
        "ledgered[td['path']] = td" in b_mf, "td.get('before') != want" in b_mf, 'pilot_rerun' in DEVRULE))

# ---------------- C1-新7・C2-4: 門の答えの分かる合成は、門の行の家族の鍵と単位を確かめる相手から借りる ----------------
AN = json.loads(T('records/B/analysis-B-2026-09-22.json'))
rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader(CL))
units_g = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
fams = sorted({r_['fam'] for r_ in rows_gate})
fa, fb = fams[0], fams[-1]
bug_fam = json.loads(json.dumps(rows_gate))                                          # 鍵を重ねない取り違え一: 二つの家族の名をすべての行で入れ替える
for r_ in bug_fam:
    r_['fam'] = fb if r_['fam'] == fa else (fa if r_['fam'] == fb else r_['fam'])
bug_y = json.loads(json.dumps(rows_gate))                                            # 鍵を重ねない取り違え二: 二つの行の行動の量を入れ替える
ia = next(i for i, r_ in enumerate(bug_y) if r_['fam'] == fa)
ib = next(i for i, r_ in enumerate(bug_y) if r_['fam'] == fb and abs(r_['y'] - bug_y[ia]['y']) > 1e-9)
bug_y[ia]['y'], bug_y[ib]['y'] = bug_y[ib]['y'], bug_y[ia]['y']
bug = json.loads(json.dumps(rows_gate))                                              # 対照: 二つの行の家族の鍵だけを入れ替える（鍵が重なる）
ia2 = next(i for i, r_ in enumerate(bug) if r_['fam'] == fa)
ib2 = next(i for i, r_ in enumerate(bug) if r_['fam'] == fb)
bug[ia2]['fam'], bug[ib2]['fam'] = bug[ib2]['fam'], bug[ia2]['fam']


def answer_known_rho(rows):
    import numpy as np
    rng_g = np.random.default_rng(23)
    eff_g = collections.defaultdict(dict)
    for r_ in rows:
        for u in units_g:
            eff_g[r_['fam']].setdefault(u, float(rng_g.normal()))
        eff_g[r_['fam']][r_['unit']] = float(r_['y'])
    return AZ.gates(T3, rows, dict(eff_g), [], ())['main']['rho']
rho_ok, rho_fam, rho_y, rho_bug = answer_known_rho(rows_gate), answer_known_rho(bug_fam), answer_known_rho(bug_y), answer_known_rho(bug)
dline = [i + 1 for i, l in enumerate(dr.split(NL)) if "eff_g[r_['fam']][r_['unit']] = float(r_['y'])" in l]
rec('C1-新7・C2-4', '門の「答えの分かる合成」は、確かめる相手（stage_b_gate_rows）が付けた家族の鍵と単位と行動の量に効き目を置くので、その割り当ての誤りは順位相関が一のまま通る',
    '合成データの器の行を読み、門の行の割り当てを取り違えた三つの写し（二つの家族の名をすべての行で入れ替える・二つの行の行動の量を入れ替える・対照として二つの行の家族の鍵だけを入れ替えて鍵を重ねる）に、同じ組み方の確かめを当てた',
    '再現した' if (dline and abs(rho_ok - 1.0) < 1e-12 and abs(rho_fam - 1.0) < 1e-12 and abs(rho_y - 1.0) < 1e-12) else '再現しない',
    '合成データの器の行 %s・元の門の行で %.12f・家族の名の入れ替えで %.12f・行動の量の入れ替えで %.12f（どちらも一のまま＝捕まえない）・対照の鍵を重ねる入れ替えで %.12f（一にならない＝捕まえる）・家族 %s と %s' % (dline, rho_ok, rho_fam, rho_y, rho_bug, fa, fb))

# ---------------- C1-新8・C2-3: DRY の CLI が本の置き場に書く ----------------
l4, b_main = body_of('tools/analyze_Bl3.py', 'main')
rec('C1-新8・C2-3', '集計の器は DRY でも既定の書き出し先が本の置き場（records/Bl3/judge-Bl3.json・analysis-Bl3.json）で、一致だけを見る段は一度だけなので、--out を付け忘れた DRY の試しが本の置き場を先に埋める',
    '集計の器の main の本体を読んだ',
    '再現した' if ('out = a.out or JUDGE' in b_main and 'out = a.out or OPENED' in b_main and not re.search(r'dry[^\n]*--out|--out[^\n]*dry', b_main)) else '再現しない',
    'judge の書き出し先 %s・open の書き出し先 %s・DRY で --out を求める行 %s' % ('out = a.out or JUDGE' in b_main, 'out = a.out or OPENED' in b_main, bool(re.search(r'dry[^\n]*--out|--out[^\n]*dry', b_main))))

# ---------------- C1-新9・C2-5: 起動器の三つの相の確かめは必ず通る ----------------
rt = rec_txt
no5 = NL.join(l for l in rt.split(NL) if not l.startswith('| 五 |'))
hdr = [l for l in rt.split(NL)[:8] if '起動器の三つの相' in l]
rec('C1-新9・C2-5', '凍結の器の「起動器の三つの相」の確かめは記録の文に語があるかだけを見るので、記録の頭の順伝播の行でいつも通る',
    '正式の記録から五の行をすべて除いた写しに、凍結の器と同じ判定の式を当てた',
    '再現した' if ('起動器の三つの相' in no5 and hdr) else '再現しない',
    '五の行を除いた写しで判定 %s・記録の頭で語を含む行 %d・凍結の器の式 %s' % ('起動器の三つの相' in no5, len(hdr), [l.strip()[:60] for l in T('tools/freeze_Bl3.py').split(NL) if "'起動器の三つの相' in txt" in l]))

# ---------------- C1-新10: 近道の振る舞いの確かめは use_cache の既定（None）を数えない ----------------
ucl = [l.strip() for l in dr.split(NL) if "fwd['use_cache'] +=" in l]
rec('C1-新10', '本の計算は近道を使わない確かめは、use_cache が真で渡された回だけを数え、渡さない（模型の設定の既定）回を数えない',
    '合成データの器の行を読んだ', '再現した' if ucl and 'bool(kwargs.get' in ucl[0] else '再現しない', '数える式 %s' % ucl[:1])

# ---------------- C1-新11: 語彙の行列の守りは module の hook ----------------
gl = [l.strip()[:120] for l in bt.split(NL) if 'register_forward_pre_hook' in l]
rec('C1-新11', '相 check の「語彙の行列」の守りは lm_head の module の前の hook なので、重みを直に掛ける計算は捕まえない', '起動器の守りの行を読んだ（hook は module を呼んだときだけ走る）',
    '読んで確かめた' if gl else '再現しない', '守りを掛ける行 %s' % gl[:2])

# ---------------- C1-新12・C2-9: 手元でトークンの並びを組むときの版を記さない ----------------
l5, b_ids = body_of('tools/freeze_Bl3.py', 'local_ids_sha16')
rec('C1-新12・C2-9', '凍結の器が手元でトークンの並びを組むとき、transformers と tokenizers の版とトークナイザのファイルの SHA を記さず、転記行 F と照らさない',
    '凍結の器の local_ids_sha16 の本体を読んだ', '再現した' if ('version' not in b_ids and not re.search(r'hashlib|sha256f\(|sha16f\(|facts\S*F', b_ids)) else '一部',
    '版を読む行 %s・トークナイザのファイルの SHA を取るか転記行と照らす行 %s' % ('version' in b_ids, bool(re.search(r'hashlib|sha256f\(|sha16f\(|facts\S*F', b_ids))))

# ---------------- C1 の疑い: 下見の中の芯の ValueError ----------------
lp, b_rp = body_of('tools/bl3_run.py', 'run_pilot')
kcalls = sorted(set(re.findall(r'K\.([A-Za-z_]+)\(', b_rp)))
import ast
_tree = ast.parse(T('tools/bl3_core.py'))
raisers = {n.name for n in _tree.body if isinstance(n, ast.FunctionDef) and any(isinstance(x, ast.Raise) and isinstance(x.exc, ast.Call) and getattr(x.exc.func, 'id', None) == 'ValueError' for x in ast.walk(n))}
rec('C1-疑い', '芯の ValueError が下見の中で起きると、起動器の器の誤りの型（TOOL_ERR）の外なので、予期しない誤りの道に入るかもしれない（票は確かめていない）',
    '走らせる器の run_pilot が呼ぶ芯の関数と、芯で ValueError を出す関数と、起動器の TOOL_ERR の型を読んだ',
    '一部' if (set(kcalls) & raisers) else '再現しない（下見は ValueError を出す芯の関数を呼ばない）',
    'run_pilot（%d 行から）が呼ぶ芯の関数 %s・芯で ValueError を出す関数（構文から拾った）%s・重なり %s・起動器の TOOL_ERR %s' % (lp, kcalls, sorted(raisers), sorted(set(kcalls) & raisers), [l.strip() for l in bt.split(NL) if l.strip().startswith('TOOL_ERR =')][:1]))

# ---------------- C2-7: 書き換えの道の NaN は判定の段で例外になる ----------------
import numpy as np
eff = {}
rng = np.random.default_rng(5)
n_iso = T3['nulls']['isotropic']['count']
for sc, b, sg in T3['cell_signs_main']:
    for s_ in (int(sg), -int(sg)):
        k = AZ.key3(sc, b, s_)
        e = {'static': float(rng.normal()), 'Nk': float(rng.normal())}
        e.update({'iso:%d' % i: float(x) for i, x in enumerate(rng.normal(size=n_iso))})
        e.update({'real:' + q: float(x) for q, x in zip(pair_names, rng.normal(size=len(pair_names)))})
        for dname in list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]:
            e.setdefault(dname, float(rng.normal()))
        eff[k] = e


def path_from(eff_):
    out = {}
    for r_ in T3['main_rows']:
        if r_['direction'] != 'static':
            continue
        s_ = r_['sign']
        k, kk = AZ.key3(r_['scenario'], r_['base'], s_), AZ.key3(r_['scenario'], r_['base'], -s_)
        E = {'static|%+d' % s_: eff_[k]['static']}
        E.update({'iso:%d|%+d' % (i, s_): eff_[k]['iso:%d' % i] for i in range(n_iso)})
        E.update({'real:%s|%+d' % (q, s_): eff_[k]['real:' + q] for q in pair_names})
        E.update({'real:%s|%+d' % (q, -s_): eff_[kk]['real:' + q] for q in pair_names})
        out[r_['id']] = {'noop_lo': 0.0, 'effects': E}
    return out
hook = path_from(eff)
rw = json.loads(json.dumps(hook))
rid0 = next(iter(rw))
sk = next(k for k in rw[rid0]['effects'] if k.startswith('static|'))
rw[rid0]['effects'][sk] = float('nan')
pilot = {'floor': 1e-6}
try:
    ag = AZ.recompute_agreement(T3, T3['main_rows'], eff, pair_names, hook, rw, pilot)
    nan_msg = '例外なし（一段目 %s・理由 %s）' % (ag['first']['agree'], ag['first'].get('reason'))
except Exception as e_:
    nan_msg = '%s: %s' % (type(e_).__name__, e_)
rec('C2-7', '書き換えの道に NaN があると、判定の段は札を組む所で ValueError になり、一致の関数の non_finite（不一致として記す）に届かない',
    '合成の効き目で二つの道を組み、書き換えの道の v̂ の効き目の一つを NaN にして、独立の再計算の一致の関数に当てた',
    '再現した' if nan_msg.startswith('ValueError') else '再現しない', nan_msg[:160])

# ---------------- C2-8: 結果を開く段は判定の段の事前の確かめをやり直さない ----------------
rec('C2-8', '結果を開く段は、DRY の混ざり・組の間の環境・等方の本数の止めをやり直さず、判定の記録の一致と読んだ出力と二段の一致の三つ組だけを照らす',
    '集計の器の open_checked の本体を読んだ',
    '再現した' if ("env_same" not in b_oc.split('pilot_sessions =')[0] and 'n_iso' not in b_oc and "len(set(" not in b_oc) else '一部',
    'open_checked の前半に環境の照らし %s・等方の本数の照らし %s・DRY の混ざりの照らし %s' % ('env_same' in b_oc.split('pilot_sessions =')[0], 'n_iso' in b_oc, 'len(set(' in b_oc))

# ---------------- C2-13: 相 check の守りの試しは掛けた数だけを見る ----------------
bl6, b_pb = body_of('tools/dry_run_Bl3.py', 'part_boot')
rec('C2-13', '相 check の守りの試しは、呼ばれた数が零で守りが一つ以上あることだけを見て、守りが止めることを試さない',
    '合成データの器の part_boot の本体を読んだ', '再現した' if ("CK.get('forward_calls') == 0" in b_pb and 'Stop' not in b_pb) else '一部',
    '判定の式に forward_calls %s・守りの止めを試す行 %s' % ("CK.get('forward_calls') == 0" in b_pb, 'Stop' in b_pb))

# ---------------- C2-14: 報告の器の封印と凍結の照らしは自己検査でしか通らない ----------------
bl7, b_ss = body_of('tools/build_report_Bl3.py', '_selftest_sealed')
rec('C2-14', '報告の器の封印と凍結の照らしは自己検査でしか通らず、その自己検査は凍結の記録を集計の器の FROZEN_CHECK から作る。正式の記録の五は報告の build を直に呼ぶ',
    '報告の器の _selftest_sealed の本体と合成データの器の part_boot を読んだ',
    '再現した' if ('FROZEN_CHECK' in b_ss and 'BRP.build(' in b_pb and 'load_inputs' not in b_pb) else '一部',
    '自己検査が FROZEN_CHECK から凍結の記録を作る %s・五が build を直に呼ぶ %s・五が load_inputs を呼ぶ %s' % ('FROZEN_CHECK' in b_ss, 'BRP.build(' in b_pb, 'load_inputs' in b_pb))

# ---------------- C2-10: 持ち出し ----------------
pkg = body_of('tools/colab/boot_Bl3.py', 'package')[1]
adop = T('records/reviews/Bl3/impl/adoption-table-impl-Bl3.md')
row7 = [l for l in adop.split(NL) if l.startswith('| R2-中7 |')]
rec('C2-10・G1-2-2', '起動器の自動のダウンロードは落とし終わりを待たずに次へ進み、既定では三つの組を一度に走らせる。最後の zip の SHA-256 は手元に残る session に書かれない（印字にだけ残る）',
    '起動器の package の本体と組の選び方の行を読み、採否の案の R2-中7 の直し方の文と比べた',
    '再現した' if ('files.download(zp)' in pkg and pkg.index('write_json(') < pkg.index("S.setdefault('zips'") and "os.environ.get('OP4B_PART', ','.join(PARTS))" in bt) else '一部',
    'session を書くのが zip の SHA を足す前 %s・ダウンロードの後に待つ行 %s・組の既定 %s・採否の案の R2-中7 の直し方に「ダウンロードの後に次の組へ進む」%s' % (
        pkg.index('write_json(') < pkg.index("S.setdefault('zips'"), bool(re.search(r'sleep|wait', pkg)), "OP4B_PART 既定は三つの組" if "os.environ.get('OP4B_PART', ','.join(PARTS))" in bt else '?',
        bool(row7 and 'ダウンロードの後に次の組へ進む' in row7[0])))

# ---------------- G1-2-3: 下見が器の誤りでやり直さないときに閉じる道が無い ----------------
te = T3['pilot']['decision']['tool_error']['rerun']
rec('G1-2-3', '下見が器の誤りで終わり、やり直さないと決めたとき、本の凍結の器は止まり、報告の器は本の凍結の記録の下見の試みを読むので、正本の「記録して閉じる」を器で通す道が無い',
    '正本 pilot.decision.tool_error.rerun の文・本の凍結の器の最後の試みの確かめ・報告の器の load_inputs の下見の試みの読み方を読んだ',
    '再現した' if ('やり直さないときは' in te and "atts[-1].get('tool_error')" in b_mf and "FR['main_freeze']['pilot_attempts']" in b_li) else '一部',
    '正本の文に「やり直さないときは…閉じる」%s・本の凍結は最後の試みが器の誤りなら止める %s・報告は本の凍結の記録から下見の試みを読む %s' % ('やり直さないときは' in te, "atts[-1].get('tool_error')" in b_mf, "FR['main_freeze']['pilot_attempts']" in b_li))

# ---------------- 数と行番号の確かめ（是認・数え方の主張） ----------------
nf = sum(1 for v in T3['inputs']['files'].values() if isinstance(v, dict) and v.get('sha16'))
rec('G2-数', 'G2 は正本 inputs.files の SHA16 を持つファイルを 27 件と書いた（R2-軽微16 の閉じ方の欄）', '正本 v8 の inputs.files を数えた',
    '数が違う' if nf != 27 else '一致', 'SHA16 を持つ項目 %d' % nf)
fck = sorted(set(AZ.FROZEN_CHECK) - (set(FZ.import_closure(FZ.TOOLS)) | set(FZ.frozen_files(T3))))
dk = [k for k in (T3['decisions'] if isinstance(T3['decisions'], dict) else {})]
ga = T('.gitattributes') if os.path.exists(os.path.join(CL, '.gitattributes')) else ''
rec('C2-是認', 'C2 の問題なしの判断のうち数で確かめられるもの: 照らす十のファイルがすべて凍結物の鍵に入る・正本 decisions の鍵が D と数字だけ・.gitattributes が text=auto eol=lf',
    '凍結の器の関数で凍結物の鍵を計算し、正本の decisions の鍵と .gitattributes を読んだ',
    '一致' if (not fck and dk and all(re.fullmatch(r'D\d+', k) for k in dk) and 'eol=lf' in ga) else '一部',
    '凍結物に入らない照らしのファイル %s・decisions の鍵 %d（D と数字だけ %s）・.gitattributes %s' % (fck, len(dk), all(re.fullmatch(r'D\d+', k) for k in dk), ga.strip()[:40]))
cites = [('G1', 'tools/build_report_Bl3.py', 320, 'def sealed_and_frozen_bad'), ('G2', 'tools/analyze_Bl3.py', 328, 'def load_outputs'),
         ('C1', 'tools/colab/boot_Bl3.py', 164, "for role in ('coordinator', 'registrant')"), ('C2', 'tools/build_draft_Bl3.py', 71, "rel(a.src), sha(a.src)")]
rec('行番号', '票の行番号の引き方の見本（各票一つ）: G1 報告の器 320 行・G2 集計の器 328 行・C1 起動器 164 行（封印の照らし）・C2 組み立ての器 71 行',
    '束の入力のコミットの器の該当の行を読んだ', '一部' if not all(txt in LINES(f)[n - 1] for _, f, n, txt in cites) else '一致',
    '・'.join('%s %s:%d %s（実の行 %s）' % (who, f.split('/')[-1], n, '当たる' if txt in LINES(f)[n - 1] else '当たらない', find(f, re.escape(txt))[:1]) for who, f, n, txt in cites))

# ---------------- 露出の走査（票に層三の結果の見込みに当たる文があるか） ----------------
PAT = r'札が付|門を通(る|ら)|結果の見込み|効き目の見込み|v̂ の行に|予想の答え'
hits = []
for lab in ('g1', 'g2', 'c1', 'c2'):
    t = open(os.path.join(REPO, 'records', 'reviews', 'Bl3', 'fixcheck', lab, 'vote.md'), encoding='utf-8').read()
    for i, l in enumerate(t.split(NL), 1):
        if re.search(PAT, l):
            hits.append('%s:%d %s' % (lab.upper(), i, l.strip()[:90]))
rec('露出', '票に層三の結果の見込み（どの行に札が付くか・門を通るかなど）に当たる文があるか', '四つの票の本文を語で走査し、当たった行を読んだ（読んだ結果は採否の案に書く）',
    '走査した', '当たった行 %d: %s' % (len(hits), ' ／ '.join(hits)))

# ---------------- 記録 ----------------
shutil.rmtree(TD, ignore_errors=True)
res_n = collections.Counter(r_['result'] for r_ in ROWS)
L = ['# 器の直しの確かめ（登録者裁定 D238）の四名の票の事実の主張の確かめ（機械生成・`verify_fixcheck_Bl3.py`・束の入力のコミット %s）' % SRC, '',
     '- 束の入力のコミット（%s・器と正本は直しのコミット a8ac5ad と同じ）を一時の置き場に複製して確かめた（取り出した HEAD %s）。方向の記録（コミットに入っていない）は作業木から一時の複製に写した。' % (SRC, HEAD[:12]),
     '- 振る舞いの再現は一時の置き場でだけ行った（実の重みを読まない・リポジトリの作業木に書かない・一時の置き場は終わりに消した）。記録の中の一時の置き場の道筋は決まった言い方に置き換えた。',
     '- 同じ筋の主張は一つの行にまとめた（番号の欄に出所の札を並べた）。結果: %s。' % '・'.join('%s %d' % kv for kv in sorted(res_n.items())), '',
     '| 番号 | 主張（要旨） | 確かめ | 結果 | 詳しく |', '|---|---|---|---|---|'] + [
     '| %s | %s | %s | %s | %s |' % (r_['no'], r_['claim'], r_['how'], r_['result'], r_['detail'].replace('|', '｜')) for r_ in ROWS] + [
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
json.dump({'src': SRC, 'head': HEAD, 'rows': ROWS, 'counts': dict(res_n)}, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('[verify_fixcheck_Bl3] wrote %d rows: %s' % (len(ROWS), dict(res_n)))
