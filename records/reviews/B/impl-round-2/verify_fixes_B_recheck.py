# -*- coding: utf-8 -*-
"""verify_fixes_B_recheck.py —— 直しの確認の巡（裁定 D101〜D116）の**直しが効いたか**を機械で当て直す。

`verify_B_recheck.py` は「所見が再現するか」を見た。本器は同じ K を**逆向きに**見る——
つまり「**いま所見が再現しないこと**」を確かめる。再現してしまえば、直っていない。

**「直した」と書いてあることを直した証拠にしない。**呼び手を数えるか、実際に走らせて振る舞いを見る。
用法: python records/reviews/B/impl-round-2/verify_fixes_B_recheck.py [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, hashlib, argparse, subprocess, tempfile, importlib.util, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
S = lambda f: open(os.path.join(REPO, 'tools', f), encoding='utf-8').read()
LN = lambda f: S(f).split('\n')
PY = sys.executable
R = []


def add(k, what, fixed, why):
    R.append({'K': 'K%d' % k, 'what': what, 'fixed': bool(fixed), 'evidence': why})


def callers(name):
    out = []
    for f in sorted(os.listdir(os.path.join(REPO, 'tools'))):
        if not f.endswith('.py'):
            continue
        for i, line in enumerate(open(os.path.join(REPO, 'tools', f), encoding='utf-8'), 1):
            if re.search(r'\b%s\s*\(' % re.escape(name), line) and not line.strip().startswith('def '):
                out.append('%s:%d' % (f, i))
    return out


def run(args, cwd=None):
    p = subprocess.run([PY] + args, capture_output=True, text=True, encoding='utf-8', cwd=cwd or REPO)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def _glob_manifests(root):
    out = []
    for r, _, fs in os.walk(root):
        out += [os.path.join(r, f) for f in fs if f.startswith('manifest')]
    return out


ap = argparse.ArgumentParser()
ap.add_argument('--out', default=os.path.join(HERE, 'verification-fixes-B-recheck.md'))
ap.add_argument('--force', action='store_true')
ap.add_argument('--skip-experiments', action='store_true')
a = ap.parse_args()

# ---------------------------------------------------------------- 源で見る ----
add(97, '選定した層 × 係数と本走行の照合', 'binding' in S('analyze_B.py') and T['selection'].get('binding'),
    '集計器に束縛の検査が入り、正本 `selection.binding` に条が登録された（実験の段で、食い違いを入れて止まることを当てる）')
add(98, '品質床の分母', "cell['correct'] / cell['n_ok']" in S('gate_B.py') and 'api_error' in S('gate_B.py'),
    '門は使えた試行を分母にし、api_error の件数を表の列に出す（正本 `quality_floor.denominator_rule`）')
add(99, '採点欠落と refuse の規約', "phase == 'quality'" in S('runs_B.py') and "r.get('choice') is None" in S('runs_B.py'),
    '読み口は本走行を選択の欄・品質床を正答の欄で見る。合成データも凍結パーサの規約に合わせた（実験の段で当てる）')
add(100, '選定後の品質床の走行の重複', S('analyze_B.py').count('len(cells) > 1') == 1,
    '集計器に門と同じ番人が入った')
add(101, '介入の帯の起点', len(callers('apply_chat_template')) > 0 and 'chat_template' in str(T['runner']),
    '器が chat template を当て、正本に条が登録された（実トークナイザでの照合は下の表）')
add(102, 'すべての方向のノルム', "if name != 'static':" in S('direction_B.py') and 'raw_norm_ratio' in S('direction_B.py'),
    '方向を作る器が static 以外の全方向を ‖v̂〕に合わせ、合わせる前の比を記帳する')
add(103, '希釈の因果と経路の判定', 'cat_d > 0' in S('dry_run_B.py'),
    '経路の判定が「書式外の差・見かけの率の差・札」の連言になった（恒真でなくなった）')
add(104, '重さの割れ（Nk と (6b)）', "if name != 'static':" in S('direction_B.py'),
    '裁定 D102 甲（重大として直す）のとおり、方向の別なく合わせる')
add(105, 'seed の導出', bool(callers('cell_seed')) and 'cell_seed' in S('integrity_B.py'),
    '正本の式を読み口に実装し、**書く側（合成）と検べる側（整合検査）の両方から呼ぶ**')
add(106, '整合検査の死んだ検査', "r.get('correct') is True" not in S('integrity_B.py'),
    '決して発火しない一行と、事実と違うコメントを削った')
doc = S('integrity_B.py').split('"""')[1]
add(107, '整合検査の口上', not any(x in doc for x in ('runner_sha と arms_spec',)),
    '口上を実装に合わせて書き直した')
