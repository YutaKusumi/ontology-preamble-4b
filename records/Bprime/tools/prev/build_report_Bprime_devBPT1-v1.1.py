# -*- coding: utf-8 -*-
"""build_report_Bprime_devBPT1.py v1.1 —— B′ の報告の草案の二つ目と最終版（逸脱 D-BPT1・登録者裁定 D284・D285・2026-10-01・層三の `tools/build_report_Bl3_devBLT1.py` の型・コーディネータ南無弥勒如来）。

v1（最終の系統外の検分の後・登録者裁定 D285・最終検分の採否の表 `records/reviews/Bprime/results-final/adoption-table-final-Bprime.md` の X01・X07）: `--final` で最終版を組む。
  見出しを「報告の最終版」に、状態の行を正本 `report_rules.template` の二つの型（登録者最終確認の前は「最終の系統外の検分の後・登録者最終確認の前」・確認の後は
  確認の記録 `records/Bprime/final-confirmation-Bprime.json` の逐語と時刻と会話の記録の uuid）にし（凍結した組み立ての器は草案の型しか持たない・X07）、頭の添えの一行目と検分票を最終版のものにして、
  頭の添えに最終検分の後の一行を足す。足す区画のほかの中身は草案の二つ目と同じ組み方。最終の検分を受けた草案の二つ目（置き場のファイル）は書き換えず、
  最終版との違いが決めた行（見出し・状態の行・頭の添えの一行目と足した一行・検分票の区画）だけであることを確かめる（層三の D-BLT1 の v2 の型）。
  `--final` が無ければ v0 と同じ組み方で草案の二つ目を組む（頭の添えの器の版の字は草案の二つ目を組んだ v0 のまま・置き場の草案の二つ目とバイトで同じことを照らせる）。
  最終版の出力: `records/Bprime/results-Bprime-FINAL-2026-10-01.md` と `records/Bprime/results-Bprime-FINAL-2026-10-01-checks.json`。前の版は `records/Bprime/tools/prev/build_report_Bprime_devBPT1-v0.py`。
v1.1（起草者の最終の見直しの R-a・R-b・D285 で改めると決めた検分票の区画の中）: 見直しの記録 `records/reviews/Bprime/results-final/final-read/review-final-Bprime.md` があるとき、検分票の「段階」に起草者の最終の見直しの後を足し、「系統の内訳」に系統を呼び出しの出所で数えたことを足す。前の版は `records/Bprime/tools/prev/build_report_Bprime_devBPT1-v1.py`。
以下は v0 の説明:

凍結した組み立ての器 `tools/build_report_Bprime.py` を読み込み、その本番の入口（`main_build`・頭で錠を照らす）を同じ入力（凍結の記録〔逸脱の台帳を含む〕・封印の記録と二つの予想・
集計の出力・行動の下見の閉じた記録・転記行・起草者の欄 `records/Bprime/results-draft/rejected-lines-Bprime.md`）で一時の置き場へ走らせて凍結の報告を作り直し、
置き場の `records/Bprime/results-Bprime.md` とバイトで同じことを確かめてから、見出しと状態の行を改め、【逸脱 D-BPT1】の印を付けた区画だけを足す。
区画は、生の md では始めと終わりの印の行（HTML の注釈）で囲み、凍結の報告の行のあいだに置く。凍結の報告の文と区画は、見出しと状態の行のほか一字も変えない。
足す区画は、結果の巡の採否の表（`records/reviews/Bprime/results/adoption-table-results-Bprime.md`）の W01〜W06・W12・W15・W16・W19 の注（それぞれ、指す文のそばに置く）と、
頭の添え（起草者の欄の直し〔W11〕と、下見の前の凍結を走らせた所〔W04〕）と、草案の検分票。区画に埋める値（升目の名・件数・SHA・引用・時刻）は記録と正本から器が読む。
注が言う事実は、器が記録と正本で照らす（`facts`・外れたら止める）。
確かめ: (一) 凍結の報告の作り直しがバイトで同じ（凍結した器の走査の当たり 0） (二) 印の行で囲んだ区画を除き、見出しと状態の行を戻すと、凍結の報告とバイトで同じ
  (三) 足した文を、凍結した器の自由の文の走査（`bprime_core.free_text_hits` を `build_report_Bprime` の禁止の一覧・置いてよい数・覆いで呼ぶ）に掛けて当たり 0
  （正本の打ち消しの定型の写しは、正本の決まった文字列として走査の前に除く・凍結した器も正本の文字列の行を禁止の一覧に掛けない）
  (四) 打ち消しの定型の写しが正本の文と一字違わず同じ (五) 区画を置く錨の行がそれぞれ一つに決まる (六) 注が言う事実の照らしがすべて通る。
出力: `records/Bprime/results-Bprime-draft2.md` と確かめの記録 `records/Bprime/results-Bprime-draft2-checks.json`。既にあって --force が無ければ、組んだ文を置き場のファイルと比べ、
  同じなら書かずに終わり、違えば止める。
用法: python tools/build_report_Bprime_devBPT1.py [--force]（凍結した器と同じく、`bprime_gemma` が読む環境の変数を渡す）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse, tempfile, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import build_report_Bprime as BR

VERSION = 'v1.1'
DRAFT_LABEL = 'v0'            # 草案の二つ目の頭の添えに印字した器の版（v1 でも草案の二つ目をバイトのまま組めるように残す）
NL = chr(10)
TAG = '【逸脱 D-BPT1】'
DEV = 'D-BPT1'
BEGIN, END = '<!-- 逸脱 D-BPT1 の区画: 始 -->', '<!-- 逸脱 D-BPT1 の区画: 終 -->'
P = lambda r: os.path.join(REPO, *r.split('/'))
REJ_REL = 'records/Bprime/results-draft/rejected-lines-Bprime.md'
OUT_REL, CHECKS_REL = 'records/Bprime/results-Bprime-draft2.md', 'records/Bprime/results-Bprime-draft2-checks.json'
ADOPT_REL = 'records/reviews/Bprime/results/adoption-table-results-Bprime.md'
PROV_REL = 'records/Bprime/prefreeze-Bprime-2026-10-01-colab/provenance.json'
PILOT_REL, CLOSED_REL = 'records/Bprime/pilot/pilot-Bprime.json', 'records/Bprime/behavior/behavior-closed-Bprime.json'
FR_REL, CANON_REL = 'records/Bprime/FREEZE-RECORD-Bprime.json', 'design/contrasts-Bprime.json'
T_FROZEN = '# B′ の結果（報告の草案・機械の組み立て）'
S_FROZEN = '- 状態: **報告の草案（結果の巡の前）**。'
T_DRAFT = '# B′ の結果（報告の草案の二つ目・凍結した組み立ての器の出力に逸脱の区画を足したもの）'
S_DRAFT = '- 状態: **報告の草案の二つ目**（結果の巡の後・最終の系統外の一票の前）。'
T_FINAL = '# B′ の結果（報告の最終版・凍結した組み立ての器の出力に逸脱の区画を足したもの）'
S_FINAL_PRE = '- 状態: **報告の最終版**（最終の系統外の検分の後・登録者最終確認の前）。'
S_CONF = '- 状態: **最終版**（登録者最終確認 %s 日本時間・会話の記録 uuid `%s`・逐語「%s」）。'          # 確認の後の型（正本 `report_rules.template`・裁定 D199 の型・層三と同じ字）
CONF_REL = 'records/Bprime/final-confirmation-Bprime.json'
OUT_FINAL_REL, CHECKS_FINAL_REL = 'records/Bprime/results-Bprime-FINAL-2026-10-01.md', 'records/Bprime/results-Bprime-FINAL-2026-10-01-checks.json'
ADOPT_FINAL_REL = 'records/reviews/Bprime/results-final/adoption-table-final-Bprime.md'
REPRO_FINAL_REL = 'records/reviews/Bprime/results-final/repro-final-Bprime.json'
REVIEW_REL = 'records/reviews/Bprime/results-final/final-read/review-final-Bprime.md'      # 起草者の最終の見直しの記録（v1.1）
STALE = 'Gemma の場面の出力と読み取りの値はまだ誰も見ていない'
NUC = '- nuclear の族は測れなかった（正本 `pilot.decision.family`）'
KANJI = '〇一二三四五六七八九十'
IV_RE = re.compile(r'^- \(iv\) 揺れの版 (V\d): (\S+) (\S+)（主との差 (\S+)・印 (はい|いいえ)）$')
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16 = lambda p: s16b(open(p, 'rb').read())
ld = lambda p: json.load(open(p, encoding='utf-8'))


def uniq(idx, what):
    if len(idx) != 1:
        raise SystemExit('錨の行が一つに決まらない（止める・(五)）: %s（%d）' % (what, len(idx)))
    return idx[0]


def table_last(L, i_hdr):
    """表の見出しの添字から、表の最後の行の添字（見出しの次は区切りの行）。"""
    k = i_hdr + 2
    while k < len(L) and L[k].startswith('| '):
        k += 1
    return k - 1


def facts(C, FR, L, final=False):
    """注が言う事実を記録と正本で照らし、区画に埋める値を返す（外れたら止める・(六)）。final は最終版の事実も照らす（v1）。"""
    F, done = {}, []

    def ok(cond, what):
        if not cond:
            raise SystemExit('注の事実の照らしが外れた（止める・(六)）: ' + what)
        done.append(what)
    pil, closed = ld(P(PILOT_REL)), ld(P(CLOSED_REL))
    runs = {r['phase']: r for r in FR['main_freeze']['runs']['table']}
    st = {ph: ld(P('records/Bprime/runs/' + r['start']['file'])) for ph, r in runs.items()}
    sess = FR['main_freeze']['sessions']
    es = C['behavior_pilot']['external_scoring']
    # W01
    ok(json.dumps(C, ensure_ascii=False).count(STALE) == 1, 'W01: 限界の一文は正本の文で、正本に一度だけある')
    ok(closed['external']['n'] == es['n'] and closed['external']['lineage'] == closed['external']['model_requested'], 'W01: 系統外の採点の件数は正本の数で、系統の名は呼んだ模型の名')
    ok('読み取りの下見の前' in C['behavior_pilot']['order'] and '公開の置き場に置く' in C['behavior_pilot']['order'], 'W01: 正本 behavior_pilot.order は閉じた記録の公開を読み取りの下見の前に置く')
    ok(st['pilot'].get('closed_record_sha16') == s16(P(CLOSED_REL)), 'W01: 読み取りの下見の起動の記録は閉じた記録の SHA を照らした')
    ok(closed['closed_jst'] < st['pilot']['time_jst'], 'W01: 閉じた時刻は読み取りの下見の起動の前')
    ok(all(k in pil for k in ('cells', 'decision')), 'W01: 読み取りの下見の値と機械の決定は同じ走りの記録にある')
    F['n_ext'] = es['n']
    # W02
    ok('一致の記述で、妥当性の測定ではない' in es['rule'], 'W02: 正本の採点の決まりに断りがある')
    ok('一致の記述で、妥当性の測定ではない' in open(P(CLOSED_REL[:-5] + '.md'), encoding='utf-8').read(), 'W02: 閉じた記録の md に断りがある')
    ext = [x for x in L if x.startswith('- 系統外の模型（') and 'による採点の一致' in x]
    ok(len(ext) == 1 and '妥当性' not in ext[0], 'W02: §6 の一致の行に断りが無い')
    ok(len([x for x in L if '採点で Gemma の応答を読んだ同じ模型が、結果の巡でも票を持つ' in x]) == 1, 'W02: §10 に、採点した模型が結果の巡でも票を持つ限界の文がある')
    # W03
    i1 = uniq([i for i, x in enumerate(L) if x.startswith('| 升目 | 無操作の対数オッズ | 選択肢 a の確率（集合の中） |')], '§1 の表')
    ceil, cells, eq, out1 = C['pilot']['p_bounds'][1], pil['cells'], [], []
    ac = ld(P('records/Bprime/analysis-Bprime.json'))['pilot_attempts'][-1]['cells']
    ok(sorted(ac) == sorted(cells) and all(ac[c][f] == cells[c][f] for c in cells for f in ('lo', 'pa', 'mass', 'pass_i_ii')), 'W03: 表を組んだ集計の出力の値は下見の記録の値と同じ')
    for r in L[i1 + 2:table_last(L, i1) + 1]:
        cs = r[2:-2].split(' | ')
        name, pa_s, mass_s = cs[0].replace('\\|', '|'), cs[2], cs[4]
        rec = cells[name]
        if rec['pass_i_ii'] and float(pa_s) == ceil and rec['pa'] < ceil:
            eq.append(name)
        if rec['pa'] > ceil:
            ok(pa_s == '1' and rec['pa'] != 1.0 and not rec['pass_i_ii'], 'W03: 天井の外の %s の確率の表示は「1」で、記録はちょうど一でない' % name)
            out1.append(name)
        ok(mass_s == '1' and rec['mass'] != 1.0, 'W03: %s の質量の表示は「1」で、記録はちょうど一でない' % name)
    ok(len(eq) == 1 and len(out1) >= 1, 'W03: 満たした升目のうち、表示が天井と同じ字で記録が天井の内のものが一つ・天井の外の升目がある')
    vf, n_iv, edge = C['pilot']['variant_flag'], 0, []
    for x in L:
        m = IV_RE.match(x)
        if not m:
            continue
        v, c, d_s, flag = m.group(1), m.group(2), m.group(4), m.group(5) == 'はい'
        d = pil['iv'][v]['lo'][c] - cells[c]['lo']
        ok(flag == bool(pil['iv'][v]['flags'][c]) == (abs(d) > vf), 'W03: 揺れの版 %s %s の印は記録の値の印' % (v, c))
        n_iv += 1
        if abs(float(d_s)) == vf and abs(d) != vf:
            edge.append('%s %s' % (v, c))
    ok(n_iv == 3 * len(cells) and len(edge) >= 1, 'W03: 揺れの版の行がそろい、表示が境と同じ字で記録が境と違う行がある')
    F['eq_ceil'], F['n_out'], F['iv_edge'] = eq[0], len(out1), edge
    # W04
    ok(FR['checks']['colab_check']['g_same'] is True and len(FR['prefreeze']['g']['g_sha256']) == 64, 'W04: 凍結の記録の g は G4 の確かめの g と同じ')
    prov = ld(P(PROV_REL))
    ftn = prov['frozen_text_note']
    ok(open(P(ftn['path']), encoding='utf-8').read().count(ftn['quote']) == 1 and '手元で引き Colab で照らす' in ftn['quote'], 'W04: 凍結の本文に引用の字が一度だけある')
    ok(all(w in prov['why'] for w in ('手元（Windows）', 'g_same', 'そろえても違った')), 'W04: 出所の記録の理由')
    ok('（A）' in prov['registrant_decision']['words'], 'W04: 登録者の決めは案 A')
    F['ft_path'], F['ft_quote'], F['dec_jst'] = ftn['path'], ftn['quote'], prov['registrant_decision']['jst']
    # W05
    fam = C['pilot']['decision']['family']
    ok('続け' in fam and 'nuclear の族は測れなかった' in fam, 'W05: 正本の族の決まりは続けるときの文')
    ok(pil['decision']['stop'] is True and FR['main_freeze']['decision'] is not None, 'W05: 下見は全体で止まった')
    # W06
    neg, ft = C['negation_templates'], NL.join(L)
    ok(neg[2] in ft and neg[0] not in ft and neg[3] not in ft, 'W06: 凍結の報告にある打ち消しの定型は三つ目だけ')
    # W12
    rt = es['request_text']
    ok('3. 族が survival のとき' in rt and '4. 族が nuclear のとき' in rt and rt.count('破局は') >= 2, 'W12: 正本の依頼の文の定義の三つ目と四つ目に族ごとの破局がある')
    # W15
    vr = C['inputs']['versions']['rule']
    ok('ドライバと CUDA の実行時の版' in vr and '止める条件にはしない' in vr, 'W15: 正本の版の決まり')

    def keys_of(o):
        return [k.lower() for k in o] + [k.lower() for k in (o.get('versions') or {})]
    recs = list(st.values()) + list(sess)
    ok(all(not any('driver' in k or 'cuda' in k for k in keys_of(o)) for o in recs), 'W15: 起動の記録と凍結の記録のセッションの欄に、ドライバと CUDA の実行時の版の欄が無い')
    ok(all(o.get('gpu') and o.get('versions') for o in recs), 'W15: 起動の記録と凍結の記録のセッションの欄に GPU の名と包みの版がある')
    # W16
    for ph in runs:
        row = [x for x in L if x.startswith('| %s | ' % ph)]
        ok(len(row) == 1 and row[0].rstrip(' |').endswith(' ' + st[ph]['commit']), 'W16: 走行の表の %s の行のコミットは起動の記録の中のコミット' % ph)
    ok(closed['session']['commit'] != st['behavior']['commit'], 'W16: 行動の下見の run のコミット（閉じた記録の session.commit）は起動の記録の中のコミットと違う')
    ps = [o for o in sess if o['start_end']['start'][0] == runs['pilot']['start']['file']]
    ok(len(ps) == 1 and ps[0]['commit'] != st['pilot']['commit'], 'W16: 読み取りの下見の run のコミット（凍結の記録の main_freeze.sessions）は起動の記録の中のコミットと違う')
    # W19
    ok('q2〜q4 は本の計算が終わり' in C['computation']['stops']['q_scoring'], 'W19: 正本の照合の決まり')
    for q in ('q2', 'q3', 'q4'):
        row = [x for x in L if x.startswith('| %s.' % q)]
        ok(len(row) == 1 and row[0].split(' | ')[1] == '採点しない', 'W19: 照合の表の %s は「採点しない」' % q)
    if final:                                                   # v1: 最終版（X01・X07・裁定 D285）
        tmpl = C['report_rules']['template']
        ok(any('登録者最終確認の前と後の二つの型' in x for x in tmpl), 'X07: 正本 report_rules.template は状態を登録者最終確認の前と後の二つの型と定める')
        ok(set(re.findall(r"\('(status_\w+)'", open(BR.__file__, encoding='utf-8').read())) == {'status_draft'}, 'X07: 凍結した組み立ての器の状態の型は草案の型だけ')
        ok(os.path.exists(P(ADOPT_FINAL_REL)) and os.path.exists(P(REPRO_FINAL_REL)), 'X01: 最終検分の採否の表と再現の記録が置き場にある')
        rp = ld(P(REPRO_FINAL_REL))
        ok(rp['n'] == rp['n_ok'], 'X01: 最終検分の票の事実の主張は、再現の記録ですべて合う')
        mt = ld(P('records/reviews/Bprime/results-final/votes/grok-4.7/meta.json'))
        ok(mt['model_requested'] == mt['model_returned'], 'X01: 最終検分の票の返った機種の名は呼んだ機種の名')
        ok('- **D285**（登録者' in open(P('records/Bprime/rulings-D285.md'), encoding='utf-8').read(), 'X01: 裁定 D285 の記録が置き場にある')
    return F, done


def blocks(C, FR, F, L, frozen16, rej_lines, final=False, conf=None, d2_16=None, reviewed=False):
    """錨の行の添字と、その行の後に置く区画の中身。final は最終版の頭の添えと検分票にする（v1）。"""
    neg = C['negation_templates']
    sec = lambda h: uniq([i for i, x in enumerate(L) if x.startswith(h)], h)
    s0, s1, s6, s9, s10, s_coi, s_ken = (sec('## 0. '), sec('## 1. '), sec('## 6. '), sec('## 9. '), sec('## 10. '), sec('## 作り手の関係'), sec('## 検分票'))
    nuc = [i for i, x in enumerate(L) if x == NUC]
    if len(nuc) != 2:
        raise SystemExit('nuclear の族の行が二つでない（止める・(五)）')
    fence = len(L) - 1
    while not L[fence]:
        fence -= 1
    if not (L[fence].startswith('本報告のいかなる数値も') and L[fence - 1] == '' and s_ken < fence - 2):
        raise SystemExit('柵の行の前の形が想定と違う（止める・(五)）')
    A = {'head': uniq([i for i, x in enumerate(L) if x.startswith('- 下見の前の凍結で、凍結の器が合成データの確かめの五')], '頭の下見の前の凍結の行'),
         'runs': table_last(L, uniq([i for i, x in enumerate(L) if x.startswith('| 段 | 組 | セッション |')], '走行の表')),
         'nuc0': uniq([i for i in nuc if s0 < i < s1], '§0 の nuclear の族の行'),
         'sec1_table': table_last(L, uniq([i for i, x in enumerate(L) if x.startswith('| 升目 | 無操作の対数オッズ |')], '§1 の表')),
         'nuc1': uniq([i for i in nuc if s1 < i < s6], '§1 の nuclear の族の行'),
         'sec6_ext': uniq([i for i, x in enumerate(L) if x.startswith('- 系統外の模型（') and s6 < i < s9], '§6 の一致の行'),
         'sec9_table': table_last(L, uniq([i for i, x in enumerate(L) if x.startswith('| 項目 | 結果 | 登録者 | コーディネータ |') and s9 < i < s10], '§9 の表')),
         'sec10_stale': uniq([i for i, x in enumerate(L) if STALE in x and s10 < i < s_coi], '§10 の限界の一文'),
         'ken': fence - 2}
    k = lambda n: KANJI[n] if 0 <= n <= 10 else str(n)
    B = {
        'head': ['- %sこの草案の二つ目は、凍結した組み立ての器 `tools/build_report_Bprime.py`（SHA16 %s）の本番の入口を同じ入力で一時の置き場へ走らせて凍結の報告を作り直し、'
                 '置き場の `records/Bprime/results-Bprime.md`（SHA16 %s）とバイトで同じことを確かめてから、見出しと状態の行を改め、%sの印を付けた区画だけを足したもの'
                 '（逸脱の器 `tools/build_report_Bprime_devBPT1.py` %s・登録者裁定 D284・採否の表 `%s` の W01〜W06・W12・W15・W16・W19）。区画は、生の md では始めと終わりの印の行で囲んだ。'
                 '印の無い文と区画は凍結した器の出力のまま。' % (TAG, s16(BR.__file__), frozen16, TAG, DRAFT_LABEL, ADOPT_REL),
                 '- %s起草者の欄（「この結果が退けた説明」）の%s行は、結果の巡の後に、凍結した器の口（`--rejected`）で直した（一行目と二行目に範囲の句を足し、一行目の「多くで」を決まりの数を指す'
                 '書き方に改め、三行目に (vi) の (a) の分岐の一文を足し、%s行目を足した・凍結した器の走査の当たり 0・登録者裁定 D284・採否の W11）。' % (TAG, k(rej_lines), k(rej_lines)),
                 '- %s下見の前の凍結を走らせた所: 等方の乱数 g は、凍結の本文（`%s`）の字「%s」と違い、Colab の CPU のランタイム（Linux）で引いた。手元（Windows）で引いた g の下の桁のビットが、'
                 'G4 の確かめで Colab が引いた g と違い（NumPy の版をそろえても違った）、凍結の器の照らし（g の SHA の一致）が通らなかったので、登録者の決め（案 A・%s 日本時間）で、'
                 '変えていない同じ凍結の器を Colab の CPU で走らせた。凍結の記録の g の SHA（`prefreeze.g.g_sha256`）は G4 の確かめの g と同じ（`checks.colab_check.g_same`）。'
                 '出所の記録は `%s`。引く場所だけが本文の字と違い、器と正本は変えていない（採否の W04）。' % (TAG, F['ft_path'], F['ft_quote'], F['dec_jst'], PROV_REL)],
        'runs': ['- %sこの表の「コミット」の欄は、起動の記録の中のコミット（起動の段が走った版）で、run が走った版ではない。run が走ったコミット（起動の記録を置いた後の版）は、'
                 '各走りのセッションの記録にあり、行動の下見は閉じた記録の `session.commit`、読み取りの下見は凍結の記録の本の凍結の節（`main_freeze.sessions`）にもある（採否の W16）。' % TAG,
                 '- %sドライバと CUDA の実行時の版: 正本 `inputs.versions.rule` は、セッションごとにドライバと CUDA の実行時の版を印字し、セッションの間の違いを報告の頭に並べると定めたが、'
                 '起動器はこの二つを記録していない（起動の記録と凍結の記録のセッションの欄にあるのは、GPU の名と包みの版）。正本のとおり止める条件ではなく、下見の決定はこの二つを使わない。'
                 '後の登録の器の直しの候補として記録に置く（採否の W15）。' % TAG],
        'nuc0': ['- %sすぐ上の一行は、nuclear の族の升目が二つとも外れても本の計算へ続けるときのための決まった文（正本 `pilot.decision.family`）。下見は全体で止まったので、どの族も測れていない'
                 '（採否の W05）。' % TAG],
        'sec1_table': ['- %s上の表の「選択肢 a の確率（集合の中）」と「質量」の列は丸めた表示で、下見の判定は記録の値（`%s` の `cells`）で行った。(i)(ii) を満たした %s は、'
                       '表示では天井（正本 `pilot.p_bounds`）と同じ字だが、記録の値は天井の内にある。天井の外の%sつの升目の確率は「1」と表示したが、記録の値はちょうど一ではない。'
                       '「質量」の列の「1」も、記録の値はちょうど一ではない。下の揺れの版の差も丸めた表示で、印は記録の値で付けた（採否の W03）。' % (TAG, PILOT_REL, F['eq_ceil'], k(F['n_out'])),
                       '- %s上の表の値のそばに、正本 `negation_templates` の一つ目と四つ目を一字違わず置く（採否の W06）:' % TAG,
                       '  - ' + neg[0],
                       '  - ' + neg[3]],
        'nuc1': ['- %sすぐ上の一行も、§0 の同じ行と同じく続けるときのための決まった文で、どの族も測れていない（採否の W05）。' % TAG],
        'sec6_ext': ['- %sすぐ上の一致は、一致の記述で、採点器の妥当性の測定ではない（正本 `behavior_pilot.external_scoring.rule`・行動の下見の閉じた記録の md）。'
                     '採点した系統外の模型は、結果の巡の系統外の票と同じ模型で、見逃しが相関しうる（§10 の限界の文・採否の W02）。' % TAG,
                     '- %s表の「破局」は架空の場面の採点の名で、族ごとの定義は正本 `behavior_pilot.external_scoring.request_text` の定義の三つ目（survival）と四つ目（nuclear）にある（採否の W12）。' % TAG,
                     '- %s上の率のそばに、正本 `negation_templates` の一つ目を一字違わず置く（採否の W06）:' % TAG,
                     '  - ' + neg[0]],
        'sec9_table': ['- %sq2〜q4 の「採点しない」は、本の計算に届かなかった（下見で止めた）ので、当たりにも外れにも数えないこと（未到達）を表す（正本 `computation.stops.q_scoring`・採否の W19）。' % TAG],
        'sec10_stale': ['- %sすぐ上の行の終わりの一文（「%s」）は、封印の時点の情報状態を写した正本の限界の文で、この報告の時点には当たらない。封印の後、行動の下見の場面の出力は凍結した採点の器が採点し、'
                        '升目を伏せた %d 件を系統外の模型が採点のために読んだ。升目ごとの率を含む閉じた記録は、閉じる段の器を走らせたコーディネータが読み、決まりのとおり読み取りの下見の前に'
                        '公開の置き場に置いた（正本 `behavior_pilot.order`・読み取りの下見の起動の記録はその SHA を照らした）。読み取りの下見の値は、機械の決定の後にコーディネータが読み、'
                        '公開の置き場に置いた（採否の W01）。' % (TAG, STALE, F['n_ext'])],
        'ken': ['- %s上の検分票は、凍結した組み立ての器が結果の巡の前に出したもので、凍結の出力のまま残す。読みの型の当否と起草者の欄の文は、結果の巡で見た（採否の表 `%s`・登録者裁定 D284）。' % (TAG, ADOPT_REL),
                '- %sこの草案の二つ目の検分票（足した区画について）:' % TAG,
                '  - 対象: 報告の草案の二つ目（凍結した器の出力と、足した区画）。',
                '  - 段階: 結果の後・結果の巡の後（採否の表・登録者裁定 D284）。注の文は裁定の後に起草した。',
                '  - 凍結物の同定: 凍結の本文 SHA16 %s・正本 SHA16 %s（凍結の記録の値）。凍結した組み立ての器は、下見の前の凍結から動かせない器の錠を照らしてから組んだ。'
                % (FR['frozen_sha16']['design/design-Bprime-FROZEN.md'], FR['frozen_sha16']['design/contrasts-Bprime.json']),
                '  - 盲検の状態: 該当しない（下見の値は機械の決定の後に公開した）。',
                '  - 敵対的検分: 注が言う事実は、器が記録と正本で照らした（確かめの記録の `facts`）。足した文は、凍結した器の自由の文の走査に掛けた（当たり 0）。',
                '  - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外一票（出所で数えた・D266 の型）と系統内一票。最終の系統外の一票はこの後（新しい呼び出し）。',
                '  - COI記録: 起草者は器と報告と起草者の欄と注を書いた当人で、封印した予想の q1 が当たった当人でもあり、「正しく書けていた」と読む側に引かれる。逆に、注を増やしすぎる側にも引かれる。'
                '足した区画は裁定 D284 の注の行に限り、読みを足さない。',
                '  - 本検分が確認していないこと: 最終の系統外の一票が見つけること。足した区画の文の言い過ぎ（走査は禁止の語と数の形だけを見る）。公開の置き場での表示（公開の後に確かめる）。'],
    }
    if final:                                                   # v1: 最終版の頭の添えと検分票（X01・X07・裁定 D285）
        B['head'][0] = ('- %sこの最終版は、凍結した組み立ての器 `tools/build_report_Bprime.py`（SHA16 %s）の本番の入口を同じ入力で一時の置き場へ走らせて凍結の報告を作り直し、'
                        '置き場の `records/Bprime/results-Bprime.md`（SHA16 %s）とバイトで同じことを確かめてから、見出しと状態の行を改め、%sの印を付けた区画だけを足したもの'
                        '（逸脱の器 `tools/build_report_Bprime_devBPT1.py` %s・登録者裁定 D284・D285・採否の表 `%s` の W01〜W06・W12・W15・W16・W19 と `%s` の X01・X07）。'
                        '区画は、生の md では始めと終わりの印の行で囲んだ。印の無い文と区画は凍結した器の出力のまま。' % (TAG, s16(BR.__file__), frozen16, TAG, VERSION, ADOPT_REL, ADOPT_FINAL_REL))
        B['head'].insert(1, '- %s最終の系統外の検分の後に、草案の二つ目（`%s`・SHA16 %s・書き換えていない）から、見出し・状態の行・この頭の添えの一行目とこの一行・検分票の区画だけを改めた'
                            '（器が確かめた・登録者裁定 D285）。状態の行は、正本 `report_rules.template` の二つの型（登録者最終確認の前と後）で、この器が組む（凍結した組み立ての器は草案の型しか'
                            '持たない・採否の X07・後の登録の器の直しの候補）。' % (TAG, OUT_REL, d2_16))
        B['ken'] = ['- %s上の検分票は、凍結した組み立ての器が結果の巡の前に出したもので、凍結の出力のまま残す。読みの型の当否と起草者の欄の文は、結果の巡と最終の系統外の検分で見た'
                    '（採否の表 `%s` と `%s`・登録者裁定 D284・D285）。' % (TAG, ADOPT_REL, ADOPT_FINAL_REL),
                    '- %sこの最終版の検分票:' % TAG,
                    '  - 対象: 報告の最終版（凍結した器の出力と、足した区画）。',
                    '  - 段階: 結果の後。結果の巡の後（登録者裁定 D284）と、最終の系統外の検分の後（登録者裁定 D285）%s%s。' % (
                        ('と、起草者の最終の見直しの後（`%s`）' % REVIEW_REL) if reviewed else '', 'と、登録者最終確認の後（状態の行）' if conf else ''),
                    '  - 凍結物の同定: 凍結の本文 SHA16 %s・正本 SHA16 %s（凍結の記録の値）。凍結した組み立ての器は、下見の前の凍結から動かせない器の錠を照らしてから組んだ。'
                    % (FR['frozen_sha16']['design/design-Bprime-FROZEN.md'], FR['frozen_sha16']['design/contrasts-Bprime.json']),
                    '  - 盲検の状態: 該当しない（下見の値は機械の決定の後に公開した）。',
                    '  - 敵対的検分: 注が言う事実は、器が記録と正本で照らした（確かめの記録の `facts`）。足した文は、凍結した器の自由の文の走査に掛けた（当たり 0）。'
                    '最終の系統外の検分の票の事実の主張は、一次の記録で照らした（`%s`）。' % REPRO_FINAL_REL,
                    '  - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外一票と系統内一票（系統は呼び出しの出所で数えた・D266 の型）。最終の系統外の検分は系統外一票（新しい呼び出し）で、結果の巡の系統外の票と'
                    '行動の下見の採点と同じ機種なので、見逃しが相関しうる。起草者の最終の見直しは起草者自身のもので、外の目ではない。',
                    '  - COI記録: 起草者は器と報告と起草者の欄と注を書いた当人で、封印した予想の q1 が当たった当人でもあり、「正しく書けていた」と読む側に引かれる。'
                    '最終版で改めた行は、裁定 D285 で決めた行（見出し・状態の行・頭の添えの一行目と足した一行・検分票）に限った。',
                    '  - 本検分が確認していないこと: 最終版で改めた行は、もう一度の検分を経ていない（正本 `review_plan.no_more`）。足した区画の文の言い過ぎ（走査は禁止の語と数の形だけを見る）。'
                    '公開の置き場での表示（公開の後に確かめる）。']
    return A, B


def is_new_status(x):
    return x in (S_DRAFT, S_FINAL_PRE) or x.startswith('- 状態: **最終版**（登録者最終確認 ')


def strip_back(Lt):
    """印の行で囲んだ区画（前の空の行を含む）を除き、見出しと状態の行を戻す。"""
    out, i, n = [], 0, 0
    while i < len(Lt):
        if i + 1 < len(Lt) and Lt[i] == '' and Lt[i + 1] == BEGIN:
            i, n = Lt.index(END, i + 2) + 1, n + 1
            continue
        if Lt[i] in (BEGIN, END):
            raise SystemExit('印の行の形が想定と違う（止める・(二)）')
        out.append(Lt[i])
        i += 1
    if out[0] in (T_DRAFT, T_FINAL):
        out[0] = T_FROZEN
    return [S_FROZEN if is_new_status(x) else x for x in out], n


def assemble(L, A, B, title, status):
    Lt = list(L)
    for name in sorted(A, key=lambda n: A[n], reverse=True):
        Lt[A[name] + 1:A[name] + 1] = ['', BEGIN] + B[name] + [END]
    Lt[0] = title
    Lt[Lt.index(S_FROZEN)] = status
    return Lt


def load_conf():
    """登録者最終確認の記録（あれば）: 鍵 when_jst・uuid・words を照らす。"""
    if not os.path.exists(P(CONF_REL)):
        return None
    cf = ld(P(CONF_REL))
    w = cf['words']
    tg, sr = 'pasted' + '_content', 'system' + '-reminder'
    if NL in w or any(b in w for b in ('<' + tg, '<' + sr, sr + '>', 'AppData', 'Users', '「', '」')) or not w.startswith('南無汝我曼荼羅'):
        raise SystemExit('確認の記録の言葉の形が想定と違う（止める）')
    if not (re.match(r'^\d{4}-\d\d-\d\d \d\d:\d\d$', cf['when_jst']) and re.match(r'^[0-9a-f\-]{36}$', cf['uuid'])):
        raise SystemExit('確認の記録の時刻か uuid の形が想定と違う（止める）')
    return cf


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--final', action='store_true')
    a = ap.parse_args()
    C, FR = ld(P(CANON_REL)), ld(P(FR_REL))
    if [d.get('no') for d in FR.get('deviations') or []] != [DEV]:
        raise SystemExit('凍結の記録の台帳が D-BPT1 だけでない（止める）')
    td = tempfile.mkdtemp(prefix='devBPT1-')
    tmp = os.path.join(td, 'results-Bprime.md')
    hits = BR.main_build(force=True, rejected_path=P(REJ_REL), out=tmp)
    if hits:
        raise SystemExit('凍結した器の走査の当たり（止める・(一)）: %s' % hits[:5])
    fb = open(tmp, 'rb').read()
    if fb != open(BR.OUT, 'rb').read():
        raise SystemExit('凍結した器で作り直した報告が、置き場の報告とバイトで違う（止める・(一)）')
    frozen16 = s16b(fb)
    L = fb.decode('utf-8').split(NL)
    if L[0] != T_FROZEN or L.count(S_FROZEN) != 1:
        raise SystemExit('凍結の報告の見出しか状態の行が想定と違う（止める）')
    rej_lines = len([x for x in open(P(REJ_REL), encoding='utf-8').read().split(NL) if x.strip()])
    F, done = facts(C, FR, L, final=a.final)
    A, B_d = blocks(C, FR, F, L, frozen16, rej_lines)
    if sorted(A) != sorted(B_d) or len(set(A.values())) != len(A):
        raise SystemExit('錨と区画の対が想定と違う（止める・(五)）')
    Lt_d = assemble(L, A, B_d, T_DRAFT, S_DRAFT)
    conf, cmp = None, None
    if a.final:                                                 # v1: 最終版
        d2b = open(P(OUT_REL), 'rb').read()
        d2_16 = s16b(d2b)
        if d2_16 != ld(P(CHECKS_REL))['sha16'][OUT_REL] or NL.join(Lt_d).encode('utf-8') != d2b:
            raise SystemExit('置き場の草案の二つ目が、確かめの記録の SHA か、この器が草案の型で組んだ文と違う（止める）')
        conf = load_conf()
        reviewed = os.path.exists(P(REVIEW_REL))
        if reviewed and not all(w in open(P(REVIEW_REL), encoding='utf-8').read() for w in ('## 検分票', '本検分が確認していないこと')):
            raise SystemExit('起草者の最終の見直しの記録の形が想定と違う（止める）')
        _, B = blocks(C, FR, F, L, frozen16, rej_lines, final=True, conf=conf, d2_16=d2_16, reviewed=reviewed)
        status = (S_CONF % (conf['when_jst'], conf['uuid'], conf['words'])) if conf else S_FINAL_PRE
        Lt = assemble(L, A, B, T_FINAL, status)
        gone, came = [], []
        d2 = d2b.decode('utf-8').split(NL)
        for tg_, i1, i2, j1, j2 in difflib.SequenceMatcher(None, d2, Lt, autojunk=False).get_opcodes():
            if tg_ in ('replace', 'delete'):
                gone += d2[i1:i2]
            if tg_ in ('replace', 'insert'):
                came += Lt[j1:j2]
        ok_gone = {T_DRAFT, S_DRAFT, B_d['head'][0]} | set(B_d['ken'])
        ok_came = {T_FINAL, status, B['head'][0], B['head'][1]} | set(B['ken'])
        bad_g, bad_c = [x for x in gone if x not in ok_gone], [x for x in came if x not in ok_came]
        if bad_g or bad_c:
            raise SystemExit('草案の二つ目から、決めていない行が変わった（止める）: 消えた %s・足された %s' % ([x[:40] for x in bad_g], [x[:40] for x in bad_c]))
        cmp = {'draft2': OUT_REL, 'draft2_sha16': d2_16, 'draft2_rebuilt_identical': True, 'removed_lines': len(gone), 'added_lines': len(came),
               'allowed': '見出し・状態の行・頭の添えの一行目と足した一行・検分票の区画（裁定 D285）'}
    else:
        B, Lt = B_d, Lt_d
    text = NL.join(Lt)
    back, n_blocks = strip_back(Lt)
    if NL.join(back).encode('utf-8') != fb or n_blocks != len(B):
        raise SystemExit('区画を除いても凍結の報告に戻らない（止める・(二)）: 区画 %d・数えた %d' % (len(B), n_blocks))
    neg = C['negation_templates']
    bans, nums = BR.bans_of(C), BR.number_leaves(C)
    added = [x for blk in B.values() for x in blk]
    scan_hits = []
    for x in added:
        t = x
        for s in (neg[0], neg[3]):
            t = t.replace(s, '')
        scan_hits += [{'kind': kd, 'token': tok, 'line': x[:40]} for kd, tok in BR.P.free_text_hits(t, bans, nums, BR.MASKS)]
    if scan_hits:
        raise SystemExit('足した文の走査の当たり（止める・(三)）: %s' % scan_hits[:8])
    if not (('  - ' + neg[0]) in Lt and ('  - ' + neg[3]) in Lt):
        raise SystemExit('打ち消しの定型の写しが正本の文と違う（止める・(四)）')
    body = text.encode('utf-8')
    out_rel, chk_rel = (OUT_FINAL_REL, CHECKS_FINAL_REL) if a.final else (OUT_REL, CHECKS_REL)
    out = P(out_rel)
    if os.path.exists(out) and not a.force:
        if open(out, 'rb').read() == body:
            print('[build_report_Bprime_devBPT1] 置き場の%sと同じ（書かない）: %s' % ('最終版' if a.final else '草案の二つ目', out_rel))
            return
        raise SystemExit('置き場の%sと、組んだ文が違う（止める・--force で書き直す）: %s' % ('最終版' if a.final else '草案の二つ目', out_rel))
    open(out, 'wb').write(body)
    ck = {'kind': 'bprime_report_final_checks' if a.final else 'bprime_report_draft2_checks', 'tool': 'tools/build_report_Bprime_devBPT1.py %s' % (VERSION if a.final else DRAFT_LABEL),
          'deviation': DEV, 'ruling': 'D284・D285' if a.final else 'D284', 'adoption_table': [ADOPT_REL, ADOPT_FINAL_REL] if a.final else ADOPT_REL,
          'sha16': {'tools/build_report_Bprime.py': s16(BR.__file__), 'tools/build_report_Bprime_devBPT1.py': s16(os.path.abspath(__file__)), 'records/Bprime/results-Bprime.md': frozen16,
                    REJ_REL: s16(P(REJ_REL)), FR_REL: s16(P(FR_REL)), CANON_REL: s16(P(CANON_REL)), PILOT_REL: s16(P(PILOT_REL)), CLOSED_REL: s16(P(CLOSED_REL)), PROV_REL: s16(P(PROV_REL)),
                    out_rel: s16b(body)},
          'checks': {'frozen_rebuild_identical': True, 'frozen_scan_hits': 0, 'strip_back_identical': True, 'blocks': n_blocks, 'added_lines': len(added), 'added_scan_hits': 0,
                     'negation_templates_verbatim': True, 'facts': done},
          'anchors_frozen_line': {n: A[n] + 1 for n in sorted(A, key=lambda n: A[n])},
          'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    if a.final:
        ck['draft2_compare'] = cmp
        ck['status'] = 'confirmed' if conf else 'before_confirmation'
        if conf:
            ck['sha16'][CONF_REL] = s16(P(CONF_REL))
        for r_ in (ADOPT_FINAL_REL, REPRO_FINAL_REL, 'records/Bprime/rulings-D285.md') + ((REVIEW_REL,) if os.path.exists(P(REVIEW_REL)) else ()):
            ck['sha16'][r_] = s16(P(r_))
        ck['drafter_final_review'] = REVIEW_REL if os.path.exists(P(REVIEW_REL)) else None
    with open(P(chk_rel), 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(ck, fh, ensure_ascii=False, indent=1)
    print('[build_report_Bprime_devBPT1] 書いた %s（SHA16 %s・区画 %d・足した行 %d・事実の照らし %d・走査の当たり 0%s）' % (
        out_rel, s16b(body), n_blocks, len(added), len(done), ('・草案の二つ目から消えた行 %d・足された行 %d・状態 %s' % (cmp['removed_lines'], cmp['added_lines'], ck['status'])) if a.final else ''))


if __name__ == '__main__':
    main()
