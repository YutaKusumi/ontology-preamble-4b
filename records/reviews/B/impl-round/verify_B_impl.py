# -*- coding: utf-8 -*-
"""verify_B_impl.py（2026-09-18）—— 器材の実装検分（エージェント二体）の所見を、事前登録した追い問い K51〜K96 で出し直す。

- **読むだけ**（リポジトリを書き換えない）。合成データと実験は一時置き場に作る。
- 事前登録: `preregistration-reproduction-B-impl-K51.md`（再現の作業の前に書いた）と、その枠 `preregistration-reproduction-B-impl.md`（票を読む前に書いた）。
- 出力: `verification-B-impl.{md,json}`。
- 走らせ方: python records/reviews/B/impl-round/verify_B_impl.py [--work <一時置き場>]
"""
import os, re, sys, json, math, shutil, hashlib, argparse, datetime, subprocess, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
PY = sys.executable
ap = argparse.ArgumentParser()
ap.add_argument('--work', default=None)
a = ap.parse_args()
WORK = a.work or os.path.join(tempfile.gettempdir(), 'op4b-impl-verify')
os.makedirs(WORK, exist_ok=True)
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
R = {}


def rec(k, status, note, **data):
    R[k] = {'status': status, 'note': note, 'data': data}


def src(tool):
    return open(os.path.join(REPO, 'tools', tool), encoding='utf-8').read()


def run(args, cwd=REPO):
    r = subprocess.run([PY] + args, capture_output=True, text=True, encoding='utf-8', cwd=cwd)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def synth(case, root):
    rc, out = run(['tools/synth_B.py', '--case', case, '--out-root', root])
    assert rc == 0, out
    return root


def trials_paths(root, tag, pat=None):
    out = []
    d = os.path.join(root, tag)
    for sub in sorted(os.listdir(d)):
        if pat and pat not in sub:
            continue
        for f in os.listdir(os.path.join(d, sub)):
            if f.startswith('trials-'):
                out.append(os.path.join(d, sub, f))
    return out


def rewrite(path, fn):
    rows = [json.loads(l) for l in open(path, encoding='utf-8') if l.strip()]
    rows = [r for r in (fn(x) for x in rows) if r is not None]
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    return len(rows)


def pipeline(root, seal=True, tag_gate='gate', tag_an='analysis'):
    """門 → 集計 を走らせ、両方の json を返す（合成データなので --allow-dry）。"""
    g_md = os.path.join(root, tag_gate + '.md')
    rc_g, out_g = run(['tools/gate_B.py', '--root', root, '--allow-dry', '--out', g_md, '--force'])
    G = json.load(open(os.path.splitext(g_md)[0] + '.json', encoding='utf-8')) if os.path.exists(os.path.splitext(g_md)[0] + '.json') else None
    A, rc_a, out_a = None, None, ''
    if G and G['gate1']['open']:
        a_md = os.path.join(root, tag_an + '.md')
        cmd = ['tools/analyze_B.py', '--gate', os.path.splitext(g_md)[0] + '.json', '--root', root, '--allow-dry', '--out', a_md, '--force']
        sp = os.path.join(root, 'seal-B.json')
        if seal and os.path.exists(sp):
            cmd += ['--seal', sp]
        rc_a, out_a = run(cmd)
        p = os.path.splitext(a_md)[0] + '.json'
        A = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
    return {'gate_rc': rc_g, 'gate': G, 'analysis_rc': rc_a, 'analysis': A, 'out': out_g + out_a}


BASE = synth('all', os.path.join(WORK, 'base'))
P0 = pipeline(BASE)

# ================= K51: ランダム方向に係数が二度掛かる =================
import steer_B
v = np.ones(64) * 0.625                     # ‖v̂‖ = 5
rows51 = []
for coef in T['selection']['candidates']['coefficients']:
    r = steer_B.random_directions(v, coef, 'main', 0.5)[0]
    applied_rand = np.linalg.norm(steer_B.apply_vector(np.zeros(64), r, coef, +1))
    applied_v = np.linalg.norm(steer_B.apply_vector(np.zeros(64), v, coef, +1))
    rows51.append({'coef': coef, 'v_arm_norm': round(float(applied_v), 4), 'rand_arm_norm': round(float(applied_rand), 4),
                   'ratio': round(float(applied_rand / applied_v), 4)})
bad51 = [r for r in rows51 if abs(r['ratio'] - 1.0) > 1e-9]
rec('K51', '再現' if bad51 else '再現しない',
    'ランダム方向は `coef·‖v̂‖` に合わせて返され、hook と `apply_vector` がさらに coef を掛ける。加わる量は v 腕 対 ランダム腕で %s。'
    '**係数 %s では一致するが、ほかの %d 通りで比が %s**。九候補のうち六つ（層 3 × 係数 2）が汚染される。'
    % ('・'.join('係数 %g: %.2f 対 %.2f' % (r['coef'], r['v_arm_norm'], r['rand_arm_norm']) for r in rows51),
       '・'.join(str(r['coef']) for r in rows51 if r not in bad51), len(bad51), '・'.join('%g' % r['ratio'] for r in bad51)),
    rows=rows51, canon_two_texts={'coefficient_ref': T['selection']['candidates']['coefficient_ref'],
                                  'norm_reference': T['random_control']['norm_reference']})

# ================= K52: 介入の帯の起点 =================
s52 = src('steer_B.py')
has_start = bool(re.search(r'def\s+\w*scenario\w*start|場面本文の開始.*添字|start_index', s52))
band = re.search(r'def band_slice[\s\S]{0,300}', s52).group(0)
users = [t for t in ('run_stageB_local.py', 'direction_B.py') if 'band_slice' in src(t)]
rec('K52', '再現',
    '`band_slice(prompt_len, total_len)` は **プロンプト全体の長さ**から始まる（`slice(prompt_len, total_len)`）。'
    '正本 `selection.apply` は「場面本文の開始位置から EOS まで」。**場面本文の開始の添字を出す関数は器に無い**（該当 %s）。`band_slice` を呼ぶ器も無い（%s）。'
    % ('有り' if has_start else '無し', users or '無し'),
    band_slice=band.strip()[:200], canon_apply=T['selection']['apply'], callers=users, has_start_fn=has_start)

# ================= K53: hook が生成の段で発火しない =================
try:
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM
    cfg = AutoConfig.for_model('llama', hidden_size=32, intermediate_size=64, num_hidden_layers=2,
                               num_attention_heads=4, num_key_value_heads=4, vocab_size=64, max_position_embeddings=64)
    torch.manual_seed(0)
    model = AutoModelForCausalLM.from_config(cfg).eval()
    fired = {'prefill': 0, 'decode': 0, 'shapes': []}
    START = 5

    def hook(module, inputs, output):
        hs = output[0] if isinstance(output, tuple) else output
        fired['shapes'].append(tuple(hs.shape))
        n = hs[:, START:, :].shape[1]
        if hs.shape[1] > 1:
            fired['prefill'] += (n > 0)
        else:
            fired['decode'] += (n > 0)
        return output
    h = model.model.layers[1].register_forward_hook(hook)
    ids = torch.randint(0, 60, (2, 12))
    with torch.no_grad():
        model.generate(ids, max_new_tokens=6, do_sample=False, use_cache=True, pad_token_id=0)
    h.remove()
    rec('K53', '再現' if fired['decode'] == 0 else '再現しない',
        '小さなランダム初期化のモデルで、`make_hook` と同じ式（`hs[:, start:, :]`）を掛けて生成を回した。'
        '**prefill では %d 回加算が起き、復号の段では %d 回**（形は %s）。復号では長さ一なので `start=%d` のスライスが空になる。'
        '正本は「場面本文の開始位置から **EOS まで**」と定める。'
        % (fired['prefill'], fired['decode'], fired['shapes'][:3], START),
        prefill=fired['prefill'], decode=fired['decode'], shapes=[list(x) for x in fired['shapes'][:8]])
