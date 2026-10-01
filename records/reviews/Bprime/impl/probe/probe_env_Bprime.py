# -*- coding: utf-8 -*-
"""probe_env_Bprime.py v0 —— B′ の器の実装の検分の前の「実行の場の小さな試し」（正本 `review_plan.impl.conditions` の一つ目・D269・2026-09-30・コーディネータ南無弥勒如来）。
claude.ai の実行の場で走らせてもらい、出力をそのまま貼ってもらう。検分の中身（器・正本・草案）は送らない。この台本は外に何も送らない（パッケージを入れる試しだけは、
入れられるかを見るために pip を一度呼ぶ・入れた物は使わない）。
見ること: Python の版・numpy と scipy と torch と transformers と tokenizers の有無と版・pip で固定の版を入れられるか（transformers 5.16.1・numpy 2.4.6）・
CPU の数と記憶・zip を開けるか・置き場に書けるか・一つのファイルの大きさの目安。
柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, time, platform, tempfile, zipfile, subprocess, importlib


def ver(name):
    try:
        m = importlib.import_module(name)
        return getattr(m, '__version__', 'ある（版の字なし）')
    except Exception as e:
        return '無い（%s）' % type(e).__name__


def main():
    out = {'python': sys.version.split()[0], 'platform': platform.platform(), 'cpu_count': os.cpu_count()}
    try:
        import shutil
        out['disk_free_gb'] = round(shutil.disk_usage(tempfile.gettempdir()).free / 2 ** 30, 1)
    except Exception as e:
        out['disk_free_gb'] = str(e)
    try:
        with open('/proc/meminfo') as fh:
            out['mem_total'] = fh.readline().strip()
    except Exception:
        out['mem_total'] = '読めない'
    for n in ('numpy', 'scipy', 'torch', 'transformers', 'tokenizers', 'jinja2', 'safetensors'):
        out[n] = ver(n)
    with tempfile.TemporaryDirectory() as td:
        z = os.path.join(td, 'a.zip')
        with zipfile.ZipFile(z, 'w') as zf:
            zf.writestr('x/y.txt', '試し')
        with zipfile.ZipFile(z) as zf:
            out['zip_roundtrip'] = zf.read('x/y.txt').decode('utf-8') == '試し'
        try:
            t0 = time.time()
            r = subprocess.run([sys.executable, '-m', 'pip', 'download', '--no-deps', '-q', '-d', td, 'transformers==5.16.1'], capture_output=True, text=True, timeout=300)
            out['pip_download_transformers_5_16_1'] = {'rc': r.returncode, 'seconds': round(time.time() - t0, 1), 'tail': (r.stdout + r.stderr)[-300:]}
        except Exception as e:
            out['pip_download_transformers_5_16_1'] = {'error': str(e)[:300]}
        try:
            r = subprocess.run([sys.executable, '-m', 'pip', 'download', '--no-deps', '-q', '-d', td, 'numpy==2.4.6'], capture_output=True, text=True, timeout=300)
            out['pip_download_numpy_2_4_6'] = {'rc': r.returncode, 'tail': (r.stdout + r.stderr)[-200:]}
        except Exception as e:
            out['pip_download_numpy_2_4_6'] = {'error': str(e)[:300]}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
