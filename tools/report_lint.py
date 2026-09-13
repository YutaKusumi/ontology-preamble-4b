# -*- coding: utf-8 -*-
"""report_lint.py v2 —— 段階 A の結果報告の走査器（正本 report_rules.lint・report_rules.typed_numbers・report_rules.machine_block・print_strings の語の禁止・2026-09-13・登録者裁定 D9 の三つ目の手順）。
走査:
 (1) 価値語・機序語（print_strings.value_word_ban・mechanism_word_ban）の出現（機械の区画の中も含む・機械の定型文にも許さない）。
 (2) 未登録の数: 機械の区画（report_rules.machine_block の begin 〜 end）の外の行で、構造として除外する型に当たらない数。凍結した報告雛形（report_rules.template）の行と逐語で同じ行は、
     雛形の束縛で入った数として許す（起草者が打ち込んだ数ではない）。打ち込んでよい型（report_rules.typed_numbers）のうち、日付・SHA16・SHA-256・逸脱番号・雛形の SHA16 は除外の型で除き、
     費用の実績（登録者申告）は行頭に費用の行の印（machine_block.cost_line_tag）を置いた行で、数を一つだけ許す（machine_block.cost_line_rule）。
 (3) 機械の区画の突合: 組み立て器（tools/build_report_A.py）が書いた記録（報告と同じ名の -machine.json）の区画ごとの中身の SHA16 と、報告の区画を順に突合する（machine_block.sidecar）。
     記録が無いのに区画があれば違反。区画の数と中身が記録と違えば違反（起草者が区画の印で囲んで数を通すことを止める）。
 (4) 埋め残し: 雛形の記入欄（〔〕で囲んだ欄）の残り（費用の行の印は除く）。
 (5) 両方向不定の条項の有無。
v2（2026-09-14・実装検分の採否表 P96）: 報告の走査では、本文の数の検査（tools/numbers_lint.py）の除外の型のうち code span・括弧の年・引用の年・章などの番号・判定の番号（D・P など）・#N・N GB・段 N を外す（REPORT_DROP）。
  機械の区画の突合（write_sidecar・block_hashes・sidecar_path）と、費用の行の数を一つに限る規則を置く。selftest で検分の探り入力（W42）がすべて違反になることを確かめる。
出力: 違反の一覧（md）。違反があれば非零で終わる（報告の組み立てを止める）。本器は語と数の形・記入欄・区画の突合・条項を見るだけで、報告の読みの当否と機械の区画の中身の正しさは検査しない。
用法: python tools/report_lint.py <報告の md> [--out <path>] [--template <雛形の md>] [--sidecar <-machine.json>]
      python tools/report_lint.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, hashlib, argparse, datetime, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import numbers_lint as NL
REPO = runs_A.REPO
VERSION = 'v2'
BLANK = re.compile(r'〔[^〕]*〕')
DEFAULT_MB = {'begin': '<!-- 機械:始 -->', 'end': '<!-- 機械:終 -->', 'cost_line_tag': '〔打ち込み・費用の実績〕'}
REPORT_DROP = {r'`[^`]*`', r'第[一二三四五六七八九十〇\d]+[章節巡票部段]', r'(?<![A-Za-z])[DCVEJKPW]\d+(?:〜[DCVEJKPW]?\d+)?(?![\d.])', r'\b\d+\s?GB\b', r'#\d+',
               r'\((?:19|20)\d{2}\)', r'(?:19|20)\d{2}(?=\s*Stat|\s*Biometrika)', r'段\s?\d'}
assert REPORT_DROP <= set(NL.MASKS), sorted(REPORT_DROP - set(NL.MASKS))
REPORT_MASK_RE = [re.compile(p, re.M) for p in NL.MASKS if p not in REPORT_DROP]
CODE = re.compile(r'(?<![A-Za-z0-9_])[A-Z]\d+(?:〜[A-Z]?\d+)?(?![0-9A-Za-z_.])')   # 英大文字に続く数（D99・P96 など・NUM は英字の直後の数を拾わない）


def machine_block(T):
    return dict(DEFAULT_MB, **(T['report_rules'].get('machine_block') or {}))


def report_numbers(line):
    """報告の走査の数（除外の型から REPORT_DROP を外した型で覆ってから数を拾う）。"""
    t = line
    for rx in REPORT_MASK_RE:
        t = rx.sub(lambda m: ' ' * len(m.group(0)), t)
    out = []
    for m in NL.NUM.finditer(t):
        tok = m.group(0); raw = tok.replace(',', '').replace('−', '-').rstrip('%')
        try:
            out.append((tok, float(raw), m.start(), m.end()))
        except ValueError:
            continue
    for m in CODE.finditer(t):
        out.append((m.group(0), None, m.start(), m.end()))
    return sorted(out, key=lambda x: x[2])


def blocks(text, T):
    """機械の区画の一覧（始まりの行番号・中身の文字列）。"""
    MB = machine_block(T); out = []; cur = None
    for i, l in enumerate(text.replace('\r\n', '\n').split('\n'), 1):
        if MB['begin'] in l:
            cur = (i, [])
            continue
        if MB['end'] in l and cur is not None:
            out.append((cur[0], '\n'.join(cur[1]))); cur = None
            continue
        if cur is not None:
            cur[1].append(l)
    return out


def block_hashes(text, T):
    return [hashlib.sha256(body.encode('utf-8')).hexdigest()[:16].upper() for _, body in blocks(text, T)]


def sidecar_path(report_path):
    return (report_path[:-3] if report_path.endswith('.md') else report_path) + '-machine.json'


def write_sidecar(report_path, text, T, builder):
    S = {'kind': 'report_machine_blocks_A', 'version': VERSION, 'builder': builder, 'report': os.path.basename(report_path), 'blocks': block_hashes(text, T),
         'rule': (T['report_rules'].get('machine_block') or {}).get('sidecar'), 'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    json.dump(S, open(sidecar_path(report_path), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    return S


def lint(text, T, template_lines=frozenset(), sidecar=None):
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
        if not in_m and l not in template_lines:
            nums = report_numbers(l[len(MB['cost_line_tag']):] if l.startswith(MB['cost_line_tag']) else l)
            if l.startswith(MB['cost_line_tag']):
                if len(nums) != 1:
                    viol.append({'kind': '費用の行の数が一つでない', 'line': i, 'token': '・'.join(t for t, _, _, _ in nums) or 'なし', 'context': l[:160]})
            else:
                for tok, v, s0, s1 in nums:
                    viol.append({'kind': '未登録の数', 'line': i, 'token': tok, 'context': l[max(0, s0 - 30):s1 + 30]})
        for m in BLANK.finditer(l):
            if m.group(0) != MB['cost_line_tag']:
                viol.append({'kind': '埋め残し', 'line': i, 'token': m.group(0)[:40], 'context': l[:160]})
    if in_m:
        viol.append({'kind': '機械の区画が閉じていない', 'line': 0, 'token': '', 'context': ''})
    bl = blocks(text, T); hs = block_hashes(text, T)
    if bl and sidecar is None:
        viol.append({'kind': '機械の区画の記録が無い', 'line': bl[0][0], 'token': '%d 区画' % len(bl), 'context': '組み立て器の -machine.json が要る'})
    elif sidecar is not None:
        want = list(sidecar.get('blocks') or [])
        if len(want) != len(hs):
            viol.append({'kind': '機械の区画の数が記録と違う', 'line': 0, 'token': '報告 %d・記録 %d' % (len(hs), len(want)), 'context': ''})
        for (ln, _), h, w in zip(bl, hs, want):
            if h != w:
                viol.append({'kind': '機械の区画の中身が記録と違う', 'line': ln, 'token': h, 'context': '記録 %s' % w})
    if '両方向不定' not in text:
        viol.append({'kind': '両方向不定の条項なし', 'line': 0, 'token': '', 'context': ''})
    return viol


def _selftest():
    T = runs_A.load_T(); MB = machine_block(T); lines = []
    good = ['# 報告', '', MB['begin'], '確証 3 本（機械の出力）', MB['end'], '雛形の行 12 本', '本報告は両方向不定。']
    text = '\n'.join(good) + '\n'; side = {'blocks': block_hashes(text, T)}
    V = lint(text, T, frozenset(['雛形の行 12 本']), sidecar=side); assert V == [], V
    lines.append('1 区画が記録と一致し、雛形と逐語で同じ行の数だけなら違反 0')
    probe = good[:5] + [MB['begin'], '確証 99 本', MB['end'], '本文 `37%` の数', '年 (2048) の数', '第3章 の数', '番号 #12 の数', '裁定 D99 の数', '容量 12 GB の数', '段 7 の数',
                        MB['cost_line_tag'] + ' 費用 1200 と確証 88 本', '本報告は両方向不定。']
    V = lint('\n'.join(probe) + '\n', T, frozenset(), sidecar=side); kinds = [v['kind'] for v in V]; toks = [v['token'] for v in V if v['kind'] == '未登録の数']
    assert '機械の区画の数が記録と違う' in kinds and '費用の行の数が一つでない' in kinds, kinds
    for want in ('37%', '2048', '3', '12', 'D99', '7'):
        assert want in toks, (want, toks)
    assert sum(1 for t in toks if t == '12') >= 2, toks
    lines.append('2 検分の探り入力（W42）: 偽の区画・code span の数・(2048)・第3章・#12・D99・12 GB・段 7・費用の行の別の数がすべて違反（%d 件）' % len(V))
    fake = good[:3] + ['確証 7 本（書き換え）'] + good[4:]
    V = lint('\n'.join(fake) + '\n', T, frozenset(['雛形の行 12 本']), sidecar=side); assert [v['kind'] for v in V] == ['機械の区画の中身が記録と違う'], V
    V = lint(text, T, frozenset(['雛形の行 12 本']), sidecar=None); assert [v['kind'] for v in V] == ['機械の区画の記録が無い'], V
    lines.append('3 区画の中身の書き換えは記録との不一致・記録が無ければ違反')
    V = lint('\n'.join([MB['cost_line_tag'] + ' 費用 1200', '記録 D-3 と 2026-09-14 と SHA16 0123456789ABCDEF', '本報告は両方向不定。']) + '\n', T, frozenset())
    assert V == [], V
    lines.append('4 打ち込んでよい型（費用の行の一つの数・逸脱番号・日付・SHA16）は違反にしない')
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'r.md'); open(p, 'w', encoding='utf-8').write(text); S = write_sidecar(p, text, T, 'selftest')
        assert os.path.exists(sidecar_path(p)) and S['blocks'] == side['blocks']
    lines.append('5 write_sidecar・sidecar_path の往復')
    print('report_lint.py %s SELFTEST PASS' % VERSION); print('\n'.join(lines))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    ap = argparse.ArgumentParser(); ap.add_argument('report'); ap.add_argument('--out', default=None); ap.add_argument('--contrasts', default=None); ap.add_argument('--template', default=None)
    ap.add_argument('--sidecar', default=None)
    a = ap.parse_args()
    T = runs_A.load_T(a.contrasts); text = open(a.report, encoding='utf-8').read()
    tp = a.template or os.path.join(REPO, T['report_rules']['template'])
    TL = frozenset(open(tp, encoding='utf-8').read().replace('\r\n', '\n').split('\n')) if os.path.exists(tp) else frozenset()
    sp = a.sidecar or sidecar_path(a.report); SIDE = runs_A.read_json(sp) if os.path.exists(sp) else None
    V = lint(text, T, TL, sidecar=SIDE)
    out = a.out or os.path.join(REPO, 'records', 'A', 'report-lint-%s.md' % os.path.splitext(os.path.basename(a.report))[0])
    kinds = {}
    for v in V:
        kinds[v['kind']] = kinds.get(v['kind'], 0) + 1
    M = ['# 報告の走査（機械生成・`tools/report_lint.py` %s・%s UTC）' % (VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')), '',
         '- 対象: `%s`（SHA16 %s）・雛形 %s（SHA16 %s）・機械の区画の記録 %s・正本 SHA16 %s' % (os.path.basename(a.report), runs_A.sha16_file(a.report), os.path.basename(tp), runs_A.sha16_file(tp) if os.path.exists(tp) else '無し',
                                                                     ('%s（SHA16 %s）' % (os.path.basename(sp), runs_A.sha16_file(sp))) if SIDE is not None else '無し', runs_A.sha16_file(a.contrasts or runs_A.CPATH)),
         '- 違反の合計: %d（%s）' % (len(V), json.dumps(kinds, ensure_ascii=False)),
         '- 限界: 本器は語と数の形・記入欄の埋め残し・機械の区画の記録との突合・条項の有無を見るだけで、報告の読みの当否・機械の区画の中身の正しさは検査しない。雛形と逐語で同じ行の数は検査しない。', '']
    M += ['| 種類 | 行 | 語・数 | 文脈 |', '|---|---|---|---|'] + ['| %s | %d | %s | %s |' % (v['kind'], v['line'], v['token'], v['context'].replace('|', '／')) for v in V]
    M += ['', '本ファイルのいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
    print('[report_lint] 違反 %d %s → %s' % (len(V), json.dumps(kinds, ensure_ascii=False), out))
    sys.exit(1 if V else 0)
