# -*- coding: utf-8 -*-
"""flow_D.py v0（2026-10-14・段階 E の E3・章 5 の言語ごとの機種の流れの数〔枠 §4 の「機種の流れ」・EF1-16〕を、公開の二つの凍結の本文の表から機械で数える器・コーディネータ南無弥勒如来）。
枠 §5 の新しい計算ではない: 統計の値を作らず、凍結の本文の表に書かれた決め（候補・余地が無い・計器が読めない・外した・本走行の場面）を数えるだけ。値は起草者が表で見ている。
読むもの（名指し・封の置き場は読まない）: 公開の置き場の records/D1p/00-frame-D1p.md（§0 の系統の表 17〜26 行・連なりの表 31〜40 行・候補の決め方 15 行・§4 の機種の表 91〜100 行）と records/D1pE/00-frame-D1pE.md（§0 の表 18〜27 行・§4 の機種の表 100〜105 行）と、二つの公開の集計の json（族の大きさの照らし）。
書く物（一度だけ）: E/E3/calc/flow/flow-D.json・flow-D-record.md。日本語の送る文の登録と英語の送る文の登録の数は、別の鍵（ja・en）に置く（判定ラベルから数えた数ではない・設計の数）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
PUB = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'flow')
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
sha = lambda b: hashlib.sha256(b).hexdigest().upper()
read = {}


def lines_of(rel):
    b = open(os.path.join(PUB, *rel.split('/')), 'rb').read()
    read[rel] = sha(b)
    return b.decode('utf-8').replace('\r\n', '\n').split('\n')


def cells(line):
    assert line.startswith('|') and line.endswith('|'), line[:40]
    return [c.strip() for c in line[1:-1].split('|')]


def kind_ja(s):
    if s.startswith('本走行の候補'):
        return 'candidate'
    if s.startswith('余地が無い'):
        return 'no_headroom'
    if s.startswith('計器が読めない'):
        return 'measurement_failure'
    raise ValueError(s)


def main():
    assert not os.path.exists(OUT), ('一度だけ', OUT)
    J = lines_of('records/D1p/00-frame-D1p.md')
    E = lines_of('records/D1pE/00-frame-D1pE.md')
    cj = json.loads(open(os.path.join(PUB, 'records', 'D1p', 'confirm', 'confirm-D1p.json'), 'rb').read().decode('utf-8'))
    ce = json.loads(open(os.path.join(PUB, 'records', 'D1pE', 'confirm', 'confirm-D1pE.json'), 'rb').read().decode('utf-8'))
    read['records/D1p/confirm/confirm-D1p.json'] = sha(open(os.path.join(PUB, 'records', 'D1p', 'confirm', 'confirm-D1p.json'), 'rb').read())
    read['records/D1pE/confirm/confirm-D1pE.json'] = sha(open(os.path.join(PUB, 'records', 'D1pE', 'confirm', 'confirm-D1pE.json'), 'rb').read())
    # 日本語の送る文の登録（D1′）: 系統の表
    assert J[16].startswith('| 系統 | 古い版 | 古い版の決め'), J[16][:40]
    rows = [cells(J[i]) for i in range(18, 26)]
    assert len(rows) == 8 and J[26] == '', J[26][:20]
    models = []
    for r in rows:
        models.append({'lineage': r[0], 'version': 'old', 'model': r[1], 'kind': kind_ja(r[2])})
        models.append({'lineage': r[0], 'version': 'new', 'model': r[3], 'kind': kind_ja(r[4])})
    # 連なり（Qwen の古い版）: 表の古い版は連なりの二つ目。一つ目と元の版は連なりの表と 28 行から
    assert '7B が「計器が読めない」' in J[39] and '3B は許諾で外し' in J[39] and '32B が候補' in J[39], J[39][:60]
    assert 'Qwen2.5-Coder-7B が「計器が読めない」' in J[27] and '連なりの一つ目の Qwen2.5-Coder-3B は候補になったが許諾' in J[27], J[27][:60]
    chain = [{'lineage': 'Alibaba（Qwen）', 'version': 'old', 'model': 'Qwen2.5-Coder-7B-Instruct', 'kind': 'measurement_failure'},
             {'lineage': 'Alibaba（Qwen）', 'version': 'old', 'model': 'Qwen2.5-Coder-3B-Instruct', 'kind': 'license_excluded'}]
    assert '十二系統のうち四つの系統は' in J[14] and '残る八系統' in J[14], J[14][:40]
    # 本走行の機種の表（§4）
    assert J[88].startswith('| 系統 | 役 | 機種 | 機種名 |'), J[88][:40]
    mrows = [cells(J[i]) for i in range(90, 100)]
    assert J[100] == '', J[100][:20]
    ja_cells = sum(len(r[9].split('・')) for r in mrows)
    allm = models + chain
    cnt = lambda L, k: sum(1 for x in L if x['kind'] == k)
    ja = {'lineages_listed': 12, 'lineages_not_candidate': 4, 'lineages_in_table': len(rows),
          'models_in_lineage_table': len(models), 'chain_models_added': len(chain), 'models_with_calibration_decision': len(allm),
          'candidates': cnt(allm, 'candidate'), 'no_headroom': cnt(allm, 'no_headroom'), 'measurement_failure': cnt(allm, 'measurement_failure'),
          'license_excluded': cnt(allm, 'license_excluded'), 'not_measured': cnt(allm, 'no_headroom') + cnt(allm, 'measurement_failure'),
          'main_models': len(mrows), 'main_cells': ja_cells, 'trials_per_condition': 200, 'main_trials': ja_cells * 800,
          'models': allm}
    assert ja['candidates'] == ja['main_models'], ja
    assert ja_cells == cj['family_P_m'] and 2 * ja_cells == cj['family_A_m'], (ja_cells, cj['family_P_m'])
    assert '29 升で合わせて 23,200 試行' in J[112], J[112][:60]
    # 英語の送る文の登録（D1′E）: §0 の表
    assert E[15].startswith('| 系統 | 機種 | 役 | 英語版の決め |'), E[15][:40]
    erows = [cells(E[i]) for i in range(17, 27)]
    assert E[27] == '', E[27][:20]

    def kind_en(s):
        if s.startswith('本走行に進む'):
            return 'main'
        if s.startswith('外した（口から下ろされた'):
            return 'unavailable'
        if s.startswith('読解の確かめで外れた'):
            return 'reading_check_failed'
        if s.startswith('余地が無い'):
            return 'no_headroom'
        raise ValueError(s)
    emodels = [{'lineage': r[0], 'model': r[1], 'version': r[2], 'kind': kind_en(r[3]), 'scenes_en': r[4]} for r in erows]
    assert E[97].startswith('| 系統 | 役 | 機種 | 機種名 |'), E[97][:40]
    emrows = [cells(E[i]) for i in range(99, 105)]
    assert E[105] == '', E[105][:20]
    en_cells = sum(len(r[9].split('・')) for r in emrows)
    en = {'candidates': len(emodels), 'unavailable': cnt(emodels, 'unavailable'), 'reading_check_failed': cnt(emodels, 'reading_check_failed'),
          'no_headroom': cnt(emodels, 'no_headroom'), 'not_measured': cnt(emodels, 'reading_check_failed') + cnt(emodels, 'no_headroom'),
          'reading_check_takers': len(emodels) - cnt(emodels, 'unavailable'),
          'reading_check_passed': len(emodels) - cnt(emodels, 'unavailable') - cnt(emodels, 'reading_check_failed'),
          'main_models': len(emrows), 'main_cells': en_cells, 'trials_per_condition': 200, 'main_trials': en_cells * 800, 'models': emodels}
    assert en['main_models'] == cnt(emodels, 'main'), en
    assert en_cells == ce['family_P_m'] and 2 * en_cells == ce['family_A_m'], (en_cells, ce['family_P_m'])
    assert '12 升で合わせて 9,600 試行' in E[114], E[114][:60]
    assert '七機種が通り、二機種が外れた' in E[13] and '六機種が本走行の候補になった' in E[13], E[13][:40]
    assert en['reading_check_passed'] == 7 and en['reading_check_failed'] == 2 and en['main_models'] == 6
    os.makedirs(OUT)
    me = sha(open(os.path.abspath(__file__), 'rb').read())
    now = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
    res = {'tool': 'flow_D.py v0', 'tool_sha256': me, 'when_jst': now, 'kind': 'design（凍結の本文の表の決めを数えた・判定ラベルから数えた数ではない）',
           'sources_sha256': read, 'ja': ja, 'en': en, 'clause': CLAUSE}
    p = os.path.join(OUT, 'flow-D.json')
    json.dump(res, open(p, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    R = ['# 機種の流れの数（%s 日本時間・器 `E/E3/calc/flow_D.py` v0・SHA16 %s）' % (now, me[:16]), '',
         '- 種別: 設計（凍結の本文の表の決めを数えた・判定ラベルから数えた数ではない・枠 §4 の機種の流れ）。',
         '- 日本語の送る文の登録（D1′）: 系統 %d（候補にしなかった系統 %d・表の系統 %d）・表の機種 %d と連なりで足した機種 %d（較正の決めのある機種 %d）・候補 %d・余地が無い %d・計器が読めない %d・許諾で外した %d・本走行 %d 機種 %d 升 %d 試行。' % (
             ja['lineages_listed'], ja['lineages_not_candidate'], ja['lineages_in_table'], ja['models_in_lineage_table'], ja['chain_models_added'], ja['models_with_calibration_decision'],
             ja['candidates'], ja['no_headroom'], ja['measurement_failure'], ja['license_excluded'], ja['main_models'], ja['main_cells'], ja['main_trials']),
         '',
         '- 英語の送る文の登録（D1′E）: 候補 %d・口から下ろされた %d・読解の確かめで外れた %d・余地が無い %d・本走行 %d 機種 %d 升 %d 試行。' % (
             en['candidates'], en['unavailable'], en['reading_check_failed'], en['no_headroom'], en['main_models'], en['main_cells'], en['main_trials']),
         '', '- 読んだ記録の SHA-256: ' + '・'.join('`%s` %s' % (k, v[:16]) for k, v in read.items()),
         '- 出力 `flow-D.json` SHA-256 %s' % sha(open(p, 'rb').read()), '', CLAUSE, '']
    open(os.path.join(OUT, 'flow-D-record.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))
    print(NL.join(R))


if __name__ == '__main__':
    main()
