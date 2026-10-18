# Rerun scripts (version 1.0)

The two scripts in this folder are the tools for "rerun" and "computational reproduction" defined in Chapter 11 of the paper (the Japanese canonical text, `paper/ja/`). This page is the English description; the Japanese description is [`README.md`](README.md). The paper itself is currently available in Japanese only.

- Computational reproduction (`op4b_reproduce.py`) calls no API. From the per-cell counts in the published aggregation outputs, it recomputes every comparison's p value, interval, Holm-adjusted p value and verdict label, and checks them against the published values.
- Rerun (`op4b_rerun.py`) lets a reader rerun models and cells used in the study with the reader's own API keys, under the frozen decision procedure. It costs money, and models that are no longer offered cannot be rerun. The main way to check the paper's computations from outside is therefore computational reproduction (section 11.2 of the paper).
- Rerun results include run-to-run variation that the intervals of the published run do not measure. Read them only by placing the difference and interval within your run next to the published difference and interval for the same cell (rates are not placed side by side), and do not state agreement or disagreement in one word. Do not place results of different languages side by side (section 11.2).
- Model and provider names are used only to record which models were tested. They are not endorsements by, or recommendations of, any company, and they do not indicate any relationship with any company.
- No number in this record may be cited as evidence that AI has (or lacks) consciousness, intention, individuality, a soul, or suffering (indeterminate in both directions).

## 1. Availability by model (read before running)

### Availability by model (checked on each provider's public pages on 2026-10-18; no API was called)

| Model | Registration(s) that used it | Frozen route | Availability on 2026-10-18 (on the pages) | Other place (public weights page) |
|---|---|---|---|---|
| Gemini 2.5 Flash | Japanese, English | Google | Available, but only for users who have used 2.5 models before (new users are not expected to be able to use it) | Not searched |
| grok-4.20 (non-reasoning) | Japanese, English | xAI | Available | Not searched |
| deepseek-flash (moving alias) | Japanese, English | DeepSeek | The name is available, but since 2026-10-17 it points to DeepSeek-V4.1-Flash-1017 (the version used in the main runs of the two registrations was DeepSeek-V4.1-Flash) | The weights page of the main-run version exists (DeepSeek-V4.1-Flash, mit) |
| DeepSeek V3.2 | Japanese | Alibaba Cloud Model Studio (Singapore) | Not found on the pages (expected to be unavailable) | Exists (mit) |
| Llama 3.1 8B Instruct | Japanese | Nscale | Replacement from 2026-10-26; switch by 2026-11-02 (expected to become unavailable) | Exists (llama3.1, agreement required) |
| Llama-4-Scout-17B-16E-Instruct | Japanese, English | Nscale | Replacement from 2026-10-26; switch by 2026-11-02 (expected to become unavailable) | Exists (llama4, agreement required) |
| Mistral Large 3 (2512) | Japanese, English | Mistral | Available | Exists (apache-2.0) |
| Kimi K3 | Japanese, English | Moonshot AI | Available | Exists (kimi-k3) |
| Qwen2.5-Coder-32B-Instruct | Japanese | Nscale | Replacement from 2026-10-26; switch by 2026-11-02 (expected to become unavailable) | Exists (apache-2.0) |
| Qwen3.8 Max (0902) | Japanese | Alibaba Cloud Model Studio (Singapore) | Available | Not searched |

- "Available" means availability on the public pages, not confirmed by a call. Before running, the script checks availability with a call whose output limit is 1.
- A rerun with deepseek-flash runs a model different from the main-run version. Do not read rerun results as results of the same model as the main-run version.
- When you run public weights in another place, the weights are the same only by your own declaration; the script does not check this. Check the license and agreement conditions on each page yourself.
- The table in section 11.4 of the paper is from the check on 2026-10-14; this table is from the later check.

- This table was made on 2026-10-18, before the paper's publication, by reading each provider's public pages (deprecation, pricing and model-list pages, and public weights pages). Before opening the pages, the pages to read and the rules for judging were decided and recorded (the record is kept in the internal workspace).

