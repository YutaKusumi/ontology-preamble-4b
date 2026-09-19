# -*- coding: utf-8 -*-
"""freeze_values_B.py v1 —— 凍結時に記帳する値（`tools/freeze_B.py` の NEED_VALUES）を、**走行の記録と正本から機械で組み立てる**（手で打たない・2026-09-20）。

出どころ:
  - 実重みが要る値（重みの rev・tokenizer の版・総層数と層の添字・腕ごとのトークン長・v̂ の SHA・方向の要約統計・‖v̂‖／‖h‖）
    → 凍結の前の方向の抽出（相 dir）の出力 `results/dirB/dirB__s<n>/freeze-values-dir.json`（正本 `activation_storage.pre_freeze_run.records`）。
  - 品質床の課題と無操作の正答率・問いの前置きの有無・下限の適用 → 正本 `quality_floor.selected`（裁定 D147・D145 の判定の記録から生成器が写したもの）。
  - top_k の実効の値 → 正本 `measured.top_k_stageA_effective`（裁定 D142）。
止める条件: NEED_VALUES に欠けがある／抽出が DRY（乱数の模型）の値／抽出の腕・抽出場面・候補の層が**いまの正本と違う**／決定性 (i) が不一致。
  決定性 (ii) の外れは止めない（記帳して登録者に上げる・正本 `activation_storage.determinism.cross_order`）。
NEED_VALUES は `tools/freeze_B.py` の並びを**構文木から読む**（二重に書かない）。
出力: records/B/freeze-values-B.json（--force が無ければ上書きしない）。凍結の器に `--values` で渡す。
用法: python tools/freeze_values_B.py [--dir-values results/dirB/dirB__s1/freeze-values-dir.json] [--force] ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, ast, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO


def need_values():
    """`tools/freeze_B.py` の NEED_VALUES を構文木から読む（凍結の器と二重に書かない）。"""
    src = open(os.path.join(REPO, 'tools', 'freeze_B.py'), encoding='utf-8').read()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == 'NEED_VALUES' for t in node.targets):
            return list(ast.literal_eval(node.value))
    raise SystemExit('freeze_B.py に NEED_VALUES が見つからない')


def build(T, dv, need=None):
    """dv = 相 dir の freeze-values-dir.json。戻り値: (値の辞書, 出どころの辞書)。止める条件に当たれば SystemExit。"""
    need = need or need_values()
    if dv.get('dry') or dv.get('model_rev') in (None, '', 'dry'):
        raise SystemExit('方向の抽出が DRY（乱数の小さな模型）の値——実重みの走行の出力を渡す')
    if not dv.get('determinism', {}).get('same_order'):
        raise SystemExit('決定性 (i)（同じ並べ方で完全一致）が通っていない値——凍結の値にしない（裁定 D91）')
    QS = T['quality_floor']['selected']
    TK = T['measured']['top_k_stageA_effective']
    acc = {arm: {'correct': QS['base_correct'][arm], 'n_ok': QS['base_n_ok'][arm],
                 'accuracy': QS['base_correct'][arm] / QS['base_n_ok'][arm], 'format_fail': QS['base_format_fail'][arm]}
           for arm in sorted(QS['base_correct'])}
    # 相 dir の値は `.get` で読む——欠けは下の「揃わない」で止める（鍵の欠けで別の落ち方をしない）
    v = {'model_rev': dv.get('model_rev'), 'tokenizer_rev': dv.get('tokenizer_rev'), 'num_hidden_layers': dv.get('num_hidden_layers'),
         'layer_indices': dv.get('layer_indices'), 'arm_token_lengths': dv.get('arm_token_lengths'),
         'quality_task': {k: QS[k] for k in ('key', 'label', 'name', 'input_form', 'fragment_sha16', 'decision_record', 'decision_record_sha16', 'branch')},
         'quality_base_accuracy': acc, 'v_hat_sha256': dv.get('v_hat_sha256'), 'direction_stats': dv.get('direction_stats'),
         'h_norm_ratio': dv.get('h_norm_ratio'), 'top_k_stageA_effective': {'value': TK['value'], 'status': TK['status'], 'source': TK['source']},
         'quality_input_mode': QS['input_form'], 'quality_base_min_applied': {'base_min': QS['base_min_applied'], 'branch': QS['branch'],
                                                                              'fallback_used': QS['base_min_applied'] != T['quality_floor']['base_min']}}
    miss = [k for k in need if k not in v or v[k] in (None, '', [], {})]
    if miss:
        raise SystemExit('凍結時に記帳する値が揃わない: %s' % '・'.join(miss))
    extra = [k for k in v if k not in need]
    if extra:
        raise SystemExit('NEED_VALUES に無い値を作った: %s' % '・'.join(extra))
    src = {'実重みが要る値': '相 dir の走行（%s）' % dv.get('source', '—'),
           '品質床の課題と無操作の正答率・前置きの有無・下限の適用': '正本 quality_floor.selected（裁定 D147・判定の記録 %s）' % QS.get('decision_record'),
           'top_k の実効の値': '正本 measured.top_k_stageA_effective（裁定 D142・%s）' % TK.get('source')}
    return v, src


def check_design_unchanged(T, drec):
    """抽出の腕・抽出場面・候補の層が**いまの正本と同じ**か（違えば凍結の値に使えない）。"""
    bad = []
    if list(drec.get('arms') or []) != list(T['arms']['panel']):
        bad.append('腕の並び')
    if list(drec.get('extraction_scenarios') or []) != list(T['extraction_scenarios']):
        bad.append('抽出場面')
    if sorted((drec.get('layer_indices') or {})) != sorted(str(r) for r in T['selection']['candidates']['layers']):
        bad.append('候補の層')
    return bad


def _selftest():
    T = runs_B.load_T()
    need = need_values()
    assert 'v_hat_sha256' in need and 'quality_task' in need, ('NEED_VALUES を読めていない', need[:3])
    base = {'model_rev': 'A' * 40, 'tokenizer_rev': 'A' * 40, 'num_hidden_layers': 36,
            'layer_indices': {'0.25': 8, '0.5': 17, '0.75': 26}, 'arm_token_lengths': {'O': {'preamble_tokens': 1, 'prompt_tokens': {'N1': 2}}},
            'v_hat_sha256': 'B' * 64, 'direction_stats': {'0.5': {'norms': {}}}, 'h_norm_ratio': {'0.5': {'vhat_over_h': 0.03}},
            'determinism': {'same_order': True, 'cross_order_ok': False}, 'dry': False, 'source': '自己検査'}
    v, src = build(T, dict(base), need)
    assert sorted(v) == sorted(need), ('組み立てた値の鍵が NEED_VALUES と違う', sorted(set(need) ^ set(v)))
    QS = T['quality_floor']['selected']
    a0 = sorted(QS['base_correct'])[0]
    # 正答率は**器を通さずに数え直した値**と照らす（恒真にしない）
    assert abs(v['quality_base_accuracy'][a0]['accuracy'] - QS['base_correct'][a0] / QS['base_n_ok'][a0]) < 1e-12
    assert v['quality_input_mode'] == QS['input_form'] and v['top_k_stageA_effective']['value'] == T['measured']['top_k_stageA_effective']['value']
    assert v['quality_base_min_applied']['fallback_used'] is False, '下限は手当てでない（裁定 D145 の枝 (i)）はず'
    # 止める条件（恒真にしない）
    for name, mut in (('DRY の値', lambda d: d.update(dry=True)), ('rev が dry', lambda d: d.update(model_rev='dry')),
                      ('決定性 (i) の不一致', lambda d: d.update(determinism={'same_order': False})),
                      ('値の欠け', lambda d: d.pop('v_hat_sha256'))):
        d = dict(base)
        mut(d)
        try:
            build(T, d, need)
            raise AssertionError('止まらなかった: %s' % name)
        except SystemExit:
            pass
    # 設計の照合（腕・場面・層）
    ok_rec = {'arms': list(T['arms']['panel']), 'extraction_scenarios': list(T['extraction_scenarios']),
              'layer_indices': {str(r): 0 for r in T['selection']['candidates']['layers']}}
    assert check_design_unchanged(T, ok_rec) == []
    for k, v2 in (('arms', ['O']), ('extraction_scenarios', ['N1']), ('layer_indices', {'0.9': 1})):
        bad = check_design_unchanged(T, dict(ok_rec, **{k: v2}))
        assert bad, ('設計の違いを見落とした: %s' % k)
    print('[freeze_values_B selftest] NEED_VALUES を構文木から読む・値の組み立て（正答率は数え直しと一致）・止める四つ（DRY・rev が dry・決定性 (i)・値の欠け）・'
          '設計の照合（腕・抽出場面・候補の層）: 通った')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--dir-values', default=os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'freeze-values-dir.json'))
    ap.add_argument('--directions', default=None, help='相 dir の directions.json（既定は --dir-values と同じ置き場）')
    ap.add_argument('--out', default=os.path.join(REPO, 'records', 'B', 'freeze-values-B.json'))
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    if os.path.exists(a.out) and not a.force:
        sys.exit('既にある（--force で上書き）: %s' % a.out)
    T = runs_B.load_T()
    dv = runs_B.read_json(a.dir_values)
    dpath = a.directions or os.path.join(os.path.dirname(a.dir_values), 'directions.json')
    drec = runs_B.read_json(dpath)
    bad = check_design_unchanged(T, drec)
    if bad:
        sys.exit('方向を抽出したときの設計と、いまの正本が違う（%s）——抽出をやり直す' % '・'.join(bad))
    v, src = build(T, dv)
    now = datetime.datetime.now(datetime.timezone.utc)
    rec = dict(v, _meta={'kind': 'freeze_values_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
                         'sources': src, 'contrasts_sha16_now': runs_B.sha16_file(runs_B.CPATH),
                         'contrasts_sha16_at_extraction': drec.get('contrasts_sha16'),
                         'direction_run': {'dir_values': os.path.relpath(a.dir_values, REPO).replace('\\', '/'),
                                           'dir_values_sha16': runs_B.sha16_file(a.dir_values),
                                           'directions_json': os.path.relpath(dpath, REPO).replace('\\', '/'),
                                           'directions_json_sha16': runs_B.sha16_file(dpath),
                                           'activations_npz_sha256': dv.get('activations_npz_sha256'),
                                           'determinism': dv.get('determinism'), 'gpu': dv.get('gpu'), 'versions': dv.get('versions')},
                         'fence': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'})
    json.dump(rec, open(a.out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    print('[freeze_values_B] %s（値 %d 件）' % (os.path.relpath(a.out, REPO).replace('\\', '/'), len(v)))
    for k, s in src.items():
        print('  出どころ: %s ← %s' % (k, s))
    if not dv.get('determinism', {}).get('cross_order_ok'):
        print('  **決定性 (ii)（バッチの組成）が許容差の外**——止めないが、凍結の記録と報告に残して登録者に上げる（正本 activation_storage.determinism.cross_order）')
