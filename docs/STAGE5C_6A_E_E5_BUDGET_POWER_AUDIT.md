# Stage 5C — 6a-E E5 claim budget and power feasibility audit

狀態：**【item 8 部分交付／OPEN／不可執行】**。本文件與
`analysis/stage5c_e5_budget.py` 提議具名 family、lineage-wide 名目預算與 successor
reserve，並在不讀任何 arm data 的條件下檢查 E5-D／E5-E 的可證 power。
它不是 6a-E preregistration freeze；沒有生成 seed、開 arm ledger、形成 arm endpoint
或觸及候選 $K$。

## 1. 對既有 region forms 的完整 claim 清單

每個 original member $j=1,\ldots,11$，selection 與 confirmation **各自**有下列七個
有名的二維 region。region 的兩座標仍採 item 4／5 固定的 $p=2$ Bonferroni–Student
rectangle；一個 region 不等於兩次可自由挑選的單座標測試。

| Region claim | 座標 1 | 座標 2 | E5 power 義務 |
| :--- | :--- | :--- | :--- |
| E1 `T-plus - T-minus` | normalized dead zone 外，兩方向皆可 | normalized dead zone 外，兩方向皆可 | 預登記至少一個固定方向／座標的 alternative；不可由 selection data 選 |
| E2 `T-plus-null-A - T-plus-null-B` | normalized 等效 | normalized 等效 | E5-E，兩座標共同 |
| E2 `T-minus-null-A - T-minus-null-B` | normalized 等效 | normalized 等效 | E5-E，兩座標共同 |
| E3 `correct-chiral - sector-blind` | raw $>1/10$ | normalized 等效於 0 | detection 與同一 region 的等效分量 |
| E3 `symmetric-diffusion - sector-blind` | raw $<-1/10$ | raw $>1/10$ | 兩個 directional 分量 |
| E3 `correct-support - wrong-support` | raw $>g_*/2$ | normalized 等效於 0 | detection 與同一 region 的等效分量 |
| E3 `sector-blind-null-A - sector-blind-null-B` | normalized 等效於 0 | normalized 等效於 0 | 兩個等效分量；不是額外 detection |

E1 的實際 scientific rule 仍是**完整 rectangle 與 closed dead zone 不相交**；此表
要求預先給出 power model 的一個受保證座標，不修改 E1 的 existential acceptance rule。
E3 directional $1/10$ 與 $g_*/2$ 是 **raw** 門檻；等效分量一律使用
$D^{-1}$ normalized open box $(-1/20,1/20)^2$，其中 $D=\mathrm{diag}(3,1)$。
所以 sector-blind null 座標 1 的 raw 等效範圍為 $(-3/20,3/20)$，
不是 $(-1/20,1/20)$。全域 sector swap 是逐位元 invariance，E4 是
well-posedness；兩者均沒有擅加 statistical alpha 或 detection-power label。

## 2. 提議的 lineage-wide error allocation

固定名目總額 $\alpha_{\rm lineage}=1/20$。令 $r=0,1,\ldots$ 為同一 lineage
中已獨立 review 的 protocol instance 序號，$r=0$ 為 genesis；同一 $r$ 的 member、
split 與七個 claim 各有不可轉讓的獨立 cell：

$$
\alpha_{r,j,s,g}=\frac{1/20}{11\cdot2\cdot7\cdot2^{r+1}},
\qquad
\sum_{r\ge0}\sum_{j=1}^{11}\sum_{s\in\{\mathrm{selection},\mathrm{confirmation}\}}
\sum_{g=1}^{7}\alpha_{r,j,s,g}=\frac1{20}.
$$

Genesis 每個 region 的 rational allocation 是 $1/6160\approx0.000162338$；
第一個 successor 是 $1/12320$。每座標兩側臨界 tail 使用此 local alpha 的
$\alpha_{r,j,s,g}/4$。交給既有 region builder 的 binary64 值必須不大於 exact rational
allocation；轉換下溢即拒絕 scientific test。每個 local alpha 皆 $<0.01$。

原始 11 個位置及兩個 splits 即使未進場，也不能把空 cell 借給已進場位置。
scientific stage 啟動便將該 operation 的七個 cells 視為 burned；若 certification
stage short-circuit 且所有 scientific gates 均 `NOT-EVALUATED`，不虛報 scientific
spend，但原 cell 仍不得挪用。中斷、`INCONCLUSIVE` 或修訂使舊 categorical verdict
失效後，只有具名新 protocol 經獨立 review 才能從 §6.3 的最早未解決 operation
以 $r+1$ 的全新 cells 與 fresh streams 重作；永不重用或回收 $r$ 的任何預算。
後繼無上限時幾何級數仍不超支，但任何一次 run 的樣本量與資源上限須在其
第一次 seed 前另行固定；沒有足夠 power／binary64 allocation 時不授權啟動。
item 9 尚須把 generation、member、split、claim、spent／burned 實際接到 committed ledger。
此模組目前可 import 只供 candidate-independent 預算審計與測試，**不構成 runner
接線授權**；prereg §8 closure matrix 的 items 9／10 把 item 8 `CLOSED` 前禁止
manifest／seed builder、runner／adjudicator import 或呼叫本模組列為交付物，
並要求未授權接線的拒絕回歸。

這是對已固定 rectangle **名目** coverage 的 union bound；item 2 在
unequal-attrition CR1 下只主張 cluster-$t$ operational reference，未提供一般
finite-sample exact coverage theorem。因此不能把上式單獨宣稱為真實有限樣本
family-wise 錯誤率的證明。