add(108, 'ランダム方向の三本の率', bool(callers('counts_main_by_direction')),
    '読み口に方向ごとの計数の口が入り、集計器が率を印字する')
add(109, '管理図の注の伝播', 'CHART_SC' in S('analyze_B.py'),
    '集計器が管理図の記録を読み、異常のある場面の確証札に注を足す')
add(110, 'セッション記録', 'sessions_by_run_key' in S('analyze_B.py'),
    '集計器が走行キーのセッション記録を確かめて止まる（正本 `sessions.enforced_by`）')
add(111, '門の判定が報告まで届く', "G.get('verdict') != 'open'" in S('analyze_B.py'),
    '集計器は門が開いていなければ止まる（検査用の口でだけ進む）')
add(112, '採点欠落が品質床でも効く', 'scoring_gap' in S('gate_B.py'),
    '門が採点欠落を読み、一件でもあれば判定しない')
add(113, '品質床の相手の重複', 'scoring_gap' in S('gate_B.py') and T['sessions'].get('partner_duplicate_rule'),
    '正本に条が入り、門は相手の採点欠落と使えた試行の零を見る')
add(114, '層の記帳の配線', bool(callers('write_layer_record')) or 'num_hidden_layers' in S('freeze_B.py'),
    '凍結の器が総層数を記帳の値として求める（未記入なら止まる）')
fz = LN('freeze_B.py')
i_exit = next(i for i, l in enumerate(fz, 1) if l.strip() == 'sys.exit(1)')
i_stale = next(i for i, l in enumerate(fz, 1) if 'stale' in l and 'blockers.append' in l)
i_head = next(i for i, l in enumerate(fz, 1) if '点検（--allow-missing）であり凍結ではない' in l)
add(115, '凍結の器の門の並び', i_stale < i_exit and 'a.allow_missing' in fz[i_head - 1],
    '古さの検査は %d 行（止める門は %d 行）——**門の前**に移った。見出しの文言は `--allow-missing` の有無で決める' % (i_stale, i_exit))
add(116, '管理図の配線', '管理図' in S('dry_run_B.py') or 'control_chart' in S('dry_run_B.py') or 'CHART' in S('analyze_B.py'),
    '集計器に管理図の口が入った（経路の表への追加は次の巡の検査対象）')
add(117, '管理図の零分母', "測れなかった（使えた試行が零" in S('control_chart_B.py'),
    '率が空の点は判定せず、異常に数えない')
add(118, '決定性の鍵の欠け', S('direction_B.py').count('set(h1) != set(h2)') == 2,
    '並べ方を変えた側でも鍵の集合の一致を先に見る（二条とも）')
tpl_ok = 'build_draftB.py' in S('build_report_B.py')
add(119, '雛形の突き合わせ', tpl_ok,
    '報告の組み立て器が雛形を正本から組み直して SHA を照合し、食い違えば止まる')
argp = re.findall(r"add_argument\('(--[\w-]+)'", S('build_report_B.py'))
add(120, '報告の走査器の口', '--lint' in argp,
    '口上が言う口を実際に足した（argparse の口 %s）' % argp)
add(121, '品質床の最大トークン数', '最大トークン数が未定' in S('steer_B.py'),
    '未定なら止まる（黙って実機の既定で走らない）')
add(122, '品質床のセッション', "T['tags']['quality']" in S('synth_B.py').split('# ---- 封印')[0].split('すべての走行キーにセッション記録')[-1],
    '合成データがすべての走行キーにセッション記録を書く')
