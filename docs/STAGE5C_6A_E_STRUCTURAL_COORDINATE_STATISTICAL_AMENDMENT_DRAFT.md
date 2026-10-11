# Stage 5C / 6a-E — 結構性座標與統計協定修訂草稿

**DESIGN-DRAFT／NOT-IMPLEMENTED／PROOF-OBLIGATIONS-OPEN。** 初稿：2026-10-10；
選項 B 修訂：2026-10-11（台北）。本稿待 exact-head 設計複核，不是已核准的執行協定。
依 PR #68 的路線 C，暫保留 E4 v0.2；不刪 primary 的第二座標、不加 jitter、
不以樣本零變異自動豁免 gate。本案提出具名的統計協定 amendment，尚未取代既有
region builder，亦不關閉 items 3–5／7／8，不授權 6a-E 執行。

**建議：二維 endpoint 與七個 claims 全部保留。對事前有完整 operator identity
證明的座標，以確定值集合形成 region；其餘座標另用經審查的 coverage 定理。
C8 E1／E2 的第二座標是 `{0}`，第一座標仍須有效推論與效果／功效證據。**
§4 給出可逐步複核的 bounded-ratio coverage 候選，不把條件定理寫成實際法則已成立。
§6 的真實 selector 診斷只完成預定 12 點中的 2 點，不能判定第一分量飽和是否普遍。

**操作者決定選項 B：不重跑 witness。** 保留既有 2/12、exit 137、死因未獨立確證
的紀錄；不追加預算、不換案例、不續跑。第一分量是否普遍接近 1 明列為 O2／O13 的
未解義務，留到效果模型設計時以事前審查的計畫處理。本週交付集中於結構性零分量
的統計協定修訂；可複核設計稿的期限仍為 **2026-10-17（台北）**，不承諾在該日前
完成 item 8 全部證明、實作或資源資格化。

## 1. 基線與授權邊界

基線是已合併的 PR #68：main `dd3323a061b5b9ad544ee02ceb29ffcbe4c8d03e`，
tree `8ec174080baea39ef2c03304d0d0ea80e6a61dbd`，與核准 head
`9ece3d4f8883783eb5fff22901eb4b32ffd3c46c` 的 tree 相同。
上輪 [items 7／8 可行性草稿](STAGE5C_6A_E_ITEM7_ITEM8_FEASIBILITY_DECISION_DRAFT.md)
的 O1–O19 是本案義務索引；該草稿的禁止 producer 呼叫是上輪範圍，不是本案 witness 授權。
本案先前依操作者要求執行 §6 的有限開發診斷；2026-10-11 明確選 B，
本次只更新設計與 execution note，不再執行任何 witness 或 E4 producer。

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

### 2.1.1 不依賴 witness 的完整零座標證明鏈

對 [prereg §2](STAGE5C_6A_E_PREREGISTRATION_DRAFT.md) 固定的 C8 E1／E2 路徑，
每個 source row 的 endpoint 都來自同一具名 massless continuum pairing；不是任意矩陣。
下面五步是 operator／primary／aggregation 的解析及實作身份核對，不以 §6 點位為前提。

1. **分佈的非對角項是零分佈。** [typed pairing §2](STAGE5C_6A_E_TYPED_PAIRING.md)
   固定 `D0=diag(∂u,∂v)` 及
   `S0=diag(H(ux−uy)δ(vx−vy), δ(ux−uy)H(vx−vy))`。
   `Sθ=pθ(x)^(-1/4) S0 pθ(y)^(-1/4)` 的左右因子都是 scalar，
   因此 `Sθ_RL=Sθ_LR=0` 是 distribution identity，無小量近似。
   固定 zero-incoming／no-reflection boundary 不新增 sector mixing。