## 3. Power audit 的正面公式與不能略過的前提

本節的 $Y$、$\widehat z$、$\mu$、$u$、$d$、$\eta$、SE 與所有公式
**一律使用 normalized 單位**。raw 座標 $k$ 的門檻、effect gap、數值半寬
進入公式前，必須各除以 $D_{kk}$。因此 chiral／diffusion 座標 1 的
raw $\pm1/10$ 對應 normalized $\pm1/30$，wrong-support 座標 1 的
raw $g_*/2$ 對應 normalized $g_*/6$；diffusion 座標 2 因
$D_{22}=1$ 仍是 $1/10$。若直接在 raw 座標 1 計算，contrast 值域
是 $[-3,3]$、SE 界為 $3\sqrt{8/(B-1)}$、tail 界為
$2\exp(-Bu_{\rm raw}^2/36)$；不可把 normalized 界套在未除以 3 的 gap 上。

每個 normalized cohort contrast $Y_{b,k}$ 只由 sharp endpoint support 可推出
$-1\le Y_{b,k}\le1$，**不能**從 pair count 192–384 推出 pair-level independence。
若另外證明 independent cohorts 在給定各 matched counts $m_b$ 後對固定 claim
有共同條件平均 $\mu_k$，則 $w_b=m_b/\sum m_b\le2/B$、
$\sum_bw_b^2\le2/B$；條件 Hoeffding 給出

$$
\Pr\{ |\widehat z_k-\mu_k|\ge u\mid(m_b)\}
\le2\exp(-Bu^2/4).
$$

不假設 covariance invertible，現有 CR1 的 marginal standard error 亦有保守的
確定界 $\mathrm{SE}_k\le\sqrt{8/(B-1)}$（由 $|Y_{b,k}-\widehat z_k|\le2$）。
因此如果 **事前** 對 normalized numerical half-width 有 $h_k^{\rm num}\le\eta_k$
的 CLEAN 保證，令 $q=t_{B-1,1-\alpha_{r,j,s,g}/4}$ 並在實作中使用 item 4
已認證的向上臨界值，單座標一側離門檻的 model gap $d_k$ 須滿足

$$
d_k>\eta_k+q\sqrt{8/(B-1)}+u
$$

才可透過上式與跨分量 union bound **反推** power-derived cohort floor。例如單個
E2 null claim、兩座標共同 $\mu_1=\mu_2=0$ 時，若兩座標的
$u_k=1/20-\eta_k-q\sqrt{8/(B-1)}>0$，可用
$2e^{-Bu_1^2/4}+2e^{-Bu_2^2/4}\le0.10$ 作充分條件。必須與
$B\ge32$ 的結構 floor 取較大者；不能由 $m\ge192$ 替代 $B$。

這個計算**目前不能填入 cohort 整數**：共同條件平均模型尚未證明，CLEAN 只給
個別 validated error 而未給所有七個 claim 的事前有限 $\eta_k<\delta_E$，
也沒有任一 C8 member 的 E1 effect $\mu$ 與 dead-zone 邊界間的正 gap。
E3 continuum planted algebra 的 $1/5$ 與 $g_*$ 是解析 control gap，
但未證明它們在 finite matched-cohort law 下保留成同樣的條件平均／variance
與數值半寬；不能以 algebra gap 直接替代 E5-D 的 sampling model。

兩個不用 arm data 的反例把阻塞說清楚：

1. E1 的 model 若真實 normalized effect 恰在 $\mu=(1/20,0)$，它屬於既有
   closed dead zone。任何覆蓋該 $\mu$ 的 rectangle 都不能通過 E1；在
   equal-count independent Gaussian cohort oracle 下，E1 PASS 機率至多
   此 local alpha，與 cohort 數無關，因此不能達 $0.90$。
2. 任一 E2 normalized coordinate 若 CLEAN 的 $h_k^{\rm num}\ge1/20$，則
   $|\widehat z_k|+h_k^{\rm stat}+h_k^{\rm num}\ge1/20$；open-box strict
   equivalence 對任何 $B$ 都不可能 PASS。現有 CLEAN 契約沒有小於 margin
   的統一上限。

### 3.1 已封存 live E4 的兩種 numerical-cap 阻塞

`tests/test_stage5c_e5_numerical_cap_feasibility.py` 使用唯一解析 Gaussian atom
$(u_x,v_x,u_y,v_y)=(0.55,0.55,0.45,0.45)$、權重 1、$\theta=+0.4$。
此 atom 嚴格在 unit box／causal pair domain 內；item 7 的 fixed-scale E4
雙 implementation、cell enclosure、leakage 與 item 3 producer-sealed certification
全走正式計算路徑。兩路 live estimates 另綁為只有 audit identity 的單筆
`EndpointCertificationSourceRow` 並重新認證，誤差逐位元相同，無正式 arm pool。
box／causal retained mass 分別約為 $1$／$0.7587$；
E4 與 certification 都是 `CLEAN`，$L\approx2.74169>0$，但該單列的
endpoint-error normalized 上界約為 $(0.08454,0.10145)$，**兩座標皆超過
E2 的 $1/20$ margin**。這是 candidate-independent planted input，沒有正式
arm identity、seed、matching 或 arm endpoint；單列反例只推翻「所有 CLEAN row
必自動小於 margin」，**不冒充一個已執行的 E2 arm verdict**。

