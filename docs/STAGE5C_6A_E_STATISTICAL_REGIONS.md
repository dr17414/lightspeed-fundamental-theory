# Stage 5C — 6a-E E1／E2／E3 simultaneous statistical regions

狀態：**【candidate-independent closure items 4／5 delivery／REVIEW-PENDING／不可執行 arm】**。

本文件固定二維 primary endpoint 的 E1 contrast region、E2 equivalence region、E3
逐分量規則、validated numerical-error 傳播，以及一個具解析 oracle 的 df-only falsifier。
唯一 source-of-record 是 `analysis/stage5c_statistical_regions.py`，regressions 是
`tests/test_stage5c_statistical_regions.py`。

這不是 item 8 的 multiplicity／power audit，不配置 family-wise spending，不選擇 local
$\alpha$，也不解除 execution firewall。沒有生成或 claim 6a-E seed、沒有開啟 arm ledger、
沒有形成 arm endpoint，且沒有設計、import、執行或觀察候選 kernel $K$。

---

## 1. 唯一輸入與使用域

每一個 comparison 只能由 item 2 已凍結的 `MatchedLawEnsemble` 轉成
`StatisticalRegionInput`。二維估計量是完整 matched-pair ensemble 的有序平均 contrast

$$
\widehat\Delta=(\widehat\Delta_1,\widehat\Delta_2),
$$

其 covariance 必須是 item 2 的 independent-cohort CR1 mean-covariance
$\widehat V$。不得從兩個 arm marginals 重建 covariance，不得刪除 cross-arm blocks，
也不得用候選資料挑 projection、norm、sign 或 ridge。

可形成 region 的結構域固定為：

- independent cohorts $B\ge32$；reference degrees of freedom 永遠為 $B-1$，不是總 matched
  pair 數 $M-1$；
- 每一 cohort 的 matched count 都須落在 item 2 已校準的 $[192,384]$；超出即
  `INCONCLUSIVE/PAIR-COUNT-OUTSIDE-CALIBRATION`；
- $\widehat\Delta$、$\widehat V$ 與 numerical half-width 全部 finite；$\widehat V$ 須在
  binary64 rounding tolerance 內 symmetric positive semidefinite，且兩個 marginal variance
  嚴格為正；
- exact-zero marginal variance、non-finite input、非 PSD covariance 或 $B<32$ 都在 region
  形成前 fail closed。scientific gate 為 `NOT-EVALUATED`，不是 `FAIL`。

Region 不反轉 covariance，也不使用 off-diagonal element。因此 singular／ill-conditioned
cross-covariance 若 PSD 且兩個 marginal variances皆正，仍可安全形成 rectangle；不得為了
讓反矩陣存在而加 ridge 或 pseudo-inverse。

---

## 2. 二維 simultaneous rectangle

Primary endpoint 的 sharp coordinate ranges 是 $[-1,2]\times[0,1]$，故固定 scale

$$
D=\operatorname{diag}(3,1),\qquad z=D^{-1}\Delta .
$$

Item 8 日後必須為每個具名 claim 提供 multiplicity-adjusted local $\alpha_g$；本交付**沒有
default**，只接受顯式 $0<\alpha_g\le0.01$。對 $p=2$ 個座標，固定

$$
q_g=t_{B-1,\,1-\alpha_g/(2p)},\qquad
h_j^{\rm stat}=q_g\sqrt{\widehat V_{jj}}.
$$

若 item 3 對 matched endpoints 給出 componentwise validated errors，§3 產生
$h_j^{\rm num}$。最終 simultaneous rectangle 是

$$
R_g=\prod_{j=1}^{2}
\left[\widehat\Delta_j-h_j^{\rm stat}-h_j^{\rm num},
      \widehat\Delta_j+h_j^{\rm stat}+h_j^{\rm num}\right].
$$

實作不以 round-to-nearest 的連鎖結果直接承重。$\sqrt{\widehat V_{jj}}$ 先以平方後的
exact-dyadic comparison向上包住；$q_g\sqrt{\widehat V_{jj}}$ 與
$h_j^{\rm stat}+h_j^{\rm num}$ 再以輸入 binary64 的 exact dyadic rationals求值並向上捨入；
lower endpoint 的減法向 $-\infty$ 捨入，upper endpoint 的加法向 $+\infty$ 捨入。
$D^{-1}R_g$ 的 lower／upper normalization亦分別向 $-\infty$／$+\infty$ 捨入。因此例如
binary64 raw boundary $(3\times0.05)$ 除以 3 時，不會因 round-to-nearest 變成
`0.05000000000000001` 而誤過 strict gate。任何 exact intermediate 超出 finite binary64
representable range 都在 region 形成前成為 `INCONCLUSIVE/NONFINITE-INPUT`。