2. **Scalar test measure 與 regulator 保持 identity。**
   [符合 prereg measure 格式的既有 selector adapter](../analysis/stage5c_e5_screen.py) 的 `build_production_atoms`
   把選出的 `(earlier,later)` 寫為四維 `(later,earlier)` atoms、uniform normalized weights。
   它不建立 spinor-valued measure；[Gaussian mixture](../analysis/stage5c_e4_wellposedness.py)
   的 `_mixture_density` 亦是 scalar。任意 member、任意非空合法 selected set、
   合法 weights／theta 下，線性 pairing 零分佈仍得零。第一座標的 `[0,1]` 界另外
   使用正 density／weights；第二座標的零 identity 本身不依賴 diagonal 大小相近。
3. **兩條數值路徑與 midpoint 不產生非對角項。**
   `pair_retarded_gauss_legendre` 與 v0.2 `_cubature_pairing` 分別累積兩個 scalar
   characteristic integrals，直接 `np.diag`；不含其他 off-diagonal accumulator。
   `_certified_midpoint` 將兩路每個實／虛部轉 exact dyadic rational 再平均：
   `(0+0)/2=0`。item 3 在 finite、agreement、strict nonzero norm 等 gates 通過後，
   以 `M/max(abs(M))` 作 primary reduction；finite nonzero scalar normalization
   保持 off-diagonal 為零。不通過者仍沒有可用 endpoint，不能由此 lemma 升格 CLEAN。
4. **Primary 的第二分量恆零。** 對每個合法非零對角真值與已認證 center，
   `I2=(|b|²+|c|²)/||M||F²=0`。匹配後的每一對第二座標差為 `0−0=0`，
   任意合法子集、uniform pair mean、既有 `m_b` 加權 cohort aggregation 都保持零；
   population conditional ratio mean 的第二座標也為零，任何正機率 conditioning 不改它。
5. **原零變異拒絕由此必然觸發。** 每個 cohort contrast 的第二座標與整體中心皆零，
   CR1 第二個 cluster score 為零，所以 `V22=0`。
   [既有 builder](../analysis/stage5c_statistical_regions.py) 的 `build_simultaneous_region`
   遇到任何 marginal variance `<=0` 都不產生 region。結構性 singleton 是為這個
   事前 identity 提出的新 consumer 規則；沒有放寬現行實作的 gate。

**作用域。** proof 綁定 canonical `(R,L)` frame、目前 massless prescription、scalar
measure／regulator、boundary 和完整 producer versions。
[typed pairing §4](STAGE5C_6A_E_TYPED_PAIRING.md) 允許的 `G=T²⋊S2` unitary monomial
basis action 只作 diagonal phases／slot swap：`B diag(a,d) B^-1` 仍 diagonal，故零
identity 保持。一般會混合 slots 的 basis change、mass／sector-mixing operator、
spinor-valued test measure、不同 boundary、E3 diffusion 或未來候選 K 不受此 proof 約束。
有 source／domain 改動就重審 certificate，不靠觀測值看起來 diagonal 自動延用。

**誤差集合與結構集合分開。** 原 item-3 ball 可包含 off-diagonal 擾動，故保守 error
第二座標大於零並不矛盾；operator proof 另限制真值位於 diagonal 子空間。
新 region 可在已驗證身份下對這個真值集合作推論，不能改寫原 ball／endpoint errors，
也不能用零座標 proof 略過 norm、certification 或全池 CLEAN gates。

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
`A_g∪S_g={1,2}`、`A_g∩S_g=∅`。提案仍回傳二維 named region：

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

若 inputs 獨立且各 `C_b` 只讀該 cohort，則 conditional joint law 的因式分解為
`Pr(∩{X_b∈E_b} | C0)=∏Pr(X_b∈E_b | C_b)`；這證明局部 conditioning 保持
cohort 獨立。共用 fitted calibration 或 aggregate cap 就不能用這一步，須另有證明。
每個 fixed claim 的兩臂可以同時依賴同一 cohort，並不要求它們或 matched pairs 獨立。

