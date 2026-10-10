# Stage 5C / 6a-E — 結構性座標與統計協定修訂草稿

**DESIGN-DRAFT／NOT-IMPLEMENTED／PROOF-OBLIGATIONS-OPEN。** 日期：2026-10-10（台北）。
依 PR #68 的路線 C，暫保留 E4 v0.2；不刪 primary 的第二座標、不加 jitter、
不以樣本零變異自動豁免 gate。本案提出具名的統計協定 amendment，尚未取代既有
region builder，亦不關閉 items 3–5／7／8，不授權 6a-E 執行。

**建議：二維 endpoint 與七個 claims 全部保留。對事前有完整 operator identity
證明的座標，以確定值集合形成 region；其餘座標另用經審查的 coverage 定理。
C8 E1／E2 的第二座標是 `{0}`，第一座標仍須有效推論與效果／功效證據。**
§4 給出可逐步複核的 bounded-ratio coverage 候選，不把條件定理寫成實際法則已成立。
§6 的真實 selector 診斷只完成預定 12 點中的 2 點，不能判定第一分量飽和是否普遍。

## 1. 基線與授權邊界

基線是已合併的 PR #68：main `dd3323a061b5b9ad544ee02ceb29ffcbe4c8d03e`，
tree `8ec174080baea39ef2c03304d0d0ea80e6a61dbd`，與核准 head
`9ece3d4f8883783eb5fff22901eb4b32ffd3c46c` 的 tree 相同。
上輪 [items 7／8 可行性草稿](STAGE5C_6A_E_ITEM7_ITEM8_FEASIBILITY_DECISION_DRAFT.md)
的 O1–O19 是本案義務索引；該草稿的禁止 producer 呼叫是上輪範圍，不是本案 witness 授權。
本案操作者另外要求真實 selector 的確定性 witness，故只執行 §6 的有限開發診斷。

本 PR 只新增本設計文件、診斷 JSON，更新 STATUS。analysis、benchmarks、tests、
既有 statistical／prereg source-of-record、manifest、run 1 evidence／assessment、pins、
registry 均不改。不產生或配置 seed、不呼叫 sprinkle generator／matching、不開主機、
不讀 scientific arm ledger、不形成 scientific arm endpoint、不設計 K、不做資源量測。
局部確定性 endpoint 診斷和既有 CI 回歸不構成 6a-E 執行。

複核者回報已逐步核對 O19，並以真實 v0.1／v0.2 producer、六組人工 atoms、兩個 theta
獨立確認 off-diagonal 與第二分量為零。本案未取得該獨立試驗原始檔，將它記為
**reviewer-reported independent confirmation**，不冒充本案 JSON 的重現紀錄。

## 2. 不變的二維主張與新增的結構證明

### 2.1 C8 的精確化約

[typed pairing](STAGE5C_6A_E_TYPED_PAIRING.md) 的 massless propagation representation
是對角的。正的 scalar Gaussian test measure、正混合權重與線性 pairing 不生成
非對角項。[fixed quadrature](../analysis/stage5c_continuum_pairing.py) 與
[v0.2 adaptive](../analysis/stage5c_e4_wellposedness_v02.py) 都用 `np.diag`。
[item-3 certification](../analysis/stage5c_numerical_certification.py) 的逐項 dyadic midpoint
保持這個零；任意 matching 子集及線性加權 contrast 也保持第二座標為零。

對真正的 C8 continuum matrix `diag(a,d)`，兩個 diagonal integral 都為正：正密度
乘嚴格正 Gaussian mixture，在兩個非零測度的 characteristic domains 上積分。
不適用於任意複數 test measure、未知 producer 或任意候選 K；數值 underflow 等
仍按 E4／item 3 fail closed，不以這個解析事實把非 CLEAN output 升格。
由 [primary 定義](../analysis/stage5c_primary_invariant.py)，

$$
I_1=\frac{(a-d)^2}{a^2+d^2}
   =1-\frac{2ad}{a^2+d^2}\in[0,1],\qquad I_2=0.
$$

精確正 `a,d` 下 `I1<1`；浮點值可能 round 到 1。若 `r=a/d`，
`1-I1=2r/(1+r²)`；比例遠離 1 可造成飽和，不能用直接平方巨大 `r` 的不穩定
計算代替 validated bound。這個關係解釋診斷問題，不證明實際 target 的比例分布。

