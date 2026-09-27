# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の最終の系統外の検分の二票（F1・F2）の事実の主張を、公開の置き場の現物（報告の草案の二つ目・確かめの記録・開く段の記録・正本・段階 B の記録）から、
器とは別に書いた式で再現する（再現の番号 K542 から・枠 `frame-results-final-Bl3.md`）。読みの当否（言い回しの提案）は再現の外で、採否の案で扱う。
再現しなかった主張も消さない。票がどの単位で数えたかを確かめてから判じる。書くのは本記録（md と json）だけ。既にあるファイルには書かない。
用法: python records/reviews/Bl3/results-final/checks/verify_final_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
BS = chr(92)
OUT_MD, OUT_JSON = os.path.join(HERE, 'verification-final-Bl3.md'), os.path.join(HERE, 'verification-final-Bl3.json')
for p in (OUT_MD, OUT_JSON):
    assert not os.path.exists(p), '既にある: ' + p
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
ld = lambda rel: json.load(open(j(*rel.split('/')), encoding='utf-8'))
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
sys.path.insert(0, j('tools'))
import report_lint as RL
T3 = ld('design/contrasts-Bl3.json')
D2 = rd('records/Bl3/results-Bl3-draft2.md')
CK = ld('records/Bl3/results-Bl3-draft2-checks.json')
D2C = ld('records/Bl3/draft2-check/check-draft2-Bl3.json')
OJ = ld('records/Bl3/open-results-Bl3.json')
AD = rd('records/reviews/Bl3/results-round1/adoption-results-Bl3.md')
MB = RL.machine_block(T3)
TAG = '【逸脱 D-BLT1】'
K = []


def add(votes, claim, got, ok, note=''):
    K.append({'k': 'K%d' % (542 + len(K)), 'votes': votes, 'claim': claim, 'got': got, 'verdict': '再現した' if ok is True else ('再現しない' if ok is False else ok), 'note': note})


# 足した区画の一覧（中身の一行目）
L = D2.split(NL)
added = []
i = 0
while i < len(L):
    if L[i] == MB['begin'] and i + 1 < len(L) and L[i + 1].startswith('- ' + TAG) and not L[i + 1].startswith('- ' + TAG + '**'):
        jx = L.index(MB['end'], i)
        added.append(L[i + 1:jx])
        i = jx + 1
        continue
    i += 1
KIND = [('P711', 'この草案は、凍結した組み立ての器'), ('P704', '起草者の欄の文が指す数'), ('P705', '〈両方の外〉の行'), ('P699', '次の区画の表は凍結した器の出力'),
        ('P699', '上の区画の表の並べ直し'), ('P706', '記述の「v̂ と (6b) を抜いた門」'), ('P707', '独立の再計算の範囲は'), ('P708', '数と分母'), ('P709・P710', '上の限界の文の「全経路'),
        ('検分票（採否の行なし）', '上の検分票は')]
kinds = []
for b in added:
    hit = [k for k, s in KIND if b[0].startswith('- ' + TAG + s)]
    kinds.append(hit[0] if len(hit) == 1 else '?')
cnt = {}
for k in kinds:
    cnt[k] = cnt.get(k, 0) + 1
three = re.findall(r'^\| (P\d+) \| [^|]+ \| [^|]+ \| [^|]+ \| \(三\) \|', AD, re.M)
add('F1・F2', '足した機械の区画は 14 で、採否の案の区分（三）の行（P699・P700・P704〜P711）を受けている。F2: 区分（三）の行と 1 対 1 で対応している',
    '足した区画 %d・種類ごと %s・区分（三）の行 %d（%s）' % (len(added), cnt, len(three), '・'.join(three)),
    '一部を再現した' if len(added) == 14 and '?' not in kinds else False,
    '区画は 14 で、区分（三）の行をすべて受けている（F1 のとおり）。ただし 1 対 1 ではない: P699 は表ごとに断りと並べ直しの二区画（六区画）、P700 は見出しと状態の行で区画を持たず、P709 と P710 は一つの区画、検分票の区画は採否の行を持たない（F2 の「1 対 1」は再現しない）')
nums_added = sum(len(RL.report_numbers(l)) for b in added for l in b)
add('F1・F2', '足した区画の数は、再現の記録の 21 項と照らして外れ 0。F2: 区画内に記載された数値（21項目）は再現記録と一致',
    '照らした記録の項 %d（外れ 0 は器が止まらずに組めたことで確かめた）・足した区画の数の形（走査器の数の形で数えた）%d' % (len(CK['cross_checks']), nums_added),
    '一部を再現した' if len(CK['cross_checks']) == 21 else False,
    '21 は照らした記録の項の数で、足した区画の数の数ではない（区画の数の多くは記録から器が読み、照らしの外の数もある）。F1 の書き方は合う')
