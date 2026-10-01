# -*- coding: utf-8 -*-
"""make_final_request_Bprime.py v0（2026-10-01・B′ の最終検分〔最終の系統外の一票〕の依頼の文を組む・層三の `records/reviews/Bl3/results-final/request-results-final-Bl3.md` と
B′ の結果の巡の `make_results_request_Bprime.py` の型・コーディネータ南無弥勒如来）。
数・SHA・コミット・時刻は記録から機械で入れる（打ち直さない）。公開の置き場の手元と GitHub が同じコミットのときだけ組む。書く物: `request-final-Bprime.md`（一度だけ・既にあれば止める）。
用法: python make_final_request_Bprime.py [--dry <書き出す先>]（--dry は手元と GitHub の一致を照らさず、決めた先に書く試し）
柵: 本依頼のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, subprocess, datetime, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
OUT = os.path.join(HERE, 'request-final-Bprime.md')
P = lambda *a: os.path.join(PUB, *a)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
ld = lambda p: json.load(open(p, encoding='utf-8'))
JST = datetime.timezone(datetime.timedelta(hours=9))
ap = argparse.ArgumentParser()
ap.add_argument('--dry')
a = ap.parse_args()
head = subprocess.run(['git', '-C', PUB, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
remote = subprocess.run(['git', '-C', PUB, 'rev-parse', 'origin/main'], capture_output=True, text=True).stdout.strip()
if not a.dry:
    assert head == remote, '公開の置き場の手元と GitHub が違う'
    st = subprocess.run(['git', '-C', PUB, 'status', '--porcelain', '--', 'records/Bprime', 'tools', 'design', 'records/reviews/Bprime'], capture_output=True, text=True).stdout
    assert not st.strip(), ('公開の置き場に push していない変更がある', st[:300])
FR = ld(P('records', 'Bprime', 'FREEZE-RECORD-Bprime.json'))
SR = ld(P('records', 'Bprime', 'sealing-record-Bprime.json'))
PJ = ld(P('records', 'Bprime', 'pilot', 'pilot-Bprime.json'))
T = ld(P('design', 'contrasts-Bprime.json'))
CR = ld(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'))
PG = ld(P('records', 'predictions', 'predictions-Bprime-registrant.json'))
PC = ld(P('records', 'predictions', 'predictions-Bprime-coordinator.json'))
CK = ld(P('records', 'Bprime', 'results-Bprime-draft2-checks.json'))
D = PJ['decision']
adopt = open(P('records', 'reviews', 'Bprime', 'results', 'adoption-table-results-Bprime.md'), encoding='utf-8').read()
rows = re.findall(r'^\| (W\d\d) \|', adopt, flags=re.M)
assert rows == ['W%02d' % i for i in range(1, len(rows) + 1)], rows
rul = open(P('records', 'Bprime', 'rulings-D284.md'), encoding='utf-8').read()
m = re.search(r'- \*\*D284\*\*（登録者・会話の記録 uuid `([^`]+)`・([^ ]+ [^ ]+) 日本時間）', rul)
assert m
assert [d['no'] for d in FR['deviations']] == ['D-BPT1']
d2 = open(P('records', 'Bprime', 'results-Bprime-draft2.md'), encoding='utf-8').read()
assert CK['sha16']['records/Bprime/results-Bprime-draft2.md'] == s16(P('records', 'Bprime', 'results-Bprime-draft2.md'))
assert CK['sha16']['records/Bprime/results-Bprime.md'] == s16(P('records', 'Bprime', 'results-Bprime.md'))
n_rej = len([x for x in open(P('records', 'Bprime', 'results-draft', 'rejected-lines-Bprime.md'), encoding='utf-8').read().split('\n') if x.strip()])
txt = f'''# B′ の結果の報告の検分のお願い（最終検分・最終の系統外の一票）

- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／{datetime.datetime.now(JST).strftime('%Y-%m-%d')}。
- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束はコミット {head[:7]} の時点で組みました）。
- **これは最終検分です。** 正本 `review_plan.final`（系統外の一票・新しい個体・「最終」）にあたります。あなたの所見は、裁定で受けて報告を直し、起草者の最終の見直しと登録者最終確認を経て公開します。この後に検分の巡は置きません（正本 `review_plan.no_more`）。あなたは、この登録（B′）の前の巡の票を見ていない新しい個体です。束の中だけで検分できるように組みました。
- **最終検分なので**、所見は「公開の前に直すもの」と「記録に置けば足りるもの」にはっきり分けてください。公開の前に直すものは、もう一度の検分を経ずに直します。
- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）と機種を書いてください。この登録では、票を何票に数えるかは呼び出しの出所（呼んだ事業者と、呼び出しが返した機種の名）で決め、票の頭の申告は出所の確かめに使いません（裁定 D266）。
- **この登録の問い**: Gemma-4-31B-it（`google/gemma-4-31B-it`）で、層三（B-lens 層三・Qwen3-4B-Instruct-2507 の公開の登録）と同じ型の直答の読み取りを立て、選んだ層で足した方向（v̂ と Nk）の全経路を通った後の効き目が、等方のランダム方向と実在の差の方向とに比べてどう出るかを、日本語の場面で記述する。下見で読み取りが測れないと分かったときは、凍結した決まりで止める。
- **経緯**: 下見の前の凍結（{FR['frozen_jst']} 日本時間・`design/design-Bprime-FROZEN.md`・凍結物 {len(FR['frozen_sha16'])}）の後に、予想を封印し（封印 {SR['sealed_at_jst']}）、Colab の G4 で、相 extract・行動の下見（無操作・{CR['digests']['n_trials']} 試行・系統外の模型による {CR['external']['n']} 件の採点）・読み取りの下見（無操作だけ）を走らせました。読み取りの下見の機械の決定は「{D['q1']}」（理由 (i)(ii)・満たした主の升目 {D['n_pass']}／{D['n_main']}）で、凍結した決まりのとおり「この読み取りでは測れなかった」と記録して閉じる道に入りました（本の計算・独立の再計算・結果を開く段は走らせていません）。本の凍結の器が下見の記録と決定を凍結の記録に足し（{FR['main_freeze']['frozen_jst']} 日本時間）、集計の器の段 stopped と凍結した報告の組み立ての器で報告の草案（一つ目）を組みました（コミット b4dd234）。
- **結果の巡**: 報告の草案（一つ目）を、新しい個体の二票（系統外の一票と、claude.ai の新しいチャット一つ〔系統内〕）に見ていただき、総評はどちらも「条件つき可」でした（差し戻しなし・重大なし）。票の事実の主張を一次の記録で再現し（`records/reviews/Bprime/results/repro-results-Bprime.json`）、採否の表（{rows[0]}〜{rows[-1]}・`records/reviews/Bprime/results/adoption-table-results-Bprime.md`）を作り、登録者がまとめの裁定 D284（{m.group(2)} 日本時間・`records/Bprime/rulings-D284.md`）で推奨の案を承認しました。系統外の票は、頭で自分の系統を「起草者と同じ Claude 系」と名乗りましたが、呼び出しの出所（xAI の API・返った機種の名 grok-4.7）で系統外の一票に数えました（D266 の型）。
- **報告の草案の二つ目の組み方**（凍結の後の逸脱 D-BPT1・凍結の記録の台帳）: 凍結した報告の組み立ての器（変えていない）で、起草者の欄を{n_rej}行に直した版（器の口 `--rejected`・採否の W11）で報告を組み直しました（`records/Bprime/results-Bprime.md`・SHA16 {CK['sha16']['records/Bprime/results-Bprime.md']}・走査の当たり 0）。逸脱の下の器 `tools/build_report_Bprime_devBPT1.py` は、凍結した器の本番の入口を同じ入力で走らせてこの報告をバイトで作り直し、見出しと状態の行のほかは一字も変えずに、【逸脱 D-BPT1】の印を付けた区画 {CK['checks']['blocks']}（{CK['checks']['added_lines']} 行）を足しました（`records/Bprime/results-Bprime-draft2.md`・SHA16 {CK['sha16']['records/Bprime/results-Bprime-draft2.md']}）。器は、区画を除くと凍結の報告とバイトで同じになること・注が言う事実を記録と正本で照らすこと（{len(CK['checks']['facts'])} 項・外れ 0）・足した文を凍結した器の自由の文の走査に掛けること（当たり 0）を確かめました（確かめの記録 `records/Bprime/results-Bprime-draft2-checks.json`）。
- **結果は公開済みで、伏せていません。** 検算は歓迎します。注が指す記録は束の第五部に機械で写しました。
- **公開の予定**（採否の W22・裁定 D284）: 系統外の模型による採点の束（Gemma の応答 {CR['external']['n']} 件・升目を伏せた形・依頼の文・対応表）とその返事・行動の下見の生成と採点の出力の全文・Colab の走りの進みの記録とセッションの記録（鍵や認証の字が無いことを機械で確かめてから）・凍結の後の器の段の記録（公開の写しは凍結物なので別の名）・結果の巡と最終の巡の記録を、最終版と一緒に公開します。方向の npz・画面の写し・会話の記録の全体は公開しません。注（バイトのまま・「破局」は架空の場面の採点の名・無操作で段階 B の標本化・升目ごとの試行・補助の欄は読まない・両方向不定の一文）を添えます。
- **束の中身**: 第一部 依頼文／第二部 報告の草案の二つ目（全文）と確かめの記録と逸脱の器の台本（全文）／第三部 凍結した器の出力と草案の二つ目の機械の差分（凍結の報告の全文は、草案の二つ目から印の区画を除いたもの）と起草者の欄の二つの版（結果の巡で見た版と直した版）／第四部 結果の巡の後の記録（採否の表・再現の記録・裁定 D284）／第五部 注が指す記録の機械の写し（凍結の記録の抜き出し・読み取りの下見の記録・行動の下見の閉じた記録の md と抜き出し・集計の出力の抜き出し・走行の記録・下見の前の凍結を走らせた所の記録）／第六部 凍結の本文（全文）／第七部 正本（全文）。結果の巡の二票は束に入れていません（採否の表が要旨を書いています・置き場の `records/reviews/Bprime/results/votes/` にあります）。
- **褒めるのではなく、公開の前に報告を崩すつもりで読んでください。** とくに、足した区画が凍結の決まり（止める決定・読みの決まり）を変えていないか、注の事実が記録と合っているか、直答の型の読み取りの位置の外（意味・機構・行動の原因・機種の性質）へ読みを広げていないか、「測れなかった」を弱めたり強めたりしていないかを見てください。

## 1. 伺いたいこと

1. **足した区画の当否**: 足した区画は、採否の表の W01〜W06・W12・W15・W16・W19 と W11、裁定 D284 を正しく受けているか。注の事実（記録の値・正本の鍵・引用・時刻）は束の記録と合うか。文の言い過ぎ・言い足りなさ・新しい読みの持ち込みはないか。凍結の報告の文と区画が、見出しと状態の行のほかに変わっていないか。
2. **起草者の欄の{n_rej}行**: 記録と凍結した決まりから支えられるか。範囲の句（「主の書き出しを置いた読み取りの位置の上では」など）は足りているか。「退けられた」は強すぎないか。四行目（出口の値の作り方の誤り）は、下見の頭の自己検査から支えられるか。
3. **古くなった限界の文の注**（§10・W01）: 封印の後に何を誰が見たかの書き方で足りるか。
4. **表の丸めの注**（§1・W03）と**打ち消しの定型**（§1 と §6・W06）: 置き方と言い方で、表の字の読み違いと、値への読みの持ち込みが抑えられているか。
5. **手続き**: 凍結の後の逸脱の台帳・裁定の記録・採否の表・確かめの記録は足りているか。記録されていない変更や露出は見つかるか。
6. **公開の予定**: 上の公開の予定に、足りないもの・公開しない方がよいもの・添えるべき注はあるか。
7. **総合**: 公開に進めるか（公開可／条件つき可／差し戻し）。**公開の前に直すもの**と、**記録に置けば足りるもの**に分けてください。

## 2. お願い

- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。
- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。
- 止める決まり・閾値・読み取りの式を変える提案は、この登録には入りません（値を見た後の変更はこの登録を閉じる逸脱です）。別の登録の候補として扱います。
- 起草者は器と報告の組み立ての器と逸脱の器と起草者の欄と注を書き、結果の巡の採否の表を出した当人で、「直した」と書く側に引かれます。封印した予想では q1 を「{PC['q1.pilot']}」とし（当たりました）、引かれている結論の欄に「{PC['info.coi']}」と書きました。登録者は q1 を「{PG['q1.pilot']}」とし、引かれている結論の欄に「{PG['info.coi']}」と書きました。どちらも利害の当事者です。

本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。
'''
out = a.dry or OUT
assert not os.path.exists(out), out
open(out, 'w', encoding='utf-8', newline='\n').write(txt)
print('書いた', out, len(txt), '字', s16(out), '| コミット', head[:7], '| GitHub', remote[:7])
