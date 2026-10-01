# -*- coding: utf-8 -*-
"""make_results_request_Bprime.py v0（2026-10-01・B′ の結果の巡の依頼の文を組む・層三の `records/reviews/Bl3/results-round1/request-results-Bl3.md` の型・コーディネータ南無弥勒如来）。
数・SHA・コミット・時刻は記録から機械で入れる（打ち直さない）。書く物: `request-results-Bprime.md`（一度だけ・既にあれば止める）。
柵: 本依頼のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, sys, json, hashlib, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
OUT = os.path.join(HERE, 'request-results-Bprime.md')
P = lambda *a: os.path.join(PUB, *a)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
ld = lambda p: json.load(open(p, encoding='utf-8'))
JST = datetime.timezone(datetime.timedelta(hours=9))
head = subprocess.run(['git', '-C', PUB, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
remote = subprocess.run(['git', '-C', PUB, 'rev-parse', 'origin/main'], capture_output=True, text=True).stdout.strip()
assert head == remote, '公開の置き場の手元と GitHub が違う'
FR = ld(P('records', 'Bprime', 'FREEZE-RECORD-Bprime.json'))
SR = ld(P('records', 'Bprime', 'sealing-record-Bprime.json'))
PJ = ld(P('records', 'Bprime', 'pilot', 'pilot-Bprime.json'))
T = ld(P('design', 'contrasts-Bprime.json'))
CR = ld(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'))
PG = ld(P('records', 'predictions', 'predictions-Bprime-registrant.json'))
PC = ld(P('records', 'predictions', 'predictions-Bprime-coordinator.json'))
D = PJ['decision']
passed = [k for k, v in PJ['cells'].items() if v['pass_i_ii']]
floor_c = [k for k, v in PJ['cells'].items() if not v['pass_i_ii'] and v['pa'] < T['pilot']['p_bounds'][0]]
ceil_c = [k for k, v in PJ['cells'].items() if not v['pass_i_ii'] and v['pa'] > T['pilot']['p_bounds'][1]]
assert sorted(floor_c + ceil_c) == sorted(D['dropped'])
limit_line = 'Gemma の場面の出力と読み取りの値はまだ誰も見ていない'
rep = open(P('records', 'Bprime', 'results-Bprime.md'), encoding='utf-8').read()
assert limit_line in rep
keys = [it['key'] for it in T['predictions']['items']]
nv1, nv2, nv3 = (sum(1 for v in PJ['iv'][x]['flags'].values() if v) for x in ('V1', 'V2', 'V3'))
nmain = len(PJ['cells'])
txt = f'''# B′ の結果の報告の草案の検分のお願い（結果の巡）

- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／{datetime.datetime.now(JST).strftime('%Y-%m-%d')}。
- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束はコミット {head[:7]} の時点で組みました）。
- **初めての方へ**: あなたは、この登録（B′）の検分に初めて加わる新しい個体です（正本 `review_plan.results.fresh`）。設計の巡と器の検分の票は公開の置き場の `records/reviews/Bprime/` にありますが、読まなくて構いません。束の中だけで検分できるように組みました。
- **この登録の問い**: Gemma-4-31B-it（`google/gemma-4-31B-it`）で、層三（B-lens 層三・Qwen3-4B-Instruct-2507 の公開の登録）と同じ型の直答の読み取りを立て、選んだ層で足した方向（v̂ と Nk）の全経路を通った後の効き目が、等方のランダム方向と実在の差の方向とに比べてどう出るかを、日本語の場面で記述する。下見で読み取りが測れないと分かったときは、凍結した決まりで止める。
- **経緯**: 下見の前の凍結（{FR['frozen_jst']} 日本時間・`design/design-Bprime-FROZEN.md`・凍結物 {len(FR['frozen_sha16'])}）の後に、予想を封印し（コーディネータが先・SHA だけを伝える順・封印 {SR['sealed_at_jst']}）、Colab の G4（NVIDIA RTX PRO 6000 Blackwell Server Edition）で、相 extract（方向の抽出）・行動の下見（無操作・{CR['digests']['n_trials']} 試行の生成と凍結の採点・系統外の模型 grok-4.7 による 40 件の採点）・読み取りの下見（無操作だけ・模型を読み込み直した新しいランタイム）を走らせました。
- **読み取りの下見の機械の決定は「{D['q1']}」**でした（理由 (i)(ii)・満たした主の升目 {D['n_pass']}／{D['n_main']}・続けるには `pilot.decision.cells_min_pass` 以上が要る）。床の外 {'・'.join(floor_c)}、天井の外 {'・'.join(ceil_c)}、満たした升目 {'・'.join(passed)}。器の誤りはなく、凍結した決まり（凍結の本文 §4.5）のとおり「この読み取りでは測れなかった」と記録して閉じる道に入りました。本の計算・独立の再計算・一致だけを見る段・結果を開く段は走らせていません。
- その後、登録者の言葉（{FR['main_freeze']['frozen_jst']} 日本時間）で、本の凍結の器が読み取りの下見の記録と機械の決定を凍結の記録に足し（器の差分 {len(FR['main_freeze']['tool_diffs_applied'])}・錠の外れ {len(FR['main_freeze']['lock']['bad'])}・凍結した決定木で出し直した決定は記録の決定と一致）、集計の器の段 stopped と報告の組み立ての器で、報告の草案（`records/Bprime/results-Bprime.md`・SHA16 {s16(P('records', 'Bprime', 'results-Bprime.md'))}・自由の文の走査の当たり 0）を組みました。凍結の後の逸脱は {len(FR.get('deviations') or [])} です。
- **結果は公開済みで、伏せていません。** 検算は歓迎します（読み取りの下見の記録 `records/Bprime/pilot/pilot-Bprime.json`〔SHA16 {s16(P('records', 'Bprime', 'pilot', 'pilot-Bprime.json'))}〕・行動の下見の閉じた記録 `records/Bprime/behavior/behavior-closed-Bprime.json`〔SHA16 {s16(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'))}〕・集計の出力 `records/Bprime/analysis-Bprime.json`〔SHA16 {s16(P('records', 'Bprime', 'analysis-Bprime.json'))}〕・凍結の記録 `records/Bprime/FREEZE-RECORD-Bprime.json`〔SHA16 {s16(P('records', 'Bprime', 'FREEZE-RECORD-Bprime.json'))}〕）。検算に要る分は束の第三部に機械で写しました。
- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）と機種を書いてください。claude.ai の Claude は起草者と同じ系列で、何票でも一票に数えます。
- **この巡の後**: 採否と裁定・報告の直し・最終の系統外の一票（「最終」と明記）・起草者の最終の見直し・登録者最終確認と公開の順で、ほかに巡は置きません（正本 `review_plan`）。
- **起草者が下見の決定の後に見つけたこと**（所見に挙げて構いません・挙げなくても構いません）:
  - 報告の §10（限界）の「…{limit_line}」は、正本の封印の前の文が機械の区画にそのまま出たもので、下見の後の報告では事実と合いません。凍結した器の出力なので、直すなら逸脱になります（まだ直していません）。
  - 報告の §6（行動の下見）の表と §1（読み取りの下見）の表は、同じ升目の並びで、行動の下見の率と、無操作の読み取りの選択肢 a の確率が、どちらも升目の族（survival と nuclear）で両端に分かれています。報告はどちらにも読みを付けていません（読み取りの値を行動の率の代わりに読まない決まり・二つの機種の安全さの比べにしない決まり・採点器の妥当性は Gemma の応答で確かめていない）。
  - 揺れの版（§1 の (iv)）で、主の書き出しとの差が `pilot.variant_flag` を超えて印が付いた升目は、V1 {nv1}／{nmain}・V2 {nv2}／{nmain}・V3 {nv3}／{nmain} でした。報告は写しの働きの有無を読みません（決まり）。
  - 系統外の模型による採点は grok-4.7 で、この巡の系統外の検分者と同じ機種です（報告 §10 の限界の文）。採点の束（Gemma の応答 40 件・升目を伏せた形）と grok の返事は、まだ公開していません（結果の段で公開する予定・登録者の了承）。
  - 起草者の欄（この結果が退けた説明）の三行は、値を書かず、なぜその位置に出たかの読みも入れていません（自由の文の走査は、測った値の数と比べの語を止めます）。
- **束の中身**: 第一部 依頼文／第二部 報告の草案（全文）と起草者の欄の元の文／第三部 止めた記録の機械の写し（読み取りの下見の記録・行動の下見の閉じた記録の md・集計の出力の要点・凍結の記録の本の凍結の節・走行の表・封印の記録と二つの予想・露出の記録・G4 の試みの記録）／第四部 凍結の本文（全文）／第五部 正本（全文）／第六部 凍結の後の記録（全体の台帳の B′ の行・下見の前の凍結の走らせた所の記録・器の段の記録の凍結の後の行）。
- **褒めるのではなく、公開の前に報告を崩すつもりで読んでください。** とくに、止めた下見の記述が、直答の型の読み取りの位置の外（意味・機構・行動の原因・機種の性質）へ出ていないか、「測れなかった」を弱めたり強めたりしていないかを見てください。

## 1. 伺いたいこと

1. **下見の決定の当否**: 凍結した決まり（正本 `pilot`・凍結の本文 §4.2・§4.5）を下見の記録の数（第三部）に当てると、機械の決定（{D['q1']}・理由 (i)(ii)・満たした升目 {D['n_pass']}／{D['n_main']}）と、(vi) の分岐（バッチの大きさ {PJ['batch']}）が出るか。決まりの読み違い・升目の取り違え・境目の扱いの誤りはないか。値の見え方から器の誤りを疑う所があれば、その根拠を書いてください（決まりでは、凍結した確かめが落ちたものだけを器の誤りに数え、疑いは登録者に上げます）。
2. **報告の機械の区画**: 止めたときの文（「この読み取りでは測れなかった（閾値は…）。B′ の問いには答えていない」）・nuclear の族の文・(iii) の「定まらなかった」の文・揺れの版の並べ方・行動の下見の表・予想の照合の表は、凍結した読みの決まり（凍結の本文 §9・正本 `reading_rules`・`print_strings`）と記録の数に照らして正しいか。止めた報告に要らない区画や、足りない区画はないか。
3. **起草者の欄（この結果が退けた説明）**: 三行は、記録と凍結した決まりから支えられるか。「退けられた」は強すぎないか。ほかに、この結果が退けた説明や、退けていないのに退けたように読める所はあるか。
4. **古くなった限界の文**（上の「見つけたこと」の一つ目）: 器を直す逸脱にするか・報告の機械の区画の外に注を足すか・記録に置けば足りるか。
5. **行動の下見の記述**: 表と限界の文は、読みの決まりのとおり記述にとどまっているか。足りない限界の文（例: 読み取りは量を読まないこと・採点器の妥当性・標本化が段階 B の値であること）はないか。
6. **手続き**: 凍結・封印・相 extract・行動の下見と閉じる段・読み取りの下見・止めたときの本の凍結・集計・報告の記録と順は足りているか。記録されていない変更や露出は見つかるか（G4 の試みの記録・起動の記録と出力の SHA の記録・push の順を含む）。
7. **公開の扱い**: 結果の段でまだ公開していないもの（系統外の採点の束と返事・行動の下見の生成の全文・走らせた置き場の進みの記録など）のうち、公開すべきもの・公開しない方がよいもの・公開するときに添えるべき注はあるか。
8. **予想の照合**: 照合の表（q1 だけを採点し、q2〜q4 は採点しない）に誤りや誤解を招く所はないか。照合は記録であり評価ではない、という書き方で足りるか。
9. **総合**: 公開に進めるか（公開可／条件つき可／差し戻し）。**公開の前に直すもの**と、**記録に置けば足りるもの**に分けてください。

## 2. お願い

- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。
- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。
- 止める決まり・閾値・読み取りの式を変える提案は、この登録には入りません（値を見た後の変更はこの登録を閉じる逸脱です）。別の登録の候補として扱います。
- 起草者は器と報告の組み立ての器と起草者の欄を書いた当人で「正しく読めている」と書く側にあり、封印した予想では q1 を「{PC['q1.pilot']}」とし（当たりました）、引かれている結論の欄に「{PC['info.coi']}」と書きました。登録者は q1 を「{PG['q1.pilot']}」とし、引かれている結論の欄に「{PG['info.coi']}」と書きました。どちらも利害の当事者です。

本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。
'''
assert not os.path.exists(OUT), OUT
open(OUT, 'w', encoding='utf-8', newline='\n').write(txt)
print('書いた', os.path.basename(OUT), len(txt), '字', s16(OUT))