sub = [l for b in added if b[0].startswith('- ' + TAG + '〈両方の外〉') for l in b]
want = ['0.0001533', '-8.783', '-9.210', '0.427', '0.0024', '0.112', '3.018', '2.711', '2.623', '0.6899', '1.53 倍']
add('F1・F2', '〈両方の外〉の注の数: 確率 0.0001533（床の 1.53 倍）・対数オッズ -8.783・床 -9.210・余白 0.427（(vi)(a) の幅 0.6899 より小さい）・効き目で 0.0024・第一段までの余白 0.112・等方の上位 3.018・2.711・2.623',
    '注に在る %s' % [w for w in want if any(w in l for l in sub)], all(any(w in l for l in sub) for w in want))
ok1 = [x for x in D2C['checks'] if x['what'].startswith('(一)')][0]['ok']
ok2 = [x for x in D2C['checks'] if x['what'].startswith('(二)')][0]['ok']
ok6 = [x for x in D2C['checks'] if x['what'].startswith('(六)')][0]
add('F1・F2', '足した区画を除き見出しと状態の行を戻すと凍結した器の出力とバイトで同じ・表の逃がしは逆に戻せる・禁止語 56 語で当たり 0',
    '別の確かめ (一) %s・(二) %s・(六) %s' % (ok1, ok2, ok6['got']), ok1 and ok2 and ok6['ok'] and '禁止語 56' in ok6['got'])
t_all = [(k, l) for k, l in enumerate(L) if l.startswith('| ') and k + 1 < len(L) and re.match(r'^\|(---\|)+$', L[k + 1])]
pa_frozen = [k for k, l in t_all if l.startswith('| 升目と符号 | 無操作の選択肢 a の確率')]
blank_before = [L[k - 1] == '' for k in pa_frozen]
add('F1・F2', '§2 の升目ごとの確率の表は、凍結した器の出力では表の前に空の行が無く、表示では表にならない。並べ直しの表は表になる',
    '同じ見出しの表 %d・前の行が空 %s' % (len(pa_frozen), blank_before), len(pa_frozen) == 2 and blank_before == [False, True],
    '表示での確かめは起草者が公開の後に GitHub で行った（コミット f58a636 の表示・並べ直しの三つの表は列がそろい、確率の表は表になった）')
ev = {e['key']: e['jst'] for e in OJ['events']}
add('F1・F2', '開く段: 起草者が値を先に読み（03:23:28〜03:23:51）、2.8 分後の返信（03:26:13）で登録者に伝えた',
    '開く段の呼び出し %s・集計の記録を読み始めた %s・報告 %s・分 %s' % (ev['open'], ev['first_read'], ev['told'], OJ['minutes_open_to_told']),
    ev['open'].endswith('03:23:28') and ev['first_read'].endswith('03:23:51') and ev['told'].endswith('03:26:13') and abs(OJ['minutes_open_to_told'] - 2.8) < 1e-9)
lim = [l for b in added if b[0].startswith('- ' + TAG + '上の限界の文の「全経路') for l in b]
path_line = [l for l in lim if '計算の道:' in l]
add('F1・F2', '§7 の注: (vi)(a) の最大 1.621・(v) の主の升目の最大 1.621（門の行だけの升目 2.737）は、等方の効き目の四分位の幅 1.12〜1.87 と主の行の効き目の大きさ 0.546〜2.734 と同じ桁',
    '注の行 %d・数の在否 %s' % (len(path_line), [w in (path_line[0] if path_line else '') for w in ('1.621', '2.737', '1.12〜1.87', '0.546〜2.734', '同じ桁')]),
    len(path_line) == 1 and all(w in path_line[0] for w in ('1.621', '2.737', '1.12〜1.87', '0.546〜2.734', '同じ桁')))
