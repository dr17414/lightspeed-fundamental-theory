# Stage 5C / 6a-E — items 7／8 可行性與決策草稿

**DESIGN-DRAFT／PROOF-FEASIBILITY-UNRESOLVED／authorization=NONE。**
日期：2026-10-10（台北）。本草稿依操作者與獨立複核者同意的設計工作範圍，
整理目前證據、承重義務及三條研究路線；不替任何 closure item 改狀態。
本輪只交文件：不跑新量測、不呼叫 generator／E4 producer、不產生或配置 seed、
不開主機、不設計候選 kernel K、不開啟 scientific arm ledger 或計算 arm endpoint。
既有結果 JSON 的讀取、描述性算術與文件完整性檢查不構成新研究樣本。
PR 的既有 CI 回歸亦不是新 campaign 或 scientific execution 授權。

**主要發現：§3.4 的 O19 定位到 C8 diagonal endpoint 與 zero-marginal-variance
region gate 的結構不相容；應先獨立複核統計接縫修訂，暫保留 v0.2 數值 producer，
再決定後續證明／資源資格化。** 這是具名設計 blocker，不是原研究問題的整體 no-go。

## 1. 基線、範圍與判斷語義

基線為 PR #67 合併後的 main：

- commit：`6941b97b8ea04700b094876f01a3512946788a6c`；
- tree：`0b757fdc2bd3e8670e1309f364fc9b909604ce25`；
- run 1 原包 SHA-256：`8c26b6574ce12956474779434f24ad54e940584dbf3ecc43c9c582fd792b06bf`；
- assessment SHA-256：`7dd51e7e54f1306a1f2a439f8440caf3e220ce216a33ca4c2d9f20aee5ad2326`。

