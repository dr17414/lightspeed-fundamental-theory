# Stage 5C item 8 — frozen E4 hard-control 可行性篩檢草案

狀態：**【審查草案／未凍結／不得執行】**。這只規劃 item 8 的
candidate-independent、audit-only 篩檢；它不是 6a-E selection 或
confirmation arm，也不完成 §3.2.1 的 $p$／$\Pr(G)$ 估計預登記。
診斷 seed、輸入或 E4 評估均須等本協定及唯一執行器經
獨立複核、CI、合併，另有正式授權紀錄及 preflight 後才可啟動。
即使 runner 已合併，缺少事後獨立審查的授權檔仍須拒絕啟動。

## 1. 固定問題與輸入

篩檢只問：**現有** item-7 producer 對來自凍結
`sprinkle-control-p-theta-v0.1` 的少數獨立因果集與原有 11 個
order-only C8 selector，是否已顯示超過 E2 數值餘裕的常見個案？
它不估計小至 $10^{-6}$ 的 tail，也不推論完整 matched-null law。

- 依固定順序 $N=(64,96,128)$，$\theta=(-0.4,+0.4)$；每個
  $(N,\theta)$ **恰好 4 個**互異診斷 causets，共 24 個。每個
  causet 一次生成並依原始 C8 family 順序各評估 11 個 selector，
  故最多 264 次 selector／E4 嘗試；不得只跑成功 member、因已見
  結果提早換 $N$，或把同一 causet 在 11 個 member 間當成 11
  個獨立 draw。$N$ 此處只是**診斷設計**，不是 6a-E 的 $N$。
- 唯一 generator 為 `analysis.stage5c_hard_controls.sprinkle_control`
  （既有 `PCG64DXSM` + rejection sampling）；唯一 selector 為
  `analysis.stage5c_selector_family.apply_selector`。構造端只能收到
  `BlindedCase(case_id="AUDIT-ONLY", order=order)`，不得把 target
  或 seed 編入 construction-facing payload；evaluator 才能以
  選中 indices 取回
  `(u_i,v_i,u_k,v_k)`。以 `uniform_pair_weights(m)`、
  `normalised_weights(weights, normalization)` 保持
  $\varphi=1,\mathcal N=m$，交給**既有**
  `evaluate_e4_wellposedness(atoms, weights, theta)`；不得修改 E4
  cell levels、adaptive 容差或認證常數。
- 提議的專屬 audit seed 整數為
  $s(i,t,r)=6{,}000{,}000{,}000+8i+4t+r$，其中
  $i=0,1,2$ 對應上述 $N$ 順序，$t=0,1$ 對應上述 $\theta$
  順序，$r=0,1,2,3$。此 24 整數不屬於既有 6a-S
  `1.3B/1.4B/1.5B/3.1B` bases；啟動前仍必須對**全部**已
  burn／reserved source-of-record 做機械互斥稽核，並在 item 9
  的未來 6a-E fresh manifest 明文排除完整區間
  $[6{,}000{,}000{,}000,6{,}000{,}000{,}023]$。
  此處只寫公式，**沒有 claim、計算或生成任一 seed**。

執行器在獨立 PR 待審，執行前須以另一份獨立審查、合併的授權
紀錄 pin 自身、協定、七份 source blob、6a-S burn registry 與 Python／NumPy／SciPy
runtime；來源、weight construction、座標排列及失敗 precedence
須有不調用 generator 的 dry-run／sentinel regression。任何差異
必須先修訂協定，不能現場修補或悄悄改用 planted mixture。
授權紀錄須事前列明**兩個不可替換的 repo 外絕對路徑**
`output_paths.burn_log`／`output_paths.report`；執行器拒絕任何
CLI 指定的其他路徑，以及路徑已存在或 repo 內已有
`docs/stage5c_e5_screen_attestation.json` 的情況。
建立 burn log 時採獨占建立並同步檔案及父目錄；同一組
診斷 seeds 從第一筆嘗試起即不可透過換路徑重跑。
操作方須保全外部檔案；手動刪除／竄改該檔不屬於程式可證的
one-shot 範圍，故事後 attestation 與 custody audit 仍是義務。
依賴基線先鎖定於已合併的 PR #35 tree `fb10f67b1afe0e1b44b60abab280dfb79a2e760c`；
篩檢 runner 之後須在獨立 PR 固定自己的 blob，且在執行前比對
上述 frozen source tree 所含 generator／selector／measure／E4／
continuum pairing／certification／primary invariant 七個程式檔的 blobs。建議先沿用
CI 的 Python `3.12.13`、NumPy `2.3.5`、SciPy `1.17.0`，
執行前逐字記錄 `sys.version` 及套件版本；與已審 profile 不同即停止。

資源停止規則提議為**單 process、無自動 retry**：完整篩檢
上限 16 core-hours、單次 E4 牆鐘時間 900 秒、process RSS
32 GiB；執行環境須能實際量測並強制停止，否則不得開始。
超限只記 `SCREEN-INCOMPLETE`，不能降低 $N$、刪除耗時
member 或重用已 claim 的 seed 補齊；這些上限與 profile
都待 runner review，仍不是執行授權。

## 2. 預先指定的輸出與隔離

