# -*- coding: utf-8 -*-
"""make_colab_dry_kit.py v0 —— B′ の合成データの正式の確かめ（`tools/dry_run_Bprime.py`）を Colab の CPU のランタイムで走らせる束を作る（裁定 D271・2026-09-30・コーディネータ南無弥勒如来）。

束（zip）に入れるもの: 作業の置き場の器（`tools/`・前の版 `tools/prev/` を含む・`__pycache__` は除く）・正本と草案（`design/`・正本の前の版は除く）・記録（`records/`）・裁定（`rulings-D*.md`）・中立の課題の感触の確かめ（移す器の自己検査が見る）・
手元の目録（`hf/…/MANIFEST-local.json`）と、Colab で走らせる台本（`run_dry_colab.py`・この器が書く）。**入れないもの**: 分けた transformers（`pylib/`）・落とした設定とトークナイザ
（Colab の側で Hugging Face から固定の版を取り、手元の目録の SHA-256 と照らす）・設計の巡の記録・モデルカードの写し。束は作業の一時の置き場に書き、GitHub には置かない。
Colab の側の台本は、版のピン（numpy・transformers）を別のプロセスの置き場に入れ、公開の置き場を決めた版で取り出し（凍結の器）、`dry_run_Bprime.py` を走らせ、
記録と走りの記録を zip にして落とす（ランタイムは照らした後に削除する）。
用法: python tools/colab/make_colab_dry_kit.py <束の置き場（zip）>
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, glob, hashlib, zipfile, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE))
VERSION = 'v0.1'        # v0.1（2026-09-30）: 正式の確かめを背後の処理で走らせる（セルの出力の表示が長い走りで固まるため）・進みと終わりは /content の記録で見る
REV = '842da3794eaa0b77d5f08bae87a17459d91ff475'
NL = chr(10)

RUN = r'''# -*- coding: utf-8 -*-
# run_dry_colab.py（make_colab_dry_kit.py %(ver)s が書いた・Colab の CPU のランタイムで B′ の合成データの正式の確かめを走らせる）
# 柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
import os, sys, json, time, glob, shutil, hashlib, zipfile, subprocess
KIT = '/content/kit'
BP = os.path.join(KIT, 'Bprime')
PUB = '/content/ontology-preamble-4b'
PYLIB = '/content/pylib-bprime'
LOG = '/content/dry-progress.log'
COMMIT = '%(commit)s'
REV = '%(rev)s'
def say(s):
    print(s, flush=True)
    open(LOG, 'a', encoding='utf-8').write(s + '\n')
def sh(cmd, **kw):
    say('$ ' + (cmd if isinstance(cmd, str) else ' '.join(cmd)))
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, **kw)
    say((r.stdout + r.stderr)[-1500:])
    if r.returncode != 0:
        raise SystemExit('止める: ' + str(cmd))
    return r
t0 = time.time()
say('[run_dry_colab] 始め')
# 1. 版のピンを分けた置き場に入れる（ランタイムの版は変えない）
if not os.path.exists(os.path.join(PYLIB, 'transformers')):
    sh([sys.executable, '-m', 'pip', 'install', '-q', '--target', PYLIB, 'transformers==%(tf)s', 'numpy==%(np)s'])
# 2. 公開の置き場を決めた版で取り出す（凍結の器）
if not os.path.isdir(os.path.join(PUB, '.git')):
    sh(['git', 'clone', '--filter=blob:none', '--no-checkout', 'https://github.com/YutaKusumi/ontology-preamble-4b.git', PUB])
    sh(['git', '-C', PUB, 'sparse-checkout', 'set', '--cone', 'tools', 'design', 'records', 'results/dirB', 'arms'])
sh(['git', '-C', PUB, 'checkout', '-q', COMMIT])
head = subprocess.run(['git', '-C', PUB, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
if head != COMMIT:
    raise SystemExit('取り出した版が決めた版と違う')
# 3. 設定とトークナイザを固定の版で取り、手元の目録の SHA-256 と照らす
HF = os.path.join(BP, 'hf', 'gemma-4-31B-it', REV)
man = json.load(open(os.path.join(HF, 'MANIFEST-local.json'), encoding='utf-8'))
env = dict(os.environ, PYTHONPATH=PYLIB, HF_HUB_DISABLE_XET='1')
code = ('from huggingface_hub import hf_hub_download as d\n'
        'import sys\n'
        'for f in %(files)s:\n'
        '    d("google/gemma-4-31B-it", f, revision="%(rev)s", local_dir=sys.argv[1], token=False)\n')
sh([sys.executable, '-c', code, HF], env=env)
bad = []
for f, r in man['files'].items():
    p = os.path.join(HF, f)
    if not os.path.exists(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != r['sha256'].lower():
        bad.append(f)
if bad:
    raise SystemExit('設定かトークナイザの SHA-256 が手元の目録と違う: %%s' %% bad)
say('[run_dry_colab] 設定とトークナイザを照らした（%%d 本）' %% len(man['files']))
shutil.rmtree(os.path.join(HF, '.cache'), ignore_errors=True)
# 4. 正式の確かめを背後で走らせる（セルは待たない・進みは /content/dry-progress.log・終わりは /content/dry-done.json）
env = dict(os.environ, PYTHONPATH=PYLIB, OP4B_PYLIB=PYLIB, OP4B_REPO=PUB, OP4B_PUBLIC_REPO=PUB, OP4B_HF_DIR=HF, PYTHONIOENCODING='utf-8')
if os.path.exists('/content/dry-done.json'):
    os.remove('/content/dry-done.json')
lf = open(LOG, 'a', encoding='utf-8')
p = subprocess.Popen([sys.executable, '-u', os.path.join(KIT, 'dry_worker_colab.py')] + sys.argv[1:], cwd=BP, env=env, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
say('[run_dry_colab] 正式の確かめを背後で走らせ始めた（pid %%d・準備 %%.0f 秒）。進みは /content/dry-progress.log・終わりは /content/dry-done.json' %% (p.pid, time.time() - t0))
'''

WORKER = r'''# -*- coding: utf-8 -*-
# dry_worker_colab.py（make_colab_dry_kit.py %(ver)s が書いた・Colab で背後に走り、正式の確かめを走らせて記録を zip にする）
# 柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
import os, sys, json, time, glob, hashlib, zipfile, subprocess
KIT = '/content/kit'
BP = os.path.join(KIT, 'Bprime')
LOG = '/content/dry-progress.log'
COMMIT = '%(commit)s'
t0 = time.time()
print('[dry_worker_colab] 始め', flush=True)
rc = subprocess.run([sys.executable, '-u', '-W', 'ignore', 'tools/dry_run_Bprime.py', '--force'] + sys.argv[1:], cwd=BP).returncode
print('[dry_worker_colab] dry_run_Bprime の終わり rc=%%d（%%.0f 秒）' %% (rc, time.time() - t0), flush=True)
vers = subprocess.run([sys.executable, '-c', 'import numpy, torch, transformers, sys; print(sys.version.split()[0], numpy.__version__, torch.__version__, transformers.__version__)'],
                      capture_output=True, text=True).stdout.strip()
out = '/content/dry-result-Bprime.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in glob.glob(os.path.join(BP, 'records', 'Bprime', 'dry-run*-Bprime-*')):
        z.write(f, 'records/Bprime/' + os.path.basename(f))
    z.write(LOG, 'dry-progress.log')
    z.writestr('colab-env.json', json.dumps({'versions': vers, 'rc': rc, 'seconds': round(time.time() - t0, 1), 'commit': COMMIT, 'cpu_count': os.cpu_count()}, ensure_ascii=False))
sha = hashlib.sha256(open(out, 'rb').read()).hexdigest().upper()
json.dump({'rc': rc, 'zip': out, 'sha256': sha, 'seconds': round(time.time() - t0, 1)}, open('/content/dry-done.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('[dry_worker_colab] 書いた %%s（SHA-256 %%s）' %% (out, sha), flush=True)
'''


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) != 2:
        raise SystemExit('用法: python tools/colab/make_colab_dry_kit.py <束の置き場（zip）>')
    out = sys.argv[1]
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    commit = C['inputs']['public_version']
    man = json.load(open(os.path.join(BP, 'hf', 'gemma-4-31B-it', REV, 'MANIFEST-local.json'), encoding='utf-8'))
    run = RUN % {'ver': VERSION, 'commit': commit, 'rev': REV, 'tf': C['inputs']['versions']['transformers'], 'np': '2.4.6', 'files': json.dumps(sorted(man['files']))}
    compile(run, 'run_dry_colab.py', 'exec')
    worker = WORKER % {'ver': VERSION, 'commit': commit}
    compile(worker, 'dry_worker_colab.py', 'exec')
    files = []
    for root, dirs, fs in os.walk(BP):
        rel_root = os.path.relpath(root, BP).replace(os.sep, '/')
        dirs[:] = [d for d in dirs if d not in ('__pycache__', 'pylib', 'reviews', 'sources', 'cost-pilot', 'port-probe', '.cache') and not (rel_root == 'design' and d == 'prev')]
        for f in fs:
            rel = (f if rel_root == '.' else rel_root + '/' + f)
            top = rel.split('/')[0]
            if top in ('tools', 'design', 'records', 'model-feel', 'model-feel-2') or (rel_root == '.' and f.startswith('rulings-D') and f.endswith('.md')) or rel == 'hf/gemma-4-31B-it/%s/MANIFEST-local.json' % REV:
                files.append(rel)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(files):
            z.write(os.path.join(BP, *rel.split('/')), 'Bprime/' + rel)
        z.writestr('run_dry_colab.py', run)
        z.writestr('dry_worker_colab.py', worker)
    sha = hashlib.sha256(open(out, 'rb').read()).hexdigest().upper()
    print('[make_colab_dry_kit] 束 %s: ファイル %d・%.1f MB・SHA-256 %s' % (os.path.basename(out), len(files) + 2, os.path.getsize(out) / 2 ** 20, sha))


if __name__ == '__main__':
    main()