另一個 candidate-independent 單 atom $(0.80,0.80,0.20,0.20)$、權重 1、
$\theta=+0.4$，沿用相同的 E4 producer、audit-only source-row binding 與
`certify_pairing` 路徑，E4／certification 仍為 `CLEAN`。重算的 causal leakage
約 $1.14\times10^{-11}$（極小，但非嚴格零），兩實作 agreement distance
約 $3.42\times10^{-10}$；然而 norm enclosure 為
$[2.89\times10^{-10},6.35\times10^{-10}]$，上／下界比約 $2.197$，
certified endpoint-error normalized 上界約 $(3.785,4.543)$，遠超 $1/20$。
作為區分絕對大小與相對寬度的對照，同一路徑的
$(0.90,0.90,0.10,0.10)$ norm 更小（約 $10^{-17}$），上／下界比卻約
$1.038$，normalized error 約 $(0.064,0.077)$。這些數字是 planted
diagnostics，**不是** E2 arm 的分布、$\Pr(C)$ 樣本或正式 endpoint。

第一個 atom 的兩實作 agreement distance 約 $5.01\times10^{-5}$，causal
leakage 約 $0.2413$，但 frozen cell enclosure 每個 sector 的寬度約
$0.09215$：直接阻塞數值 cap 的是 cell／causal-boundary enclosure 的寬度，
**leakage diagnostic 本身沒有直接加到 ErrorBudget**；兩者在此例相關，
不可把 leakage mass 當成誤差的不可降低下界。第二個 atom 的 cell enclosure
每座標寬僅約 $3.01\times10^{-12}$；兩實作雖只差
$3.42\times10^{-10}$，adaptive estimate 卻顯著偏離約
$[4.459,4.489]\times10^{-10}$ 的 validated analytic cell enclosure；
frozen adaptive cubature 的絕對容差 $2^{-30}\approx9.31\times10^{-10}$
甚至大於該 pairing 量級，該輸入的 solver 以零次 subdivision 回報
`converged`。其 solver error estimate 只是 diagnostic，沒有被當成
validated ErrorBudget；正式誤差由 analytic cell enclosure 的 farthest corner
產生。item 7 `STAGE5C_6A_E_WELLPOSEDNESS.md` §6 已有 regression：
即使 adaptive 自評 error 小於 validated enclosure error，`ErrorBudget`
仍取後者以防 estimated-error undercoverage。因此此處 adaptive 精度不足
會擴大 validated error、壓低 detection power，**不構成悄悄縮窄 region
的 validity 證據**；solver `converged` 也不授權使用其自評 error 代替證明。
item 3 允許此 agreement 並以 midpoint／error-ball 傳到近零分母，
使 certified norm upper/lower 比達 $2.197$。因此這裡的「相對寬度」指
**最終 norm enclosure**，不是 E4 analytic cell enclosure 自己很寬。
僅改善第一種 cell／boundary enclosure，不能由此證明第二種也符合 cap；
第二種須審查 adaptive cubature 精度與相對 norm 認證在目標輸入律下的行為。

#### 聚合尺度與收緊界的 candidate-independent 探查

同一 E4 producer 與 audit-only sealed-row 認證的固定輸入（每列等權、
$\theta=+0.4$）顯示：增加**有顯著 pairing norm** 的 atom 可以稀釋第二種
單點病態；單純增加 atom 數並不保證這件事。下表只是構造例，沒有
6a-E arm、matching、seed 或 $\Pr(C)$ 估計：

| 固定 Gaussian mixture centres | atom 數 | causal leakage | certified norm 下界 | normalized error 上界 |
| :--- | ---: | ---: | ---: | :--- |
| $(.8,.8,.2,.2)$ | 1 | $1.14\times10^{-11}$ | $2.89\times10^{-10}$ | $(3.785,4.543)$ |
| 上列＋$(.6,.6,.4,.4)$ | 2 | $0.0118$ | $0.233$ | $(0.0177,0.0213)$ |
| 上列＋$(.801,.801,.199,.199)$ | 2 | $1.05\times10^{-11}$ | $2.60\times10^{-10}$ | $(4.107,4.929)$ |
| $(.55,.55,.45,.45)$ | 1 | $0.2413$ | $2.742$ | $(0.08454,0.10145)$ |
| 同一 $(.55,.55,.45,.45)$ 重複四次 | 4 | $0.2413$ | $2.742$ | $(0.08454,0.10145)$ |

最後兩列的 mixture density 完全相同，故 repeated atom 不會自動產生
$1/\sqrt m$ 的數值誤差衰減；causal leakage 是混合質量分率，亦無此
通用衰減。但其他配置可以改變 bound，表中的二點改善不是
「(b) 對所有多 atom arm 自動消失」的證明；item 2 的 matched selection
也不能由 $m\ge192$ 直接推出 pairing norm 的非退化下界。
`tests/test_stage5c_e5_numerical_cap_feasibility.py` 現把前述單 atom、
稀釋與不稀釋的兩點混合，以及 repeated near-diagonal atom 釘為回歸。

為界定下一步的工程可行性，僅在**開發期敏感度探查**沿用
`_level_pairing_enclosure` 的正值 cell 計算，對原本 frozen 的 16／32／64
levels 另試 128 與 256 cells，使用相同兩路已算好的 implementation
estimates 重算 error-ball。這些額外 level **不屬** item 7 的正式
producer／經 review 的資源上限，重算數值不構成新的 `CLEAN` 認證或 cap：

| 單 atom | frozen 64 cells 的 normalized error | 試探 128 cells | 試探 256 cells |
| :--- | :--- | :--- | :--- |
| $(.55,.55,.45,.45)$ | $(0.08454,0.10145)$ | $(0.04010,0.04812)$ | $(0.01956,0.02347)$ |
| $(.8,.8,.2,.2)$ | $(3.785,4.543)$ | $(3.730,4.476)$ | $(3.704,4.444)$ |

