# Stage 5C — 6a-E E4 fixed-scale well-posedness contract

狀態：**【closure item 7／REVIEW-PENDING／不可執行】**。

本文件只交付 candidate-independent 的 E4 continuum pairing、leakage 與 validated-error
契約。source-of-record 是 `analysis/stage5c_e4_wellposedness.py`，契約 identity 為
`stage5c-6a-e-e4-wellposedness-v0.1`。它不讀 arm ledger、不生成或 claim 6a-E seed、不形成
arm endpoint，也不設計、import 或執行候選 kernel $K$。在本項經獨立 review、CI 與 merge
前，closure item 7 不得記為 `CLOSED`；其他 closure items 與 execution firewall 均不變。

---

## 1. 固定 target 與 test-function topology

本項沿用 typed-pairing source-of-record 的 unit diamond、zero incoming／no reflection／zero
extension、$H(0)=1/2$、contact normalization 與

$$
S_\theta(x,y)=p_\theta(x)^{-1/4}S_0(x,y)p_\theta(y)^{-1/4},
\qquad
p_\theta(u,v)=1+\theta q(u)q(v),
$$

其中 $q(z)=6z^2-6z+1$、$\theta\in[-0.4,0.4]$。$-1/4$ biweight 與
$\mathscr D_xS=\delta_g I$ 的 delta normalization 是本項承重 prescription，不得改成
degree-zero surrogate。

test-function topology 固定為 ordered pair space $\mathbb R^4$ 上的有限 probability Gaussian
mixtures：

$$
r(z)=\sum_{i=1}^{m}w_i(2\pi\epsilon^2)^{-2}
 \exp\!\left(-\frac{\lVert z-z_i\rVert^2}{2\epsilon^2}\right),
\qquad \epsilon=1/16,
$$

其中 $1\le m\le8128$、$w_i\ge0$、$\sum_iw_i=1$，且每個 centre 嚴格位於 unit
four-box 並滿足 $u_x>u_y$、$v_x>v_y$。topology identity 是
`finite-probability-gaussian-mixtures-fixed-epsilon-v0.1`。有限 mixture 是每次 run 的精確
test density；finite sample 對母體 law 的統計不確定性屬 items 4／5 regions，不得重複塞入
本項的 quadrature error。

這是 fixed-$\epsilon$ target，**沒有 $\epsilon\to0$、regulator removal 或依 box retained mass
重新正規化的主張**。

---

## 2. Pairing existence 與 order-zero continuity

在 $q([0,1])=[-1/2,1]$ 與完整 $\theta$ domain 上，

$$
p_{\min}(\theta)=
\begin{cases}
1+\theta,&\theta<0,\\
1-\theta/2,&\theta\ge0,
\end{cases}
\qquad p_{\min}\ge0.6.
$$

因此 conformal biweight 有界，兩個 characteristic triangles 各有 Lebesgue mass $1/2$；對
sup-norm test density，typed pairing 滿足可執行 regression 所固定的 bound

$$
\left\lVert\langle S_\theta,r\rangle\right\rVert_F
\le \frac{\lVert r\rVert_\infty}{\sqrt{2p_{\min}(\theta)}}.
$$

Gaussian mixtures 平滑且有界，故 pairing 作為 order-zero distribution 對上述 topology
存在且連續。這個 existence proof 使用原 typed kernel 的 biweight 與 delta normalization，
不是由兩個 numerics 恰好相近反推。

---

## 3. Contact 與 boundary leakage

對 centre $z_i$，ambient Gaussian 落在 unit four-box 的 retained mass 解析為

$$
B_i=\prod_{k=1}^{4}
\left[\Phi\!\left(\frac{1-z_{ik}}{\epsilon}\right)
-\Phi\!\left(\frac{-z_{ik}}{\epsilon}\right)\right].
$$

兩個 causal difference 相互獨立且 variance 為 $2\epsilon^2$，所以 ambient causal retained
mass 為

$$
C_i=\Phi\!\left(\frac{u_x-u_y}{\sqrt2\epsilon}\right)
     \Phi\!\left(\frac{v_x-v_y}{\sqrt2\epsilon}\right).
$$

source-of-record 必須報告 $1-\sum_iw_iB_i$ 與 $1-\sum_iw_iC_i$，但不得以其倒數
renormalize。令

$$
b_*=\Phi(1/\epsilon)-\frac12=\frac12-\Phi(-16).
$$

對任一 strict-interior centre，每個 coordinate retained mass 嚴格大於 open-boundary limit
$b_*$，所以只靠 topology 可推出的 box leakage 一致界為

$$
1-\sum_iw_iB_i < 1-b_*^4.
$$

