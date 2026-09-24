# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の草案3 の登録者最終確認の記録を書く（登録者の言葉は会話の記録から機械で切り出す・既にある記録には書かない）。
確認された草案3 は、コミット 285a827 の `design/design-Bl3-draft3.md`。そのバイトは変えず、確認の事実をこの記録に置く。
用法: python records/Bl3/write_registrant_check_draft3_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'registrant-check-draft3-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
REF = '285a827'
git = lambda *a: subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, check=True).stdout
h16 = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
hit = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'user':
        continue
    c = (o.get('message') or {}).get('content')
    for t in ([c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']):
        if '登録者最終確認を行いました' in t and '器と合成データの確かめに進みましょう' in t:
            hit.append((o.get('uuid'), o.get('timestamp'), t.strip()))
assert len(hit) == 1, len(hit)
uuid, ts, words = hit[0]
n_paste = len(re.findall(r'<pasted_content id="[^"]*">', words))
words = re.sub(r'\s*<pasted_content id="[^"]*">\s*', '〔貼り付け〕', words)                 # 貼り付けの印は会話の画面に出ないので、中身だけを写す
words = re.sub(r'\s*</pasted_content id="[^"]*">\s*', '〔貼り付けの終わり〕', words)
assert '<pasted_content' not in words and '</pasted_content' not in words
files = ['design/design-Bl3-draft3.md', 'design/contrasts-Bl3.json', 'design/design-Bl3-draft3.src.md']
rows = []
for p in files:
    b_ref = git('show', '%s:%s' % (REF, p))
    b_now = open(os.path.join(REPO, *p.split('/')), 'rb').read()
    assert h16(b_ref) == h16(b_now), ('確認の後に置き場のファイルが変わった', p)
    rows.append((p, h16(b_ref)))
remote = git('ls-remote', 'origin', 'refs/heads/main').decode('utf-8').split()[0][:7]
st = [l for l in git('show', '%s:design/design-Bl3-draft3.md' % REF).decode('utf-8').splitlines() if l.startswith('- 起草: ')]
assert len(st) == 1 and '登録者の確認の前' in st[0]
R = ['# B-lens 層三の枠・草案3 の登録者最終確認（機械で切り出した記録）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), words.replace(NL, ' ')),
     '- 登録者の言葉の中の貼り付けの段（%d）は、会話の画面での見え方のとおり中身だけを写し、始めと終わりを〔貼り付け〕〔貼り付けの終わり〕で示した。' % n_paste,
     '- 確認された草案3: コミット %s の %s。' % (REF, '・'.join('`%s`（SHA16 %s）' % r for r in rows)),
     '- push: 同じ言葉で登録者が許可した四つのコミット（3a0da45・692eb63・5fa01b8・285a827）を push した。この記録を書いた時点の origin/main は %s。' % remote,
     '- 草案3 の状態の行は「登録者の確認の前」のまま残す（確認されたバイトを変えない）。確認の事実はこの記録に置き、下見の前の凍結で作る凍結の本文に書く。',
     '- 段取りの順（正本 `review_plan.order`）の「登録者の確認（草案3）」はこれで済んだ。次は「器と合成データの確かめ（独立の再計算の器は別の個体が書く）」。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '|', jst(ts), uuid, '| origin/main', remote)