此探查表明 near-diagonal 例可藉 cell-bound refinement 降到每座標
$1/20$ 以下；**這既非全體輸入的 uniform bound，也不足以保證雙臂
numerical errors 相加、統計半寬與完整 split power 通過。**
近零例的額外 cell 細化效果有限，因 adaptive implementation 自身與
窄 cell enclosure 的分歧佔主要誤差；其精度和可用資源需另行研究。
在此固定單 atom 的開發期探查，64→128→256 cells 時首例兩路 validated
quadrature errors 大致隨 cells 倍增減半；這是**單例趨勢，不是全輸入
$1/n$ 誤差定理**。cell traversal 的 pair／pair／transverse 網格數為
$O(n^3)$；額外 128、256 cells 在本地分別約需 $0.1$、$1$ 秒，獨立
複核的同例 512 cells 約 $9.3$ 秒、1024 cells 在其容器觸及記憶體上限。
時間／記憶體是開發環境觀察，不能直接當作正式 resource cap 或所有 mixture
的成本律，尤須先在 E4 最多 8128 atoms 的 domain 上審核。

數值半寬與 cohort floor 共享同一個 $1/20$ 等效 margin。在**純示例**中，
若同一 planted row 填滿左右兩臂且兩側各有相同的 normalized error 上界
$\eta$，則 item 4 的 matched-error triangle propagation 給出的雙臂半寬
為 $2\eta$。此例不是 item 2 實際 matched arm；用 genesis local
$\alpha=1/6160$ 的 §3 保守功效算式，須有

$$
u(B)=1/20-2\eta-q(B)\sqrt{8/(B-1)}>0,
\qquad 4e^{-Bu(B)^2/4}\le0.10,
$$

其中 $q(B)$ 必須由 frozen 向上認證的 Student 臨界值給出。上表首例
在 64／128 cells 的 $2\eta$（取較大的第二座標）約為 $0.20290$／
$0.09624$，故**這個固定示例**即使 $B\to\infty$ 亦不滿足 open-box
PASS 必要的 $2\eta<1/20$；不能據此斷言所有 frozen 64-cell E2 arms
都不能 PASS。256 cells 的 $2\eta\approx0.04694$，餘裕約 $0.00306$；
只用這個最壞情況 Hoeffding 充分條件、甚至假設 $q(B)=0$，也須
$B>1.57\times10^6$ 才可能滿足該算式，實際 $q(B)>0$ 只會提高
算式所需 $B$。**這是特定 planted 示範的保守證明成本，不是實際
matched-null power 的最小樣本數、正式 cohort floor 或可行性估計。**

上述兩條改善路徑都會改動 item 7 已 `CLOSED` 的凍結面：§4 的
$(16,32,64)$ enclosure levels／producer identity，或 §5 的 adaptive
`atol`／resource cap。**item 8 不能自行把試探常數接入正式 producer。**
若以修改 E4 producer 承擔 cap feasibility，先須有明文 item-7 amendment，
獨立 review、CI，及對 item 3 certification、items 4／5 source-row／region
傳播和後續功效義務的影響複核；item 7 已有的 `CLOSED` 不能充當新版本授權。
另一個仍待證的途徑是在**不更動 frozen E4** 下，證明現有 producer
對事前 matched-null law 的 cap 成功機率和條件分布足夠；單 atom 反例
沒有排除這條途徑。兩條途徑均不解除 6a-E execution firewall。
先做 candidate-independent producer-bound 的收緊與資源可行性研究，
再論證完整 matched-null 輸入律、$\Pr(C)$ 與 cap；不得從這些 planted
例子直接選 $\eta$ 或 $B$。

若另登記 numerical cap $\eta_k<1/20$，必須在任何正式 seed 前定義它的
producer-bound、normalized 計算、拒絕理由、evaluation 時序與資源上限；
兩個反例證明它必排除至少一部分原本 `CLEAN` 的 item-7 合規輸入。
設 $C$ 為完整 split 的 certification／cap／cohort preconditions 全通過事件。
cap feasibility 須分別回答：(a) cell／causal-boundary enclosure 收緊後，完整 split 的
certification-success event $C$ 有何可證下界；(b) 不讀 6a-S／6a-E arm
data，如何在 E2 null matched-cohort law 下控制 near-zero norm
enclosure 的高相對寬度及 adaptive 誤差，並將其失敗機率計入同一個 $\Pr(C)$；
不能以 atom 數下界取代這兩項證明。
於是 $\Pr(\mathrm{E2\ PASS})=\Pr(C)\Pr(\mathrm{E2\ PASS}\mid C)
\le\Pr(C)$；因此單有「在 $C$ 上半寬小於
margin」**不能**推出完整 split 的 power $\ge0.90$。還須獨立證明
$\Pr(C)$ 的下界，以及受 matching／cap conditioning 後的 null 均值與
cohort distribution，且兩項機率下界的乘積須 $\ge0.90$；各自
$\ge0.90$ 僅保證乘積 $\ge0.81$。否則 §3 的 Hoeffding floor
只屬條件性算式。
本交付不選擇 $\eta_k$、不把已形成 region 的邊界 `FAIL` 改寫成
`INCONCLUSIVE`，也不從單一 planted witness 推估 $\Pr(C)$。

### 3.2 Frozen E4 的 raw-to-matched 數值誤差律：不生成 seed 的橋接

