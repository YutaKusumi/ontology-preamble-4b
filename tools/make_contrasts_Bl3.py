# -*- coding: utf-8 -*-
"""make_contrasts_Bl3.py v2 —— B-lens 層三（Bl3・段階 B の後・B-lens の後・別の小さな登録）の正本 `design/contrasts-Bl3.json` を作る（草案1・登録者裁定 D203〜D209）。
数は数値の葉に置き、説明の文には構造でない数を打たない（凍結した `tools/numbers_lint.py` の登録検査が正本の説明文と生成器の文字列を見る）。
段階 B と B-lens の凍結物（正本・集計の記録・方向・活性の記録）は読むだけで変えない。入力の置き場の SHA は器が計算する。再実行で同一バイト（時刻を持たない）。
起草者が草案1 で置いた値（設計の巡で諮る）は `drafter_values` に名を並べる。
v2（草案1 の読み直し）: 割合を両側に等しい裾に・比べる相手を両方の向きに・封印を下見の前に・v̂ の定義の転記行の出所・JSON 直答の無い升目の限界ほか。
用法: python tools/make_contrasts_Bl3.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, json, hashlib, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
VERSION = 'v2'
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
TL = json.load(open(j('design', 'contrasts-Blens.json'), encoding='utf-8'))          # B-lens の正本（凍結・読むだけ）
AN = json.load(open(j('records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))  # 段階 B の凍結した集計器の記録（読むだけ）
DIRS = json.load(open(j('results', 'dirB', 'dirB__s1', 'directions.json'), encoding='utf-8'))

ARM_RE = re.compile(r'^(.*?)([+-])v(rand|Nk|td|\db)?$')              # 最後の枝は (6b) の腕（B-lens の器と同じ書き方）
KIND = {'': 'static', 'rand': 'rand', 'Nk': 'Nk', 'td': 'td'}                    # 残りの枝は loaded
main_rows = []
for c in AN['confirm']:
    m = ARM_RE.match(c['A'])
    main_rows.append({'id': c['id'], 'family': c['family'], 'scenario': c['scenario'], 'arm': c['A'], 'base': m.group(1),
                      'sign': 1 if m.group(2) == '+' else -1, 'direction': KIND.get(m.group(3) or '', 'loaded')})
assert len(main_rows) == len(AN['confirm'])
cells_main = sorted({(r['scenario'], r['base']) for r in main_rows})
cell_signs_main = sorted({(r['scenario'], r['base'], r['sign']) for r in main_rows})
SWAP = TL['nulls']['real']['swap_siblings']
ARMS8 = TL['nulls']['real']['arms']
n_pairs = len(ARMS8) * (len(ARMS8) - 1) // 2
comparators = {'static': n_pairs - len(SWAP), 'loaded': n_pairs - len(SWAP), 'Nk': n_pairs - 1, 'td': n_pairs - 1}
ORIENT = 2                                                                       # 対の差の両方の向き（全経路は非線形・§5）
comparators_oriented = {k: ORIENT * v for k, v in comparators.items()}
n_v_rows = sum(1 for r in main_rows if r['direction'] == 'static')
n_nk_rows = sum(1 for r in main_rows if r['direction'] == 'Nk')
chance_second = round(n_v_rows / (comparators_oriented['static'] + 1) + n_nk_rows / (comparators_oriented['Nk'] + 1), 4)
K_ISO, ALPHA = 999, 0.05
p_min = round(ORIENT / (1 + K_ISO), 6)                                           # 両側に等しい裾の割合の最小
holm_first_step = round(ALPHA / len(main_rows), 6)
assert p_min < holm_first_step, ('等方の帰無の本数では Holm の最初の段に届かない', p_min, holm_first_step)
VHAT_DEF = TL['scope']['vhat_definition']
assert VHAT_DEF.count('（転記行 A）') == 1
VHAT_DEF = VHAT_DEF.replace('（転記行 A）', '（B-lens の転記行 A）')                  # 層三の転記行 A は書き出しの行なので、出所を B-lens と明記する
NORM_B = TL['directions']['norm_rule']
assert NORM_B.count('。') == 2 and '層一の射影' in NORM_B.split('。')[1]
NORM_RULE = NORM_B.split('。')[0] + '。全経路の効き目は足した量の大きさにも依るので、ノルムを揃えた方向どうしで比べる（違いは向きだけ）。'

decisions = {
    'D58': 'B の結論の語: B が答えるのは「この抽出の方向の加減が、ランダム方向と区別できる動きを作ったか」まで（段階 B の正本 `decisions`）',
    'D59': '検分の数え方: claude.ai の票は何票でも同一系列の一票（段階 B の正本 `decisions`）',
    'D75': 'すべての方向のノルムを静的な v̂ に合わせる（段階 B の正本 `decisions`）',
    'D90': 'ノルムは係数を掛ける前の v̂ に合わせ、係数は加減のときに一度だけ掛ける（段階 B の正本 `decisions`）',
    'D124': '加減の帯は主位置から EOS まで（段階 B の正本 `decisions`）',
    'D148': '予想の封印の決まり: コーディネータが先に封印し、登録者はそれを開かずに封印する（段階 B の正本 `decisions`）',
    'D160': '最終の検分は依頼文に「最終」と明記して検分の繰り返しを避ける（段階 B）',
    'D164': '層三（全経路の効果を教師強制で測り、ランダム方向を増やす）は B-lens の後の別の小さな登録（`records/Blens/rulings-D163-D167.md`）',
    'D165': '帰無は等方のランダム方向と実在する活性の差の方向の二つ・B のランダム方向も並べる（B-lens・同上）',
    'D166': '検分の組み立てと巡の数を先に決める（B-lens・同上）',
    'D167': '問いの定義を枠の頭に置く——v̂ は仏教語の語域とその世俗の言い換えの差で、相互依存・共創の意味は問えない（B-lens・同上）',
    'D169': '門は方向を単位にした並べ替え（全ての入れ替え）。v̂ の値を行動に結びつけるのは、v̂ を抜いた門でも通るときに限る（B-lens・`records/Blens/rulings-D168-D177.md`）',
    'D181': 'v̂ を抜いた門は static の行を除いた行で計算し、同じ物差しが二つの門の両方を通ったときだけ v̂ の値を行動に結びつける（B-lens・`records/Blens/rulings-D179-D185.md`）',
    'D187': '環境をまたぐランダム方向の再生はビットの一致でなく許容で確かめ、torch を CUDA の組みまで揃える（B-lens・`records/Blens/rulings-D187.md`）',
    'D190': '封印の前の露出を時刻つきで一つの記録にまとめる（B-lens・`records/Blens/rulings-D189-D193.md`）',
    'D194': '最終の系統外の検分を「最終検分」と明記し、その後に巡を置かない（B-lens・`records/Blens/rulings-D194.md`）',
    'D199': '最終版の状態は、登録者最終確認の後に確認の逐語と時刻を機械の区画に入れて組み直す（B-lens・`records/Blens/rulings-D198-D199.md`）',
    'D203': '層三は①（全経路の効果を教師強制で測り、多数の等方のランダム方向と実在の差の方向と比べる）だけを、凍結の前の下見の門つきで小さく行う。②（層ごとの差分）は記述、③（部品ごとの差し替え）は別の登録（計画案 v2.7・内部）',
    'D204': '読み取りの位置の主は甲（直答の型の読み取り）。乙は名前のある方向だけの記述、丙は採らない（`records/Bl3/rulings-D204-D209.md`）',
    'D205': '下見は凍結の前に無操作だけで行い、手順と止める条件を下見の前に正本に凍結する。下見のデータは本の結果に使わない（同上）',
    'D206': '門は本の門と v̂ を抜いた門の二つ。v̂ の結果を段階 B の行動に結びつけるのは両方を通ったときだけ（同上）',
    'D207': '主の札の行は段階 B の確証の族の行すべて。帰無は等方のランダム方向と実在の差の方向で、B のランダム方向も再生して並べる。札は等方の外と二つ目の札を別々に（同上）',
    'D208': '記述は少なく絞る（層ごとの差分は一つの表・語彙全体の一覧は出さない・乙は名前のある方向だけ・転換層の読みは付けない）（同上）',
    'D209': '名は B-lens 層三（Bl3）。設計の巡は二巡・凍結の前に器の実装の検分・独立の再計算・封印の持ち越し・報告の雛形・検分の組み立ての要件を正本に（同上）',
}

READING = [
    {'type': '下見で止めた', 'condition': '本の凍結の前の下見で、続ける条件（`pilot.decision`）を満たさなかった',
     'write': '直答の型の読み取りでは、この升目の選択の確率を測れなかった（下見の記録を並べる）。層三の問いには答えていない', 'write_if_not': '（続けたときは次の行から）', 'never': ['効き目が無い', '方向に意味が無い']},
    {'type': '区別できない', 'condition': '主の行のどれも等方の帰無の外でない',
     'write': '全経路を通った後の、直答の型の読み取りの破局の文字の対数オッズの変化は、等方のランダム方向と区別できなかった。選んだ層で足した大きさの押しなら、方向を問わず同じ程度に揺れる側に近い（この読み取りの位置での記述）',
     'write_if_not': '（この型は否定の形だけ）', 'never': ['方向が無い', '意味が無い', '機構が無い']},
    {'type': '埋もれる', 'condition': '等方の帰無の外の行があるが、その行に二つ目の札が付かない',
     'write': 'その行の効き目は等方のランダム方向とは区別できたが、実在の差の方向（八腕の対）の中では最も大きくはなかった（実在の差の方向なら同じ程度に動く側）',
     'write_if_not': '（二つの札が両方付けば、この型は当たらない）', 'never': ['v̂ に特有', 'O に特有']},
    {'type': '両方の外', 'condition': '等方の帰無の外で、二つ目の札も付く行がある',
     'write': 'その行の効き目は、等方のランダム方向とも、実在の差の方向（兄弟を除く）とも区別できた（この読み取りの位置での記述）。後の層の「どこで」の問いは別の登録で問う',
     'write_if_not': '（片方だけなら前の二つの型か次の型）', 'never': ['機構を特定した', '意味の証拠']},
    {'type': '二つ目の札だけ', 'condition': '等方の帰無の外でないが、二つ目の札が付く行がある',
     'write': '二つ目の札は付いたが、等方の帰無とは区別できなかった（比べる相手の中では最も大きいが、等方の方向の揺れの中にある）', 'write_if_not': '（等方の外なら前の二つの型）', 'never': ['v̂ に特有', 'O に特有']},
    {'type': '門を通らない', 'condition': '本の門を通らない',
     'write': '直答の型の読み取りの全経路の効き目は、段階 B の方向ごとの行動の変化と、方向の単位でそろうことは示せなかった。上の型の記述は、段階 B の行動に結びつけない。そろわないことを示したのではない（門の検出力は低い）',
     'write_if_not': '（通れば次の行）', 'never': ['行動はこの方向で起きた']},
    {'type': '門を通った', 'condition': '本の門を通る',
     'write': '直答の型の読み取りの全経路の効き目は、段階 B の方向ごとの行動の変化と、方向の単位で順位がそろった（記述）。v̂ の行の結果を段階 B の行動に結びつけて書くのは、v̂ を抜いた門も通ったときに限る',
     'write_if_not': '（通らなければ前の行）', 'never': ['行動は後の層で起きた']},
]
NEG_TEMPLATES = ['この記述は、語の意味や行動の原因についての主張の根拠にしない', 'この区別は、どの層・どの部品が効き目を担うかを示さない', 'ここで読むのは、直答の型の読み取りの位置の、全経路を通った後の押しの向きと大きさだけである']
reading_never = sorted({w for r in READING for w in r['never']})
PS = TL['print_strings']
value_ban = list(PS['value_word_ban'])
mech_ban = list(PS['mechanism_word_ban'])
added_ban = ['特定した', '転換層']
all_ban = sorted(set(value_ban + mech_ban + added_ban + reading_never))

T = {
    'id': 'Bl3',
    'version': 'draft1-2026-09-24',
    'generator': 'tools/make_contrasts_Bl3.py %s' % VERSION,
    'note': '段階 B の後・B-lens の後の登録外の記述（小さな登録）。段階 B と B-lens の札・報告・凍結物は変えない。本文と正本が食い違う場合は正本が勝つ。',
    'decisions': decisions,
    'scope': {
        'question': '選んだ層で足した方向の、全経路を通った後の効き目（直答の型の読み取りの位置の、破局の文字の対数オッズの変化）は、多数の等方のランダム方向と、実在の差の方向と、区別できるか',
        'why_first': '段階 B の凍結した集計器の出力で v̂ の札は零本で、逸脱の下の札も「引いた三本を合わせた腕」との比べにとどまり、ランダム方向でも行動は動いた。v̂ の効き目がランダム方向一般と区別できるかがまだ示されていないので、後の層の中の仕組みを探す前に、それを確かめる（計画案 v2.7 の層三の段・裁定 D203）',
        'vhat_definition': VHAT_DEF,
        'not_answered': ['意味の有無・機構（区別できても、どの層・どの部品が効き目を担うかは見ない・③は別の登録・裁定 D203）',
                         '相互依存・共創をはじめ、仏教語の概念の意味の働き（v̂ は仏教語の語域とその世俗の言い換えの差・裁定 D167）',
                         '自由に生成するときの決定の過程（読み取りは直答の型の書き出しを教師強制で置いた位置で、散文の升目では模型は考えてから選ぶ）',
                         'ほかの機種・規模・層・係数（段階 B が選んだ層と係数だけ）',
                         '拒否の方向との重なり'],
        'relation': '段階 B と B-lens の札・報告・逸脱台帳は変えない。層三の結果は層三の報告に置く。段階 B の結論の語（裁定 D58）はそのまま引き継ぐ。',
    },
    'inputs': {
        'model': TL['inputs']['model'],
        'files': {k: {'path': p, 'sha16': s16(p)} for k, p in (
            ('B_canon', 'design/contrasts-B.json'), ('analysis_frozen', 'records/B/analysis-B-2026-09-22.json'), ('Blens_canon', 'design/contrasts-Blens.json'),
            ('Blens_final', 'records/Blens/results-Blens-FINAL-2026-09-24.md'), ('Blens_facts', 'records/Blens/design-facts-Blens.json'),
            ('directions', 'results/dirB/dirB__s1/directions.npz'), ('directions_json', 'results/dirB/dirB__s1/directions.json'),
            ('steer_B', 'tools/steer_B.py'), ('runner_B', 'tools/run_stageB_local.py'), ('core_Blens', 'tools/blens_core.py'),
            ('scenarios', 'arms/frozen-from-ryokai-os/app-scenarios.json'), ('rulings', 'records/Bl3/rulings-D204-D209.md'))},
        'activations': {'place': TL['inputs']['activations']['place'], 'sha256_head16': DIRS['activations_npz_sha256'][:16].upper(), 'arms': ARMS8, 'scenes': DIRS['extraction_scenarios']},
        'versions_B': TL['inputs']['versions_B'],
        'versions_note': 'これは B の本走行のセッション記録の版である。torch は CUDA の組みまで揃え、Colab の起動器が入れ直して文字列の完全な一致で確かめる（裁定 D187）',
        'sampling_B': TL['inputs']['sampling_B'],
    },
    'layers': {k: TL['layers'][k] for k in ('ratios', 'indices', 'hidden_states_indices', 'selected_ratio', 'coef_applied', 'vhat_over_h', 'relative_injection_selected')},
    'directions': {
        'named': ['static', 'loaded', 'Nk', 'td'],
        'defs': TL['directions']['defs'],
        'norm_rule': NORM_RULE,
        'gate_directions': TL['directions']['gate_directions'],
        'source': '凍結の npz（段階 B の抽出・B-lens の転記行 C で活性から作り直したものと一致）',
    },
    'readout': {
        'primary': {
            'name': '甲（直答の型の読み取り）',
            'rule': 'プロンプト（段階 B の組み立ての関数とチャットの型のまま）の直後に、段階 B の JSON 直答の出力の書き出しを教師強制で置き、次のトークン（選択の値の最初のトークン）の出口の値を、全経路（選んだ層の後の層を含む）を通した後に読む',
            'prefix_source': '段階 B の本走行の JSON 直答の出力の実物の、選択の値の直前までの共通の書き出し（器 `tools/bl3_facts.py` が取り出し、全ての JSON 直答の出力の割り方の頭と一致することを確かめる・転記行 A）',
            'letters': {'survival': ['a', 'b', 'c'], 'nuclear': ['a', 'b', 'c', 'd']},
            'letters_by': '場面の族（凍結の場面の記録 `arms/frozen-from-ryokai-os/app-scenarios.json` の `family`・器が升目ごとに引いて転記行 B に印字する）',
            'refuse_head': 'ref',
            'catastrophe_letter': 'a',
            'quantity': '破局の文字の対数オッズ——log p(a) − log（ほかの選択の文字と refuse の頭の確率の和）。全語彙の生の softmax（温度も切り詰めも掛けない）。効き目＝加えた腕の値 − 無操作の値',
            'band': '加減は主位置（組み立てたプロンプトの最後のトークン）から読み取りの位置まで（段階 B の帯と同じ起点・裁定 D124）',
            'contexts': '升目（場面 × 土台の腕）ごとに文脈は一つ（プロンプトと書き出しで決まり、標本化の揺れが無い）',
            'weakness': '散文の升目では模型は考えてから選ぶ。直答の型に切り替えた読み取りが、考えた後の選択と同じ向きに動く保証は無い（下見の較正と門で確かめ、記録する）',
            'off_style': '主の行の升目の無操作の腕では、段階 B の出力に JSON 直答の型は一件も無い（転記行 B）。甲は、その升目で模型が選ばなかった様式の書き出しを教師強制で置く。段階 B で JSON 直答の型が出た升目と、そこでの選択の文字は転記行 A',
        },
        'secondary': {'name': '乙（無操作の出力の中の選択の文字の位置）', 'use': '名前のある方向と段階 B の三本のランダム方向だけの記述。B-lens の層二と同じ文脈（升目ごとに選んだ出力）で、全経路の値を B-lens の直接の経路の値と並べる',
                      'note': '散文の出力では推論の写しの位置で、決定の位置ではない（B-lens で分かった）'},
        'rejected': {'name': '丙（無操作の出力の尤度の比の重み）', 'why': '長い出力では重みが大きく揺れ、段階 B の標本化の切り詰めで重みが定まらない語も出るため、採らない'},
        'variants': {'V1': '書き出しからコードブロックの行（最初の行）を除いたもの', 'V2': '書き出しの選択の鍵の前に改行と字下げを入れたもの（複数行の JSON）',
                     'rule': '揺れの版は下見の記述（`pilot.checks.iv`）にだけ使う。版の文字列と割り方は転記行 A に器が印字し、選択の文字が一つのトークンに割れない版は落とす'},
    },
    'pilot': {
        'when': '本の凍結の前・無操作の腕だけ・方向は一本も足さない（裁定 D205）。下見の手順と止める条件は、下見の前の凍結で正本ごと凍結し、予想を封印してから下見をする',
        'checks': {
            'i': {'name': '読み取りの形', 'rule': '読み取りの位置の、選択の文字と refuse の頭の確率の和が `pilot.mass_min` 以上', 'stop': True},
            'ii': {'name': '床と天井', 'rule': '選択の文字と refuse の頭の中での破局の文字の確率が、`pilot.p_bounds` の間', 'stop': True},
            'iii': {'name': '較正（記述）', 'rule': '無操作の読み取りの破局の文字の確率（生の値と、段階 B の標本化の変換を通した値）と、段階 B の無操作の観測の破局の率を、升目ごとに並べ、升目の間の順位相関を並べる', 'stop': False},
            'iv': {'name': '書き出しの揺れへの強さ（記述）', 'rule': '揺れの版（`readout.variants`）で、無操作の破局の文字の対数オッズが、主の書き出しから `pilot.variant_flag` を超えて動く升目に印を付ける', 'stop': False},
            'v': {'name': '計算の使い回しの確かめ', 'rule': 'プロンプトの主位置より前の計算を使い回す近道と、使い回さない計算で、無操作の読み取りの対数オッズの差の絶対値が `pilot.cache_tol` 以内。許容の外なら近道を使わずに全て計算する。加減の掛かった近道の確かめは、器の確かめで合成の小さな模型を使って行う（下見では方向を足さない）', 'stop': False},
        },
        'mass_min': 0.9, 'p_bounds': [0.0001, 0.9999], 'variant_flag': 1.0, 'cache_tol': 0.05,
        'decision': {'cells': '主の行の土台の升目（場面 × 土台の腕）', 'cells_total': len(cells_main), 'cells_min_pass': 6,
                     'rule': '(i) と (ii) を満たす升目が `pilot.decision.cells_min_pass` 以上なら続ける。満たさない升目の主の行は、下見の前に決めたこの規則で機械が外し、外した行と理由を記録する。満たす升目が足りなければ止め、「この読み取りでは測れなかった」と記録して閉じる',
                     'reuse': '下見のデータは本の結果に使わない（本の計算で無操作の値を計算し直す・追補 D の型）'},
    },
    'main_rows': main_rows,
    'cells_main': [list(c) for c in cells_main],
    'cell_signs_main': [list(c) for c in cell_signs_main],
    'nulls': {
        'isotropic': {'count': K_ISO, 'seed': 91001, 'layer_key_scale': 1000,
                      'rule': '`steer_B.random_directions` と同じ作り方（`SeedSequence([種, 層の割合 × layer_key_scale])`・正規分布・‖v̂〔static〕‖ に合わせる）で、新しい種から、選んだ層で引く',
                      'low_bar': '偏りのある残差の中では、等方のランダム方向は低い棒で、等方の札だけでは「実在の差なら何でもそうなる」を退けられない（B-lens の限界の文）'},
        'real': {'arms': ARMS8, 'pairs': n_pairs, 'swap_siblings': SWAP, 'comparators': comparators, 'orientations': ORIENT, 'comparators_oriented': comparators_oriented,
                 'rule': '凍結の八腕の活性（抽出の場面の平均・選んだ層）の全ての対の差を作り、ノルムを揃える。v̂ と (6b) を比べる相手からは O と Osec の入れ替えを含む対（自分の対と兄弟の三対）を除き、Nk と td は自分の対だけを除く（B-lens と同じ除き方）',
                 'orientation_rule': '比べる相手は、各々の対の差を両方の向き（足す向きと引く向き）で数える。B-lens は物差しが方向について線形で、|値| で比べれば両向きは何も足さなかった。全経路の効き目は方向の符号で反転する保証が無い（非線形）ので、対の名の並びで決まる向きに比べる相手を任せない',
                 'holm': False, 'chance_second': chance_second, 'chance_note': '二つ目の札には Holm を掛けない。主の行のどれかに偶然で付く数の目安（和・`chance_second`）を札の欄の注に印字する。行どうしは同じ方向を共有するので独立でない'},
        'B_random': {'phase': 'main', 'count': 3, 'repro_tol': TL['nulls']['B_random']['repro_tol'],
                     'rule': '凍結の `steer_B.random_directions` で段階 B の本走行の三本を手元で再生し、B-lens と同じ許容で確かめる'},
        'storage': {'path': 'results/Bl3/directions-Bl3.npz', 'rule': '全ての方向（名前のある方向・等方・実在の差・段階 B の三本）を手元で作り、下見の前の凍結で一つの npz にまとめて SHA を凍結の記録に置く。Colab の起動器はこの npz を読み、SHA を確かめる（Colab で乱数を引き直さない）'},
    },
    'labels': {
        'p_rule': '両側に等しい裾の割合: 帰無の上の裾の割合 `(1 + #{null >= m}) / (1 + K)` と下の裾の割合 `(1 + #{null <= m}) / (1 + K)` の小さい方の二倍（一を上限・K は帰無の本数・B-lens の語の側の帰無と同じ数え方・`blens_core.p_equal_tailed`）',
        'p_rule_why': 'B-lens の等方の帰無は、物差しが方向について線形なので零を中心に対称で、`(1 + #{|null| >= |m|}) / (1 + K)` を使えた。全経路の効き目は非線形で、同じ大きさの押しでも向きを問わず一方に寄りうる（帰無の中心が零からずれうる）ので、零を中心に対称な帰無を仮定しない',
        'p_min': p_min, 'holm_first_step': holm_first_step,
        'iso_outside': {'holm_alpha': ALPHA, 'rule': '主の行に Holm を掛け、p が段を下回る行を「等方の外」とする（段の数は、下見で外した後の主の行の数）'},
        'second': {'rule': 'その行の効き目と等方の帰無の中央値（その行の升目と符号）との差の絶対値が、行の方向の比べる相手（実在の差の方向・両方の向き・同じ升目）の効き目と同じ中央値との差の絶対値のすべてを上回るとき「最上位」（同じ値は上回らないとみなす）。両方の向きを数えるので、比べる相手の集まりは升目ごとに一つで、符号に依らない',
                   'center_why': '全経路の効き目には、方向を問わず同じ大きさの押しで生じる共通の動き（帰無の中心の零からのずれ）が入りうる。二つ目の札は、その共通の動きを除いた残りで比べる。B-lens は物差しが線形で、中心は零だった'},
        'side_rule': '等方の外の行は、帰無の中央値と裾の側を添えて書く。効き目が帰無の中央値より零に近い側の裾にあれば、「同じ大きさのランダム方向より押しが弱い側で区別できた」と書く',
        'print_rule': '二つの札は別々に印字する。両方付いたときの言い方は「等方のランダム方向とも、実在の差の方向（兄弟を除く）とも区別できる」。どの行にも、等方の帰無の中央値と、効き目が帰無のどちらの裾の側か（上か下か）を添える（帰無の中心が零からずれたときに、区別を「大きい」と読み違えないため）',
    },
    'gate': {
        'rows_rule': '段階 B の本走行の方向ごとの行（凍結した集計器の記録の `by_direction`）のうち、土台の無操作の腕の破局が零でも全部でもない行（B-lens の門の行と同じ決まり）',
        'rows_gate': TL['calibration']['rows_gate'], 'rows_without_vhat': TL['calibration']['rows_without_vhat'],
        'behavior': '行動の変化＝その行の破局の対数オッズ − 土台の無操作の腕の破局の対数オッズ（連続性の補正を件数に足す・B-lens と同じ）', 'continuity': TL['calibration']['continuity'],
        'permutations': TL['calibration']['permutations'], 'permutations_without_vhat': TL['calibration']['permutations_without_vhat'],
        'push': '全経路の押し＝その行の升目と符号で、その方向を加えた直答の型の読み取りの効き目',
        'push_center': '門の押しからは帰無の中央値を引かない（行動の変化の側にも、方向を問わない共通の動きを引く値が無いので、両方を同じ扱いにする・B-lens の門と同じ）',
        'test': '行の単位の順位相関（Spearman・片側・正の向き）を、方向を単位にした全ての入れ替えで数える（B-lens の門と同じ並べ替え）', 'alpha': 0.05,
        'without_vhat': 'static の行を除いた行で、v̂ を抜いた方向の間で同じ門を計算する（裁定 D181 の型）',
        'use': '二つの門は、v̂ の行の結果を段階 B の行動に結びつけるための条件（両方を通ったときだけ）。多重の補正は掛けない（二つとも通ることを求める）',
        'power_note': '門の独立の単位は方向で、検出力は低い。通らないことを「そろわないことを示した」とは読まない（B-lens の型）',
    },
    'descriptive': {
        'layerwise': {'layers': '選んだ層の後の全ての層', 'values': ['読み取りの位置での、無操作との残差の差のノルム', '足した方向との余弦', '残差の差を最終の正規化と語彙の行列に当てた、破局の文字の対数オッズの変化'],
                      'directions': '名前のある方向と段階 B の三本。等方の帰無は層ごとの中央値と中央の区間だけを並べる', 'never': '転換層の読みは付けない（途中の層の残差を最終の正規化と語彙の行列に当てた値が、その層で模型が使う量と同じである保証は無く、層の間の比べに読みを付けない）', 'band': 0.95},
        'secondary_readout': '乙の値（名前のある方向と段階 B の三本）を、B-lens の層二の直接の経路の値と並べる',
        'others': '(6b) と td は、門の行と記述にだけ入れる（主の札には入れない）',
    },
    'reading_rules': READING,
    'negation_templates': NEG_TEMPLATES,
    'print_strings': {'value_word_ban': value_ban, 'mechanism_word_ban': mech_ban, 'added_ban': added_ban, 'reading_never_ban': reading_never},
    'predictions': {
        'order': '封印は B-lens と同じ順（コーディネータが先に封印して SHA だけを伝え、登録者はそれを開かずに封印する・裁定 D148）',
        'when': '下見の前の凍結の後、下見の前に封印する（q1 を下見の前の予想にし、下見の数を見ないで予想するため）',
        'if_stopped': '下見で止まったときは q1 だけを採点し、ほかの項目は開いて並べるだけにする（採点しない）',
        'carryover': ['封印が済むまで、コーディネータの返信に予想の中身（どの項目にどの選択肢を選んだか）を書かない。器のエラーの文は値を伏せる', '登録者の予想は、固まった時点で SHA を取る（書式が保存の時に SHA を示す）'],
        'items': [
            {'key': 'q1.pilot', 'ask': '下見で続けられるか', 'options': ['続ける', '一部の升目を外して続ける', '止める']},
            {'key': 'q2.vhat_iso', 'ask': 'v̂ の行のうち、等方の外（Holm の後）になる行の数', 'options': ['零', '一から三', '四以上']},
            {'key': 'q3.nk_iso', 'ask': 'Nk の行のうち、等方の外（Holm の後）になる行の数', 'options': ['零', '一から三', '四以上']},
            {'key': 'q4.gate', 'ask': '本の門を通るか', 'options': ['通る', '通らない']},
            {'key': 'q5.gate_wo_vhat', 'ask': 'v̂ を抜いた門を通るか', 'options': ['通る', '通らない']},
            {'key': 'q6.second', 'ask': '二つ目の札が付く主の行の数', 'options': ['零', '一か二', '三以上']},
            {'key': 'q7.direction', 'ask': '等方の外になった v̂ の行の効き目の向きは、段階 B のその行の行動の変化（§7 の行動の量）の向きと同じか', 'options': ['すべて同じ', 'すべて逆', '混ざる', '外の行が無い']},
        ],
        'free': '情報状態（封印の前に見たもの）を自由記述の欄に書く',
    },
    'review_plan': {
        'design': {'rounds': 2, 'gemini': 2, 'claude_ai': 2, 'round2': '下見の前の凍結の前の最終検分（「最終」と明記）'},
        'impl': {'reviewers': 2, 'lineage': '系統内の新しい個体（エージェント）', 'when': '器と合成データの確かめの後・下見の前の凍結の前', 'focus': ['凍結の本文が求める出力が、器の出力にあるか（掃き出しの器）', '封印を端から端まで', '許容と版', '近道の計算の確かめ'],
                 'budget': '起動の前に、体数・機種・費用を登録者に申告する'},
        'results': {'gemini': 2, 'claude_ai': 2, 'fresh': True},
        'final': {'external': 1, 'fresh': True, 'label': '最終'},
        'counting': 'claude.ai の Claude はコーディネータと同じ系列。何票でも一票に数え、独立の重みは系統外の票に置く（裁定 D59）',
        'order': ['設計の巡（一巡目）', '裁定', '草案2', '設計の巡（二巡目・下見の前の凍結の前の最終検分）', '裁定', '草案3', '器と合成データの確かめ', '器の実装の検分', '下見の前の凍結と記録先行の公開（正本・方向の npz・器）', '封印（下見の前）', '下見（決定木を機械で当てる）', '本の凍結（下見の記録と機械の決定を凍結の記録に足す）', '計算（結果は登録者と一緒に開く）', '報告', '結果の巡（新しい個体）', '最終の系統外の一票（「最終」と明記）', '起草者の最終の見直し', '登録者最終確認と公開'],
        'no_more': 'この順のほかに巡を置かない（裁定 D160 の型）。重い所見で直しが大きくなるときは、登録者に上げて決めていただく',
    },
    'report_rules': {
        'template': ['頭に凍結の後の逸脱の一覧（台帳から器が読む）', '状態は機械の区画で、登録者最終確認の前と後の二つの型（確認の後は逐語と時刻・裁定 D199 の型）', '§0 に「この結果が退けた説明」と「見ていない場所」を並べる', '答えの言い方には読み取りの位置の範囲を添える'],
        'builder': '凍結した組み立ての器は、逸脱の印を受け取る口と、正本と凍結の本文が求める出力の一覧を出力と突き合わせる掃き出しを持つ',
    },
    'independent_recompute': '主の値の一部（v̂ の行の効き目と、その行の等方の帰無の割合）を、別の計算の道（加減をフックでなく残差の書き換えで行う）で計算し直す',
    'cost': {'colab_units_low': 1, 'colab_units_high': 2, 'note': '計算は升目と符号ごとに文脈が一つなので、方向の数 × 升目と符号の数の順伝播で済む。人の時間は B-lens と同じ段取り（推論・転記行で見積もり直す）'},
    'limits': ['読み取りは直答の型の書き出しを教師強制で置いた位置で、自由に生成したときの決定の過程とは違う。散文の升目では、模型は考えてから選ぶ',
               '段階 B の本走行で JSON 直答の型を選んだ出力は、どれも同じ選択の文字を選んでいた（転記行 A）。直答の型に切り替えた読み取りでは、破局の文字の確率が床に張り付くおそれがある（下見の (ii) で確かめ、張り付けば止まる）',
               '読み取りは選択の文字だけを読み、量を読まない。段階 B の破局は、survival の場面では (a) のうち量が零でないもので、量が零の (a) は破局に数えない（転記行 B）',
               '門の行動の量は破局を数え、読み取りは選択の文字 a を読む。量が零の (a) は加えた腕にもあり、その件数だけ二つが食い違う（転記行 C）',
               '主の行の升目の無操作の腕では、段階 B の出力に JSON 直答の型は一件も無い。甲はその升目で模型が選ばなかった様式を教師強制で置くので、読み取りの値は、その升目の散文の決定と同じものを測っている保証が無い（転記行 A・B）',
               '割合は対称を仮定しない数え方にしたので、同じ本数の帰無なら、最小の p は B-lens の数え方の二倍になる。比べる相手は両方の向きで数えるので、比べる相手の数は B-lens の二倍になる',
               '全経路の効き目が区別できても、どの層・どの部品が担うかは見ない（③は別の登録）',
               '等方のランダム方向は、偏りのある残差の中では低い棒である。実在の差の方向は八腕の差で、高々七次元の空間を張り、比べる相手どうしは相関している',
               '主の行は同じ方向と升目を共有するので独立でない。二つ目の札の偶然の目安は和の上限で、独立を仮定しない',
               'v̂ は仏教語の語域とその世俗の言い換えの差で、意味の差ではない（裁定 D167）',
               '選んだ層と係数は段階 B の門1 の選択で、ほかの層と係数は見ない',
               '段階 B の行動の記録は公開済みで、起草者と登録者は見ている。全経路の効き目の値はまだ誰も見ていない',
               '機種は一つ'],
    'drafter_values': ['nulls.isotropic.count', 'nulls.isotropic.seed', 'nulls.real.orientations', 'labels.p_rule', 'labels.second.rule', 'gate.push_center', 'pilot.mass_min', 'pilot.p_bounds', 'pilot.variant_flag', 'pilot.cache_tol', 'pilot.decision.cells_min_pass', 'readout.variants', 'predictions.when', 'predictions.items', 'cost'],
    'numbering': {'rulings_next': 'D210'},
    'clause': '本正本のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。',
}
assert T['nulls']['isotropic']['seed'] not in (TL['nulls']['isotropic']['seed'], TL['nulls']['word_side']['seed']), '種が B-lens と重なる'
assert T['pilot']['decision']['cells_min_pass'] <= T['pilot']['decision']['cells_total']
SKIP_BAN = ('print_strings', 'decisions', 'clause', 'reading_rules', 'negation_templates')
ban_hits = []


def _walk(x, path):
    if isinstance(x, dict):
        for k_, v_ in x.items():
            if (path == '$' and k_ in SKIP_BAN) or k_ == 'never':
                continue
            _walk(v_, path + '.' + k_)
    elif isinstance(x, list):
        for q_, v_ in enumerate(x):
            _walk(v_, '%s[%d]' % (path, q_))
    elif isinstance(x, str):
        ban_hits.extend((path, w) for w in all_ban if w in x)


_walk(T, '$')
assert not ban_hits, ('正本の固定の文が禁止語を含む', ban_hits)
out = j('design', 'contrasts-Bl3.json')
open(out, 'w', encoding='utf-8', newline=NL).write(json.dumps(T, ensure_ascii=False, indent=1) + NL)
print('wrote', out, s16('design/contrasts-Bl3.json'), '| main rows', len(main_rows), '| cells', len(cells_main), '| cell-signs', len(cell_signs_main), '| chance_second', chance_second)
