# Stage 5C — 6a-E joint matched law and paired covariance

狀態：**【candidate-independent closure item 2／REVIEW-PENDING／不可執行 arm】**。

本文件固定 C8 的 generator／matcher source-of-record、matching certification 邊界、joint
matched-pair law 與 paired covariance schema。對應 executable source 為
`analysis/stage5c_joint_matched_law.py`，regressions 為
`tests/test_stage5c_joint_matched_law.py`。

本交付物沒有讀取任何 arm ledger、沒有生成或 claim 正式 6a-E seed、沒有形成 arm endpoint、
沒有設計候選 kernel $K$，也不選擇 E1／E2 的 scientific region、effect floor、equivalence
margin、multiplicity 或 power allocation。後五者仍分別屬 closure items 4、5、8。

---

## 1. Source-of-record 與型別邊界

| 物件 | 唯一 source-of-record | identity |
| :--- | :--- | :--- |
| C8 target generator | `stage5c_hard_controls.sprinkle_control`，$p_\theta(u,v)=1+\theta q(u)q(v)$、$\theta=\pm0.4$ | `stage5c-hard-controls-sprinkle-control-p-theta-v0.1` |
| nuisance features | `stage5c_hard_controls.baseline_features` 的 11 維 `FEATURE_NAMES` | 隨 matcher identity 一併版本化 |
| calibration scale | `stage5c_hard_controls.calibration_scale` 的 pooled sample SD | 隨 matcher identity 一併版本化 |
| C8.1 matcher | `stage5c_hard_controls.match_controls` | `stage5c-hard-controls-c8.1-matcher-v0.1` |
| joint law adapter | `certify_matching` 後才可呼叫 `form_joint_matched_law` | `stage5c-6a-e-joint-matched-law-v0.1` |
| paired covariance | 4D joint sample covariance 的 block reduction，`ddof=1` | `stage5c-paired-delta-covariance-ddof1-v0.1` |

正式 runner 必須從 item 9 的 fresh manifest 將 calibration pools 與 evaluation pools 連到上述
generator。item 2 只固定 generator/matcher 的計算來源和 typed identities；它**不**生成 manifest。
`calibration_identity` 與 `pool_identity` 必須不同，實際 seed ranges 的 disjointness 仍由 item 9
在 generator 呼叫前驗證。

Generator 只在 evaluator-side 保存 coordinates 與 target metadata。construction-facing payload
仍只能是 `BlindedCase(case_id, order)`；本模組不 import selector runner、arm ledger 或任何
候選程式。

---

## 2. Frozen matching lifecycle

令兩臂 evaluation feature pools 為 $X^L,X^R\in\mathbb R^{n\times11}$，獨立 calibration
pools 為 $C^L,C^R$。唯一 lifecycle 是：

1. 以 $C^L,C^R$ 的 pooled sample SD 形成逐分量尺度；任一尺度為零或非有限時停止；
2. 以 standardized Euclidean distance 建 cost matrix；
3. component caliper $1.0$、Euclidean caliper $2.0$；
4. Hungarian assignment 先最大化 valid cardinality，再在其中最小化總距離；
5. 每個 pool element 最多進一 pair，所有 unmatched elements 明確丟棄並由 indices／coverage 記帳；
6. certification 同時要求 matched pairs $\ge192$、coverage $\ge0.35$、maximum absolute SMD
   $\le0.20$、maximum KS $\le0.18$。

邊界等號皆通過。任何一項不通過都在 certification stage 得
`INCONCLUSIVE`，不得形成或顯示 endpoint law：

| reason code | 條件 |
| :--- | :--- |
| `CALIBRATION-SCALE-INVALID` | pooled calibration scale 無法形成 |
| `MATCHER-FAILURE` | valid assignment 少於兩 pairs，matcher 無 covariance 定義域 |
| `COHORT-TOO-SMALL` | retained pairs $<192$ |
| `COVERAGE-TOO-LOW` | retained fraction $<0.35$ |
| `SMD-BALANCE-FAILED` | maximum absolute SMD $>0.20$ |
| `KS-BALANCE-FAILED` | maximum KS $>0.18$ |

同一 cohort 可同時保存多個不通過的 reason。shape、feature count、arm identity 或 typed stream
identity 缺失屬 schema defect，拋出 `JointLawProtocolError`，未來 runner 必須映為
`PROTOCOL-INVALID`，不能降成 matching `INCONCLUSIVE`。

`form_joint_matched_law` 的第一個動作是檢查 matching `CLEAN`，發現非 clean 時在觸碰 endpoint
input 前即停止。regression 以拒絕任何 array conversion 的 sentinel endpoint 證明此
short-circuit 是計算層的，不是只在裁決表上標 `NOT-EVALUATED`。

