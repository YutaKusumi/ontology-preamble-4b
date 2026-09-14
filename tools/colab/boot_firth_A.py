# -*- coding: utf-8 -*-
"""boot_firth_A.py v1 —— 段階 A の Firth の一致検査（R logistf と tools/firth.py）を Colab の CPU ランタイムで走らせる起動スクリプト（2026-09-14・正本 firth_check.run・登録者裁定 D14・D33）。
運用: コーディネータが登録者の Chrome 越しに Colab を操作する。登録者の手に残すのは Drive 接続の OAuth 同意・ローカルへのダウンロードの許可・プランと支払い。資格情報は入力しない。
セルに打つのは一行だけ（先頭の下線は type が先頭十数字を落とす事故の緩衝・<commit> は 40 桁）:
    ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_firth_A.py').read().decode('utf-8'))
手順:
 (1) Drive の接続（許可は登録者）→ リポジトリをコミット固定で取り出す（tools・design・records/A の sparse checkout）→ 取り出した HEAD がコミットと一致することを確かめる。
 (2) 登録の命令 python tools/firth_check_A.py --install をそのまま走らせる（R と logistf を入れる・合否規則と許容差は正本 firth_check・本器は規則に触れない）。標準出力と標準エラーは Drive のログに書く。
 (3) 終了コードに依らず、records/A/firth-check-A.{json,md} と作業置き場（合成データ・r_results.csv・r_session.txt・同梱データの CSV）を Drive に写し、
     セッション記録（コミット・終了コード・Python と R と logistf と apt の r-base-core と numpy と scipy の版・pip freeze の SHA16・時刻・ファイルの SHA16）を書き、zip にする。
 合否は記録の判定欄（firth_check_A.py）が決める。R や logistf の導入に失敗した場合もログとセッション記録と zip を残す（正本 firth_check.failure_options の（一））。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, time, subprocess, datetime, hashlib, shutil

T0 = time.time(); COMMIT = os.environ.get('OP4B_COMMIT', ''); LOG = []
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'; REPO = '/content/ontology-preamble-4b'
BASE = '/content/drive/MyDrive/op4b-stageA'; PERSIST = os.path.join(BASE, 'firth-check')
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
sha16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


def mark(step, **kw):
    LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw)); print('[boot_firth] %-10s %6.0fs %s' % (step, time.time() - T0, kw or ''), flush=True)


def sh(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-4000:]); raise RuntimeError('失敗: %s' % ' '.join(cmd))
    return r


def out(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout.strip()
    except Exception as ex:
        return 'ERR %s' % str(ex)[:80]


if not re.fullmatch(r'[0-9a-f]{40}', COMMIT):
    sys.exit('[boot_firth] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える')
print('[boot_firth] 段階 A Firth の一致検査 boot v1 開始 commit=%s' % COMMIT[:12], flush=True)
# ---- 1. Drive とリポジトリ
if not os.path.isdir('/content/drive/MyDrive'):
    print('[boot_firth] Drive の接続を求めます——「Google ドライブに接続」の許可は登録者が押してください', flush=True)
    from google.colab import drive
    drive.mount('/content/drive')
os.makedirs(PERSIST, exist_ok=True)
shutil.rmtree(REPO, ignore_errors=True)
sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO]); sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone', 'tools', 'design', 'records/A']); sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
HEAD = sh(['git', '-C', REPO, 'rev-parse', 'HEAD']).stdout.strip()
if HEAD != COMMIT:
    sys.exit('[boot_firth] 取り出したコミット %s が OP4B_COMMIT %s と違う' % (HEAD, COMMIT))
mark('repo', head=HEAD[:12], persist=PERSIST)
# ---- 2. 登録の命令（python tools/firth_check_A.py --install）
WORK = os.path.join(REPO, 'records', 'A', 'firth-check-work'); LOGP = os.path.join(PERSIST, 'firth-check-run.log')
with open(LOGP, 'w', encoding='utf-8') as lf:
    lf.write('[boot_firth] command: %s tools/firth_check_A.py --install (cwd %s) started %s\n' % (sys.executable, REPO, now())); lf.flush()
    rc = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'firth_check_A.py'), '--install'], cwd=REPO, stdout=lf, stderr=subprocess.STDOUT).returncode
mark('check', rc=rc)
print(open(LOGP, encoding='utf-8', errors='replace').read()[-3000:], flush=True)
# ---- 3. 版・写し・セッション記録・zip
import importlib.metadata as md


def pv(k):
    try:
        return md.version(k)
    except Exception:
        return None


VER = {'python': sys.version.split()[0], 'numpy': pv('numpy'), 'scipy': pv('scipy'), 'r_base_core_apt': out(['dpkg-query', '-W', '-f=${Version}', 'r-base-core']),
       'R': out(['Rscript', '-e', 'cat(R.version.string)']), 'logistf': out(['Rscript', '-e', 'cat(as.character(packageVersion("logistf")))']),
       'pip_freeze_sha16': hashlib.sha256(out([sys.executable, '-m', 'pip', 'freeze']).encode('utf-8')).hexdigest()[:16].upper()}
mark('versions', **VER)
DST = os.path.join(PERSIST, 'records-A'); shutil.rmtree(DST, ignore_errors=True); os.makedirs(DST)
FILES = {}
for nm in ('firth-check-A.json', 'firth-check-A.md'):
    sp = os.path.join(REPO, 'records', 'A', nm)
    if os.path.exists(sp):
        shutil.copyfile(sp, os.path.join(DST, nm)); FILES['records/A/' + nm] = sha16(sp)
if os.path.isdir(WORK):
    shutil.copytree(WORK, os.path.join(DST, 'firth-check-work'))
    for f in sorted(os.listdir(WORK)):
        if os.path.isfile(os.path.join(WORK, f)):
            FILES['records/A/firth-check-work/' + f] = sha16(os.path.join(WORK, f))
SREC = {'kind': 'firth_check_session_A', 'boot': 'v1', 'commit': COMMIT, 'repo_head': HEAD, 'command': 'python tools/firth_check_A.py --install', 'rc': rc, 'versions': VER,
        'tool_sha16': {'tools/firth_check_A.py': sha16(os.path.join(REPO, 'tools', 'firth_check_A.py')), 'tools/firth_check_A.R': sha16(os.path.join(REPO, 'tools', 'firth_check_A.R')),
                       'tools/firth.py': sha16(os.path.join(REPO, 'tools', 'firth.py')), 'design/contrasts-A.json': sha16(os.path.join(REPO, 'design', 'contrasts-A.json'))},
        'files_sha16_lf': FILES, 'run_log_sha16': sha16(LOGP), 'started': LOG[0]['at'] if LOG else None, 'ended': now(), 'wall_s': round(time.time() - T0, 1), 'log': LOG, 'clause': CLAUSE}
json.dump(SREC, open(os.path.join(PERSIST, 'firth-check-session-A.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ZP = shutil.make_archive(os.path.join(BASE, 'stageA-firth-check-%s' % datetime.date.today().isoformat()), 'zip', PERSIST)
print('[boot_firth] zip → %s（%d バイト・sha256 %s）。登録者の許可を得て手元に落とし、SHA をセッション記録の files_sha16_lf と突合する。' % (ZP, os.path.getsize(ZP), hashlib.sha256(open(ZP, 'rb').read()).hexdigest()), flush=True)
print('[boot_firth] 完了 rc=%d・壁時計 %.0f 秒。%s' % (rc, time.time() - T0, CLAUSE), flush=True)