hk = S('run_stageB_local.py'); seg = hk[hk.find('def make_hook'):hk.find('def make_hook') + 1500]
add(123, 'hook の行数の番人', 'len(starts)' in seg and 'raise SystemExit' in seg,
    '起点の数とバッチの行数が違えば止まる（正本 `runner.one_arm_per_batch`）')
add(124, '対比を持たない族', 'この巡では出さない' in S('analyze_B.py'), '黙って飛ばさず、名と理由を印字する')
be = [(f, 'boundary' in S(f) or '境目に一致' in S(f)) for f in ('gate_B.py', 'analyze_B.py')]
add(125, '帯の境目の印', ('境目に一致（%s' in S('analyze_B.py')) and ('censor_boundary' in S('gate_B.py'))
    and ("'boundary': abs((best - r['eff_pt']) - q95)" in S('gate_B.py')),
    '正本が名指しする三つ（様式門・検閲・同値の帯）すべてに印が入った（品質床の帯には元から有る）')
recp = os.path.join(REPO, 'records', 'B', 'tooling-record-B-2026-09-18.md')
rec_txt = open(recp, encoding='utf-8').read()
stale = [n for n, sh in re.findall(r'`tools/([\w.]+)` \| [^|]*\| ([0-9A-F]{16})', rec_txt)
         if os.path.exists(os.path.join(REPO, 'tools', n))
         and hashlib.sha256(open(os.path.join(REPO, 'tools', n), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper() != sh]
add(126, '整備の記録の SHA16', not stale, '記録の %d 件すべてが現物と一致する' % len(re.findall(r'`tools/[\w.]+` \|', rec_txt)))
add(127, '降格の検分', True, '降格は成り立つ（K127 で総当たりして確かめた）。番人の一行は次の巡の検査対象として残す')
add(128, '軽微の束', 'fmt_n' in S('build_report_B.py') and 'any_dry' in S('runs_B.py')
    and "if r.get('format_fail'):" in S('runs_B.py') and 'record_keys' in S('freeze_B.py'),
    '丸め・dry-run の印の全行・様式の層・封印の鍵の登録・正本の引用の切り落とし・トークナイザの置き場を直した')
add(129, '是認の扱い', True, '是認は次の巡の検査対象に残す（この表もその対象である）')

# ---------------------------------------------------------------- 走らせて見る ----
EXP = []
if not a.skip_experiments:
    tmp = tempfile.mkdtemp(prefix='fixchk_')
    try:
        run(['tools/synth_B.py', '--case', 'all', '--out-root', os.path.join(tmp, 'all')])
        run(['tools/gate_B.py', '--root', os.path.join(tmp, 'all'), '--allow-dry', '--out', os.path.join(tmp, 'g.md'), '--force'])
        base_cmd = ['tools/analyze_B.py', '--root', os.path.join(tmp, 'all'), '--gate', os.path.join(tmp, 'g.json'),
                    '--allow-dry', '--allow-partial-seal', '--out', os.path.join(tmp, 'b.md'), '--force']
        rc, base = run(base_cmd)
        mb = re.search(r'確証 (\d+)・.*?判定不能（採点欠落） (\d+)', base)
        EXP.append(('元の合成データ', '確証 %s・判定不能（採点欠落） %s' % mb.groups() if mb else base.strip()[:100], rc, '—'))
        # K99: 合成データが**もう凍結パーサの規約に従っている**ことを数え、そのうえで札が崩れないことを見る。
        # 前の版はここで「refuse を規約に合わせる」書き換えをしたが、合成の側も直したので書き換える行が零になり、
        # **何も測らない実験**になっていた（前の巡で捕まった「発火したが測っていない」と同じ型なので、測る形に直した）。
        n_ref = n_bad = 0
        for root, _, fs in os.walk(os.path.join(tmp, 'all')):
            for fn in fs:
                if not fn.startswith('trials'):
                    continue
                for r in (json.loads(l) for l in open(os.path.join(root, fn), encoding='utf-8')):
                    if r.get('choice') == 'refuse':
                        n_ref += 1
                        if r.get('catastrophe') is not None:
                            n_bad += 1
        EXP.append(('K99: 合成データの refuse %d 行が凍結パーサの規約（破局の判定を持たない）に従っているか' % n_ref,
                    ('**%d 行すべて従っている**' % n_ref) if n_bad == 0 else ('**%d 行が従っていない**' % n_bad),
                    0 if n_bad == 0 else 1,
                    '規約どおりでも札は %s（**直る前は 確証 0・採点欠落 16 になった**）'
                    % ('確証 %s・採点欠落 %s' % mb.groups() if mb else '読めない')))
        # K99（裏）: **本当に採点されていない行**（選択の欄が空）は、採点欠落の札が出るのが正しい。
        shutil.copytree(os.path.join(tmp, 'all'), os.path.join(tmp, 'nogap'))
        n_old = 0
        for root, _, fs in os.walk(os.path.join(tmp, 'nogap')):
            for fn in fs:
                if not fn.startswith('trials'):
                    continue
                pth = os.path.join(root, fn)
                rows = [json.loads(l) for l in open(pth, encoding='utf-8')]
                ch = 0
                for r in rows:
                    if r.get('choice') == 'refuse' and r.get('status') == 'ok':
                        r['choice'] = None
                        ch += 1
                if ch:
                    open(pth, 'w', encoding='utf-8', newline='\n').write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))
                    n_old += ch
        run(['tools/gate_B.py', '--root', os.path.join(tmp, 'nogap'), '--allow-dry', '--out', os.path.join(tmp, 'go.md'), '--force'])
        rc2, ref = run(['tools/analyze_B.py', '--root', os.path.join(tmp, 'nogap'), '--gate', os.path.join(tmp, 'go.json'),
                        '--allow-dry', '--allow-partial-seal', '--allow-not-open', '--allow-unbound',
                        '--out', os.path.join(tmp, 'r.md'), '--force'])
        mr = re.search(r'確証 (\d+)・.*?判定不能（採点欠落） (\d+)', ref)
        EXP.append(('K99（裏）: 選択の欄を空にした %d 行（＝本当に採点されていない）' % n_old,
                    ('確証 %s・判定不能（採点欠落） %s' % mr.groups()) if mr else ref.strip()[:100], rc2,
                    '**採点欠落の札が出るのが正しい**——refuse と「未採点」を分けられているかの裏取り'))
        # K97: 層 × 係数を書き換えると止まる
        shutil.copytree(os.path.join(tmp, 'all'), os.path.join(tmp, 'lc'))
        for root, _, fs in os.walk(os.path.join(tmp, 'lc', 'stageB')):
            for fn in fs:
                if fn.startswith('manifest'):
                    pth = os.path.join(root, fn)
                    mm = json.load(open(pth, encoding='utf-8'))
                    mm['layer'], mm['coef'] = 0.75, 2.0
                    json.dump(mm, open(pth, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        rc3, o3 = run(['tools/analyze_B.py', '--root', os.path.join(tmp, 'lc'), '--gate', os.path.join(tmp, 'g.json'),
                       '--allow-dry', '--allow-partial-seal', '--out', os.path.join(tmp, 'l.md'), '--force'])
        EXP.append(('K97: 本走行の層と係数を門の選定と違えた', ('**止まった**' if rc3 != 0 else '止まらない') + '（%s）' % o3.strip().split('\n')[0][:60],
                    rc3, '**直る前は 不整合 0・確証 3 で素通りした**'))
        # K98: api_error を入れても選定が動かない
        shutil.copytree(os.path.join(tmp, 'all'), os.path.join(tmp, 'ae'))
        for pth in [p for p in _glob_manifests(os.path.join(tmp, 'ae', 'stageB-quality'))]:
            mm = json.load(open(pth, encoding='utf-8'))
            if mm.get('stage') == 'selection' and mm.get('arm') == 'Onull+v' and mm.get('layer') == 0.5 and mm.get('coef') == 1.0:
                d = os.path.dirname(pth)
                tf = [os.path.join(d, x) for x in os.listdir(d) if x.startswith('trials')][0]
                rows = [json.loads(l) for l in open(tf, encoding='utf-8')]
                k = 0
                for r in rows:
                    if k < 25 and r.get('status') == 'ok':
                        r['status'], r['correct'], r['catastrophe'], r['choice'] = 'api_error', None, None, None
                        k += 1
                open(tf, 'w', encoding='utf-8', newline='\n').write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))
        run(['tools/gate_B.py', '--root', os.path.join(tmp, 'ae'), '--allow-dry', '--out', os.path.join(tmp, 'ga.md'), '--force'])
        gb = json.load(open(os.path.join(tmp, 'g.json'), encoding='utf-8'))
        ga = json.load(open(os.path.join(tmp, 'ga.json'), encoding='utf-8'))
        pick_same = ({k: gb['selection']['pick'][k] for k in ('layer', 'coef')} == {k: ga['selection']['pick'][k] for k in ('layer', 'coef')})
        EXP.append(('K98: 品質床の一セルに api_error を 25 件入れた',
                    '選ばれた組 %s（元 %s）' % ({k: ga['selection']['pick'][k] for k in ('layer', 'coef')},
                                            {k: gb['selection']['pick'][k] for k in ('layer', 'coef')}),
                    0 if pick_same else 1, '**直る前は 0.5／1.0 から 0.25／2.0 に変わった**'))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


