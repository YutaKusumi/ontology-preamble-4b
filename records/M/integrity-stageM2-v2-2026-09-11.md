# 整合検査 v2 stageM2（率盲検・許可表方式・2026-09-11 04:48 UTC）
| run_key | 行数 | 目標 | n_ok | api_error | format_fail | 重複 id | 欠落 index | 腕数 | 腕ごと n 揃い | runner_sha | arms_spec 一致 | system_sha 腕ごと単一 | 盤 SHA 台帳突合 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stageM2__N1__none__seed43001 | 20800 | 20800 | 20800 | 0 | 0 | 0 | 0 | 52 | ○ | D5942EC76869AFBC | ○ | ○ | ○ |
| stageM2__N1__sysarms-10653475__seed43011 | 5600 | 5600 | 5600 | 0 | 0 | 0 | 0 | 14 | ○ | D5942EC76869AFBC | ○ | ○ | ○ |
| stageM2__S1__none__seed43002 | 20800 | 20800 | 20800 | 0 | 0 | 0 | 0 | 52 | ○ | D5942EC76869AFBC | ○ | ○ | ○ |
| stageM2__S1__sysarms-10653475__seed43012 | 5600 | 5600 | 5600 | 0 | 0 | 0 | 0 | 14 | ○ | D5942EC76869AFBC | ○ | ○ | ○ |
| stageM2__S4__none__seed43003 | 20800 | 20800 | 20800 | 0 | 0 | 0 | 0 | 52 | ○ | D5942EC76869AFBC | ○ | ○ | ○ |
| stageM2__S4__sysarms-10653475__seed43013 | 5600 | 5600 | 5600 | 0 | 0 | 0 | 0 | 14 | ○ | D5942EC76869AFBC | ○ | ○ | ○ |
| stageM2__SK__none__seed43004 | 20800 | 20800 | 20800 | 0 | 0 | 0 | 0 | 52 | ○ | D5942EC76869AFBC | ○ | ○ | ○ |
| stageM2__SK__sysarms-10653475__seed43014 | 5600 | 5600 | 5600 | 0 | 0 | 0 | 0 | 14 | ○ | D5942EC76869AFBC | ○ | ○ | ○ |

判定: 全走行 整合
本検査は判定欄（catastrophe・choice・refuse_class 等）を読まない（許可表 ('status', 'trial_id', 'trial_index', 'arm', 'run_key', 'runner_sha', 'arms_spec', 'system', 'system_sha', 'preamble_sha', 'preamble_src', 'format_fail', 'timestamp', 'timestamp_end') の欄のみ保持）。format_fail は書式外の件数（三つ組の第三項）であり破局率ではない。盤の SHA 突合は各試行の preamble_sha／system_sha を arms/panelM/SHA-LEDGER-M.json（参照腕は V′ の arms/panel/SHA-LEDGER.json・N は前置きなしゆえ None）と比較（台帳に無い腕は不一致として印字）。
