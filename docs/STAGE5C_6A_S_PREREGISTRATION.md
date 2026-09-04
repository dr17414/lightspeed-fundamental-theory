# Stage 5C — smearing／normalization／6a-S numerical preregistration

狀態：**【原 preregistration 已交付；首次 plus arm `PROTOCOL-INVALID`；Amendment-001 已凍結；
DEV-0012 dress rehearsal mechanically clean 並待獨立複核／合併；replacement 尚未執行】**。

本文件固定 C8 intrinsic selector family 的 smearing、normalization、同 target measure
metric、數值門檻、樣本格、seed manifest 與 failure semantics。它不執行 6a-S、不讀
$T_+$ vs $T_-$ contrast、不設計或接觸候選 $K$，也不完成 6a-E、active wrong-support E3
或 Freeze-1a。

source of record：`analysis/stage5c_measure_prereg.py`；結構測試：
`tests/test_stage5c_measure_prereg.py`。

2026-09-03 的 `docs/STAGE5C_6A_S_PROTOCOL_AMENDMENT_001.md` 只在明列範圍內
取代本文件 §4.2、§5.4 與 §6 的執行 lifecycle／internal-recomputation semantics；其餘
selector、smearing、normalization、sampling grid 與 scientific gates 全部不變。

---

## 1. 適用範圍與資料隔離

本 prereg 只作用於 `docs/STAGE5C_SELECTOR_FAMILY.md` 的 11 個有序 C8 參數點。每個
selector 仍只接收 `BlindedCase(case_id, order)`；sealed coordinates 只在 selector 回傳 pair
後由 evaluator 取回，用於形成 induced measure。下列任何量都不得進入 selector：target
label、coordinates、seed、realizer、reference-probe bank、候選輸出或 endpoint。

6a-S 只作**同一 target 內**的 block-to-block 比較。兩 target 可在同一 batch 中各自執行，
但不得形成、檢視或報告 between-target contrast。reserved 6a-S streams 與未來 6a-E
selection／confirmation、candidate holdout 全部不相交。

---

## 2. Pair domain、smearing 與 normalization

### 2.1 Domain 與 orientation

離散 pair domain 固定為

$$\mathcal D(C)=\{(x,y):x\prec y\},$$

orientation 固定為 source-first。sealed null coordinates 依

$$(x,y)\mapsto (u_x,v_x,u_y,v_y)\in[0,1]^4$$

嵌入 ordered pair space；base measure 是
$du_x\,dv_x\,du_y\,dv_y$。selector 只選嚴格因果 pair，所以 exact diagonal 不在 raw
measure 中；本 prereg 不另作 coordinate-defined near-contact 或 boundary exclusion。

### 2.2 Pair weight $\varphi$ 與 $\mathcal N_C$

固定

$$\varphi_C(x,y)=1,\qquad
\mathcal N_C=|\Sigma(C)|,$$

故

$$\widetilde\nu^C_\Sigma
=\frac1{|\Sigma(C)|}\sum_{(x,y)\in\Sigma(C)}
\delta_{(u_x,v_x,u_y,v_y)}$$

是非負 probability measure。它的 total mass 與 total variation 都是 1；Kish weight ESS
恰為 $|\Sigma(C)|$。這個 ESS 只量測 weight degeneracy，**不把同一 causet 內相關的 pairs
冒充為獨立 observations**；inferential unit 仍是 causet。

$\varphi$ 與 $\mathcal N_C$ 只由 selector output count（因而只由 order）決定，沒有自由
尺度、optimizer、lookup、負權重或 complex phase。若 $\mathcal N_C=0$，這是 selection
failure，不得更換 normalization。

### 2.3 Linear regulator $R_\epsilon$

固定 dimensionless physical smearing scale

$$\epsilon=1/16$$

及四維 mass-one Gaussian

