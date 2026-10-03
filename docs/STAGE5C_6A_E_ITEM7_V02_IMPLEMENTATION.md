# Item 7 v0.2 implementation — draft, qualification pending

日期：2026-10-02。`authorization=NONE`。本文件不關閉 item 7、items 3–5、item 8，
亦不授權 6a-E execution。

## 1. Reviewed baseline 與實作範圍

PR #58 exact head `3036cda618827ebd07416fc63b72d070d9824754` 經獨立 GO 後
squash-merge 為 `c4e79adcec031038b2fed66915956992b5a3904e`。merge tree 是
`31e72d2792a46d4bd6a0c16b744baf23d16f188f`，與受審 tree 相同。
本 implementation 只實作已合併 proposal／candidate JSON 的 combined candidate。

`analysis/stage5c_e4_wellposedness_v02.py` 是獨立版本。歷史 v0.1 producer、
selector、adapter、item-3 certification、joint-law／region 公式，以及歷史
authorization／attestation／burn registry 均保留；只有既有 screen 的
`_one_member` consumer 改成先判斷 non-CLEAN，再讀 optional certification。
該函式的顯式 v0.2 keyword 只供 component validation，`run_screen` 仍走 v0.1，
既有 burned namespace 不可重跑。本 PR 沒有新增 runner、protocol、seed 或 authorization。

v0.2 的固定內容如下：

- enclosure levels `(64,128,256)`，metadata 記錄實際級數；保留 finite／ordered invariant；
- `rtol=2^-14`，effective `atol=min(2^-30,down_binary64(2^-14*max(U)))`；
  用 exact dyadic product 和必要的一次 `nextafter(...,0)`，沒有 fallback；
- structural leakage 優先；zero scale／正尺度乘積 underflow 回報具名
  `ADAPTIVE_TOLERANCE_UNDEFINED`；這兩條 skipped-adaptive 路徑的四個 optional
  欄位全部為 `None`；非有限／不符次序 enclosure 則沿用 `E4ProtocolError`，不建立 report；
- adaptive helper 顯式接受本列 `atol`；其後 reason 優先序是 NONFINITE、resource cap、
  numerical certification，最後才可 CERTIFIED；
- contract、enclosure、兩個 estimate identities 升為 candidate 固定的 v0.2；
  topology／leakage identities 與所有其他常數維持 v0.1；
- 每個 estimate 的 validated quadrature budget 都取新 enclosure 的 farthest-corner error，
  adaptive backend 自評誤差不替代 validated enclosure。

## 2. Component revalidation

`tests/test_stage5c_e4_v02.py` 使用 deterministic development fixtures：

1. 鎖定 candidate constants／identities、finite enclosure invariant、zero／underflow、
   downward-rounding 修正、reason 優先序及 nullable schema。
2. 三個既有單 atom witnesses 使用真實 v0.2 producer；非對稱 max-scale witness 在
   pinned SciPy 下為 83 subdivisions。僅作回歸的 min-scale counterfactual 達 4096 cap，
   不修改正式 policy 或 module global。
3. real selector→adapter→v0.2 E4→`_one_member` seam 使用
   `(10^-200,10^-200) ≺ (2*10^-200,2*10^-200)` 與 antichain 尾巴。
   在 N=64、96、128 與 `all_relations`／`links` 六格中，真實 selected pairs 都是
   `[[0,1]]`，leakage-invalid report 歸入 `E4-OR-ITEM3-NONCLEAN`，沒有 mock report、
   `run_screen` 或 seed。此 witness 位於 R_geo 的 10^-12 margin 之外。
4. 新 estimates 重新 bind item-3 source rows、certify／seal，再形成 typed endpoint pool；
   把 v0.2 estimates 塞進 v0.1 source row 會因 fingerprint 不符而拒絕。
5. 由真實 v0.1／v0.2 reports 分別重新建立 32 個 deterministic cohort fixtures、
   每 cohort 192 個 typed rows、joint-law／ensemble producer seals、region inputs 與
   matched numerical half-width。matching indices 是固定 typed fixture；重複 rows
   **不是獨立 scientific observations**，不宣稱完成任何 matched-law 或 power 實驗。
   舊 width 不能用在新 region input。E4 矩陣為 diagonal，第二 endpoint 精確為零，
   因而 region 正確保留 `DEGENERATE-MARGINAL-VARIANCE` fail-closed；未放寬此 gate。

既有 items 4–5 的 E1／E2／E3 strict equality、directed rounding、source seal、
df-only oracle 與 mutation regressions 一併重跑；公式與 boundary constants 不變。
以上是 component coverage，仍須 independent exact-head review 決定 revalidation closeout，
不能以歷史 v0.1 closure 自動關閉 v0.2。

## 3. 完整公開 payload diff

`benchmarks/stage5c_e4_v02_validation.py payload-diff` 同時執行兩個真實版本。
完整 report public numerical fields 以 binary64 hex 保存，包含 leakage、fixed/adaptive
matrix／budget／implementation IDs、levels、effective tolerance、agreement、norm interval、
endpoint／error／bounds、reason 與 status；不序列化 process-private seal token。
結果在 `docs/stage5c_e4_v02_development_evidence.json`，並附被執行 source 的 Git blob IDs。

