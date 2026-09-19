# 器材のソース（逐語・参照）（参照・関わる問い (b)(g)・機械生成・2026-09-19 01:57 UTC）

## `tools/mutation_B.py`（SHA16 EDB3B6B5D93E9047・346 行）

```python
# -*- coding: utf-8 -*-
"""mutation_B.py v3 —— **自己検査が、直す前の誤りを入れ直したときに落ちるか**を確かめる（正本 `selftest_rule`・裁定 D122）。

系統の外への検分で、**差し戻しの原因そのものに戻しても両方の自己検査が「すべて通った」と印字する**ことが分かった。
「検査が通った」を品質の証拠にしないために、**検査そのものを検査する**器を置く。

やり方: 器材を一時置き場に丸ごと写し、**一件ずつ誤りを入れ直して**自己検査を走らせ、**落ちることを確かめる**。
        落ちなければ、その検査は守りになっていない（終了コード非零で止まる）。
出力: records/B/mutation-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/mutation_B.py [--force] [--list]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, argparse, subprocess, tempfile, datetime

VERSION = 'v3'
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
    # ---- 採否表の引用の照合（2026-09-19・束の前の点検で手で打った引用の誤りが多数見つかった） ----
    ('引用の裁定の照合を外す', '—', 'citations_B.py',
     ('                if not (ds & rd):', '                if False:'),
     ['citations_B.py'],
     '引用の括弧の裁定と、引いた採否表の行の裁定が食い違っても止めない誤り（直す前の器材に実際に四十件余りあった型）'),
    ('出所の札の照合を外す', '—', 'citations_B.py',
     ('                if not ok(voters):', '                if False:'),
     ['citations_B.py'],
     '系統内の検分が挙げた所見に「系統外の検分」の札を付けても止めない誤り（独立の票の記録が水増しされる側）'),
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
```

## `tools/endtoend_B.py`（SHA16 5F7564CE5AA66C2E・422 行）