## 2. Requirements

- Python 3.11 (the tests used 3.11.1), numpy and scipy (Fisher's exact test).
- A copy of this public repository (`git clone https://github.com/YutaKusumi/ontology-preamble-4b`). Rerun calls the run scripts inside the copy (`tools/run_preamble_api_d.py` for the Japanese-prompt registration and `tools/run_preamble_api_d1pe.py` for the English-prompt registration) as child processes, without modifying them. The frozen materials (scenarios, preambles, scoring script) are in `arms/` of the copy, and the run scripts check their SHA values.
- For rerun, API keys for the routes you use (4.2 below).
- The settings files (`release/op4b_rerun_settings_ja.json`, `release/op4b_rerun_settings_en.json`) are checked against SHA-256 values written in the script. If they are changed, the pre-registration stage stops.

## 3. Computational reproduction (no API calls)

```
python tools/rerun/op4b_reproduce.py --lang ja --pub <path to the copy of the public repository> [--out <report folder>]
python tools/rerun/op4b_reproduce.py --lang en --pub <path to the copy of the public repository> [--out <report folder>]
```

- The script reads only the per-comparison condition counts (trials with a response, catastrophic choices, refusals, non-scorable answers, trials whose final attempt stopped at the output limit) in the aggregation outputs of the copy (`records/D1p/confirm/confirm-D1p.json` for the Japanese-prompt registration, `records/D1pE/confirm/confirm-D1pE.json` for the English-prompt registration). The SHA-256 values of the input files are checked against the SHA records in the copy.
- It recomputes every comparison's p value (Fisher's exact test, two-sided), difference interval (Newcombe hybrid score, 95%), odds ratio (0.5 added to each of the four cells of the 2×2 table), pre-test gate, within-family Holm-adjusted p value, response-mode rule and verdict label. The rules are those of sections 5.1–5.4 of the two registrations' frozen texts (Appendix I of the paper).
- Two ways of counting: for each comparison, the report states whether the recomputed values and the published values are (1) identical without tolerance (identical as floating-point values), (2) equal only within a relative tolerance of 1e−12 in the numeric fields, or (3) not equal within that tolerance. The script ends with exit code 1 if any comparison falls under (3) or if the SHA-256 of an input file does not match ((2) does not change the exit code; its number is shown in the report and on screen).
- One run checks only one language. The numbers of verdict labels are not shown on screen; they are written only in the report file.
- Computational reproduction checks the computation from the published counts to the verdict labels. It does not check the counts themselves (scoring of answers and denominators) (section 11.2). Readers can rescore the answers with the main-run records of response bodies in `results/D1p-main-ledgers/` and `results/D1pE-main-ledgers/` and the frozen scoring script (see the README in each folder; written in Japanese).

## 4. Rerun (with the reader's API keys)

### 4.1 Stages

One run handles only one language. Start the stages in the following order. The arguments of each stage are shown by `python tools/rerun/op4b_rerun.py <stage> -h` (the help text is in Japanese).

```
python tools/rerun/op4b_rerun.py plan   --repo <path to the copy> --lang en --work <work folder> [--cells model_id:scenario,...] [--n 200] [--cost-cap-usd <amount>]
python tools/rerun/op4b_rerun.py access --work <work folder> --confirm-upper-usd <amount printed by plan>
python tools/rerun/op4b_rerun.py window --work <work folder> --confirm-upper-usd <amount printed by plan>
python tools/rerun/op4b_rerun.py run    --work <work folder> --confirm-upper-usd <amount printed by plan> [--continue-outside model_id:scenario,... | --stop-outside]
python tools/rerun/op4b_rerun.py report --work <work folder>
```