iid 的同一 conditional cohort law 是最後一項的充分條件。真實 runner 是否有共享校準、
matching tie-breaking／arm orientation 是否破壞 null symmetry，都必須由 O2／O10 證明。
`μ` 是本候選明文的 **pair-weighted matched-conditional population estimand**，不是
`E[Y_b]`、raw target mean 或平均 invariant of matrix；也不是有限 B 的 `E[hat z]`。
若科學主張需要原有不同目標，必須證兩者橋接或另行修訂主張，不能默換 estimand。
同 raw target 不自動推出 `μ=0`；更不能用本診斷的 point values 推出它。

### 4.2 可逐步核對的定理（以上前提成立時）

寫 `m_min=192`、`m_max=384`、`R=R_k`，
`Z_b=m_b(Y_b,k−μ_k)`。依上述 ratio 定義，`E[Z_b | C0]=0`。
因 `μ_k∈[-R,R]`，每個 `Z_b` 都在
`[m_max(−R−μ_k), m_max(R−μ_k)]` 這個固定區間內；兩端分別非正／非負，
所以任意 `m_b≤m_max` 不會超出它，區間長度為 `2R m_max`。
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
每個隨機座標的尾機率至多 `alpha_g/d_g`，對固定 `d_g` 個座標 union bound
才得到上述 simultaneous coverage；依 operator identity 證明的 singleton 則 coverage 為 1。
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
在 `Pr(A | C0)>0` 時，從上述定理只能推出

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

**具名未解義務 `O2/O13-FIRST-COORDINATE-SATURATION`：OPEN-NO-DISTRIBUTION-EVIDENCE。**
第一分量在一般真實 selector 輸出／目標律中是否普遍接近 1，其 distribution、variance
與 E1 matched effect gap 的影響，都尚未證明。O2 承擔 matched／conditioned law 和
coverage 目標橋接；O13 承擔事前有方向的 positive-gap model，兩者不能由點位代替。
目前僅存的 2 筆同屬 `u=v` 的對稱 chain／all_relations，不能代表一般 selector。
按操作者選項 B，這項義務留到效果模型設計，以事前審查的分析或診斷計畫處理；
本週不為回答它追加運算，也不用不完整 witness 選 reference、effect model、cap 或 B。

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

成本換算供決策參考：若單一 claim／member／split 的每 cohort 至少 192 matched pairs、
兩個 arms 的每個 endpoint 各需一次 E4，且不重用結果，則上述 `B=3349` 對應
`3349×192×2=1,286,016` 次 E4；以 run 1 production 平均約 56.4 whole-child CPU s
代入，約為 **2.3 CPU 年**（一年按 365 日）。這是該保守 sufficient bound 的條件式
工作量示例，不是 E1／E2 的必要成本下界或不可行定理：run 1 fixtures 不代表正式輸入，
whole-child CPU 包含非 E4 開銷；全池 certification 尚有成本，跨 claims／members
是否可合法重用 endpoints 亦須另核，不能直接再乘所有 claims。此候選界尚不足以支持
投入正式計算；優先工作是證更緊的真實條件律／集中界或另審 claim 範圍，不能把
O2／O13 未解的飽和觀察當成已證 variance／support 界。

### 5.2 逐項義務與版本遷移

