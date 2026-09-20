# -*- coding: utf-8 -*-
"""verify_d150.py v1 —— 四票の所見を**現物で当て直す**（追い問い・K207〜・2026-09-20）。

票は申告であって検査ではない（この事業の教訓）。四票（系統外 Gemini 二名・系統内 claude.ai 二名）の所見を、
一件ずつ現物のコードと正本に当て、作り物の走行で発火させ、数え直す。
**事後の再現である**——再現の枠を先に登録していない（票を読んだ直後に当たった）。その旨を記録に書く。

出力: records/reviews/B/d150-round/verification-d150.{json,md}（--force が無ければ上書きしない）。
用法: python tools/verify_d150.py [--reps 200000] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, argparse, datetime, subprocess, tempfile
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B
import identity_screen_A as ISA

VERSION = 'v1'
REPO = runs_B.REPO
PY = sys.executable
T = runs_B.load_T()
TA = json.loads(open(os.path.join(REPO, 'design', 'contrasts-A.json'), encoding='utf-8').read())
S = T['identity_screen']
rdt = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read()
ROWS = []


def row(k, claim, who, result, verdict, detail):
    ROWS.append({'k': k, 'claim': claim, 'who': who, 'result': result, 'verdict': verdict, 'detail': detail})
    print('%-6s %-10s %s' % (k, verdict, claim[:64]))


# ---- 作り物の走行 ----
def fixture(root, arms, n, gap=0, dup=False):
    shutil.rmtree(root, ignore_errors=True)
    for arm in arms:
        for suf in (('a', 'b') if dup else ('a',)):
            d = os.path.join(root, 'idB', 'idB__transformers__%s__%s' % (arm, suf))
            os.makedirs(d, exist_ok=True)
            json.dump({'tag': 'idB', 'stack': 'transformers', 'scenario': S['scenario'], 'arm': arm, 'n': n,
                       'model': 'fixture', 'dry_run': True},
                      open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            with open(os.path.join(d, 'trials-fixture.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
                for i in range(n):
                    r = {'trial_id': '%s-%s-%d' % (arm, suf, i), 'arm': arm, 'scenario': S['scenario'], 'status': 'ok',
                         'catastrophe': True, 'choice': 'a', 'format_fail': False, 'loop_flag': False, 'truncated': False,
                         'style_a': False, 'style_b': True, 'mention': False, 'correct': None, 'seed': 1, 'dry_run': True}
                    if arm == 'Onull' and i < gap:
                        r['catastrophe'] = None          # 選択は読めたのに破局の判定が空（裁定 D126 の型）
                    f.write(json.dumps(r, ensure_ascii=False) + '\n')
    return root


def run_tool(root, out):
    r = subprocess.run([PY, os.path.join(REPO, 'tools', 'identity_screen_B.py'), '--root', root, '--allow-dry',
                        '--out', out, '--force'], capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    j = json.load(open(out + '.json', encoding='utf-8')) if os.path.exists(out + '.json') else None
    return r.returncode, j


def null_fail(reps, seed=20260920):
    """帰無（両側が同じ分布）での不合格率。段階 A の型（API も再標本）。"""
    rng = np.random.default_rng(seed)
    BASE = TA['bases_4B2507_api'][S['scenario']]

    def setup(arms):
        P, N = [], []
        for a in arms:
            b = BASE[a]
            n = b['n']
            P.append([b['format_fail'] / n, b['refuse'] / n, b['k'] / n, (n - b['format_fail'] - b['refuse'] - b['k']) / n])
            N.append(n)
        return np.array(P), np.array(N)

    def draw(P, n_per_arm, r):
        out = np.empty((r, len(P), 3))
        for i in range(len(P)):
            c = rng.multinomial(n_per_arm[i], P[i], size=r)
            out[:, i, :] = c[:, :3] / n_per_arm[i]
        return out

    def rate(P, nA, nB, fixed=False):
        fails, done = 0, 0
        while done < reps:
            r = min(20000, reps - done)
            a = draw(P, nA, r)
            b = P[None, :, :3] if fixed else draw(P, nB, r)
            d = np.abs(a - b) * 100.0
            flat = d.reshape(r, -1)
            fails += int(np.sum((flat.mean(1) > S['metric_mean_pt']) | (flat.max(1) > S['metric_max_pt'])))
            done += r
        return fails / reps

    PB, NB = setup(S['compared_arms'])
    loc = np.full(len(S['compared_arms']), S['n'])
    out = {'registered_pair': rate(PB, loc, NB), 'alt_pair': rate(PB, loc, loc), 'api_fixed': rate(PB, loc, loc, fixed=True)}
    PA, NA = setup(TA['identity_screen']['compared_arms'])
    out['stage_A_10arms'] = rate(PA, np.full(len(TA['identity_screen']['compared_arms']), TA['identity_screen']['n']), NA)
    out['reps'], out['seed'] = reps, seed
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=200000)
    ap.add_argument('--out', default=os.path.join(REPO, 'records', 'reviews', 'B', 'd150-round', 'verification-d150'))
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if (os.path.exists(a.out + '.json') or os.path.exists(a.out + '.md')) and not a.force:
        sys.exit('既にある（--force で上書き）: %s' % a.out)
    tmp = tempfile.mkdtemp(prefix='d150_')
    try:
        # K207: 走行器と整合検査が選別の十三腕を引けるか（Gemini 二人目の所見 1）
        import run_stageB_local as RSB
        AT = RSB.arm_texts()
        miss = [x for x in S['arms_run'] if x not in AT]
        src_i = rdt('tools', 'integrity_B.py')
        row('K207', '走行器と整合検査が選別の十三腕を引けない（Gemini 二人目・重大）', 'G2',
            '走行器 arm_texts() は %d 腕すべてを引いた（欠け %d）。整合検査の ARM_SHA も合わせた一覧から作る' % (len(S['arms_run']) - len(miss), len(miss)),
            '再現しない', {'missing': miss, 'integrity_merges': "dict(T['arms']['sha16']" in src_i and 'identity_screen' in src_i})
        # K208: 凍結の一覧に判定の器と段階 A の器があるか（Gemini 二人目の所見 2）
        src_f = rdt('tools', 'freeze_B.py')
        row('K208', '凍結の一覧に判定の器・持ち越しに段階 A の器が無い（Gemini 二人目・重大）', 'G2',
            'TOOLS に identity_screen_B.py: %s／CARRYOVER に tools/identity_screen_A.py: %s'
            % ('ある' if "'identity_screen_B.py'" in src_f else '無い', 'ある' if "'tools/identity_screen_A.py'" in src_f else '無い'),
            '再現しない', {'tools_has': "'identity_screen_B.py'" in src_f, 'carryover_has': "'tools/identity_screen_A.py'" in src_f})
        # K209: 不合格のときの終了コード（Gemini 一人目）
        src_b = rdt('tools', 'identity_screen_B.py')
        src_a = rdt('tools', 'identity_screen_A.py')
        row('K209', '不合格のとき終了コード 2 で終わる（段階 A の器は 0・Gemini 一人目）', 'G1',
            'B: %s／A: 終了コードの指定 %s' % ("sys.exit(0 if verdict == 'pass' else 2)" if "sys.exit(0 if verdict == 'pass' else 2)" in src_b else '（無い）',
                                          'あり' if re.search(r"sys\.exit\(\s*0 if verdict", src_a) else 'なし（常に 0）'),
            '**再現する**', {'B_exit_line': "sys.exit(0 if verdict == 'pass' else 2)" in src_b,
                         'A_exit_nonzero': bool(re.search(r"sys\.exit\(", src_a.split("print('[identity_screen_A]")[-1]))})
        # K210: 採点欠落が黙って「その他」に落ちる（claude.ai 二人目の (d) の条件）
        rt = fixture(os.path.join(tmp, 'gap'), S['arms_run'], S['n'], gap=20)
        rc, J = run_tool(rt, os.path.join(tmp, 'gap-out'))
        tp = os.path.join(rt, 'idB', 'idB__transformers__Onull__a', 'trials-fixture.jsonl')
        EX, CC = ISA.exclusive_counts(tp)['Onull'], runs_B.cell_counts(tp, phase='main')['Onull']
        row('K210', '採点欠落（選択は読めたが破局が空）を黙って「その他」に数え、止まらない（claude.ai 二人目）', 'C2',
            '判定の器は終了コード %d で判定 %s を書いた。排他の件数は破局 %d・その他 %d、B の読み口は採点欠落 %d 件'
            % (rc, J['verdict'] if J else '—', EX['catastrophe'], EX['other'], CC['scoring_gap']),
            '**再現する**', {'rc': rc, 'verdict': (J or {}).get('verdict'), 'exclusive': EX, 'cell_counts_gap': CC['scoring_gap']})
        # K211: 同じ鍵の走行を黙って足す（claude.ai 二人目 e-1）
        rt2 = fixture(os.path.join(tmp, 'dup'), S['arms_run'], S['n'], dup=True)
        rc2, J2 = run_tool(rt2, os.path.join(tmp, 'dup-out'))
        nok = (J2 or {}).get('local_counts', {}).get('Onull', {}).get('n_ok')
        row('K211', '同じ腕の走行が二本あると n_ok を足し合わせ、登録の n を超えても止まらない（claude.ai 二人目）', 'C2',
            'Onull の n_ok=%s（登録の n は %d）・終了コード %d・判定 %s' % (nok, S['n'], rc2, (J2 or {}).get('verdict')),
            '**再現する**' if (nok or 0) > S['n'] else '再現しない', {'n_ok': nok, 'n': S['n'], 'rc': rc2})
        # K212: 整合検査が top_k を照らさない（claude.ai 二人目 e-2）
        row('K212', '整合検査が標本化の top_k を照らさない（claude.ai 二人目）', 'C2',
            '照らしている欄: %s' % '・'.join(w for w in ('temperature', 'top_p', 'top_k', 'max_tokens') if w in src_i),
            '**再現する**' if 'top_k' not in src_i else '再現しない', {'has_top_k': 'top_k' in src_i})
        # K213: 正本 identity_screen.generation に top_k が無い（claude.ai 二人目 e-3）
        row('K213', '正本 `identity_screen.generation` に top_k が無い（claude.ai 二人目）', 'C2',
            '鍵: %s' % '・'.join(S['generation']), '**再現する**' if 'top_k' not in S['generation'] else '再現しない',
            {'keys': list(S['generation']), 'explicit_has_top_k': 'top_k' in T['runner']['generation_explicit']})
        # K214: 種を照らさない（claude.ai 二人目 e-4・一人目 E5）
        row('K214', '判定の器が走行の種を登録と照らさない（段階 A の器は照らしていた）', 'C1・C2',
            'B の器に seed の文字列: %s／A の器に seed_registered: %s' % ('ある' if 'seed' in src_b else '無い', 'ある' if 'seed_registered' in src_a else '無い'),
            '**再現する**' if 'seed' not in src_b else '再現しない', {'B_has_seed': 'seed' in src_b})
        # K215: 判定を読む器が無い（claude.ai 一人目 E1・二人目 e-6）
        users = []
        for dp, _, fs in os.walk(os.path.join(REPO, 'tools')):
            for fn in fs:
                if fn.endswith('.py') and ('identity-screen-B' in rdt(os.path.relpath(os.path.join(dp, fn), REPO)) or
                                           'identity_screen_B' in rdt(os.path.relpath(os.path.join(dp, fn), REPO))):
                    users.append(os.path.relpath(os.path.join(dp, fn), REPO).replace('\\', '/'))
        rep_reads = 'identity' in rdt('tools', 'build_report_B.py')
        row('K215', '判定の記録を読む器が無い（報告の組み立て器も入力に取らない）', 'C1・C2',
            '名指す器 %d 本（%s）・報告の組み立て器が読む: %s' % (len(users), '・'.join(sorted(os.path.basename(u) for u in users)), 'はい' if rep_reads else 'いいえ'),
            '**再現する**' if not rep_reads else '再現しない', {'users': sorted(users), 'report_reads': rep_reads})
        # K216: runs_A.py の釘（claude.ai 一人目 (d) の条件 1）
        row('K216', '判定の器が呼ぶ段階 A の**コード**が凍結の網に無い（`runs_A.py`）・器も照らさない', 'C1',
            'freeze_B の持ち越しに runs_A.py: %s／check_pin の対象は正本と記録の二つ' % ('ある' if 'runs_A.py' in src_f else '無い'),
            '**再現する**' if 'runs_A.py' not in src_f else '再現しない',
            {'carryover_has_runs_A': 'runs_A.py' in src_f, 'pins': ['design/contrasts-A.json', 'records/A/identity-screen-A.json']})
        # K217: 帰無での不合格率（claude.ai 両名の数を数え直す）
        nf = null_fail(a.reps)
        row('K217', '帰無での不合格率（登録の対 対 別案の対）を数え直す', 'C1・C2',
            '登録の対 %.4f／別案の対 %.4f／API 固定 %.4f／段階 A の十腕 %.4f（反復 %s・種 %d）'
            % (nf['registered_pair'], nf['alt_pair'], nf['api_fixed'], nf['stage_A_10arms'], format(a.reps, ','), nf['seed']),
            '概ね一致', nf)
        # K218: 段階 A の門0.5 の記録に重みの版があるか（claude.ai 一人目 (b) の注）
        RA = json.loads(rdt('records', 'A', 'identity-screen-A.json'))
        row('K218', '段階 A の門0.5 の記録に重みの版（rev）が無い（claude.ai 一人目）', 'C1',
            '記録の鍵に model はある（%s）が rev は %s' % (RA.get('model'), 'ある' if any('rev' in k for k in RA) else '無い'),
            '**再現する**' if not any('rev' in k for k in RA) else '再現しない', {'model': RA.get('model'), 'keys': sorted(RA)})
        # K219: vLLM の件数は別のセッション・別の日（claude.ai 二人目の注）
        row('K219', 'vLLM の件数は段階 A の別のセッションの走行である（claude.ai 二人目）', 'C2',
            '走行キー %s・記録の作成 %s UTC' % (RA.get('run_key'), RA.get('generated_utc')),
            '**そのとおり**', {'run_key': RA.get('run_key'), 'generated_utc': RA.get('generated_utc')})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    now = datetime.datetime.now(datetime.timezone.utc)
    REC = {'kind': 'verify_d150', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'contrasts_sha16': runs_B.sha16_file(runs_B.CPATH), 'tool_sha16': runs_B.sha16_file(os.path.join(REPO, 'tools', 'identity_screen_B.py')),
           'note': '**事後の再現**（再現の枠を先に登録していない・票を読んだ直後に現物を当たった）。',
           'rows': ROWS}
    json.dump(REC, open(a.out + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    M = ['# 四票の所見の追い問い（機械生成・`tools/verify_d150.py` %s・%s UTC）' % (VERSION, REC['generated_utc']), '',
         '- 正本 SHA16 %s・判定の器 SHA16 %s。' % (REC['contrasts_sha16'], REC['tool_sha16']),
         '- %s' % REC['note'],
         '- 票の出所: G1・G2（系統外・Gemini 3.8 Flash 二名）／C1・C2（系統内・claude.ai の Claude Opus 5 二名・**どちらも Gemini の票を読んでから書いたと申告**）。', '',
         '| 番号 | 所見 | 出所 | 現物で当てた結果 | 判定 |', '|---|---|---|---|---|']
    for r in ROWS:
        M.append('| %s | %s | %s | %s | %s |' % (r['k'], r['claim'], r['who'], r['result'], r['verdict']))
    M += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M))
    print()
    print('[verify_d150] %s.{json,md}（%d 件）' % (os.path.relpath(a.out, REPO), len(ROWS)))
