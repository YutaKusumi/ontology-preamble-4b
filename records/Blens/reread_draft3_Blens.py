# -*- coding: utf-8 -*-
"""B-lens 草案3 の起草者の二度目の通読の記録を書く（2026-09-23・Claude Opus 5.5・登録者の依頼）。
コミット ab35ca6 の草案3 を頭から終わりまで読み直し、見つけた所を正本の器・事実の器・原稿で直して組み直した。
直す前の版はコミットにあるので、各所について、直す前の文が ab35ca6 に在って今は無いことと、直した後の文が今の草案3 か正本か器に在ることを器で確かめる
（足した所は、ab35ca6 に無く今は在ることを確かめる）。是認した所のうち機械で確かめられるものも器で確かめる。
一度目の通読の記録 `records/Blens/draft3-read-Blens.md` は ab35ca6 の草案3 についての記録なので、書き直さない。
用法: python records/Blens/reread_draft3_Blens.py"""
import os, re, json, math, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
BASE = 'ab35ca6'
P = lambda rel: os.path.join(REPO, *rel.split('/'))
rd = lambda rel: open(P(rel), encoding='utf-8').read()
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16 = lambda rel: s16b(open(P(rel), 'rb').read())
old = lambda rel: subprocess.run(['git', 'show', '%s:%s' % (BASE, rel)], cwd=REPO, capture_output=True, check=True).stdout.decode('utf-8')
DR, SRC, CA, GEN, FA, FM = ('design/design-Blens-draft3.md', 'design/design-Blens-draft3.src.md', 'design/contrasts-Blens.json',
                            'tools/make_contrasts_Blens.py', 'records/Blens/design-facts-Blens.json', 'records/Blens/design-facts-Blens.md')
LINT, MAP = 'records/Blens/numbers-lint-draft3-Blens.md', 'records/Blens/draft3-mapping-Blens.md'
NEW = {'d': rd(DR), 'c': rd(CA), 'g': rd(GEN)}
OLD = {'d': old(DR), 'c': old(CA), 'g': old(GEN)}
TL = json.load(open(P(CA), encoding='utf-8'))
TB = json.load(open(P('design/contrasts-B.json'), encoding='utf-8'))
FJ = json.load(open(P(FA), encoding='utf-8'))['facts']
LAY, BR, MOD = TL['layers'], TL['nulls']['B_random'], TL['inputs']['model']
mixed = FJ['H']['mixed_without_hiragana']
WATASHI = FJ['B']['F']['prose_sens'][0]
sens_cells = FJ['B']['F']['sens_cells'][str(WATASHI)]
cells_str = '・'.join('%s %d' % kv for kv in sens_cells.items())