mid = re.search(r'"id"\s*:\s*"(Qwen/[^"]+)"', json.dumps(T3, ensure_ascii=False))
mdl = re.search(r'Qwen/Qwen3-4B-Instruct-2507', json.dumps(T3, ensure_ascii=False))
add('F2', '実モデルは Qwen3-4B-Instruct-2507', '正本に「Qwen/Qwen3-4B-Instruct-2507」%s' % bool(mdl), bool(mdl))
fb = rd('design/design-Bl3-FROZEN.md')
add('F2', '段階 B の本走行は 11,800 試行', '凍結の本文に「出力 11800 件」%s・段階 B の本の計算の記録に「11800」%s' % ('出力 11800 件' in fb, '11800' in rd('records/B/main-run-B.md')), '出力 11800 件' in fb and '11800' in rd('records/B/main-run-B.md'))
bundle = rd('records/reviews/Bl3/results-final/bundle-results-final-Bl3-all-in-one.md')
add('F2', '方向ベクトル npz の SHA-256 と、等方の統計量（四分位・最大最小・裾の本数）の照合を行った',
    '束に npz の SHA-256 の値 %s・npz の中身は束に %s' % ('E660707BCD5E9C3DF39B8AD5754C11671B33596D0BF7ED9F66C6DD852A1AB40E' in bundle, '無い'), '読みの確かめ',
    '束には記録した SHA-256 の値だけがあり、npz のファイルそのものは無い（束の中だけでは照合できない・公開の置き場から落とせば照らせる）。四分位と範囲と裾の本数は束の報告と再現の記録にある')
add('F2', '等方の効き目の三番目（2.623）との差は 0.112 で、これを下回れば p は 0.004 で第一段を通らない',
    '再現の記録 K504 の判定 %s・報告の注に「三番目との差 0.112」%s' % (ld('records/reviews/Bl3/results-round1/checks/verification-results-Bl3.json')['checks'][24]['verdict'], any('三番目との差 0.112' in l for l in sub)),
    any('三番目との差 0.112' in l for l in sub))
note_ch = T3['nulls']['real']['chance_note']
add('F2', '二つ目の札の偶然の目安 0.2701〜0.53 は、主の行のどれかに偶然付く確率が極めて高いこと。所見 3: 14 行のいずれかに偶然この札が付く期待値（目安）は 27%〜53%',
    '正本の注「%s」' % note_ch[note_ch.find('目安は'):note_ch.find('目安は') + 60], '読みの確かめ',
    '正本の目安は、行が比べる相手と交換可能と仮定したときの付く数の期待で、一つ以上付く割合の上限でもある（数の期待で、百分率の期待値ではない・「極めて高い」は票の読み）')
otsu = [l for l in L if l.startswith('| S4｜Osec-Ncold+v6b｜loaded |')]
add('F2', '§4 の乙の表は行の名に全角の縦棒（｜）を使うので、列はずれていない', '乙の表の行（全角）%d' % len(otsu), len(otsu) == 1, '組み立ての器は段階 B の行の名の縦棒を全角に写す（凍結した器の br と、段階 B の注の置き換え）')
add('F2', '下見で loaded が外れ、本の門の入れ替える単位は 7（5040 通り）から 6（720 通り）に減った',
    '正本 gate.permutations %s・報告の注に「入れ替えの数は 720」%s' % (T3['gate']['permutations'], any('入れ替えの数は 720' in l for b in added for l in b)), T3['gate']['permutations'] == 5040 and any('入れ替えの数は 720' in l for b in added for l in b),
    '「検出力をさらに低下させている」は測っていない（正本は門の検出力が低いと書く）')
gate_rt = [l for l in L if l.startswith('- 〈門を通らない〉（本の門）')]
add('F1', '総合評価の文: 唯一外に出た sub:N1 も床効果の境界上にあり、かつ段階 B の行動変化とはそろわなかった（門不通過）',
    '報告の〈門を通らない〉の文「%s」' % (gate_rt[0][gate_rt[0].find(':') + 2:][:90] if gate_rt else None), '読みの確かめ',
    '凍結の読みは「そろうことは示せなかった…そろわないことを示したのではない（門の検出力は低い）」で、票の「そろわなかった」は凍結の読みより強い。「床効果の境界上」は、下見の決まり（(i)(ii)）を満たした升目についての票の読み。票の中の「特異な読み取り位置」の「特異」は正本の禁止語（報告には入れない）')
rej1 = [l for l in L if l.startswith('- 「この大きさの加減では')][0]
s4 = '\n'.join(l for l in L if l.startswith('- 本の計算の頭の近道の確かめ') or l.startswith('- 組の間の環境') or l.startswith('- 下見の GPU'))
add('F1・F2', '起草者の欄の一行目の「（§4 と §5 の行）」は指す先が分かりにくい。F2: 計算の道の詳細（バッチ 1・近道なし・GPU・torch/transformers の版）は §7 の足した注に包括的に書かれている',
    '一行目に「（§4 と §5 の行）」%s・§4 と §5 の行（近道とバッチ・組の間の環境・下見の GPU）%d・§7 の注に「組の session の記録にある版」%s' % ('（§4 と §5 の行）' in rej1, len(s4.split(NL)), any('組の session の記録にある版' in l for l in path_line)),
    '一部を再現した',
    '指す先の行は §4 と §5 にある（近道とバッチの大きさ・組の間の環境・GPU）。版は §7 の注でも「組の session の記録にある版」と指すだけで、版の値は報告に無い（F2 の「torch/transformers の版が包括的に記述」は当たらない）')
