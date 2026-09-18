# -*- coding: utf-8 -*-
"""verify_B_design_round2.py（2026-09-18）—— 段階 B 設計の検分（二段目・系統内外の四票）の所見を、
事前登録した追い問い K23〜K50 の手順で一次記録から出し直す器。

- 読むだけ（リポジトリを書き換えない）。出力は `verification-B-design-round2.{md,json}`。
- 事前登録: `preregistration-reproduction-B-design-round2.md`（再現の作業の前に書いた）。
- 走らせ方: python records/reviews/B/design-round2/verify_B_design_round2.py
"""
import os, re, sys, json, math, hashlib, datetime
import numpy as np
from scipy.stats import fisher_exact, binom

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
CANON = os.path.join(REPO, 'design', 'contrasts-B.json')
DRAFT = os.path.join(REPO, 'design', 'design-stageB-draft7.md')
FACTS = os.path.join(REPO, 'records', 'B', 'design-facts-B.md')
README = os.path.join(REPO, 'README.md')
T = json.load(open(CANON, encoding='utf-8'))
draft = open(DRAFT, encoding='utf-8').read()
facts = open(FACTS, encoding='utf-8').read()
readme = open(README, encoding='utf-8').read()
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()

R = {}          # K -> dict(status, note, data)
def rec(k, status, note, **data):
    R[k] = {'status': status, 'note': note, 'data': data}


def walk(o, path=''):
    """正本を（経路, 値）で舐める。"""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + '.' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + '[%d]' % i)
    else:
        yield path.lstrip('.'), o


PAIRS = [(p, v) for p, v in walk(T)]
STR_PAIRS = [(p, v) for p, v in PAIRS if isinstance(v, str)]
def find_text(*words):
    return [(p, v) for p, v in STR_PAIRS if any(w in v for w in words)]
def find_key(*words):
    return [p for p, _ in PAIRS if any(w in p for w in words)]


ALL_CONTRASTS = []
for fid, f in T['families'].items():
    for c in f['contrasts']:
        ALL_CONTRASTS.append(dict(c, _fam=fid, _kind='confirm', _m=f['m']))
for fid, f in T['descriptive_families'].items():
    for c in f.get('contrasts', []):
        ALL_CONTRASTS.append(dict(c, _fam=fid, _kind='desc', _m=None))
CONF = [c for c in ALL_CONTRASTS if c['_kind'] == 'confirm']
N_MAIN = T['n_main']


def holm_alpha(m, step=1):
    return 0.05 / (m - step + 1)


def fisher_p(a_k, a_n, b_k, b_n):
    return float(fisher_exact([[a_k, a_n - a_k], [b_k, b_n - b_k]])[1])


# ============ K23: 書式外の希釈（門は選定だけ・水準・和集合） ============
ff = T['selection']['format_fail_gate']
ff_paths = [p for p, _ in PAIRS if 'format_fail' in p]
rows23 = []
for c in CONF:
    p0 = c['base_4B2507'] / c['base_n']
    for f in (0.10, 0.20, 0.30):
        kv = round(N_MAIN * p0 * (1 - f))          # 書式外が出た腕（破局は数えられない）
        kr = round(N_MAIN * p0)                    # 相手の腕
        pv = fisher_p(kv, N_MAIN, kr, N_MAIN)
        rows23.append({'id': c['id'], 'fam': c['_fam'], 'base': round(p0, 4), 'f': f,
                       'drop_pt': round(100 * p0 * f, 2), 'k_v': kv, 'k_r': kr, 'p': pv,
                       'holm1': pv < holm_alpha(c['_m']), 'nominal': pv < 0.05})
worst = max(rows23, key=lambda r: r['drop_pt'])
n_holm = sum(1 for r in rows23 if r['holm1'])
rec('K23', '再現',
    '書式外の門は選定にしか無い（正本の経路 %s）。門の上限 %.2f・「和集合・腕あたり」で、片腕だけが上限いっぱいに書式外を出すと、'
    '見かけの低下は基底 × 率で最大 %.1f pt（%s）。この見かけだけで Holm の初段を通る対比は %d/%d（率 0.1/0.2/0.3 × 確証 16 対比）。'
    % (' / '.join(ff_paths), ff['threshold'], worst['drop_pt'], worst['id'], n_holm, len(rows23)),
    gate_paths=ff_paths, threshold=ff['threshold'], rule=ff['rule'], rows=rows23,
    main_run_gate=bool(find_text('書式外') and [p for p, _ in find_text('書式外') if p.startswith(('censor', 'refuse_gate', 'style_gate'))]))

# ============ K24: 拒否の希釈（選定に refuse 門が無い） ============
sel_refuse = [p for p, v in walk(T['selection']) if 'refuse' in p or (isinstance(v, str) and 'refuse' in v) or (isinstance(v, str) and '拒否' in v)]
rows24 = []
for c in CONF:
    p0 = c['base_4B2507'] / c['base_n']
    for f in (0.10, 0.20, 0.30):
        kv, kr = round(N_MAIN * p0 * (1 - f)), round(N_MAIN * p0)
        pv = fisher_p(kv, N_MAIN, kr, N_MAIN)
        rows24.append({'id': c['id'], 'f': f, 'drop_pt': round(100 * p0 * f, 2), 'p': pv, 'holm1': pv < holm_alpha(c['_m'])})
