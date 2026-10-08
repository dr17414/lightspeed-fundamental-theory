# Item 7 deterministic resource measurement manifest v0.5

`REVIEW-DRAFT`；`authorization=NONE`。本 PR 提供完整的固定輸入、方法、執行計畫與
診斷 harness，供 exact-head 複核；本輪只執行已公開training資料的方法驗證與tests；真實Linux limits/signals測試
使用短sleep／busy stubs，不呼叫numeric producer，也不形成research timing evidence。
沒有執行新計時 probes、screen、generator、seed、arm ledger／endpoint 或候選 K。
合併不等於執行授權，沒有提交 external authorization receipt。

v0.3 已由 PR #62 合併為 `e77515a887a0a015bef6b45c789724d1c04de4e6`，tree
`227b03a93db2fb5adea923a67efdfbc5b81eb2f4` 與受審版本一致。v0.4 只補 terminal
summary 的權威規則、殘餘訊號窗口說明與 preflight 錯誤紀錄／handler 清理；139 個
jobs、caps、methods、fixtures、solver reference 與原 evidence 均不變，待新 exact-head 複核。

v0.5 提議 Vultr runtime／正式映像 pins，以及在 receipt read 前實際核對 Docker
image、參數、掛載與有效 runtime 的 launcher；OpenBLAS 0.3.30／SkylakeX kernel
明列於 manifest。映像 smoke 與套件來源已由獨立 reviewer 核對；新 launcher
待 exact-head 主機 preflight-only 驗收與獨立 review，通過後才 merge。詳見
`STAGE5C_6A_E_ITEM7_VULTR_CONTAINER_LAUNCH_REVIEW.md`。authorization 仍 NONE。

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
| 0 | Receipt、source/host/memory pins、training method verification | — | Supervisor whole-process soft CPU 600 s |
| 1 | 單次 direct stress (8128,4096) | 1 | 4500 / 5000 s |
| 2 | 39 fixture/member × theta {-0.4,+0.4} | 78 | 1020 whole-child / 1100 s；E4 scope 900 s |
| 3a | a=8128, s=128，32 invocations | 32 | 900 / 1000 s |
| 3b | a=8128, s=256，16 invocations | 16 | 900 / 1000 s |
| 3c | a=8128, s=512，8 invocations | 8 | 900 / 1000 s |
| 3d | a=8128, s=1024，4 invocations | 4 | 900 / 1000 s |

總共139個新 timed invocations，每個 fresh child process，任何時刻只存在一個 worker。
**整體計畫上限：60000 s wall、57600 s accounted CPU**，不是逐 probe caps 相加。
計畫 wall 從 receipt/preflight 開始，含方法驗證／imports／setup／cleanup；CPU 是 whole
supervisor `process_time()` 加 direct child user+system CPU。Receipt前的package/pool檢查
與receipt後既有training method驗證各在fresh exec短命子程序執行，supervisor不載入
NumPy／SciPy。兩個子程序CPU由`RUSAGE_CHILDREN`納入初始children帳；後續jobs用`wait4`。
worker 沒有 subprocess/parallel backend；這是 diagnostic campaign 的 aggregate 計量，
不改 production 的 process_time cap，也不能充作 production schedule CPU 上界。

Supervisor CPU soft=600 s、inherited hard=5001 s（由最大child cap+1決定）。
Soft超限仍送SIGXCPU；handler只設stop flag並改SIG_IGN，不在任意位置拋例外。
Preflight／job之間／monitor checkpoints讀flag，停止並kill/reap當前child，記
PLAN-PARENT-CPU-INCOMPLETE和所有剩餘NOT-RUN；write/fsync與Popen不被signal例外打斷。
Final summary寫入期間若新設flag，追加更正的terminal summary；忽略後續SIGXCPU直到cleanup完成。
Terminal summary以`record_type=TERMINAL-SUMMARY`識別，初版`summary_revision=1`；
更正版為revision=2並帶`supersedes_previous_summary=true`。讀取者必須以最後一筆
完整terminal summary為唯一權威，前一筆即使寫PLAN-COMPLETE也已被取代。
最後一次flag檢查之後、handler還原之前仍有微小殘餘窗口：新SIGXCPU可設flag但不再
修訂summary，後續訊號被忽略。`parent_cpu_seconds`只到最後取樣時刻，不含其後
summary寫入／stream關閉／handler還原的CPU；不宣稱包含全數cleanup或已有validated bound。
原SIGXCPU handler由`finally`還原，正常完成與preflight／checkpoint例外均適用。
每worker將繼承的hard降低至自身cap+1，不需提升hard權限。
Supervisor／worker均設RLIMIT_CORE=0。Admission保留完整600 s parent額度與2 s
hard-tail／collection margin：`completed_child_CPU + next_cap + 2 + 600 > 57600`
即不啟動下一項。600 s是diagnostic停止上限，不宣稱輪詢成本已有validated bound。

