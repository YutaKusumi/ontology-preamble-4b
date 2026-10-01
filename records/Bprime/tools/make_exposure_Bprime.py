# -*- coding: utf-8 -*-
"""make_exposure_Bprime.py v0（2026-10-01・B′ の封印の前の露出の記録を組む・層三の D190 と D217 の型・コーディネータ南無弥勒如来）。
正本 `predictions.exposure`・草案12 §11 と §12 の「封印の前に見たもの」のとおり、封印の前に登録者とコーディネータの目に触れたもの（層三の公開の結果・登録外の二つの記述・
Gemma の中立の課題の感触・台帳・費用の下見・設計の巡の票の中の見込みの文・封印の前の実物の走りで印字した値〔バッチ一の繰り返しの合否を含む〕）を、時刻つきの一つの記録にまとめる。
時刻は公開の置き場のコミットの時刻か、作業の置き場のファイルの時刻（日本時間・分まで）。SHA16 はファイルの実物から（改行を LF にそろえた値）。票の行は逐語保全した票のファイルから器が切り出した行。
封印の前の実物の走りの値は、G4 の確かめの出力の zip（SHA-256 を照らす）の `check.json` から、正本 `computation.before_seal.may_print` の値だけを写す。
書く物: 作業の置き場と公開の置き場の `records/Bprime/exposure-before-seal-Bprime.md`（同じバイト・どちらも一度だけ）。
用法: python records/Bprime/tools/make_exposure_Bprime.py <G4 の確かめの zip> <zip の SHA-256>（作業の置き場の根で）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, glob, hashlib, zipfile, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
REL = 'records/Bprime/exposure-before-seal-Bprime.md'
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
mt = lambda p: datetime.datetime.fromtimestamp(os.path.getmtime(p), JST).strftime('%Y-%m-%d %H:%M')
# 票の中の見込みの文: 見込みの語の当たり（機械）から、コーディネータが読んで、封印する予想の項目（q1〜q4）か行動の下見の書き出しに触れうると選んだ行（選びは読み・機械ではない）
VOTE_LINES = [
    ('reviews/design-round1/votes/claude-ai-2/response.md', 3, 'q1〜q4（見込みを書かないと断った上で、層三の値を条件つきで引いた所があると申告）'),
    ('reviews/design-round1/votes/claude-ai-1/response.md', 95, 'q1・床の余白の印（層三の値を引いた条件つきの文）'),
    ('reviews/design-round2/votes/claude-ai-4/response.md', 15, '行動の下見の書き出しの根の件数（封印する項目ではない・推論）'),
    ('reviews/design-round2/votes/claude-ai-4/response.md', 311, '行動の下見の書き出しの根の件数と読み取りの集合の出口の値（推論）'),
    ('reviews/design-round2/votes/claude-ai-6/response.md', 15, '行動の下見の書き出しの根の件数（封印する項目ではない・推論）'),
    ('reviews/design-round2/votes/claude-ai-6-followup1/response.md', 75, 'q1（バッチ一の繰り返しの合否を知ると q1 の見込みが動くという指摘・推論）'),
]


def git_time(commit):
    r = subprocess.run(['git', '-C', PUB, 'show', '-s', '--format=%ad', '--date=format:%Y-%m-%d %H:%M', commit], capture_output=True, text=True)
    assert r.returncode == 0, commit
    return r.stdout.strip()


def git_s16(commit, rel):
    r = subprocess.run(['git', '-C', PUB, 'show', '%s:%s' % (commit, rel)], capture_output=True)
    assert r.returncode == 0, (commit, rel)
    return hashlib.sha256(r.stdout.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def main(zp, want):
    for root in (BP, PUB):
        assert not os.path.exists(os.path.join(root, *REL.split('/'))), ('既にある（一度だけ）', root)
    zb = open(zp, 'rb').read()
    got = hashlib.sha256(zb).hexdigest().upper()
    assert got == want.replace(' ', '').upper(), ('G4 の確かめの zip の SHA-256 が違う', got)
    z = zipfile.ZipFile(zp)
    ck = [n for n in z.namelist() if n.endswith('/check.json')]
    ss = [n for n in z.namelist() if n.endswith('/session.json')]
    assert len(ck) == 1 and len(ss) == 1
    CK = json.loads(z.read(ck[0]).decode('utf-8'))
    S = json.loads(z.read(ss[0]).decode('utf-8'))
    assert CK['all_pass'] is True and S['dry'] is False
    it = CK['items']
    lk, dsp, mem, gs, tk, coef = it['logit_tolerance_k'], it['determinism_and_speed'], it['memory_not_growing'], it['generation_smoke'], it['tokenizer_only'], it['coefficient_on_bl3']
    E = [
        ('E1', git_time('1099f27'), '層三の結果（公開・報告の最終版）', '公開の置き場 1099f27 `records/Bl3/results-Bl3-FINAL-2026-09-27.md`（SHA16 %s）' % git_s16('1099f27', 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'),
         '登録者とコーディネータ', 'q1〜q4（別の機種の層三の値として）'),
        ('E2', git_time('6166796'), '層三の登録外の記述（層ごとの差分）', '公開の置き場 6166796', '登録者とコーディネータ', 'q2〜q4（別の機種の値として）'),
        ('E3', git_time('0a45688'), '層三の登録外の記述（等方のランダム方向の押しの下の升目ごとの揺れの広さ）', '公開の置き場 0a45688', '登録者とコーディネータ', 'q1〜q4（別の機種の値として）'),
        ('E4', '%s〜%s' % (mt(os.path.join(BP, 'model-feel', 'frame-model-feel-Bprime.md')), mt(os.path.join(BP, 'model-feel-2', 'feel-check-Bprime-2.md'))),
         'Gemma の中立の課題の感触（二度・場面と腕と JSON の指示と書き出しを使っていない）',
         '`records/Bprime/model-feel/feel-check-Bprime.md`（SHA16 %s）・`records/Bprime/model-feel-2/feel-check-Bprime-2.md`（SHA16 %s）' % (s16(os.path.join(BP, 'model-feel', 'feel-check-Bprime.md')), s16(os.path.join(BP, 'model-feel-2', 'feel-check-Bprime-2.md'))),
         'コーディネータ（登録者は報告で）', '行動の下見の応答の書式（封印する項目ではない）'),
        ('E5', mt(os.path.join(BP, 'tools', 'ledger-bprime.json')), 'Gemma のトークナイザでの台帳（トークンの並びだけ）', '`tools/ledger-bprime.json`（SHA16 %s）' % s16(os.path.join(BP, 'tools', 'ledger-bprime.json')),
         'コーディネータ', 'なし'),
        ('E6', mt(os.path.join(BP, 'cost-pilot', 'cost-bprime.json')), '費用の下見（意味のないトークン列の速さと記憶だけ）', '`records/Bprime/cost-pilot/cost-bprime.json`（SHA16 %s）' % s16(os.path.join(BP, 'cost-pilot', 'cost-bprime.json')),
         '登録者とコーディネータ（報告）', 'なし（バッチ 16 の速さ）'),
        ('E7', '%s〜%s' % (mt(os.path.join(BP, 'reviews', 'design-round1', 'votes', 'grok-4.7', 'response.md')), mt(os.path.join(BP, 'reviews', 'design-round3', 'votes', 'claude-ai-7-followup1', 'response.md'))),
         '設計の巡の票と追い問いの答え（三巡・grok-4.7 と claude.ai）', '`records/reviews/Bprime/design-round1〜3/votes/`', 'コーディネータ（登録者は報告と採否の表で）', '下の「票の中の見込みの文」'),
        ('E8', '%s〜%s' % (mt(os.path.join(BP, 'reviews', 'impl', 'votes', 'claude-ai-10', 'response.md')), mt(os.path.join(BP, 'reviews', 'recheck', 'votes', 'claude-ai-12-cont1', 'response.md'))),
         '器の実装の検分と直しの確かめの巡の票（grok-4.7 と claude.ai）', '`records/reviews/Bprime/impl/votes/`・`records/reviews/Bprime/recheck/votes/`', 'コーディネータ（登録者は報告と採否の表で）',
         '見当たらない（見込みの語の当たりは、器の作りと費用の文だけ）'),
        ('E9', '%s〜%s' % (datetime.datetime.fromisoformat(S['log'][0]['at'].replace('Z', '+00:00')).astimezone(JST).strftime('%Y-%m-%d %H:%M') if isinstance(S.get('log'), list) and S['log'] and 'at' in S['log'][0] else '2026-10-01 09:05',
                            datetime.datetime.fromisoformat(str(S['finished']).replace('Z', '+00:00')).astimezone(JST).strftime('%Y-%m-%d %H:%M') if S.get('finished') else '2026-10-01 09:15'),
         '封印の前の実物の走り（G4・意味のない列だけ・相 check）で印字した値', 'G4 の確かめの出力の zip（SHA-256 `%s`・コミット %s）' % (got, S['commit'][:12]), '登録者とコーディネータ（報告）', 'q1（バッチ一の繰り返しの合否）・ほかは器の値'),
    ]
    L = ['# B′ の封印の前の露出の記録（層三の D190 と D217 の型・時刻つき・機械の組み立て `records/Bprime/tools/make_exposure_Bprime.py` v0）', '',
         '- 何の記録か: B′ の予想（正本 `predictions.items`・q1〜q4）を封印する前に、登録者とコーディネータの目に触れたものの記録（正本 `predictions.exposure`・草案12 §11 と §12）。'
         '封印する二人は、予想の自由記述に、この記録を読んだことを書く（層三の D217 の型）。',
         '- 見ていないもの: Gemma の場面の出力と読み取りの値（場面・腕・JSON の指示・書き出しを含む入力の順伝播はしていない）。',
         '- 時刻: 公開の置き場のコミットの時刻か、作業の置き場のファイルの時刻（日本時間・分まで）。', '',
         '## 露出の一覧（時刻の順）', '',
         '| 番号 | 時刻（日本時間） | 何 | 出所 | 見た人 | 触れうる予想の項目 |', '|---|---|---|---|---|---|']
    L += ['| %s |' % ' | '.join(e) for e in E]
    L += ['', '## 票の中の見込みの文（E7・逐語保全した票のファイルから器が切り出した行）', '',
          '- 選び方: 見込みの語（見込み・おそらく・可能性が高い・予想・はず ほか）に当たった行（票ぜんたいで 57 行）を、コーディネータが読み、封印する予想の項目か行動の下見の書き出しに触れうる行を選んだ（選びは読みで、機械ではない）。'
          'ほかの当たりは、器の作り・許容の式・費用の見込みの文だった。',
          '', '| 票（ファイルの SHA16） | 行 | 触れうる項目 | 切り出した行 |', '|---|---|---|---|']
    for rel, ln, what in VOTE_LINES:
        p = os.path.join(BP, *rel.split('/'))
        text = open(p, encoding='utf-8').read().split(NL)[ln - 1].strip().replace('|', '\\|')
        L.append('| `%s`（%s） | %d | %s | %s |' % (rel.replace('reviews/', '').replace('/votes/', ':').replace('/response.md', ''), s16(p), ln, what, text))
    bins = lk.get('bins_batch1') or []
    L += ['', '## 封印の前の実物の走りで印字した値（E9・確かめの出力 `check.json` から機械で写した・正本 `computation.before_seal.may_print` の値だけ）', '',
          '- 合否: %d 項目すべて通った（%s）・順伝播 %d 回' % (len(it), '・'.join(it.keys()), CK['n_forward']),
          '- 出口の値の自己検査の k: %s（バッチ 16 %s・バッチ一 %s）・z₀ %s・測った行 %s・|z| ≥ 16 の行 %s・下限への切り替え %s' % (lk['k'], lk['k_by_batch']['16'], lk['k_by_batch']['1'], lk['z0'], lk['n_rows'], lk['big_rows'], 'なし' if not lk['fallback'] else 'あり'),
          '- 出口の大きさの区間ごと（バッチ一）: ' + '・'.join('[%s, %s) 行 %s・「あり」の差の最大 %.4g・「なし」との差の最小 %.4g・「二重」との差の最小 %.4g' % (b['bin'][0], b['bin'][1] if b['bin'][1] is not None else '∞', b['rows'], b['on_max'], b['off_min'], b['dbl_min']) for b in bins),
          '- 見分ける力の確かめ（正しい・正規化の二重がけ・softcap の抜け）: %s' % json.dumps(it['bugs_caught']['states'], ensure_ascii=False),
          '- **バッチ一の繰り返し: ビットで一致 %s**（合否だけ・q1 に触れうる・上の claude-ai-6 の追い問いの答えの指摘）・速さの中央値 バッチ一 %s 秒・バッチ 16 %s 秒（列の長さ %s）' % (dsp['batch1_repeat_bitwise_equal'], dsp['sec_median_by_batch']['1'], dsp['sec_median_by_batch']['16'], dsp['seq_len']),
          '- 記憶の最大: 5 回の後 %s GiB・30 回の後 %s GiB' % (mem['peak_gib_after_5'], mem['peak_gib_after_30']),
          '- 生成の煙試験（意味のない列・%d トークンまで）: ' % gs['max_new_tokens_smoke'] + '・'.join('止まり方 %s（印 %s）・トークン %s・思考の欄を開くトークン %s・%s 秒' % (r['finish'], r['stop_token'], r['n_tokens'], 'あり' if r['think_token'] else 'なし', r['sec']) for r in gs['runs'])
          + '・標本化で二度の生成が違う %s・BOS 一つ %s・`generate` に渡った設定 %s' % (gs['sampling_differs'], gs['bos_one'], json.dumps(gs['resolved']['values'], ensure_ascii=False)),
          '- トークナイザの確かめ: 揺れの版 %s を保つ・V3 の確かめ %s・プロンプトごとの BOS %s' % ('・'.join(tk['variants_kept']), json.dumps(tk['v3_checks'], ensure_ascii=False), tk['bos_per_prompt']),
          '- 係数の確かめ（層三の凍結の活性で）: 係数 %s・Qwen の比 %s・‖h‖ の相対の差 %.3g・‖v̂‖ の相対の差 %.3g' % (coef['coef_on_bl3'], coef['qwen_ratio'], coef['rel_h'], coef['rel_v']),
          '- 版と設定: %s・GPU %s・決定性の設定 %s' % (json.dumps(CK['versions'], ensure_ascii=False), CK['gpu'], json.dumps(CK['determinism'], ensure_ascii=False)), '',
          '## 採点の合成の応答と中立の課題の感触の書式', '',
          '- 合成データの確かめで採点の器に通した合成の応答（`tools/dry_bprime_behavior.py`）は、器が型から組んだ JSON の塊と、Gemma のチャットの型の印（思考の欄の印を含む）でできている。中立の課題の感触の応答の字は使っていない。',
          '- ただし、合成の応答の形（思考の欄の印を置く形を含む）は、中立の課題の感触（E4・二度目で思考の欄の出方を見た）の後に作った。形の選びに感触の知識が入りうる（コーディネータの申告）。', '',
          '## 扱い', '',
          '- 封印する二人（コーディネータが先・登録者）は、予想の自由記述に、この記録を読んだことを書く（層三の D217 の型・正本 `predictions.exposure`）。',
          '- コーディネータは、封印が済むまで、q1〜q4 についての自分の見込みを返信に書かない。', '',
          '## この記録が確認していないこと', '',
          '- 票の中の見込みの文の選び出しは、見込みの語の当たり（機械）とコーディネータの読みによる。票の通読や、語の当たらない見込みの文の拾い出しはしていない。',
          '- 登録者が報告で読んだ範囲（コーディネータの報告の字）を、項目ごとに照らしてはいない。', '', CLAUSE, '']
    md = NL.join(L)
    for root in (BP, PUB):
        p = os.path.join(root, *REL.split('/'))
        with open(p, 'w', encoding='utf-8', newline=NL) as fh:
            fh.write(md)
    print('wrote', REL, 'in workspace and public | sha16', hashlib.sha256(md.encode('utf-8')).hexdigest().upper()[:16], '| lines', md.count(NL))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