```python
# -*- coding: utf-8 -*-
"""endtoend_B.py v2 —— 走行器と抽出器の本体を、**小さな模型で端から端まで通す**（裁定 D117・2026-09-18）。

系統の外への検分で、四票すべてが「**介入を掛けて走らせる器がまだ無い**」ことを最初に挙げた。
本体を書いたので、**実重みが無くても通せるところまで通す**——
ランダム初期化の小さな Qwen3 形（層が少なく隠れ次元も小さい）で、
方向の抽出 → 凍結 → 読み込み → hook → 生成 → 採点 → 記録の書き出しを一本の流れで走らせる。

確かめること（いずれも**恒真にならない形**で・裁定 D122）:
  (1) `hidden_states[idx+1]` が `layers[idx]` の出力と一致する（抽出した層と介入する層が同じ）。
  (2) 係数 0 の hook を掛けた生成が、hook 無しと**一致**する（hook そのものが結果を壊していない）。
  (3) 係数 ≠ 0 で、**prefill の主位置**と**復号の各段**に、狙いどおりの量が加わる。
  (4) hook はバッチの後に**零本**になる（`finally` で外す）。
  (5) 腕が混ざったバッチは**止まる**。
  (6) 凍結した方向のノルムが崩れていたら、走行器が**読み込みの時点で止まる**。
  (7) 試行の記録が正本の欄をそろえている。
  (8) 走行器の出力を置き場に書き、本物の整合検査に通す（種・再開）。
  (9) v2（2026-09-19・束の前の点検で見つけた穴）: **すべての種類の腕**を走らせる（前は無操作と +v の二腕だけで、
      ランダム方向の腕が走らないことに気づかなかった）。ランダム方向の行ごとの割り当て・hook の中身の照合・
      様式と言及と refuse の分類とループが段階 A の凍結した関数と一致・生テキストの書き出し・副位置の活性。
**実重みでは何も確かめていない。** 模型は乱数で初期化したもので、率にも活性にも意味は無い。
出力: records/B/endtoend-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/endtoend_B.py [--force] [--layers 4] [--hidden 64]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, tempfile, shutil

VERSION = 'v2'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.dirname(HERE)

ap = argparse.ArgumentParser()
ap.add_argument('--layers', type=int, default=4)
ap.add_argument('--hidden', type=int, default=64)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
a = ap.parse_args()

try:
    import torch
    import numpy as np
    from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
except Exception as e:
    sys.exit('torch／transformers が無い: %s' % e)

import runs_B, steer_B, direction_B
import run_stageB_local as RUN

T = runs_B.load_T()
SNAP = os.environ.get('OP4B_TOKENIZER_DIR')
if not SNAP:
    sys.exit('OP4B_TOKENIZER_DIR に、登録機種のトークナイザの置き場を渡す（実重みは要らない）')

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'endtoend-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

checks, fails = [], 0


def check(name, ok, detail):
    global fails
    checks.append({'name': name, 'ok': bool(ok), 'detail': str(detail)[:220]})
    if not ok:
        fails += 1
    print('  %-44s %s  %s' % (name, '通った' if ok else '**落ちた**', str(detail)[:90]))


# ---- 小さな模型（乱数で初期化・実重みではない） ----
tok = AutoTokenizer.from_pretrained(SNAP)
tok.padding_side = 'left'
cfg = AutoConfig.from_pretrained(SNAP)
cfg.num_hidden_layers = a.layers
cfg.hidden_size = a.hidden
cfg.intermediate_size = a.hidden * 2
cfg.num_attention_heads = max(2, a.hidden // 32)
cfg.num_key_value_heads = cfg.num_attention_heads
torch.manual_seed(11)
model = AutoModelForCausalLM.from_config(cfg)
# **float32 に明示で揃える**（2026-09-19）。実物の設定を読んで作ると設定の dtype（bf16）になる版があり、
# 「小さな模型は float32」を前提に置いた (8e) の期待が版によって変わった。小さな模型の数の照合（9g・9h）も float32 のほうが確か。
model = model.float()
model.eval()
n_layers = model.config.num_hidden_layers
ratios = T['selection']['candidates']['layers']
idxs = {r: direction_B.layer_index(r, n_layers) for r in ratios}
print('[endtoend_B] 小さな模型: 層 %d・隠れ次元 %d・層の添字 %s' % (n_layers, cfg.hidden_size, idxs))

AT = {k: v['text'] for k, v in RUN.arm_texts().items()}
scen, inst = RUN.scenario_and_instruction(T['scenarios'][0])
ids = steer_B.apply_chat(tok, RUN.user_message(AT['O'], scen['text'], inst))
inp = torch.tensor([ids])
am = torch.ones_like(inp)

# (1) 層の対応
try:
    d = direction_B.assert_layer_alignment(model, inp, am, idxs[ratios[0]])
    check('(1) hidden_states[idx+1] ＝ layers[idx] の出力', True, '最大差 %g' % d)
except AssertionError as e:
    check('(1) hidden_states[idx+1] ＝ layers[idx] の出力', False, e)

# ---- 方向を作る（抽出器と同じ経路で・小さな模型の活性から） ----
def act(arm, sc, ratio):
    s_, i_ = RUN.scenario_and_instruction(sc)
    t = torch.tensor([steer_B.apply_chat(tok, RUN.user_message(AT[arm], s_['text'], i_))])
    with torch.no_grad():
        o = model(input_ids=t, attention_mask=torch.ones_like(t), output_hidden_states=True)
    return o.hidden_states[direction_B.hidden_states_index(idxs[ratio])][0, -1, :].detach().float().numpy()


H = {(arm, sc, r): act(arm, sc, r) for arm in T['arms']['panel'] for sc in T['extraction_scenarios'] for r in ratios}
dirs, stats = direction_B.build_directions(H)
tmp = tempfile.mkdtemp(prefix='e2eB_')
npz = os.path.join(tmp, 'directions.npz')
np.savez(npz, **{'%s__%s' % (n, r): v for (n, r), v in dirs.items()})

# (6) ノルムが崩れた npz は読み込みで止まる
bad_npz = os.path.join(tmp, 'bad.npz')
bad = {('%s__%s' % (n, r)): (v * 2.0 if n == 'Nk' else v) for (n, r), v in dirs.items()}
np.savez(bad_npz, **bad)
try:
    RUN.load_directions(bad_npz)
    check('(6) ノルムの崩れた方向を読み込みで止める', False, '止まらなかった')
except SystemExit as e:
    check('(6) ノルムの崩れた方向を読み込みで止める', True, str(e)[:80])
loaded, _ = RUN.load_directions(npz)
check('(6b) 正しい方向は読める', len(loaded) == len(dirs), '%d 本' % len(loaded))

# (2)(3) hook の効き目
ratio = ratios[0]
li = idxs[ratio]
v = loaded[('static', ratio)]
gen = {'do_sample': False, 'max_new_tokens': 4}


def gen_once(coef, sign=+1):
    h = None
    if coef is not None:
        h = RUN.register_hook(model, li, RUN.make_hook(v, coef, sign, [inp.shape[1] - 1]))
    try:
        torch.manual_seed(5)
        with torch.no_grad():
            return model.generate(input_ids=inp, attention_mask=am, **gen)
    finally:
        if h is not None:
            h.remove()


base = gen_once(None)
zero = gen_once(0.0)
check('(2) 係数 0 の hook は結果を変えない', torch.equal(base, zero), '一致 %s' % bool(torch.equal(base, zero)))
big = gen_once(50.0)
check('(2b) 大きな係数は結果を変える', not torch.equal(base, big), '違う %s' % bool(not torch.equal(base, big)))

# (3) 加わる量を直に測る（prefill の主位置と復号の各段）
seen = {'prefill': None, 'decode': []}
ref = {}


def probe(module, inputs, output):
    hs = output[0] if isinstance(output, tuple) else output
    key = 'decode' if hs.shape[1] == 1 else 'prefill'
    if key == 'prefill':
        ref['prefill'] = hs.detach().clone()
    else:
        ref.setdefault('decode', []).append(hs.detach().clone())


h0 = direction_B.decoder_layers(model)[li].register_forward_hook(probe)
try:
    torch.manual_seed(5)
    with torch.no_grad():
        model.generate(input_ids=inp, attention_mask=am, **gen)
finally:
    h0.remove()

coef = 2.0
add = {'prefill': None, 'decode': []}


def probe2(module, inputs, output):
    hs = output[0] if isinstance(output, tuple) else output
    if hs.shape[1] == 1:
        add.setdefault('decode', []).append(hs.detach().clone())
    else:
        add['prefill'] = hs.detach().clone()


hk = RUN.make_hook(v, coef, +1, [inp.shape[1] - 1])
h1 = direction_B.decoder_layers(model)[li].register_forward_hook(hk)
h2 = direction_B.decoder_layers(model)[li].register_forward_hook(probe2)
try:
    torch.manual_seed(5)
    with torch.no_grad():
        model.generate(input_ids=inp, attention_mask=am, **gen)
finally:
    h1.remove(); h2.remove()

want = torch.as_tensor(v, dtype=ref['prefill'].dtype) * coef
d_last = float((add['prefill'][0, -1, :] - ref['prefill'][0, -1, :] - want).abs().max())
d_prev = float((add['prefill'][0, :-1, :] - ref['prefill'][0, :-1, :]).abs().max())
check('(3) prefill は主位置にだけ加わる', d_last < 1e-3 and d_prev < 1e-6,
      '主位置の差 %.3g・それ以外の差 %.3g' % (d_last, d_prev))
n_dec = len(add.get('decode', []))
check('(3b) 復号の各段に加わる', n_dec == gen['max_new_tokens'] - 1 or n_dec == gen['max_new_tokens'],
      '復号の段 %d 回' % n_dec)

# (4) hook が残らない
try:
    RUN.assert_no_hooks(model, li)
    check('(4) バッチの後に hook が零本', True, '零本')
except SystemExit as e:
    check('(4) バッチの後に hook が零本', False, e)

# (5) 腕が混ざったバッチは止まる
try:
    steer_B.assert_batch_uniform([AT['O'], AT['Onull']])
    check('(5) 腕が混ざったバッチを止める', False, '止まらなかった')
except SystemExit:
    check('(5) 腕が混ざったバッチを止める', True, '止まった')

# (7) 一つのセルを本当に走らせて、記録の欄がそろうか
LIDX = [idxs[r] for r in ratios]
try:
    rows = RUN.run_cell(model, tok, scenario=T['scenarios'][0], arm='Onull+v', layer_ratio=ratio, coef=1.0,
                        n=3, cell_seed_value=12345, tag=T['tags']['main'], run_key='e2e__test',
                        dirs=loaded, layer_idx=li, gen=gen, batch=2, resp_layer_idxs=LIDX)['trials']
    need = set(T['trial_record_fields']['fields'])
    got = set(rows[0]) if rows else set()
    check('(7) セルを走らせて記録の欄がそろう', len(rows) == 3 and need <= got,
          '%d 行・欠けた欄 %s' % (len(rows), sorted(need - got) or 'なし'))
except Exception as e:
    check('(7) セルを走らせて記録の欄がそろう', False, '%s: %s' % (type(e).__name__, e))

# (8) **走行器の出力を置き場に書き、本物の整合検査に通す**（裁定 D117・D127・2026-09-19）。
#     前は走行器が記録を書かず、走行器の出力は一度も集計の器に読まれていなかった。
#     さらに種の単位が走行器（バッチの種）と整合検査・合成データ（試行の種）で食い違っており、
#     **合成データは通り、本物の出力は全件落ちる**形になっていた。
import subprocess
root = os.path.join(tmp, 'runroot')
sc0 = T['scenarios'][0]
tag = T['tags']['main']
run_key = '%s__%s__s1__e2e' % (tag, sc0)
cells, raws_all, resp_all, n_cell, bt = [], [], {}, 5, 2          # 五試行・バッチ二（区切りを跨ぐ）
arms_run = ['Onull', 'Onull+v', 'Onull+vrand']
for arm in arms_run:
    cs = runs_B.cell_seed(T, T['seeds']['main'][sc0], 'main', (sc0, arm))
    o_ = RUN.run_cell(model, tok, scenario=sc0, arm=arm, layer_ratio=ratio, coef=1.0, n=n_cell,
                      cell_seed_value=cs, tag=tag, run_key=run_key, dirs=loaded, layer_idx=li, gen=gen, batch=bt, resp_layer_idxs=LIDX)
    cells += o_['trials']
    raws_all += o_['raws']
    resp_all.update(o_['resp'])
# 正本の欄をそろえた manifest（整合検査がこの一覧を読む）
T_b = dict(T)
man = {'tag': tag, 'run_key': run_key, 'session': 1, 'n': n_cell, 'seed': T['seeds']['main'][sc0],
       'batch': T['runner']['batch'], 'padding': 'left', 'model': 'e2e/random-init', 'model_rev': 'E2E',
       'tokenizer_rev': 'E2E', 'runner_sha': runs_B.sha16_file(os.path.join(HERE, 'run_stageB_local.py')),
       'pip_freeze_sha16': 'E2E', 'gpu': 'cpu', 'started': 'e2e', 'ended': 'e2e', 'dry_run': True,
       'scenario': sc0, 'arms': arms_run, 'layer': ratio, 'coef': 1.0, 'direction_ids': ['fixed', 'static', 'rand'],
       'dtype': str(next(model.parameters()).dtype).replace('torch.', ''), 'order': T['runner']['order_id'],
       'transformers_version': __import__('transformers').__version__, 'refuse_rules_sha16': runs_B.sha16_file(RUN.REFUSE_RULES)}
try:
    RUN.write_cell(root, tag, run_key, man, cells, raws_all, resp_all)
    RUN.write_session(root, tag, 1, [run_key], {'gpu': 'cpu'})
    check('(8a) 走行器が記録とセッション記録を置き場に書く', os.path.exists(os.path.join(root, tag, run_key, 'manifest.json')),
          '%d 行を書いた' % len(cells))
except SystemExit as e:
    check('(8a) 走行器が記録とセッション記録を置き場に書く', False, e)
# 上書きしないこと
try:
    RUN.write_cell(root, tag, run_key, man, cells)
    check('(8b) 既にある記録に上書きしない', False, '上書きした')
except SystemExit:
    check('(8b) 既にある記録に上書きしない', True, '止まった')
# 読み口が読めるか
cc = runs_B.counts_main(T, root=root, allow_dry=True)[0]
check('(8c) 読み口（runs_B）が走行器の出力を読める', sum(c['n'] for c in cc.values()) == len(cells),
      '読んだ試行 %d／書いた試行 %d' % (sum(c['n'] for c in cc.values()), len(cells)))
# **本物の整合検査に通す**（種は「バッチの種」で組み直して照合される）
p = subprocess.run([sys.executable, os.path.join(HERE, 'integrity_B.py'), '--tag', tag, '--root', root, '--allow-dry',
                    '--out', os.path.join(tmp, 'i.md'), '--force'], capture_output=True, text=True, encoding='utf-8', cwd=REPO)
ij = os.path.join(tmp, 'i.json')
probs = json.load(open(ij, encoding='utf-8')).get('problems', []) if os.path.exists(ij) else ['記録が読めない']
seed_probs = [x for x in probs if 'seed' in x]
check('(8d) 走行器の種が整合検査の組み直しと一致する（裁定 D127）', not seed_probs,
      ('種の不整合 %d 件' % len(seed_probs)) if seed_probs else '種の不整合 零')
# この検査は**速さのために四点を登録から外している**——貪欲の生成・セルの試行数（本走行の n より小さい）・
# 走らせるセルの数（登録の升目の一部だけ）・模型の dtype（小さな模型は float32）。
# 整合検査は**その四点を捕まえるべき**であり（眠っていないことの確かめ）、**それ以外は零であるべき**である。
_expected = ('生成の設定が登録と違う', '連番でない', '登録の升目', 'dtype')
caught = [x for x in probs if 'seed' not in x and any(e in x for e in _expected)]
other = [x for x in probs if 'seed' not in x and not any(e in x for e in _expected)]
check('(8e) 検査のために登録から外した四点を、整合検査が捕まえる',
      all(any(e in x for x in caught) for e in _expected),
      '捕まえた %d 件（%s）' % (len(caught), '・'.join(e for e in _expected if any(e in x for x in caught))))
check('(8e2) それ以外の不整合は零', not other, ('%d 件: %s' % (len(other), other[:2])) if other else '零')
# 再開: 途中から走らせ直しても、同じ試行は同じ種を持つ
cs = runs_B.cell_seed(T, T['seeds']['main'][sc0], 'main', (sc0, 'Onull'))
full = RUN.run_cell(model, tok, scenario=sc0, arm='Onull', layer_ratio=ratio, coef=1.0, n=n_cell,
                    cell_seed_value=cs, tag=tag, run_key='r', dirs=loaded, layer_idx=li, gen=gen, batch=bt, resp_layer_idxs=LIDX)['trials']
part = RUN.run_cell(model, tok, scenario=sc0, arm='Onull', layer_ratio=ratio, coef=1.0, n=n_cell,
                    cell_seed_value=cs, tag=tag, run_key='r', dirs=loaded, layer_idx=li, gen=gen, batch=bt, start=3, resp_layer_idxs=LIDX)['trials']
same = all(a_['seed'] == b_['seed'] for a_, b_ in zip(full[3:], part))
check('(8f) 途中から再開しても同じ試行は同じ種を持つ', same and len(part) == n_cell - 3,
      '再開 %d 行・種の一致 %s' % (len(part), same))

# (9) **すべての種類の腕**（v2・2026-09-19）。反証の場面にはすべての種類の腕がそろう。
sc4 = T['falsification_scenario']
kinds = {'Osec-Ncold': None, 'Onull+v': 'static', 'O-Ncold-v': 'static', 'Onull+vrand': 'random', 'O-Ncold+vNk': 'Nk',
         'O-Ncold-vtd': 'td', 'Osec-Ncold+v6b': 'loaded'}
outs, errs = {}, []
for arm in kinds:
    try:
        outs[arm] = RUN.run_cell(model, tok, scenario=sc4, arm=arm, layer_ratio=ratio, coef=1.0, n=n_cell,
                                 cell_seed_value=runs_B.cell_seed(T, T['seeds']['main'][sc4], 'main', (sc4, arm)),
                                 tag=tag, run_key='e2e__s4', dirs=loaded, layer_idx=li, gen=gen, batch=bt, resp_layer_idxs=LIDX)
    except BaseException as e:
        errs.append('%s: %s' % (arm, str(e)[:80]))
check('(9a) すべての種類の腕が走る（無操作・静的・ランダム・Nk・td・(6b)）', not errs and all(len(o['trials']) == n_cell for o in outs.values()),
      ('止まった腕: %s' % errs) if errs else '腕 %d 種・各 %d 試行' % (len(outs), n_cell))
if 'Onull+vrand' in outs:
    got_ids = [t_['direction_id'] for t_ in outs['Onull+vrand']['trials']]
    want_ids = ['rand:%d' % steer_B.direction_of(t_['trial_index'], n_cell) for t_ in outs['Onull+vrand']['trials']]
    check('(9b) ランダム方向の腕は試行ごとに登録順の等分で方向を持つ', got_ids == want_ids and len(set(got_ids)) > 1,
          '記録 %s／登録の割り当て %s' % (got_ids, want_ids))
    V_, D_ = RUN.row_vectors(RUN.arm_plan('Onull+vrand'), loaded, ratio, list(range(n_cell)), n_cell, 'main')
    R_ = steer_B.random_directions(loaded[('static', ratio)], 'main', ratio)
    ok_v = all(np.allclose(V_[i], R_[steer_B.direction_of(i, n_cell)]) for i in range(n_cell))
    check('(9b2) 行ごとの方向は、その試行に割り当てた方向そのもの', ok_v, '行ごとの一致 %s' % ok_v)
# hook の中身の照合: 別の層に残った hook があれば、走らせる前に止まる
_stray = direction_B.decoder_layers(model)[(li + 1) % n_layers].register_forward_hook(lambda m, i, o: o)
try:
    RUN.run_cell(model, tok, scenario=sc4, arm='Onull+v', layer_ratio=ratio, coef=1.0, n=2, cell_seed_value=1, tag=tag,
                 run_key='e2e__stray', dirs=loaded, layer_idx=li, gen=gen, batch=bt, resp_layer_idxs=LIDX)
    check('(9c) 掛けるべきでない層の hook を見つけて止まる（裁定 D122）', False, '止まらなかった')
except SystemExit as e:
    check('(9c) 掛けるべきでない層の hook を見つけて止まる（裁定 D122）', 'hook' in str(e), str(e)[:80])
finally:
    _stray.remove()
# 様式・言及・refuse の分類・ループ・打ち切り: 生テキストの最終試行を、段階 A の凍結した関数で**別に**採点し直して照らす
import response_mode_A as _RMA
TF_ = RUN.frozen_text_funcs()
s4s, s4i = RUN.scenario_and_instruction(sc4)
bad_mode = []
for arm, o in outs.items():
    at_ = RUN.arm_texts()[RUN.base_arm_of(arm)]['text']
    sent_ = ('', at_, s4s['text'], s4i)
    for t_, r_ in zip(o['trials'], o['raws']):
        mf = _RMA.measure(r_['final'], tuple(_RMA._norm(x) for x in sent_))
        lp_ = TF_['loop_info'](r_['final'])
        want_ = {'style_a': bool(mf['a']), 'style_b': bool(mf['b']), 'mention': bool(mf['c1']), 'loop_flag': bool(lp_['fired']),
                 'truncated': r_['finish'] == 'length'}
        if any(t_[k_] != v_ for k_, v_ in want_.items()) or t_['refuse_class'] is None:
            bad_mode.append((t_['trial_id'], {k_: (t_[k_], v_) for k_, v_ in want_.items() if t_[k_] != v_}))
check('(9d) 様式・言及・ループ・打ち切りが段階 A の関数の採点と一致し、refuse の分類が空でない', not bad_mode,
      ('食い違い %d 件: %s' % (len(bad_mode), bad_mode[:1])) if bad_mode else '試行 %d 件すべて一致' % sum(len(o['trials']) for o in outs.values()))
# 生テキスト: 置き場に書かれ、試行と行が対応する
rawp = os.path.join(root, tag, run_key, 'raw-%s.jsonl' % run_key)
rraw = [json.loads(l) for l in open(rawp, encoding='utf-8')] if os.path.exists(rawp) else []
check('(9e) 生テキストが置き場に書かれ、試行と行が対応する', len(rraw) == len(cells) and all(r_.get('text') is not None and r_['trial_id'] == c_['trial_id']
                                                                   for r_, c_ in zip(rraw, cells)),
      '生テキストの行 %d／試行 %d・引き直しの印 %d 件' % (len(rraw), len(cells), sum('===RETRY===' in (r_.get('text') or '') for r_ in rraw)))
# 副位置の活性: 置き場の npz・形・有限・小分けと一行ずつの一致・手で組んだ計算との一致
rp = os.path.join(root, tag, run_key, 'resp-%s.npz' % run_key)
zr = np.load(rp) if os.path.exists(rp) else None
with_path = [c_ for c_ in cells if c_.get('resp_mean_path')]
ok_shape = zr is not None and all(zr[c_['resp_mean_path'].split('#')[1]].shape == (len(ratios), cfg.hidden_size) and
                                  np.isfinite(zr[c_['resp_mean_path'].split('#')[1]].astype(np.float32)).all() for c_ in with_path)
check('(9f) 副位置の活性が置き場に書かれる（候補の層 × 隠れ次元・有限）', bool(with_path) and ok_shape,
      '活性を持つ試行 %d／%d' % (len(with_path), len(cells)))
resp_ids = [tok(r_['final'], add_special_tokens=False)['input_ids'][:6] or [0] for r_ in raws_all[:4]]
_hv = np.stack([loaded[('static', ratio)]] * len(resp_ids))
h_args = {'layer_idx': li, 'vecs': _hv, 'coef': 1.0, 'sign': +1}
m4 = RUN.capture_resp_mean(model, ids, resp_ids, LIDX, h_args, rows=4)
m1 = RUN.capture_resp_mean(model, ids, resp_ids, LIDX, h_args, rows=1)
d41 = max(float(np.abs(a_.astype(np.float32) - b_.astype(np.float32)).max()) for a_, b_ in zip(m4, m1))
check('(9g) 副位置の活性は、左詰めの小分けと一行ずつで一致する（位置の番号の扱い）', d41 < 1e-2, '最大差 %.3g（fp16 の丸めの内）' % d41)
# 手で組む: 列をつなぎ、hook を掛けて順伝播し、応答の位置の平均を取る（器を通さない計算）
_seq = torch.tensor([list(ids) + list(resp_ids[0])])
_h = RUN.register_hook(model, li, RUN.make_hook(loaded[('static', ratio)], 1.0, +1, [len(ids) - 1]))
try:
    with torch.no_grad():
        _o = model(input_ids=_seq, attention_mask=torch.ones_like(_seq), output_hidden_states=True)
finally:
    _h.remove()
_man = np.stack([_o.hidden_states[k_ + 1][0, len(ids):, :].float().mean(0).numpy() for k_ in LIDX])
d_man = float(np.abs(_man - m1[0].astype(np.float32)).max())
check('(9h) 副位置の活性は、手で組んだ計算と一致する', d_man < 1e-2, '最大差 %.3g' % d_man)

shutil.rmtree(tmp, ignore_errors=True)

json.dump({'kind': 'endtoend_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'model': {'layers': n_layers, 'hidden': cfg.hidden_size, 'random_init': True},
           'checks': checks, 'failed': fails, 'total': len(checks)},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B **端から端まで**の検査（小さな模型・機械生成・`tools/endtoend_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 裁定 D117: 走行器と抽出器の本体を書き、**小さな模型で端から端まで通す**。',
     '- 模型は**乱数で初期化**した小さな Qwen3 形（層 %d・隠れ次元 %d）。**実重みではない**——率にも活性にも意味は無い。' % (n_layers, cfg.hidden_size),
     '- トークナイザだけは**登録機種の現物**を使う（`OP4B_TOKENIZER_DIR`）。',
     '- **%d 件のうち落ちた検査は %d 件。**' % (len(checks), fails), '',
     '| 確かめたこと | 結果 | 中身 |', '|---|---|---|']