完整 primary 的 global sharp ranges 仍是 `[-1,2] × [0,1]`，固定 normalization
`D=diag(3,1)`、normalized margins `1/20` 都不變。C8 的較窄範圍只可用作
經證明的 concentration bound：每個 matched cohort 的 normalized contrast 第一分量
`Y1∈[-1/3,1/3]`。不得改用 `D11=1` 或借此放寬 E1 門檻。
二維 minimality 的既有全域主張亦不改：E3 diffusion 需要非零第二座標。

### 2.2 事前的 profile；不得按觀測選 mask

下表是待審的固定 profile，不是可接受 caller 傳入的 `structural=True` flag。
結構身份必須涵蓋**兩個 arms 的完整 endpoint producer**，不只是目前返回一個對角 array。
若 formal finite-cohort mapping 不等於表列 operator，這個 profile 不成立，須另案重審。

| 具名 claim | 事前結構座標 | 隨機座標與原 gate |
| :--- | :--- | :--- |
| C8 E1 `T-plus − T-minus` | contrast 第二座標精確 0 | 第一座標；完整 region 避開 closed `[-1/20,1/20]²` |
| C8 E2 plus-null | contrast 第二座標精確 0 | 第一座標；完整 region 嚴格含於 open `(-1/20,1/20)²` |
| C8 E2 minus-null | 同上，獨立具名 comparison | 同上；plus／minus 仍須都 PASS |
| E3 correct-chiral − sector-blind | 兩個完整 planted matrices 都 diagonal 時，第二座標 0 | 第一座標 raw region `>1/10` |
| E3 symmetric-diffusion − sector-blind | 不套用 C8 零座標 profile | 兩座標；raw 第一 `<−1/10`、第二 `>1/10` |
| E3 correct-support − wrong-support | 完整 registered support pairings 都 diagonal 時，第二座標 0 | 第一座標 raw region `>g*/2` |
| E3 sector-blind-null-A − sector-blind-null-B | 真正完整 matrices 為非零 `sI` 時，兩個 endpoint 都 `(0,0)`，contrast 都 0 | 無隨機座標；兩個原 equivalence gates 都以結構證書承擔 |

E3 profile 的代數來源為 [planted_matrix／support pairing](../analysis/stage5c_planted_certification.py)
與 [item-6 contract](STAGE5C_6A_E_CERTIFICATION.md)。列出來源不完成 O15 的
finite-cohort mapping／conditioning／功效義務。global swap 仍是原 trace／bitwise gate，
不使用新的 statistical alpha。

### 2.3 未來 typed structural certificate 的最低契約

實作案須另交 `StructuralCoordinateCertificate` 與專用驗證器，至少綁定：

- operator／prescription、positive scalar measure class、primary source／版本、basis／boundary、
  E4 source identity、完整 arm roles、claim identity、確定座標及 exact value；
- 允許的幾何／混合域和上述線性／比值證明，registered E3 的完整 parameter／scale 域；
- item-3 CLEAN source-row seals、matching／ensemble fingerprint、aggregation operation trace。

proof 的適用域須涵蓋全部被聚合的原始 rows；仍保留全池 non-CLEAN 拒絕與 norm gate。
不能因某座標結構化而丟掉其他失敗列。若身份／seal／source／域不符，或宣稱零座標卻
產生非零值，必須 `PROTOCOL-INVALID`／不產生 region，不容許 epsilon 補救。
未知 profile 與任意 observed-zero arrays 不能取得結構證書；legacy reference 仍保持原 gate。

item-3 的原 matrix enclosure、endpoint errors、lower／upper 及 seals 不改、不清零。
新 derived region 可以在**另驗證的 exact identity** 下把該座標限制為 singleton，
但保留原保守 numerical evidence 供審計。這是明文新推論規則，不是修改原誤差資料。
非結構座標即使 sample variance 為零也不視為已知常數；§4 的正半寬仍保留。

## 3. 二維 region、claim 規則與 family budget

設 `A_g` 是事前固定的隨機座標集合，`S_g` 是經證明的結構座標集合，
`A_g∪S_g={1,2}`。提案仍回傳二維 named region：

$$
\mathcal R_g=\prod_{k\in A_g}[\hat z_k-h_k,\hat z_k+h_k]
             \times\prod_{k\in S_g}\{c_{g,k}\},
