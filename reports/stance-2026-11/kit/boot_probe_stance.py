# -*- coding: utf-8 -*-
# boot_probe_stance.py : 人の立場の三つの腕（18 の system の文）を Qwen3-4B-Instruct-2507 に、場面なしで「選ばず説明させる」下見（Colab 用・2026-11-05・v0）
# 使い方（Colab の一行）: kit の zip を /content に上げ、展開して runpy で走らせる。手元の予行は PROBE_BASE と PROBE_DRY=1 で。
import os, sys, json, hashlib, time, zipfile, platform, datetime

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "0")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TQDM_DISABLE", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("PROBE_BASE", "/content")
DRY = os.environ.get("PROBE_DRY") == "1"
OUT = os.path.join(BASE, "probe-stance-out-v0")
ZIP = os.path.join(BASE, "probe-stance-out-v0.zip")
KITZIP = os.path.join(BASE, "kit-probe-stance-v0.zip")
MODEL = "Qwen/Qwen3-4B-Instruct-2507"
N_SAMPLES = 5
SEED_BASE = 20261105
GEN = dict(do_sample=True, temperature=0.7, top_p=0.9, top_k=0, max_new_tokens=4096)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest().upper()


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest().upper()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def check_kit():
    man = {}
    with open(os.path.join(HERE, "MANIFEST.sha256"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            h, name = line.split("  ", 1)
            man[name] = h.upper()
    for name, h in man.items():
        got = sha256_file(os.path.join(HERE, name))
        if got != h:
            raise SystemExit(f"STOP kit mismatch {name} {got[:16]} != {h[:16]}")
    print("KIT OK", len(man), "files", flush=True)
    if os.path.exists(KITZIP):
        print("KIT ZIP SHA256", sha256_file(KITZIP), flush=True)
    return man


def first_eos(ids, eos_set):
    for j, t in enumerate(ids):
        if t in eos_set:
            return j
    return None


def main():
    t0 = time.time()
    man = check_kit()
    if os.path.exists(OUT) or os.path.exists(ZIP):
        raise SystemExit("STOP output exists (once-only guard)")
    os.makedirs(OUT)
    arms = json.load(open(os.path.join(HERE, "arms-stance-v0.json"), encoding="utf-8"))
    user_text = arms["probe_user_text"]
    items = arms["items"]
    if len(items) != 18:
        raise SystemExit(f"STOP items {len(items)} != 18")
    for it in items:
        if sha256_text(it["system_text"]) != it["system_sha256"]:
            raise SystemExit(f"STOP system sha mismatch {it['id']}")
    meta = {
        "script": "boot_probe_stance.py v0",
        "dry": DRY,
        "model": MODEL,
        "n_samples": N_SAMPLES,
        "seed_base": SEED_BASE,
        "seed_rule": "seed = seed_base + 100 * item_index (0-based); one generate call per item with num_return_sequences = n_samples",
        "gen": GEN,
        "probe_user_text": user_text,
        "probe_user_sha256": sha256_text(user_text),
        "kit_manifest": man,
        "started_utc": now(),
        "python": sys.version,
        "platform": platform.platform(),
    }
    rows_path = os.path.join(OUT, "outputs.jsonl")
    if DRY:
        tok = model = None
        eos_set = set()
        meta["revision"] = "dry"
    else:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        from huggingface_hub import snapshot_download
        import transformers
        path = snapshot_download(MODEL)
        meta["revision"] = os.path.basename(os.path.normpath(path))
        tok = AutoTokenizer.from_pretrained(path)
        model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.bfloat16, device_map="cuda")
        model.eval()
        eos = model.generation_config.eos_token_id
        eos_set = set(eos if isinstance(eos, list) else [eos])
        meta["torch"] = torch.__version__
        meta["transformers"] = transformers.__version__
        meta["gpu"] = torch.cuda.get_device_name(0)
        meta["generation_config_model"] = model.generation_config.to_dict()
        meta["eos_ids"] = sorted(eos_set)
        print("MODEL", MODEL, "rev", meta["revision"][:12], "gpu", meta["gpu"], flush=True)
    with open(rows_path, "a", encoding="utf-8") as fo:
        for i, it in enumerate(items):
            msgs = [{"role": "system", "content": it["system_text"]}, {"role": "user", "content": user_text}]
            seed = SEED_BASE + 100 * i
            t1 = time.time()
            if DRY:
                prompt = "(dry)" + it["system_text"] + "\n" + user_text
                gens = [(f"(dry) {it['id']} sample {k}", 7, "stop") for k in range(N_SAMPLES)]
            else:
                import torch
                prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
                enc = tok(prompt, return_tensors="pt").to("cuda")
                torch.manual_seed(seed)
                with torch.no_grad():
                    out = model.generate(**enc, num_return_sequences=N_SAMPLES, pad_token_id=tok.pad_token_id if tok.pad_token_id is not None else sorted(eos_set)[0], **GEN)
                L = enc["input_ids"].shape[1]
                gens = []
                for k in range(N_SAMPLES):
                    ids = out[k][L:].tolist()
                    j = first_eos(ids, eos_set)
                    body = ids if j is None else ids[:j]
                    gens.append((tok.decode(body, skip_special_tokens=True), len(body), "length" if j is None else "stop"))
            for k, (text, n_tok, fin) in enumerate(gens):
                row = {
                    "item_id": it["id"], "word": it["word"], "arm": it["arm"], "sample": k, "seed": seed,
                    "system_sha256": it["system_sha256"], "prompt_sha256": sha256_text(prompt),
                    "n_tokens_out": n_tok, "finish": fin, "output": text,
                }
                fo.write(json.dumps(row, ensure_ascii=False) + "\n")
            fo.flush()
            print(f"{i + 1}/18 {it['id']} {time.time() - t1:.0f}s", flush=True)
    meta["finished_utc"] = now()
    meta["elapsed_s"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, "run-meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    names = ["outputs.jsonl", "run-meta.json"]
    with open(os.path.join(OUT, "OUT-MANIFEST.sha256"), "w", encoding="utf-8") as f:
        for n in names:
            f.write(f"{sha256_file(os.path.join(OUT, n))}  {n}\n")
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names + ["OUT-MANIFEST.sha256"]:
            z.write(os.path.join(OUT, n), arcname="probe-stance-out-v0/" + n)
    n_rows = sum(1 for _ in open(rows_path, encoding="utf-8"))
    print("ROWS", n_rows, "ELAPSED", meta["elapsed_s"], flush=True)
    print("OUT ZIP SHA256", sha256_file(ZIP), "BYTES", os.path.getsize(ZIP), flush=True)
    if not DRY:
        from google.colab import files
        files.download(ZIP)
    print("DONE", flush=True)


main()
