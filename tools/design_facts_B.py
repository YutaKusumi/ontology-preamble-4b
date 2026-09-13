# -*- coding: utf-8 -*-
"""design_facts_B.py v1 —— 段階 B の設計事実（転記行 A〜I）を `design/contrasts-B.json` と門0 の係数から機械生成する（2026-09-13）。
A 規模／B 対比／C 保留 AUC の置換帯と門1 の誤判率（シミュレーション）／D v 対 v_random の検出力（両側 Fisher・n=200・Holm）／E 品質床の閾値の単位・帰無発火率・検出力／F 費用と時間／G 凍結射程と器材の対応表／H seed・tag／I 活性保存の容量と収容（見積り・◐）。
出力: records/B/design-facts-B.md と同 .json。
"""
import os, sys, json, math, hashlib, datetime
import numpy as np
from scipy.stats import fisher_exact, binom, norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vprime_power import make_power
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8')); n = T['n_main']; nt = T['n_tune']; SC = T['scenarios']
HF = json.load(open(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'), encoding='utf-8'))
rng = np.random.default_rng(20260913); sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper(); F = {}
# ---- A: 規模
arms_main = {'sub': ['O-Ncold-v', 'O-Ncold-vrand', 'O-Ncold'], 'add': ['Onull+v', 'Onull+vrand', 'Onull'], 'cross': ['O-Ncold+vNk', 'Onull+vNk'], 'O_sub_desc': ['O-v', 'O-vrand', 'O']}
n_main_arms = sum(len(v) for v in arms_main.values()); t_main = len(SC) * n_main_arms * n + 3 * n   # ＋S4 反証 3 腕
t_id = 13 * T['identity_screen']['n']; t_tune = 6 * 2 * nt * 2 + 3 * 2 * nt * 2   # 6 候補 × 2 腕（O・Osec）× n=40 × 2（抽出・保留は同じ試行を分割・ここでは上限として 2 場面）＋係数 3 段 × 2 腕（Onull+v・+vrand）× 40 × 2 場面
t_q = T['quality_floor']['items'] * (4 + 3 * 2)   # 品質床: 4 腕＋方向の加減 3 係数 × 2
F['A'] = {'text': '規模: 同一性選別（transformers 経路）%s／調整走行 %s（6 候補 × O・Osec × n=40 × 抽出場面 2＋係数 3 段 × 2 腕 × 40 × 2 場面・上限）／本走行 %s（4 場面 × %d 腕 × n=200＋S4 反証 3 腕 × 200）／品質床 %s 問（200 問 × 10 腕・係数）＝**合計 %s 試行**。隠れ状態の保存は調整走行と本走行の全試行（容量は転記行 I）。' % (
    format(t_id, ','), format(t_tune, ','), format(t_main, ','), n_main_arms, format(t_q, ','), format(t_id + t_tune + t_main + t_q, ',')), 'data': {'identity': t_id, 'tune': t_tune, 'main': t_main, 'quality': t_q}}
# ---- B
fam = T['families']; F['B'] = {'text': '対比: 確証 %d（減算 %d・加算 %d・交差 %d・v 対 v_random・両側 Fisher・全分母・Holm を族ごと・上界 0.15）・記述 %d（無操作との差 8・O 減算 4・S4 反証 1・層別・用量・様式）・ランダム方向 %d 本（合併して一腕）・id 重複 0。土台の 4B-2507 既測（V′・全分母）: O-Ncold %s／Onull %s。' % (
    sum(x['m'] for x in fam.values()), fam['B_sub']['m'], fam['B_add']['m'], fam['B_cross']['m'], sum(len(v.get('contrasts', [])) for v in T['descriptive_families'].values()), T['random_control']['count'],
    '・'.join('%s %d/%d' % (sc, T['bases_4B2507_api_stageVp'][sc]['O-Ncold']['k'], T['bases_4B2507_api_stageVp'][sc]['O-Ncold']['n']) for sc in SC), '・'.join('%s %d/%d' % (sc, T['bases_4B2507_api_stageVp'][sc]['Onull']['k'], T['bases_4B2507_api_stageVp'][sc]['Onull']['n']) for sc in SC))}
# ---- C: 保留 AUC の置換帯と門1 の誤判率（保留 20 × 2 腕・ラベル置換 B=10,000）
def auc(x, y):
    return float((x[:, None] > y[None, :]).mean() + 0.5 * (x[:, None] == y[None, :]).mean())
h = T['gate1']['holdout_per_arm']; B = 2000
null_auc = []
for _ in range(B):
    x = rng.normal(size=h); y = rng.normal(size=h); null_auc.append(auc(x, y))
band = float(np.quantile(null_auc, 0.95)); power = {}
for true_auc in (0.6, 0.7, 0.8):
    d = math.sqrt(2) * norm.ppf(true_auc); hits = 0
    for _ in range(B):
        x = rng.normal(d, 1, h); y = rng.normal(0, 1, h); hits += auc(x, y) > band
    power[str(true_auc)] = round(hits / B, 3)
F['C'] = {'text': '保留 AUC の置換帯（保留 20 試行 × 2 腕・正規近似で B=%d の帰無標本・片側 95%%）: 帯 %.3f。真の AUC 0.6／0.7／0.8 のとき帯の外に出る確率 %.2f／%.2f／%.2f。**門1 が閉じたとき、真の AUC 0.6 なら約 %d%% は「試行数の不足」であり「方向の非存在」と書き分ける**（凍結前に保留試行数を増やすかは裁定・n=40 の分割は設計定数）。' % (B, band, power['0.6'], power['0.7'], power['0.8'], round(100 * (1 - power['0.6']))), 'data': {'band': band, 'power': power, 'holdout': h}}
# ---- D: v 対 v_random の検出力（両側 Fisher・n=200・Holm 初段 α/8）
pw = make_power(n); rows = []
for base in (0.13, 0.30, 0.50, 0.70):
    for d in (0.10, 0.15, 0.20, 0.30):
        for alpha, lab in ((0.05, 'nominal'), (0.05 / 8, 'holm_first_m8')):
            p2 = min(base + d, 0.99); rows.append({'base': base, 'delta_pt': d, 'alpha': lab, 'power': round(pw(base, p2, alpha) if callable(pw) else float('nan'), 3)})
F['D'] = {'text': 'v 対 v_random の検出力（両側 Fisher・n=200 対 200・全数列挙）: 基底 0.13（O-Ncold N1）で ±15pt %.2f（名目）／%.2f（Holm 初段 m=8）・±20pt %.2f／%.2f。基底 0.5 で ±15pt %.2f／%.2f・±20pt %.2f／%.2f。±10pt は基底 0.5 で %.2f（名目）——検出域外。' % tuple(
    next(r['power'] for r in rows if r['base'] == b and r['delta_pt'] == d and r['alpha'] == a) for b, d, a in [(0.13, 0.15, 'nominal'), (0.13, 0.15, 'holm_first_m8'), (0.13, 0.20, 'nominal'), (0.13, 0.20, 'holm_first_m8'), (0.50, 0.15, 'nominal'), (0.50, 0.15, 'holm_first_m8'), (0.50, 0.20, 'nominal'), (0.50, 0.20, 'holm_first_m8'), (0.50, 0.10, 'nominal')]), 'data': rows}
# ---- E: 品質床
q = T['quality_floor']['items']; thr = -T['quality_floor']['threshold_pt'] / 100
def null_fire_q(p):   # 同じ真の正答率 p の二腕で差が −10pt 以下になる確率（二項・独立）
    a = rng.binomial(q, p, 20000); b = rng.binomial(q, p, 20000); return float(((b - a) / q <= -thr).mean())
def power_q(p, drop):
    a = rng.binomial(q, p, 20000); b = rng.binomial(q, max(p - drop, 0.01), 20000); return float(((b - a) / q <= -thr).mean())
F['E'] = {'text': '品質床（200 問・−10pt・分子＝正答数・分母＝200・集計単位＝腕 × 係数）: 帰無発火率（同じ真の正答率で −10pt 以下になる確率）は正答率 0.5 で %.3f・0.7 で %.3f・0.9 で %.3f。真の低下 15pt を捕まえる確率は 0.7 で %.2f・0.9 で %.2f。判定単位は 3 係数 × 4 腕＝12 セルで、帰無での誤って不合格にする期待セル数は 0.7 で %.2f。' % (
    null_fire_q(0.5), null_fire_q(0.7), null_fire_q(0.9), power_q(0.7, 0.15), power_q(0.9, 0.15), 12 * null_fire_q(0.7))}
# ---- F: 費用（L4 の料率・transformers 経路は vLLM より遅い——係数 3 を仮定 ◐）
units_h, tph, setup = 2.67, 3839, 512; slow = 3.0
tr = t_id + t_tune + t_main + t_q; hrs = tr * slow / tph; sess = math.ceil(hrs / (8 - setup / 3600)); h_tot = hrs + sess * setup / 3600; u = h_tot * units_h
F['F'] = {'text': '費用と時間（門0 の L4 係数 2.67 ユニット/h・3,839 試行/h・経費 512 s × transformers 経路の遅さの仮定 %.0f 倍 ◐・セッション 8 時間）: %s 試行 ≈ %.1f 時間・%d セッション・**≈%.0f ユニット**。活性保存の容量と時間は調整走行の最初のセッションで実測し置換（v2.3 §6 の見込み B ≈5〜6 と同じ桁）。' % (slow, format(tr, ','), h_tot, sess, u), 'data': {'trials': tr, 'hours': round(h_tot, 1), 'units': round(u, 1)}}
# ---- G・H・I
F['G'] = {'text': '凍結射程と器材の対応表: 腕・場面・族・選定規則→contrasts-B.json／同一性→identity_screen（A と共用）／抽出・AUC・置換→extract_B.py／加減・ランダム・品質床・強制デコード→steer_B.py／族・検閲・refuse 門・様式門→analyze_B.py／転記行→design_facts_B.py／整合→integrity_B.py・sample_inspection_B.py／報告→template・build_report_B.py・report_lint／凍結→freeze_B.py。**本草案4 時点で実在する器材: make_contrasts_B.py・design_facts_B.py（と A の firth.py・cost_facts.py）。残りは凍結前に整備。**'}
F['H'] = {'text': 'seed: %s。tag: %s。' % (json.dumps(T['seeds'], ensure_ascii=False), json.dumps(T['tags'], ensure_ascii=False))}
m = HF['models']['4B-2507']; act_gib = m['hidden_size'] * 2 / 2**30   # 1 トークン × 1 層の bf16
F['I'] = {'text': '活性保存の容量（見積り ◐・4B-2507・hidden %d・bf16）: 末尾トークンの隠れ状態 1 本＝%.1f KB。凍結 3 層 × 全試行 %s ≈ %.2f GiB（Drive）。応答平均（副抽出位置）も同じ桁。重み %.2f GiB＋hook の活性（同時要求 1・逐次生成）≈ L4 の 90%% の内側。実測は調整走行の最初のセッションで置換。' % (
    m['hidden_size'], m['hidden_size'] * 2 / 1024, format(tr, ','), 3 * tr * act_gib, m['safetensors_gib'])}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'); os.makedirs(os.path.join(REPO, 'records', 'B'), exist_ok=True)
json.dump({'generated_utc': now, 'contrasts_sha16': sha(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8').read()), 'facts': F}, open(os.path.join(REPO, 'records', 'B', 'design-facts-B.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 設計事実（機械生成・`tools/design_facts_B.py` v1・%s UTC・正本 contrasts-B.json SHA16 %s）' % (now, sha(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8').read())), '']
for k in 'ABCDEFGHI':
    L.append('- **転記行 %s** — %s' % (k, F[k]['text'])); L.append('')
L.append('本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
open(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[design_facts_B] written records/B/design-facts-B.{md,json}')
