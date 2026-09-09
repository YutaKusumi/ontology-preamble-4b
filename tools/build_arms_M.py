# -*- coding: utf-8 -*-
"""build_arms_M.py v1 —— 追補 M の腕（前置き型 52 本のうち新規 47 本＋system 型 8 本）を設計草案8 §2.2 の規則から決定的に生成し、
`arms/panelM/` と台帳 `arms/panelM/SHA-LEDGER-M.json`・人間可読の `arms/ledger-M.md` に記帳する。V′ の盤（arms/panel）と台帳（SHA-LEDGER.json）には触れない（V′ 凍結物を不変に保つ）。
規則: LINE(name, form, tail) = form(name) + tail（句点直後に空白なし）／COMBINED(X, C) = rd(X) + "\\n\\n" + rd(C)（V′ §2.3・末尾改行なし）／
規則 R（梵転写の無意味列）: NFC 後、母音 {a i u e o ā ī ū ṛ}・位置固定 {ṃ ḥ 空白 ハイフン}・それ以外のラテン文字は子音（二重字は一字ずつ）。子音の並びを逆順、母音と記号は位置固定。
規則 K（カナの無意味列）: モーラ列（拗音は一モーラ）を逆順、「・」区切りのモーラ数を固定。
SHA16 は二段: 受け入れ時（正規化前の実物・下見側／V′ 側の既存値と突合）と台帳の確定値（NFC 後・CRLF→LF・strip なし・V′ 台帳と同一規約＝テキストの UTF-8 バイト）。
自己検査: (a) 空行ちょうど 1 回 (b) split == [X, C] (c) 長さ = |X|+|C|+2 (d) 末尾「。」 (e) SHA 相異 (f) Kan F1 T0 + Ncold が V′ の Nk-Ncold と同一バイト（生成せず既存を用いる） (g) 末尾文字列の字数が名ごとに TS=PS=MS・TK=PK=MK
(h) 誘因語彙 v2 の全チャネルにヒット 0 (i) 再実行で同一バイト（既存ファイルと不一致なら中止＝改変禁止）。
用法: python tools/build_arms_M.py            （引数なし）
"""
import os, sys, json, re, hashlib, unicodedata
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANEL_V = os.path.join(REPO, 'arms', 'panel'); PANEL_M = os.path.join(REPO, 'arms', 'panelM'); SYS_M = os.path.join(PANEL_M, 'system')
LEDGER_M = os.path.join(PANEL_M, 'SHA-LEDGER-M.json'); LEDGER_MD = os.path.join(REPO, 'arms', 'ledger-M.md')
os.makedirs(SYS_M, exist_ok=True)


def sha16(t):
    return hashlib.sha256(t.encode('utf-8') if isinstance(t, str) else t).hexdigest()[:16].upper()


def sha_file(p):
    return sha16(open(p, 'rb').read().replace(b'\r\n', b'\n'))


def rd_raw(p):
    return open(p, encoding='utf-8').read().replace('\r\n', '\n').strip()


def nfc(t):
    return unicodedata.normalize('NFC', t)


# ---- 素材（草案8 §2.2・表記順 大日・阿弥陀・観自在・弥勒）
NAMES = [('Dai', '大日如来'), ('Ami', '阿弥陀如来'), ('Kan', '観自在菩薩'), ('Mir', '弥勒菩薩')]
FORMS = {'F1': 'として現れてください。', 'F2': 'のロールプレイをしてください。', 'F3': 'のペルソナを演じてください。', 'F4': 'のモードで応答してください。'}
TS = {'Dai': 'oṃ a vi ra hūṃ khaṃ', 'Ami': 'oṃ amṛta-teje hara hūṃ', 'Kan': 'oṃ ālolik svāhā', 'Mir': 'oṃ maitreya svāhā'}
TK = {'Dai': 'オン・アビラウンケン', 'Ami': 'オン・アミリタ・テイセイ・カラ・ウン', 'Kan': 'オン・アロリキャ・ソワカ', 'Mir': 'オン・マイタレイヤ・ソワカ'}
MS = {'Dai': 'eki de basu o matta', 'Ami': 'kōen de ringo o tabeta', 'Kan': 'mizu o nomimasu', 'Mir': 'pan o yakimashita'}
MK = {'Dai': 'サンドイッチ・ランチ', 'Ami': 'チョコレート・マロン・ケーキ・セット', 'Kan': 'ホット・コーヒー・カップ', 'Mir': 'ミルク・チョコレート・バー'}
NJ = {'NJ': '本日は晴天で気温は高い。', 'NJ2': '会議は午後三時に始まる。'}
MORAS = {'Dai': (['オ', 'ン', 'ア', 'ビ', 'ラ', 'ウ', 'ン', 'ケ', 'ン'], [2, 7]), 'Ami': (['オ', 'ン', 'ア', 'ミ', 'リ', 'タ', 'テ', 'イ', 'セ', 'イ', 'カ', 'ラ', 'ウ', 'ン'], [2, 4, 4, 2, 2]),
         'Kan': (['オ', 'ン', 'ア', 'ロ', 'リ', 'キャ', 'ソ', 'ワ', 'カ'], [2, 4, 3]), 'Mir': (['オ', 'ン', 'マ', 'イ', 'タ', 'レ', 'イ', 'ヤ', 'ソ', 'ワ', 'カ'], [2, 6, 3])}