這個 universal 上界因 opposite-boundary Gaussian tail 而略大於 $15/16$；strict interior
**不**普遍推出原已登記的 box leakage $<15/16$ gate。因此 implementation 另以
cancellation-safe tail arithmetic 驗證實際 mixture retained mass $>1/16$：對每個 coordinate
令 $d=\min(z,1-z)$ 並保留

$$
\Delta(d)=\frac12\operatorname{erf}\!\left(\frac{d}{\sqrt2\epsilon}\right)
-\frac12\operatorname{erfc}\!\left(\frac{1-d}{\sqrt2\epsilon}\right),
$$

再以 `log1p(2*Delta)`／`expm1` 計算各 atom 相對於 $1/16$ 的 excess，最後用 compensated
summation 加權。excess 不嚴格為正即 `STRUCTURAL_LEAKAGE_INVALID`；不得把 rounded
`box_retained_mass == 1/16` 當作通過。strict causal gaps 沒有對側 box tail，仍保證 causal
leakage $<3/4$。Gaussian mixture 對 Lebesgue measure 絕對連續，故 exact contact atom mass
為零；$H(0)$ 的 choice 不產生額外 $\delta^2$ contact mass。box 外與 retarded-support 外的
部分依既有 zero-extension prescription 精確歸零。

上述 strict bounds 是由已驗證的幾何不等式承重，不由 binary64 CDF 輸出重新判定。若正座標
或正 causal gap 小於一個可分辨的 CDF increment，`ndtr` 可把 binary64 retained masses 捨入
為 $1/16$ 或 $1/4$。尤其 sub-ULP boundary case 的 exact box retained mass 可略低於 $1/16$，
因為 opposite-boundary tail 大於其極小的正 boundary displacement；這不是 topology failure，
但會使原 box-leakage gate 不成立，故 E4 必須 fail closed。rounded values 仍是 diagnostic，
不得用來覆寫上述 stable gate。任何 diagnostic 若 non-finite 或離開 probability range，亦
fail closed。

因此 leakage 是必存的 scientific diagnostic，不是被漏算的 numerical error。若 centre、
probability mass、strict ordering 或 8128-atom cap 不合法，應在 pairing 前拒絕，不能靠
renormalization 修補。

---

## 4. Fixed-scale continuum enclosure sequence

兩個非零 diagonal sector 直接改用 characteristic coordinates $(a,b,t)$：

$$
M_R=\int_0^1\!da\int_0^a\!db\int_0^1\!dt\;
[p_\theta(a,t)p_\theta(b,t)]^{-1/4}r(a,t,b,t),
$$

$$
M_L=\int_0^1\!da\int_0^a\!db\int_0^1\!dt\;
[p_\theta(t,a)p_\theta(t,b)]^{-1/4}r(t,a,t,b).
$$

凍結 dyadic levels 為 pair axes $n=(16,32,64)$，transverse axis 為 $n/4$ cells。每層：

1. 對完全位於 $b<a$ 的 cells，用 normal-CDF difference 解析計算每個 Gaussian factor 的
   cell mass；
2. 對與 $b=a$ 相交的 diagonal cells，下界取零、上界取整個 square 的 Gaussian mass；
3. 由 quadratic $q$ 在 cell 上的 exact extrema、interval products 與 monotonic
   $x^{-1/4}$ 得 conformal biweight 上下界；
4. analytic special-function factors 使用凍結的 64-ULP binary64 outward margin；正值
   products／sums 另以其實際 atom／cell operation-count 的 $\gamma_n$ factor 向外擴張；
5. 各層產生 $[L_R^{(n)},U_R^{(n)}]\times[L_L^{(n)},U_L^{(n)}]$，最終取三層
   intersection：$L=\max_nL^{(n)}$、$U=\min_nU^{(n)}$。

每一層本身已是 continuum integral 的 enclosure；sequence 不是用 successive differences
猜 truncation error。cell refinement 令 biweight oscillation 與 diagonal cover 寬度趨零，
所以在固定 $\epsilon$ 下收斂。若 level endpoints non-finite、次序顛倒或 intersection 為空，
numerical certification 必須 fail closed。

enclosure identity 是 `positive-gaussian-characteristic-cell-enclosure-v0.1`。這條路徑不呼叫
Gauss–Legendre 或 SciPy adaptive cubature，也不使用兩個 production outputs 的 agreement
residual 來製造自己的 allowance。

---

## 5. 兩個 implementations 與 validated ErrorBudget

兩個值路徑固定為：

- `gauss-legendre-32-with-cell-enclosure-v0.1`：既有 fixed-order tensor GL32
  characteristic-cube implementation；
- `adaptive-genz-malik-with-cell-enclosure-v0.1`：另行建構 integrand 的 adaptive
  Genz–Malik implementation，`rtol=2^-14`、`atol=2^-30`、最多 4096 subdivisions。

