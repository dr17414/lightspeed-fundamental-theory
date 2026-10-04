# Item 7 deterministic resource measurement manifest v0.1

`REVIEW-DRAFT`；`authorization=NONE`。本 PR 提供完整的固定輸入、方法、執行計畫與
診斷 harness，供 exact-head 複核；本輪只執行已公開 training 資料的方法驗證和 tests。
沒有執行新計時 probes、screen、generator、seed、arm ledger／endpoint 或候選 K。
合併不等於執行授權，沒有提交 external authorization receipt。

## 1. Baseline 與用途

引用 main merge commit `81f3d70079d32fe989050d4295b0ec2c9084a2e6`、tree
`2a137a2aac32bb6429447e9c13db9329b1b91765`；其 parent 為 #60 merge
`95d0ceaf0e57127046258b9ee7596e05faab2a21`、tree
`3b515d5da12539589e3c084403167500211e7b79`。Closeout 引用 merge commits，不把
original PR heads 當 main。原 evidence JSON blob
`54b69083db971661b38196a5de65a1ec9b3c0e41` 保留不變。

事前選定的 package 是 **維持 production caps，診斷可達性與模型適切性**，沒有選定
提高預算、平行化、切分或改 qualification。本輪零 parallel jobs；1.25 safety multiplier
與 1.10 parallel CPU ratio policy 沿用受審 framework，但沒有 resource ADOPT verdict。
Machine-readable plan 是 `stage5c_e4_v02_resource_measurement_manifest.json`；全部來源、
方法／fixture artifacts 有 SHA256 pins，receipt 再釘 exact reviewed merge commit 和
manifest file SHA256，因此不存在 manifest 自己引用自己 hash 的循環。

本 campaign 是 development，不是完整 264-call schedule／target-host qualification。
即使所有 probes 成功，也不能只靠樣本關閉 item 7 或 item-8 failure tails／power。

## 2. 方法驗證（已執行；沒有新量測）

七列 stress 都是**未 censored、outcome=FORCED-BUDGET-EXHAUSTED、非 timeout**；
另外三列 enclosure outcome=COMPLETED。十列都已被看過，是 development/training。
44 個 CPU／wall fits 的 coefficients、active-positive masks、七列或三列 predictions／
residuals 與 residual norm 保存為 `stage5c_e4_v02_resource_method_reference.json`。
這是方法 regression fixture，不是 held-out validation；沒有保存新 held-out 點的預測。

釘 NumPy 2.3.5／SciPy 1.17.0，`scipy.optimize.nnls(maxiter=10000)`，binary64。
Pinned implementation 的 `atol` 不參與求解，所以刻意不傳，也不把它宣稱為 solver
accuracy control。保存 NNLS Python wrapper SHA256；actual active set 要與 reference
完全一致，數值漂移用 `rtol=1e-8, atol=1e-10` 比較 coefficients／predictions／residuals／norm。
這些是 regression acceptance tolerances，不是 cost-model uncertainty bounds。
Reference 在 Python 3.12.14 生成；CI 以 Python 3.12.13 重驗。

順序與 loss 固定：保持 evidence 原列序、等權 absolute-second squared loss，CPU／wall
各自擬合，不以 per-atom normalization 改權重。Stress 主形式 columns 固定為
`[1,a/8192,s/4096,a*s/(8192*4096)]`。Reference 儲存此縮放座標的係數；原式
`[b0,b1,b2,b3]` 分別除以 `[1,8192,4096,8192*4096]` 還原。
Power forms 為 `[1,(a/8192)^p*(s/4096)^q]`，p,q 各取 {0.9,1,1.1,1.25}，
對同一七列 NNLS 擬合 h0 與 scaled k；original k 除以 `8192^p*4096^q`。
Enclosure affine／power 對同一三列，columns 為 `[1,a/8192]` 或 `[1,(a/8192)^p]`。
沒有新 fitting weights、替代 solver 或最佳模型選擇。

SVD rank threshold 固定為 `smallest > 2^-40 * largest`，full-column-rank 才進 NNLS。
Full rank 下 convex NNLS 的係數解唯一；tie policy 是接受 pinned solver 的 active set，
不用第二個 solver 選較樂觀解。Rank 不足或 regression 漂移即方法驗證失敗，停止計畫。
主 design rank=4、residual df=3；條件數取決於欄位縮放，不能把 rank 當成 extrapolation
可靠性的證明。交互項由兩個低 a／s=4096 點及 (8128,512) 稀疏支撐，須在報告保留。

所有新資料只能拿 frozen reference 作 residual check，禁止 refit／調 threshold。
若要新 mixture 的 training／hold-out 方法，須另訂 manifest，不把本輪 production
fixtures 的 full-E4 timing 冒充 cyclic-mixture 的 stress-phase residual。

## 3. Fixtures 的選擇規則及 exact bytes

候選全集是原 inventory：3 N ×12 geometries ×11 members，沒有 target-law 抽樣。
對每 N、每 member，選 `category=SELECTED` 中 selected count 最大的 geometry；
平手按 fixture ID 的 ASCII lexical order，忽略計時與結果 reason。

