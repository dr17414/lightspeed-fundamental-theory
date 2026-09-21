# Stage 5C item 8 — audit-only E4 screen 授權審查清單

狀態：**runner 平台防護 REVIEW-PENDING／不構成執行授權／不得執行**。
audit-only 協定已由 PR #41 merge `a5cf4dd6` 成為
`FROZEN-PROTOCOL`。本 PR 只在 preflight 明確拒絕非 Linux 平台，
避免 macOS 的 `ru_maxrss` bytes 被再次乘以 1024、直到 seed burn 後才
誤判超過 RSS cap；並同步更新
`docs/stage5c_e5_screen_authorization.candidate.json` 的 runner blob pin。
runner 實際讀取的
`docs/stage5c_e5_screen_authorization.json` 在完整 PR tree 中必須不存在。
候選檔可在審查期間修改，也可用 squash、merge commit 或 rebase 方式
安全合併；任何合併方式都不能解除 runner 的 fail-closed preflight。
候選路徑本身可有多次審查提交；one-shot 歷史計數只承重真實路徑，
故 candidate PR 的所有可達提交都不得新增、修改或刪除真實路徑。

九類內容定稿且下列阻塞全部解除後，須另開一個 trigger PR，從已合併
候選檔**逐位元複製**建立真實授權路徑。該 trigger branch 只能有一個
新增真實路徑的 commit，並以回歸確認兩檔 bytes 相同。如此不論採
squash、merge commit 或 rebase，真實路徑在 `main` 的歷史計數均為 1；
trigger 合併後不得修改 JSON 補救，否則 preflight 永久拒絕同一診斷
seed namespace。

建立真實授權檔的同一個 trigger commit，必須同時把 review 階段的
`test_review_tree_cannot_authorize_execution` 不存在性斷言，替換為
真實檔與已合併候選檔**逐位元相同**的斷言；不得先讓必然失敗的 CI
進入 trigger branch，再以第二個補救 commit 修改測試。

PR #41 的 exact head 已通過 CI、獨立複核並合併；audit-only 協定
因此已成為 `FROZEN-PROTOCOL`，第三個 trigger 阻塞解除。trigger
之前協定檔不得再改動任何位元組，包括看似純美化的狀態字樣；否則
候選 pin 與 authorization regression 必須 fail closed。不得把
候選檔內的 `AUTHORIZED` 當成覆蓋協定文字或真實路徑缺席的授權。
凍結協定時保留既有檔名
`docs/STAGE5C_6A_E_FROZEN_E4_SCREEN_PROTOCOL_DRAFT.md`，只修改檔內
狀態與承重文字。若改名，runner 的 `PROTOCOL` 常數與 executable blob
也必須改動，屆時不再是純文件凍結，須另行重審 runner；不得在協定
凍結 PR 順手完成。

## 九類審查項目