對每個已凍結的 C8 selector 位置 $j\in\{1,\ldots,11\}$、target
$\theta\in\{-0.4,+0.4\}$ 及待固定的 causet cardinality $N$，令
$U=(X_1,\ldots,X_N)$ 為 iid $p_\theta(u,v)$ 座標，$O(U)$ 為它們的
causal order。先以 **order-only** $\Sigma_j(O(U))$ 選 typed ordered pairs，
再由 evaluator 取回座標，形成

$$
r_{j,U}(z)=\frac{1}{|\Sigma_j(O(U))|}
\sum_{(i,k)\in\Sigma_j(O(U))}
\gamma_{1/16}\bigl(z-(X_i,X_k)\bigr).
$$

此處 $\gamma_{1/16}$ 是 item 7 固定的四維 mass-one Gaussian；它使用
$\varphi=1$、$\mathcal N=|\Sigma|$，每個 causet **各自**正規化，
不得以所有 causet 的 pair 總數重新正規化。令 $e_{j,N,\theta}(U)$
為 frozen E4／item-3 producer 對此 mixture 給出的兩座標 **raw**
`endpoint_error`；最後須按 item 4 的 outward `ENDPOINT_RANGE_WIDTHS`
正規化後才和 $1/20$ margin 比較。選取失敗、E4 非 `CLEAN`、
item 3 非 `CLEAN` 或 E4 atom cap 不符時，為了機率計算記
$e_{j,N,\theta}(U)=+\infty$。這是**未執行的數學推前映射**，
不是一個 6a-E arm row 或 endpoint。

item 7 的 `E4_MAX_ATOMS=8128=\binom{128}{2}`。因為每個 selector
只選不重複的 strict causal ordered pairs，$|\Sigma_j(O(U))|\le\binom N2$；
**$N\le128$ 是對所有 causet／member 保證不觸及 atom cap 的充分條件**。
$N>128$ 並非一律拒絕：仍有 pair 數不超過 8128 的個別輸入；
若要採用此範圍，必須把超額拒絕算進下述 tail 並另外審查資源。
這個算術上界不自行凍結 6a-E 的 $N$，也不保證 selector 或 E4 `CLEAN`。

raw 單 causet tail 定義為

$$
p_{j,N,\theta}(a)=
\int_{([0,1]^2)^N}
\mathbf1\{e_{j,N,\theta}(U)\not\le a\}
\prod_{i=1}^{N}p_\theta(X_i)\,d^{2N}U,
$$

其中向量 $\le$ 逐分量解讀。這是無 seed 的完整定義，**目前沒有算出
任何分位數或可用的上界**；不能用 §3.1 的 planted atom 表代入
$p_{j,N,\theta}$。item 2 的 2048-replication covariance calibration 使用
抽象 bounded endpoint oracle，不評估上述 frozen E4，故不能從其 coverage
或 covariance 表讀出 $p_{j,N,\theta}$。

正式 E2 null claim 的對象還包括兩臂 evaluation pools、獨立 calibration
pools、feature 尺度、Hungarian matching、unmatched 與 matching `CLEAN`
條件。令每臂 raw evaluation pool 有 $L$ 個 iid causets、$G$ 為完整
matching `CLEAN` 事件，$M$ 為其 matched pair 數；對 matched rows，item 4
給的完整 split **raw** 數值半寬為

$$
h^{\rm num}=\frac1M\sum_{(i,k)\in\mathcal M}
\bigl(e^L_i+e^R_k\bigr).
$$

只知道 raw $p_{j,N,\theta}(a)$ **不能**把 matched rows 當 iid raw
樣本：matching 依所有 pool 的 features 選 indices。仍有不依賴
選取獨立性的嚴格但可能很鬆的充分界：當兩臂同 target、每臂上界
皆為有限非負 binary64 raw 向量 $a$，所有 $2L$ 個 raw rows 均通過時，
$G$ 下 item-4 exact-rational pair addition／outward rounding 仍給
$h^{\rm num}\le2a$（此量級 $2a$ 可精確表示）；因此

$$
\Pr\{G,\ h^{\rm num}\le2a\}
\ \ge\ \Pr(G)-2L\,p_{j,N,\theta}(a).
$$

這是對 raw bad-row events 的 union bound，**不是**已取得的
$\Pr(C)$ 下界：右側的 $\Pr(G)$ 和 $p_{j,N,\theta}(a)$ 目前均未證明，
還沒有固定 6a-E 所需的 $N$、每臂 $L$、candidate cap $a$、
各 split/cohort 的配置與資源限制。C8.1 的 $N=96$、pool $768$
是既有 matchability feasibility benchmark，不得默認為全部 6a-E
正式 streams；6a-S 的 $N\in\{64,96,128\}$ 也不自動固定
6a-E 的 $N$。若要得到 normalized cap，還須按 item 4 對
$h^{\rm num}/D$ 向上取界，並留足嚴格 $1/20$ boundary 的 rounding slack。
完整 $B$-cohort 成功率須在匹配、認證與 cap 的聯合律下
另行界定；即便先取得這個數值門檻事件的下界，cap conditioning 後的
null 均值、cohort 變異與 §3 的 power 仍需獨立證明。

