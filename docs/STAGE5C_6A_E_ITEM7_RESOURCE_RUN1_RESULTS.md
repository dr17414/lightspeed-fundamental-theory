# Stage 5C / 6a-E item 7 — Vultr resource campaign run 1 結果草案

**DRAFT-RAW-EVIDENCE-AUDITED-PENDING-INDEPENDENT-REVIEW。** 已直接核對原始證據包及 reviewer 的 `assessment.json`；用既有 `assess_held_out` 對原始 280 筆 records 重播，與附件完全一致。139 個 jobs 無跳過，78 production 全部 CLEAN，61 stress 全為 FORCED-BUDGET-EXHAUSTED。34 個模型均為 `MODEL-INVALID`，整組為 `INSUFFICIENT-EVIDENCE`；item 7 仍不可 ADOPT，沒有任何上限或新 count／mixture domain 獲得資格化。

## 1. 證據、身分與可核對範圍

| 證據 | 身分／hash | 本 PR 可核對的範圍 |
| :--- | :--- | :--- |
| 原始 `run1-evidence.tar.gz` | SHA-256 `8c26b6574ce12956474779434f24ad54e940584dbf3ecc43c9c582fd792b06bf`；35361 bytes | 原包收到且保持原樣；283 個檔案／287 archive members；完整 member hashes 留在 evidence JSON |
| reviewer 的原始判讀附件，逐位元保存為 [run1 assessment](stage5c_e4_v02_resource_run1_assessment.json) | SHA-256 `7dd51e7e54f1306a1f2a439f8440caf3e220ce216a33ca4c2d9f20aee5ad2326`；290261 bytes | 34 × 37 判讀及完整頂層結果 |
| run commit／tree | `595d834e27a4fd43b1c760eedeaccf48402ef544`／`b10460f46766b1060172297ff440212cb8f004f7` | receipt 與 run-mode launcher proof 一致，是 PR #66 squash-merged main 身分；屬 archived trusted-host records 的核對，未重新登入主機 |
| 凍結 manifest | SHA-256 `fb589f98a4dc085565c89047945f909b2ded9ebe8e09ef7d8345bbfc6c4500d2` | receipt／proof／records header 一致；139-job 計畫、caps、35 input hashes 均未更動 |
| 映像 | `sha256:cf5c2502a59f57f2156be75c928c0c3b6db5b37e9a3f244e542662ccd5cc2f25` | receipt／prepared inspect／final inspect／manifest 一致 |
| host profile | SHA-256 `99c7bdf720973bf25fb2400b750145615d649c85c79b25fa2ebdb51e8c442132` | 與 manifest 的 canonical host JSON 一致；receipt／proof 的 boot ID 及 host output directory 相符 |
| 判讀與逐筆轉錄 | [run1 evidence](stage5c_e4_v02_resource_run1_evidence.json)、[run1 results](stage5c_e4_v02_resource_run1_results.json) | 原始 parsed job records、逐 line／member hashes、資源帳與完整 139-job 表 |

以 repo 既有 `verify_inspection` 核對 prepared proof（`stopped=True`）及終止後 inspect（`stopped=False`），run-mode command、Docker caps／隔離／唯讀掛載／output 掛載均通過，兩份 inspect 的 container ID 一致。`HostConfig.OomKillDisable` 在 prepared 記為 false、final 記為 null；其餘 HostConfig 相同，兩份都通過既有檢查，不宣稱兩份 inspect 逐位元相同。每個 job 的 threadpool、worker／supervisor affinity 與 frozen manifest 一致。

Receipt 為 single-use `DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY`，與 records header 保存的 receipt 完全相同；header 顯示 `method_verified: true`，故本次已通過 receipt gate 並消耗收據，不能沿用。原 manifest 的 `authorization: NONE` 是凍結計畫欄位，維持原樣，不回填為執行授權。

Receipt 引用獨立 merged-main pf3 包 SHA-256 `6187e7942e431bc096c9613a35540cf3e69b97d99b50bdb77c485f13eff1f33e`；**該 pf3 包未包含於本原包，故這輪不聲稱直接核對 standalone preflight 證據**。本次 run 的 stopped proof、final inspect、已驗證方法的 header 與完整 outcomes 則已直接核對。此核對依賴既有 trusted operator／Docker daemon 邊界，不是主機的密碼學 attestation。

## 2. 執行完整性（原包直接核對）