整體wall保留5 s cleanup；每次admission（含memory preflight後重新確認）要求
`now + next_full_child_wall_cap + 5 s startup_margin <= plan_deadline`。
啟動前起算whole-child wall，supervisor用monotonic浮點deadline，不向下取整；每列保存
per-child／plan deadline及哪個較緊。Plan deadline先到一律PLAN-WALL-BUDGET-INCOMPLETE，
不誤當個別censor或再放行新job。即使unexpected setup delay耗盡margin，也走此停止路徑。

輪詢改500 ms，最多名義120000次／60000 s；supervisor pin CPU1，worker pin CPU0。
Live RSS監控保留，wait4.ru_maxrss另作事後完整peak檢查。Worker不設whole-child SIGALRM；
Linux PR_SET_PDEATHSIG=SIGKILL及設定後parent PID再驗保護orphan，supervisor負責wall kill。
Production whole-child上限1020 s，其中固定setup allowance120 s；CPU cap1100 s，
大於整個child wall cap，單CPU配置下不會吃掉120 s setup allowance。Admission按1100 s
預留production child CPU，總57600 s不變；stress cycles仍1000 s。Worker以ITIMER_REAL
只包evaluate設900 s，和production _e4_deadline同scope。Timeout輸出
PRODUCTION-E4-WALL-CENSORED，wall lower bound=900 s；whole-child1020超時另記
WALL-CAP-CENSORED，仍不可冒充evaluate-only witness。Allowance不足不加時或重跑。

Direct probe 固定在最前。Individual wall／CPU censor 仍續跑其餘 jobs；不補跑、不延長，
不因 direct censor 改成較小 a。Source／runtime mismatch、方法 regression、memory
abort、unexplained exit/signal 或 global budget failure 停止並保留剩餘 NOT-RUN。
SIGXCPU 才記 CPU censor；無已知 supervisor kill reason 的 SIGKILL 一律 implementation
abort，包括無法判因的 hard-cap/OOM kill，不靠時間接近 cap 猜測原因。
任何資料夾只允許一次 attempt；exclusive create、即時 JSONL checkpoint/fsync，無 resume。
若 crash 前只有 ATTEMPT-STARTED，該項仍占 attempt，不能當未嘗試後重跑。
Receipt通過後、建立output目錄之前若limits／runtime／memory／method／fixture preflight
拋例外，stderr會flush一筆JSON `event=PREFLIGHT-ABORT`，含error type/message、receipt的
reviewed commit、manifest hash、output path、全部NOT-RUN IDs、worker未啟動及CPU／wall取樣。
CPU stop flag已設時outcome為PLAN-PARENT-CPU-INCOMPLETE，其他為PREFLIGHT-ABORT；
保留原例外並還原handler，不建立output目錄。執行端須保存stderr；此紀錄不授權重試。
RLIMIT本身不還原，supervisor仍只用一次性process；handler清理不表示可在同process重跑。

