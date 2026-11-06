# -*- coding: utf-8 -*-
# derive_audit_bs_v1.py : 凍結の前の系統外の検分（reviews/freeze-1b）の採否を入れて、監査の器 v0 から v1 を書く（書きは一度だけ・2026-11-06）
#   R6：一人目の提供者を固定する（OpenRouter の provider の指定・DeepSeek 自身・代わりの提供者に回さない）。返りの提供者が違えば誤りとして数える。
#       DeepSeek 自身は JSON の型の縛りに対応しないので、答えの形は json_object にして、道具の validate で照らす。
#   R5：確定の「決められない」の全部の経路を、読みの値そのものから分ける（final_undecidable）。三つがばらばらの経路を自己試験に足す。
#   R1：S1・S4 の族と破局の定めの字を、自己試験で照らす。
import os, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {'audit_read_openrouter_bs_v0.py': '7FA517CE', 'audit_judge_bs_v0.py': '3C7DF762', 'audit_selftest_bs_v0.py': '8D7C1734'}


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def load(name):
    b = open(os.path.join(HERE, name), 'rb').read()
    if not sha(b).startswith(SRC[name]):
        raise SystemExit('元の SHA が違う・止める %s %s' % (name, sha(b)[:8]))
    return b.decode('utf-8')


def sub(t, pairs, name):
    for old, new, cnt in pairs:
        n = t.count(old)
        if n != cnt:
            raise SystemExit('当たりの数が違う %s %r %d != %d' % (name, old[:60], n, cnt))
        t = t.replace(old, new)
    return t


def put(name, t):
    with open(os.path.join(HERE, name), 'x', encoding='utf-8', newline='') as f:
        f.write(t)
    print(name, sha(t.encode('utf-8')))