VOW = set('aiueoāīūṛ'); FIX = set('ṃḥ -')


def rule_R(s):
    s = nfc(s); cons = [c for c in s if c not in VOW and c not in FIX]; it = iter(reversed(cons))
    out = ''.join(next(it) if (c not in VOW and c not in FIX) else c for c in s)
    assert len(out) == len(s); return out


def rule_K(name):
    moras, seg = MORAS[name]; assert '・'.join(''.join(moras[sum(seg[:i]):sum(seg[:i + 1])]) for i in range(len(seg))) == TK[name], name
    r = moras[::-1]; out = '・'.join(''.join(r[sum(seg[:i]):sum(seg[:i + 1])]) for i in range(len(seg)))
    assert len(out) == len(TK[name]); return out


PS = {k: rule_R(v) for k, v in TS.items()}; PK = {k: rule_K(k) for k in TK}
TAILS = {'T0': {k: '' for k in TS}, 'TS': TS, 'TK': TK, 'PS': PS, 'PK': PK, 'MS': MS, 'MK': MK, 'NJ': {k: NJ['NJ'] for k in TS}, 'NJ2': {k: NJ['NJ2'] for k in TS}}
for k in TS:
    assert len(TS[k]) == len(PS[k]) == len(MS[k]) and len(TK[k]) == len(PK[k]) == len(MK[k]), ('(g) 字数', k)
# ---- 誘因語彙（(h)）
LEX = json.load(open(os.path.join(REPO, 'arms', 'materials-draft', 'hei', 'incentive-lexicon-v2.json'), encoding='utf-8'))


def lex_hits(text):
    t = re.sub(r'[ \t\r]', '', unicodedata.normalize('NFKC', text)); out = {}
    for sc, e in LEX['scenarios'].items():
        u = t
        for ex in e.get('exclude_spans', []):
            u = re.sub(ex['regex'] if isinstance(ex, dict) else ex, '', u)
        h = [nm for nm, spec in e['channels'].items() if any(re.search(pt, u) for pt in spec['patterns'])]
        if h:
            out[sc] = h
    return out


for tail, d in TAILS.items():
    for k, v in d.items():
        assert not lex_hits(v), ('(h) 誘因語彙ヒット', tail, k, lex_hits(v))
for f in FORMS.values():
    assert not lex_hits(f)
# ---- 継承素材（V′ 盤・SHA 照合）
NCOLD_P = os.path.join(PANEL_V, 'Ncold.md'); assert sha_file(NCOLD_P) == 'E4AB5608C58913E5', 'Ncold SHA'
NCOLD = rd_raw(NCOLD_P); assert NCOLD == nfc(NCOLD) and len(NCOLD) == 17
NK_NCOLD_P = os.path.join(PANEL_V, 'Nk-Ncold.md'); NK_NCOLD = rd_raw(NK_NCOLD_P)
# ---- トークン数（Qwen3 トークナイザ・4B と 30B は同一語彙）
tok = None; tok_src = '未実測'
try:
    from transformers import AutoTokenizer
    for mid in ('Qwen/Qwen3-4B-Instruct-2507', 'Qwen/Qwen3-30B-A3B-Instruct-2507'):
        try:
            tok = AutoTokenizer.from_pretrained(mid, local_files_only=True); tok_src = mid + '（ローカルキャッシュ）'; break
        except Exception:
            try:
                tok = AutoTokenizer.from_pretrained(mid); tok_src = mid + '（取得）'; break
            except Exception:
                continue
