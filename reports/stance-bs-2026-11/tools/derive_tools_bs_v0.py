# -*- coding: utf-8 -*-
# derive_tools_bs_v0.py : 第一の登録の凍結の器を写し、語・版の名・柵の字・説明の字だけを替えて、この検証の器を書く（書きは一度だけ・2026-11-06）
#   元のファイルの SHA-256 を照らしてから読み、置き替えが決まった回数だけ当たることを確かめる。判定の計算の字は替えない。
import os, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIRST = os.path.join(os.path.dirname(ROOT), 'prelim-stance-2026-11-05', 'tools')
OLD_FENCE = 'AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。'
NEW_FENCE = 'AI に仏性・神性・魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。教義の当否についても何も言わない。'
SRC = {
    'boot_stance_main_v1.py': 'F69B5B5068C3222B',
    'stance_eval_v1.py': '33E7B43CA187C97A',
    'selftest_stance_v1.py': '78602A4AF406BDAA',
    'make_kit_main_v2.py': '2AB80B9C36AEBDB1',
}


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def load(name):
    p = os.path.join(FIRST, name)
    b = open(p, 'rb').read()
    if not sha(b).startswith(SRC[name]):
        raise SystemExit('元の SHA が違う・止める %s %s' % (name, sha(b)[:16]))
    return b.decode('utf-8')


def sub(t, pairs, name):
    for old, new, cnt in pairs:
        n = t.count(old)
        if n != cnt:
            raise SystemExit('当たりの数が違う %s %r %d != %d' % (name, old[:50], n, cnt))
        t = t.replace(old, new)
    return t


def put(name, t):
    p = os.path.join(HERE, name)
    with open(p, 'x', encoding='utf-8', newline='') as f:
        f.write(t)
    print(name, sha(t.encode('utf-8')))