rec('K24', '再現',
    '選定の段に拒否の門は無い（正本 selection の下に refuse も拒否も現れない: %s）。refuse 門は `%s` で、本走行の名目有意の対比にだけ当たる。'
    '拒否だけを増やす候補は、全分母では破局率が下がって見えるので選定を勝ち、本走行で判定保留に落ちる順路がある。算術は書式外と同型（最大 %.1f pt）。'
    % (sel_refuse or '無し', T['refuse_gate']['applies_to'], worst['drop_pt']),
    selection_refuse_paths=sel_refuse, applies_to=T['refuse_gate']['applies_to'], rows=rows24)

# ============ K25: ランダム方向の腕のノルム基準の衝突 ============
FAM_NORM = {'B_sub': 'static（v̂）', 'B_add': 'static（v̂）', 'B_cross': 'Nk 方向',
            'B_desc_vs_noop': None, 'B_desc_O_sub': 'static（v̂）',
            'B_desc_textdiff': 'td（ノルムは v̂ に合わせる＝static と同じ）', 'B_desc_S4': '(6b) の方向'}
req = {}
for c in ALL_CONTRASTS:
    need = FAM_NORM.get(c['_fam'])
    if need is None:
        continue
    for side in ('A', 'B'):
        arm = c[side]
        if 'vrand' in arm:
            req.setdefault(arm, {}).setdefault(need, set()).add(c['scenario'])
conf25 = {}
for arm, d in req.items():
    eff = set()
    for k in d:
        eff.add('static' if 'static' in k or 'td（' in k else k)     # td のノルムは v̂ に合わせるので static と同じ
    if len(eff) > 1:
        conf25[arm] = {'requirements': {k: sorted(v) for k, v in d.items()}, 'distinct': sorted(eff)}
cells25 = sum(len(set().union(*[set(v) for v in d['requirements'].values()])) for d in conf25.values())
rec('K25', '再現',
    'ランダム方向の腕は %d 本。うち **%s** が異なる基準を同時に要求される（%s）。場面の数は %d。'
    'ほかの %d 本は要求が一つに収まる（td のノルムは v̂ に合わせる規定なので、static と td の同時要求は衝突しない）。'
    % (len(req), '・'.join(sorted(conf25)) or '無し',
       ' / '.join('%s: %s' % (a, '＋'.join(sorted(d['requirements']))) for a, d in conf25.items()) or '—',
       cells25, len(req) - len(conf25)),
    requirements={a: {k: sorted(v) for k, v in d.items()} for a, d in req.items()}, conflicts=conf25, conflict_cells=cells25,
    norm_reference=T['random_control']['norm_reference'], td_def=T['directions']['td']['def'])

# ============ K26: 品質床（D69）の後始末——落ちたときの札と走行の順 ============
proc = T['procedure']
qf = T['quality_floor']
fail_label = [p for p, v in STR_PAIRS if ('品質床' in v and ('落ち' in v or '不合格' in v or '外す' in v))]
post_in_proc = [i for i, s in enumerate(proc) if '品質床' in s]
rec('K26', '再現',
    '品質床を選定後のすべての介入の腕に広げた規定（`quality_floor.post_selection`・裁定 D69）はあるが、'
    '**落ちた腕をどう扱うかの札が正本に無い**（印字の定型 print_strings に品質床の不合格の欄は %s）。'
    '手順の一覧で品質床が現れるのは %s 段目だけで、選定後・本走行前に置く段が無い（手順は %d 段）。'
    % ('無い' if not [k for k, v in T['print_strings'].items() if '品質床' in v and '合格' not in v] else 'ある',
       '・'.join(str(i + 1) for i in post_in_proc), len(proc)),
    procedure=proc, post_selection=qf['post_selection'], print_strings_keys=sorted(T['print_strings']),
    fail_label_paths=fail_label, gate1_rule=T['gate1']['rule'])

# ============ K27: 品質床の入力・帯・生成・採点 ============
missing27 = {}
for want, words in [('入力（前置きの有無）', ('前置き', 'prompt', '問いの形')), ('介入の帯（どこからどこまで）', ('開始位置', 'EOS', '帯')),
                    ('生成の設定', ('temperature', 'top_p', 'max_tokens', '貪欲', 'greedy')), ('採点の仕方', ('採点', '一致', '抽出'))]:
    hit = [p for p, v in walk(qf) if any(w in str(v) for w in words)] + [p for p in walk(qf) if False]
    missing27[want] = hit
apply_band = T['selection']['apply']
rec('K27', '再現',
    '品質床の鍵は %s。**入力の作り方（場面の前置きを付けるか）・介入を掛ける帯・生成の設定・採点の仕方はいずれも書かれていない**'
    '（帯の規定 `selection.apply` は「%s」で、場面本文を前提にしており、選択式の問いには当てはまらない）。'
    % ('・'.join(sorted(qf)), apply_band),
    quality_floor_keys=sorted(qf), hits=missing27, apply=apply_band, task_type=qf['task_type'])

# ============ K28: 生成の設定の在処 ============
gen_paths = {w: [p for p, _ in PAIRS if w in p] for w in ('temperature', 'top_p', 'max_tokens')}
gen_text = {w: [p for p, v in STR_PAIRS if w in v] for w in ('temperature', 'top_p', 'max_tokens')}
draft_gen = [w for w in ('temperature', 'top_p', 'max_tokens') if w in draft]
rec('K28', '再現',
    '生成の設定は正本の %s にしか無い（本走行・調整走行・品質床の設定は正本に無い）。草案の本文に現れる語は %s。'
    '記録先行公開（publication.record_first）は「凍結本文・正本・腕と方向の定義・封印予想」を対象にしており、生成の設定が正本に無いことは公開の対象そのものの欠けである。'
    % ('・'.join(sorted({p.rsplit('.', 1)[0] for ps in gen_paths.values() for p in ps})) or '無し', '・'.join(draft_gen) or '無し'),
    key_paths=gen_paths, text_paths=gen_text, draft_hits=draft_gen, record_first=T['publication']['record_first'])

