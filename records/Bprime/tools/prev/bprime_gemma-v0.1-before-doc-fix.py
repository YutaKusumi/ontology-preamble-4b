# -*- coding: utf-8 -*-
"""bprime_gemma.py v0（2026-09-29・B′ の器の下地・Gemma-4-31B-it・transformers 5 系・コーディネータ南無弥勒如来）。

段階 B・層三の凍結した器のうち、模型に依らない関数（腕の本文・場面と指示・発話の組み立て・加減のフック・層の割合から添字への式・
対数オッズの式）は読み込んで使い、模型に依る所（層と正規化の道・softcap・チャットの型の返り値）だけをここに置く。凍結した器は書き換えない。

下調べ（`../port-probe/port-notes-2026-09-29.md`）で確かめたこと:
  - 層は `model.model.language_model.layers`・最後の正規化は `model.model.language_model.norm`・lm_head は埋め込みと共有。
  - 層の出力はテンソル（凍結の `make_hook` は両方の形を扱う）。
  - `hidden_states[-1]` は最後の正規化の後の値（層ごとの読み取りは層の出力をフックで取る・`hidden_states` を使わない）。
  - ロジットは softcap（`final_logit_softcapping`）を掛けた値。
  - transformers 5 では `apply_chat_template(tokenize=True)` が辞書の形を返し、凍結の `steer_B.apply_chat` は鍵の並びを返す（使わない）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys

REPO = os.environ.get('OP4B_REPO', 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b')
TOOLS = os.path.join(REPO, 'tools')
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

VERSION = 'v0.1'   # v0.1（2026-09-29）: transformers 5 の隠れ状態を集めるフックを数えない（印で見分ける）


class PortError(Exception):
    """器の移しの前提が崩れた（道・形・版）。"""


def text_cfg(model):
    return model.config.get_text_config()


def language_model(model):
    """Gemma 4 の文の側の模型（`Gemma4ForConditionalGeneration` の中）。道が無ければ止める。"""
    m = getattr(model, 'model', None)
    lm = getattr(m, 'language_model', None) if m is not None else None
    if lm is None or not hasattr(lm, 'layers') or not hasattr(lm, 'norm'):
        raise PortError('model.model.language_model（layers・norm）が無い——Gemma 4 の形でない')
    return lm


def decoder_layers(model):
    return language_model(model).layers


def final_norm(model):
    return language_model(model).norm


def n_layers(model):
    n = int(text_cfg(model).num_hidden_layers)
    if len(decoder_layers(model)) != n:
        raise PortError('設定の層の数（%d）と模型の層の数（%d）が違う' % (n, len(decoder_layers(model))))
    return n


def softcap(model):
    c = text_cfg(model).final_logit_softcapping
    return None if c is None else float(c)


def rms_eps(model):
    return float(text_cfg(model).rms_norm_eps)


def apply_chat(tokenizer, user_message):
    """段階 B と同じ組み立て（user の発話一つ・system なし・生成の口つき）。transformers 5 の辞書の返り値から `input_ids` を取る。"""
    r = tokenizer.apply_chat_template([{'role': 'user', 'content': user_message}], add_generation_prompt=True, tokenize=True)
    ids = r['input_ids'] if hasattr(r, 'keys') else r
    ids = [int(x) for x in ids]
    if not ids or not all(isinstance(x, int) for x in ids):
        raise PortError('チャットの型の返り値が整数の並びでない')
    return ids


def main_position(ids, pad_len=0):
    """主位置＝組み立て済みの列の最後のトークン（段階 B の `steer_B.main_position` と同じ式）。"""
    return int(pad_len) + len(ids) - 1


def layer_index(ratio, n):
    """層の割合 → 層の添字（段階 B の凍結の `direction_B.layer_index` をそのまま呼ぶ）。"""
    import direction_B
    return direction_B.layer_index(float(ratio), int(n))


def _ours(layer):
    """B′ のフック（凍結の `make_hook` が付ける印 `op4b` を持つもの）だけを数える。
    transformers 5 は、初めて `output_hidden_states=True` で順伝播したときに、隠れ状態を集めるフック（`transformers.utils.output_capturing`）を
    すべての層に掛け、外さない（下調べで確かめた）。そのフックは数えない。"""
    return [fn for fn in (getattr(layer, '_forward_hooks', {}) or {}).values() if hasattr(fn, 'op4b')]


def foreign_hooks(model):
    """層ごとの、B′ の印を持たないフックの数（記録のため）。"""
    return [len(getattr(L, '_forward_hooks', {}) or {}) - len(_ours(L)) for L in decoder_layers(model)]


def register_hook(model, layer_idx, hook):
    """B′ のフックを一本だけ掛け、掛ける前より一本だけ増えたことと、B′ のフックがちょうど一本であることを確かめる（段階 B の `register_hook` と同じ決まり・層の道と数え方だけ Gemma 4 と transformers 5 に合わせた）。"""
    if not hasattr(hook, 'op4b'):
        raise PortError('B′ のフックに印（op4b）が無い')
    layer = decoder_layers(model)[layer_idx]
    if _ours(layer):
        raise PortError('この層に B′ のフックが既に掛かっている')
    n0 = len(getattr(layer, '_forward_hooks', {}) or {})
    handle = layer.register_forward_hook(hook)
    if len(_ours(layer)) != 1 or len(getattr(layer, '_forward_hooks', {}) or {}) != n0 + 1:
        handle.remove()
        raise PortError('B′ のフックが一本になっていない')
    return handle


def assert_no_hooks(model, layer_idx):
    layer = decoder_layers(model)[layer_idx]
    n = len(_ours(layer))
    if n:
        raise PortError('B′ のフックが外れていない（%d 本）' % n)