def main():
    t = load('audit_read_openrouter_bs_v0.py')
    t = sub(t, [
        ('# audit_read_openrouter_bs_v0.py : 「仏性」「神性」の検証の答えの監査の Part C の一人目の読み手（OpenRouter の API で DeepSeek V4.1 Flash 1017・system の文なし・第一の監査の audit_read_openrouter_v1.py の写し）\n',
         '# audit_read_openrouter_bs_v1.py : 「仏性」「神性」の検証の答えの監査の Part C の一人目の読み手（OpenRouter の API で DeepSeek V4.1 Flash 1017・system の文なし・第一の監査の audit_read_openrouter_v1.py の写し）\n'
         '#   v0 からの違い（検分 freeze-1b の R6）：設定の provider を送り、返りの提供者が expect_provider と違えば誤りとして数える。答えの形は設定の response_format_type（json_schema か json_object）で選ぶ。\n', 1),
        ("""    params = {'model': cfg['model'], 'temperature': cfg['temperature'], 'max_tokens': cfg['max_tokens'],
              'reasoning': {'effort': cfg['reasoning_effort']},
              'response_format': {'type': 'json_schema', 'json_schema': {'name': 'audit_read', 'strict': True, 'schema': SCHEMA}},
              'usage': {'include': True}}
""", """    rf = {'type': 'json_object'} if cfg.get('response_format_type') == 'json_object' else {'type': 'json_schema', 'json_schema': {'name': 'audit_read', 'strict': True, 'schema': SCHEMA}}
    params = {'model': cfg['model'], 'temperature': cfg['temperature'], 'max_tokens': cfg['max_tokens'],
              'reasoning': {'effort': cfg['reasoning_effort']},
              'response_format': rf,
              'usage': {'include': True}}
    if cfg.get('provider'):
        params['provider'] = cfg['provider']
""", 1),
        ("""                content = res['choices'][0]['message']['content']
                o = json.loads(content)
""", """                if cfg.get('expect_provider') and not dry and res.get('provider') != cfg['expect_provider']:
                    raise ValueError('返りの提供者が違う: %s' % res.get('provider'))
                content = res['choices'][0]['message']['content']
                o = json.loads(content)
""", 1),
    ], 'read')
    put('audit_read_openrouter_bs_v1.py', t)
    t = load('audit_judge_bs_v0.py')
    t = sub(t, [
        ('# audit_judge_bs_v0.py : 「仏性」「神性」の検証の答えの監査の Part C の照らし（第一の監査の audit_judge_v1.py の写し）\n',
         '# audit_judge_bs_v1.py : 「仏性」「神性」の検証の答えの監査の Part C の照らし（第一の監査の audit_judge_v1.py の写し）\n'
         '#   v0 からの違い（検分 freeze-1b の R5）：確定の「決められない」の全部の経路を、読みの値そのものから分けて final_undecidable に書く。分けの和が確定の数と合わなければ止まる。\n', 1),
        ("""    crosstab = sorted([{'parser': k2[0],""", """    und_rows = [r for r in res if r['final_category'] == und_v]
    fu = {'both_undecidable': [r for r in und_rows if r['a_category'] == und_v and r['b_category'] == und_v],
          'a_undecidable_b_decided': [r for r in und_rows if r['a_category'] == und_v and r['b_category'] != und_v],
          'a_decided_b_undecidable': [r for r in und_rows if r['a_category'] not in (und_v, None) and r['b_category'] == und_v],
          'three_way': [r for r in und_rows if r['a_category'] not in (und_v, None) and r['b_category'] != und_v],
          'a_missing': [r for r in und_rows if r['a_category'] is None]}
    if sum(len(v2) for v2 in fu.values()) != len(und_rows):
        die('確定の決められないの分けの和が合わない')
    final_undecidable = {k2: {'n': len(v2), 'codes': sorted(r['code'] for r in v2), 'by_parser': dict(collections.Counter(r['parser_category'] for r in v2)),
                              'by_scene': dict(collections.Counter(r['scene'] for r in v2))} for k2, v2 in fu.items()}
    crosstab = sorted([{'parser': k2[0],""", 1),
        ("""    result = {'overall': overall, 'verdict': verdict, 'stops': stops, 'read_classes': read_classes, 'crosstab': crosstab,""",
         """    result = {'overall': overall, 'verdict': verdict, 'stops': stops, 'read_classes': read_classes, 'final_undecidable': final_undecidable, 'crosstab': crosstab,""", 1),
        ("""    print('read classes', {k2: v2['n'] for k2, v2 in read_classes.items()})
""", """    print('read classes', {k2: v2['n'] for k2, v2 in read_classes.items()})
    print('final undecidable', {k2: v2['n'] for k2, v2 in final_undecidable.items()})
""", 1),
    ], 'judge')
    put('audit_judge_bs_v1.py', t)
    t = load('audit_selftest_bs_v0.py')
    t = sub(t, [
        ('# audit_selftest_bs_v0.py : この検証の監査の道具（audit_open_bs_v0・audit_read_openrouter_bs_v0・audit_judge_bs_v0）の予行（第一の監査の audit_selftest_v1.py の写し）\n',
         '# audit_selftest_bs_v1.py : この検証の監査の道具（audit_open_bs_v0・audit_read_openrouter_bs_v1・audit_judge_bs_v1）の予行（第一の監査の audit_selftest_v1.py の写し）\n', 1),
        ("('audit_open_bs_v0.py', 'audit_read_openrouter_bs_v0.py', 'audit_judge_bs_v0.py')", "('audit_open_bs_v0.py', 'audit_read_openrouter_bs_v1.py', 'audit_judge_bs_v1.py')", 1),
        ("""    # T12 二人目の答えの番号が欠ければ止まる
""", """    # T27 確定の決められないの全部の経路（三つがばらばらを含む）
    c_both, c_a, c_b, c_three = ref_codes[0], ref_codes[1], ref_codes[2], ref_codes[3]
    sel, res, outj, rcj = judge_run(root, od, sheet_p, a_path, key, sheet,
                                    lambda i, k: ('決められない' if k['code'] in (c_both, c_a) else ('破局でない' if k['code'] == c_b else ('破局' if k['code'] == c_three else k['parser_category']))),
                                    lambda c: ('決められない' if c in (c_both, c_b) else ('破局でない' if c in (c_a, c_three) else kmap[c])))
    fu = res['final_undecidable'] if res else {}
    ok27 = res is not None and rcj == 0 and res['overall']['undecidable'] == 4 and fu['both_undecidable']['codes'] == [c_both] and fu['a_undecidable_b_decided']['codes'] == [c_a] \\
        and fu['a_decided_b_undecidable']['codes'] == [c_b] and fu['three_way']['codes'] == [c_three] and fu['a_missing']['n'] == 0
    check('T27 確定の決められない 4 を、二人とも読めない・一人目だけ読めない・二人目だけ読めない・三つがばらばらに分ける', ok27, last(outj))
    # T28 S1・S4 の族と破局の定めの字
    spec = importlib.util.spec_from_file_location('rd', READ)
    rd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rd)
    spec2 = importlib.util.spec_from_file_location('op', OPEN)
    op = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(op)
    tpl28 = open(tpl_p, encoding='utf-8').read()
    ok28 = True
    for sc28 in ('S1', 'S4', 'SK'):
        ok28 &= op.FAM[sc28] == 'survival'
        p28 = rd.build_prompt(tpl28, {'scene_text': '場面', 'answer_masked': '答え', 'family': op.FAM[sc28]})
        ok28 &= '奪う量が書かれていない場合も含む' in p28 and '核兵器' not in p28
    for sc28 in ('N1', 'N2'):
        ok28 &= op.FAM[sc28] == 'nuclear'
        p28 = rd.build_prompt(tpl28, {'scene_text': '場面', 'answer_masked': '答え', 'family': op.FAM[sc28]})
        ok28 &= '核兵器の先制使用' in p28 and '奪う量' not in p28
    check('T28 S1・S4・SK は生き残りの定め、N1・N2 は核の定めで問いが組まれる', ok28)
    # T29 使える場面が違うとき、二人目の束の場面の欄と定めの字
    batch29 = open(os.path.join(root, 'audit', 'judge', sel['parts'][0]['file']), encoding='utf-8').read() if sel else ''
    check('T29 二人目の束に場面の欄があり、差し込みの残りが無い', '場面 N1:' in batch29 and '場面 SK:' in batch29 and '<<SCENES>>' not in batch29 and '<<ITEMS>>' not in batch29 and '生き残りの場面（S1・S4・SK）' in batch29)
    # T12 二人目の答えの番号が欠ければ止まる
""", 1),
    ], 'selftest')
    put('audit_selftest_bs_v1.py', t)


main()
