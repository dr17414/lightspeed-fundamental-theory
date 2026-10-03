# Item 7 v0.2 resource characterization — qualification remains blocked

日期：2026-10-03。`authorization=NONE`。本交付不修改 producer、runner、resource caps、
selector family 或 candidate JSON，也不開新 namespace。

## 1. Reviewed baseline

PR #59 exact head `536925694a0f32f25caaf1567063543c140a73eb` 經獨立 GO 後
squash-merge `d2c665ad78bbd2d3dd12360e934307d67ed979f7`，merge tree 是
`971a521fbc18128295878925babf46d38c279868`，與受審 tree 逐位元相同。
這是 implementation draft 的合併，並非 item-7 closeout。

獨立 review 指出低細分 repeated gate_a 不能界住 4096 exhaustion 的成本，且
`TimeoutError` 目前會作廢整個已 burn 的 screen。本輪因此先交付便宜的固定成本
特性分析，未投入完整 264-call qualification。此前記錄的 8128-atom probe 只有
49 subdivisions，已在 implementation 文件補明其不是每 atom 成本上界；historical
targeted 88 的 reproduction 指令也改為實際五個 test files。

## 2. 固定環境與 stress scope

新 harness 為 `benchmarks/stage5c_e4_v02_resource_characterization.py`：

- 在任何 numerical import 前，要求 OMP、OpenBLAS、MKL、BLIS、VECLIB、NUMEXPR
  六個 thread env 都為字串 `1`；Linux affinity 限為一個當時可用的 logical CPU；
- NumPy 2.3.5、SciPy 1.17.0、threadpoolctl 3.6.0；每次 probe 記錄 Python／CPU model／
  cgroup quotas／affinity／threadpool library versions 與實際 thread count，且 threadpool
  不為 1 時拒跑；此主機不是指定約 7 GB target host；
  evidence 記錄的 cgroup quota 為 8 CPU、memory limit 為 8 GiB，實際 affinity 為 1 CPU；
- 每個 phase 用新程序，RSS 是該程序的 Linux `ru_maxrss*1024`；CPU 用
  `time.process_time()`。保留 900 s wall、57600 s process CPU、32 GiB RLIMIT_AS；
- 純固定 fixtures，沒有 RNG、generator、seed、matching 或 scientific arm ledger；
- enclosure 使用真實 v0.2 producer。Adaptive stress 的 integrand 逐項轉錄 production
  primitive，另用 regression 驗證 bitwise parity；共享 frozen density／biweight helpers；
- stress 直接呼叫真實 Genz–Malik，顯式 `workers=1`，刻意設 `atol=rtol=0` 來走到
  指定 subdivision budget。沒有改寫 producer globals，沒有建立 E4 report，亦沒有
  將這些 stress tolerances 當成新 candidate。實際 subdivisions 未達指定 budget 時
  拒絕把 probe 記作有效 exhaustion 成本。

所有成本只涵蓋被量測 phase，排除 imports／input setup、fixed rule、selector／adapter、
certification 與完整 schedule 的其他成本。RSS 含程序 import 的峰值。這種 phase clock
可用於分解成本，但**不是** proposal 要求的完整 schedule 同起點 qualification。
計時期間逐 probe 執行，不並行另一組 numerical tests／probes。

## 3. Selected-count 的結構性 witnesses

在 N=64、96、128 上，各跑十二個固定 geometry fixtures、全部十一 members，共
396 次純 selector 評估：chain、antichain、two/four layers、bit reversal、三個 modular
permutations，以及四個 interval bridges。Domain／selection empty 以 categorical rows
記錄；不把不存在的 selected pairs 偽裝成可積分 atoms。

### 3.1 可達大 count

Total chain 的 all_relations 取 N(N−1)/2。兩層 antichains、層間全 comparable，
其 links 取 N²/4；所有 pair 的 depth score 相同、midquantile 都是 1/2，所以中央
[0.4,0.6) band 也取全部 N²/4，不能用「五個 bands」推出逐 band ≤20% pair count。
三層 interval bridge 的中央有 m=1..4 個點，兩側平衡分配 N−m 個點；兩側之間每對
的 open interval 恰含 m 個點，故 interval_exact(m) 可取 floor((N−m)²/4)。

這些 points 在 unit box 嚴格內部，有限 coordinate gaps 遠大於 10^-12 margin；它們
只證明大 count 不能被既有 topology／selector 規則排除，不給出 target-law 機率。

