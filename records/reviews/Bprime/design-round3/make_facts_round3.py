# -*- coding: utf-8 -*-
"""make_facts_round3.py v0（2026-09-29・B′ の設計の巡・三巡目〔最終の検分〕の採否のため・票の主張の前提を一次の資料から機械で抜き出す・コーディネータ南無弥勒如来）。
枠（`00-frame-design-round3.md`）の「票の主張の前提は、コーディネータが一次の資料で確かめ、出所を採否の表に書く」による。
出力 `facts-round3.md` は一度だけ書く。値と文は出所から読み、手で打たない。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'kit')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b/'
NL = chr(10)
FENCE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
CARRIED = ['下見で止めた', '下見で一部を外した', '揺れの版の値', '区別できない', '外でない行', '埋もれる', '両方の外', '二つ目の札だけ']


def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]


def draft_table(draft):
    rows = {}
    on = False
    for l in draft.split(NL):
        if l.startswith('### 9.1'):
            on = True
            continue
        if on and l.startswith('### '):
            break
        if on and l.startswith('| ') and not l.startswith('| 型 ') and not l.startswith('|---'):
            cells = [c.strip() for c in l.strip().strip('|').split(' | ')]
            assert len(cells) == 4, ('欄の数が 4 でない', cells[0])
            rows[cells[0]] = cells
    return rows


def main():
    out_path = os.path.join(HERE, 'facts-round3.md')
    assert not os.path.exists(out_path), '既にある（一度だけ）'
    pd = os.path.join(KIT, 'design-Bprime-draft6.md')
    draft = open(pd, encoding='utf-8').read()
    pL = os.path.join(KIT, 'reference', 'contrasts-Bl3.json')
    L3 = json.load(open(pL, encoding='utf-8'))
    out = ['# 三巡目の採否で確かめた事実（機械で抜き出した・B′ の設計の巡・三巡目〔最終の検分〕・2026-09-29・コーディネータ南無弥勒如来・非公開）', '',
           '- 何か: 三巡目の四票（grok-4.7・claude-ai-7〜9）の主張の前提を、出所のファイルから器 `make_facts_round3.py` が抜き出したもの。値と文は出所から読み、手で打っていない。',
           '- 出所: 草案6 `kit/design-Bprime-draft6.md`（SHA16 %s）・層三の正本 `kit/reference/contrasts-Bl3.json`（SHA16 %s）・ほかは節ごとに書く。' % (sha16(pd), sha16(pL)), '']

    # 1. 読みの表の持ち越し
    rr = {r['type']: r for r in L3['reading_rules']}
    t6 = draft_table(draft)
    out += ['## 1. 読みの表の持ち越し（層三の `reading_rules` と草案6 §9.1 の表・持ち越した八つの型）', '',
            '- 「落ちた書かない語」は、層三の `never` の語が、草案6 の同じ型の「書かない」の欄に一字違わない語として無いもの（部分の字としてはあることもある・その印を添える）。', '']
    for t in CARRIED:
        a = rr[t]
        b = t6[t]
        never6 = [x.strip() for x in b[3].split('・')]
        missing = [w for w in a['never'] if w not in never6]
        added = [w for w in never6 if w not in a['never']]
        out += ['### %s' % t, '',
                '- 層三の書く文: 「%s」' % a['write'],
                '- 草案6 の書く文: %s' % b[2],
                '- 層三の書かない語: %s' % '・'.join('「%s」' % w for w in a['never']),
                '- 草案6 の書かない欄: %s' % b[3],
                '- 落ちた書かない語: %s' % ('・'.join('「%s」%s' % (w, '（草案6 の欄の中に部分の字としてはある）' if w in b[3] else '') for w in missing) if missing else 'なし'),
                '- 草案6 で足した書かない語: %s' % ('・'.join('「%s」' % w for w in added) if added else 'なし'), '']
    # 2. 禁止語の一覧
    ps = L3['print_strings']
    m = re.search(r'次の語と句は、どこでも一律に使わない（限定つきで許す言い方は置かない）: (.*?)。これらを正本の', draft)
    ban6 = [x.strip() for x in m.group(1).split('・')] if m else []
    table_never = '・'.join(r[3] for r in t6.values())
    out += ['## 2. 禁止語の一覧（層三の `print_strings` と草案6 §9.4）', '',
            '- 草案6 §9.4 の一律の禁止の一覧（%d 語と句）: %s' % (len(ban6), '・'.join('「%s」' % w for w in ban6)), '']
    for k in ('value_word_ban', 'mechanism_word_ban', 'added_ban', 'reading_never_ban'):
        lst = ps[k]
        not_in = [w for w in lst if w not in ban6 and w not in table_never]
        out += ['- 層三の `print_strings.%s`（%d）: %s' % (k, len(lst), '・'.join('「%s」' % w for w in lst)),
                '  - 草案6 §9.4 の一覧にも §9.1 の「書かない」の欄にも（部分の字としても）無いもの: %s' % ('・'.join('「%s」' % w for w in not_in) if not_in else 'なし')]
    neg = L3['negation_templates']
    out += ['', '- 層三の `negation_templates`（%d）と草案6 の中の有無:' % len(neg)]
    for s in neg:
        out.append('  - 「%s」: %s' % (s, 'ある' if s in draft else '無い'))
    out += ['- 草案6 §9.4 の一覧に「個性」があるか: %s／柵の文（草案6 の最後の行）に「個性」があるか: %s' % ('個性' in ban6, '個性' in draft.strip().split(NL)[-1]),
            '- 草案6 §8 の文「どの層も「転換層」と呼ばない。」があるか: %s／§9.4 の一覧に「転換層」があるか: %s' % ('どの層も「転換層」と呼ばない。' in draft, '転換層' in ban6), '']

    # 3. 層三の正本のほかの鍵
    def g(path):
        v = L3
        for p in path.split('.'):
            v = v[int(p)] if isinstance(v, list) else v[p]
        return v
    keys = ['computation.logit_tol', 'computation.self_checks.logit', 'independent_recompute.stages.second.tol', 'independent_recompute.print',
            'nulls.isotropic.low_bar', 'labels.p_rule_why', 'labels.side_rule', 'report_rules.template.3', 'pilot.decision.report',
            'pilot.checks.iii.rule', 'pilot.decision.tool_error.rerun', 'computation.tool_error']
    out += ['## 3. 層三の正本のほかの鍵（逐語）', '']
    for k in keys:
        out.append('- `%s`: 「%s」' % (k, g(k)))
    order = L3['review_plan']['order']
    out += ['- `review_plan.order` のうち「計算」で始まる段: %s' % '／'.join('「%s」' % x for x in order if x.startswith('計算')), '']

    # 4. 段階 B の正本
    pB = PUB + 'design/contrasts-B.json'
    B = json.load(open(pB, encoding='utf-8'))
    out += ['## 4. 段階 B の正本（公開の置き場 `design/contrasts-B.json`・SHA16 %s）の鍵（逐語）' % sha16(pB), '',
            '- `denominators.n_ok`: 「%s」' % B['denominators']['n_ok'],
            '- `dilution_gate.why`: 「%s」' % B['dilution_gate']['why'],
            '- `interval.method`: 「%s」' % B['interval']['method'], '']

    # 5. 場面の本文
    pS = os.path.join(KIT, 'scenarios', 'app-scenarios.json')
    S = json.load(open(pS, encoding='utf-8'))
    sc = {x['question_id']: x['text'] for x in S['scenarios']}
    out += ['## 5. 場面の本文の頭（`kit/scenarios/app-scenarios.json`・SHA16 %s）' % sha16(pS), '']
    for q in ('S1', 'S4', 'N1'):
        out.append('- %s（%d 字）の最初の文: 「%s」' % (q, len(sc[q]), sc[q].split('。')[0] + '。'))
    out += ['- S4 の本文は S1 の本文を含むか: %s／S4 の本文から最初の文を除いたものは S1 の本文と同じか: %s' % (sc['S1'] in sc['S4'], sc['S4'].split('。', 1)[1] == sc['S1']), '']

    # 6. 用語の手引き
    pG = os.path.join(KIT, 'glossary-bprime.md')
    G = open(pG, encoding='utf-8').read().split(NL)
    out += ['## 6. 用語の手引き（`kit/glossary-bprime.md`・三版・SHA16 %s）の行（逐語）' % sha16(pG), '']
    for i, l in enumerate(G, 1):
        if l.startswith('- **softcap を見分ける自己検査**') or l.startswith('- **書き出しの根の件数**') or l.startswith('- **約束の値**'):
            out.append('- %d 行目: 「%s」' % (i, l))
    out.append('')

    # 7. 草案6 の文
    out += ['## 7. 草案6 の文（有無）', '']
    for s in ['閾値は層三の登録の値を写したもので、Gemma で較正していない', '進まないと決めたときは逸脱として理由とともに記し、そこまでの記録をすべて公開の置き場に置く。',
              '封印の後は、機械の止め（器の誤り・下見の止め・GPU の期限）のほかでは止めない。', 'q1 はいつも採点する（器の誤りで閉じたときは上の型）。',
              'そういう行が一つも無いときは〈この位置では見分ける力が無い〉と印字し、器の誤りに数えずに登録者に上げる。',
              '除いた数を表の注に書く', '場面は違うが場面の文は共通なので', '結果は登録者と一緒に開く', '一緒に開く']:
        n = draft.count(s)
        lines = [str(i) for i, l in enumerate(draft.split(NL), 1) if s in l]
        out.append('- 「%s」: %d 回（%s 行目）' % (s, n, '・'.join(lines) if lines else '—'))
    last = draft.strip().split(NL)[-1]
    out += ['- §16 の「この後」の行に「独立の再計算」の字があるか: %s' % ('独立の再計算' in [l for l in draft.split(NL) if l.startswith('- この後:')][0]), '']

    # 8. 二巡目の採否の表の行（逐語の句の有無）
    pA = os.path.join(KIT, 'round2', 'adoption-design-round2.md')
    A = open(pA, encoding='utf-8').read()
    out += ['## 8. 二巡目の採否の表（`kit/round2/adoption-design-round2.md`・SHA16 %s）の句の有無' % sha16(pA), '']
    for s in ['割る相手が零の対も除き、その数を印字する', '四つを一字まで先に置き', '件数に依らず報告の頭に置く', '主語の無い「区別できた」は走査で止める',
              '進まないと決めたときは逸脱として理由とともに記し', 'q1 はいつも', '器の誤りに数えない（登録者に上げる）', '揺れの床の 2 倍と下限 0.005 の大きい方']:
        lines = [l.split(' | ')[0].strip('| ') for l in A.split(NL) if s in l]
        out.append('- 「%s」: %s' % (s, '・'.join(lines) if lines else '無い'))
    out += ['', '## この記録が確認していないこと', '',
            '- 読みの表の「書く」の文の違いは両方の文を並べただけで、どの句が落ちたかの判定は採否の表で人が読む（書き直しの語順の違いがあるため）。',
            '- 公開の置き場の写しが GitHub の上の版と同じか（手元の写しの版 0a45688 の後に push は無い）。', '', FENCE, '']
    open(out_path, 'w', encoding='utf-8', newline=NL).write(NL.join(out))
    print('written facts-round3.md', len(out), 'lines | sha16', sha16(out_path))


if __name__ == '__main__':
    main()