\qquad z=D^{-1}\Delta.
$$

座標按原 index 排列；上述乘積不是刪欄。C8 的形式為 `R1 × {0}`。
每個原 component gate 都執行，包括 `{0}` 是否位於 equivalence open margin。
E1 只有第一座標能清除 dead zone，這是事前 identity 的結果，不能讀數據挑座標。
原 boundary equality 仍 FAIL，schema／未認證輸入仍不產生 scientific verdict。

[budget audit](STAGE5C_6A_E_E5_BUDGET_POWER_AUDIT.md) 的 11 members、兩 splits、七個
named regions、selection／fresh confirmation／successor accounting 均保留：

$$
\alpha_g=\frac{1/20}{11\cdot2\cdot7\cdot2^{r+1}},
\qquad \alpha_{g,r=0}=1/6160.
$$

不向結構性 singleton 分配 sampling error；同一 region 的 random coordinates 可用完整
既有 `alpha_g`，若 `d_g=|A_g|=2` 則 union bound 分配兩座標。
`d_g=0` 的 cell 仍在七個 named claims 與原 ledger 中；保留其原 allocation，不移轉、
不回收、不另創擴大其他 claims 的容量。family 數量不縮；新的 reference 必須在 seeds 前
freeze，不按 witness、selection 或 scientific data 選較窄者。

## 4. Coverage 候選：有界、隨機分母的 pair-weighted mean

### 4.1 目標與未完成前提

目前 unequal-attrition CR1 cluster-Student 是 operational reference；df-only Gaussian
oracle 不證真實 matched law 的 finite-sample coverage。把 `p=2` 改成 `p=1` 不能補上 O2。
本案優先提出下面的有界 reference 作為**待審候選**，不自動採用、不假定其成本可負擔。
它保持 existing pair-weighted aggregation，不改成 equal-cohort mean。

對固定的 `j,N,theta`、有序 arms、generation／split 與 producer versions，令：

- `B` 是事前固定 independent cohorts 數，`m_b∈[192,384]` 是 matched counts；
- `Y_b,k` 是第 b cohort 的**精確、pre-numerical** normalized matched contrast mean；
  `|Y_b,k|≤R_k`。C8 取已證 `R1=1/3`；只知 global primary 範圍的座標取 `R_k=1`；
- `C_b` 是只依該 cohort 自身 inputs／獨立 calibration／matching／全池 certification
  的局部成功事件，不包含依賴全部 cohorts 的 aggregate cap 或 cross-cohort selection；
- cohort inputs 與 calibration streams 互相獨立，`Pr(C_b)>0`，且在 `C0=∩C_b` 下
  `(m_b,Y_b,k)` 保持獨立；每個 b 都有同一個確定值
  `μ_k = E[m_b Y_b,k | C_b] / E[m_b | C_b]`。

iid 的同一 conditional cohort law 是最後一項的充分條件。真實 runner 是否有共享校準、
matching tie-breaking／arm orientation 是否破壞 null symmetry，都必須由 O2／O10 證明。
`μ` 是本候選明文的 **pair-weighted matched-conditional population estimand**，不是
`E[Y_b]`、raw target mean 或平均 invariant of matrix；也不是有限 B 的 `E[hat z]`。
若科學主張需要原有不同目標，必須證兩者橋接或另行修訂主張，不能默換 estimand。
同 raw target 不自動推出 `μ=0`；更不能用本診斷的 point values 推出它。

### 4.2 可逐步核對的定理（以上前提成立時）

寫 `m_min=192`、`m_max=384`、`R=R_k`，
`Z_b=m_b(Y_b,k−μ_k)`。依上述 ratio 定義，`E[Z_b | C0]=0`。
因 `μ_k∈[-R,R]`，每個 `Z_b` 在長度 `2R m_max` 的固定區間內。
Hoeffding 對 independent bounded variables 的雙尾界給出

$$
\Pr\left(\left|\sum_b Z_b\right|>t\mid C_0\right)
\le 2\exp\left(-\frac{t^2}{2B R^2 m_{\max}^2}\right).
$$

又 `Σm_b≥B m_min`，故真正的有限 B estimator
`tilde z_k=Σm_bY_b,k/Σm_b` 滿足