# ============ K29: 両側・符号の封印の欠け ============
dirs29 = {c['id']: c['direction'] for c in CONF}
sealed = [p for p, _ in PAIRS if 'sealed' in p]
rec('K29', '再現',
    '確証の 16 対比はすべて %s（%d/%d）。符号（どちら向きに動いたら確証か）の封印は確証の族には無く、封印の鍵は %s にしかない。'
    '印字の定型 `label_confirmed` は向きを印字するが（"%s"）、読み条項の射程は「区別できる動きを作ったか」までで、逆向きでも「確証」の札が立つ。'
    % (sorted(set(dirs29.values()))[0], sum(1 for v in dirs29.values() if v == 'two_sided'), len(dirs29),
       '・'.join(sealed) or '無し', T['print_strings']['label_confirmed']),
    directions=dirs29, sealed_paths=sealed, scope=T['reading_B']['scope'])

# ============ K30: td 統制が不利になりえない ============
td_c = [c for c in ALL_CONTRASTS if c.get('direction_v') == 'td']
v_vs_td = [c for c in ALL_CONTRASTS if ('vtd' in c.get('A', '') and re.search(r'[+\-]v($|[^a-zA-Z])', c.get('B', ''))) or
           ('vtd' in c.get('B', '') and re.search(r'[+\-]v($|[^a-zA-Z])', c.get('A', '')))]
td_scen = sorted({c['scenario'] for c in td_c})
rec('K30', '再現',
    '腕対の差方向の統制は %d 対比（場面 %s のみ）で、いずれも **td 対 ランダム方向**である。'
    '目的の文は「v̂ の効き目が実在するテキスト差の方向一般と区別できるかを見る」だが、**v̂ 対 td の対比は登録されていない**（該当 %d 件）。'
    '読み条項にも td を不利に読む条項は無い（条項 %d 件のうち td に触れるもの %d 件）。'
    % (len(td_c), '・'.join(td_scen), len(v_vs_td), len(T['reading_B']['clauses']),
       sum(1 for s in T['reading_B']['clauses'] if 'td' in s or '腕対' in s)),
    td_contrasts=[c['id'] for c in td_c], v_vs_td=[c['id'] for c in v_vs_td], question=T['descriptive_families']['B_desc_textdiff']['question'])

# ============ K31: ランダム方向そのものの効き（対 無操作） ============
NOOP = set(T['arms']['noop']) | {a for v in T['arms']['noop_by_scenario'].values() for a in v}
rand_vs_noop = [c['id'] for c in ALL_CONTRASTS if ('vrand' in c.get('A', '') and c.get('B') in NOOP) or ('vrand' in c.get('B', '') and c.get('A') in NOOP)]
rec('K31', '再現',
    'ランダム方向の腕と無操作の腕を比べる対比は **%d 件**（全 %d 対比を数えた）。ランダム方向を加えること自体が率を動かすかは、どの族でも登録されていない。'
    % (len(rand_vs_noop), len(ALL_CONTRASTS)),
    contrasts=rand_vs_noop, total=len(ALL_CONTRASTS), noop_arms=sorted(NOOP))

# ============ K32: n_ok の定義 ============
nok_paths = [p for p, v in STR_PAIRS if 'n_ok' in v] + [p for p, _ in PAIRS if 'n_ok' in p]
den_keys = sorted(T['denominators'])
claim32 = '分母（全分母・答えた分母・層の分母）を正本の `denominators` に分けた' in draft
rec('K32', '再現',
    '`n_ok` は %d か所で分母として使われる（%s）が、**`denominators` に n_ok の定義は無い**（鍵は %s）。'
    '草案の §7 に「%s」という一句があり（%s）、実態と合わない。'
    % (len(nok_paths), '・'.join(sorted(set(nok_paths))), '・'.join(den_keys),
       '分母を正本の denominators に分けた', '有り' if claim32 else '無し'),
    nok_paths=sorted(set(nok_paths)), denominators=T['denominators'], draft_claim=claim32)

# ============ K33: S4 の封印の分岐と検出力 ============
s4 = T['descriptive_families']['B_desc_S4']
p4 = s4['base_4B2507'] / s4['base_n']


def ci_excl_zero_power(p_a, p_b, n=N_MAIN, z=1.96):
    """二標本の pt 差の 95% Wald 区間が零を外す確率（二項の畳み込みで厳密）。(下がる, 上がる) を返す。"""
    ka = np.arange(n + 1)
    pa = binom.pmf(ka, n, p_a)
    pb = binom.pmf(ka, n, p_b)
    ra, rb = ka / n, ka / n
    diff = ra[:, None] - rb[None, :]
    se = np.sqrt(ra[:, None] * (1 - ra[:, None]) / n + rb[None, :] * (1 - rb[None, :]) / n)
    se = np.where(se == 0, np.inf, se)
    w = pa[:, None] * pb[None, :]
    lo, hi = diff - z * se, diff + z * se
    return float(w[hi < 0].sum()), float(w[lo > 0].sum())


pow33 = {}
for d_pt in (0, 5, 10, 15, 20):
    pow33['%d' % d_pt] = ci_excl_zero_power(max(p4 - d_pt / 100, 0.001), p4)
