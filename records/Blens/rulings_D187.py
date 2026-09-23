# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D187 の記録を書く（凍結の前の Colab の確かめの後・ランダム方向の再生の確かめと torch の組み・2026-09-24）。
登録者の言葉と、裁定の前にコーディネータが示した案は、会話の記録から機械で切り出す。一度目の Colab の確かめの出力は置き場に写し（既にあれば書かない）、
その事実と、裁定を受けて変えたもの（正本・設計の事実・語の集合・予想の書式・草案3・器）の差を機械で取る。数と SHA は手で打たない。既にあるファイルには書かない。
用法: python records/Blens/rulings_D187.py <会話の記録 jsonl> <一度目の確かめの check.json> <その zip> [<NumPy 2.1.3 の python>]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, shutil, hashlib, datetime, difflib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import numpy as np
import steer_B
import blens_lens as BL
import make_predictions_form_Blens as FORM

NL = chr(10)
D186_COMMIT, TOOLS_COMMIT = '567c74e', 'b5dbf3d'
OUT = os.path.join(HERE, 'rulings-D187.md')
CHECK1 = os.path.join(HERE, 'colab-check-1-Blens.json')
assert not os.path.exists(OUT), '既にある: ' + OUT
transcript, check_src, zip_src = sys.argv[1], sys.argv[2], sys.argv[3]
np213 = sys.argv[4] if len(sys.argv) > 4 else None
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
show = lambda c, rel: subprocess.run(['git', 'show', '%s:%s' % (c, rel)], cwd=REPO, capture_output=True, check=True).stdout
cur = lambda rel: open(os.path.join(REPO, *rel.split('/')), 'rb').read()