$$
\Pr(|\tilde z_k-\mu_k|>h\mid C_0)
\le 2\exp\left(-\frac{B m_{\min}^2h^2}{2R_k^2m_{\max}^2}\right).
$$

對 `d_g≥1`，取

$$
h^{\rm stat}_{g,k}=R_k\frac{m_{\max}}{m_{\min}}
 \sqrt{\frac{2\log(2d_g/\alpha_g)}{B}}.
$$

現有 source-sealed、ensemble-bound triangle propagation 若已證
`|hat z_k−tilde z_k|≤ν_k`，用 `h_k=h_stat+ν_k` 即得
`Pr(μ∈R_g | C0)≥1−alpha_g`；結構座標是確定 identity，不需 sampling tail。
不要求 cohort 內 pairs 獨立，亦不要求座標間獨立；要求的是 cohorts 及局部條件律。
`d_g=0` 另走全結構 proof path，不對 `log(0)` 套公式。

Hoeffding 原始來源：W. Hoeffding (1963), *Probability Inequalities for Sums of Bounded
Random Variables*, JASA 58(301), 13–30，Theorem 2，
[DOI](https://doi.org/10.1080/01621459.1963.10500830)，
[原文掃描](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf)。
隨機分母、ratio estimand、numerical width 及本案 conditioning 的接線是本草稿推導，
不是該論文替實際 repo law 證明的結論。

未來實作仍須 outward validated log／sqrt／rational alpha、centres／width／bounds，
保持 source-bound provenance 與 strict comparisons；不得把 binary64 規劃值當上界。
CR1 covariance 可留作診斷，但不在這個 reference 中冒充 coverage 證據。
有限 sample variance 為零不縮此半寬；要縮界須事前另有有效定理和審查。

### 4.3 全域 cap 與條件化：本定理不能跨過的界線

若 `A` 是全域 numerical cap／resource／selection gate，依全部 cohorts 而定，
從上述定理只能推出

$$
\Pr(\mu\notin\mathcal R_g, A\mid C_0)\le\alpha_g;
\qquad
\Pr(\mu\notin\mathcal R_g\mid C_0\cap A)
 \le\alpha_g/\Pr(A\mid C_0).
$$

不能直接宣稱 cap-conditioned coverage `1−alpha_g`，亦不能把 `μ` 自動換成
`E[mY | C_b,A]/E[m | C_b,A]`。若 contract 要求後者，需對該條件律另證定理；
若有事前成功機率 lower bound，可另審更小內部 alpha，但不得用觀測成功率反推。
不輸出 region 的失敗不算科學 PASS；這可支持同一固定 conditional estimand 的
error-intersection 帳，但不能自動完成所有 conditioned coverage／科學目標橋接。
family union bound 仍須各 cell 對固定目標有效、fresh streams 與原 spending 成立。

## 5. 功效、items 4–5／8 與資源影響

### 5.1 O2／O13：第一分量仍可能缺效果

飽和和小變異是不同命題。若兩個 targets 的 `I1` 都接近 1，contrast 可能小；
也可能存在事前有方向的差距。若都接近 0 也一樣，單一點不回答 `μ_plus−μ_minus`。
E1 所需的是對**配對後、既定條件律**的第一分量正 gap，而不是矩陣 diagonal ratio 大、
低 sample variance 或 unpaired endpoint 均值看起來不同。

設真實目標距固定 gate 的最小 normalized slack 為 `g_k>0`，
全域成功事件上有 `ν_k≤η_k`。若 statistical deviation 以

$$
t_{\beta,k}=R_k\frac{m_{\max}}{m_{\min}}
 \sqrt{\frac{2\log(2d_g/\beta)}{B}}
$$

控制，`g_k>h_stat+2η_k+t_beta` 是保守 conditional PASS 充分條件。
這裡 `g` 對精確 `μ` 定義：numerical error 可同時偏移中心並擴張 region，所以出現
`2η`。若另一 power model 直接對可觀測 endpoint 定義 gap，須明列不同定義與橋接，
不混用只含一個 `η` 的示例。`beta` 是另行預登記的 power failure budget，不等於 alpha，
也不是全部 claims 都自動取 0.10。全局 `A` 存在時，還須處理 `Pr(A^c | C0)`，
並把 `Pr(C0)`、certification／matching／resource failures 接回無條件功效。

保守界的代價不能略去：純規劃算術在 `alpha=1/6160`、`d=1`、C8 `R=1/3`、
`η=0` 時，僅要 `h_stat<1/20` 就需 `B>3348.9704`，即至少 3349。
這不是 power-derived floor、不是必要最小樣本數、更不是新 cohort 配置；它只表明這個
候選 sufficient bound 很保守。加 `t_beta`／numerical slack 後可能更貴。若無法負擔，
合法下一步是證更銳利的事前 concentration／law，或另外評估研究範圍；不放寬 margin。

### 5.2 逐項義務與版本遷移

| O／closure | 本案可支持的改動 | 仍缺的證據與下一份交付 |
| :--- | :--- | :--- |
| O19；items 4–5 | 提出完整二維 structural-region 接縫；保留所有 named component gates | typed proof／source seals、真實 v0.2 seam 與 mutation checks、獨立複核；目前 blocker 未被可執行程式解除 |
| O1；item 8 budget | 保留七 regions／11 members／splits／lineage；零座標不借 alpha | ledger／fixed profiles／freshness 接線，對每個 cell 真正有效的 coverage |
| O2／O10／O12 | §4 有明確 ratio estimand 與局部条件定理 | 真實 matching 推前、null symmetry、局部獨立性、共享校準稽核、全域 cap conditioning 與科學目標橋接 |
| O13／O14 | E1／兩個 E2 的 stochastic 問題只在第一座標；原 threshold 不改 | matched conditional positive gap／null law、error slack、success 概率；§6 不能代替它們 |
| O15 | 區分 diagonal E3／diffusion／全結構 blind-null，保留原 Gate O/E | 完整 finite-cohort operator 身份；逐 claim 的 directional／equivalence 效果，不把 continuum gap 當有限樣本功效 |
| O3–O8 | 本案不改 selector／E4／norm gates | 各 empty-selection、geometry、backend／subdivision、underflow／certification failure 的承重界仍 OPEN |
| O9／O11 | 結構零可經獨立證明限制 derived coord 2，但不改原 error vector | 第一座標完整 mixture error／matched amplification／cap 界；不能把現有 factor 8 私自縮小 |
| O16；item 7 | 新 reference 的 cohort 成本須加入真正 workload | conditional 和 unconditional power、每 claim／operation floors、完整 cost envelope；不是只重跑 264 calls |
| O17；item 3／4–5 | E4 v0.2 payload 不變；新增 derived inference 版本 | item-3 seals 不變但消費者重審；新的 region ID／width／mask／proof fingerprint，舊 Student objects 不自動升級 |
| O18；items 9–12 | 本 witness 是明定的非隨機開發診斷 | 任何 stochastic pilot／新 seed／runner／decision table／正式 closeout 均另案事前審查 |

item 7 的紙上範圍仍同時要求 `1.25 U_wall≤900 s` 與完整 264-call **development**
qualification 的 `1.25 U_CPU_schedule≤57600 s`；margin 前每次平均規劃量
174.545455 CPU s 不是新增 per-call cap。完整 production 域需涵蓋 mixture scales／weights、
細分、enclosure／certification、overhead 與新 target host；run 1 的 39 fixtures 不能補上。
264-call schedule 不代表正式 `B` cohorts 的費用。資源資格化延後，沒有主機重建授權。

## 6. 真實 selector 的確定性 witness：不完整結果

證據：[stage5c_structural_coordinate_design_witnesses.json](stage5c_structural_coordinate_design_witnesses.json)，
SHA-256 `a15455d19492f928478cb819fd4cad592b44a2aca46abe6b2b2fab1a6723aeab`。
JSON 包含事前 plan 原文／hash、diagnostic runner 原文／hash、基線 source blobs、
已開始 case 的 exact coordinates／order／pairs
bytes與 hashes、atom／weight hashes、fixed／adaptive matrices、certified endpoint／error hex、
actual runtime 與 incomplete terminal。它不是 run 1 證據，也不修改任何既有 assessment。

### 6.1 事前選點與實際路徑

在看 numerical output 前固定 3 個 N=64 cases：既有 frozen coordinates 的 `64:chain`、
`64:modular_5`，以及 two asymmetric comparable points 加 62 antichain tail 的明定 recipe。
每個 case 跑真實 `all_relations`／`links`、空 parameter tuple、theta `−0.4/+0.4`，共 12 點。
不是完整 11-member family，也不是 39 fixtures 或 target-law 抽樣。

實際呼叫順序：`order_from_uv` → `BlindedCase` → `apply_selector` →
`build_production_atoms` → `evaluate_e4_wellposedness` → existing item-3 endpoint。
沒有手寫 selector pairs／atoms／判讀。RNG／sprinkle generator 入口置為拒絕函式；
沒有 matching／arm ledger。已有 coordinates 只作固定開發 fixtures，不賦予其 target-law 地位。

本機 Python 3.12.14、NumPy 2.3.5、SciPy 1.17.0、threadpoolctl 3.6.0；一 CPU affinity、
six thread envs 固定 1，CPU hard limit 180 s、address-space limit 3 GiB。
這些是局部診斷上限，不修改 E4 contract、CI pins，也不代表 Vultr runtime qualification。
初次 writer 使用兩個不存在的 result attributes，未保存任何 row；修正欄位 mapping 後，
按完全相同的 plan 重啟。這不是一次性 receipt campaign，不能宣稱只呼叫 12 次 producer。

### 6.2 全部已保存結果與缺漏

| case／selector／theta | atoms | v0.2 status | certified point I1 | I2／max off-diagonal | a/d |
| :--- | ---: | :--- | ---: | :--- | ---: |
| chain64／all_relations／−0.4 | 2016 | CLEAN | 6.162975822039156e−33 | 0／0 | 1.0000000000000002 |
| chain64／all_relations／+0.4 | 2016 | CLEAN | 2.4651903288156624e−32 | 0／0 | 1.0000000000000002 |

runner 在下一個未保存請求 `chain64／links／−0.4` 期間以 shell exit 137（signal 9）結束。
沒有 terminal success；配置了上述 hard limits，但**沒有獨立證據確定 kill 原因**，
不宣稱 OOM、正常 budget completion 或正式 E4 timeout。2 筆已保存、10 筆未有 outcome；
未保存不記成 CLEAN／FAIL／censored。沒有追加預算、補選 cases 或挑出較有利結果。

兩個點都在 0 附近，故「人工 atom 的 near-one 現象可直接套給所有真實 selector」沒有
證據；但這也不能否定真實 target 的飽和或證明效果良好。只完成同一 chain 的兩個 theta，
無法回答其他 cases／members 的分布。point midpoint 不是精確 continuum truth：本案
第一分量 certified error 分別 0.10733285441070511、0.10338824640116889；
第二分量仍有原保守 error，未清零。這些不能當零 population variance 或 numeric-cap 合格。

若需要擴充診斷，須先另定有限 cases、全 11 members 適用性、預算／stop policy，
保存全部 outcome（包括 incomplete），才執行；本案不隱性續跑未完成 10 點。
若目的是 O2／O13 的**分布**或 positive-gap 證據，確定性 witness 不足，須先提交
candidate-independent 的 target-law 分析／合法 stochastic manifest，不能讀 scientific arms。

## 7. 決策與後續審查界線

**建議先審此結構性 amendment；保留 v0.2，延後 item 7 資格化。**
O19 已有獨立 producer 複核，確實需要統計接縫修訂；本案沒有證據要求 numerical E4 改版。
第一分量是否普遍飽和仍未解，不用不完整 witness 選 effect model／reference／cap。

本設計經審查後，下一份實作 PR 才交 proof-bearing profiles、bounded reference 或其他
事前獲准 reference、version migration 與 real-producer seam／negative tests：
錯 source／claim／mask／非零結構值／seal mutation 必須拒絕；任意 sample-zero stochastic
座標不得變 singleton；diffusion 第二分量仍有原 directional gate；strict boundaries、
全池非 CLEAN 拒絕、cross-arm blocks、family allocation 不變。不得僅刪舊 variance 檢查。

審查必須分別決定：(1) structural identity 的完整適用域；(2) §4 estimand 是否符合科學
主張，以及實際條件律前提何處有證據；(3) finite-sample reference 的保守成本是否值得
繼續證更銳利的界；(4) O13–O16 的 gap／numerical slack／無條件 power 與成本缺口。
若前提或成本未證，就保留 OPEN，不把設計合併寫成 item 8 CLOSED 或 6a-E 可跑。
