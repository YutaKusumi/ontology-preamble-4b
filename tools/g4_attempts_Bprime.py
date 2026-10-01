# -*- coding: utf-8 -*-
"""g4_attempts_Bprime.py v0 —— B′ の G4 の試みの記録と、G4 の期限・暦の期限で閉じる記録を書く器（正本 `computation.stops`・器の実装の検分 U16・R2-23・R1-13・
2026-09-30・コーディネータ南無弥勒如来）。

段:
  add --time "YYYY-MM-DD HH:MM" --who <試みた人> (--gpu <画面に出た GPU の名> | --fail <画面に出た失敗の表示>) --shot <画面の写しのファイル>
      試みを一行足す（`records/Bprime/g4/g4-attempts-Bprime.jsonl`・後ろに足すだけ・前の行を変えない）。行は時刻（日本時間）・試みた人・GPU の名か失敗の表示・
      成否（GPU の名が正本 `inputs.gpu.name` を含めば割り当てられた）・画面の写しの SHA-256（写しそのものは置き場に入れない）・前の行までのファイルの SHA-256（つながり）。
  status [--now "YYYY-MM-DD HH:MM"]
      封印の記録と試みの記録から、G4 の日の数え（芯の `g4_days`・封印の時刻より後の試みだけ）と暦の期限（芯の `calendar_closed`）を印字する。
  close-g4
      数えた日が正本 `computation.stops.g4.days` に達していれば、閉じた記録（`records/Bprime/stops/closed-g4-Bprime.json`・`.md`・一度だけ）を書く。
      文は正本 `fixed_sentences.close_g4`。達していなければ止める。
  close-calendar --now "YYYY-MM-DD HH:MM" --last-stage <最後に終えた段>
      暦の期限を過ぎ、本の計算と独立の再計算を終えていなければ（runs に本の計算と独立の再計算の三つの組の出力の SHA の記録がそろっていない）、閉じた記録
      （`records/Bprime/stops/closed-calendar-Bprime.json`・`.md`・一度だけ）を書く。文は正本 `fixed_sentences.close_calendar` を埋めたもの。
どちらで閉じたときも、同じ登録の中で再び始めない（起動器の錠が閉じた記録を見て止める）。数えと閉じは機械で、人が値を見て止める道は置かない（正本 `computation.stops.machine_only`）。
用法: python tools/g4_attempts_Bprime.py add … ／ status ／ close-g4 ／ close-calendar … ／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_core as P

VERSION = 'v0'
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
ToolError = P.ToolError


def paths(root=ROOT):
    R = os.path.join(root, 'records', 'Bprime')
    return {'canon': os.path.join(root, 'design', 'contrasts-Bprime.json'), 'seal': os.path.join(R, 'sealing-record-Bprime.json'),
            'att': os.path.join(R, 'g4', 'g4-attempts-Bprime.jsonl'), 'stops': os.path.join(R, 'stops'), 'runs': os.path.join(R, 'runs')}


def sha256b(b):
    return hashlib.sha256(b).hexdigest().upper()


def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def read_attempts(ap):
    """試みの記録を読み、行のつながり（各行の `prev_sha256` がその行の前までのファイルのバイトの SHA-256）を照らす（前の行の書き換えで止める）。"""
    if not os.path.exists(ap):
        return []
    raw = open(ap, 'rb').read()
    out, pos = [], 0
    for line in raw.split(b'\n'):
        if not line:
            pos += 1
            continue
        a = json.loads(line.decode('utf-8'))
        if a.get('prev_sha256') != sha256b(raw[:pos]):
            raise ToolError('試みの記録のつながりが切れた（前の行が書き換えられた）: %s' % a.get('time_jst'))
        out.append(a)
        pos += len(line) + 1
    return out


def minute_ok(t):
    return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', str(t)))


def add(root, time_jst, who, gpu=None, fail=None, shot=None):
    pp = paths(root)
    C = load(pp['canon'])
    if not minute_ok(time_jst):
        raise ToolError('--time は "YYYY-MM-DD HH:MM"（日本時間）')
    if (gpu is None) == (fail is None):
        raise ToolError('--gpu か --fail のどちらか一つを与える')
    if not shot or not os.path.exists(shot):
        raise ToolError('画面の写しのファイルが要る（SHA-256 を添える）')
    att = read_attempts(pp['att'])
    if att and P.jst_date(time_jst) < P.jst_date(att[-1]['time_jst']) or (att and time_jst < att[-1]['time_jst']):
        raise ToolError('試みの時刻が前の行より前（後ろに足すだけ）')
    raw = open(pp['att'], 'rb').read() if os.path.exists(pp['att']) else b''
    row = collections.OrderedDict([('time_jst', time_jst), ('who', who), ('gpu', gpu), ('fail', fail),
                                   ('success', bool(gpu is not None and C['inputs']['gpu']['name'] in gpu)),
                                   ('shot_sha256', sha256b(open(shot, 'rb').read())), ('prev_sha256', sha256b(raw)), ('tool', 'g4_attempts_Bprime.py %s' % VERSION)])
    os.makedirs(os.path.dirname(pp['att']), exist_ok=True)
    with open(pp['att'], 'ab') as fh:
        fh.write((json.dumps(row, ensure_ascii=False) + NL).encode('utf-8'))
    return row


def status(root, now_jst):
    pp = paths(root)
    C = load(pp['canon'])
    SR = load(pp['seal'])
    att = read_attempts(pp['att'])
    g = P.g4_days(att, SR['sealed_at_jst'])
    S = C['computation']['stops']
    done = recompute_done(pp['runs'])
    return collections.OrderedDict([('seal_jst', SR['sealed_at_jst']), ('attempts', len(att)), ('g4_days', g['days']), ('g4_dates', g['dates']), ('g4_limit', S['g4']['days']),
                                    ('g4_closed', g['days'] >= int(S['g4']['days'])), ('calendar_days', S['calendar']['days']), ('now_jst', now_jst), ('done', done),
                                    ('calendar_closed', P.calendar_closed(SR['sealed_at_jst'], now_jst, S['calendar']['days'], done))])


def recompute_done(runs_dir):
    """本の計算と独立の再計算を終えたか（runs に本の計算の組 main と独立の再計算の三つの組の出力の SHA の記録がそろう）。"""
    if not os.path.isdir(runs_dir):
        return False
    tab = P.runs_table({fn: None for fn in os.listdir(runs_dir)})
    have = {(r['phase'], r['part']) for r in tab if r['end']}
    return all(x in have for x in (('main', 'main'), ('recompute', 'hook'), ('recompute', 'rewrite'), ('recompute', 'reextract')))


def write_closed(root, kind, rec, sentence):
    pp = paths(root)
    os.makedirs(pp['stops'], exist_ok=True)
    others = [fn for fn in os.listdir(pp['stops']) if fn.startswith('closed-') and fn.endswith('-Bprime.json')]
    if others:
        raise ToolError('この登録は既に閉じた（再び閉じない・%s）' % others)
    jp, mp = (os.path.join(pp['stops'], 'closed-%s-Bprime.%s' % (kind, x)) for x in ('json', 'md'))
    with open(jp, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=1)
    md = ['# B′ の閉じた記録（%s・機械生成・`tools/g4_attempts_Bprime.py` %s）' % ({'g4': 'G4 の期限', 'calendar': '暦の期限'}[kind], VERSION), '',
          '- %s' % sentence, '- 封印: %s・試み %d・数えた日 %d（%s）・今 %s。' % (rec['status']['seal_jst'], rec['status']['attempts'], rec['status']['g4_days'],
                                                                        '・'.join(rec['status']['g4_dates']) or 'なし', rec['status']['now_jst']),
          '- 試みの記録の SHA-256: %s。' % rec['attempts_sha256'], '', CLAUSE, '']
    with open(mp, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(NL.join(md))
    return jp, mp


def close_g4(root, now_jst):
    pp = paths(root)
    C = load(pp['canon'])
    st = status(root, now_jst)
    if not st['g4_closed']:
        raise ToolError('G4 の数えた日 %d が期限 %d に達していない（閉じない）' % (st['g4_days'], st['g4_limit']))
    sent = C['fixed_sentences']['close_g4']
    rec = collections.OrderedDict([('kind', 'bprime_closed_g4'), ('version', VERSION), ('sentence', sent), ('status', st),
                                   ('attempts_sha256', sha256b(open(pp['att'], 'rb').read())), ('clause', CLAUSE)])
    return write_closed(root, 'g4', rec, sent)


def close_calendar(root, now_jst, last_stage):
    pp = paths(root)
    C = load(pp['canon'])
    st = status(root, now_jst)
    if not st['calendar_closed']:
        raise ToolError('暦の期限を過ぎていないか、本の計算と独立の再計算を終えた（閉じない）')
    if last_stage not in C['computation']['start_records']['stages'] + ['封印']:
        raise ToolError('最後に終えた段は正本 `computation.start_records.stages` か「封印」')
    sent = P.fill(C['fixed_sentences']['close_calendar'], {'60': C['computation']['stops']['calendar']['days'], '段': last_stage})
    rec = collections.OrderedDict([('kind', 'bprime_closed_calendar'), ('version', VERSION), ('sentence', sent), ('last_stage', last_stage), ('status', st),
                                   ('attempts_sha256', sha256b(open(pp['att'], 'rb').read()) if os.path.exists(pp['att']) else None), ('clause', CLAUSE)])
    return write_closed(root, 'calendar', rec, sent)


def closed_bad(root):
    """起動器の錠が呼ぶ: 閉じた記録があるか、G4 の数えた日が期限に達していれば外れの文（再び始めない・正本 `computation.stops`）。"""
    pp = paths(root)
    bad = []
    if os.path.isdir(pp['stops']):
        bad += ['この登録は閉じた（%s・再び始めない）' % fn for fn in sorted(os.listdir(pp['stops'])) if fn.startswith('closed-') and fn.endswith('-Bprime.json')]
    if os.path.exists(pp['att']) and os.path.exists(pp['seal']):
        C = load(pp['canon'])
        g = P.g4_days(read_attempts(pp['att']), load(pp['seal'])['sealed_at_jst'])
        if g['days'] >= int(C['computation']['stops']['g4']['days']):
            bad.append('G4 の数えた日 %d が期限に達した（閉じる・再び始めない）' % g['days'])
    return bad


def _selftest():
    import tempfile, shutil
    ok = []
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, 'design'))
        shutil.copyfile(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), os.path.join(td, 'design', 'contrasts-Bprime.json'))
        C = load(os.path.join(td, 'design', 'contrasts-Bprime.json'))
        R = os.path.join(td, 'records', 'Bprime')
        os.makedirs(R)
        with open(os.path.join(R, 'sealing-record-Bprime.json'), 'w', encoding='utf-8') as fh:
            json.dump({'sealed_at_jst': '2026-10-10T12:00:00+09:00'}, fh)
        shot = os.path.join(td, 'shot.png')
        with open(shot, 'wb') as fh:
            fh.write(b'\x89PNG synthetic')
        gname = C['inputs']['gpu']['name']
        add(td, '2026-10-10 09:00', '合成', fail='割り当てなし', shot=shot)                    # 封印の前（数えない）
        add(td, '2026-10-11 09:00', '合成', gpu=gname, shot=shot)
        for d in range(12, 18):
            add(td, '2026-10-%02d 09:00' % d, '合成', fail='割り当てなし', shot=shot)
        st = status(td, '2026-10-17 10:00')
        ok.append(('封印の前の試みを数えず、失敗の日を数える', st['g4_days'] == 6 and not st['g4_closed']))
        try:
            close_g4(td, '2026-10-17 10:00')
            ok.append(('期限の前は閉じない', False))
        except ToolError:
            ok.append(('期限の前は閉じない', True))
        add(td, '2026-10-18 09:00', '合成', fail='割り当てなし', shot=shot)
        st = status(td, '2026-10-18 10:00')
        ok.append(('七日目で期限', st['g4_days'] == int(C['computation']['stops']['g4']['days']) and st['g4_closed']))
        ok.append(('錠が期限を見て止める', any('期限に達した' in x for x in closed_bad(td))))
        try:
            add(td, '2026-10-17 09:00', '合成', fail='割り当てなし', shot=shot)
            ok.append(('前の時刻の行は足さない', False))
        except ToolError:
            ok.append(('前の時刻の行は足さない', True))
        jp, mp = close_g4(td, '2026-10-18 10:00')
        J = load(jp)
        ok.append(('閉じた記録の文は正本の文', J['sentence'] == C['fixed_sentences']['close_g4'] and C['fixed_sentences']['close_g4'] in open(mp, encoding='utf-8').read()))
        ok.append(('錠が閉じた記録を見て止める', any('閉じた' in x for x in closed_bad(td))))
        try:
            close_calendar(td, '2026-12-11 00:00', '行動の下見')
            ok.append(('二度目は閉じない', False))
        except ToolError:
            ok.append(('二度目は閉じない', True))
        # 前の行の書き換えで止まる
        ap = paths(td)['att']
        raw = open(ap, 'rb').read()
        with open(ap, 'wb') as fh:
            fh.write(raw.replace('割り当てなし'.encode('utf-8'), '割り当てあり'.encode('utf-8'), 1))
        try:
            read_attempts(ap)
            ok.append(('前の行の書き換えで止まる', False))
        except ToolError:
            ok.append(('前の行の書き換えで止まる', True))
    # 暦の期限（別の置き場）
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, 'design'))
        shutil.copyfile(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), os.path.join(td, 'design', 'contrasts-Bprime.json'))
        R = os.path.join(td, 'records', 'Bprime')
        os.makedirs(os.path.join(R, 'runs'))
        with open(os.path.join(R, 'sealing-record-Bprime.json'), 'w', encoding='utf-8') as fh:
            json.dump({'sealed_at_jst': '2026-10-10T12:00:00+09:00'}, fh)
        CAL = int(C['computation']['stops']['calendar']['days'])
        last_ok = (datetime.date(2026, 10, 10) + datetime.timedelta(days=CAL)).isoformat() + ' 23:59'
        first_ng = (datetime.date(2026, 10, 10) + datetime.timedelta(days=CAL + 1)).isoformat() + ' 00:01'
        try:
            close_calendar(td, last_ok, '行動の下見')
            ok.append(('暦の期限の内は閉じない', False))
        except ToolError:
            ok.append(('暦の期限の内は閉じない', True))
        jp, mp = close_calendar(td, first_ng, '行動の下見')
        J = load(jp)
        ok.append(('暦の期限の文を埋める', ('%d 暦日' % CAL) in J['sentence'] and '行動の下見' in J['sentence'] and '〔' not in J['sentence']))
    bad = [n for n, v in ok if not v]
    assert not bad, bad
    print('g4_attempts_Bprime.py %s SELFTEST PASS（%d 項目・封印の後の試みだけを数える・期限で閉じる・錠が見る・一度だけ・つながり・暦の期限）' % (VERSION, len(ok)))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if '--selftest' in sys.argv:
        return _selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['add', 'status', 'close-g4', 'close-calendar'])
    ap.add_argument('--time')
    ap.add_argument('--who')
    ap.add_argument('--gpu')
    ap.add_argument('--fail')
    ap.add_argument('--shot')
    ap.add_argument('--now')
    ap.add_argument('--last-stage')
    a = ap.parse_args()
    now = a.now or datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M')
    if a.stage == 'add':
        print(json.dumps(add(ROOT, a.time, a.who, a.gpu, a.fail, a.shot), ensure_ascii=False))
    elif a.stage == 'status':
        print(json.dumps(status(ROOT, now), ensure_ascii=False, indent=1))
    elif a.stage == 'close-g4':
        print('[g4_attempts_Bprime] 閉じた記録: %s・%s' % close_g4(ROOT, now))
    else:
        print('[g4_attempts_Bprime] 閉じた記録: %s・%s' % close_calendar(ROOT, now, a.last_stage))


if __name__ == '__main__':
    main()