PR #67 的資源結果記錄已合併、該量測回合已結案；這不是 item 7 closeout。
依 [prereg §8](STAGE5C_6A_E_PREREGISTRATION_DRAFT.md#8-freeze-closure-matrix)，
item 7 仍 `AMENDMENT-REVIEW-PENDING`，items 3–5 仍
`CLOSED-v0.1 / REVALIDATION-PENDING`，item 8 仍 `OPEN`；items 9／10／12
仍 `OPEN`、11 仍 `DRAFT`，6a-E 仍 `PREREGISTRATION-INCOMPLETE`。
歷史文件中的 v0.1 CLOSED 敘述須依此版本化狀態解讀。

判斷採以下四類，不能只用缺少上界就填「不可行」：

| 標記 | 在本草稿中的意思 | 可支持的後續 |
| :--- | :--- | :--- |
| `ESTABLISHED-PARTIAL` | 已有具名解析／結構證據，但只覆蓋指定子義務 | 可重用該子義務，不代表整個 gate 關閉 |
| `OPEN-METHOD-IDENTIFIED` | repo 已有化約或充分條件，尚缺承重上界／前提 | 可推進證明，不預測一定證得出來 |
| `OPEN-NO-BOUND` | 尚無可支持正面資格化的界 | 不填 cap、cohort floor 或 ADOPT |
| `REJECTED-SPECIFIC-SHORTCUT` | 反例／sharpness 已排除特定論證 | 只排除該論證，不擴張成整個 v0.2 或研究問題的 no-go |

表中的「可用方法」都是待審證明計畫；列出方法不是完成證明。
若須改 support、selector、matching、統計 reference 或宣稱範圍，即使不用改 E4，
也屬 protocol amendment，不能在本草稿內默改。

## 2. 證據索引與適用版本

| ID | repo 內 source-of-record | 在本評估中承重的內容／限制 |
| :--- | :--- | :--- |
| P | [prereg draft](STAGE5C_6A_E_PREREGISTRATION_DRAFT.md)，§0／§1／§8 | 完整 closure、禁止 numerical access、未固定的 6a-E N／streams／power floors |
| A | [E5 budget／power audit](STAGE5C_6A_E_E5_BUDGET_POWER_AUDIT.md)，§1–§3.3 | 七個 regions、名目 spending、Gate A/B、selector 化約、功效前提；早期 numerical witnesses 是 v0.1，不能直接當 v0.2 failure witnesses |
| J | [joint matched law](STAGE5C_6A_E_JOINT_MATCHED_LAW.md)，§1–§5 | 真實 generator／calibration／matcher、matching failures、paired covariance；抽象 calibration 不是 E4 error law |
| S | [statistical regions](STAGE5C_6A_E_STATISTICAL_REGIONS.md)，§2–§6 | outward numerical propagation、E1 dead zone、E2／E3 strict component rules |
| V | [v0.2 proposal](STAGE5C_6A_E_ITEM7_AMENDMENT_PROPOSAL.md)，§2–§6；[implementation](STAGE5C_6A_E_ITEM7_V02_IMPLEMENTATION.md)，§1–§4 | 已知點位改善、in-sample levels 選擇、版本／seal／real-seam 回歸；不是均勻 cap 或 matched-law 證據 |
| Q | [resource amendment review](STAGE5C_6A_E_ITEM7_RESOURCE_AMENDMENT_REVIEW.md)，§1.2／§2–§4 | count／mixture／subdivision 共同限制、完整 schedule、誤差及 overhead、資源決策規則 |
| M | [measurement manifest](STAGE5C_6A_E_ITEM7_RESOURCE_MEASUREMENT_MANIFEST.md)，§1 及 qualification 規則 | run 1 是 development；39 fixtures 不涵蓋完整 probability／cost domain；禁止事後 refit、選模型或 ADOPT |
| R | [run 1 results](STAGE5C_6A_E_ITEM7_RESOURCE_RUN1_RESULTS.md)，§1–§6；[139-job JSON](stage5c_e4_v02_resource_run1_results.json) | 可核對的點位 execution／timing／RSS／outcomes；不能從 CLEAN 點位推 tail 或跨 host bound |
| Z | [typed pairing](STAGE5C_6A_E_TYPED_PAIRING.md)，§2；[primary invariant source](../analysis/stage5c_primary_invariant.py)，`unnormalised_components`；[real-seam regression](../tests/test_stage5c_e4_v02.py)，`test_actual_v02_rows_rebuild_item4_5_width_and_reject_v01_width` | 對角 continuum pairing 的 exact-zero 第二分量，與既有 region zero-marginal-variance gate 的相容性問題；詳§3.4 |

本草稿的連結均指向上述基線內容；新增文件不改寫 R 的 assessment、原始轉錄或判讀。

## 3. Item 8 義務矩陣

### 3.1 Claim family、統計 reference 與 Gate A

| ID／義務 | 已有證據 | 缺口與可行性判斷 | 可用證明方法（提案） | 是否需要改 E4 |
| :--- | :--- | :--- | :--- | :--- |
| O1 七個 regions、11 members、兩 splits、lineage／successor spending | A §1–§2 有 exact rational allocation；genesis 每 region 1/6160，successor 不回收／借用 | `ESTABLISHED-PARTIAL`：名目總額有界；尚未接入正式 manifest／ledger，也不是實際 finite-sample coverage 定理 | 依固定 claim／generation／split 核對不可回收帳，正式接線留 items 9–10；不得新增或刪除 claim 偷換 family | 此義務本身不需；E4 新版本須由 O17 重綁 |
| O2 matched／conditioned statistical reference 的有效性 | J 的 paired covariance 與 S 的固定 region forms；A §2 明列 unequal-attrition CR1 cluster-t 是 operational reference | `OPEN-NO-BOUND`：一般 finite-sample exact coverage 未證；抽象 calibration、名目 Bonferroni 不能補上它 | 在實際 matched／cap-conditioned law 下證 reference 所需條件及 coverage；若需替換 reference，另案 amendment，不能在此自動改用其他 test | 未知；可能是統計／matching 設計問題，改 E4 不保證解決 |
| O3 all_relations／links selector failure | A §3.3 的 antichain upper：最壞示例 N=64、theta=+0.4 小於 1.78e-80 | `ESTABLISHED-PARTIAL`：對此兩 selector 已有解析界；不是其他九 strata 或全部 Gate A | 對日後選定 N／theta 重新對應原解析式，與幾何／backend／certification 分桶，不能以成功 fixture 替代 | 不需改 E4；N／support 若變須重新核對 |
| O4 四個 interval_exact(1..4) empty-selection tails | A §3.3 化約為 permutation rectangle-occupancy avoidance；Hölder likelihood moments 固定六格 uniform targets 約 2.30e-9–1.56e-8 | `OPEN-METHOD-IDENTIFIED`：targets 不是 bounds；N=6 chamber counts 只驗證化約。套 antichain 單 chamber 界的捷徑已否定 | 證可驗證的 recurrence／enumeration／解析 avoidance upper，逐 m、N、theta 比對既有目標；若方法只給鬆界，保留未解，不宣稱 selector 不可行 | E4 無法修 selector empty；若需 selector／support amendment，屬路線 C |
| O5 五個 endpoint_depth_mass_band empty-selection tails | A §3.3：empty 必須有相鄰／boundary score-block mass 至少 2M/5；height-two order 與 N=6 counts 驗證不能保證每 band 非空 | `OPEN-METHOD-IDENTIFIED`：必要條件尚無 target-law concentration upper；band 分割不是逐 band 非空證明 | 對每 band 的 score-block event 證 uniform upper，再用固定 Hölder transfer；或直接證 target-law empty upper。必要條件的事件可能太大，需更細直接 empty-event 化約 | 不需靠 E4 解決；selector／support 改動另審 |
| O6 production schema、atom cap、box／causal leakage | A §3.3 的 R_geo：rho=gamma=1e-12，N=128 complement <=3.3024e-8；selector success 下結構 gates 確定通過；N<=128 count<=8128 | `ESTABLISHED-PARTIAL`：此部分可重用，V 保留 topology／leakage identities；不含 empty、adaptive 或 item-3。完整 iid support 的確定性全 CLEAN 捷徑有 positive-measure 反例，但反例不證 failure mass 超預算 | 保留既有 boundary／near-tie union bound、dyadic weight deficit 與分層事件；R_geo 是證明事件，不是新增 coordinate trimming；未來 N>128 要另處理實際 atom 超額 tail | 這個子義務不需；縮 margin／改 leakage/support 都須明文 amendment |
| O7 E4 backend：finite output、4096 subdivisions、zero／underflow、runtime／memory | V 有具名 fail-closed branches／reason priority；R 的78 production CLEAN。反事實 min-scale probe cap hit 不屬目前 max-scale policy | `OPEN-NO-BOUND`：實作拒跑正確不等於拒跑機率足夠小；無所有 production mixtures 的 adaptive／runtime bound | 在 selector success 且 R_geo 上分析有效尺度、積分誤差／細分停止及 finite arithmetic；逐 reason 控制剩餘 tail，與 §5 資源上界配對。operation bound 仍須 host/runtime 校準，不能直接等同秒數 | 未知；若證明必須改 levels／tolerance／caps，走路線 B；只見缺界不構成改版理由 |
| O8 item-3 strict nonzero norm／ratio certification | V 的真實新 rows／seal／certify regressions，舊 Gate-A witness 改善；A 的 norm-touch-zero witness 僅針對 v0.1 | `OPEN-NO-BOUND`：v0.2 target law 的 failure upper 未證；不得把舊 witness 原封不動當新版不可行證據 | 從實際 v0.2 enclosure 推 norm lower 與相對誤差界，分出接近零／不能認證事件並界其 mass；保留 item-3 strict gates 與 producer provenance | 未知；只有新版承重分析顯示必要時才改 E4；改 certification rule 屬更大 protocol amendment |

### 3.2 Gate B、matched law 與數值 cap

| ID／義務 | 已有證據 | 缺口與可行性判斷 | 可用證明方法（提案） | 是否需要改 E4 |
| :--- | :--- | :--- | :--- | :--- |
| O9 causal-boundary／cell-enclosure、near-zero 相對寬度的 producer-bound feasibility | V 三個單 atom witnesses 的 normalized errors 改善至 (0.00580,0.00696)、(0.00279,0.00335)、(0.01956,0.02347) | `OPEN-NO-BOUND`：levels 256 使用 wide-cell witness 選定，屬 in-sample；三點不是任意 mixture 的上界或 error mean，norm 小也不單獨決定相對 error | 從 v0.2 enclosure／denominator 的相依關係建立完整 mixture 的 error bound 或 law；分清絕對尺度與相對寬度，不以 atom 數代替 | 未知；不能僅因0.02347接近0.025就加密 levels，須先看聚合與統計 slack |
| O10 matching G、calibration failures、attrition 與 raw-to-matched 推前 | J 固定 feature／independent calibration／Hungarian／calipers／balance gates；A §3.2 完整推前映射 | `OPEN-METHOD-IDENTIFIED`：實際各 j、N、theta、L 的 Pr(G)、與 error 的 joint law 未證；同 raw target 不自動推出 CLEAN 條件下的所需均值／變異 | 對 calibration、匹配數／coverage／SMD／KS failures 分帳；證 feature／error／matched-index 的 joint law 及 null conditioning，保留 cross-arm blocks | E4 改版會改 error law；其餘多屬 matching／統計問題，不能假定改 E4 即足夠 |
| O11 normalized numerical cap、raw mean／top-M／matching-conditioned factor | A §3.3 全池 factor 8 在既有抽象條件下 sharp；factor2只是理想 benchmark；S 使用 outward numerical half-width | `OPEN-METHOD-IDENTIFIED`：無 per-coordinate mean/tail/cap；只用非負／subset 條件推出 factor<8 的捷徑已否定，未否定實際 matcher 可改善 | 先用 x_k=e_k/D_kk，分別證有限 CLEAN errors 的 mean／tail，再證 top-M amplification 或 feature-conditioned selection restriction；完整 Gate A 先成立。screen scalar max(x1,x2) 不可替代任何座標均值 | 未知；若在固定上界路線的必要條件上有承重反證，先比較更細 matched-law 方法，再考慮改 E4 |
| O12 cap-conditioned null law 與完整 split success | A §3.2 的 joint-event union bound 與 §3.3 全 raw-pool CLEAN gate；S 的strict open box | `OPEN-NO-BOUND`：Pr(matching、certification、cap 成功)及通過後 null law 未證；conditional CLEAN power 不能當無條件 power | 定義完整 success event C，直接控制其 joint probability 與 conditional moments／reference；不把 failures 換有限 error、丟棄 raw non-CLEAN rows或交給 matcher 避開 | 未知；若把 timeout／non-CLEAN 納入替代資格化，仍須同時重審 O2／O10／O12–O16 |

Gate A 是原始 pool 的逐列、連續、全部 CLEAN 要求；matching 是否選到失敗列無關。
Gate B 才處理成功條件下有限誤差的大小。平均 error 很小不能彌補 Gate A。
在歷史 L=768、m_min=192 的示例，factor8／2 對應零 statistical-width
極限下 per-arm mean <1/160／1/40；這些是特定充分界路線的必要條件，
不是通用 E4 cap，也不是任何 matching 機制的必要條件。
pair addition、cohort aggregation、兩臂與 D=diag(3,1) normalization
須按 S 的向外 rounding 全部保留；不得混用 raw 與 normalized 單位。

### 3.3 效果模型、整體功效與下游影響

| ID／義務 | 已有證據 | 缺口與可行性判斷 | 可用證明方法（提案） | 是否需要改 E4 |
| :--- | :--- | :--- | :--- | :--- |
| O13 E1 positive-gap model | S 固定 normalized closed dead zone 1/20；A §3 有邊界 effect 無法達0.90的特定反例 | `OPEN-NO-BOUND`：所有需承重位置的事前方向／座標與正 gap 未證；此反例不證實際 target effect 恰在邊界 | 從允許的 candidate-independent evaluator／target law 提出且證明 effect model；逐 claim說清保證方向／gap，不能讀6a-S或6a-E arm data、挑選觀察較大座標或設計K補 gap | 改 E4只縮數值不確定性，不創造真實效果；缺 effect 不等同需要改 E4 |
| O14 E2兩個 target-null claims | S 固定同pipeline、同theta、fresh兩臂及兩座標等效 margin1/20；A §3有 power充分式 | `OPEN-NO-BOUND`：各 target 的 CLEAN／matching／cap-conditioned null mean、variance／distribution與 eta<margin未證 | 在 O2／O10–O12 下證兩個 null laws，保留同region兩座標共同成功；若採條件 Hoeffding 路線，另證 independent cohorts、給定 matched counts 的共同條件平均 | 未知；E4可能影響 eta，不能解決所有 conditional-law 前提 |
| O15 E3四個 regions的有限cohort directional／equivalence效果 | S／item6固定 chiral、diffusion、wrong-support、sector-blind-null；continuum planted magnitude／g_* 有解析證據 | `OPEN-NO-BOUND`：continuum separation 不自動等於 finite-N matched-cohort gap；每個directional與equivalence分量的效果／null law未證 | 分別橋接 finite-N、selector／matching／conditioning；逐分量證 gap與variance。coord1 raw±1/10、g_*/2須除D_11=3；coord2依原規則。global sector swap 是bitwise gate，勿加 statistical alpha | 未知；E4只處理數值部分，不能替代 finite-cohort effect model |
| O16 完整功效、selection／confirmation／successor cohort floors與可負擔性 | A §3的條件充分式；B>=32僅結構floor；A §3.2–§3.3列完整success與罕見failure成本 | `OPEN-METHOD-IDENTIFIED`：未有可承重eta、gap、共同條件均值、success概率與完整資源配置，故不能填B整數或宣布>=0.90 | 對每個需要功效的claim和generation分別證 C及Pr(PASS\|C)，由Pr(C)*Pr(PASS\|C)給保守無條件下界；含matching、numerical、statistical失敗與真正總成本。名目alpha帳與failure／power帳分開 | 改E4／reference／support任一項都可能重算；不能預設多加cohorts即可解決 |
| O17 v0.2的items3–5重驗與closeout依賴 | V implementation有完整payload diff、nullable／reason、newsource rows／seals、真實下游regions與strict-boundary regressions | `ESTABLISHED-PARTIAL`：component coverage已存在；尚無正式v0.2closeout，不能把歷史v0.1 rows／width／seals沿用 | 以確定的E4版本逐項核對已有real-seam與mutation證據、獨立review、CI及state-only closeout。若再改E4，所有相關payload／identities／numerical propagation重審 | 保留v0.2可重用已交component證據但須closeout；新改版一定重審 |
| O18 任何未來diagnostic estimation的合法性 | A §3.2.1及§3.3已有rare-tail／mean／factor協定清單；既有screen與burn紀錄存在 | `OPEN-METHOD-IDENTIFIED`：本草稿未定新replications、cap、seed provenance或confidence allocation，也不授權沿用已burn streams | 僅若純分析評估顯示需要，另立manifest，事前固定j/N/theta/L/H、統計量、simultaneous uncertainty、stop／fail-closed、資源及隔離，再獨立review／merge後執行 | 不必然；diagnostic manifest不是E4 amendment，也不能用pilot挑cap |

O15 的四個 regions必須逐一覆蓋：chiral對sector-blind的directional＋equivalence，
diffusion對sector-blind的兩個directional，correct對wrong-support的directional＋equivalence，
sector-blind-null兩座標equivalence。不能因「有g_*」跳過其他三列。
O16 不把七個regions的所有PASS自動當同一個0.90事件；每項／每operation的功效目標
與整體stage成功定義須明列，若要joint成功率另分配其failure額度。

### 3.4 O19：exact-zero 分量與 region 前置條件的相容性

這是新增的設計評估結論，來自基線內已有公式、source 與 regression，**沒有執行
新的 endpoint 計算或 scientific input**。它比「先量更多資源」更早成為前置問題。

| 義務 | 已有證據 | 缺口／判斷 | 可用方法（設計提案） | E4 影響 |
| :--- | :--- | :--- | :--- | :--- |
| O19 正式 E1／E2 的 producer 能進入固定 region 的結構域 | Z 的 diagonal propagation representation；P §2 的 pairing→primary→joint-law 路徑；S §1 及真實接縫明記拒絕零 marginal variance | `REJECTED-SPECIFIC-SHORTCUT`：把目前 diagonal C8 endpoint 直接接到未修改的 region builder，不能形成 CLEAN region；這不是從缺界推不可行，而是下面的 exact 結構推導 | 先獨立核對正式 pipeline 身分。若沿 P §2，需另提對事前可證 exact／deterministic 分量的統計 reference／region 協定；若主張正式 arms 另有非 diagonal producer，須具名修改／釐清 source-of-record 並證 real-seam，不能用抽象 oracle 代替 | 加密 levels／收緊 tolerance 不改 diagonal 結構；純 numerical E4 改版不能解此接縫，涉及 items 4–5／8 與受影響的型別鏈 |

具體推導如下，適用範圍僅為 P §2 所登記的 C8 continuum target／target-null 路徑：

1. [typed pairing §2](STAGE5C_6A_E_TYPED_PAIRING.md#2-propagation-representation-與-retarded-inverse)
   的 `S_theta` 是 diagonal。線性套 scalar test density／Gaussian mixture 仍 diagonal。
   [固定 quadrature](../analysis/stage5c_continuum_pairing.py) 的
   `pair_retarded_gauss_legendre` 及 [v0.2 adaptive](../analysis/stage5c_e4_wellposedness_v02.py)
   的 `_cubature_pairing` 都直接用 `np.diag` 形成 estimates，並非「off-diagonal 很小」。
2. item-3 的 midpoint／scale normalization 保留 off-diagonal exact zero。
   primary 的第二分量是
   `S/||M||_F^2 = (|M01|^2+|M10|^2)/||M||_F^2 = 0`，
   其中只討論 nonzero certificate 已成功的 rows；失敗 rows 本來就先 short-circuit。
3. C8 的 E1／E2 兩臂第二分量均為零，所以每個 matched contrast、cohort mean
   與 CR1 的第二 marginal variance 都為零；改變 selector、theta、mixture、L／B
   或 matching indices 不會把 exact zero 變成正 variance。
4. [region builder](../analysis/stage5c_statistical_regions.py) 的
   `build_simultaneous_region` 對任一 marginal variance <=0 回傳
   `INCONCLUSIVE/DEGENERATE-MARGINAL-VARIANCE`，且 `region=None`。
   既有 Z regression 已以真實兩版本 producer→certification→joint-law→region 鎖定此結果。
   因而直接接線的 C8 E1／E2 不會產生 scientific PASS，增加 samples／縮 numerical width
   亦不會繞過此 precondition。這不是重新判讀任何已執行的 scientific arm。

此結果否定的是「目前 C8 producer＋不變 region 前置條件」的直接組合；
**不否定研究問題本身，也不授權刪第二座標、加 jitter／ridge、換 endpoint 或放寬 gate。**
E3 的 diffusion 等 producer 不可一概套用 diagonal 結論，須逐 arm 核對。
對 deterministic coordinate，可能有保留二維 claim 並另證 coverage 的協定方向，
但目前沒有受審實作；它必須事前明訂結構證明、數值誤差如何傳播、null／alternative
規則及非 deterministic 退化的拒絕條件，連同 items 4–5／8 獨立複核。

因此 O19 是本輪最先應複核的明確 blocker。O2 的一般 coverage 問題仍存在，
不能以處理 exact-zero 分量就宣布所有 statistical-reference 或 item-8 義務關閉。

## 4. 示例 failure 帳本與已否定方法的邊界

A §3.3 的 L=768、H=32、c_clean=0.90 示例給出

`p_row <= (1-c_clean)/(2*L*H) = 1/491520 ≈ 2.0345e-6`。

這僅讓 full raw-pool CLEAN 的 union-bound 下界達0.90；完整PASS還要conditional
power及matching／cap成功。因此它不是正式6a-E結案門檻，更不是九strata概率的總額。
在該既有示例內，扣 beta_geo 後四分，selector／backend／item3各桶與reserve
各為 beta_* =48035549/96000000000000≈5.003703e-7。selector桶要求每個指定
(j,N,theta)單列upper一致滿足，不能再除以九；抽樣confidence的multiplicity另算。
既有桶不可互借，未來實際L/H／success target若不同，須事前重訂受審帳本。

已有證據支持下列方法界限，卻沒有支持「v0.2整體不可行」：

- 完整iid support的pointwise／almost-sure全CLEAN已否定；positive mass不等於超過tail預算。
- 小N chamber counts不能證registered N tails，band分割不保證各band非空。
- factor8在只知非負／subset／matching floor的假設下sharp；改善需新增joint-law資訊。
- 普通iid零failure估計＋全raw-row零超標union-bound的示例需約4.27e8次E4評估
  （A §3.2，66 strata、528 CI cells、delta=0.001），不能規劃成小型確認實驗。
  這是指定估計方式的樂觀樣本下限，不是所有解析／matched-error方法的no-go。
- 增加cohorts不能修復E1無正gap或數值半寬已佔滿E2margin的特定情況。
- v0.1 planted errors不是v0.2 target-law樣本；v0.2三個修正點位也不是out-of-sample確認。

## 5. Item 7 紙上資源檢查

### 5.1 計時scope、已存在資料與兩種schedule

R的139jobs全部完成、78production CLEAN。以下只對既有
`job_outcome_ledger` 中78個 `PRODUCTION-REPORT` 做描述性算術；沒有重新量測，
沒有重算模型或refit。p90定義為ascending order的nearest-rank
`ceil(0.9*78)=71`，不是線性插值。

| 78個production的CPU scope | 合計s | 平均s | p90 s | 最大s | >174.5454545s的筆數 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 整個child（含import／setup等） | 4401.998142 | 56.435874 | 146.149988 | 259.672226 | 6 |
| E4 phase | 4313.576690 | 55.302265 | 145.014293 | 258.542052 | 5 |

若採線性插值`(n-1)*0.9`，whole-child p90為119.194913s；兩個p90差異只是定義，
不能挑對論證有利的版本。E4 wall最大258.568497s（R §4），只佔900s的28.73%。
CPU、wall、E4 phase、whole-child和含parent／所有children的aggregate不得互換。

39fixtures依development strata／count規則選出，不是正式264calls的機率組成或
worst-case集合。6個whole-child超過174.5s既不證總預算超標，平均56.4s也不證合格。
相鄰兩scope有一筆跨過174.5s，顯示不能忽略setup成本。

Q／V的完整資源qualification development schedule為
`3 N × 2 targets × 4 reps × 11 members = 264 calls`。
它不是尚未固定N、L、B、selection／confirmation與successor配置的正式6a-E總工作量。
M的run1亦不是該完整264-call schedule；通過將來的development qualification，
仍不能代替O16對真正scientific workload的可負擔性審核。

### 5.2 單次、總CPU與完整production domain

依Q／M既有qualification路線，1.25作用於**已含validated domain/model error及
overhead**的上界；它本身沒有coverage含義。維持caps至少須有

`1.25 * U_wall <= 900 s`；`1.25 * U_CPU_schedule <= 57600 s`，

以及4096-subdivision contract、memory和target-host preflight。對264calls，
忽略其他成本的平均規劃量是`57600/1.25/264=174.5454545 CPU s/call`。
若`C_other`為margin前的non-E4上界，E4平均可分配量須再減`C_other/264`。
174.5不是每個call的新增CPU cap，不取代900wall，也不是cohort／seed配置。

| 資源義務 | 已有證據 | 尚缺且不可省略的涵蓋 | 紙上證明路線／停止條件 |
| :--- | :--- | :--- | :--- |
| production domain與atom count | V逐membercount<=N(N-1)/2；N64/96/128對應2016/4560/8128 | 相同count的座標mixture、density／theta、boundary、effective scale、enclosure、fixed/adaptive成本未被count界住；39fixtures無domination證明 | 對所有可由真實selector→adapter形成的mixtures建立domain；若無worst-case domination／validated enclosure或cost上界，路線A仍證據不足 |
| subdivision與count的joint可達性 | Q強調a、s、mixture共同限制；R有到4096的zero-tolerance stress | stress用atol=rtol=0，不是production max-scale tolerance；不能當production必要成本。反之production fixtures未hit cap也不證不可能hit | 證production可達s(a,mixture,theta,scale)界或保守全4096界；若要排除高成本區，必須有domain exclusion，不能只删fixture |
| 單次wall | R點位最大258.568497s，該profile下明顯低於900 | 新主機runtime、host contention、primitive operation成本及其他mixtures的上界未證 | 將可驗證operation／error bound與受審host envelope相接；之後另案host驗收。CPU上界不能單獨推出wall上界 |
| 完整264-call aggregate CPU | Q給共同case下sum_b|B_b|=|D|、links/I0與I1..4互斥；11members總count<=3|D|，schedule count upper352896 | count不能乘典型per-atom秒數成CPU上界；需joint subdivisions、enclosure、fixed rule、certification與全部overhead | 在共同case的joint count約束下合計validated costs；非E4包含burn／generation／selector／adapter／imports／preflight／supervisor／cleanup等，按同一schedule起點與實際runtime accounting逐項列帳，不重複或漏帳 |
| error allowance與safety margin | Q固定delta_nonE4+sum delta_j及共同profile誤差；1.25 policy沿用M | empirically fitted residual、repeat spread、×1.25均不能取代domain upper；無獨立性不能用平方和根號 | 留共同host／model／mixture偏差，再作用margin；upper跨cap只是證據不足，只有有效超限witness／必要成本lower才可REJECT |
| memory與環境身分 | R child峰510.183MiB，parent＋child各自peak最大和536.566MiB；run profile驗證通過 | 這不是同步RSS或全域memory界；32GiB address-space與RSS／cgroup物理額度不同；未來host／image尚不存在 | 整個worker／supervisor／library／child存活期間峰值上界＋host餘量；保留source/env/thread/affinity pins、preflight及receipt，另案重新review |

完整domain可能有多種保守上界方法，但目前repo沒有已證成的一種。
選8128atoms、拿sample maximum乘1.25、重跑同host training／held-out，均不自動補此缺口。
若下一版bound只在較小domain成立，須先amend研究適用範圍，不能事後以run1結果縮域。
現在Vultr已由操作者刪除，local-only `cf5c2502` 映像隨之消失；run1是archived
profile上的證據，不是未來新image的qualification。raw archive須保持原樣並另備份；
本設計PR不新建備份，也不宣稱重建映像會逐位元相同。

## 6. 關鍵依賴、限時交付與停止條件

評估窗口為2026-10-10至2026-10-17（台北）；這是**設計評估時限**，不是一週內
完成全部proof的承諾，也不授權到期後自動量測、配置seed或開主機。
本草稿是第一份可供獨立複核的交付。既有數值／資源證據只可引用，不新增probe。

| 優先序 | 本階段要回答的問題 | 可複核的交付與判斷規則 |
| :--- | :--- | :--- |
| 1：結構域、研究效果與reference | 先複核O19的diagonal producer／zero-variance接縫；O2／O13–O15是否有可陳述且不讀armdata的效應／null假設？ | 先定正式source-of-record及統計協定修訂需求；每個claim列明law／conditioning／raw或normalized gap／reference條件。這個接縫未處理前不排付費qualification；缺正gap或有效reference保持OPEN，不以數值加密代替 |
| 2：Gate A | O4／O5化約能否得到目標上界？O7／O8還需哪些producer facts？ | 列出實際可驗證的解析lemma／recurrence需求和依賴；尚未完成的inequality不得填「可行」。若只有普通MC零失敗方案，記錄A已示其示例規模，暫停該量測路線 |
| 3：Gate B與resource同步 | 更細matched-law方法是否必要？v0.2的完整mixture／subdivision成本界缺什麼？ | 將O9–O12的error需求與§5的成本約束配對；不能單方面把eta縮小、或把cells增加而不重算成本。無jointlaw不縮factor8 |
| 4：依賴與決策 | 哪些結果真需改E4，哪些需改研究假設？ | 依§7分類理由、未解義務與下一份design交付；時限到而無承重界時標UNRESOLVED，不用「做完分析」充當閉合 |

這四項可在紙上交互進行；不要求所有item8證明完成後才開始item7成本分析。
只有E4版本與需資格化的domain確定後，才值得考慮付費host工作。
items3–5已交的component provenance／revalidation證據可先核對，不需等新量測；
但其state-only closeout、item7qualification與item8closed仍各有獨立review義務。
items9–12留待其前置條件成立，現在不實作或接線budget／seed／ledger。

## 7. 三條路線的決策表與本次建議

「E4是否保留」與「統計／研究協定是否要修訂」是兩個軸，路線不必互斥：
例如保留v0.2數值producer，同時修訂已被O19定位的statistical接縫。
第三條路線包含協定修訂評估，不預設一定縮小科學問題或刪selector。

| 路線 | 可支持選定它的證據 | 目前repo可推出的判斷 | 選定後的合法下一步 |
| :--- | :--- | :--- | :--- |
| A：保留v0.2，推進解析／validated qualification | 固定v0.2在實際law下的GateA/B、效應／reference與資源義務有承重界或具體可審查proof交付；最後須完整domain與host通過 | **可保留數值基線，但完整protocol不變的直接接線被O19擋住。** V移除了已知點位bottlenecks，R證點位可達；O2、O4–O5、O7–O16及§5另缺界，仍不支持qualification | 先處理O19並補design／proof；domain與版本固定、獨立審查後另定qualification manifest及新host流程，不先跑新training |
| B：修改E4，再重驗／資格化 | 在v0.2、指定承重law／方法下證明數值cap或failure／成本不满足；並定位可修改的producer瓶頸與新候選可解的理由 | **現在沒有足夠證據證明必須改。** v0.1反例與v0.2 in-sample點位不能替代此判斷；某個鬆bound失效也不證v0.2本身失效 | 另立combined amendment，明訂levels／tolerance／error與cost、identities／nullable／reason，完整重驗3–5；不得直接改常數或追量測 |
| C：修訂統計／研究協定，必要時重新界定問題／support／qualification | 有具名producer／consumer不相容證據，或可信effect／reference／GateA/B／資源分析顯示原claim無法達到既定目標或投入上限；或操作者明確選擇較窄新問題 | **O19支持先進行統計接縫amendment設計。** 這不支持縮selector或宣稱整個問題no-go；timeout正式失敗仍要tail／power，丟失敗列改matchedlaw | 先以保留v0.2及二維claims為評估起點，明訂exact-coordinate／reference協定與證明；重審4–5／8和受影響的3／typedchain。若另需縮域，另外明列保留／放棄的claims，不事後只留通過strata |

**本次建議：先走C的統計接縫修訂評估，E4數值基線暫保留v0.2，資源資格化延後。**
理由是O19有基線source／公式／既有real-seam regression支持，純numerical改版
不能解它；這比立即重做cost fit或加密cells更先決。沒有新版tail／error反證
要求立即改E4，也沒有證據要求放棄原研究問題或縮selector；O2／O13／O15等
缺口亦不會被新host量測解決。**這只是amendment設計優先序，不是已核准替代
reference、ADOPT、item7 CLOSED或6a-E凍結。** 若獨立複核證明正式producer
不在§3.4所列範圍，須先明訂其真實typed路徑及證據，再重評本優先序。

除O19目前已有明確的接縫修訂理由之外，其他未解義務若一週內仍欠承重證據，合法結論是
`PROOF-FEASIBILITY-UNRESOLVED／DECISION-DEFERRED`，並明列欠缺的lemma／假設。
不能為了交一份「結論」而把未知強行判成可行／不可行。
後續投入上限由操作者另定；本草稿不替操作者許諾研究月數或費用。

## 8. 獨立複核清單與變更界線

- O1–O18是否完整對應P §8及A／J／S，而非只列九selector？每列是否有證據、缺口、
  proof方法、E4影響與可行性語義？示例failure額度是否與正式目標分清？
- 是否把v0.1反例、新版in-sample改善、抽象calibration與實際target-law證據分開？
  是否只否定已證有問題的方法，沒有把缺界變成整體no-go？
- §5是否同時處理900wall、264-call aggregate CPU、joint mixture／count／subdivision、
  overhead、error、memory與host；是否分清E4phase／child／aggregate、development與scientific工作量？
- O19的source chain與正式E1／E2適用範圍是否正確？是否分清已證的直接接線blocker，
  與尚未證成的替代統計協定，沒有擴張成所有E3 arms或整個研究問題的no-go？
- §7建議是否由前文推得？有O19證據才優先評估C的統計修訂；其餘缺界是否保留
  DECISION-DEFERRED，而非強行判v0.2可行／不可行？
- 變更只允許本設計文件及STATUS索引／更新紀錄；analysis、benchmarks、tests、
  manifests、candidate JSON、run1三份JSON、assessment、source pins及burn registry皆不改。
  合併本文件不簽receipt、不授權新樣本，也不改closure狀態。