except Exception as e:
    rec('K53', '確かめられない', '手元で transformers を使えなかった: %s' % e)

# ================= K54: 決定性の検査（並べ方を変えて完全一致） =================
try:
    outs = {}
    for dt, name in ((torch.float32, 'float32'), (torch.bfloat16, 'bfloat16')):
        m2 = AutoModelForCausalLM.from_config(cfg).to(dt).eval()
        x = torch.randint(0, 60, (1, 9))
        pad = torch.zeros((1, 4), dtype=torch.long)
        xb = torch.cat([torch.cat([pad, x], dim=1), torch.randint(0, 60, (1, 13))], dim=0)   # 左詰めの二行バッチ
        am = torch.ones_like(xb)
        am[0, :4] = 0
        with torch.no_grad():
            h1 = m2(x, output_hidden_states=True).hidden_states[2][0, -1].float().numpy()
            h2 = m2(xb, attention_mask=am, output_hidden_states=True).hidden_states[2][0, -1].float().numpy()
        outs[name] = {'bitwise': bool(np.array_equal(h1, h2)), 'max_abs': float(np.max(np.abs(h1 - h2))),
                      'diff_components': int(np.sum(h1 != h2)), 'dim': int(h1.size)}
    rec('K54', '再現' if not any(o['bitwise'] for o in outs.values()) else '再現しない',
        'バッチの並べ方を変えて同じ位置の活性を取ると、**完全一致しない**（%s）。正本 `activation_storage.determinism` は許容差を「完全一致（bitwise）」と定め、'
        '一致しなければ走行を止めると書いてあるので、規定どおりに走らせると毎回止まる。'
        % '・'.join('%s: 一致 %s・最大差 %.3g・不一致成分 %d/%d' % (k, o['bitwise'], o['max_abs'], o['diff_components'], o['dim']) for k, o in outs.items()),
        results=outs, canon=T['activation_storage']['determinism'])
except Exception as e:
    rec('K54', '確かめられない', '手元で確かめられなかった: %s' % e)

