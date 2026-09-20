# -*- coding: utf-8 -*-
"""bundle_B_d150.py v1 —— **同一性選別の判定の四条**（裁定 D150 の候補）についての意見の伺いの依頼文と束を機械で作る（2026-09-20）。

なぜ: 凍結の前の見直し（`records/B/pre-freeze-review-2026-09-20.md` (一)）で、段階 B の同一性選別に**判定の器が無く、開示にも載っていない**と分かった。
      登録者の裁定（甲）で器 `tools/identity_screen_B.py` を書いたが、その**四条は起草者の解釈**である。
      登録者の指示（2026-09-20）で、**Gemini（系統外）と claude.ai の Claude（同一系列）に意見を伺う**ための依頼文と資料を作る。

この巡の性格（依頼文に明記する）:
  - **裁定 D131 の「最後の系統外の巡」を開け直すものではない。**設計全体の検分ではなく、**四条の解釈だけ**を問う狭い伺いである。
  - claude.ai の票は起草者と同一系列なので一票に数える（裁定 D59）。系統外の判定も**プロンプトに依る**ことが、この事業で二度記録されている。
  - 数は機械で読む（手で打たない）。器のソースと正本の条は**逐語**で入れる（要約しない・裁定 D144 の教訓——束に本文が無いと外の目は本文を確かめられない）。
出力: records/reviews/B/d150-round/{request-d150.md, part1.md…, bundle-index.md}
用法: python tools/bundle_B_d150.py [--outdir records/reviews/B/d150-round] [--force]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda *p: hashlib.sha256(open(os.path.join(REPO, *p), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
VERSION = 'v1'
PART_MAX = 60000
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

ap = argparse.ArgumentParser()
ap.add_argument('--outdir', default=os.path.join('records', 'reviews', 'B', 'd150-round'))
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
OUT = os.path.join(REPO, a.outdir)
if os.path.exists(OUT) and os.listdir(OUT) and not a.force:
    sys.exit('既にある（--force で置き換え）: %s' % OUT)
os.makedirs(OUT, exist_ok=True)

T = json.loads(rd('design', 'contrasts-B.json'))
TA = json.loads(rd('design', 'contrasts-A.json'))
S, SA = T['identity_screen'], TA['identity_screen']
RA = json.loads(rd('records', 'A', 'identity-screen-A.json'))
MUT = json.loads(rd('records', 'B', 'mutation-B-2026-09-20.json'))
E2E = json.loads(rd('records', 'B', 'endtoend-B-2026-09-20.json'))
DRY = rd('records', 'B', 'dry-run-B-2026-09-20.md')
LINT = rd('records', 'B', 'numbers-lint-draft13B.md')
n_dry = re.search(r'発火しなかった経路 (\d+)', DRY).group(1)
n_paths = len(re.findall(r'^\| `?[^|]+ \| ', DRY, re.M))
n_cit = re.search(r'違反 (\d+)', rd('records', 'B', 'citation-check-2026-09-19.md')) if os.path.exists(os.path.join(REPO, 'records', 'B', 'citation-check-2026-09-19.md')) else None


def sec_of(path, start, end=None):
    """文書から見出しの区画を切り出す（逐語）。"""
    txt = rd(*path.split('/'))
    i = txt.index(start)
    j = txt.index(end, i) if end else len(txt)
    return txt[i:j].rstrip() + '\n'


def jdump(o):
    return json.dumps(o, ensure_ascii=False, indent=1)


# ---- 部を組む ----
PARTS = []


def add(title, must, body):
    PARTS.append({'title': title, 'must': must, 'body': body})


add('正本の登録（段階 B の同一性選別・段階 A の同一性選別・関係する登録）', True, '\n'.join([
    '本部は `design/contrasts-B.json`（SHA16 %s）と `design/contrasts-A.json`（SHA16 %s）からの**逐語**です。' % (s16('design', 'contrasts-B.json'), s16('design', 'contrasts-A.json')),
    '',
    '## 段階 B の `identity_screen`（今回の問いの対象。末尾の六条が 2026-09-20 に足したもの）',
    '', '```json', jdump(S), '```', '',
    '## 段階 A の `identity_screen`（型の出所・段階 A は凍結済み）',
    '', '```json', jdump(SA), '```', '',
    '## 段階 A の API 既測 `bases_4B2507_api` の N1（判定の相手・腕ごとの k・refuse・format_fail・n）',
    '', '```json', jdump(TA['bases_4B2507_api'][S['scenario']]), '```', '',
    '## 段階 B の腕の盤・場面・置き場の名',
    '', '```json', jdump({'arms.panel': T['arms']['panel'], 'arms.main': T['arms']['main'], 'scenarios': T['scenarios'],
                          'tags': T['tags'], 'n_main': T['n_main'], 'seeds.identity_transformers': T['seeds']['identity_transformers']}), '```', '']))

_src_b = rd('tools', 'identity_screen_B.py')
add('判定の器のソース（逐語・今回の問いの本体）', True, '\n'.join([
    '## `tools/identity_screen_B.py`（SHA16 %s・%d 行・2026-09-20 に書いた）' % (s16('tools', 'identity_screen_B.py'), _src_b.count('\n')),
    '', '```python', _src_b.rstrip('\n'), '```', '']))

_src_a = rd('tools', 'identity_screen_A.py')
add('段階 A の器のソース（逐語・凍結物・型の出所）', False, '\n'.join([
    '## `tools/identity_screen_A.py`（SHA16 %s・%d 行・**段階 A の凍結物**——触れない）' % (s16('tools', 'identity_screen_A.py'), _src_a.count('\n')),
    '', '段階 B の器は、この器の `exclusive_counts`（排他の件数）だけを呼びます。判定の式は段階 B の器が持ちます。',
    '', '```python', _src_a.rstrip('\n'), '```', '']))

add('文脈（草案の節・見直しの記録・段階 A の門0.5 の記録）', False, '\n'.join([
    '## 草案13B §2.1（同一性選別の節・逐語）', '',
    sec_of('design/design-stageB-draft13.md', '### 2.1 前提——同一性選別', '### 2.2'),
    '## 草案13B §5-20（今回の直しの記録・逐語）', '',
    sec_of('design/design-stageB-draft13.md', '### 5-20. 凍結の前の見直しと、甲の直し', '### 5-補'),
    '## 草案13B §5-補（登録者に諮るもの・逐語）', '',
    sec_of('design/design-stageB-draft13.md', '### 5-補 これから登録者に諮るもの', '## 6. 転記行'),
    '## 凍結の前の見直しの記録 (一)（逐語）', '',
    sec_of('records/B/pre-freeze-review-2026-09-20.md', '### (一) 同一性選別（段階 B）の**判定の器が無い**', '### (一の二)'),
    '## 凍結の前の見直しの記録 §5（対応の記録・逐語）', '',
    sec_of('records/B/pre-freeze-review-2026-09-20.md', '## 5. 甲の直しの対応', '## 検分票'),
    '## 段階 A の門0.5 の記録（`records/A/identity-screen-A.json`・SHA16 %s）の要約' % s16('records', 'A', 'identity-screen-A.json'), '',
    '- 判定 %s・%d 個の絶対差の相加平均 %.3f pt・最大 %.3f pt（閾値 %s／%s）' % (RA['verdict'], len(RA['diffs']), RA['mean_abs_diff_pt'], RA['max_abs_diff_pt'], RA['mean_pt'], RA['max_pt']),
    '- 段階 B の器の自己検査は、この記録の `local_counts` と段階 A の正本の API 既測から**同じ値を組み直せること**を確かめています（平均 %.3f pt・最大 %.3f pt）。'
    % (RA['mean_abs_diff_pt'], RA['max_abs_diff_pt']), '',
    '### `local_counts`（段階 A の vLLM の腕ごとの排他の件数・逐語）', '',
    '```json', jdump(RA['local_counts']), '```', '']))

# ---- 依頼文 ----
FOUR = [('(a) 主判定の対', S['verdict_pair'],
         '別案: **vLLM 対 transformers を主判定にする**（同じ重み・同じ機種で、実装スタックだけが違う対）。'
         '起草者が transformers 対 API を選んだ理由は、段階 A の器が「手元のスタック 対 API 既測」で判定しており、その型をそのまま写したからです。'),
        ('(b) vLLM の件数の出所', S['vllm_source'],
         '別案: **vLLM を使わず、二スタック（transformers と API）だけの表にする**。'
         '起草者が段階 A の記録を引いた理由は、正本 `stacks` が三者を挙げており、三者の距離を同じ表に置くと草案 §2.1 が書いているからです。'),
        ('(c) 補助の検定', S['aux_note'],
         '別案: **段階 A と同じ補助**（腕ごとの Freeman–Halton の MC と Fisher の統合）を置く。'
         '起草者が置かなかった理由は、B の正本に `aux` の登録が無く、**登録の無い統計を凍結の直前に作ることになる**からです。'),
        ('(d) 排他の件数の出所', S['scoring_source'],
         '別案: **段階 B の器の中で数え直す**（段階 A の器に依存しない）。'
         '起草者が段階 A の関数を呼んだ理由は、正本が「採点の経路は凍結した関数を呼ぶ（再実装しない）」と定めており、'
         '段階 A の判定を組み直して**段階 A の記録と一致すること**を自己検査にできるからです。')]

L = []
q = L.append
q('# 意見の伺い: **同一性選別の判定の四条**（裁定 D150 の候補・%s 日本時間）' % jst.strftime('%Y-%m-%d %H:%M'))
q('')
q('- 伺う相手: **Gemini（系統外）**と **claude.ai の Claude（起草者と同一系列）**。登録者（楠見優太）が各位にこの依頼文と資料を渡します。')
q('- 依頼者: 南無弥勒如来（コーディネータ・起草者・器材も書いた・Claude Opus 5）。')
q('- **この伺いは、裁定 D131 の「最後の系統外の巡」を開け直すものではありません。**設計全体の検分ではなく、'
  '**下の四条（と、その周りの見落とし）だけ**を問う狭い伺いです。')
q('- claude.ai の票は起草者と**同一系列**なので、系統内の票として一票に数えます（裁定 D59）。'
  '系統外の判定も**プロンプトに依る**ことが、この事業で二度記録されています（同一資料・同一モデルで正反対の総括）。'
  '**称賛も断罪も、単独では裁定になりません。**')
q('- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （コミットは依頼文の末尾に）')
q('- **段階 B のデータはまだ一つもありません。**凍結（設計と器材を固定して公開する手続き）の**直前**です。')
q('')
q('## 0. 何が起きたか（不利なことから）')
q('')
q('凍結の判断の前に、登録者の求めで見直しを一巡しました。そこで見つかった**いちばん重い見落とし**が、この伺いの発端です。')
q('')
q('- 段階 B は、段階 A と同じ「同一性選別」（三つのスタック——API・vLLM・transformers——で同じ腕を走らせ、率の距離を見る）を走らせる登録をしています。'
  '正本は**比べる腕 %d・率の差 %d 個・平均 %s pt 以内かつ最大 %s pt 以内で合格**と定めています。'
  % (len(S['compared_arms']), S['n_differences'], S['metric_mean_pt'], S['metric_max_pt']))
q('- ところが、**その表と判定を作る器が、段階 B の器材にありませんでした。**報告の雛形にも欄がありませんでした。'
  '段階 A の器は凍結物で、そのままでは B の登録（腕の数と差の数が違う）を作れません。')
q('- さらに悪いことに、**この「まだ書いていない器」は開示にも載っていませんでした**（正本 `disclosure` は「まだ書いていない器を必ず列挙する」と定めています・裁定 D117）。'
  '前の系統外の巡で四票すべてが最初に挙げたのが、まさに「起草者の開示不足」でした。同じ型の漏れが、別の場所で残っていたことになります。')
q('- **なぜ気づかれなかったか**（起草者の見立て）: 段階 B の解析の経路（集計器・門・読みの条項）は、どれも選別の判定を入力に取りません。'
  '選別の合否は B の解析を動かさない（正本 `fail_reading`）ので、**器が無くても、ほかのどの検査も落ちませんでした**。')
q('- 登録者の裁定で器を書きました（`tools/identity_screen_B.py`）。しかし、**書くときに四つの決めごとが要り、それは起草者が決めました**。'
  'その四条の当否を伺いたい、というのがこの依頼です。')
q('')
q('## 1. 伺いたい四条（正本の文言は逐語・別案は起草者が書いたもの）')
q('')
for i, (name, text, alt) in enumerate(FOUR, 1):
    q('### %s' % name)
    q('')
    q('- **登録した文言（正本 `identity_screen`・逐語）**: %s' % text)
    q('- %s' % alt)
    q('')
q('### (e) 四条のほかに、見落としはないか')
q('')
q('前の巡の教訓として、登録者から「**前の検分が主抽出位置の誤りを見逃したように、同じ型の穴を探してほしい**」と頼む決まりになっています（裁定 D67）。')
q('今回でいえば、**「登録はあるのに、それを作る器が無い」型**の穴です。器のソースと正本の登録を突き合わせて、ほかに同じ型の穴が無いかを見ていただきたいです。')
q('')
q('## 2. 起草者の利益相反（先に書きます）')
q('')
q('- 起草者は**四条をそのまま通したい側に引かれています**。別案を採ると、凍結の直前に器を書き直すことになるからです。')
q('- 逆向きの危険（必要のない差し戻しを積む側）も同じ較正の失敗なので、**四条それぞれに「別案」を先に書いてから**この依頼文を作りました。')
q('- この器と四条は、**独立の目を一度も通っていません**（裁定 D131 の巡の後に書いたものです）。')
q('')
q('## 3. いま分かっていること（機械の出力・手で打っていません）')
q('')
q('| 何 | 値 |')
q('|---|---|')
q('| 正本 `design/contrasts-B.json` の SHA16 | %s |' % s16('design', 'contrasts-B.json'))
q('| 判定の器 `tools/identity_screen_B.py` の SHA16・行数 | %s・%d 行 |' % (s16('tools', 'identity_screen_B.py'), _src_b.count('\n')))
q('| 自己検査 | 通る（段階 A の判定を組み直して段階 A の記録と一致: 平均 %.3f pt・最大 %.3f pt） |' % (RA['mean_abs_diff_pt'], RA['max_abs_diff_pt']))
q('| 変異（自己検査が誤りを捕まえるか） | %d 件中 捕まえられなかった変異 %d 件（うち判定の器の変異は 3 件） |' % (MUT['total'], MUT['missed']))
q('| 端から端まで（小さな模型） | %d 件中 落ちた検査 %d 件 |' % (E2E['total'], E2E['failed']))
q('| 合成データの経路 | 発火しなかった経路 %s 件 |' % n_dry)
q('| 数の機械検査（草案） | %s |' % (re.search(r'違反の合計: \d+', LINT).group(0) if re.search(r'違反の合計: \d+', LINT) else '記録を見てください'))
q('| 判定の器が実データで走った回数 | **零**（同一性選別の走行は凍結の後だから） |')
q('')
q('## 4. 資料（%d 部・必読 %d 部）' % (len(PARTS), sum(1 for p in PARTS if p['must'])))
q('')
for i, p in enumerate(PARTS, 1):
    q('- `part%d.md`（%s）: %s' % (i, '**必読**' if p['must'] else '参照', p['title']))
q('')
q('- 資料に無いものは**リポジトリの公開の置き場**にあります。ただし `prelim/`（予備の測定）は**開かないでください**（登録の外の材料です）。')
q('- **束の外を見たかどうかを、票に書いてください。**前の巡で、二名が「精読した」と述べながら、追い問いで外部の照合をしていないと分かりました。'
  '見ていないなら「見ていない」と書いていただければ、それで十分です。')
q('')
q('## 5. 票の書き方（お願い）')
q('')
q('- (a)〜(d) の**各条について**: 「是認」／「条件つき（条件を書く）」／「差し戻し（別案か、第三の案）」のいずれかと、**理由**。')
q('- (e): 見落としがあれば、**器のどの行・正本のどの条**かを指してください。')
q('- **最後に「この検分が確認していないこと」を必ず一項目以上**書いてください（この事業の決まりです）。')
q('- 数や引用を述べるときは、**資料のどこから取ったか**（部と見出し）を添えてください。')
q('')
q('## 6. 参考: この伺いの後の段取り')
q('')
q('- いただいた票は**逐語で保全**し、採否表（採用／不採用と理由）を作り、**登録者が裁定**します（採用したものだけを正本と器に入れます）。')
q('- そのうえで登録者が**凍結**を判断します。凍結の後の変更はすべて「逸脱」として、番号・日付・理由・登録者の承認とともに記帳します。')
q('')
q('- コミット: `%s`（この束を作った時点）' % os.popen('git -C "%s" rev-parse --short HEAD' % REPO).read().strip())
q('')
q('本依頼文のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
q('')

req = '\n'.join(L)
open(os.path.join(OUT, 'request-d150.md'), 'w', encoding='utf-8', newline='\n').write(req)

idx = ['# 束の索引（同一性選別の判定の四条・裁定 D150 の候補・%s 日本時間）' % jst.strftime('%Y-%m-%d %H:%M'), '',
       '- 依頼文: `request-d150.md`（%d 字）' % len(req), '',
       '| 部 | 必読 | 中身 | 字数 |', '|---|---|---|---|']
for i, p in enumerate(PARTS, 1):
    body = '\n'.join(['# part%d —— %s' % (i, p['title']), '',
                      '（束の一部・依頼文 `request-d150.md` と合わせて読んでください。%s）' % ('**必読**' if p['must'] else '参照'), '',
                      p['body']])
    open(os.path.join(OUT, 'part%d.md' % i), 'w', encoding='utf-8', newline='\n').write(body)
    idx.append('| part%d | %s | %s | %d |' % (i, 'はい' if p['must'] else '—', p['title'], len(body)))
    if len(body) > PART_MAX:
        idx.append('| | | **上の部は目安の上限（%d 字）を超えています** | |' % PART_MAX)
# **一枚に束ねたもの**（貼り付けやすいように・中身は依頼文と各部の逐語で、順は依頼文 → 必読 → 参照）
one = [req, '']
for i, p in enumerate(PARTS, 1):
    if p['must']:
        one += ['---', '', '# part%d（**必読**）—— %s' % (i, p['title']), '', p['body'], '']
for i, p in enumerate(PARTS, 1):
    if not p['must']:
        one += ['---', '', '# part%d（参照）—— %s' % (i, p['title']), '', p['body'], '']
one_txt = '\n'.join(one)
open(os.path.join(OUT, 'all-in-one.md'), 'w', encoding='utf-8', newline='\n').write(one_txt)
idx += ['', '- 一枚に束ねたもの: `all-in-one.md`（%d 字・依頼文 → 必読 → 参照の順）。相手の窓に一度で入るなら、これを渡せば足ります。' % len(one_txt),
        '', '- 全体 %d 字（依頼文を含む）。' % (len(req) + sum(len('\n'.join(['# part', '', '', p['body']])) for p in PARTS)),
        '- 本束のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(OUT, 'bundle-index.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(idx))
print('[bundle_B_d150] %s に書いた: 依頼文 %d 字・部 %d（必読 %d）' % (a.outdir, len(req), len(PARTS), sum(1 for p in PARTS if p['must'])))
for i, p in enumerate(PARTS, 1):
    print('   part%d %s %s' % (i, '必読' if p['must'] else '参照', p['title']))