| O／closure | 本案可支持的改動 | 仍缺的證據與下一份交付 |
| :--- | :--- | :--- |
| O19；items 4–5 | 提出完整二維 structural-region 接縫；保留所有 named component gates | typed proof／source seals、真實 v0.2 seam 與 mutation checks、獨立複核；目前 blocker 未被可執行程式解除 |
| O1；item 8 budget | 保留七 regions／11 members／splits／lineage；零座標不借 alpha | ledger／fixed profiles／freshness 接線，對每個 cell 真正有效的 coverage |
| O2／O10／O12 | §4 有明確 ratio estimand 與局部條件定理 | 真實 matching 推前、null symmetry、局部獨立性、共享校準稽核、全域 cap conditioning 與科學目標橋接 |
| O13／O14 | E1／兩個 E2 的 stochastic 問題只在第一座標；原 threshold 不改 | matched conditional positive gap／null law、error slack、success 概率；O2／O13 第一分量飽和義務仍 OPEN，對稱 chain 的 2 筆不承重 |
| O15 | 區分 diagonal E3／diffusion／全結構 blind-null，保留原 Gate O/E | 完整 finite-cohort operator 身份；逐 claim 的 directional／equivalence 效果，不把 continuum gap 當有限樣本功效 |
| O3–O8 | 本案不改 selector／E4／norm gates | 各 empty-selection、geometry、backend／subdivision、underflow／certification failure 的承重界仍 OPEN |
| O9／O11 | 結構零可經獨立證明限制 derived coord 2，但不改原 error vector | 第一座標完整 mixture error／matched amplification／cap 界；不能把現有 factor 8 私自縮小 |
| O16；item 7 | 新 reference 的 cohort 成本須加入真正 workload | conditional 和 unconditional power、每 claim／operation floors、完整 cost envelope；不是只重跑 264 calls |
| O17；item 3／4–5 | E4 v0.2 payload 不變；新增 derived inference 版本 | item-3 seals 不變但消費者重審；新的 region ID／width／mask／proof fingerprint，舊 Student objects 不自動升級 |
| O18；items 9–12 | 本 witness 是明定的非隨機開發診斷 | 任何 stochastic pilot／新 seed／runner／decision table／正式 closeout 均另案事前審查 |

**Items 4–5 的新交付邊界。** 依 [closure §8](STAGE5C_6A_E_PREREGISTRATION_DRAFT.md)，
item 4 是 E1 joint contrast：其二維 interval object 須新增 identity-bound structural
coordinates、active dimension 與 coverage-reference ID，保留原 E1 closed-box exclusion。
item 5 是 E2 null equivalence：plus-null／minus-null 每個 comparison 都要同一版本的新
二維 region，保留 typed same-target specs、兩者共同成功和 strict open-box inclusion。
兩項的第一座標 numerical width 仍由原 sealed rows／matching／ensemble 傳播；第二座標
以已證 singleton 送進原 component gate。共用這個 builder 的 E3 亦按 §2.2 逐 profile
重審，原方向／equivalence rules 不改。舊 Student objects／歷史 v0.1 closeout 不能直接
升級；新的 typed real-seam／mutation evidence 與獨立 review 仍待交。

**Item 8 沒有被縮成一維功效問題。** sampling coverage 只在 active coordinates 分配，
但全 11 members 的 selector／E4／certification failures、matching 推前與 cap conditioning、
E1 positive effect、兩個 E2 null laws、四個 E3 finite-cohort claims、完整無條件功效及
資源工作量仍全部承擔。結構恆零只完成具名子義務，不把其餘缺界寫成已解。
§4 是有明確前提的候選定理；實際 law 前提和科學 estimand 橋接未證就維持 OPEN。

item 7 的紙上範圍仍同時要求 `1.25 U_wall≤900 s` 與完整 264-call **development**
qualification 的 `1.25 U_CPU_schedule≤57600 s`；margin 前每次平均規劃量
174.545455 CPU s 不是新增 per-call cap。完整 production 域需涵蓋 mixture scales／weights、
細分、enclosure／certification、overhead 與新 target host；run 1 的 39 fixtures 不能補上。
264-call schedule 不代表正式 `B` cohorts 的費用。資源資格化延後，沒有主機重建授權。

## 6. 真實 selector 的確定性 witness：不完整結果

證據：[stage5c_structural_coordinate_design_witnesses.json](stage5c_structural_coordinate_design_witnesses.json)，
SHA-256 `6aff24d77ce196a123618eebf664fffa2518ab7956a2128ec0598b679a487d50`。
JSON 包含事前 plan 原文／hash、diagnostic runner 原文／hash、基線 source blobs、
已開始 case 的 exact coordinates／order／pairs
bytes與 hashes、atom／weight hashes、fixed／adaptive matrices、certified endpoint／error hex、
actual runtime 與 incomplete terminal。原證據版本 SHA-256 `a15455d19492f928478cb819fd4cad592b44a2aca46abe6b2b2fab1a6723aeab`
可由前一 head `ac3d0276` 取得；本次 JSON 只在 execution note 增補選項 B 的說明，
原 rows／cases／plan／runner／source hashes／runtime／terminal 及既有 note 欄位均不改。
它不是 run 1 證據，也不修改任何既有 assessment。

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