另對每 N 的下列三個**geometry recipe strata**選 all_relations count 最大者，平手同上：

| Stratum | 固定候選 |
|---|---|
| total_order | chain |
| layered | two_layers, four_layers, interval_bridge_1..4 |
| dispersed | bit_reversal, modular_5, modular_17, modular_31 |

這些不是 probability strata。合併上述選取、按 `(N,fixture ID,member evaluation index)`
排序；同一 `(N,fixture,member,parameters)` 去重，保留全部選取理由。結果為 39 組。
每組再按 theta=-0.4、+0.4 的固定順序，共 78 個 production-tolerance calls。

`stage5c_e4_v02_resource_fixture_bytes.json` 保存全部 36 個 geometry 的座標 **binary64
little-endian、C-order bytes（base64）、shape 與 SHA256**，而非只列勝出名單。
39 組另保存 real selector 的 pair indices `<i8` hash，及 real production adapter 的
atoms／weights `<f8` hashes、selected count。Pinned generator 可重建全部 bytes；
每次使用先驗 hashes，且 selectors 只看 `BlindedCase` order／constant ID。
不建構帶 seed 的 `ControlSample`，不呼叫 generator、`run_screen` 或 burn。

Stress 固定為原三個 atoms 的 exact hex、theta=+0.4，cyclic repeat 至 a=8128，
production uniform weights；atol=rtol=0、Genz–Malik、workers=1。
Production calls 用真實 selector→adapter→v0.2 evaluate，完全保留 candidate tolerance；
只記 a、實際 subdivisions、adaptive-skipped、status/reason 與 clocks，不輸出 endpoints。
它們是 pointwise reachability witnesses，沒有撞 cap 不構成完整 domain exclusion。

## 4. 執行順序、預算與停止規則（未執行）

順序與 job IDs 全部在 JSON 中，沒有輪替／randomization／事後重排：

| 順序 | 工作 | Calls | Per-child wall / CPU cap |
|---|---|---:|---|
| 0 | Receipt、source/host/memory pins、training method verification | — | Supervisor whole-process CPU 120 s |
| 1 | 單次 direct stress (8128,4096) | 1 | 4500 / 5000 s |
| 2 | 39 fixture/member × theta {-0.4,+0.4} | 78 | 900 / 1000 s |
| 3a | a=8128, s=128，32 invocations | 32 | 900 / 1000 s |
| 3b | a=8128, s=256，16 invocations | 16 | 900 / 1000 s |
| 3c | a=8128, s=512，8 invocations | 8 | 900 / 1000 s |
| 3d | a=8128, s=1024，4 invocations | 4 | 900 / 1000 s |

總共139個新 timed invocations，每個 fresh child process，任何時刻只存在一個 worker。
**整體計畫上限：60000 s wall、57600 s accounted CPU**，不是逐 probe caps 相加。
計畫 wall 從 receipt/preflight 開始，含方法驗證／imports／setup／cleanup；CPU 是 whole
supervisor `process_time()`（含 imports）加 `wait4` 所取 direct child user+system CPU。
worker 沒有 subprocess/parallel backend；這是 diagnostic campaign 的 aggregate 計量，
不改 production 的 process_time cap，也不能充作 production schedule CPU 上界。

Supervisor hard CPU=120 s；每 child 使用 RLIMIT_CPU soft=listed cap、hard=cap+1。
Admission 固定保留完整120 s parent額度與2 s child kernel/collection margin：若
`completed_child_CPU + next_cap + 2 + 120 > 57600`，不啟動下一項，記全部剩餘 NOT-RUN。
Supervisor 留5 s wall cleanup margin；到整體 deadline 即 kill/reap current child 並停止。
Worker 自身也有 SIGALRM，deadline 不超過 per-child 或剩餘整體 wall，以免 supervisor
異常終止後留下無 wall 限制的 orphan。監控以50 ms cadence；若實測最終超限或缺完整
summary，一律 PLAN-INCOMPLETE／證據不足，不宣稱診斷 cap 的 validated execution bound。

Direct probe 固定在最前。Individual wall／CPU censor 仍續跑其餘 jobs；不補跑、不延長，
不因 direct censor 改成較小 a。Source／runtime mismatch、方法 regression、memory
abort、unexplained exit/signal 或 global budget failure 停止並保留剩餘 NOT-RUN。
SIGXCPU 才記 CPU censor；無已知 supervisor kill reason 的 SIGKILL 一律 implementation
abort，包括無法判因的 hard-cap/OOM kill，不靠時間接近 cap 猜測原因。
任何資料夾只允許一次 attempt；exclusive create、即時 JSONL checkpoint/fsync，無 resume。
若 crash 前只有 ATTEMPT-STARTED，該項仍占 attempt，不能當未嘗試後重跑。