for c in checks:
    L.append('| %s | %s | %s |' % (c['name'], '通った' if c['ok'] else '**落ちた**', c['detail']))
L += ['', '## この検査が確認していないこと', '',
      '- **実重み（Qwen3-4B-Instruct-2507）では一行も走らせていない。**模型は乱数の初期化である。',
      '- したがって**破局率も活性のノルムも、この検査からは何も言えない**。',
      '- バッチ 16・実重み・実際のメモリでの挙動（OOM・KV キャッシュ・速度）は確かめていない。',
      '- 品質床の走行は含まない（課題が未定・裁定 D66）。',
      '- **相をまたいだ走らせ方の順**（同一性選別 → 調整走行 → 品質床 → 本走行）と、Colab での起動は、'
      '  まだ書いていない（一つのセルを走らせて書く口と、セッション記録を書く口までは書いた）。',
      '- 様式と言及の照らし合わせ（9d）は、走行器と同じ段階 A の関数で採点し直したもので、**関数そのものの正しさ**は段階 A の検分と走行器の自己検査（見本の文）に拠る。',
      '- 乱数の模型の出力はほぼすべて書式外になるので、**答えの読める試行（破局・refuse の判定）の経路は、ここでは走らない**（走行器の自己検査の見本の文で確かめた）。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[endtoend_B] %s | %d 件中 落ちた検査 %d 件' % (os.path.relpath(out_md, REPO), len(checks), fails))
sys.exit(1 if fails else 0)
```
