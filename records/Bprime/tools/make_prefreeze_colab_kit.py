# -*- coding: utf-8 -*-
"""make_prefreeze_colab_kit.py v0（2026-10-01・B′ の下見の前の凍結を Colab の CPU〔Linux〕で走らせる束を作る・登録者の決め〔案 A・器の段の記録〕・コーディネータ南無弥勒如来）。
手元（Windows）で引いた等方の乱数 g のビットが Colab（Linux）と違ったので、同じ凍結の器（`tools/freeze_Bprime.py`・変えない）を、相 extract と同じ OS で走らせる。
束に入れる物: 走らせる台本 `run_prefreeze_colab.py`・G4 の確かめの出力の zip（SHA-256 を台本が照らす）・露出の記録（SHA16 を台本が照らす）・設定とトークナイザの目録 `MANIFEST-local.json`。
台本は、版のピン（transformers 5.16.1・numpy は G4 の確かめと同じ 2.1.3）を分けた置き場に入れ、公開の置き場を決めたコミットで取り出し、設定とトークナイザを固定の版で取って目録と照らし、
露出の記録と G4 の確かめの出力を置いてから、合成データの確かめの五と同じ環境の変数で凍結の器の `prefreeze` を背後で走らせる。終わると、置き場で増えたか変わったファイル（git が見るもの）を zip にし、
終わりの印 `/content/pf-done.json`（返りの値・zip の SHA-256・ファイルの並び）を書く。進みは `/content/pf-progress.log`。
用法: python records/Bprime/tools/make_prefreeze_colab_kit.py <G4 の確かめの zip> <書く束の zip>（作業の置き場の根で）
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
COMMIT = 'dcd9617a5c8a3a8084cc052eaba22c292db6f8cc'
REV = '842da3794eaa0b77d5f08bae87a17459d91ff475'
CHECK_SHA = 'B1DEA62E2BE3EF47BA6FAE41EB6F270B2F332D0F615ED6DBF490928D52443D58'
EXPO_SHA16 = '4CB80352B097EAF4'
RUN = r'''# -*- coding: utf-8 -*-
# run_prefreeze_colab.py（make_prefreeze_colab_kit.py v0 が書いた・Colab の CPU〔Linux〕で B′ の下見の前の凍結を走らせる・器は変えない）
# 柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
import os, sys, json, time, glob, shutil, hashlib, zipfile, subprocess
KIT, PUB, PYLIB, LOG = '/content/pfkit', '/content/ontology-preamble-4b', '/content/pylib-pf', '/content/pf-progress.log'
COMMIT, REV = '%(commit)s', '%(rev)s'
CHECK_ZIP, CHECK_SHA, EXPO_SHA16 = 'check-run-20261001T000529Z.zip', '%(check_sha)s', '%(expo16)s'
def say(s):
    print(s, flush=True)
    open(LOG, 'a', encoding='utf-8').write(s + '\n')
def sh(cmd, **kw):
    say('$ ' + (cmd if isinstance(cmd, str) else ' '.join(cmd))[:300])
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, **kw)
    say((r.stdout + r.stderr)[-1500:])
    if r.returncode != 0:
        raise SystemExit('止める: ' + str(cmd)[:200])
    return r
t0 = time.time()
say('[run_prefreeze_colab] 始め')
if os.path.exists('/content/pf-done.json'):
    raise SystemExit('既に走った（/content/pf-done.json がある）')
sh([sys.executable, '-m', 'pip', 'install', '-q', '--target', PYLIB, 'transformers==5.16.1', 'numpy==2.1.3'])
if not os.path.isdir(os.path.join(PUB, '.git')):
    sh(['git', 'clone', '--filter=blob:none', '--no-checkout', 'https://github.com/YutaKusumi/ontology-preamble-4b.git', PUB])
    sh(['git', '-C', PUB, 'sparse-checkout', 'set', '--cone', 'tools', 'design', 'records', 'results/dirB', 'arms'])
sh(['git', '-C', PUB, 'checkout', '-q', COMMIT])
assert subprocess.run(['git', '-C', PUB, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip() == COMMIT, '取り出した版が決めた版と違う'
HF = os.path.join('/content/hf-gemma', REV)
man = json.load(open(os.path.join(KIT, 'MANIFEST-local.json'), encoding='utf-8'))
code = ('from huggingface_hub import hf_hub_download as d\nimport sys\n'
        'for f in %%r:\n    d("google/gemma-4-31B-it", f, revision="%%s", local_dir=sys.argv[1], token=False)\n' %% (sorted(man['files']), REV))
sh([sys.executable, '-c', code, HF], env=dict(os.environ, PYTHONPATH=PYLIB, HF_HUB_DISABLE_XET='1'))
bad = [f for f, r in man['files'].items() if hashlib.sha256(open(os.path.join(HF, f), 'rb').read()).hexdigest() != r['sha256'].lower()]
if bad:
    raise SystemExit('設定かトークナイザの SHA-256 が目録と違う: %%s' %% bad)
shutil.rmtree(os.path.join(HF, '.cache'), ignore_errors=True)
say('[run_prefreeze_colab] 設定とトークナイザを照らした（%%d 本）' %% len(man['files']))
ex = open(os.path.join(KIT, 'exposure-before-seal-Bprime.md'), 'rb').read()
assert hashlib.sha256(ex.replace(b'\r\n', b'\n')).hexdigest().upper()[:16] == EXPO_SHA16, '露出の記録の SHA16 が違う'
dst = os.path.join(PUB, 'records', 'Bprime', 'exposure-before-seal-Bprime.md')
assert not os.path.exists(dst), '露出の記録が既にある'
open(dst, 'wb').write(ex)
zb = open(os.path.join(KIT, CHECK_ZIP), 'rb').read()
assert hashlib.sha256(zb).hexdigest().upper() == CHECK_SHA, 'G4 の確かめの zip の SHA-256 が違う'
zipfile.ZipFile(os.path.join(KIT, CHECK_ZIP)).extractall('/content/pfcheck')
cc = glob.glob('/content/pfcheck/check-run-*')[0]
W = json.load(open(os.path.join(PUB, 'records', 'Bprime', 'freeze-words-Bprime.json'), encoding='utf-8'))
C = json.load(open(os.path.join(PUB, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
args = ['tools/freeze_Bprime.py', 'prefreeze', '--words', W['words'], '--when', W['date_jst'], '--colab-check', cc, '--behavior-batch', str(C['behavior_pilot']['seeds']['batch_size'])]
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONPATH=PYLIB, OP4B_REPO=PUB, OP4B_PUBLIC_REPO=PUB, OP4B_PUB_TOOLS=os.path.join(PUB, 'tools'), OP4B_HF_DIR=HF)
for k in [k for k in env if k.startswith('OP4B_DRY') or k in ('OP4B_PHASE', 'OP4B_STEP', 'OP4B_PART', 'OP4B_COMMIT', 'OP4B_NPZ', 'OP4B_OUT', 'OP4B_REPO_DIR', 'OP4B_BPRIME_DIR')]:
    env.pop(k)
worker = r"""
import os, sys, json, time, hashlib, zipfile, subprocess
PUB, args, t0 = __PUB__, __ARGS__, time.time()
r = subprocess.run([sys.executable, '-W', 'ignore'] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=PUB)
open('/content/pf-progress.log', 'a', encoding='utf-8').write(r.stdout[-20000:] + r.stderr[-8000:] + '\n[pf_worker] prefreeze の返り %%d（%%.0f 秒）\n' %% (r.returncode, time.time() - t0))
st = subprocess.run(['git', '-C', PUB, 'status', '--porcelain', '-uall'], capture_output=True, text=True).stdout.splitlines()
files = sorted(l[3:] for l in st)
with zipfile.ZipFile('/content/pf-result.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(os.path.join(PUB, f), f)
    z.write('/content/pf-progress.log', 'pf-progress.log')
sha = hashlib.sha256(open('/content/pf-result.zip', 'rb').read()).hexdigest().upper()
json.dump({'rc': r.returncode, 'zip': '/content/pf-result.zip', 'sha256': sha, 'files': files, 'seconds': round(time.time() - t0, 1)}, open('/content/pf-done.json', 'w'), ensure_ascii=False)
""".replace('__PUB__', repr(PUB)).replace('__ARGS__', repr(args))
open('/content/pf_worker.py', 'w', encoding='utf-8').write(worker)
lf = open(LOG, 'a', encoding='utf-8')
p = subprocess.Popen([sys.executable, '/content/pf_worker.py'], env=env, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
say('[run_prefreeze_colab] 凍結の器を背後で走らせ始めた（pid %%d・準備 %%.0f 秒）。終わりは /content/pf-done.json' %% (p.pid, time.time() - t0))
'''


def main(check_zip, out_zip):
    zb = open(check_zip, 'rb').read()
    assert hashlib.sha256(zb).hexdigest().upper() == CHECK_SHA, 'G4 の確かめの zip の SHA-256 が違う'
    ex = open(os.path.join(PUB, 'records', 'Bprime', 'exposure-before-seal-Bprime.md'), 'rb').read()
    assert hashlib.sha256(ex.replace(b'\r\n', b'\n')).hexdigest().upper()[:16] == EXPO_SHA16, '露出の記録の SHA16 が違う'
    man = open(os.path.join(BP, 'hf', 'gemma-4-31B-it', REV, 'MANIFEST-local.json'), 'rb').read()
    run = (RUN % {'commit': COMMIT, 'rev': REV, 'check_sha': CHECK_SHA, 'expo16': EXPO_SHA16}).encode('utf-8')
    compile(run.decode('utf-8'), 'run_prefreeze_colab.py', 'exec')
    assert not os.path.exists(out_zip), out_zip
    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('run_prefreeze_colab.py', run)
        z.writestr('check-run-20261001T000529Z.zip', zb)
        z.writestr('exposure-before-seal-Bprime.md', ex)
        z.writestr('MANIFEST-local.json', man)
    print('kit', out_zip, os.path.getsize(out_zip), hashlib.sha256(open(out_zip, 'rb').read()).hexdigest().upper())


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