| 欄位 | 核對結果 |
| :--- | :--- |
| Docker StartedAt／FinishedAt | `2026-10-08T15:33:27.801477191Z`／`2026-10-08T18:25:58.795822656Z`；台北時間為 10/8 23:33:27.801 至 10/9 02:25:58.796，與分鐘精度摘要相符 |
| 容器 | exited／exit 0；OOMKilled false；restart count 0；State.Error 為空 |
| records | 280 行：1 header＋139 對交替 start／result＋1 terminal；沒有重複 id、缺筆或跳過；順序與 manifest 相同 |
| 終止原因 | 唯一 `TERMINAL-SUMMARY`，revision 1，`PLAN-COMPLETE`；production_schedule_cpu_bound false |
| plan wall | 10350.67999774 秒；cap 60000 秒；此 scope 與 Docker 起訖時間分開 |
| job whole-child CPU 加總 | 10312.558223 秒 |
| children CPU 帳 | 10314.749451000003 秒；比 jobs 多 2.191228000003 秒，按 frozen source 是 run 前已收集的 git／數值 preflight direct-child usage；原包沒有各 preflight 子程序分帳 |
| parent CPU／總 CPU 帳 | 8.395346158 秒／10323.144797158004 秒；總 cap 57600 秒 |
| RSS 高峰 | child 534966272 bytes（510.183 MiB），cap 2048 MiB；parent + child 各自 peak 的最大加總 562630656 bytes（536.566 MiB），cap 2560 MiB；**這是分別 high-water marks 的加總，不是同步 RSS 採樣** |
| Docker logs／worker stderr | Docker logs 0 bytes；139 stderr 各有 WORKER-READY／PHASE-STARTED／PHASE-FINISHED 三項 instrumentation，最後 outcome 均與 stdout／supervisor result 一致；空 logs 不取代 outcome 審計 |

## 3. 全部 139 筆 outcome

[機器可讀結果與完整 139-job 表](stage5c_e4_v02_resource_run1_results.json) 的 `job_outcome_ledger` 逐筆保留 frozen manifest 順序、原 job 定義、raw records 的 line 位置、phase／whole-child timing、RSS 與 outcome。[Evidence JSON](stage5c_e4_v02_resource_run1_evidence.json) 保存全部 278 個 start／result parsed objects；每個 worker stdout 欄位均與相應 supervisor result 相同。

| job 類別 | 筆數 | outcome／status | 證據來源 |
| :--- | ---: | :--- | :--- |
| production reachability | 78 | `PRODUCTION-REPORT`／`CLEAN`；adaptive_skipped false | 原包逐筆核對，無 censor |
| stress held-out | 37 | `FORCED-BUDGET-EXHAUSTED` | 原包逐筆核對；全部保留於判讀 |
| stress seen-cell repeat | 24 | `FORCED-BUDGET-EXHAUSTED` | 原包逐筆核對；只作診斷，不添入 held-out 判讀 |
| 合計 | 139 | 78 production＋61 stress | 全部有 start／result，均未超過自己的 whole-child CPU／wall cap |

## 4. production 可達性（原包直接核對）

78 production jobs（39 組 fixture，各兩個 theta）全為 `PRODUCTION-REPORT`／`CLEAN`，無超時或 censor。E4 wall 最短 7.769057209 秒、中位數 36.695758539 秒、最長 258.568497097 秒；最長為 900 秒 E4 cap 的 28.7298%。setup allowance 與整個 job cap 仍按 manifest 分帳，這些 E4 時間不是 whole-job timing。

依事前規則，這只報告該主機、該映像上這 39 組 fixture 的點位可達性。不驗證 stress 模型、不外推 count／mixture domain、不資格化任何上限，也不構成 item 7 ADOPT。

## 5. stress 判讀（原包與附件可核對）


以原包 `records.jsonl` 的全部 280 筆紀錄（包含 37 held-out results）呼叫 repo 原有 `benchmarks.stage5c_e4_v02_resource_methods.assess_held_out(manifest, reference, records)`，所得 parsed JSON 與原附件完全相等。這次使用原始 records 重播判讀，而非僅從 assessment 反向投影；另核對每個 worker stdout 與 supervisor result 欄位一致。Timing 仍是原 worker 記錄，不重新量測；未重新擬合、未寫替代判讀邏輯、未執行 worker／研究計算。

主要模型為 `stress_affine`；全部 16 個 power scenarios 均保留，CPU／wall 各 17 模型，每模型包含全部 37 held-out rows。

