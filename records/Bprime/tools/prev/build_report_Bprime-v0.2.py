# -*- coding: utf-8 -*-
"""build_report_Bprime.py v0（2026-09-30・B′ の結果の報告の草案を組む器・層三の `tools/build_report_Bl3.py` v4 の型に、走査の二つの層を最初から入れた・コーディネータ南無弥勒如来）。

組み立て（正本 `report_rules`・`reading_rules`・`reading`・`negation_templates`・`fixed_sentences`・`cross_model`・`scan`・`limits`）:
  - 行ごとに種類を記録する: 〈決まった行〉（正本の決まった文字列か、この器の決まった型から組んだ行・〔〕に埋めるのは記録の鍵から器が取った数と識別子と正本の言い方だけ）・
    〈自由の文〉（起草者の欄と逸脱の台帳の文）・〈外す行〉（COI の開示の節・登録者の逐語・柵の文）。
  - 走査の一つ目の層（決まった行）: 行を、記録した道（正本の鍵の道か、この器の型の名）から型を引き直し、〔〕を記録した値で埋めたものと一字違わず同じことを確かめる。
    埋めた値は、数・識別子・正本と器の決まった言い方だけ。器の型の行は禁止の一覧でも走査する。「層三」「Qwen」は、正本の決まった文字列の行と「層三との並び」と §8 の表の行だけに許す。
  - 走査の二つ目の層（自由の文）: 禁止の一覧（正本 `print_strings` の一覧と `free_text_ban_bprime`）の部分一致・「層三」「Qwen」・置いてよい数の外の数・「区別でき」を止める（`bprime_core.free_text_hits`）。
  - 数はすべて決まった行に置く（自由の文に置いてよい数は、日付・時刻・SHA・コミットの短い名・節と行と升目と問いの識別子・正本の設計の定数だけ）。
  - 読みの型は、正本の読みの表の条件を器が当て、当たった型の「書く」の文（「」の中・入れ子を数えて取る）を埋めて並べる（型は重なりうる）。床の余白の印のある行は、印の文を同じ文に括弧で置く。
  - 報告の頭に、凍結の後の逸脱の一覧・一度目の下見の記録（やり直したとき）・書き出しの根の件数の定型の文と添え書き（件数に依らず）・見分ける力の無い位置の定型の文（あれば）を置く。
  - (iii) の文は読み取りの下見の記録の節に置く（T14）。二つの機種の数は「層三との並び」の節と §8 の表だけに置く（`cross_model.where`）。
入力: 集計の器の結果を開く段の出力（`records/Bprime/analysis-Bprime.json`）・一致だけを見る段の記録・凍結の記録・封印の記録と二つの予想・行動の下見の閉じた記録・転記行・層三の記録（`cross_model.bl3_keys_list`）・正本。
出力: `records/Bprime/results-Bprime.md`・`-lines.json`（行ごとの種類と道と値）・`-scan.md`（走査の結果）。走査に当たりがあれば、書いた後に非零で終わる。
用法: python build_report_Bprime.py [--force] [--rejected <起草者の行の md>] ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_gemma as G          # 凍結の器の置き場を sys.path に足す
import bprime_core as P

VERSION = 'v0.2'        # v0.2（2026-09-30）: 読みの表の型の名を正本の名に合わせた（「質量」「道の違い」→「…（B′ で足した）」・前は引けずに止まる形で、自己検査の合成の値がこの二つの枝を通らず見逃していた・Colab の合成データの確かめで見つけた・K23）・器が引く型の名がすべて正本にちょうど一つあることを自己検査で照らす・報告の頭（§0 の下見の機械の決定）にも「nuclear の族は測れなかった」を置く（正本 `pilot.decision.family`「報告の頭に」・裁定 D214・層三の器と同じ形・前は下見の節にだけ置いた・K22）。前の版は `prev/build_report_Bprime-v0.1.py`／v0.1（2026-09-30）: 報告を組む前に掃き出しの器（`sweep_Bprime`）を呼び、欠けがあれば止める（正本 `report_rules.builder`）・合成の出力を掃き出しの器が求める形にそろえた。前の版は `prev/build_report_Bprime-v0.py`
NL = chr(10)
RECS = os.path.join(ROOT, 'records', 'Bprime')
OUT = os.path.join(RECS, 'results-Bprime.md')
ToolError = P.ToolError
f4 = lambda x: 'なし' if x is None else ('%.4g' % x)
yn = lambda b: 'はい' if b else 'いいえ'
REJECTED_BLANK = '〔この結果が退けた説明: 結果を登録者と一緒に開いた後に起草者が書く〕'
CROSS_SECTIONS = ('cross', 'spread')
ID_RE = re.compile(r'^[A-Za-z0-9|:~+\-_./′\\]+$')

# ---------------- 器の決まった型（行の型・見出し・機械の表） ----------------
BT = collections.OrderedDict([
    ('title', '# B′ の結果（報告の草案・機械の組み立て）'),
    ('status_draft', '- 状態: **報告の草案（結果の巡の前）**。'),
    ('author', '- 起草: 南無弥勒如来（コーディネータ）／登録者: 楠見優太。組み立ての器: `build_report_Bprime.py` 〔版〕。'),
    ('shas', '- 正本 SHA16 〔正本〕・凍結の記録 SHA16 〔凍結〕・封印の記録 SHA16 〔封印〕・集計の出力 SHA16 〔集計〕・一致だけを見る段の記録 SHA16 〔判定〕。'),
    ('exposure', '- 封印の前の露出の記録: `records/Bprime/exposure-before-seal-Bprime.md`。'),
    ('h_dev', '## 凍結の後の逸脱'), ('dev_none', '- 無し'),
    ('h_first_pilot', '## 一度目の下見の記録（やり直した下見の前）'),
    ('h0', '## 0. 要約（できないことから）'), ('h0_not', '**見ていない場所**（正本の「この登録で答えられないこと」）:'), ('h0_rej', '**この結果が退けた説明**:'),
    ('h0_reach', '**答えの範囲**:'), ('h0_dec', '**下見の機械の決定**:'), ('h0_sum', '**全体の要約**:'), ('h0_root', '**書き出しの根の件数**（行動の下見・件数に依らず報告の頭に置く）:'),
    ('dec', '- 機械の決定: 〔決定〕・外した主の升目: 〔外した〕'), ('dec_tool', '- 器の誤りで下見を終えられなかった'),
    ('h1', '## 1. 読み取りの下見の記録（本の凍結で凍結した・無操作だけ）'),
    ('p_logit', '- 出口の値の自己検査（下見の頭）: 〔状態〕'), ('p_vi', '- (vi) (a) バッチの違いの揺れ（升目の間の最大）〔a〕・(b) バッチ一の繰り返しの揺れ（升目の間の最大）〔b〕・上限 〔上限〕'),
    ('p_vi_cell', '  - 〔升目〕: (a) 〔a〕・(b) 〔b〕'), ('p_batch', '- 本の計算のバッチの大きさ 〔バッチ〕・揺れの床 〔床〕'),
    ('p_head', '| 升目 | 無操作の対数オッズ | 選択肢 a の確率（集合の中） | 変換の後の確率 | 質量 | 行動の下見の主の率 | (i)(ii) |'), ('sep7', '|---|---|---|---|---|---|---|'),
    ('p_row', '| 〔升目〕 | 〔対数オッズ〕 | 〔確率〕 | 〔変換〕 | 〔質量〕 | 〔率〕 | 〔満たす〕 |'),
    ('p_iii', '- (iii) 較正（記述）: 順位相関 〔相関〕・升目 〔升目の数〕・除いた升目 〔除いた〕'),
    ('p_iv', '- (iv) 揺れの版 〔版〕: 〔升目〕 〔値〕（主との差 〔差〕・印 〔印〕）'),
    ('p_nuclear', '- nuclear の族は測れなかった（正本 `pilot.decision.family`）'),
    ('h2', '## 2. 主の札（等方の帰無・実在の差の方向）'),
    ('m_head', '| 行 | 方向 | 升目と符号 | 効き目 | p | 上の裾 | 下の裾 | 割合を決めた裾 | Holm の段 | 等方の外 | 等方の中央値 | 効き目の側 | 二つ目の札の中心 | 最上位 | 順位（向き） | 順位（対） | 等方の最上位の割合 | 床の余白の印 |'),
    ('sep18', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|'),
    ('m_row', '| 〔行〕 | 〔方向〕 | 〔升目と符号〕 | 〔効き目〕 | 〔p〕 | 〔上〕 | 〔下〕 | 〔裾〕 | 〔段〕 | 〔外〕 | 〔中央値〕 | 〔側〕 | 〔中心〕 | 〔最上位〕 | 〔順位向き〕 | 〔順位対〕 | 〔割合〕 | 〔印〕 |'),
    ('m_holm', '- Holm の段の数（下見で外した後の主の行の数）〔段の数〕・外した行 〔外した行〕'),
    ('m_chance', '- 二つ目の札の偶然の目安（Holm を掛けない・下見で外した後の行で数えた）: 向きまで数えて 〔向き〕・対の単位で 〔対〕'),
    ('m_floor', '- 床の余白の印の相手: (vi) の (a) の升目の間の最大 〔a〕・(b) の升目の間の最大 〔b〕'),
    ('pa_head', '| 升目と符号 | 無操作の選択肢 a の確率（選択の文字と refuse の頭の中） | 質量が下限を下回った方向（名前のある・等方・実在の差） |'), ('sep3', '|---|---|---|'),
    ('pa_row', '| 〔升目と符号〕 | 〔確率〕 | 〔名前〕・〔等方〕・〔実在〕 |'),
    ('h3', '## 3. 読み（正本の読みの表の条件を器が当てた・型は重なりうる）'),
    ('h3_neg', '**打ち消しの定型**:'),
    ('h4', '## 4. 記述（札を付けない）'),
    ('d_head', '| 升目と符号 | 等方の張り付きの割合 | 等方の四分位の幅 | 95% の中央の区間の幅 | 標準偏差 | 中央値 | 実在の差の四分位の幅 | 広がりの比 |'), ('sep8', '|---|---|---|---|---|---|---|---|'),
    ('d_row', '| 〔升目と符号〕 | 〔張り付き〕 | 〔幅〕 | 〔区間〕 | 〔標準偏差〕 | 〔中央値〕 | 〔実在の幅〕 | 〔比〕 |'),
    ('d_head_check', '- 本の計算の頭の自己検査: 出口の値 〔状態〕・最後の層 差 〔差〕（許容 〔許容〕・〔合否〕）・バッチの大きさ 〔バッチ〕'),
    ('d_layerwise', '- 層ごとの差分の値は集計の出力の `layerwise` に置いた（名前のある方向・等方は層ごとの中央値と中央の区間）'),
    ('h5', '## 5. 独立の再計算と独立の再抽出'),
    ('rc_first', '- 一段目（本の器のフック と 残差の書き換え・無操作の値と効き目の値と札）: 〔一致〕・差の最大 〔差〕（許容 〔許容〕）'),
    ('rc_second', '- 二段目（本の道 と 本の器のフック・札の一致）: 〔一致〕・効き目の差の最大 〔差〕（許容 〔許容〕・許容の内 〔内〕）'),
    ('rc_reext', '- 独立の再抽出: 〔一致〕・‖h‖ の相対の差の最大 〔h〕・‖v̂‖ の相対の差 〔v〕・名前のある方向の余弦の最小 〔余弦〕'),
    ('rc_env', '- 組の間の環境: 〔環境〕'),
    ('h6', '## 6. 行動の下見（記述・読み取りの下見の決めに使わない）'),
    ('b_head', '| 升目 | 試行 | 破局 | 主の率 | Wilson の 95% の区間 | refuse | 書式外 | JSON 直答 | 上限で切れた | 除いた率 | 採点できなかった（切れた・例外） |'), ('sep11', '|---|---|---|---|---|---|---|---|---|---|---|'),
    ('b_row', '| 〔升目〕 | 〔試行〕 | 〔破局〕 | 〔率〕 | 〔下〕〜〔上〕 | 〔refuse〕 | 〔書式外〕 | 〔直答〕 | 〔切れた〕 | 〔除いた率〕 | 〔切れ〕・〔例外〕 |'),
    ('b_root_head', '| 升目 | (a) 文字列 | (a) 番号 | (d) | 主 | V1 | V2 | V3 | 囲いあり候補外 | 囲いなし候補外 | 鍵あり値の頭が候補外 | 鍵なし | 鍵が二つ以上 | 解析器の塊 | 平らな塊 | 最後の鍵 |'),
    ('sep16', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|'),
    ('b_root_row', '| 〔升目〕 | 〔a文字列〕 | 〔a番号〕 | 〔d〕 | 〔主〕 | 〔V1〕 | 〔V2〕 | 〔V3〕 | 〔囲いあり〕 | 〔囲いなし〕 | 〔値の頭〕 | 〔鍵なし〕 | 〔二つ以上〕 | 〔塊〕 | 〔平ら〕 | 〔最後〕 |'),
    ('b_ext', '- 系統外の模型（〔系譜〕）による採点の一致: 〔一致〕／〔件数〕（欄ごとの一致: 書式の判定 〔書式〕・選択 〔選択〕・破局 〔破局〕）'),
    ('h7', '## 7. 層三との並び'), ('h8', '## 8. 揺れの広さの表（二つの機種・各機種の中の物差しで割った値）'),
    ('cm_row', '| 〔行〕 | 〔升目と符号〕 | 〔層三外〕 | 〔層三札〕 | 〔層三割合〕 | 〔層三比〕 | 〔外〕 | 〔札〕 | 〔割合〕 | 〔比〕 |'),
    ('cm_count_row', '| 〔機種〕 | 〔残った〕 | 〔外〕 | 〔札〕 |'),
    ('cm_pa_row', '| 〔升目〕 | 〔層三〕 | 〔B〕 |'),
    ('cm_len_row', '| 〔文脈〕 | 〔g本文〕 | 〔gプロンプト〕 | 〔g主位置〕 | 〔q本文〕 | 〔qプロンプト〕 | 〔q主位置〕 |'),
    ('sep10', '|---|---|---|---|---|---|---|---|---|---|'), ('sep4', '|---|---|---|---|'),
    ('sp_head', '| 升目と符号 | 層三の広がりの比 | B′ の広がりの比 |'), ('sp_row', '| 〔升目と符号〕 | 〔層三〕 | 〔B〕 |'),
    ('h9', '## 9. 予想の照合（記録であり評価ではない）'),
    ('q_head', '| 項目 | 結果 | 登録者 | コーディネータ |'), ('q_row', '| 〔項目〕 | 〔結果〕 | 〔登録者〕 | 〔コーディネータ〕 |'),
    ('q_note', '- 的中は誰の判断の重みも変えない。照合は記録であり評価ではない。'),
    ('h10', '## 10. 限界（正本の限界の文）'),
    ('h_coi', '## 作り手の関係（COI・事実の開示・走査の外）'),
    ('h_card', '## 検分票'),
    ('card', '- 本検分が確認していないこと: 読みの型の当否と起草者の欄の文は、結果の巡で見る。'),
    ('bullet', '- 〔名〕'),
])
SIDE_SIGN = {1: '符号だけ・正', -1: '符号だけ・負', 0: '符号だけ・零'}


def fill_or_verbatim(tpl, vals):
    """値を与えない型は字のまま（正本の文の中の〔〕が字の括弧のもの）、値を与えた型は〔名〕をすべて埋める（名が無ければ・埋め残しがあれば止める）。"""
    return tpl if vals is None else P.fill(tpl, vals)


def resolve(C, path):
    """正本の道（`a.b[2].c`）の値。"""
    cur = C
    for part in re.findall(r'[^.\[\]]+|\[\d+\]', path):
        cur = cur[int(part[1:-1])] if part.startswith('[') else cur[part]
    return cur


def quotes_top(s):
    """入れ子を数えて、いちばん外の「」の中身を並べる。"""
    out, depth, start = [], 0, None
    for i, ch in enumerate(s):
        if ch == '「':
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == '」':
            depth -= 1
            if depth == 0:
                out.append(s[start:i])
            if depth < 0:
                raise ToolError('「」の対がそろわない')
    if depth != 0:
        raise ToolError('「」の対がそろわない')
    return out


def rule_quote(C, typ, i=0):
    idx = [j for j, r in enumerate(C['reading_rules']) if r['type'] == typ]
    if len(idx) != 1:
        raise ToolError('読みの表の型がちょうど一つでない: %s' % typ)
    return 'reading_rules[%d].write' % idx[0], i


def side_words(C):
    q = re.findall(r'〔([^〕]*)〕', C['labels']['side_rule'])
    if len(q) != 3:
        raise ToolError('効き目の側の言い方が三つでない')
    return {'stronger': q[0], 'weaker': q[1], 'opposite': q[2]}


def side_text(C, s):
    if not s:
        return 'なし'
    if s['side'] == 'sign_only':
        return SIDE_SIGN[int(s['sign'])]
    return side_words(C)[s['side']]


class Doc:
    """行ごとの種類・道・値を記録しながら報告を組む。"""

    def __init__(self, C):
        self.C, self.lines, self.section = C, [], 'head'

    def sec(self, name, key):
        self.section = name
        self.blank()
        self.b(key)
        self.blank()

    def blank(self):
        self.lines.append({'kind': 'blank', 'text': '', 'section': self.section})

    def _add(self, src, key, tpl, vals, prefix, suffix):
        text = prefix + fill_or_verbatim(tpl, vals) + suffix
        self.lines.append({'kind': 'fixed', 'src': src, 'key': key, 'vals': None if vals is None else dict(vals), 'prefix': prefix, 'suffix': suffix, 'text': text, 'section': self.section})

    def b(self, key, vals=None, prefix='', suffix=''):
        """器の型から組む。表の行の型では、値の中の「|」を、前に逆斜線を置いた形に写す（表の区切りと読まれないように・層三の採否表 T33 の型）。"""
        if vals is not None and BT[key].startswith('|'):
            vals = {k_: (v_.replace('|', '\\|') if isinstance(v_, str) else v_) for k_, v_ in vals.items()}
        self._add('B', key, BT[key], vals, prefix, suffix)

    def c(self, path, vals=None, prefix='- ', suffix='', quote=None):
        """正本の決まった文字列から組む（quote が与えられたら、その文字列の中の「」の quote 番目）。"""
        s = resolve(self.C, path)
        tpl = quotes_top(s)[quote] if quote is not None else s
        key = path if quote is None else '%s#%d' % (path, quote)
        self._add('C', key, tpl, vals, prefix, suffix)

    def combo(self, parts, vals=None, prefix='- '):
        """二つ以上の正本の文字列を一つの行（同じ文）に組む。parts: [(道, quote か None, 前に置く字)]。"""
        tpl = ''.join(j + (quotes_top(resolve(self.C, p))[q] if q is not None else resolve(self.C, p)) for p, q, j in parts)
        text = prefix + fill_or_verbatim(tpl, vals)
        self.lines.append({'kind': 'fixed', 'src': 'combo', 'key': [list(x) for x in parts], 'vals': None if vals is None else dict(vals), 'prefix': prefix, 'suffix': '', 'text': text, 'section': self.section})

    def free(self, text):
        self.lines.append({'kind': 'free', 'text': text, 'section': self.section})

    def excluded(self, text, why):
        self.lines.append({'kind': 'excluded', 'text': text, 'why': why, 'section': self.section})

    def text(self):
        return NL.join(L['text'] for L in self.lines) + NL


# ---------------- 走査の二つの層 ----------------
def template_of(C, L):
    if L['src'] == 'B':
        return BT[L['key']]
    if L['src'] == 'C':
        path, _, q = L['key'].partition('#')
        s = resolve(C, path)
        return quotes_top(s)[int(q)] if q else s
    return ''.join(j + (quotes_top(resolve(C, p))[q] if q is not None else resolve(C, p)) for p, q, j in L['key'])


def allowed_phrases(C):
    ph = set(side_words(C).values()) | set(SIDE_SIGN.values()) | {'はい', 'いいえ', 'なし', '上', '下', '合', '否', '見分ける力無し', '一致', '不一致', '無い', '同じ', '違う', '予想しない', '採点しない',
                                                                   '満たす', '満たさない', '通った', '落ちた', 'Gemma-4-31B-it', 'Qwen3-4B', '層三', 'B′', '主', 'V1', 'V2', 'V3'}
    ph |= set(C['pilot']['decision']['q1_map'])
    for it in C['predictions']['items']:
        ph |= set(it['options'])
    return ph


def value_ok(v, phrases):
    if isinstance(v, bool):
        return True
    if isinstance(v, (int, float)):
        return True
    if not isinstance(v, str):
        return False
    return bool(ID_RE.match(v)) or v in phrases or all(bool(ID_RE.match(x)) or x in phrases for x in re.split(r'[・ ]', v) if x)


def bans_of(C, free=True):
    """禁止の一覧（正本 `scan.list`）。free=False は決まった行の型の走査（比べの語の一覧 `free_text_ban_bprime` は自由の文だけに掛ける・A1）。"""
    ps = C['print_strings']
    out = []
    for k in ('value_word_ban', 'mechanism_word_ban', 'added_ban', 'reading_never_ban', 'reading_never_ban_bprime', 'added_ban_bprime') + (('free_text_ban_bprime',) if free else ()):
        out += [w for w in ps[k] if w not in out]
    for r in C['reading_rules']:
        out += [w for w in r.get('never', []) if w not in out and not w.startswith('`')]
    out += [w for w in C['fixed_sentences']['root_counts']['never'] if w not in out]
    return out


def number_leaves(C):
    out = set()

    def walk(x):
        if isinstance(x, bool):
            return
        if isinstance(x, (int, float)):
            out.add(('%g' % x) if isinstance(x, float) else str(x))
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(C)
    return out


MASKS = [re.compile(p) for p in (r'\d{4}-\d{2}-\d{2}', r'\d{1,2}:\d{2}(?::\d{2})?', r'\b[0-9A-Fa-f]{7,64}\b', r'\bD\d{3}\b', r'\bq\d\b', r'§\s?\d+', r'\b[A-Z]\d{1,2}\b',
                                 r'[A-Za-z]+\d*\|[A-Za-z0-9\-]+(?:\|[+\-]\d)?', r'[Gg]emma-\d+(?:-[\w.]+)*', r'Qwen\d+(?:-[\w.]+)*', r'\bv\d+(?:\.\d+)*\b', r'\bG4\b')]


def scan(C, lines):
    bans = bans_of(C)
    bans_fixed = bans_of(C, free=False)
    nums = number_leaves(C)
    ph = allowed_phrases(C)
    hits = []
    for i, L in enumerate(lines, 1):
        k, t = L['kind'], L['text']
        if k in ('blank', 'excluded'):
            continue
        if k == 'fixed':
            try:
                want = L['prefix'] + fill_or_verbatim(template_of(C, L), L['vals']) + L['suffix']
            except (ToolError, KeyError, IndexError) as e:
                hits.append({'line': i, 'layer': 'fixed', 'kind': 'template', 'token': str(e)[:80]})
                continue
            if t != want:
                hits.append({'line': i, 'layer': 'fixed', 'kind': 'mismatch', 'token': t[:80]})
            badv = [v for v in (L['vals'] or {}).values() if not value_ok(v, ph)]
            if badv:
                hits.append({'line': i, 'layer': 'fixed', 'kind': 'fill_value', 'token': str(badv[:3])[:80]})
            if L['src'] == 'B':
                hits += [{'line': i, 'layer': 'fixed', 'kind': 'ban', 'token': w} for w in bans_fixed if w in BT[L['key']]]
                if L['section'] not in CROSS_SECTIONS and any(w in t for w in ('層三', 'Qwen')):
                    hits.append({'line': i, 'layer': 'fixed', 'kind': 'cross_word_outside_section', 'token': t[:60]})
            if L['src'] == 'combo' and '区別でき' in t and not all(p.startswith('reading') or p.startswith('floor_margin') for p, _, _ in L['key']):
                hits.append({'line': i, 'layer': 'fixed', 'kind': 'distinguish_outside_reading', 'token': t[:60]})
            continue
        for kind, tok in P.free_text_hits(t, bans, nums, MASKS):
            hits.append({'line': i, 'layer': 'free', 'kind': kind, 'token': tok})
    return hits


# ---------------- 組み立て ----------------
def reading_block(C, D, A):
    """読みの型（正本の読みの表の条件を器が当てる）。"""
    rows = A['rows']
    if not any(o['iso_outside'] for o in rows.values()):
        D.c(rule_quote(C, '区別できない')[0], {'n': A['rows_meta']['m_rows']}, quote=0)
    for rid, o in rows.items():
        mk = (o.get('floor_mark') or {}).get('mark')
        vals = {'行': rid, '側': side_text(C, o['side']) if o['iso_outside'] else 'なし', '値': f4(o['iso_median'])}
        if o['iso_outside']:
            typ = '両方の外' if o['second']['top'] else '埋もれる'
            parts = [(rule_quote(C, typ)[0], 0, '')] + ([('floor_margin.mark_sentences.iso_outside', None, '（')] if mk else [])
            D.combo(parts, vals)
            if mk:
                D.lines[-1]['text'] += '）'
                D.lines[-1]['suffix'] = '）'
        else:
            D.c(rule_quote(C, '外でない行')[0], {'行': rid}, quote=0)
            if o['second']['top']:
                parts = [(rule_quote(C, '二つ目の札だけ')[0], 0, '')] + ([('floor_margin.mark_sentences.second_only', None, '（')] if mk else [])
                D.combo(parts, {'行': rid})
                if mk:
                    D.lines[-1]['text'] += '）'
                    D.lines[-1]['suffix'] = '）'
    for k, m in (A['descriptive'].get('mass_below_min') or {}).items():
        n_b = sum(v['below'] for v in m.values())
        n_all = sum(v['n'] for v in m.values())
        if n_b:
            D.c(rule_quote(C, '質量（B′ で足した）')[0], {'割合': '%d/%d' % (n_b, n_all)}, prefix='- %s: ' % k if ID_RE.match(k) else '- ', quote=0)
    pd = A.get('path_difference')
    if pd and pd.get('comparable'):
        D.c(rule_quote(C, '道の違い（B′ で足した）')[0], {'数': pd['n_rows_label_differs'], '値': f4(pd['max_abs_diff'])}, quote=0)


def pilot_block(C, D, rec):
    if rec.get('tool_error'):
        D.b('dec_tool')
        return
    D.b('p_logit', {'状態': '・'.join('%s %s' % kv for kv in rec['logit_check']['states'].items())})
    if rec['logit_check'].get('n_no_discrimination'):
        D.c('fixed_sentences.no_discrimination', {'数': rec['logit_check']['n_no_discrimination']})
    vi = rec['vi']
    D.b('p_vi', {'a': f4(vi['decision']['spread_a']), 'b': f4(vi['decision']['spread_b']), '上限': f4(C['pilot']['noise_max'])})
    for k_ in vi['a']:
        D.b('p_vi_cell', {'升目': k_, 'a': f4(vi['a'][k_]), 'b': f4(vi['b'][k_])})
    dec = rec.get('decision') or {}
    if dec.get('stop') and dec.get('reason') == 'vi_b':
        return
    D.b('p_batch', {'バッチ': rec.get('batch'), '床': f4(rec.get('floor'))})
    D.blank()
    D.b('p_head')
    D.b('sep7')
    P_ = C['pilot']
    for k_, c_ in rec['cells'].items():
        D.b('p_row', {'升目': k_, '対数オッズ': f4(c_['lo']), '確率': f4(c_['pa']), '変換': f4(c_.get('pa_transformed')), '質量': f4(c_['mass']), '率': f4(c_.get('behavior_rate')),
                      '満たす': '満たす' if c_['pass_i_ii'] else '満たさない'})
    D.blank()
    iii = rec.get('iii') or {}
    if iii.get('fail'):
        D.c('pilot.iii_fail_sentences.%s' % iii['fail'])
    elif iii.get('sentence_key'):
        D.b('p_iii', {'相関': f4(iii.get('rho')), '升目の数': iii['n'], '除いた': iii['dropped_n']})
        D.c('pilot.iii_sentences.%s' % iii['sentence_key'])
    for name, v in (rec.get('iv') or {}).items():
        for c_, x in v['lo'].items():
            D.b('p_iv', {'版': name, '升目': c_, '値': f4(x), '差': f4(x - rec['cells'][c_]['lo']), '印': yn(v['flags'][c_])})
    if (rec.get('iv') or {}):
        D.c(rule_quote(C, '揺れの版の値')[0])
    if len([k_ for k_ in (dec.get('dropped') or []) if k_.startswith('N1|')]) >= 2:
        D.b('p_nuclear')


def stop_line(C, D, dec):
    """「下見で止めた」の文（止まった理由で選ぶ・閾値の添え書きを同じ文に・B′ の問いには答えていない）。"""
    path = rule_quote(C, '下見で止めた')[0]
    q = 1 if dec.get('reason') == 'vi_b' else 0
    D.combo([(path, q, ''), (path, 2, '（'), (path, 3, '）。')])


def build(C, A, preds, meta, closed, facts, bl3, deviations=(), rejected=None):
    import sweep_Bprime as SW                                           # 正本と凍結の本文が求める出力 ⊆ 集計の出力（正本 `report_rules.builder`・v0.1）
    miss = SW.sweep(C, A)
    if miss:
        raise SystemExit('掃き出しの器が欠けを見つけた（報告を組まない）: %s' % miss[:10])
    D = Doc(C)
    D.b('title')
    D.blank()
    D.b('status_draft')
    D.b('author', {'版': VERSION})
    D.b('shas', {'正本': meta['canon'], '凍結': meta['freeze'], '封印': meta['seal'], '集計': meta['analysis'], '判定': meta['judge']})
    D.b('exposure')
    D.sec('dev', 'h_dev')
    if deviations:
        for d in deviations:
            D.free('- 【逸脱 %s】%s（%s）' % (d.get('no'), d.get('what'), d.get('date')))
    else:
        D.b('dev_none')
    atts = A['pilot_attempts']
    if len(atts) > 1:
        D.sec('first_pilot', 'h_first_pilot')
        for rec in atts[:-1]:
            pilot_block(C, D, rec)
    stopped = A['predictions_meta']['stopped']
    last = atts[-1]
    dec = last.get('decision') or {}
    # 0. 要約
    D.sec('summary', 'h0')
    D.b('h0_not')
    D.blank()
    for i in range(len(C['scope']['not_answered'])):
        D.c('scope.not_answered[%d]' % i)
    D.blank()
    D.b('h0_rej')
    D.blank()
    D.free('- ' + (rejected.strip() if rejected else REJECTED_BLANK))
    D.blank()
    D.b('h0_reach')
    D.blank()
    D.c('scope.reach')
    D.c('negation_templates[2]')
    D.blank()
    D.b('h0_dec')
    D.blank()
    if last.get('tool_error'):
        D.b('dec_tool')
    else:
        D.b('dec', {'決定': dec.get('q1'), '外した': '・'.join(dec.get('dropped') or []) or 'なし'})
        if stopped:
            stop_line(C, D, dec)
        elif dec.get('dropped'):
            D.c(rule_quote(C, '下見で一部を外した')[0], quote=0)
        if len([k_ for k_ in (dec.get('dropped') or []) if k_.startswith('N1|')]) >= 2:
            D.b('p_nuclear')                                            # 報告の頭に（正本 `pilot.decision.family`・裁定 D214・v0.2）
    if not stopped and not last.get('tool_error'):
        D.blank()
        D.b('h0_sum')
        D.blank()
        S, N = C['reading']['summary'], A['summary_numbers']
        if N['k'] >= 1:
            for i in range(3):
                D.c('reading.summary.k_pos[%d]' % i, N)
        else:
            D.c('reading.summary.k_zero_first', N)
            D.c('reading.summary.k_pos[2]', N)
    D.blank()
    D.b('h0_root')
    D.blank()
    root_block(C, D, closed)
    # 1. 読み取りの下見
    D.sec('pilot', 'h1')
    pilot_block(C, D, last)
    if not stopped and not last.get('tool_error'):
        main_sections(C, D, A)
    behavior_block(C, D, closed)
    if not stopped and not last.get('tool_error'):
        cross_block(C, D, A, bl3, facts)
    # 9. 予想の照合
    D.sec('predictions', 'h9')
    D.b('q_note')
    D.blank()
    D.b('q_head')
    D.b('sep4')
    oc = A['predictions_truth']
    for it in C['predictions']['items']:
        k = it['key']
        res = oc.get(k)
        cell = lambda who: preds[who].get(k, '予想しない')
        D.b('q_row', {'項目': k, '結果': '採点しない' if res is None else res, '登録者': cell('registrant'), 'コーディネータ': cell('coordinator')})
    # 10. 限界
    D.sec('limits', 'h10')
    for i in range(len(C['limits']['carry'])):
        D.c('limits.carry[%d].bprime' % i)
    for i in range(len(C['limits']['bprime'])):
        D.c('limits.bprime[%d]' % i)
    D.sec('coi', 'h_coi')
    for k_ in ('coordinator', 'registrant', 'makers', 'lineage', 'rounds'):
        D.excluded('- ' + C['coi'][k_], 'COI の開示の節（`scan.excluded`）')
    D.sec('card', 'h_card')
    D.b('card')
    D.blank()
    D.excluded(C['clause'].replace('本正本', '本報告'), '柵の文')
    return D


def root_block(C, D, closed):
    """書き出しの根の件数の定型の文（正本 `fixed_sentences.root_counts.choose`）。"""
    rc = C['fixed_sentences']['root_counts']
    for key, s in (closed.get('summaries') or {}).items():
        r = s['root_counts']
        ch = P.root_sentence_choice({'d': r['d'], 'a_str': r['a_str'], 'a_tok': r['a_tok'], 'a_tok_error': r['a_tok_error']})
        if ch['main'] == 'one':
            D.c('fixed_sentences.root_counts.one', {'升目': key})
        elif ch['main'] == 'two':
            D.c('fixed_sentences.root_counts.two', {'升目': key, '件数': r['d']})
        else:
            D.c('fixed_sentences.root_counts.three', {'升目': key, '含む件数': r['a_str'], '分母': r['n']})
        if ch['four']:
            D.c('fixed_sentences.root_counts.four', {'升目': key, '分母': r['n'], '文字列の件数': r['a_str'], '番号の件数': r['a_tok'], '差': abs(r['a_str'] - r['a_tok'])})
    D.c('fixed_sentences.root_counts.coda')


def main_sections(C, D, A):
    rows = A['rows']
    D.sec('main', 'h2')
    D.b('m_head')
    D.b('sep18')
    for rid, o in rows.items():
        s = o['second']
        D.b('m_row', {'行': rid, '方向': o['direction'], '升目と符号': o['cell_sign'], '効き目': f4(o['effect']), 'p': f4(o['p']), '上': o['upper'], '下': o['lower'],
                      '裾': {'upper': '上', 'lower': '下'}.get(o['tail'], o['tail']), '段': f4(o['holm_step']), '外': yn(o['iso_outside']), '中央値': f4(o['iso_median']),
                      '側': side_text(C, o['side']), '中心': f4(s['center']), '最上位': yn(s['top']), '順位向き': '%d/%d' % (s['rank_oriented'], s['of_oriented']),
                      '順位対': '%d/%d' % (s['rank_pair'], s['of_pair']), '割合': f4(o['iso_top_share']), '印': yn((o.get('floor_mark') or {}).get('mark'))})
    D.blank()
    D.b('m_holm', {'段の数': A['rows_meta']['m_rows'], '外した行': '・'.join(A['rows_meta']['dropped_rows']) or 'なし'})
    D.b('m_chance', {'向き': f4(A['chance']['oriented']), '対': f4(A['chance']['pair'])})
    fl = A['rows_meta'].get('floor') or {}
    D.b('m_floor', {'a': f4(fl.get('vi_a_max')), 'b': f4(fl.get('vi_b_max'))})
    D.c('labels.print_rule')
    D.c('nulls.real.chance_note')
    D.blank()
    Dd = A['descriptive']
    D.b('pa_head')
    D.b('sep3')
    for k, v in Dd['pa_noop'].items():
        m = Dd['mass_below_min'][k]
        D.b('pa_row', {'升目と符号': k, '確率': f4(v), '名前': '%d/%d' % (m['named']['below'], m['named']['n']), '等方': '%d/%d' % (m['iso']['below'], m['iso']['n']),
                       '実在': '%d/%d' % (m['real']['below'], m['real']['n'])})
    D.c('descriptive.mass')
    D.sec('reading', 'h3')
    reading_block(C, D, A)
    D.blank()
    D.b('h3_neg')
    D.blank()
    for i in range(len(C['negation_templates'])):
        D.c('negation_templates[%d]' % i)
    D.sec('descriptive', 'h4')
    H = A['head']
    D.b('d_head_check', {'状態': '・'.join('%s %s' % kv for kv in H['logit_check']['states'].items()), '差': f4(H['layer_check']['diff']), '許容': f4(H['layer_check']['tol']),
                         '合否': '通った' if H['layer_check']['pass'] else '落ちた', 'バッチ': A['main_run']['batch']})
    D.b('d_layerwise')
    D.c('descriptive.6b_td')
    D.blank()
    D.b('d_head')
    D.b('sep8')
    for k, sp in Dd['iso_spread'].items():
        D.b('d_row', {'升目と符号': k, '張り付き': f4(Dd['iso_ties_share'][k]), '幅': f4(sp['iqr']), '区間': f4(sp['central95']), '標準偏差': f4(sp['std']), '中央値': f4(sp['median']),
                      '実在の幅': f4(sp['iqr_real']), '比': f4(sp['iqr_over_real'])})
    D.c('descriptive.ties')
    D.sec('recompute', 'h5')
    rc = A.get('recompute') or {}
    f1 = rc.get('first')
    D.b('rc_first', {'一致': ('一致' if f1['agree'] else '不一致') if f1 else '無い', '差': f4((f1 or {}).get('max_abs_diff')), '許容': f4(rc.get('tol_first'))})
    s2 = rc.get('second') or {}
    D.b('rc_second', {'一致': '一致' if s2.get('agree') else '不一致', '差': f4(s2.get('max_abs_diff')), '許容': f4(rc.get('tol_second')), '内': yn(s2.get('values_within_tol'))})
    rx = A.get('reextract') or {}
    if rx:
        D.b('rc_reext', {'一致': '一致' if rx.get('agree') else '不一致', 'h': f4(rx.get('rel_h_max')), 'v': f4(rx.get('rel_v')), '余弦': f4(rx.get('cos_min'))})
    D.b('rc_env', {'環境': '同じ' if (A.get('env') or {}).get('same') else '違う'})


def behavior_block(C, D, closed):
    D.sec('behavior', 'h6')
    D.c('behavior_pilot.reading')
    D.blank()
    D.b('b_head')
    D.b('sep11')
    for key, s in (closed.get('summaries') or {}).items():
        D.b('b_row', {'升目': key, '試行': s['n'], '破局': s['catastrophe'], '率': f4(s['rate']), '下': f4(s['wilson95'][0]), '上': f4(s['wilson95'][1]), 'refuse': s['refuse'],
                      '書式外': s['format_fail'], '直答': s['json_direct'], '切れた': s['truncated'], '除いた率': f4(s['rate_excl_truncated']),
                      '切れ': s['unscorable_by_reason']['truncated'], '例外': s['unscorable_by_reason']['scorer_error']})
    D.blank()
    D.b('b_root_head')
    D.b('sep16')
    for key, s in (closed.get('summaries') or {}).items():
        r = s['root_counts']
        cl, kr = r['classes'], r['key_rule']
        D.b('b_root_row', {'升目': key, 'a文字列': r['a_str'], 'a番号': ('器の誤りで数えられなかった' if r['a_tok_error'] else r['a_tok']), 'd': r['d'], '主': cl['主'], 'V1': cl['V1'], 'V2': cl['V2'], 'V3': cl['V3'],
                           '囲いあり': cl['囲いあり候補外'], '囲いなし': cl['囲いなし候補外'], '値の頭': cl['鍵あり値の頭が候補外'], '鍵なし': cl['鍵なし'], '二つ以上': r['multi_key'],
                           '塊': kr['scorer_block'], '平ら': kr['scorer_flat'], '最後': kr['last_key']})
    ex = closed.get('external') or {}
    if ex.get('fail'):
        D.c('fixed_sentences.external_scoring_fail')
    elif ex:
        D.b('b_ext', {'系譜': ex['lineage'], '一致': ex['agree'], '件数': ex['n'], '書式': ex['by_field']['format'], '選択': ex['by_field']['choice'], '破局': ex['by_field']['catastrophe']})


def cross_block(C, D, A, bl3, facts):
    """「層三との並び」の節と §8 の表（正本 `cross_model`・`descriptive.spread.cross`）。行はすべて正本の決まった文字列と記録の鍵から組む。"""
    H = C['cross_model']['headings_fixed']
    D.sec('cross', 'h7')
    D.c('cross_model.fixed_sentence')
    D.blank()
    D.c('cross_model.headings_fixed.counts', prefix='')
    D.b('sep4')
    if len(bl3['rows']) != bl3['m_rows'] or len(A['rows']) != A['rows_meta']['m_rows']:
        raise ToolError('残った主の行の数が札の行の数と違う')
    for name, rows in (('Qwen3-4B', bl3['rows']), ('Gemma-4-31B-it', A['rows'])):
        D.b('cm_count_row', {'機種': name, '残った': len(rows), '外': sum(1 for o in rows.values() if o['iso_outside']), '札': sum(1 for o in rows.values() if o['second']['top'])})
    D.blank()
    D.c('cross_model.headings_fixed.rows', prefix='')
    D.b('sep10')
    bst, gst = bl3['stats'], A['descriptive']['iso_spread']
    for rid, o in A['rows'].items():
        q = bl3['rows'].get(rid)
        cs = o['cell_sign']
        rq = (bst.get(cs) or {})
        ratio_q = (rq['iqr'] / rq['real_iqr']) if rq.get('real_iqr') else None
        D.b('cm_row', {'行': rid, '升目と符号': cs, '層三外': yn(q['iso_outside']) if q else 'なし', '層三札': yn(q['second']['top']) if q else 'なし', '層三割合': f4(q['iso_top_share']) if q else 'なし',
                       '層三比': f4(ratio_q), '外': yn(o['iso_outside']), '札': yn(o['second']['top']), '割合': f4(o['iso_top_share']), '比': f4((gst.get(cs) or {}).get('iqr_over_real'))})
    D.blank()
    D.c('cross_model.headings_fixed.pa', prefix='')
    D.b('sep3')
    for sc, arm in C['cells_main']:
        k = '%s|%s|+1' % (sc, arm)
        D.b('cm_pa_row', {'升目': '%s|%s' % (sc, arm), '層三': f4(bl3['pa_noop'].get(k)), 'B': f4(A['descriptive']['pa_noop'].get(k))})
    D.blank()
    D.c('cross_model.headings_fixed.lengths', prefix='')
    D.b('sep7')
    for r in facts['facts']['B']['two_models']:
        D.b('cm_len_row', {'文脈': r['context'], 'g本文': r['gemma_arm_tokens'], 'gプロンプト': r['gemma_prompt_len'], 'g主位置': r['gemma_main_position'],
                           'q本文': r['qwen_arm_tokens'], 'qプロンプト': r['qwen_prompt_len'], 'q主位置': r['qwen_main_position']})
    D.blank()
    both = set(bst) & set(gst)
    dropped = len((set(bst) | set(gst)) - both)                     # どちらかの機種で外した対（升目と符号）の数
    zero = sum(1 for k in both if not (bst[k].get('real_iqr')) or not (gst[k].get('iqr_real')))     # 割る相手が零で除いた対の数
    D.c('cross_model.headings_fixed.note', {'記録': 'cell-sensitivity-Bl3.json', 'SHA': bl3['sha16'], '外した対の数': dropped, '除いた対の数': zero})
    D.sec('spread', 'h8')
    D.b('sp_head')
    D.b('sep3')
    for k, sp in gst.items():
        if k not in bst:
            continue
        rq = bst.get(k) or {}
        D.b('sp_row', {'升目と符号': k, '層三': f4((rq['iqr'] / rq['real_iqr']) if rq.get('real_iqr') else None), 'B': f4(sp['iqr_over_real'])})


def bl3_values(C, repo):
    """層三の記録の値（正本 `cross_model.bl3_keys_list` の鍵だけ・二つの記録の SHA16 を正本 `inputs.files_public` と照らす）。"""
    sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
    fp = C['inputs']['files_public']
    cs_path = os.path.join(repo, *fp['Bl3_cell_sensitivity']['path'].split('/'))
    if sha16f(cs_path) != fp['Bl3_cell_sensitivity']['sha16']:
        raise ToolError('層三の登録外の記録の SHA16 が正本と違う')
    an = json.load(open(os.path.join(repo, 'records', 'Bl3', 'analysis-Bl3.json'), encoding='utf-8'))
    cs = json.load(open(cs_path, encoding='utf-8'))
    rows = {rid: {'iso_outside': o['iso_outside'], 'second': {'top': o['second']['top']}, 'iso_top_share': o['iso_top_share'], 'cell_sign': o['cell_sign']} for rid, o in an['rows'].items()}
    return {'rows': rows, 'm_rows': an['rows_meta']['m_rows'], 'pa_noop': dict(an['descriptive']['pa_noop']), 'stats': {k: {'iqr': v['iqr'], 'real_iqr': v['real_iqr']} for k, v in cs['stats'].items()},
            'sha16': fp['Bl3_cell_sensitivity']['sha16']}


def write(D, C, out):
    text = D.text()
    hits = scan(C, D.lines)
    open(out, 'w', encoding='utf-8', newline=NL).write(text)
    json.dump({'kind': 'bprime_report_lines', 'version': VERSION, 'lines': D.lines, 'clause': C['clause']}, open(out.replace('.md', '-lines.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1, default=str)
    L = ['# 報告の走査（機械生成・`build_report_Bprime.py` %s・走査の二つの層）' % VERSION, '', '- 行の種類: %s' % '・'.join('%s %d' % kv for kv in sorted(collections.Counter(x['kind'] for x in D.lines).items())),
         '- 当たり %d' % len(hits)] + ['- %d 行目・%s・%s: %s' % (h['line'], h['layer'], h['kind'], h['token']) for h in hits] + ['', C['clause'].replace('本正本', '本記録'), '']
    open(out.replace('.md', '-scan.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    return hits


# ---------------- 自己検査 ----------------
def _synthetic(C, drop=()):
    """合成の集計の出力（集計の器の自己検査と同じ作り方）と、行動の下見の閉じた記録・転記行・層三の値の合成。
    drop: 下見で (i)(ii) を満たさなかったことにする升目（決定は凍結の芯の `cells_decision` で出し直す・v0.2）。"""
    import numpy as np
    import analyze_Bprime as AZ
    import bl3_core as K
    Cs = json.loads(json.dumps(C))
    Cs['nulls']['isotropic']['count'] = 999
    rng = np.random.default_rng(5)
    arms = C['nulls']['real']['arms']
    pairs = ['%s~%s' % (arms[i], arms[j]) for i in range(len(arms)) for j in range(i + 1, len(arms))]
    names = {'named': list(C['directions']['named']), 'iso': ['iso:%d' % i for i in range(999)], 'real': ['real:' + p for p in pairs]}
    cs = [tuple(x) for x in C['cell_signs_main']]
    rev = [(sc, b, -g) for sc, b, g in cs if (sc, b, -g) not in cs]
    main_out = collections.OrderedDict()
    for sc, b, g in cs + rev:
        k = AZ.key3(sc, b, g)
        eff = {d: float(rng.normal(0, 0.1)) for d in names['iso'] + names['real']}
        if (sc, b, g) in cs:
            eff.update({d: float(rng.normal(0, 0.1)) for d in names['named']})
            if b == 'O-Ncold' and g == -1:
                eff['static'] = 5.0
        mass = {d: 0.95 for d in eff}
        main_out[k] = {'effects': eff, 'mass': mass, 'pa_noop': 0.3, 'lo': {K.NOOP: (9.2 if sc == 'SK' else 0.0)}, 'layers': {}}
    cells = sorted({'%s|%s' % (sc, b) for sc, b, _ in cs})
    pilot = {'decision': {'q1': '続ける', 'dropped': [], 'n_pass': 8, 'n_main': 8}, 'batch': 16, 'floor': 0.001,
             'vi': {'a': {c: (0.05 if c.startswith('SK|') else 0.002) for c in cells}, 'b': {c: 0.001 for c in cells}, 'decision': {'spread_a': 0.05, 'spread_b': 0.001}},
             'logit_check': {'states': {c: '合' for c in cells}, 'n_no_discrimination': 0},
             'cells': {c: {'lo': 0.1, 'pa': 0.4, 'pa_transformed': 0.3, 'mass': 0.95, 'pass_i_ii': True, 'behavior_rate': 0.2} for c in cells},
             'iii': {'rho': 0.5, 'n': 8, 'dropped_n': 0, 'sentence_key': 'positive'}, 'iv': {'V1': {'lo': {c: 0.2 for c in cells}, 'flags': {c: False for c in cells}}}}
    if drop:
        for c in drop:
            pilot['cells'][c]['pass_i_ii'] = False
        pilot['decision'] = K.cells_decision({c: v['pass_i_ii'] for c, v in pilot['cells'].items()}, {}, C['pilot']['decision']['cells_min_pass'])
        pilot['iii'] = dict(pilot['iii'], n=8 - len(drop), dropped_n=len(drop))
    A = AZ.analyze(Cs, main_out, [pilot], pairs, names)
    A.update({'pilot_attempts': [pilot], 'head': {'logit_check': {'states': {c: '合' for c in cells}}, 'layer_check': {'diff': 0.0, 'tol': 1e-4, 'pass': True}},
              'main_run': {'batch': 16, 'dropped': list(pilot['decision']['dropped'])}, 'env': {'same': True},
              'reextract': {'agree': True, 'keys_same': True, 'rel_h_max': 1e-7, 'rel_v': 1e-7, 'cos_min': 0.999999}})
    A['recompute'] = {'first': {'agree': True, 'max_abs_diff': 1e-6, 'values_within_tol': True, 'labels_same': True}, 'tol_first': 0.001,
                      'second': {'agree': True, 'max_abs_diff': 1e-5, 'values_within_tol': True, 'labels_same': True}, 'tol_second': 0.006}
    n_lay = 3                                                                   # 合成の層の数（v0.1: 掃き出しの器が求める形にそろえた）
    A['layerwise'] = {AZ.key3(sc, b, g): {'noop_lo': {str(j): 0.0 for j in range(n_lay)}, 'rows': {d: [[0.1, 0.2, 0.3]] * n_lay for d in names['named']},
                                          'iso_summary': {'median': [[0.0, 0.0, 0.0]] * n_lay, 'lo': [[-0.1, -0.1, -0.1]] * n_lay, 'hi': [[0.1, 0.1, 0.1]] * n_lay, 'n': 999}}
                      for sc, b, g in cs}
    A['judge_record_sha16'], A['inputs'], A['dry'] = '4' * 16, {'main': '合成'}, True
    summ = collections.OrderedDict()
    for sc, arm in C['cells_main']:
        key = '%s|%s' % (sc, arm)
        summ[key] = {'n': 40, 'catastrophe': 3, 'rate': 0.075, 'wilson95': [0.03, 0.2], 'refuse': 1, 'format_fail': 2, 'json_direct': 30, 'truncated': 0, 'rate_excl_truncated': 0.075,
                     'unscorable': 0, 'unscorable_by_reason': {'truncated': 0, 'scorer_error': 0},
                     'root_counts': {'n': 40, 'a_str': 5, 'a_tok': 5, 'a_tok_error': False, 'd': (0 if sc == 'N1' else 4), 'multi_key': 1,
                                     'classes': {c: (40 if c == '主' else 0) for c in P.CLASSES}, 'key_rule': {'scorer_block': 38, 'scorer_flat': 1, 'last_key': 0, 'no_key': 1}}}
    closed = {'summaries': summ, 'external': {'lineage': 'grok-4.7', 'agree': 39, 'n': 40, 'by_field': {'format': 40, 'choice': 39, 'catastrophe': 39}}, 'row_C': {'cells': {}}}
    A['behavior'] = {'summaries': closed['summaries'], 'row_C': closed['row_C'], 'external': closed['external']}
    facts = {'facts': {'B': {'two_models': [{'context': 'N1|O', 'gemma_arm_tokens': 100, 'gemma_prompt_len': 400, 'gemma_main_position': 399, 'qwen_arm_tokens': 110, 'qwen_prompt_len': 430, 'qwen_main_position': 429}]}}}
    bl3 = {'rows': {rid: {'iso_outside': False, 'second': {'top': False}, 'iso_top_share': 0.1, 'cell_sign': o['cell_sign']} for rid, o in A['rows'].items()},
           'm_rows': len(A['rows']), 'pa_noop': {AZ.key3(sc, b, g): 0.05 for sc, b, g in cs}, 'stats': {AZ.key3(sc, b, g): {'iqr': 1.0, 'real_iqr': 0.9} for sc, b, g in cs}, 'sha16': '0123456789ABCDEF',
           'dropped_pairs': 0, 'zero_pairs': 0}
    preds = {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '続ける', 'q2.vhat_iso': '零', 'q3.nk_iso': '零', 'q4.second': '零'}}
    meta = {'canon': '0' * 16, 'freeze': '1' * 16, 'seal': '2' * 16, 'analysis': '3' * 16, 'judge': '4' * 16}
    return Cs, A, preds, meta, closed, facts, bl3


def _selftest():
    import tempfile
    C = json.load(open(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    Cs, A, preds, meta, closed, facts, bl3 = _synthetic(C)
    D = build(Cs, A, preds, meta, closed, facts, bl3)
    hits = scan(Cs, D.lines)
    kinds = collections.Counter(x['kind'] for x in D.lines)
    assert not hits, hits[:10]
    assert kinds['free'] == 1 and kinds['fixed'] > 100, kinds          # 自由の文は起草者の欄（この結果が退けた説明）だけ（逸脱が無いときの「無し」は器の型）
    # 止まるべき当たり（二つの層）
    bad_cases = []
    D2 = build(Cs, A, preds, meta, closed, facts, bl3, rejected='層三と比べて Gemma は 12 行で区別できた（より多い）')
    h2 = scan(Cs, D2.lines)
    got = {h['kind'] for h in h2}
    bad_cases.append(('自由の文の禁止の語・層三・数・区別でき', {'ban', 'word', 'number'} <= got))
    D3 = build(Cs, A, preds, meta, closed, facts, bl3)
    i3 = next(i for i, L in enumerate(D3.lines) if L['kind'] == 'fixed' and L['src'] == 'C' and L['key'].startswith('reading_rules') and '区別できなかった' in L['text'])
    D3.lines[i3]['text'] = D3.lines[i3]['text'].replace('区別できなかった', '区別できた')
    bad_cases.append(('決まった行の書き換え', any(h['kind'] == 'mismatch' for h in scan(Cs, D3.lines))))
    D4 = build(Cs, A, preds, meta, closed, facts, bl3)
    i4 = next(i for i, L in enumerate(D4.lines) if L['kind'] == 'fixed' and L['src'] == 'B' and L['key'] == 'm_row')
    D4.lines[i4]['vals']['行'] = '主語の無い文を足した'
    D4.lines[i4]['text'] = D4.lines[i4]['prefix'] + fill_or_verbatim(BT['m_row'], D4.lines[i4]['vals'])
    bad_cases.append(('埋めた値が数でも識別子でもない', any(h['kind'] == 'fill_value' for h in scan(Cs, D4.lines))))
    D5 = build(Cs, A, preds, meta, closed, facts, bl3)
    i5 = next(i for i, L in enumerate(D5.lines) if L['kind'] == 'fixed' and L['src'] == 'B' and L['key'] == 'm_holm')
    D5.lines[i5]['section'] = 'main'
    D5.lines[i5]['text'] += '（層三）'
    D5.lines[i5]['suffix'] = '（層三）'
    bad_cases.append(('器の型の行の「層三」（節の外）', any(h['kind'] == 'cross_word_outside_section' for h in scan(Cs, D5.lines))))
    miss = [n for n, ok in bad_cases if not ok]
    assert not miss, miss
    # 器が引く読みの表の型の名が、すべて正本にちょうど一つある（v0.2・K23・器の本文から機械で拾う）
    src = open(os.path.abspath(__file__), encoding='utf-8').read()
    typs = sorted(set(re.findall(r"rule_quote\(C, '([^']+)'", src)))
    bad_t = [t for t in typs if sum(1 for r in C['reading_rules'] if r['type'] == t) != 1]
    assert typs and not bad_t, bad_t
    # 質量が下限を下回った方向がある升目と、道の違いの記述（本の計算がバッチ一に移った）の枝を合成で通す（v0.2・K23）
    Am = json.loads(json.dumps(A))
    k_m = next(iter(Am['descriptive']['mass_below_min']))
    g_m = next(iter(Am['descriptive']['mass_below_min'][k_m]))
    Am['descriptive']['mass_below_min'][k_m][g_m]['below'] = 1
    Am['main_run']['batch'] = 1
    Am['path_difference'] = {'comparable': True, 'n_rows_label_differs': 0, 'max_abs_diff': 0.0, 'rows_label_differs': []}
    Dm = build(Cs, Am, preds, meta, closed, facts, bl3)
    hm = scan(Cs, Dm.lines)
    assert not hm, hm[:5]
    got_t = {L['key'] for L in Dm.lines if L['kind'] == 'fixed' and L['src'] == 'C'}
    assert all(any(g.startswith(rule_quote(Cs, t)[0]) for g in got_t) for t in ('質量（B′ で足した）', '道の違い（B′ で足した）')), sorted(got_t)[:5]
    # N1 の二つの升目を外して続けた報告（v0.2・K22）: 報告の頭（§0）と下見の節の両方に「nuclear の族は測れなかった」
    dropN1 = sorted('%s|%s' % tuple(c) for c in C['cells_main'] if c[0] == 'N1')
    Cn, An, pn, mn, cn, fn, bn = _synthetic(C, drop=dropN1)
    Dn = build(Cn, An, pn, mn, cn, fn, bn)
    hn = scan(Cn, Dn.lines)
    assert not hn, hn[:5]
    nuc = [L['section'] for L in Dn.lines if L['kind'] == 'fixed' and L['src'] == 'B' and L['key'] == 'p_nuclear']
    assert An['pilot_attempts'][-1]['decision']['q1'] == '一部の升目を外して続ける' and 'summary' in nuc and len(nuc) == 2, nuc
    assert not [L for L in D.lines if L['kind'] == 'fixed' and L['src'] == 'B' and L['key'] == 'p_nuclear']       # 外さなければ置かない
    # 止まった下見の報告（集計の出力なし）
    stop_att = dict(A['pilot_attempts'][-1], decision={'q1': '止める', 'dropped': list(A['pilot_attempts'][-1]['cells']), 'stop': True, 'reason': 'i_ii'})
    As = {'pilot_attempts': [stop_att], 'predictions_truth': {'q1.pilot': '止める', 'q2.vhat_iso': None, 'q3.nk_iso': None, 'q4.second': None}, 'predictions_meta': {'stopped': True}}
    Ds = build(Cs, As, preds, meta, closed, facts, bl3)
    hs = scan(Cs, Ds.lines)
    assert not hs, hs[:5]
    stop_txt = [L['text'] for L in Ds.lines if L['kind'] == 'fixed' and L['src'] == 'combo']
    assert stop_txt and stop_txt[0].startswith('- この読み取りでは測れなかった（閾値は層三の登録の値を写したもので、Gemma で較正していない）。B′ の問いには答えていない'), stop_txt
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, 'r.md')
        assert write(D, Cs, out) == [] and os.path.exists(out.replace('.md', '-lines.json')) and os.path.exists(out.replace('.md', '-scan.md'))
    print('build_report_Bprime.py %s SELFTEST PASS（行 %d・決まった行 %d・自由の文 %d・外す行 %d・止まるべき当たり %d 通り・読みの表の型の名 %d・質量と道の違いの枝・N1 を外して続けた報告の頭の行・止まった下見の報告）' % (
        VERSION, len(D.lines), kinds['fixed'], kinds['free'], kinds['excluded'], len(bad_cases), len(typs)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--rejected')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    print(__doc__)