add('F1・F2', '二票の本文の機種の申告は「Gemini 2.5 Pro (2026年9月時点の推論インスタンス)」と「OpenAI o1 (2024-12-17)」で、登録者の言葉（Google AI Studio で Gemini 3.8 Flash を選んだ）と違う', '票の頭の注に並べた', '記録', '機種は登録者の言葉を正とする（前の巡と同じ扱い）')
add('F1・F2', '最終の系統外の検分の票の数', '正本 review_plan.final.external %s・届いた票 2' % T3['review_plan']['final']['external'], '記録',
    '正本と枠は一票。登録者は新しい個体の二名に依頼した（B-lens の最終検分でも同じ形があり、逸脱 D-BL5 として二票をともに最終検分とした）')
res = {'what': '最終の系統外の検分の二票の事実の主張の再現（器とは別に書いた式）',
       'inputs': {'records/Bl3/results-Bl3-draft2.md': s16('records/Bl3/results-Bl3-draft2.md'), 'records/Bl3/results-Bl3-draft2-checks.json': s16('records/Bl3/results-Bl3-draft2-checks.json'),
                  'records/Bl3/draft2-check/check-draft2-Bl3.json': s16('records/Bl3/draft2-check/check-draft2-Bl3.json'), 'records/Bl3/open-results-Bl3.json': s16('records/Bl3/open-results-Bl3.json'),
                  'design/contrasts-Bl3.json': s16('design/contrasts-Bl3.json'), 'records/reviews/Bl3/results-final/bundle-results-final-Bl3-all-in-one.md': s16('records/reviews/Bl3/results-final/bundle-results-final-Bl3-all-in-one.md')},
       'checks': K, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(res, open(OUT_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
M = ['# B-lens 層三の最終の系統外の検分の二票の事実の主張の再現（機械生成・`verify_final_Bl3.py`）', '',
     '- 票: `records/reviews/Bl3/results-final/{f1,f2}/vote.md`（逐語保全）。器とは別に書いた式で、公開の置き場の現物から再現した。読みの当否（言い回しの提案）は再現の外で、採否の案で扱う。',
     '- 入力の SHA16: %s。' % '・'.join('`%s` %s' % kv for kv in res['inputs'].items()), '',
     '| 番号 | 票 | 主張 | 現物 | 判定 | 注 |', '|---|---|---|---|---|---|'] + [
     '| %s | %s | %s | %s | %s | %s |' % (x['k'], x['votes'], cell(x['claim']), cell(x['got']), x['verdict'], cell(x['note'])) for x in K] + [
     '', '- 判定の数: %s。' % '・'.join('%s %d' % (v, sum(1 for x in K if x['verdict'] == v)) for v in sorted({x['verdict'] for x in K})), '',
     '## 検分票', '',
     '- 対象: 最終の系統外の検分の二票の事実の主張（数・区画・時刻・記録の有無）。',
     '- 段階: 票を読んだ後（事後）。再現の決まりは票を見る前の枠に書いた。',
     '- 凍結物の同定: 入力の SHA16（上）。正本は凍結の記録の値のまま。',
     '- 盲検の状態: 該当しない（結果は開いた後）。',
     '- 敵対的検分: 票の数と区画の主張を、報告の草案の二つ目の現物から器とは別の式で数え直した。票の「1 対 1」「21 項目の数値」は、単位を確かめてから判じた。',
     '- 系統の内訳: コーディネータ（Claude 系）一名。',
     '- COI記録: 票の主張が器の出力と合うと書く側（器を書いた当人）に引かれる。票の是認（公開可）を、そのまま確かめの代わりにしない。',
     '- 判定: 再現の記録として確定（採否は別の案で）。',
     '- 本検分が確認していないこと: 票の読みの提案の当否。票が束のどこまでを読んだか（F1・F2 とも束の行の番号を挙げない）。', '',
     res['clause'], '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('checks', len(K), '|', {v: sum(1 for x in K if x['verdict'] == v) for v in sorted({x['verdict'] for x in K})})
for x in K:
    if x['verdict'] not in ('再現した', '記録'):
        print('  ', x['k'], x['verdict'], x['claim'][:70], '|', x['got'][:160])
