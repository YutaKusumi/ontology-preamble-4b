# -*- coding: utf-8 -*-
"""B-lens の結果の独立の再計算（コーディネータの確かめ・2026-09-24・凍結した器を import しない）。
v̂（選んだ層）の主の物差しのうち M_E と M_L_nuclear を、safetensors から語彙の行と最終の正規化の重みだけを読んで組み直し、層一の器の値と、
等方の帰無の解析の標準偏差から出した両側の p（正規の近似）を、器の等方の割合と並べる。既にある記録には書かない。
用法: python records/Blens/indep_check_Blens.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, json, math, hashlib
import numpy as np
from safetensors import safe_open

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'indep-check-Blens.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
SETS = os.path.join(REPO, 'records', 'Blens', 'sets-Blens.json')
LENS = os.path.join(REPO, 'results', 'Blens', 'lens-Blens.json')
DIRS = os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz')
SJ = json.load(open(SETS, encoding='utf-8'))
LJ = json.load(open(LENS, encoding='utf-8'))
v = np.load(DIRS)['static__0.5'].astype(np.float64)
idx = json.load(open(os.path.join(SNAP, 'model.safetensors.index.json'), encoding='utf-8'))['weight_map']


def rows(name, ids=None):
    with safe_open(os.path.join(SNAP, idx[name]), framework='pt') as f:
        t = f.get_slice(name)
        if ids is None:
            return t[:].float().numpy().astype(np.float64)
        return np.stack([t[r:r + 1].float().numpy()[0] for r in ids]).astype(np.float64)


emb = 'model.embed_tokens.weight' if 'model.embed_tokens.weight' in idx else 'lm_head.weight'
g = rows('model.norm.weight')


def metric(pos, neg):
    ids = list(pos) + list(neg)
    w = np.array([1.0 / len(pos)] * len(pos) + [-1.0 / len(neg)] * len(neg))
    a = g * (w @ rows(emb, ids))                  # 重みの和が零なので、語彙の平均による中心化は値を変えない
    val = float(a @ v)
    sd = float(np.linalg.norm(a) * np.linalg.norm(v) / math.sqrt(len(v)))
    return val, sd, val / sd, math.erfc(abs(val / sd) / math.sqrt(2))


E, L = SJ['sets']['E']['static'], SJ['sets']['L']
res = {'M_E_static': metric(E['plus'], E['minus']), 'M_L_nuclear': metric([L['a']], [L['b'], L['c'], L['d']])}
lens = LJ['layers']['0.5']['directions']['static']
R = ['# B-lens の結果の独立の再計算（コーディネータの確かめ・機械生成・`records/Blens/indep_check_Blens.py`）', '',
     '- 入力: 語の集合 `records/Blens/sets-Blens.json`（SHA16 %s）・凍結の方向 `results/dirB/dirB__s1/directions.npz`（SHA16 %s）・層一の記録 `results/Blens/lens-Blens.json`（SHA16 %s）・重みは HF のキャッシュの safetensors（`%s` と `model.norm.weight` の行だけを読む）。'
     % (s16(SETS), s16(DIRS), s16(LENS), emb),
     '- 凍結した器（`tools/blens_core.py`・`tools/blens_lens.py`）は import しない。', '',
     '| 物差し | 再計算の値 | 層一の器の値 | 等方の解析の標準偏差 | z | 両側の p（正規の近似） | 器の等方の割合（千本の抽選） |', '|---|---|---|---|---|---|---|']
for k, (val, sd, z, p) in res.items():
    R.append('| %s | %.6g | %.6g | %.4g | %.3f | %.4f | %.4f |' % (k, val, lens[k]['value'], sd, z, p, lens[k]['p_iso']))
TOL = 1e-5      # 層一の器は重みを bf16 から float32 に上げて計算する（正本 `projection.dtype`）。二千五百余りの次元の内積で float32 の丸めが積もる幅より広く、式の取り違えより十分に狭い
rel = max(abs(res[k][0] - lens[k]['value']) / max(1e-12, abs(lens[k]['value'])) for k in res)
R += ['', '- 値の一致（相対の差の許容 %g）: %s（相対の差の最大 %.2e）。' % (TOL, '一致' if rel <= TOL else '**不一致**', rel),
      '- 前の走らせ方（2026-09-24・コミットの前）は許容を 1e-9 に置き、同じ値の組を「不一致」と印字した。器の値は float32 で計算するので、その許容は狭すぎた（許容を直してこの記録を作り直した・前の出力は残していない）。',
      '', '## 検分票', '',
      '- 対象: 層一の主の値のうち二つ（M_E と M_L_nuclear）。',
      '- 段階: 結果の後（封印の後・結果を開いた日に、報告の前に行った）。',
      '- 凍結物の同定: 入力の SHA16 を上に並べた。',
      '- 盲検の状態: 該当しない（数の再計算）。',
      '- 敵対的検分: 凍結した器の値そのものを疑い、器を通らない別の道で組み直した。',
      '- 系統の内訳: コーディネータ（Claude 系）一名。',
      '- COI記録: 再計算は器の値を確かめる向きで、結果の読みは変えない。',
      '- 本検分が確認していないこと: ほかの四つの主の物差し・二つ目の札の順位・語の側の帰無・門・大きさの目盛りは再計算していない。等方の割合は正規の近似と並べただけで、千本の抽選は組み直していない。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', OUT)
