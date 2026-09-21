# -*- coding: utf-8 -*-
"""make_results_B.py —— 段階 B の**表紙の結果報告** `records/B/results-B.md` を組む（登録者裁定 D151: 凍結した集計器の出力と、逸脱 D-B1 の下の出力を**同じ重さで並べる**）。
数は二つの集計の記録・予想の照合の記録・門の記録・凍結の記録から**機械の区画**（`<!-- 機械:始 -->`〜`<!-- 機械:終 -->`）に転記し、散文には数を打たない（正本 `report_rules.typed_numbers`）。
機械の区画の SHA16 は、凍結した走査器 `tools/report_lint.py` の `write_sidecar` で `results-B-machine.json` に書く。走査は `python tools/report_lint.py records/B/results-B.md --contrasts design/contrasts-B.json`。
凍結した器は変えない。用法: python records/B/make_results_B.py [--label 草案1]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_B
import report_lint as RL
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda rel: runs_B.sha16_file(j(*rel.split('/')))
load = lambda rel: json.load(open(j(*rel.split('/')), encoding='utf-8'))

ap = argparse.ArgumentParser()
ap.add_argument('--label', default='草案1')
a = ap.parse_args()

T = load('design/contrasts-B.json')
FZ, DV = load('records/B/analysis-B-2026-09-22.json'), load('records/B/analysis-B-devB1-2026-09-22.json')
PF, PD = load('records/B/predictions-check-B-frozen.json'), load('records/B/predictions-check-B-devB1.json')
G = load('records/B/gate-B-2026-09-21.json')
FR = load('records/B/FREEZE-RECORD-B.json')
SEAL = load('records/B/seal-B.json')
S = {t: load('results/sessions-B/%s__s1.json' % t) for t in ('idB', 'tuneB', 'stageB-quality', 'stageB')}
MB = RL.machine_block(T)
BEG, END = MB['begin'], MB['end']
fz = {r['id']: r for r in FZ['confirm']}
dv = {r['id']: r for r in DV['confirm']}
order = [r['id'] for r in FZ['confirm']]
assert order == [r['id'] for r in DV['confirm']]


def fp(p):
    return '—' if p is None else ('<1e-5' if p < 1e-5 else ('%.3g' % p))


def fh(h):
    return '—' if h is None else ('%.4g' % h)


def block(lines):
    return [BEG] + lines + [END]


# ---- 機械の区画 ----
KEYS = ['確証', '判定不能（検閲）', '判定不能（品質床）', '判定不能（採点欠落）', '判定不能（測れなかった）', '判定保留（書式外転位）',
        '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定保留（様式転位）', '非有意']
n_marked = sum(1 for r in DV['confirm'] if str(r['label']).startswith('確証') and r.get('deviation') == 'D-B1')
M_A = ['| 札 | 凍結した集計器（`analyze_B.py` %s） | 逸脱 D-B1 の下（`analyze_B_devB1.py` %s） |' % (FZ['version'], DV['version']), '|---|---|---|']
for k in KEYS:
    if FZ['counts'].get(k) or DV['counts'].get(k):
        M_A.append('| %s | %d | %d%s |' % (k, FZ['counts'].get(k, 0), DV['counts'].get(k, 0), ('（うち逸脱 D-B1 の印つき %d）' % n_marked) if k == '確証' else ''))
M_A.append('| 計 | %d | %d |' % (sum(FZ['counts'].values()), sum(DV['counts'].values())))
M_A += ['', '- 確証の札で、起草者の封印の符号と一致したもの: 凍結した集計器 %d／%d・逸脱 D-B1 の下 %d／%d。' % (
    FZ['sign_agreement']['agree'], FZ['sign_agreement']['checked'], DV['sign_agreement']['agree'], DV['sign_agreement']['checked'])]

M_B = ['| 対比 | 場面 | 破局 A/n | 破局 B/n | 書式外 A／B（pt） | refuse A／B（pt） | pt 差（A − B） | 区間（Newcombe） | p（両側 Fisher） | Holm の段（凍結／逸脱の下） | 札（凍結した集計器） | 札（逸脱 D-B1 の下） | ランダム方向の不均一 |',
       '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for i in order:
    f, d = fz[i], dv[i]
    assert all(f[k] == d[k] for k in ('k_A', 'n_ok_A', 'k_B', 'n_ok_B', 'diff_pt', 'ci', 'p', 'ff_pt_A', 'ff_pt_B', 'refuse_pt_A', 'refuse_pt_B')), i
    hom = d.get('homogeneity') or {}
    M_B.append('| %s | %s | %d/%d | %d/%d | %s／%s | %s／%s | %s | %s | %s | %s／%s | %s | %s | %s |' % (
        i, d['scenario'], d['k_A'], d['n_ok_A'], d['k_B'], d['n_ok_B'], d['ff_pt_A'], d['ff_pt_B'], d['refuse_pt_A'], d['refuse_pt_B'], d['diff_pt'], d['ci'], fp(d['p']),
        fh(f.get('holm_alpha')), fh(d.get('holm_alpha')), f['label'], d['label'], ('注（三本の率の差 %.1f pt）' % hom['spread_pt']) if hom.get('note') else '—'))
M_B += ['', '- A は方向 v̂（交差族は Nk 方向）を加減した腕、B はノルムを合わせたランダム方向を加減した腕。率は三つ組（破局・書式外・refuse）で読む。分母は使えた試行。',
        '- 二つの出力で、破局・書式外・refuse の件数と pt 差・区間・p は同じである（器が行ごとに確かめた）。違うのは、逸脱 D-B1 の印のある行の札と Holm の段だけ。']

SIGNJ = {'上': '上昇', '下': '低下', '零': 'どちらでもない'}
M_C = ['| 対比 | 起草者の封印の符号（`records/B/seal-B.json`） | 観測の向き（A − B） | 札（逸脱 D-B1 の下） |', '|---|---|---|---|']
for i in order:
    d = dv[i]
    if str(d['label']).startswith('確証'):
        M_C.append('| %s | %s | %s | %s |' % (i, SEAL['signs'].get(i), SIGNJ.get(d.get('sign'), d.get('sign')), d['label']))

M_D = ['| 族 | 場面 | v̂ の腕 − td の腕（pt） | 区間 | p | 確証の対比の札（凍結） | 特異性（凍結） | 確証の対比の札（逸脱の下） | 特異性（逸脱の下） |', '|---|---|---|---|---|---|---|---|---|']
tdf = {t['id']: t for t in FZ['td_specificity']}
for t in DV['td_specificity']:
    f = tdf[t['id']]
    M_D.append('| %s | %s | %.1f | %s | %s | %s | %s | %s | %s |' % (t['family'], t['scenario'], t['diff_pt'], t['ci'], fp(t['p']), f['conf_label'], f['label'], t['conf_label'], t['label']))

M_E = ['| 予想者 | 種別 | 凍結した集計器の出力（的中／外れ／照合不能／予想しない） | 逸脱 D-B1 の下の出力（同） |', '|---|---|---|---|']
for who in PF['results']:
    for kind in ('向き', 'S4', '全体'):
        def cnt(P):
            rows = [r for r in P['results'][who]['rows'] if r['kind'] == kind]
            return '／'.join(str(sum(1 for r in rows if r['verdict'] == v)) for v in ('的中', '外れ', '照合不能', '予想しない'))
        M_E.append('| %s | %s | %s | %s |' % (who, kind, cnt(PF), cnt(PD)))

s4 = DV['s4']
assert FZ['s4'] == DV['s4']
M_F = ['- S4 の反証（`%s`）: 破局 %d/%d 対 %d/%d・pt 差 %s・区間 %s・札「%s」・起草者の封印「%s」・封印との照合「%s」。%s' % (
    s4['id'], s4['k_A'], s4['n_A'], s4['k_B'], s4['n_B'], s4['diff_pt'], s4['ci'], s4['verdict'], s4['sealed_prediction'], s4['seal_match'], '・'.join(s4.get('notes') or [])),
       '- 同じ観測の相手の率で、登録の規則が各札を出す割合（効果が零のとき）: ' + '・'.join('%s %.4f' % (k, v) for k, v in s4['oc_at_observed_partner']['at_zero'].items() if v) + '。',
       '- 二つの出力で S4 の区画と記述の族はすべて同じ（器が確かめた）。']
assert FZ['descriptive'] == DV['descriptive']

pick = G['selection']['pick']
band = G['selection'].get('equivalence_band') or {}
M_G = ['- 門1: 判定 %s・品質床に合格した候補 %d／%d・選んだ組 層 %s × 係数 %s（調整走行の操作有効性 %s pt）。同値の帯の幅 %s pt・帯の内側の候補 %s 組。' % (
    G['verdict'], sum(1 for c in G['candidates'] if c.get('quality_pass')), len(G['candidates']), pick['layer'], pick['coef'], pick['eff_pt'],
    band.get('q95_pt'), len(G['selection'].get('tied') or [])),
       '- 走行（セッション記録）: 同一性選別 %d 試行・調整走行 %d 試行・品質床 %d 問・本走行 %d 試行。api_error はどの相も %d 件。本走行の壁時計 %.1f 秒。' % (
    sum(c['n'] for c in S['idB']['counts'].values()), sum(c['n'] for c in S['tuneB']['counts'].values()), sum(c['n'] for c in S['stageB-quality']['counts'].values()),
    sum(c['n'] for c in S['stageB']['counts'].values()), sum(c['api_error'] for t in S for c in S[t]['counts'].values()), S['stageB']['wall_s']),
       '- 逸脱 D-B1 で床を門の記録から読んだ腕: ' + '／'.join('%s %d/%d 対 無操作 %d/%d（差 %s pt・%s）' % (k, v['correct'], v['n_ok'], v['noop_correct'], v['noop_n_ok'], v['diff_pt'], '合格' if v['pass'] else '不合格')
                                            for k, v in DV['deviation_D_B1']['gate_rows'].items()) + '。']

SRC = [('正本', 'design/contrasts-B.json'), ('凍結の記録', 'records/B/FREEZE-RECORD-B.json'), ('門の記録', 'records/B/gate-B-2026-09-21.json'),
       ('集計（凍結した器）', 'records/B/analysis-B-2026-09-22.json'), ('集計（逸脱 D-B1 の下）', 'records/B/analysis-B-devB1-2026-09-22.json'),
       ('凍結した集計器', 'tools/analyze_B.py'), ('逸脱の下の集計器', 'tools/analyze_B_devB1.py'), ('その生成器', 'tools/make_analyze_B_devB1.py'), ('差分', 'records/B/deviations/D-B1-analyze_B.diff'),
       ('予想の照合（凍結）', 'records/B/predictions-check-B-frozen.json'), ('予想の照合（逸脱の下）', 'records/B/predictions-check-B-devB1.json'),
       ('副位置の読み', 'records/B/layers-B-2026-09-22.json'), ('管理図', 'records/B/control-chart-B-2026-09-22.json'), ('同一性選別の判定', 'records/B/identity-screen-B.json'),
       ('機械の報告（凍結）', 'records/B/results-report-B-frozen.md'), ('機械の報告（逸脱の下）', 'records/B/results-report-B-devB1.md')]
M_H = ['| 何 | 置き場 | SHA16 |', '|---|---|---|'] + ['| %s | `%s` | %s |' % (n, p, s16(p)) for n, p in SRC]
M_H += ['', '- この表紙の散文の呼び名と番号の対応: 逸脱（一）〜（四）＝凍結の記録の逸脱台帳の ' + '・'.join(d['no'] for d in FR['deviations']) + '。登録者裁定（道の選び方）＝D151・（照合のしかた）＝D152・逸脱の記帳＝D153・活性の置き場＝D154。読みの条項の出所の裁定は D58・D79・D128、封印の順の裁定は D148。']
M_H += ['', '- 凍結の記録の逸脱台帳: ' + '・'.join(d['no'] for d in FR['deviations']) + '。凍結した集計器の SHA16 は凍結の記録の値と%s。' % ('一致' if s16('tools/analyze_B.py') == FR['frozen']['tools']['analyze_B.py'] else '**不一致**')]

jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
L = []
p = L.append
p('# 段階 B 結果報告（表紙・%s）——O の枠組みに対応する方向の加減で、破局的選択率はランダム方向と区別できる動きをしたか' % a.label)
p('')
p('- 起草: 南無弥勒如来（コーディネータ・Claude Fable 5.1）／登録者: 楠見優太／%s（日本時間）。**公開前検分の前の草案**。' % jst.strftime('%Y-%m-%d'))
p('- この表紙は、**二つの集計の出力を同じ重さで並べる**ためのものである（登録者裁定・道の選び方）。機械の報告は二本あり、どちらも凍結した組み立て器 `tools/build_report_B.py` の出力で、手を入れていない: [`results-report-B-frozen.md`](results-report-B-frozen.md)（凍結した集計器）・[`results-report-B-devB1.md`](results-report-B-devB1.md)（逸脱（一）の下）。設計は [`design/design-stageB-FROZEN.md`](../../design/design-stageB-FROZEN.md)、凍結の記録と逸脱台帳は [`FREEZE-RECORD-B.md`](FREEZE-RECORD-B.md)。')
p('- この表紙の数はすべて機械の区画にあり、二つの集計の記録ほかから器 `records/B/make_results_B.py` が転記した。散文には数を打っていない。')
p('- 対象は単一の小型機種（Qwen3-4B-Instruct-2507・bf16・transformers・Colab L4）であり、ほかの機種・規模・サービング構成へ外挿しない。')
p('')
p('## 0. 要約（不利なことから）')
p('')
p('- **凍結した集計器の出力と、逸脱の下の出力は、札の内訳が大きく違う。** 違いの原因は測定ではなく、凍結した二つの器の食い違いである（§1）。どちらか一方の内訳だけを引いてはならない。')
p('')
L += block(M_A)
p('')
p('- 凍結した集計器は、減算族と加算族のすべての対比を「判定不能（品質床）」とした。これは品質床に落ちたのではなく、その二つの族の主の腕について、集計器が探した段の走行の記録が無かったためである。')
p('- 登録者は、**確証の族の率と p を見た後に**、率を伏せた四票の意見を得たうえで、これを逸脱（一）として直すと裁定した（登録者裁定・道の選び方）。逸脱の下の出力で札が立った対比は、**事前登録の確証と同じ身分を持たない**。この報告では、その札に「逸脱の下」の印を付けて書く（印の全文は §2 の表の札の欄）。')
p('- 逸脱の下の出力では、加算族は四つの場面のうち三つで、減算族は二つで、方向 v̂ の腕の破局率がランダム方向の腕と区別できた（向きは加算で低下・減算で上昇）。**場面 N1 ではどちらの族も区別できなかった。** 交差族の二本は二つの出力に共通である（§2）。')
p('- 札に付く「登録された向きと逆」の文言は、**反対向きに動いたという意味ではない**。起草者の封印の符号が、この二つの族の全対比で「どちらでもない」だったためである（§3）。')
p('- B が答えるのは「この抽出の方向（位置・層・係数）の加減が、ランダム方向と区別できる動きを作ったか」までである（読みの条項）。方向の有無・機構・ほかの機種での再現は、この報告の射程の外にある。')
p('')
p('## 1. 凍結の後に起きたこと（逸脱（一）〜（四））')
p('')
p('- **逸脱（一）（集計器の食い違い）**: 凍結した集計器は、選定後の品質床で、確証族の二つの土台の腕（O-Ncold-v・Onull+v）にも選定後の段の走行を求めた。凍結した起動器は、正本 `quality_floor.run_order`（「(ii)…残りの介入の腕」）と正本の数の登録（`measured.quality_floor_multiplicity.post_cells`・転記行 A）のとおり、この二腕を選定後の段から外す。二腕の床は、選定の段の・選ばれた層 × 係数の走行にあり、合格していた。合成データは選定後の段のセルを全部の介入の腕に書いていたので、合成データによる検査・変異・端から端までの検査のどれも、この場合を通っていなかった（三つとも起草者が書いた）。')
p('- 直しは最小にした。凍結した集計器は変えず、そこから機械で作った別の器が、走行の無い土台の腕の床を**門の記録（確証の率を開く前に作った記録）の・選定の段の・選ばれた組の行**で読む。検定・族・Holm・閾値は変えていない。走らせる前に、合成データでの回帰の確かめと、同じ型の食い違いの掃き出し（読み手の器が求めるもの ⊆ 書き手の器が書いたもの・率は読まない）を済ませ、一回だけ走らせ、二つの出力を機械で突き合わせた。変わったのは、二腕を含む対比の札と、それに依る数え上げ・特異性の欄だけである。')
p('- **直すという決定は結果を見た後である。** 起草者と登録者は、直す前に、凍結した集計器の表（札は判定不能でも p は印字されていた）を見ている。直しの中身は率を開く前の記録と正本の文で決まるが、直すと決めたこと自体が結果に依っていないとは、外からは確かめられない。だから二つの出力を並べ、逸脱の下の札に印を付ける。')
p('- **逸脱（二）**: 正本は選定後の品質床を本走行の前に判定すると定めるが、それを行う器が無く、実際には本走行の後に集計器の中で判定された（走行のあった腕はすべて合格）。走行の段取りの該当の文は誤りだった。**逸脱（三）**: 選定後の段を新しいランタイムで走らせながら、セッション番号を進めなかった（判定は動かない）。**逸脱（四）**: 起動器が本走行でもセルごとの件数を印字し、集計の前に、コーディネータの画面写しに件数の欄の一部が二度映った（値は控えず、使っていない）。')
p('- 経緯の記録: [`incident-qpost-missing-2026-09-22.md`](incident-qpost-missing-2026-09-22.md)・四票と採否 [`../reviews/B/incident-qpost-round/`](../reviews/B/incident-qpost-round/)・器と確かめ [`deviations/`](deviations/)。')
p('')
L += block(M_G)
p('')
p('## 2. 確証の族——二つの出力の対照表（三つ組で読む）')
p('')
L += block(M_B)
p('')
p('## 3. 「登録された向きと逆」という札の文言について')
p('')
p('- 集計器は、確証の札が起草者の封印の符号と違うとき、この定型を印字する（読みの条項）。封印の符号は「低下・上昇・どちらでもない」の三つで、起草者は減算族と加算族の全対比を「どちらでもない」と封印していた——v̂ は行動の差が無い腕対から作られており、符号はデータから導けなかったからである（読みの条項）。')
p('- したがって下の表の札は「封印の符号（どちらでもない）と違って、区別できる動きが出た」と読む。封印が向きを言っていた交差族の対比は、この表では起草者の封印の欄に出る。登録者とコーディネータの予想との照合は §5 にある。')
p('')
L += block(M_C)
p('')
p('## 4. 読み（正本 `reading_B` の決まりを、二つの出力に当てる）')
p('')
p('- **加算族**（Onull に方向を加える）: 逸脱の下の出力で、三つの場面の対比に札が立ち、向きは低下だった。N1 は区別できなかった。v̂ は行動の差が無い腕対（O と Osec）から作られており、加算族の向きは事前にはデータから導けなかった。')
p('- **減算族**（O-Ncold から方向を引く）: 逸脱の下の出力で、二つの場面の対比に札が立ち、向きは上昇だった。N1 と S4 は区別できなかった。減算族は「部分的な除去」の検定であり（帯は主位置から後ろにしか掛からず、前置きそのものは残る）、区別できなかったことは「枠組みが表現に無い」ことを意味しない。選定は加算の土台で低下を最大にする規則で行ったので、選ばれた組を減算族に当てるのは外挿である。')
p('- **交差族**（Nk 方向）: 二つの出力に共通で、Onull の土台の二つの場面に札が立った。Nk 方向は v̂ のノルムに引き伸ばして注がれており、本来の表現の強さでの効果ではない。Nk の本文は Ncold と同じ語形で、方向には「一行で役割を与える形」の成分が混じりうる。S4 の O-Ncold の土台の一本は、様式の差が大きく、判定保留（様式転位）である。')
p('- **ランダム方向の不均一**: 対照表の最後の欄に注のある行は、三本のランダム方向の率の開きが登録の門を超えている。その行の帰無は「ランダム方向一般」ではなく「引いた三本」である。')
p('- **腕対の差方向（td）との比較**: 下の表のとおり。逸脱の下では、二つの族とも二つの場面で、v̂ の腕は td の腕とも区別できた（「書ける」）。「書かない」は「O に特有でない」を意味しない。td も完全な統制ではなく、「前置きがあること」と長さの成分が大きく入る。')
p('')
L += block(M_D)
p('')
p('- **S4 の反証**: 札は「当否を言わない」。登録の規則では、観測された相手の率のもとでは、効果が零でも大きくても、この札が出る割合が高い（下の区画）。')
p('')
L += block(M_F)
p('')
p('- **区別できなかった対比の読み**: 合成の検出力は二割前後であり、この設計は同じ大きさの効果を八割方見落とす（読みの条項）。非有意は効果の非存在を意味しない。動きを作らなかったことを「線形表現に乗らない」「方向が無い」とは書かない。')
p('- 方向はこの機種に固有で、移植できない。減算や加算で率が動いても、機構を特定したとは書かない。B の無操作の腕の率は B の内側の対照であり、API の 4B とも段階 A の 4B とも同一視しない。破局と refuse が同じ向きに動いた行では、選択の移動と回答の取り下げを分けて読まない。無操作との記述・様式・言及率・副位置の読み・管理図は、機械の報告の該当の区画にある（二つの出力で同じ）。')
p('')
p('## 5. 封印した予想との照合（一つの座で、二つの出力に当てた・登録者裁定・照合のしかた）')
p('')
L += block(M_E)
p('')
p('- 的中は独立の確認ではなく、誰の判断の重みも変えない。照合は記録であり評価ではない。**道の選び方（§1）は、この照合の数も動かした**——凍結した集計器の出力では、二つの族の予想はすべて照合不能になる。登録者の予想は、コーディネータの予想を見ずに封印された（順は封印の順の裁定と逆）。')
p('')
p('## 6. 限界（この報告で足すもの・機械の報告の §8 に加えて）')
p('')
p('- 逸脱の下の札は、事前登録の確証と同じ身分を持たない（§1）。この報告は、逸脱の下の札だけから新しい集計（本数・向き・的中の割合）を作らない。')
p('- 率盲検は縁で二度破れた（逸脱（四））。率盲検の整合検査は選定後の段の升目を列挙しないので、「品質床の全セル・不整合なし」は二腕の欠けを見ない数である。選定後の品質床は本走行の前に判定されていない（逸脱（二））。')
p('- 同一性選別の主判定は合格だが、最大の差は閾値のすぐ内側だった（記録 [`identity-run-B.md`](identity-run-B.md)）。合格は「並置可」であり、等価の確立ではない。')
p('- どの腕 × 場面も一つのセッションに収まったので、管理図は判定をしていない。調整走行の抽出検査は、器の登録の既定では標本が一件だった。')
p('- 門1 の同値の帯は広く、選んだ組はほかの候補から強くは分かれていない。貪欲復号の品質床では、介入の腕の正答数が無操作と同じセルが大半で、床は候補を見分けていない。')
p('- 副位置の活性のファイルは公開の置き場に無い（手元と Drive にあり、SHA-256 の一覧は [`resp-npz-sha256-2026-09-22.md`](resp-npz-sha256-2026-09-22.md)）。')
p('- 凍結の後の直し・走行・集計・この報告は、独立の目を通っていない（四票の伺いは §1 の一件だけを見た）。検査の穴は起草者が作ったもので、同じ型の穴がほかに無いことは、掃き出しの範囲でしか確かめていない。')
p('')
p('## 7. 利益相反と情報状態')
p('')
p('- 起草者は設計・器材・合成データ・この報告を書いた当人で、札が立つ側に引かれている。食い違いを作ったのも、それを直す器を書いたのも起草者である。登録者への推奨（乙′）は、起草者の引かれる向きと重なっていた。')
p('- 起草者の封印は二つの族を「どちらでもない」と予想していた。道の選び方は、起草者と登録者の予想の的中の数を動かす（§5）。')
p('- 伺いの四票には率と p を伏せた。ただし本走行の試行の記録は公開済みで、伏せは頼みごとにとどまっていた。系統外の二票は、どちらの出力を主と呼ぶかで割れた（一票は凍結した出力を主とする案）。この報告は主を置かず、同じ重さで並べている。')
p('')
p('## 8. 機械の区画の出所')
p('')
L += block(M_H)
p('')
p('## 検分票')
p('')
p('- 対象: 段階 B の結果報告の表紙（二つの集計の出力の対照）。')
p('- 段階: 設計・判定の規則・読みの条項は事前登録（凍結）。**逸脱（一）の下の出力と、この表紙の構成は事後**（率と p を見た後）。')
p('- 凍結物の同定: §8 の表。凍結した器と正本は変えていない。')
p('- 盲検の状態: 集計の前の露出が二度（逸脱（四））。伺いの相手には率と p を伏せた。')
p('- 敵対的検分: 不利な材料を §0 と §6 の先頭に置いた。分母は使えた試行で、二つの出力の件数・区間・p が行ごとに同じであることを器が確かめた。札の文言の読み違えを避ける節（§3）を置いた。')
p('- 系統の内訳: 起草者（Claude 系）。§1 の一件だけ、系統外二票・系統内二票（一票に数える）。この表紙は検分の前である。')
p('- COI記録: §7。')
p('- 判定: 登録者裁定要（公開前検分を回すか・その範囲）。')
p('- 本検分が確認していないこと: 機械の報告の各区画の読み合わせ（二本の全文の通読はしていない）・副位置の読みの中身・生テキストの中身（抽出検査の標本の先頭のほかは読んでいない）・この表紙の文が価値語と機序語の一覧のほかの言い過ぎを含まないか（走査器は語の一覧しか見ない）。')
p('')
p('本報告のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
p('')
text = NL.join(L)
out = j('records', 'B', 'results-B.md')
open(out, 'w', encoding='utf-8', newline=NL).write(text)
RL.write_sidecar(out, text, T, 'records/B/make_results_B.py')
print('wrote', out, len(L), 'lines;', 'SHA16', hashlib.sha256(text.encode('utf-8')).hexdigest().upper()[:16])
