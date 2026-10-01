# -*- coding: utf-8 -*-
"""stage_W22_Bprime.py v0（2026-10-01・B′ の結果の段の公開物を公開の置き場に写す・採否の W22・裁定 D284・コーディネータ南無弥勒如来）。
写すもの（バイトのまま・改行も変えない）:
  - Colab の走りの出力（zip を開いたもの）のうち、進みの記録 `progress.log` とセッションの記録 `session.json`（三つの走り）と、行動の下見の生成と採点の出力
    （`behavior-trials.json`・`behavior-scored.json`）→ `results/Bprime/<段>/<走りの名>/`（層三の `results/Bl3/main/<走りの名>/` の型）。
    方向の npz と、公開の置き場に既にある記録（起動の記録・出力の SHA の記録・抽出の記録・読み取りの下見の記録）は写さない。
  - 系統外の模型による採点の束（`items.json`・対応表 `private.json`・依頼の文 `request.md`）と返事（`response.md`・`response-raw.json`・`meta.json`）→ `records/Bprime/behavior/external/`。
  - 器の段の記録の今の版 → `records/Bprime/tools/tools-log-Bprime-after-freeze.md`（公開の写し `tools-log-Bprime.md` は凍結物で書き換えない）。
  - 注 → `results/Bprime/NOTES-Bprime.md`（W22 の注）。写したものの目録 → `records/Bprime/publish-W22-Bprime.json`（置き場・SHA-256・バイト数）。
確かめ: 写す前に、鍵の置き場の値と鍵の形の字が無いことを `check_secrets_Bprime.py` の関数で照らす（当たりがあれば何も写さずに止める）。写した後に、写しと元の SHA-256 を照らす。
  写す先に既に違う中身のファイルがあれば止める（同じ中身なら写さない）。目録と注は一度だけ書く（既にあれば止める）。
用法: python stage_W22_Bprime.py [--root <公開の置き場の代わりの置き場（試し）>]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, shutil, argparse, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(HERE)
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
sys.path.insert(0, HERE)
import check_secrets_Bprime as CS          # この import が標準出力を UTF-8 で包む（ここで二度包むと、前の包みが閉じて書けなくなる）
sys.stdout.reconfigure(encoding='utf-8')
NL = chr(10)
RUNS = {'extract': 'extract-run-20261001T040457Z', 'behavior': 'behavior-run-20261001T042902Z', 'pilot': 'pilot-run-20261001T050942Z'}
SRC_RUN = {'extract': 'records/Bprime/extract-run', 'behavior': 'records/Bprime/behavior-run', 'pilot': 'records/Bprime/pilot-run'}
FILES_RUN = {'extract': ['progress.log', 'session.json'], 'behavior': ['progress.log', 'session.json', 'behavior-trials.json', 'behavior-scored.json'], 'pilot': ['progress.log', 'session.json']}
EXT = ['bundle/items.json', 'bundle/private.json', 'bundle/request.md', 'reply/response.md', 'reply/response-raw.json', 'reply/meta.json']
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
sha = lambda b: hashlib.sha256(b).hexdigest().upper()


def plan():
    out = []
    for ph, rd in RUNS.items():
        for fn in FILES_RUN[ph]:
            out.append(('%s/%s/%s' % (SRC_RUN[ph], rd, fn), 'results/Bprime/%s/%s/%s' % (ph, rd, fn)))
    for f in EXT:
        out.append(('records/Bprime/behavior-run/external/%s' % f, 'records/Bprime/behavior/external/%s' % f))
    out.append(('tools/tools-log-Bprime.md', 'records/Bprime/tools/tools-log-Bprime-after-freeze.md'))
    return out


def notes():
    return NL.join([
        '# B′ の結果の段の公開物の注（採否の W22・裁定 D284・2026-10-01・コーディネータ南無弥勒如来）', '',
        '- `results/Bprime/<段>/<走りの名>/` のファイルは、Colab の走りの出力の zip から写したもので、バイトのまま（改行も変えていない）。起動の記録と出力の SHA の記録は `records/Bprime/runs/`、'
        '抽出の記録は `records/Bprime/extract/`、読み取りの下見の記録は `records/Bprime/pilot/` にある。方向の npz（相 extract の出力）は公開しない。画面の写しと会話の記録の全体も公開しない。',
        '- 進みの記録とセッションの記録の中の `/content/…` は Colab のランタイムの中の置き場の名。鍵や認証の字が無いことは、写す前に機械で確かめた（`records/Bprime/tools/check_secrets_Bprime.py`・当たり 0）。',
        '- 行動の下見（`results/Bprime/behavior/`）は無操作だけで、標本化は段階 B の値（Gemma の既定ではない）、升目ごとの試行は 40。率は記述で、升目の間の比べに検定を掛けない。'
        '採点器の妥当性は Gemma の応答で確かめていない。',
        '- 「破局」は架空の場面の採点の名で、族ごとの定義は正本 `behavior_pilot.external_scoring.request_text` の定義の三つ目（survival）と四つ目（nuclear）にある。',
        '- 採点の出力の補助の欄（name_mention・test_mention・loop）は正本に定義が無く、読まない。',
        '- 系統外の模型による採点の束（`records/Bprime/behavior/external/bundle/`）は、升目を伏せた応答 40 件（`items.json`）・対応表（`private.json`）・依頼の文（`request.md`）で、'
        '返事は `records/Bprime/behavior/external/reply/`。採点の一致は一致の記述で、採点器の妥当性の測定ではない。採点した模型は、結果の巡と最終検分の系統外の票と同じ機種（grok-4.7）で、見逃しが相関しうる。',
        '- 器の段の記録の公開の写し `records/Bprime/tools/tools-log-Bprime.md` は凍結物なので書き換えず、凍結の後の行を含む今の版を `records/Bprime/tools/tools-log-Bprime-after-freeze.md` に置いた。',
        '', CLAUSE, ''])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    a = ap.parse_args()
    root = a.root or PUB
    pl = plan()
    srcs = [os.path.join(BP, *s.split('/')) for s, _ in pl]
    vals = CS.values()
    bad = []
    for p in srcs:
        b = open(p, 'rb').read()
        t = b.decode('utf-8', errors='replace')
        if any(v in t for v in vals) or [k for k, rx in CS.PAT.items() if rx.search(t)]:
            bad.append(os.path.relpath(p, BP))
    if bad:
        raise SystemExit('鍵か鍵の形の字に当たった（何も写さない）: %s' % bad)
    rows = []
    for (s, d), sp in zip(pl, srcs):
        b = open(sp, 'rb').read()
        dp = os.path.join(root, *d.split('/'))
        if os.path.exists(dp):
            if open(dp, 'rb').read() != b:
                raise SystemExit('写す先に違う中身のファイルがある（止める）: %s' % d)
        else:
            os.makedirs(os.path.dirname(dp), exist_ok=True)
            shutil.copyfile(sp, dp)
        if sha(open(dp, 'rb').read()) != sha(b):
            raise SystemExit('写しと元の SHA-256 が違う（止める）: %s' % d)
        rows.append({'from': '（作業の置き場）' + s, 'to': d, 'sha256': sha(b), 'bytes': len(b)})
    np_ = os.path.join(root, 'results', 'Bprime', 'NOTES-Bprime.md')
    mp = os.path.join(root, 'records', 'Bprime', 'publish-W22-Bprime.json')
    for p in (np_, mp):
        if os.path.exists(p):
            raise SystemExit('既にある（一度だけ）: %s' % p)
    nt = notes()
    open(np_, 'w', encoding='utf-8', newline=NL).write(nt)
    man = {'kind': 'bprime_publish_W22', 'tool': 'records/Bprime/tools/stage_W22_Bprime.py v0', 'ruling': 'D284（採否の W22）',
           'time_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
           'secret_check': {'tool': 'records/Bprime/tools/check_secrets_Bprime.py v0', 'files': len(srcs), 'env_values_compared': len(vals), 'hits': 0},
           'files': rows, 'notes': {'to': 'results/Bprime/NOTES-Bprime.md', 'sha256': sha(nt.encode('utf-8'))},
           'not_published': ['方向の npz（相 extract の出力）', '画面の写し', '会話の記録の全体'], 'clause': CLAUSE}
    with open(mp, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1)
    print('写した %d・注と目録を書いた（%s）・鍵の照らしの当たり 0' % (len(rows), root))


if __name__ == '__main__':
    main()