此界的主要鬆弛在「**全部 $2L$ 個 rows 均不超標**」這個充分條件，
而不是稀有超標事件的 union bound 本身；matched errors 的平均值
即使包含少數較大值，也可能落在 cap 內。若另行證明所有**已認證的**
rows 有逐座標有限共同上界 $a_{\max}\ge a$，且 $k$ 定義為含至少一個
超過 $a$ row 的 matched pairs 數，則在 matching `CLEAN`、全部 matched
rows 認證成功的事件上可用
$h^{\rm num}\le2a+(2k/M)(a_{\max}-a)$。對選取失敗或 E4／item 3
非 `CLEAN` 而記為 $+\infty$ 的 rows，這個有限界**不能**套用；
須另行控制失敗事件，亦不能改寫成一個可通過的 finite-error row。
這只是候選改善方向，現無 $a_{\max}$、$k$ 的 law 或相應 cap。

原界要有正的下界，至少需 $p_{j,N,\theta}(a)<\Pr(G)/(2L)$。
例如僅以歷史 C8.4 的 $L=768$ 代入，且 $\Pr(G)\le1$，
必要條件為 $p<1/1536\approx6.51\times10^{-4}$；這不是該
benchmark 的實測 $p$。調大 $L$ 可能在某些設計改善 matching，
同時也增大 $2Lp$ 罰項；$\Pr(G)$ 對 $L$ 的單調性並未證明，
不得由單點 benchmark 斷言最適 $L$。用普通 iid Monte Carlo
就算 $R=2048$ 且零次超標，單一 tail 的 99.9% 單側 exact
binomial 上界仍是 $1-0.001^{1/2048}\approx0.00337$，
無法使 $L=768$ 的此界非空；多個 member／threshold 的同時推論
還會更難。因此在承諾大規模計算前，必須先審查所需精度與資源。

**非空與足夠完整 split power 是不同的資源目標。** 假設歷史
$L=768$、至少 $H=B=32$ 個 cohort、最佳情況 $\Pr(G)=1$、
各 cohort 同一上界 $p$；若完整 split numerical-success 下界
$c\ge0.90$，原 union bound 即要求

$$
p\le\frac{1-c}{2LH}
\le\frac{0.10}{1536\cdot32}
\approx2.03\times10^{-6}.
$$

只為**單 cohort 下界非空**而估的 $R\sim2\times10^4$／stratum
並不滿足這個任務。即使 $G$ 真為 1、所有觀察零超標，若為
11 members × 2 targets × 3 個 $N$ × 8 個 grid points 共
528 個事前 CI cell 等分 $\delta=0.001$，exact-binomial 上界要
降到上式以下，至少約 $6{,}476{,}680$ 次**每 stratum**；
66 個 strata 共至少約 $427{,}460{,}880$ 次 frozen E4 評估。
同一 stratum 的一批 causets 可供 8 個 grid 門檻共同評分；
grid 只分攤 $\delta$，**不**將 E4 呼叫數再乘以 8。
這只是示例組態與零超標的**樂觀下限**：實際 $\Pr(G)<1$、
$c>0.90$（因 conditional power $d<1$）、$G$ 的信賴額度、
額外 splits 或任一超標都會加重負擔。依獨立 reviewer 在單一
容器的 1024／4096-atom timing $31.8$／$101.9$ 秒／次，
若粗略外推會達約 $3.8\times10^6$–$1.21\times10^7$
core-hours；這些 timing 未經正式 resource review、不能當成
8128-atom domain 的成本律。結論只針對目前的**全 raw-pool
零超標 union bound + 普通 iid exact-binomial估計**；不能由此
宣稱 frozen E4 或其他平均誤差界在統計上無望。

另見 `STAGE5C_6A_E_FROZEN_E4_SCREEN_PROTOCOL_DRAFT.md`：
少量真正的 $r_{j,U}$ 可以事前篩掉明顯阻塞，但零次超標
不會估出 $p\sim10^{-6}$，也不能以 pilot 數值反選 cap。

#### 3.2.1 估計前的預登記閘門（尚未完成，不授權執行）

若要以 hard-control Monte Carlo 而非可證的積分界填入上述未知量，
須**在任何診斷輸入生成或 frozen E4 評估之前**另立已 review／merge 的
audit-only 協定，逐項凍結：$j,N,\theta$ 全部 strata、每臂 raw
evaluation／獨立 calibration pool 的 $L$、每 stratum 的 iid raw
replications $R_p$ 與 full-split replications $R_G$、E4／matcher
source digests、runtime 與資源停止條件、diagnostic seed 的來源／
專用 namespace／與既 burned 及未來正式 seed ranges 的互斥證據。
正式 6a-E 的 $N,L,B$、每個 claim/split 對應的 cohort 操作數 $H$
與此 audit design 的關係亦須事前固定；
diagnostic seeds 不得借名成為正式 arm streams，失敗或資源不足
不得挑選有利 strata 重跑。

同一協定還須**在看任何 $e(U)$、matching outcome 或 pilot diagnostics
之前**固定一個有限、有序的 binary64 raw candidate grid $\mathcal A$
（每座標經 item-4 outward normalization 後須與 $1/20$ 留有嚴格
slack）、同時信賴額度 $\delta$、full-split numerical-success 目標
$c$ 與 conditional-power 目標 $d$（要求 $c\,d\ge0.90$）。
計數時每個失敗 producer 依本節 $+\infty$ 約定算超標，不丟掉失敗列；
對每個 $a\in\mathcal A$ 與 stratum，以事前指定的 one-sided exact
binomial／Clopper–Pearson 同時上界 $U_p(a)$，對 matching `CLEAN`
以獨立完整 pool replications 的同時下界 $L_G$；各格與各
strata 的 $\delta$ 分配須預先固定。對事前列出的每個 cohort 操作
$h=1,\ldots,H$，令保守下界
$q_h(a)=\max\{0,L_{G,h}-2L_hU_{p,h}(a)\}$。不需要 cohort 獨立性，
union bound 即給整個 split 的 numerical-success 機率下界
$1-\sum_{h=1}^H[1-q_h(a)]$（為負時截為零）。
選擇規則是依**預先固定**的 grid 順序，取第一個在全部預定
claim／split 均滿足 $\sum_h[1-q_h(a)]\le1-c$、normalized
cap 的嚴格 slack 與預登記資源限制的 $a$；若不存在，紀錄
`NO-FEASIBLE-CAP`，不得據結果延長 $R$、移動 grid／$L$／$N$、
改變 $c,d,\delta$ 或轉而使用 seeded diagnostic 作正面 power 證據。
即使有候選 $a$，仍須另證 cap-conditioned null law 與 $d$；
映射規則本身不授權設定正式 $\eta$ 或 $B$。