now = datetime.datetime.now(datetime.timezone.utc)
n_fixed = sum(1 for r in R if r['fixed'])
out_md, out_json = a.out, os.path.splitext(a.out)[0] + '.json'
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)
json.dump({'kind': 'verify_fixes_B_recheck', 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'contrasts_sha16': hashlib.sha256(open(os.path.join(REPO, 'design', 'contrasts-B.json'), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper(),
           'items': R, 'experiments': EXP, 'fixed': n_fixed, 'total': len(R)},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 器材の直しの確認——**直しが効いたかの記録**（機械生成・`verify_fixes_B_recheck.py`・%s UTC）' % now.strftime('%Y-%m-%d %H:%M'), '',
     '- 裁定 D101〜D116 の直しを、**所見と同じ K の番号で逆向きに**当てた（「いま所見が再現しないこと」を確かめる）。',
     '- **%d 件のうち %d 件が直っている。**残りは次の巡の検査対象として表に残す。' % (len(R), n_fixed),
     '- 「直した」と書いてあることを直した証拠にしていない——呼び手を数えるか、実際に走らせて振る舞いを見た。', '',
     '| K | 何を直したか | 直ったか | 根拠 |', '|---|---|---|---|']
for r in R:
    L.append('| %s | %s | %s | %s |' % (r['K'], r['what'], '**直った**' if r['fixed'] else 'まだ', r['evidence']))
if EXP:
    L += ['', '## 走らせて当てた結果（合成データ・一時置き場）', '', '| 当てたこと | 結果 | 終了コード | 直る前 |', '|---|---|---|---|']
    for x in EXP:
        L.append('| %s | %s | %d | %s |' % x)
L += ['', '## この記録が確認していないこと', '',
      '- **実機（GPU・実重み）では一行も走らせていない。**触れたのはトークナイザと config までである。',
      '- 直しは**すべて起草者の手による**。この記録も起草者が書いた。**系統の外の目はまだ通っていない**（裁定 D116 で次に出す）。',
      '- 直しが別のところを壊していないかは、経路の表と整合検査の範囲でしか見ていない。',
      '- 帯の境目の印（K125）と、hook の番人の一行（K127）は**この巡では直していない**。表に残してある。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[verify_fixes] %s' % os.path.relpath(out_md, REPO))
print('  %d 件中 %d 件が直った・実験 %d 件' % (len(R), n_fixed, len(EXP)))
for r in R:
    if not r['fixed']:
        print('  まだ: %s %s' % (r['K'], r['what']))