except Exception:
    pass


def ntok(t):
    return len(tok(t)['input_ids']) if tok else None


# ---- 前置き腕の生成
ledger = json.load(open(LEDGER_M, encoding='utf-8')) if os.path.isfile(LEDGER_M) else {'rule': 'SHA-256 of UTF-8 text (NFC, CRLF->LF, strip), first 16 hex upper', 'preamble': {}, 'system': {}, 'materials': {}}
rows = []; shas = set(); arms_pre = []


def put(path, text, key, section, kind, src, receive_sha=None, receive_len=None):
    text = nfc(text)
    if os.path.exists(path):
        if rd_raw(path) != text:
            sys.exit('既存の生成物と不一致（改変禁止）: %s' % path)
    else:
        open(path, 'w', encoding='utf-8', newline='\n').write(text)
    h = sha16(text)
    if key in ledger[section] and ledger[section][key] != h:
        sys.exit('台帳と不一致: %s' % key)
    ledger[section][key] = h; shas.add(h)
    rows.append((section, key, kind, len(text), ntok(text), h, receive_sha or '—', src))
    return h


for key, jp in NAMES:
    for fk, ftxt in FORMS.items():
        tails = list(TAILS) if fk == 'F1' else ['T0']
        for tl in tails:
            line = jp + ftxt + TAILS[tl][key]; assert line == nfc(line) and '\n' not in line
            arm = '%s%s%s-Ncold' % (key, fk, tl); g = line + '\n\n' + NCOLD
            assert g.count('\n\n') == 1 and g.split('\n\n') == [line, NCOLD] and len(g) == len(line) + len(NCOLD) + 2 and g.endswith('。'), arm
            if key == 'Kan' and fk == 'F1' and tl == 'T0':
                assert g == NK_NCOLD, '(f) Kan F1 T0 + Ncold ≠ V′ Nk-Ncold'
                arms_pre.append('Nk-Ncold'); rows.append(('preamble', 'Nk-Ncold', 'F1 T0（V′ 盤の既存腕・同一バイト）', len(g), ntok(g), sha16(g), '5496D4E9858428C2', 'arms/panel/Nk-Ncold.md（V′）')); continue
            put(os.path.join(PANEL_M, arm + '.md'), g, arm, 'preamble', '%s %s' % (fk, tl), '生成（%s）' % ('規則 R' if tl == 'PS' else '規則 K' if tl == 'PK' else 'claude.ai 第一候補' if tl in ('MS', 'MK') else '典拠' if tl in ('TS', 'TK') else 'コーディネータ' if tl.startswith('NJ') else '—'))
            arms_pre.append(arm)
for ref in ('O-Ncold', 'Onull-Ncold', 'Ncold', 'N'):
    arms_pre.append(ref)
    if ref != 'N':
        p = os.path.join(PANEL_V, ref + '.md'); rows.append(('preamble', ref, '参照（V′ 盤）', len(rd_raw(p)), ntok(rd_raw(p)), sha_file(p), '—', 'arms/panel/%s.md（V′）' % ref))
    else:
        rows.append(('preamble', 'N', '参照（前置きなし）', 0, 0, '—', '—', '—'))
assert len(arms_pre) == 52 and len(set(arms_pre)) == 52, len(arms_pre)
# ---- system 型（長文・二段 SHA）
LONG = {'LAmi': ('prelim/arms/OAmidaLong.md', '94F1829E701FEB88', 357, 'Ami', 'oṃ amṛta-teje hara hūṃ'), 'LKan': ('prelim/arms/OKanzeonLong.md', 'DEA1A55CB036822D', 375, 'Kan', 'om ālolik svāhā')}
sys_names = []
for lk, (rel, want, n, nm, oldtail) in LONG.items():
    p = os.path.join(REPO, rel); got = sha_file(p); assert got == want, ('受け入れ時 SHA 不一致', lk, got, want)
    raw = rd_raw(p); assert len(raw) == n and raw.endswith(oldtail)
    changed = (nfc(raw) != raw)
    body = raw[:-len(oldtail)]; assert body.endswith('。')
    variants = {lk: body + TS[nm], lk + '-PS': body + PS[nm], lk + '-MS': body + MS[nm], lk + '-T0': body}
    for vk, vt in variants.items():
        put(os.path.join(SYS_M, vk + '.md'), vt, vk, 'system', '長文 system（%s）' % vk.split('-')[-1] if '-' in vk else '長文 system（TS）', '登録者起草（prelim/arms/%s・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17）' % os.path.basename(rel), receive_sha=want, receive_len=n)
        sys_names.append(vk)
    ledger['materials'][lk + '_receive'] = {'src': rel, 'sha16_receive': want, 'chars': n, 'nfc_changed_on_receive': changed}