**本 PR 只預先規定協定必須具備的欄位與映射形式，沒有固定上述
grid、$R_p,R_G,\delta,c,d$、seed bases 或資源上限，因此不是
已完成的估計預登記，也沒有產生任何 Monte Carlo 結果。**
可先用預先固定的真實 $r_{j,U}$ 診斷輸入做 candidate-independent
可行性篩檢，但若事先沒有將其來源、輸出及隔離規則凍結，
結果只能作不承重的探索；不能從診斷誤差反選 $a$，或以單個
mixture 推斷 $p$。超出此協定的路徑只能版本化修訂、使用全新
互斥的診斷 streams，並接受獨立複核。

### 3.3 Averaged-error 路徑的兩個承重 gate 與 factor audit

全 raw-pool 零超標界把「平均 numerical half-width」換成「最大列不得
超標」，因而產生 $LH$ 尺度的 rare-tail 負擔。改用 averaged error
只能改善**有限 CLEAN 誤差的大小聚合**；它不能改變現有 adapter 對
原始 pool 完整性的要求。以下兩個 gate 必須分帳，而且 Gate A 先於
Gate B 承重。

#### Gate A：原始 pool 必須逐列、連續、全部 `CLEAN`

`CertifiedEndpointPool.__post_init__` 要求 producer-bound row indices
從零連續覆蓋原始 pool，且每列都同時滿足 `status is CLEAN` 與
`is_clean`。因此任一 raw row 非 `CLEAN` 即拒絕整個 pool；matching
是否選中該列無關。若單列 failure 機率為 $p_{\rm fail}$，在 $H$ 個
cohorts、兩臂、每臂 $L$ 列下，僅靠 marginal tail 與 union bound 有

$$
\Pr\{\hbox{all source rows CLEAN}\}
\ge 1-2LH\,p_{\rm fail}.
$$

故僅為此 gate 留下 $c_{\rm clean}\ge0.90$，在 $L=768,H=32$ 的
樂觀示例也已要求

$$
p_{\rm fail}\le\frac{0.10}{2\cdot768\cdot32}
\approx2.03\times10^{-6}.
$$

完整 power 還要分配 matching、finite-width 與 conditional power，實際
額度只會更嚴。除非另證 frozen producer 在所採 admissible support 上
**確定性 `CLEAN`**，或以可負擔且事前固定的協定取得足夠 failure-tail
上界，Gate B 的任何 averaged-error 結果都不能形成完整 split 的正面
證據。不得把 non-`CLEAN` 列丟棄、改成有限誤差或交給 matcher 避開。

#### Gate B：CLEAN 條件下的誤差大小與放大因子

在 Gate A 成立時，令

$$
x^A_{hi,k}=e^A_{hi,k}/D_{kk},\qquad A\in\{L,R\},
$$

為 cohort $h$、arm $A$、row $i$、座標 $k$ 的 normalized endpoint
error，$M_h$ 為該 cohort matched pairs，
$M_{\rm tot}=\sum_hM_h$。非負性與 matched rows 為 raw pool 子集給出
不需要任何 selection independence 的確定界

$$
h^{\rm num}_k
\le
\frac{\sum_{h=1}^H\sum_{i=1}^L
 (x^L_{hi,k}+x^R_{hi,k})}{M_{\rm tot}}
\le
\frac{L}{m_{\min}}
 (\bar x^L_k+\bar x^R_k),
$$

其中 $M_h\ge m_{\min}$，$\bar x^A_k$ 是該 arm 全部 $HL$ 列的
sample mean。若兩臂同 law 且共同 mean 為 $\mu_k$，歷史
$L/m_{\min}=768/192=4$ 對應 expectation-scale coefficient
$\kappa_{\rm pool}=8$；在零 statistical-width 極限
$h_k^{\rm num}<1/20$，故此界至少需要

$$
\mu_k<\frac{1/20}{8}=\frac1{160}=0.00625.
$$

較緊但仍 selection-agnostic 的確定界，是把每臂 selected sum 以該
pool 最大的 $M_h$ 個 errors 之和（top-$M_h$ sum）取代。令 top mean
相對 full-pool mean 的 amplification 為 $r^A_{h,k}$；只要分母非零，

$$
1\le r^A_{h,k}\le L/M_h.
$$

兩臂合計 factor 的理想下限是 $\kappa_{\rm top}=2$，而
$M_h/L\ge1/4$ 時粗略上限回到 $8$。所以任何**只使用 raw error law、
不利用 matcher--error 關係**的 worst-subset 上界要在理想 factor 下
留下零 statistical-width 餘裕，至少須有

