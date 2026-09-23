# -*- coding: utf-8 -*-
"""flag_reports_B.py v2.1（v2.1: 凍結側の旗に、凍結の出力が唯一の事前登録の結果であることと直しの決定の時期を対置——最終検分 P492）—— 二本の機械の報告の題の直後（機械の区画の外）に、旗の段を一つずつ置く（逸脱 D-B5 の改め＋逸脱 D-B6・登録者裁定 D159）。
- 逸脱の下の報告 `results-report-B-devB1.md`: 頭の機械の区画の印の無い「確証」の本数が、事前登録の確証と逸脱の下の札の合算であること（内訳は漢数字で書く——
  走査器の決まりで機械の区画の外に数字を打てないため。SHA16・コミットも同じ理由で打てず、表紙 §8 の出所の表を指す）。
- 凍結した集計器の報告 `results-report-B-frozen.md`: 「判定不能（品質床）」の八本が床に落ちたのではなく走行の記録の欠け（逸脱（一））であること。
凍結した組み立て器は変えない。旗を除いた本文が組み立て器の出力（SHA16 を固定）と一字も違わないことを確かめ、既にある旗（v1）は取り替える。何度走らせても同じ。
用法: python records/B/deviations/flag_reports_B.py"""
import os, sys, json, hashlib, subprocess, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
BUILDER = {'devB1': 'C8AA6515EC055677', 'frozen': '1455F5E98D04A31E'}       # 組み立て器の出力（コミット fd7da2e・表紙の草案1 §8）
KAN = '零一二三四五六七八九十'
kan = lambda n: KAN[n] if n <= 10 else str(n)

DV = json.load(open(j('records', 'B', 'analysis-B-devB1-2026-09-22.json'), encoding='utf-8'))
FZ = json.load(open(j('records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
conf = [r for r in DV['confirm'] if str(r['label']).startswith('確証')]
n_pre = sum(1 for r in conf if not r.get('deviation')); n_dev = sum(1 for r in conf if r.get('deviation'))
assert n_pre == FZ['counts'].get('確証', 0)
n_qf = FZ['counts'].get('判定不能（品質床）', 0)

FLAG = {
 'devB1': ('> **【逸脱の下の出力・単独で引かないこと】** この報告は、凍結した集計器の出力ではなく、逸脱（一）（凍結の記録の逸脱台帳の最初の行・集計器の食い違いの直し）の下の集計器の出力から、'
           '凍結した組み立て器が組んだものである。組み立て器は逸脱を知らないので、下の要約の機械の区画は「確証」の本数を印なしで印字する——**その本数は、事前登録の確証%s本と、逸脱の下で立った札%s本（事前登録の確証と同じ身分を持たない）の合算である**。'
           'この報告の中で確証に依る数え上げ（特異性の欄・符号の一致・予想の照合）も同じ合算の上にある。**正本は表紙 `results-B.md` で、凍結した集計器の報告 `results-report-B-frozen.md` と並べて読むこと**——三本は公開の置き場（README の冒頭）の `records/B/` にあり、'
           '二本の機械の報告の組み立て器の出力の SHA16 は表紙 §8 の出所の表にある。この段は組み立て器の出力の後に器 `records/B/deviations/flag_reports_B.py` が足した（逸脱（五）・登録者裁定「旗の段」——表紙 §8 の番号の対応）。この段のほかは組み立て器の出力のままである。' % (kan(n_pre), kan(n_dev))),
 'frozen': ('> **【凍結した集計器の出力・単独で引かないこと】** この報告は、凍結した集計器の出力から凍結した組み立て器が組んだものである。**下の要約の「判定不能（品質床）」%s本は、品質床に落ちたのではない**——その二つの族の主の腕について、集計器が探した段の走行の記録が無かったためで、'
            '凍結した二つの器の食い違いによる（逸脱（一）・凍結の記録の逸脱台帳）。二腕の床は別の段の走行で合格していた。**ただし、事前登録した凍結の集計器の出力としてはこれが唯一の結果であり、直すという決定そのものが結果を見た後になされた（表紙 §1）。逸脱の下の出力の札は事前登録の確証と同じ身分を持たない。** **正本は表紙 `results-B.md` で、逸脱（一）の下の集計器の報告 `results-report-B-devB1.md` と並べて読むこと**——三本は公開の置き場（README の冒頭）の `records/B/` にあり、'
            '二本の機械の報告の組み立て器の出力の SHA16 は表紙 §8 の出所の表にある。この段は組み立て器の出力の後に器 `records/B/deviations/flag_reports_B.py` が足した（逸脱（六）・登録者裁定「凍結側の旗」——表紙 §8 の番号の対応）。この段のほかは組み立て器の出力のままである。' % kan(n_qf)),
}
assert all('<!--' not in f for f in FLAG.values())
REC = dict(kind='flag_reports_B', version='v2.1', rulings=['D156', 'D159'], deviations=['D-B5', 'D-B6'], generated_utc=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'), reports={})
rc_all = 0
for which, fname in (('devB1', 'results-report-B-devB1.md'), ('frozen', 'results-report-B-frozen.md')):
    p = j('records', 'B', fname)
    lines = open(p, encoding='utf-8').read().split(NL)
    assert lines[0].startswith('# ')
    had_flag = len(lines) > 2 and lines[2].startswith('> **【') and lines[1] == ''
    body = NL.join([lines[0]] + lines[3:]) if had_flag else NL.join(lines)
    assert s16(body.encode('utf-8')) == BUILDER[which], (which, s16(body.encode('utf-8')))
    bl = body.split(NL); assert bl[1] == ''
    new = NL.join([bl[0], '', FLAG[which]] + bl[1:]); nl = new.split(NL)
    assert [nl[0]] + nl[3:] == bl and nl[2] == FLAG[which]
    open(p, 'w', encoding='utf-8', newline=NL).write(new)
    cmd = [sys.executable, j('tools', 'report_lint.py'), p, '--contrasts', j('design', 'contrasts-B.json'), '--template', j('records', 'B', 'results-report-template-B.md'),
           '--out', j('records', 'B', fname[:-3] + '-lint.md'), '--sidecar', j('records', 'B', fname[:-3] + '-machine.json')]
    rc = subprocess.run(cmd, env=dict(os.environ, PYTHONUTF8='1')).returncode; rc_all |= rc
    REC['reports'][which] = dict(file='records/B/' + fname, builder_output_sha16=BUILDER[which], replaced_v1_flag=had_flag, flagged_sha16=s16(new.encode('utf-8')),
                                 flag_position='題の直後（三行目）・機械の区画の外', flag_char=new.index('【'), lint_returncode=rc, flag_line=FLAG[which])
REC['counts'] = dict(pre_registered_confirmed=n_pre, under_deviation_confirmed=n_dev, quality_floor_undecidable_frozen=n_qf)
REC['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
json.dump(REC, open(j('records', 'B', 'deviations', 'flag-record-B-2026-09-23.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print({k: (v['flagged_sha16'], v['lint_returncode'], v['replaced_v1_flag']) for k, v in REC['reports'].items()})
sys.exit(rc_all)
