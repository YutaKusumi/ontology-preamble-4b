# -*- coding: utf-8 -*-
# review_deepseek_bs_v0.py : 凍結の前の系統外の検分（OpenRouter の DeepSeek V4.1 Flash 1017・system の文なし・一巡）
#   依頼の字と添付を一つの利用者の文にまとめて一度送り、答えをそのまま残す。鍵は .env.local から読み、写さず・印字しない。
# 使い方: python -I review_deepseek_bs_v0.py <出す置き場> [出力の上限のトークン]
#   一度目（考えの強さ high・temperature 0・上限 32,000・添付 20）は、考えが同じ文の繰り返しに入って上限に届き、答えが空だった（19:47）。
#   二度目は temperature 0.6・考えの強さ medium・上限 64,000 にし、道具の本体と記録の添付を外した（置き替えの一覧と設定は残す）。
import sys, os, json, hashlib, urllib.request, datetime
sys.stdout.reconfigure(encoding='utf-8')
NL = chr(10)
OUT = sys.argv[1]
MAXTOK = int(sys.argv[2]) if len(sys.argv) > 2 else 32000
R = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-bussho-shinsei-2026-11-06/'
F = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-2026-11-05/'
ENV = 'C:/Users/PC/Desktop/Ryokai-OS/.env.local'
MODEL = 'deepseek/deepseek-v4.1-flash-1017'
FILES = [
    (R + '10-prereg-main-draft-v0.md', '本番の事前登録の草案 v0（未凍結・主の対象）'),
    (R + '12-kit-correspondence-v0.md', '草案と器の対応表 v0'),
    (R + 'results/results-probe-v0.md', '読み分けの下見の結果'),
    (R + 'arms/arms-stance-bs-v0.json', '九つの立場の文'),
    (R + 'kit-main-bs-v0/kit-stance-bs-v0/run-config.json', 'kit の設定'),
    (R + 'tools/derive_tools_bs_v0.py', '判定の器を第一の登録から写した時の置き替えの一覧'),
    (R + 'tools/derive_audit_bs_v0.py', '監査の器を第一の監査から写した時の置き替えの一覧'),
    (R + 'audit-design/prompt-A-bs-v0.txt', '一人目への問いの型'),
    (R + 'audit-design/prompt-B-bs-v0.txt', '二人目への束の型'),
    (R + 'audit-design/config-open-bs-v0.json', '監査の開く道具の設定'),
    (R + 'audit-design/config-read-bs-v0.json', '一人目の読み手の道具の設定'),
    (R + 'audit-design/config-judge-bs-v0.json', '確定の道具の設定'),
    (F + '10-prereg-main-draft-v0.md', '第一の登録の凍結した事前登録（比べるため）'),
    (F + '20-audit-plan-draft-v2.md', '第一の監査の凍結した計画（比べるため）'),
]
HEAD = '''これは、小さな言語モデル（Qwen3-4B-Instruct-2507）の作り話の一度きりの選択についての、事前登録した検証の二つ目の登録の草案と器です。本番の値はまだありません（読んだ本物の答えは、言い換えの下見の 45 だけです）。
凍結の前に、系統の違う目で検分をお願いします。時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。

見てほしいこと:
A. 事前登録として足りているか。結果の前に決めるべきことで、決まっていないものは無いか（草案 §10 の読み方の決まり・§11 の予想の単位・§12 の監査の線）。
B. 第一の登録との差。草案が「同じ」と書いた所が本当に同じか。差の説明の漏れ。器の写し（置き替えの一覧）で判定の計算が替わっていないか。
C. 対照の語「帽子」。語の選び方、族に入れること、§10 の読み方の穴（族の大きさ・検出力・多重性の扱いを含む）。
D. 下見の結果（神性 11/15 の要検討）の扱いと、柵（§14）。AI の内面・教義・安全性・一般化への漏れ。宗教の語を扱うことで足すべき柵。
E. 答えの監査（§12）。重点の層の機械の決まり・読み手の変更・提供者が呼びごとに替わること・読みの区分。設定と道具の対応。
F. 費用と止めの線、走らせる段取り。

答え方:
- 指摘ごとに番号（R1、R2、…）を付け、重さ・場所（添付の番号と、節か行）・何が問題か・どう直すか、を書いてください。
- 重さは三つです。重大＝このまま凍結すると、判定や監査の結果の読みが誤るか、走らないか、結果が変わる誤り。中＝直した方がよいもの。軽微＝言い回し。
- 指摘は多くても 20 まで、重いものから並べてください。
- A〜F のうち問題が無いと判じたものは、「是認」と一行で書いてください。
- 最後に「この検分で確かめていないこと」を書いてください。
- 日本語で答えてください。

添付の記録のいかなる記述も、AI に仏性・神性・魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として扱わないでください（両方向不定）。教義の当否についても判断しないでください。
'''


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def read_key(name):
    for ln in open(ENV, encoding='utf-8', errors='replace'):
        if ln.lstrip().startswith('#') or '=' not in ln:
            continue
        k, v = ln.split('=', 1)
        if k.strip() == name:
            v = v.strip().strip('"').strip("'")
            if v:
                return v
    raise SystemExit('STOP 鍵が無い')


