# -*- coding: utf-8 -*-
"""bprime_publish_map.py v0 —— B′ の作業の置き場（非公開・git でない）から公開の置き場（`ontology-preamble-4b`）へ移す物と道筋の表（案・2026-09-30・コーディネータ南無弥勒如来）。

層三の公開の形にそろえる: 器は `tools/`（Colab の起動器は `tools/colab/`・台帳も `tools/`）・正本と草案と凍結の本文は `design/`・記録は `records/Bprime/`
（裁定は `records/Bprime/rulings-D*.md`・器の段の記録と独立の器の指示と開発の記録は `records/Bprime/tools/`）・設計の巡と器の実装の検分は `records/reviews/Bprime/`・予想の書式は `records/predictions/`。
規則は上から順に当て、最初に当たった規則で決める。どの規則にも当たらないファイルがあれば止める（すべてのファイルを「移す・移さない・登録者の決め」のどれかに振り分ける）。
移さない物: 手元の器のための写し（分けた置き場の transformers `pylib/`・Hugging Face から落とした設定とトークナイザ `hf/`〔目録は記録として移す〕）・他者の著作物の写し（モデルカードの写し `sources/`）・
Python の一時の置き場（`__pycache__`）。登録者の決め（OPEN）に上げる物は、推しを添える。移す操作（`publish_Bprime.py`）は、登録者の確認と push の確認を得てから行う。
用法: python tools/bprime_publish_map.py [--md <案の文書の置き場>]（作業の置き場のすべてのファイルを振り分けて数を印字する）／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, fnmatch, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(HERE)
VERSION = 'v0'
REV = '842da3794eaa0b77d5f08bae87a17459d91ff475'

# (型, 行き先〔'{rest}' は型の ** に当たった残り・'{name}' は名〕 か None〔移さない〕 か 'OPEN'、理由)
RULES = [
    ('**/__pycache__/**', None, 'Python の一時の置き場'),
    ('pylib/**', None, '手元の器のための transformers 5.16.1 の分けた置き場（第三者の配布物・版は正本 `inputs.versions`）'),
    ('hf/gemma-4-31B-it/%s/MANIFEST-local.json' % REV, 'records/Bprime/MANIFEST-local-gemma-4-31B-it.json', '手元の設定とトークナイザの目録（重みの断片の値は凍結の前に足す・K9）'),
    ('hf/**', None, 'Hugging Face から落とした設定とトークナイザとチャットの型（配布元にある・SHA は台帳と目録）'),
    ('sources/**', None, 'モデルカードの写し（他者の著作物・候補の事実の記録は URL と SHA で指す）'),
    ('tools/independent/bprime_recompute_rewrite.py', 'tools/bprime_recompute_rewrite.py', '独立の再計算の書き換えの道（別の個体が書いた器・起動器が import する）'),
    ('tools/independent/bprime_reextract.py', 'tools/bprime_reextract.py', '独立の再抽出の道（別の個体が書いた器・起動器が import する）'),
    ('tools/independent/**', 'records/Bprime/tools/independent/{rest}', '別の個体への指示・開発の記録・確かめの器'),
    ('tools/tools-log-Bprime.md', 'records/Bprime/tools/tools-log-Bprime.md', '器の段の記録'),
    ('tools/dry-*', 'records/Bprime/dry/{name}', '合成データの確かめの作業の記録（正式の記録は凍結の前に取り直す）'),
    ('tools/prev/**', 'OPEN', '凍結の前の器の前の版（推し: `records/Bprime/tools/prev/` に移す・器の育ちの跡）'),
    ('tools/kit/**', 'records/Bprime/cost-pilot/kit/{rest}', '費用の下見で Colab に送った束'),
    ('tools/colab/**', 'tools/colab/{rest}', 'Colab の起動器'),
    ('tools/*.py', 'tools/{name}', 'B′ の器'),
    ('tools/ledger-bprime.*', 'tools/{name}', '台帳（起動器が `tools/` から読む）'),
    ('design/contrasts-Bprime.json', 'design/contrasts-Bprime.json', '正本'),
    ('design/design-Bprime-draft*.md', 'design/{name}', '草案（層三の形・草案は `design/`）'),
    ('design/prev/**', 'records/Bprime/design/prev/{rest}', '正本の前の版'),
    ('design/*.py', 'records/Bprime/design/tools/{name}', '草案と用語集を組んだ器'),
    ('design/*.md', 'records/Bprime/design/{name}', '正本の組み立ての所見・用語集・数の検査の記録'),
    ('records/Bprime/**', 'records/Bprime/{rest}', '記録'),
    ('rulings-D*.md', 'records/Bprime/{name}', '裁定の記録（会話の記録から機械で切り出した）'),
    ('rulings_D*.py', 'records/Bprime/rulings-tools/{name}', '裁定の記録を切り出した器'),
    ('reviews/**', 'records/reviews/Bprime/{rest}', '設計の巡の記録（依頼文・束・票・追い問い・採否の表）'),
    ('cost-pilot/**', 'records/Bprime/cost-pilot/{rest}', '費用の下見の記録'),
    ('port-probe/**', 'records/Bprime/port-probe/{rest}', '器の移しの下調べ'),
    ('plan-Bprime-steps-*.md', 'records/Bprime/{name}', '段取り書'),
    ('model-candidates-facts-*.md', 'records/Bprime/{name}', '機種の候補の事実'),
    ('write_notes_Bprime*.py', 'records/Bprime/notes-tools/{name}', '枠づくりの前の記録を書いた器'),
    ('model-feel/**', 'OPEN', 'Gemma の中立の課題の感触の確かめ（場面と腕を使っていない・封印の前の露出に数える・推し: `records/Bprime/model-feel/` に移す）'),
    ('model-feel-2/**', 'OPEN', '同じく二度目（推し: `records/Bprime/model-feel-2/` に移す）'),
]


def _match(rel, pat):
    """glob の型（** は置き場をまたぐ）。当たれば (rest, name) を返す。"""
    rx = '^' + re.escape(pat).replace(r'\*\*', '(.*)').replace(r'\*', '([^/]*)') + '$'
    m = re.match(rx, rel)
    if not m:
        return None
    rest = rel[len(pat.split('**')[0]):] if '**' in pat else os.path.basename(rel)
    return rest, os.path.basename(rel)


def classify(rel):
    """一つのファイル（作業の置き場からの道筋・/ で区切る）→ (行き先 か None か 'OPEN', 理由, 規則の番号)。どの規則にも当たらなければ (False, None, None)。"""
    for i, (pat, dst, why) in enumerate(RULES):
        m = _match(rel, pat)
        if m is None:
            continue
        if dst is None or dst == 'OPEN':
            return dst, why, i
        rest, name = m
        return dst.replace('{rest}', rest).replace('{name}', name), why, i
    return False, None, None


def walk(bp=BP):
    out = []
    for root, dirs, files in os.walk(bp):
        dirs.sort()
        for f in sorted(files):
            out.append(os.path.relpath(os.path.join(root, f), bp).replace(os.sep, '/'))
    return out


def plan(bp=BP):
    """作業の置き場のすべてのファイルを振り分ける。戻り値: {'publish': [(元, 行き先)], 'exclude': [(元, 理由)], 'open': [(元, 理由)], 'unmatched': [元], 'collide': [行き先]}。"""
    P = {'publish': [], 'exclude': [], 'open': [], 'unmatched': [], 'collide': []}
    seen = collections.Counter()
    for rel in walk(bp):
        dst, why, i = classify(rel)
        if dst is False:
            P['unmatched'].append(rel)
        elif dst is None:
            P['exclude'].append((rel, why))
        elif dst == 'OPEN':
            P['open'].append((rel, why))
        else:
            P['publish'].append((rel, dst))
            seen[dst] += 1
    P['collide'] = sorted(d for d, n in seen.items() if n > 1)
    return P


def public_path(internal_rel):
    """作業の置き場の道筋（`Bprime/` を付けても付けなくてもよい）→ 公開の置き場の道筋（移さないか登録者の決めのときは None）。"""
    rel = internal_rel[len('Bprime/'):] if internal_rel.startswith('Bprime/') else internal_rel
    dst, _, _ = classify(rel)
    return dst if dst not in (False, None, 'OPEN') else None


def summary_md(P):
    NL = chr(10)
    by = collections.OrderedDict()
    for rel in walk():
        dst, why, i = classify(rel)
        if dst is False:
            continue
        k = (i, RULES[i][0], 'publish' if dst not in (None, 'OPEN') else ('exclude' if dst is None else 'open'), RULES[i][1], why)
        by[k] = by.get(k, 0) + 1
    L = ['# B′ の公開の置き場への移し方の表（案・機械生成・`tools/bprime_publish_map.py` %s・登録者の決めの前）' % VERSION, '',
         '- 作業の置き場のファイル %d（移す %d・移さない %d・登録者の決め %d・どの規則にも当たらない %d・行き先の重なり %d）。' % (
             len(walk()), len(P['publish']), len(P['exclude']), len(P['open']), len(P['unmatched']), len(P['collide'])),
         '- 規則は上から順に当て、最初に当たった規則で決める。移す操作は登録者の確認と push の確認の後（`publish_Bprime.py`・行き先に違う中身の同じ名があれば止める）。', '',
         '| 規則 | 型 | 振り分け | 行き先 | 数 | 理由 |', '|---|---|---|---|---|---|']
    for (i, pat, kind, dst, why), n in by.items():
        L.append('| %d | `%s` | %s | %s | %d | %s |' % (i + 1, pat, {'publish': '移す', 'exclude': '移さない', 'open': '**登録者の決め**'}[kind],
                                                   ('`%s`' % dst) if kind == 'publish' else '—', n, why))
    L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    return NL.join(L)


def _selftest():
    cases = {
        'tools/bprime_run.py': 'tools/bprime_run.py', 'tools/colab/boot_bprime.py': 'tools/colab/boot_bprime.py', 'tools/ledger-bprime.json': 'tools/ledger-bprime.json',
        'tools/__pycache__/x.pyc': None, 'tools/independent/bprime_reextract.py': 'tools/bprime_reextract.py',
        'tools/independent/instructions-rewrite-reextract-Bprime.txt': 'records/Bprime/tools/independent/instructions-rewrite-reextract-Bprime.txt',
        'design/design-Bprime-draft10.md': 'design/design-Bprime-draft10.md', 'design/prev/contrasts-Bprime-v3.json': 'records/Bprime/design/prev/contrasts-Bprime-v3.json',
        'rulings-D270.md': 'records/Bprime/rulings-D270.md', 'reviews/design-round3/votes/grok-4.7/response.md': 'records/Bprime/../reviews/Bprime/design-round3/votes/grok-4.7/response.md'.replace('records/Bprime/../', 'records/'),
        'pylib/transformers/__init__.py': None, 'hf/gemma-4-31B-it/%s/config.json' % REV: None, 'sources/google_gemma-4-31b-it.html': None,
        'hf/gemma-4-31B-it/%s/MANIFEST-local.json' % REV: 'records/Bprime/MANIFEST-local-gemma-4-31B-it.json', 'model-feel/blind-ja.md': 'OPEN', 'tools/prev/bprime_run-v0.py': 'OPEN',
        'records/Bprime/facts-Bprime-pre.json': 'records/Bprime/facts-Bprime-pre.json', 'reviews/design-round3/__pycache__/a.pyc': None,
    }
    bad = {k: (classify(k)[0], v) for k, v in cases.items() if classify(k)[0] != v}
    assert not bad, bad
    assert classify('unknown-top-file.bin')[0] is False
    assert public_path('Bprime/rulings-D270.md') == 'records/Bprime/rulings-D270.md' and public_path('Bprime/pylib/x.py') is None
    P = plan()
    print('bprime_publish_map.py %s SELFTEST PASS（例 %d・作業の置き場 %d ファイル: 移す %d・移さない %d・登録者の決め %d・当たらない %d・行き先の重なり %d）' % (
        VERSION, len(cases), len(walk()), len(P['publish']), len(P['exclude']), len(P['open']), len(P['unmatched']), len(P['collide'])))
    return P


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if '--selftest' in sys.argv:
        P = _selftest()
        if P['unmatched'] or P['collide']:
            print('当たらない: %s' % P['unmatched'][:20]); print('重なり: %s' % P['collide'][:20]); sys.exit(1)
        sys.exit(0)
    P = plan()
    if '--md' in sys.argv:
        out = sys.argv[sys.argv.index('--md') + 1]
        with open(out, 'w', encoding='utf-8', newline=chr(10)) as fh:
            fh.write(summary_md(P))
    print('移す %d・移さない %d・登録者の決め %d・当たらない %d・行き先の重なり %d' % (len(P['publish']), len(P['exclude']), len(P['open']), len(P['unmatched']), len(P['collide'])))
    for x in P['unmatched'][:30]:
        print('  当たらない: %s' % x)
    for x in P['collide'][:30]:
        print('  重なり: %s' % x)