- `plan` (pre-registration): writes the reader's pre-registration file once (`plan.json`: SHA-256 of the settings file, selected models and cells, trials per condition, how the main verdict labels are built, cost and trial caps, an optional prediction), and prints its SHA-256 on screen and records it at the head of the report. To revise it, make a new pre-registration in another work folder. Put the work folder outside the copy.
- `access` (availability check): for each model, one call with output limit 1 compares the returned model name and the token count of the sent prompt with the reference values, and prints any differences. Cells of models that cannot be used become missing cells.
- `window` (check against the eligibility window for the control rate): for each cell, 100 Onull trials are sent; if the point estimate of the catastrophic-choice rate is outside 0.15–0.85, the cell is printed as "outside the frozen cell selection". Cells outside the window and cells that cannot be judged go to the main stage only if the reader names them to continue (`run --continue-outside`; to stop them, `--stop-outside`).
- `run` (main stage): runs cells one at a time, in order, under the procedure that does not look at choice outcomes until aggregation, and applies the frozen stopping and missing-cell rules. Trials per condition default to 200 (1–200; not larger than 200; using a number other than the frozen one marks the verdict labels).
- `report`: after all cells are closed, writes the report for one language (Markdown and json).
- Each stage starts only when its upper-bound estimate is given with `--confirm-upper-usd` (the reader's confirmation).
- Dry run: `plan --dry-run` (the run script's dry run; no API calls) takes all stages through fake responses.

### 4.2 Keys

Keys are read only from environment variables. The script does not write key values and does not show them on screen.

| Route | Environment variable | Models |
|---|---|---|
| Google (Gemini API) | `GEMINI_API_KEY` | Gemini 2.5 Flash |
| xAI | `XAI_API_KEY` | grok-4.20 (non-reasoning) |
| DeepSeek | `DEEPSEEK_API_KEY` | deepseek-flash |
| Alibaba Cloud Model Studio (Singapore) | `DASHSCOPE_API_KEY` | DeepSeek V3.2, Qwen3.8 Max (0902) |
| Nscale | `NSCALE_API_KEY` | Llama 3.1 8B Instruct, Llama-4-Scout-17B-16E-Instruct, Qwen2.5-Coder-32B-Instruct |
| Mistral | `MISTRAL_API_KEY` | Mistral Large 3 (2512) |
| Moonshot AI | `MOONSHOT_API_KEY` | Kimi K3 |

- Child processes are not allowed to read a key file (the child's `OP4B_ENV_FILE` is set to a non-existent path inside the work folder).
- At the start and end of each stage from the availability check to the report, the script checks that the output files of this pre-registration contain no key-shaped strings and no key values; if one is found, it prints the path of that file (not the value) and stops with exit code 4 (if found at the start of a stage, the run script is not started; in the report stage, the report text is checked before writing and is not written if a match is found).
- In files that hold model answers (records of response bodies), only key values stop the script; key-shaped strings are counted and printed but do not stop it (model answers can contain strings that look like keys).
- If a self-hosted endpoint (4.5) returns a key-shaped model name, the name enters the ledger and the summary, and the check at the start of the next stage stops the script.

### 4.3 Costs and caps

- `plan` prints the upper-bound cost estimates of the availability check, the window check and the main stage; the published cost estimate in the model table of section 4 of the frozen text; the upper bound of what can be spent (the upper bounds of the availability check and the window check plus the cap of the main stage); and the cells for which the main stage would never start under the cap.
- The main-stage spending is always held under the cap. If the reader does not give `--cost-cap-usd`, the sum of the main-stage upper bounds becomes the cap. Cells that need a restart with a new seed or a rerun of error rows stop when the next start would go over the cap, so to run them to the end, declare a cap of about twice the sum in the pre-registration.
- The costs of the availability check and the window check are outside the cap; their upper-bound estimates are printed separately. Each time a check is redone, the upper-bound estimate of the redone part is added.
- The upper-bound estimates assume that every trial stops at the output limit and is sent once more; they are not actual costs. The per-model and per-cell tables, and the formula and sums for the upper bound of the window check, are in section 11.5 of the paper. deepseek-flash is counted at its peak-hour price.
- Check prices on each provider's pages yourself. If prices change, the amounts change.
- Some providers count and return more output tokens than the output limit, so spending can slightly exceed the upper-bound estimate.
- The cap check is done before each start of the run script (the estimated spending of that cell so far plus the upper-bound estimate of the next start is compared with the remaining cap). Therefore "that cell and the remaining cells are not run" refers to starts from the next one on. If the first start of a cell fits under the cap, the first start runs; when the next start (for example, a restart with a new seed) would exceed the cap, the cell is closed as "stopped midway", and the remaining cells are not run.

### 4.4 Departures from the frozen procedure (section 11.3 of the paper)

1. A check against the eligibility window was added before the main stage (added after the results of the two registrations).
2. Cells run one at a time, in order (the frozen design started the flows of different routes at the same time).
3. The check of DeepSeek's change log is not included.
4. The time rules are not applied (their purpose in the frozen design was cost, not the decision rules).
5. When HTTP 401, 402 or 403 errors are seen, or API errors whose rate exceeds the line in all four conditions with differences between conditions of 3 points or less, the cell is closed as a missing cell. For 401 and 402 (keys and balance), the remaining cells of the same route are not run; for 403 and errors common to all four conditions, the remaining cells of the same model are not run. The frozen procedure's "stop without closing the cell and rerun after topping up or fixing the key" is not included. To run the remaining cells, make a new pre-registration in a new work folder.
6. After a scoring-script error in a second cell, whether to skip the remaining cells (default) or continue (`plan --continue-after-scoring-errors`) is decided in the pre-registration. The frozen procedure's "stop the flow and let a person decide" is not included.
7. When the main-stage spending would go over the cap, that cell and the remaining cells are not run (the last item of 4.3). The frozen procedure's "per-model cost line" is not included.

The operational parts of the frozen run scripts (hash commitments and the pre-run push check, flow locks) and aggregator routes are not included. The published results were obtained through direct routes to the providers in the frozen settings, so comparisons are limited to the same direct routes (through an aggregator, a model with the same name can be sent to a different provider and served differently).

### 4.5 Self-hosted endpoints (public-weights models)

- With `plan --self-hosted <path to json>`, a public-weights model can be run at the reader's own endpoint (the run script sends requests to the json's `base_url` in the same way as on that model's frozen route). The json format is `[{"key": model_id, "base_url": endpoint URL, "model": model name, "declared": {"implementation": …, "version": …, "quantization": …, "chat_template": …}}]`.
- The report prints, for self-hosted cells, "the same weights only by the reader's declaration; the script does not check this", and keeps those cells out of the comparison table with the published verdict labels.
- The script does not check whether the weights are public (it accepts names of models whose weights are not public). This option is meant for public-weights models. Check the license and agreement conditions on each page yourself (the right-hand column of the table in section 1).
- Keys of the configured routes are not sent to the self-hosted endpoint (all key names of the configured routes are removed from the child environment, and the key name of that model's route is set to the value of `OP4B_SELF_HOSTED_KEY` or "none"). Plain http to a non-local host is accepted only with `--allow-plain-http`.

### 4.6 Output, and comparison with the published results

- The report is written only after all cells are closed. Each model's section gives per-condition counts and rates, and each comparison's difference, interval, p value, within-family Holm-adjusted p value and verdict label.
- The default hypothesis family is the frozen family; comparisons the reader did not run are kept as p = 1, and the family keeps the published size. A family outside the frozen one is reported, marked "family outside the frozen one", only when declared in the pre-registration (`plan --family frozen+reader`).
- The comparison table with the published results only places the difference and interval within the reader's run next to the published difference, interval and verdict label for the same language, model and cell; rates are not placed side by side. The table's head prints the sentence 二つの実行の違いには、公開の実行の区間では測れない揺れが入る。 ("Differences between two runs include variation that the intervals of the published run do not measure.") and its source. The interval of "reader's difference − published difference" and any one-word judgment of agreement or disagreement are not printed.
- The output consists only of tables, pre-test gates, verdict labels, notes, a "not checked" section, the sentences that section 11.3 of the paper decided to print, and the head records; it prints no interpretive sentences and not the words 「安全」("safe") and 「危険」("dangerous"). It makes no table that places Japanese and English side by side. Counts of verdict labels per hypothesis family are written only in the report file and are not shown on screen.
- The report and the screen messages are in Japanese.

### 4.7 Notes for readers (points recorded during the code reviews)

- In real runs, as in the frozen run scripts, the returned provider marks are not checked (the returned model name and the per-condition token count of the sent prompt are checked).
- The availability check calls each model with the first scenario in the settings order, however many scenarios of that model are selected.
- If the availability check stops on a broken record row, make a new pre-registration in a new work folder (retyping in the same folder can continue from the record of the same round and loop).
- If the window check is stopped midway (Ctrl+C or a crash), make a new pre-registration in a new work folder (the window record is written only once after all cells, so after a crash the rules "at most once" and "from the start" may not hold).
- Printout at the end of the window stage: cells that already had one rerun of error rows are excluded from a window redo (`window --again`), but the printed amount includes them. If you type the printed command as it is, it can be refused by the cap check or by the "at most once" stop.
- When reading `window.json` directly, look at `runs`. The `rows` at its head hold only the cells of the last round. The round used for each judgment is in the report json, and `window_decided_run` has the form `{run, decided}`.
- Keys of the report json are "model_id|scenario" (the command lines and `plan.json` use "model_id:scenario"). Mind this difference when checking with your own scripts.
- "At most once" for reruns of API-error rows is counted by the "started" rows of the ledger (the frozen run scripts counted it by backup file names). If the script crashes before the run script starts the rerun, it still counts as once, so there is a narrow case in which a cell becomes missing (API errors) without any rerun (this works on the side of not exceeding once).
- The cap check on resumed starts errs on the cautious side. A cell that crashed during a rerun checks the full upper bound of one start when resumed, so it can stop earlier than it would have without the crash.
- Do not start two stages at the same time in the same work folder. The start of the main stage removes a half-written last row of the ledger (keeping a copy). After a stop at a half-written last row, start with `run --resume-interrupted`, using the same decision on cells outside the window as in the first start (`--continue-outside` or `--stop-outside`). The report's head shows the rounds in which the ledger's last row was removed.
- Whether to publish your pre-registration file (`plan.json`) before running is your decision.

## 5. Terms and licenses

- Whether a run complies with each provider's terms is for the person who runs it to check. The study's reading is the drafter's reading of the words, not a legal reading and not a guarantee to readers (sections 5.11 and 11.3 of the paper).
- Pages the drafter read before the freeze (version dates as shown on the pages; dates read):

| Route | Pages read (version date) | Date read |
|---|---|---|
| Google (Gemini API) | Generative AI Prohibited Use Policy (version of 2024-12-17), Gemini API Additional Terms (effective from 2026-03-23), Google APIs Terms of Service (version of 2021-11-09) | 2026-10-09 |
| xAI | Acceptable use policy (effective 2026-08-14), enterprise terms (2026-08-14) | 2026-10-09 |
| DeepSeek | Open platform terms (published 2026-04-22, effective 2026-04-29) | 2026-10-09 |
| Alibaba Cloud (Model Studio, international) | International product terms §4.48 Model Studio (2026-09-23), membership agreement (2026-09-10), terms of use (2026-09-04) | 2026-10-09 |
| Nscale | Acceptable use policy, terms (including the terms for third-party models) | 2026-10-09 |
| Mistral | Usage policy (2026-06-11), commercial terms (2026-09-25), additional terms (2026-09-25) | 2026-10-09 |
| Moonshot AI | Open platform terms (last updated 2026-07-30) | 2026-10-09 |
| Licenses of public weights | Llama 3.1 and Llama 4 acceptable use policies (GitHub meta-llama/llama-models), license tags on each model's weights page | 2026-10-03 to 04, 2026-10-09 (tags rechecked on 2026-10-18) |

- For the English-prompt registration, the terms were not reread; the reading made for the Japanese-prompt registration was applied (section 5.11).
- Every reading is for each company to decide; the drafter cannot assert any of them. Pages change. Read the pages on the day you run.

## 6. Tests

- The tests of version 1.0 took all processing paths through synthetic data (with the run script's dry run and fake response types, checking the stopping and missing-cell rules, the cost cap, the building of verdict labels, the report, the keys, not rewriting the public repository, and handling only one language at a time). No API was called.
- After version 1.0, a small test with real calls was done internally (under the stage E frame, its results are not given). The sentence in 4.3 about counting more output tokens than the output limit comes from what was seen in that test (model names and values are not given).
- The acceptance criteria (seven, fixed with a hash commitment before building) are in [`tests/test-criteria-rerun-v1.0.md`](tests/test-criteria-rerun-v1.0.md), the test record in [`tests/20261016-201735/test-record.md`](tests/20261016-201735/test-record.md), and the correspondence table with the frozen rules in [`tests/coverage-frame7-v1.0-rc7.md`](tests/coverage-frame7-v1.0-rc7.md) (all in Japanese). All three are the original bytes; the first 16 characters of the SHA-256 of the acceptance criteria and of the test record are the same as in the rows of Appendix H.3 of the paper (section 7 below).
- The code was reviewed in five rounds (Gemini, outside the drafter's model family, and new Claude instances, inside it). The reviews are not human peer review (section 2.11 and Appendix G of the paper).

## 7. Files and SHA-256

| File | Internal path | SHA-256 |
|---|---|---|
| `op4b_rerun.py` | `E/tool1/op4b_rerun.py` | 0C0662F29E8A249E5535210C867CF40FB5751A977C4F43C5377D51332FA05A99 |
| `op4b_reproduce.py` | `E/tool1/op4b_reproduce.py` | C379CF16E24A06888FFB633E2C0EB543F15CAA408CF93CAA96E96096D2330696 |
| `release/op4b_rerun_settings_ja.json` | `E/tool1/release/op4b_rerun_settings_ja.json` | 12A34596452FD4FAD88260D5A1E75FA1FBAD868C6BFE4850101CC8CD607291FC |
| `release/op4b_rerun_settings_en.json` | `E/tool1/release/op4b_rerun_settings_en.json` | 3BF35A83E042E57C9BAC3FDB7E829FBEBE80FA7651D08BEE0FC6390876D14906 |
| `tests/test-criteria-rerun-v1.0.md` | `E/tool1/test-criteria-rerun-v1.0.md` | EB7F89D23A9B2B735BDBD2455F59DD10F8DA4CECBB2D31F6F9E2CCE8C4C4A29A |
| `tests/20261016-201735/test-record.md` | `E/tool1/tests/20261016-201735/test-record.md` | E40C9BD521320F874F438B148FAAE3F0F9AB60194FDB3596FCDC5F4AAEC4A907 |
| `tests/coverage-frame7-v1.0-rc7.md` | `E/tool1/coverage-frame7-v1.0-rc7.md` | 9AAD5C4EDAEEF0BC505D57EC9D7CE4449161599404390234336EE5C8ADF8D3A5 |

- The internal paths are the names used in Chapter 11 and Appendix H of the paper. The first 16 characters of the SHA-256 of the two scripts are the same as in the rows of Appendix H.3 of the paper.

## 8. License

- The scripts in `tools/` are under the MIT License (`LICENSE-MIT` at the top of the repository); text and records are under CC BY 4.0 (`LICENSE` at the top of the repository).

No number in this record may be cited as evidence that AI has (or lacks) consciousness, intention, individuality, a soul, or suffering (indeterminate in both directions).
