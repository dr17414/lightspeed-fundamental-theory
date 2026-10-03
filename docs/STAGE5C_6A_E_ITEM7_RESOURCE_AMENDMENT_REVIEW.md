# Item 7 resource amendment — decision-rule review draft

狀態：`REVIEW-DRAFT / NON-EXECUTABLE`；`authorization=NONE`。
本文件提出新量測之前的判準，尚未選定資源政策，也尚未完成 measurement preregistration。
只有本文件的 exact-head independent review，以及另附完整 measurement manifest 的
freeze／review 完成後，才可進行該 manifest 所列的新 deterministic resource probes。
文件合併本身不授權 probe、screen 或 namespace。

## 1. 基線、證據與承重範圍

- Main：`d2c665ad78bbd2d3dd12360e934307d67ed979f7`；tree
  `971a521fbc18128295878925babf46d38c279868`。PR #59 的 implementation draft
  已依 exact-head GO 合併，resource qualification／item-7 closeout 尚未完成。
- PR #60 仍為未合併、未取得 exact-head GO 的 draft；引用 head
  `447dda42b1bf7f7459dd2401e79d3a6ad7b1f366`、tree
  `fb38b9659c3d81521b9878e1a6d682a1e9186524` 中的 development evidence。
  [證據 JSON](https://github.com/dr17414/lightspeed-fundamental-theory/blob/447dda42b1bf7f7459dd2401e79d3a6ad7b1f366/docs/stage5c_e4_v02_resource_characterization.json)
  與同一 head 的 characterization 文件／harness 是來源；引用不代表該 PR 已通過複核。
  Evidence JSON blob：`54b69083db971661b38196a5de65a1ec9b3c0e41`。
  #60 的文字整理 head `660122d98be37e3784c93236dfb96d61f0ade38b`、tree
  `3b515d5da12539589e3c084403167500211e7b79` 保留該 evidence blob、harness 與全部
  analysis blobs。本 PR 疊在這個 #60 head 上；兩者仍待獨立 exact-head GO。
- 既有 candidate、producer、runner、caps、historical custody／attestation／burn registry
  不變。原 caps：4096 subdivisions、900 s per-E4 wall、57600 s schedule CPU、32 GiB
  address space；約 7 GB target-host physical memory 另須 preflight。
- 本輪只整理上述既有資料與提出規則，沒有新計時、generator、seed、arm ledger、
  scientific endpoint 或候選 K。Item 7 `AMENDMENT-REVIEW-PENDING`；items 3–5
  `CLOSED-v0.1 / REVALIDATION-PENDING`；item 8 `OPEN`；6a-E
  `PREREGISTRATION-INCOMPLETE`。

### 1.1 Stress 是目前資源疑慮的主體

全部十個既有 probes 如下。它們都已被看過，model candidates 是看過這些結果後才提出；
這是 development／training 資料，不能改稱 held-out 或事前模型的獨立驗證。

| Phase | Atoms a | Subdivisions s | CPU s | Wall s |
|---|---:|---:|---:|---:|
| enclosure | 2016 | — | 35.213259238 | 35.234957806 |
| enclosure | 4560 | — | 77.549257706 | 77.571420577 |
| enclosure | 8128 | — | 138.697154385 | 138.712722553 |
| stress | 252 | 4096 | 56.796317550 | 56.803138072 |
| stress | 1008 | 4096 | 200.459355604 | 200.473943827 |
| stress | 2016 | 256 | 24.401296493 | 24.405588543 |
| stress | 4560 | 256 | 54.423398554 | 54.426502489 |
| stress | 8128 | 256 | 94.351012622 | 94.359243006 |
| stress | 8128 | 512 | 190.332595884 | 190.347226212 |
| stress | 1008 | 256 | 12.670941483 | 12.674727478 |

兩個單次 s=4096 probes 最貼近 subdivision cap，但 a 仍僅為 252／1008。
1008 atoms 的 4096/256 CPU ratio 約 15.820（名義為 16），8128 atoms 的
512/256 ratio 約 2.017（名義為 2）；s=256 的每 atom CPU 約從 12.57 ms
降至 11.61 ms。正截距、sublinear／superlinear 訊號尚不能區分，正是並列模型的理由。
要研究的 stress 目標是**單次** (a,s)=(8128,4096)，不是疊加短 calls。

8128 atoms 的 enclosure 是實測 `138.697154385` CPU s；stress 是實測
`94.351012622` CPU s at 256 subdivisions、`190.332595884` CPU s at 512。
以下乘法是外推，並未實際執行 16 或 8 次完整呼叫：

| Illustrative composition | Extrapolated stress CPU s | Enclosure + stress CPU s |
|---|---:|---:|
| 16 × measured 256 | 1509.616201952 | 1648.313356337 |
| 8 × measured 512 | 1522.660767072 | 1661.357921457 |

兩者 nominal subdivision 總數皆為 4096；每 subdivision 約 0.36856／0.37174 CPU s，
差約 0.86%。13.045 s 的 subtotal 差異只反映兩種線性外推的不同，並非 confidence
interval、model-error bound 或 enclosure 差異。沒有擬合過 exponent，也沒有已驗證殘差界。
近似線性／輕微超線性只是待檢驗假設；不得把乘法誤認為已觀察的 repeated-call 結果。

Enclosure 佔這兩個 illustrative subtotals 約 8.4%。若用這個 phase decomposition
討論 900 s，stress 留下的餘額為 `761.302845615` s，約須減半；fixed-GL、adapter、
certification 等尚未納入的成本會再減少餘額。這是單執行緒 CPU≈wall 環境的規劃算術，
不是 production timeout 證明或可承重的 wall 上界。Zero-tolerance stress 也不是
candidate tolerance，其 mixture 不宣稱是真實 selector output。

完整 schedule 的 CPU cap 也可能先成為限制：57600/264≈218.18 s per call，且其中
尚須留 generation／selector 等非 E4 成本。若只作規劃算術，把 selected-count upper
352896 全部放在 s=4096，按實測 (8128,256) 的 stress per-atom/per-subdivision
係數與 (8128) enclosure per-atom 係數縮放，stress 約 65543.49 CPU s、enclosure
約 6021.86 CPU s，phase subtotal 約 71565.35 CPU s。這不是 schedule 上界或 joint
profile 可達性證明，只提醒提高預算須同時處理 wall 與 total CPU。平行化不會自動
解除 CPU cap；也不把 CPU_parallel/CPU_single≥1 當定理，實際 ratio 與完整總 CPU
都須獨立證成。

### 1.2 Enclosure 與計數的適用域

Enclosure 在 2016／4560／8128 atoms 的實測 CPU 分別為
35.213259238／77.549257706／138.697154385 s，平均約 17.5／17.0／17.1 ms per atom，
相鄰區段斜率約 16.6／17.2 ms per atom。三點不能區分 affine 與輕微超線性模型。
N≤128、unordered selected pairs 的結構上界是 8128；在 count 軸的最大值已有
enclosure 實測，不需向更大 count 外推。但同一 count 的其他 mixture／host 仍未被界住，
8128 這個樣本不是 enclosure 全域成本上界。若 future domain 超出 N=128，須另案 review。

396 列是 3 N ×12 fixed geometries ×11 members 的 categorical count inventory，
不是 target-law distribution 或 396 次成本觀察。單次 E4 的直接尺度是 selected atom
count a、subdivisions s、mixture structure g；selector 呼叫數在 schedule 層承重。
8128 atoms 對應 N=128 chain 的 all_relations 選取數，不能推論它同時到達 production cap。

## 2. 兩層模型與誤差傳遞義務

以下形式事前列為候選比較組；不得看過新結果才增加形式並挑較樂觀者。
「事前」只相對於後續新量測；不倒稱它們先於 §1.1 的 training 資料。
CPU、wall 分開擬合／診斷；RSS 不由計時模型推出。

### 2.1 Per-call layer

分解 `T_call = T_setup + T_enclosure + T_stress + T_other`，每 phase 明列區間。
Proposal §5 的正式 E4 timing 必須包含完整 E4，不能只以 stress subtotal 替代。
候選形式：

- Enclosure：`E(a,g) = e0(g) + e1(g)*a`；與 sensitivity 形式
  `e0(g) + k(g)*a^p` 並列。截距與 count-growth 分開，不預設 enclosure 為固定成本。
- Stress 主形式：`S(a,s,g) = b0(g) + b1(g)*a + b2(g)*s + b3(g)*a*s`。
  它容許每次呼叫的固定成本及 per-atom／per-subdivision 成本。
- Stress sensitivity：`S(a,s,g) = h0(g) + k(g)*a^p*s^q`。
  mixture strata 在 manifest 中固定；不以只量過的一個 mixture 推出所有 g 的界。

固定擬合方式：對現有固定 cyclic recipe 的七列 completed stress training rows，以全部
七列、等權 absolute-second squared loss 作 nonnegative least squares；主形式的
四個 b 係數非負。Sensitivity 在每個固定 (p,q) 上以相同七列、同一 loss／非負
約束擬合 h0、k。CPU／wall 各擬合一套，不以每-atom normalization 改變權重。
Enclosure 用全部三列、相同等權 loss，e0/e1 或 e0/k 非負。新的 mixture g 在
manifest 先固定 training／validation 分割；不能混用 g 或用未見 g 的零 residual。
此處只指定方法，未執行新擬合或新量測。Rank deficiency／nonunique solution 要
報 `NOT-IDENTIFIED`；solver、tolerance、tie rule 在 manifest 釘選，未定前不執行。
此 recipe 在不同 a 下的 uniform weights／末尾 atoms 按 exact payload 固定，不宣稱
所有 a 都有逐位元相同的 normalized mixture；此差異也屬模型適用範圍。

另列可直接重算的 **zero-intercept anchored scenarios**：
`S_anchor(a,s;p,q)=94.351012622*(a/8128)^p*(s/256)^q`，以實測
(8128,256) CPU 為唯一錨點；h0=0，不以其餘 rows 擬合 k。
這與上述 fitted-offset family 分開，兩者不得互換。

| q（a=8128、s=4096） | Anchored stress CPU s |
|---:|---:|
| 0.9 | 1144.075 |
| 1.0 | 1509.616 |
| 1.1 | 1991.951 |
| 1.25 | 3019.232 |

在此錨定 grid 中 stress 單項都超過 900 s，p 因 a=8128 抵消；但這仍不是
offset models 或 production runtime 的界。決定性缺口之一是 production tolerance
下 registered domain 的實際 subdivision 可達性。Manifest 必須包含真實
selector→adapter→v0.2 producer 的 deterministic reachability probes，記錄 selected
count、實際 subdivisions、status/reason 與 timing/censoring；不使用 zero tolerance
替代 producer，也不執行 screen／generator／seed。固定 fixtures 能給 pointwise
reachability witness，不能以「沒有撞 cap」證全部 domain 不可達；exclusion 仍須
validated domain bound。Count 與 subdivision 的共同限制須一併證成。

必須公布 coefficients、全部逐點 residual（CPU／wall 秒與相對值）、最大正 residual、
held-out count／subdivision／mixture residual，以及 timeout 的 right-censored observations。
不能將 timeout 刪除、當成 exact runtime 或視為已完成的低成本樣本。
資料不足以識別 exponent／截距時明列 `NOT-IDENTIFIED`，不能報虛假的窄區間。

固定總細分數、改變單次 subdivision budget 的比較列為新 manifest 的必要設計：
例如 a=8128、s∈{128,256,512,1024}，每種 cycle nominal total=4096，
且每個 invocation 都有獨立 deadline。須分列 fresh-process/import、setup、stress 與
cycle total，才能判斷單次 s 增加是否使 unit cost 上升。這不是 production 分割方案；
重啟 cubature 改變 partition／convergence，不能以 repeated integrals 拼出合格 report。
具體 repetitions、順序、停止規則及總資源預算仍須在 manifest freeze，現在不得執行。

Manifest 也必須列一次 a=8128、s=4096 的直接單次 diagnostic stress probe（相同
固定 mixture、zero tolerances、workers=1；只測成本）。供審查的初始計畫為一個
attempt、4500 s diagnostic wall／5000 s process CPU，以容納上述 3019 s scenario
再加 25% planning margin；這不是 runtime bound 或必然不 censored 的保證。
若 preflight 不能負擔，manifest freeze 前拒絕或修訂整個計畫；timeout 後不延長重跑。
必須用另行受審的 diagnostic harness 明文設定自己的 caps，禁止改 production globals，
production 900／57600 caps 完全不動。直接 probe 也不等於 production exhaustion witness。

Sensitivity 必須至少顯示 p,q∈{0.9,1.0,1.1,1.25} 的事前指定 scenarios，以及
data-supported exponent set（若可識別）在 (a,s)=(8128,4096) 導出的時間範圍。
scenario grid 不是 exponent 的上下界；若資料不能限制更高 exponent，qualification
記為證據不足。附上模型間的範圍，而不是只保留最佳 residual 的單一形式。
Empirical residual、repetition scatter、sensitivity range 都不能自行升格為 validated
production bound；需要另證 input-domain coverage 與 bound 的方法。

### 2.2 Schedule layer

對每個 registered case/member 記錄 `(N, member, a, s, g)`，以
`C_schedule = C_nonE4 + sum_j C_call,j` 組成 CPU 模型；selector／generation／adapter／
burn 與其餘 runtime 成本依實際呼叫關係計入，禁止 double-count 或省略。
正式 CPU 區間與 runner 的起點一致，採 `time.process_time()`。

若使用 subprocess，父程序 process_time 不包含 child CPU；任何此類方案必須先
amend runtime accounting，明訂總 CPU、child cleanup 及 cap 的同一定義，不能拿
子程序 wall 或 parent-only CPU 冒充原 contract。

保留同一 case 各 selectors 的 joint count 約束。令 B_b 為 depth bands，I_m 為
open-interval cardinality=m 的 relations；`sum_b |B_b|=|D|`，但
`sum_{m=0..4}|I_m|≤|D|` 一般不取等號。實際十一 calls 的總和
`A=2|D|+sum_{m=0..4}|I_m|`，而上界為
`A≤|D|+|D|+sum_b|B_b|=3|D|`；第二個 |D| 是 links/I_0 與 interval_exact/I_1..I_4
互斥聯集的上界。36 個 inventory cases 實際總和 248315，逐 case 的 identity／bound
均成立。登記 264 calls=3 N×2 targets×4 reps×11，count upper
`8×3×(2016+4560+8128)=352896`，
只界住 counts，沒有界住 s、g 或 CPU。不能把十一個各自 fixture maxima 當同時可達，
也不能把這個 count bound 乘上一個典型 per-atom cost 當 qualification。

若 validated per-call error allowance 為 delta_j，schedule allowance 至少採
`delta_nonE4 + sum_j delta_j`；共同 host／mixture／model 偏差也須保留。
沒有獨立性證明時禁止以平方和開根號縮小誤差。公布 complete deterministic development
schedule 的逐列 residual、總 residual 與未涵蓋項；它不是 scientific one-shot screen。
無可承重的 delta／domain coverage 時，schedule model 只能作規劃，判為證據不足。

## 3. 共通判定規則（待 exact-head review）

以下 decision labels 是資源方案判定，不是 Gate A/B 或 scientific verdict。
先檢查 REJECT，再檢查 ADOPT；其餘一律 `INSUFFICIENT-EVIDENCE`，不能預設採納。

- **REJECT**：發現該方案違反 frozen numerical／seal／custody contract，或有效的
  production-domain witness 在所提 caps 下超限；若方案正式更改 contract，則以其
  已 review 的 replacement contract 判斷。Stress-only 超時只能否定該 stress 計畫
  的可負擔性，不能當 production witness。
- **ADOPT**：方案的 contract、identity、source/env pins 已受審，exact implementation
  及 downstream revalidation 通過，完整域有 validated wall／CPU／memory bounds，
  並通過 target-host preflight。ADOPT 只允許資源方案進下一步，不等於 item-7 CLOSED。
- **INSUFFICIENT-EVIDENCE**：只有 fixture measurements／extrapolation、無 uniform 或
  validated domain bound、缺 host／thread 對應、censored run 未處理、model 不可識別，
  或一項 bound 跨越判定門檻。新增量測需新 manifest，不事後縮 domain、刪 strata 或換模型。

規劃用 safety multiplier 提案固定為 1.25；平行化 CPU inflation limit 提案為 1.10。
這兩個值是待審的政策選擇，不是資料估計、coverage probability 或誤差界；本草案
未宣稱它們已 freeze。若 review 改值，須在新量測之前改 exact head 並記錄理由。
25% margin 必須作用於已含 validated model/domain error 的上界，不能替代那個上界。

## 4. 各選項的採納／拒絕／證據不足

| 選項 | ADOPT 的額外必要條件 | REJECT | INSUFFICIENT-EVIDENCE |
|---|---|---|---|
| 維持現行 caps | 完整 domain 的 validated U_wall×1.25≤900、U_CPU×1.25≤57600，含全部 model/domain error 與 overhead；4096 subdivision contract、memory 及 target-host preflight 均通過 | 有有效 production-domain 超限 witness，或已證必要成本使該方案不能符合含 margin 的門檻 | 只有短 calls、training fits 或 reachability probes 沒撞 cap；validated upper 跨門檻不等於已證超時 |
| 提高 wall／CPU 預算 | 以 validated U_wall、U_CPU 及完整 error allowance 定案；新 wall cap ≥1.25 U_wall，新 total CPU cap ≥1.25 U_CPU；先確認 target-host 可負擔性、scheduler limits、memory 與 timeout cleanup，正式 amendment 舊 caps | 已受審的新預算仍無法容納有效 witness，或所需 budget 超出明訂 host/scheduler 限制 | 只有 1661 s 外推、無 model-error upper，或可負擔性未證；不得直接定成 1661×1.25 |
| 切分工作量 | 說清是 scheduling/chunking 或新積分演算法；總 CPU／overhead 全計，report/enclosure/certification/seals 有等價性證明或新版 contract 與重驗；每個原 logical E4 的 wall 起點/截止仍按 contract | 重設 deadline 逃避原 per-call cap、忽略跨 chunk CPU、部分 estimate 冒充完整 report | 只有小 chunk 快，無重組誤差與總成本界；restart subdivisions 的 stress cycle 不證演算法等價 |
| 經驗證平行化 | 相同 inputs/source 上的事前配對比較；validated wall 與 schedule CPU 都在 approved caps；CPU inflation ratio 的 validated upper ≤1.10；thread/worker/affinity/pools 及 peak memory 全 pin | production-domain 實測 CPU ratio >1.10，或 wall 雖過而 total CPU／memory 超 cap；本提案明訂拒絕此種 CPU tradeoff | ratio 上界跨 1.10、baseline 不配對、只見 wall speedup、無 thread/pool 或 CPU 子程序計量 |
| 修改 qualification 判準 | 事前寫清替代哪條 §5、domain、失敗事件及何種證明承重；若以 timeout NONCLEAN 替代完成保證，須有 typed reason／nullable schema／cleanup／real-seam 與 failure-bucket accounting，並重審 item-8 tail／power 義務 | 把 timeout 後 partial result 當 CLEAN、漏記 failure、把已 burned namespace 重跑，或宣稱平均成本即可證所有 calls | runner 可存活但 failure tail／matching-conditioned law 未證；fixture 成功率不承重 |
| 限制 atom/count 或降低 compute budget | 明訂 eligibility、十一 members／strata coverage、cap-exhaustion reason、新 identities；selector、failure tails、下游 seals／law／power 全重新 preregister／review | 看到結果後刪昂貴 strata／選取 rows、無 amendment 就改 count/subdivision cap | 單純成本下降，未證改動後的 selection／failure／numerical／power 合約 |

平行化比值定義為完整同任務 `CPU_parallel / CPU_single`，包括 orchestration／setup；
正式 schedule 比值另列，兩者都須符合 1.10。CPU_single 有不確定性時採保守 ratio
上界，不能用平均值掩蓋 inflation。若希望接受更高 CPU 以換 wall，須在量測前另訂
amendment；不能看到結果後改採納規則。不同 host 或 source 不構成有效 paired baseline。

### 4.1 組合選項與判定順序

Selected option(s) 只指事前列齊的方案 package；不得看完結果才混搭最有利子項。
每個 package 須指定 exact contract／caps、同源同任務 baseline，以及組合 interaction
的重新資格化。順序固定為：(1) custody/numerical/eligibility 與 CPU accounting，
(2) 平行化 ratio gate，(3) package 的 wall／total CPU／memory budget gates，
(4) failure-law／downstream obligations，最後才檢查全域 ADOPT。
任何一項 REJECT 即整個 package REJECT；無 REJECT 但有 unresolved 項即證據不足。
「平行化＋提高預算」也先檢查 1.10 ratio；新 CPU cap 再高都不能蓋掉 ratio 超限。
以 validated upper 加 margin 檢查 approved caps；任何放寬都必須先寫成正式 amendment。
U_wall/U_CPU 是 bounds，不是 point estimates；upper 過大但沒有 violation witness 時
不得直接宣稱 production 失敗，判證據不足。

## 5. 新量測前必須完成的 manifest

這份 framework 不取代 executable measurement protocol。新 PR 必須列齊：

1. Selected option(s)、fixed comparison order、input domain／mixture strata、全部 fixtures
   的 exact bytes、counts／s-grid、repetitions、paired baseline 與 held-out plan；無 RNG／seed。
   全部十個舊 probes 是 training；new held-out bytes／count/subdivision／mixture cells
   在量測前固定，不以其結果 refit/pick models。須包含 production-tolerance reachability
   與單次 (8128,4096) diagnostic probe，分列用途／caps，不以短-call cycles 取代後者。
2. 精確 source/dependency/host/cgroup pins、六個 thread env、workers、CPU affinity、
   實際 runtime threadpools；single-thread baseline 與擬議 production environment 各自固定。
   Characterization host 是 cgroup 8 CPU／8 GiB、affinity=1 CPU，target 約 7 GB，兩者
   不等同。8128 enclosure 的單 process peak RSS 467124224 bytes 是觀察，不是 worker
   memory bound。Parallel manifest 必須 pin resident worker count、同時存活的 phase、
   parent/child aggregate peak、共享頁面計量及 host/cgroup available-memory margin；不能
   只用單 worker RSS 或 32 GiB address-space cap 保證 target 可負擔。
3. Wall 用 monotonic clock；CPU 用與 runtime cap 相同的定義；per-phase 與全區間
   起止、imports／setup、子程序 accounting、RSS／available-memory 記錄及 cleanup。
4. 每 probe／cycle／整個 plan 的 wall、CPU、memory caps；固定 timeout/censor/abort
   與 checkpoint 規則。不允許昂貴 run 失敗後自行加預算、換 fixture 或多跑一次。
5. Model forms／fits、residual outputs、sensitivity grid、validated-bound 方法、coverage
   與 error propagation；所有 unresolved cells 維持 evidence-insufficient。
6. §3–4 的值與 decision rule 經 exact-head independent review 後 freeze；如任何值未定，
   不進行依賴該值的量測。Resource probes 不執行 `run_screen` 或 burn namespace。

單執行緒觀察不得自動換算成 production 平行效率；production env 若不同，要實測並
證成兩種計量。Full qualification 只用 exact reviewed implementation，在 approved
domain/env/caps 上完成；不得把 stress harness report 當 production E4 report。

## 6. 後續狀態順序

PR #60／#61 均保留 draft。本 PR 的 base 是 #60 的 branch，合併順序明訂為 #60
取得新 exact-head GO 後先合併；核對其 merge tree，再將 #61 retarget main，必要時
解衝突並重新 exact-head review／CI，之後才可合併 #61。STATUS 保留 v2.02→v2.03，
不遺失任一記錄；#61 不先併入 main，也不代為放行 #60 head。Stacked #61 的 tree
包含 #60 檔案，但相對 base 的修改仍只有 review 文件與 STATUS。
先 review 判準與 measurement manifest，再做被授權的 deterministic probes；依事前
規則選定／拒絕方案，正式 amend contract，另開 implementation／qualification evidence PR。
完成 item 7 resource qualification、items 3–5 revalidation 與 independent exact-head
review 後，另開 state-only closeout 決定狀態。PR #59 不需重開，也不因已合併而免除 closeout。
新 screen protocol／namespace／authorization 在這之後仍須另行 preregister／review。
任何未完成步驟均保留現有 gates；原 burned namespace 永久不可回收。