**已知預算配置問題。** 原腳本在同一 process 設 `RLIMIT_CPU=(180,180)`：
imports 與 12 個請求共用累積 CPU 預算，soft 與 hard 相同。
[run 1 §4](STAGE5C_6A_E_ITEM7_RESOURCE_RUN1_RESULTS.md) 先前已有 E4 wall 中位數
36.695758539 s、最長 258.568497097 s 的紀錄，phase CPU／wall 差最多 0.110598 s。
12 倍中位數約 440.35 s，單次既有最長值更已超過 180 s，所以 180 s 作為整輪預算
事前即規劃不足；這是已知的配置問題。跨 profile 數字只作規劃參考，不是本機 12 點
的 CPU 下界，也不能單憑它確證終止死因。CPU hard limit 是主要解釋，但保留
「死因未獨立確證」，不把推斷補寫為歷史測量。

未來任何另案診斷須事前審查，逐點使用短命子程序、CPU soft 嚴格低於 hard，
明列單點與總預算，由 supervisor 保存每點 start／result、signal、CPU／記憶體用量；
記錄寫入不與會被硬停止的 worker 共命運。這是未來設計要求，本次不改 runner、不執行。

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
證據；但這也不能否定真實 target 的飽和或證明效果良好。只完成同一 `u=v` 對稱 chain 的兩個 theta，
不是其他 cases／members 的分布證據。這組 coordinates 的每個 atom 都保持 sector-swap
對稱，scalar Gaussian 與 `pθ(u,v)=pθ(v,u)` 配合使精確 characteristic integrals 相等，
故第一分量精確為 0；表中極小非零數是既有浮點 producer 的 certified point，非一般
selector 的效果模型。此對稱性可直接由保存的 coordinate bytes 與已固定公式核對，
不是新增 numerical witness。point midpoint 不是精確 continuum truth：本案
第一分量 certified error 分別 0.10733285441070511、0.10338824640116889；
第二分量仍有原保守 error，未清零。這些不能當零 population variance 或 numeric-cap 合格。

**本輪採選項 B，不重跑或擴充診斷。** §5.1 的 O2／O13 未解義務留到效果模型設計，
任何後續計畫須在執行前審查 cases／member 適用性、完整 outcome、budget／stop policy
與 target-law 分析；若需 stochastic evidence，另立合法 manifest，不讀 scientific arms。
現有 10 個未完成請求維持無 outcome，不換案例、不追加預算或補跑。

## 7. 決策與後續審查界線

**依操作者選 B：本稿交付 exact-head 設計複核；保留 v0.2，延後 item 7 資格化。**
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

### 7.1 本週交付與 exact-head 複核清單

可複核交付是本設計、既有不完整 witness 加註說明與 STATUS；期限 2026-10-17（台北）。
標記 PR ready 是**待審設計已可複核**，不是科學結果、implementation review 或執行 GO。
本案完成文件檢查及新 head 的 CI 後，由操作者將 exact head／tree 交 Claude 複核：

- §2.1.1 的 operator → scalar pairing → actual fixed／adaptive／midpoint → primary →
  matching／CR1 證明是否完整，且版本／basis／boundary／E3／K 的作用域正確；
- §3／§4 的二維 singleton region、第一座標 coverage、ratio estimand、numerical width、
  局部／全域 conditioning 與未證前提是否分清，沒有把 Student reference 自動視為有效；
- §5 的 items 4–5／8 新交付與仍 OPEN 的義務是否完整，沒有藉恆零回收 alpha 或放寬 gate；
- §5.1／§6 明列 O2／O13 缺口、對稱 chain 的限制、已知預算配置與死因未確證是否相容，
  不完整 witness 是否完全沒有用於 coverage、effect、variance、cap、B 或可行性結論。
