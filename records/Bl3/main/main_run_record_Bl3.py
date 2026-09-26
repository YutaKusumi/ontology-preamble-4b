# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の本の計算の走りの記録（Colab の相 main の三つの組）を書く。数・時刻・SHA は、置いた組の出力（session）と、落とした zip と、
会話の記録の道具の結果（コーディネータが Colab の画面の文を機械で読んだユニットの読み）と、一致だけを見る段の記録から、機械で切り出す（手で打たない）。
効き目の値は読まない（組の出力の JSON は SHA-256 だけを取る）。既にある記録には書かない。
用法: python records/Bl3/main/main_run_record_Bl3.py <会話の記録 jsonl> <zip を落とした置き場>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, glob, hashlib, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
NL = chr(10)
OUT = os.path.join(HERE, 'main-run-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
DL = sys.argv[2]
OUTS = os.path.join(REPO, 'results', 'Bl3', 'main')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()
J = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'judge-Bl3.json'), encoding='utf-8'))
FR = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json'), encoding='utf-8'))
dirs = sorted(d for d in os.listdir(OUTS) if os.path.isdir(os.path.join(OUTS, d)))
rows, t_first, t_last = [], None, None
for d in dirs:
    S = json.load(open(os.path.join(OUTS, d, 'session.json'), encoding='utf-8'))
    part = S['parts'][0]
    assert len(S['parts']) == 1 and not S['dry']
    fz, pz = os.path.join(DL, d + '.zip'), os.path.join(DL, '%s-part-%s.zip' % (d, part))
    zf, zp = zipfile.ZipFile(fz), zipfile.ZipFile(pz)
    same = all(zf.read(n) == open(os.path.join(OUTS, *n.split('/')), 'rb').read() for n in zf.namelist())
    assert same, ('置いた出力が終わりの zip の中身と違う', d)
    part_in_session = any(x['tag'] == 'part-%s' % part and x['sha256'] == sha(pz) for x in S.get('zips', []))
    assert part_in_session and S['part_sha256'][part] == sha(os.path.join(OUTS, d, '%s.json' % part))
    copies = sorted(os.path.basename(p) for p in glob.glob(os.path.join(DL, d + ' (*).zip')))
    copies_same = all(open(os.path.join(DL, c), 'rb').read() == open(fz, 'rb').read() for c in copies)
    t0 = S['log'][0]['at']
    t_first = min(t_first or t0, t0)
    t_last = max(t_last or S['finished'], S['finished'])
    rows.append((d, part, S, fz, pz, zf, copies, copies_same))
# ユニットの読み（道具の結果の {at, found}）
reads = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and isinstance(c, list):
        for x in c:
            if isinstance(x, dict) and x.get('type') == 'tool_result':
                cc = x.get('content')
                txt = cc if isinstance(cc, str) else ''.join(y.get('text', '') for y in (cc or []) if isinstance(y, dict))
                if '利用可能なコンピューティング ユニット数' in txt and '"at"' in txt:
                    try:
                        j = json.loads(txt[txt.index('{'):txt.rindex('}') + 1])
                    except Exception:
                        continue
                    u = [f for f in j.get('found') or [] if f.startswith('利用可能なコンピューティング ユニット数')]
                    if u:
                        reads.append((j['at'], u[0], [f for f in j['found'] if not f.startswith('利用可能')]))
pre = [r for r in reads if r[0] < t_first]
post = [r for r in reads if r[0] > t_last]
assert pre and post
b4, af = max(pre), min(post)
S0 = rows[0][2]
R = ['# B-lens 層三の本の計算の走りの記録（Colab の相 main の三つの組・機械生成・`main_run_record_Bl3.py`）', '',
     '- 走り: GPU %s・コミット %s・起動器 %s・相 main の三つの組を、同じランタイムで一つずつ走らせた（組 %s・裁定 D239）。最初の組の始め %s・最後の組の終わり %s（協定世界時・session の記録）。版: %s。' % (
         S0['gpu'], S0['commit'], S0['boot'], '→'.join(r[1] for r in rows), t_first, t_last, '・'.join('%s %s' % kv for kv in S0['versions'].items())),
     '- 下見の記録の使い方（session の pilot_used）: %s。' % json.dumps(S0['pilot_used'], ensure_ascii=False),
     '- 手順: 最初の組の最初の走りは版を入れ直して止まり（transformers）、セッションを再起動して同じ一行を走らせ直した。残りの二つの組は同じランタイムで版を入れ直さずに走った。'
     'HF_TOKEN の画面はキャンセルした（公開の重み）。どの組も、打った一行を走らせる前に、期待の一行と字ごとに照らしてちょうど同じであることを確かめた。前の相 check のセルは走らせていない。']
