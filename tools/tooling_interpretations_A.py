# -*- coding: utf-8 -*-
"""tooling_interpretations_A.py v1.1 ——運用の解釈の一覧 records/A/tooling-interpretations-A.md を正本 design/contrasts-A.json から組み立てる（2026-09-14・凍結前の最終検分の採否表 P106・P140・登録者裁定 D26）。
各項の文言は正本の該当キーからの逐語転記。「なぜ要ったか」「採らなかった案」「向き（§0-1 の引かれる向きとの関係・コーディネータの読み）」は本器に置く（一覧の再現のため公開する）。
v2.3〜v2.4 の一覧は一時置き場の一回きりの器で組み立てていた。本器はその文言を引き継ぎ、向きの一行（採否表 P140）と追補の二項（calibration.claim_release・judge_validity.extract.echo・登録者裁定 D26）を足す。
用法: python tools/tooling_interpretations_A.py [--out records/A/tooling-interpretations-A.md]
柵: 本器の出力のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1.1'   # v1.1（2026-09-15・登録者裁定 D38〜D40 の器材化）: 判定器の妥当性の運びの追補六項の「なぜ要ったか」「採らなかった案」「向き」と COI の一行
SAME = '§0-1 (a) の引かれる向き（傾向が立ってほしい）と同じ側（保留や降格が減り、確証が増えうる）'
OPP = '§0-1 (a) の引かれる向きと逆の側（判定不能や規模の除外が増え、確証が減りうる）'
MEAS = '§0-1 (a) の引かれる向きと同じ側（測れた効果種が減り、規模非依存の読みに届きにくい）'
NOLABEL = '札に効かない（注・記録・手順の側）'
UNDET = '札への向きは決まらない（登録の値や本物の出力で動く）'
WHY = {
    'gate2.unit_rule': ('登録の文言は「残る場面」の数え方（対比ごとか、場面の和か）を決めていなかった。', '場面の規模の和で数える（どれか一つの対比が残る規模を場面の規模に数える）案。対比の残存規模で傾きを当てはめる判定不能の規則と同じ単位にそろえるため、対比ごとの案を採った。', OPP),
    'unmeasurable.applied_on': ('測定不能をパイロットで決めるか本走行で決めるかが決まっていなかった（機種の適格の行はパイロット、測定不能の節は走行を定めない）。', 'パイロットで決めて本走行に持ち越す案。集計する試行そのものの測定可能性で外すほうが、外した点と残した点の食い違いが少ないため、本走行の案を採った。', UNDET),
    'unmeasurable.model_rule': ('「機種の適格」を、機種を本走行から外す規則と読む余地があったが、外す条件は登録されていない。', '機種の全セルが測定不能なら外す案（新しい規則を足すことになる）。規則を足さない読みを採った。', UNDET),
    'calibration.timing': ('「当該セッションを新 seed で一度だけ再走」の単位と時機が決まっていなかった。', 'セッションの最後に校正腕を走らせ、外れたらそのセッションの機種の走行を新 seed で丸ごと再走する案（費用が倍になりうる・再走の seed の規則が要る）。最初に走らせて外れたら機種の走行に進まない案は、機種の走行を無駄にせず、セッション番号で seed が変わるため、こちらを採った。', NOLABEL),
    'calibration.series_rule': ('不合格枝で、橋のセッションとやり直しのセッションが系列のどこに入るかが決まっていなかった。', '—', NOLABEL),
    'calibration.withdrawal.cell': ('パイロットに校正腕を置くかどうかと、撤退条件を判定するセルが決まっていなかった。', 'パイロットの各セッションに校正腕を置く案（費用の見積りに含まれていない）。見積りに合わせ、パイロットの 4B-2507 の Ncold × N1 のセルで判定する案を採った。', NOLABEL),
    'calibration.withdrawal.rerun': ('撤退条件が外れた後の再走の seed と、器の異常を記帳したときに注を付す札の範囲が決まっていなかった。', '—', NOLABEL),
    'anchor_band.compare': ('錨帯で比べる二つの率（本走行と二走行目）と、二腕のどちらかが外れたときの扱いが文言になっていなかった。', '—', OPP),
    'runner.extra_body_applies_to': ('非思考モードの指定を思考モードを持たない 4B-2507 にも併合するかが決まっていなかった。門0 と API の既測は併合なし。', '全機種に併合する案（テンプレートは未使用の変数を無視する見込みだが、門0.5 の比較の条件が門0 と API からずれる）。', UNDET),
    'reading_selection.measurable_effect_type.details': ('測れた効果種の計算で、実測で外した規模と 4B の点が外れた対比の扱いが決まっていなかった。', '外した規模を戻して六規模で計算する案（測れる見込みを実際より高く見せ、選択規則を適用する側に引く）。外すほうを採った。', MEAS),
    'descriptive_families.A_desc_critical_size.rule': ('臨界規模の「符号が変わる」の基準と零の扱いが決まっていなかった。', '—', NOLABEL),
    'descriptive_families.A_desc_floor.unmeasurable': ('床持続の記述で、測定不能のセルの扱いが決まっていなかった。', '—', NOLABEL),
    'style_gate.stratified': ('様式門の文言にある「層別（散文層）の再検定を副次終点として先置」の、層のセルの下限と印字の形が決まっていなかった。', '段階 M の下限を借りる案（正本 A に無い数を足すことになる）。A の正本にある refuse 門の答えた分母の下限を参照する案を採った。', NOLABEL),
    'sessions': ('セッション記録の置き場と欄、環境値の取り方（走行器の manifest には環境値の欄が無い）、中断で走行キーが二つのセッションにまたがるときの扱いが決まっていなかった。', '—', UNDET),
    'response_mode': ('応答様式 (a)(b) の語彙・分母・最終試行か初回試行か、言及の語彙の出所が A の正本に無かった。', '—', UNDET),
    'sample_inspection': ('抽出検査の枠・件数・seed が A の正本に無かった。', '段階 M のように腕あたり二件にする案（本走行で九百を超える件数になり目視に向かない）。', NOLABEL),
    'judge_validity.extract': ('判定器の断片の抽出の seed・伏せる欄・鍵の封じ方・判定者のラベルの形が決まっていなかった。凍結パーサの破局の定義は選択肢の記号だけでは決まらない（核の escalation・奪取量）。', '判定者に破局か否かだけを付けてもらう案（判定者に定義を渡すことになり、機械と同じ定義を当てる検査にならない）。', NOLABEL),
    'integrity_check': ('整合検査の項目が A の正本に無かった（段階 M の器の項目を A の相に合わせた）。', '—', NOLABEL),
    'seeds.rerun_offset': ('撤退条件の再走の seed の規則が無かった。', '—', NOLABEL),
    'seeds.sample_inspection': ('抽出検査の seed が無かった。', '—', NOLABEL),
    'seeds.judge_extract': ('判定器の断片の抽出の seed が無かった。', '—', NOLABEL),
    'api_rerun': ('門0.5 に合格したときの API 再走行の事業者と要求の設定が決まっていなかった。', '—', NOLABEL),
    'report_rules.machine_block': ('報告の走査器が「起草者が打ち込んだ数」を見分ける印が決まっていなかった。', '—', NOLABEL),
    'calibration.incomplete_rule': ('校正腕の件数（n_ok）が calibration.n に満たないとき（api_error が残るとき）の扱いが決まっていなかった（実装検分の所見 F2・F-18）。', '件数が足りなくても判定する案（帯の判定の帰無発火率と検出が登録の n の値と変わる）。判定せずに次のセッション番号で走らせ直す案を採った（採否表 P77・P91・登録者裁定 D26 で確認）。', NOLABEL),
    'sessions.commit_rule': ('走行を起こすコミットの固定の要否が決まっていなかった（実装検分の所見 F-14 (f)・採否表 P82 は本走行の相を挙げた）。', '本走行の相だけに固定を求める案。門2 と撤退条件の判定を決めるパイロットもデータを作る相なので、データを作るすべての相に広げた（門0.5 と dry-run は main を許す・登録者裁定 D26 で確認）。', NOLABEL),
    'style_gate.applies_sizes': ('様式門を当てる規模（全規模か、対比の残存規模か）が決まっていなかった（実装検分の所見 F-33）。', '全規模に当てる案（検閲や除外で外した規模の様式差で札を保留することになる）。札を決める規模にそろえ、残存規模の案を採った（登録者裁定 D25）。', SAME),
    'families.A_slope.interpretation_clause.count_after': ('解釈条項の飽和を数える規模（検閲の後か、測定不能と錨帯の除外の後か）が決まっていなかった（実装検分の所見 F-33）。', '検閲の後の規模で数える案（除外した規模の飽和で記述に回すことになる）。傾きを当てはめる規模にそろえた（登録者裁定 D25）。', SAME),
    'families.A_slope.refuse_gate.denominator_detail': ('refuse 門の (c) の refuse 率の分母と、refuse の数え方（答えの JSON の refuse か、散文の拒否も含むか）が決まっていなかった（実装検分の所見 F-33）。', '散文の拒否も refuse に数える案（書式外と refuse の区別が走行器の分類の細目に依存する）。答えの JSON の choice に限った（登録者裁定 D25）。', SAME),
    'calibration.claim_release': ('不合格枝で初点を名乗った機種を走らせられない事情が出たときの、名乗りの移し替えの手順が、器の説明文と反映の記録にだけあり、正本に無かった（凍結前の最終検分の Cl3 中8・採否表 P144）。', '発生したときに逸脱台帳に書く案（手順が走らせる前に登録されない）。正本に置く案を採った（登録者裁定 D26）。', NOLABEL),
    'judge_validity.extract.echo': ('判定器の断片で、応答の本文が前置きを復唱すると腕が推測されうることが器の説明文の限界にだけ書かれ、測る手順が無かった（凍結前の最終検分の Ge2 軽3・採否表 P141）。', '断片から復唱の部分を除く案（判定者に渡す本文を変え、機械と同じ定義を当てる検査にならない）。本文は変えずに一致字数を測って記述する案を採った（登録者裁定 D26）。', NOLABEL),
    'judge_validity.files.balance': ('登録者裁定 D38 で最小のファイル数は決まるが、その数のもとでの区切りの位置は一通りに決まらない。', '前から上限まで詰める案（前の数本が上限に近くなり、後ろのファイルだけが小さくなる。読み込みの失敗は上限に近いファイルで起きやすい）。', NOLABEL),
    'judge_validity.files.fallback': ('登録者の手元の系統が上限の大きさのファイルを読み込めない場合の手が決まっていなかった（登録者の言葉は「その都度、新規のGemini,Grokに追加で依頼する」）。', '読み込めなかったときに登録者が裁定して上限を決め直す案（判定の途中で区切りの規則を決めることになる）。上限を半分にした区切りを同じ規則で機械が作る案を採った。', NOLABEL),
    'judge_validity.attachment.request': ('添付ファイルに置く依頼文の文言（読み取る欄・答えが変わる場合・回答の指示の形の外の本文・判定不能）が決まっていなかった。', 'v2.1 の断片の MD をそのまま送る案（見出しに「機種と腕と機械判定は伏せる」と書いており、研究の組み立てを判定者に伝える）。', NOLABEL),
    'judge_validity.attachment.reply': ('判定者の書き出しの形と、登録者が送る文が決まっていなかった。v2.1 のラベルの形は一つの塊の JSON で、一件あたりの字数が大きく、何回かに分けて受け取るときの境が決まらない。', 'v2.1 の JSON の形のまま受け取る案（二千件を超える書き出しが一回の返信に収まりにくく、分けたときに塊が壊れやすい）。', NOLABEL),
    'judge_validity.attachment.merge': ('貼られた返信からラベルを読み取る規則（やり直しの区切り・同じ番号の重なり・範囲の外の番号・形の崩れ・大文字と全角）が決まっていなかった。', '同じ番号の読みが食い違えば形の不備に数える案（続きの返信で重ねて書いた行を落とし、対が減る）。後の行を採り、食い違いの件数を印字する案を採った。', NOLABEL),
    'judge_validity.position.measures': ('登録者裁定 D39 は「位置ごとに機械の判定との一致を記述する」で、一致の量と位置の区分の細目が決まっていなかった。', '位置ごとに κ を出す案（位置ごとの対の数が少なく、基底率の違いで値が大きく揺れる）。', NOLABEL),
}


def get(T, path):
    v = T
    for seg in path.split('.'):
        v = v[seg]
    return v


def build(T):
    TI = T['tooling_interpretations']; missing = [k for k in TI['items'] if k not in WHY]
    assert not missing, ('運用の解釈の項に「なぜ要ったか」が無い', missing)
    same = [k for k in TI['items'] if WHY[k][2] == SAME]; meas = [k for k in TI['items'] if WHY[k][2] == MEAS]
    out = ['# 器材の整備で確定した運用の解釈（登録者の確認待ち・2026-09-13・登録者裁定 D9 の三つ目の手順・追補と文言の直し 2026-09-14・登録者裁定 D16〜D25・D26・追補 2026-09-15・登録者裁定 D38〜D40 の器材化）', '',
           '- 性格: 登録済みの文言が決めていなかった運用を、器材を一義に動かすために正本 `design/contrasts-A.json`（SHA16 %s）に書き足した。各項の文言は正本の該当キーからの逐語転記（`tools/tooling_interpretations_A.py` %s が組み立てる）。' % (runs_A.sha16_file(runs_A.CPATH), VERSION),
           '- 変えていないもの: 確証の規則・札の定義・閾値・帯の値は変えていない。札の入力を決める運用の読み（門2 の数え方・測定不能の走行・錨帯の比べ方・環境値）を含む（採否表 P103 で文言を改めた）。',
           '- 状態: %s' % TI['status'],
           '- 読み方: 「なぜ要ったか」は登録の文言の欠け、「採らなかった案」はコーディネータが比べた別の読み（無ければ —）、「向き」は選んだ読みが §0-1 の引かれる向きのどちら側に効くかのコーディネータの読み（採否表 P140）。確認は凍結確認の直前に受け、変える場合は正本と草案と器材と合成検査を作り直す。', '']
    for i, k in enumerate(TI['items'], 1):
        v = get(T, k); why, alt, pull = WHY[k]
        body = ('（値は正本の該当キーを見る・seed は設計定数の数の検査の対象外）' if k.startswith('seeds.') else (json.dumps(v, ensure_ascii=False, indent=1) if isinstance(v, (dict, list)) else str(v)))
        out += ['## %s. `%s`' % (i, k), '', '- なぜ要ったか: %s' % why, '- 採らなかった案: %s' % alt, '- 向き: %s' % pull, '- 正本の文言:', '', '```text', body, '```', '']
    out += ['## COI（事実のみ）', '', '- 引かれる向き: 器材を早く凍結に回したい（解釈を自分で決めて済ませたい）。置いた印: 解釈を正本の一か所（tooling_interpretations）に集め、確認を仰ぐ一覧にした。',
            '- 器材の試走で門0 の既存のデータ（4B-2507 × N1）の腕別の (b) 率と層ごとの破局数が目に入った。閾値と帯は動かしていない。',
            '- 実装検分の反映（2026-09-14）で追補した項のうち、sessions.commit_rule は採否表 P82 の本走行の相を、データを作るすべての相に広げた。calibration.incomplete_rule は採否表 P77・P91 の器材の直しを正本の文言にした。どちらも登録者裁定 D26（2026-09-14）で確認を受けた。',
            '- %s は、いずれも §0-1 (a) の引かれる向きと同じ側（保留や降格が減る）に効く（凍結前の最終検分の Cl1 軽1・Cl2 中7・採否表 P140）。%s も同じ側（測れた効果種が減り、規模非依存の読みに届きにくい・コーディネータの読み）に効く。値は変えていない。' % ('・'.join(same), '・'.join(meas)),
            '- 登録者裁定 D26（2026-09-14）で calibration.claim_release と judge_validity.extract.echo を追補した。一覧の全項の確認は、反映の後の版で凍結確認の直前に受ける。',
            '- 追補（2026-09-15）の六項（judge_validity.files.balance・files.fallback・attachment.request・attachment.reply・attachment.merge・position.measures）は、登録者裁定 D38〜D40 を器材に移すときにコーディネータが決めた細目で、札に効かない（判定器の妥当性は記述）。'
            '登録者の「盲検を複雑にしない」という依頼に合わせて手順を簡単に見せたい向きがあるので、手順書に登録者の操作の数（判定者 × ファイルの会話の数・続きの送信・貼り付け）を書いた。', '',
            '本文書のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
    return '\n'.join(out) + '\n', len(TI['items'])


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'tooling-interpretations-A.md')); ap.add_argument('--contrasts', default=None)
    a = ap.parse_args(); T = runs_A.load_T(a.contrasts); text, n = build(T)
    open(a.out, 'w', encoding='utf-8', newline='\n').write(text)
    print('[tooling_interpretations_A %s] written %s（%d 項・SHA16 %s）' % (VERSION, a.out, n, runs_A.sha16_file(a.out)))