$$
(R_\epsilon\widetilde\nu)(z)
=\int_{\mathbb R^4}\frac{
e^{-\|z-z'\|_2^2/(2\epsilon^2)}}{(2\pi\epsilon^2)^2}
\,d\widetilde\nu(z').
$$

這是 linear、positive，且在 ambient $\mathbb R^4$ 上 mass-preserving 的 Schwartz regulator。
它在 unit null-coordinate box 的尺度 convention 下固定，不由任一 target 或 selector 結果
調整；executable API 不接受 caller 覆寫 $\epsilon$。限制回 $[0,1]^4$ 時並不
mass-preserving，boundary leakage 必須由 E4 量化。本階段採
**固定 physical smearing scale**，不宣稱 $\epsilon\to0$；未來 6a-E/E4 必須用同一尺度證明 continuum
distribution pairing 存在並由兩個獨立 implementation 重現。若 E4 失敗，只能依 amendment
流程修改，不能在執行 6a-S 後靜默換 regulator。

**6a-S 對 $\epsilon$ 的能力上限.** 第一個 Fourier shell 對 $\epsilon=1/16$ 只有溫和衰減；
S5 並未被設計成 smearing-scale discrimination test，不能宣稱它「驗證」或「鎖住」
$\epsilon$。本 prereg 只固定 convention；其物理／distributional 適切性與 boundary leakage
完全推遲到 E4。S5 通過對 $\epsilon$ 的正確性沒有獨立蘊涵。

### 2.4 Dimensional covariance

6a-S 固定的是 dimensionless unit box、fixed cardinality 與 probability measure。若 continuum
physical null coordinates 為 $(U,V)=L(u,v)$，則 regulated density 對四維 pair-space
Lebesgue measure 帶 $L^{-4}$，而 $d^4Z$ 帶 $L^4$，總質量不變。$\mathcal N_C$ 無量綱。
primary endpoint $\mathfrak I_G$ 對 smeared matrix 的共同非零 scalar rescaling為 degree-zero，
所以 object 的共同工程量綱不進最終二維 ratio；near-zero gate 仍須在後續 contract 另行固定，
不得由此推成自動通過。

---

## 3. S5 finite-resolution random-measure metric

6a-S 不以有限樣本宣稱證明完整 weak convergence。它固定一個可執行、target-independent
的 finite-resolution prefilter；6a-E/E4 仍須負責 continuum／distributional well-posedness。

### 3.1 Regulated Fourier signature

取 unit four-cube 第一個非零 Fourier shell 的 conjugation-nonredundant half-shell

$$
\Omega_+=\{2\pi k:k\in\{-1,0,1\}^4,\ k\ne0,
\text{ first nonzero component of }k\text{ is positive}\},
\qquad |\Omega_+|=40.
$$

對每個 causet measure 記錄

$$
F_\omega(\nu^{C,\epsilon})
=e^{-\epsilon^2\|\omega\|^2/2}
\sum_a w_a e^{i\omega\cdot z_a},\qquad \omega\in\Omega_+.
$$

此 grid 沒有 fitted bandwidth、random features、optimizer 或 target-dependent projection。
zero mode 由 total-mass gate 獨立精確檢查，故不重複收入 signature。因 measure 為實，
$F_{-\omega}=\overline{F_\omega}$；完整 80 modes 只有 40 個 complex／80 個 real 自由度，
所以 source-of-record 不重複儲存 conjugate modes。

### 3.2 Weighted-mean measure distance

兩個同 target、同 $N$、同 selector 的獨立 blocks $A,B$ 取

$$
d_{\rm mean}(A,B)=
\max_{\omega\in\Omega_+}\left|
\frac1{|A|}\sum_{C\in A}F_\omega(C)-
\frac1{|B|}\sum_{C\in B}F_\omega(C)
\right|.
$$

預登記 equivalence margin：

$$d_{\rm mean}\le0.20.$$

### 3.3 Random-measure law distance

把 40 個 complex signatures 實化成 $\mathbb R^{80}$，並除以 $\sqrt{40}$。對兩個
independent blocks $A=(A_i)_{i=1}^n$、$B=(B_j)_{j=1}^m$ 使用保留符號的 unbiased
U-statistic

$$
\widehat E_U=
\frac{2}{nm}\sum_{i,j}\|A_i-B_j\|
-\frac{1}{n(n-1)}\sum_{i\ne i'}\|A_i-A_{i'}\|
-\frac{1}{m(m-1)}\sum_{j\ne j'}\|B_j-B_{j'}\|,
\qquad
d_{\rm law}=\sqrt{[\widehat E_U]_+}.
$$

$\widehat E_U$ 的 finite-sample 值允許為負，raw signed value 必須保存並報告；只在形成
non-negative reporting／gate quantity $d_{\rm law}$ 時取 positive part。within-block sums
明確排除 diagonal，避免 V-statistic 把 per-causet dispersion／pair count 轉成正的 null bias。

預登記 gross-breakage tripwire threshold：

$$d_{\rm law}\le0.20.$$

$d_{\rm law}$ 這一臂只作 gross numerical breakage tripwire。DEV-0009 的 pre-execution
development audit 顯示，移除 V-statistic null bias 後，$0.20$ 對明顯的 cross-$N$ law
difference 仍缺乏 power；因此 $d_{\rm law}$ 通過**不構成 random-measure law stability 的
獨立證據**，也不得與 $d_{\rm mean}$ 並稱為兩個等效性判決。本 prefilter 的實際承重為
$d_{\rm mean}$ 與 S1/S6 floors；$d_{\rm mean}$ 本身也只檢查已登記 Fourier means，不能外推
成完整 law stability。

$d_{\rm mean}$ 的 $0.20$ equivalence margin 與 $d_{\rm law}$ 的 $0.20$ tripwire threshold
沿用本專案 C8.1 candidate-independent balance contract 的 maximal standardized discrepancy
尺度作 operational tolerance，但不把不同統計量冒充為同一量，也不宣稱它們給出
family-wise hypothesis-test $p$ 值。所有 11 個 selector、兩個 target、三個 $N$、六組
block pairs 均須逐一通過；不平均、不挑最好的一個 block pair。

relative-to-uniform divergence 與 $T_+$/$T_-$ measure difference只可作不改判 secondary
diagnostic；本次執行明禁計算後者。

---

## 4. Frozen numerical design

### 4.1 Sampling grid

- RNG：NumPy `PCG64DXSM`（與 C8 control generator 一致）；
- targets：$\theta=+0.4$ 與 $\theta=-0.4$，但只各自在 target 內比較；
- fixed-cardinality sequence：$N\in\{64,96,128\}$；
- 每 target、每 $N$：4 個互相獨立 blocks；
- 每 block：64 causets；
- 每個 causet 對全部 11 個 selector parameter points 求值；不得為某 member 加樣本或換 block；
- 所有 pair-level summaries 先在 causet 內 normalization，再以 causet 為同權 block unit。

這個 sequence 只檢查三個有限 $N$ 上的同-target numerical stability；不得寫成 continuum
limit 已證。若要擴充 $N$ 或 blocks，須在揭露 reserved streams 前走 amendment。

### 4.2 Seed manifest

令 target base

$$b_+=1{,}300{,}000{,}000,\qquad b_-=1{,}400{,}000{,}000.$$

對 $N$ index $i=0,1,2$、block $j=0,1,2,3$、case $k=0,\ldots,63$：

$$\operatorname{seed}=b_\pm+10^6i+10^4j+k.$$

精確 mapping 由 `preregistered_seed()` 鎖定。這 1536 個 seeds 在本 prereg commit 前均不得
生成；首次生成即 burned，不論程式中斷、member failure 或最終判決。它們不得進 6a-E、
候選 calibration 或 holdout。

**Amendment-001 disposition.** 1.3B plus 的 768 seeds 已於 DEV-0011 全部生成並永久
burned，正式 verdict 不重判；1.4B minus 尚未生成，但已由 Amendment-001 加上 prerequisite
鎖。replacement plus 改用 fresh 1.5B，reserved 前的完整 development dress rehearsal 使用
3.1B。精確 manifests、四個承重 code files 的 cross-commit protocol-invariant digest、
committed append-only burn registry 與 sequential authorization 以 amendment §2.4–§5 為準。
3.1B plus-distribution development ledger 不得與任何 minus ledger 配對或形成 numerical
contrast，也不得回流成 replacement control／calibration／power input。

---

## 5. S1–S6 gates 與判決

### 5.1 Exact structural gates

- **S1**：每個 sample 對該 selector 都須成功選出至少 32 pairs；沒有 sample exclusion。
- **S2**：沿用 selector source-of-record 的 relabel covariance，逐位元。
- **S3**：C8 family sector-blind，sector swap 逐位元不變。
- **S4**：`BlindedCase` payload falsifier、closed capacity 11 與完整 ledger 全過。

其中五個 depth-grid members 已依 DEV-0008 的 pre-execution audit，由原本不具 pair-balance
且破壞 order duality 的 `source_depth_band`，改為 `endpoint_depth_mass_band`。新規則先以
$d_-(x)+d_+(y)$ 對 causal pair 分層，再按每個 score level 的 pair-mass midquantile 套用
同一組 $0,.2,.4,.6,.8,1$ half-open grid；同一 score level 不拆分。capacity 仍為 11。

**已知 floor-binding cell.** DEV-0009 在 development-only 2.9B streams 上把
`interval_exact(4)`、$N=64$ 識別為最靠近 32-pair floor 的已知 cell：每 target 各 384
causets 的觀察最小值為 38 與 43；以該 audit 的常態近似外推，正式兩 targets、四 blocks
合計 512 causets 約有 $3\%$ 機率至少一次跌破 floor。這只是事前風險估計，不是 calibrated
failure probability，也不改 gate：若 reserved execution 任一 causet 少於 32 pairs，該
selector 仍須記 `6a-S FAIL`；不得事後降低 floor、排除 sample 或改記 `INCONCLUSIVE`。

### 5.2 S5 gates

對每個 selector、target、$N$ 的 $\binom42=6$ 組 block pairs：

- total mass 與 total variation 各在 $1\pm10^{-12}$；
- $d_{\rm mean}\le0.20$；
- signed $\widehat E_U$ 完整保存，且 $d_{\rm law}=\sqrt{[\widehat E_U]_+}\le0.20$。

任一組超標，該 selector 記 `6a-S FAIL`；不得刪掉該 block 或改 margin／threshold。
$d_{\rm law}$ 在本 prereg 只承擔 gross-breakage tripwire；即使全部通過，也不得獨立宣稱
random-measure law stable。S5 的可承重 finite-resolution evidence 是已登記 Fourier means
的 $d_{\rm mean}$；完整 law／continuum stability 仍留給 6a-E/E4。

**已知 $d_{\rm mean}$ binding cell.** DEV-0010 在 development-only 3.0B segment 上把
$N=64$ 的 `endpoint_depth_mass_band(0.8,1.0)` 識別為最緊的同分布 block-pair cell：兩個
targets 的已報 null p99 約 `0.122/0.123`、p99.9 約 `0.146/0.151`，各 5000 draws 的最大值
為 `0.172/0.171`，仍低於 0.20。這是 pre-execution tail-risk registration，不是 calibrated
family-wise false-FAIL probability，也不改 margin；若 reserved run 超過 0.20，仍依原規格
記 `6a-S FAIL`，不得事後稱為 null tail 而重跑、換 block 或放寬 margin。

### 5.3 S6 gates

每個 causet逐一要求：

- selected-pair coverage $\ge0.005$；
- $\mathcal N_C=|\Sigma(C)|\ge32$ 且 finite；
- Kish ESS $\ge32$；
- ESS／selected-pair count $\ge0.95$；
- exact diagonal exclusion由 $x\prec y$ 逐位元成立；本 prereg 的 coordinate boundary
  exclusion 數為 0，禁止執行後追加未登記 trimming。

uniform weights 理論上令 ESS fraction 恰為 1；這一 gate 的作用是封住日後權重或
normalization 被靜默修改。

### 5.4 Verdict semantics

| 情形 | 6a-S verdict |
| :--- | :--- |
| S1–S6 全部通過 | `6a-S PASS`；只代表該 selector 可進 6a-E，**不代表 SELECTOR-VIABLE** |
| well-defined run 中任一預登記 floor／margin 失敗 | `6a-S FAIL` |
| 資源不足、非有限 numerical output、可證的 backend 數值故障 | `INCONCLUSIVE`；不得換門檻或 seeds |
| 接觸 between-target contrast、candidate output、未登記 metadata，或在本 commit 前生成 reserved streams | `PROTOCOL-INVALID` |
| ledger stored field／gate flag／verdict 與 frozen schema、raw fields 或 deterministic transform 的 internal recomputation 不一致 | `PROTOCOL-INVALID`；reason 必須依 Amendment-001 §2 分類，不得由 runner 擴張成未登記類別 |

6a-S 是對全部 11 點的 batch prefilter，不消耗 6a-E contrast spending，也不改變原始 family
順序。被 6a-S 淘汰的位置不向後重分配任何 future 6a-E alpha／e-value budget。

---

## 6. Runner freeze 與尚未完成

runner／ledger／adjudicator 原由 `docs/STAGE5C_6A_S_RUNNER_FREEZE.md` 與
`analysis/stage5c_6a_s_runner.py` v1 固定；DEV-0011 後由 Amendment-001 與 runner v2 在不改
scientific gates 的前提下修正 implementation defect。1.3B plus 已 burned；3.1B dress、1.5B
replacement plus 與 1.4B minus 均尚未生成。

runner v2 另要求每臂 header／attestation 保存同一組四檔 protocol-invariant digest 與
`sys.version`／NumPy／SciPy runtime versions，combine 只接受 code digest 與 runtime 都相同的
兩臂；每次 claim 前並要求 burn registry 是合法 lifecycle prefix、目前 profile／target 未登記。
這些是跨 commit scientific-rule consistency 與 anti-rerun custody checks，不修改任何 S1–S6
threshold。若 3.1B rehearsal 後必須修改四檔，或 formal process 的 `sys.version`／NumPy／
SciPy version strings 已漂移，唯一出口都是 AMEND-0002＋全新 dress profile／seed base；
不得重跑 3.1B、改寫 DEV-0012 的實際環境，或就地修改／升降級後直接進 1.5B。
DEV-0012 的 categorical pattern 亦不得用來解釋、校正或重判 1.5B；replacement plus 的
verdict 必須只依自身 frozen ledger 與 adjudicator 決定。

本文件刻意不固定或不宣稱：

- 6a-S 執行結果與 selector ledger；
- 6a-E 的 between-target joint metric、effect/equivalence regions、power、spending、selection
  與 fresh-confirmation seeds；
- active wrong-support E3 typed intervention；
- C6/C7 gate-specific selectors；
- Gaussian-regulated continuum $S_\theta$ pairing 的 E4 proof；
- candidate endpoint、候選 $K$、C3b candidate-specific instantiation；
- Freeze-1a 完成。

所以 Amendment-001／runner v2 合併、CI 與獨立 review 完成並重新核對 `main` 後，唯一
獲准的下一步是先執行完整 3.1B development dress rehearsal。只有 DEV-0012 與 committed
hash attestation 通過後才可執行 1.5B replacement plus；再經 DEV-0013 與 plus attestation
確認無 `PROTOCOL-INVALID`／`INCONCLUSIVE`，才可啟動 1.4B minus。不得跳過中間 commit、
直接開始 6a-E 或候選設計。