# (種類, 所, 直す前〔None は足した所〕, 直した後, なぜ, 照らす先〔d 草案・c 正本・g 正本の器〕)
FIND = [
    ('中身', '§13 起草者が置いた値（足した）', None, '草案1 から置いたまま、裁定で数を決めていない値',
     '大きさの目盛りの層ごとの件数・読みの比・門の行動の量の連続性の補正・主の札と門の水準・語の一覧の数・様式の感度の上位の数は、草案1 から起草者が置いた値で、裁定で数を決めていない（裁定 D170 は件数と読みの比に触れていない）。登録者の確かめを頼む一覧から漏れていた。', 'd'),
    ('中身', '冒頭 起草者のモデル', '段階 B の記録の起草者は Claude Fable 5.1', '段階 B の設計の起草者は Claude Opus 5（凍結の直前の 2026-09-20 に Claude Fable 5.1 に替わった）',
     '不正確だった。段階 B の凍結した設計の起草の行は Claude Opus 5 で、2026-09-20 の途中の節から Claude Fable 5.1 に替わった（`design/design-stageB-FROZEN.md` の起草の行と「機種の切り替え」の注）。結果の報告の起草の行は Claude Fable 5.1。', 'd'),
    ('中身', '§3.2 語の側の帰無・字の種類', 'かなまじり（漢字か片仮名と、平仮名がまじるもの）', 'かなまじり（二つ以上の字の種類がまじるもの。平仮名を含まない漢字と片仮名のまじりも、かなまじりに入れる）',
     '器（`ctype`）は、平仮名を含まない漢字と片仮名のまじりを、かなまじりに入れていた。文の定めはそれを外しており、器と食い違っていた（候補の中に %d 個: %s）。文を器に合わせ、その数とトークンを転記行 H に印字した。' % (len(mixed), '・'.join('「%s」' % w for w in mixed)), 'd'),
    ('中身', '§4 比（対数オッズ）', '（観測の側は連続性の補正つき）。土台か行の率が零か一の行には印を付ける', '変換の後の確率が零か一で対数オッズが定まらない行では、対数オッズの比を出さず、その印を付ける',
     '切り詰めのため、変換の後の確率はちょうど零か一になりうる（観測の様式の率が零の升目で起こりうる）。そのとき対数オッズは定まらないのに、扱いを決めていなかった。', 'd'),
    ('中身', '§4 較正の検査', '主位置では様式の率（升目ごと）', '主位置では、選び方の層の升目ごとの様式の率（その升目の無操作の試行の全件が分母）',
     '較正の検査の升目と、二項分布の分母を書いていなかった。', 'd'),
    ('中身', '§4 大きさの目盛り・位置', '主位置が凍結の `steer_B.main_position` と同じで、加減の帯（主位置から EOS まで）の中にあることを', '答えの文字の位置が加減の帯（主位置から EOS まで）の中にあることを器で確かめる',
     '何が帯の中にあるかを書いていなかった（主位置は帯の起点なので、確かめるのは答えの文字の位置）。', 'd'),
    ('中身', '§9 器の自己検査・主位置', '主位置: 凍結の `steer_B.main_position` と同じで、加減の帯の中にある。', '主位置: 凍結の `steer_B.main_position` と同じであり、答えの文字の位置が加減の帯の中にある。',
     '同上。', 'd'),
    ('中身', '§9 器の自己検査（足した）', None, '語の側の帰無: 層の組み立て（層ごとの候補の数と要る数・合わせた層）が凍結の記録と一致し',
     '語の側の帰無の層の組み立てと、門の行の数の確かめが、凍結の器の自己検査に無かった（事実の器は確かめている）。外れたときは止める（裁定 D184 の「ほかは止める」）。', 'd'),
    ('中身', '§9 器の自己検査（足した）', None, '門の行: 三つの門の行の数が正本の値と一致する', '同上。', 'd'),
    ('中身', '§8 情報状態', '封印の前に設計の巡の二巡の八票とその整理（再現の表・採否表）を読んだ', '草案の設計の事実（§6 の転記行）を見られる',
     '予想者が見られる設計の事実（比を出す行と v̂ の行で比が出ないことが、封印の前に決まっていること）を書いていなかった。「読んだ」は、封印の前のことを過去で書いていた。', 'd'),
    ('中身', '§1 加えた量（フックの所）', '（抽出の hidden_states の添字と同じ所）', '抽出で取った hidden_states では一つ後の添字（`hidden_states_indices`）に当たり、同じ所である',
     '「hidden_states の添字と同じ所」は、hidden_states の添字 %d と読める。B の器は `layers[添字]` の出力に掛け、抽出は `hidden_states[添字 + 1]` を取る（`tools/direction_B.py` が一致を確かめた）。' % LAY['indices']['0.5'], 'd'),
    ('中身', '§7 限界（「私は」）', '「私は」は、O の腕の出力の書き出し', '「私は」は、O の腕（と N1 の O-Ncold）の出力の書き出し',
     '不完全だった。「私は」が最初に来た升目は、O の腕の四つと N1 の O-Ncold（全件: %s）。事実の器に、感度のトークンが最初に来た升目の全件を印字させた（前は升目ごとに上位三つしか記録に無かった）。' % cells_str, 'd'),
    ('中身', '§3.2 語の側の帰無・薄い層', '帯の真ん中の側の隣の帯と合わせ、足りるまで', '（層の帯の平均が真ん中の帯のときは下の側の隣と合わせる）',
     '真ん中の帯が薄いときの合わせ方を、文が決めていなかった。器（`merged`）は下の側の隣と合わせる。器の定めを文に書いた（いまの層では、合わせる層は無い）。', 'd'),
    ('中身', '§3.2 語の側の帰無・感度', '候補を限った語の側の帰無を並べる（記述）', '（帯の境と層の決まりは主の候補のまま・記述）',
     '器は感度でも、主の候補で決めた帯の境を使う。文に書いていなかった。', 'd'),
    ('形', '転記行 H（足した）', None, 'かなまじりのうち平仮名を含まないもの', '字の種類の直しの数とトークンを器で印字した。', 'd'),
    ('形', '転記行 B（足した）', None, '様式の感度のトークンが最初に来た升目（全件）', '「私は」の直しを確かめるため。', 'd'),
    ('形', '§1 読みの条項の出所', '（段階 B の読みの条項）。', '（段階 B の読みの条項・裁定 D128）',
     '出所の裁定番号を足した（段階 B の凍結した設計の、その読みの条項の行が裁定 D128 を引く）。正本の裁定の台帳に D128 を足した（組み立ての器は、台帳に無い裁定番号を引くと止まる）。', 'd'),
    ('形', '§12 第一巡の不採', '（語の規則の相手の数・余弦の確かめ）', '（M_E の比べる相手を語の規則で決める案・(6b) と v̂ の余弦の確かめ）',
     '要約が短すぎて、何を不採にしたかが読めなかった。第一巡の採否表の不採の二行の案の文に合わせた。', 'd'),
    ('形', '§12 登録者が見たもの（足した）', None, '草案1・草案2・草案3（設計の事実の転記行を含む）を受け取っている', '§8 の情報状態の直しに合わせた。', 'd'),
    ('形', '§2 語彙', '学習されていない詰めの行を除く）（〔転記行 G・§6〕）', '。`base_vocab` は %d（〔転記行 G・§6〕）' % MOD['base_vocab'],
     'キーの名だけで値が無く、括弧が二つ続いていた。', 'd'),
    ('形', '§3.1 段階 B のランダム方向', '段階 B のランダム方向 %d 本（本走行の種' % BR['count'],
     '段階 B のランダム方向（本走行は選んだ層の %d 本・種 %d／調整走行は層ごとに %d 本・種 %d）' % (BR['count'], BR['main_seed'], BR['count'], BR['tune_seed']),
     '本数が、本走行と調整走行を合わせた数とも読めた。', 'd'),
    ('形', '§3.2 段階 B のランダム方向の再生', '（本走行と調整走行の種・三本）', '（本走行と調整走行の種で、層ごとに引く全ての方向）', '同上。数を漢数字で手書きしていた。', 'd'),
    ('形', '正本の器・B のランダム方向の本数', "'B_random': {'count': %d," % BR['count'], "'B_random': {'count': TB['random_control']['count'],",
     '本数を手で書いていた。段階 B の正本から取る形にした（値は同じ）。', 'g'),
    ('形', '冒頭 状態（足した）', None, '起草者の二度目の通読（登録者の依頼・2026-09-23）の直しを含む', '二度目の通読の直しを含むことと、記録の所を書いた。', 'd'),
]
bad = []
for kind, where, before, after, why, tgt in FIND:
    if before is None:
        if after in OLD[tgt]:
            bad.append(('足した文が ab35ca6 に既に在る', where, after))
    else:
        if before not in OLD[tgt]:
            bad.append(('直す前の文が ab35ca6 に無い', where, before))
        if before in NEW[tgt]:
            bad.append(('直す前の文が残っている', where, before))
    if after not in NEW[tgt] and after not in NEW['c']:
        bad.append(('直した後の文が無い', where, after))

