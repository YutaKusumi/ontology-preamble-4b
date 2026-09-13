# -*- coding: utf-8 -*-
"""report_lint.py v1 —— 段階 A の結果報告の走査器（正本 report_rules.lint・report_rules.typed_numbers・print_strings の語の禁止・2026-09-13・登録者裁定 D9 の三つ目の手順）。
走査:
 (1) 価値語・機序語（print_strings.value_word_ban・mechanism_word_ban）の出現（機械の区画の中も含む・機械の定型文にも許さない）。
 (2) 未登録の数: 機械の区画（report_rules.machine_block の begin 〜 end・無ければ既定の <!-- 機械:始 --> 〜 <!-- 機械:終 -->）の外の行で、
     構造として除外する型（tools/numbers_lint.py の MASKS・節番号・日付・版・機種名・SHA など）に当たらない数。凍結した報告雛形（report_rules.template）の行と逐語で同じ行は、
     雛形の束縛で入った数として許す（起草者が打ち込んだ数ではない）。打ち込んでよい型（report_rules.typed_numbers）のうち、日付・SHA16・SHA-256・逸脱番号・雛形の SHA16 は MASKS で除き、
     費用の実績（登録者申告）は行頭に費用の行の印（machine_block.cost_line_tag・既定「〔打ち込み・費用の実績〕」）を置いた行だけ許す。
 (3) 埋め残し: 雛形の記入欄（〔〕で囲んだ欄）の残り（費用の行の印は除く）。
 (4) 両方向不定の条項の有無。
出力: 違反の一覧（md）。違反があれば非零で終わる（報告の組み立てを止める）。本器は語と数の形・記入欄・条項を見るだけで、報告の読みの当否と機械の区画の中身の正しさは検査しない。
用法: python tools/report_lint.py <報告の md> [--out <path>] [--template <雛形の md>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import numbers_lint as NL
REPO = runs_A.REPO
VERSION = 'v1'
BLANK = re.compile(r'〔[^〕]*〕')
DEFAULT_MB = {'begin': '<!-- 機械:始 -->', 'end': '<!-- 機械:終 -->', 'cost_line_tag': '〔打ち込み・費用の実績〕'}


def machine_block(T):
    return dict(DEFAULT_MB, **(T['report_rules'].get('machine_block') or {}))


def lint(text, T, template_lines=frozenset()):
    MB = machine_block(T); PS = T['print_strings']; bans = [('価値語', w) for w in PS['value_word_ban']] + [('機序語', w) for w in PS['mechanism_word_ban']]
    viol = []; in_m = False
    for i, l in enumerate(text.replace('\r\n', '\n').split('\n'), 1):
        if MB['begin'] in l:
            in_m = True; continue
        if MB['end'] in l:
            in_m = False; continue
        for kind, w in bans:
            if w in l:
                viol.append({'kind': kind, 'line': i, 'token': w, 'context': l[:160]})
        if not in_m and not l.startswith(MB['cost_line_tag']) and l not in template_lines:
            for tok, v, s0, s1 in NL.numbers(l):
                viol.append({'kind': '未登録の数', 'line': i, 'token': tok, 'context': l[max(0, s0 - 30):s1 + 30]})
        for m in BLANK.finditer(l):
            if m.group(0) != MB['cost_line_tag']:
                viol.append({'kind': '埋め残し', 'line': i, 'token': m.group(0)[:40], 'context': l[:160]})
    if in_m:
        viol.append({'kind': '機械の区画が閉じていない', 'line': 0, 'token': '', 'context': ''})
    if '両方向不定' not in text:
        viol.append({'kind': '両方向不定の条項なし', 'line': 0, 'token': '', 'context': ''})
    return viol


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('report'); ap.add_argument('--out', default=None); ap.add_argument('--contrasts', default=None); ap.add_argument('--template', default=None)
    a = ap.parse_args()
    T = runs_A.load_T(a.contrasts); text = open(a.report, encoding='utf-8').read()
    tp = a.template or os.path.join(REPO, T['report_rules']['template'])
    TL = frozenset(open(tp, encoding='utf-8').read().replace('\r\n', '\n').split('\n')) if os.path.exists(tp) else frozenset()
    V = lint(text, T, TL)
    out = a.out or os.path.join(REPO, 'records', 'A', 'report-lint-%s.md' % os.path.splitext(os.path.basename(a.report))[0])
    kinds = {}
    for v in V:
        kinds[v['kind']] = kinds.get(v['kind'], 0) + 1
    M = ['# 報告の走査（機械生成・`tools/report_lint.py` %s・%s UTC）' % (VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')), '',
         '- 対象: `%s`（SHA16 %s）・雛形 %s（SHA16 %s）・正本 SHA16 %s' % (os.path.basename(a.report), runs_A.sha16_file(a.report), os.path.basename(tp), runs_A.sha16_file(tp) if os.path.exists(tp) else '無し', runs_A.sha16_file(a.contrasts or runs_A.CPATH)),
         '- 違反の合計: %d（%s）' % (len(V), json.dumps(kinds, ensure_ascii=False)),
         '- 限界: 本器は語と数の形・記入欄の埋め残し・条項の有無を見るだけで、報告の読みの当否・機械の区画の中身の正しさは検査しない。雛形と逐語で同じ行の数は検査しない。', '']
    M += ['| 種類 | 行 | 語・数 | 文脈 |', '|---|---|---|---|'] + ['| %s | %d | %s | %s |' % (v['kind'], v['line'], v['token'], v['context'].replace('|', '／')) for v in V]
    M += ['', '本ファイルのいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
    print('[report_lint] 違反 %d %s → %s' % (len(V), json.dumps(kinds, ensure_ascii=False), out))
    sys.exit(1 if V else 0)