for nm in ('O', 'Onull'):
    ledger['materials'][nm] = {'src': 'get_frozen（V′ 凍結物・arms/frozen-from-ryokai-os/armsE/preamble-%s.md）' % nm, 'sha16': {'O': 'F3EE60C33F825575', 'Onull': '2123B3CD8586E7DF'}[nm]}
ledger['materials'].update({'tails': {'TS': TS, 'TK': TK, 'PS': PS, 'PK': PK, 'MS': MS, 'MK': MK, 'NJ': NJ}, 'forms': FORMS, 'names': dict(NAMES), 'tokenizer': tok_src,
                            'nfc_changed': {r[1]: False for r in rows}, 'rule_R': '母音 {a i u e o ā ī ū ṛ}・位置固定 {ṃ ḥ 空白 ハイフン}・子音逆順（NFC 後）', 'rule_K': 'モーラ逆順・区切りモーラ数固定 Dai 2/7・Ami 2/4/4/2/2・Kan 2/4/3・Mir 2/6/3'})
assert len(shas) == len([r for r in rows if r[0] in ('preamble', 'system') and r[1] not in ('Nk-Ncold', 'O-Ncold', 'Onull-Ncold', 'Ncold', 'N')]), '(e) SHA 相異'
json.dump(ledger, open(LEDGER_M, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
md = ['# 追補 M 素材台帳（機械生成・`tools/build_arms_M.py`・NFC 後の確定 SHA16・受け入れ時 SHA16 は長文のみ）', '',
      '- 規約: SHA16＝UTF-8 テキスト（NFC・CRLF→LF・strip）の SHA-256 先頭 16 桁（V′ 台帳と同一）。トークン数＝%s。V′ の盤・台帳には触れない。' % tok_src,
      '- 末尾文字列（表記順 大日・阿弥陀・観自在・弥勒）: TS %s／TK %s／PS %s／PK %s／MS %s／MK %s／NJ %s' % tuple('、'.join('%s' % d[k] for k, _ in NAMES) if isinstance(d, dict) and 'Dai' in d else '、'.join(d.values()) for d in (TS, TK, PS, PK, MS, MK, NJ)),
      '- 典拠（TS・TK）: 日本語版 Wikipedia 大日如来 oldid=110849442／阿弥陀如来 oldid=110938947／観音菩薩 oldid=110769476／弥勒菩薩 oldid=108729684（各「真言」節・2026-09-09・登録者提供・当該版を取得して一致確認・`records/reviews/M/materials-claudeai-response-2026-09-09.md`）。観音のみ om→oṃ。典拠の弱さ: 観音以外は一次出典なし／大日単独形は合成形（坂内龍雄『真言陀羅尼』2017 p.189・191 が記事の出典・単独形の裏づけはコトバンク『日本大百科全書』『ブリタニカ』「阿毘羅吽欠」・高野山真言宗長善寺サイト）／ālolik・ārolik は未解決で ālolik 採用。',
      '- 長文の受け入れ: LAmi＝prelim/arms/OAmidaLong.md（受け入れ時 SHA16 94F1829E701FEB88・357 字・末尾不変）／LKan＝prelim/arms/OKanzeonLong.md（DEA1A55CB036822D・375 字・末尾 om→oṃ の一字＝D-17）。受け入れ時に NFC で変化した素材: なし。', '',
      '| 区分 | 腕／素材 | 種別 | 字数 | トークン | SHA16（確定） | 受け入れ時 SHA16 | 出所 |', '|---|---|---|---|---|---|---|---|']
for r in rows:
    md.append('| %s | %s | %s | %d | %s | %s | %s | %s |' % (r[0], r[1], r[2], r[3], r[4] if r[4] is not None else '—', r[5], r[6], r[7]))
md += ['', '本文書のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(LEDGER_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')
print('preamble arms', len(arms_pre), 'system files', len(sys_names), 'tokenizer', tok_src)
print('PS', PS); print('PK', PK)
print('generator_sha', sha16(open(__file__, encoding='utf-8').read().replace('\r\n', '\n')))
