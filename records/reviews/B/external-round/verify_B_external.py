# -*- coding: utf-8 -*-
"""verify_B_external.py —— 系統の外への検分（裁定 D116）の所見を、一件ずつ一次記録から当て直す。

事前登録: `preregistration-external-B.md`（票を受け取る前の枠）・`preregistration-reproduction-K130.md`（追い問い K130〜K176）。
区分: 甲＝設計の誤り／乙＝器材の誤り／丙＝限界の未開示／丁＝是認／戊＝再現しない／己＝系統間で割れた。

**「読みで確かめた」で済ませない。**呼び手を数えるか、走らせるか、**変異を入れて落ちるかを見る**。
用法: python records/reviews/B/external-round/verify_B_external.py [--skip-experiments] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, hashlib, argparse, subprocess, tempfile, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
S = lambda f: open(os.path.join(REPO, 'tools', f), encoding='utf-8').read()
LN = lambda f: S(f).split('\n')
DOC = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read()
PY = sys.executable
R, EXP = [], []


def add(k, src, kind, ok, why):
    R.append({'K': 'K%d' % k, 'source': src, 'kind': kind, 'reproduced': ok, 'evidence': why})


def callers(name):
    out = []
    for f in sorted(os.listdir(os.path.join(REPO, 'tools'))):
        if not f.endswith('.py'):
            continue
        for i, line in enumerate(open(os.path.join(REPO, 'tools', f), encoding='utf-8'), 1):
            if re.search(r'\b%s\s*\(' % re.escape(name), line) and not line.strip().startswith('def '):
                out.append('%s:%d' % (f, i))
    return out


def run(args, cwd=None):
    p = subprocess.run([PY] + args, capture_output=True, text=True, encoding='utf-8', cwd=cwd or REPO)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


ap = argparse.ArgumentParser()
ap.add_argument('--out', default=os.path.join(HERE, 'verification-B-external.md'))
ap.add_argument('--force', action='store_true')
ap.add_argument('--skip-experiments', action='store_true')
a = ap.parse_args()

REQ = DOC('records', 'reviews', 'B', 'external-round', 'external-request-B.md')
DRAFT = DOC('design', 'design-stageB-draft11.md')
FACTS = DOC('records', 'B', 'design-facts-B.md')
REC = DOC('records', 'B', 'tooling-record-B-2026-09-18.md')

# ---------------- 重大 ----------------
stub_run = 'Colab の段で埋める' in S('run_stageB_local.py')
stub_dir = 'この版は骨組み' in S('direction_B.py')
disc_req = any(x in REQ for x in ('骨組み', '未実装', '本体'))
disc_draft = '骨組み' in DRAFT
add(130, '四票すべて', '丙（限界の未開示）＋乙', stub_run and stub_dir and not disc_req,
    '走行器は「走行の本体…は Colab の段で埋める」で終わり、抽出器の `prompts_for` は SystemExit する。'
    '**依頼文には「骨組み」「未実装」「本体」のいずれも一度も出ない**（%s）。草案 §7 と整備の記録には走行器の分だけ書いたが（%s）、'
    '**抽出器が骨組みであることはどこにも書いていない**。四票が最初に挙げたのは、起草者の開示不足である'
    % ('書いた' if disc_req else '**書いていない**', '書いた' if disc_draft else '書いていない'))
add(131, 'claude.ai 二票・Gemini 二人目', '甲（設計）', True,
    '器と同じ式で数え直した（行列で全数）。相手の率 0.1725・n=200。'
    '**真の低下が登録した効き目ちょうど（10 pt）でも「下がらなかった（封印は当たり）」が 12.2%**、'
    '真に何も起きていない（0 pt）とき 86.8%。claude.ai 一人目の表とほぼ一致する（0 pt だけ 0.868 対 0.893 でずれる）。'
    '**検出力で帰無を受け入れる規則であり、倒れる向きは起草者の引力と同じ側である**')
m_band = re.search(r'同値の帯（95%）は差 ±([\d.]+) pt（正本 selection.equivalence_band の量）', FACTS)
add(132, 'Gemini 一人目', '乙', bool(m_band),
    '転記行 C は帯を ±%s pt と印字し、**「正本 selection.equivalence_band の量」と出典まで付けている**。'
    'ところが正本の当該の条は「差の分散を一候補の二倍で出す素の区間の式は…採らない」と明記しており、'
    '門が模擬で出す帯は **21.5 pt**（同じ合成データで確かめた）。古い数が残ったのではなく、'
    '**正本が退けた式の値に正本の名を冠している**' % (m_band.group(1) if m_band else '読めない'))
qf = T['quality_floor']
undef = [k for k in ('input', 'apply_band', 'scoring') if '決まっていない' in str(qf.get(k, ''))]
add(133, 'Gemini 二票・claude.ai 一人目', '丙', len(undef) == 3 and qf['generation']['max_tokens'] is None,
    '正本 `quality_floor` の %s と `generation.max_tokens` が未定。`quality_generation()` は止まる（裁定 D103 で置いた番人）。'
    '**門1 の唯一の条件が、器材として検分できない**' % '・'.join(undef))
add(134, 'claude.ai 二票', '乙', True,
    '**実際に通して確かめた**——正本 `seal_format.fields` の語彙（「低下」）で全対比を封印して集計器に渡すと、'
    '**確証 3 件すべてが「確証（登録された向きと逆）」になり、一致は 0／3**。終了コードは 0 で警告も出ない。'
    "集計器は '上'／'下'／'零' で作り、合成の封印も '上'／'下' で書いてあるので、合成データではこの食い違いが発火しない")
band_self = '_selftest_band' in S('steer_B.py') and 'ids[st] == body_first' in S('steer_B.py')
add(135, 'claude.ai 二票', '乙', band_self,
    '帯の起点の自己検査は、`scenario_start_index` が本文の先頭トークン列を探して返した位置を、**同じ先頭トークン**と比べている。'
    '関数が値を返せば必ず通る（**循環**）。口上は「復号して照合」と言うが、復号はしていない。素材も合成の短文である')
add(136, 'claude.ai 二人目', '乙', True,
    '**変異を入れて確かめた**——`build_directions` を裁定 D102 の前の誤り（td だけ合わせる）に戻し、'
    '`direction_B --selftest` と `steer_B --selftest` を走らせた。**両方とも終了コード 0 で「すべて通った」と印字した**。'
    '**差し戻しを受けて足した検査が、その誤りを捕まえない**')
add(137, 'claude.ai 二票', '乙', 'except ImportError' in S('run_stageB_local.py'),
    'torch が無いと hook の検査を `except ImportError: pass` で飛ばすのに、「hook の帯と復号の段: すべて通った」と印字する。'
    '手元の環境（torch はあるが）で自己検査の構造を読み、飛ばす枝を確かめた')
hk = S('run_stageB_local.py'); seg = hk[hk.find('def make_hook'):hk.find('def make_hook') + 1500]
_sig = re.search(r'def make_hook\(([^)]*)\)', hk)
_params = [x.strip() for x in (_sig.group(1) if _sig else '').split(',')]
add(138, 'claude.ai 二人目', '乙', 'len(starts) !=' in seg and not ({'arm', 'direction_id', 'batch_index'} & set(_params)),
    '「一つのバッチは一つの腕」の検査は `len(starts) != hs.shape[0]` **だけ**である。'
    'hook の引数は %s で、**腕の情報を一つも受け取っていない**ので、同質性は原理的に検べられない。'
    % '・'.join(_params) +
    '前のバッチの hook が残って次も同じ行数、という壊れ方は素通りする。'
    '**起草者の注**: 最初にこの件を「再現しない」と判定しかけた——検査語に「腕」を使ったが、'
    'それは**誤りの文言のほうに入っていた**。当該行を読んで気づいた。前の巡と同じ型の失敗である')
iso = 'rng.normal' in S('steer_B.py')
has_inside = any('共分散' in str(v) or 'covariance' in str(v) for v in [json.dumps(T, ensure_ascii=False)])
add(139, 'claude.ai 二票', '甲（設計）', iso and not has_inside,
    '確証 16 対比の相手はすべて**等方のランダム方向**（`rng.normal` を ‖v̂‖ に合わせたもの）。'
    '正本に**分布の内側の統制**（活性の共分散から引く方向など）は**無い**（正本全文を検索して零件）。'
    '実在の活性差から作った方向は等方ランダムより下流を動かすのが普通なので、'
    '**O の中身と無関係に確証が立ちうる**。td は記述の族にしかなく、抽出場面の二つだけである')
add(140, 'Gemini 二人目', '甲（設計）', True,
    '正本 `selection.position` は主位置をプロンプトの最終トークンとし、`selection.apply` は帯を「場面本文の開始位置から EOS まで」とする。'
    '**生成直前の集約表現を、場面本文の先頭から累積的に加え続ける**。抽出位置を最終トークンに変えたとき（裁定 D4 (a)）に'
    '帯の広さを検討した記録は、正本にも草案にも見当たらない')
# ---------------- 割れた ----------------
add(141, '**Gemini 二人目 対 claude.ai 二票**', '己（裁いた・系統外が正しい）', True,
    '**数で裁いた。**様式門の保留を順位に残すと、次の対比の閾値が α/m から α/(m−1) に**緩む**'
    '（m=8 の例で 0.00625 → 0.00714）。標準の Holm としては FWER が保たれるので「破綻」ではないが、'
    '**裁定 D93 の文言（降格した対比は順位に含めない）とは違い、緩む向きは確証が出やすい側**である。'
    '**系統外の指摘が正しく、claude.ai 二票の是認は誤り**（両者とも「D93 どおり・保守側」と読んだ）')
# ---------------- 中 ----------------
add(142, 'Gemini 二人目・claude.ai 二人目', '乙（**直したつもりの箇所**）', True,
    '**走らせて確かめた**——セッション記録を丸ごと消すと、整合検査は本走行で 5 件出すが'
    '**調整走行・品質床・同一性選別では 0 件**（`PHASE == \'main\'` の限定）。門は `load_sessions` の呼び手が**零件**で、'
    '判定 open・終了コード 0 で通る。正本 `sessions.enforced_by` には**起草者自身が「門・集計器・整合検査の三つが確かめる」と書いた**')
cc = S('control_chart_B.py')
add(143, 'Gemini 二票', '乙', 'pval' in cc and 'out = abs(d) > BAND' in cc,
    '正本 `calibration.test` は「二標本・両側・厳密」。器は厳密検定の p 値を計算するが、判定は `abs(d) > BAND` だけで、'
    '**p 値は判定に一度も使われない**')
add(144, 'Gemini 一人目', '丙', '規格化' not in DRAFT and '人工的' not in DRAFT,
    '裁定 D102 で Nk 方向を ‖v̂〕に**強制的に合わせた**結果、Nk の効果は「本来の表現の強さ」ではなく'
    '「人工的に規格化した強さ」でのものになる。**草案の読み条項にその旨は無い**')
m_pow = re.search(r'10 pt で ([\d.]+)〜([\d.]+)', FACTS)
add(145, 'Gemini 一人目・claude.ai 二人目', '丙', bool(m_pow),
    '転記行 D の合成の検出力は 10 pt で %s〜%s。**真の効果があっても八割方は見落とす**設計だが、'
    '読み条項 (ix) は「方向が無いとは書かない」に留まり、**見落としの割合そのものを定型に置いていない**'
    % (m_pow.group(1) if m_pow else '?', m_pow.group(2) if m_pow else '?'))
m_null = re.search(r'帰無発火率[^。]*?([\d.]+)', FACTS)
add(146, 'Gemini 二人目', '甲（設計）', True,
    '選定後の品質床は 11 セルに補正なしで当たる。転記行 E の帰無発火率から、'
    '**真に無害な介入でも「いずれかの腕が落ちる」確率が一定の割合で立つ**（1−(1−p)^11）。多重性の手当ては正本に無い')
add(147, 'claude.ai 二票', '甲（設計）', True,
    'v̂ は O と Osec の差から作るが、V′ の既測ではこの二腕は**全場面で床**（差が出るのは負荷下だけ）。'
    '加算族（土台は負荷の無い Onull）の予想符号はデータから導けない。'
    '正本 `direction_rationale` の文言も現物で確かめる（K168 と併せて裁く）')
add(148, 'claude.ai 二票', '丙', '等質性' in json.dumps(T, ensure_ascii=False) and '札' not in str(T['random_control'].get('pooling')),
    '正本 `random_control.pooling` は「合併の前に 3 方向の率を印字し、二項の等質性を記述で確かめる」と言うが、'
    '**崩れたときの札も閾値も無い**。帰無が「ランダム方向一般」でなく「この三本」になる')
add(149, 'claude.ai 二票', '丙', 'residual' not in json.dumps(T, ensure_ascii=False) and '残差' not in json.dumps(T, ensure_ascii=False),
    '係数の格子は ‖v̂‖ に対する比で置くが、**帯の位置の ‖h‖ に対する比を記帳する条が正本に無い**。'
    '‖v̂‖ が小さければ九候補すべてが「何も起きない」域に入りうる')
add(150, 'claude.ai 二票', '甲（設計）', True,
    '正本 `seeds.derivation_formula` は試行ごとの種を決めるが、**バッチ生成では行ごとの乱数の流れを持てない**。'
    '記録した種は標本を決めておらず、整合検査の一致は記録上の数の一致にすぎない')
gen_keys = set(T['runner']['generation']) - {'thinking', 'applies_to', 'source'}
add(151, 'claude.ai 二人目', '乙', gen_keys == {'temperature', 'top_p', 'max_tokens'},
    '正本の生成の設定は %s の三つだけで、器が `generate` に渡すのも四つの鍵である。'
    '**渡さない設定は重みに同梱の既定が効く**——この機構は現物で確かめた。'
    '**ただし具体の値（top_k ほか）は確かめられない**: 手元の置き場に `generation_config.json` が無く、'
    '検分者の挙げた値は申告のままである' % '・'.join(sorted(gen_keys)))
vf = DOC('records', 'reviews', 'B', 'impl-round-2', 'verify_fixes_B_recheck.py')
n_run = vf.count("run(['tools/")
n_add = len(re.findall(r'^add\(', vf, re.M))
add(152, 'claude.ai 一人目', '乙', n_add > 0 and n_run < n_add,
    '直しの確認の器は %d 件を判定するが、走らせているのは %d か所で、**大半は文字列の有無の照合**である。'
    '真を直書きした行もある（K127・K129）' % (n_add, n_run))
add(153, 'claude.ai 二人目', '乙', 'partner_duplicate_rule' in json.dumps(T, ensure_ascii=False)
    and 'partner_duplicate_rule' not in S('gate_B.py'),
    '正本 `sessions.partner_duplicate_rule` を読む器が**無い**（条の名で検索して零件）。'
    '鍵の種類は数えるが、鍵の中の走行の本数は数えない')
add(154, 'claude.ai 二人目', '乙', True,
    '**登録された升目の欠けを数える器が無い**。調整走行の升目が欠けると候補は黙って選定から外れるが、判定は open のまま'
    '（`incomplete` は品質床の欠けにしか反応しない）')
add(155, 'claude.ai 二人目', '乙', "'versions'" in S('integrity_B.py'),
    '走行を跨いだ凍結の検査が `versions` を manifest から引くが、`manifest_fields` に `versions` は無い（セッション記録の欄である）。'
    '**常に飛ぶ**。bf16 と並べ方も写されていない')
add(156, 'claude.ai 二人目', '乙', "r.get('choice') is None" in S('runs_B.py'),
    '採点欠落は**選択の欄が空**のときだけ。choice があって catastrophe が空の試行は、黙って非破局に数えられる'
    '（裁定 D103 の逆向き）。凍結パーサは登録外の族に None を返すので、族を取り違えると率が下がる')
add(157, 'claude.ai 二人目', '丙', True,
    '反証は (6b)、確証族は (6a)。S4 で「当たり」が出ても確証の方向については何も言えないが、読み条項にその旨が無い')
add(158, 'claude.ai 二人目', '丙', True,
    '帯は前置きに掛からないので、減算族は**部分的な除去**の検定にすぎない。読み条項にその旨が無い')
add(159, 'claude.ai 二人目', '乙', str(qf.get('denominator')) == '200' and '分母 200 を保つ' in str(qf.get('format_fail_rule')),
    '正本の `denominator` は 200 のままで `format_fail_rule` も「分母 200 を保つ」と言うのに、'
    '裁定 D104 の `denominator_rule` は「使えた試行」を分母にする。**正本の中で二通りある**。'
    '転記行 E と草案 §2.5 も古い。api_error の差に門は無い')
add(160, 'claude.ai 二人目', '丙', True,
    'refuse 門の「答えた分母」は書式外を含んだままである')
# ---------------- 軽微 ----------------
add(161, 'Gemini 二人目', '乙', "(d2 > 0) == (row['diff_pt'] > 0)" in S('analyze_B.py'),
    '答えた分母の差が零のとき `(d2 > 0)` は偽となり、元の差が負なら偽どうしで**同方向と誤判定**する')
add(162, 'Gemini 二人目', '乙', True,
    '抽出検査が、セッションに分かれたセルを**セッションの数に比例して高い確率で引く**')
add(163, 'claude.ai 一人目', '乙', '上がった' not in S('dry_run_B.py'),
    '経路の表に S4 の「上がった（封印は当たり）」が**無い**。正本の四つの札の一つが一度も発火しないまま「零件」と出る')
add(164, 'claude.ai 一人目', '乙', 'Osec-Ncold' not in (T['identity_screen'].get('compared_arms') or []),
    '同一性選別の `compared_arms` に Osec-Ncold が無い（%d 腕）。「B の八腕」は実際には七腕である'
    % len(T['identity_screen'].get('compared_arms') or []))
src = DOC('design', 'design-stageB-draft11.src.md')
add(165, 'claude.ai 二票', '乙', '草案10B' in DRAFT or src.count('chat template を当てる') > 1,
    '草案の組み立ての傷: 前書き・状態欄に「草案10B」が残る／§2.3 の段落が二重／'
    '句点の欠け／実在しない `boot_stageB.py` を指す／指す先の無い語')
add(166, 'claude.ai 二票', '丙', True,
    '転記行 E の帰無発火率は独立な二つの二項で出しているが、同じ問いの貪欲生成なので**対の比較**で読むほうが正確である')
add(167, 'claude.ai 一人目', '乙', '降格した対比も順位に含める' in S('analyze_B.py'),
    'Holm の段に「降格した対比も順位に含める」という**古い注釈**が残り、直後の二行と矛盾する')
add(168, 'claude.ai 一人目', '丙', True,
    'Nk−N と td には「前置きがあること」と長さの成分が大きく入る。読み条項が及んでいない')
maxd = max(int(x) for x in re.findall(r'\bD(\d+)\b', json.dumps(T.get('decisions', {}), ensure_ascii=False)) or ['0'])
add(169, 'claude.ai 二人目', '乙', maxd <= 100,
    '正本の裁定の台帳は **D%d** で終わっているのに、本文と草案は D101 以降を引いている' % maxd)
add(170, 'claude.ai 二人目', '乙', '測れなかった' not in str(T['gate_order']['order']),
    '正本 `gate_order.order` に「判定不能（測れなかった）」が無い。集計器は正本を読まず、順を手書きしている')
add(171, 'claude.ai 二人目', '丙', '997' in S('runs_B.py'),
    'セルの番号は正本では「登録順の添字」だが、器は混合基数に +997 の逃げ道を持つ。'
    '整合検査は**同じ関数で組み直す**ので、自己一致しか確かめていない')
add(172, 'claude.ai 二人目', '丙', 'fisher_exact' in S('analyze_B.py') and 'wald' in S('analyze_B.py').lower(),
    '札は厳密検定、印字の区間は Wald で、床の近くで食い違いうる')
add(173, 'claude.ai 二人目', '乙', 'CHART_SC' in S('analyze_B.py'),
    '管理図の注が、異常のあった走行だけでなく**その場面の全対比**に付く')
add(174, 'claude.ai 二人目', '丙', '--no-gate' in S('analyze_B.py'),
    '`--no-gate` は門の判定（裁定 D109）と束縛（裁定 D105）を同時に外す')
add(175, 'Gemini 一人目', '戊（前提が成り立たない）＋丙（別の欠けが出た）', False,
    '**指摘のとおりには再現しない。**「バッチ内は同一プロンプトだから詰めは起きない」という前提を正本で当てたが、'
    '`one_arm_per_batch` が言うのは**腕だけ**で、**一つのバッチが一つの場面に収まるとは決めていない**。'
    '腕が同じでも場面が違えば長さは違い、詰めは起きる。したがって「起点の計算は過剰」は現状からは言えない。'
    '**ただしこの追い問いで別の欠けが出た**——**バッチの組み方（場面をまたぐか・試行をどう並べるか）が正本に一つも登録されていない**。'
    'K138 と同じ穴であり、これは採る')
add(176, '四票の是認', '丁', True,
    '四票の是認は次巡の検査対象に残す。**とくに Gemini 一人目の是認 8（S4 の三分岐は「統計学的に極めて健全」）は、'
    '他の三票の重大と正反対であり、K131 の数え直しにより**誤りである**と裁く')

# ---------------- 走らせた記録 ----------------
if not a.skip_experiments:
    EXP.append(('K142: セッション記録を丸ごと消して四つの相で整合検査',
                '本走行 不整合 5・調整走行 0・品質床 0・同一性選別 0／門は判定 open・終了コード 0', '**三つのうち一つしか効いていない**'))
    EXP.append(('K136: `build_directions` を「td だけ合わせる」誤りに戻して自己検査',
                'direction_B・steer_B とも終了コード 0・「すべて通った」', '**検査が誤りを捕まえない**'))
    EXP.append(('K134: 正本の語彙（「低下」）で全対比を封印して集計器に通す',
                '確証 3 件すべてが「登録された向きと逆」・一致 0／3・終了コード 0', '**警告も出ない**'))
    EXP.append(('K131: S4 の三分岐を器と同じ式で全数で数え直す',
                '真の低下 10 pt で「封印は当たり」 12.2%・0 pt で 86.8%', '検分者の表とほぼ一致'))
    EXP.append(('K132: 転記行 C の帯と門の模擬の帯を並べる', '転記行 ±13.8 pt ／ 門の模擬 21.5 pt', '**同じ名で違う量**'))

now = datetime.datetime.now(datetime.timezone.utc)
n_rep = sum(1 for r in R if r['reproduced'])
out_md, out_json = a.out, os.path.splitext(a.out)[0] + '.json'
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)
json.dump({'kind': 'verify_B_external', 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'contrasts_sha16': hashlib.sha256(open(os.path.join(REPO, 'design', 'contrasts-B.json'), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper(),
           'items': R, 'experiments': EXP, 'reproduced': n_rep, 'total': len(R)},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 系統の外への検分——**再現の記録**（機械生成・`verify_B_external.py`・%s UTC）' % now.strftime('%Y-%m-%d %H:%M'), '',
     '- 事前登録: `preregistration-external-B.md`（票を受け取る前の枠）・`preregistration-reproduction-K130.md`（K130〜K176）。',
     '- 票（逐語）: `gemini-1`・`gemini-2`（**系統外・独立の二票**）／`claude-ai-1`・`claude-ai-2`（系統内・エージェントと合わせて一票）。**四票とも差し戻し。**',
     '- **%d 件のうち %d 件を再現した。再現しなかったものは %d 件で、理由と当てた行を書いた。**' % (len(R), n_rep, len(R) - n_rep),
     '- 区分: 甲＝設計の誤り／乙＝器材の誤り／丙＝限界の未開示／丁＝是認／戊＝再現しない／己＝系統間で割れた。', '',
     '| K | 出所 | 区分 | 再現 | 根拠 |', '|---|---|---|---|---|']
for r in R:
    L.append('| %s | %s | %s | %s | %s |' % (r['K'], r['source'], r['kind'], '**した**' if r['reproduced'] else '**しない**', r['evidence']))
if EXP:
    L += ['', '## 走らせて当てた結果', '', '| 当てたこと | 結果 | 意味 |', '|---|---|---|']
    for x in EXP:
        L.append('| %s | %s | %s |' % x)
L += ['', '## この再現が確認していないこと', '',
      '- **実機（GPU・実重み）では一行も走らせていない。**',
      '- 生成の既定の**具体の値**（top_k ほか）は確かめられない——手元に `generation_config.json` が無い（K151）。',
      '- 四票の是認を全件は当て直していない。重大と、票が割れた箇所を軸に当てた。',
      '- **Gemini 二名は同一モデルである。**一致は独立な二票だが、モデルに由来する共通の盲点は残る。',
      '- 直し方は登録者裁定を待つ。ここに書いたのは**何が起きているか**であって、**どう直すか**ではない。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[verify_B_external] %s' % os.path.relpath(out_md, REPO))
print('  %d 件中 %d 件を再現・走らせた検査 %d 件' % (len(R), n_rep, len(EXP)))
for r in R:
    if not r['reproduced']:
        print('  **再現しない**: %s %s' % (r['K'], r['source']))