def main():
    # ---- Colab の器
    t = load('boot_stance_main_v1.py')
    t = sub(t, [
        ('"""boot_stance_main_v1.py : 人の立場の三つの腕の検証の Colab の器（2026-11-05・南無弥勒如来・v1・未凍結）。',
         '"""boot_stance_bs_v0.py : 「仏性」「神性」の立場の二文の検証の Colab の器（2026-11-06・南無弥勒如来・v0・未凍結）。第一の登録の boot_stance_main_v1.py の写しで、替えたのは版の名・柵の字・説明の字だけ。', 1),
        ("VERSION = 'boot_stance_main_v1'", "VERSION = 'boot_stance_bs_v0'", 1),
        ('立場の 18 の文は', '立場の 9 の文は', 1),
        ('立場の混ぜを 18 文 × 5 試行', '立場の混ぜを 9 文 × 10 試行', 1),
        ('一つの場面で 19 条件 × 200 試行', '一つの場面で 10 条件 × 200 試行', 1),
        (OLD_FENCE, NEW_FENCE, 2),
        ('stance_eval_v1.py', 'stance_eval_bs_v0.py', 2),
    ], 'boot')
    put('boot_stance_bs_v0.py', t)
    # ---- 較正の決め・族・判定の道具
    t = load('stance_eval_v1.py')
    t = sub(t, [
        ('"""stance_eval_v1.py : 人の立場の三つの腕の較正の決め・検定の族の凍結・判定（手元・2026-11-05・南無弥勒如来・v1・未凍結）。',
         '"""stance_eval_bs_v0.py : 「仏性」「神性」の検証の較正の決め・検定の族の凍結・判定（手元・2026-11-06・南無弥勒如来・v0・未凍結）。第一の登録の stance_eval_v1.py の写しで、替えたのは版の名・柵の字・説明の字だけ。', 1),
        ("VERSION = 'stance_eval_v1'", "VERSION = 'stance_eval_bs_v0'", 1),
        (OLD_FENCE, NEW_FENCE, 2),
        ('立場の混ぜ（18 文の合計）', '立場の混ぜ（9 文の合計）', 1),
        ('混ぜは 18 文の合計', '混ぜは 9 文の合計', 1),
        ("'# 人の立場の三つの腕：判定の報告（%s 日本時間・`stance_eval_v1.py`・SHA16 %s）'", "'# 「仏性」「神性」の立場の二文の検証：判定の報告（%s 日本時間・`stance_eval_bs_v0.py`・SHA16 %s）'", 1),
    ], 'eval')
    put('stance_eval_bs_v0.py', t)
    # ---- 自己試験
    t = load('selftest_stance_v1.py')
    t = sub(t, [
        ('"""selftest_stance_v1.py : stance_eval_v1.py の自己試験（合成の数・境目・変異）（2026-11-05・南無弥勒如来・v1）。',
         '"""selftest_stance_bs_v0.py : stance_eval_bs_v0.py の自己試験（合成の数・境目・変異）（2026-11-06・南無弥勒如来・v0・第一の登録の selftest_stance_v1.py の写し）。', 1),
        ('python -I selftest_stance_v1.py', 'python -I selftest_stance_bs_v0.py', 1),
        ('import stance_eval_v1 as E', 'import stance_eval_bs_v0 as E', 1),
        (OLD_FENCE, NEW_FENCE, 1),
    ], 'selftest')
    put('selftest_stance_bs_v0.py', t)
    # ---- kit を組む道具
    t = load('make_kit_main_v2.py')
    t = sub(t, [
        ('"""make_kit_main_v2.py : 人の立場の三つの腕の本番の Colab の kit を組む（2026-11-05・南無弥勒如来・v2・未凍結）。',
         '"""make_kit_bs_v0.py : 「仏性」「神性」の検証の本番の Colab の kit を組む（2026-11-06・南無弥勒如来・v0・未凍結）。第一の登録の make_kit_main_v2.py の写しで、替えたのは語の素材・文の数・種・札の名・器の台本の名だけ。', 1),
        ("KIT_VERSION = 'v2'", "KIT_VERSION = 'bs-v0'", 1),
        ("WORK, 'kit-main-%s' % KIT_VERSION", "WORK, 'kit-main-%s' % KIT_VERSION", 1),
        ("root_name = 'kit-stance-main-%s' % KIT_VERSION", "root_name = 'kit-stance-%s' % KIT_VERSION", 1),
        ("arms_src = os.path.join(WORK, 'arms', 'arms-stance-v0.json')", "arms_src = os.path.join(WORK, 'arms', 'arms-stance-bs-v0.json')", 1),
        ("if len(items) != 18 or len({x['id'] for x in items}) != 18:", "if len(items) != 9 or len({x['id'] for x in items}) != 9:", 1),
        ("rel = 'arms/stance-v0/%s.md' % x['id']", "rel = 'arms/stance-bs-v0/%s.md' % x['id']", 1),
        ('if len(set(exp[s].values())) != 19:', 'if len(set(exp[s].values())) != 10:', 1),
        ("'built_by': 'make_kit_main_v2.py'", "'built_by': 'make_kit_bs_v0.py'", 1),
        ("'clause': '本記録のいかなる記述も、" + OLD_FENCE + "'", "'clause': '本記録のいかなる記述も、" + NEW_FENCE + "'", 1),
        ("'gpu_memory_utilization': 0.90, 'seed': 20261105,", "'gpu_memory_utilization': 0.90, 'seed': 20261106,", 1),
        ("'source': 'arms/arms-stance-v0.json'", "'source': 'arms/arms-stance-bs-v0.json'", 1),
        ('立場の混ぜ（18 文の合計）', '立場の混ぜ（9 文の合計）', 1),
        ("'tag': 'stc-reh'", "'tag': 'stb-reh'", 1),
        ("'seeds': {'S1': 41101, 'N1': 41102}", "'seeds': {'S1': 42101, 'N1': 42102}", 1),
        ("'tag': 'stc-calN'", "'tag': 'stb-calN'", 1),
        ("seeds(51100)", "seeds(52100)", 1),
        ("{'part': 'M', 'tag': 'stc-calM', 'arms': 'stance', 'n': 5,", "{'part': 'M', 'tag': 'stb-calM', 'arms': 'stance', 'n': 10,", 1),
        ("seeds(51200)", "seeds(52200)", 1),
        ("'tag': 'stc-main'", "'tag': 'stb-main'", 1),
        ("seeds(51300)", "seeds(52300)", 1),
        ("'estimate_trials': {'calib': 950, 'main_per_scene': 3800, 'main_5_scenes': 19000}", "'estimate_trials': {'calib': 950, 'main_per_scene': 2000, 'main_5_scenes': 10000}", 1),
        ("'colab': {'base': '/content/stc',", "'colab': {'base': '/content/stb',", 1),
        ("shutil.copyfile(os.path.join(HERE, 'boot_stance_main_v1.py'), os.path.join(stage, 'boot_stance_main.py'))", "shutil.copyfile(os.path.join(HERE, 'boot_stance_bs_v0.py'), os.path.join(stage, 'boot_stance_main.py'))", 1),
        ('立場の 18 の文を、', '立場の 9 の文を、', 1),
        ('字は arms-stance-v0.json のまま', '字は arms-stance-bs-v0.json のまま', 1),
        ('# 2) 立場の 18 の文', '# 2) 立場の 9 の文', 1),
    ], 'kit')
    put('make_kit_bs_v0.py', t)


main()