---

## 3. $\Pi_{\mathcal M}$ 的唯一有限樣本表示

對 clean matching，令 matcher 給出的 ordered index pairs 為
$\mathcal M=\{(i_k,j_k):k=1,\ldots,m\}$。兩臂已認證的二維 endpoint vectors 記為
$Z^L_i,Z^R_j\in\mathbb R^2$。一個 matched observation 是不可拆開的四維 tuple

$$
X_k=(Z^L_{i_k},Z^R_{j_k})\in\mathbb R^4,
\qquad D_k=Z^L_{i_k}-Z^R_{j_k}\in\mathbb R^2.
$$

本版 matcher 是無重複的一對一 assignment，raw samples 也沒有 unequal sampling weights；故
pair weights 唯一固定為 $w_k=1/m$。有限樣本 joint empirical law 與 marginals 是

$$
\widehat\Pi_{\mathcal M}=\frac1m\sum_{k=1}^m\delta_{X_k},\qquad
\widehat\Pi_{L\mid\mathcal M}=\frac1m\sum_k\delta_{Z^L_{i_k}},\qquad
\widehat\Pi_{R\mid\mathcal M}=\frac1m\sum_k\delta_{Z^R_{j_k}}.
$$

$\Pi_{\mathcal M}$ 的 population meaning 涵蓋兩臂 generator、獨立 calibration pools、matching、
calipers、unmatched handling、cohort／balance conditioning 與上述 uniform pair weights。它不是
兩個 raw arm laws 的乘積，也不是兩個 matched marginals 的任意 coupling。$T_+$ vs $T_+$ 與
$T_-$ vs $T_-$ null controls 必須原樣走同一 lifecycle；不能預先指定 perfect pairs 或跳過
attrition。

本 schema 固定 ordered contrast 為「傳入的第一 arm identity 減第二 arm identity」。哪一個
scientific target 放在第一位、E1 的方向以及 E2 的 equivalence functional 仍由 items 4／5
明文固定；item 2 不替它們做選擇。

---

## 4. Paired covariance schema

令 $\widehat\Sigma_X$ 為 $X_k$ 的 unbiased sample covariance（分母 $m-1$），分塊為

$$
\widehat\Sigma_X=
\begin{pmatrix}
\widehat\Sigma_{LL}&\widehat\Sigma_{LR}\\
\widehat\Sigma_{RL}&\widehat\Sigma_{RR}
\end{pmatrix}.
$$

pair-level paired delta covariance 唯一為

$$
\widehat\Sigma_D=
\widehat\Sigma_{LL}+\widehat\Sigma_{RR}
-\widehat\Sigma_{LR}-\widehat\Sigma_{RL}.
$$

Executable code 同時保存完整 $4\times4$ joint covariance、四個 $2\times2$ blocks、
$\widehat\Sigma_D$，並另由 raw $D_k$ 直接重算 sample covariance作 identity regression。
下式被明禁：

$$
\widehat\Sigma_D\ne
\widehat\Sigma_{LL}+\widehat\Sigma_{RR}
\quad\text{（除非 cross blocks 恰為零；不得預設）。}
$$

Hungarian assignment 是整個 pool 上的 global operation；同一 assignment 內的 $D_k$ 不得被
默認為 $m$ 個獨立 sampling units。因此本 contract **不**以 $\widehat\Sigma_D/m$ 作 inferential
mean covariance。正式 split 必須含 $B\ge2$ 個彼此獨立的完整 matching lifecycles（calibration
與 evaluation pool identities 均逐 block 不同）。令第 $b$ 個 cohort 為 $\mathcal M_b$、pair
數 $m_b$、總 pair 數 $M=\sum_bm_b$，則

$$
\bar D=\frac1M\sum_{b=1}^B\sum_{k\in\mathcal M_b}D_{bk},\qquad
g_b=\frac1M\sum_{k\in\mathcal M_b}(D_{bk}-\bar D),
$$

而唯一 inferential covariance schema 是 matched-cohort cluster sandwich

$$
\widehat{\mathrm{Cov}}(\bar D)
=\frac{B}{B-1}\sum_{b=1}^B g_bg_b^T.
$$

它容許各 block attrition 後的 $m_b$ 不同，且不需要 pair-level independence。若所有
$m_b=m$，上式正好化為 block means 的 sample covariance 除以 $B$。有效自由度由獨立
matched cohorts 決定，不得用總 pair 數 $M$ 冒充。`aggregate_joint_matched_laws` 會拒絕重複
calibration／evaluation pool identity，讓 item 9 有明確的 custody 接點。