| Selector / parameters | N=64 | N=96 | N=128 |
|---|---:|---:|---:|
| all_relations | 2016 | 4560 | 8128 |
| links | 1024 | 2304 | 4096 |
| interval_exact (1,) | 992 | 2256 | 4032 |
| interval_exact (2,) | 961 | 2209 | 3969 |
| interval_exact (3,) | 930 | 2162 | 3906 |
| interval_exact (4,) | 900 | 2116 | 3844 |
| endpoint_depth_mass_band (0.0, 0.2) | 406 | 903 | 1653 |
| endpoint_depth_mass_band (0.2, 0.4) | 900 | 1152 | 2048 |
| endpoint_depth_mass_band (0.4, 0.6) | 1024 | 2304 | 4096 |
| endpoint_depth_mass_band (0.6, 0.8) | 768 | 1728 | 3072 |
| endpoint_depth_mass_band (0.8, 1.0) | 420 | 905 | 1573 |

表中的值是**十二個 fixtures 的已觀察最大值**，並非逐 member 的一般上界、正式
distribution quantile 或 failure tail。完整 396 列見 companion evidence JSON。

### 3.2 links 的較細上界

Cover graph 沒有 triangle：若三點兩兩 comparable，傳遞性使最低到最高的 edge
包含中間點，不能為 link。Triangle-free graph 的每條 edge uv 滿足 d(u)+d(v)≤N；
若有 E 條 edges，則 sum_v d(v)^2≤NE，而 Cauchy 給
sum_v d(v)^2≥(2E)^2/N。因此 E≤N²/4，links 的 exact upper 為 floor(N²/4)，
且 two-layer witness 達到。這改善 links 的 count 上界，仍不是 CPU／wall 上界。
其他 members 此處只保留通用 N(N−1)/2 上界與已觀察可達 counts，不宣稱更細上界。

### 3.3 完整 family 的 joint count 上界

令 D 為全部 relations、B_b 為五個 depth bands、I_m 為 open-interval cardinality
恰為 m 的 relations。B_b 分割 D，所以 `sum_b |B_b|=|D|`；links=I_0 與
四個 interval_exact=I_1..I_4 互斥，但它們一般不涵蓋 cardinality≥5 的 relations。
十一 calls 的實際總和是 `A=2*|D|+sum_{m=0}^4 |I_m|`，其上界寫作
`A ≤ |D| + |D| + sum_b |B_b| = 3*|D|`。第二個 |D| 是五個互斥
low-cardinality selectors 的上界，最後一項才是 depth-band 的恆等式。
36 個 inventory cases 實際 A 的總和為 248315，每一 case 均符合上述 identity／bound。
不能把不同 fixtures 的逐 member maxima
當作能同時實現的 joint profile。登記 schedule 每個 N 有 2 targets ×4 repetitions，
故 264 calls 的 count 總和保守上界為
`8*3*(2016+4560+8128)=352896`。這是 count 上界，沒有把未證成的 per-atom 成本
套入後宣稱 CPU 上界；generation／selector／adapter 等成本也不由它涵蓋。

## 4. Phase 成本曲線與可用的結論

輸入是三個固定 interior atoms cyclic 重複，使用 production uniform-weight adapter；
沒有合併重複 atoms。固定 plan：三個 registered conservative count profiles 的 enclosure、
252／1008 atoms 的完整 4096 stress，以及 2016／4560／8128 atoms 的 256 stress、
8128 atoms 的 512 stress；另補 1008 atoms 的 256 stress 以比較同一 count 的細分尺度。
每個 probe 有 exact source blob pins。

| Phase | Atoms | Subdivisions | CPU s | Wall s | Peak RSS MiB |
|---|---:|---:|---:|---:|---:|
| enclosure | 2016 | — | 35.213 | 35.235 | 371.71 |
| enclosure | 4560 | — | 77.549 | 77.571 | 409.80 |
| enclosure | 8128 | — | 138.697 | 138.713 | 445.48 |
| adaptive_stress | 252 | 4096 | 56.796 | 56.803 | 82.62 |
| adaptive_stress | 1008 | 4096 | 200.459 | 200.474 | 82.64 |
| adaptive_stress | 2016 | 256 | 24.401 | 24.406 | 61.24 |
| adaptive_stress | 4560 | 256 | 54.423 | 54.427 | 61.39 |
| adaptive_stress | 8128 | 256 | 94.351 | 94.359 | 61.50 |
| adaptive_stress | 8128 | 512 | 190.333 | 190.347 | 62.89 |
| adaptive_stress | 1008 | 256 | 12.671 | 12.675 | 61.38 |

完整觀察與 source／environment pins 在 `docs/stage5c_e4_v02_resource_characterization.json`。
該 JSON blob 為 `54b69083db971661b38196a5de65a1ec9b3c0e41`，本輪文字整理不改其內容。
全部十個 probes 均已被看過；後續 resource amendment 的 model candidates 是看過它們
之後才提出。因此這些都是 development／training 資料，不能改稱 held-out validation。

