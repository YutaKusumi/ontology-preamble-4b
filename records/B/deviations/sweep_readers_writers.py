# -*- coding: utf-8 -*-
"""同じ型の食い違いの掃き出し（採否表 P441・登録者裁定 D151 の条件）——**逸脱の下の集計器を走らせる前に**、向きに依らず行う。
「読み手の器が求める升目・欄・ファイル」⊆「書き手の器が実際に書いたもの」を、実データの**置き場の名と、判定に関わらない欄だけ**で照らす（率・判定欄は読まない）。
出力: records/B/deviations/sweep-readers-writers-2026-09-22.md。用法: python records/B/deviations/sweep_readers_writers.py"""
import os, sys, json, glob, hashlib, datetime
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_B
j = lambda *p: os.path.join(REPO, *p)
T = json.load(open(j('design', 'contrasts-B.json'), encoding='utf-8'))
G = json.load(open(j('records', 'B', 'gate-B-2026-09-21.json'), encoding='utf-8'))
A = json.load(open(j('records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
F = json.load(open(j('records', 'B', 'FREEZE-RECORD-B.json'), encoding='utf-8'))
CANON = runs_B.sha16_file(j('design', 'contrasts-B.json'))
PICK = G['selection']['pick']
rows = []


def add(no, what, reader, writer, result, ok, note=''):
    rows.append((no, what, reader, writer, result, '食い違いなし' if ok else '**食い違い**', note))


def dirs(tag, part=''):
    return sorted(d for d in os.listdir(j('results', tag)) if os.path.isdir(j('results', tag, d)) and part in d)


# S1 本走行の升目（集計器が数える升目 ⊆ 走行の置き場）
add('S1', '本走行の升目と対比に現れない腕', 'analyze_B', 'boot（main）', '記録の無いセル %d・対比に現れない腕 %d・置き場 %d' % (len(A['missing_cells']), len(A['orphan_arms']), len(dirs('stageB'))),
    not A['missing_cells'] and not A['orphan_arms'] and len(dirs('stageB')) == 59)

# S2 選定の段の升目（門が読む 18 セル＋無操作 2）
sel_cells = [d for d in dirs('stageB-quality', '__selection__') if '__noop__' not in d]
sel_noop = dirs('stageB-quality', '__selection__noop__')
add('S2', '品質床・選定の段の升目', 'gate_B', 'boot（quality・selection）', '介入のセル %d（登録 %d）・無操作 %d（土台 %d）' % (len(sel_cells), T['quality_floor']['selection_cells'], len(sel_noop), len(T['quality_floor']['arms'])),
    len(sel_cells) == T['quality_floor']['selection_cells'] and len(sel_noop) == len(T['quality_floor']['arms']))

# S3 選定後の段の升目——**既知の食い違い**（逸脱 D-B1）。読み一の升目（残りの介入の腕＋その土台の無操作）と置き場を、過不足の両向きで照らす
interv = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
base_two = {'O-Ncold-v', 'Onull+v'}
want_post = sorted(a for a in interv if a not in base_two)
want_noop = sorted({a.split('+v')[0].split('-v')[0] for a in want_post})
post_cells = [d for d in dirs('stageB-quality', '__post__') if '__noop__' not in d]
post_noop = dirs('stageB-quality', '__post__noop__')
got_post = sorted(d.split('__post__')[1].split('__L')[0] for d in post_cells)
got_noop = sorted(d.split('__post__noop__')[1].split('__s')[0] for d in post_noop)
add('S3', '品質床・選定後の段の升目（読み一の升目）', 'analyze_B（post だけを読む）', 'boot（quality・post）',
    '介入 %d／%d・無操作 %d／%d・余りのセル %d・集計器が「走行が無い」とした腕 %s' % (len(got_post), len(want_post), len(got_noop), len(want_noop),
        len(set(got_post) - set(want_post)), '・'.join(r['arm'] for r in A['quality_post'] if r.get('missing'))),
    False, '**これが逸脱 D-B1 の一件**。読み一の升目には過不足なし（%s）。集計器の側が二腕にも post を求める' % ('一致' if got_post == want_post and got_noop == want_noop else '**不一致**'))
assert got_post == want_post and got_noop == want_noop

# S4 選定後の段の層 × 係数の束縛（選ばれた組でしか走っていないこと）
bad_bind = [d for d in post_cells if ('__L%sC%s__' % (PICK['layer'], PICK['coef'])) not in d]
add('S4', '選定後の段と本走行の束縛（選ばれた組）', 'analyze_B（binding）', 'boot', '選ばれた組でない選定後のセル %d・集計器の束縛の食い違い %d' % (len(bad_bind), len(A.get('binding') or [])),
    not bad_bind and not (A.get('binding') or []))

# S5 副位置の活性（layers_B が読む npz）——判定に関わらない欄（trial_id・status・resp_mean_path）だけを読む
miss, total, no_path, cells_npz = 0, 0, 0, 0
for d in dirs('stageB'):
    tp = glob.glob(j('results', 'stageB', d, 'trials-*.jsonl'))[0]
    npz_cache = {}
    for r in runs_B.iter_jsonl(tp, ('trial_id', 'status', 'resp_mean_path')):
        if r.get('status') != 'ok':
            continue
        total += 1
        p = r.get('resp_mean_path')
        if not p:
            no_path += 1
            continue
        fn, key = p.split('#', 1)
        if fn not in npz_cache:
            fp = j('results', 'stageB', d, fn)
            npz_cache[fn] = set(np.load(fp).files) if os.path.exists(fp) else None
            cells_npz += int(npz_cache[fn] is not None)
        if npz_cache[fn] is None or key not in npz_cache[fn]:
            miss += 1
add('S5', '副位置の活性（応答トークン平均）', 'layers_B（欠けで止まらない）', 'run_stageB_local（resp-*.npz）',
    '本走行の使えた試行 %d・path の無い試行 %d・npz か鍵が解けない試行 %d・npz のあるセル %d／59' % (total, no_path, miss, cells_npz), miss == 0 and cells_npz == 59,
    'npz は手元と Drive にあり、公開の置き場には無い（登録者裁定 D154・SHA16 はセッション記録）。path の無い試行は「応答が空」の登録どおりの扱い')

# S6 凍らせた方向（layers_B・起動器が読む）
dn = j('results', 'dirB', 'dirB__s1', 'directions.npz')
vsha = hashlib.sha256(open(dn, 'rb').read()).hexdigest().upper()
FV = json.load(open(j('records', 'B', 'freeze-values-B.json'), encoding='utf-8'))
want_v = json.dumps(FV, ensure_ascii=False)
add('S6', '凍らせた方向 directions.npz', 'layers_B・boot', 'direction_B（相 dir）', 'SHA-256 %s…が凍結の値に%s' % (vsha[:12], 'ある' if vsha in want_v else '**無い**'), vsha in want_v)

# S7 予想の照合の入力（confirm の id が登録の対比と一致・予想の二つのファイルの SHA-256 が凍結の記録と一致）
import compare_predictions_B as CP
ids_want = sorted(CP.conf_ids(T)); ids_got = sorted(r['id'] for r in A['confirm'])
pred_ok = []
for who in ('registrant', 'coordinator'):        # 凍結の記録の predictions は {予想者: {path, sha256, …}} の形（最初の版は形を読み違えて 0 件と数えた）
    pr = (F.get('predictions') or {}).get(who) or {}
    fp = j(*pr['path'].split('/')) if pr.get('path') else None
    pred_ok.append(bool(fp and os.path.exists(fp) and hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper() == str(pr.get('sha256', '')).upper()))
labels = sorted({str(r.get('label')) for r in A['confirm']})
add('S7', '封印予想の照合の入力', 'compare_predictions_B', 'analyze_B・seal', '対比の id %d／%d 一致・予想のファイルの SHA-256 一致 %d／%d・札の種類 %s' % (
    len(set(ids_want) & set(ids_got)), len(ids_want), sum(pred_ok), len(pred_ok), '／'.join(labels)), ids_want == ids_got and all(pred_ok) and len(pred_ok) >= 2,
    '照合の器は札の頭「確証」と「非有意」で読む——逸脱の印は頭を変えない（採否表 P444）')

# S8 報告の組み立ての入力（必須の記録が揃い、正本 SHA16 が同じ）
need = {'gate': 'records/B/gate-B-2026-09-21.json', 'integrity': 'records/B/integrity-stageB-2026-09-21.json', 'sampling': 'records/B/sampling-inspection-B-stageB-seal.json',
        'chart': 'records/B/control-chart-B-2026-09-22.json', 'identity': 'records/B/identity-screen-B.json', 'analysis': 'records/B/analysis-B-2026-09-22.json'}
st = []
for k, rel in need.items():
    ok_ = os.path.exists(j(*rel.split('/')))
    sha = (json.load(open(j(*rel.split('/')), encoding='utf-8')).get('contrasts_sha16') if ok_ else None)
    st.append((k, ok_, sha))
add('S8', '報告の組み立ての入力の記録', 'build_report_B', '各器', '・'.join('%s %s%s' % (k, 'あり' if o else '**無し**', '' if s in (None, CANON) else '（正本 SHA16 が違う）') for k, o, s in st),
    all(o and s in (None, CANON) for _, o, s in st), 'layers と predictions-check はこれから作る')

# S9 セッション記録と走行キー（どの相も、走行キーがセッション記録に載っている）
sess_bad = []
for tag in ('idB', 'tuneB', 'stageB-quality', 'stageB'):
    keys = set()
    for sp in glob.glob(j('results', 'sessions-B', '%s__s*.json' % tag)):
        keys |= set(json.load(open(sp, encoding='utf-8')).get('run_keys') or [])
    sess_bad += [d for d in dirs(tag) if d not in keys]
add('S9', 'セッション記録と走行キー', 'gate_B・analyze_B・integrity_B', 'boot（write_session）', 'セッション記録に載っていない走行 %d' % len(sess_bad), not sess_bad,
    '選定後の段を新しいランタイムで走らせながら番号 1 のままにした件は別に記帳する（逸脱 D-B3）')

now = datetime.datetime.now(datetime.timezone.utc)
L = ['# 同じ型の食い違いの掃き出し（読み手の器 ⊆ 書き手の器・2026-09-22・**逸脱の下の集計器を走らせる前**）', '',
     '- 機械生成（`records/B/deviations/sweep_readers_writers.py`・%s UTC）。正本 SHA16 %s。**率と判定欄は読んでいない**（置き場の名と、trial_id・status・resp_mean_path の欄だけ）。' % (now.strftime('%Y-%m-%d %H:%M'), CANON),
     '- 向きに依らない: 足りないもの（読み手が求めて無いもの）も、余るもの（書き手が書いて登録に無いもの）も数える。', '',
     '| 番号 | 何を | 読み手 | 書き手 | 結果 | 判定 | 注 |', '|---|---|---|---|---|---|---|']
L += ['| %s | %s | %s | %s | %s | %s | %s |' % r for r in rows]
bad = [r for r in rows if r[5] != '食い違いなし']
L += ['', '- 食い違い %d 件（%s）。既知の一件（S3＝逸脱 D-B1）のほかに食い違いは%s。' % (len(bad), '・'.join(r[0] for r in bad), '無い' if [r[0] for r in bad] == ['S3'] else '**ある**'),
      '', '## この掃き出しが確認していないこと', '',
      '- 欄の**中身の意味**の食い違い（たとえば同じ欄を二つの器が別の単位で読む）は、この掃き出しでは捕まらない。置き場・升目・鍵・ファイルの有無と SHA だけを見た。',
      '- 報告の組み立て器が機械の区画に貼る行の書式。副位置の読みと予想の照合の出力（これから作る）。',
      '- 起草者が思いつかなかった型の食い違い（この一覧も起草者が作った）。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
out = j('records', 'B', 'deviations', 'sweep-readers-writers-2026-09-22.md')
open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('\n'.join(L[6:6 + len(rows) + 3]))