Per-phase clocks與whole-child clocks分列。Stress phase從開始marker至結束marker flush完成，
包含marker flush與結果metadata的instrumentation成本；這是相對舊training的額外overhead，
residual只作cross-profile diagnostic，不能解釋成純numeric cost/domain bound。
Production marker/setup不在E4 timer裡；evaluate-only timeout不保存假completed時間或subdivisions。
Censored stress若有phase-start marker及identity-verified最後live樣本：wall lower bound
用sample前monotonic減phase起點；CPU lower bound用同worker的/proc總utime+stime減
phase process_time，再扣2個SC_CLK_TCK ticks並截到0。不同process的process_time不可相減。
使用最後proven-live取樣時刻，不用kill／reap時間，以免完成/termination race產生假下界。
Missing marker、phase已finished、missing/早於phase的sample均保留null／證據不足。
Worker先公布/proc/self實際PID、namespace PID與start ticks；supervisor驗identity後才讀
/proc CPU/RSS，避免PID namespace不一致或PID reuse誤讀其他process。
Timeout不刪除、不當completed output；whole-child cost永遠不代替phase lower bound。
PLAN-COMPLETE 只表示全計畫 attempts 已記錄，允許其中有 censoring；不等於模型驗證
通過或 qualification 完成。缺 final summary 的 crash 一律屬 incomplete。

## 5. Host、memory 與執行 gate

提議固定為 Vultr development host：Sep 29 build 的 Python 3.12.14、AMD EPYC-Turin Processor、
cgroup cpu.max=`200000 100000`／memory.max=`6442450944`／memory.swap.max=`0`；allowed affinity={0,1}，
supervisor pin={1}、worker pin={0}。六個 thread env 在 numerical imports 前均為1；NumPy 2.3.5、SciPy1.17.0、
threadpoolctl3.6.0，實際全部 BLAS pools必須1，integrator workers=1。
CPU0/1 為同一實體核心的 SMT siblings；兩套 wheel OpenBLAS 0.3.30 皆選 SkylakeX kernel。
Runtime 比對 version／architecture／prefix／thread 數；舊 training 僅 cross-profile diagnostic。
Pool收集前明確import scipy.linalg、scipy.integrate及scipy.optimize，避免lazy import只見
NumPy一套BLAS。Supervisor的檢查子程序30 s wall逾時kill/reap、CPU soft/hard=30/31 s、
沿用32 GiB address-space cap、無core dump及parent-death guard；先退出再驗memory headroom。
Preflight-only僅imports／版本／pools比對，不讀receipt、不fit reference、不呼叫producer。
Production仍檢查SkylakeX；CI真實fresh-interpreter regression僅比兩個pools的數量與prefix。
Host 不符即 preflight fail，不自行選新 host／threads。Host移轉需新 manifest/review。

每次啟動前要求 host MemAvailable 與 cgroup剩餘記憶體均≥3 GiB；child peak RSS cap
2 GiB，parent+child concurrent RSS cap2.5 GiB，RLIMIT_AS32 GiB另記。每個 child 的
ru_maxrss 與 live RSS監控均保留，retroactive RSS超限同樣停止。
每項也記host/cgroup available memory、parent/child peaks。兩者peak之和是concurrent
RSS的保守上界，未宣稱兩個peak同時發生；若此上界超2.5 GiB也停止，不取樣漏掉峰值。
單 process 舊觀察467 MB不是 memory bound。本輪無 parallel worker memory資格化；6 GiB容器亦不是約7 GB
target。Target preflight／aggregate worker memory仍須另證。

新 harness 為 `benchmarks/stage5c_e4_v02_resource_campaign.py`。沒有 receipt 時在
resource mutations／numeric producer之前拒跑，tests鎖住這個 gate。
未建立 receipt；待 exact-head review／merge與明確 resource execution授權後，external
receipt才可釘：authorization=`DETERMINISTIC-RESOURCE-DEVELOPMENT-ONLY`、reviewed_commit
（當時main merge SHA）、reviewed_tree、manifest_sha256、image_config_digest、host_profile_sha256、host_boot_id、host_output_directory、absolute output_directory。Receipt/output均
在repo之外，checkout須clean。Receipt不授權 scientific screen或新seed namespace。
Host launcher 先 create stopped container、核對 actual inspect、start 前重驗；container
再驗 read-only proof 與有效 runtime，才 read receipt。固定 container paths 是
`/custody/receipt.json` 與 `/output/campaign`；proof 為獨立 `/launch:ro`。不沿用舊 receipt。
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
- Censored stress有上述可信phase lower bound時，對每個model執行one-sided residual檢查；
  lower bound已超10%門檻才MODEL-INVALID，否則INSUFFICIENT-EVIDENCE，永不pass。
  Not-run／phase-cost未知同樣INSUFFICIENT-EVIDENCE；不得拿whole-child時間套入。

