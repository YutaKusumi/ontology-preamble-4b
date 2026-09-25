# -*- coding: utf-8 -*-
"""器についての意見伺いのご意見が引いた行番号の抜き取りの確かめ（束の行番号＝ファイルの行番号・束の入力のコミット 029d55f）。
各行に「当たるはずの字」を置き、その字が引かれた行の中にあるかを見る。字の選び方はコーディネータの判断（一度目に C1 の direction_B.py 39 行の字を選び違えたので直した）。
出力: checks/citation-spotcheck.txt
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
C = [('C1', 'tools/direction_B.py', 39, 39, 'math.floor(ratio * n_layers'), ('C1', 'tools/bl3_run.py', 116, 116, 'starts = [cell.mp]'), ('C1', 'tools/bl3_run.py', 122, 122, 'starts = [0]'),
     ('C1', 'tools/bl3_recompute_rewrite.py', 240, 240, "h[0, int(mp):, :]"), ('C1', 'tools/analyze_Bl3.py', 109, 109, 'ue = {u:'), ('C1', 'tools/analyze_Bl3.py', 244, 244, "chance="),
     ('C1', 'tools/bl3_core.py', 146, 146, 'len(us) < 2'), ('C1', 'tools/bl3_run.py', 461, 461, 'if ck in dropped'), ('C1', 'tools/run_stageB_local.py', 546, 546, 'apply_chat'),
     ('C2', 'tools/run_stageB_local.py', 184, 184, 'hs['), ('C2', 'tools/analyze_Bl3.py', 100, 102, 'labels_signature'), ('C2', 'tools/bl3_run.py', 119, 119, "pc['end'] != cell.mp"),
     ('C2', 'tools/colab/boot_Bl3.py', 390, 390, "main_freeze']['pilot']"), ('C2', 'tools/analyze_Bl3.py', 365, 365, 'pilot_attempts'), ('C2', 'tools/analyze_Bl3.py', 65, 65, 'glob.glob'),
     ('C2', 'tools/bl3_run.py', 211, 211, 'pt[c.set_ids[0]]'), ('C2', 'tools/dry_run_Bl3.py', 323, 323, 'rows_subset'),
     ('G1', 'tools/bl3_run.py', 423, 423, 'i_c = 2'), ('G1', 'tools/bl3_run.py', 120, 120, 'ToolError'), ('G1', 'tools/bl3_recompute_rewrite.py', 291, 291, 'def recompute_rewrite'),
     ('G1', 'tools/colab/boot_Bl3.py', 436, 436, 'use_cache=False'), ('G1', 'tools/bl3_run.py', 130, 130, 'register_hook'),
     ('G2', 'design/contrasts-Bl3.json', 292, 292, 'precision'), ('G2', 'design/contrasts-Bl3.json', 297, 297, 'band'), ('G2', 'design/contrasts-Bl3.json', 1145, 1145, 'what'),
     ('G2', 'design/contrasts-Bl3.json', 1164, 1165, 'agreement'), ('G2', 'tools/bl3_run.py', 86, 87, 'Zs'), ('G2', 'tools/bl3_recompute_rewrite.py', 267, 267, 'logsumexp'),
     ('G2', 'tools/analyze_Bl3.py', 164, 165, 'as_eff'), ('G2', 'tools/bl3_core.py', 218, 227, 'def agreement')]
res, L = {}, ['# ご意見が引いた行番号の抜き取りの確かめ（機械生成・`checks/citation_spotcheck.py`・束の入力のコミット 029d55f）', '']
for who, f, a, b, key in C:
    src = subprocess.run(['git', 'show', '029d55f:%s' % f], cwd=REPO, capture_output=True, check=True).stdout.decode('utf-8').split('\n')
    seg = '\n'.join(src[a - 1:b])
    ok = key in seg
    near = [i + 1 for i, l in enumerate(src) if key in l] if not ok else []
    res.setdefault(who, []).append(ok)
    L.append('- %s `%s` %d〜%d 行「%s」: %s | %s' % (who, f, a, b, key, '当たる' if ok else '当たらない（その字のある行 %s）' % near[:3], seg.strip()[:150].replace('\n', ' ⏎ ')))
L += ['', '- まとめ: %s' % {k: '%d/%d' % (sum(v), len(v)) for k, v in res.items()}, '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'citation-spotcheck.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print(L[-4])
