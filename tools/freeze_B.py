# -*- coding: utf-8 -*-
"""freeze_B.py v4 —— 段階 B の**凍結の記帳**（凍結物の SHA・封印予想・凍結時に記帳する値・逸脱台帳の口）。

凍結するもの（正本 `publication.record_first`・草案8B §2.11）:
  凍結本文（草案）・正本 `design/contrasts-B.json`・腕と方向の定義・器材・報告の雛形・**封印予想**。
凍結時に記帳する値（設計の段では書けないもの）:
  - 重みの rev・tokenizer の版・**総層数**（`selection.candidates.layer_index_rule`）と層の添字
  - **腕ごとのトークン長**（裁定 D82・`position_length.record_at_freeze`）
  - 品質床の課題の出所・版・ライセンス・断片の SHA（裁定 D66）と、**無操作の実測の正答率**（下限 `quality_floor.base_min` を凍結する根拠・裁定 D129）
    （入力・帯・採点・最大トークン数は裁定 D120 で正本に登録したので、ここでは求めない・v4）
  - **‖v̂‖ と主位置の ‖h‖ の比**（層ごと・`activation_storage.h_norm_record`・採否表 P356）
  - **まだ下りていない登録者の裁定**: 同一性選別に Osec-Ncold を足すか（`identity_screen.b_panel_arms_compared`）・S4 の効き目を絶対値のままにするか（`effect_pt_caveat`）
  - v̂ の SHA（`selection.vector_fix`）と方向の要約統計（ノルム・コサイン・場面間の安定性）
封印予想（`seal_format`）: 確証の各対比の符号と S4 の反証。**B のデータを一つも見る前**に書き、情報状態と時機を添える。
凍結の後の変更はすべて**逸脱**とし、番号・日付・理由・登録者の承認を記帳する（`deviation.rule`）。
出力: records/B/FREEZE-RECORD-B.md と同 .json（--force が無ければ上書きしない）。
用法: python tools/freeze_B.py --draft design/design-stageB-draft12.md [--seal records/B/seal-B.json] [--values records/B/freeze-values-B.json] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v4'
REPO = runs_B.REPO
CARRYOVER = {'凍結走行器（組み立てと採点の型）': 'tools/run_preamble_local.py',
             '凍結パーサ': 'arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py',
             '場面の素材': 'arms/frozen-from-ryokai-os/app-scenarios.json',
             # 走行器が様式・言及・refuse の分類・ループを段階 A の凍結した関数で書くようになったので、その出所も凍結物に数える（2026-09-19）
             '様式と言及の器（段階 A）': 'tools/response_mode_A.py',
             '名の語彙（段階 M）': 'tools/response_mode_M.py',
             '名の語彙（段階 F・一致の照合）': 'tools/response_mode_F.py',
             '言及の語彙（段階 F の正本）': 'design/contrasts-F.json',
             'refuse の分類の規則（丙）': 'arms/materials-draft/hei/refuse-rules-v2.json'}
TOOLS = ['runs_B.py', 'rules_B.py', 'make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py', 'numbers_lint.py', 'gate_B.py', 'analyze_B.py',
         'layers_B.py', 'integrity_B.py', 'sample_inspection_B.py', 'direction_B.py', 'steer_B.py', 'run_stageB_local.py', 'synth_B.py',
         'dry_run_B.py', 'mutation_B.py', 'endtoend_B.py', 'build_report_B.py', 'freeze_B.py', 'control_chart_B.py']
NEED_VALUES = ['model_rev', 'tokenizer_rev', 'num_hidden_layers', 'layer_indices', 'arm_token_lengths',
               'quality_task', 'quality_base_accuracy', 'v_hat_sha256', 'direction_stats', 'h_norm_ratio',
               'identity_osec_ncold_decision', 's4_effect_decision']
ap = argparse.ArgumentParser()
ap.add_argument('--draft', required=True)
ap.add_argument('--seal', default=None)
ap.add_argument('--values', default=None, help='凍結時に記帳する値（json・上の NEED_VALUES）')
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-missing', action='store_true', help='記帳の値や封印が揃っていなくても書く（**凍結ではなく点検用**）')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
cpath = a.contrasts or runs_B.CPATH
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'FREEZE-RECORD-B.md')
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

frozen = {'canon': {'path': 'design/contrasts-B.json', 'sha16': runs_B.sha16_file(cpath), 'version': T['version']},
          'draft': {'path': os.path.relpath(a.draft, REPO).replace('\\', '/'), 'sha16': runs_B.sha16_file(a.draft)},
          'facts': {'path': 'records/B/design-facts-B.md', 'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'))},
          'report_template': {'path': 'records/B/results-report-template-B.md',
                              'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))},
          'arms': T['arms']['sha16'], 'arm_files': T['arms'].get('files'),
          'tools': {}}
for t in TOOLS:
    p = os.path.join(REPO, 'tools', t)
    frozen['tools'][t] = runs_B.sha16_file(p) if os.path.exists(p) else None
frozen['carryover'] = {}
for name, rel in CARRYOVER.items():
    p = os.path.join(REPO, *rel.split('/'))
    frozen['carryover'][name] = {'path': rel, 'sha16': runs_B.sha16_file(p) if os.path.exists(p) else None}
missing_carry = [n for n, v in frozen['carryover'].items() if not v['sha16']]
missing_tools = [t for t, v in frozen['tools'].items() if v is None]

VALUES = runs_B.read_json(a.values) if a.values else {}
missing_values = [k for k in NEED_VALUES if k not in VALUES or VALUES[k] in (None, '', [], {})]   # **空も欠けと見る**（採否表 P282）
SEAL = runs_B.read_json(a.seal) if a.seal else None
conf_ids = [c['id'] for F in T['families'].values() for c in F['contrasts']]
missing_seal = [] if not SEAL else [i for i in conf_ids if i not in (SEAL.get('signs') or {})]
blockers = []
if missing_tools:
    blockers.append('器材が揃っていない: %s' % '・'.join(missing_tools))
if missing_carry:
    blockers.append('B が依存する凍結物が見つからない: %s' % '・'.join(missing_carry))
if missing_values:
    blockers.append('凍結時に記帳する値が揃っていない: %s' % '・'.join(missing_values))
if SEAL is None:
    blockers.append('封印予想が渡されていない（`seal_format` の様式で、データを一つも見る前に書く）')
else:
    if missing_seal:
        blockers.append('封印の無い確証の対比: %s' % '・'.join(missing_seal))
    if not SEAL.get('s4'):
        blockers.append('**S4 の反証の封印が無い**（正本 seal_format.scope は確証の族と S4 の両方を対象にする）')
    # **予想符号を列挙として検べる**（裁定 D121・採否表 P341）——集計器だけでなく凍結の器でも止める。v3 までは有無しか見ていなかった
    _vals = set(T['seal_format']['sign_values'])
    _bad = sorted({str(v) for v in (SEAL.get('signs') or {}).values() if v not in _vals})
    if _bad:
        blockers.append('封印の予想符号が正本の一覧（seal_format.sign_values）に無い: %s（使える語: %s・裁定 D121）' % ('・'.join(_bad), '・'.join(sorted(_vals))))
    if SEAL.get('s4') and SEAL['s4'] not in _vals:
        blockers.append('S4 の反証の封印が正本の一覧に無い: %s（裁定 D121）' % SEAL['s4'])
    # **正本の鍵の登録から見る**（手書きの並びを置かない・裁定 D115・採否表 P328）
    for need, label in sorted(T['seal_format']['record_keys'].items()):
        if need in ('signs', 's4'):
            continue                      # 上で別に見ている
        if not SEAL.get(need):
            blockers.append('封印の記録に欄が無い: %s（%s・seal_format.record_keys）' % (need, label))
# 整備の記録に載る SHA16 が現物と一致するかを見る（実装検分の採否表 P299——古い記録のまま凍結しない）。
# **止める門の前に置く**（裁定 D112・採否表 P321）。前は門の後ろにあったので、古い記録だけのときに
# 記録が書かれ、しかも「点検であり凍結ではない」と事実でないことを書いていた。
import re as _re
rec_path = os.path.join(REPO, 'records', 'B', 'tooling-record-B-2026-09-18.md')
stale, unlisted = [], []
if os.path.exists(rec_path):
    _txt = open(rec_path, encoding='utf-8').read()
    _listed = dict(_re.findall(r'`tools/([\w.]+)` \| [^|]*\| ([0-9A-F]{16})', _txt))
    for _name, _sha in _listed.items():
        _p = os.path.join(REPO, 'tools', _name)
        if os.path.exists(_p) and runs_B.sha16_file(_p) != _sha:
            stale.append(_name)
    unlisted = [t for t in TOOLS if t not in _listed]
if stale:
    blockers.append('器材の整備の記録の SHA16 が現物と違う（記録を作り直してから凍結する）: %s' % '・'.join(stale))
if unlisted:
    blockers.append('器材の整備の記録に載っていない器材がある（記録に足す）: %s' % '・'.join(unlisted))

if blockers and not a.allow_missing:
    print('[freeze_B] 凍結できない（--allow-missing は点検用）:')
    for b in blockers:
        print('  - ' + b)
    sys.exit(1)

REC = {'kind': 'freeze_B', 'version': VERSION, 'frozen_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'frozen_jst': jst.strftime('%Y-%m-%d %H:%M'),
       'frozen': frozen, 'values': VALUES, 'seal': SEAL, 'seal_sha256': (None if not a.seal else __import__('hashlib').sha256(open(a.seal, 'rb').read()).hexdigest().upper()),
       'stale_record_hashes': stale, 'unlisted_tools': unlisted, 'blockers': blockers, 'deviations': [],
       'deviation_rule': T['deviation']['rule'], 'record_first': T['publication']['record_first']}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 凍結記録（機械生成・`tools/freeze_B.py` %s）' % VERSION, '',
     '- 凍結の時刻: %s UTC（日本時間 %s）。%s' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M'),
                                            ('**点検（--allow-missing）であり凍結ではない**' if a.allow_missing else
                                             ('**止めているものがある——凍結していない**' if blockers else '凍結した。'))), '',
     '## 凍結物', '', '| 物 | 置き場 | SHA16 |', '|---|---|---|']
for k in ('canon', 'draft', 'facts', 'report_template'):
    L.append('| %s | `%s` | %s |' % (k, frozen[k]['path'], frozen[k]['sha16']))
for t, v in sorted(frozen['tools'].items()):
    L.append('| 器材 | `tools/%s` | %s |' % (t, v or '**無い**'))
for name, v in sorted(frozen['carryover'].items()):
    L.append('| 持ち越しの凍結物 | `%s` | %s |' % (v['path'], v['sha16'] or '**無い**'))
for arm, sha in sorted((frozen['arms'] or {}).items()):
    L.append('| 腕 | %s | %s |' % (arm, sha or '（前置きを持たない）'))
L += ['', '## 凍結時に記帳する値', '']
for k in NEED_VALUES:
    L.append('- %s: %s' % (k, json.dumps(VALUES[k], ensure_ascii=False) if k in VALUES else '**まだ無い**'))
L += ['', '## 封印予想（`seal_format`）', '']
if SEAL:
    L += ['- 時機: %s' % T['seal_format']['timing'], '- 情報状態: %s' % T['seal_format']['information_state'],
          '- 封印した符号: %d／確証の対比 %d' % (len(SEAL.get('signs') or {}), len(conf_ids)),
          '- S4 の反証: %s' % (SEAL.get('s4') or '**まだ無い**'), '- %s' % T['seal_format']['reading']]
else:
    L.append('- **まだ無い**（`seal_format` の様式で、データを一つも見る前に書く）')
if blockers:
    L += ['', '## 凍結を止めているもの', ''] + ['- ' + b for b in blockers]
L += ['', '## 逸脱台帳', '', '- %s' % T['deviation']['rule'], '- %s' % T['deviation']['silent_fix'], '- （凍結の後に足す）', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[freeze_B] %s | 止めているもの %d 件' % (out_md, len(blockers)))
sys.exit(2 if blockers else 0)