# 是認した所（機械で確かめる）
cited = re.findall(r'`([\w./-]+)`[^`\n]{0,6}?SHA16 ([0-9A-F]{16})', NEW['d'])
sha_bad = [(p_, h_) for p_, h_ in cited if os.path.exists(P(p_)) and s16(p_) != h_]
act = os.path.expanduser('~/.cache/op4b-dir/dirB__s1/main_position_activations.npz')
act_ok = None
if os.path.exists(act):
    b_ = open(act, 'rb').read()
    A_ = TL['inputs']['activations']
    act_ok = len(b_) == A_['bytes'] == TL['publication']['bytes'] and hashlib.sha256(b_).hexdigest().upper()[:16] == A_['sha256_head16']
lines = NEW['d'].split(NL)
merged = [i + 1 for i in range(2, len(lines)) if re.match(r' *- ', lines[i - 2]) and lines[i - 1] == '' and lines[i].startswith('- ')]
m_map = re.search(r'無かったもの (\d+)。', rd(MAP))
frozenB, finalB = rd('design/design-stageB-FROZEN.md'), rd('records/B/results-B-FINAL-2026-09-23.md')
at1 = [l for l in rd('records/reviews/Blens/design-round1/adoption-table-Blens-design-r1.md').split(NL) if l.startswith('| P')]
rej1 = [l.split(' | ')[0].strip('| ') for l in at1 if l.split(' | ')[3].lstrip('*').startswith('不採')]
CAL, NW = TL['calibration'], TL['nulls']['real']
o_cells = set(k for k in sens_cells if k.split('|')[1] == 'O') | {'N1|O-Ncold|prose'}
checks = [
    ('草案が SHA16 を引いたファイル（%d 件）が今のファイルと一致する' % len(cited), not sha_bad),
    ('八腕の主位置の活性のバイト数と SHA-256 の頭が正本と一致する（手元にあるとき・無ければ確かめない）', act_ok is not False),
    ('ランダム方向の作り方（`SeedSequence([種, 層の割合 × layer_key_scale])` の layer_key_scale）が凍結の器と同じ',
     'int(round(layer_ratio * %d))' % TL['nulls']['isotropic']['layer_key_scale'] in rd('tools/steer_B.py')),
    ('段階 B のランダム方向の種と本数が段階 B の正本と同じ', BR['main_seed'] == TB['random_control']['seed']['main'] and BR['tune_seed'] == TB['random_control']['seed']['tune'] and BR['count'] == TB['random_control']['count']),
    ('フックの所: 正本の hidden_states の添字が、三つの層とも復号の層の添字の一つ後', all(LAY['hidden_states_indices'][k] == LAY['indices'][k] + 1 for k in LAY['indices'])),
    ('フックの所: 段階 B の器が hidden_states[idx+1] と layers[idx] の出力の一致を確かめる', 'hidden_states[idx+1]' in rd('tools/direction_B.py')),
    ('§1 の「O と Osec は V′ の既測でどの場面でも床」が段階 B の凍結した設計にある', 'V′ の既測では O と Osec はどの場面でも床' in frozenB),
    ('段階 B の起草者の機種: 凍結した設計は Claude Opus 5 で途中から Claude Fable 5.1、結果の報告は Claude Fable 5.1',
     'コーディネータ・Claude Opus 5）' in frozenB and '機種の切り替え' in frozenB and 'コーディネータ・Claude Fable 5.1' in finalB),
    ('正本の裁定の台帳に D128 があり、段階 B の正本にも D128 がある', 'D128' in TL['decisions'] and 'D128' in TB['decisions']),
    ('並べ替えの数が方向の単位の数の階乗（本の門・v̂ を抜いた門・v̂ と (6b) を抜いた門）',
     (CAL['permutations'], CAL['permutations_without_vhat'], CAL['permutations_without_vhat_loaded']) == tuple(math.factorial(n) for n in (len(FJ['D']['eligible_by_direction']), len(FJ['D']['eligible_by_direction']) - 1, len(FJ['D']['eligible_by_direction']) - 2))),
    ('偶然で一つ付く割合の目安が、物差しの数 ÷（比べる相手の数 ＋ 一）', abs(NW['chance_one_label'] - round(NW['real_label_metrics'] / (NW['comparators']['static'] + 1), 4)) < 1e-12),
    ('転記行 G: 語彙の行 − 含める行 ＝ 追加の特別なトークン ＋ 詰めの行', MOD['vocab_size'] - MOD['base_vocab'] == (MOD['tokenizer_len'] - MOD['base_vocab']) + (MOD['vocab_size'] - MOD['tokenizer_len'])),
    ('「私は」が最初に来た升目は O の腕と N1 の O-Ncold だけ（全件）', set(sens_cells) <= o_cells and 'N1|O-Ncold|prose' in sens_cells),
    ('平仮名を含まないかなまじりの数とトークンが転記行 H と草案にある', all(('「%s」' % w) in NEW['d'] for w in mixed)),
    ('第一巡の採否表の不採は二行（§12 の文）', len(rej1) == 2),
    ('空行だけを挟んで同じ記号で続く箇条が無い', not merged),
    ('数の検査器の違反の合計が零', '違反の合計: 0' in rd(LINT)),
    ('採否表の突き合わせで無かったものが零', bool(m_map) and m_map.group(1) == '0'),
]
bad += [('是認の確かめが外れた', c, '') for c, ok in checks if not ok]
assert not bad, bad

