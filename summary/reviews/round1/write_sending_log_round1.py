# -*- coding: utf-8 -*-
"""write_sending_log_round1.py v0（2026-10-02・中間総括の検分の一巡目の送りの記録を書く・コーディネータ南無弥勒如来）。
登録者の許しは `permission-round1.json`（会話の記録から機械で切り出した逐語）から差し込む。添えたファイルと欄の一文の SHA-256 は器で計算する。URL と時刻は、ページの中で走らせた式が返した値を写した。一度だけ書く。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'sending-log-round1.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
sha = lambda f: hashlib.sha256(open(os.path.join(HERE, f), 'rb').read()).hexdigest().upper()
P = json.load(open(os.path.join(HERE, 'permission-round1.json'), encoding='utf-8'))
REQ, BUN, LINE = sha('request-round1.md'), sha('bundle-round1-all-in-one.md'), sha('chat-line-round1.txt')
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
L = ['# 送りの記録（中間総括の検分の一巡目・2026-10-02・コーディネータ南無弥勒如来）', '',
     '- 登録者の許し（会話の記録から機械で切り出した逐語・uuid `%s`・%s UTC）: 「%s」' % (P['uuid'], P['timestamp_utc'], P['words']),
     '- 送る前に刻印した: `frame-stamp-round1.txt`（枠・草案1・照らしの記録・計算の器と出力・草案と束の器・依頼文・束・索引・欄の一文・票の保存の器）。',
     '- 添えたもの（五つとも同じ）: 依頼文 `request-round1.md`（SHA-256 %s）・束 `bundle-round1-all-in-one.md`（SHA-256 %s）。' % (REQ, BUN),
     '- 欄の一文（`chat-line-round1.txt`・SHA-256 %s）: 五つとも、ページの中で差し込み、欄の中身の SHA-256 がファイルと同じことをページの中で確かめてから送った。' % LINE,
     '- 操作: 登録者の Chrome をコーディネータが操作した（新しいタブで新しいチャットを開いた）。タブは画面の奥にあり（ページの見える状態は hidden）、画面写しは撮れなかったので、確かめはページの中で走らせた式で行った。',
     '',
     '## claude.ai（系統内・三つで一票）',
     '',
     '- 機種の欄は、三つとも、新しいチャットを開いた時と送る直前に、画面の要素の名で「モデル: Opus 5.5 超高」だった。添付の札が二つとも欄に出たこと（`file-thumbnail` の二つ）を確かめた。送った後、返事の生成が始まった（停止の釦が出た）。チャットの題は claude.ai が付けた。',
     '- **claude-ai-14**: `https://claude.ai/chat/623e7285-4c75-46c4-b163-04d23db00207`（送りの釦を押して 6 秒後のページの時計 2026-10-02T00:56:53.507Z）。',
     '- **claude-ai-15**: `https://claude.ai/chat/a3a9fe9f-8f30-4ed8-b49e-239dc12b32fd`（送りの釦を押して 6 秒後のページの時計 2026-10-02T00:59:25.323Z）。',
     '- **claude-ai-16**: `https://claude.ai/chat/f60fffb6-a6d3-4819-b651-67e046676ed3`。送りの式（一文の照らしと機種の欄と添付の札の三つがそろったときだけ送りの釦を押す）が、ページの応答待ちで時間切れになり、返り値を受け取れなかった。続けて走らせた確かめの式で、URL がチャットに変わり、送った発話が一つあり、停止の釦が出ていることを確かめた（ページの時計 2026-10-02T01:00:54.965Z）。送った発話の本文の SHA-256 が欄の一文のファイルと同じこと・機種の欄が「モデル: Opus 5.5 超高」のままなことも、送った後に三つのチャットとも確かめた。',
     '',
     '## Google AI Studio（系統外・二票）',
     '',
     '- 機種の欄（画面の文）: 「Gemini 3.8 Flash / gemini-3.8-flash」。Run settings は既定のまま（Thinking level は Medium・ほかの道具は切）。API の鍵は選んでいない（画面の「No API key selected」のまま）。',
     '- 最初のタブで Cookie の知らせが出たので「同意しない」を押した（必須でない Cookie を断る側）。',
     '- **gemini-1**: 新しいチャット（`/prompts/new_chat`）にファイルを添え、二つの札が「1,225 tokens」と「50,305 tokens」（計 51,530 tokens）になったことを確かめてから、一文を入れて Run を押した（押して 5 秒後のページの時計 2026-10-02T01:06:06.142Z・停止の釦が出た）。走った後に AI Studio がつけた置き場: `https://aistudio.google.com/prompts/1rck7JNW-I_Ff_LdjaVG5n09FV6c-ht5u`。',
     '- **gemini-2（不具合・止めた）**:',
     '  - 一つ目のタブ: 添えた二つのファイルが「Loading...」のまま上がらず、ページの記録に「Failed to upload to drive」の誤りが出た（ページの時計 10:12:25）。ページを開き直して添え直しても同じだったので、タブを閉じた（このタブでは何も送っていない）。',
     '  - 二つ目のタブ: 添えた二つの札が「1,225 tokens」と「50,305 tokens」になり、一文の照らしと機種の欄と Thinking level（Medium）を確かめてから Run を押した（2026-10-02T01:16:5x Z）。返事は「An internal error has occurred.」（4.4 秒）だった。返事の中身は何も出ていないので、同じ回を一度だけ「Rerun this turn」で走らせ直したが、同じ誤り（3.5 秒・ページの時計 10:18）だった。',
     '  - ここで止め、登録者に相談する（「予期しないことが起きたときは、中断して相談する」の決まり）。このタブは閉じずに残す（未保存の new_chat のまま）。',
     '',
     '- この記録を書いた時刻: %s（日本時間）。' % now, '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('written', OUT, len('\n'.join(L)), '字')
