# Stage 5C 6a-E item-7 combined amendment proposal

**狀態：`AMENDMENT-REVIEW-PENDING / NON-EXECUTABLE`。**

本提案明文重開 closure item 7 的 amendment track，但不修改或取代已封存的
v0.1 producer。歷史 v0.1 closure、第一個 E5 screen authorization／attestation 與
burned seed namespace 均保持逐位元不動；本提案不生成 seed、不呼叫 generator、不讀
arm data、不形成 endpoint，也不授權 runner。機器可讀的唯一候選紀錄是
`stage5c_e4_item7_amendment_candidate_v0.2.json`，其 `executable` 固定為 `false`。

候選是在已見本文件 §4 的 candidate-independent development witnesses、PR #46
所封存但 `e4_completed_evaluations=0` 的無效 screen incident，以及 §5 的本地資源
探查之後提出；不是事前未知資料的原始 freeze。提出時沒有任何 6a-E arm ledger、有效
screen E4 row、matched endpoint、between-target contrast 或候選 $K$。這個已見資料狀態
必須隨未來 implementation／closeout reviews 一併保存，不得把 v0.2 倒寫成原始預登記。

## 1. 為何必須合併提出

既有 assessment 已隔離兩個不同但相互作用的 frozen bottlenecks：

1. fixed `E4_CUBATURE_ATOL = 2^-30` 對小 pairing scale 過大，使 adaptive backend
   零細分就收斂；同一機制同時影響 Gate A item-3 certification 與 Gate B near-zero
   relative error；
2. frozen `E4_ENCLOSURE_LEVELS = (16,32,64)` 對一般尺度 wide-cell witness 的
   validated enclosure 過寬；只改 `atol` 完全不改善此分支。

兩項不能拆成兩次 producer amendment。尺度感知 `atol` 直接使用 enclosure upper
endpoint，故 enclosure levels 改變會同時改變 adaptive tolerance；而任何一項改動都會
使 item-3 numerical rows、source-row fingerprints 與 items 4--5 numerical regions 需要
完整重驗。分兩次修改會讓相同下游 review 付費兩次，且第一次 review 的 effective
`atol` 會被第二次 enclosure 修改推翻。

## 2. v0.2 candidate surface

本 PR 只固定下一個 implementation PR 必須實作及審查的候選，不把它接入 production：

| 欄位 | v0.1 frozen | v0.2 candidate |
|---|---:|---:|
| enclosure levels | $(16,32,64)$ | $(64,128,256)$ |
| relative tolerance | $2^{-14}$ | 保持 $2^{-14}$ |
| absolute tolerance | 固定 $2^{-30}$ | $a_{\rm eff}$，上限仍為 $2^{-30}$ |
| max subdivisions | $4096$ | 保持 $4096$ |
| max atoms | $8128$ | 保持 $8128$ |
| density chunk | $128$ | 保持 $128$ |

先以新 levels 計算 validated enclosure，令

$$
s=\max(U_1,U_2),\qquad
a_{\rm eff}=\min\!\left(2^{-30},
\operatorname{down}_{\rm binary64}(2^{-14}s)\right),
$$

其中 $U_k$ 是 enclosure upper endpoints，
`down_binary64` 表示對 exact dyadic product 向零取不大於該值的 binary64。
若 $s$ 非有限、$s\le0$，或乘積向零取整後為零，producer 必須在 adaptive call 前
fail closed 為 `INCONCLUSIVE / ADAPTIVE_TOLERANCE_UNDEFINED`；不得把零 scale 改寫成
固定 fallback tolerance，也不得把 underflow 當作精確零誤差。這個具名 reason 是
v0.2 contract 的一部分，implementation 不得從既有 enum 任選一個近似理由代替。

`down_binary64` 必須先以 exact dyadic arithmetic 形成 $2^{-14}s$，再轉為 binary64；若
轉換結果高於 exact value，須以一次 `nextafter(..., 0)` 向零修正。不得只呼叫會採
round-to-nearest 的 `ldexp` 就宣稱已向零取整。除 subnormal underflow 外，乘以
$2^{-14}$ 本身在 binary64 可精確表示；此條款主要封住 underflow 與未來實作漂移。

正式計算順序固定為：input validation → leakage／fixed rule → validated enclosure →
effective `atol` → adaptive cubature → item-3 certification。`_cubature_pairing` 必須顯式
接收本列 `atol`，不得由測試或 caller 改寫 module global。`PairingEnclosure.levels` 必須
記錄實際使用的 $(64,128,256)$，不能依賴 dataclass definition-time 的舊 default。

v0.2 status/reason 優先序亦固定如下；input contract violations 仍在報告建立前拋出
`E4ProtocolError`，不屬下表：