OK = [
    '§0〜§14（§6 の転記行を含む）と検分票を頭から読み直し、上の直しのほかは、裁定 D163〜D185 と正本と設計の事実に合うと判じた（器で確かめた項は下に並べる）。',
    '§3.1 の落とした成分の式（RMSNorm の一次の展開と、−(ĥ·u／‖h‖)·ℓ(h)）と、§3.2 の等方の帰無の解析の標準偏差（係数のベクトルのノルム × ‖v̂‖ ÷ 隠れの次元の平方根）を、式で追い直した（器では確かめていない）。',
    '§4 の S4 の自然の対照の「偶然なら六分の一」（四本のうち決めた二本が上の二本に来る割合）を数え直した。',
    '§4 の門の手順（方向の組ごとの入れ替え・行の升目と腕の符号は固定・片側・Holm）が、行の数の違う方向の単位でも定まることを確かめた（家族ごとの値の組が方向と一緒に動く）。',
    '§4 の大きさの目盛りは、主位置の値が升目のプロンプトだけで決まる（その升目の一つの値）ので、比を出す行の土台の升目（S4 の O-Ncold と Osec-Ncold）が選び方の層にあることを確かめた。',
]
OPEN = [
    '一度目の通読の記録（`records/Blens/draft3-read-Blens.md`）は、コミット %s の草案3 についての記録なので、書き直していない（その器を今走らせると、今の草案3 について書き直す）。' % BASE,
    '§4 の大きさの目盛りの文に、正本のキーの名（`ci`・`z_min`・`near_band`・`calibration_check`・`letter_ratio`）を残した（一度目の通読と同じ判断）。',
    '§1 の「添字は復号の層の添字で、…選んだ層の添字の復号の層（`layers[添字]`）」は言葉が重なるが、正確さを先にした。',
    '正本の数のうち、転記行 A の表示にだけ使う `diff_merge`・凍結の器から写した `layer_key_scale`・検分の組み立ての票の数・費用の見込みは、設計の値として §13 に並べなかった（語の集合・帰無・門・目盛りの結果を変えない）。',
]
R = ['# B-lens 草案3 の起草者の二度目の通読の記録（2026-09-23・Claude Opus 5.5・登録者の依頼・器 `records/Blens/reread_draft3_Blens.py`）', '',
     '- 登録者の依頼（2026-09-23）: 凍結の前の登録者の最終の確かめの前に、草案3 を最初から最後まで見直す。',
     '- 読んだもの: コミット %s の草案3（SHA16 %s）の全文（§0〜§14・転記行・検分票）。見つけた所を、正本の器 `tools/make_contrasts_Blens.py`・事実の器 `tools/blens_facts.py`・原稿 `%s` で直し、正本・設計の事実・草案3 を組み直した。' % (BASE, s16b(OLD['d'].encode('utf-8')), SRC),
     '- 今の草案3: `%s`（SHA16 %s）・正本 `%s`（SHA16 %s）・設計の事実 `%s`（SHA16 %s）。下の各所について、直す前の文が %s に在って今は無いことと、直した後の文が今の草案3 か正本か器に在ることを器で確かめた（足した所は、%s に無く今は在ること）（%d 所・止めたもの %d）。是認した所のうち %d 項を器で確かめた。' % (DR, s16(DR), CA, s16(CA), FM, s16(FM), BASE, BASE, len(FIND), len(bad), len(checks)),
     '- 外の目: 通っていない（裁定 D178）。', '',
     '## 直した所（中身 %d・形 %d）' % (sum(1 for f in FIND if f[0] == '中身'), sum(1 for f in FIND if f[0] == '形')), '',
     '| 種類 | 所 | 直す前 | 直した後 | なぜ |', '|---|---|---|---|---|']