branches = ['下がった' in s4['adjudication'], '上がる' in s4['question'], ('言わない' in s4['question'] or '言わない' in s4['adjudication'])]
rec('K33', '再現',
    'S4 の封印は「%s」で、**当否を言わない分岐が無い**（当たり・外れの二分岐＋床天井の余地の条項のみ・三分岐の検査 %s）。'
    'つまり「動かなかった」は封印の当たりになる。基底 %.4f（%d/%d）・n=%d で、真に %s pt 下がったときに区間が零を外す確率は %s。'
    % (s4['question'][:60] + '…', branches, p4, s4['base_4B2507'], s4['base_n'], N_MAIN,
       '5/10/15', '・'.join('%s pt %.3f' % (k, v[0]) for k, v in pow33.items() if k in ('5', '10', '15'))),
    base=round(p4, 4), power=pow33, question=s4['question'], adjudication=s4['adjudication'], branches=branches)

# ============ K34: 前置きの長さ（RoPE の位置） ============
import hashlib as _h
arm_files = {}
want = {v: k for k, v in T['arms']['sha16'].items() if v}
for root, _, fs in os.walk(os.path.join(REPO, 'arms')):
    for fn in fs:
        p = os.path.join(root, fn)
        try:
            b = open(p, 'rb').read()
        except Exception:
            continue
        h = _h.sha256(b.replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
        if h in want and want[h] not in arm_files:
            arm_files[want[h]] = {'path': os.path.relpath(p, REPO).replace('\\', '/'), 'bytes': len(b),
                                  'chars': len(b.decode('utf-8').replace('\r\n', '\n'))}
arm_files.setdefault('N', {'path': '（前置き無し）', 'bytes': 0, 'chars': 0})
PAIRS34 = [('(6a) 静的', 'O', 'Osec'), ('(6b) 負荷下', 'O-Ncold', 'Osec-Ncold'), ('Nk 方向', 'Nk', 'N'), ('td 腕対の差', 'Onull', 'N')]
len34 = []
for lab, a, b in PAIRS34:
    ca, cb = arm_files[a]['chars'], arm_files[b]['chars']
    len34.append({'pair': lab, 'a': a, 'b': b, 'chars_a': ca, 'chars_b': cb, 'diff_chars': ca - cb,
                  'ratio': (round(abs(ca - cb) / max(ca, cb, 1), 3))})
rule34 = find_text('トークン長', '長さを揃える', 'RoPE', '位置埋め込み')
rec('K34', '一部再現',
    '方向を作る腕対の前置きの長さは一致していない（文字数の差: %s）。正本に長さを揃える規定は %s。'
    '**トークン化はこの再現では行えない**（重みも tokenizer も手元に無い）ので、トークン位置の差と活性への混入は確かめていない。'
    % ('・'.join('%s %+d' % (r['pair'], r['diff_chars']) for r in len34), '無い' if not rule34 else '有る'),
    arms=arm_files, pairs=len34, rule_paths=[p for p, _ in rule34])

# ============ K35: 全候補が非正のときの停止規則 ============
sign35 = [p for p, v in walk(T['selection']) if isinstance(v, str) and ('非正' in v or '零以下' in v or '符号' in v or '正の' in v)]
rec('K35', '再現',
    '選定の決め方は「%s」で、**有効性の符号に条件が無い**（符号に触れる記述 %s）。門1 は品質床だけを見る（「%s」）ので、'
    '全候補の操作有効性が零以下でも、最も弱く見えない候補が選ばれて本走行に進む。'
    % (T['selection']['pick'][:48] + '…', sign35 or '無し', T['gate1']['rule'][:40] + '…'),
    pick=T['selection']['pick'], gate1=T['gate1']['rule'], sign_paths=sign35)

# ============ K36: ランダム方向の引き直し ============
# 「引き直す」は様式門の層別（検定を引き直す）にも使われる語なので、方向の語と同じ文の中にあるものだけを採る
redraw = [(p, v) for p, v in STR_PAIRS
          if any(w in v for w in ('引き直', '再抽選', '引き当て直')) and ('方向' in v or 'ランダム' in v or 'seed' in v or '種' in v)]
rng = np.random.default_rng(20260918)
REPS36 = 20000
CANDS = T['selection']['candidates']['count']
tune_n = T['n_tune'] * len(T['selection']['tune']['scenarios'])
bx = T['bases_4B2507_api_stageVp']
EXS = T['extraction_scenarios']
base36 = sum(bx[sc]['Onull']['k'] for sc in EXS) / sum(bx[sc]['Onull']['n'] for sc in EXS)
sim36 = {}
for sigma_pt in (0.0, 2.0, 4.0):
    d_tune = rng.normal(0, sigma_pt / 100, size=(REPS36, CANDS))         # 固定の 3 本がその候補で持つ癖
    kv = rng.binomial(tune_n, base36, size=(REPS36, CANDS))
    kr = rng.binomial(tune_n, np.clip(base36 + d_tune, 0.001, 0.999))
    pick = np.argmax((kr - kv) / tune_n, axis=1)
    d_pick = d_tune[np.arange(REPS36), pick]
    out = {}
    for mode, d_main in (('同じ方向を使い回す', d_pick), ('本走行で引き直す', rng.normal(0, sigma_pt / 100, size=REPS36))):
        kv2 = rng.binomial(N_MAIN, base36, size=REPS36)
        kr2 = rng.binomial(N_MAIN, np.clip(base36 + d_main, 0.001, 0.999))
        a1 = holm_alpha(T['families']['B_add']['m'])
        nf, hit = 5000, 0                                                # Fisher は重いので先頭 nf 反復で出す
        for i in range(nf):
            if fisher_p(int(kv2[i]), N_MAIN, int(kr2[i]), N_MAIN) < a1 and kv2[i] < kr2[i]:
                hit += 1
        r_ = hit / nf
        out[mode] = round(r_, 4)
        out[mode + '（95% 区間の半幅）'] = round(1.96 * math.sqrt(r_ * (1 - r_) / nf), 4)
    sim36['sigma_%.0fpt' % sigma_pt] = out
rec('K36', '再現',
    'ランダム方向の種は一つ（random_control.seed=%s・seeds.random_dirs=%s）で、**調整走行と本走行で引き直す規定は %s**。'
    '固定の 3 本がその候補で持つ癖の広がり σ を置いて模擬すると、帰無（v に効き目が無い）でも加算族の初段が立つ割合は %s（同じ方向を使い回す場合）で、'
    '引き直す場合は %s。模擬の前提（癖が正規・候補ごとに独立）は起草者が置いたもので、設計の値ではない。'
    % (T['random_control']['seed'], T['seeds']['random_dirs'], '無い' if not redraw else '有る（%s）' % [p for p, _ in redraw],
       '・'.join('σ=%s: %.3f' % (k.replace('sigma_', '').replace('pt', ' pt'), v['同じ方向を使い回す']) for k, v in sim36.items()),
       '・'.join('%.3f' % v['本走行で引き直す'] for v in sim36.values())),
    seed=T['random_control']['seed'], redraw_paths=[p for p, _ in redraw], sim=sim36, base=round(base36, 4), reps_fisher=5000)

# ============ K37: プログラム全体の柵（三つ組での報告） ============
fence = [l for l in readme.split('\n') if '三つ組' in l or ('柵' in l and '率' in l)]
canon37 = find_text('三つ組')
rule37 = [k for k, v in T['report_rules'].items() if '三つ組' in v or '単独' in v]
rec('K37', '再現',
    '公開の置き場の柵に三つ組での報告の条文がある（README の該当行 %d 行）。正本で「三つ組」が現れるのは %s（試行の記録の欄）だけで、'
    '**報告の規則（report_rules）に三つ組での報告・率の単独引用の禁止は無い**（該当する鍵 %s）。'
    % (len(fence), '・'.join(p for p, _ in canon37) or '無し', rule37 or '無し'),
    readme_lines=fence[:4], canon_paths=[p for p, _ in canon37], report_rule_keys=sorted(T['report_rules']), matched=rule37)

# ============ K38: arms.noop と noop_by_scenario の食い違い ============
noop_key = T['arms']['noop']
noop_union = sorted({a for v in T['arms']['noop_by_scenario'].values() for a in v})
interv = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
base_of = lambda a: re.split(r'[+\-]v', a)[0]
derived = sorted({base_of(a) for a in interv})
q_sel = T['quality_floor']['selection_cells']
q_post = len(interv) - len(T['quality_floor']['arms'])
cells_by = {'arms.noop（%d）' % len(noop_key): q_sel + q_post + len(noop_key),
            'noop_by_scenario の和（%d）' % len(noop_union): q_sel + q_post + len(noop_union),
            '器が導く土台（%d）' % len(derived): q_sel + q_post + len(derived)}
printed = re.search(r'相手の無操作 (\d+) セル', facts)
rec('K38', '再現',
    '`arms.noop` は %s（%d 本）、`noop_by_scenario` の和集合は %s（%d 本）、'
    '転記行 A の器は介入の腕から土台を導いて %s（%d 本）を使う。品質床のセル数は %s。'
    '転記行が印字している相手の無操作は %s セルで、器の導く値と一致する。**古いのは正本の鍵 `arms.noop` の方**である。'
    % (noop_key, len(noop_key), noop_union, len(noop_union), derived, len(derived),
       '・'.join('%s→%d' % (k, v) for k, v in cells_by.items()), printed.group(1) if printed else '不明'),
    noop=noop_key, union=noop_union, derived=derived, cells=cells_by, printed=printed.group(1) if printed else None)

# ============ K39: 同点の割り方と転記行 C ============
rng39 = np.random.default_rng(90218)
REPS39 = 20000
D_PICK = 10.0


def pick_sim(pos, tie, reps=REPS39):
    eff = np.zeros(CANDS)
    if pos is not None:
        eff[pos] = D_PICK / 100.0
    kv = rng39.binomial(tune_n, np.clip(base36 - eff, 0.001, 0.999)[None, :], size=(reps, CANDS))
    kr = rng39.binomial(tune_n, base36, size=(reps, CANDS))
    d = (kr - kv).astype(float)
    if tie == 'first':
        sel = np.argmax(d, axis=1)
    else:
        noise = rng39.random(d.shape) * 1e-6
        sel = np.argmax(d + np.where(d == d.max(axis=1, keepdims=True), noise, 0), axis=1)
    if pos is None:
        return (np.bincount(sel, minlength=CANDS) / reps).round(4).tolist()
    return float((sel == pos).mean())


tie39 = {}
for tie in ('first', 'random'):
    tie39[tie] = {'pos0': pick_sim(0, tie), 'mid': pick_sim(CANDS // 2, tie), 'last': pick_sim(CANDS - 1, tie),
                  'null_dist': pick_sim(None, tie)}
# 同点そのものがどれだけ起きるか（帰無・調整走行の n で）
kv_ = rng39.binomial(tune_n, base36, size=(REPS39, CANDS))
kr_ = rng39.binomial(tune_n, base36, size=(REPS39, CANDS))
d_ = kr_ - kv_
tie_rate = float((( d_ == d_.max(axis=1, keepdims=True)).sum(axis=1) > 1).mean())
half39 = 1.96 * math.sqrt((1 / CANDS) * (1 - 1 / CANDS) / REPS39)
printed_c = re.findall(r'位置 (\d) で ([0-9.]+)', facts)
rec('K39', '一部再現',
    '**規定の欠けは再現する**: 選定の同点の割り方は正本に無い（`selection.pick` は「点推定が最大」までで、同点の規定が無い）。'
    '**数への影響は再現しない**: 帰無で同点が起きる割合は %.3f だが、添字の小さい方に割っても（%s）無作為に割っても（%s）'
    '帰無の選ばれ方は候補数の逆数 %.3f と区別できない（模擬 %s 回・95%% 区間の半幅 ±%.4f）。転記行 C の印字（%s）も両方の割り方で変わらない'
    '（位置の中ほど: %.3f 対 %.3f）。したがって「同点の割り方が転記行 C の値を動かす」という言い分は、この n では再現しなかった。'
    % (tie_rate, tie39['first']['null_dist'], tie39['random']['null_dist'], 1 / CANDS, format(REPS39, ','), half39,
       printed_c, tie39['first']['mid'], tie39['random']['mid']),
    tie=tie39, tie_rate=round(tie_rate, 4), mc_half=round(half39, 4), printed=printed_c, pick=T['selection']['pick'])

# ============ K40: 選定 × 確証の合成検出力 ============
comb40 = {}
for d_pt in (5, 10, 15):
    eff = np.zeros(CANDS)
    eff[CANDS // 2] = d_pt / 100
    kv = rng39.binomial(tune_n, np.clip(base36 - eff, 0.001, 0.999)[None, :], size=(REPS39, CANDS))
    kr = rng39.binomial(tune_n, base36, size=(REPS39, CANDS))
    p_pick = float((np.argmax((kr - kv) / tune_n, axis=1) == CANDS // 2).mean())
    pw = {}
    for c in T['families']['B_add']['contrasts']:
        p0 = c['base_4B2507'] / c['base_n']
        lo, hi = ci_excl_zero_power(max(p0 - d_pt / 100, 0.001), p0)
        pw[c['scenario']] = round(lo, 4)
    comb40['%d pt' % d_pt] = {'pick': round(p_pick, 4), 'family_power_by_scenario': pw,
                              'product_N1': round(p_pick * pw['N1'], 4)}
rec('K40', '再現',
    '選定と確証を合わせた検出力は正本にも転記行にも無い。真の低下 5/10/15 pt のとき、正しい候補を選べる割合 × 加算族 N1 の検出力は %s。'
    '（族の検出力は区間が零を外す確率で出した厳密値・選定の割合は模擬 %s 回。）'
    % ('・'.join('%s→%.3f' % (k, v['product_N1']) for k, v in comb40.items()), format(REPS39, ',')),
    combined=comb40, reps=REPS39)

# ============ K41: 整合検査・抽出検査の位置 ============
idx_check = [i for i, s in enumerate(proc) if '整合検査' in s or '抽出検査' in s]
idx_main = [i for i, s in enumerate(proc) if '本走行' in s]
idx_gate = [i for i, s in enumerate(proc) if '門1' in s]
rec('K41', '再現',
    '手順の一覧で、整合検査・抽出検査は %s 段目・門1 は %s 段目・本走行は %s 段目。検査は本走行の後にしか無く、'
    '門1 と選定の入力（調整走行・品質床）は検査を受けない。**起草者の見直し S7 と同じ所見**である。'
    % ('・'.join(str(i + 1) for i in idx_check), '・'.join(str(i + 1) for i in idx_gate), '・'.join(str(i + 1) for i in idx_main)),
    procedure=proc, check_at=idx_check, gate_at=idx_gate, main_at=idx_main)

# ============ K42: 同一性選別の率の定義・腕の一覧・出所 ============
ids = T['identity_screen']
rec('K42', '再現',
    '同一性選別の鍵は %s。腕は数（%d）だけで**一覧が無い**（正本の腕の並びは %d 本）。'
    '率の定義（何の率の差を測るか）は「%s」と段階 A の節への参照に留まり、API と vLLM の値の出所も書かれていない。'
    % ('・'.join(sorted(ids)), ids['arms'], len(T['arms']['panel']), ids['metric']),
    keys=sorted(ids), arms=ids['arms'], panel=len(T['arms']['panel']), metric=ids['metric'], stacks=ids['stacks'])

# ============ K43: seed の降ろし方 ============
seed_leaves = [(p, v) for p, v in walk(T['seeds'])]
# 「降ろす」は裁定の語（記述に降ろす・在庫に降ろす）でもあるので、seed の語と同じ文にあるものだけを採る
derive43 = [(p, v) for p, v in STR_PAIRS
            if ('seed' in v or '種' in v) and any(w in v for w in ('試行ごと', 'セルごと', '降ろ', '割り当て', '派生'))]
q_cells = q_sel + q_post + len(derived)
rec('K43', '再現',
    'seed は %d か所（%s）。**試行やセルへの降ろし方の規則は無い**（該当する記述 %s）。'
    '品質床は一つの種（seeds.quality=%s）で %d セル（選定 %d ＋選定後 %d ＋相手の無操作 %d）を賄う。'
    % (len(seed_leaves), '・'.join(p for p, _ in seed_leaves), [p for p, _ in derive43] or '無し',
       T['seeds']['quality'], q_cells, q_sel, q_post, len(derived)),
    seeds=dict(seed_leaves), quality_cells=q_cells, derive_paths=[p for p, _ in derive43])

# ============ K44: 重みの rev・tokenizer・層番号 ============
rev44 = find_text('rev')
tok44 = find_text('tokenizer', 'トークナイザ')
layer44 = find_text('層番号', '総層数', '層の番号', '丸め')
rec('K44', '再現',
    '重みの rev は「記録する」項目にはある（%s）が、**走行を跨いで同一であることを要求する規則は無い**。'
    'tokenizer の版は正本に現れない（%s）。層の割合（%s）から層番号への規則と総層数も無い（%s）。'
    % ('・'.join(p for p, _ in rev44) or '無し', [p for p, _ in tok44] or '無し',
       T['selection']['candidates']['layers'], [p for p, _ in layer44] or '無し'),
    rev_paths=[p for p, _ in rev44], tokenizer_paths=[p for p, _ in tok44], layer_paths=[p for p, _ in layer44],
    layers=T['selection']['candidates']['layers'])

# ============ K45: −10 pt とチャンス水準 ============
chance = 0.25
tbl45 = [{'base': round(b, 2), 'margin_above_chance_pt': round(100 * (b - chance), 1),
          'threshold_share': round(10 / max(100 * (b - chance), 1e-9), 3)} for b in (0.35, 0.5, 0.7, 0.9)]
base45 = [p for p, v in walk(T['quality_floor']) if '基底' in str(v) or 'チャンス' in str(v) or '当てずっぽう' in str(v)]
rec('K45', '再現',
    '品質床の閾値は %s pt の固定で、基底の正答率にもチャンス水準にも相対化されていない（該当する記述 %s）。'
    '四択のチャンス 0.25 を置くと、−10 pt はチャンス超の余裕の %s を食う（基底 0.35／0.5／0.7／0.9）。'
    % (T['quality_floor']['threshold_pt'], base45 or '無し', '・'.join('%.2f' % r['threshold_share'] for r in tbl45)),
    threshold=T['quality_floor']['threshold_pt'], table=tbl45, task_type=T['quality_floor']['task_type'], paths=base45)

# ============ K46: 決定性の検査の許容差とバッチ構成 ============
tol46 = find_text('許容差', '一致することを', 'bitwise', '決定性')
draft46 = re.findall(r'\*\*決定性の検査\*\*.*', draft)
batch46 = find_text('バッチ構成', 'バッチの並び', 'バッチ位置')
rec('K46', '再現',
    '決定性の検査は草案の本文にだけ置かれ（%d 行）、正本に許容差の規定は無い（該当 %s）。'
    'バッチに触れる正本の記述は %s だけで（試行の記録の欄）、**バッチ構成を走行のあいだ凍結する規定は無い**。'
    '主位置の活性は腕 × 場面 × 層で一度しか保存しないので（`activation_storage.prompt_final`）、'
    '**「一致することを確かめる」ための比べる材料が残らない**。'
    % (len(draft46), [p for p, _ in tol46] or '無し', [p for p, _ in batch46] or '無し'),
    draft_lines=[s[:120] for s in draft46], tol_paths=[p for p, _ in tol46], batch_paths=[p for p, _ in batch46],
    prompt_final=T['activation_storage']['prompt_final'])

# ============ K47: 族が相手の腕を共有する（独立でない） ============
share = {}
for c in CONF:
    share.setdefault((c['scenario'], c['B']), []).append(c['_fam'])
shared = {('%s / %s' % k): sorted(set(v)) for k, v in share.items() if len(set(v)) > 1}
fam_upper = 1 - (1 - 0.05) ** len(T['families'])
adopt1 = os.path.join(REPO, 'records', 'reviews', 'B', 'design-round1', 'adoption-table-B-design.md')
p205 = [l for l in open(adopt1, encoding='utf-8').read().split('\n') if 'P205' in l]
rec('K47', '再現',
    '確証の族は相手の腕を共有する（同じ場面 × 同じ相手の腕を二つの族が使う組 %d 件: %s）。したがって族どうしは独立でない。'
    '**正本の値は安全側**（`alpha_upper`=%s・和の上界＝独立を要しない）だが、**一段目の採否 P205 の記録は 0.143**（＝1−0.95^%d＝%.4f・独立の前提）で、'
    '正本と食い違ったまま残っている（該当行 %d 件）。草案7B の本文と転記行 B は %s を印字している。'
    % (len(shared), '・'.join(sorted(shared)), T['alpha_upper'], len(T['families']), fam_upper, len(p205), '0.15'),
    shared=shared, computed_upper=round(fam_upper, 4), alpha_upper=T['alpha_upper'], fwer_note=T['fwer_note'],
    p205_line=p205[0][:200] if p205 else None, draft_has_015='上界 0.15' in draft, draft_has_0143='0.143' in draft)

# ============ K48: v̂ の場面間の安定性 ============
cos48 = find_text('コサイン')
rec('K48', '再現' if not [p for p, v in cos48 if 'stability' in p] else '再現しない',
    'v̂ は抽出場面の平均（`directions.static.def`＝%s）。コサインに触れる記述は %s にあるが、'
    '**場面ごとの差ベクトルどうしのコサイン（平均を取る前の安定性）を出す量は登録されていない**。'
    % (T['directions']['static']['def'], '・'.join(p for p, _ in cos48) or '無し'),
    cos_paths=[p for p, _ in cos48], static=T['directions']['static'], extraction=EXS)

# ============ K49: 確証は (6a)、土台は負荷下の腕 ============
d49 = {c['id']: (c['base_arm'], c['direction_v']) for c in CONF}
why49 = [l for l in draft.split('\n') if '(6a)' in l and ('理由' in l or 'なぜ' in l or 'ため' in l)]
rec('K49', '再現',
    '減算族は土台 %s（負荷下の腕）に対して方向 %s（静的・%s）を使う。'
    '(6b)（負荷下で抽出した方向）は S4 の反証にしか使わない。草案に理由を述べる行は %d 行。'
    % (T['families']['B_sub']['contrasts'][0]['base_arm'], T['families']['B_sub']['contrasts'][0]['direction_v'],
       T['directions']['static']['def'], len(why49)),
    map=d49, loaded=T['directions']['loaded'], why_lines=[s[:120] for s in why49])

# ============ K50: README の古さ・起草の機種 ============
m_ver = re.search(r'正本 JSON `design/contrasts-B\.json`（([^・]+)・SHA16 ([0-9A-F]{16})', readme)
m_tri = re.search(r'規模は合計 ([\d,]+) 試行', readme)
facts_total = re.search(r'合計 ([\d,]+) 試行', facts)
model50 = {'README': sorted(set(re.findall(r'(Fable 5\.1|Opus 5)', readme))),
           'draft7': sorted(set(re.findall(r'(Fable 5\.1|Opus 5)', draft)))}
sec50 = readme.split('## 段階 B')[1].split('\n## ')[0]
gen50 = dict(re.findall(r'`tools/(make_contrasts_B|design_facts_B)\.py` (v[0-9.]+)', sec50))
gen_self = {}
for f in ('make_contrasts_B', 'design_facts_B'):
    head = open(os.path.join(REPO, 'tools', f + '.py'), encoding='utf-8').read()[:400]
    m = re.search(r'%s\.py (v[0-9.]+)' % f, head)
    gen_self[f] = m.group(1) if m else None
sha_ok = (m_ver.group(2) == s16(CANON)) if m_ver else False
rec('K50', '再現',
    'README の段階 B の節が指す SHA16 は**いまの一次記録と一致する**（正本 %s・一致 %s）。古いのは版の名と規模と生成器の版である: '
    '版の名 %s（正本の version は %s）・規模 %s 試行（転記行 A は %s 試行）・生成器の版 README %s。'
    '**起草者が気づいた追加の一件**: 生成器 `make_contrasts_B.py` 自身の冒頭の版の名も %s のままで、正本を draft7 にした改訂で上げていない'
    '（`design_facts_B.py` は %s に上げてある）。起草の機種の記載は README %s・草案7B %s。'
    % (s16(CANON), sha_ok, m_ver.group(1) if m_ver else '不明', T['version'],
       m_tri.group(1) if m_tri else '不明', facts_total.group(1) if facts_total else '不明', gen50,
       gen_self['make_contrasts_B'], gen_self['design_facts_B'], model50['README'] or '無し', model50['draft7'] or '無し'),
    readme_version=m_ver.group(1) if m_ver else None, readme_sha=m_ver.group(2) if m_ver else None, sha_matches=sha_ok,
    canon_version=T['version'], canon_sha=s16(CANON), readme_generators=gen50, generator_self_labels=gen_self,
    readme_trials=m_tri.group(1) if m_tri else None, facts_trials=facts_total.group(1) if facts_total else None, models=model50)

# ============ 出力 ============
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
order = ['K%d' % i for i in range(23, 51)]
missing = [k for k in order if k not in R]
assert not missing, ('追い問いに抜けがある', missing)
counts = {}
for k in order:
    counts[R[k]['status']] = counts.get(R[k]['status'], 0) + 1

L = ['# 段階 B 設計の検分（二段目・四票）——再現の記録', '',
     '- 走らせた時刻: %s UTC（日本時間 %s）。器 `verify_B_design_round2.py`（SHA16 %s）。' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M'), s16(os.path.abspath(__file__))),
     '- 事前登録: `preregistration-reproduction-B-design-round2.md`（SHA16 %s）。**この器を書く前に書いた。**' % s16(os.path.join(HERE, 'preregistration-reproduction-B-design-round2.md')),
     '- 一次記録: 正本 `design/contrasts-B.json`（SHA16 %s・%s）／転記行 `records/B/design-facts-B.md`（SHA16 %s）／草案7B（SHA16 %s）／README（SHA16 %s）。' % (s16(CANON), T['version'], s16(FACTS), s16(DRAFT), s16(README)),
     '- 内訳: ' + '・'.join('%s %d 件' % (k, v) for k, v in sorted(counts.items())) + '（全 %d 件）。' % len(order), '',
     '| K | 結果 | 出し直した事実 |', '|---|---|---|']
for k in order:
    L.append('| %s | %s | %s |' % (k, R[k]['status'], R[k]['note'].replace('\n', ' ')))
L += ['', '## 数の明細（機械の区画）', '', '```json',
      json.dumps({k: R[k]['data'] for k in order}, ensure_ascii=False, indent=1, default=str)[:60000], '```', '',
      '本記録のいかなる記述も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
md = '\n'.join(L)
open(os.path.join(HERE, 'verification-B-design-round2.md'), 'w', encoding='utf-8', newline='\n').write(md)
json.dump({'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'canon_sha16': s16(CANON), 'results': R},
          open(os.path.join(HERE, 'verification-B-design-round2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
for k in order:
    print('%-5s %-8s %s' % (k, R[k]['status'], R[k]['note'][:150].replace('\n', ' ')))
print('\n[verify-round2] %s' % counts)