1. leakage 不合法時為 `INCONCLUSIVE / STRUCTURAL_LEAKAGE_INVALID`；這個結構性理由
   優先於 tolerance derivation，且不得啟動 adaptive；
2. leakage 合法但 $s$／$a_{\rm eff}$ 未定義時為
   `INCONCLUSIVE / ADAPTIVE_TOLERANCE_UNDEFINED`，不得啟動 adaptive；
3. adaptive 已啟動後，依序判定 `NONFINITE_BACKEND`、`ADAPTIVE_RESOURCE_CAP`、
   `NUMERICAL_CERTIFICATION_INCONCLUSIVE`，最後才可為 `CLEAN / CERTIFIED`。

為避免把「未執行」偽裝成數值結果，v0.2 `E4Report` 必須新增
`effective_atol: float | None`，並把 `adaptive`、`adaptive_run`、`certification` 明訂為
optional。上述第 1、2 分支仍須保留已計算的 `leakage`、`gauss` 與 `enclosure`，但
`effective_atol`、`adaptive`、`adaptive_run`、`certification` 全為 `None`。不得填入零矩陣、
NaN 或 synthetic `CertificationResult`。所有 consumer（含 `clean` property、item 3、screen
與 ledger serialization）都必須先依 status/reason 分支，再存取 optional fields。

## 3. Version identities 與 seal 影響

候選 identities 固定為：

- contract：`stage5c-6a-e-e4-wellposedness-v0.2`；
- enclosure：`positive-gaussian-characteristic-cell-enclosure-v0.2`；
- fixed estimate：`gauss-legendre-32-with-cell-enclosure-v0.2`；
- adaptive estimate：`adaptive-genz-malik-scale-aware-with-cell-enclosure-v0.2`。

fixed Gauss--Legendre matrix 公式雖不變，其 validated `ErrorBudget` 由新 enclosure 產生，
故 implementation identity 也必須升版。topology 與 leakage 公式未改，分別保留
`finite-probability-gaussian-mixtures-fixed-epsilon-v0.1` 與
`ambient-gaussian-box-and-causal-leakage-v0.1`。

item-3 certification 公式本身可保持，但兩個 estimates、agreement、norm interval、
endpoint error、implementation IDs 與 source-row fingerprint 都須視為新 payload。
items 4--5 的 source-ensemble seal、numerical half-width 與 strict boundary classification
必須由新 rows 全部重建；不得跨 v0.1／v0.2 重用 seal。

## 4. Deterministic development evidence

下表只使用三個 candidate-independent single-atom witnesses；沒有 RNG、seed、generator、
matching 或 arm data。每列以新 enclosure levels 與上述 $a_{\rm eff}$ 在記憶體中探查：

| witness | enclosure width | subdivisions | normalized endpoint error |
|---|---:|---:|---:|
| Gate A $(.70,.70,.05,.05)$ | $2.2248\times10^{-14}$ | 49 | $(0.00580,0.00696)$ |
| Gate B near-zero $(.80,.80,.20,.20)$ | $7.4350\times10^{-13}$ | 68 | $(0.00279,0.00335)$ |
| wide-cell $(.55,.55,.45,.45)$ | $2.2836\times10^{-2}$ | 158 | $(0.01956,0.02347)$ |

三列均低於理想 top-$M$ selection-agnostic benchmark 的 per-arm $1/40$，只證候選同時
移除三個已知 pointwise bottlenecks。它**不**證 admissible support 的 uniform cap、
Gate-A failure tail、matched-null mean／factor、完整 split certification probability、
cohort floor 或任何 scientific PASS。特別是 $0.02347$ 靠近 $0.025$，沒有可任意消耗的
統計餘裕；而 factor-8 全池 benchmark 要求 $1/160=0.00625$，Gate-A witness 的第二
座標與 wide-cell witness 仍未滿足。combined amendment 不會自動恢復該路線。

enclosure 最高級 256 是在已看過 wide-cell witness 後選出的最小已探查級數，使該
witness 的第二座標降到 $1/40$ 以下；因此該 witness 是 in-sample design input，不是
v0.2 的獨立確認，也不得在 closeout 中被改寫成 out-of-sample validation。

implementation regression 另須加入非對稱 atom $(.70,.30,.05,.20)$。development 探查中
$U_1/U_2\approx2.7\times10^{11}$：本候選的 $s=\max(U_1,U_2)$ policy 為 `CLEAN`、83 次
細分且 normalized endpoint error 約 $0.0092$；反事實改用 `min(U_1,U_2)` 則耗盡 4096
細分並成為 `ADAPTIVE_RESOURCE_CAP`。這條 regression 必須同時鎖住 max policy 與 min
counterfactual，防止未來以「更保守」為名改成 min；三個對稱 witnesses 無法偵測此退化。

