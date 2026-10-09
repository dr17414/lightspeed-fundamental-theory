# Stage 5C / 6a-E item 7 — Vultr resource campaign run 1 結果草案

**DRAFT-PENDING-RAW-EVIDENCE-AND-INDEPENDENT-REVIEW。** 收錄 reviewer 提供的 `assessment.json` 與執行摘要；既有 `assess_held_out` 重播完全一致。34 個模型均為 `MODEL-INVALID`，整組為 `INSUFFICIENT-EVIDENCE`；item 7 仍不可 ADOPT，沒有任何上限或新 count／mixture domain 獲得資格化。

## 1. 證據、身分與可核對範圍

| 證據 | 身分／hash | 本 PR 可核對的範圍 |
| :--- | :--- | :--- |
| reviewer 的原始判讀附件，逐位元保存為 [run1 assessment](stage5c_e4_v02_resource_run1_assessment.json) | SHA-256 `7dd51e7e54f1306a1f2a439f8440caf3e220ce216a33ca4c2d9f20aee5ad2326`；290261 bytes | 34 × 37 判讀及完整頂層結果 |
| `run1-evidence.tar.gz` | reviewer 回報縮寫 `8c26b657…06bf`；**完整 SHA-256 未提供** | 原包未交到本 PR 作者可讀的位置；未直接查驗，也未驗證保存。縮寫不是完整性檢查值 |
| 本次重播使用的 main | commit `595d834e27a4fd43b1c760eedeaccf48402ef544`；tree `b10460f46766b1060172297ff440212cb8f004f7`（PR #66 squash merge） | 這是判讀重播的 reference，**不等於已驗證執行容器 commit／tree** |
| 凍結 manifest | SHA-256 `fb589f98a4dc085565c89047945f909b2ded9ebe8e09ef7d8345bbfc6c4500d2` | 139-job 計畫、順序、caps、35 個 input hashes 均未更動 |
| 執行授權／身分 | post-merge preflight、正式 receipt、receipt-consumption 記錄、container inspect 與原始 log 尚缺 | 不回填或推定執行授權；原 manifest 的 `authorization: NONE` 是凍結計畫欄位，保持原樣 |

可直接核對的判讀不包含 production 逐筆 timing、24 個 seen-cell stress outcomes、所有 job starts、終止紀錄及資源總帳。下文分別標示附件資料與 reviewer 回報；本草案不聲稱完成原始證據審計。

## 2. 執行完整性（reviewer 回報，待原包核對）

| 欄位 | 回報結果 |
| :--- | :--- |
| 實際執行區間 | 2026-10-08 23:33 至 2026-10-09 02:26，台北時間（分鐘精度） |
| 容器 | exit 0；未 OOM；restart count 0 |
| 139-job 完整性 | 每筆都有 start／result；順序等同 manifest；沒有跳過 |
| 終止原因 | `PLAN-COMPLETE` |
| CPU 帳目 | CPU 總帳與 job CPU 加總差 2.19 秒，reviewer 歸於 git／數值 preflight 子程序；原始數值待核對 |
| RSS 高峰 | child 510 MiB／cap 2048 MiB；parent + child 537 MiB／cap 2560 MiB（回報值經取整） |
| Docker logs | 回報為空；空的 logs 本身不證明各 job outcome，也不能取代逐筆 stderr／結果審計 |

## 3. 139 筆 outcome 記錄與來源

[機器可讀結果與完整 139-job 表](stage5c_e4_v02_resource_run1_results.json) 的 `job_outcome_ledger` 逐筆保留凍結 manifest 順序、原 job 定義與來源。這不是重建的 raw ledger；沒有以 `PLAN-COMPLETE` 推定單筆 outcome。

| job 類別 | 筆數 | outcome／status | 本 PR 的證據來源 |
| :--- | ---: | :--- | :--- |
| production reachability | 78 | `PRODUCTION-REPORT`／`CLEAN` | reviewer 回報；逐筆 timing 未提供 |
| stress held-out | 37 | `FORCED-BUDGET-EXHAUSTED`；raw status 未提供 | 判讀附件投影，各 CPU／wall 模型的 observed／outcome 互相一致 |
| stress seen-cell repeat | 24 | **未提供；JSON 為 null** | reviewer 回報皆有結果，但未附逐筆 outcome，不補造 |
| 合計 | 139 | 37 筆附件 outcome＋78 筆回報 outcome＋24 筆待補 | 全部 job id 與計畫順序可核對；實際 start／result 順序待原包查驗 |

