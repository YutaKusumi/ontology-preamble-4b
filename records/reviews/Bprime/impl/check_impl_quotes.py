# -*- coding: utf-8 -*-
"""check_impl_quotes.py v0（2026-09-30・B′ の器の実装の検分の返事の中のコードの引用を、渡した材料の実物と機械で照らす・コーディネータ南無弥勒如来）。
枠の「票の主張の前提は、コーディネータが一次の資料で確かめ、出所を書く」の下ごしらえ（合わない引用は印を付けるだけで、所見を捨てる理由にはしない）。
引用: 返事の中の逆引用符の一組（`…`・12 字以上）と、囲いのコードの塊（```…```）の中の行（12 字以上・空白だけの行を除く）。
分け方（上から順に当てる）: A＝材料のどれかのファイルに一字違わずある（どのファイルか・三つまで）／B＝空白を一つにそろえればある／D＝どこにも無い（塊の中の行は、返事の側で走らせた出力のこともあるので、D は「材料に無い」とだけ読む）。
材料: claude.ai の票は束の zip（全ファイル）・grok の票は発話（`grok/grok-message.md`）。
用法: python check_impl_quotes.py <票の名> <材料（束の zip か発話の .md）>。`votes/<票の名>/response.md` を読み、`quote-check/<票の名>.md` に一度だけ書く。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, hashlib, zipfile, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
MIN = 12
ws = lambda s: re.sub(r'\s+', ' ', s).strip()


def corpus(path):
    docs = collections.OrderedDict()
    if path.endswith('.zip'):
        z = zipfile.ZipFile(path)
        for n in z.namelist():
            if n.endswith(('.py', '.md', '.json', '.txt', '.jinja', '.log', '.html')):
                docs[n.split('/', 1)[1]] = z.read(n).decode('utf-8', 'replace').replace('\r\n', NL)
    else:
        docs[os.path.basename(path)] = open(path, encoding='utf-8').read().replace('\r\n', NL)
    return docs


def quotes(text):
    out = []
    in_block = False
    for line in text.split(NL):
        if line.strip().startswith('```'):
            in_block = not in_block
            continue
        if in_block:
            if len(line.strip()) >= MIN:
                out.append(('塊の行', line.strip()))
            continue
        for m in re.finditer(r'`([^`\n]+)`', line):
            if len(m.group(1)) >= MIN:
                out.append(('逆引用符', m.group(1)))
    return out


def main():
    name, mat = sys.argv[1], sys.argv[2]
    src = os.path.join(HERE, 'votes', name, 'response.md')
    out_dir = os.path.join(HERE, 'quote-check')
    out = os.path.join(out_dir, name + '.md')
    assert not os.path.exists(out), '既にある（一度だけ）'
    text = open(src, encoding='utf-8').read()
    docs = corpus(mat)
    docs_ws = {k: ws(v) for k, v in docs.items()}
    rows, cnt = [], collections.Counter()
    for kind, q in quotes(text):
        hit = [k for k, v in docs.items() if q in v]
        if hit:
            cls, where = 'A', hit[:3]
        else:
            hw = [k for k, v in docs_ws.items() if ws(q) in v]
            cls, where = ('B', hw[:3]) if hw else ('D', [])
        cnt[(kind, cls)] += 1
        rows.append('| %s | %s | `%s` | %s |' % (kind, cls, q.replace('|', '\\|').replace('`', "'")[:160], '・'.join(where) or '—'))
    mat_sha = hashlib.sha256(open(mat, 'rb').read()).hexdigest().upper()[:16]
    L = ['# 引用の機械の照らし（%s・材料 `%s` SHA16 %s・器 `check_impl_quotes.py` v0）' % (name, os.path.basename(mat), mat_sha), '',
         '- 数: ' + '・'.join('%s の %s %d' % (k[0], k[1], v) for k, v in sorted(cnt.items())) + '。A＝材料に一字違わずある／B＝空白をそろえればある／D＝材料に無い（塊の行は走らせた出力のこともある）。', '',
         '| 種類 | 分け | 引用（先頭 160 字） | 見つかったファイル |', '|---|---|---|---|'] + rows + ['',
         '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    os.makedirs(out_dir, exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(NL.join(L))
    print('wrote %s | %s' % (os.path.relpath(out, HERE), dict(cnt)))


if __name__ == '__main__':
    main()