Singular／ill-conditioned covariance 如何進入 E1／E2 region 是 items 4／5 必須型別化的
statistical acceptance 問題；item 2 不加入 ridge、pseudo-inverse 或 data-dependent projection。

---

## 5. Candidate-independent calibration suite

本 suite 沿用 item 3 的 shared planted infrastructure 規律：完整 typed domain 與 boundary／
interior suite 分開登記、ground truth 解析已知、matching normal／failure cases 共用同一
feature generator、correct／falsifier covariance paths逐位元共用同一 random draws，且所有
acceptance bounds 在任何 arm data 存在前固定。它不重用 item 3 的 matrix-scale 數值，因本項的
隨機物件是 bounded endpoint vector 而非未 normalization 的 pairing matrix；把兩者硬套同一
有因次 scale 反而會混淆型別。

### 5.1 Matching／attrition failure suite

`planted_matching_inputs` 使用同一個 11 維 matcher 與所有 frozen calipers／floors，但完全不建立
arm endpoints。它包含：

- 256/256 exact match：`CLEAN`；
- 191/256 retained：只觸發 `COHORT-TOO-SMALL`；
- 192/600 retained：只觸發 `COVERAGE-TOO-LOW`；
- 0 retained：`MATCHER-FAILURE`；
- zero-variance calibration pool：`CALIBRATION-SCALE-INVALID`。

因此 calibration 不只跑理想配對；matched cohort 變小與完全 matching failure 均走正式
fail-closed path。

### 5.2 Covariance consistency 與 region calibration 分帳

Known-ground-truth law 為零均值四維 Gaussian，二維 component covariance

$$
C=\begin{pmatrix}1&1/4\\1/4&3/2\end{pmatrix},\qquad
\Sigma_X(\rho)=\begin{pmatrix}C&\rho C\\\rho C&C\end{pmatrix}.
$$

完整 planted domain 為 $m\in[192,384]$、$\rho\in[-3/4,3/4]$；executable suite 取 cohort
boundary $m\in\{192,384\}$ 及 symmetric correlation boundary/interior
$\rho\in\{-3/4,0,3/4\}$。此 domain 只壓測 joint covariance，不是 effect domain 或科學
threshold。$|\rho|<1$ 與 $C\succ0$ 解析保證 $\Sigma_X\succ0$，且 true paired covariance 是
$2(1-\rho)C$。

每格使用 $B=32$ 個獨立 matched-cohort sampling units與 2048 個 development-only deterministic
replications；每個 planted cohort mean 的已知 covariance 為 $\Sigma_X(\rho)/m$。stream identity
由 suite identity、$m$、$\rho$、$B$ 與 replication count 的 SHA-256 導出。這些 streams明文不是 item 9 的正式
6a-E manifests，不可成為 selection／confirmation／power input，也不消耗 confirmatory budget。

兩個診斷分開：

1. **covariance consistency**：以 Normal/Wishart 的逐 entry standard error比較 repeated mean
   cluster covariance 與 analytic $2(1-\rho)C/m$，maximum standardized discrepancy必須 $\le6$；
2. **finite-sample calibration**：以二維 Gaussian 下 exact Hotelling $T^2/F$ region 作純診斷
   oracle，使用 $B-1$ 而非 $Bm-1$ 的 covariance degrees of freedom，名目 coverage 0.95；
   2048 次 coverage count 必須落在其事前 99.9% binomial acceptance interval。type-I error
   另列為 $1-$coverage，不得用 consistency 代替 calibration。

Hotelling region **不是** E1／E2 scientific region 提案；它只提供一個已知有限樣本 oracle，
用來檢查 paired covariance schema 是否把 region 的名目性質傳遞正確。

六個正確-schema cells 的 observed maximum covariance $z$ 為 2.505，coverage 範圍
0.9404–0.9517，全部通過 consistency 與 calibration。刻意錯誤的
`independent-marginals` falsifier 在 $(m,\rho)=(192,-3/4)$ 保留正確 covariance estimator，
但形成 region 時刪掉 cross-arm blocks；其 coverage 為 0.8418、type-I error 為 0.1582，落在
事前 acceptance interval 外。故這個檢查不是恆真，也明確抓得到 observable contract 禁止的
獨立-marginal variance。

---

## 6. Closure 與尚未授權事項

本 PR 合併前 closure item 2 只能是 `REVIEW-PENDING`。只有 source、tests、文件、獨立複核、
CI 與 merge 全部完成，才可另以 state-only closeout 提議 `CLOSED`。

即使 item 2 日後 `CLOSED`，items 4／5／7–10／12 仍 `OPEN`、item 11 仍 `DRAFT`；不得生成
6a-E seed、開啟 arm numerical ledger、形成 arm endpoint，亦不得把本 calibration-only
Hotelling oracle升格為 scientific region。