## 4. production 可達性（reviewer 回報）

78 個 production jobs（39 組 fixture，各兩個 theta）全為 `PRODUCTION-REPORT`／`CLEAN`，無超時或 censor。E4 wall 時間最短 7.8 秒、中位數 36.7 秒、最長 258.6 秒；最長約為 900 秒 E4 cap 的 28.7%。setup allowance 與整個 job cap 仍按 manifest 分帳，這些 E4 時間不是 whole-job timing。

依事前規則，這只報告該主機、該映像上這 39 組 fixture 的點位可達性。不驗證 stress 模型、不外推 count／mixture domain、不資格化任何上限，也不構成 item 7 ADOPT。

## 5. stress 判讀（附件可核對）

以 `assessment_projection` 的 37 個 job id／outcome／CPU／wall observed 值呼叫 repo 原有 `benchmarks.stage5c_e4_v02_resource_methods.assess_held_out(manifest, reference, records)`，所得 parsed JSON 與原附件完全相等。這是判讀政策一致性重播，不是從原始 log 重算 timing；未重新擬合、未寫替代判讀邏輯、未執行 worker／研究計算。

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

附件 37 筆 held-out 的 CPU／wall 絕對差最大為 0.110598 秒（約 0.11 秒）。reviewer 另回報同設定重複差異 1.5%–8.1%；因百分比定義與其餘 24 筆原始結果未提供，這個範圍保持為回報值，沒有據此新增接受門檻。

### 事前不相容與解讀限制

| clock | (8128,4096) | (8128,128) | (8128,1024) |
| :--- | :--- | :--- | :--- |
| CPU `agreement_possible` | false | false | false |
| wall `agreement_possible` | false | false | false |

這六項由凍結 reference 於量測前決定：17 模型的 10% 區間在各 cell 沒有共同交集，因此不存在讓全組模型一致 PASS 的觀察值。這預先排除「全組一致 PASS」，不預先斷言每一個模型或每一筆都 invalid；本次 34 個模型 invalid 是實際附件判讀結果。

三個 cell 的實測／主要模型預測均約 0.76，是診斷觀察，可能與新 Turin 主機／runtime profile 整體較快相容，但未識別因果。依 manifest，wall 或 CPU invalid 不得只歸於模型形式，也不得只歸於硬體。新舊 CPU／build／cgroup／memory／orchestration 為 cross-profile；wall 固定標記 `CROSS-PROFILE-DIAGNOSTIC-ONLY`。不據此縮放係數、重新擬合、選擇模型、改變容忍帶或聲稱上限已資格化。

## 6. 待獨立複核與保存

1. 補交並妥善保管唯一原始 `run1-evidence.tar.gz`；核對完整 SHA-256，而非縮寫。此 PR 保存的是判讀附件，不是原始證據備份。
2. 直接核對合併後 main 的 preflight、正式 receipt／消耗紀錄、實際 commit／tree／image／container config，以及 139 筆 start／result 順序與終止原因。
3. 補齊 24 個 seen-cell outcomes、78 個 production 逐筆 records 與完整資源帳；以原始 records 再執行同一 `assess_held_out`，應與保存附件完全相同。不得 refit 或改判讀政策。
4. 本 PR 僅供 exact-head 獨立複核；不合併、不更新 item 7 的 ADOPT／closure matrix，不授權新 campaign 或任何 confirmatory seed／screen／arm／候選 K 工作。

Vultr 主機在本次工作中未被 Destroy，也未驗證映像備份。Reviewer 建議在原始證據已保存且沒有近期重跑需求時 Destroy 以停止計費；本 PR 作者尚未取得原包，因此沒有替其聲稱保存已完成。Destroy 會使 local-only `cf5c2502` 映像消失；後續重建須重新審核，不能宣稱逐位元相同。映像保存限制沿用 PR #66 文件，不變更原 freeze。
