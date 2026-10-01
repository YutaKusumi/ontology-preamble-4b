# -*- coding: utf-8 -*-
"""log_final_Bprime.py v0（2026-10-01・B′ の器の段の記録に、裁定 D285 の実施と登録者最終確認の行を足す・コーディネータ南無弥勒如来）。
足す行の数・SHA・時刻・uuid は、置き場の記録（裁定 D285 の記録・確認の記録・最終版の確かめの記録・起草者の最終の見直しの記録）から機械で読む（打ち直さない）。
記録は後ろに足すだけで、前の行を書き換えない（「この記録が確認していないこと」の節の前に置く）。一度だけ（既に足してあれば止める）。
用法: python log_final_Bprime.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'tools-log-Bprime.md')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
NL = chr(10)
MARK = '- **最終検分の後のまとめの裁定 D285 の実施と登録者最終確認（2026-10-01）**'
R = lambda *a: os.path.join(PUB, *a)
ld = lambda *a: json.load(open(R(*a), encoding='utf-8'))


def main():
    log = open(LOG, encoding='utf-8').read()
    assert MARK not in log, '既に足してある（一度だけ）'
    rul = open(R('records', 'Bprime', 'rulings-D285.md'), encoding='utf-8').read()
    m = re.search(r'- \*\*D285\*\*（登録者・会話の記録 uuid `([^`]+)`・([^ ]+ [^ ]+) 日本時間）', rul)
    assert m
    cf = ld('records', 'Bprime', 'final-confirmation-Bprime.json')
    ck = ld('records', 'Bprime', 'results-Bprime-FINAL-2026-10-01-checks.json')
    assert ck['status'] == 'confirmed'
    cp = ck['draft2_compare']
    row = ('%s: 裁定 D285（会話の記録 uuid `%s`・%s 日本時間・`records/Bprime/rulings-D285.md`・`rulings_D285.py` が機械で切り出した。この器が画面に出す一行は、写し元の器の名残りで'
           '「wrote rulings-D284.md」と表示したが、書いた記録は rulings-D285.md で、rulings-D284.md は変わっていない〔SHA で確かめた〕）。'
           '(1) 鍵の確かめの器を v0.1 に上げた（`check_secrets_Bprime.py`・形を広げ、メールの宛先の形も見る・前の版は `prev/`）。公開済みの B′ のファイル全体（603）に試しに掛けると、'
           '当たりは前に公開した検分の束の zip の三つだけで、圧縮したバイトの偶然の並びがメールの宛先の形に当たったもの（中の項目を開いて照らすと宛先は無い）。'
           '(2) 写しの器を v0.1 に上げた（`stage_W22_Bprime.py`・確かめの器 v0.1 の照らしを使う）。'
           '(3) 逸脱の器を v1（`--final`・状態の行を正本の二つの型で組む・草案の二つ目との違いを照らす）に上げ、最終版の案を組んだ。検分票の一語が凍結した器の禁止の語に当たったので直した。'
           '起草者の最終の見直し（`reviews/results-final/final-read/review-final-Bprime.md`・R-a〜R-d）で、検分票の区画の二点（R-a・R-b）を直す器 v1.1 にし、最終版の案（SHA16 %s）を登録者に送った。'
           '(4) 登録者最終確認（会話の記録 uuid `%s`・%s 日本時間）: 確認の記録 `records/Bprime/final-confirmation-Bprime.json` と確認していただいた案の写し `records/Bprime/results-Bprime-proposal-confirmed-2026-10-01.md`'
           '（`records/Bprime/final_confirmation_Bprime.py` が会話の記録から機械で切り出した）。確認の言葉に鉤括弧があり、層三の型の器の照らし（鉤括弧を拒む）に当たるので、'
           '確認の記録の器（走らせる前）と逸脱の器（v1.2）で、数がそろい入れ子が閉じる鉤括弧を許す形に直した（状態の行の型は変えない）。'
           '(5) 逸脱の器 %s で最終版を組み直した（`records/Bprime/results-Bprime-FINAL-2026-10-01.md`・SHA16 %s・状態は確認の後の型・草案の二つ目から消えた行 %d・足された行 %d・'
           '確認していただいた案から消えた行 %d・足された行 %d〔状態の行・段階の行・器の版の字〕・事実の照らし %d 項・走査の当たり 0）。') % (
        MARK, m.group(1), m.group(2), cf['proposal_sha16'], cf['uuid'], cf['when_jst'], ck['tool'].split()[-1], ck['sha16']['records/Bprime/results-Bprime-FINAL-2026-10-01.md'],
        cp['removed_lines'], cp['added_lines'], cp['confirmed_proposal']['removed_lines'], cp['confirmed_proposal']['added_lines'], len(ck['checks']['facts']))
    anchor = '## この記録が確認していないこと'
    assert log.count(anchor) == 1
    i = log.index(anchor)
    open(LOG, 'w', encoding='utf-8', newline=NL).write(log[:i] + row + NL + NL + log[i:])
    print('足した | D285 %s %s | 確認 %s %s' % (m.group(1), m.group(2), cf['uuid'], cf['when_jst']))


if __name__ == '__main__':
    main()