cell = lambda x: '（足した）' if x is None else x.replace('|', '｜').replace(NL, '⏎')
R += ['| %s | %s | %s | %s | %s |' % (k, w, cell(b), cell(a_), y) for k, w, b, a_, y, t_ in FIND]
R += ['', '## 読んで問題が無いと判じた所（是認も記録する）', ''] + ['- ' + x for x in OK]
R += ['', '器で確かめた是認（%d 項・外れたもの %d）:' % (len(checks), sum(1 for c, ok in checks if not ok)), '']
R += ['- %s: %s' % (c, '合う' if ok else '外れた') for c, ok in checks]
R += ['', '## 残した所（直さず、記録に置く）', ''] + ['- ' + x for x in OPEN]
R += ['', '## この通読が確認していないこと', '',
      '- 二度目の通読も起草者一人で、外の目を通っていない（裁定 D178）。一度目の通読の後に残っていた誤り（起草者のモデルの行・字の種類の定めと器の食い違い・§13 の一覧の漏れ）は、一度目の通読でも、設計の巡の二巡の八票でも見つかっていなかった。同じ型の見落としがまだ残る見込みがある。',
      '- 器（集合の凍結・層一・層二・起動器・組み立て・合成データ）はまだ書いていない。較正の検査の分母や、対数オッズの定まらない行の扱いが器で素直に書けるかは、器を書くときと合成データで確かめる。',
      '- 箇条のつながりは行の並びの型で機械に探した。GitHub で描かれた姿は見ていない。',
      '- 手書きの漢数字は、正本の文と原稿を型（二桁以上の漢数字と、本・件・組などの前の漢数字）で探した。「三つの層」「二つの札」のような構造の数は残した。',
      '- 正本の値そのもの（§13 に並べた値）が設計として妥当か。登録者の確かめを頼む。',
      '', '## 検分票', '',
      '- 対象: コミット %s の草案3 の全文と、それを組み立てる正本と設計の事実。' % BASE,
      '- 段階: 事前登録の前段（射影は一つも計算していない）。',
      '- 凍結物の同定: 段階 B の凍結物に触れていない。段階 B の凍結した設計と結果の報告と器は読むだけ。',
      '- 盲検の状態: 射影の値と方向どうしの余弦は、誰も見ていない。語彙の行列は、事実の器が行のノルムだけを使った。',
      '- 敵対的検分: 起草者のモデルの行（事実の誤り）・字の種類の定めと器の食い違い・§13 の一覧の漏れを、形の直しより先に置いた。直す前の文は %s に在ったことを器で確かめた。是認した所のうち %d 項を器で確かめた。' % (BASE, len(checks)),
      '- 系統の内訳: 起草者（Claude 系・Claude Opus 5.5）のみ。',
      '- COI記録: 起草者は「全て直した」「合う」と書く側に引かれる。直す前の文を %s と、直した後の文を今の版と照らすのは、その歯止め。一度目の通読と二巡の八票が見落とした誤りが見つかったことを、確認していないことの欄に書いた。' % BASE,
      '- 判定: 確定（通読の記録として）。',
      '- 本検分が確認していないこと: 上の節。',
      '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'draft3-reread-Blens.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('findings', len(FIND), 'bad', len(bad), '| checks', len(checks), '| cited', len(cited), '| act', act_ok, '| rej1', rej1, '| merged', merged)