| 類別 | 待核對的確切內容 | 草案證據／阻塞 |
| --- | --- | --- |
| 1 runner | `analysis/stage5c_e5_screen.py` blob | 本 PR 候選為 `3873ee3eec93908dffa0faee22fdae83939c7b3c`；只新增 `sys.platform == "linux"` 的 pre-burn fail-closed guard，須對 exact head 獨立複核。 |
| 2 協定 | `docs/STAGE5C_6A_E_FROZEN_E4_SCREEN_PROTOCOL_DRAFT.md` blob | 已凍結為 `59c23e2ce45a45bb02f12bdc88e9d78b5bd85a95`；候選 JSON 維持 pin 此 blob。檔名保留 `_DRAFT`，且凍結仍不授權執行。 |
| 3 七個來源 | 逐檔 `HEAD:<path>`，且須等於 runner `FROZEN_BLOBS` | 下表七個 SHA；不可只核對 JSON 內部彼此一致。 |
| 4 6a-S burn registry | `docs/stage5c_6a_s_burn_registry.json` blob、全部已 burn／reserved source-of-record 與完整 24-seed 區間互斥 | blob `74a0299fd251e598beb34293c2f9b0880c2b3368`；若新的保留區間出現，須重新審。 |
| 5 runtime | Python **完整** `sys.version` 字串；NumPy `2.3.5`、SciPy `1.17.0`；OS 的 `RLIMIT_AS`、`SIGALRM`、`ru_maxrss` 單位 | 借用已封存 6a-S 的 Python `3.12.13 (main, Aug  7 2026, 02:25:39) [Clang 22.1.3 ]` 作候選，**尚未證實擬用主機存在這個 build**；當前工作環境為 3.12.14，不能執行。 |
| 6 seed | `[6000000000,6000000023]`；公式 `6000000000 + 8i + 4t + r`，$i\in\{0,1,2\}$、$t\in\{0,1\}$、$r\in\{0,1,2,3\}$ | 須窮舉恰有 24 個相異整數，並稽核後續 6a-E manifest 將整段排除。 |
| 7 resource | `cpu_seconds=57600`、`e4_wall_seconds=900`、`rss_bytes=34359738368` | 須在目標主機完成資源可執行性審查；必要的 16 core-hours、單 E4 15 分、32 GiB memory 不因 CI 綠燈而自動成立。 |
| 8 外部 custody | 兩個**絕對、已 resolve、互異、未存在**的路徑，父目錄在 repo 外、可持久保全、可 `fsync` | 草案 `/srv/lightspeed-fundamental-theory/audit/stage5c-e5-screen-v1/` **只是提議**；目前沒有該目標主機／持久磁碟的驗收證據。須確定容量、權限、留存及不可刪除／竄改的操作責任。 |
| 9 one-shot／狀態 | 候選審查合併後真實授權路徑歷史計數仍為 0；trigger PR 才以單一 commit 建立逐位元相同的真實檔。attestation 不存在、輸出未 claim；`state=AUTHORIZED`，item 8 仍 OPEN、6a-E 仍未預登記完成 | candidate PR 回歸要求真實路徑不存在；trigger PR 回歸要求兩檔 bytes 相同，且合併後 `git rev-list --count HEAD -- docs/stage5c_e5_screen_authorization.json` 應為 1。**trigger 合併本身仍不構成執行命令**。所有後續失敗與 `SCREEN-INCOMPLETE` 都不得重跑同一 seed。 |

第三類逐檔核對（均為 PR #38 合併 `09c61cd4` 的實際 blob，
並逐一與 runner 的 `FROZEN_BLOBS` 比對）：

| Source path | Exact Git blob SHA |
| --- | --- |
| `analysis/stage5c_hard_controls.py` | `32f593c0b710b4c591fb7746c7014d72784da554` |
| `analysis/stage5c_selector_family.py` | `9b9bb5497e0dc432eb63939b47bede0070bd8120` |
| `analysis/stage5c_measure_prereg.py` | `0b05b1fc913da77b4f1824fbf7901c52734efc19` |
| `analysis/stage5c_e4_wellposedness.py` | `a96d368f75b03b1fc0317cb20dd34dfd9de2f581` |
| `analysis/stage5c_continuum_pairing.py` | `8b32a3cf7a8ef23e5abae1e397f179c18ef3711e` |
| `analysis/stage5c_numerical_certification.py` | `deae60470abfddf2d636a4b3fd9160bbfebccc91` |
| `analysis/stage5c_primary_invariant.py` | `6756fd1dae86065fc209b99a4b8cedb57efdaaac` |

本 runner hardening PR 的協定、七個來源、6a-S registry、seed／resource／
output-path 欄位 **不得**修改；唯一候選 JSON 變更是 runner blob pin。
測試只可新增非 Linux 在 generator／burn 前拒絕且零輸出的回歸。
若 `main` 在 trigger 前改變任何被 pin 的 blob，須另行更新候選檔、合併
並重新取得 exact-head 複核；trigger PR 不得自行修訂任何欄位。
不可讓 preflight 到執行時才發現無法啟動。雖然測試可檢查
JSON 與 Git blob 的一致性，它不能代替對 runtime、外部磁碟與
全 source-of-record seed namespace 的獨立操作稽核。

候選檔合併不會讓 runner 具備執行能力。即使將來 trigger PR 合併，
也只讓既定 runner 在全部 preflight 通過後具備執行能力；未取得獨立
明確執行指令前，不啟動 runner。實際
執行後先保全 burn log 與 report，再獨立提交僅載 status／report
digest 的 attestation。此篩檢僅能早期發現阻塞，不能據
`SCREEN-NO-OBSTRUCTION` 宣稱已證得 $p$、cap、power 或 item-8 closure。