Per-phase clocks 是 stress integral 或完整 E4 evaluate 前後 process_time／monotonic 差值；
whole-child CPU/wall 包含 imports／selector／adapter／setup，兩者分開。Censored worker
的 phase clocks 若不可取得，保存 null；whole-child cost 不能冒充 phase lower bound。
Timeout 不刪除，也不當 completed output 或假造 adaptive subdivisions。
PLAN-COMPLETE 只表示全計畫 attempts 已記錄，允許其中有 censoring；不等於模型驗證
通過或 qualification 完成。缺 final summary 的 crash 一律屬 incomplete。

## 5. Host、memory 與執行 gate

固定為 development host：Python 3.12.14、AMD EPYC 9V74 80-Core Processor、
cgroup cpu.max=`800000 100000`／memory.max=`8589934592`；allowed affinity=0..8，
實際pin={0}。六個 thread env 在 numerical imports 前均為1；NumPy 2.3.5、SciPy1.17.0、
threadpoolctl3.6.0，實際全部 BLAS pools必須1，integrator workers=1。
Host 不符即 preflight fail，不自行選新 host／threads。Host移轉需新 manifest/review。

每次啟動前要求 host MemAvailable 與 cgroup剩餘記憶體均≥3 GiB；child peak RSS cap
2 GiB，parent+child concurrent RSS cap2.5 GiB，RLIMIT_AS32 GiB另記。每個 child 的
ru_maxrss 與 live RSS監控均保留，retroactive RSS超限同樣停止。
每項也記host/cgroup available memory、parent/child peaks。兩者peak之和是concurrent
RSS的保守上界，未宣稱兩個peak同時發生；若此上界超2.5 GiB也停止，不取樣漏掉峰值。
單 process 舊觀察467 MB不是 memory bound。本輪無 parallel worker memory資格化；8 GiB不是約7 GB
target。Target preflight／aggregate worker memory仍須另證。

新 harness 為 `benchmarks/stage5c_e4_v02_resource_campaign.py`。沒有 receipt 時在
resource mutations／numeric producer之前拒跑，tests鎖住這個 gate。
未建立 receipt；待 exact-head review／merge與明確 resource execution授權後，external
receipt才可釘：authorization=`DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY`、reviewed_commit
（當時main merge SHA）、manifest_sha256、absolute output_directory。Receipt/output均
在repo之外，checkout須clean。Receipt不授權 scientific screen或新seed namespace。
Worker只接受 supervisor parent／receipt／internal job index，不能以普通CLI啟動timing。

## 6. Held-out 判讀門檻（量測前固定）

三個未見 stress cells 為 (8128,4096)、(8128,128)、(8128,1024)，共37個 planned
observations；repetitions不算37個獨立inputs。s=256/512的24個新invocations是 seen-cell
repeatability diagnostics，不是 held-out。原十個 probes與 reference全部是training。
本計畫沒有新的 count／mixture-domain model validation；coverage缺口必須明列證據不足。

對每個 CPU／wall stress model、每個 held-out observation，令
`r = observed_phase_seconds - frozen_prediction`：

- `|r| ≤ 0.10*max(1 s, observed_phase_seconds)`：POINTWISE-MODEL-CHECK-PASS。
- 超過此門檻：該 model為MODEL-INVALID。界線取≤通過，正負 residual都檢查。
- Censored/not-run/phase-cost未知：INSUFFICIENT-EVIDENCE。若有獨立可信的 phase
  lower bound，也只能在已超門檻時判invalid；不得拿whole-child時間套入。

固定 loss/scaling／17個 stress model candidates不改，全部逐列 residual、最大正 residual、
active set／coefficients、repeat scatter與censoring一併報告。不挑最快模型、不刪失敗列，
不靠repetition平均或平方和縮小systematic error。任何model invalid或unresolved，整組
規劃model判INSUFFICIENT-EVIDENCE，不事後選通過子集；即使全部pointwise pass，也只標
POINTWISE-ONLY-NO-DOMAIN-BOUND，不能ADOPT resource方案。

Framework「維持現行caps」仍需要 production-domain validated U_wall×1.25≤900、
U_CPU×1.25≤57600、完整error/overhead與memory資格化。REJECT中的必要成本lower
bound也必須來自production domain，不能來自zero-tolerance stress或diagnostic probe。
Observed production超時只能按實際E4區間解讀；若只是whole-child含setup超時，未完成
的E4是否自身超900仍未知。任何ADOPT/REJECT不得偷換這兩種scope。

## 7. 下一步

本 manifest／harness exact-head review通過後先merge，另處理external execution receipt；
目前authorization=NONE。新結果另開evidence PR，附139項完整結果／not-run、accounting、
model checks與source/environment pins。若需要policy amendment，依framework重審，
不得看到結果後延長預算、改fixture或放寬門檻。Item7仍AMENDMENT-REVIEW-PENDING、
items3–5 REVALIDATION-PENDING、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE。
完整resource qualification／下游revalidation／independent review之後，另開state-only
closeout；沒有新namespace、scientific authorization或候選K。