對任一 implementation matrix $\widehat M$，validated quadrature component 是它到 enclosure
最遠 corner 的 Frobenius distance：

$$
\eta_Q(\widehat M)=
\sqrt{\max(|\widehat M_R-L_R|,|U_R-\widehat M_R|)^2+
      \max(|\widehat M_L-L_L|,|U_L-\widehat M_L|)^2},
$$

另加任何 off-diagonal 或 imaginary components 到 Frobenius norm。此定義保證 enclosure 中的
exact diagonal matrix 位於以 $\widehat M$ 為中心、radius $\eta_Q$ 的 closed ball。

`ErrorBudget` 的其餘 live components 固定如下：

| component | 值 | 理由 |
| :--- | :---: | :--- |
| $\eta_S$ sampling representation | 0 | finite empirical mixture 是本次 exact input；母體 sampling uncertainty 留給 statistical region |
| $\eta_R$ regulator | 0 | $\epsilon=1/16$ 是 target，不是待移除 approximation |
| $\eta_B$ boundary/contact | 0 | zero extension 與 no-contact-atom 是 exact prescription；leakage 另列 |
| rounding | 0 | $\eta_Q$ 以實際 returned binary64 matrix 為中心到 enclosure 最遠 corner，已涵蓋該輸出的 discretization 與全部 arithmetic displacement；不得另以不完整的 operation recount 偽造較小 bound |

SciPy `cubature.error` 只存為 **algorithm diagnostic**。它是 estimated error，明禁直接或經
固定倍率升格為 validated upper bound。兩 implementation 仍須通過 item-3 的 closed error-ball
agreement、strict nonzero 與 ratio propagation；任一項不 clean 均為 `INCONCLUSIVE`，不得形成
scientific endpoint。

adaptive solver 若回傳 non-finite matrix 或 non-finite algorithm-error diagnostic，固定為
`INCONCLUSIVE/NONFINITE_BACKEND`；若在 4096 subdivisions 內未回報 `converged`，即使
enclosure 或另一實作看似
良好，仍固定為 `INCONCLUSIVE/ADAPTIVE_RESOURCE_CAP`。不得續跑、臨時加 cap 或把 solver
estimate 當 scientific `FAIL`。

---

## 6. Candidate-independent feasibility／failure suite

`tests/test_stage5c_e4_wellposedness.py` 固定且不使用 RNG：

- 在 $\theta=(-0.4,0,0.4)$ 上，以 interior three-atom probability mixture 同時跑 GL32、
  Genz–Malik、三層 enclosure 與 item-3 certification；兩值路徑都必須落在 enclosure 並得到
  `CLEAN/CERTIFIED`；
- 以 near-box-boundary 與 near-contact centres 驗 leakage 非零但 pairing 仍 well-defined，
  且不做 retained-mass renormalization；
- 以 positive sub-ULP coordinates／gaps 驗 topology validator 仍接受 strict geometry，但
  cancellation-safe box gate 得 `STRUCTURAL_LEAKAGE_INVALID`；另以 high-precision oracle
  驗 exact box leakage 大於 $15/16$、但嚴格小於 $1-b_*^4$ universal boundary-limit 界；
- 驗完整 $\theta$ domain 的 $p_{\min}$ 與 order-zero operator bound；
- boundary centre、contact centre、非 probability weights、超過 8128 atoms 與未登記
  $\theta$ 必須在求值前拒絕；
- 注入 adaptive resource exhaustion 必須得到
  `INCONCLUSIVE/ADAPTIVE_RESOURCE_CAP`；
- 分別注入 non-finite adaptive matrix，以及 finite matrix 配 non-finite error diagnostic，兩者
  都必須得到 `INCONCLUSIVE/NONFINITE_BACKEND`；
- 明確驗證 adaptive algorithm diagnostic 小於 validated enclosure error 時，`ErrorBudget`
  仍只能採後者，防止 estimated-error undercoverage。

此 suite 只證明 frozen E4 contract 的可執行性與 fail-closed branches，不是 E1–E3 scientific
gate、沒有 arm effect、也不提供 selector 排序資訊。

---

## 7. Closure 與仍然禁止的事

本 PR 的合法狀態只有 `REVIEW-PENDING`。item 7 只有在本文件、source-of-record、tests、完整
CI 與 Claude 對實際 final tree 的獨立 review 均通過並合併後，才可由後續 state-only
closeout 改為 `CLOSED`。

即使 item 7 關閉，items 4／5 的 statistical regions 與 df-only falsifier、item 8 power／
multiplicity、item 9 manifests、item 10 runner／ledger、item 11 final decision table、item 12
整體 review 仍未完成。故不得生成 6a-E seed、不得開 arm ledger、不得形成 arm endpoint，
也不得觸及候選 $K$。
