# -*- coding: utf-8 -*-
"""bprime_cells.py v0（2026-09-29・B′ の升目の組み立てと実トークンの台帳・Gemma-4-31B-it のトークナイザ・模型の値は出さない・コーディネータ南無弥勒如来）。

組み立ては段階 B の凍結の関数のまま（`run_stageB_local.arm_texts`・`scenario_and_instruction`・`user_message`）。チャットの型は B′ の
`bprime_gemma.apply_chat`（transformers 5 の返り値を正しく取る）。層三と同じ升目（場面 × 土台の腕）と、方向の抽出の文脈（八腕 × 抽出の二場面）を組む。
読み取りの書き出しは、層三の主の書き出しと同じ文字列（プロンプトの中の JSON の指示の雛形の頭）を Gemma のトークナイザで割ったもの。
台帳に置くもの: 升目ごとのプロンプトの長さ・主位置とその字・読み取りの位置・書き出しの割り方・読み取りの集合（選択の文字と refuse の頭）と、
割り方の確かめ（書き出しに各々の文字を足しても割り方が変わらないか・プロンプトの文字列に書き出しを足して割っても同じ並びになるか・
書き出しの並びがプロンプトの中にあるか〔写しの手がかり〕）。
出力: `ledger-bprime.json`・`.md`（機械生成）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G

VERSION = 'v0'
HF = os.path.join(HERE, '..', 'hf', 'gemma-4-31B-it', '842da3794eaa0b77d5f08bae87a17459d91ff475')
CELLS_MAIN = [('N1', 'O-Ncold'), ('N1', 'Onull'), ('S1', 'O-Ncold'), ('S1', 'Onull'), ('S4', 'O-Ncold'), ('S4', 'Onull'), ('SK', 'O-Ncold'), ('SK', 'Onull')]
EXTRACT_SCENES = ['N1', 'S1']
REAL_ARMS = ['O', 'Osec', 'Onull', 'Nk', 'N', 'O-Ncold', 'Osec-Ncold', 'Onull-Ncold']
PREFIX_TEXT = '```json\n{"choice": "'
LETTERS = {'survival': ['a', 'b', 'c'], 'nuclear': ['a', 'b', 'c', 'd']}
REFUSE_WORD = 'refuse'
NL = chr(10)
s16 = lambda b: hashlib.sha256(b).hexdigest().upper()[:16]


def sub_index(seq, sub):
    for i in range(len(seq) - len(sub) + 1):
        if seq[i:i + len(sub)] == sub:
            return i
    return -1


def build(tok):
    import run_stageB_local as RB
    texts = RB.arm_texts()
    prefix = tok.encode(PREFIX_TEXT, add_special_tokens=False)
    heads = {}
    for x in ['a', 'b', 'c', 'd', REFUSE_WORD]:
        full = tok.encode(PREFIX_TEXT + x, add_special_tokens=False)
        heads[x] = {'stable_prefix': full[:len(prefix)] == prefix, 'next': full[len(prefix)] if len(full) > len(prefix) else None,
                    'n_after': len(full) - len(prefix), 'pieces_after': [tok.decode([t]) for t in full[len(prefix):]]}
    cells, ctx = {}, {}

    def one(sc, arm):
        s, inst = RB.scenario_and_instruction(sc)
        um = RB.user_message(texts[arm]['text'], s['text'], inst)
        ids = G.apply_chat(tok, um)
        rendered = tok.apply_chat_template([{'role': 'user', 'content': um}], add_generation_prompt=True, tokenize=False)
        joint = tok.encode(rendered + PREFIX_TEXT, add_special_tokens=False)
        return s, ids, joint, um

    for sc, arm in CELLS_MAIN:
        s, ids, joint, um = one(sc, arm)
        fam = s['family']
        letters = LETTERS[fam]
        set_ids = [heads[x]['next'] for x in letters] + [heads[REFUSE_WORD]['next']]
        mp = G.main_position(ids)
        cells['%s|%s' % (sc, arm)] = {'scenario': sc, 'arm': arm, 'family': fam, 'letters': letters, 'prompt_len': len(ids), 'main_position': mp,
                                      'main_position_token': tok.decode([ids[mp]]), 'readout_position': len(ids) + len(prefix) - 1,
                                      'set_ids': set_ids, 'set_pieces': [tok.decode([t]) for t in set_ids],
                                      'joint_tokenization_same': joint == ids + prefix, 'prefix_in_prompt_at': sub_index(ids, prefix),
                                      'ids_sha16': s16(','.join(str(x) for x in ids + prefix).encode('ascii')), 'user_message_sha16': s16(um.encode('utf-8'))}
    for arm in REAL_ARMS:
        for sc in EXTRACT_SCENES:
            s, ids, joint, um = one(sc, arm)
            ctx['%s|%s' % (sc, arm)] = {'scenario': sc, 'arm': arm, 'prompt_len': len(ids), 'main_position': G.main_position(ids),
                                        'main_position_token': tok.decode([ids[-1]]), 'ids_sha16': s16(','.join(str(x) for x in ids).encode('ascii'))}
    arms = {a: {'sha16': texts[a]['sha16'], 'path': texts[a]['path'], 'n_tokens_text_only': len(tok.encode(texts[a]['text'], add_special_tokens=False)) if texts[a]['text'] else 0}
            for a in REAL_ARMS}
    return {'prefix_text': PREFIX_TEXT, 'prefix_ids': prefix, 'prefix_pieces': [tok.decode([t]) for t in prefix], 'heads': heads,
            'cells_main': cells, 'extract_contexts': ctx, 'arms': arms}


def ids_for(tok):
    """組み立てたトークンの並びそのもの（主の升目: プロンプト・書き出し・読み取りの集合／抽出の文脈: プロンプト）。台帳と同じ組み立て。"""
    import run_stageB_local as RB
    texts = RB.arm_texts()
    prefix = tok.encode(PREFIX_TEXT, add_special_tokens=False)
    nxt = lambda x: tok.encode(PREFIX_TEXT + x, add_special_tokens=False)[len(prefix)]
    main_, ext = {}, {}
    for sc, arm in CELLS_MAIN:
        s, inst = RB.scenario_and_instruction(sc)
        ids = G.apply_chat(tok, RB.user_message(texts[arm]['text'], s['text'], inst))
        main_['%s|%s' % (sc, arm)] = {'prompt': ids, 'prefix': prefix, 'set_ids': [nxt(x) for x in LETTERS[s['family']]] + [nxt(REFUSE_WORD)]}
    for arm in REAL_ARMS:
        for sc in EXTRACT_SCENES:
            s, inst = RB.scenario_and_instruction(sc)
            ext['%s|%s' % (sc, arm)] = G.apply_chat(tok, RB.user_message(texts[arm]['text'], s['text'], inst))
    return {'main': main_, 'extract': ext}


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    from transformers import AutoTokenizer
    import transformers
    tok = AutoTokenizer.from_pretrained(HF)
    L = build(tok)
    L['meta'] = {'version': VERSION, 'transformers': transformers.__version__, 'tokenizer_sha16': s16(open(os.path.join(HF, 'tokenizer.json'), 'rb').read()),
                 'chat_template_sha16': s16(open(os.path.join(HF, 'chat_template.jinja'), 'rb').read()), 'revision': os.path.basename(os.path.normpath(HF))}
    json.dump(L, open(os.path.join(HERE, 'ledger-bprime.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    esc = lambda t: t.replace(NL, '⏎').replace('|', '｜')
    M = ['# B′ の升目の実トークンの台帳（機械生成・`bprime_cells.py`・Gemma-4-31B-it のトークナイザ・模型の値は出さない）', '',
         '- 版: トークナイザ SHA16 %s・チャットの型 SHA16 %s・transformers %s・置き場の版 `%s`。' % (L['meta']['tokenizer_sha16'], L['meta']['chat_template_sha16'], L['meta']['transformers'], L['meta']['revision']),
         '- 書き出し（層三の主の書き出しと同じ文字列）の割り方: %d トークン（%s）。' % (len(L['prefix_ids']), '・'.join('%d「%s」' % (i, esc(p)) for i, p in zip(L['prefix_ids'], L['prefix_pieces']))),
         '- 書き出しの次のトークン: ' + '・'.join('%s → %s「%s」（割り方が保たれる %s・書き出しの後のトークン数 %d）' % (x, h['next'], esc(''.join(h['pieces_after'][:1])), 'はい' if h['stable_prefix'] else '**いいえ**', h['n_after']) for x, h in L['heads'].items()), '',
         '## 主の升目（8）', '', '| 升目 | 族 | プロンプトの長さ | 主位置（字） | 読み取りの位置 | 読み取りの集合 | 文字列で割っても同じ並び | 書き出しの並びがプロンプトの中にある位置 |', '|---|---|---|---|---|---|---|---|']
    for k, c in L['cells_main'].items():
        M.append('| %s | %s | %d | %d（%s） | %d | %s | %s | %s |' % (k.replace('|', '｜'), c['family'], c['prompt_len'], c['main_position'], esc(c['main_position_token']), c['readout_position'],
                                                                ' '.join('%s' % esc(p) for p in c['set_pieces']), 'はい' if c['joint_tokenization_same'] else '**いいえ**', c['prefix_in_prompt_at']))
    M += ['', '## 方向の抽出の文脈（八腕 × 抽出の二場面）', '', '| 文脈 | プロンプトの長さ | 主位置の字 |', '|---|---|---|']
    for k, c in L['extract_contexts'].items():
        M.append('| %s | %d | %s |' % (k.replace('|', '｜'), c['prompt_len'], esc(c['main_position_token'])))
    M += ['', '## 腕の本文のトークン数（本文だけ・チャットの型を当てない）', '', '| 腕 | SHA16 | トークン数 |', '|---|---|---|']
    for a, v in L['arms'].items():
        M.append('| %s | %s | %d |' % (a, v['sha16'] or '—', v['n_tokens_text_only']))
    M += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(os.path.join(HERE, 'ledger-bprime.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(M))
    bad = [k for k, c in L['cells_main'].items() if not c['joint_tokenization_same'] or c['main_position_token'] != '<channel|>']
    print('cells', len(L['cells_main']), '| contexts', len(L['extract_contexts']), '| prefix tokens', len(L['prefix_ids']), '| heads stable', all(h['stable_prefix'] for h in L['heads'].values()),
          '| letters single', all(L['heads'][x]['n_after'] == 1 for x in 'abcd'), '| refuse n_after', L['heads'][REFUSE_WORD]['n_after'], '| bad cells', bad)


if __name__ == '__main__':
    main()