# ---- 会話の記録から: 登録者の言葉（裁定・ユニットの数）と、コーディネータが示した案
words = opts = None
units = []
for line in open(transcript, encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    t = o.get('type')
    if t not in ('user', 'assistant'):
        continue
    c = (o.get('message') or {}).get('content')
    texts = [c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']
    for s in texts:
        if t == 'user' and len(s) < 600 and 'ユニット数は' in s:
            units.append((o.get('timestamp'), o.get('uuid'), s.strip()))
        if t == 'user' and len(s) < 600 and '案Aと甲' in s:
            words = (s.strip(), o.get('uuid'), o.get('timestamp'))
        if t == 'assistant' and '問題一' in s and '問題二' in s and '私の推奨は A です' in s:
            opts = (s, o.get('uuid'), o.get('timestamp'))
assert words and opts and len(units) >= 2, '会話の記録から言葉か案か、ユニットの数が見つからない'


def unit_value(s):
    import re
    m = re.search(r'ユニット数は、?\s*([0-9]+(?:\.[0-9]+)?)', s)
    return m.group(1) if m else None


u_before = [u for u in units if u[0] < opts[2]][-1]
u_after = [u for u in units if u[0] > opts[2]][0]
ub, ua = unit_value(u_before[2]), unit_value(u_after[2])

# ---- 一度目の Colab の確かめ（写す・事実を取る）
cb = open(check_src, 'rb').read()
zb = open(zip_src, 'rb').read()
if os.path.exists(CHECK1):
    assert open(CHECK1, 'rb').read() == cb, '置き場の一度目の確かめが与えた check.json と違う'
else:
    open(CHECK1, 'wb').write(cb)
CK = json.loads(cb.decode('utf-8'))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
FJ = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
D = np.load(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'))
sel = BL.rkey(T['primary']['ratio'])
ratios = [BL.rkey(r) for r in T['layers']['ratios']]
local = {'main@%s' % sel: BL.dirs_sha256(steer_B.random_directions(D['static__%s' % sel], 'main', float(sel)))}
for r in ratios:
    local['tune@%s' % r] = BL.dirs_sha256(steer_B.random_directions(D['static__%s' % r], 'tune', float(r)))
loc213, v213 = None, None
if np213:
    code = ("import sys,json,hashlib;sys.path.insert(0,r'%s');import numpy as np;import steer_B;D=np.load(r'%s');"
            "f=lambda vs:hashlib.sha256(b''.join(np.asarray(v,dtype=np.float64).tobytes() for v in vs)).hexdigest().upper();"
            "o={'main@%s':f(steer_B.random_directions(D['static__%s'],'main',%s))};"
            "o.update({'tune@'+r:f(steer_B.random_directions(D['static__'+r],'tune',float(r))) for r in %r});"
            "print(json.dumps({'numpy':np.__version__,'sha':o}))") % (os.path.join(REPO, 'tools'), os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'), sel, sel, sel, ratios)
    r_ = subprocess.run([np213, '-c', code], capture_output=True, text=True, encoding='utf-8')
    assert r_.returncode == 0, r_.stderr[-800:]
    j_ = json.loads(r_.stdout.strip().splitlines()[-1])
    loc213, v213 = j_['sha'], j_['numpy']
pins = T['inputs']['versions_B']
lc = CK['logit_check']
cal = CK['calibration']
cal_in = sum(1 for v in cal.values() if v['main']['inside'] and all(x['inside'] for x in (v.get('letter') or {}).values()))

# ---- 裁定を受けて変えたもの（機械の差）
def tree_diff(a, b, p='$'):
    out = []
    if type(a) != type(b):
        return [(p, 'changed', a, b)]
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append((p + '.' + k, 'added', None, b[k]))
            elif k not in b:
                out.append((p + '.' + k, 'removed', a[k], None))
            else:
                out += tree_diff(a[k], b[k], p + '.' + k)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((p, 'list %d → %d' % (len(a), len(b)), a[len(b):], b[len(a):]))
        for i, (x, y) in enumerate(zip(a, b)):
            out += tree_diff(x, y, '%s[%d]' % (p, i))
    elif a != b:
        out.append((p, 'changed', a, b))
    return out


canon_old_b, canon_new_b = show(D186_COMMIT, 'design/contrasts-Blens.json'), cur('design/contrasts-Blens.json')
canon_old = json.loads(canon_old_b.decode('utf-8'))
cdiff = tree_diff(canon_old, T)
facts_old = json.loads(show(D186_COMMIT, 'records/Blens/design-facts-Blens.json').decode('utf-8'))
facts_keys = [k for k in sorted(set(facts_old) | set(FJ)) if facts_old.get(k) != FJ.get(k)]
sets_old = json.loads(show(TOOLS_COMMIT, 'records/Blens/sets-Blens.json').decode('utf-8'))   # 語の集合は器のコミットで作った
same_at_tools = {rel: show(D186_COMMIT, rel) == show(TOOLS_COMMIT, rel) for rel in ('design/contrasts-Blens.json', 'design/design-Blens-draft3.md', 'design/design-Blens-draft3.src.md', 'records/Blens/design-facts-Blens.json')}
sets_new = json.load(open(os.path.join(REPO, 'records', 'Blens', 'sets-Blens.json'), encoding='utf-8'))
sets_keys = [k for k in sorted(set(sets_old) | set(sets_new)) if sets_old.get(k) != sets_new.get(k)]
sets_check_keys = [k for k in sorted(set(sets_old['checks']) | set(sets_new['checks'])) if sets_old['checks'].get(k) != sets_new['checks'].get(k)]
form_rel = 'records/predictions/predictions-form-Blens-v1.html'
form_b = cur(form_rel)
form_same_commit = form_b == show(TOOLS_COMMIT, form_rel)
form_rebuilt_same = FORM.build(T).encode('utf-8') == form_b.replace(b'\r\n', b'\n')
draft_old_b, draft_new_b = show(D186_COMMIT, 'design/design-Blens-draft3.md'), cur('design/design-Blens-draft3.md')
ddiff = [l for l in difflib.unified_diff(draft_old_b.decode('utf-8').split(NL), draft_new_b.decode('utf-8').replace('\r\n', NL).split(NL), 'design-Blens-draft3.md（%s）' % D186_COMMIT, 'design-Blens-draft3.md（裁定 D187 の後）', n=0, lineterm='')]
changed = subprocess.run(['git', 'diff', '--name-only', TOOLS_COMMIT], cwd=REPO, capture_output=True, text=True, check=True).stdout.split()
tool_rows = []
for rel in sorted(x for x in changed if x.startswith('tools/')):
    tool_rows.append((rel, s16b(show(TOOLS_COMMIT, rel)), s16b(cur(rel))))

# ---- 書く
q = lambda v: ('「%s」' % v) if isinstance(v, str) else ('`%s`' % json.dumps(v, ensure_ascii=False))
R = ['# 登録者裁定 D187（2026-09-24・凍結の前の Colab の確かめの後・段階 B のランダム方向の再生の確かめと torch の組み）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (words[1], jst(words[2]), words[0].replace(NL, ' ')), '',
     '| 裁定 | 中身 |', '|---|---|',
     '| D187 | %s（許容 `nulls.B_random.repro_tol` ＝ %g） |' % (T['decisions']['D187'], T['nulls']['B_random']['repro_tol']), '',
     '「案A」は再生の確かめを方向ごとの相対の差の許容に改める案、「甲」は起動器で torch を B の組みのまま入れる案（下の案の逐語）。', '',
     '## 一度目の Colab の確かめ（相 check・止めた）', '',
     '- 出力: `records/Blens/colab-check-1-Blens.json`（起動器の出力 `check.json` を写した・SHA-256 %s・%d バイト）。落とした zip の SHA-256 %s（%d バイト・中身は `check.json` だけ）。'
     % (sha256b(cb), len(cb), sha256b(zb), len(zb)),
     '- 起動器 %s・コミット `%s`・GPU %s・終わり %s（UTC）。' % (CK['boot'], CK['commit'], CK['gpu'], CK['finished']),
     '- 版（Colab）: NumPy %s・torch %s・transformers %s（B の版: NumPy %s・torch %s・transformers %s）。起動器 v1 は版を `+` の前で比べたので、torch の CUDA の組みの違いでは止まらなかった。'
     % (CK['versions']['numpy'], CK['versions']['torch'], CK['versions']['transformers'], pins['numpy'], pins['torch'], pins['transformers']),
     '- 通った確かめ: 重みの断片の SHA-256 が転記行 F と %s・logits の突き合わせ（主位置の差の最大 %.4g・答えの文字の位置 %.4g・許容 %g・最上位の語は %s）・較正の検査（%d 層のうち区間の内 %d）・選んだ試行の一覧の SHA16 %s（設計の事実と %s）。'
     % ('同じ' if CK['weights_sha256'] == FJ['facts']['F']['sha256'] else '違う', lc['main_max_abs'], lc['letter_max_abs'], T['magnitude']['logit_check']['atol'],
        '両方の位置で同じ' if lc['main_argmax_equal'] and lc['letter_argmax_equal'] else '違う', len(cal), cal_in, CK['selected_sha16'], '同じ' if CK['selected_sha16'] == FJ['facts']['E']['selected_sha16'] else '違う'),
     '- 止まった確かめ（段階 B のランダム方向の再生の SHA-256・起動器 v1 はビットの一致を求めた）:', '',
     '| 方向の組 | Colab（NumPy %s） | 手元（NumPy %s） | %sColab と手元 |' % (CK['versions']['numpy'], np.__version__, ('手元（NumPy %s） | ' % v213) if loc213 else ''),
     '|---|---|---|%s---|' % ('---|' if loc213 else '')]
for k in sorted(local):
    R.append('| %s | %s | %s | %s%s |' % (k, CK['random_dirs_sha256'].get(k), local[k], (loc213[k] + ' | ') if loc213 else '', '合う' if CK['random_dirs_sha256'].get(k) == local[k] else '**違う**'))
R += ['',
      ('- 手元の二つの版の NumPy（%s と %s）の再生は、四組とも同じ SHA-256 だった（手元では NumPy の版で再生が変わらない。Colab との食い違いは NumPy の版からは説明できない）。' % (np.__version__, v213)
       if loc213 == local else '- **手元の二つの版の NumPy（%s と %s）の再生の SHA-256 が違った**。' % (np.__version__, v213)) if loc213 else
      '- 手元の NumPy 2.1.3 での再生は、この記録では走らせていない。',
      '- コーディネータのチャットの診断（Colab の画面から読んだ値に基づく・機械の記録ではない）: 引いた乱数の列のノルムは最後の桁の内で同じで（列が変わっていれば上の桁から違う）、違ったのは方向の大きさを揃えるノルムの計算の最後の桁だった。'
      '二度目の確かめは、再生した方向そのものを置くので、方向ごとの相対の差を機械で測って凍結の記録に並べる。',
      '- ランタイムは、裁定を待つあいだに接続を解いて削除した。登録者がチャットに書いたユニットの数は、確かめの前 %s（%s 日本時間）・後 %s（%s 日本時間）で、差は %s（登録者の言葉から機械で読んだ）。'
      % (ub, jst(u_before[0]), ua, jst(u_after[0]), ('%.2f' % (float(ub) - float(ua))) if ub and ua else '読めなかった'), '',
      '## 裁定の前にコーディネータが示した案（逐語・会話の記録 uuid `%s`・%s 日本時間）' % (opts[1], jst(opts[2])), '',
      '````text', opts[0].rstrip(), '````', '',
      '## 裁定を受けて変えたもの（機械で取った差）', '',
      '- **正本** `design/contrasts-Blens.json`: SHA16 %s（裁定 D186 で確かめたコミット %s）→ %s。版の名（`version`）は `%s` のまま（予想の書式の「正本の版」の欄と合わせるため・`version_note`）。予想の項目（`predictions`）は%s。'
      % (s16b(canon_old_b), D186_COMMIT, s16b(canon_new_b), T['version'], '変わっていない' if canon_old['predictions'] == T['predictions'] else '**変わった**'),
      '']
for path, kind, a, b in cdiff:
    if kind == 'changed':
        R.append('  - `%s`（改めた）: 前 %s → 後 %s' % (path, q(a), q(b)))
    elif kind == 'added':
        R.append('  - `%s`（足した）: %s' % (path, q(b)))
    elif kind == 'removed':
        R.append('  - `%s`（除いた）: %s' % (path, q(a)))
    else:
        R.append('  - `%s`（%s）: 足した項目 %s' % (path, kind, q(b)))
R += ['',
      '- **設計の事実** `records/Blens/design-facts-Blens.json`: 作り直した。コミット %s と違う欄は %s だけ（転記行の中身は同じ）。' % (D186_COMMIT, '・'.join('`%s`' % k for k in facts_keys)),
      '- **語の集合** `records/Blens/sets-Blens.json`: 作り直した。集合（`sets`）は%s。コミット %s と違う欄は %s（`checks` の中では %s）だけ。'
      % ('同じ' if sets_old.get('sets') == sets_new.get('sets') else '**違う**', TOOLS_COMMIT, '・'.join('`%s`' % k for k in sets_keys), '・'.join('`%s`' % k for k in sets_check_keys)),
      '- 正本・草案3（本文と原稿）・設計の事実は、コミット %s と %s で%s（器のコミットはこれらを変えていない）。' % (D186_COMMIT, TOOLS_COMMIT, 'バイトで同じ' if all(same_at_tools.values()) else '**違う: %s**' % [k for k, v in same_at_tools.items() if not v]),
      '- **予想の書式** `%s`: コミット %s のファイルと%s。改めた正本から組み直した書式が、置き場の書式と%s（登録者が書式で作った予想の JSON は、そのまま封印できる）。'
      % (form_rel, TOOLS_COMMIT, 'バイトで同じ' if form_same_commit else '**違う**', 'バイトで同じ' if form_rebuilt_same else '**違う**'),
      '- **器**（コミット %s からの差・SHA16 は改行を LF に揃えて取った）:' % TOOLS_COMMIT, '', '| 器 | 前 | 後 |', '|---|---|---|']
R += ['| `%s` | %s | %s |' % row for row in tool_rows]
R += ['',
      '- **草案3** `design/design-Blens-draft3.md`: SHA16 %s（裁定 D186 で確かめたコミット %s）→ %s。組み立てた本文の差（行の単位・%d 行）:' % (s16b(draft_old_b), D186_COMMIT, s16b(draft_new_b), sum(1 for l in ddiff if l[:1] in '+-' and not l.startswith(('---', '+++')))),
      '', '````diff'] + ddiff + ['````', '',
      '## 注（事実のみ）', '',
      '- 裁定 D186 で登録者が確かめた草案3 の文を、この裁定で改めた。名は草案3 のまま置き、改めた所は本文の冒頭の行・§2・§3.2・§9・§13 に書いた。凍結の本文は、改めた後の草案3 の原稿から、題名と凍結の一行だけを変えて組む。',
      '- 合成データの器に、許容の内の突き合わせの経路を足した（`records/Blens/dry-run-Blens-2026-09-24.md`）。正本の `synthetic` の一覧に一つ足したのはこのため。',
      '- 次: コミットを登録者に示し、push の許可を得る → 改めた起動器で Colab の確かめ（相 check）をもう一度走らせる → 凍結。二度目の確かめで何かが外れたら、止めて登録者に相談する（登録者の決まり・裁定 D184）。',
      '- 番号: 次の裁定は D188 から（正本の `numbering.rulings_next`）。', '',
      '## 検分票', '',
      '- 対象: 裁定 D187 の記録と、裁定を受けた改め（正本・草案3・器）の差。',
      '- 段階: 凍結の前（射影は一つも計算していない）。一度目の Colab の確かめは射影を計算しない相で、方向の値そのものは置いていない。',
      '- 凍結物の同定: 凍結はまだ無い。裁定 D186 で確かめたコミット %s の正本と草案3 を比べる相手にした。' % D186_COMMIT,
      '- 盲検の状態: 該当しない（器の確かめの改め）。',
      '- 敵対的検分: 予想の項目が変わっていないこと・書式がバイトで同じこと・語の集合が同じことを機械で確かめた。許容が本当の食い違い（乱数の列・大きさ・方向の数の違い）で止まることは、層一の器の自己検査と合成データの器で確かめた。',
      '- 系統の内訳: この記録と改めはコーディネータ（Claude 系）だけで作った。外の目は通っていない。',
      '- COI記録: コーディネータは凍結へ進む側に引かれている。確かめを緩める向きの改めなので、許容を一つの数（`repro_tol`）に固定し、ビットの一致を求めない理由と、許容で捕まる食い違いの型を正本に書いた。',
      '- 判定: 登録者の裁定どおりに改めた（登録者の確かめは push の許可のときに受ける）。',
      '- 本検分が確認していないこと: 段階 B の走行が実際に使ったランダム方向とのビットの一致（段階 B は方向そのものも SHA-256 も記録していない。Colab の再生は同じ種類の機械での再生で、B の方向そのものではない）。'
      'Colab の機械が変わったときに相対の差が許容の内に留まること（二度目の確かめで測る）。torch を B の組みに入れ直す経路（Colab の実機で確かめる）。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', OUT, '|', jst(words[2]), words[1], '| canon diffs', len(cdiff), '| draft diff lines', len(ddiff), '| tools', len(tool_rows))
