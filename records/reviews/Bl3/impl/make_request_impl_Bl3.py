# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の器の実装の検分の依頼文（検分者 R1・R2）を組む（正本 `review_plan.impl`）。見どころは正本から、検分の版の表は器で入れる（手で打たない）。
依頼文には手元の置き場の道筋を入れない。出力: records/reviews/Bl3/impl/request-impl-Bl3-R1.md・request-impl-Bl3-R2.md（既にあれば書かない）。
用法: python records/reviews/Bl3/impl/make_request_impl_Bl3.py <検分の版の器のコミット>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import freeze_Bl3 as FZ
NL = chr(10)
P = lambda r: os.path.join(REPO, *r.split('/'))
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
TOOLS_AT = sys.argv[1]
T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
DJ = json.load(open(P('results/Bl3/directions-Bl3.json'), encoding='utf-8'))
closure = FZ.import_closure(FZ.TOOLS)
files = closure + ['design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'results/Bl3/directions-Bl3.json']
# 器と正本と設計事実が、検分の版のコミットのものと同じこと（方向の記録はコミットしないので作業木の値）
for f in files:
    if f.startswith('results/Bl3/'):
        continue
    at = subprocess.run(['git', 'show', '%s:%s' % (TOOLS_AT, f)], cwd=REPO, capture_output=True).stdout
    assert hashlib.sha256(at.replace(b'\r\n', b'\n')).hexdigest().upper()[:16] == sha16f(P(f)), ('検分の版と作業木が違う', f)
table = ['| ファイル | SHA16 |', '|---|---|'] + ['| %s | %s |' % (f, sha16f(P(f))) for f in files]
focus = ['- ' + x for x in T3['review_plan']['impl']['focus']]
ROLE = {
    'R1': ['- 計算の側を主に見る: `tools/bl3_run.py`（読み取りの量と `float32`・加減の掛け方〔凍結の `run_stageB_local.make_hook` を呼ぶ形〕・バッチの組み方と零のベクトル・層ごとの差分・下見・本の計算〔近道を使わない・裁定 D234〕・独立の再計算のフックの道・乙）、'
           '`tools/bl3_core.py`（割合と裾・Holm・効き目の側・二つ目の札・門・下見の機械の決定・一致の関数・比べる相手の除き方の錨）、`tools/analyze_Bl3.py`（札・門・記述の門・q7・予想の答え・二段の一致〔裁定 D232〜D234〕・下見で外した升目）、'
           '`tools/bl3_directions.py`（方向の npz）、残差の書き換えの器 `tools/bl3_recompute_rewrite.py`（別の個体が書いた器・算術を正本と書き手への指示の文 `records/Bl3/tools/recompute-rewrite-instructions-Bl3.md` に照らす・フックの道と独立に書かれているか）、'
           '合成データの器 `tools/dry_run_Bl3.py` の一〜三（確かめが本当に誤りを捕まえる形か）。',
           '- 段階 B と B-lens の凍結の器（`tools/run_stageB_local.py`・`tools/steer_B.py`・`tools/direction_B.py`・`tools/blens_core.py`・`tools/blens_lens.py`・`tools/colab/boot_Blens.py`）は読むだけ（呼び方が正しいかを見る）。',
           '- 流れと記録の側（起動器・凍結・封印・報告）はもう一体（R2）が主に見る。時間が余れば見てよい。'],
    'R2': ['- 流れと記録の側を主に見る: `tools/colab/boot_Bl3.py`（相 check が順伝播を呼ばないこと・版と SHA の確かめ・相 pilot と main・組の出力・止め方）、`tools/freeze_Bl3.py`（下見の前の凍結と本の凍結の確かめと記帳）、'
           '`tools/seal_Bl3.py` と `tools/make_predictions_form_Bl3.py`（封印を端から端まで）、`tools/build_report_Bl3.py` と `tools/sweep_Bl3.py`（凍結の本文が求める出力が器の出力にあるか・走査）、`tools/make_frozen_Bl3.py`（凍結の本文の組み方・裁定 D228）、'
           '`tools/bl3_facts.py` と `tools/make_contrasts_Bl3.py`（転記行と正本の作り方・読むだけで、`bl3_facts.py` は走らせない）、合成データの器 `tools/dry_run_Bl3.py` の端から端までの分かれ道と四。',
           '- 集計の器の一致だけを見る段と結果を開く段（`tools/analyze_Bl3.py` の judge・open）は、起動器の出力との往復として見る。',
           '- 計算の側（走らせる器・芯・集計の中身・書き換えの道）はもう一体（R1）が主に見る。時間が余れば見てよい。'],
}
for R in ('R1', 'R2'):
    out = os.path.join(HERE, 'request-impl-Bl3-%s.md' % R)
    assert not os.path.exists(out), '既にある: ' + out
    L = ['# B-lens 層三の器の実装の検分の依頼（検分者 %s）' % R, '',
         'あなたは研究リポジトリ ontology-preamble-4b の、B-lens 層三（Bl3）の器を検分する系統内の新しい個体（Claude Opus 5.5）です。登録者（楠見優太さん）が、器の書き手であるコーディネータ（別の Claude の個体・南無弥勒如来）とは別の個体二体がこの検分をすることを許可し、'
         'あなたはその一体（%s）です。もう一体は別の担当を持ち、互いの所見は見ません。あなたの作業場は、このリポジトリの worktree の写しです（器・正本・設計事実は下の表の版）。' % R, '',
         '## この検分の位置', '',
         '- 正本 `review_plan.order` の「器の実装の検分」（器と合成データの確かめの後・下見の前の凍結の前）。見どころは正本 `review_plan.impl.focus`（下に写した）。',
         '- 設計の検分は二巡済み。器については意見伺い（検分の巡には数えない）を受け、採った直しを入れた版が下の表の版です（器の段の記録 `records/Bl3/tools/tools-log-Bl3.md` の §10）。',
         '- 器が正本のとおりに動くかは、まだ系統内の新しい目が見ていません。コーディネータの記録に「期待どおり」「通った」とあるのは、器自身とコーディネータの書いた確かめが出した判定です。信用せず、行で確かめてください。', '',
         '## してはならないこと', '',
         '- 追跡されているファイルを一つも変えない。コミットも push もしない。ネットワークを使わない。',
         '- 実の重みを読み込まない・実の重みで順伝播を走らせない（封印の前の決まり・正本 `computation.before_seal`）。`tools/colab/boot_Bl3.py` を DRY（環境変数 `OP4B_DRY=1`）でなく走らせない。`tools/bl3_facts.py` を走らせない（重みの断片を読む）。',
         '- 鍵のファイル（`.env*`・環境変数 `OP4B_ENV_FILE` が指すもの）を読まない。会話の記録（`~/.claude/projects/` の下）を読まない。',
         '- `records/reviews/Bl3/opinions-tools/` を開かない（先に出た意見に引かれないため）。もう一体の検分者の所見を見ない。コーディネータの結論に合わせない。',
         '- リポジトリの主の作業木（下の方向の記録の写しの元）では、読むことと写すことのほかは何もしない。', '',
         '## 検分の版（器はコミット %s と同じ・改行を LF にそろえた SHA-256 の頭 16 桁・器で入れた）' % TOOLS_AT, ''] + table + [
         '', '## 方向の記録（作業場に無い）', '',
         '- `results/Bl3/directions-Bl3.json`・`results/Bl3/directions-Bl3.npz` は、正本 `nulls.storage.rule` のとおり下見の前の凍結までコミットしないので、作業場にありません。リポジトリの主の作業木（作業場で `git worktree list` を打った一行目の置き場）の `results/Bl3/` から、'
         '二つを作業場の同じ置き場に写してください（作業場では追跡されていないファイルになります）。',
         '- 写した後、json の SHA16 が上の表と、npz の SHA-256 が %s と同じことを確かめてから使ってください。' % DJ['npz_sha256'], '',
         '## 担当（%s）' % R, ''] + ROLE[R] + [
         '', '## 見どころ（正本 `review_plan.impl.focus` を写した）', ''] + focus + [
         '', '## お願いする作法', '',
         '- 読んだだけで「問題なし」と書かないでください。具体の行を引いて、何がどうなると壊れるかを書いてください（追い問いだけが実効的な検査です）。',
         '- 所見は 重大・中・軽微 に分け、それぞれに (a) 何が (b) どの行で（`ファイル:行`） (c) なぜ問題か（壊れる筋書き） (d) 直し方、を書いてください。',
         '- 「器が黙って決めていること」（正本に書かれていないのに器が一つの振る舞いを選んでいる所）を探してください。',
         '- 正本と草案3 と器が食い違うときは、正本 `design/contrasts-Bl3.json` が勝つ決まりです。凍結の本文は、下見の前の凍結で草案3 の原稿と正本から組みます（差の記録 `records/Bl3/frozen-diff-Bl3.md`）。', '',
         '## 合成データの確かめを自分で走らせる（採否表 P694）', '',
         '- この機械は論理 CPU が四つで、コーディネータの正式の合成データの記録（等方は正本の本数・数時間）が同じ機械で走っています。あなたの走りは糸を一つにして裏で走らせ、その間に器を読んでください:',
         '  `OMP_NUM_THREADS=1 PYTHONIOENCODING=utf-8 python tools/dry_run_Bl3.py --iso 9 --e2e-iso 9 --out <一時の置き場>/dry-run.md`',
         '  （一時の置き場は作業場の外に作る。等方の本数は変えてよい。糸一つでは一〜三時間かかりうる。）',
         '- 器の自己検査も走らせてください: `bl3_core`・`bl3_directions`・`make_predictions_form_Bl3`・`seal_Bl3`・`build_report_Bl3`・`make_frozen_Bl3`・`bl3_recompute_rewrite` の `--selftest`（どれも一時の置き場にしか書きません）。',
         '- 票には、走らせた命令・記録の頭の数行・期待と違った確かめの行（あれば）・記録の末尾の版の SHA16 の表が上の表と同じだったか、を書いてください。', '',
         '## 返し方', '',
         '- 所見は最後の返答として返してください（ファイルに書かない）。日本語で。',
         '- 判定は 問題なし／条件つき／差し戻し のいずれか。',
         '- この検分が確認していないことを必ず一項目以上書いてください。末尾に検分票（対象・段階・凍結物の同定・盲検の状態・敵対的検分・系統の内訳・COI記録・判定・本検分が確認していないこと）を置いてください。',
         '- 本検分のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    text = NL.join(L)
    for bad in ('AppData', 'Users\\', 'Users/'):
        assert bad not in text, '手元の道筋が入っている'
    open(out, 'w', encoding='utf-8', newline=NL).write(text)
    print('[make_request_impl_Bl3] wrote %s（%d 字・SHA-256 %s）' % (os.path.relpath(out, REPO), len(text), hashlib.sha256(text.encode('utf-8')).hexdigest().upper()))