for d, part, S, fz, pz, zf, copies, copies_same in rows:
    R.append('- 組 %s: 置き場 `%s`・%s 秒・凍結の照らし %d（取り出しの外で飛ばした %d・外れ %d）。組の zip `%s`（%d バイト・SHA-256 %s）と終わりの zip `%s`（%d バイト・SHA-256 %s）。'
             '組の zip の SHA-256 は終わりの zip の中の session の値と機械で一致し、二つの zip の SHA-256 は起動器の印字の末尾と画面で目で照らして一致した。終わりの zip の中身（%s）を `results/Bl3/main/%s/` に置いた（バイトで同じ）。%s' % (
                 part, d, S['seconds'], S['frozen_check']['checked'], len(S['frozen_check']['skipped']), len(S['frozen_check']['bad']),
                 os.path.basename(pz), os.path.getsize(pz), sha(pz), os.path.basename(fz), os.path.getsize(fz), sha(fz),
                 '・'.join('%s（%d バイト）' % (i.filename.split('/')[-1], i.file_size) for i in zf.infolist()), d,
                 ('終わりの zip は自動のダウンロードが遅れて届いた。届く前に手元を確かめたときは無かったので、コーディネータが「ファイル」の欄からも落とし、同じ中身の写し %s が手元にできた（バイトで同じ・消していない）。' % '・'.join('`%s`' % c for c in copies)) if copies and copies_same else ''))
R += ['- ユニット（コーディネータが Colab の画面の文を機械で読んだ道具の出力）: 走りの前「%s」（%s）・走りの後「%s」（%s・%s）。' % (b4[1], b4[0], af[1], af[0], '・'.join(af[2])),
      '- ランタイムは、最後の組の zip を落として照らした後に、接続を解除して削除した。',
      '- 効き目の値は、組の出力を開かずに扱った（zip の中身は SHA-256 と大きさだけを見た）。',
      '- 一致だけを見る段（`tools/analyze_Bl3.py judge`・`records/Bl3/judge-Bl3.json`・%s）: 器の誤り %s・組の環境 %s・一段目 %s・二段目（札） %s・二段目の値 %s・全体 %s（値は開いていない）。' % (
          J['written_utc'], '無し' if not any(J['tool_error'].values()) else 'あり', '同じ' if J['env']['same'] else '違う', '一致' if J['first'] else '不一致',
          '一致' if J['second'] else '不一致', '許容の内' if J['second_values_within_tol'] else '許容の外', '一致' if J['agree'] else '不一致'),
      '- 結果を開く段は、登録者と一緒に行う（この記録を書いた時点では開いていない）。本の凍結: %s（日本時間）。' % FR['main_freeze']['frozen_jst'], '',
      '## 検分票', '',
      '- 対象: Colab の相 main の三つの組の走り（L4）と、その出力の受け取りと、一致だけを見る段。',
      '- 段階: 本の計算の手順・組の分け方・一致の決まりは、凍結で先に決めた（事前）。この走りの記録は事後。',
      '- 凍結物の同定: 本の凍結の記録（`main_freeze`・逸脱 %d）・本の計算のコミット %s・session の凍結の照らし。' % (J['deviations_n'], S0['commit'][:7]),
      '- 盲検の状態: 効き目の値は開いていない（一致だけを見る段は一致か不一致かだけを出す）。結果を開く段は登録者と一緒に行う。',
      '- 敵対的検分: 組の zip と終わりの zip の SHA-256 を session の値と印字に照らし、置いた出力を zip の中身とバイトで照らし、組の出力の SHA-256 を session に照らした。一致だけを見る段は凍結した器で走らせた。',
      '- 系統の内訳: コーディネータ（Claude 系）一名。',
      '- COI記録: 走りが通る側・一致する側に引かれる。一致だけを見る段の決まりは凍結したものをそのまま使い、値を開いて確かめ直すことはしていない。',
      '- 判定: 本の計算の走りの記録として確定（結果はまだ開いていない）。',
      '- 本検分が確認していないこと: 効き目の値そのもの（結果を開く段まで見ない）。zip の SHA-256 の末尾の照らしは画面での目の照らし。別の環境（別の GPU や版）での再現。'
      '最初の組の最初の走り（版の入れ直し）の出力の置き場はランタイムとともに消え、落としていない。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
text = NL.join(R)
for bad in ('Users', 'AppData', 'Downloads'):
    assert bad not in text, '手元の道筋が入る'
open(OUT, 'w', encoding='utf-8', newline=NL).write(text)
print('wrote', os.path.basename(OUT), '| parts', [r[1] for r in rows], '| units before', b4[0], b4[1], '| after', af[0], af[1])
