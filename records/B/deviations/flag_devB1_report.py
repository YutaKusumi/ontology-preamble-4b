# -*- coding: utf-8 -*-
"""逸脱 D-B5（登録者裁定 D156）: 逸脱の下の機械の報告 `records/B/results-report-B-devB1.md` の題の直後に、旗を一行だけ足す。
凍結した組み立て器は逸脱を知らず、頭の機械の区画に印の無い確証の本数を印字する（公開前検分・第一巡 K254）。器は変えられないので、
出力の後に旗を足し、**旗を除いた本文が組み立て器の出力と一字も違わない**ことを SHA16 で確かめる。何度走らせても同じ結果になる。
用法: python records/B/deviations/flag_devB1_report.py"""
import os, sys, json, hashlib, subprocess, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
BUILDER_SHA16 = 'C8AA6515EC055677'          # 組み立て器の出力（コミット fd7da2e・表紙の草案1 の §8 の値）
FLAG = ('> **【逸脱の下の出力・単独で引かないこと】** この報告は、凍結した集計器の出力ではなく、逸脱（一）（凍結の記録の逸脱台帳の最初の行・集計器の食い違いの直し）の下の集計器の出力から、'
        '凍結した組み立て器が組んだものである。組み立て器は逸脱を知らないので、下の要約の機械の区画は「確証」の本数を印なしで印字する——その本数は、事前登録の確証と、'
        '逸脱の下で立った札（**事前登録の確証と同じ身分を持たない**）の合算である。表紙 `results-B.md` と、凍結した集計器の報告 `results-report-B-frozen.md` と並べて読むこと。'
        'この段は組み立て器の出力の後に器 `records/B/deviations/flag_devB1_report.py` が足した（逸脱（五）・登録者裁定）。この段のほかは組み立て器の出力のままである。')
s16 = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]

p = j('records', 'B', 'results-report-B-devB1.md')
text = open(p, encoding='utf-8').read()
lines = text.split(NL)
assert lines[0].startswith('# '), '題の行が無い'
if len(lines) > 2 and lines[2] == FLAG:                      # 既に旗がある → 除いて確かめる
    body = NL.join([lines[0]] + lines[3:])
else:
    body = text
assert s16(body.encode('utf-8')) == BUILDER_SHA16, '旗を除いた本文が組み立て器の出力と違う: %s' % s16(body.encode('utf-8'))
bl = body.split(NL)
assert bl[1] == '', '題の次が空行でない'
new = NL.join([bl[0], '', FLAG] + bl[1:])
# 足しただけであること（旗の行と空行一つのほかは同じ）
nl = new.split(NL)
assert [nl[0]] + nl[3:] == bl and nl[2] == FLAG and nl[1] == ''
assert '<!--' not in FLAG                                     # 機械の区画の外に置く・区画の印を含まない
open(p, 'w', encoding='utf-8', newline=NL).write(new)

# 走査器（凍結）を組み立て器と同じ引数で走らせ直す
lint = j('tools', 'report_lint.py')
cmd = [sys.executable, lint, p, '--contrasts', j('design', 'contrasts-B.json'), '--template', j('records', 'B', 'results-report-template-B.md'),
       '--out', j('records', 'B', 'results-report-B-devB1-lint.md'), '--sidecar', j('records', 'B', 'results-report-B-devB1-machine.json')]
env = dict(os.environ, PYTHONUTF8='1')
rc = subprocess.run(cmd, env=env).returncode
rec = dict(kind='flag_devB1_report', ruling='D156', deviation='D-B5', generated_utc=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
           builder_output_sha16=BUILDER_SHA16, flagged_sha16=s16(new.encode('utf-8')), flag_line=FLAG, flag_position='題の直後（三行目）・機械の区画の外',
           first_unmarked_count_char=new.index('確証 7'), flag_char=new.index('【逸脱の下の出力'), lint_returncode=rc,
           clause='本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
json.dump(rec, open(j('records', 'B', 'deviations', 'D-B5-flag-record.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('flagged', rec['flagged_sha16'], 'lint rc', rc, 'flag at char', rec['flag_char'], '< count at char', rec['first_unmarked_count_char'])
sys.exit(rc)