| 模型／clock | rows | 逐點 PASS | 逐點 INVALID | 模型總判決 |
| :--- | ---: | ---: | ---: | :--- |
| `cpu_seconds:stress_affine` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p0.9_q0.9` | 37 | 1 | 36 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p0.9_q1.0` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p0.9_q1.1` | 37 | 5 | 32 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p0.9_q1.25` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.0_q0.9` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.0_q1.0` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.0_q1.1` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.0_q1.25` | 37 | 4 | 33 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.1_q0.9` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.1_q1.0` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.1_q1.1` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.1_q1.25` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.25_q0.9` | 37 | 1 | 36 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.25_q1.0` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.25_q1.1` | 37 | 0 | 37 | `MODEL-INVALID` |
| `cpu_seconds:stress_power_p1.25_q1.25` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_affine` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p0.9_q0.9` | 37 | 1 | 36 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p0.9_q1.0` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p0.9_q1.1` | 37 | 5 | 32 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p0.9_q1.25` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.0_q0.9` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.0_q1.0` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.0_q1.1` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.0_q1.25` | 37 | 4 | 33 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.1_q0.9` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.1_q1.0` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.1_q1.1` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.1_q1.25` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.25_q0.9` | 37 | 1 | 36 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.25_q1.0` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.25_q1.1` | 37 | 0 | 37 | `MODEL-INVALID` |
| `wall_seconds:stress_power_p1.25_q1.25` | 37 | 0 | 37 | `MODEL-INVALID` |

少數逐點 PASS 不代表模型總判決 PASS；每個模型只要有 invalid row 就維持 `MODEL-INVALID`。整組 `model_set_verdict = INSUFFICIENT-EVIDENCE`，`qualification = false`，`new_count_or_mixture_domain_validation = false`。

### 主要模型的預測與觀察

以下均是事前固定的 phase timing scope，單位為秒；cell 多次執行列中位數，完整逐筆數值留在附件與 JSON projection。

| clock | held-out cell | 次數 | 預測 | 實測中位數 | 實測／預測 | 實測範圍 |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| cpu | (8128, 4096) | 1 | 1527.8 | 1153.6 | 0.755 | 1153.6–1153.6 |
| cpu | (8128, 128) | 32 | 47.7 | 36.5 | 0.765 | 36.2–39.1 |
| cpu | (8128, 1024) | 4 | 382.0 | 292.5 | 0.766 | 290.7–299.0 |
| wall | (8128, 4096) | 1 | 1527.9 | 1153.7 | 0.755 | 1153.7–1153.7 |
| wall | (8128, 128) | 32 | 47.7 | 36.5 | 0.765 | 36.2–39.1 |
| wall | (8128, 1024) | 4 | 382.0 | 292.5 | 0.766 | 290.7–299.0 |

原包全部 139 筆的 phase CPU／wall 絕對差最大為 0.110598 秒（約 0.11 秒）。CPU 重複範圍以 `(max − min) / median × 100%` 作描述性診斷：s128 的 32 次為 8.084%，s256 的 16 次為 2.755%，s512 的 8 次為 1.471%，s1024 的 4 次為 2.839%，與 reviewer 的 1.5%–8.1% 摘要相符。這個百分比只描述 spread，不新增接受門檻或模型判讀規則。

### 事前不相容與解讀限制

| clock | (8128,4096) | (8128,128) | (8128,1024) |
| :--- | :--- | :--- | :--- |
| CPU `agreement_possible` | false | false | false |
| wall `agreement_possible` | false | false | false |

這六項由凍結 reference 於量測前決定：17 模型的 10% 區間在各 cell 沒有共同交集，因此不存在讓全組模型一致 PASS 的觀察值。這預先排除「全組一致 PASS」，不預先斷言每一個模型或每一筆都 invalid；本次 34 個模型 invalid 是實際附件判讀結果。

三個 cell 的實測／主要模型預測均約 0.76，是診斷觀察，可能與新 Turin 主機／runtime profile 整體較快相容，但未識別因果。依 manifest，wall 或 CPU invalid 不得只歸於模型形式，也不得只歸於硬體。新舊 CPU／build／cgroup／memory／orchestration 為 cross-profile；wall 固定標記 `CROSS-PROFILE-DIAGNOSTIC-ONLY`。不據此縮放係數、重新擬合、選擇模型、改變容忍帶或聲稱上限已資格化。

## 6. 待獨立複核與保存

原始 `run1-evidence.tar.gz` 已作為本對話附檔收到，未改寫其 bytes，完整 SHA-256 與原回報縮寫相符。本 PR 保存其 member／line hashes、parsed job records 與原 assessment，**不是替代原始 gzip 包的備份**；沒有聲稱驗證額外的離線備份。持有者應保留該唯一原包與完整 hash，日後從原包重播；不得重新擬合或更換判讀政策。Receipt、boot／container IDs 與主機路徑原文留在原包，公開轉錄只列核對結果及其 raw member hashes。

本 PR 已完成原包核對，仍是待 exact-head 獨立複核的 draft，不合併、不更新 item 7 的 ADOPT／closure matrix，不授權新 campaign 或任何 confirmatory seed／screen／arm／候選 K 工作。獨立 pf3 包若要作 standalone preflight 複核仍須另提供，不能以 receipt 中的引用代替原包。

本輪未操作 Vultr 管理介面，未 Destroy，也未驗證映像備份。Reviewer 的停止計費建議仍適用於證據持有者確認原包已妥善保存、沒有近期重跑需求之後。Destroy 會使 local-only `cf5c2502` 映像消失；後續重建須重新審核，不能宣稱逐位元相同。映像保存限制沿用 PR #66 文件，不變更原 freeze。
