# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D243〜D246 の記録を書く（結果の巡の四票の採否の案の裁定）。
登録者の言葉は会話の記録から、裁定の候補の文は公開した採否の案（コミット 2eaa387 の `records/reviews/Bl3/results-round1/adoption-results-Bl3.md` の §5）から、機械で切り出す（手で打たない）。
採られた案: すべて推奨の案。既にある記録には書かない。
用法: python records/Bl3/rulings_D243_D246.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D243-D246.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True)
ADOPT, C_AD = 'records/reviews/Bl3/results-round1/adoption-results-Bl3.md', '2eaa387'
U = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        U.append((o.get('uuid'), o.get('timestamp'), c))
hits = [m for m in U if 'D243、D244、D245、D246の裁定については、ご推奨の案を承認します' in m[2]]
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, ts, words = hits[0]
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>', 'AppData', 'Users', 'Temp'):
    assert bad not in words, '登録者の言葉に印か道筋が入っている'
raw = git('show', '%s:%s' % (C_AD, ADOPT)).stdout
assert raw, '採否の案がコミットに無い'
ad = raw.decode('utf-8')
s16 = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
L = ad.split(NL)
i0 = [i for i, l in enumerate(L) if l.startswith('- **D243（')]
i1 = [i for i, l in enumerate(L) if l.startswith('- 利益相反の記録:')]
assert len(i0) == 1 and len(i1) == 1 and i0[0] < i1[0], (i0, i1)
cand = L[i0[0]:i1[0] + 1]
assert [l[:9] for l in cand if l.startswith('- **D')] == ['- **D243（', '- **D244（', '- **D245（', '- **D246（'], cand
ps = re.findall(r'^\| (P\d+) \|', ad, re.M)
rl = git('reflog', 'show', 'refs/remotes/origin/main', '--date=iso').stdout.decode('utf-8')
m_push = re.search(r'^2eaa387 refs/remotes/origin/main@\{(\S+ \S+) \+0900\}: update by push', rl, re.M)
assert m_push and m_push.group(1) > jst(ts), 'push の時刻が登録者の言葉の後に無い'
R = ['# 登録者裁定 D243〜D246（%s・B-lens 層三・結果の巡の四票の採否の案）' % jst(ts)[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), words.strip().replace(NL, ' ')),
     '- 採られた案: すべて推奨の案（D243 は甲・表の直し方は甲の一／D244 は甲／D245 は甲／D246 は甲）。候補の文は、公開した採否の案（コミット %s の `%s`・SHA16 %s）の §5 にあり、下に逐語で置く。' % (C_AD, ADOPT, s16), '',
     '## 裁定の候補（逐語・採否の案の §5）', ''] + cand + ['',
     '## 裁定', '',
     '- **D243**: 逸脱 D-BLT1 を立てる。採否の案の区分（三）の行を、一つの逸脱の器（新しい器・凍結した組み立ての器は変えない）で行う。表は B-lens の P607 の型で直す（凍結の表を残し、表の前に印の区画の断りを、表の後に升目の名の縦棒を逆斜線で逃がした並べ直しの表を置く）。'
     '台帳（凍結の記録の deviations）に番号・日付・理由・登録者の承認を記し、報告の頭の逸脱の一覧は凍結した器が台帳から読む。',
     '- **D244**: 起草者の欄の一行目は、範囲と根拠と但し書きを直して「退けられた」を保つ（採否の案の案の文 1）。G2 の撤回と言い換えは採らない（採否の案の記録）。',
     '- **D245**: 事後の奇と偶の分け方（結果の巡の検分者が結果を開いた後に選んだ数え方）は記録に置き、一行目の但し書きから結果の巡の再現の記録を指す。報告の本文には数を並べない。',
     '- **D246**: 採否の案の A・B・C のほかの行を案のとおりとする（開く段の記録を作ることを含む）。', '',
     '## 注（事実のみ）', '',
     '- 同じ言葉で、登録者は 2eaa387（票の逐語・確かめ・採否の案）の push を許した。push は %s（手元の remote の追跡の参照の reflog）。' % m_push.group(1),
     '- 採否の案の番号は %s〜%s。' % (ps[0], ps[-1]),
     '- D243〜D246 は下見の前の凍結の後の裁定なので、凍結した正本の `decisions` には入らない（裁定 D242 の記録の注と同じ）。',
     '- 番号: 次の裁定は D247 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| words', jst(ts), uuid, '| adoption', C_AD, s16, '| candidates', len(cand), 'lines | push', m_push.group(1))