| Development fixture | theta | v0.1 | v0.2 | v0.2 subdivisions |
|---|---:|---|---|---:|
| gate_a | 0.4 | INCONCLUSIVE／numerical certification | CLEAN | 49 |
| near_zero | 0.4 | CLEAN | CLEAN | 68 |
| wide_cell | 0.4 | CLEAN | CLEAN | 158 |
| asymmetric | 0.4 | CLEAN | CLEAN | 83 |
| leakage_invalid | 0.4 | INCONCLUSIVE／structural leakage | 同理由；adaptive skipped | — |
| interior | -0.4 | CLEAN | CLEAN | 478 |
| interior | 0.0 | CLEAN | CLEAN | 479 |
| interior | 0.4 | CLEAN | CLEAN | 480 |
| boundary_contact | 0.4 | CLEAN | CLEAN | 207 |

九列不是全輸入覆蓋、cap 成功機率、scientific arm data 或 uniform numerical cap。
256 是已探查 levels 中足以改善三個已知 witnesses 的級數，不是理論最小值。

## 4. 單次 resource probe 與未完成的 qualification

獨立程序執行 8,128 個 repeated gate_a atoms，使用真實 v0.2 density／cubature，
不折疊 atom 列。保留 900 s per-call wall、57600 s process CPU、32 GiB RLIMIT_AS。
測量以 `time.process_time()` 為 CPU 定義；`getrusage` 只作補充診斷。
此 8128-atom probe 使用只有 49 subdivisions 的低細分 fixture，不代表每 atom 的成本上界。

| 單次開發觀察 | 結果 |
|---|---:|
| CPU | 330.301451943 s |
| wall | 226.506293870 s |
| process peak RSS | 482721792 bytes（約 460.36 MiB） |
| getrusage CPU diagnostic | 330.299719 s |
| status／reason | CLEAN／CERTIFIED |
| subdivisions | 49 |

記錄環境是 Python 3.12.14、NumPy 2.3.5、SciPy 1.17.0；CI 另以 Python 3.12.13
及 pinned dependencies 驗證 regressions。該 probe 不在指定約 7 GB target host 上，
亦沒有記錄完整 host／thread configuration，不能充作可轉移的 qualification。
單次 RSS 與 RLIMIT_AS 是不同量；32 GiB address-space limit 不是實體記憶體保證。

**本 draft 尚未滿足 proposal §5 的完整 resource qualification，因此不可 closeout／授權。**
可先釘住所有十一 members 的保守 selected-pair count 上界：每個 selector 都只取
strict order 的 causal relations；每個 unordered point pair 至多有一個方向，故
selected count ≤N(N−1)/2。此論證逐 member 覆蓋 `all_relations`、`links`、四個
`interval_exact` 與五個 `endpoint_depth_mass_band`；上界可由 total chain 的
`all_relations` 達到，但不宣稱其他 members 都能達到。

| N | 逐 member 保守 count 上界 |
|---|---:|
| 64 | 2016 |
| 96 | 4560 |
| 128 | 8128 |

待完成的硬門包括：

- 較細的逐 member registered count profiles；上述保守 count 上界本身不提供 CPU 上界；
- exact v0.2 blobs 在各 profile 上的 wall／CPU／RSS，以及 nonfinite／4096 exhaustion 的 fail-closed；
- 事前 264-call schedule CPU 上界 ≤57600 s、每 call wall ≤900 s；
  完整 schedule 起點與 runtime cap 相同，涵蓋 burn／generation／selector／adapter 的成本；
- 指定 host 的 memory preflight，及未來新 runner／authorization 對 current blobs 的完整 pin。

本開發 script **不**執行上述完整 schedule。不得把單次數值線性外推成已證上界，
亦不得因此縮減 strata、levels、延長 caps 或重用既有 burned namespace。
若完整 qualification 不能在既有 caps 內證成，依 proposal 回到 amendment review。

## 5. Reproduction 與狀態

從 repository root：

```sh
python -m benchmarks.stage5c_e4_v02_validation payload-diff
python -m benchmarks.stage5c_e4_v02_validation resource --atoms 8128
python -m pytest -q tests/test_stage5c_e4_v02.py tests/test_stage5c_statistical_regions.py tests/test_stage5c_e5_screen.py tests/test_stage5c_e5_screen_authorization.py tests/test_stage5c_e5_item7_amendment_proposal.py
python verify_integrity.py
python -m pytest -q tests/
```

PR #59 歷史本地驗證：targeted suite **88 passed**（上列五個檔案；只跑前兩檔為 68 tests）；全庫 **418 passed, 5 warnings**；
integrity 與 `git diff --check` 通過。五個 warnings 與原基線相同。

item 7 保持 `AMENDMENT-REVIEW-PENDING`；items 3–5 保持歷史 `CLOSED-v0.1`／
v0.2 `REVALIDATION-PENDING`；item 8 `OPEN`，6a-E `PREREGISTRATION-INCOMPLETE`。
proposal JSON 仍 `executable=false`／`authorization=NONE`。沒有新增 arm ledger、
generator／seed namespace 或 candidate K。

PR #59 exact head `536925694a0f32f25caaf1567063543c140a73eb` 經獨立 GO 後，
squash-merge `d2c665ad78bbd2d3dd12360e934307d67ed979f7`，merge tree
`971a521fbc18128295878925babf46d38c279868` 與受審 tree 一致。此合併只納入
implementation draft，不構成 item-7 closeout。後續 qualification 前的資源特性分析
另見 `docs/STAGE5C_6A_E_ITEM7_RESOURCE_CHARACTERIZATION.md`。未來 consumer 必須
以 `enclosure_id`／`contract_id` 判版本；v0.2 enclosure 繼承 v0.1，不能用 `isinstance` 判版本。
