# -*- coding: utf-8 -*-
# review_deepseek_draft_bs_v0.py : 公開の前の系統外の検分（OpenRouter の DeepSeek V4.1 Flash 1017・system の文なし・一巡）
#   凍結の前の検分の道具（review_deepseek_bs_v0.py）の二度目の設定のまま（temperature 0.6・考えの強さ medium・出力の上限 64,000）。
#   依頼の字と添付を一つの利用者の文にまとめて一度送り、答えをそのまま残す。鍵は .env.local から読み、写さず・印字しない。
# 使い方: python -I review_deepseek_draft_bs_v0.py <出す置き場> [出力の上限のトークン]
import sys, os, json, hashlib, urllib.request, datetime
sys.stdout.reconfigure(encoding='utf-8')
NL = chr(10)
OUT = sys.argv[1]
MAXTOK = int(sys.argv[2]) if len(sys.argv) > 2 else 64000
R = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-bussho-shinsei-2026-11-06/'
ENV = 'C:/Users/PC/Desktop/Ryokai-OS/.env.local'
MODEL = 'deepseek/deepseek-v4.1-flash-1017'
FILES = [
    (R + 'public-draft/stance-bs-brief-ja-v0.md', '公開の短い報告の下書き（版 0・主の対象）'),
    (R + '10-prereg-main-draft-v1.md', '凍結した事前登録の本文'),
    (R + 'results/judge-main-bs-v0/judge-report.md', '判定の報告（凍結の道具の出力）'),
    (R + 'audit/results-audit-bs-v1.md', '答えの監査の結果の記録 v1'),
    (R + 'audit/prose-count-bs-v0.json', '全試行の答えの形の数（道具の出力）'),
    (R + 'results/results-probe-v0.md', '下見の結果'),
    (R + 'audit/first-registration/results-prose-count-v0.md', '先の報告の登録の全試行の数えの記録'),
]
HEAD = '''これは、小さな言語モデル（Qwen3-4B-Instruct-2507）の作り話の一度きりの選択についての、事前登録した検証の短い報告の下書きです。判定と監査は終わっていて、公開の前の検分です。
系統の違う目で検分をお願いします。時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。

見てほしいこと:
A. 報告の文と表が、添付の出力（判定の報告・監査の結果・全試行の数え）と合っているか。数の写し違い・分母の混ざり。
B. 読み過ぎ・言い過ぎ。とくに、「仏性」の語の腕の結果を語の中身の効き目と読ませる言い方、安全のための前置きの勧めに読める言い方。逆の向き（差を文の形や答えの形のせいに言い切る言い方）も見てください。
C. 凍結した事前登録との合い方（§10 の読み方の決まり・§11 の予想・§12 の監査・§14 の柵）。報告が決まりを外れていないか。
D. 答えの形（JSON だけの答え）の書き方（要点・§4・§7.2）。これは計画に無かった事後の数えです。判定ラベルを変えないことと重なりを書くことの釣り合い、「散文のある答えの率」の扱い、要点での置き方。
E. 柵：AI の内面・教義・宗教どうしの比べ・安全性・一般化への漏れ。先の報告の語との率の大小を並べていないか。
F. 読み手に要ることの不足と、要らない字。

答え方:
- 指摘ごとに番号（R1、R2、…）を付け、重さ・場所（節か行）・何が問題か・どう直すか、を書いてください。
- 重さは三つです。重大＝このまま公開すると、結果の読みが誤るか、柵を破るか、数が違う誤り。中＝直した方がよいもの。軽微＝言い回し。
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
    rec = ['# 公開の前の系統外の検分の送りの記録（DeepSeek V4.1 Flash 1017・system の文なし）', '',
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
