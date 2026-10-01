# -*- coding: utf-8 -*-
"""publish_Bprime.py v0 —— B′ の作業の置き場（非公開）から、公開の置き場の形の置き場へ、移し方の表（`bprime_publish_map`）のとおりにファイルを字のまま写す器（2026-09-30・コーディネータ南無弥勒如来）。

- 写すのは表の「移す」ファイルだけ。「登録者の決め」のファイルは、`--include-open` を与えたときだけ、表の推しの行き先に写す（登録者が決めた後）。
- 行き先に同じ名のファイルがあるとき: 中身が同じなら写さない（数える）。違えば止める（上書きしない・`--replace <行き先の道筋>` で名指ししたものだけ上書き）。
- 写した表を、行き先の置き場の `records/Bprime/publish-map-Bprime.json` に書く（元の道筋・行き先の道筋・SHA-256・規則の番号・移さなかった物の数と理由・登録者の決めの物）。
- 作業の置き場のファイルは変えない。行き先が git の作業木でも、コミットと push はしない（push は登録者の確認を得てから別に行う）。
- 合成データの正式の確かめでは、一時の置き場に公開の形を作るのに使う（`--to <一時の置き場>`）。本物の公開の置き場へ写すのは、登録者の確認の後。
用法: python tools/publish_Bprime.py --to <行き先の置き場> [--include-open] [--replace <道筋> …] [--plan-only] ／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, hashlib, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_publish_map as PM

VERSION = 'v0.1'        # v0.1（2026-09-30・D271）: 登録者の決めの物が無くなったので、自己検査はそれが零であることと、移す物に入ったことを確かめる。前の版は `prev/publish_Bprime-v0.py`
NL = chr(10)
MAP_REL = 'records/Bprime/publish-map-Bprime.json'
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 22), b''):
            h.update(blk)
    return h.hexdigest().upper()


def open_dst(rel, why):
    """登録者の決めの物の推しの行き先（理由の文の `records/Bprime/…/` の型から）。"""
    import re
    m = re.search(r'`(records/Bprime/[^`]*/)`', why or '')
    if not m:
        return None
    base = m.group(1)
    top = rel.split('/')[0] if not rel.startswith('tools/prev/') else 'tools/prev'
    rest = rel[len(top) + 1:]
    return base + rest


def publish(to, include_open=False, replace=(), plan_only=False, bp=BP):
    P = PM.plan(bp)
    if P['unmatched'] or P['collide']:
        raise SystemExit('移し方の表に当たらないファイルか、行き先の重なりがある: %s %s' % (P['unmatched'][:5], P['collide'][:5]))
    pairs = list(P['publish'])
    if include_open:
        for rel, why in P['open']:
            d = open_dst(rel, why)
            if d is None:
                raise SystemExit('登録者の決めの物の推しの行き先が読めない: %s' % rel)
            pairs.append((rel, d))
    dsts = collections.Counter(d for _, d in pairs)
    if any(n > 1 for n in dsts.values()):
        raise SystemExit('行き先の重なり: %s' % [d for d, n in dsts.items() if n > 1][:5])
    rows, same, conflicts = [], 0, []
    for src, dst in pairs:
        sp, dp = os.path.join(bp, *src.split('/')), os.path.join(to, *dst.split('/'))
        s_sha = sha256f(sp)
        if os.path.exists(dp):
            if sha256f(dp) == s_sha:
                same += 1
                rows.append({'src': src, 'dst': dst, 'sha256': s_sha, 'state': 'same'})
                continue
            if dst not in set(replace):
                conflicts.append(dst)
                continue
        rows.append({'src': src, 'dst': dst, 'sha256': s_sha, 'state': 'write'})
    if conflicts:
        raise SystemExit('行き先に中身の違う同じ名のファイルがある（上書きしない・--replace で名指しする）: %s' % conflicts[:10])
    if plan_only:
        return rows, P
    for r in rows:
        if r['state'] != 'write':
            continue
        dp = os.path.join(to, *r['dst'].split('/'))
        os.makedirs(os.path.dirname(dp), exist_ok=True)
        shutil.copyfile(os.path.join(bp, *r['src'].split('/')), dp)
        if sha256f(dp) != r['sha256']:
            raise SystemExit('写したファイルの SHA-256 が元と違う: %s' % r['dst'])
    rec = collections.OrderedDict([
        ('kind', 'bprime_publish_map'), ('version', VERSION), ('rules_tool', 'tools/bprime_publish_map.py %s' % PM.VERSION),
        ('files', [{k: r[k] for k in ('src', 'dst', 'sha256')} for r in rows]),
        ('excluded', collections.Counter(why for _, why in P['exclude'])), ('open', [{'src': s, 'why': w, 'included': include_open} for s, w in P['open']]),
        ('clause', CLAUSE)])
    mp = os.path.join(to, *MAP_REL.split('/'))
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    with open(mp, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=1)
    return rows, P


def _selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        rows, P = publish(td)
        n_w = sum(1 for r in rows if r['state'] == 'write')
        assert n_w == len(P['publish']) and all(os.path.exists(os.path.join(td, *r['dst'].split('/'))) for r in rows)
        assert os.path.exists(os.path.join(td, *MAP_REL.split('/')))
        rows2, _ = publish(td)                                # 二度目は同じ中身なので写さない
        assert all(r['state'] == 'same' for r in rows2)
        # 行き先の中身が違えば止める
        victim = rows[0]['dst']
        with open(os.path.join(td, *victim.split('/')), 'ab') as fh:
            fh.write(b'x')
        try:
            publish(td)
            raise AssertionError('中身の違う行き先を上書きした')
        except SystemExit:
            pass
        rows3, _ = publish(td, replace=[victim])
        assert [r['state'] for r in rows3 if r['dst'] == victim] == ['write']
        # 登録者の決めの物は零（D271 で移す規則に替えた）・移す物に入った
        assert P['open'] == []
        assert any(r['dst'].startswith('records/Bprime/model-feel/') for r in rows) and any(r['dst'].startswith('records/Bprime/tools/prev/') for r in rows)
    print('publish_Bprime.py %s SELFTEST PASS（写す %d・二度目は写さない・中身の違う行き先で止まる・名指しで上書き・登録者の決めの物は零）' % (VERSION, n_w))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument('--to', required=True)
    ap.add_argument('--include-open', action='store_true')
    ap.add_argument('--replace', nargs='*', default=[])
    ap.add_argument('--plan-only', action='store_true')
    a = ap.parse_args()
    rows, P = publish(os.path.abspath(a.to), a.include_open, a.replace, a.plan_only)
    c = collections.Counter(r['state'] for r in rows)
    print('[publish_Bprime] 写す %d・同じ %d・移さない %d・登録者の決め %d（%s）' % (c.get('write', 0), c.get('same', 0), len(P['exclude']), len(P['open']),
                                                                   '写した' if not a.plan_only else '計画だけ'))