Illustrative CPU phase-subtotal 外推（enclosure +16×256-subdivision stress）：

| Atoms | Measured enclosure CPU | 16×256 stress + enclosure |
|---|---:|---:|
| 2016 | 35.213 s | 425.634 s |
| 4560 | 77.549 s | 948.324 s |
| 8128 | 138.697 s | 1648.313 s |

8128 atoms 另以 8×512 的 stress 外推加 enclosure 得 1661.358 CPU s；
1008 atoms 的已量測 4096／256 CPU 比為 15.820（名義 subdivision 比為 16）。
這支持在此固定 mixture 上成本近似隨細分數增加，但不是線性性定理或有效 bound。
單執行緒下所有 phase 的 CPU／wall 接近 1；threadpools 中兩個 OpenBLAS library 都實測為 1 thread。

外推只比較固定 harness 的已觀察尺度，**不是 production v0.2 call 的 lower／upper bound**。
Zero-tolerance stress 不是 candidate 的有效 tolerance；且該 mixture 不宣稱來自真實
selector→adapter output。因此「大 selected count 可達」與「強制 4096 的成本大」
不能合併成已證明 registered production 必然 timeout。反過來，有限低細分 samples
也不能排除這個組合，或證明所有 calls 都在 900 s 內。

結論是：目前沒有在既有 caps 內證成 proposal §5，qualification／closeout 維持 blocked；
不可從這組 fixture 成本直接進入完整 one-shot screen。若不能用 validated bound 排除
昂貴的 exhaustion 組合，下一步應回到 resource amendment review。

## 5. Resource amendment review 的範圍

現有 `_one_member` 不捕捉 `TimeoutError`；`run_screen` 的 BaseException handler 會
報 `SCREEN-INCOMPLETE`，而 seed 已 burn。本交付沒有改變這個既有語意。
供下一份明文 amendment 比較的選項是：

1. 把 per-call timeout 規範為 per-member NONCLEAN，明訂分類／reason、short-circuit、
   nullable serialization 與 partial-result 處理；failure bucket 必須包括 timeout。
2. 調整 subdivision／wall／CPU caps，重新證成 target-host 可負擔；不能把未知成本
   直接轉成無上限等待。57600 s total CPU 的證成須涵蓋完整 schedule 起點與 overhead。
3. 明訂 atom count 限制或計算預算 policy；其對十一 members 的 eligibility、failure
   tail、scientific gates 與新 identity 的影響須重新 preregister／review。

本 PR 不選定其中一個方案，也不改任何常數／catch policy。任何選項都須在新 namespace
之前正式 freeze、獨立 review、重新 pin。未來 authorization 應明訂 thread environment、
workers、CPU affinity／host profile，qualification 必須使用相同設定並檢查實際 runtime
threadpools；不能僅因 shell 宣稱單執行緒就推定 BLAS 已照做。

未來 consumer 以 `enclosure_id`／`contract_id` 判版本，不能以 `isinstance` 判 v0.1／v0.2：
v0.2 PairingEnclosure 是 v0.1 類別的子類。歷史 custody、attestation、burn registry、
frozen producer／runner 與本輪所有 analysis files 逐位元不動。

## 6. Reproduction 與 gates

Linux、pinned numerical dependencies；另安裝 development-only `threadpoolctl==3.6.0`。
每個新 CLI invocation 都先設以下環境（必須在 NumPy／SciPy import 之前）：

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python -m benchmarks.stage5c_e4_v02_resource_characterization selector-counts
python -m benchmarks.stage5c_e4_v02_resource_characterization suite
python -m benchmarks.stage5c_e4_v02_resource_characterization probe --stage adaptive_stress --atoms 1008 --subdivisions 256
python -m pytest -q tests/test_stage5c_e4_v02_resource_characterization.py
python verify_integrity.py
python -m pytest -q tests/
```

Suite 輸出 JSONL，每個完成 probe 立即保留；不跑完整 264-call screen。計時重現時應
單獨執行 suite，測試放在它完成之後；改 host／threads 的結果不能直接搬成資格證據。

本地驗證：harness targeted **6 passed**；全庫 **424 passed, 5 existing warnings**
（91.79 s）；integrity 與 `git diff --check` 通過。Source／environment pins 與全部 ten probes
一致，計時完成後才跑 numerical tests。

Item 7 `AMENDMENT-REVIEW-PENDING`；items 3–5 歷史 `CLOSED-v0.1`／v0.2
`REVALIDATION-PENDING`；item 8 `OPEN`；6a-E `PREREGISTRATION-INCOMPLETE`。
沒有新 runner authorization、namespace、arm endpoints 或 candidate K。