## 5. Resource evidence 與不可放寬的 caps

enclosure refinement 的寬度約每次加倍 cells 減半，但 traversal 成本約每次加倍 cells
增加一個立方階。development container 上，以 8128 個重複 Gate-A atoms 只量
`pairing_enclosure`（不含 fixed／adaptive cubature）得到：

| levels | wall | process peak `ru_maxrss` | enclosure width |
|---|---:|---:|---:|
| $(16,32,64)$ | 2.606 s | 121036 KiB | $8.8339\times10^{-14}$ |
| $(32,64,128)$ | 17.939 s | 186832 KiB | $4.4427\times10^{-14}$ |
| $(64,128,256)$ | 141.038 s | 470748 KiB | $2.2248\times10^{-14}$ |

這些是單一輸入、單一環境的 development observations，不是正式 worst-case bound。
v0.2 不得放寬既有 4096 subdivisions、900 s per-E4 wall、57600 s total CPU、32 GiB
address-space caps。目標主機總記憶體約 7 GB，因此任何新 authorization 前另須以 exact
v0.2 blobs 在該主機確認可用記憶體大於 qualified peak；32 GiB address-space cap 不是
實體記憶體保證。

implementation PR 必須交付 candidate-independent resource qualification，至少涵蓋：

1. 三個 $N$ 與十一 selectors 的可達 selected-pair count 上界；
2. exact v0.2 producer 在各 registered count profile 的 wall／CPU／RSS；
3. 264-call schedule 的事前 CPU 上界不超 57600 s；
4. 每一 E4 call 不超 900 s，且任何 nonfinite／4096 exhaustion 均 fail closed；
5. target-host preflight 與新 runner authorization pin 當時 current blobs。

CPU 一律以每個測量區間前後
`resource.getrusage(resource.RUSAGE_SELF).ru_utime + ru_stime` 的差值計算，並須同時報告
per-call 與完整 264-call schedule；不得以 wall time 代替 CPU time。若 BLAS 或其他 backend
使用多執行緒，CPU 可以大於 wall，仍以 CPU 值對 57600 s cap 判定。

若無法在既有 caps 內證成，candidate 必須回到 amendment review；不得根據已看過的
screen 或 arm 結果縮小 levels、放寬 caps、刪除 strata 或延長資源。

## 6. Downstream revalidation 與不可宣稱事項

本提案使 closure matrix 的 item 7 進入 `AMENDMENT-REVIEW-PENDING`，並把 items 3--5
標為歷史 v0.1 closure 保留、v0.2 `REVALIDATION-PENDING`。這不否定原 deliverables；
它表示任何 v0.2 preregistration 都不能引用舊 rows／regions 當作已複核輸出。

正式 closeout 至少需要：

- item 7：producer implementation、zero／underflow branch、actual-level metadata、
  具名 reason／skipped-adaptive nullable schema、非對稱 max-vs-min regression、resource
  regressions、full test suite、independent exact-head review；
- item 3：既有 CLEAN 與 INCONCLUSIVE cases 的完整 numerical payload diff、agreement、
  norm／ratio、source-row seal 及 mutation／real-seam tests；
- items 4--5：由新 rows 重建 numerical half-width／ensemble seal，重跑 E1／E2／E3
  strict boundaries；
- screen／custody：歷史 authorization、candidate、attestation 與 burned namespace
  逐位元不動；若開新 namespace，須用新 protocol／runner／authorization 並重新 pin
  所有 executable blobs。

即使上述兩個 bottlenecks 都由 v0.2 移除，Gate B 仍可能因真實 matched-law mean、
matching-conditioned factor、statistical width 或其他 admissible mixtures 而失敗；Gate A
的 selector、adaptive-resource 與 item-3 failure-probability buckets也不會由三個 witness
自動關閉。**amendment deliverable 是移除已指明的 producer bottlenecks並重新驗證下游，
不是 Gate A／Gate B closure。**

## 7. 合法後續順序

1. 本 proposal exact head 經 CI、independent review 與 merge；
2. 另開 implementation PR，且只實作本文件／JSON 固定的 v0.2 candidate；
3. 完成 resource qualification 與 items 3--5 revalidation；
4. exact-head independent review 後，以 state-only closeout 決定 v0.2 是否可 `CLOSED`；
5. 只有其後才可另設新 screen protocol／seed namespace／authorization。

任何一步失敗均保持 fail closed；不得把本 proposal、development timings 或 witness
數值直接 import 到 runner，亦不得觸及候選 $K$。
