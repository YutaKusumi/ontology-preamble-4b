# -*- coding: utf-8 -*-
"""freeze_A.py v2 —— 段階 A の凍結マニフェストを発行・検証する（発行は登録者の凍結指示があってから・2026-09-13 整備・登録者裁定 D9 の三つ目の手順）。
v2（2026-09-14・実装検分の採否表 P98）: 走行器の refuse の規則と語彙・起動時の台帳（F・M）・転記行 F と G の入力・運用の解釈の一覧・名の語彙の出所（response_mode_M.py・F）を凍結範囲に加える。凍結本文の原稿は凍結本文の名（.md を .src.md に）から決める。枠の検証は見出しの名の完全一致（各枠ちょうど一つ）にする。
凍結範囲（FILES）: 凍結本文・正本と生成器・確証と帯と読み出しの共通関数・Firth の基準実装と一致検査・格子と設計事実とその出力・本文の数の検査と組み立て器・走行器と起動器・
  門・集計・様式・整合・抽出・断片・管理図の器・合成検査とその記録・報告の組み立て器と走査器・報告雛形（原稿と組み立て）・機種の記録・盤の台帳と凍結物の写し（前置き・場面・パーサ）・
  門0.5 と Firth の一致検査の記録・凍結器。
発行の前に、報告雛形に正本 report_rules.frames の枠の見出しがすべて実在することを機械検証する（無ければ発行しない・frames_rule）。
出力: records/freeze-A-<日付>.json（同名があれば連番・上書きなし）。--verify <manifest> で現物と突合（不一致は非零終了）。SHA16 はファイルバイトの SHA-256 先頭 16 桁（CRLF→LF 正規化・strip なし）。
用法: python tools/freeze_A.py --design design/design-stageA-FROZEN.md [--check]（--check は発行せずに一覧・欠け・枠の検証だけを印字）
      python tools/freeze_A.py --verify records/freeze-A-<日付>.json
      python tools/freeze_A.py --verify-public records/freeze-A-<日付>.json --commit <公開のコミットの完全な SHA または main>（公開物の照合・採否表 P107）
v3（2026-09-14・凍結前の最終検分の採否表 P107・P131）: 発行の前に共有関数と検査器の自己検査（SELFTESTS）を走らせ、合否と器の SHA16 をマニフェストに書く。凍結本文の §6 の見出しの正本 SHA16 と現物が違えば発行しない。
  --check は欠けがあれば終了コード 2。公開物の照合（--verify-public）を足した。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, argparse, datetime, subprocess, time, hashlib, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v3'   # v3（2026-09-14・凍結前の最終検分の採否表 P107・P131）: 発行の前に自己検査を走らせて合否を記帳・凍結本文の正本 SHA16 と現物の一致・--check の欠けは終了コード 2・公開物の照合（--verify-public）
PUBLIC_RAW = 'https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b'
SELFTESTS = [('confirm_A.py', ['--selftest']), ('firth.py', ['--selftest']), ('bands_A.py', ['--selftest']), ('numbers_lint.py', ['--selftest']), ('report_lint.py', ['--selftest']),
             ('judge_fragments_A.py', ['selftest']), ('sample_inspection_A.py', ['selftest'])]
TOOLS = ['make_contrasts_A.py', 'confirm_A.py', 'bands_A.py', 'runs_A.py', 'zaxis_A.py', 'firth.py', 'firth_check_A.py', 'firth_check_A.R', 'power_grid_A.py', 'design_facts_A.py', 'numbers_lint.py', 'build_draftA.py',
         'run_preamble_local.py', 'colab/boot_stageA.py', 'identity_screen_A.py', 'gate_A.py', 'calib_band_A.py', 'control_chart_A.py', 'analyze_A.py', 'response_mode_A.py', 'integrity_A.py',
         'sample_inspection_A.py', 'judge_fragments_A.py', 'synth_A.py', 'synth_gates_A.py', 'build_report_A.py', 'report_lint.py', 'freeze_A.py', 'cost_facts.py', 'response_mode_M.py', 'response_mode_F.py',
         'tooling_interpretations_A.py']
RECORDS = ['design/contrasts-A.json', 'records/A/power-grid-A.json', 'records/A/power-grid-A.md', 'records/A/design-facts-A.json', 'records/A/design-facts-A.md', 'records/A/hf-models-A.json',
           'records/A/results-report-template-A.src.md', 'records/A/results-report-template-A.md', 'records/A/identity-screen-A.json', 'records/A/identity-screen-A.md', 'records/A/firth-check-A.json', 'records/A/firth-check-A.md',
           'arms/panel/SHA-LEDGER.json', 'arms/frozen-from-ryokai-os/app-scenarios.json', 'arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py',
           'arms/frozen-from-ryokai-os/armsE/preamble-O.md', 'arms/frozen-from-ryokai-os/armsE/preamble-Onull.md', 'arms/frozen-from-ryokai-os/armsE/preamble-Lneg.md', 'design/contrasts-F.json',
           'arms/materials-draft/hei/refuse-rules-v2.json', 'arms/materials-draft/hei/incentive-lexicon-v2.json', 'arms/panelF/SHA-LEDGER-F.json', 'arms/panelM/SHA-LEDGER-M.json',
           'records/F/style-stageF1.json', 'records/A/tooling-interpretations-A.md']   # 走行器の語彙と refuse の規則・起動時の台帳・転記行 G の入力・運用の解釈の一覧（採否表 P98）
GLOBS = ['records/A/synth-A-*.json', 'records/A/synth-A-*.md', 'records/A/synth-gates-A-*.json', 'records/A/synth-gates-A-*.md', 'records/A/numbers-lint-*A*.md']


def rel(p):
    return p.replace('\\', '/')


def file_list(design):
    src = (design[:-3] if design.endswith('.md') else design) + '.src.md'   # 凍結本文の原稿は凍結本文の名から決める（採否表 P98）
    T = runs_A.load_T()
    cost = re.search(r'records/[\w\-./]+\.md', T['cost']['source']).group(0)   # 転記行 F の入力
    fs = [design, src] + ['tools/' + t for t in TOOLS] + RECORDS + [cost]
    fs += ['arms/panel/%s.md' % a for a in T['arms']['preamble'] if a not in ('N', 'O', 'Onull', 'Lneg')]
    for g in GLOBS:
        fs += sorted(rel(os.path.relpath(p, REPO)) for p in glob.glob(os.path.join(REPO, g)))
    seen = set(); out = []
    for f in fs:
        if f not in seen:
            seen.add(f); out.append(f)
    return out


def frames_check(T):
    tp = os.path.join(REPO, T['report_rules']['template'])
    if not os.path.exists(tp):
        return ['雛形が無い: %s' % T['report_rules']['template']]
    names = [re.sub(r'（.*$', '', l.lstrip('#').strip()).strip() for l in open(tp, encoding='utf-8').read().split('\n') if l.startswith('#')]   # 見出しの名（最初の全角括弧の前）の完全一致（採否表 P98）
    return ['枠の見出しが%s: %s（完全一致 %d 件）' % ('無い' if names.count(f) == 0 else '重複', f, names.count(f)) for f in T['report_rules']['frames'] if names.count(f) != 1]


def run_selftests():
    """発行の前に共有関数と検査器の自己検査を走らせる（採否表 P107）。"""
    out = []
    for nm, args in SELFTESTS:
        p = subprocess.run([sys.executable, os.path.join(REPO, 'tools', nm)] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1'))
        out.append({'tool': nm, 'sha16': runs_A.sha16_file(os.path.join(REPO, 'tools', nm)), 'args': args, 'rc': p.returncode, 'tail': ((p.stdout or '') + (p.stderr or '')).strip()[-240:]})
    return out


def design_spec_sha16(design):
    """凍結本文の §6 の見出しに組み立て器が書いた正本の SHA16。"""
    m = re.search(r'`design/contrasts-A\.json`〔SHA16 ([0-9A-F]{16})〕', open(os.path.join(REPO, design), encoding='utf-8').read())
    return m.group(1) if m else None


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--design', default='design/design-stageA-FROZEN.md'); ap.add_argument('--verify', default=None); ap.add_argument('--check', action='store_true')
    ap.add_argument('--verify-public', default=None); ap.add_argument('--commit', default=None)
    a = ap.parse_args()
    if a.verify_public:
        if not (a.commit and (re.fullmatch(r'[0-9a-f]{40}', a.commit) or a.commit == 'main')):
            sys.exit('--verify-public には --commit に完全な SHA か main を与える（採否表 P107 はコミットと main の両方を照合する）')
        MF = runs_A.read_json(a.verify_public); bad = []
        for f, want in MF['files'].items():
            try:
                got = hashlib.sha256(urllib.request.urlopen('%s/%s/%s' % (PUBLIC_RAW, a.commit, urllib.parse.quote(f)), timeout=60).read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
            except Exception as ex:
                got = 'ERR %s' % str(ex)[:60]
            if got != want:
                bad.append((f, want, got))
            time.sleep(0.2)
        print('[freeze_A --verify-public] コミット %s の公開物 %d/%d 一致' % (a.commit[:12], len(MF['files']) - len(bad), len(MF['files'])))
        for b in bad:
            print('  不一致: %s 凍結 %s 公開 %s' % b)
        sys.exit(1 if bad else 0)
    if a.verify:
        MF = runs_A.read_json(a.verify); bad = []
        for f, want in MF['files'].items():
            p = os.path.join(REPO, f)
            got = runs_A.sha16_file(p) if os.path.exists(p) else None
            if got != want:
                bad.append((f, want, got))
        print('[freeze_A --verify] %d/%d 一致' % (len(MF['files']) - len(bad), len(MF['files'])))
        for b in bad:
            print('  不一致: %s 凍結 %s 現物 %s' % b)
        sys.exit(1 if bad else 0)
    T = runs_A.load_T(); files = file_list(a.design); missing = [f for f in files if not os.path.exists(os.path.join(REPO, f))]; fr = frames_check(T)
    print('[freeze_A] 対象 %d・欠け %d・枠の検証 %s' % (len(files), len(missing), '一致' if not fr else '・'.join(fr)))
    for m in missing:
        print('  欠け: %s' % m)
    if a.check:
        if missing:
            print('  欠けがあるので発行はできない（採否表 P131）')
        sys.exit(1 if fr else (2 if missing else 0))
    if missing or fr:
        sys.exit('欠けまたは枠の不一致があるので発行しない')
    DSHA = design_spec_sha16(a.design); CSHA = runs_A.sha16_file(runs_A.CPATH)
    if DSHA != CSHA:
        sys.exit('凍結本文に書かれた正本の SHA16 %s と現物の %s が違うので発行しない（採否表 P107）' % (DSHA, CSHA))
    ST = run_selftests(); STBAD = [s for s in ST if s['rc'] != 0]
    if STBAD:
        sys.exit('自己検査が通らない器があるので発行しない: %s' % '・'.join('%s（rc %d）' % (s['tool'], s['rc']) for s in STBAD))
    stamp = datetime.date.today().isoformat(); p = os.path.join(REPO, 'records', 'freeze-A-%s.json' % stamp); k = 2
    while os.path.exists(p):
        p = os.path.join(REPO, 'records', 'freeze-A-%s-%d.json' % (stamp, k)); k += 1
    MF = {'kind': 'freeze_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'design': a.design, 'sha16_rule': 'SHA-256 の先頭 16 桁（CRLF→LF 正規化・strip なし）',
          'files': {f: runs_A.sha16_file(os.path.join(REPO, f)) for f in files}, 'frames_checked': T['report_rules']['frames'], 'design_contrasts_sha16': DSHA, 'selftests': ST,
          'public_check': '凍結の公開の後に python tools/freeze_A.py --verify-public <このマニフェスト> --commit <公開のコミットの完全な SHA> と --commit main の二度で公開物を照合し、結果を凍結記録に書く（採否表 P107）',
          'clause': '本マニフェストのいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    json.dump(MF, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    print('[freeze_A] written %s（%d ファイル）' % (p, len(MF['files'])))
