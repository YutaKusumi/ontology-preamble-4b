# -*- coding: utf-8 -*-
"""bprime_meaningless.py v0（2026-09-30・B′ の意味のない列を作る器・Gemma-4-31B-it のトークナイザ・模型は読まない・コーディネータ南無弥勒如来）。

正本 `computation.before_seal.meaningless` と `computation.self_checks.logit.measure` のとおり:
  - 語彙: 特別なトークン（トークナイザの特別なトークンと足されたトークンのすべて）と、場面の文（主の升目と抽出の場面）・八つの腕の文・JSON の指示・主の書き出しと V1〜V3 の文字列を
    割ったトークンを除いた番号から、凍結した種（`computation.before_seal.meaningless.seed`）で一様に引く。
  - 長さ: 八升目の読み取りの位置にそろえる（升目の列の長さ＝プロンプトの長さ ＋ 書き出しの長さ・台帳から）。長さごとに二種類 × 中身二つ（`computation.self_checks.logit.measure.split`）。
  - 二種類: どちらも、チャットの型（user の発話一つ・生成の口つき）の user の発話の所にランダムなトークンの塊を置く（型を一字の目印で組み、目印の番号の所に塊の番号を差し込む）。
    flat は `<channel|>` の後にランダムなトークン七つ、confident は `<channel|>` の後に塊の頭の七つを置く（七は主の書き出しの長さ）。
  - 戻した文字列が禁じた文字列（主の書き出しと揺れの版・選択の鍵・場面と腕と指示の文の 12 字以上の片）を含まないことを assert する（T24）。
  - 読み取るのは列の最後の位置（読み取りの位置と同じ）。器は列の番号と SHA を記録に置く（露出の記録の欄）。
出力: `../records/Bprime/meaningless-Bprime.json`（機械生成・時刻を持たない・再実行で同一バイト）。
用法: python bprime_meaningless.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, re, json, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G
import bprime_core as P

VERSION = 'v0'
BP = os.path.dirname(HERE)
NL = chr(10)
MARK = '§'
ToolError = P.ToolError
MIN_SEG = 12


def ids_sha16(ids):
    return hashlib.sha256(','.join(str(int(x)) for x in ids).encode('ascii')).hexdigest().upper()[:16]


def source_texts(C, L):
    """除くトークンと禁じた文字列の元: 場面の文（主の升目と抽出の場面）・八つの腕の文・JSON の指示・主の書き出しと揺れの版。"""
    import run_stageB_local as RB
    AT = RB.arm_texts()
    scenes = sorted({sc for sc, _ in C['cells_main']} | set(C['directions']['extraction']['scenes']))
    texts = []
    for sc in scenes:
        s, inst = RB.scenario_and_instruction(sc)
        texts += [s['text'], inst]
    for arm in C['directions']['extraction']['arms']:
        if AT[arm]['text']:
            texts.append(AT[arm]['text'])
    strings = P.variant_strings(L['prefix_text'])
    return texts, list(strings.values()) + [P.KEY]


def pool(tok, texts, strings):
    bad = set(int(i) for i in tok.all_special_ids)
    bad |= set(int(i) for i in getattr(tok, 'added_tokens_decoder', {}).keys())
    for t in texts + strings:
        bad |= set(tok.encode(t, add_special_tokens=False))
    n = len(tok)
    return [i for i in range(n) if i not in bad], len(bad)


def forbidden_segments(texts, strings):
    segs = set(strings)
    for t in texts:
        segs |= {x.strip() for x in re.split(r'[。\n、「」]', t) if len(x.strip()) >= MIN_SEG}
    return sorted(segs, key=len, reverse=True)


def template(tok):
    """チャットの型の、目印の前と後の番号（目印はちょうど一つのトークンで、型の中にちょうど一度だけ現れる）。"""
    mk = tok.encode(MARK, add_special_tokens=False)
    if len(mk) != 1:
        raise ToolError('目印が一つのトークンでない')
    ids = G.apply_chat(tok, MARK)
    at = [i for i, t in enumerate(ids) if t == mk[0]]
    if len(at) != 1:
        raise ToolError('目印が型の中にちょうど一度でない')
    return ids[:at[0]], ids[at[0] + 1:]


def build(tok, C, L):
    M = C['computation']['self_checks']['logit']['measure']
    B = C['computation']['before_seal']['meaningless']
    import numpy as np
    texts, strings = source_texts(C, L)
    vocab, n_bad = pool(tok, texts, strings)
    segs = forbidden_segments(texts, strings)
    pre, post = template(tok)
    k_head = len(L['prefix_ids'])
    lengths = [L['cells_main']['%s|%s' % (sc, arm)]['readout_position'] + 1 for sc, arm in C['cells_main']]      # 正本の升目の順（同じ長さがあっても升目ごとに一つ）
    if len(lengths) != M['split']['lengths']:
        raise ToolError('升目の読み取りの位置にそろえた長さの数が正本と違う（%d・正本 %d）' % (len(lengths), M['split']['lengths']))
    if list(B['kinds']) != list(M['kinds']) or M['split']['kinds'] != len(M['kinds']):
        raise ToolError('二種類の名が正本の中で食い違う')
    rng = np.random.default_rng(int(B['seed']))
    seqs = collections.OrderedDict()
    for ci, Ln in enumerate(lengths):
        m = Ln - len(pre) - len(post) - k_head
        if m < k_head:
            raise ToolError('塊が書き出しの長さより短い')
        for kind in M['kinds']:
            for c in range(M['split']['contents']):
                chunk = [int(vocab[i]) for i in rng.integers(0, len(vocab), size=m)]
                tail = chunk[:k_head] if kind == 'confident' else [int(vocab[i]) for i in rng.integers(0, len(vocab), size=k_head)]
                ids = list(pre) + chunk + list(post) + tail
                if len(ids) != Ln:
                    raise ToolError('意味のない列の長さが升目の長さと違う')
                back =tok.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
                hit = [s for s in segs if s in back]
                if hit:
                    raise ToolError('意味のない列の戻した文字列が禁じた文字列を含む（%d 件）' % len(hit))
                seqs['%s-c%d-%d-%d' % (kind, ci, Ln, c)] = ids
    if len(seqs) != M['positions']:
        raise ToolError('意味のない列の本数が正本と違う（%d・正本 %d）' % (len(seqs), M['positions']))
    mp_tok = tok.convert_tokens_to_ids('<channel|>')
    if any(ids[len(ids) - k_head - 1] != mp_tok for ids in seqs.values()):
        raise ToolError('塊の後の型の最後が `<channel|>` でない')
    return seqs, {'pool': len(vocab), 'excluded': n_bad, 'segments': len(segs), 'lengths': lengths, 'template_pre': len(pre), 'template_post': len(post), 'head': k_head}


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    from transformers import AutoTokenizer
    import transformers
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    L = json.load(open(os.path.join(HERE, 'ledger-bprime.json'), encoding='utf-8'))
    if transformers.__version__ != C['inputs']['versions']['transformers']:
        raise ToolError('transformers の版が固定の版でない: %s' % transformers.__version__)
    tok = AutoTokenizer.from_pretrained(os.path.join(BP, 'hf', 'gemma-4-31B-it', C['inputs']['model']['revision']))
    seqs, meta = build(tok, C, L)
    seqs2, _ = build(tok, C, L)
    if seqs2 != seqs:
        raise ToolError('同じ種で作り直した列が同じでない')
    out = {'kind': 'bprime_meaningless', 'version': VERSION, 'seed': C['computation']['before_seal']['meaningless']['seed'], 'meta': meta,
           'sha16': {k: ids_sha16(v) for k, v in seqs.items()}, 'all_sha16': ids_sha16([x for v in seqs.values() for x in v]), 'sequences': seqs,
           'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    os.makedirs(os.path.join(BP, 'records', 'Bprime'), exist_ok=True)
    json.dump(out, open(os.path.join(BP, 'records', 'Bprime', 'meaningless-Bprime.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print('meaningless sequences %d | lengths %s | pool %d | excluded %d | all_sha16 %s' % (len(seqs), meta['lengths'], meta['pool'], meta['excluded'], out['all_sha16']))


if __name__ == '__main__':
    main()