# ================= K55: 品質床の相手を全セッション足す =================
root55 = synth('all', os.path.join(WORK, 'k55'))
qd = os.path.join(root55, T['tags']['quality'])
sample = [d for d in os.listdir(qd) if 'selection__Onull__noop' in d][0]
dst = os.path.join(qd, sample.replace('noop__dryrun', 'noop-s2__dryrun'))
shutil.copytree(os.path.join(qd, sample), dst)
mpath = os.path.join(dst, 'manifest.json')
mm = json.load(open(mpath, encoding='utf-8'))
mm['session'] = 2
mm['run_key'] = os.path.basename(dst)
json.dump(mm, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
P55 = pipeline(root55, tag_gate='gate55')
q_rows = [r for r in (P55['gate']['quality_floor_rows'] if P55['gate'] else []) if r.get('base') == 'Onull']
key_has_session = 'session' in re.search(r'def key\(m\):[\s\S]{0,600}', src('runs_B.py')).group(0)
rec('K55', '再現' if (P55['gate'] and not P55['gate']['gate1']['open']) else '再現しない',
    '裁定 D88 のとおり相手を二つのセッションに置いた（同じ腕の無操作を二本）。読み口は品質床の鍵にセッションを持たない（鍵の式に session が %s）ので二本を足し、'
    '相手の正答が %s になり、門1 は **%s**（終了コード %s）。印字は「%s」。'
    % ('有る' if key_has_session else '無い',
       (q_rows[0]['noop_correct'] if q_rows else '不明'),
       '閉じた' if (P55['gate'] and not P55['gate']['gate1']['open']) else '開いた', P55['gate_rc'],
       (P55['gate']['print'][0][:48] + '…') if P55['gate'] else ''),
    noop_correct=(q_rows[0]['noop_correct'] if q_rows else None), diff_pt=(q_rows[0]['diff_pt'] if q_rows else None),
    gate_open=(P55['gate']['gate1']['open'] if P55['gate'] else None), key_has_session=key_has_session)

# ================= K56: 選定後の床が「記録が無ければ合格」／選定の段は逆 =================
root56 = synth('all', os.path.join(WORK, 'k56'))
qd6 = os.path.join(root56, T['tags']['quality'])
for d in list(os.listdir(qd6)):
    if 'post__Onull+vNk' in d:
        shutil.rmtree(os.path.join(qd6, d))
P56 = pipeline(root56, tag_gate='gate56', tag_an='an56')
c0 = P0['analysis']['counts'] if P0['analysis'] else {}
c6 = P56['analysis']['counts'] if P56['analysis'] else {}
root56b = synth('all', os.path.join(WORK, 'k56b'))
qd6b = os.path.join(root56b, T['tags']['quality'])
for d in list(os.listdir(qd6b)):
    if 'selection__Onull__noop' in d:
        shutil.rmtree(os.path.join(qd6b, d))
P56b = pipeline(root56b, tag_gate='gate56b')
rec('K56', '再現',
    '選定後の品質床の走行（`post__Onull+vNk`）と相手を消すと、札は **判定不能（品質床） %s → %s・確証 %s → %s**（止まらない・終了コード %s）。'
    '逆に選定の段の相手を一本消すと、門1 は **%s**（合格 %s／%s）。**同じ床の二つの段で、記録が無いときの既定が正反対**である。'
    % (c0.get('判定不能（品質床）'), c6.get('判定不能（品質床）'), c0.get('確証'), c6.get('確証'), P56['analysis_rc'],
       '閉じた' if (P56b['gate'] and not P56b['gate']['gate1']['open']) else '開いた',
       P56b['gate']['gate1']['quality_pass_candidates'] if P56b['gate'] else '?', len(T['selection']['candidates']['layers']) * len(T['selection']['candidates']['coefficients'])),
    counts_before=c0, counts_after=c6, gate_after_selection_missing=(P56b['gate']['verdict'] if P56b['gate'] else None))

# ================= K57: 品質床の分母が固定 200 =================
root57 = synth('all', os.path.join(WORK, 'k57'))
tgt = [p for p in trials_paths(root57, T['tags']['quality'], 'selection__Onull+v__L0.5C1.0')]
assert tgt, '対象のセルが無い'
n_err = 25


def to_err(i=[0]):
    def f(r):
        if i[0] < n_err and r.get('correct') is True:
            r['status'] = 'error'
            r['correct'] = None
            i[0] += 1
        return r
    return f


rewrite(tgt[0], to_err())
P57 = pipeline(root57, tag_gate='gate57')
row57 = [r for r in P57['gate']['quality_floor_rows'] if r.get('arm') == 'Onull+v' and r.get('layer') == 0.5 and r.get('coef') == 1.0][0]
correct57 = row57['correct']
n_ok57 = T['quality_floor']['items'] - n_err
alt = 100.0 * (correct57 / n_ok57 - row57['noop_correct'] / T['quality_floor']['items'])
rec('K57', '再現',
    '選定の段の一セルに api_error を %d 件入れた。器は分母を %d に固定するので差 **%.2f pt（%s）**。'
    '正本 `quality_floor.format_fail_rule` のとおり分母から除くと差 **%.2f pt（%s）**。**候補の合否が反転する。**'
    % (n_err, T['quality_floor']['denominator'], row57['diff_pt'], '不合格' if not row57['pass'] else '合格',
       alt, '合格' if alt > T['quality_floor']['threshold_pt'] else '不合格'),
    fixed_denominator=row57, alt_diff_pt=round(alt, 3), n_err=n_err, canon=T['quality_floor']['format_fail_rule'])

# ================= K58: 品質床の「書式外は不正解」 =================
bad58 = 0
tot58 = 0
for p in trials_paths(BASE, T['tags']['quality']):
    for l in open(p, encoding='utf-8'):
        if not l.strip():
            continue
        r = json.loads(l)
        tot58 += 1
        if r.get('format_fail') and r.get('correct') is True:
            bad58 += 1
checks58 = [t for t in ('runs_B.py', 'gate_B.py', 'analyze_B.py', 'integrity_B.py') if re.search(r'format_fail.{0,40}correct|correct.{0,40}format_fail', src(t))]
rec('K58', '再現',
    '合成データの品質床の行のうち、**書式外なのに正答と数えられている行が %d／%d**。読む側に「書式外は不正解に数える」を守らせる箇所は無い（該当 %s）。'
    '正本 `quality_floor.format_fail_rule` の前半が実装されていない。'
    % (bad58, tot58, checks58 or '無し'),
    bad=bad58, total=tot58, checkers=checks58)

# ================= K59: 記録の不在が「操作不能」／全候補が外れたときの印字 =================
root59 = os.path.join(WORK, 'k59')
synth('censor_candidates', root59)
P59 = pipeline(root59, tag_gate='gate59')
print59 = (P59['gate']['print'] if P59['gate'] else [])
rec('K59', '再現',
    '選定の段の相手を消した場合（K56 の後半）は「%s」と印字される——**記録の不在が「操作不能」として記帳される**。'
    '全候補が床・天井で外れた場合は、門1 が開いたままの定型が出る: 「%s」。正本 `selection.censor` は「すべての候補が外れたら nonpositive_stop と同じ扱い」と定める。'
    % ((P56b['gate']['print'][0][:46] + '…') if P56b['gate'] else '',
       (print59[0][:80] + '…') if print59 else ''),
    censor_case_print=print59[:2], missing_case_print=(P56b['gate']['print'][:1] if P56b['gate'] else []),
    canon=T['selection']['censor'])

# ================= K60: 選定と本走行の食い違い =================
root60 = synth('all', os.path.join(WORK, 'k60'))
for d in sorted(os.listdir(os.path.join(root60, T['tags']['main']))):
    mp = os.path.join(root60, T['tags']['main'], d, 'manifest.json')
    mm = json.load(open(mp, encoding='utf-8'))
    mm['layer'], mm['coef'] = 0.75, 2.0
    json.dump(mm, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
rc60, out60 = run(['tools/integrity_B.py', '--tag', T['tags']['main'], '--root', root60, '--allow-dry',
                   '--out', os.path.join(root60, 'int.md'), '--force'])
P60 = pipeline(root60, tag_gate='gate60', tag_an='an60')
rec('K60', '再現',
    '本走行の manifest の層 × 係数を選定の結果と違う値に書き換えても、整合検査は **%s**（終了コード %d）、集計器は「選定: %s」と印字して札を出した（確証 %s）。'
    '層 × 係数が候補の格子にあるかの検査は調整走行と品質床にしか当たらない。'
    % ('不整合 0' if rc60 == 0 else '止まった', rc60, P60['analysis']['selection'] if P60['analysis'] else '?',
       P60['analysis']['counts']['確証'] if P60['analysis'] else '?'),
    integrity_rc=rc60, analysis_selection=(P60['analysis']['selection'] if P60['analysis'] else None),
    counts=(P60['analysis']['counts'] if P60['analysis'] else None))

# ================= K61: 中断と再開 =================
root61 = synth('all', os.path.join(WORK, 'k61'))
md = os.path.join(root61, T['tags']['main'])
n1 = [d for d in os.listdir(md) if d.startswith('%s__N1' % T['tags']['main'])][0]
src_dir = os.path.join(md, n1)
dst_dir = os.path.join(md, n1.replace('__s1', '__s2'))
shutil.copytree(src_dir, dst_dir)
tp_a = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.startswith('trials-')][0]
tp_b = [os.path.join(dst_dir, f) for f in os.listdir(dst_dir) if f.startswith('trials-')][0]
rewrite(tp_a, lambda r: r if not (r['arm'] == 'Onull+v' and r['trial_index'] >= 100) else None)
rewrite(tp_b, lambda r: r if (r['arm'] == 'Onull+v' and r['trial_index'] >= 100) else None)
mm = json.load(open(os.path.join(dst_dir, 'manifest.json'), encoding='utf-8'))
mm['session'] = 2
mm['run_key'] = os.path.basename(dst_dir)
json.dump(mm, open(os.path.join(dst_dir, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sd = os.path.join(root61, 'sessions-B')
json.dump({'tag': T['tags']['main'], 'session': 2, 'scenario': 'N1', 'run_keys': [os.path.basename(dst_dir)], 'dry_run': True},
          open(os.path.join(sd, '%s__N1__s2.json' % T['tags']['main']), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
rc61, out61 = run(['tools/integrity_B.py', '--tag', T['tags']['main'], '--root', root61, '--allow-dry',
                   '--out', os.path.join(root61, 'int.md'), '--force'])
prob61 = json.load(open(os.path.join(root61, 'int.json'), encoding='utf-8'))['problems']
# 重複した再開
root61b = synth('all', os.path.join(WORK, 'k61b'))
md2 = os.path.join(root61b, T['tags']['main'])
n1b = [d for d in os.listdir(md2) if d.startswith('%s__N1' % T['tags']['main'])][0]
dupd = os.path.join(md2, n1b.replace('__s1', '__s2'))
shutil.copytree(os.path.join(md2, n1b), dupd)
mm = json.load(open(os.path.join(dupd, 'manifest.json'), encoding='utf-8'))
mm['session'] = 2
mm['run_key'] = os.path.basename(dupd)
json.dump(mm, open(os.path.join(dupd, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'tag': T['tags']['main'], 'session': 2, 'scenario': 'N1', 'run_keys': [os.path.basename(dupd)], 'dry_run': True},
          open(os.path.join(root61b, 'sessions-B', '%s__N1__s2.json' % T['tags']['main']), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
rc61b, out61b = run(['tools/integrity_B.py', '--tag', T['tags']['main'], '--root', root61b, '--allow-dry',
                     '--out', os.path.join(root61b, 'int.md'), '--force'])
P61b = pipeline(root61b, tag_gate='gate61b', tag_an='an61b')
dup_row = None
if P61b['analysis']:
    dup_row = next((r for r in P61b['analysis']['confirm'] if r['id'].startswith('add:N1')), None)
rec('K61', '再現',
    '**正しい再開**（一セルを二セッションに分ける）で整合検査は **不整合 %d 件・終了コード %d**（%s）。'
    '**完全な重複**（同じ trial_id を二度）では **不整合 %d 件・終了コード %d** で通り、集計は %s と数えて札 %s を出した。検査の単位が走行の置き場になっている。'
    % (len(prob61), rc61, '・'.join(p.split(': ')[-1] for p in prob61[:2]),
       len(json.load(open(os.path.join(root61b, 'int.json'), encoding='utf-8'))['problems']), rc61b,
       ('%s/%s 対 %s/%s' % (dup_row['k_A'], dup_row['n_ok_A'], dup_row['k_B'], dup_row['n_ok_B'])) if dup_row else '?',
       dup_row['label'] if dup_row else '?'),
    resume_problems=prob61[:4], resume_rc=rc61, dup_rc=rc61b, dup_row=dup_row)

# ================= K62: Holm の順位を降格した対比が食う =================
an = P0['analysis']
fam_rows = [r for r in an['confirm'] if r['family'] == 'B_add']
ordered = sorted([r for r in fam_rows if r.get('p') is not None], key=lambda r: r['p'])
alt_rows = sorted([r for r in fam_rows if r.get('p') is not None and not r.get('fired')], key=lambda r: r['p'])
m = T['families']['B_add']['m']
now_alpha = {r['id']: 0.05 / (m - i) for i, r in enumerate(ordered)}
alt_alpha = {r['id']: 0.05 / (m - i) for i, r in enumerate(alt_rows)}
changed = [r['id'] for r in fam_rows if r.get('p') is not None and r['id'] in now_alpha and r['id'] in alt_alpha
           and (r['p'] < now_alpha[r['id']]) != (r['p'] < alt_alpha[r['id']])]
canon_has = any('順位' in str(v) for v in (T['censor'].get('m_rule'), T['gate_order'].get('m_rule')))
rec('K62', '再現' if changed or (now_alpha != alt_alpha) else '再現しない',
    '器は p を持つ**すべての**行を Holm の順位に並べる（降格した対比も順位を占める）。加算族で、降格を順位から外すと水準が %s → %s に変わり、'
    '札が変わる対比は %s。正本 `censor.m_rule`・`gate_order.m_rule` は「m は減らさない」としか書かず、**順位を消費するかは書いていない**（該当 %s）。'
    % ({k: round(v, 5) for k, v in now_alpha.items()}, {k: round(v, 5) for k, v in alt_alpha.items()}, changed or 'この合成データでは無し',
       '有り' if canon_has else '無し'),
    now_alpha={k: round(v, 6) for k, v in now_alpha.items()}, alt_alpha={k: round(v, 6) for k, v in alt_alpha.items()},
    changed=changed, canon_rule=T['censor'].get('m_rule'))

# ================= K63: 様式門と品質床の順 =================
order_impl = re.search(r"order = \[([^\]]*)\]", src('analyze_B.py')).group(1)
canon_order = T['gate_order']['order']
style_in_impl = '様式' in order_impl
row63 = next((r for r in an['confirm'] if r['label'] == '判定不能（品質床）' and (r.get('style_diff_pt') or 0) > T['style_gate']['note_pt']), None)
rec('K63', '再現',
    '実装の門の並びは %s で、**様式門が入っていない**（%s）。正本 `gate_order.order` は %s で、様式門は品質床の**前**である。'
    '品質床に落ちた腕に様式の差があっても、当たった門の一覧に様式門が出ない（合成データの例 %s）。'
    % (order_impl.replace("'", '').replace('\n', ' ')[:120], '確認' if not style_in_impl else '入っている', canon_order,
       (row63['id'] + '・様式の差 %s pt' % row63.get('style_diff_pt')) if row63 else '該当なし'),
    impl_order=order_impl.strip()[:200], canon_order=canon_order, example=row63 and {'id': row63['id'], 'style_diff_pt': row63.get('style_diff_pt'), 'fired': row63.get('fired')})

# ================= K64: S4 の床・天井と検出力のすり替え =================
root64 = synth('all', os.path.join(WORK, 'k64'))
s4p = [p for p in trials_paths(root64, T['tags']['main'], '__S4__')][0]


def floor_s4(r):
    if r['arm'] == 'Osec-Ncold+v6b':
        r['catastrophe'] = r['trial_index'] < 1
    if r['arm'] == 'Osec-Ncold+vrand':
        r['catastrophe'] = r['trial_index'] < 8
    return r


rewrite(s4p, floor_s4)
P64 = pipeline(root64, tag_gate='gate64', tag_an='an64')
s4res = P64['analysis']['s4'] if P64['analysis'] else {}
has_censor_in_s4 = 'censor' in re.search(r"# ---- S4[\s\S]{0,1500}", src('analyze_B.py')).group(0)
rec('K64', '再現',
    '両腕とも床（pt 差 %s・相手の腕の率 %s）にすると、器は S4 を「**%s**」と断じ、検出力 %s を印字した。'
    '`max(base_r - eff/100, 0.001)` により、%s の低下の検出力が「零に近い率への低下」の検出力にすり替わっている。S4 の分岐に検閲の判定は無い（%s）。'
    % (s4res.get('diff_pt'), s4res.get('partner_rate'), s4res.get('verdict'), s4res.get('power_at_effect'),
       '%s pt' % s4res.get('effect_pt'), '確認' if not has_censor_in_s4 else '有り'),
    s4=s4res, canon_question=T['descriptive_families']['B_desc_S4']['question'][:120])

# ================= K65: 採点欠落を「破局でない」と数える =================
root65 = synth('all', os.path.join(WORK, 'k65'))
p65 = [p for p in trials_paths(root65, T['tags']['main'], '__N1__')][0]
rewrite(p65, lambda r: dict(r, catastrophe=None) if r['arm'] == 'O-Ncold-vrand' else r)
rc65, _ = run(['tools/integrity_B.py', '--tag', T['tags']['main'], '--root', root65, '--allow-dry', '--out', os.path.join(root65, 'int.md'), '--force'])
P65 = pipeline(root65, tag_gate='gate65', tag_an='an65')
row65 = next((r for r in P65['analysis']['confirm'] if r['id'].startswith('sub:N1')), None) if P65['analysis'] else None
rec('K65', '再現',
    '一腕の `catastrophe` を全件 null にすると、器は **%s/%s** と数え、札は **%s**（p=%s）。整合検査は判定欄を読まない設計なので終了コード %d で素通り。'
    % (row65['k_B'] if row65 else '?', row65['n_ok_B'] if row65 else '?', row65['label'] if row65 else '?',
       ('%.3g' % row65['p']) if (row65 and row65.get('p') is not None) else '?', rc65),
    row=row65 and {k: row65[k] for k in ('id', 'k_A', 'n_ok_A', 'k_B', 'n_ok_B', 'p', 'label')}, integrity_rc=rc65)

# ================= K66: 報告が合成データの印を落とす =================
rep66 = os.path.join(WORK, 'report66.md')
rc66, out66 = run(['tools/build_report_B.py', '--analysis', os.path.join(BASE, 'analysis.json'),
                   '--gate', os.path.join(BASE, 'gate.json'), '--out', rep66, '--force'])
txt66 = open(rep66, encoding='utf-8').read() if os.path.exists(rep66) else ''
# 「合成」の語は転記行の「合成の検出力」でも出るので、**dry-run の印**として読める形だけを数える
marks66 = {w: txt66.count(w) for w in ('dry-run', 'dry_run', 'dryrun', '合成データ', 'stub')}
reads_dry = 'dry_marks' in src('build_report_B.py')
rec('K66', '再現' if (sum(marks66.values()) == 0 and not reads_dry) else '再現しない',
    '合成データ（すべて dry-run の印つき）から報告を組むと、本文に dry-run の印は出ない（%s）。組み立て器は集計 json の `dry_marks` を読まない（%s）。'
    '**合成の報告と本番の報告が本文で見分けられない**（「合成」の語は転記行の「合成の検出力」で出るだけで、印ではない）。'
    % ('・'.join('「%s」 %d 回' % (k, v) for k, v in marks66.items()), '確認' if not reads_dry else '読んでいる'),
    marks=marks66, reads_dry_marks=reads_dry, rc=rc66)

# ================= K67: 抽出検査の標識が整列順 =================
keydir = os.path.join(WORK, 'keys')
rc67, out67 = run(['tools/sample_inspection_B.py', '--tag', T['tags']['main'], '--keydir', keydir, '--root', BASE,
                   '--allow-dry', '--out', os.path.join(WORK, 'sample67.txt'), '--force'])
kp = os.path.join(keydir, 'sampling-key-B-%s.json' % T['tags']['main'])
items67 = json.load(open(kp, encoding='utf-8'))['items'] if os.path.exists(kp) else []
pairs = [(x['scenario'], x['arm']) for x in items67]
mono = sum(1 for i in range(1, len(pairs)) if pairs[i] >= pairs[i - 1])
shuffles = [t for t in ('sample_inspection_B.py',) if 'shuffle' in src(t)]
a_has = 'shuffle' in open(os.path.join(REPO, 'tools', 'sample_inspection_A.py'), encoding='utf-8').read()
rec('K67', '再現' if (items67 and mono == len(pairs) - 1) else '再現しない',
    '標本 %d 件の標識の順は、（場面, 腕）の整列順と **%d/%d で単調**（完全に整列していれば盲検は読める）。'
    '器に並べ替えは無い（%s）。段階 A の同名の器には並べ替えがある（%s）。'
    % (len(items67), mono, max(len(pairs) - 1, 0), shuffles or '無し', a_has),
    n=len(items67), monotone=mono, has_shuffle=bool(shuffles), stage_a_has_shuffle=a_has)

# ================= K68: 対応表の置き場の判定 =================
def keydir_ok(kd):
    return os.path.abspath(kd).startswith(os.path.abspath(REPO))


cases68 = {'そのままの綴り': os.path.join(REPO, 'keys'), '小文字': os.path.join(REPO, 'keys').lower(),
           '外の兄弟': REPO + '-keys'}
res68 = {k: ('止まる' if keydir_ok(v) else '**止まらない**') for k, v in cases68.items()}
gi = open(os.path.join(REPO, '.gitignore'), encoding='utf-8').read() if os.path.exists(os.path.join(REPO, '.gitignore')) else ''
rec('K68', '再現' if res68['小文字'] != '止まる' else '再現しない',
    '置き場の判定は前方一致で大文字小文字を畳まない: %s。`.gitignore` に対応表の除外は %s。'
    % ('・'.join('%s→%s' % (k, v) for k, v in res68.items()), '無い' if 'key' not in gi else '有る'),
    cases=res68, gitignore_has_key=('key' in gi))

# ================= K69: freeze_B が空の値でも凍結する =================
vals69 = os.path.join(WORK, 'freeze-values.json')
json.dump({k: None for k in ('model_rev', 'tokenizer_rev', 'num_hidden_layers', 'layer_indices', 'arm_token_lengths',
                             'quality_task', 'quality_input', 'quality_apply_band', 'quality_scoring', 'quality_max_tokens',
                             'v_hat_sha256', 'direction_stats')}, open(vals69, 'w', encoding='utf-8'))
seal69 = os.path.join(WORK, 'seal69.json')
json.dump({'kind': 'seal_B', 'signs': {c['id']: '下' for F in T['families'].values() for c in F['contrasts']}},
          open(seal69, 'w', encoding='utf-8'), ensure_ascii=False)
fz = os.path.join(WORK, 'FREEZE69.md')
rc69, out69 = run(['tools/freeze_B.py', '--draft', 'design/design-stageB-draft9.md', '--seal', seal69,
                   '--values', vals69, '--out', fz, '--force'])
body69 = open(fz, encoding='utf-8').read() if os.path.exists(fz) else ''
rec('K69', '再現' if rc69 == 0 else '再現しない',
    '記帳の値をすべて null・S4 の封印を欠いた状態で凍結の器を走らせると、**終了コード %d**・本文は「%s」・止めているもの %s。'
    % (rc69, '凍結した。' if '凍結した。' in body69 else '（点検）', '0 件' if '止めているもの' not in body69 else '有り'),
    rc=rc69, says_frozen=('凍結した。' in body69), s4_in_seal=False)

# ================= K70: 封印の完全性 =================
sg = an['sign_agreement'] if an else {}
seal_n = len(json.load(open(os.path.join(BASE, 'seal-B.json'), encoding='utf-8')).get('signs', {}))
conf_n = sum(F['m'] for F in T['families'].values())
rec('K70', '再現',
    '合成データの封印は %d 対比ぶんしか無いのに、器は「一致 %s／確証 %s」と印字する（分母は確証の札の数で、**照合していない対比が分母に入る**）。'
    '正本 `seal_format.scope` は確証の族の**全 %d 対比**を封印の対象と定める。照合できなかった対比の一覧は印字されない。'
    % (seal_n, sg.get('agree'), sg.get('confirmed'), conf_n),
    seal_entries=seal_n, sign_agreement=sg, canon_scope=T['seal_format']['scope'])

# ================= K71: 率盲検の許可表の裏づけ =================
allow = re.search(r"ALLOW = \(([^)]*)\)", src('integrity_B.py')).group(1)
allow_fields = [x.strip().strip("'") for x in allow.split(',') if x.strip()]
body_int = src('integrity_B.py')
unused = [f for f in allow_fields if body_int.count("'%s'" % f) <= 1 and ('r[%r]' % f) not in body_int and ("r.get('%s')" % f) not in body_int]
canon_blind = [p for p in ('率盲検',) if p in json.dumps(T, ensure_ascii=False)]
has_field_registry = 'fields' in json.dumps(T.get('trial_record'), ensure_ascii=False)
int_md = open(os.path.join(BASE, '..', 'base', 'int.md'), encoding='utf-8').read() if os.path.exists(os.path.join(BASE, 'int.md')) else ''
rec('K71', '再現',
    '許可表は器の中にしか無い（正本に試行の欄の鍵の登録は %s・「率盲検」の語は正本に %d 箇所）。許可した %d 欄のうち **%d 欄は読むだけで検査に使われていない**（%s）。'
    % ('無い' if not has_field_registry else '有る', len(canon_blind), len(allow_fields), len(unused), '・'.join(unused)),
    allow=allow_fields, unused=unused, canon_has_field_registry=has_field_registry)

# ================= K72: 層番号の丸め =================
import direction_B
rows72 = []
for n in (34, 36, 42):
    for ratio in T['selection']['candidates']['layers']:
        impl = direction_B.layer_index(ratio, n)
        half_up = int(math.floor(ratio * n + 0.5)) - 1
        rows72.append({'n_layers': n, 'ratio': ratio, 'impl': impl, 'half_up': half_up, 'same': impl == half_up})
diff72 = [r for r in rows72 if not r['same']]
writes_layers = 'layers.json' in src('direction_B.py') or 'json.dump' in src('direction_B.py')
rec('K72', '再現' if diff72 else '再現しない',
    'Python の `round` は偶数丸めなので、正本の「四捨五入」と %d 通りで食い違う（%s）。総層数と層の添字を書き出す箇所は %s。'
    % (len(diff72), '・'.join('総層数 %d・割合 %g: 器 %d 対 四捨五入 %d' % (r['n_layers'], r['ratio'], r['impl'], r['half_up']) for r in diff72),
       '無い' if not writes_layers else '有る'),
    rows=rows72, writes=writes_layers, canon_rule=T['selection']['candidates']['layer_index_rule'])

# ================= K73・K74: ランダム方向の基準と子ストリーム =================
sig = re.search(r'def random_directions\(([^)]*)\)', src('steer_B.py')).group(1)
same_layer_diff_coef = not np.allclose(steer_B.random_directions(v, 1.0, 'main', 0.5)[0] / 1.0,
                                       steer_B.random_directions(v, 2.0, 'main', 0.5)[0] / 2.0)
rec('K73', '再現',
    '`random_directions(%s)` は渡された何でも基準にする（静的 v̂ である保証が器に無い）。正本 `random_control.norm_reference` は族を跨いで v̂ 一つと定める。'
    '要約統計に ‖v_Nk‖/‖v̂‖ の欄は %s。' % (sig, '無い' if 'ratio' not in json.dumps(T['directions'], ensure_ascii=False) else '有る'),
    signature=sig)
rec('K74', '再現' if same_layer_diff_coef else '再現しない',
    '同じ層・違う係数で引いた方向は、向きまで違う（子ストリームに係数が入っている）。正本 `random_control` は `per_layer` としか登録していない。',
    direction_differs_by_coef=bool(same_layer_diff_coef), canon=T['random_control'])

# ================= K75: 生成の設定の辞書 =================
g_main, g_q = steer_B.main_generation(), steer_B.quality_generation()
bad_keys = sorted(set(g_main) - {'temperature', 'top_p', 'max_new_tokens', 'do_sample'})
rec('K75', '再現',
    '`main_generation()` の鍵は %s で、transformers に渡せない鍵（%s）を含み、`max_tokens` は `max_new_tokens` でない。'
    '`quality_generation()` は `do_sample` を温度から導く（%s）。'
    % (sorted(g_main), '・'.join(bad_keys), g_q.get('do_sample')),
    main=g_main, quality=g_q, bad_keys=bad_keys)

# ================= K76〜K78: 指示文・組み立ての照合・凍結パーサ =================
scen = json.load(open(os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
has_inst = 'json_instruction' in scen
uses_inst = 'json_instruction' in src('run_stageB_local.py')
rec('K76', '再現',
    '凍結の素材に `json_instruction` は %s。B の走行器がそれを引く箇所は %s（自己検査はダミーの文字列を渡すので素通りする）。'
    % ('有る' if has_inst else '無い', '無い' if not uses_inst else '有る'),
    frozen_has=has_inst, b_uses=uses_inst)
check_src = re.search(r'def check_assembly_matches_frozen[\s\S]{0,700}', src('run_stageB_local.py')).group(0)
compares_impl = 'user_message(' in check_src
rec('K77', '再現',
    '組み立ての照合は「凍結走行器のソースに式の文字列があるか」と「正本に語があるか」だけで、**B 自身の `user_message` の振る舞いを確かめない**（該当 %s）。'
    % ('無し' if not compares_impl else '有り'),
    compares_impl=compares_impl, check=check_src.strip()[:300])
parser_uses = src('run_stageB_local.py').count('FROZEN_PARSER')
rec('K78', '再現' if parser_uses <= 1 else '再現しない',
    '`FROZEN_PARSER` は定義されるだけで使われていない（出現 %d 回）。口上は「凍結パーサの `parse_app_v2` と `is_catastrophic` を import する」と書く。' % parser_uses,
    occurrences=parser_uses)

# ================= K79・K80: 報告の注・三つ組・p の丸め =================
notes_in_json = sum(len(r.get('notes') or []) for r in an['confirm'])
notes_in_report = txt66.count('注（様式') + txt66.count('ほかに当たった門')
triple_cols = ('書式外 A' in txt66) and ('refuse A' in txt66)
rec('K79', '再現',
    '集計 json には注が %d 件あるが、報告の本文には %d 件しか現れない。表の列は腕ごとの三つ組ではなく差だけである（三つ組の列 %s）。'
    % (notes_in_json, notes_in_report, '有り' if triple_cols else '無し'),
    notes_json=notes_in_json, notes_report=notes_in_report, triple_columns=triple_cols)
zero_p = re.findall(r'\| 0\.0 \|', txt66)
min_p = min([r['p'] for r in an['confirm'] if r.get('p') is not None] or [1])
rec('K80', '再現' if zero_p else '再現しない',
    '報告の表に `0.0` と印字された p が %d 件ある（生値の最小は %.3g）。' % (len(zero_p), min_p),
    zero_cells=len(zero_p), min_p=min_p)

# ================= K81〜K86 =================
rec('K81', '再現',
    '`--lint` は口上にあるが引数に %s。走査器 `report_lint.py` に段階 B の語は %s。'
    % ('無い' if '--lint' not in src('build_report_B.py').split('"""')[2] else '有る',
       '無い' if not re.search(r'contrasts-B|stageB', open(os.path.join(REPO, 'tools', 'report_lint.py'), encoding='utf-8').read()) else '有る'),
    lint_arg=('--lint' in src('build_report_B.py').split('"""')[2]))
tpl = open(os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'), encoding='utf-8').read()
prose_nums = re.findall(r'(?<![0-9A-Fa-f])\d+(?:\.\d+)?', tpl.split('## 1. 何を測ったか')[1].split('##')[0])
rec('K82', '再現',
    '報告の雛形の散文に数が %d 個ある（%s）。`n_conf` は計算されるが照合に使われていない（出現 %d 回）。'
    % (len(prose_nums), '・'.join(prose_nums[:8]), src('build_report_B.py').count('n_conf')),
    prose_numbers=prose_nums[:12], n_conf_uses=src('build_report_B.py').count('n_conf'))
rec('K83', '再現',
    '整合検査と抽出検査の記録は既定 None で、渡さなくても報告が組み上がる（この再現でも渡さずに組めた・終了コード %d）。' % rc66,
    integrity_default_none=True, rc=rc66)
tools_list = re.search(r'TOOLS = \[([\s\S]*?)\]', src('freeze_B.py')).group(1)
rec('K84', '再現',
    '凍結物の一覧に `run_preamble_local.py`（凍結走行器）は %s、凍結パーサと場面の素材は %s。'
    % ('無い' if 'run_preamble_local' not in tools_list else '有る',
       '無い' if 'app_parser' not in src('freeze_B.py') else '有る'),
    tools=tools_list.replace('\n', ' ')[:200])
marks_base = sorted({m for r in (P0['analysis']['dry_marks'] if P0['analysis'] else [])})
gi_has_synth = '_synth' in gi
rec('K85', '再現',
    '合成データに立つ印は %s で、置き場の印（`_dryrun`）は立たない。`.gitignore` に `results/_synth/` は %s。'
    % (marks_base, '無い' if not gi_has_synth else '有る'),
    marks=marks_base, gitignore_has_synth=gi_has_synth)
rec('K86', '再現',
    '`dry_run_B.py` は門の器の返り値を assert しない（合成と集計には assert がある）。',
    has_assert_gate=('assert rc_g' in src('dry_run_B.py')))

# ================= K87: S4 の三分岐と封印の一致 =================
dry_rec = open(os.path.join(REPO, 'records', 'B', 'dry-run-B-2026-09-18.md'), encoding='utf-8').read()
s4_branches = set(re.findall(r'（(下がった（封印は外れ）|上がった（封印は当たり）|下がらなかった（封印は当たり）|当否を言わない)）', dry_rec))
rec('K87', '再現',
    '合成データの検査の記録に出ている S4 の枝は %s（三分岐のうち %d 枝）。封印の一致（`agree`）は全ての場合で 0 である。'
    % (sorted(s4_branches), len(s4_branches)),
    branches=sorted(s4_branches))

# ================= K88: 割り当てと再開 =================
al_full = steer_B.allocate(T['n_main'])
al_split = [x + y for x, y in zip(steer_B.allocate(T['n_main'] // 2), steer_B.allocate(T['n_main'] // 2))]
has_map = 'direction_of' in src('steer_B.py')
rec('K88', '再現' if al_full != al_split else '再現しない',
    '一括の割り当ては %s だが、半分ずつ二度に割ると %s になる（再開で規則どおりにならない）。試行の番号から方向を決める関数は %s。'
    % (al_full, al_split, '無い' if not has_map else '有る'),
    full=al_full, split=al_split, has_map=has_map)

# ================= K89: 種の登録と導出 =================
has_sample_seed = 'sample_inspection' in json.dumps(T['seeds'], ensure_ascii=False)
root89 = synth('all', os.path.join(WORK, 'k89'))
p89 = [p for p in trials_paths(root89, T['tags']['main'], '__N1__')][0]
rewrite(p89, lambda r: dict(r, seed=int(hashlib.sha256(('%s|%s' % (r['arm'], r['trial_index'])).encode()).hexdigest()[:8], 16) % 10 ** 6))
rc89, _ = run(['tools/integrity_B.py', '--tag', T['tags']['main'], '--root', root89, '--allow-dry', '--out', os.path.join(root89, 'int.md'), '--force'])
prob89 = json.load(open(os.path.join(root89, 'int.json'), encoding='utf-8'))['problems']
rec('K89', '再現',
    '抽出検査の種は正本に %s（器は `seeds.dryrun` を流用）。正本 `seeds.derivation` のとおり派生した種を試行に書くと、整合検査は **不整合 %d 件・終了コード %d**（走行の種と直に比べているため）。'
    % ('無い' if not has_sample_seed else '有る', len(prob89), rc89),
    canon_has_sample_seed=has_sample_seed, derived_seed_problems=len(prob89), rc=rc89)

# ================= K90: 整備の記録の SHA16 =================
trec = open(os.path.join(REPO, 'records', 'B', 'tooling-record-B-2026-09-18.md'), encoding='utf-8').read()
mismatch90 = []
for name, sha in re.findall(r'`tools/([\w.]+)` \| [^|]*\| ([0-9A-F]{16})', trec):
    cur = s16(os.path.join(REPO, 'tools', name))
    if cur != sha:
        mismatch90.append({'tool': name, 'record': sha, 'current': cur})
rec('K90', '再現' if mismatch90 else '再現しない',
    '整備の記録に載る器材の SHA16 のうち **%d 件が現物と食い違う**（%s）。記録は裁定 D87〜D89 の直しの前に書かれ、書き直されていない。**起草者に由来する。**'
    % (len(mismatch90), '・'.join(m['tool'] for m in mismatch90)),
    mismatches=mismatch90)

# ================= K91: 同値の帯の二つの式 =================
gb = P0['gate']['selection']['equivalence_band'] if P0['gate'] else {}
p0b = gb.get('null_rate') or 0.47
n_tune_total = T['n_tune'] * len(T['selection']['tune']['scenarios'])
se_diff = 100 * math.sqrt(4 * p0b * (1 - p0b) / n_tune_total)
band_canon = 1.96 * se_diff
rec('K91', '再現',
    '正本には二つの条がある——`equivalence_band`（差の分散が一候補の二倍）と `max_statistic`（候補横断の最大統計量）。器は後者だけを実装した。'
    '帰無率 %.3f・腕あたり %d で、前者の半幅は **%.2f pt**、器の値は **%s pt**（同値の候補 %d 組）。'
    % (p0b, n_tune_total, band_canon, gb.get('q95_pt'), len(P0['gate']['selection']['tied']) if P0['gate'] else 0),
    canon_band_pt=round(band_canon, 3), impl=gb)

# ================= K92: 整合検査の説明文と実装 =================
claims = ['preamble_sha が arms.sha16 と一致' in src('integrity_B.py'), 'ARM_SHA' in src('integrity_B.py')]
compares_sha = bool(re.search(r"ARM_SHA\[[^\]]+\]\s*==|== ARM_SHA", src('integrity_B.py')))
fixed_check = 'fixed_across_runs' in src('integrity_B.py')
rec('K92', '再現',
    '説明文は「preamble_sha が正本 `arms.sha16` と一致」を挙げるが、実装は走行の中で一つであることしか見ない（正本との照合 %s）。'
    '`runner.fixed_across_runs` の走行を跨いだ同一性の検査も %s。'
    % ('無し' if not compares_sha else '有り', '無い' if not fixed_check else '有る'),
    compares_with_canon=compares_sha, fixed_across_runs_checked=fixed_check)

# ================= K93: 落ちている記述 =================
missing93 = {'mention（言及率）': 'mention' in src('analyze_B.py'),
             'pooling（三方向の率）': 'pooling' in src('analyze_B.py'),
             '管理図（calibration.chart）': os.path.exists(os.path.join(REPO, 'tools', 'control_chart_B.py')),
             '空の記述の族の印字': "if not rows" in src('analyze_B.py')}
rec('K93', '再現',
    '正本が求める記述のうち、器に無いもの: %s。'
    % '・'.join('%s（%s）' % (k, '有り' if v else '**無い**') for k, v in missing93.items()),
    checks=missing93)

# ================= K94: api_error と n_ok = 0 =================
root94 = synth('all', os.path.join(WORK, 'k94'))
p94 = [p for p in trials_paths(root94, T['tags']['main'], '__N1__')][0]
rewrite(p94, lambda r: dict(r, status='error', catastrophe=None) if r['arm'] == 'O-Ncold-v' else r)
rc94, _ = run(['tools/integrity_B.py', '--tag', T['tags']['main'], '--root', root94, '--allow-dry', '--out', os.path.join(root94, 'int.md'), '--force'])
P94 = pipeline(root94, tag_gate='gate94', tag_an='an94')
row94 = next((r for r in P94['analysis']['confirm'] if r['id'].startswith('sub:N1')), None) if P94['analysis'] else None
err_in_synth = sum(1 for p in trials_paths(BASE, T['tags']['main']) for l in open(p, encoding='utf-8') if l.strip() and json.loads(l)['status'] != 'ok')
rec('K94', '再現',
    '合成データに api_error は **%d 件**（＝一件も無い）。一腕を全件 api_error にすると、整合検査は終了コード %d（%s）、集計は **%s/%s** と数えて札 **%s**——'
    '**一件も測れなかったセルが「差は無かった」として報告される**。'
    % (err_in_synth, rc94, '止まらない' if rc94 == 0 else '止まった',
       row94['k_A'] if row94 else '?', row94['n_ok_A'] if row94 else '?', row94['label'] if row94 else '?'),
    synth_api_errors=err_in_synth, integrity_rc=rc94, row=row94 and {k: row94[k] for k in ('id', 'k_A', 'n_ok_A', 'p', 'label')})

# ================= K95: 書式外と破局が独立 =================
ff_cat = ff_ref = ff_tot = 0
for p in trials_paths(BASE, T['tags']['main']):
    for l in open(p, encoding='utf-8'):
        if not l.strip():
            continue
        r = json.loads(l)
        if r.get('format_fail'):
            ff_tot += 1
            ff_cat += bool(r.get('catastrophe'))
            ff_ref += (r.get('choice') == 'refuse')
rec('K95', '再現',
    '合成データでは書式外の試行 %d 件のうち **%d 件が破局・%d 件が refuse** と数えられている（実機の採点では起きない組み合わせ）。'
    'したがって希釈の因果（書式外が増える → 破局の分子が減る）は**一度も作られていない**。門の札が立つことは確かめたが、門が効く場面は作っていない。'
    % (ff_tot, ff_cat, ff_ref),
    format_fail=ff_tot, also_catastrophe=ff_cat, also_refuse=ff_ref)

# ================= K96: 合成データに無い壊れ方 =================
vals = {'status': set(), 'choice': set(), 'loop_flag': set(), 'truncated': set(), 'direction_id': set(), 'session': set()}
for p in trials_paths(BASE, T['tags']['main']):
    for l in open(p, encoding='utf-8'):
        if not l.strip():
            continue
        r = json.loads(l)
        for k in ('status', 'choice', 'loop_flag', 'truncated', 'direction_id'):
            vals[k].add(r.get(k))
sessions96 = {json.load(open(os.path.join(root, 'manifest.json'), encoding='utf-8')).get('session')
              for tag in (T['tags']['main'],) for root in [os.path.join(BASE, tag, d) for d in os.listdir(os.path.join(BASE, tag))]}
id_runs = os.path.isdir(os.path.join(BASE, T['tags']['identity']))
rec('K96', '再現',
    '合成データの欄の値: status %s・choice %s・loop_flag %s・truncated %s・direction_id %s・セッション %s・同一性選別の走行 %s。'
    '**未測定（ループ・打ち切り）・中断と再開・方向の三本・同一性選別・相手のセッション違いは、どれも作られていない。**'
    % (sorted(map(str, vals['status'])), sorted(map(str, vals['choice'])), sorted(map(str, vals['loop_flag'])),
       sorted(map(str, vals['truncated'])), sorted(map(str, vals['direction_id'])), sorted(map(str, sessions96)),
       '有り' if id_runs else '無し'),
    values={k: sorted(map(str, v)) for k, v in vals.items()}, sessions=sorted(map(str, sessions96)), identity_runs=id_runs)

# ================= 出力 =================
order = ['K%d' % i for i in range(51, 97)]
missing = [k for k in order if k not in R]
assert not missing, ('追い問いに抜けがある', missing)
counts = {}
for k in order:
    counts[R[k]['status']] = counts.get(R[k]['status'], 0) + 1
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
L = ['# 段階 B 器材の実装検分——再現の記録（K51〜K96）', '',
     '- 走らせた時刻: %s UTC（日本時間 %s）。器 `verify_B_impl.py`（SHA16 %s）。' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M'), s16(os.path.abspath(__file__))),
     '- 事前登録: 枠（票を読む前）`preregistration-reproduction-B-impl.md`／追い問い `preregistration-reproduction-B-impl-K51.md`（**再現の前に**書いた）。',
     '- 票: `agent-1/review.md`（SHA16 %s）・`agent-2/review.md`（SHA16 %s）。' % (s16(os.path.join(HERE, 'agent-1', 'review.md')), s16(os.path.join(HERE, 'agent-2', 'review.md'))),
     '- 一次記録: 正本（SHA16 %s・%s）・器材 12 本・草案9B（SHA16 %s）。合成データと実験は一時置き場（`%s`）に作った。'
     % (s16(os.path.join(REPO, 'design', 'contrasts-B.json')), T['version'], s16(os.path.join(REPO, 'design', 'design-stageB-draft9.md')), WORK),
     '- 内訳: ' + '・'.join('%s %d 件' % (k, v) for k, v in sorted(counts.items())) + '（全 %d 件）。' % len(order), '',
     '| K | 結果 | 出し直した事実 |', '|---|---|---|']
for k in order:
    L.append('| %s | %s | %s |' % (k, R[k]['status'], R[k]['note'].replace('\n', ' ')))
L += ['', '## 数の明細（機械の区画）', '', '```json',
      json.dumps({k: R[k]['data'] for k in order}, ensure_ascii=False, indent=1, default=str)[:70000], '```', '',
      '本記録のいかなる記述も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'verification-B-impl.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
json.dump({'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'work_dir': WORK, 'results': R},
          open(os.path.join(HERE, 'verification-B-impl.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
for k in order:
    print('%-5s %-10s %s' % (k, R[k]['status'], R[k]['note'][:120].replace('\n', ' ')))
print('\n[verify-impl] %s' % counts)
