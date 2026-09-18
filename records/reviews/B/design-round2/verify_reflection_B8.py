# -*- coding: utf-8 -*-
"""verify_reflection_B8.py（2026-09-18）—— 草案8B への反映が、事前登録した対応表のとおりに入ったかを機械で確かめる。

- 読むだけ（リポジトリを書き換えない）。出力は `verification-reflection-B8.{md,json}`。
- 事前登録: `preregistration-reflection-B-round2.md`（反映の作業の前に書き、コミットした）。
- 各項は「正本の鍵の実在」ではなく**中身の語**まで照らす（鍵だけ作って中身を書かない反映を止めるため）。
- 走らせ方: python records/reviews/B/design-round2/verify_reflection_B8.py
"""
import os, re, sys, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
draft = open(os.path.join(REPO, 'design', 'design-stageB-draft8.md'), encoding='utf-8').read()
facts = open(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'), encoding='utf-8').read()
readme = open(os.path.join(REPO, 'README.md'), encoding='utf-8').read()
lint = open(os.path.join(REPO, 'records', 'B', 'numbers-lint-draft8B.md'), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(os.path.join(REPO, rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


def get(path, d=None):
    cur = T
    for k in path.split('.'):
        if isinstance(cur, list):
            cur = cur[int(k)]
        elif isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return d
    return cur


def txt(path, *words):
    v = get(path)
    return bool(v) and all(w in str(v) for w in words)


CONF = [c for F in T['families'].values() for c in F['contrasts']]
DESC = {k: (v.get('contrasts') or []) for k, v in T['descriptive_families'].items()}
clauses = ' / '.join(T['reading_B']['clauses'])
READ_B_SEC = readme.split('## 段階 B')[1].split('\n## ')[0] if '## 段階 B' in readme else ''

CHECKS = [
 ('P212 / D75', 'すべてのランダム方向のノルムを v̂ に合わせる',
  txt('random_control.norm_reference', 'v̂', '族ごとに基準を変えない') and 'Onull+vrandNk' not in json.dumps(T, ensure_ascii=False)
  and 'Nk のノルムに合わせた統制ではない' in clauses),
 ('P213・P214 / D76', '希釈の門（書式外と拒否の差）を本走行と選定に置く',
  txt('dilution_gate.rule', '判定保留', '選定から外す') and get('dilution_gate.threshold_pt') == 10
  and txt('selection.dilution_gate', '書式外率の差', 'refuse 率の差') and '希釈の門' in draft),
 ('P215 / D77', '品質床の不合格の札と走行の順',
  txt('quality_floor.fail_label', '品質床') and txt('quality_floor.fail_rule', '記述に降ろし', 'm は減らさない')
  and any('選定後の品質床' in p for p in T['procedure'])),
 ('P216', '品質床の入力・帯・採点・生成の欄（器材の段で埋める）',
  all(txt('quality_floor.' + k, '器材の段') for k in ('input', 'apply_band', 'scoring')) and get('quality_floor.generation.temperature') == 0),
 ('P217 / D78', '生成の設定を走行の欄に置く',
  all(get('runner.generation.' + k) == v for k, v in (('temperature', 0.7), ('top_p', 0.9), ('max_tokens', 4096)))
  and txt('runner.generation.applies_to', '本走行') and 'runner/generation' in open(os.path.join(REPO, 'design', 'design-stageB-draft8.src.md'), encoding='utf-8').read()),
 ('P218 / D79', '確証族の予想符号の封印',
  all(F.get('sealed_sign') for F in T['families'].values()) and txt('print_strings.sign_agreement', '予想符号')
  and txt('print_strings.label_reverse', '逆') and txt('seal_format.timing', 'データを一つも見る前')),
 ('P219 / D80', 'v̂ 対 td の対比と読み条項',
  len([c for c in DESC['B_desc_textdiff'] if 'vtd' in c['B']]) == 4 and '同じだけ動いた場合' in clauses),
 ('P220', 'ランダム方向 対 無操作の記述',
  len(DESC['B_desc_rand_vs_noop']) == 17 and all(c['B'] in T['arms']['noop'] for c in DESC['B_desc_rand_vs_noop'])),
 ('P221', 'n_ok の定義と §7 の一句の訂正',
  txt('denominators.n_ok', 'api_error', '書式外と refuse を含む') and txt('denominators.note', '対比の数え方')
  and '分母を正本の `denominators` に分けた' not in draft),
 ('P222 / D81', 'S4 の封印の三分岐と検出力',
  txt('descriptive_families.B_desc_S4.adjudication', '当否を言わない') and get('descriptive_families.B_desc_S4.three_way.effect_pt') == 10
  and 'S4 の反証' in facts and '当否を言わない' in facts),
 ('P223 / D82', '前置きの長さの記帳と限界の先置',
  bool(get('position_length.pair_char_diff')) and txt('position_length.decision', '書き換えない')
  and '前置きの長さ' in clauses and bool(get('inventory_excluded.length_matched_arms'))),
 ('P224 / D83', '全候補が非正のときの停止（費用の停止規則）',
  txt('selection.nonpositive_stop', '費用の停止規則', '門1 の判定は変えない') and any('非正' in c or '零以下' in c for c in get('withdrawal.conditions', []))),
 ('P225 / D84', 'ランダム方向の引き直し',
  txt('random_control.redraw', '引き直す') and set(get('seeds.random_dirs', {})) == {'tune', 'main'}
  and get('seeds.random_dirs.tune') != get('seeds.random_dirs.main')),
 ('P226', '三つ組での報告の柵',
  txt('report_rules.triple_reporting', '三つ組', '単独引用')),
 ('P227', 'arms.noop を和集合に揃える',
  set(T['arms']['noop']) == {a for v in T['arms']['noop_by_scenario'].values() for a in v} and len(T['arms']['noop']) == 4),
 ('P228', '同点の割り方の登録',
  txt('selection.tie_break', '無作為') and 'tiebreak' in T['seeds']),
 ('P229', '合成検出力',
  txt('report_rules.combined_power', '積') and '合成の検出力' in facts),
 ('P230', '調整走行と品質床の整合検査・抽出検査',
  any('整合検査' in p and '門1 の前' in p for p in T['procedure'])
  and T['procedure'].index([p for p in T['procedure'] if '整合検査' in p][0]) < T['procedure'].index([p for p in T['procedure'] if p.startswith('門1')][0])),
 ('P231', '同一性選別の腕の一覧・率の定義・出所',
  len(get('identity_screen.arms_run', [])) == 13 and txt('identity_screen.rate_definition', '絶対差')
  and bool(get('identity_screen.compared_sources')) and txt('identity_screen.arms_source', '機械で引く')),
 ('P232・P244', 'seed の降ろし方と調整走行の対比の作り',
  txt('seeds.derivation', '試行の種') and txt('selection.tune.pairing', '独立')),
 ('P233', '重みの rev・tokenizer・層番号の規則',
  'tokenizer の版' in get('runner.fixed_across_runs', []) and txt('runner.fixed_rule', '走行を跨いで')
  and txt('selection.candidates.layer_index_rule', '総層数', '凍結時に記帳')),
 ('P234 / D85', '品質床の基底の条件',
  get('quality_floor.base_min') == 0.5 and txt('quality_floor.base_condition', 'base_min')),
 ('P235', '決定性の許容差・二度保存・バッチの凍結',
  txt('activation_storage.determinism.tolerance', '完全一致') and txt('activation_storage.determinism.material', '二度')
  and txt('activation_storage.determinism.batch_freeze', '凍結')),
 ('P236', '族は独立でない（上界の出し方）',
  '独立でない' in T['fwer_note'] and T['alpha_upper'] == 0.15),
 ('P237', 'v̂ の場面間の安定性',
  txt('directions.static.stability', 'コサイン', '場面ごと')),
 ('P238', '(6a) と負荷下の土台の理由',
  all(txt('families.%s.direction_rationale' % k) for k in T['families'])),
 ('P239', '公開の導線と生成器の版の名',
  ('draft8-2026-09-18' in READ_B_SEC) and (s16('design/contrasts-B.json') in READ_B_SEC)
  and ('23,280' in READ_B_SEC) and ('make_contrasts_B.py` v4' in READ_B_SEC or 'make_contrasts_B.py v4' in READ_B_SEC)),
 ('P240', '選定の向きを結論に印字',
  txt('selection.extrapolation', '加算の土台での低下') and txt('print_strings.selection_direction', '外挿')),
 ('P241', 'バッチの詰めと最終トークンの取り方',
  txt('runner.padding', '左詰め', '詰めでない最後の位置')),
 ('P242', '門の順と札の一意性',
  len(get('gate_order.order', [])) == 6 and txt('gate_order.rule', '最初に当たった門') and txt('gate_order.label_uniqueness', '二つ以上の札を付けない')),
 ('P243', '調整走行のランダム方向の割り当て',
  txt('random_control.allocation', '調整走行')),
 ('P245', '転記行 C の二層の但し書き',
  '場面の二層' in facts),
 ('P246', '降格しても m は減らさない',
  txt('censor.m_rule', 'm は減らさない')),
 ('P247', '調整走行の床・天井の扱い',
  txt('selection.censor', '床', '天井', '選定から外す')),
 ('P248 / S1', '校正の管理図',
  txt('calibration.chart', '管理図') and txt('calibration.limitation', '登録者裁定を要する') and get('calibration.band_pt') == 15),
 ('P249 / S2', '撤退条件',
  len(get('withdrawal.conditions', [])) == 4 and txt('withdrawal.not_a_direction_test', '検定ではない')),
 ('P250 / S3', '中断と再開',
  txt('sessions.resume_rule', '再開') and txt('sessions.commit_rule', '固定のコミット')),
 ('P251 / S4', '費用の停止規則',
  get('cost.stop_rule.multiplier') == 1.25 and txt('cost.stop_rule.text', '本走行の前に登録者')),
 ('P252 / S6', '判定器の妥当性の持ち越しと限界',
  txt('judge_validity.carry_over', '持ち越す') and txt('judge_validity.limitation', '介入のある腕')),
 ('P253 / S8', '逸脱の記帳',
  txt('deviation.rule', 'FREEZE-RECORD') and txt('deviation.silent_fix', '黙って直す')),
 ('P254 / S9', '環境をどの走行で記録するか',
  txt('runner.record_scope', '走行ごと')),
 ('P255 / S11', '予想封印の様式',
  len(get('seal_format.fields', [])) == 5 and txt('seal_format.reading', '較正の証拠にはならない')),
 ('P256', '軽微（品質床の二標本・転記行 I の内訳・N の SHA16・試行の記録の射程）',
  txt('quality_floor.two_sample_note', '二標本') and '内訳と「全腕」の意味' in facts
  and txt('arms.sha16_note', '前置きを持たない') and txt('trial_record_scope', '品質床')),
 ('D86', '次の段取り（器材の実装検分に外の目を置く）',
  '器材の実装検分' in draft and '条件つき' in draft),
 ('反映の検査', '草案8B の数の検査が違反 零',
  '違反の合計: 0' in lint),
 ('反映の検査', '試行数が動いていない（事前登録の予想）',
  '合計 23,280 試行' in facts),
]

ok = [c for c in CHECKS if c[2]]
ng = [c for c in CHECKS if not c[2]]
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
L = ['# 草案8B への反映の確かめ（機械）', '',
     '- 走らせた時刻: %s UTC（日本時間 %s）。器 `verify_reflection_B8.py`（SHA16 %s）。' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M'), s16('records/reviews/B/design-round2/verify_reflection_B8.py')),
     '- 事前登録（反映の前に書いてコミットした）: `preregistration-reflection-B-round2.md`（SHA16 %s）。' % s16('records/reviews/B/design-round2/preregistration-reflection-B-round2.md'),
     '- 対象: 正本（SHA16 %s・%s）／転記行（SHA16 %s）／草案8B（SHA16 %s）／数の検査（SHA16 %s）／README（SHA16 %s）。'
     % (s16('design/contrasts-B.json'), T['version'], s16('records/B/design-facts-B.md'), s16('design/design-stageB-draft8.md'),
        s16('records/B/numbers-lint-draft8B.md'), s16('README.md')),
     '- 結果: **入った %d／%d**。入っていない %d。' % (len(ok), len(CHECKS), len(ng)), '',
     '| 採否・裁定 | 何を確かめたか | 結果 |', '|---|---|---|']
for item, what, res in CHECKS:
    L.append('| %s | %s | %s |' % (item, what, '入った' if res else '**入っていない**'))
L += ['', '本記録のいかなる記述も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'verification-reflection-B8.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
json.dump({'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'canon_sha16': s16('design/contrasts-B.json'),
           'results': [{'item': i, 'what': w, 'ok': bool(r)} for i, w, r in CHECKS]},
          open(os.path.join(HERE, 'verification-reflection-B8.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for item, what, res in CHECKS:
    print('%-14s %-4s %s' % (item, 'OK' if res else 'NG', what))
print('\n[verify-reflection] 入った %d／%d' % (len(ok), len(CHECKS)))
sys.exit(1 if ng else 0)
