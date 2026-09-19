# -*- coding: utf-8 -*-
"""mutation_B.py v2 —— **自己検査が、直す前の誤りを入れ直したときに落ちるか**を確かめる（正本 `selftest_rule`・裁定 D122）。

系統の外への検分で、**差し戻しの原因そのものに戻しても両方の自己検査が「すべて通った」と印字する**ことが分かった。
「検査が通った」を品質の証拠にしないために、**検査そのものを検査する**器を置く。

やり方: 器材を一時置き場に丸ごと写し、**一件ずつ誤りを入れ直して**自己検査を走らせ、**落ちることを確かめる**。
        落ちなければ、その検査は守りになっていない（終了コード非零で止まる）。
出力: records/B/mutation-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/mutation_B.py [--force] [--list]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, argparse, subprocess, tempfile, datetime

VERSION = 'v2'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

# (名, 直した裁定, どの器の何を戻すか, 置換〔前 → 後〕, 落ちてほしい自己検査)
MUTATIONS = [
    ('全方向のノルム合わせ', 'D102', 'direction_B.py',
     ("            if name != 'static':", "            if name == 'td':"),
     ['direction_B.py'],
     '方向を作る器が td にしか合わせない誤り（交差族と S4 の反証に「加わる量が腕と統制で違う」構図が残る）。'
     '**守るのは方向を作る器である**——介入の器（steer_B）は自分で合わせた模造ベクトルしか見られないので、'
     'ここは守れない。走行器が npz を読むときにノルムを確かめる検査は、**本体を書くときに足す**（裁定 D117）'),
    ('帯の起点（主位置）', 'D124', 'steer_B.py',
     ('    return pad_len + len(ids) - 1', '    return pad_len + 0'),
     ['steer_B.py'],
     '起点が列の先頭になる誤り（帯が役割トークンから掛かる）'),
    ('係数の掛け方', 'D90', 'steer_B.py',
     ('        out.append(g * (target / n) if n else g)', '        out.append(g * (target / n) * 2.0 if n else g)'),
     ['steer_B.py'],
     'ランダム方向のノルムが v̂ と違う誤り（加わる量が腕と統制で違う）'),
    ('バッチの腕の同質性', 'D124', 'steer_B.py',
     ("    if len(set(arm_texts)) > 1:", "    if False:"),
     ['steer_B.py'],
     'バッチに複数の腕が混ざっても止めない誤り'),
    ('層番号の四捨五入', 'D4', 'direction_B.py',
     ('int(math.floor(ratio * n_layers + 0.5)) - 1', 'int(math.floor(ratio * n_layers)) - 1'),
     ['direction_B.py'],
     '層の添字が一つずれる誤り'),
    # ---- 直しの監査（2026-09-19）で器に入れた規則 ----
    ('S4 の片側上限を狭める', 'D118', 'rules_B.py',
     ('    one = newcombe(kB, nB, kA, nA, 0.90)', '    one = newcombe(kB, nB, kA, nA, 0.50)'),
     ['rules_B.py'],
     '「下がらなかった（封印は当たり）」が出やすくなる誤り（封印が当たりやすい側・起草者の引力と同じ側）'),
    ('区間を Wald に戻す', 'D130', 'rules_B.py',
     ('    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)', '    lo = d - _z(conf) * math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)'),
     ['rules_B.py'],
     '床の近くで被覆が崩れる区間に戻る誤り'),
    ('等質性の境目を注に数える', 'D127', 'rules_B.py',
     ("    return {'note': bool(spread > thr),", "    return {'note': bool(spread >= thr),"),
     ['rules_B.py'],
     '境目ちょうどに注を付ける誤り（正本は「超えたら」）'),
    ('同方向の判定を大小の一致に戻す', 'D130', 'rules_B.py',
     ('    return d1 is not None and d2 is not None and (d1 * d2) > 0', '    return d1 is not None and d2 is not None and (d2 > 0) == (d1 > 0)'),
     ['rules_B.py'],
     '差が零のとき、偽どうしで同方向と誤判定する誤り（系統外の検分で捕まった型）'),
    ('読めた分母から書式外を除かない', 'D127', 'rules_B.py',
     ("('readable', lambda c: c['n_ok'] - c['refuse'] - c['ff'])", "('readable', lambda c: c['n_ok'] - c['refuse'])"),
     ['rules_B.py'],
     '書式外による希釈が refuse 門をすり抜ける誤り'),
    ('api_error の門を外す', 'D127', 'rules_B.py',
     ('    return bool(d > thr + 1e-12)', '    return False'),
     ['rules_B.py'],
     '差のある欠測を品質床の門で止めない誤り'),
    ('行ごとの方向を一本にする', 'D117', 'run_stageB_local.py',
     ('                hs[i, int(st):, :] = hs[i, int(st):, :] + (add[i] if per_row else add)',
      '                hs[i, int(st):, :] = hs[i, int(st):, :] + (add[0] if per_row else add)'),
     ['run_stageB_local.py'],
     'ランダム方向の腕のすべての行に同じ方向が掛かる誤り'),
    ('様式の欄を空で書く', 'D117', 'run_stageB_local.py',
     ("            'style_a': bool(mf['a']), 'style_b': bool(mf['b']), 'mention': bool(mf['c1']),",
      "            'style_a': None, 'style_b': None, 'mention': None,"),
     ['run_stageB_local.py'],
     '様式門が実データで黙って効かない誤り（走行器 v4 まで実際にこうだった）'),
]

# 合成データを通して確かめる変異（自己検査では見えない・裁定 D122／D125・D126・D121・D119）
# (名, 裁定, 器, 置換, 何が起きてはいけないか, 見る場所)
PIPELINE_MUTATIONS = [
    ('様式門を Holm の順位に戻す', 'D125', 'analyze_B.py',
     ("not (r.get('fired') or [])", "not _hard(r)"),
     '様式門の保留が順位を消費し、次の対比の閾値が α/m から α/(m−1) に緩む',
     'analyze', None),
    ('封印の語彙の写しを外す', 'D121', 'analyze_B.py',
     ("want = SIGN_MAP.get((SEAL.get('signs') or {}).get(r['id']))",
      "want = (SEAL.get('signs') or {}).get(r['id'])"),
     '正本の語彙で封印すると確証がすべて「登録された向きと逆」になる',
     'analyze', None),
    ('セッション記録の検査を本走行だけに戻す', 'D126', 'integrity_B.py',
     ("    if rk not in sessions:", "    if PHASE == 'main' and rk not in sessions:"),
     '調整走行・品質床・同一性選別で記録が無くても素通りする',
     'integrity', 'drop_sessions'),
    ('門のセッション検査を外す', 'D126', 'gate_B.py',
     ("if _miss and not a.allow_no_sessions:", "if False:"),
     '門が記録の不在を素通りする',
     'gate', 'drop_sessions'),
    ('升目の欠けを incomplete に倒さない', 'D126', 'gate_B.py',
     ("if _gap_tune and not a.allow_missing_cells:", "if False:"),
     '調整走行の升目が欠けても判定が open のまま',
     'gate', 'drop_tune_cell'),
    # ---- 直しの監査（2026-09-19）で集計器と読み口に繋いだ規則 ----
    ('等質性の注を集計器が付けない', 'D127', 'analyze_B.py',
     ("HOMOG = {k: rules_B.homogeneity(v, T) for k, v in HOMOG.items()}", "HOMOG = {k: dict(rules_B.homogeneity(v, T), note=False) for k, v in HOMOG.items()}"),
     'ランダム方向の三本が不均一でも注が付かない',
     'analyze', None),
    ('td の特異性を集計器が数えない', 'D123', 'analyze_B.py',
     ("    ts = rules_B.td_specificity(r['k_A'], r['n_A'], r['k_B'], r['n_B'], T)", "    ts = {'write_specificity': True}"),
     'td が v と同じだけ動いても特異性を書ける（起草者の引力と同じ側）',
     'analyze', None),
    ('様式の欄の空を採点欠落に数えない', 'D117', 'runs_B.py',
     ("        if phase != 'quality' and any(r.get(k) is None for k in ('style_a', 'style_b', 'mention')):", "        if False:"),
     '走行器が様式を書かなくても、様式門が黙って素通りする（走行器 v4 まで実際にそうだった）',
     'analyze', 'null_style'),
]


def break_data(root, how):
    """守りを試すために入力を壊す（**壊れた入力を止めるのが守りである**）。"""
    import glob
    if how == 'drop_sessions':
        shutil.rmtree(os.path.join(root, 'sessions-B'), ignore_errors=True)
    elif how == 'drop_tune_cell':
        d = sorted(glob.glob(os.path.join(root, 'tuneB', '*')))
        if d:
            shutil.rmtree(d[0], ignore_errors=True)
    elif how == 'null_style':
        # 本走行の一つの腕の試行の様式・言及の欄を空にする（走行器が様式を書かなかった場合・2026-09-19）
        for f in sorted(glob.glob(os.path.join(root, 'stageB', '*', 'trials-*.jsonl')))[:1]:
            rows = [json.loads(l) for l in open(f, encoding='utf-8') if l.strip()]
            arm0 = next(r['arm'] for r in rows if '+v' in r['arm'] and 'vrand' not in r['arm'])
            for r in rows:
                if r['arm'] == arm0:
                    r['style_a'] = r['style_b'] = r['mention'] = None
            with open(f, 'w', encoding='utf-8', newline='\n') as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + '\n')


def run(tool, cwd):
    # **飛ばしを失敗に倒して走らせる**（裁定 D122・2026-09-19）。前は実トークナイザの置き場を渡し忘れると
    # 帯の起点の検査が「飛ばした」で通り、変異を「守りが無い」と誤って記録した（実際に起きた）。
    # いまは置き場が無ければ、変異を入れる前の土台の確認で止まる。
    p = subprocess.run([PY, os.path.join(cwd, 'tools', tool), '--selftest'],
                       capture_output=True, text=True, encoding='utf-8', cwd=cwd,
                       env=dict(os.environ, OP4B_REQUIRE_FULL_SELFTEST='1'))
    return p.returncode, ((p.stdout or '') + (p.stderr or '')).strip().split('\n')[-1][:160]



def pipeline_probe(cwd, kind, root):
    """合成データを通して、変異が**札や判定に出るか**を見る。戻りは (終了コード, 見分けのための値)。

    **走らせる前に古い記録を消す**——変異を入れた器が例外で落ちると記録を書かないので、
    前回の記録が残っていると**それを読んでしまい、守りがあるように見える**（この器自身がその型で作られていた）。
    """
    import glob
    for f in glob.glob(os.path.join(root, '[agi]*.json')) + glob.glob(os.path.join(root, 'i_*.json')):
        try:
            os.remove(f)
        except OSError:
            pass
    g_md, g_js = os.path.join(root, 'g.md'), os.path.join(root, 'g.json')
    rc_g = subprocess.run([PY, os.path.join(cwd, 'tools', 'gate_B.py'), '--root', root, '--allow-dry',
                           '--out', g_md, '--force'], capture_output=True, text=True, encoding='utf-8', cwd=cwd).returncode
    if kind == 'gate':
        v = None
        if os.path.exists(g_js):
            v = json.load(open(g_js, encoding='utf-8')).get('verdict')
        return rc_g, v
    if kind == 'integrity':
        # **不整合の件数で見る**（終了コードだけだと、例外で落ちた場合と区別できない）。
        out = {}
        for t in ('stageB', 'tuneB', 'stageB-quality', 'idB'):
            ij = os.path.join(root, 'i_%s.json' % t)
            rc = subprocess.run([PY, os.path.join(cwd, 'tools', 'integrity_B.py'), '--tag', t, '--root', root,
                                 '--allow-dry', '--out', os.path.join(root, 'i_%s.md' % t), '--force'],
                                capture_output=True, text=True, encoding='utf-8', cwd=cwd).returncode
            n = None
            if os.path.exists(ij):
                try:
                    n = len(json.load(open(ij, encoding='utf-8')).get('problems') or [])
                except Exception:
                    n = 'json が読めない'
            out[t] = {'rc': rc, 'problems': n}
        return (0 if all(v['rc'] == 0 for v in out.values()) else 1), out
    seal = os.path.join(root, 'seal-B.json')
    cmd = [PY, os.path.join(cwd, 'tools', 'analyze_B.py'), '--root', root, '--gate', g_js, '--allow-dry',
           '--allow-partial-seal', '--out', os.path.join(root, 'a.md'), '--force']
    if os.path.exists(seal):
        cmd += ['--seal', seal]
    rc_a = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', cwd=cwd).returncode
    aj = os.path.join(root, 'a.json')
    if not os.path.exists(aj):
        return rc_a, None
    d = json.load(open(aj, encoding='utf-8'))
    return rc_a, {'holm_alpha': sorted(round(c['holm_alpha'], 6) for c in d['confirm'] if c.get('holm_alpha') is not None),
                  'confirm': sum(1 for c in d['confirm'] if str(c.get('label', '')).startswith('確証')),
                  'reverse': sum(1 for c in d['confirm'] if '逆' in str(c.get('label'))),
                  'style_hold': sum(1 for c in d['confirm'] if c.get('label') == '判定保留（様式転位）'),
                  'agree': (d.get('sign_agreement') or {}).get('agree'),
                  'homog_notes': sum(1 for c in d['confirm'] if any('不均一' in n for n in (c.get('notes') or []))),
                  'td_write': sum(1 for t in (d.get('td_specificity') or []) if t.get('write_specificity')),
                  'gap': sum(1 for c in d['confirm'] if c.get('label') == '判定不能（採点欠落）')}


ap = argparse.ArgumentParser()
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--list', action='store_true')
a = ap.parse_args()
if a.list:
    for m in MUTATIONS:
        print('  %-20s（裁定 %s・%s）: %s' % (m[0], m[1], m[2], m[5]))
    for m in PIPELINE_MUTATIONS:
        print('  %-24s（裁定 %s・%s・壊し方 %s）' % (m[0], m[1], m[2], m[6] or '無し'))
    sys.exit(0)

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'mutation-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p_ in (out_md, out_json):
        if os.path.exists(p_):
            sys.exit('既にある（--force で上書き）: %s' % p_)

tmp = tempfile.mkdtemp(prefix='mutB_')
rows, n_bad = [], 0
try:
    for sub in ('tools', 'design', 'arms'):
        src = os.path.join(REPO, sub)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(tmp, sub))
    # 変異を入れる前に、全部通ることを確かめる（土台の確認）
    base = {}
    for tool in sorted({t for m in MUTATIONS for t in m[4]}):
        base[tool] = run(tool, tmp)
        if base[tool][0] != 0:
            sys.exit('変異を入れる前から自己検査が落ちている: %s（%s）' % (tool, base[tool][1]))
    for name, ruling, target, (old, new), tools, what in MUTATIONS:
        p = os.path.join(tmp, 'tools', target)
        s = open(p, encoding='utf-8').read()
        if s.count(old) != 1:
            rows.append({'name': name, 'ruling': ruling, 'target': target, 'applied': False,
                         'note': '変異の相手が %d 件（器が変わったので変異の定義を直す）' % s.count(old)})
            n_bad += 1
            continue
        open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new))
        got = {t: run(t, tmp) for t in tools}
        caught = [t for t, (rc, _) in got.items() if rc != 0]
        missed = [t for t, (rc, _) in got.items() if rc == 0]
        rows.append({'name': name, 'ruling': ruling, 'target': target, 'applied': True, 'what': what,
                     'caught': caught, 'missed': missed,
                     'lines': {t: got[t][1] for t in tools}})
        if missed:
            n_bad += 1
        open(p, 'w', encoding='utf-8', newline='\n').write(s)      # 戻す
    # ---- 合成データを通して見る変異（自己検査では見えないもの） ----
    if PIPELINE_MUTATIONS:
        root = os.path.join(tmp, 'synth')
        rc = subprocess.run([PY, os.path.join(tmp, 'tools', 'synth_B.py'), '--case', 'all', '--out-root', root],
                            capture_output=True, text=True, encoding='utf-8', cwd=tmp).returncode
        if rc != 0:
            sys.exit('合成データを作れない（変異の前）')
        base_probe = {}
        for kind in sorted({m[5] for m in PIPELINE_MUTATIONS}):
            base_probe[kind] = pipeline_probe(tmp, kind, root)
        for name, ruling, target, (old, new), what, kind, how in PIPELINE_MUTATIONS:
            p = os.path.join(tmp, 'tools', target)
            s0 = open(p, encoding='utf-8').read()
            if s0.count(old) != 1:
                rows.append({'name': name, 'ruling': ruling, 'target': target, 'applied': False, 'pipeline': True,
                             'note': '変異の相手が %d 件（器が変わったので変異の定義を直す）' % s0.count(old)})
                n_bad += 1
                continue
            # **壊した入力で当てる**（健全な入力では守りの有無が出力に出ない）
            probe_root = root
            if how:
                probe_root = os.path.join(tmp, 'broken_' + how)
                shutil.rmtree(probe_root, ignore_errors=True)
                shutil.copytree(root, probe_root)
                break_data(probe_root, how)
                before = pipeline_probe(tmp, kind, probe_root)      # 直した器が壊れた入力を止めるか
            else:
                before = base_probe[kind]
            open(p, 'w', encoding='utf-8', newline='\n').write(s0.replace(old, new))
            got = pipeline_probe(tmp, kind, probe_root)
            changed = (got != before)
            rows.append({'name': name, 'ruling': ruling, 'target': target, 'applied': True, 'pipeline': True,
                         'what': what, 'kind': kind, 'changed': changed, 'broken': how or '（健全な入力）',
                         'base': str(before)[:110], 'mutated': str(got)[:110]})
            if not changed:
                n_bad += 1
            open(p, 'w', encoding='utf-8', newline='\n').write(s0)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

json.dump({'kind': 'mutation_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'rows': rows, 'missed': n_bad, 'total': len(MUTATIONS) + len(PIPELINE_MUTATIONS)},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B **自己検査の検査**（変異・機械生成・`tools/mutation_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 正本 `selftest_rule`（裁定 D122）: **自己検査は、変異を入れて落ちるところまで作る。**',
     '- やり方: 器材を一時置き場に写し、**直す前の誤りを一件ずつ入れ直して**自己検査を走らせ、**落ちることを確かめる**。',
     '- **%d 件のうち、捕まえられなかった変異は %d 件。**（自己検査で見る %d 件・合成データを通して見る %d 件）'
     % (len(MUTATIONS) + len(PIPELINE_MUTATIONS), n_bad, len(MUTATIONS), len(PIPELINE_MUTATIONS)), '',
     '| 入れ直した誤り | 直した裁定 | 器 | 落ちた検査 | **落ちなかった検査** |', '|---|---|---|---|---|']
for r in rows:
    if not r.get('applied'):
        L.append('| %s | %s | `%s` | — | **変異を入れられない**（%s） |' % (r['name'], r['ruling'], r['target'], r['note']))
        continue
    if r.get('pipeline'):
        L.append('| %s | %s | `%s` | %s | %s |'
                 % (r['name'], r['ruling'], r['target'],
                    ('%s で出力が変わった（%s → %s）' % (r['broken'], r['base'], r['mutated'])) if r['changed']
                    else ('%s' % r['broken']),
                    '無し' if r['changed'] else '**出力が変わらない＝守りが無い**'))
        continue
    L.append('| %s | %s | `%s` | %s | %s |'
             % (r['name'], r['ruling'], r['target'],
                '・'.join(r['caught']) or '**無し**', ('**' + '・'.join(r['missed']) + '**') if r['missed'] else '無し'))
L += ['', '## 入れ直した誤りの中身', ''] + ['- **%s**（裁定 %s）: %s' % (r['name'], r['ruling'], r.get('what', r.get('note', '')))
                                              for r in rows]
L += ['', '## この検査が確認していないこと', '',
      '- **変異の一覧は起草者が選んだものである。**起草者が想像しなかった壊れ方は入っていない。',
      '- 自己検査が**通る**ことは、器が正しいことを意味しない（この器が見るのは「守りがあるか」だけである）。',
      '- 実機（GPU・実重み）では何も走らせていない。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[mutation_B] %s | %d 件中 捕まえられなかった変異 %d 件'
      % (os.path.relpath(out_md, REPO), len(MUTATIONS) + len(PIPELINE_MUTATIONS), n_bad))
for r in rows:
    if r.get('missed') or not r.get('applied'):
        print('  **守りが無い**: %s（%s）' % (r['name'], '・'.join(r.get('missed', [])) or r.get('note', '')))
sys.exit(1 if n_bad else 0)
