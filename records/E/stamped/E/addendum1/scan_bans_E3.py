# -*- coding: utf-8 -*-
"""scan_bans_E3.py v0（2026-10-14・枠の追記一〔E3 の起草の前〕の走査の器・合成の試しを通してから追記一と一緒に刻む・コーディネータ南無弥勒如来）。
読む物: 集めの一覧 `E/addendum1/bans-E3.json`（SHA-256 の頭 16 桁を引数で照らす）と、渡したファイル。
当て方（追記一の決まりのとおり）:
  (1) 日本語の語（words_ja）: 行ごとに部分一致。
  (2) 英語の型（patterns_en）: 前後が英字でない所で、大文字と小文字を区別しない（D1′E の器と同じ）。
  (3) D1′E の器の許す文の型の崩れ（行の単位・D1′E の器と同じ）。
  (4) 文の単位の決まり: 成功の定義（success）・二つの版をつなぐ英語の語（connectors_en）・床の持続（floor）。
  (5) 「も」の型（ja_mo・行の単位）と、COI の節の語（coi・見出しで節を決める）。
  (6) 成功の定義を指す語のある文の一覧（当たりではない・すべて目で読む）。
当たりは外さない。助けの印（当たりが「」か引用符の中か・柵の文らしい行か・禁止の語を定める行か・どの見出しの下か）を付ける。
当たりの扱い（直す・逐語の引用の中・柵の文・決まりの文脈の外）は、起草者が走査の記録に一つずつ書く（追記一）。
用法: python scan_bans_E3.py <一覧の SHA16> <名（英小文字と数字）> <ファイル> [...]
書く物: `E/addendum1/scans/scan-bans-E3-<名>.json`（一度だけ）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
if len(sys.argv) < 4 or not re.match(r'^[0-9A-F]{16}$', sys.argv[1]) or not re.match(r'^[a-z0-9]+$', sys.argv[2]):
    raise SystemExit('用法: python scan_bans_E3.py <一覧の SHA16> <名（英小文字と数字）> <ファイル> [...]')
WANT, LABEL, FILES = sys.argv[1], sys.argv[2], sys.argv[3:]
BANS = os.path.join(HERE, 'bans-E3.json')
bb = open(BANS, 'rb').read()
assert hashlib.sha256(bb).hexdigest().upper()[:16] == WANT, '一覧の SHA16 が違う'
B = json.loads(bb.decode('utf-8'))
OUTD = os.path.join(HERE, 'scans')
os.makedirs(OUTD, exist_ok=True)
OUT = os.path.join(OUTD, 'scan-bans-E3-%s.json' % LABEL)
assert not os.path.exists(OUT), '一度だけ'
R = B['rules_by_addendum1']
WORDS = [d['w'] for d in B['words_ja']]
SRC = {d['w']: d['sources'] for d in B['words_ja']}
EN_RE = [(d['re'], re.compile(r'(?<![A-Za-z])' + d['re'] + r'(?![A-Za-z])', re.I)) for d in B['patterns_en']]
T_LINE, T_LANG = re.compile(r'(?:族|family)', re.I), re.compile(r'(?:英語|English)', re.I)
T_BAD = re.compile(r'(?<![A-Za-z])(?:too|also|as well|even)(?![A-Za-z])', re.I)
CON = [(w, re.compile(r'(?<![A-Za-z])' + re.escape(w) + r'(?![A-Za-z])', re.I)) for w in R['connectors_en']['words']]
PAIR_ANY = [re.compile(p_, re.I) for p_ in R['connectors_en']['pair_en_any']]
MO = re.compile(R['ja_mo']['re'])
FL_EN = [re.compile(p_, re.I) for p_ in R['floor']['en']]
FL_EN_WITH = [re.compile(p_, re.I) for p_ in R['floor']['en_with_any']]
COI_H = re.compile(R['coi']['section_heading'])
COI_EN = [re.compile(p_, re.I) for p_ in R['coi']['en']]
S_TJA, S_PJA = R['success']['terms_ja'], R['success']['paraphrase_ja']
S_TEN = [re.compile(p_, re.I) for p_ in R['success']['terms_en']]
S_PEN = [re.compile(p_, re.I) for p_ in R['success']['paraphrase_en']]
HEAD = re.compile(r'^#{1,6} ')
FENCE_LIKE = re.compile(r'書かない|書かず|使わない|用いない|用いず|言わない|とは言えない|読まない|読まず|要約しない|置かない|並べない|ではない|てはならない|証拠にしない|禁|[Dd]o not|must not|never|should not', re.I)
DEF_LINE = re.compile(r'禁止の語|禁じる語|禁じる言い換え|banned|bans-E3|scan_bans_E3')
OPEN, CLOSE = '「『“"', '」』”"'


def in_quote(line, i):
    depth = 0
    for ch in line[:i]:
        if ch in '「『“':
            depth += 1
        elif ch in '」』”' and depth > 0:
            depth -= 1
    return depth > 0 or line[:i].count('"') % 2 == 1


def sentences(line):
    out = []
    for part in re.split(r'(?<=[。！？])', line):
        out += re.split(r'(?<=[.!?])\s+(?=[A-Z"“(\[「])', part)
    return [s for s in out if s.strip()]


hits, mentions, files_rec = [], [], []
for f in FILES:
    p = f if os.path.isabs(f) else os.path.join(os.getcwd(), f)
    if not os.path.isfile(p):
        raise SystemExit('ファイルが無い: %s' % f)
    raw = open(p, 'rb').read()
    files_rec.append({'path': f.replace('\\', '/'), 'sha256': hashlib.sha256(raw).hexdigest().upper()})
    heading = ''
    for n, line in enumerate(raw.decode('utf-8', errors='replace').split(NL), 1):
        line = line.rstrip('\r')
        if HEAD.match(line):
            heading = line.strip()
        aid = {'file': f.replace('\\', '/'), 'line': n, 'heading': heading[:80], 'fence_like': bool(FENCE_LIKE.search(line)), 'def_line': bool(DEF_LINE.search(line))}

        def hit(kind, what, pos=None, extra=None):
            h = dict(aid, kind=kind, what=what, in_quote=(in_quote(line, pos) if pos is not None else None), context=line.strip()[:160])
            if extra:
                h.update(extra)
            hits.append(h)
        for w in WORDS:
            i = line.find(w)
            while i >= 0:
                hit('word_ja', w, i, {'sources': SRC[w][:3]})
                i = line.find(w, i + len(w))
        for p_, rx in EN_RE:
            for m in rx.finditer(line):
                hit('pattern_en', m.group(0), m.start(), {'pattern': p_})
        if T_LINE.search(line) and T_LANG.search(line):
            for m in T_BAD.finditer(line):
                hit('template_D1pE', m.group(0), m.start())
            if 'でも' in line and re.search(r'英語の送る文', line):
                hit('template_D1pE', 'でも', line.find('でも'))
        for m in MO.finditer(line):
            hit('ja_mo', m.group(0), m.start())
        if COI_H.search(heading):
            for w in R['coi']['ja']:
                i = line.find(w)
                if i >= 0:
                    hit('coi', w, i)
            for rx in COI_EN:
                for m in rx.finditer(line):
                    hit('coi', m.group(0), m.start())
        for s in sentences(line):
            # 成功の定義
            tj = [t for t in S_TJA if t in s]
            te = [m.group(0) for rx in S_TEN for m in rx.finditer(s)]
            if tj or te:
                pj = [w for w in S_PJA if w in s]
                pe = [m.group(0) for rx in S_PEN for m in rx.finditer(s)]
                mentions.append(dict(aid, sentence=s.strip()[:240], terms=tj + te, paraphrases=pj + pe))
                if pj or pe:
                    hit('success', '・'.join(tj + te) + ' × ' + '・'.join(pj + pe), None, {'sentence': s.strip()[:240]})
            # 二つの版をつなぐ英語の語
            cw = [w for w, rx in CON if rx.search(s)]
            if cw:
                pair = ('Japanese' in s and 'English' in s) or any(rx.search(s) for rx in PAIR_ANY)
                if pair:
                    hit('connector', '・'.join(cw), None, {'sentence': s.strip()[:240]})
            # 床の持続
            fj = [w for w in R['floor']['ja'] if w in s] if any(w in s for w in R['floor']['ja_with_any']) else []
            fe = [m.group(0) for rx in FL_EN for m in rx.finditer(s)] if any(rx.search(s) for rx in FL_EN_WITH) else []
            if fj or fe:
                hit('floor', '・'.join(fj + fe), None, {'sentence': s.strip()[:240]})
kinds = {}
for h in hits:
    kinds[h['kind']] = kinds.get(h['kind'], 0) + 1
rec = {'tool': 'scan_bans_E3.py v0', 'tool_sha256': hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest().upper(),
       'bans': 'E/addendum1/bans-E3.json', 'bans_sha256': hashlib.sha256(bb).hexdigest().upper(), 'label': LABEL,
       'when_jst': datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'), 'files': files_rec, 'n_hits': len(hits), 'kinds': kinds,
       'hits': hits, 'success_mentions': mentions,
       'note': '当たりは外さない。扱い（直す・逐語の引用の中・柵の文・決まりの文脈の外）は起草者が走査の記録に一つずつ書く。一覧は網羅ではない。当たりの無いことを、禁じた書き方の無いことの証にしない。',
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(rec, open(OUT, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('書いた %s・ファイル %d・当たり %d %s・成功の定義を指す文 %d' % (os.path.basename(OUT), len(FILES), len(hits), json.dumps(kinds, ensure_ascii=False), len(mentions)))
