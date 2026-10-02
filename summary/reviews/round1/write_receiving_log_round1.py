# -*- coding: utf-8 -*-
"""write_receiving_log_round1.py v0（2026-10-02・中間総括の検分の一巡目の受け取りの記録を書く・コーディネータ南無弥勒如来）。
票の SHA-256・字数・置き場・機種の欄は、`votes/<名>/meta.json`（保存の器が一度だけ書いた）から差し込む。所見の番号の数は、票の本文から正規表現で数える。一度だけ書く。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'receiving-log-round1.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
PAT = {'claude-ai-14': r'\*\*所見 (\d+)【', 'claude-ai-15': r'^\| (重\d+|中\d+|軽\d+) \|', 'claude-ai-16': r'\*\*((?:S|X|C|F|R|K)-\d+)\b', 'gemini-1': r'### 【所見 (\d+)】'}
L = ['# 受け取りの記録（中間総括の検分の一巡目・2026-10-02・コーディネータ南無弥勒如来）', '',
     '- 票は、画面の写しの釦が渡す文をページの中で受け取り、ページの中で SHA-256 を計算して書き出し、保存の器 `save_round1_vote.py` が手元の SHA-256 と照らしてから一度だけ書いた（クリップボードは使わない）。書き出した元のファイルは `downloads-stash/` に移した。',
     '- 票の数え方: 呼び出しの出所で数える（claude.ai の三つで系統内の一票〔裁定 D59 の数え方〕・Google AI Studio の Gemini 3.8 Flash は一つごとに系統外の一票）。票の頭の系統の申告は出所の確かめに使わない（D266 の型）。四票とも、申告は出所と食い違わなかった。', '',
     '| 名 | 出所 | 機種の欄（画面） | 受け取った文の SHA-256 | 字数 | 保存した時刻 | 所見の番号の数（器で数えた） |', '|---|---|---|---|---|---|---|']
for name in ('claude-ai-14', 'claude-ai-15', 'claude-ai-16', 'gemini-1'):
    m = json.load(open(os.path.join(HERE, 'votes', name, 'meta.json'), encoding='utf-8'))
    t = open(os.path.join(HERE, 'votes', name, 'response.md'), encoding='utf-8').read()
    ids = sorted(set(re.findall(PAT[name], t, flags=re.M)))
    L.append('| %s | %s | %s | %s | %d | %s | %d |' % (name, m['chat_url'], m['model_label_on_screen'], m['response_sha256'], m['response_chars'], m['saved_jst'], len(ids)))
L += ['',
      '- 所見の番号の数え方: claude-ai-14 は「所見 N【」、claude-ai-15 は総合の表の行の番号（重・中・軽）、claude-ai-16 は太字の S・X・C・F・R・K の番号（C-1 は検算の報告で所見ではないが番号として数えた）、gemini-1 は「【所見 N】」。番号の数は所見の重さや正しさを表さない。',
      '- gemini-1 の meta.json の `model_label_note` は、保存の器の定型の文（画面の要素の名〔aria-label〕を写した）で、Google AI Studio では機種の欄の画面の文（ms-model-selector の文）を写した。器は替えていない（ここに記録する）。',
      '- **gemini-2 は受け取っていない**: 送りの記録のとおり、ファイルの上げの誤り（一つ目のタブ）と「An internal error has occurred.」（二つ目のタブ・走らせ直しの一度を含めて二度）で返事が出なかった。登録者に相談する。',
      '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('\n'.join(L[5:10]))
