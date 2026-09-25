# -*- coding: utf-8 -*-
"""器の実装の検分の R2 の票の事実の主張を、検分の版（コミット 87ce664）の一次の実物で確かめる（枠 `frame-impl-Bl3.md` §2・票を読んだ後・採否の案の前）。
検分の版を git から一時の置き場に取り出して、行を読み、安く試せるものは一時の置き場で実演する（実の重みを読まない・リポジトリの作業木に書かない）。
出力: records/reviews/Bl3/impl/checks/verification-impl-r2-Bl3.{json,md}（既にあれば書かない）
用法: python records/reviews/Bl3/impl/checks/verify_impl_r2_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, io, sys, json, shutil, hashlib, tarfile, tempfile, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
AT = '87ce664'
NL = chr(10)
OUT_J, OUT_M = os.path.join(HERE, 'verification-impl-r2-Bl3.json'), os.path.join(HERE, 'verification-impl-r2-Bl3.md')
assert not os.path.exists(OUT_J) and not os.path.exists(OUT_M), '既にある'
V = collections.OrderedDict()
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()


def rec(k, claim, ok, how, detail):
    V[k] = {'claim': claim, 'reproduced': ok, 'how': how, 'detail': detail}
    print('[verify_impl_r2] %s %s %s' % (k, '再現' if ok else ('一部' if ok is None else '再現せず'), detail[:170]), flush=True)


TD = tempfile.mkdtemp(prefix='verify-impl-r2-')
WT = os.path.join(TD, 'wt')
tarfile.open(fileobj=io.BytesIO(subprocess.run(['git', 'archive', '--format=tar', AT], cwd=REPO, capture_output=True, check=True).stdout)).extractall(WT)
for f in ('results/Bl3/directions-Bl3.json', 'results/Bl3/directions-Bl3.npz'):
    os.makedirs(os.path.dirname(os.path.join(WT, f)), exist_ok=True)
    shutil.copyfile(os.path.join(REPO, f), os.path.join(WT, f))
src = lambda p: open(os.path.join(WT, *p.split('/')), encoding='utf-8').read()
L = lambda p: src(p).split(NL)
hit = lambda p, pat: [i + 1 for i, l in enumerate(L(p)) if re.search(pat, l)]
sys.path.insert(0, os.path.join(WT, 'tools'))
try:
    T3 = json.load(open(os.path.join(WT, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
    FJ = json.load(open(os.path.join(WT, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
    DJ = json.load(open(os.path.join(WT, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
    import bl3_core as K
    import build_report_Bl3 as BRP

    # 重大-1: 封印した予想の SHA-256 を採点の時に照らさない（一時の置き場で、封印の後に予想を書き換えて報告の入力を読む）
    readers = {}
    for t in ('tools/build_report_Bl3.py', 'tools/analyze_Bl3.py', 'tools/colab/boot_Bl3.py', 'tools/freeze_Bl3.py', 'tools/sweep_Bl3.py'):
        s_ = src(t)
        readers[t] = bool(re.search(r"\['predictions'\]\[[^\]]+\]\['sha256'\]|\['sha256'\]\s*!=|sha256f\(p\)\s*!=\s*SR", s_))
    blens_has = 'def require_sealed' in src('tools/blens_lens.py') and "SR['predictions'][role]['sha256']" in src('tools/blens_lens.py')
    pdir = os.path.join(WT, 'records', 'predictions')
    os.makedirs(pdir, exist_ok=True)
    pc_, pr_ = os.path.join(pdir, 'predictions-Bl3-coordinator.json'), os.path.join(pdir, 'predictions-Bl3-registrant.json')
    open(pc_, 'w', encoding='utf-8').write(json.dumps({'q1.pilot': '続ける', 'q4.gate': '通る'}, ensure_ascii=False))
    open(pr_, 'w', encoding='utf-8').write(json.dumps({'q1.pilot': '続ける', 'q4.gate': '通らない'}, ensure_ascii=False))
    A = BRP.synth_analysis(T3, FJ, DJ)
    json.dump(A, open(os.path.join(WT, 'records', 'Bl3', 'analysis-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump({'main_freeze': {'pilot_attempts': A['pilot_attempts']}, 'deviations': []}, open(os.path.join(WT, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    seal = {'predictions': {r: {'path': 'records/predictions/%s' % os.path.basename(p), 'sha256': sha256b(open(p, 'rb').read())} for r, p in (('coordinator', pc_), ('registrant', pr_))}}
    json.dump(seal, open(os.path.join(WT, 'records', 'Bl3', 'sealing-record-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    before = BRP.load_inputs()[3]['coordinator']['q4.gate']
    open(pc_, 'w', encoding='utf-8').write(json.dumps({'q1.pilot': '続ける', 'q4.gate': '通らない'}, ensure_ascii=False))
    stopped = None
    try:
        T3x, FRx, Ax, predsx, metax, conf = BRP.load_inputs()
        after = predsx['coordinator']['q4.gate']
        text = BRP.build(T3x, Ax, predsx, metax, rejected='（合成）')
        row = [l for l in text.split(NL) if l.startswith('| q4.gate |')]
    except SystemExit as e_:
        stopped, after, row = str(e_), None, []
    rec('重大-1', '封印した予想の SHA-256 を、報告の組み立てでも起動器でも本の凍結でも照らさない（B-lens の器は照らしていた）',
        (not any(readers.values())) and blens_has and stopped is None and after != before,
        '検分の版の器で予想の SHA を読む行を探し、一時の置き場で封印の後にコーディネータの予想を書き換えて報告の入力を読み、報告を組んだ',
        '予想の SHA を照らす行: %s・B-lens の require_sealed に照合 %s・書き換えの前 %s → 後 %s・止まった %s・報告の q4 の行 %s' % (
            {k: v for k, v in readers.items()}, blens_has, before, after, stopped, row[:1]))

    # 重大-2: 結果を開く段は、一致だけを見る段が見た出力に結びつかない
    A_ = L('tools/analyze_Bl3.py')
    jfields = src('tools/analyze_Bl3.py').split('def judge(')[1].split('def open_results(')[0]
    has_sha_in_judge = 'sha256' in jfields or 'sha16' in jfields
    main_ = src('tools/analyze_Bl3.py').split('def main():')[1]
    open_part = main_.split("jp = a.judge_record or JUDGE")[1]
    open_checks_agree_only = ".get('agree')" in open_part and 'sha' not in open_part
    open_checks_rc = "A['recompute']" in open_part or "['recompute']['agree']" in open_part
    rec('重大-2', '一致だけを見る段の記録は読んだ出力の同定を持たず、結果を開く段は記録の agree だけを見て別に与えられた置き場を開き、開いた集計の再計算の一致が不一致でも止まらない',
        (not has_sha_in_judge) and open_checks_agree_only and not open_checks_rc,
        '検分の版の集計の器の judge と、main の open の枝を読んだ',
        'judge の中の SHA の同定 %s・open の枝は記録の agree だけを見る %s・open の枝で開いた集計の再計算の一致を見る %s' % (has_sha_in_judge, open_checks_agree_only, open_checks_rc))

    # 中-3: 相 check のコミットの器と凍結する器を照らさない・順伝播を呼んだ数は定数・守りは最上位の forward の前だけ
    fz = src('tools/freeze_Bl3.py')
    cc = fz.split("if colab_dir is not None:")[1].split("return T3, res, bad")[0]
    only_canon = "'canon_at_commit': S.get('canon_sha16') == canon16" in cc and 'git' not in cc and 'show' not in cc
    const0 = "'forward_calls': 0" in src('tools/colab/boot_Bl3.py')
    guard_top = "guard = model.register_forward_pre_hook(" in src('tools/colab/boot_Bl3.py')
    import torch
    import dry_run_Bl3 as DR

    class Stop(Exception):
        pass
    model, cfg = DR.tiny_model()
    g = model.register_forward_pre_hook(lambda m, a: (_ for _ in ()).throw(Stop('guard')))
    top_stops = inner_stops = False
    ids = torch.tensor([[1, 2, 3, 4]])
    try:
        with torch.no_grad():
            model(input_ids=ids)
    except Stop:
        top_stops = True
    try:
        with torch.no_grad():
            model.model(input_ids=ids)
    except Stop:
        inner_stops = True
    g.remove()
    rec('中-3', '凍結の器は相 check のコミットの正本の SHA16 だけを照らし、器・設計事実・方向の記録を照らさない。順伝播を呼んだ数は定数 0。守りは最上位の forward の前だけで、模型の本体を直に呼べば止まらない',
        only_canon and const0 and guard_top and top_stops and not inner_stops,
        '検分の版の凍結の器の相 check の確かめと起動器の行を読み、乱数の小さな模型に同じ形の守りを掛けて最上位と本体を呼んだ',
        '照らすのは正本の SHA16 だけ %s・順伝播の数は定数 %s・守りは最上位 %s・最上位を呼ぶと止まる %s・本体を呼ぶと止まる %s' % (only_canon, const0, guard_top, top_stops, inner_stops))

    # 中-4: 本の凍結は下見の試みを与えた順に並べ、由来を写すだけ
    mfc = fz.split('def main_freeze_checks(')[1].split('def main_freeze(')[0]
    order_given = 'for d in pilot_dirs:' in mfc and 'atts.append(PJ' in mfc and not re.search(r'sort[^\n]*finished|finished[^\n]*sort', mfc)      # 試みを finished で並べ直す行が無い
    only_exists = "in_commit(c, 'records/Bl3/FREEZE-RECORD-Bl3.json')" in mfc and 'cat-file' in fz and "canon_sha16') ==" not in mfc
    rec('中-4', '本の凍結は下見の試みを与えた順に並べて最後を本の下見にし、session の正本と npz は写すだけで照らさず、試みのコミットの二つの記録は有るかだけを見る',
        order_given and only_exists, '検分の版の凍結の器の本の凍結の確かめを読んだ', '与えた順のまま %s・有るかだけ %s' % (order_given, only_exists))

    # 中-5: 手元の二つの段と報告は凍結の記録の SHA16 を照らさず、DRY の印は組の一つで全体に効く
    an = src('tools/analyze_Bl3.py')
    no_frozen_check = 'frozen_sha16' not in an and 'frozen_sha16' not in src('tools/build_report_Bl3.py')
    dry_any = "dry = any(s.get('dry') for s in sessions.values())" in an
    rec('中-5', '手元の一致だけを見る段・結果を開く段・報告の組み立ては、凍結の記録の SHA16 と手元の器と正本を照らさず、組の一つの DRY の印で全体を DRY として扱う',
        no_frozen_check and dry_any, '検分の版の集計の器と報告の器を読んだ', '凍結の記録の SHA16 を読む行が無い %s・DRY は組の一つで全体 %s' % (no_frozen_check, dry_any))

    # 中-6: 合成データの正式の記録は起動器を別のプロセスとして走らせない
    dr = src('tools/dry_run_Bl3.py')
    no_boot = not re.search(r'subprocess\.run\([^\n]*boot_Bl3', dr) and not re.search(r'import boot_Bl3|boot_Bl3\.run\(', dr)      # 起動器を別のプロセスで走らせる行も import も無い（docstring の名は数えない）
    subp = [l.strip()[:80] for l in dr.split(NL) if 'subprocess.run(' in l]
    in_proc = 'def e2e(pilot_e):' in dr and 'AZ.judge(T3, parts, sessions' in dr
    rec('中-6', '合成データの器の端から端までは、器の関数を同じプロセスの中で呼び session を手で作る。起動器の三つの相と、ファイルを通した集計の器の CLI は、凍結の器が見る記録では走らない',
        no_boot and in_proc, '検分の版の合成データの器を読んだ', '起動器の名が出てこない %s・同じプロセスの端から端まで %s・別のプロセスで走らせるもの %s' % (no_boot, in_proc, subp))

    # 中-7: 組の出力は /content に置き、持ち出しは最後だけ
    bt = src('tools/colab/boot_Bl3.py')
    dl_lines = hit('tools/colab/boot_Bl3.py', r'files\.download\(')
    fin = bt.split('def finish(')[1].split('# ---- 7.')[0]
    only_in_finish = len(dl_lines) == 1 and 'files.download' in fin
    parts_default = "os.environ.get('OP4B_PART', ','.join(PARTS))" in bt
    content = "'/content/ontology-preamble-4b', '/content/op4b-Bl3'" in bt
    rec('中-7', '起動器は既定で三つの組を一度の起動で走らせ、組の出力は /content に置き、zip とダウンロードは最後の一度だけ',
        only_in_finish and parts_default and content, '検分の版の起動器を読んだ', 'ダウンロードの行 %s（終わりの関数の中だけ %s）・組の既定は三つ %s・置き場は /content %s' % (dl_lines, only_in_finish, parts_default, content))

    # 軽微 8: 報告の §1 は「近道を使う」と印字し、§4 は「本の計算の近道: いいえ」と印字する
    p8 = hit('tools/build_report_Bl3.py', r"近道を使う: %s")
    p8b = hit('tools/build_report_Bl3.py', r"本の計算の近道: %s")
    rec('軽微8', '報告の §1 の (v) の行は「近道を使う」と印字し、§4 は「本の計算の近道: いいえ」と印字して食い違う', bool(p8 and p8b), '検分の版の報告の器の行を探した', '(v) の行 %s・§4 の行 %s' % (p8, p8b))

    # 軽微 9: 凍結の記録の rulings に段階 B の番号が入る（文字列の比べ）
    rul = sorted(k for k in T3['decisions'] if k >= 'D204')
    extra = [k for k in rul if int(k[1:]) < 204]
    rec('軽微9', "凍結の記録の rulings は `k >= 'D204'` の文字列の比べで、D58・D59・D75・D90 のような番号も入る", bool(extra) and "k >= 'D204'" in fz,
        '正本の decisions に検分の版の式を当てた', '入る 204 より前の番号 %s' % extra)

    # 軽微 10: 門の行だけの升目だけを外しても〈下見で一部を外した〉の型が当たる
    cm = ['%s|%s' % tuple(c) for c in T3['cells_main']]
    go = sorted({'%s|%s' % (x[0], x[1]) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']})
    dec = K.cells_decision({c: True for c in cm}, {c: False for c in go}, T3['pilot']['decision']['cells_min_pass'])
    Ad = dict(BRP.synth_analysis(T3, FJ, DJ))
    Ad['pilot_attempts'] = [dict(Ad['pilot_attempts'][0], decision=dec)]
    types = [t for t, _, _ in BRP.reading_types(T3, Ad)]
    rec('軽微10', '門の行だけの升目だけが (i)(ii) を満たさないとき、q1 は「続ける」のまま、読みの型〈下見で一部を外した〉が当たる',
        dec['q1'] == '続ける' and bool(dec['dropped']) and '下見で一部を外した' in types, '芯の決定の関数に門の行だけの升目の不合格を与え、報告の器の読みの型を当てた',
        'q1 %s・外した升目 %s・当たった型に〈下見で一部を外した〉 %s' % (dec['q1'], dec['dropped'], '下見で一部を外した' in types))

    # 軽微 11: 「nuclear の族は測れなかった」は下見の節に置かれ、報告の頭（§0）には置かれない
    n11 = hit('tools/build_report_Bl3.py', r"nuclear の族は測れなかった")
    fn = [i for i in n11]
    in_pilot_lines = any(i for i in fn if 'def pilot_lines' in NL.join(L('tools/build_report_Bl3.py')[:i]).split('def ')[-1][:40] or True)
    head_rule = '報告の頭' in json.dumps(T3['pilot']['decision']['family'], ensure_ascii=False)
    pl = src('tools/build_report_Bl3.py').split('def pilot_lines(')[1].split('def outcomes(')[0]
    rec('軽微11', '「nuclear の族は測れなかった」は下見の記録の節（pilot_lines）にだけ置かれ、正本 pilot.decision.family の「報告の頭に」と違う',
        head_rule and 'nuclear の族は測れなかった' in pl and len(n11) == 1, '検分の版の報告の器の行と正本の文を読んだ', '行 %s・正本の文に「報告の頭」 %s' % (n11, head_rule))

    # 軽微 12: 掃き出しは層ごとの差分の鍵があるかだけを見る
    sw = src('tools/sweep_Bl3.py')
    s12 = "need({'noop_lo', 'rows', 'iso_summary'} <= set(lw)" in sw and 'len(lw' not in sw
    rec('軽微12', '掃き出しは層ごとの差分の三つの鍵があるかだけを見て、行の中身と層の数を見ない', s12, '検分の版の掃き出しの器を読んだ', '鍵だけ %s' % s12)

    # 軽微 13: 凍結の本文の確かめは凍結版の原稿を見ない（引数 fsrc を使わない）
    rb = src('tools/make_frozen_Bl3.py').split('def rebuild_and_check(')[1].split('def write_diffrec(')[0]
    body = rb.split(NL, 1)[1]
    rec('軽微13', '凍結の本文の確かめ（rebuild_and_check）は引数 fsrc を受けるが使わず、凍結版の原稿と本文の食い違いを見ない', 'fsrc' not in body, '検分の版の凍結の本文の器を読んだ', '関数の本体に fsrc が出てこない %s' % ('fsrc' not in body))

    # 軽微 14: 凍結の一行の登録者の逐語と日時が、数の検査と禁止語の走査を通る（一時の置き場で凍結の本文を組んでみる）
    def mf(words, date):
        for f in ('design/design-Bl3-FROZEN.src.md', 'design/design-Bl3-FROZEN.md'):
            fp = os.path.join(WT, *f.split('/'))
            if os.path.exists(fp):
                os.remove(fp)
        r = subprocess.run([sys.executable, os.path.join(WT, 'tools', 'make_frozen_Bl3.py'), '--words', words, '--commit', 'deadbee', '--date', date],
                           capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=WT, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        out = r.stdout + r.stderr
        return r.returncode, ('組み立てが止まった' in out), out[-400:]
    a_ = mf('凍結してください', '2026-09-26 10:00')
    b_ = mf('10時に凍結してください', '2026-09-26 10:00')
    rec('軽微14', '凍結の一行の登録者の逐語に数（「10時」など）があると、組み立ての数の検査で止まる（日時の形だけなら止まらない）',
        (not a_[1]) and b_[1], '一時の置き場で、数を含まない言葉と含む言葉の二通りで凍結の本文を組んだ（組み立てより後の確かめは一時の置き場に git が無いので外れる）',
        '数を含まない言葉: 終わりの値 %d・組み立てで止まった %s／「10時」を含む言葉: 終わりの値 %d・組み立てで止まった %s' % (a_[0], a_[1], b_[0], b_[1]))

    # 軽微 15: 版の確かめは inputs.versions_B の scipy を外す
    pins = sorted(T3['inputs']['versions_B'])
    want_line = [l.strip() for l in bt.split(NL) if l.strip().startswith('want = {')]
    rec('軽微15', '起動器の版の確かめは正本 inputs.versions_B の三つだけを照らし、scipy を外す', 'scipy' in pins and not any('scipy' in l for l in want_line),
        '正本の版の欄と検分の版の起動器の行を読んだ', '正本の欄 %s・起動器の照らす行 %s' % (pins, want_line))

    # 軽微 16: 凍結の器は正本 inputs.files の SHA16 を照らさない
    ff = fz.split('def frozen_files(')[1].split('def latest_dry_run(')[0] + fz.split('def prepilot_checks(')[1].split('def prepilot(')[0]
    s16 = "T3['inputs']['files']" in ff and not re.search(r"inputs'\]\['files'\].*sha16", ff)
    rec('軽微16', '凍結の器は正本 inputs.files の置き場を凍結物に入れるが、正本に書いた SHA16 と照らさない', s16, '検分の版の凍結の器を読んだ', '照らさない %s' % s16)

    # 軽微 17: verify_frozen は無いファイルを飛ばすだけ
    vf = bt.split('def verify_frozen(')[1].split('def pick_recompute_rows(')[0]
    rec('軽微17', '起動器の verify_frozen は、無いファイルを疎な取り出しの内外を問わず飛ばす', 'skipped.append(rp)' in vf and 'SPARSE' not in vf, '検分の版の起動器を読んだ', '内外を分けない %s' % ('SPARSE' not in vf))

    # 軽微 18: 下見と本の計算の GPU が同じかを見ない
    envk = re.search(r"def env_same\(sessions\):.*?keys = \(([^)]*)\)", an, flags=re.S)
    rec('軽微18', '集計の器の環境の比べは本の計算の組の間だけで、下見の session の GPU と比べない', bool(envk) and 'pilot' not in an.split('def env_same(')[1].split('def with_iso(')[0],
        '検分の版の集計の器を読んだ', '比べる鍵 %s' % (envk.group(1) if envk else None))

    # 軽微 19: 登録者の情報状態の欄が空でも封印の検べを通る
    import make_predictions_form_Bl3 as FORM
    os.makedirs(os.path.dirname(FORM.OUT), exist_ok=True)
    open(FORM.OUT, 'w', encoding='utf-8', newline=NL).write(FORM.build(FORM.load_T()))      # 書式は下見の前の凍結で組むので、一時の置き場で組む
    import seal_Bl3 as SEAL
    Tf, keys, opts, M = SEAL.form_spec()
    v5 = {k: FORM.NP for k in FORM.prediction_keys(Tf)}
    v5.update({'q1.pilot': '続ける', 'q4.gate': '通らない', 'who': '登録者', 'info.coi': '', 'free': '', 'date': '2026-09-26'})
    ok19 = True
    try:
        SEAL.validate(v5, keys, opts, 'registrant', Tf, full=False)
    except (AssertionError, SystemExit, ValueError) as e_:
        ok19 = False
    rec('軽微19', '登録者の予想の情報状態の欄（info.coi・free）が空でも、封印の検べを通る', ok19, '検分の版の封印の器の検べに、欄を空にした登録者の JSON を与えた', '通った %s' % ok19)

    # 軽微 20: 方向の npz が無いと、起動器は止め方でなく予期しない誤りで落ちる
    i20 = [l.strip() for l in bt.split(NL) if 'npz_sha = sha256f(NPZ)' in l]
    exists20 = 'os.path.exists(NPZ)' in bt
    rec('軽微20', '起動器は方向の npz の有無を確かめずに SHA-256 を取るので、npz が無いと止め方でなく予期しない誤りで落ちる', bool(i20) and not exists20, '検分の版の起動器を読んだ', '行 %s・有無の確かめ %s' % (i20, exists20))

    # 軽微 21: 止めの印は session に入らず、予期しない誤りでは session と zip が作られず、n_forward は起動の中で累積する
    st = bt.split('def stop(')[1].split('def jdefault(')[0]
    tail = bt.split("if __name__ == '__main__':")[1]
    cum = "out['n_forward'] = R.n_forward" in bt
    rec('軽微21', '止めは記録の印と終わりだけで session.json を書かず、予期しない誤りの枝も session と zip を作らず、組の n_forward は起動の中の累積', ('session' not in st) and ('finish(' not in tail) and cum,
        '検分の版の起動器を読んだ', '止めで session を書かない %s・予期しない誤りの枝で finish を呼ばない %s・累積 %s' % ('session' not in st, 'finish(' not in tail, cum))

    # 軽微 22: 古い記述と、転記行 F の断片の欠けに柵が無い
    mc_head = L('tools/make_contrasts_Bl3.py')[1]
    mc_ver = [l for l in L('tools/make_contrasts_Bl3.py') if l.startswith('VERSION =')]
    sw_head = L('tools/sweep_Bl3.py')[3]
    no_required = 'REQUIRED' in sw_head and 'REQUIRED =' not in sw
    skip = hit('tools/bl3_facts.py', r'skip_weights_hash')
    rec('軽微22', '正本の生成器の頭の文は v5 のまま（版は v7）・掃き出しの器の頭の文は無い REQUIRED を指す・設計事実を --skip-weights-hash で作り直すと転記行 F から断片が落ちる',
        ('v5' in mc_head) and bool(mc_ver) and 'v7' in mc_ver[0] and no_required and bool(skip), '検分の版の三つの器を読んだ',
        '生成器の頭 %s・版 %s・掃き出しの頭に REQUIRED %s・断片を落とす引数の行 %s' % (mc_head[:40], mc_ver, no_required, skip))
finally:
    shutil.rmtree(TD, ignore_errors=True)

json.dump({'version_under_review': AT, 'checks': V, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'},
          open(OUT_J, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
Lm = ['# 器の実装の検分の R2 の票の事実の主張の確かめ（機械生成・`verify_impl_r2_Bl3.py`・検分の版 %s）' % AT, '',
      '- 検分の版を git から一時の置き場に取り出して確かめた。実演は一時の置き場でだけ行った（実の重みを読まない・リポジトリの作業木に書かない）。', '',
      '| 番号 | 主張 | 確かめ | 結果 | 詳しく |', '|---|---|---|---|---|'] + [
      '| %s | %s | %s | %s | %s |' % (k, v['claim'], v['how'], '再現した' if v['reproduced'] else ('一部' if v['reproduced'] is None else '再現しない'), v['detail'].replace('|', '｜')) for k, v in V.items()] + [
      '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_M, 'w', encoding='utf-8', newline=NL).write(NL.join(Lm))
print('[verify_impl_r2] wrote %s' % os.path.relpath(OUT_M, REPO))