固定 loss/scaling／17個 stress model candidates不改，全部逐列 residual、最大正 residual、
active set／coefficients、repeat scatter與censoring一併報告。不挑最快模型、不刪失敗列，
不靠repetition平均或平方和縮小systematic error。任何model invalid或unresolved，整組
規劃model判INSUFFICIENT-EVIDENCE，不事後選通過子集；即使全部pointwise pass，也只標
POINTWISE-ONLY-NO-DOMAIN-BOUND，不能ADOPT resource方案。

量測前已用frozen training coefficients確認：在三個held-out cells、CPU與wall各自
17個模型的10% acceptance intervals交集全為空。因此整組model_set_verdict必然
INSUFFICIENT-EVIDENCE，這不是等待新量測才決定的gate，也不是本輪ADOPT標準。
程式以absolute(<1 s)／relative(>=1 s)兩段interval交集檢查此事，只報existence booleans，
沒有新增held-out numerical prediction artifact。

事前指定stress_affine為primary predictive-adequacy diagnostic；16個power forms全部
作scenario sensitivity／coverage報告。逐模型invalid／unresolved／pointwise pass及刪失
下界仍有用途，但不得看到結果後選贏家、refit或以primary pass關閉item7。
舊training為single-process CPU0，沒有新supervisor wakeups；本輪獨立CPU1 supervisor
也不是相同orchestration。CPU與wall residual均標cross-profile diagnostic；尤其wall
invalid不得單獨歸因於模型形式，須保留host/scheduler/instrumentation的差異，無paired
training remeasurement，不能作like-for-like wall qualification或放大為domain verdict。

Framework「維持現行caps」仍需要 production-domain validated U_wall×1.25≤900、
U_CPU×1.25≤57600、完整error/overhead與memory資格化。REJECT中的必要成本lower
bound也必須來自production domain，不能來自zero-tolerance stress或diagnostic probe。
Production-E4-WALL-CENSORED由evaluate-only900 s timer產生，是該固定fixture／host的
該fixture／host上evaluate-only超過900秒的timeout witness；若只是whole-child1020 s含setup超時，E4自身是否超900仍未知。任何ADOPT/REJECT不得偷換這兩種scope。

## 7. 下一步

本 manifest／harness exact-head review通過後先merge，另處理external execution receipt；
目前authorization=NONE。新結果另開evidence PR，附139項完整結果／not-run、accounting、
model checks與source/environment pins。若需要policy amendment，依framework重審，
不得看到結果後延長預算、改fixture或放寬門檻。Item7仍AMENDMENT-REVIEW-PENDING、
items3–5 REVALIDATION-PENDING、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE。
完整resource qualification／下游revalidation／independent review之後，另開state-only
closeout；沒有新namespace、scientific authorization或候選K。

## 8. Harness 修訂與驗證範圍

v0.2修訂對應獨立review的六點；c4e3b754受審版本不予合併。
CPU inherited hard／全額wall admission／plan分類為blocking fixes；supervisor預算、
E4 timer scope、censor lower bounds與model用途均在freeze前更正。

真實Linux end-to-end tests在獨立interpreter用test-only stub manifest與短sleep／busy
workers，走過setrlimit繼承、SIGXCPU、scoped SIGALRM、unknown SIGALRM abort、
supervisor kill/reap、parent CPU停止、NOT-RUN與完整wall admission。另驗parent-death
kernel guard及/proc PID/start identity。Stub不呼叫numeric producer，resource限額只改
可拋棄的test subprocess；測試輸出不當research probes或資源資格化evidence。
Fixtures、solver reference、analysis、production caps與原evidence均未改動。


v0.3依第二輪review補A/B/C：production child CPU1100；supervisor SIGXCPU改flag+SIG_IGN，
不異步拋例外；production timeout統一用evaluate-only900秒timeout witness措辭。
新增real SIGXCPU注入launch、write/fsync及final-summary的stub regressions；仍未執行研究probes。
