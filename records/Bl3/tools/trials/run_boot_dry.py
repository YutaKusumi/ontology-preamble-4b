# -*- coding: utf-8 -*-
"""起動器 `tools/colab/boot_Bl3.py` の DRY（乱数の小さな模型・CPU）を、相 check → pilot → main（三つの組）の順に走らせ、手元の集計の器の一致だけを見る段 →
結果を開く段 → 掃き出し → 報告の組み立て → 走査まで通す（合成だけ・値は印字しない・起動器と集計の器と報告の器の往復の形の確かめ）。
出力の置き場（一時）: 引数の置き場。記録に残すのは、相ごとの進みの印字と session と、一致だけを見る段の記録と、この走りのまとめ（boot-dry-<n>/）。
用法: python records/Bl3/tools/trials/run_boot_dry.py <一時の置き場> <記録の置き場（records/Bl3/tools/trials/boot-dry-<n>）>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, glob, shutil, hashlib, subprocess, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
OUT, REC = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
assert not os.path.exists(REC), '既にある: ' + REC
os.makedirs(OUT, exist_ok=True)
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
env = dict(os.environ, OP4B_DRY='1', OP4B_REPO_DIR=REPO, OP4B_OUT=OUT, OP4B_DRY_ISO='9', OP4B_DRY_SEC='2', OP4B_DRY_RC='2', PYTHONIOENCODING='utf-8')
steps = []


def run(cmd, extra=None):
    e = dict(env, **(extra or {}))
    r = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO, env=e)
    steps.append({'cmd': ' '.join(cmd), 'env': {k: v for k, v in (extra or {}).items()}, 'returncode': r.returncode, 'stdout_tail': r.stdout[-1500:], 'stderr_tail': r.stderr[-1500:]})
    print('[run_boot_dry] %s → %d' % (' '.join(cmd + ['%s=%s' % kv for kv in (extra or {}).items()]), r.returncode), flush=True)
    if r.returncode != 0:
        print(r.stdout[-3000:]); print(r.stderr[-3000:])
        raise SystemExit('止まった: %s' % cmd)
    return r


def newest(prefix):
    ds = [d for d in sorted(glob.glob(os.path.join(OUT, prefix + '-*'))) if os.path.isdir(d)]
    return ds[-1]


run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'check'})
dc = newest('check')
run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'pilot'})
dp = newest('pilot')
pj = os.path.join(dp, 'pilot.json')
run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'main', 'OP4B_DRY_PILOT': pj})
dm = newest('main')
judge = os.path.join(OUT, 'judge.json')
opened = os.path.join(OUT, 'analysis.json')
run(['tools/analyze_Bl3.py', 'judge', dm, '--pilot', pj, '--out', judge])
run(['tools/analyze_Bl3.py', 'open', dm, '--pilot', pj, '--judge-record', judge, '--out', opened])
run(['tools/sweep_Bl3.py', opened])
sys.path.insert(0, os.path.join(REPO, 'tools'))
import build_report_Bl3 as BRP
T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
A = json.load(open(opened, encoding='utf-8'))
text = BRP.build(T3, A, {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '続ける'}}, {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}, [], None, '起草者の行（合成）')
V, _ = BRP.lint_report(text, T3)
print('[run_boot_dry] 報告 %d 行・走査の違反 %d' % (text.count('\n') + 1, len(V)), flush=True)
os.makedirs(REC)
for tag, d in (('check', dc), ('pilot', dp), ('main', dm)):
    shutil.copyfile(os.path.join(d, 'progress.log'), os.path.join(REC, '%s-progress.log' % tag))
    shutil.copyfile(os.path.join(d, 'session.json'), os.path.join(REC, '%s-session.json' % tag))
shutil.copyfile(judge, os.path.join(REC, 'judge-dry.json'))
J = json.load(open(judge, encoding='utf-8'))
S = json.load(open(os.path.join(dm, 'session.json'), encoding='utf-8'))
CK = json.load(open(os.path.join(dc, 'check.json'), encoding='utf-8'))
summ = ['# 起動器の DRY の走り（機械生成・`records/Bl3/tools/trials/run_boot_dry.py`・%s）' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), '',
        '- 起動器 `tools/colab/boot_Bl3.py` SHA16 %s・走らせる器 `tools/bl3_run.py` SHA16 %s・集計の器 `tools/analyze_Bl3.py` SHA16 %s・掃き出しの器 %s・報告の器 %s・正本 %s。' % (
            sha16f(os.path.join(REPO, 'tools', 'colab', 'boot_Bl3.py')), sha16f(os.path.join(REPO, 'tools', 'bl3_run.py')), sha16f(os.path.join(REPO, 'tools', 'analyze_Bl3.py')),
            sha16f(os.path.join(REPO, 'tools', 'sweep_Bl3.py')), sha16f(os.path.join(REPO, 'tools', 'build_report_Bl3.py')), sha16f(os.path.join(REPO, 'design', 'contrasts-Bl3.json'))),
        '- 小さな本数: 等方 %s・乙の文脈 %s・独立の再計算の v̂ の行 %s（DRY の環境変数）。' % (env['OP4B_DRY_ISO'], env['OP4B_DRY_SEC'], env['OP4B_DRY_RC']),
        '- 相 check: 順伝播 %s 回・比べる相手の除き方の錨 %s・‖static‖ と転記行 D %s・書き換えの器を import できた %s。' % (
            CK.get('forward_calls'), 'あり' if CK.get('comparator_anchor') else '無し', '同じ' if CK.get('static_norm_matches_fact_D') else '違う', CK.get('rewrite_importable')),
        '- 相 main の組: %s・本の計算の近道 %s。' % ('・'.join(S.get('parts') or []), (json.load(open(os.path.join(dm, 'main.json'), encoding='utf-8')).get('shortcut'))),
        '- 一致だけを見る段: 一段目 %s・二段目（札） %s・二段目の値 %s・全体 %s（値は開いていない）。' % (J.get('first'), J.get('second'), '許容の内' if J.get('second_values_within_tol') else '許容の外', J.get('agree')),
        '- 結果を開く段 → 掃き出し（欠け 0）→ 報告の組み立て（%d 行）→ 走査（違反 %d）。' % (text.count('\n') + 1, len(V)), '',
        '| 段 | 終わりの値 |', '|---|---|'] + ['| `%s`%s | %d |' % (s['cmd'], ('（%s）' % '・'.join('%s=%s' % kv for kv in s['env'].items())) if s['env'] else '', s['returncode']) for s in steps] + [
        '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(REC, 'summary.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(summ))
print('[run_boot_dry] wrote %s' % os.path.relpath(REC, REPO))
if V:
    raise SystemExit('走査に違反がある')
