# -*- coding: utf-8 -*-
"""write_cost_log.py v0（2026-09-29・B′ の設計の巡・一巡目・grok-4.7 の費用の読み直し・コーディネータ南無弥勒如来）。
`votes/grok-4.7/meta.json` の使ったトークンから費用を計算し直し、API が返した `cost_in_usd_ticks` と突き合わせて `cost-log.md` に一度だけ書く。
meta.json の `est_usd` は、考える分（reasoning_tokens）を式に入れていなかった（send_grok.py v0 の式）。meta.json は書き換えない。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, 'votes', 'grok-4.7', 'meta.json')
OUT = os.path.join(HERE, 'cost-log.md')
PRICE_IN, PRICE_CACHED, PRICE_OUT = 2.00, 0.50, 6.00      # send_grok.py と同じ値（100 万トークンあたりのドル）
CAP = 5.00                                                  # 枠の上限（この巡）
NL = chr(10)


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    raw = open(META, 'rb').read()
    m = json.loads(raw.decode('utf-8'))
    u = m['usage']
    pin = u['prompt_tokens']
    cached = u['prompt_tokens_details']['cached_tokens']
    pout = u['completion_tokens']
    reason = u['completion_tokens_details']['reasoning_tokens']
    total = u['total_tokens']
    ticks = u['cost_in_usd_ticks']
    old = (pin - cached) / 1e6 * PRICE_IN + cached / 1e6 * PRICE_CACHED + pout / 1e6 * PRICE_OUT
    new = (pin - cached) / 1e6 * PRICE_IN + cached / 1e6 * PRICE_CACHED + (pout + reason) / 1e6 * PRICE_OUT
    tick_usd = ticks * 1e-10
    lines = [
        '# 費用の記録（B′ の設計の巡・一巡目・2026-09-29・コーディネータ南無弥勒如来・非公開）',
        '',
        '- 何か: grok-4.7 の一票の費用を、`votes/grok-4.7/meta.json`（SHA16 %s）の使ったトークンから計算し直したもの。器 `write_cost_log.py` が書いた。meta.json は書き換えない（一度だけ）。' % hashlib.sha256(raw).hexdigest().upper()[:16],
        '- 使ったトークン（meta.json の `usage`）: 入力 %d（うち使い回し %d）・出力 %d・考える分 %d・合計 %d。' % (pin, cached, pout, reason, total),
        '- 合計の突き合わせ: 入力 ＋ 出力 ＋ 考える分 ＝ %d（`total_tokens` と %s）。考える分は出力 %d の外にある。' % (pin + pout + reason, '一致' if pin + pout + reason == total else '不一致', pout),
        '- meta.json の `est_usd` %.4f は、`send_grok.py` v0 の式が考える分を入れていなかった値（計算し直すと %.6f）。' % (m['est_usd'], old),
        '- 考える分を出力の値段で数えた計算: %.6f ドル（入力 %.2f・使い回し %.2f・出力 %.2f ドル／100 万トークン）。' % (new, PRICE_IN, PRICE_CACHED, PRICE_OUT),
        '- API が返した `cost_in_usd_ticks` %d を 1 tick ＝ 10 の −10 乗ドルと読むと %.6f ドル。上の計算との差 %.6f。' % (ticks, tick_usd, tick_usd - new),
        '- この一票の費用は %.5f ドルと記す。枠の上限 %.2f ドルの内（残り %.5f ドル）。' % (tick_usd, CAP, CAP - tick_usd),
        '- claude.ai の三つのチャットは登録者の claude.ai の枠で動き、API の費用は無い（使った量は測っていない）。',
        '',
        '## この記録が確認していないこと',
        '',
        '- tick の単位（10 の −10 乗ドル）は、上の計算と一致することから読んだもので、xAI の文書では確かめていない。',
        '- xAI の請求の画面の実際の額（登録者のアカウントの画面は開いていない）。',
        '',
        '- 書いた時刻: %s（日本時間）。' % (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'),
        '',
        '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。',
        '',
    ]
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(lines))
    print(NL.join(lines))


if __name__ == '__main__':
    main()