$$
\mu_k<\frac{1/20}{2}=\frac1{40}=0.025.
$$

這是該類 worst-subset **上界**的必要條件，不是實際 matched error
對所有 matching 機制的必要條件。若 matcher 系統性選到 low-error rows，
實際 matched mean 可以低於 raw mean，等效 factor 甚至可低於 2；但此時
必須交付 feature／error／matched-index 的 joint law 或另一個可審查的
matching-conditioned 證明，不能由 raw mean 或少量 diagnostics 預設。
反之，top-$M$ factor 接近 2 也不能未證先用。**factor 本身是獨立研究
對象**：先界定它能從 8 收到多少，可能比直接加密 E4 cells 更便宜。

一項未預登記、不可承重的 reviewer 診斷在 $N=64$、單一 target、
五個 selectors、兩個自行選取 seeds 的十筆輸入上回報 screen scalar
$\bar v\approx0.060$，其中 $v=\max(e_1/D_{11},e_2/D_{22})$。它不是任何
$\mu_{j,N,\theta,k}$ 的估計，不能
關閉路徑、選 cells 或反推 cap；只可說明量級稽核值得先做。若僅作
工程尺度假設，且 error 暫按 $1/\text{cells}$、成本按
$\text{cells}^{3.3}$ 外推，$0.060\to0.025$ 約為 154 cells／現行
成本 18 倍，$0.060\to0.00625$ 約為 615 cells／成本
$1.7\times10^3$ 倍。這些不是 item-7 amendment 的核准常數或資源律；
factor 若能接近 2，約 154 cells 的方向不可因最保守界而提前排除。
更具體地，對 $x_k=e_k/D_{kk}$ 有
$E[\max(x_1,x_2)]\ge\max(E[x_1],E[x_2])$；screen scalar $v$ 的
mean 不小於任一 per-coordinate mean，且一般會嚴格偏高。
因此 $v$ 只供既有 screen 分帶，**不得**代入下述 mean／factor audit、
不得與 per-coordinate 的 $1/160$ 或 $1/40$ 門檻比較，也不得用其
truncated mean 否決任一座標。即使一批探索資料的兩個座標各自也超標，
仍須以各自預先登記的 $x_k$ 統計量承重，不能由 $v$ 倒推。

#### Mean／factor 估計的事前協定義務

$\mu_{j,N,\theta,k}$ 是指定 generator law 下的分布期望，不是
「admissible inputs」集合本身的確定性平均。任意 planted mixtures、
任意 seeds 或跨 strata 混合都不能估它。若估計結果要正式否決一個
factor-bound，必須在呼叫 generator 前由獨立 review／merge 固定：

1. 每個承重的 $j,N,\theta,k$ strata 與其 generator／selector／E4／item-3
   source blobs；audit 統計量必須逐座標使用 $x_k=e_k/D_{kk}$，screen
   scalar $v=\max(x_1,x_2)$ 只供分帶、不得代入 mean／factor audit；不得把
   未來 arm data 或 item-2 abstract endpoint oracle 代入；
2. replications、diagnostic seed provenance、跨 strata／座標的 simultaneous
   confidence allocation、resource stop 與缺失／non-`CLEAN` handling；
3. factor 對應的判定門檻、固定最大樣本數與停止規則；同一 seeds 的精確
   replay 可供重現，任何新增樣本、延長或改 strata 都須 amendment；
4. `NO-BOUND-OBSTRUCTION` 只代表該協定未否決指定 factor-bound，不能作
   frozen E4 可行、cap 已取得或 matching-conditioned law 成立的正面證據。

這是設計參數 audit，不 claim 新的 one-shot scientific namespace；但
「不是 scientific verdict」不等於可事後增抽或挑選 seeds。若只需保守
**否決**，可對各座標事前固定有限 $\tau_k$ 並估計
$Z_{\tau,k}=\min(x_k,\tau_k)$：因 $E[x_k]\ge E[Z_{\tau,k}]$，bounded one-sided lower
confidence bound 高於 $(1/20)/\kappa$ 足以否決「以該 factor 與 raw mean
作正面 cap 證明」所需的 population-mean 條件，且不需假設 $x_k$ 有 uniform
finite upper bound；它不否決實際 matcher 可能選到較小 errors。反方向不成立：lower bound 未超標
或 clipped mean 很小，不能證明 $E[x]$ 小；正面 feasibility 仍須 tail／moment
控制、matching-conditioned law 或確定性上界。

因此第三條路徑的順序改為：先處理 Gate A；再以純分析界定 factor，
只在必要時執行已固定的 mean／factor audit；若指定 worst-subset bound
被否決，應比較 matching-conditioned 證明與 item-7 amendment，而非把
「某個 bound 失效」擴張為所有 averaged-error 或 matching 路線失效。
只有兩者皆不可行時才轉入 claim redesign。本節不呼叫 generator、
不配置／生成 seed、不設 cap 或 cohort floor，也不授權第二輪 screen。

閉合 item 8 須先取得不接觸 6a-S／6a-E arm data 的 E1 positive-gap model，
每一 E3 finite-cohort directional／equivalence effect model，以及所有 E2/E3 null
claims 的事前 worst-case distribution／variance、numerical cap 及其
certification-success probability／conditioned-null model，逐 claim 計算
selection、confirmation 和已預留 successor 的 $B$ floors，連同可負擔的資源上限
提交獨立 review。**item 8 保持 `OPEN`；items 9、10、12 保持 `OPEN`，item 11
保持 `DRAFT`，6a-E 保持 `PREREGISTRATION-INCOMPLETE`。**