這是兩座標 Bonferroni Student-$t$ reference region。在 equal-count independent Gaussian
cohort-mean oracle 下，每個座標的 $t_{B-1}$ coverage 是解析的，Bonferroni 給 simultaneous
coverage 下界。對實際 CR1、unequal attrition 的使用，它是預先固定的 cluster-$t$ operational
reference，不宣稱新的 exact finite-sample theorem；item 2 的 calibration domain與 item 8
尚待完成的 power／multiplicity audit仍是能力邊界。

---

## 3. Item-3 numerical uncertainty 的唯一傳播

對 cohort $b$ 的 frozen matched indices $(i_{bk},j_{bk})$，item 3 的兩臂 componentwise
endpoint-error vectors 分別記為 $e^L_{bi}$、$e^R_{bj}$。API 不接受裸 error arrays；每個
pool 必須是 `CertifiedEndpointPool`，逐 row 持有由 `certify_pairing` 產生且帶 module-private
producer seal 的 CLEAN `CertificationResult`。arm、matching pool 與原始 row index 在
certification 產生時寫入 `EndpointCertificationProvenance`；pool adapter 不再接受 caller
另貼的 identity labels，而只從 sealed rows 推導並驗證共同 arm／pool與連續原始 row 順序。
聚合另驗證 `CERTIFICATION_ID`，以及 certified endpoint 與 item-2 joint law 中實際 matched
endpoint 逐位元相同。直接建構的 CLEAN record、failed certification、solver diagnostic、
別的 pool／arm／row或替代的零 error都不能進入聚合。

同一 pair contrast 的 triangle bound為
$e^L_{b i_{bk}}+e^R_{b j_{bk}}$；使用 item 2 相同的 total-pair weights，固定

$$
h^{\rm num}
=\frac1M\sum_b\sum_{k=1}^{m_b}
\left(e^L_{b i_{bk}}+e^R_{b j_{bk}}\right).
$$

每個輸入 binary64 error 先轉成其 exact dyadic rational；pair addition、全體求和與除以
$M$ 都在 exact rational 中完成，最後才作一次 directed-upward binary64 rounding。這避免
「各步 round-to-nearest、最後只 `nextafter` 一次」仍不足以包住真值的漏洞。unmatched rows
不進入此式。cubature solver 自報的 estimated error 或任何 diagnostic 不得升格成
$h^{\rm num}$。

聚合結果不是裸 vector，而是 opaque、aggregation-only 的 `ValidatedNumericalHalfWidth`；其
公開 constructor 不可用，只有 matched aggregation 能以 module-private producer token 建立。
它綁定 certification／propagation／joint-law IDs、ordered arms、$B$ 與 $M$。
`build_simultaneous_region` 只接受這個 producer-authenticated 型別，且須與
`StatisticalRegionInput` 的 arms、cluster count、pair count與 joint-law ID 完全一致。故直接
手造吻合 labels 的零 radius、傳入裸 zero vector，或把另一個 comparison 的 radius 移用到本
region，都在 region 形成前成為 protocol error。

---

## 4. E1：target contrast

有序 arm identity 固定為 `(T-plus, T-minus)`，所以
$\Delta=\mathcal O_{T_+}-\mathcal O_{T_-}$。candidate-independent joint effect floor 固定為
完整 coordinate range 的 $1/20$：

$$
\delta_J=\frac1{20},\qquad
\mathcal B_J=[-\delta_J,\delta_J]^2
$$

（在 normalized $z$ coordinates）。E1 `PASS` 當且僅當完整 normalized rectangle
$D^{-1}R_{E1}$ 與 closed dead-zone box $\mathcal B_J$ 不相交；對 axis-aligned rectangle，等價於

$$
\exists j:\quad L_j/D_{jj}>\delta_J
\quad\text{或}\quad U_j/D_{jj}< -\delta_J.
$$

碰到 boundary、跨過 box 或完全落在 box 內都為 `FAIL`，不是 numerical
`INCONCLUSIVE`。不得事後挑一個效果較大的座標；規則是預先固定的 scaled $L_\infty$
joint gate。

---

## 5. E2：兩個 target-null equivalence claims

E2 是兩個不同且都承重的 same-pipeline comparisons：

1. `(T-plus-null-A, T-plus-null-B)`；
2. `(T-minus-null-A, T-minus-null-B)`。

`e2_null_pair_spec` 將 plus pair 的兩臂都固定到 item 2 的
`stage5c-hard-controls-sprinkle-control-p-theta-v0.1`、$\theta=+0.4$，minus pair 則同一
source、$\theta=-0.4$。A／B 不是不同 target 或不同 generator；它們只能是 item 9 日後
配置的兩個 fresh、互異 pool identities／seed streams。typed spec 本身不接受 seed，也不
呼叫 generator。

兩者各自形成 §2 rectangle。equivalence margin 固定為 normalized coordinates 的

$$
\delta_E=(1/20,1/20).
$$

