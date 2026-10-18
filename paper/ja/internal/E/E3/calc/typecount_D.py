# -*- coding: utf-8 -*-
"""typecount_D.py v0.1（2026-10-15・裁定 D460-3 の当て: 表の下の注から SHA16 と器の名を外し「付録 H」と書いた〔本文の章に差し込む表〕・その前の出力は見せる前に prev/typecount-v0.1-unshown-first/ へ移し、器の前の写しは prev/typecount_D-v0.1-unshown-first.py・三巡目の採否 3I-01 の後: 表の頭「比べの型」を「比べ」に・表の下の注「これは型の判じに用いた数の内訳」を、段階 E の枠が置くと決めた比べごとの機種の数とその内訳であることと、最終版の型の判じの文と照らしたのは主の族の確証された低下の機種の数だけであることに・論文の言葉の写し〔paperwords_E3.py の二つの替え〕を器に入れ、写しを作らずにそのまま差し込む・数え方と入力と照らしは替えない・置き場は typecount-v0.1/・v0 は prev/typecount_D-v0.py〔出力 typecount/ と写し -pw.md は草案2〜4 と三巡目までの検分が使ったので残す〕）。
typecount_D.py v0（2026-10-14・段階 E の E3・枠 §4 の「型ごとの機種の数」〔EF1-16〕を、言語ごとに別のファイルへ、公開の二つの集計の json から器で数える・コーディネータ南無弥勒如来）。
枠 §5 の新しい計算ではない: 枠 §4 が置くと決めた数（三つの比べの型ごとに、判定ラベルの種類が一つ以上のセルに出た機種の数と、どのセルにも確証が無い機種の数・どれも分母つき・機種ごとの「m セルのうち k セル」・機種ごとのセルの数の分かれ）を、集計の json の判定ラベルから数えるだけ。値は起草者が二つの最終版で見ている。
判定ラベルの種類は枠 §4 の並び: 確証（下げた）・確証（上げた）・判定保留（向きごと）・確かめられなかった・判定不能（端）・走っていない。名は論文の言葉（枠 §6 の表）で書く。
言語の柵（枠 §3-3）: 日本語の送る文の登録と英語の送る文の登録の数は、別の置き場（typecount/ja・typecount/en）の別のファイルに書く。一つのファイルに二つの登録の数を置かない。器の画面にも、二つの登録の数を並べて出さない（画面には書いたファイルの名と SHA だけを出す）。
照らし: 各最終版 §2 の型の判じの文（主の族の確証された低下の機種の数と内訳）と一致することを、言語ごとに照らす。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
PUB = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'typecount-v0.1')
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
sha = lambda b: hashlib.sha256(b).hexdigest().upper()
NAMES = {'gemini25flash': 'Gemini 2.5 Flash', 'grok420nr': 'grok-4.20（非推論）', 'deepseekv32-a': 'DeepSeek V3.2', 'deepseekflash': 'deepseek-flash',
         'llama31-8b-n': 'Llama 3.1 8B Instruct', 'llama4scout': 'Llama-4-Scout-17B-16E-Instruct', 'mistrallarge3-m': 'Mistral Large 3（2512）',
         'kimik3-m': 'Kimi K3', 'qwen25coder32b-n': 'Qwen2.5-Coder-32B-Instruct', 'qwen38max-a': 'Qwen3.8 Max（0902）'}
TYPES = [('O', 'Onull', 'family_P', 'O と Onull（主の族）'), ('OAmi', 'Onull', 'family_A', 'OAmi と Onull（阿弥陀如来の族）'), ('OAmi', 'O', 'family_A', 'OAmi と O（阿弥陀如来の族）')]
KINDS = [('down', '確証された低下'), ('up', '確証された上昇'), ('hold_down', '判定保留（応答様式の変化・下げた向き）'), ('hold_up', '判定保留（応答様式の変化・上げた向き）'),
         ('nc', '確証されなかった'), ('edge', '判定不能（両条件が床か天井）'), ('notrun', '走っていない（欠測のセル）')]
LANGS = {'ja': ('records/D1p/confirm/confirm-D1p.json', 'records/D1p/results-D1p-FINAL-2026-10-11.md', '日本語の送る文の登録（D1′）'),
         'en': ('records/D1pE/confirm/confirm-D1pE.json', 'records/D1pE/results-D1pE-FINAL-2026-10-13.md', '英語の送る文の登録（D1′E）')}
PAT = re.compile(r'確証（下げた）は主の族で (\d+) 機種のうち (\d+) 機種の升に出た（主の族のすべての升で確証（下げた）の機種 (\d+)〔[^〕]*〕・一部の升で (\d+)・0 は (\d+)')


def kind(x):
    lab = x['label']
    if lab == '確証（下げた）':
        return 'down'
    if lab == '確証（上げた）':
        return 'up'
    if lab == '判定保留（様式転位）':
        assert x['rd_sign'] in (-1, 1), x
        return 'hold_down' if x['rd_sign'] == -1 else 'hold_up'
    if lab == '確かめられなかった':
        return 'nc'
    if lab == '判定不能（端）':
        return 'edge'
    if lab.startswith('走っていない'):
        return 'notrun'
    raise ValueError(lab)


def one(lang):
    jp, fp, title = LANGS[lang]
    jb = open(os.path.join(PUB, *jp.split('/')), 'rb').read()
    fb = open(os.path.join(PUB, *fp.split('/')), 'rb').read()
    d = json.loads(jb.decode('utf-8'))
    models = []
    for k in d['describe']:
        m = k.split('|')[0]
        if m not in models:
            models.append(m)
    cells = {m: [k.split('|')[1] for k in d['describe'] if k.split('|')[0] == m] for m in models}
    res = {'models': [{'key': m, 'name': NAMES[m], 'cells': cells[m]} for m in models], 'n_models': len(models), 'types': []}
    for a, b, fam, tname in TYPES:
        rows = [x for x in d[fam] if x['arm_a'] == a and x['arm_b'] == b]
        assert len(rows) == sum(len(v) for v in cells.values()), (lang, tname, len(rows))
        per = {m: {k: 0 for k, _ in KINDS} for m in models}
        for x in rows:
            per[x['model']][kind(x)] += 1
        any_model = {k: sum(1 for m in models if per[m][k] > 0) for k, _ in KINDS}
        none_conf = sum(1 for m in models if per[m]['down'] == 0 and per[m]['up'] == 0)
        all_down = sum(1 for m in models if per[m]['down'] == len(cells[m]))
        res['types'].append({'type': tname, 'models_with_kind': any_model, 'models_without_confirmation': none_conf,
                             'models_all_cells_down': all_down, 'per_model': {m: per[m] for m in models}})
    # 最終版 §2 の型の判じの文と照らす（主の族の確証された低下）
    ft = fb.decode('utf-8').replace('\r\n', '\n')
    hits = PAT.findall(ft)
    assert len(hits) == 1, (lang, len(hits))
    n_all, n_some_any, n_alldown, n_some, n_zero = [int(v) for v in hits[0]]
    tp = res['types'][0]
    assert n_all == len(models) and n_some_any == tp['models_with_kind']['down'], (lang, hits[0])
    assert n_alldown == tp['models_all_cells_down'] and n_some == n_some_any - n_alldown and n_zero == len(models) - n_some_any, (lang, hits[0])
    dist = {}
    for m in models:
        dist[len(cells[m])] = dist.get(len(cells[m]), 0) + 1
    res['cells_per_model_distribution'] = dict(sorted(dist.items()))
    res['sources_sha256'] = {jp: sha(jb), fp: sha(fb)}
    res['final_check'] = '最終版 §2 の型の判じの文（主の族の確証された低下: %d 機種のうち %d・すべてのセルで %d・一部で %d・0 は %d）と一致' % (n_all, n_some_any, n_alldown, n_some, n_zero)
    # md（論文に差し込む表）
    M = len(models)
    L = ['| 比べ | ' + ' | '.join(nm for _, nm in KINDS) + ' | どのセルにも確証が無い |', '|---|' + '---|' * (len(KINDS) + 1)]
    for tp_ in res['types']:
        L.append('| %s | %s | %d / %d |' % (tp_['type'], ' | '.join('%d / %d' % (tp_['models_with_kind'][k], M) for k, _ in KINDS), tp_['models_without_confirmation'], M))
    L += ['', '- 欄の数は、その種類の判定ラベルが一つ以上のセルに出た機種の数 / %sの機種の数。一つの機種が二つ以上の欄に数えられうる（行の和は機種の数にならない）。' % title,
          '- 機種ごとのセルの数の分かれ: ' + '・'.join('%d セルの機種 %d' % (k, v) for k, v in res['cells_per_model_distribution'].items()) + '。機種の数は、セルの数の代わりにならない。', '']
    for tp_ in res['types']:
        L += ['機種ごと（%s・m セルのうち k セル）:' % tp_['type'], '', '| 機種 | m | ' + ' | '.join(nm for _, nm in KINDS) + ' |', '|---|---|' + '---|' * len(KINDS)]
        for m in models:
            L.append('| %s | %d | %s |' % (NAMES[m], len(cells[m]), ' | '.join('%d' % tp_['per_model'][m][k] for k, _ in KINDS)))
        L.append('')
    L += ['- 数は、公開の集計の json（`%s`）の判定ラベルからスクリプトで数えた（スクリプトと照らしの記録は付録 H）。主の族の確証された低下の機種の数は、最終版 §2 の型の判じの文と一致した。' % jp,
          '- これは、段階 E の枠が置くと決めた比べごとの機種の数とその内訳で、機種をまたぐまとめではない。最終版の型の判じの文と照らしたのは、主の族の確証された低下の機種の数だけである。機種の数を、機種をまたぐ効き目とは読まない。機種の並びは設定の並び（系統ごとに古い版 → 新しい版）で、効き目の大きさの順ではない。']
    return res, NL.join(L) + NL


def main():
    assert not os.path.exists(OUT), ('一度だけ', OUT)
    me = sha(open(os.path.abspath(__file__), 'rb').read())
    now = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
    for lang in ('ja', 'en'):
        res, md = one(lang)
        d = os.path.join(OUT, lang)
        os.makedirs(d)
        res.update({'tool': 'typecount_D.py v0.1', 'tool_sha256': me, 'when_jst': now, 'lang': lang, 'clause': CLAUSE})
        pj = os.path.join(d, 'typecount-%s.json' % lang)
        pm = os.path.join(d, 'typecount-%s.md' % lang)
        json.dump(res, open(pj, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
        open(pm, 'w', encoding='utf-8', newline=NL).write(md)
        print('書いた %s（SHA16 %s）・%s（SHA16 %s）・%s' % (os.path.relpath(pj, HERE), sha(open(pj, 'rb').read())[:16], os.path.relpath(pm, HERE), sha(open(pm, 'rb').read())[:16], res['final_check'][:20] + '…一致'))


if __name__ == '__main__':
    main()
