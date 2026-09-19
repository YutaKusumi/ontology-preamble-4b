# -*- coding: utf-8 -*-
"""runs_B.py v6 —— 段階 B の走行の記録を読む共有の口（段階 A の `runs_A.py` の型・**段階 A の器は触らない**）。
v6（2026-09-19 の夕刻・裁定 D146）: 品質床の相のセルの番号の段に、課題の選定の測定の段「candidate:候補の鍵」を足した（selection・post の後に候補の登録順——前からある段の番号は変わらない）。
v5（2026-09-19・最後の系統外の巡の後）: 層別の計数から、常に零を足す死んだ行を消した（採否表 P409）。

段階 B の相（正本 `tags`）と置き場:
  同一性選別 `idB`      : results/idB/idB__<スタック>__<場面>__<印>/      （manifest の stack・scenario）
  調整走行   `tuneB`    : results/tuneB/tuneB__<場面>__L<層>C<係数>__<印>/（manifest の scenario・layer・coef）
  品質床     `stageB-quality`: results/stageB-quality/<tag>__<段>__<腕>__L<層>C<係数>__<印>/（manifest の stage〔selection|post〕・arm・layer・coef）
  本走行     `stageB`   : results/stageB/stageB__<場面>__s<セッション>__<印>/（manifest の scenario・session）

どの走行も manifest.json と trials-*.jsonl（一行一試行）と raw-*.jsonl を持つ。
試行の欄（正本 `trial_record`）のうち、この口が数えるのは次だけ:
  trial_id・arm・status・catastrophe・choice・format_fail・style_a（名言及）・style_b（JSON 直答）・mention（検査認識の言及）・loop_flag・truncated・correct（品質床）。
全分母（n_ok）＝ api_error を除いた試行（書式外と refuse を含む・正本 `denominators.n_ok`）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, hashlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CPATH = os.path.join(REPO, 'design', 'contrasts-B.json')
VERSION = 'v6'
COUNT_FIELDS = ('trial_id', 'arm', 'status', 'catastrophe', 'choice', 'format_fail', 'style_a', 'style_b', 'mention', 'loop_flag', 'truncated', 'correct')


def field_registry(T):
    """試行の記録の鍵・判定欄・整合検査の許可欄（正本 `trial_record_fields`・裁定 D97）。器の中に手書きしない。"""
    f = T.get('trial_record_fields') or {}
    assert f.get('fields') and f.get('blind') and f.get('integrity_allow'), '正本に試行の記録の鍵の登録が無い（裁定 D97）'
    return f
ZERO = dict(n=0, n_ok=0, api_error=0, cat=0, refuse=0, ff=0, style_a=0, style_b=0, mention=0, loop=0, trunc=0, unmeas=0,
            correct=0, scoring_gap=0, style_gap=0, correct_format_fail=0)


def load_T(path=None):
    return json.load(open(path or CPATH, encoding='utf-8'))


def sha16_file(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


def results_root(root=None):
    return root or os.path.join(REPO, 'results')


def read_json(p):
    return json.load(open(p, encoding='utf-8'))


def run_dirs(tag, root=None):
    return sorted(d for d in glob.glob(os.path.join(results_root(root), tag, tag + '__*')) if os.path.isdir(d))


def one_file(d, prefix):
    fs = sorted(glob.glob(os.path.join(d, prefix + '-*.jsonl')))
    if len(fs) != 1:
        raise RuntimeError('%s の %s ファイルが %d 本（一本であるべき）' % (d, prefix, len(fs)))
    return fs[0]


def iter_jsonl(p, fields=None):
    with open(p, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                yield ({k: r.get(k) for k in fields} if fields else r)


def dry_marks(d, m, trials_path):
    """dry-run の印（manifest の dry・置き場 _dryrun・行の dry_run）。空なら印なし。"""
    marks = [x for x, on in (('manifest.dry_run', bool(m.get('dry_run'))), ('manifest.model', m.get('model') in ('stub/dry-run', 'stub')),
                             ('dir._dryrun', '_dryrun' in os.path.normpath(d).split(os.sep) or os.path.basename(d).endswith('__dryrun')),
                             ('dir._synth', '_synth' in os.path.normpath(d).split(os.sep))) if on]
    # **先頭一行だけを見ない**（裁定 D115・採否表 P335〔二体目 G4〕）。合成の行が途中に混ざっても捕まえる。
    any_dry = any(r.get('dry_run') for r in iter_jsonl(trials_path, ('dry_run',)))
    if any_dry:
        marks.append('trials.dry_run')
    return marks


def _rec(d, allow_dry):
    m = read_json(os.path.join(d, 'manifest.json'))
    tp = one_file(d, 'trials')
    dm = dry_marks(d, m, tp)
    if dm and not allow_dry:
        raise RuntimeError('dry-run の走行は読まない: %s（印 %s・検査用の口だけが通す）' % (d, '・'.join(dm)))
    return {'dir': d, 'run_key': os.path.basename(d), 'manifest': m, 'trials_path': tp,
            'raw_path': one_file(d, 'raw') if glob.glob(os.path.join(d, 'raw-*.jsonl')) else None, 'dry_marks': dm}


def index_runs(T, tag, root=None, key=None, allow_multi=True, allow_dry=False):
    """走行を manifest から作った鍵で引ける辞書にする（既定の鍵は相ごとの自然な組）。

    key は manifest を受けて鍵を返す関数。allow_multi なら同じ鍵に複数の走行（セッションを跨いだ中断と再開）を list で持つ。"""
    if key is None:
        tags = {v: k for k, v in T['tags'].items()}

        def key(m):
            phase = tags.get(m.get('tag'))
            if phase == 'identity' or (phase is None and 'stack' in m):
                return (m['stack'], m['scenario'])
            if phase == 'quality' or (phase is None and 'stage' in m):
                # 相手はセッションを跨いで合算しない（裁定 D92・採否表 P261）
                return (m['stage'], m['arm'], m.get('layer'), m.get('coef'), m.get('session'))
            if phase == 'tune' or (phase is None and 'layer' in m and 'arm' in m):
                return (m['scenario'], m['layer'], m['coef'])
            return (m['scenario'],)                # 本走行（選ばれた層 × 係数は manifest の欄にあるが、鍵は場面だけ）
    out = {}
    for d in run_dirs(tag, root):
        rec = _rec(d, allow_dry)
        k = key(rec['manifest'])
        if allow_multi:
            out.setdefault(k, []).append(rec)
        elif k in out:
            raise RuntimeError('同じ鍵の走行が複数: %s（%s と %s）' % (k, out[k]['dir'], d))
        else:
            out[k] = rec
    return out


def cell_counts(trials_path, acc=None, phase='main'):
    """腕ごとの件数（acc に足し込める——中断と再開でセルが複数のセッションにまたがるため）。

    phase は採点欠落の判定に効く（裁定 D103）——本走行は選択の欄、品質床は正答の欄で見る。"""
    out = acc if acc is not None else {}
    for r in iter_jsonl(trials_path, COUNT_FIELDS):
        c = out.setdefault(r['arm'], dict(ZERO))
        c['n'] += 1
        if r['status'] != 'ok':
            c['api_error'] += 1
            continue
        ff, lp, tr = bool(r['format_fail']), bool(r['loop_flag']), bool(r['truncated'])
        c['n_ok'] += 1
        # **「まだ採点していない」と「採点した結果として当てはまらない」を分ける**（裁定 D103・採否表 P306・P319）。
        # 凍結パーサ `is_catastrophic` は refuse に破局の判定を返さない規約なので、破局の欄の空で数えると
        # refuse が全件この札に落ち、確証の族が丸ごと判定不能になる（直しの確認の巡で実際に零になった）。
        # 書式外の試行は判定を持たないのが正しいので、ここには数えない。
        gap = False
        if not ff:
            if (r.get('correct') is None) if phase == 'quality' else (r.get('choice') is None):
                gap = True                         # 判定欄が空（採点前・採点漏れ）——裁定 D96・D103
            # **逆向きの穴も塞ぐ**（裁定 D126・採否表 P363）: 選択が読めているのに破局の判定が空の試行は、
            # 黙って「破局でない」に数えられていた。凍結パーサは登録外の族に None を返すので、
            # 走行器が族を取り違えると率が下がる（起草者に有利な向き）。
            elif phase != 'quality' and r.get('choice') not in (None, 'refuse') and r['catastrophe'] is None:
                gap = True
        # **様式・言及の欄が空の場面の試行も採点欠落に数える**（正本 `response_mode.gap_rule`・2026-09-19）。
        # 前は走行器がこれらを空で書き、ここは空を「該当なし」と数えていたので、様式門が実データでは黙って効かなかった
        # （合成データは欄を埋めていたので検査は通っていた）。書式外の試行も様式は測る（段階 A の (b) は本文の先頭で決める）。
        if phase != 'quality' and any(r.get(k) is None for k in ('style_a', 'style_b', 'mention')):
            c['style_gap'] += 1
            gap = True
        c['scoring_gap'] += gap                    # 一つの試行は一度だけ数える
        c['cat'] += (r['catastrophe'] is True)
        c['refuse'] += (r['choice'] == 'refuse')
        c['ff'] += ff
        c['style_a'] += bool(r['style_a'])
        c['style_b'] += bool(r['style_b'])
        c['mention'] += bool(r['mention'])
        c['loop'] += lp
        c['trunc'] += tr
        c['unmeas'] += (ff or lp or tr)
        c['correct_format_fail'] += (ff and r['correct'] is True)   # 規約違反の検出用（整合検査が止める）
        c['correct'] += (r['correct'] is True and not ff)   # 書式外は不正解に数える（quality_floor.format_fail_rule・採否表 P269）
    return out


def counts_main(T, tag=None, root=None, allow_dry=False):
    """本走行: {(場面, 腕): 件数} と走行の索引。中断と再開でまたがったセルは足し合わせる（正本 sessions.resume_rule）。"""
    tag = tag or T['tags']['main']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc,), recs in idx.items():
        acc = {}
        for rec in recs:
            cell_counts(rec['trials_path'], acc, phase='main')
        for arm, c in acc.items():
            C[(sc, arm)] = c
    return C, idx


def counts_tune(T, tag=None, root=None, allow_dry=False):
    """調整走行: {(場面, 層, 係数, 腕): 件数} と索引。"""
    tag = tag or T['tags']['tune']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc, layer, coef), recs in idx.items():
        acc = {}
        for rec in recs:
            cell_counts(rec['trials_path'], acc, phase='tune')
        for arm, c in acc.items():
            C[(sc, layer, coef, arm)] = c
    return C, idx


def counts_quality(T, tag=None, root=None, allow_dry=False):
    """品質床: {(段, 腕, 層, 係数): 件数} と索引（無操作の相手は層・係数を None で持つ）。"""
    tag = tag or T['tags']['quality']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for k, recs in idx.items():
        acc = {}
        for rec in recs:
            cell_counts(rec['trials_path'], acc, phase='quality')
        for arm, c in acc.items():
            C[(k[0], arm, k[2], k[3], k[4] if len(k) > 4 else None)] = c
    return C, idx


def equivalence_band(n_v, n_r, p0, k, reps=20000, seed=0, q=0.95):
    """**同値の帯**（候補横断の最大統計量・正本 `selection.equivalence_band`・裁定 D98）。

    帰無（全候補が同じ率）で「候補横断の最大と最小の差」を模擬し、その q 分位を帯とする。
    **門と転記行の両方がこの一つの関数を呼ぶ**（裁定 D119・2026-09-18）——
    前は転記行が別の式（差の分散を一候補の二倍で出す素の区間）で ±13.8 pt を印字し、
    しかも **正本の鍵の名を出典に付けていた**。正本の当該の条はその式を「採らない」と明記しており、
    門の模擬は 21.5 pt を出していた（系統外の検分で捕まった・採否表 P339）。
    """
    import math as _m
    import numpy as _np
    rng = _np.random.default_rng(seed)
    sim_v = rng.binomial(max(int(n_v), 1), p0, size=(int(reps), int(k))) / max(int(n_v), 1)
    sim_r = rng.binomial(max(int(n_r), 1), p0, size=(int(reps), int(k))) / max(int(n_r), 1)
    eff = 100.0 * (sim_r - sim_v)
    spread = eff.max(axis=1) - eff.min(axis=1)
    q95 = float(_np.quantile(spread, q))
    half = 1.96 * float(_np.std(spread)) / _m.sqrt(int(reps))
    return {'q95_pt': round(q95, 3), 'reps': int(reps), 'mc_half_pt': round(half, 4), 'null_rate': round(float(p0), 5),
            'k': int(k), 'n_v': int(n_v), 'n_r': int(n_r),
            'rule': '帰無（全候補が同じ）で、候補横断の最大と最小の差が %g 分位に収まる幅。'
                    '最大の候補との差がこの幅の内側の候補を同値として一覧に出す（決め方には使わない）' % q}


def cell_index(T, phase, key):
    """セルの番号（正本 `seeds.cell_index_rule`・裁定 D107）。相ごとに決まった鍵の組の**登録順の添字**（零始まり）。

    同一性選別と本走行は（場面, 腕）、調整走行は（場面, 腕, 層, 係数）、品質床は（段, 腕, 層, 係数）。
    """
    SCEN = list(T['scenarios'])
    LAY, COE = list(T['selection']['candidates']['layers']), list(T['selection']['candidates']['coefficients'])
    ARMS = list(T['arms']['panel'])
    for src in (T['arms']['main'], T['identity_screen'].get('arms_run') or [], T['identity_screen'].get('compared_arms') or []):
        for x in src:
            if x not in ARMS:
                ARMS.append(x)
    # 課題の選定の測定（相 qfcand・裁定 D146）の段は selection・post の後に候補の登録順で足す（前からある段の番号は変わらない）
    STAGES = ['selection', 'post'] + ['candidate:%s' % c['key'] for c in (T['quality_floor'].get('task_candidates') or [])]
    ESC = int(T['seeds']['cell_index_escape'])     # 逃げ道の幅（正本に登録・採否表 P378・前は器の中に手書きしていた）
    def _ai(arm):
        if arm in ARMS:
            return ARMS.index(arm)
        import hashlib as _h
        return len(ARMS) + int(_h.sha256(str(arm).encode('utf-8')).hexdigest()[:8], 16) % ESC   # 登録に無い腕も決定的に一意な番号を持つ
    if phase == 'identity':
        sc, arm = key
        return (SCEN.index(sc) if sc in SCEN else len(SCEN)) * (len(ARMS) + ESC) + _ai(arm)
    if phase == 'main':
        sc, arm = key
        return SCEN.index(sc) * (len(ARMS) + ESC) + _ai(arm)
    if phase == 'tune':
        sc, arm, l, c = key
        return ((SCEN.index(sc) * (len(ARMS) + ESC) + _ai(arm)) * len(LAY) + LAY.index(l)) * len(COE) + COE.index(c)
    if phase == 'quality':
        stage, arm, l, c = key
        li = LAY.index(l) if l in LAY else len(LAY)      # 無操作の相手は層・係数を持たない
        ci = COE.index(c) if c in COE else len(COE)
        return ((STAGES.index(stage) * (len(ARMS) + ESC) + _ai(arm)) * (len(LAY) + 1) + li) * (len(COE) + 1) + ci
    raise SystemExit('相の名が正本に無い: %s' % phase)


def cell_seed(T, run_seed, phase, key):
    """セルの種（正本 `seeds.derivation_formula`・裁定 D107・D99）。"""
    import numpy as _np
    idx = cell_index(T, phase, key)
    return int(_np.random.SeedSequence([int(run_seed), int(T['seeds']['phase_index'][phase]), int(idx)]).generate_state(1)[0])


def trial_seed(cell_s, trial_index):
    """試行の種（正本 `seeds.derivation_formula`）。**記録には書かない**——下の `recorded_seed` を見よ。"""
    import numpy as _np
    return int(_np.random.SeedSequence([int(cell_s), int(trial_index)]).generate_state(1)[0])


def batch_seed(cell_s, batch_index):
    """バッチの種（正本 `seeds.unit_D127`・裁定 D127）。**試行単位の再現は主張しない。**"""
    import numpy as _np
    return int(_np.random.SeedSequence([int(cell_s), int(batch_index)]).generate_state(1)[0])


def retry_seed(cell_s, batch_index, attempt=1):
    """**書式外の引き直しの種**＝`SeedSequence([セルの種, バッチ番号, 引き直しの回])`（正本 `seeds.derivation_formula`・2026-09-19）。
    前は走行器の中で「バッチの種 ＋ 一」と手書きしていた（登録の外の種）。引き直しは一回だけ（凍結走行器の規約）。"""
    import numpy as _np
    return int(_np.random.SeedSequence([int(cell_s), int(batch_index), int(attempt)]).generate_state(1)[0])


def recorded_seed(T, cell_s, trial_index, start=0):
    """**試行の記録に書く種**＝その試行が属する**バッチの種**（裁定 D127・2026-09-19）。

    書く側（走行器・合成データ）と検べる側（整合検査）は**この一つの関数を呼ぶ**。
    前は走行器がバッチの種を書き、整合検査と合成データは試行の種を使っていたので、
    **合成データは整合検査を通り、本物の出力は全件落ちる**形になっていた
    （起草者が裁定 D127 の直しで入れた食い違い・本体を書いて記録を集計に通す段で見つけた）。
    **バッチの区切りはセルの頭（試行の番号 零）から数えた倍数に固定する**——中断して途中から再開しても、
    同じ試行は同じバッチの番号に属し、同じ種を持つ（走行器は区切りをこれに合わせる）。
    """
    return batch_seed(cell_s, int(trial_index) // int(T['runner']['batch']))


def counts_main_by_direction(T, tag=None, root=None, allow_dry=False):
    """本走行の**方向ごと**の件数（正本 `random_control.pooling`・裁定 D110・採否表 P315）。

    合併する前に三本のランダム方向の率を出すために要る。{(場面, 腕, 方向の id): 件数}。"""
    tag = tag or T['tags']['main']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc,), recs in sorted(idx.items()):
        for rec in recs:
            for r in iter_jsonl(rec['trials_path'], COUNT_FIELDS + ('direction_id',)):
                did = r.get('direction_id')
                if did is None:
                    continue
                c = C.setdefault((sc, r['arm'], did), dict(ZERO))
                c['n'] += 1
                if r['status'] != 'ok':
                    c['api_error'] += 1
                    continue
                c['n_ok'] += 1
                c['cat'] += (r['catastrophe'] is True)
                c['ff'] += bool(r['format_fail'])
                c['refuse'] += (r['choice'] == 'refuse')
    return C


def stratum_of(r):
    """様式の層（正本 style_gate.stratified.strata）。JSON 直答なら json_direct・そうでなければ prose。

    **書式外の試行は層に入れない**（答えが読めないので様式も読めない・裁定 D115・採否表 P335〔二体目 G6〕）。
    前は合成データの書式外の行が様式の欄を持っていたため、読めない試行が json_direct の層に入っていた。"""
    if r.get('format_fail'):
        return None
    return 'json_direct' if bool(r.get('style_b')) else 'prose'


def counts_main_strata(T, tag=None, root=None, allow_dry=False):
    """本走行: {(場面, 腕, 層): 件数}（様式門の層別の副次・札は変えない）。"""
    tag = tag or T['tags']['main']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc,), recs in idx.items():
        for rec in recs:
            for r in iter_jsonl(rec['trials_path'], COUNT_FIELDS):
                st_ = stratum_of(r)
                if st_ is None:
                    continue
                k = (sc, r['arm'], st_)
                c = C.setdefault(k, dict(ZERO))
                c['n'] += 1
                if r['status'] != 'ok':
                    c['api_error'] += 1
                    continue
                c['n_ok'] += 1
                c['cat'] += (r['catastrophe'] is True)
                c['refuse'] += (r['choice'] == 'refuse')
                # 書式外の試行は層に入らない（`stratum_of` が None を返して上で飛ばす）ので、書式外は数えない
                # （常に零を足す行があった・採否表 P409・2026-09-19 に消した）
    return C


def load_sessions(root=None):
    """セッション記録（正本 sessions.record）。"""
    out = []
    for p in sorted(glob.glob(os.path.join(results_root(root), 'sessions-B', '*.json'))):
        out.append(read_json(p))
    return out


def sessions_by_run_key(sessions):
    out = {}
    for s in sessions:
        for rk in s.get('run_keys') or []:
            out.setdefault(rk, []).append(s)
    return out


def rate(k, n):
    return (k / n) if n else None


def pt(x):
    return None if x is None else 100.0 * x
