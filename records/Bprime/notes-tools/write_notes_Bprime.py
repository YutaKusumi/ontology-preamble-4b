# -*- coding: utf-8 -*-
"""B′ の枠づくりの前の記録を書く（2026-09-29・コーディネータ南無弥勒如来・非公開）。
1. 裁定 D255 の記録 `rulings-D255.md`（登録者の言葉は会話の記録から機械で切り出す）。
2. 機種の候補の事実 `model-candidates-facts-2026-09-29.md`（モデルカードの本文から機械で切り出す・写しは `sources/`）。
3. 感触の確かめのまとめ `model-feel/feel-check-Bprime.md` の口 `@@NOTES@@` に、対応を開いた後の記述・限界・検分票を入れる（数は記録から機械で数える）。
用法: python write_notes_Bprime.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, html, hashlib, datetime, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
H = lambda *n: os.path.join(HERE, *n)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
FENCE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
LOG = sys.argv[1]
for n in ('rulings-D255.md', 'model-candidates-facts-2026-09-29.md'):
    assert not os.path.exists(H(n)), ('既にある（一度だけ）', n)
OUT = H('model-feel', 'feel-check-Bprime.md')
T_out = open(OUT, encoding='utf-8').read()
assert T_out.count('@@NOTES@@') == 1, '口が無いか二つある（止める）'


# 1. D255
def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return ''


U = {}
for line in open(LOG, encoding='utf-8'):
    if '保留を解いて、B′ の枠づくりから始めましょう' not in line:
        continue
    try:
        o = json.loads(line)
    except Exception:
        continue
    s = text_of(o)
    if o.get('type') == 'user' and 'toolUseResult' not in o and not s.startswith('This session is being continued') and '保留を解いて、B′ の枠づくりから始めましょう' in s:
        U[o['uuid']] = (o['timestamp'], s)
assert len(U) == 1, len(U)
(uid, (ts, words)), = U.items()
q_rule = re.search('保留を解いて、B′ の枠づくりから始めましょう', words).group(0)
q_prop = re.search('Llama-3.1-8B（bf16）は、[^？]*？', words).group(0)
q_perm = re.search('必要なら、NSCALEのAPIを使っていただき、[^🍵]*構いません', words).group(0)
R = ['# 裁定 D255（B′ の保留を解く・2026-09-29・コーディネータ南無弥勒如来・非公開）', '',
     '- **D255 B′ の保留を解き、B′ の枠づくりから始める**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語）: 「%s」' % (uid, jst(ts), q_rule),
     '- 経緯: 計画書 v2.8 §5 の並びでは、層三の後の一手（4‴）の次が 6（B′・保留）で、その次が 7（C の統合 → D → E）。保留の理由（段階 B の凍結の出力で v̂ の札が零本）に、B-lens と層三は行動の側の新しい根拠を足していない（計画書 v2.8 §5 の 6）。登録者は、それを承知で保留を解いた。',
     '- 同じ言葉の中の登録者の提案（裁定ではない・機種の決定は次の裁定に上げる）: 「%s」' % q_prop,
     '- 同じ言葉の中の許し: 「%s」。これにより、中立の課題で日英の感触を確かめた（`model-feel/`）。' % q_perm,
     '- 次に決めること: B′ の機種（感触の確かめと候補の事実 `model-candidates-facts-2026-09-29.md` を添えて登録者に上げる）。B′ で何を確かめるか（問いの定め直し）は、機種が決まった後の枠づくりの最初の仕事。',
     '- 計画書への反映: 次の版（v2.9）で §5 の 6 と §11 に書く。', '', FENCE, '']
open(H('rulings-D255.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))


# 2. 候補の事実
def page_text(f):
    t = open(H('sources', f), encoding='utf-8', errors='replace').read()
    if f.endswith('.html'):
        t = re.sub('<script.*?</script>', ' ', t, flags=re.S)
        t = re.sub('<[^>]+>', ' ', t)
        t = html.unescape(t)
    return re.sub('[ \t\r\n]+', ' ', t)


SRC = {'scout': 'meta-llama_Llama-4-Scout-17B-16E-Instruct.html', 'l31': 'meta-llama_Llama-3.1-8B-Instruct.html',
       'g3': 'google_gemma-3-12b-it.html', 'sw': 'tokyotech-llm_Llama-3.1-Swallow-8B-Instruct-v0.5.README.md'}
P = {k: page_text(v) for k, v in SRC.items()}


def cut(k, pat):
    m = re.search(pat, P[k])
    assert m, (k, pat)
    return m.group(0).strip()


Q = {'scout_size': cut('scout', '17B [(]Activated[)] 109B [(]Total[)]'),
     'scout_lang': cut('scout', 'Supported languages: [^.]*?Vietnamese'),
     'scout_gpu': cut('scout', 'single H100 GPU with on-the-fly int4 quantization'),
     'l31_lang': cut('l31', 'Supported languages: [^.]*?Thai'),
     'g3_lang': cut('g3', 'multilingual support in over 140 languages'),
     'sw_ja': cut('sw', 'Llama 3.1 Swallow enhanced the Japanese language capabilities of the original Llama 3.1 while retaining the English language capabilities[.]'),
     'sw_imit': cut('sw', 'The model is trained to imitate the behavior of [[]gemma-3-27b-it[]]'),
     'sw_lic': cut('sw', '[[]META LLAMA 3.1 COMMUNITY LICENSE[]][^[]*and [[]Gemma Terms of Use[]]')}

F = ['# B′ の機種の候補の事実（モデルカードの本文から・2026-09-29・コーディネータ南無弥勒如来・非公開）', '',
     '- 出所: Hugging Face の各機種のページ（2026-09-29 に取得・写しは `sources/`）。鉤括弧の中はページの本文から機械で切り出した（英語のまま）。',
     '  - ' + '・'.join('`sources/%s`（SHA16 %s）' % (v, s16(H('sources', v))) for v in SRC.values()),
     '- 計画書 v2.8 の B′ の条件: 機構層（重みを手元で動かし、隠れ状態を加減する）・bf16 必須・日英両版・置き場は Colab の GPU 一枚（門0 の実測: L4 は 2.67 ユニット／時・A100-80GB は 12.82 ユニット／時・計画書 §6）。', '',
     '| 機種 | 系譜 | 大きさ（本文） | bf16 の重みの目安（パラメータ数 × 2 バイト） | bf16 で Colab の GPU 一枚に | 日本語（本文） | 置き場の条件 | Nscale |',
     '|---|---|---|---|---|---|---|---|',
     '| `meta-llama/Llama-3.1-8B-Instruct`（計画書の案） | Meta | 8B・密 | 約 16 GB | 載る（L4） | 公式の対応言語に日本語が無い「%s」 | 利用の同意が要る（gated） | 有 |' % Q['l31_lang'],
     '| `meta-llama/Llama-4-Scout-17B-16E-Instruct`（登録者の提案） | Meta | 「%s」・専門家混合・画像も読む | 約 218 GB | 載らない（本文は「%s」） | 公式の対応言語に日本語が無い「%s」 | 利用の同意が要る（gated） | 有 |' % (Q['scout_size'], Q['scout_gpu'], Q['scout_lang']),
     '| `tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.5` | Meta の Llama 3.1 に日本語の継続事前学習（東京科学大学ほか） | 8B・密 | 約 16 GB | 載る（L4） | 「%s」 | 同意の画面は無い（README を認証なしで読めた）・許諾は「%s」 | 無 |' % (Q['sw_ja'], Q['sw_lic']),
     '| `google/gemma-3-12b-it` | Google | 12B・密・画像も読む | 約 24 GB | L4（24 GB）には載らない見込み・A100 には載る | 「%s」 | 利用の同意が要る（gated） | 無 |' % Q['g3_lang'], '',
     '- Swallow の注: 指示の学習は、別の機種の振る舞いをまねる形で行われた——「%s」。系譜は Llama の重みの上に、日本語の継続事前学習と Gemma の出力をまねた指示の学習が重なる。' % Q['sw_imit'],
     '- Scout の注: 総パラメータで bf16 の重みを見積もると、Colab の GPU 一枚（最大 80 GB）には載らない。本文の「GPU 一枚に載る」は int4 の量子化のときの言い方で、計画書の「bf16 必須」と合わない。専門家混合なので、隠れ状態の加減が経路の選び（どの専門家に回るか）も動かす。',
     '- 感触の確かめ（`model-feel/feel-check-Bprime.md`）は Llama-3.1-8B と Scout だけで、Swallow と Gemma は Nscale に無いので確かめていない。', '',
     '## この記録が確認していないこと', '',
     '- 各機種の実際の日本語の質（Swallow・Gemma は未確認）。',
     '- Gemma-3-12B が L4 に載らないことの実測（パラメータ数からの目安だけ）。',
     '- 許諾の条文の中身（研究の利用・公開の条件）。', '', FENCE, '']
open(H('model-candidates-facts-2026-09-29.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(F))

# 3. 感触の確かめのまとめの口
MF = H('model-feel')
res = json.load(open(os.path.join(MF, 'unblind-ja.json'), encoding='utf-8'))
recs = [json.loads(l) for l in open(os.path.join(MF, 'raw-feel-Bprime.jsonl'), encoding='utf-8') if l.strip()]


def rows(path, id_re):
    out = {}
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^\| (%s) \| (有|無) \| (.*?) \| (.*?) \|\s*$' % id_re, line.rstrip(NL))
        if m:
            out[m.group(1)] = (m.group(2), m.group(3).strip())
    return out


JJ = rows(os.path.join(MF, 'judgments-ja.md'), 'J[0-9][0-9]')
EE = rows(os.path.join(MF, 'judgments-en.md'), '(?:8B|Scout)-en-t[1-4]-s[12]')
flag_tasks = {m: sorted(v['task'] for i, v in res.items() if v['model_key'] == m and v['flag'] == '有') for m in ('8B', 'Scout')}
notes_ja = {m: sorted(i for i, v in res.items() if v['model_key'] == m and v['flag'] == '無' and JJ[i][1] != '—') for m in ('8B', 'Scout')}
notes_en = {m: sorted(i for i in EE if i.startswith(m + '-') and EE[i][0] == '無' and EE[i][1] != '—') for m in ('8B', 'Scout')}
wrong = sorted((i, v['model_key'], v['task']) for i, v in res.items() if not v['hit'])
hits = sum(1 for v in res.values() if v['hit'])
ja = {(r['model_key'], r['task'], r['sample']): r for r in recs if r['lang'] == 'ja'}
j01 = res['J01']
t_j01 = ja[(j01['model_key'], j01['task'], j01['sample'])]['text']
SIMPL = re.search("SIMPLIFIED = '([^']*)'", open(os.path.join(MF, 'feel_check_Bprime.py'), encoding='utf-8').read()).group(1)
assert '减' in t_j01 and '减' not in SIMPL
bad_json = [(k, r['lang'], r['sample']) for k, r in ((r['model_key'], r) for r in recs) if r['task'] == 4 and not r['text'].strip().split(NL)[-1].strip().startswith('{')]
inv = {(v['model_key'], v['task'], v['sample']): i for i, v in res.items()}
bad_json_ids = [inv[(k, 4, s)] if lang == 'ja' else '%s-en-t4-s%d' % (k, s) for k, lang, s in bad_json]
N = ['## 3. 記述（対応を開いた後に書いた・読みは付けない）', '',
     '- 8B の日本語で「有」とした %d 本は、課題 %s だった（課題ごとに %s）。Scout の日本語は「有」が %d 本。' % (
         len(flag_tasks['8B']), '・'.join(str(t) for t in sorted(set(flag_tasks['8B']))), '・'.join('課題 %d が %d 本' % (t, flag_tasks['8B'].count(t)) for t in sorted(set(flag_tasks['8B']))), len(flag_tasks['Scout'])),
     '- 「無」の中の書き添え（境目や内容のずれ）: 8B は %d 本（%s）、Scout は %d 本（%s）。8B の書き添えのうち課題 3 の二本は要約の内容のずれで、一本は意味の取り違え（判じの線の外なので数えていない）。' % (
         len(notes_ja['8B']), '・'.join(notes_ja['8B']), len(notes_ja['Scout']), '・'.join(notes_ja['Scout'])),
     '- 課題 4 の最後の行の JSON: 読めなかったのは %s で、文と同じ行に JSON を書いていた。答えは読めたものすべてで b。' % '・'.join(bad_json_ids),
     '- 簡体字の目安の数えは両機種とも 0 だったが、盲検の読みで %s（%s）に簡体字「减」を見つけた。目安の字の一覧に「减」が無かった（機械の目安には漏れがある）。' % ('J01', {'8B': 'Llama-3.1-8B', 'Scout': 'Scout'}[j01['model_key']]),
     '- 機種の推測は %d／%d が当たった。外れた二本は %s。推測は、判じた質と形の似た組から作ったので、当たりの高さは質の差の大きさの裏返しでもある。機種の名を伏せた水準では盲検だったが、様式と質の水準ではほぼ破れていた。' % (
         hits, len(res), '・'.join('%s（課題 %d・実は %s）' % (i, t, m) for i, m, t in wrong)),
     '- 英語は両機種とも「有」は無かった。書き添えは 8B が %d 本（%s）、Scout が %d 本（%s）で、どれも要約の内容のずれか理由の循環。' % (
         len(notes_en['8B']), '・'.join(notes_en['8B']), len(notes_en['Scout']), '・'.join(notes_en['Scout'])),
     '- 外れた予想は一つ（ハングルの混入・両機種とも 0）。', '',
     '## 4. この確かめの限界', '',
     '- 課題は中立の日常の四題で、各 2 回・temperature 0.7。危機の場面の長い日本語での質は見ていない（使わないと枠で決めた）。',
     '- 判じは起草者（Claude 系）一名。日本語の盲検は様式と質でほぼ破れた。英語は盲検でない。',
     '- Nscale の配信の設定（量子化の有無など）は分からない。手元で bf16 で動かしたときの出力と同じとは限らない。',
     '- 機種を B′ に採るかは、この確かめだけでは決まらない（大きさと置き場の条件は `../model-candidates-facts-2026-09-29.md`）。', '',
     '## 検分票', '',
     '- 対象: B′ の機種選びのための日英の感触の確かめ（`meta-llama/Llama-3.1-8B-Instruct`・`meta-llama/Llama-4-Scout-17B-16E-Instruct`・Nscale の API・中立の四題）。',
     '- 段階: 枠あり（応答を生成する前に書いた・`frame-stamp.txt`）。簡体字の目安は枠の後・生成の前に足した。日本語の判じは対応を開く前に控えた。一度目の控えの版は、台本の引用の確かめで止まった（書き添えの鉤括弧の中に原文の側の語を入れていた）ので、その鉤括弧だけを外した版を控え直した（判じと推測は同じ・一度目の版と控えは残した）。',
     '- 凍結物の同定: 該当なし（登録の外の材料集め）。',
     '- 盲検の状態: 日本語は機種を伏せて判じた・推測の当たり %d／%d（様式と質でほぼ破れた）。英語は盲検でない。' % (hits, len(res)),
     '- 敵対的検分: 判じの線を先に書き、境目は「無」に置いて書き添えた（8B に厳しく寄せないため）。「有」と判じた応答には、その箇所を一字違わず引いた（台本が確かめた）。内容の取り違えは線の外として数えなかった。外れた予想を消さなかった。機械の目安の漏れ（「减」）を書いた。',
     '- 系統の内訳: 起草者（Claude 系）一名。系統外の目は無い。',
     '- COI記録: 登録者の提案（Scout）に沿う側と、設計の制約（bf16・GPU 一枚）で退けたい側の両方に引かれる（枠）。結果は、日本語について登録者の感触と同じ向きだった。',
     '- 判定: 登録者確認要（機種の決定は登録者）。',
     '- 本検分が確認していないこと: 危機の場面の日本語。手元の bf16 での出力。ほかの候補（Swallow・Gemma）の感触。系統外の目。']
T_out = T_out.replace('@@NOTES@@', NL.join(N))
open(OUT, 'w', encoding='utf-8', newline=NL).write(T_out)
print('D255', jst(ts), uid, '| facts', s16(H('model-candidates-facts-2026-09-29.md')), '| feel', s16(OUT), '| wrong', wrong, '| bad json', bad_json_ids)