單一 comparison 只有在完整 normalized rectangle 嚴格落入 open box
$(-\delta_E,\delta_E)^2$ 時 `PASS`；任一座標碰界或越界即 `FAIL`。Selector split 只有在
plus-null 與 minus-null 兩個 claims 都通過時才可通過 E2。這是 simultaneous interval
inclusion，等價承擔兩座標 TOST 的嚴格判準。

$B\ge32$ 只是 item 2 calibration 的結構 floor，不是 E2 power 宣稱。item 8 必須以此固定
margin、最壞登記 variance／distribution 與 adjusted $\alpha$ 反推每個 null claim 自己的
cohort floor，且只能提高、不能降低 32。

---

## 6. E3：完整 simultaneous component rules

E3 discrimination arms 仍須先通過 item 6 的 Gate O；本節只固定 Gate E statistical rule。
方向為 0 的座標不是忽略，而是必須直接用 §2 已 directed-outward 的 normalized
lower／upper bounds 通過 §5 open-box equivalence component；不得先以 binary64
round-to-nearest 形成 raw margin $D_{jj}/20$ 再比較。

| Claim | ordered arms／contrast | coordinate 1 | coordinate 2 |
| :--- | :--- | :--- | :--- |
| correct chiral vs sector blind | `correct-chiral - sector-blind` | full region $>1/10$ | equivalent to 0 |
| symmetric diffusion vs sector blind | `symmetric-diffusion - sector-blind` | full region $<-1/10$ | full region $>1/10$ |
| correct vs active wrong support | `correct-support - wrong-support` | full region $>g_*/2$ | equivalent to 0 |
| sector-blind null | `sector-blind-null-A - sector-blind-null-B` | equivalent to 0 | equivalent to 0 |

其中 item 6 的 complete-domain analytic separation 是
$g_*\approx0.051303234639605456$，故 frozen wrong-support floor
$g_*/2\approx0.025651617319802728$。chiral／diffusion 的 complete-domain planted magnitude
下界為 $1/5$，同樣保留一半 gap 成為 $1/10$ floor。所有列都要求兩個 component rules
同時通過；boundary equality 一律失敗。

Item 6 早期以 correct／wrong 兩個 marginal regions 不相交描述 finite-causet success rule；
item 2 隨後凍結了 matched-pair law 與必須保留的 cross-arm covariance。為避免 marginalization
丟掉該 covariance，本交付以同一 orientation 的直接 paired contrast region 取代早期寫法，
並在 `STAGE5C_6A_E_CERTIFICATION.md` 明記此具體化。這不是放寬到只比較 point estimates：
完整 contrast region 仍須嚴格清除 $g_*/2$，且第二分量同時承擔 equivalence gate。

Global sector swap 不使用 statistical region：它仍依 item 6 的 canonical relabel construction
要求相同 operation trace 與逐位元完全相等。

---

## 7. df-only analytic falsifier

Item 2 已證明刪除 nonzero cross-arm covariance blocks 會失效，但其 $\rho=0$ cell 無法單獨
檢出「covariance target 正確、reference df 錯置」。本交付另固定
`stage5c-6a-e-df-only-t-reference-oracle-v0.1`：

- $B=32$ independent cohorts、每 cohort $m=192$、$p=2$、local $\alpha=0.01$；
- covariance／standard-error target 完全不變；正確 reference df 是 $31$；
- falsifier **只**把 df 換成總 pairs 的 $Bm-1=6143$；
- 在真實 pivot $T\sim t_{31}$ 的解析 oracle 下，以 Student-$t$ CDF 直接計算，不用 RNG。

每座標 nominal coverage 是 $1-\alpha/p=0.995$。正確 critical value 的解析 coverage 是
$0.9950000000000001$（binary64 evaluation）；df-only falsifier coverage 是
$0.99145302805641$，coverage gap 約 $0.00354697194>0$，因此機械判為 detected。
這個 oracle 只認證 df-only 錯置的方向與非零 coverage loss；它不配置 confirmatory alpha，
也不替代 item 8 的實際 claim-family power audit。

---

## 8. Closure 與未完成義務

本交付使 closure items 4／5 與 E3 statistical-region 子項成為 `REVIEW-PENDING`，不是
`CLOSED`。必須等 exact-head 獨立複核、CI、automated review、merge，再另作 state-only
closeout。Item 8 的完整 claim family、lineage-wide multiplicity／successor reserve、local
$\alpha$ allocation、detection／equivalence power與 power-derived cohort floors仍為 `OPEN`。
Items 9、10、12 仍 `OPEN`，item 11 仍 `DRAFT`。

在 closure matrix 12 列全部 `CLOSED` 前，不得生成第一個 6a-E seed，不得建立或讀取 arm
ledger，不得形成、保存或顯示 arm endpoint，也不得用這些 regions 評測任何候選 $K$。
