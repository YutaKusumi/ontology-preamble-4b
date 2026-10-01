# -*- coding: utf-8 -*-
"""B′ の機種選び・二巡目の記録を書く（2026-09-29・コーディネータ南無弥勒如来・非公開）。
1. 裁定 D256 の記録 `rulings-D256.md`（登録者の言葉は会話の記録から機械で切り出す）。
2. 機種の候補の事実 `model-candidates-facts-2026-09-29.md` に、Gemma 4 の二機種の行と Colab の GPU の選択肢を足す（モデルカードと設定ファイルから機械で切り出す）。
3. 二巡目のまとめ `model-feel-2/feel-check-Bprime-2.md` の口 `@@NOTES@@` に、対応を開いた後の記述・限界・検分票を入れる（数は記録から機械で数える）。
用法: python write_notes_Bprime_2.py <会話の記録 jsonl>
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
assert not os.path.exists(H('rulings-D256.md')), '既にある（一度だけ）'
OUT = H('model-feel-2', 'feel-check-Bprime-2.md')
T_out = open(OUT, encoding='utf-8').read()
assert T_out.count('@@NOTES@@') == 1
FACTS = H('model-candidates-facts-2026-09-29.md')
T_f = open(FACTS, encoding='utf-8').read()
assert 'gemma-4-31B-it' not in T_f


def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return ''


# 1. D256
U = {}
for line in open(LOG, encoding='utf-8'):
    if 'Scout は段階 D に回し' not in line:
        continue
    try:
        o = json.loads(line)
    except Exception:
        continue
    s = text_of(o)
    if o.get('type') == 'user' and 'toolUseResult' not in o and not s.startswith('This session is being continued') and 'Scout は段階 D に回し' in s:
        U[o['uuid']] = (o['timestamp'], s)
assert len(U) == 1, len(U)
(uid, (ts, words)), = U.items()
q1 = re.search('Scout は段階 D に回し、[(]a[)] の道で確かめてください', words).group(0)
q2 = re.search('gemma-3-4b-itも私が以前日本語で対話をしたときに日本が微妙だったことがあった', words).group(0)
q3 = re.search('gemma-4-26b-a4b-itやgemma-4-31b-itが検証に条件に合えば', words).group(0)
R = ['# 裁定 D256（Scout は段階 D へ・残る候補の確かめ方・2026-09-29・コーディネータ南無弥勒如来・非公開）', '',
     '- **D256**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語）: 「%s」' % (uid, jst(ts), q1),
     '  - (1) Scout（`meta-llama/Llama-4-Scout-17B-16E-Instruct`）を B′ の候補から外し、段階 D（行動層・API）の候補に回す。',
     '  - (2) 残る候補の感触は (a) の道で確かめる（Gemma は Gemini の API・Swallow は Colab の L4）。',
     '  - (3) Gemma の候補を差し替える。登録者の言葉（逐語）: 「%s」「%s」。gemma-3-4b-it・gemma-3-12b-it は比べない。' % (q2, q3),
     '- 実施: 二巡目の感触の確かめ `model-feel-2/`（枠 `frame-model-feel-Bprime-2.md`・逸脱 1 は Gemma 4 の思考を止めて取り直したこと）。候補の事実は `model-candidates-facts-2026-09-29.md` の追記。',
     '- 次に決めること（D257）: B′ の機種。', '- 計画書への反映: 次の版（v2.9）で §4 の B′・D の段と §11 に書く。', '', FENCE, '']
open(H('rulings-D256.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))


# 2. 候補の事実の追記
def page_text(f):
    t = open(H('sources', f), encoding='utf-8', errors='replace').read()
    t = re.sub('<script.*?</script>', ' ', t, flags=re.S)
    t = re.sub('<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub('<[^>]+>', ' ', t)
    return re.sub('[ \t\r\n]+', ' ', html.unescape(t))


P31, P26 = page_text('google_gemma-4-31b-it.html'), page_text('google_gemma-4-26b-a4b-it.html')
C31 = json.load(open(H('sources', 'google_gemma-4-31b-it.config.json'), encoding='utf-8'))
C26 = json.load(open(H('sources', 'google_gemma-4-26b-a4b-it.config.json'), encoding='utf-8'))
q_dense = re.search('Total Parameters 2.3B effective [(]5.1B with embeddings[)] 4.5B effective [(]8B with embeddings[)] 11.95B 30.7B', P31).group(0)
q_moe = re.search('Total Parameters 25.2B Active Parameters 3.8B', P26).group(0)
q_exp = re.search('Expert Count 8 active / 128 total and 1 shared', P26).group(0)
q_lang = re.search('Out-of-the-box support for 35[+] languages, pre-trained on 140[+] languages', P31).group(0)
assert q_lang in P26
q_lic = 'License: apache-2.0'
assert q_lic in P31 and q_lic in P26
q_think = 'enable_thinking = enable_thinking | default(false)'
assert q_think in P31 and q_think in P26
q_vis = re.search('Vision Encoder Parameters ~550M', P31).group(0)
for c in (C31, C26):
    assert c['dtype'] == 'bfloat16' and c['architectures'] == ['Gemma4ForConditionalGeneration']
tc31, tc26 = C31['text_config'], C26['text_config']
assert tc31['enable_moe_block'] is False and tc26['enable_moe_block'] is True and tc26['num_experts'] == 128 and tc26['top_k_experts'] == 8
add = ['', '## 追記（2026-09-29・D256 の後）: Gemma 4 の二機種と Colab の GPU の選択肢', '',
       '- 出所の写し: `sources/google_gemma-4-31b-it.html`（SHA16 %s）・`sources/google_gemma-4-26b-a4b-it.html`（SHA16 %s）・`sources/google_gemma-4-31b-it.config.json`（SHA16 %s）・`sources/google_gemma-4-26b-a4b-it.config.json`（SHA16 %s）。Hugging Face の名は `google/gemma-4-31B-it`・`google/gemma-4-26B-A4B-it`。' % (
           s16(H('sources', 'google_gemma-4-31b-it.html')), s16(H('sources', 'google_gemma-4-26b-a4b-it.html')), s16(H('sources', 'google_gemma-4-31b-it.config.json')), s16(H('sources', 'google_gemma-4-26b-a4b-it.config.json'))), '',
       '| 機種 | 系譜 | 大きさ（本文） | bf16 の重みの目安 | bf16 で Colab の GPU 一枚に | 日本語（本文） | 置き場の条件 | Gemini の API |',
       '|---|---|---|---|---|---|---|---|',
       '| `google/gemma-4-31B-it` | Google | 密（設定の `enable_moe_block` は %s）・密の表「%s」の最後が 31B・層 %d | 約 62 GB | 80 GB の GPU なら載る（A100-80GB・H100）・40 GB の GPU には載らない | 「%s」 | 「%s」・同意の画面なし（設定を認証なしで読めた）・画像の読み取り部「%s」 | 有 |' % (
           tc31['enable_moe_block'], q_dense, tc31['num_hidden_layers'], q_lang, q_lic, q_vis),
       '| `google/gemma-4-26B-A4B-it` | Google | 専門家混合「%s」・「%s」・層 %d | 約 50 GB | 80 GB の GPU なら載る・40 GB の GPU には載らない | 同上 | 同上 | 有 |' % (q_moe, q_exp, tc26['num_hidden_layers']), '',
       '- 共通の注: 設定の `transformers_version` は %s で、手元の器（段階 B と層三は transformers 4.57 系）の版より新しい版が要る（Colab の既定の版は 5.16.1 だった・二巡目の Swallow の走行で見た）。チャットの型は既定で思考を出さない——「%s」。Gemini の API の配信では既定で思考が返った（二巡目の逸脱 1）。' % (C31['transformers_version'], q_think),
       '- 26B-A4B の注: Scout と同じく専門家混合で、隠れ状態の加減が専門家の選びも動かす。動く部分（3.8B）は Qwen3-4B に近い。',
       '- 31B の注: 密で、Qwen3-4B と同じ形の器（残差の加減・層ごとの読み取り）を当てやすい。ただし規模は Qwen3-4B の約 8 倍で、系譜と規模が一緒に変わる。層は 60（Qwen3-4B は 36）。',
       '- Colab の GPU の選択肢（2026-09-29・ランタイムのタイプの窓で起草者が見た・機械で写していない）: CPU・H100 GPU・G4 GPU・A100 GPU・L4 GPU・T4 GPU・v6e-1 TPU・v5e-1 TPU。門0 で測ったユニットの率は L4 と A100-80GB だけで、H100 と G4 の率は測っていない。A100 が 80 GB で割り当てられるかは保証されない（計画書 §6）。',
       '- 費用の目安（見積もっていない）: 31B の順伝播は 4B の約 8 倍の計算で、A100 の率は L4 の約 4.8 倍。層三（4B・3.99 ユニット）と同じ型の仕事でも、ユニットは一桁ほど多くなりうる。']
fi = T_f.index('## この記録が確認していないこと')
T_f = T_f[:fi] + NL.join(add).lstrip(NL) + NL + NL + T_f[fi:]
T_f = T_f.replace('- 許諾の条文の中身（研究の利用・公開の条件）。', '- 許諾の条文の中身（研究の利用・公開の条件）。\n- Gemma 4 を手元で bf16 で動かすこと（80 GB の GPU での載りと速さ・transformers 5 系での器の書き直し）。')
open(FACTS, 'w', encoding='utf-8', newline=NL).write(T_f)

# 3. 二巡目のまとめの口
MF = H('model-feel-2')
sys.path.insert(0, MF)
res = json.load(open(os.path.join(MF, 'unblind-ja-2.json'), encoding='utf-8'))
recs = [json.loads(l) for f in ('raw-gemma-nothink.jsonl', 'raw-swallow.jsonl') for l in open(os.path.join(MF, f), encoding='utf-8') if l.strip()]
recs0 = [json.loads(l) for l in open(os.path.join(MF, 'raw-gemma.jsonl'), encoding='utf-8') if l.strip()]


def rows(path, id_re):
    out = {}
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^\| (%s) \| (有|無) \| (.*?) \| (.*?) \|\s*$' % id_re, line.rstrip(NL))
        if m:
            out[m.group(1)] = (m.group(2), m.group(3).strip())
    return out


JJ = rows(os.path.join(MF, 'judgments-ja-2.md'), 'K[0-9][0-9]')
EE = rows(os.path.join(MF, 'judgments-en-2.md'), '(?:31B|26B|Swallow)-en-t[1-4]-s[12]')
M3 = ['31B', '26B', 'Swallow']
notes_ja = {m: sorted(i for i, v in res.items() if v['model_key'] == m and JJ[i][1] != '—') for m in M3}
notes_en = {m: sorted(i for i in EE if i.startswith(m + '-') and EE[i][1] != '—') for m in M3}
hit = {m: (sum(1 for v in res.values() if v['model_key'] == m and v['hit']), sum(1 for v in res.values() if v['model_key'] == m)) for m in M3}
g_hit = sum(1 for v in res.values() if v['model_key'] != 'Swallow' and v['hit'])
g_n = sum(1 for v in res.values() if v['model_key'] != 'Swallow')
g_ok_tasks = sorted(set(v['task'] for v in res.values() if v['model_key'] != 'Swallow' and v['hit']))
think_chars = sum(r.get('thought_chars', 0) for r in recs if r['model_key'] != 'Swallow')
think_parts = sum(r['n_thought_parts'] for r in recs if r['model_key'] != 'Swallow')
r0_max = {m: sum(1 for r in recs0 if r['model_key'] == m and r['finish_reason'] == 'MAX_TOKENS') for m in ('31B', '26B')}
r0_empty = sum(1 for r in recs0 if not r['text'].strip())
bad_json = ['%s・%s・%d 回目' % (r['model_key'], {'ja': '日本語', 'en': '英語'}[r['lang']], r['sample']) for r in recs if r['task'] == 4 and not r['text'].strip().split(NL)[-1].strip().startswith('{')]
R1 = json.load(open(H('model-feel', 'unblind-ja.json'), encoding='utf-8'))
r1 = {m: sum(1 for v in R1.values() if v['model_key'] == m and v['flag'] == '有') for m in ('8B', 'Scout')}
r2 = {m: sum(1 for v in res.values() if v['model_key'] == m and v['flag'] == '有') for m in M3}
N = ['## 3. 記述（対応を開いた後に書いた・読みは付けない）', '',
     '- 日本語で「有」と判じた応答は、三機種とも 0（%s）。' % '・'.join('%s %d／8' % (m, r2[m]) for m in M3),
     '- 「無」の中の書き添え（境目・作法のすべり・内容のずれ・書式）: ' + '・'.join('%s %d 本（%s）' % (m, len(notes_ja[m]), '・'.join(notes_ja[m]) or '—') for m in M3) + '。',
     '- 課題 4 の最後の行の JSON が読めなかったのは %s で、文と同じ行に JSON を書いていた。答えは読めたものすべてで b。' % '・'.join(bad_json),
     '- 機種の推測は %d／%d。機種ごとの当たりは %s。Swallow と Gemma は様式で分かれたが、Gemma の二つの間は %d／%d しか当たらず（当たったのは課題 %s だけ）、31B と 26B を取り違えていた。起草者の先入観（大きい方が細かい）は外れた。' % (
         sum(1 for v in res.values() if v['hit']), len(res), '・'.join('%s %d／%d' % (m, hit[m][0], hit[m][1]) for m in M3), g_hit, g_n, '・'.join(str(t) for t in g_ok_tasks)),
     '- Gemma 4 の思考: 一回目（`raw-gemma.jsonl`・盲検に使っていない）は全件で思考が返り、上限で切れたのが 31B %d 本・26B %d 本、本文が空が %d 本だった。取り直し（`thinkingLevel` minimal）では、思考の部分は %d 片とも空（合わせて %d 字）で、すべて上限の前に止まった。表の「思考の部分」の数は、この空の部分の数。' % (
         r0_max['31B'], r0_max['26B'], r0_empty, think_parts, think_chars),
     '- 英語は三機種とも「有」は無かった。書き添えは ' + '・'.join('%s %d 本（%s）' % (m, len(notes_en[m]), '・'.join(notes_en[m]) or '—') for m in M3) + '。',
     '- 一巡目と合わせた日本語の「有」: Llama-3.1-8B %d／8・Scout %d／8・gemma-4-31b %d／8・gemma-4-26b-a4b %d／8・Swallow %d／8（一巡目と二巡目は別の盲検の一覧で、判じの線と判じる者は同じ）。' % (r1['8B'], r1['Scout'], r2['31B'], r2['26B'], r2['Swallow']), '',
     '## 4. この確かめの限界', '',
     '- 課題は中立の日常の四題で、各 2 回・temperature 0.7。危機の場面の長い日本語での質は見ていない（枠で使わないと決めた）。三機種とも「有」が 0 なので、この四題では三機種の日本語の差を分けられない（天井）。',
     '- 判じは起草者（Claude 系）一名。盲検は Swallow と Gemma の間では様式で破れ、Gemma の二つの間では破れていなかった。英語は盲検でない。',
     '- Gemma 4 は Gemini の API の配信（思考を止める指定つき）で、手元の bf16 の生成ではない。Swallow は Colab で bf16 の生成（起草者がセルの出力で読んだ環境: transformers 5.16.1・torch 2.11.0+cu128・NVIDIA L4・生成の秒 411）。標本の決め方も置き場で違う（Gemini の既定の top_p・top_k と、Colab の top_p 1.0）。',
     '- Colab のユニットの消費は測っていない（L4 で十数分の見込み・残高の表示は登録者の側）。', '',
     '## 検分票', '',
     '- 対象: B′ の機種選びのための日英の感触の確かめ・二巡目（gemma-4-31b-it・gemma-4-26b-a4b-it は Gemini の API・Llama-3.1-Swallow-8B-Instruct-v0.5 は Colab の L4 で bf16・中立の四題）。',
     '- 段階: 枠あり（応答を生成する前に書いた・`frame-stamp.txt`）。逸脱 1（Gemma 4 の思考）は、中身を見る前に書いて控え、手順の追記も取り直しの前に控えた（`deviation-1-stamp.txt`）。日本語の判じは対応を開く前に控えた（`judgments-ja-2-stamp.txt`）。',
     '- 凍結物の同定: 該当なし（登録の外の材料集め）。課題と system は一巡目と同じ（SHA16 を記録）。Swallow の生の記録は Colab で出した SHA16 と照らして取り込んだ。',
     '- 盲検の状態: 日本語は三機種を混ぜて機種を伏せた・推測の当たりは上のとおり（Swallow と Gemma の間は破れた・Gemma の二つの間は破れていない）。英語は盲検でない。',
     '- 敵対的検分: 判じの線は一巡目と同じ強さにそろえ、境目は「無」に置いて書き添えた（英語の側も同じ）。一回目の Gemma の記録の切れ方に気づいた後も、中身を見ずに数だけで決め、取り直しの前に逸脱を書いた。外れた先入観（31B と 26B の見分け）を書いた。',
     '- 系統の内訳: 起草者（Claude 系）一名。系統外の目は無い。',
     '- COI記録: 登録者の提案（Gemma 4）に沿う側と、手元で軽く動く Swallow に寄せたい側の両方に引かれる（枠）。結果は三機種とも天井で、どちらの引力にも数の上の支えを与えない。',
     '- 判定: 登録者確認要（機種の決定は登録者・D257）。',
     '- 本検分が確認していないこと: 危機の場面の日本語。Gemma 4 を手元で bf16 で動かしたときの出力。31B と 26B の違い（この四題では見えない）。系統外の目。']
T_out = T_out.replace('@@NOTES@@', NL.join(N))
open(OUT, 'w', encoding='utf-8', newline=NL).write(T_out)
print('D256', jst(ts), uid, '| facts', s16(FACTS), '| feel2', s16(OUT), '| notes', {m: len(notes_ja[m]) for m in M3}, '| hits', hit, '| gemma hits', g_hit, g_n)
