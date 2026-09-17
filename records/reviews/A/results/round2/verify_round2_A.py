# -*- coding: utf-8 -*-
"""verify_round2_A.py v1（2026-09-17・コーディネータ）—— 公開前の最終検分（第二巡・一票）の所見を、一次記録で出し直す器。凍結物ではない（本巡のために書いた）。
事前登録 `preregistration-reproduction-round2-A.md` の W154〜W161 に対応する。出力: 同じ置き場の verification-round2-A.{md,json}（--force なしでは上書きしない）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, hashlib, subprocess, datetime, argparse, collections

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, numbers_lint as NL
VERSION = 'v1.1'   # v1.1（2026-09-17・一回目の走行の後）: W160 の申し送りのファイルの検索から prelim/ を除き、名の型を反映メモ・申し送りに限る
ap = argparse.ArgumentParser(); ap.add_argument('--force', action='store_true'); a = ap.parse_args()
out_md = os.path.join(HERE, 'verification-round2-A.md'); out_js = os.path.join(HERE, 'verification-round2-A.json')
if (os.path.exists(out_md) or os.path.exists(out_js)) and not a.force:
    sys.exit('出力が既にある（上書きしない・--force で置き換え）')
rd = lambda rel: open(os.path.join(REPO, rel), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda rel: runs_A.sha16_file(os.path.join(REPO, rel))
git = lambda *args: subprocess.run(['git', '-C', REPO] + list(args), capture_output=True, text=True, encoding='utf-8').stdout
status_before = git('status', '--porcelain', '--untracked-files=no')
D4P = 'records/A/results-report-A-draft4-2026-09-17.md'
L4 = rd(D4P).split('\n'); ln = lambda n: L4[n - 1]
T = json.loads(rd('design/contrasts-A.json')); AN = json.loads(rd('records/A/analysis-stageA.json')); C = {x['id']: x for x in AN['contrasts']}
LB = T['families']['A_slope']['confirm_rule']['labels']; SIZES = T['sizes']
V1 = json.loads(rd('records/reviews/A/results/round1/verification-results-A-round1.json'))
W130 = next(x for x in V1['items'] if x['w'] == 'W130')['detail']
P03 = next(p for p in W130['passes'] if p['upward'])
UPN = 'N2 の Onull 対 N と S1 の Onull-Ncold 対 Onull'
R = []


def rec(w, finding, checked, verdict, detail):
    R.append(collections.OrderedDict(w=w, finding=finding, checked=checked, verdict=verdict, detail=detail))


def first(prefix):
    return [i + 1 for i, l in enumerate(L4) if l.startswith(prefix)]


# ---- W154 行番号
checks = [
    ('一致点1', '42', UPN in ln(42)),
    ('一致点1', '1993', UPN in ln(1993)),
    ('一致点1（並記表の札）', '548 以降', ln(548).startswith('| N2:Onull~N |') or ln(548).startswith('| S1:Onull-Ncold~Onull |')),
    ('一致点2', '48', ln(48).startswith('   - 様式門の hold の旗が立った対比では') and 'SK の O-Ncold 対 Osec-Ncold' in ln(48)),
    ('一致点3', '49', ln(49).startswith('   - 検査認識の言及率（語彙の機械計数）が半分以上のセルがある')),
    ('一致点3（§6 の応答様式の表）', '1161 以降', ln(1161).startswith('| 機種 | 場面 | 腕 |') or ln(1162).startswith('| 機種 | 場面 | 腕 |')),
    ('一致点4', '87〜92', ln(87).startswith('- 選択規則の読み') and all(ln(n).startswith('  - ') for n in range(88, 93))),
    ('一致点4（破局/n の区画）', '566 以降', ln(566).startswith('破局/n') or ln(565).startswith('破局/n') or ln(566).startswith('- S1:Lneg~Onull: A ')),
    ('一致点5', '250〜252', ln(250).startswith('- 散文層の副次終点の行と場面の対応') and ln(252).startswith('- 散文層の当てはめが判定不能に落ちた対比')),
    ('一致点6', '674〜682', ln(674).startswith('- 確証の一本（起草者の記入）') and ln(682) == '  - 札は主閾値のものを主とする。'),
    ('一致点7', '449〜450', ln(450).startswith('- 判定器の範囲と読み方')),
    ('一致点7', '1979', ln(1979).startswith('  - (xv) 適用: 判定器の妥当性は全機種・全場面で測った')),
    ('一致点7', '1990', ln(1990).startswith('  - 判定器の方向別の誤判定率のうち')),
    ('一致点8', '5', ln(5).startswith('- 打ち込んだ数の一覧') and 'D-33〜D-44' in ln(5)),
    ('一致点8', '1959', ln(1959).startswith('- 逸脱台帳') and 'D-34〜D-44' in ln(1959)),
    ('指摘1', '42・89・91・675・680', '二本' in ln(42) and '三規模' in ln(89) and '三対比' in ln(91) and '二つの Holm' in ln(91) and '三規模' in ln(675) and '一規模の差' in ln(680) and '二規模以上' in ln(680)),
    ('指摘2', '42', 'どちらも連続でないか端を欠く' in ln(42)),
    ('指摘3', '1950', '的中の行を載せていない' in ln(1950)),
    ('指摘3', '2006', 'predictions.compare_rules' in ln(2006)),
]
actual = {'並記表の見出し': first('| 対比 | 残った規模 |'), '並記表の N2:Onull~N の行': first('| N2:Onull~N |')[:1], '並記表の S1:Onull-Ncold~Onull の行': first('| S1:Onull-Ncold~Onull |')[:1],
          '破局/n の見出し': first('破局/n（規模順'), '§6 の応答様式の表の見出し': first('| 機種 | 場面 | 腕 | (a) |'), '566 行の中身': ln(566)[:40], '548 行の中身': ln(548)[:40], '1161 行の中身': ln(1161)[:40]}
bad = [(g, n) for g, n, ok in checks if not ok]
rec('W154', '票が示した草案4 の行番号', '草案4 の行を読み、票の述べる中身が当たるかを見る', '一部再現（%d か所のうち %d か所が合い、%d か所がずれる）' % (len(checks), len(checks) - len(bad), len(bad)),
    {'mismatch': bad, 'actual_positions': actual})

# ---- W155
ids = P03['upward']; conf = {p['id']: p for p in P03['confirmed']}
d = {'sensitivity': [P03['low'], P03['high']], 'upward': ids, 'main_labels': {i: C[i]['label'] for i in ids}, 'kept': {i: conf[i]['kept'] for i in ids}}
ok = ids == ['N2:Onull~N', 'S1:Onull-Ncold~Onull'] and d['main_labels'] == {'N2:Onull~N': LB['undecidable'], 'S1:Onull-Ncold~Onull': LB['clause']} and d['kept'] == {'N2:Onull~N': ['0.6B', '14B', '32B'], 'S1:Onull-Ncold~Onull': ['4B', '14B', '32B']}
rec('W155', '感度閾値の上向きの二本の名・主閾値の札・残った規模（一致点1）', '第一巡の再現の記録の W130 と機械集計の札', '再現' if ok else '一部再現', d)

# ---- W156
S = json.loads(rd('records/A/style-stageA.json')); c = C['S4:Onull~N']
cnt = {'%s|%s' % (s_, arm): S['cells'][s_]['S4'][arm]['c2_final'] for s_ in ('4B', '14B', '32B') for arm in ('N', 'Onull')}
want = {'4B|N': 144, '4B|Onull': 89, '14B|N': 5, '14B|Onull': 2, '32B|N': 4, '32B|Onull': 52}
b = {s_: (S['cells'][s_]['S4']['Onull']['b_final'], S['cells'][s_]['S4']['N']['b_final']) for s_ in SIZES}
i14 = SIZES.index('14B')
ok = (cnt == want and all(b[s_] == (0, 0) for s_ in ('4B', '14B', '32B')) and all(b[s_] == (200, 200) for s_ in ('0.6B', '1.7B', '8B'))
      and AN['size_env']['4B|S4'] == ['L4'] and AN['size_env']['14B|S4'] == ['A100'] and AN['size_env']['32B|S4'] == ['A100'] and c['critical_size']['size'] == '14B'
      and (c['counts']['kB'][i14], c['counts']['nB'][i14]) == (195, 200))
rec('W156', '確証の一本の数（一致点6）', '様式の記録の言及の件数と (b)・機械集計の環境・臨界規模・14B の N', '再現' if ok else '一部再現', {'c2_counts': cnt, 'b_final_Onull_N': b})

# ---- W157
MB = ('<!-- 機械:始 -->', '<!-- 機械:終 -->')
tpl = set(rd('records/A/results-report-template-A.md').split('\n'))
pat = re.compile(r'[一二三四五六七八九十]+(?:つ|本|規模|対比|票|名|件|段|か所|行|項|種|腕|セル|区画|尺度|向き|巡)')
kan = []; cur = False
for i, l in enumerate(L4, 1):
    if l == MB[0]:
        cur = True; continue
    if l == MB[1]:
        cur = False; continue
    if cur or l in tpl:
        continue
    kan += [(i, m.group(0)) for m in pat.finditer(l)]
tn = T['report_rules']['typed_numbers']
d = {'count_draft4': len(kan), 'by_token': dict(collections.Counter(t for _, t in kan)), 'ordinal_round_names': sum(1 for _, t in kan if t == '一巡'),
     'typed_numbers': tn, 'numbers_lint_NUM_matches_kanji': bool(NL.NUM.findall('三規模・二本・一規模')), 'numbers_lint_NUM_matches_digits': bool(NL.NUM.findall('3 規模'))}
ok = len(kan) == 66 and not d['numbers_lint_NUM_matches_kanji'] and d['numbers_lint_NUM_matches_digits'] and '限り' in tn
rec('W157', '漢数字の件数（指摘1）', '草案4 の区画の外の漢数字の件数・正本 typed_numbers・走査器の数の拾い方', '再現（件数は順番の名「第一巡」を含む数え方）' if ok else '一部再現', d)

# ---- W158
def pattern(kept):
    idx = [SIZES.index(s_) for s_ in kept]
    return {'non_contiguous': (idx[-1] - idx[0] + 1) != len(idx), 'ends_missing': [SIZES[j] for j in (0, len(SIZES) - 1) if j not in idx],
            'gaps': [SIZES[j] for j in range(idx[0], idx[-1] + 1) if j not in idx]}
d = {i: pattern(conf[i]['kept']) for i in ids}
ok = d['N2:Onull~N'] == {'non_contiguous': True, 'ends_missing': [], 'gaps': ['1.7B', '4B', '8B']} and d['S1:Onull-Ncold~Onull'] == {'non_contiguous': True, 'ends_missing': ['0.6B'], 'gaps': ['8B']}
rec('W158', '上向きの二本の残存の欠け方（指摘2）', '感度閾値の下の残った規模を、非連続・端の欠け・間の欠けに分ける', '一部再現（N2 は両端があり間を欠く〔票どおり〕。S1 は小さい側の端を欠くうえに間の 8B も欠く〔票は端の欠けだけを書く〕）' if ok else '検査不能', d)

# ---- W159
PC = rd('records/A/predictions-check-A.md').split('\n'); PJ = json.loads(rd('records/A/predictions-check-A.json'))
summ = [l for l in PC if re.match(r'^\| (向き|床持続|全体) \| \d+ \| \d+ \| \d+ \| \d+ \|$', l)]
det = [l for l in PC if re.match(r'^\| (向き|床持続|全体) \| a\.', l)]
readme = rd('README.md')
d = {'md_summary_rows': summ, 'md_detail_rows_with_hit': sum(1 for l in det if l.rstrip(' |').split('|')[-1].strip() == '的中'),
     'json_hits': {k2: sum(1 for r in v if r.get('result') == '的中') for k2, v in PJ['detail'].items()},
     'readme_mentions_predictions_check_A': readme.count('predictions-check-A'), 'readme_mentions_stage_A_report': readme.count('results-report-A-')}
ok = len(summ) == 6 and d['md_detail_rows_with_hit'] == 0 and all(v > 0 for v in d['json_hits'].values())
rec('W159', '照合の記録の md の読み違いのおそれ（指摘3）', 'md の冒頭の件数の表・明細の的中の行・JSON の的中の行・README の言及', '一部再現（md の明細に的中の行は無いが、冒頭の件数の表に的中の数がある）' if ok else '一部再現', d)

# ---- W160
proc = T['procedure']; step20 = proc[19] if isinstance(proc, list) else None
tracked = git('ls-files').split('\n')
d = {'procedure_step20': step20, 'public_files_named_memo_or_carryover': [f for f in tracked if not f.startswith('prelim/') and re.search(r'reflection-memo|carry-?over|反映メモ|申し送り', f, re.I)],   # v1.1: prelim/ の下見のメモを除く
     'records_B_files': [f for f in tracked if f.startswith('records/B/')],
     'adoption_round1_section6': '## 6. 段階 B の前の器の改訂の候補' in rd('records/reviews/A/results/round1/adoption-table-results-A-round1.md')}
ok = step20 and '反映メモ A' in step20 and not d['public_files_named_memo_or_carryover'] and d['adoption_round1_section6']
rec('W160', '段階 B の前の器の改訂の候補の追跡（条件 B2）', '手順表の手順 20・公開の置き場の申し送りのファイル・第一巡の採否表 §6', '再現（手順 20 に反映メモ A があり、まだ書いていない。候補は第一巡の採否表 §6 にだけある）' if ok else '一部再現', d)

# ---- W161
blob = subprocess.run(['git', '-C', REPO, 'show', '92c2495:' + D4P], capture_output=True).stdout
cur_b = open(os.path.join(REPO, D4P), 'rb').read()
G = json.loads(rd('records/A/main/report-lint-guard-draft4-2026-09-17.json'))
d = {'same_bytes_as_92c2495': blob == cur_b, 'draft4_sha16': s16(D4P), 'guard_report_sha16': G['report_sha16'], 'guard_pass': G['pass'],
     'changed_since_92c2495': git('diff', '--name-only', '92c2495', 'HEAD', '--', D4P).strip()}
ok = d['same_bytes_as_92c2495'] and d['draft4_sha16'] == G['report_sha16'] == 'AE5678309977243F' and G['pass'] and not d['changed_since_92c2495']
rec('W161', '公開の対象を「コミット 92c2495 の草案4」とする判定 A', '92c2495 の草案4 と現在の草案4 のバイト・歯止めの記録', '再現' if ok else '再現しない', d)

status_after = git('status', '--porcelain', '--untracked-files=no')
counts = collections.Counter(x['verdict'].split('（')[0] for x in R)
RES = collections.OrderedDict(kind='verify_round2_A', version=VERSION, generated_utc=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
                              head=git('rev-parse', 'HEAD').strip(), draft4_sha16=s16(D4P), tool_sha16=runs_A.sha16_file(os.path.abspath(__file__)),
                              tracked_changes_before=status_before, tracked_changes_after=status_after, counts=dict(counts), items=R,
                              clause='本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
json.dump(RES, open(out_js, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=str)
M = ['# 公開前の最終検分（第二巡）の所見の再現（機械生成・`verify_round2_A.py` %s・%s UTC）' % (VERSION, RES['generated_utc']), '',
     '- 事前登録: `preregistration-reproduction-round2-A.md`（`verify.log` の [prereg-reproduction-round2]）。票は `gemini-1/review.md`（出所は `provenance.md`）。',
     '- 対象: コミット %s・草案4 SHA16 %s・器 SHA16 %s。' % (RES['head'][:7], RES['draft4_sha16'], RES['tool_sha16']),
     '- 判定の数: %s（全 %d 項）。' % ('・'.join('%s %d' % kv for kv in counts.items()), len(R)),
     '- 追跡中のファイルの変更: 実行前 %s・実行後 %s（リポジトリは書き換えていない）。' % ('なし' if not status_before.strip() else 'あり', 'なし' if not status_after.strip() else 'あり'), '',
     '| W | 所見（票） | 確かめたこと | 判定 | 詳細（先頭） |', '|---|---|---|---|---|']
M += ['| %s | %s | %s | %s | %s |' % (x['w'], x['finding'], x['checked'], x['verdict'], json.dumps(x['detail'], ensure_ascii=False, default=str)[:300].replace('|', '／')) for x in R]
M += ['', RES['clause'], '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(M))
print('[verify-round2] %s | %s' % (dict(counts), [(x['w'], x['verdict'][:40]) for x in R]))
