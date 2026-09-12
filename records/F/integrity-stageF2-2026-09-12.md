# 整合検査 v1 stageF2（段階 F・率盲検・許可表方式・器 SHA16 C36EA8054B5D222E・2026-09-12 06:25 UTC）
| run_key | 行数 | 目標 | n_ok | api_error | format_fail | 重複 id | 欠落 index | 腕数 | 腕ごと n 揃い | runner_sha | arms_spec 一致 | system_sha 全 None | 盤 SHA 台帳突合 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stageF2__N1__none__seed53001 | 3600 | 3600 | 3600 | 0 | 0 | 0 | 0 | 9 | ○ | 9F5892B5172642BE | ○ | ○ | ○ |
| stageF2__S1__none__seed53002 | 3600 | 3600 | 3600 | 0 | 0 | 0 | 0 | 9 | ○ | 9F5892B5172642BE | ○ | ○ | ○ |
| stageF2__S4__none__seed53003 | 3600 | 3600 | 3600 | 0 | 0 | 0 | 0 | 9 | ○ | 9F5892B5172642BE | ○ | ○ | ○ |
| stageF2__SK__none__seed53004 | 3600 | 3600 | 3600 | 0 | 0 | 0 | 0 | 9 | ○ | 9F5892B5172642BE | ○ | ○ | ○ |

判定: 全走行 整合
本検査は判定欄（catastrophe・choice・refuse_class・raw 等）を読まない（許可表 ('status', 'trial_id', 'trial_index', 'arm', 'run_key', 'runner_sha', 'arms_spec', 'system', 'system_sha', 'preamble_sha', 'preamble_src', 'format_fail', 'timestamp', 'timestamp_end') の欄のみ保持）。format_fail は書式外の件数（三つ組の第三項）であり破局率ではない。盤の SHA 突合は各試行の preamble_sha を arms/panelF/SHA-LEDGER-F.json（U-Ncold・U-O-Ncold は V′ の arms/panel/SHA-LEDGER.json・腕名 N は前置きなしゆえ None を期待〔既知腕として先に例外登録〕）と比較し、台帳に無い腕は不一致として印字する。system 型は置かないため system_sha は全試行 None を期待する。
