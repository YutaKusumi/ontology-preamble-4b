# -*- coding: utf-8 -*-
"""qf_task_B.py v1 —— 段階 B の品質床の課題の器（候補の断片・問いの組み立て・記号の読み取り・出所の登録）（登録者裁定 D146・2026-09-19 の夕刻）。

正本 `design/contrasts-B.json` の `quality_floor.task_candidates`（候補の出所・版・ファイル・問いの並べ方）・`presentation`（問いの組み立て）・
`extraction_rule`（記号の読み取り）・`fragment_rule`（断片の引き方）に従う。登録した値（ファイルの大きさと SHA256・断片の id と SHA256）は
本器の `--register` が書く出所の記録 `records/B/qf-selection/qf-sources-B.json` にあり、正本の `quality_floor.task_registered` がそれを写す。

- 候補のデータは**リポジトリの外**に置く（CC BY-SA 4.0 の継承の条件・裁定 D146）。置き場は環境変数 `OP4B_QF_CACHE`、無ければ `~/.cache/op4b-qf`。
  取るのはコミットで固定した URL から（`fetch`）。取ったファイルは登録の値と照らし、違えば止まる。
- 断片: 候補ごとに、全問を `id_rule` の順に並べ、`random.Random(seeds.quality).sample(全問, items)` で引く。**提示の順は引いた順**。行は除かない。
- 組み立て: `block(item)` は「課題の指示 ＋ 空行 ＋ 問題：問題文 ＋ 選択肢」。**前置きには触れない**——前置きの付け方は走行器の `user_message`（凍結走行器と同じ式）。
- 読み取り: `extract_letter(text, letters)`——NFKC で正規化し、許された記号のうち、前後の字がラテン文字でない最初の一字。無ければ書式外（None）。
用法: python tools/qf_task_B.py --selftest ／ --fetch（候補のデータを取る）／ --register（出所の記録を書く・候補のデータと MMLU の分類を照らす）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, io, sys, csv, json, random, hashlib, argparse, unicodedata, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
T = runs_B.load_T()
QF = T['quality_floor']
REG_PATH = 'records/B/qf-selection/qf-sources-B.json'
MMLU_CATEGORIES = {'repo': 'hendrycks/test', 'commit': '1668818d3b9730255f587f72792441528b991b80', 'path': 'categories.py'}
_ASCII_LETTER = re.compile(r'[A-Za-z]')


def cache_dir():
    return os.environ.get('OP4B_QF_CACHE') or os.path.join(os.path.expanduser('~'), '.cache', 'op4b-qf')


def candidates():
    c = QF.get('task_candidates') or []
    if not c:
        raise SystemExit('正本に品質床の課題の候補が無い（quality_floor.task_candidates・裁定 D146）')
    return c


def candidate(key):
    for c in candidates():
        if c['key'] == key:
            return c
    raise SystemExit('品質床の課題の候補に無い鍵: %s' % key)


def local_path(cand, name):
    """候補のファイルの置き場（`<置き場>/<配布元の名の小文字>/<コミットの先頭十二桁>/<ファイル名>`）。"""
    return os.path.join(cache_dir(), cand['repo'].split('/')[1].lower(), cand['commit'][:12], name)


def raw_url(cand, name):
    return 'https://raw.githubusercontent.com/%s/%s/%s/%s' % (cand['repo'], cand['commit'], cand['dir'], name)


def registered(key=None):
    """正本に写した登録の値（`quality_floor.task_registered`）。無ければ None。"""
    R = QF.get('task_registered')
    if R is None:
        return None
    return R if key is None else R['by_key'].get(key)


def _sha256(b):
    return hashlib.sha256(b).hexdigest().upper()


def source_record():
    """出所の記録（全長の SHA256 を持つ）。**正本に写した記録の SHA16 と照らしてから**返す。記録がリポジトリに無ければ None。"""
    R = QF.get('task_registered')
    if R is None:
        return None
    p = os.path.join(REPO, *R['record'].split('/'))
    if not os.path.exists(p):
        return None
    b = open(p, 'rb').read().replace(b'\r\n', b'\n')
    if hashlib.sha256(b).hexdigest()[:16].upper() != R['record_sha16']:
        raise SystemExit('出所の記録 %s が正本の写し（SHA16 %s）と違う' % (R['record'], R['record_sha16']))
    return json.loads(b.decode('utf-8'))


def _record_row(key):
    rec = source_record()
    if rec is None:
        return None
    rows = [c for c in rec['candidates'] if c['key'] == key]
    return rows[0] if rows else None


def fetch(cand, verify=True):
    """候補のファイルを、コミットで固定した URL から置き場に取る（既にあれば取り直さない）。
    登録の値があれば、大きさと SHA16（正本）を照らし、出所の記録があれば全長の SHA256 も照らす。"""
    reg = registered(cand['key']) if verify else None
    row = _record_row(cand['key']) if verify else None
    full = {f['name']: f['sha256'] for f in (row or {}).get('files', [])}
    out = []
    for name in cand['files']:
        p = local_path(cand, name)
        if not os.path.exists(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            b = urllib.request.urlopen(raw_url(cand, name), timeout=120).read()
            open(p, 'wb').write(b)
        b = open(p, 'rb').read()
        h = _sha256(b)
        if reg is not None:
            want = reg['files'].get(name)
            if want is None or want['bytes'] != len(b) or want['sha16'] != h[:16] or (full and full.get(name) != h):
                raise SystemExit('候補のファイルが登録の値と違う（裁定 D146）: %s %s（大きさ %d・SHA16 %s）'
                                 % (cand['key'], name, len(b), h[:16]))
        out.append({'name': name, 'bytes': len(b), 'sha256': h})
    return out


def _strip(x):
    return str(x).strip()        # 前後の空白を除く（中の改行は残す・presentation.field_strip）


def load_pool(cand):
    """候補の全問を `id_rule` の順に並べて返す。一問は {id, question, choices, answer}。形が違えば止まる（行は除かない）。"""
    items = []
    if cand['format'] == 'jsonl_jcqa':
        (name,) = cand['files']
        for line in open(local_path(cand, name), encoding='utf-8'):
            if not line.strip():
                continue
            r = json.loads(line)
            ch = [_strip(r['choice%d' % k]) for k in range(cand['choices'])]
            lab = int(r['label'])
            if not 0 <= lab < cand['choices']:
                raise SystemExit('答えの番号が選択肢の外: %s q_id %s' % (cand['key'], r['q_id']))
            items.append({'id': str(int(r['q_id'])), 'question': _strip(r['question']), 'choices': ch, 'answer': 'ABCDE'[lab]})
        items.sort(key=lambda it: int(it['id']))
    elif cand['format'] == 'csv_jmmlu':
        for subj in sorted(cand['subjects']):
            txt = open(local_path(cand, subj + '.csv'), encoding='utf-8-sig').read()
            for i, row in enumerate(csv.reader(io.StringIO(txt))):
                if len(row) != 6 or _strip(row[5]) not in ('A', 'B', 'C', 'D'):
                    raise SystemExit('JMMLU の行の形が違う: %s 行 %d（欄 %d）' % (subj, i, len(row)))
                items.append({'id': '%s:%03d' % (subj, i), 'question': _strip(row[0]), 'choices': [_strip(x) for x in row[1:5]],
                              'answer': _strip(row[5])})
    else:
        raise SystemExit('候補の形式が器に無い: %s' % cand['format'])
    ids = [it['id'] for it in items]
    if len(set(ids)) != len(ids):
        raise SystemExit('問いの id が重複している: %s' % cand['key'])
    for it in items:
        if not it['question'] or any(not c for c in it['choices']):
            raise SystemExit('空の問題文か選択肢がある: %s %s' % (cand['key'], it['id']))
    return items


def fragment(cand, pool=None):
    """断片（`fragment_rule`）: 全問から seeds.quality の種で items 問を引く。提示の順は引いた順。"""
    pool = load_pool(cand) if pool is None else pool
    n = int(QF['items'])
    if len(pool) < n:
        raise SystemExit('全問が断片の数より少ない: %s %d 問' % (cand['key'], len(pool)))
    return random.Random(int(T['seeds']['quality'])).sample(pool, n)


def fragment_sha256(items):
    s = json.dumps([{'id': it['id'], 'question': it['question'], 'choices': it['choices'], 'answer': it['answer']} for it in items],
                   ensure_ascii=False, separators=(',', ':'))
    return _sha256(s.encode('utf-8'))


def letters_of(item):
    return 'ABCDE'[:len(item['choices'])]


def block(item):
    """問いの本文（`presentation`）: 課題の指示 ＋ 空行 ＋ 問題：問題文 ＋ 選択肢（一行に一つ）。前置きは付けない（走行器が付ける）。"""
    P = QF['presentation']
    L = letters_of(item)
    inst = P['instruction_template'].format(letters=P['letters_sep'].join(L))
    lines = [P['question_prefix'] + item['question']] + [P['choice_format'].format(letter=l, text=c) for l, c in zip(L, item['choices'])]
    return inst + '\n\n' + '\n'.join(lines)


def extract_letter(text, letters):
    """記号の読み取り（`extraction_rule`）。許された記号のうち、前後の字がラテン文字でない最初の一字。無ければ None（書式外）。"""
    s = unicodedata.normalize('NFKC', text or '')
    for i, ch in enumerate(s):
        if ch not in letters:
            continue
        prev = s[i - 1] if i > 0 else ''
        nxt = s[i + 1] if i + 1 < len(s) else ''
        if _ASCII_LETTER.fullmatch(prev or '-') or _ASCII_LETTER.fullmatch(nxt or '-'):
            continue
        return ch
    return None


def source_sha16(cand):
    """候補の出所の SHA16（走行の記録の `task_source_sha16`）: 登録したファイルの（名・SHA256）の並びの JSON の SHA256 の先頭十六桁。"""
    reg = registered(cand['key'])
    if reg is None:
        raise SystemExit('品質床の課題の登録が無い（quality_floor.task_registered）')
    pairs = [[name, reg['files'][name]['sha16']] for name in cand['files']]
    return hashlib.sha256(json.dumps(pairs, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()[:16].upper()


def presentation_sha16():
    return hashlib.sha256(json.dumps(QF['presentation'], ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()[:16].upper()


def verify_fragment(cand, items):
    """組み直した断片を登録の値と照らす（違えば止まる）。登録が無ければ止まる——実機の測定は登録の後にしか走らせない。"""
    reg = registered(cand['key'])
    if reg is None:
        raise SystemExit('品質床の課題の登録が無い（quality_floor.task_registered・先に --register と正本の生成をする）')
    got = fragment_sha256(items)
    row = _record_row(cand['key'])
    if got[:16] != reg['fragment_sha16'] or (row is not None and row['fragment_sha256'] != got):
        raise SystemExit('組み直した断片が登録と違う（裁定 D146）: %s %s 対 %s' % (cand['key'], got[:16], reg['fragment_sha16']))
    if QF['task_registered']['template_sha16'] != presentation_sha16():
        raise SystemExit('問いの組み立てが登録の後に変わった（presentation の SHA16）')
    return got


def _dup_choice(it):
    return len(set(it['choices'])) < len(it['choices'])


def mmlu_stem_subjects():
    """MMLU の公式の分類（`categories.py`・コミット固定）を読んで、STEM に入る科目の一覧と、そのファイルの SHA16 を返す（ファイルは保存しない）。
    **取ったソースは実行しない**——代入の右辺を `ast.literal_eval` で読む（辞書と文字列の並びだけを受ける）。"""
    import ast
    url = 'https://raw.githubusercontent.com/%s/%s/%s' % (MMLU_CATEGORIES['repo'], MMLU_CATEGORIES['commit'], MMLU_CATEGORIES['path'])
    b = urllib.request.urlopen(url, timeout=60).read()
    ns = {}
    for node in ast.parse(b.decode('utf-8')).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            ns[node.targets[0].id] = ast.literal_eval(node.value)
    stem = set(ns['categories']['STEM'])
    subj = sorted(s for s, v in ns['subcategories'].items() if set(v) & stem)
    return subj, _sha256(b)[:16]


def register():
    """出所の記録を書く（**決定的**——同じ候補のデータからは同じバイト）。JMMLU の科目の一覧は MMLU の分類から組み直して正本と照らす。"""
    out = {'generated_by': 'tools/qf_task_B.py %s' % VERSION, 'rule': '裁定 D146（2026-09-19）',
           'seed': int(T['seeds']['quality']), 'items': int(QF['items']), 'template_sha16': presentation_sha16(), 'candidates': []}
    for cand in candidates():
        files = fetch(cand, verify=False)
        pool = load_pool(cand)
        frag = fragment(cand, pool)
        dist = {}
        for it in frag:
            dist[it['answer']] = dist.get(it['answer'], 0) + 1
        row = {'key': cand['key'], 'repo': cand['repo'], 'commit': cand['commit'], 'files': files,
               'pool_n': len(pool), 'fragment_n': len(frag), 'fragment_ids': [it['id'] for it in frag],
               'fragment_sha256': fragment_sha256(frag), 'fragment_sha16': fragment_sha256(frag)[:16],
               'dup_choice_rows_pool': sum(1 for it in pool if _dup_choice(it)), 'dup_choice_rows_fragment': sum(1 for it in frag if _dup_choice(it)),
               'answer_dist_fragment': dict(sorted(dist.items()))}
        if cand['format'] == 'csv_jmmlu':
            subj, sha = mmlu_stem_subjects()
            have = [s for s in subj if s in cand['subjects']]
            if have != sorted(cand['subjects']) or sorted(set(subj) - set(cand['subjects'])):
                missing = sorted(set(subj) - set(cand['subjects']))
                raise SystemExit('正本の科目の一覧が MMLU の分類の STEM と違う（正本に無い科目 %s）' % missing)
            out['mmlu_categories'] = dict(MMLU_CATEGORIES, sha16=sha, stem_subjects=len(subj))
        out['candidates'].append(row)
    p = os.path.join(REPO, *REG_PATH.split('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    s = json.dumps(out, ensure_ascii=False, indent=1) + '\n'
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return p, hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper(), out


def _selftest():
    # (1) 読み取りの規則（extraction_rule）
    cases = [('B', 'ABCDE', 'B'), ('答え：C', 'ABCDE', 'C'), ('C. マザーボード', 'ABCDE', 'C'), ('**D**', 'ABCD', 'D'),
             ('Ｂ', 'ABCDE', 'B'), ('選択肢Aです', 'ABCDE', 'A'), ('DNA の話ではなく B', 'ABCD', 'B'), ('E', 'ABCD', None),
             ('AI としては C', 'ABCDE', 'C'), ('わかりません', 'ABCDE', None), ('', 'ABCD', None), (None, 'ABCD', None),
             ('b', 'ABCD', None), ('答えは (A)', 'ABCD', 'A'), ('A、B、C のいずれか', 'ABC', 'A')]
    for text, L, want in cases:
        got = extract_letter(text, L)
        assert got == want, ('記号の読み取りが規則と違う', text, L, got, want)
    # (2) 問いの組み立て（presentation）: 指示 ＋ 空行 ＋ 問題 ＋ 選択肢。前置きは付けない
    it5 = {'id': '1', 'question': '問い', 'choices': ['甲', '乙', '丙', '丁', '戊'], 'answer': 'C'}
    it4 = {'id': 'x:000', 'question': '行1\n行2', 'choices': ['一', '二', '三', '四'], 'answer': 'A'}
    b5, b4 = block(it5), block(it4)
    P = QF['presentation']
    assert b5.startswith(P['instruction_template'].format(letters='A、B、C、D、E') + '\n\n問題：問い\nA. 甲\n') and b5.endswith('\nE. 戊'), b5
    assert '（A、B、C、Dのいずれか）' in b4 and '問題：行1\n行2\nA. 一' in b4 and b4.endswith('\nD. 四') and 'E.' not in b4, b4
    assert letters_of(it5) == 'ABCDE' and letters_of(it4) == 'ABCD'
    # (3) 断片の引き方は決定的で、提示の順は引いた順（fragment_rule）
    pool = [{'id': str(i), 'question': 'q%d' % i, 'choices': ['a', 'b', 'c', 'd'], 'answer': 'A'} for i in range(500)]
    f1 = fragment({'key': 'synth'}, pool)
    f2 = fragment({'key': 'synth'}, list(pool))
    assert [x['id'] for x in f1] == [x['id'] for x in f2] and len(f1) == QF['items'] and fragment_sha256(f1) == fragment_sha256(f2)
    assert [x['id'] for x in f1] != sorted((x['id'] for x in f1), key=int), '提示の順が並べ直されている（引いた順のはず）'
    assert [x['id'] for x in f1] == [x['id'] for x in random.Random(int(T['seeds']['quality'])).sample(pool, QF['items'])]
    # (4) 候補の定義が正本にある・置き場の形
    keys = [c['key'] for c in candidates()]
    assert keys == ['jcqa', 'jmmlu_stem'], keys
    assert raw_url(candidate('jcqa'), 'valid-v1.3.json').startswith('https://raw.githubusercontent.com/yahoojapan/JGLUE/%s/' % candidate('jcqa')['commit'])
    # (5) 手元に候補のデータがあり、登録があれば、断片を組み直して登録と照らす
    done = []
    for cand in candidates():
        if registered(cand['key']) is None or not all(os.path.exists(local_path(cand, n)) for n in cand['files']):
            continue
        fetch(cand, verify=True)
        verify_fragment(cand, fragment(cand))
        done.append(cand['key'])
    full = source_record() is not None
    print('[qf_task_B selftest] 読み取りの規則 %d 例・問いの組み立て・断片の決定性・候補の定義: 通った。%s'
          % (len(cases), ('登録と照らした候補: %s（%s）' % ('・'.join(done), '正本の SHA16 と出所の記録の全長の SHA256' if full else '正本の SHA16 だけ——出所の記録がこの置き場に無い'))
             if done else '**候補のデータか登録が無いので、登録との照合は飛ばした**'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--fetch', action='store_true')
    ap.add_argument('--register', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
    if a.fetch:
        for c in candidates():
            print('[qf_task_B] %s: %s' % (c['key'], '・'.join('%s %d B' % (f['name'], f['bytes']) for f in fetch(c))))
    if a.register:
        p, sha, out = register()
        print('[qf_task_B] 出所の記録を書いた: %s（SHA16 %s）' % (os.path.relpath(p, REPO), sha))
        for r in out['candidates']:
            print('  %s: 全問 %d・断片 %d・断片の SHA16 %s・選択肢の重なる問い 全問 %d／断片 %d・答えの分布 %s'
                  % (r['key'], r['pool_n'], r['fragment_n'], r['fragment_sha16'], r['dup_choice_rows_pool'], r['dup_choice_rows_fragment'],
                     r['answer_dist_fragment']))
