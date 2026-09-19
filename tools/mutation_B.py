# -*- coding: utf-8 -*-
"""mutation_B.py v8 —— **自己検査が、直す前の誤りを入れ直したときに落ちるか**を確かめる（正本 `selftest_rule`・裁定 D122）。
v8（2026-09-20・凍結の前の方向の抽出の準備・独立の目を通っていない）: 方向の抽出器 v7 の二つの型を足した（決定性 (i) の不一致で止めない・腕ごとのトークン長で場面を落とす）。
v7（2026-09-19 の夜・封印の後・結果の前・独立の目を通っていない）: 予想の照合の器（`compare_predictions_B`）の写し方と照らしを外す型を五つ足した（非有意の写し方・逆向きの確証の向き・帯の境目・集計と門の記録の照合・予想しないの数え方）。
v6（2026-09-19 の夜・封印の後・独立の目を通っていない）: 封印した予想の照合（`seal_B.check_predictions`）の五つの検査を外す型を足した（出所の SHA・向き・封印の経緯の記録の SHA・予想者・様式の名）。
v5（2026-09-19 の後刻）: 腕の本文の末尾の改行を残して読む誤り（走行器 v6 まで実際にこうだった・O・Osec・Onull で前置きと場面の本文の間の改行が一つ多かった）を足した。
v4（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: 最後の巡の所見を入れ直した型を足した——td の特異性の向きを見ない（裁定 D133）・S4 の門を外す（D134）・S4 の封印の照合をしない（D135）・品質床の境目を合格に数える（D137）・ランダム方向を塊に戻す（D140）・様式門の札を保留に戻す（採否表 P401）・層の添字の照合を外す（P393）・相手の重複の番人を外す（P403）。帯の起点の変異は起点の関数（P404）に当て直した。

系統の外への検分で、**差し戻しの原因そのものに戻しても両方の自己検査が「すべて通った」と印字する**ことが分かった。
「検査が通った」を品質の証拠にしないために、**検査そのものを検査する**器を置く。

やり方: 器材を一時置き場に丸ごと写し、**一件ずつ誤りを入れ直して**自己検査を走らせ、**落ちることを確かめる**。
        落ちなければ、その検査は守りになっていない（終了コード非零で止まる）。
出力: records/B/mutation-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/mutation_B.py [--force] [--list]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, argparse, subprocess, tempfile, datetime

VERSION = 'v8'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

# (名, 直した裁定, どの器の何を戻すか, 置換〔前 → 後〕, 落ちてほしい自己検査)
MUTATIONS = [
    ('全方向のノルム合わせ', 'D102', 'direction_B.py',
     ("            if name != 'static':", "            if name == 'td':"),
     ['direction_B.py'],
     '方向を作る器が td にしか合わせない誤り（交差族と S4 の反証に「加わる量が腕と統制で違う」構図が残る）。'
     '**守るのは方向を作る器である**——介入の器（steer_B）は自分で合わせた模造ベクトルしか見られないので、'
     'ここは守れない。走行器が npz を読むときにノルムを確かめる検査は、**本体を書くときに足す**（裁定 D117）'),
    ('帯の起点（主位置）', 'D124', 'steer_B.py',
     ('    return int(pad_len) + len(ids) - 1', '    return int(pad_len) + 0'),
     ['steer_B.py'],
     '起点が列の先頭になる誤り（帯が役割トークンから掛かる）。**起点の式は `main_position` 一つ**で、走行器もこれを呼ぶ（採否表 P404）'),
    ('係数の掛け方', 'D90', 'steer_B.py',
     ('        out.append(g * (target / n) if n else g)', '        out.append(g * (target / n) * 2.0 if n else g)'),
     ['steer_B.py'],
     'ランダム方向のノルムが v̂ と違う誤り（加わる量が腕と統制で違う）'),
    ('バッチの腕の同質性', 'D124', 'steer_B.py',
     ("    if len(set(arm_texts)) > 1:", "    if False:"),
     ['steer_B.py'],
     'バッチに複数の腕が混ざっても止めない誤り'),
    ('層番号の四捨五入', 'D4', 'direction_B.py',
     ('int(math.floor(ratio * n_layers + 0.5)) - 1', 'int(math.floor(ratio * n_layers)) - 1'),
     ['direction_B.py'],
     '層の添字が一つずれる誤り'),
    # ---- 方向の抽出器 v7（2026-09-20・凍結の前の方向の抽出の準備） ----
    ('決定性 (i) の不一致で止めない', 'D91', 'direction_B.py',
     ('    if not ok_same:', '    if False:'),
     ['direction_B.py'],
     '同じ並べ方で二度取った活性が一致しなくても、方向を作って凍結へ進む誤り（登録は止めて登録者に上げる）'),
    ('腕ごとのトークン長で場面を落とす', 'D82', 'direction_B.py',
     ("for sc in scenarios}}", "for sc in scenarios[:1]}}"),
     ['direction_B.py'],
     '凍結時に記帳するトークン長が一つの場面の分しか無い誤り（正本 position_length.record_at_freeze・主位置の位置は場面ごとに違う）'),
    # ---- 直しの監査（2026-09-19）で器に入れた規則 ----
    ('S4 の片側上限を狭める', 'D118', 'rules_B.py',
     ('    one = newcombe(kB, nB, kA, nA, 0.90)', '    one = newcombe(kB, nB, kA, nA, 0.50)'),
     ['rules_B.py'],
     '「効き目以上の低下は否定」の札が出やすくなる誤り（反証が当たりやすい側・起草者の引力と同じ側）'),
    ('区間を Wald に戻す', 'D130', 'rules_B.py',
     ('    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)', '    lo = d - _z(conf) * math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)'),
     ['rules_B.py'],
     '床の近くで被覆が崩れる区間に戻る誤り'),
    ('等質性の境目を注に数える', 'D127', 'rules_B.py',
     ("    return {'note': bool(spread > thr),", "    return {'note': bool(spread >= thr),"),
     ['rules_B.py'],
     '境目ちょうどに注を付ける誤り（正本は「超えたら」）'),
    ('同方向の判定を大小の一致に戻す', 'D130', 'rules_B.py',
     ('    return d1 is not None and d2 is not None and (d1 * d2) > 0', '    return d1 is not None and d2 is not None and (d2 > 0) == (d1 > 0)'),
     ['rules_B.py'],
     '差が零のとき、偽どうしで同方向と誤判定する誤り（系統外の検分で捕まった型）'),
    ('読めた分母から書式外を除かない', 'D127', 'rules_B.py',
     ("('readable', lambda c: c['n_ok'] - c['refuse'] - c['ff'])", "('readable', lambda c: c['n_ok'] - c['refuse'])"),
     ['rules_B.py'],
     '書式外による希釈が refuse 門をすり抜ける誤り'),
    ('api_error の門を外す', 'D127', 'rules_B.py',
     ('    return bool(d > thr + 1e-12)', '    return False'),
     ['rules_B.py'],
     '差のある欠測を品質床の門で止めない誤り'),
    ('行ごとの方向を一本にする', 'D117', 'run_stageB_local.py',
     ('                hs[i, int(st):, :] = hs[i, int(st):, :] + (add[i] if per_row else add)',
      '                hs[i, int(st):, :] = hs[i, int(st):, :] + (add[0] if per_row else add)'),
     ['run_stageB_local.py'],
     'ランダム方向の腕のすべての行に同じ方向が掛かる誤り'),
    ('様式の欄を空で書く', 'D117', 'run_stageB_local.py',
     ("            'style_a': bool(mf['a']), 'style_b': bool(mf['b']), 'mention': bool(mf['c1']),",
      "            'style_a': None, 'style_b': None, 'mention': None,"),
     ['run_stageB_local.py'],
     '様式門が実データで黙って効かない誤り（走行器 v4 まで実際にこうだった）'),
    # ---- 最後の系統外の巡の所見を入れ直した型（2026-09-19・v4） ----
    ('td の特異性の向きを見ない', 'D133', 'rules_B.py',
     ("        elif same_direction(cd, r['diff_pt']):", "        elif True:"),
     ['rules_B.py'],
     'td のほうが動いた組でも「書ける」になる誤り（前の規則の型・特異性を書ける側・起草者の引力と同じ側）'),
    ('S4 の書式外の門を外す', 'D134', 'rules_B.py',
     ("            fire('希釈の門（書式外の差）')", "            pass"),
     ['rules_B.py'],
     '書式外が片腕だけ増えても、S4 が三分岐に進む誤り（反証の結果が分母で逆になりうる）'),
    ('S4 の封印の照合をしない', 'D135', 'rules_B.py',
     ("    return table[seal_value].get(outcome, '言えない')", "    return '言えない'"),
     ['rules_B.py'],
     '封印の値を読まずに照合を出す誤り（前は札の文言に当否を固定で入れていた）'),
    ('品質床の境目を合格に数える', 'D137', 'rules_B.py',
     ("    return int(math.ceil(abs(float(T['quality_floor']['threshold_pt'])) / 100.0 * n - 1e-9))",
      "    return int(math.ceil(abs(float(T['quality_floor']['threshold_pt'])) / 100.0 * n - 1e-9)) + 1"),
     ['rules_B.py'],
     '閾値ちょうどの差を合格に数える誤り（正本は不合格・多重性の数が境目の規則と合わなくなる）'),
    ('様式門の札を保留に戻す', 'P401', 'rules_B.py',
     ("    return '判定保留（様式転位）' if (p is not None and p < nominal) else '非有意'", "    return '判定保留（様式転位）'"),
     ['rules_B.py'],
     '非有意の対比が様式門で保留に化ける誤り（起草者に有利な向き）'),
    ('ランダム方向を塊に戻す', 'D140', 'steer_B.py',
     ("    return int(trial_index) % int(count)",
      "    al = allocate(n_trials, count)\n    acc = 0\n    for i, n in enumerate(al):\n        acc += n\n        if trial_index < acc:\n            return i"),
     ['steer_B.py'],
     '方向が登録順の連続した塊に割られ、バッチ・時刻・セッションと交絡する誤り'),
    ('層の添字の照合を外す', 'P393', 'run_stageB_local.py',
     ("    return int(layer_idx) == direction_B.layer_index(float(layer_ratio), int(n_layers))", "    return True"),
     ['run_stageB_local.py'],
     '層の割合と層の添字が食い違っても走行器が止まらない誤り（記録の層は割合なので、違う層に掛けても記録は正しく見える）'),
    ('腕の本文の末尾の改行を残す', 'D144', 'run_stageB_local.py',
     ("                                  'text': _RD(p)}", "                                  'text': b.decode('utf-8').replace('\\r\\n', '\\n')}"),
     ['run_stageB_local.py'],
     '腕の本文を凍結走行器の rd で読まず、末尾の改行を残す誤り（走行器 v6 まで実際にこうだった——O・Osec・Onull で前置きと場面の本文の間の改行が一つ多く、段階 A と V′ の列と一字違った）'),
    # ---- 品質床の課題の選定（裁定 D145・D146・2026-09-19 の夕刻） ----
    ('記号の読み取りで隣のラテン文字を見ない', 'D146', 'qf_task_B.py',
     ("        if _ASCII_LETTER.fullmatch(prev or '-') or _ASCII_LETTER.fullmatch(nxt or '-'):\n            continue\n", ""),
     ['qf_task_B.py'],
     'DNA の D や AI の A を答えに読む誤り（読めないはずの応答が正答や誤答に化ける）'),
    ('断片の提示の順を並べ直す', 'D146', 'qf_task_B.py',
     ("    return random.Random(int(T['seeds']['quality'])).sample(pool, n)",
      "    return sorted(random.Random(int(T['seeds']['quality'])).sample(pool, n), key=lambda it: it['id'])"),
     ['qf_task_B.py'],
     '提示の順が登録（引いた順）と違う誤り（断片の SHA が登録と合わなくなる）'),
    ('問いの本文の空行を落とす', 'D146', 'qf_task_B.py',
     ("    return inst + '\\n\\n' + '\\n'.join(lines)", "    return inst + '\\n' + '\\n'.join(lines)"),
     ['qf_task_B.py'],
     '課題の指示と問題文の間の空行が無くなり、登録した組み立て（presentation.layout）と違う誤り'),
    ('品質床の記録の生成の設定を渡した鍵だけにする', 'D146', 'run_stageB_local.py',
     ("    return dict(gen, temperature=g0['temperature'], top_p=g0['top_p'])", "    return dict(gen)"),
     ['run_stageB_local.py'],
     '記録に温度と top_p が無く、本物の出力が整合検査で全件「生成の設定が登録と違う」に落ちる誤り（合成データは正本の値を書くので通る型）'),
    ('判定の順を二つの土台の平均で見る', 'D145', 'qf_select_B.py',
     ("        row[k] = {'min_acc': min(accs.values()),", "        row[k] = {'min_acc': sum(accs.values()) / len(accs),"),
     ['qf_select_B.py'],
     '一方の土台が下限に届かなくても平均で (1) に入る誤り（起草者の引力と同じ側）'),
    ('手当ての下限に届かないとき付けない側に戻る', 'D145', 'qf_select_B.py',
     ("    r3 = [k for k in keys if row[k]['min_acc'] >= floor and row[k]['max_ff'] > thr]",
      "    r3 = [k for k in keys if row[k]['min_acc'] < floor or row[k]['max_ff'] > thr]"),
     ['qf_select_B.py'],
     'どの候補も手当ての下限に届かないとき、止まらずに付けない側へ戻って先へ進む誤り（裁定 D145 で止まる側に決めた・起草者の引力の側）'),
    ('予想の書式の向きの欄の鍵から前置きを落とす', 'D148', 'make_predictions_form_B.py',
     ("                pills(F['direction']['key_prefix'] + c['id'], F['direction']['options'], NP, DG, pred=True)))",
      "                pills(c['id'], F['direction']['options'], NP, DG, pred=True)))"),
     ['make_predictions_form_B.py'],
     '予想の JSON の向きの鍵が正本の決まり（b.dir.）と違い、照合の器が対比を引けなくなる誤り'),
    ('予想の書式の封印の JS の置き換えを外す', 'D148', 'make_predictions_form_B.py',
     ("    return js.replace(V5_META, \"form:'%s',program:'%s',contrasts:'%s'\" % (M['form'], M['program'], M['contrasts'])).replace(V5_DL, M['download'])",
      "    return js"),
     ['make_predictions_form_B.py'],
     '封印の JSON が V′ 様式の名と保存の名のまま出る誤り（どの段の予想か JSON から分からなくなる）'),
    # ---- 封印した予想の照合（v6・2026-09-19 の夜・封印の後・凍結の器が呼ぶ `seal_B.check_predictions`） ----
    ('封印の出所の SHA-256 を照らさない', 'D148', 'seal_B.py',
     ("        if src.get('sha256') != info['coordinator']['sha256']:", "        if False:"),
     ['seal_B.py'],
     '封印の後にコーディネータの予想の JSON が書き換わっても、凍結の器が通す誤り'),
    ('封印の向きを予想の JSON と照らさない', 'D148', 'seal_B.py',
     ("        if diff or set(seal.get('signs') or {}) != set(conf):", "        if False:"),
     ['seal_B.py'],
     '起草者の封印の向きがコーディネータの予想の JSON と違っても通す誤り（封印を二重に書いた形・seal_format.from_predictions の違反）'),
    ('封印の経緯の記録の SHA を照らさない', 'D148', 'seal_B.py',
     ("            if s not in txt:", "            if False:"),
     ['seal_B.py'],
     '封印の経緯の記録に載る SHA-256 と現物が違っても通す誤り（封印の後に登録者の予想のファイルが替わっても分からない）'),
    ('予想者の欄を名の役と照らさない', 'D148', 'seal_B.py',
     ("        if v.get(F['who']['key']) != who:", "        if False:"),
     ['seal_B.py'],
     '登録者のファイルにコーディネータの予想が入っていても通す誤り（照合が二人の予想を取り違える）'),
    ('予想の様式の名を照らさない', 'D148', 'seal_B.py',
     ("            if d.get(k) != M[k]:", "            if False:"),
     ['seal_B.py'],
     '別の段・別の版の書式で作った予想の JSON を通す誤り（正本 predictions.compare_rules.validation）'),
    # ---- 予想の照合の器（v7・2026-09-19 の夜・結果の前） ----
    ('非有意を照合不能に写す', 'D148', 'compare_predictions_B.py',
     ("            d[cid] = ('どちらでもない', lab)", "            d[cid] = (None, lab)"),
     ['compare_predictions_B.py'],
     '「どちらでもない」の予想が、非有意の結果でも照合不能に落ちる誤り（正本 compare_rules.direction の違反・当たりも外れも数えられなくなる）'),
    ('逆向きの確証を封印の向きで写す', 'D148', 'compare_predictions_B.py',
     ("            v = inv.get(r.get('sign'))", "            v = inv.get('下')"),
     ['compare_predictions_B.py'],
     '札の向き（集計の記号）を読まず、確証をすべて低下に写す誤り（逆向きに立った確証が、低下と予想した人の的中に化ける）'),
    ('確証の本数の帯の境目を外す', 'D148', 'compare_predictions_B.py',
     ('        if lo <= n <= hi:', '        if lo <= n < hi:'),
     ['compare_predictions_B.py'],
     '帯の上の端の本数（3・8・16 本）が帯に入らない誤り（照合不能に落ちる）'),
    ('照合で集計と門の記録の照合を外す', 'D148', 'compare_predictions_B.py',
     ("        if A.get('gate_sha16') != runs_B.sha16_file(gate_path):", '        if False:'),
     ['compare_predictions_B.py'],
     '別の門の記録から作った集計で照合できてしまう誤り'),
    ('予想しないを照合に数える', 'D148', 'compare_predictions_B.py',
     ("        add('向き', cid, want, got, why, v)", "        add('向き', cid, want, got, why, V_MISS if want == NP else v)"),
     ['compare_predictions_B.py'],
     '「予想しない」の欄を外れに数える誤り（正本 compare_rules.not_predicted の違反）'),
    ('書式外の境目を当たりに数える', 'D145', 'qf_select_B.py',
     ("    t1 = [k for k in keys if row[k]['min_acc'] >= bmin and row[k]['max_ff'] <= thr]",
      "    t1 = [k for k in keys if row[k]['min_acc'] >= bmin and row[k]['max_ff'] < thr]"),
     ['qf_select_B.py'],
     '書式外の率がちょうど閾値の候補を落とす誤り（登録は「超えたら当たる」）'),
    # ---- 採否表の引用の照合（2026-09-19・束の前の点検で手で打った引用の誤りが多数見つかった） ----
    ('引用の裁定の照合を外す', '—', 'citations_B.py',
     ('                if not (ds & rd):', '                if False:'),
     ['citations_B.py'],
     '引用の括弧の裁定と、引いた採否表の行の裁定が食い違っても止めない誤り（直す前の器材に実際に四十件余りあった型）'),
    ('出所の札の照合を外す', '—', 'citations_B.py',
     ('                if not ok(voters):', '                if False:'),
     ['citations_B.py'],
     '系統内の検分が挙げた所見に「系統外の検分」の札を付けても止めない誤り（独立の票の記録が水増しされる側）'),
]

# 合成データを通して確かめる変異（自己検査では見えない・裁定 D122／D125・D126・D121・D119）
# (名, 裁定, 器, 置換, 何が起きてはいけないか, 見る場所)
PIPELINE_MUTATIONS = [
    ('様式門を Holm の順位に戻す', 'D125', 'analyze_B.py',
     ("not (r.get('fired') or [])", "not _hard(r)"),
     '様式門の保留が順位を消費し、次の対比の閾値が α/m から α/(m−1) に緩む',
     'analyze', None),
    ('封印の語彙の写しを外す', 'D121', 'analyze_B.py',
     ("want = SIGN_MAP.get((SEAL.get('signs') or {}).get(r['id']))",
      "want = (SEAL.get('signs') or {}).get(r['id'])"),
     '正本の語彙で封印すると確証がすべて「登録された向きと逆」になる',
     'analyze', None),
    ('セッション記録の検査を本走行だけに戻す', 'D126', 'integrity_B.py',
     ("    if rk not in sessions:", "    if PHASE == 'main' and rk not in sessions:"),
     '調整走行・品質床・同一性選別で記録が無くても素通りする',
     'integrity', 'drop_sessions'),
    ('門のセッション検査を外す', 'D126', 'gate_B.py',
     ("if _miss and not a.allow_no_sessions:", "if False:"),
     '門が記録の不在を素通りする',
     'gate', 'drop_sessions'),
    ('升目の欠けを incomplete に倒さない', 'D126', 'gate_B.py',
     ("if _gap_tune and not a.allow_missing_cells:", "if False:"),
     '調整走行の升目が欠けても判定が open のまま',
     'gate', 'drop_tune_cell'),
    # ---- 直しの監査（2026-09-19）で集計器と読み口に繋いだ規則 ----
    ('等質性の注を集計器が付けない', 'D127', 'analyze_B.py',
     ("HOMOG = {k: rules_B.homogeneity(v, T) for k, v in HOMOG.items()}", "HOMOG = {k: dict(rules_B.homogeneity(v, T), note=False) for k, v in HOMOG.items()}"),
     'ランダム方向の三本が不均一でも注が付かない',
     'analyze', None),
    ('td の特異性を集計器が数えない', 'D133', 'analyze_B.py',
     ("        TD_SPEC += rules_B.td_specificity_family(_items, T)", "        TD_SPEC += [dict(x, label='書ける') for x in _items]"),
     'td の特異性をどの場面でも書ける（起草者の引力と同じ側）',
     'analyze', None),
    ('S4 の門を集計器が当てない', 'D134', 'analyze_B.py',
     ("    s4['gates'] = rules_B.s4_gates(s4A, s4B, T, qf_fail=(s4c['A'] in QF_FAIL or s4c['B'] in QF_FAIL))", "    s4['gates'] = []"),
     'ランダム方向の腕だけ書式外が増えても、S4 が三分岐に進む（反証の結果が分母で逆になりうる）',
     'analyze', 's4_ff'),
    ('様式門の札を集計器が使わない', 'P401', 'analyze_B.py',
     ("            r['label'] = rules_B.style_hold_label(r.get('p'))", "            r['label'] = '判定保留（様式転位）'"),
     '様式門に当たった非有意の対比が保留に化ける（起草者に有利な向き）',
     'analyze', None),
    ('選定後の相手の重複の番人を外す', 'P403', 'analyze_B.py',
     ("    if _n_runs > 1 or noop.get('n', 0) > QF['items']:", "    if False:"),
     '選定後の品質床の無操作の相手が二本あっても合算して読む（分母が倍になる）',
     'analyze', 'dup_post_partner'),
    ('様式の欄の空を採点欠落に数えない', 'D117', 'runs_B.py',
     ("        if phase != 'quality' and any(r.get(k) is None for k in ('style_a', 'style_b', 'mention')):", "        if False:"),
     '走行器が様式を書かなくても、様式門が黙って素通りする（走行器 v4 まで実際にそうだった）',
     'analyze', 'null_style'),
]


def break_data(root, how):
    """守りを試すために入力を壊す（**壊れた入力を止めるのが守りである**）。"""
    import glob
    if how == 'drop_sessions':
        shutil.rmtree(os.path.join(root, 'sessions-B'), ignore_errors=True)
    elif how == 'drop_tune_cell':
        d = sorted(glob.glob(os.path.join(root, 'tuneB', '*')))
        if d:
            shutil.rmtree(d[0], ignore_errors=True)
    elif how == 's4_ff':
        # S4 のランダム方向の腕だけ、答えの読めた試行を書式外に落とす（門が当たる入力・裁定 D134）
        for f in sorted(glob.glob(os.path.join(root, 'stageB', '*', 'trials-*.jsonl'))):
            rows = [json.loads(l) for l in open(f, encoding='utf-8') if l.strip()]
            if not any(r['arm'] == 'Osec-Ncold+vrand' for r in rows):
                continue
            k = 0
            for r in rows:
                if r['arm'] == 'Osec-Ncold+vrand' and r['status'] == 'ok' and not r['format_fail'] and k < 80:
                    r['format_fail'], r['catastrophe'], r['choice'] = True, None, None
                    k += 1
            with open(f, 'w', encoding='utf-8', newline='\n') as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    elif how == 'dup_post_partner':
        # 選定後の品質床の無操作の相手（Onull）を、同じセッション番号のままもう一本置く（採否表 P403）
        # **二本目にもセッション記録を書く**（同じ番号）——書かないと門と集計器がセッション記録の欠けで先に止まり、
        # 重複の番人まで届かない（一回目の変異の走行で、この壊し方がそうなっていた・2026-09-19）
        d = sorted(glob.glob(os.path.join(root, 'stageB-quality', '*post__Onull__noop*')))
        if d:
            shutil.copytree(d[0], d[0] + '__dup')
            rk = os.path.basename(d[0] + '__dup')
            json.dump({'tag': 'stageB-quality', 'session': 1, 'gpu': 'synth', 'batch': 16, 'run_keys': [rk], 'dry_run': True},
                      open(os.path.join(root, 'sessions-B', '%s.json' % rk), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    elif how == 'null_style':
        # 本走行の一つの腕の試行の様式・言及の欄を空にする（走行器が様式を書かなかった場合・2026-09-19）
        for f in sorted(glob.glob(os.path.join(root, 'stageB', '*', 'trials-*.jsonl')))[:1]:
            rows = [json.loads(l) for l in open(f, encoding='utf-8') if l.strip()]
            arm0 = next(r['arm'] for r in rows if '+v' in r['arm'] and 'vrand' not in r['arm'])
            for r in rows:
                if r['arm'] == arm0:
                    r['style_a'] = r['style_b'] = r['mention'] = None
            with open(f, 'w', encoding='utf-8', newline='\n') as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + '\n')


def run(tool, cwd):
    # **飛ばしを失敗に倒して走らせる**（裁定 D122・2026-09-19）。前は実トークナイザの置き場を渡し忘れると
    # 帯の起点の検査が「飛ばした」で通り、変異を「守りが無い」と誤って記録した（実際に起きた）。
    # いまは置き場が無ければ、変異を入れる前の土台の確認で止まる。
    p = subprocess.run([PY, os.path.join(cwd, 'tools', tool), '--selftest'],
                       capture_output=True, text=True, encoding='utf-8', cwd=cwd,
                       env=dict(os.environ, OP4B_REQUIRE_FULL_SELFTEST='1'))
    return p.returncode, ((p.stdout or '') + (p.stderr or '')).strip().split('\n')[-1][:160]



def pipeline_probe(cwd, kind, root):
    """合成データを通して、変異が**札や判定に出るか**を見る。戻りは (終了コード, 見分けのための値)。

    **走らせる前に古い記録を消す**——変異を入れた器が例外で落ちると記録を書かないので、
    前回の記録が残っていると**それを読んでしまい、守りがあるように見える**（この器自身がその型で作られていた）。
    """
    import glob
    for f in glob.glob(os.path.join(root, '[agi]*.json')) + glob.glob(os.path.join(root, 'i_*.json')):
        try:
            os.remove(f)
        except OSError:
            pass
    g_md, g_js = os.path.join(root, 'g.md'), os.path.join(root, 'g.json')
    rc_g = subprocess.run([PY, os.path.join(cwd, 'tools', 'gate_B.py'), '--root', root, '--allow-dry',
                           '--out', g_md, '--force'], capture_output=True, text=True, encoding='utf-8', cwd=cwd).returncode
    if kind == 'gate':
        v = None
        if os.path.exists(g_js):
            v = json.load(open(g_js, encoding='utf-8')).get('verdict')
        return rc_g, v
    if kind == 'integrity':
        # **不整合の件数で見る**（終了コードだけだと、例外で落ちた場合と区別できない）。
        out = {}
        for t in ('stageB', 'tuneB', 'stageB-quality', 'idB'):
            ij = os.path.join(root, 'i_%s.json' % t)
            rc = subprocess.run([PY, os.path.join(cwd, 'tools', 'integrity_B.py'), '--tag', t, '--root', root,
                                 '--allow-dry', '--out', os.path.join(root, 'i_%s.md' % t), '--force'],
                                capture_output=True, text=True, encoding='utf-8', cwd=cwd).returncode
            n = None
            if os.path.exists(ij):
                try:
                    n = len(json.load(open(ij, encoding='utf-8')).get('problems') or [])
                except Exception:
                    n = 'json が読めない'
            out[t] = {'rc': rc, 'problems': n}
        return (0 if all(v['rc'] == 0 for v in out.values()) else 1), out
    seal = os.path.join(root, 'seal-B.json')
    cmd = [PY, os.path.join(cwd, 'tools', 'analyze_B.py'), '--root', root, '--gate', g_js, '--allow-dry',
           '--allow-partial-seal', '--out', os.path.join(root, 'a.md'), '--force']
    if os.path.exists(seal):
        cmd += ['--seal', seal]
    rc_a = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', cwd=cwd).returncode
    aj = os.path.join(root, 'a.json')
    if not os.path.exists(aj):
        return rc_a, None
    d = json.load(open(aj, encoding='utf-8'))
    return rc_a, {'holm_alpha': sorted(round(c['holm_alpha'], 6) for c in d['confirm'] if c.get('holm_alpha') is not None),
                  'confirm': sum(1 for c in d['confirm'] if str(c.get('label', '')).startswith('確証')),
                  'reverse': sum(1 for c in d['confirm'] if '逆' in str(c.get('label'))),
                  'style_hold': sum(1 for c in d['confirm'] if c.get('label') == '判定保留（様式転位）'),
                  'agree': (d.get('sign_agreement') or {}).get('agree'),
                  'homog_notes': sum(1 for c in d['confirm'] if any('不均一' in n for n in (c.get('notes') or []))),
                  'td_write': sum(1 for t in (d.get('td_specificity') or []) if t.get('label') == '書ける'),
                  'gap': sum(1 for c in d['confirm'] if c.get('label') == '判定不能（採点欠落）'),
                  'qfloor': sum(1 for c in d['confirm'] if c.get('label') == '判定不能（品質床）'),
                  's4': (d.get('s4') or {}).get('verdict')}


ap = argparse.ArgumentParser()
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--list', action='store_true')
a = ap.parse_args()
if a.list:
    for m in MUTATIONS:
        print('  %-20s（裁定 %s・%s）: %s' % (m[0], m[1], m[2], m[5]))
    for m in PIPELINE_MUTATIONS:
        print('  %-24s（裁定 %s・%s・壊し方 %s）' % (m[0], m[1], m[2], m[6] or '無し'))
    sys.exit(0)

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'mutation-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p_ in (out_md, out_json):
        if os.path.exists(p_):
            sys.exit('既にある（--force で上書き）: %s' % p_)

tmp = tempfile.mkdtemp(prefix='mutB_')
rows, n_bad = [], 0
try:
    # records/predictions は予想の書式の器が封印の JS を流用する元（V′ 様式）を持つ（裁定 D148・2026-09-19 の夜に足した——足す前は、書式の器の自己検査が一時の置き場で元を見つけられず、変異を入れる前の土台の確認で止まった）
    for sub in ('tools', 'design', 'arms', os.path.join('records', 'predictions')):
        src = os.path.join(REPO, sub)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(tmp, sub))
    # 変異を入れる前に、全部通ることを確かめる（土台の確認）
    base = {}
    for tool in sorted({t for m in MUTATIONS for t in m[4]}):
        base[tool] = run(tool, tmp)
        if base[tool][0] != 0:
            sys.exit('変異を入れる前から自己検査が落ちている: %s（%s）' % (tool, base[tool][1]))
    for name, ruling, target, (old, new), tools, what in MUTATIONS:
        p = os.path.join(tmp, 'tools', target)
        s = open(p, encoding='utf-8').read()
        if s.count(old) != 1:
            rows.append({'name': name, 'ruling': ruling, 'target': target, 'applied': False,
                         'note': '変異の相手が %d 件（器が変わったので変異の定義を直す）' % s.count(old)})
            n_bad += 1
            continue
        open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new))
        got = {t: run(t, tmp) for t in tools}
        caught = [t for t, (rc, _) in got.items() if rc != 0]
        missed = [t for t, (rc, _) in got.items() if rc == 0]
        rows.append({'name': name, 'ruling': ruling, 'target': target, 'applied': True, 'what': what,
                     'caught': caught, 'missed': missed,
                     'lines': {t: got[t][1] for t in tools}})
        if missed:
            n_bad += 1
        open(p, 'w', encoding='utf-8', newline='\n').write(s)      # 戻す
    # ---- 合成データを通して見る変異（自己検査では見えないもの） ----
    if PIPELINE_MUTATIONS:
        root = os.path.join(tmp, 'synth')
        rc = subprocess.run([PY, os.path.join(tmp, 'tools', 'synth_B.py'), '--case', 'all', '--out-root', root],
                            capture_output=True, text=True, encoding='utf-8', cwd=tmp).returncode
        if rc != 0:
            sys.exit('合成データを作れない（変異の前）')
        base_probe = {}
        for kind in sorted({m[5] for m in PIPELINE_MUTATIONS}):
            base_probe[kind] = pipeline_probe(tmp, kind, root)
        for name, ruling, target, (old, new), what, kind, how in PIPELINE_MUTATIONS:
            p = os.path.join(tmp, 'tools', target)
            s0 = open(p, encoding='utf-8').read()
            if s0.count(old) != 1:
                rows.append({'name': name, 'ruling': ruling, 'target': target, 'applied': False, 'pipeline': True,
                             'note': '変異の相手が %d 件（器が変わったので変異の定義を直す）' % s0.count(old)})
                n_bad += 1
                continue
            # **壊した入力で当てる**（健全な入力では守りの有無が出力に出ない）
            probe_root = root
            if how:
                probe_root = os.path.join(tmp, 'broken_' + how)
                shutil.rmtree(probe_root, ignore_errors=True)
                shutil.copytree(root, probe_root)
                break_data(probe_root, how)
                before = pipeline_probe(tmp, kind, probe_root)      # 直した器が壊れた入力を止めるか
            else:
                before = base_probe[kind]
            open(p, 'w', encoding='utf-8', newline='\n').write(s0.replace(old, new))
            got = pipeline_probe(tmp, kind, probe_root)
            changed = (got != before)
            rows.append({'name': name, 'ruling': ruling, 'target': target, 'applied': True, 'pipeline': True,
                         'what': what, 'kind': kind, 'changed': changed, 'broken': how or '（健全な入力）',
                         'base': str(before)[:110], 'mutated': str(got)[:110]})
            if not changed:
                n_bad += 1
            open(p, 'w', encoding='utf-8', newline='\n').write(s0)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

json.dump({'kind': 'mutation_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'rows': rows, 'missed': n_bad, 'total': len(MUTATIONS) + len(PIPELINE_MUTATIONS)},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B **自己検査の検査**（変異・機械生成・`tools/mutation_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 正本 `selftest_rule`（裁定 D122）: **自己検査は、変異を入れて落ちるところまで作る。**',
     '- やり方: 器材を一時置き場に写し、**直す前の誤りを一件ずつ入れ直して**自己検査を走らせ、**落ちることを確かめる**。',
     '- **%d 件のうち、捕まえられなかった変異は %d 件。**（自己検査で見る %d 件・合成データを通して見る %d 件）'
     % (len(MUTATIONS) + len(PIPELINE_MUTATIONS), n_bad, len(MUTATIONS), len(PIPELINE_MUTATIONS)), '',
     '| 入れ直した誤り | 直した裁定 | 器 | 落ちた検査 | **落ちなかった検査** |', '|---|---|---|---|---|']
for r in rows:
    if not r.get('applied'):
        L.append('| %s | %s | `%s` | — | **変異を入れられない**（%s） |' % (r['name'], r['ruling'], r['target'], r['note']))
        continue
    if r.get('pipeline'):
        L.append('| %s | %s | `%s` | %s | %s |'
                 % (r['name'], r['ruling'], r['target'],
                    ('%s で出力が変わった（%s → %s）' % (r['broken'], r['base'], r['mutated'])) if r['changed']
                    else ('%s' % r['broken']),
                    '無し' if r['changed'] else '**出力が変わらない＝守りが無い**'))
        continue
    L.append('| %s | %s | `%s` | %s | %s |'
             % (r['name'], r['ruling'], r['target'],
                '・'.join(r['caught']) or '**無し**', ('**' + '・'.join(r['missed']) + '**') if r['missed'] else '無し'))
L += ['', '## 入れ直した誤りの中身', ''] + ['- **%s**（裁定 %s）: %s' % (r['name'], r['ruling'], r.get('what', r.get('note', '')))
                                              for r in rows]
L += ['', '## この検査が確認していないこと', '',
      '- **変異の一覧は起草者が選んだものである。**起草者が想像しなかった壊れ方は入っていない。',
      '- 自己検査が**通る**ことは、器が正しいことを意味しない（この器が見るのは「守りがあるか」だけである）。',
      '- 実機（GPU・実重み）では何も走らせていない。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[mutation_B] %s | %d 件中 捕まえられなかった変異 %d 件'
      % (os.path.relpath(out_md, REPO), len(MUTATIONS) + len(PIPELINE_MUTATIONS), n_bad))
for r in rows:
    if r.get('missed') or not r.get('applied'):
        print('  **守りが無い**: %s（%s）' % (r['name'], '・'.join(r.get('missed', [])) or r.get('note', '')))
sys.exit(1 if n_bad else 0)