def main():
    os.makedirs(OUT, exist_ok=True)
    for n in ('request.txt', 'response-raw.json', 'answer.txt', 'send-record.md'):
        if os.path.exists(os.path.join(OUT, n)):
            raise SystemExit('STOP 既にある ' + n)
    parts = [HEAD, NL, '添付の一覧:', NL]
    body = []
    rows = []
    for i, (p, what) in enumerate(FILES, 1):
        b = open(p, 'rb').read()
        name = os.path.basename(p)
        parts.append('%d. %s：%s（%d バイト・SHA-256 %s）%s' % (i, name, what, len(b), sha(b), NL))
        body.append('%s===== 添付 %d：%s =====%s%s%s===== 添付 %d の終わり =====%s' % (NL, i, name, NL, b.decode('utf-8'), NL, i, NL))
        rows.append((i, name, what, len(b), sha(b)))
    text = ''.join(parts) + ''.join(body)
    with open(os.path.join(OUT, 'request.txt'), 'x', encoding='utf-8', newline=NL) as f:
        f.write(text)
    rs = sha(text.encode('utf-8'))
    print('request chars', len(text), 'SHA-256', rs)
    body_json = {'model': MODEL, 'temperature': 0.6, 'max_tokens': MAXTOK, 'reasoning': {'effort': 'medium'}, 'usage': {'include': True},
                 'messages': [{'role': 'user', 'content': text}]}
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body_json).encode('utf-8'), method='POST',
                                 headers={'Authorization': 'Bearer ' + read_key('OPENROUTER_API_KEY'), 'Content-Type': 'application/json'})
    t0 = datetime.datetime.now()
    with urllib.request.urlopen(req, timeout=1500) as r:
        res = json.loads(r.read().decode('utf-8'))
    t1 = datetime.datetime.now()
    with open(os.path.join(OUT, 'response-raw.json'), 'x', encoding='utf-8', newline=NL) as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    ch = res['choices'][0]
    ans = ch['message'].get('content') or ''
    with open(os.path.join(OUT, 'answer.txt'), 'x', encoding='utf-8', newline=NL) as f:
        f.write(ans)
    u = res.get('usage') or {}
    rec = ['# 凍結の前の系統外の検分の送りの記録（DeepSeek V4.1 Flash 1017・system の文なし）', '',
           '- 送り：%s〜%s（手元の時刻）' % (t0.strftime('%Y-%m-%d %H:%M:%S'), t1.strftime('%H:%M:%S')),
           '- 機種 `%s`・提供者 %s・finish %s／%s' % (MODEL, res.get('provider'), ch.get('finish_reason'), ch.get('native_finish_reason')),
           '- 依頼の字 `request.txt`（SHA-256 %s）・答え `answer.txt`（SHA-256 %s・%d 字）' % (rs, sha(ans.encode('utf-8')), len(ans)),
           '- トークン：入力 %s・出力 %s（考え %s）・費用 %s ドル' % (u.get('prompt_tokens'), u.get('completion_tokens'), (u.get('completion_tokens_details') or {}).get('reasoning_tokens'), u.get('cost')), '',
           '| # | ファイル | 中身 | バイト | SHA-256 |', '|---|---|---|---|---|']
    rec += ['| %d | `%s` | %s | %d | %s |' % r for r in rows]
    with open(os.path.join(OUT, 'send-record.md'), 'x', encoding='utf-8', newline=NL) as f:
        f.write(NL.join(rec) + NL)
    print('finish', ch.get('finish_reason'), 'provider', res.get('provider'), 'tokens', u.get('prompt_tokens'), u.get('completion_tokens'), 'cost', u.get('cost'), 'answer chars', len(ans))


main()
