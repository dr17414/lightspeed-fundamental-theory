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
產生。
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

閉合 item 8 須先取得不接觸 6a-S／6a-E arm data 的 E1 positive-gap model，
每一 E3 finite-cohort directional／equivalence effect model，以及所有 E2/E3 null
claims 的事前 worst-case distribution／variance、numerical cap 及其
certification-success probability／conditioned-null model，逐 claim 計算
selection、confirmation 和已預留 successor 的 $B$ floors，連同可負擔的資源上限
提交獨立 review。**item 8 保持 `OPEN`；items 9、10、12 保持 `OPEN`，item 11
保持 `DRAFT`，6a-E 保持 `PREREGISTRATION-INCOMPLETE`。**