每個 $(j,N,\theta)$ 的四次嘗試僅落入以下**六個互斥欄位之一**，
六欄總數必須等於 4：`SELECTOR-OR-ATOM-INVALID`（selector
缺 pair、shape／cap 不合法）、`E4-OR-ITEM3-NONCLEAN`
（包括 E4 已回傳的 adaptive resource-cap／非有限 status）、
`CLEAN-LOW`、`CLEAN-MID`、`CLEAN-NEAR`、`CLEAN-OVER`。
只在 E4 與 item-3 certification 都 `CLEAN` 且兩個 raw
`endpoint_error` 有限時，以 exact rational 定義
$v=\max(e_1/3,e_2)$，依下列固定分帶評後四欄：

$$
\begin{aligned}
\texttt{CLEAN-LOW}&:\quad 0\le v<1/160,\\
\texttt{CLEAN-MID}&:\quad 1/160\le v<1/80,\\
\texttt{CLEAN-NEAR}&:\quad 1/80\le v<1/40,\\
\texttt{CLEAN-OVER}&:\quad v\ge1/40.
\end{aligned}
$$

將 raw binary64 誤差轉成 exact fraction 比較，不先在 binary64
計算 $e_1/3$；各分帶等號只屬右側分帶，$1/40$ 等號屬 `CLEAN-OVER`。
這只是兩臂同界時 $2a_k/D_{kk}<1/20$ 的**必要**餘裕篩檢，
各帶只供事前比較量級，**不是**可從中挑選的 $a$／$\eta$
或完整 region 的 PASS。單次 `CLEAN-OVER` 就足以顯示
「此批全部低於門檻」不成立，但不能證明 underlying $p$
大於任何預登記量。

對外只提交每 stratum 六個 counts、完整／中斷標籤、來源 commit／
runtime identity、呼叫次數及總 CPU／wall／峰值記憶體資源記錄；
不提交各因果集座標、order、selector pair 陣列、逐列 e、
matching features、E4 endpoint、arm 名稱或 seed 與任何正式 arm
的對應關係。診斷執行器不讀 6a-S／6a-E arm numerical fields、
不寫 arm ledger、不形成 arm endpoint、不呼叫候選 $K$，且不能
import `analysis.stage5c_e5_budget` 形成未授權 allocation。

若所有 66 strata 都有四筆而無任何 invalid／NONCLEAN／OVER，
唯一輸出 `SCREEN-NO-OBSTRUCTION`；只要任一有上述計數，
輸出 `SCREEN-OBSTRUCTION` 並列出該 stratum 的六個 counts。
任一呼叫在 E4 回傳 status 前中斷、或外部 CPU／記憶體上限
使完整性缺失時，只能輸出
`SCREEN-INCOMPLETE`，保留已生成的診斷 seed 為 burned，
**不得**以刪去失敗列、原 seed 重跑或延長抽樣補成 clean。
若執行器自身的 count／category 完整性檢查失敗，另記
`SCREEN-INTEGRITY-FAILURE`，與資源／中斷的 `SCREEN-INCOMPLETE`
區分；兩者都不公布部分 counts，亦不可重跑。
一旦 burn log 建立，即使在第一筆 generator 呼叫前中斷，
整段 24 個診斷 seeds 都保持 reserved，不准刪掉檔案重試。
每次實際嘗試後、任何後續 item-8 工作前，必須獨立 PR
將 `docs/stage5c_e5_screen_attestation.json` 合入 main，
只記終局 status 與外部 report 的 SHA-256 digest，不提交
逐列數值或外部 burn log；若中斷使 report 從未寫成，
status 記 `SCREEN-INCOMPLETE`、report digest 記 `null` 並保全
固定的 burn log。核對 custody 後方可使用摘要。
此四個字串均不是 E1／E2／E3 verdict、不是 $\Pr(C)$ 估計。

## 3. 篩檢到 $R$ 的唯一合法關係

`SCREEN-OBSTRUCTION` 是停止按**現有全 raw-pool 零超標界**
承諾大規模計算的觸發器；可以另行設計更精確的 averaged-error
界或 item-7 amendment，但**不能**從這四筆估計 $p$、放寬
candidate grid 或宣稱 frozen E4 普遍無望。`SCREEN-NO-OBSTRUCTION`
只准進入**另一份**獨立 review／merge 的完整估計協定設計，
不授權直接執行，也不能以篩檢數值選 $a$。
若 `SCREEN-NO-OBSTRUCTION` 主要來自 `CLEAN-NEAR`，
那只是低於零統計餘裕的必要門檻，**不能**據此認定
數值 cap 可行或完整估計協定值得投入；仍須另審平均誤差、
統計半寬與資源成本。

零超標的四筆仍給單一 stratum 99.9% one-sided exact binomial
上界 $1-0.001^{1/4}\approx0.822$，所以篩檢**無法**告訴我們
$p$ 是否為 $10^{-4}$ 或 $10^{-6}$。故未來 $R_p$ 不能從這
四筆的點估計「校準」：必須由**事前**固定的正式 $L,H,c,d,\delta$、
有序 $a$ grid、$\Pr(G)$ 的下界與資源停止條件算出，同時為
`NO-FEASIBLE-CAP` 保留終局；若資源不可負擔，選擇其他有明確
證明的 bound，不能依首輪結果追加 replications 或另取種子。
換言之，篩檢結果只決定是否開啟該規劃，**不決定 $R$ 的數值**。

本草案僅提議 resource cap；runner 與 burn attestation／preflight
尚待獨立複核，授權檔刻意不存在；**不得執行**。item 8 及 6a-E preregistration
狀態維持 `OPEN`／`PREREGISTRATION-INCOMPLETE`。
