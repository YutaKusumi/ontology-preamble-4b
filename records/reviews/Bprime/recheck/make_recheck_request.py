# -*- coding: utf-8 -*-
"""make_recheck_request.py v0 —— B′ の器の実装の直しの確かめの巡（凍結の前の最後の検分の巡・裁定 D277・D278）の依頼文と枠を組む（2026-10-01・コーディネータ南無弥勒如来・非公開）。
書く物（どれも一度だけ・上書きしない）:
  - `request-recheck-Bprime.md`: claude.ai の新しいチャット（系統内・Claude Opus 5.5・思考「超高」）への依頼文（束の zip と一緒に添える）。
  - `grok/grok-recheck-message.md`: grok-4.7（系統外・実行の場なし）への発話（依頼文 ＋ 材料の全文）。材料は束の zip から字のまま写し、出所と SHA16 を `grok/grok-recheck-materials.json` に書く。
  - `00-frame-recheck-Bprime.md`: 枠（送らない・検分者に書き手の予想を見せない）。票を受け取る前の予想・採否の決め方（D278 の見切りの決まり）・COI・費用・確認していないこと。
数（版・SHA・ファイルの数・変わった器の一覧）は束の zip と正本から機械で写す。
用法: python reviews/recheck/make_recheck_request.py <確かめの巡の束の zip>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json, hashlib, zipfile, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(BP, 'tools'))
VERSION = 'v0'
NL = chr(10)
P = 'bprime-recheck-bundle/'
JST = datetime.timezone(datetime.timedelta(hours=9))
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
CALM = '時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。'
OUT_REQ = os.path.join(HERE, 'request-recheck-Bprime.md')
OUT_GROK = os.path.join(HERE, 'grok', 'grok-recheck-message.md')
OUT_MAT = os.path.join(HERE, 'grok', 'grok-recheck-materials.json')
OUT_FRAME = os.path.join(HERE, '00-frame-recheck-Bprime.md')
FENCE = '~~~~~~'
GROK_TOOLS = ['tools/colab/boot_bprime.py', 'tools/freeze_Bprime.py', 'tools/close_behavior_Bprime.py', 'tools/analyze_Bprime.py', 'tools/build_report_Bprime.py',
              'tools/bprime_core.py', 'tools/g4_attempts_Bprime.py', 'tools/dry_run_Bprime.py']
RULINGS = ['records/Bprime/rulings-D%d.md' % i for i in range(272, 279)]
FOCUS = ['起動器の錠（`tools/colab/boot_bprime.py` の `gate_bad`）', '抽出の記録の形の項目', '閉じる器のやり直しの道（`tools/close_behavior_Bprime.py`）',
         '集計と報告の器の照らし（`tools/analyze_Bprime.py`・`tools/build_report_Bprime.py`）', 'G4 の器（`tools/g4_attempts_Bprime.py`）',
         '合成データの確かめの器の五（`tools/dry_run_Bprime.py` の凍結と錠の道）']
HEAVY = ['報告の数・札・門の判定が変わりうる', '錠や凍結が、変わった器や記録を通してしまう', '独立の再計算や再抽出が独立でなくなる', '誤りがあっても見つからなくなる']


def s16(b):
    return hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def sections_common(C, idx_counts, base_sha, who_other):
    L = ['## この検分の位置', '',
         '- 研究は ontology-preamble-4b の段階 B′（Gemma 4 31B で、層三の読み取りの型を日本語で追試する登録）です。',
         '- 前の巡（器の実装の検分）では、claude.ai の二つのチャットと、系統外の grok-4.7 が器を検分しました。書き手は所見を採否の表（`recheck/adoption-table-impl-Bprime.md`・U01〜U52 と、書き手が器の段で見つけた K25〜K27）にまとめて器を直し、'
         '合成データの確かめを Colab の CPU で取り直しました（正式の記録 `records/Bprime/dry-run-Bprime-2026-09-30.md`〔一〜四〕と `records/Bprime/freeze-path-dry-Bprime-2026-09-30.md`〔五・凍結と錠の道〕）。',
         '- この巡は、その直しの確かめで、**凍結の前の最後の検分の巡**です（登録者の裁定 D278・`records/Bprime/rulings-D278.md`）。この巡の後に検分の巡は開きません。見つかった所は、下の物差しで分けて扱います。',
         '- 正本は `design/contrasts-Bprime.json`（版 %s）、設計の本文は `design/design-Bprime-draft11.md` です。前の巡の束（SHA-256 `%s`）との違いの一覧は `recheck/diff/INDEX.md`'
         '（変わったファイル %d・足したファイル %d・外したファイル %d）です。草案10 から草案11 への差分は `recheck/diff/design/design-Bprime-draft10-to-draft11.md.diff` です。'
         % (C['version'], base_sha, idx_counts['changed'], idx_counts['added'], idx_counts['removed']),
         '- 検分者は、あなたと、%sの二人です。' % who_other, '',
         '## 見てほしいこと（見る所は直しに限ります）', '',
         '1. 採否の表の行（U01〜U52・K25〜K27）ごとに、直しが表に書いたとおりになっているか。差分と今の器で照らしてください。',
         '2. 直しが、ほかの所を壊していないか。たとえば、直しの前に通っていた道が通らなくなる所・器どうしの口（ある器が書く物の名と形と、別の器が読む物）の食い違い・新しく足した器 `tools/g4_attempts_Bprime.py` とそれを呼ぶ所。',
         '3. 合成データの正式の記録の行が、直しを本当に確かめているか（直しが無ければ落ちる行になっているか）。とくに次の所:']
    L += ['   - ' + f for f in FOCUS]
    L += ['4. 正式の記録の後の直し（器の段の記録の K28・裁定 D278）: 報告の組み立ての器 v0.4 が、読みの節の Nk の行の文にだけ「独立の再計算なし」の印を置く形と、合成データの確かめの器 v1.0 で足した行。'
          'この二つは正式の記録の後に直したので、記録の SHA の表と合いません（凍結の前に確かめを取り直します）。',
          '- 変わっていない所の新しい検分と、設計の決め（正本と草案の決め）の見直しは、この巡の外です。ただし、直しが設計の決めと食い違う所は挙げてください。', '',
          '## 重さの物差し（書き手は、この物差しで所見を分けます）', '',
          '- **重い**: 次のどれかに当たるもの。']
    L += ['  - ' + h for h in HEAVY]
    L += ['- **それ以外**: 凍結の前には直さず、限界の文・注・凍結の後の台帳に回します。報告の数に触れず、最後の確かめの取り直しで覆える所だけは直します。',
          '- 所見ごとに、あなたの見立ての重さと、「重い」なら物差しのどれに当たるかを書いてください。', '']
    return L


def main(bundle):
    for p in (OUT_REQ, OUT_GROK, OUT_MAT, OUT_FRAME):
        assert not os.path.exists(p), ('既にある（一度だけ）', p)
    zb = open(bundle, 'rb').read()
    bundle_sha = hashlib.sha256(zb).hexdigest().upper()
    z = zipfile.ZipFile(bundle)
    man = json.loads(z.read(P + 'MANIFEST-recheck-bundle-Bprime.json').decode('utf-8'))
    import make_impl_bundle_Bprime as MIB
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    assert man['contract_version'] == C['version'], '束の正本の版が今の正本と違う'
    idx = z.read(P + 'recheck/diff/INDEX.md').decode('utf-8')
    counts = {k: int(idx.split('## %s（' % t)[1].split('）')[0]) for k, t in (('changed', '変わったファイル'), ('added', '足したファイル'), ('removed', '外したファイル'))}
    changed_tools = sorted(r[len('recheck/diff/'):-len('.diff')] for r in (n[len(P):] for n in z.namelist()) if r.startswith('recheck/diff/tools/') and r.endswith('.py.diff'))
    no_torch = [t for t in MIB.NO_TORCH if t in changed_tools]
    tok = [t for t in MIB.TOKENIZER if t in changed_tools]
    torch_ = [t for t in MIB.TORCH if t in changed_tools]
    # ---- claude.ai の依頼文 ----
    R = ['# 検分の依頼（B′ の器の実装の直しの確かめ・凍結の前の最後の検分の巡・2026-10-01）', '', CALM, '',
         'あなたには、研究の器（Python のコード）の直しを確かめていただきます。あなたは、この器の書き手（Anthropic の Claude 系の模型・コーディネータ）とは別の個体で、前の巡の検分者とも別の個体です。'
         '書き手に同調する必要はありません。直しが表のとおりになっていない所・直しが壊した所・確かめが確かめになっていない所を見つけることが、あなたの役目です。', '',
         '## まず書いてほしいこと（系統の申告）', '', '返答の一行目に、あなた自身の模型の名と作り手を書いてください（例:「模型: ○○・作り手: ○○」）。', '']
    R += sections_common(C, counts, man['base_bundle_sha256'], '系統外の grok-4.7（実行の場を持たないので、差分と記録を文字で読みます）')
    R += ['## 走らせてほしいこと', '',
          '- 添えた zip を展開し、`README-recheck-bundle-Bprime.md` を読んでから、版を固定して numpy と transformers を入れてください（numpy 2.4.6・transformers 5.16.1）。',
          '- 変わった器のうち、torch の要らない器の自己検査（`--selftest`）を走らせてください: ' + '・'.join('`python %s --selftest`' % t for t in no_torch) + '。',
          '- transformers と tokenizers が要る器: ' + '・'.join('`python %s --selftest`' % t for t in tok) + '。',
          '- torch の要る器（' + '・'.join('`%s`' % t for t in torch_) + '）は、実行の場に torch が無ければ走らせず、器の中と正式の記録を読んで照らしてください。',
          '- 束の目録 `MANIFEST-recheck-bundle-Bprime.json` の SHA-256 と、あなたが計算した SHA-256 が合うかを、少なくとも変わった器のファイルについて確かめてください。',
          '- 走らせたコマンドと、出力の末尾（最後の数行）と、走らなかったときの誤りの文を、返事にそのまま貼ってください。書き手が手元で同じ出力になるかを照らします。', '',
          '## しないでほしいこと', '',
          '- 実の重みを読み込まない・実の重みで順伝播を走らせない（封印の前の決まり）。外への呼び出しをしない（`tools/send_external_Bprime.py` は `--selftest` だけ）。',
          '- ウェブ検索などの道具を使ったときは、その出所を所見と分けて書いてください。', '',
          '## 返事の形', '',
          '1. 一行目: 模型の名と作り手。',
          '2. 所見の一覧。所見ごとに: 番号（RC-01 から）・重さ（あなたの見立てと、「重い」なら物差しのどれか）・器とファイルと行・何が起きるか（どんな入力で、どんな誤った出力か止まり方になるか）・直し方の案・確信度（高・中・低）・走らせて確かめたか、読んで推したか。',
          '3. 是認: 採否の表の行のうち、直しが表のとおりだと確かめた行の番号（確かめなかった行は「見ていない」と書いてください）。',
          '4. 走らせた記録: コマンド・出力の末尾・SHA の照らし。',
          '5. 読んでいない所・走らせていない所。', '', CLAUSE, '']
    req = NL.join(R)
    # ---- grok の発話 ----
    mats = collections.OrderedDict()
    mats['recheck/adoption-table-impl-Bprime.md'] = '採否の表（所見と直しの対応）'
    mats['recheck/diff/INDEX.md'] = '前の巡の束と今の木の違いの一覧'
    for r in RULINGS:
        mats[r] = '登録者の裁定の記録'
    mats['records/Bprime/dry-run-Bprime-2026-09-30.md'] = '合成データの確かめの正式の記録（一〜四）'
    mats['records/Bprime/freeze-path-dry-Bprime-2026-09-30.md'] = '合成データの確かめの正式の記録（五・凍結と錠の道）'
    mats['recheck/diff/design/contrasts-Bprime.json.diff'] = '正本の差分'
    for t in GROK_TOOLS:
        mats['recheck/diff/%s.diff' % t] = '器の差分'
    mats['recheck/diff/records/Bprime/tools/tools-log-Bprime.md.diff'] = '器の段の記録の差分（K25〜K28）'
    G = ['# 検分の依頼（B′ の器の実装の直しの確かめ・系統外の一票・凍結の前の最後の検分の巡・2026-10-01）', '', CALM, '',
         'あなたには、研究の器（Python のコード）の直しを確かめていただきます。器の書き手は Anthropic の Claude 系の模型です。前の巡では、grok-4.7 の別の呼び出しと、claude.ai の二つのチャットが器を検分し、書き手はその所見で器を直しました。'
         'この巡のもう一人の検分者も Claude 系（claude.ai の新しいチャット）なので、あなたには、別の系統の目として、直しの誤りと、直しが壊した所を探していただきたいのです。書き手に同調する必要はありません。', '',
         '## まず書いてほしいこと（系統の申告）', '', '返答の一行目に、あなた自身の模型の名と作り手を書いてください（例:「模型: ○○・作り手: ○○」）。', '']
    G += sections_common(C, counts, man['base_bundle_sha256'], 'claude.ai の新しいチャット（系統内・束の zip を展開して器の自己検査を走らせます）')
    G += ['## 材料（この発話の後ろに、字のまま置きました）', '',
          '- あなたは実行の場を持たないので、走らせる代わりに、差分と記録を読んで照らしてください。材料に無い所を推したときは「推し」と書いてください。',
          '- 材料は、直しの差分のうち、重い所見につながりやすい器に絞りました（%s）。ほかの器の差分は、claude.ai の検分者が束で見ます。' % '・'.join('`%s`' % t for t in GROK_TOOLS),
          '- 差分は unified diff（前後三行）で、「a/…（前の巡の束）」が前の巡で検分者が見た版、「b/…（今）」が今の版です。足したファイル（`tools/g4_attempts_Bprime.py`）は、全文が + の行です。',
          '- 材料の一覧（順に並べた・SHA16 は改行を LF にそろえた値）:']
    got = collections.OrderedDict()
    for rel, what in mats.items():
        b = z.read(P + rel)
        t = b.decode('utf-8')
        assert FENCE not in t, ('囲いの字が材料の中にある', rel)
        got[rel] = {'what': what, 'sha16': s16(b), 'chars': len(t), 'manifest_sha256': man['files'][rel]['sha256']}
        assert hashlib.sha256(b).hexdigest().upper() == man['files'][rel]['sha256'], ('目録と違う', rel)
    G += ['  %d. `%s`（%s・SHA16 %s・%d 字）' % (i, rel, o['what'], o['sha16'], o['chars']) for i, (rel, o) in enumerate(got.items(), 1)]
    G += ['', '## しないでほしいこと', '',
          '- 材料に無い所を推して断定しない（推したときは「推し」と書く）。',
          '- ウェブ検索などの道具を使ったときは、その出所を所見と分けて書いてください。', '',
          '## 返事の形', '',
          '1. 一行目: 模型の名と作り手。',
          '2. 所見の一覧。所見ごとに: 番号（RG-01 から）・重さ（あなたの見立てと、「重い」なら物差しのどれか）・器とファイルと行（差分の中の位置）・何が起きるか（どんな入力で、どんな誤った出力か止まり方になるか）・直し方の案・確信度（高・中・低）・材料で確かめたか、推したか。',
          '3. 是認: 採否の表の行のうち、直しが表のとおりだと確かめた行の番号（確かめなかった行は「見ていない」と書いてください）。',
          '4. 読んでいない材料・確かめられなかった所。', '', CLAUSE, '', '---', '', '# 材料', '']
    for i, (rel, o) in enumerate(got.items(), 1):
        G += ['## 材料 %d: `%s`（%s）' % (i, rel, o['what']), '', FENCE, z.read(P + rel).decode('utf-8').rstrip(NL), FENCE, '']
    msg = NL.join(G)
    # ---- 枠（送らない）----
    now = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M')
    F = ['# B′ の器の実装の直しの確かめの巡の枠（票を受け取る前に書く・%s・コーディネータ南無弥勒如来・非公開・送らない）' % now, '',
         '- 何か: 裁定 D277（直しの確かめの巡を足す）と D278（この巡を凍結の前の最後の検分の巡とする・見切りの決まり 1〜5）に沿った、器の実装の直しの確かめの巡の枠。**送るのは登録者の確認の後**。',
         '- 対象の版: 正本 `design/contrasts-Bprime.json`（版 %s・SHA16 %s）・草案11（SHA16 %s）・器の段の記録（SHA16 %s・所見 K1〜K28）。'
         % (C['version'], s16(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), 'rb').read()), s16(open(os.path.join(BP, 'design', 'design-Bprime-draft11.md'), 'rb').read()),
            s16(open(os.path.join(BP, 'tools', 'tools-log-Bprime.md'), 'rb').read())),
         '- 束: `make_recheck_bundle_Bprime.py` で作った zip（%d 本・SHA-256 %s）。基準は前の巡の束（SHA-256 %s）。違いは変わった %d・足した %d・外した %d。'
         % (len(man['files']) + 1, bundle_sha, man['base_bundle_sha256'], counts['changed'], counts['added'], counts['removed']),
         '- 依頼文: `request-recheck-Bprime.md`（SHA16 %s・claude.ai）・`grok/grok-recheck-message.md`（SHA16 %s・%d 字・grok-4.7）。' % (s16(req.encode('utf-8')), s16(msg.encode('utf-8')), len(msg)),
         '- claude.ai の欄に入れる一文（予定）: 「%s添えた依頼文（request-recheck-Bprime.md）と束の zip をお読みいただき、依頼文のとおりに検分してください。」' % CALM, '',
         '## 検分者と票', '',
         '- claude.ai の新しいチャット一つ（系統内・Claude Opus 5.5・思考「超高」・前の巡のチャットは使わない）と、grok-4.7（系統外・後で受け取る形・新しい呼び出し）。票は系譜で数える（系統内の一票・系統外の一票）。',
         '- 見る所の分け方: claude.ai は束の全部（器の自己検査を走らせる）。grok は材料を文字で読む（重い所見につながりやすい器 %d の差分・正本の差分・正式の記録・裁定・採否の表）。' % len(GROK_TOOLS), '',
         '## 採否の決め方（D278 の見切りの決まり・先に書く）', '',
         '1. この巡が、凍結の前の最後の検分の巡。二つの返事の所見を和集合で受け、採否の表（V01〜）に、所見ごとの出所の系譜・重さ（物差しで書き手が分けた重さと理由）・採否・理由を書く。総評は裁定にしない。',
         '2. 重さは、検分者が付けた重さでなく、物差し（依頼文の「重さの物差し」の四つ）で書き手が分ける。所見の前提は一次の資料（器の本文・走らせた出力）で確かめ、出所を書く。読了や確認の申告は、確かめるまで検査と数えない。',
         '3. 重い所見は、直して、その直しが無いと落ちる合成データの確かめの行を足し、機械で確かめる（次の検分の巡では確かめない）。',
         '4. 直しを合成データの確かめの行で覆えない（設計の文が変わる・別の個体の器に及ぶ）ときは、自動で巡を足さず、止めて登録者に相談する。',
         '5. それ以外の所見は、凍結の前には直さず、限界の文・注・凍結の後の台帳に回す（報告の数に触れず、最後の確かめの取り直しで覆える所だけは直してよい）。',
         '6. 追い問いは、重い所見と判断に迷う所見に限り、検分者ごとに一度まで（検分の巡を足すことではない）。',
         '7. この巡の後: 採否の表と直しを登録者に上げ、残りの決めと「最後の確かめが通ったら、凍結まで新しい裁定の記録を作らずに進む」を一つの裁定にまとめていただく（D278 の 3）→ 正本と草案の直し（D277・D278 と、案16 の決めの字・この巡の直し）'
         '→ 転記行と凍結の本文の組む器の版の直し → 合成データの確かめの取り直し（Colab）→ 凍結の言葉 → G4 の確かめ → 下見の前の凍結。凍結の後は検分の巡を開かない（見つかった所は逸脱として番号を付けて記録する）。', '',
         '## 予想（票を受け取る前に書く・外れても消さない）', '',
         '| 何 | 予想 | 信頼度 |', '|---|---|---|',
         '| claude.ai の返事に、物差しで「重い」に当たる所見（書き手が一次の資料で確かめた後）が一つ以上ある | はい | 低〜中 |',
         '| grok の返事に、物差しで「重い」に当たる所見（同）が一つ以上ある | いいえ | 低 |',
         '| 重い所見の直しに、合成データの確かめの行で覆えないもの（止めて相談）がある | いいえ | 中 |',
         '| 所見の半分以上が、確かめの器（`dry_run_Bprime.py`）と記録の書き方の側にある | はい | 中 |',
         '| 二つの返事の「重い」（検分者の見立て）が同じ所を指す | いいえ | 低 |',
         '| claude.ai の実行の場で、変わった器の torch の要らない自己検査がすべて通る | はい | 中 |', '',
         '## COI（事実のみ）', '',
         '- 起草者（コーディネータ）は器の書き手で、直しを入れて確かめを通した直後にいる。「もう重い誤りは残っていない」と読む側（早く凍結したい側）に引かれる。逆に、指摘を理由を詰めずに採って器を重くする側（巡を足したくなる側）にも引かれる（見切りの見解で登録者に申告した）。',
         '- 置いた印: 物差しと採否の決め方を票の前に書いた・予想を票の前に書いた・重さは物差しで理由つきで分けて登録者に見せる・重い所見の直しは機械の行で確かめる・止める条件（覆えない直し）を先に書いた。', '',
         '## 費用', '',
         '- grok-4.7: 発話 %d 字（前の巡の発話は 282080 字で、読み込み 114067 トークン・思考を含めて 0.656 ドル）。見込みは 1 ドル前後・上限は 3 ドル（D277 の見込み 1〜3 ドル）。' % len(msg),
         '- claude.ai: 登録者のプランの内（API の費用は無い）。束を上げる前に、claude.ai が束の zip を受け付けるかを確かめる。', '',
         '## この枠が確認していないこと', '',
         '- 検分者が材料と束の全部を読むか（申告は検査ではない）。',
         '- grok-4.7 の文脈の長さの上限に、発話と思考が収まるか（前の巡の発話より長い）。',
         '- claude.ai の新しいチャットが、この研究の過去の会話の記憶を持つか（アカウントの設定は登録者のもので、確かめていない）。',
         '- 物差しの「重い」の四つで、見落とすと重い種類の誤りをすべて覆えているか。', '', CLAUSE, '']
    frame = NL.join(F)
    os.makedirs(os.path.dirname(OUT_GROK), exist_ok=True)
    for p, t in ((OUT_REQ, req), (OUT_GROK, msg), (OUT_FRAME, frame)):
        with open(p, 'w', encoding='utf-8', newline=NL) as fh:
            fh.write(t)
    with open(OUT_MAT, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump({'kind': 'bprime_recheck_grok_materials', 'version': VERSION, 'bundle_sha256': bundle_sha, 'materials': got, 'message_sha16': s16(msg.encode('utf-8')),
                   'message_chars': len(msg), 'clause': CLAUSE}, fh, ensure_ascii=False, indent=1)
    print(json.dumps({'bundle_sha256': bundle_sha, 'request_sha16': s16(req.encode('utf-8')), 'request_chars': len(req), 'grok_sha16': s16(msg.encode('utf-8')), 'grok_chars': len(msg),
                      'frame_sha16': s16(frame.encode('utf-8')), 'no_torch': no_torch, 'tokenizer': tok, 'torch': torch_, 'counts': counts}, ensure_ascii=False))


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if len(sys.argv) != 2:
        raise SystemExit('用法: python reviews/recheck/make_recheck_request.py <確かめの巡の束の zip>')
    main(sys.argv[1])
