# Stage 5C 6a-E closure items 3＋6 — numerical certification and planted controls

狀態：**【candidate-independent 交付物／v0.1；REVIEW-PENDING】**。本文共同交付
`STAGE5C_6A_E_PREREGISTRATION_DRAFT.md` closure items 3 與 6 的 certification algebra、
shared planted domain、具名 $\Sigma_{C7/E3}$ support mapping、active wrong-support Gate O/E，
以及 global-swap exact-relabel trace proof。獨立 review、CI 與 merge 前不得標為 `CLOSED`。

本文不設計候選 $K$、不讀任何 arm ledger、不生成 6a-E seed，也不形成 arm／scientific
endpoint。所有數值只來自下列 candidate-independent 解析 construction。items 2、4、5、7–10
與 12 仍為 `OPEN`，item 11 仍為 `DRAFT`，故 6a-E 仍不可執行。

---

## 1. Typed certification input

兩個不同 implementation identity 分別回傳

$$
(\widehat M_k,\eta_k,\mathsf{id}_k),\qquad k=1,2,
$$

其中 $\widehat M_k\in\mathbb C^{2\times2}$，而 $\eta_k$ 是下列五個 Frobenius-norm
上界的和：

$$
\eta_k=\eta_{Q,k}+\eta_{S,k}+\eta_{R,k}+\eta_{B,k}+\eta_{F,k}.
\tag{1}
$$

依序代表 quadrature、sampling／finite representation、regulator、boundary／contact 與
floating-point accumulation。每一項必須是 finite nonnegative **validated upper bound**；缺欄、
負值、NaN／Inf 或兩個 implementation identity 相同是 schema violation，不得降格為
scientific `FAIL`。

設第 $k$ 路固定 accumulation order 含 $n_k$ 次 real additions，所有 matrix terms 的
Frobenius norm 和為 $A_k$。binary64 unit roundoff 為 $u=2^{-53}$，本 contract 固定

$$
\gamma_{n_k}=\frac{n_ku}{1-n_ku},\qquad
\eta_{F,k}=\gamma_{n_k}A_k,\qquad n_ku<1.
\tag{2}
$$

式 (2) 把 rounding 明確映到 accumulation length 與實際尺度；不得以裸 `machine epsilon`
或全域 `1e-12` 代替。`analysis/stage5c_numerical_certification.py` 對正向上界作 outward
rounding，matrix center 的兩次 binary64 operation 另計入 center error。

本文固定 error schema 與組合公式；closure item 7 仍須為 live continuum sequence 交付
$\eta_Q,\eta_S,\eta_R,\eta_B$ 的 validated producer、fixed-scale convergence／leakage criteria
與 resource cap。雙實作 agreement 只認證 quadrature／accumulation；依 item 1／J2，它不得
單獨升格為 geometry、Jacobian、support、boundary 或 biweight 的 mapping certificate。

---

## 2. 三階段 certification 與 boundary conventions

### 2.1 Independent-implementation agreement

先計算

$$
d=\|\widehat M_1-\widehat M_2\|_F,
\qquad E=\eta_1+\eta_2.
$$

agreement region 是閉集合：

$$
\boxed{d\le E.}
\tag{3}
$$

executable comparison 以 $d$ 的 outward upper enclosure 對 $E$ 的 inward lower enclosure；
因此 floating-point 無法證明恰在邊界內時會保守 fail closed，而不會把外部點誤收為 agreement。

$d>E$ 記 `INCONCLUSIVE/IMPLEMENTATION-DISAGREEMENT`。若提供 planted analytic truth $M_\star$，
還必須**分別**滿足 $\|\widehat M_k-M_\star\|_F\le\eta_k$；兩路共同偏移即使 $d=0$ 仍記
`INCONCLUSIVE/PLANTED-GROUND-TRUTH-MISMATCH`。這是 agreement 不得冒充整體 mapping
certification 的 executable 落點。

### 2.2 Strict nonzero certificate

令

$$
\bar M=\frac{\widehat M_1+\widehat M_2}{2},\qquad
\bar\eta=\frac{\eta_1+\eta_2}{2}+\eta_{\rm center},
$$

其中 $\eta_{\rm center}$ 是平均運算本身依式 (2) 型式得到的 outward binary64 bound。定義

$$
L=\operatorname{down}(\|\bar M\|_F-\bar\eta),\qquad
U=\operatorname{up}(\|\bar M\|_F+\bar\eta).
$$

nontriviality region 是開集合：

$$
\boxed{L>0.}
\tag{4}
$$

因此 $L=0$ 明確不通過，記 `INCONCLUSIVE/NORM-INTERVAL-TOUCHES-ZERO`；兩路與 error
皆逐位元 exact zero 時另記 `INCONCLUSIVE/EXACT-ZERO`。任一路 non-finite 先記
`INCONCLUSIVE/NONFINITE-BACKEND`。所有這些分支都在形成 ratio 前 short-circuit，endpoint
相關欄位必須為 `None/NOT-EVALUATED`，不得保存或顯示 provisional value。

### 2.3 Ratio uncertainty

只有 §2.1–§2.2 clean 才可在 candidate-independent test 或日後合法 runner 中形成
$\mathfrak I_G(\bar M)$。寫 $r=\|\bar M\|_F$ 並令

$$
\Delta_N=\bar\eta(2r+\bar\eta).
\tag{5}
$$

對 $\|\Delta M\|_F\le\bar\eta$，squared norm 的變動至多 $\Delta_N$。利用
$|\Delta Q|\le2\Delta_N$、$|\Delta(2|W|)|\le\Delta_N$、
$|\Delta S|\le\Delta_N$，以及兩個 endpoint 的 sharp bounds，固定 simultaneous
component-wise numerical enclosure

$$
\varepsilon_1=\frac{5\Delta_N}{L^2},\qquad
\varepsilon_2=\frac{2\Delta_N}{L^2}.
\tag{6}
$$

第一分量的係數 $5=3+2$：numerator perturbation 為 $3\Delta_N$，ratio denominator 項以
$|I_1|\le2$ 給 $2\Delta_N$；第二分量用 $1+1$。最終 interval 對式 (6) outward rounding，
並以 endpoint source 的 32 次 real-operation bound $\gamma_{32}\max(1,|I_j|)$ 再擴張，
最後與已證 sharp support $[-1,2]\times[0,1]$ 相交。任何 non-finite enclosure 記
`INCONCLUSIVE/RATIO-ERROR-UNBOUNDED`。這是 numerical enclosure，不是 E1／E3 statistical
confidence region；items 4、6、8 的 multiplicity／power 不能以它取代。

---

## 3. Items 3＋6 共用的 planted domain

near-zero 與 swap trace 都是 protocol-instance kill switch；兩者不得各自挑一套有利尺度。
source-of-record `analysis/stage5c_planted_certification.py` 固定同一個
`stage5c-6a-e-shared-planted-domain-v0.1`：

| 軸 | 完整 domain | executable boundary／interior suite | 結構來源 |
| :--- | :--- | :--- | :--- |
| selected pair count $n$ | $32\le n\le\binom{128}{2}=8128$ | $32,512,8128$ | frozen C8 minimum 與 $N=128$ 全 pair upper bound |
| cancellation $\kappa_A=A/\|M_\star\|_F$ | $1\le\kappa_A\le8128$ | $1,32,8128$ | triangle inequality 與 pair-count upper bound |
| matrix 2-norm condition | $1\le\kappa_2\le7$ | 各 family boundary | 下列三 family 的解析 extrema |
| common matrix scale $s$ | $2^{-503}\le s\le2^{504}$ | $2^{-503},1,2^{504}$ | binary64 exponent、最大 coefficient $3$、最大 cancellation 及二次 endpoint 的安全範圍 |

scale exponent 不是經驗 tolerance。binary64 `minexp=-1022`、`maxexp=1024`；對最大
arithmetic magnification $3\cdot8128$ 預留
$m=\lceil\log_2(3\cdot8128)\rceil=15$ bits，再因 endpoint 是二次式取

$$
e_{\min}=\left\lceil\frac{-1022+m}{2}\right\rceil=-503,
\qquad
e_{\max}=\left\lfloor\frac{1024-1-m}{2}\right\rfloor=504.
$$

planted accumulator 以權重 $(1+\kappa_A)/2,(1-\kappa_A)/2,0,\ldots,0$ 建立 exact analytic
sum $M_\star$，再以 forward／reverse fixed orders 作兩個 implementation。它分離測試 pair
count 與 cancellation；weight formation／scalar multiplication 以 $\gamma_4A$ 計入
$\eta_S$，accumulation 則把 $A=\sum_i\|T_i\|_F$ 交給式 (2)，不從 observed residual 回填 error。

三個完整 algebraic domains 是

$$
sI,\qquad s\operatorname{diag}(1,r),\;2\le r\le3,
\qquad s\begin{pmatrix}1&g\\g&1\end{pmatrix},\;\frac12\le g\le\frac34.
\tag{7}
$$

其 condition ranges 分別是 $1$、$[2,3]$ 與
$[(1+g)/(1-g)]=[3,7]$；endpoint regions 分別是

$$
(0,0),\qquad ([1/5,2/5],0),\qquad
\{(-x,x):x\in[1/5,9/25]\}.
\tag{8}
$$

所有 scale、condition、near-zero、common-mode bias、agreement 與 non-finite branches 均以
解析 truth 錨定。這套 suite 是 certification feasibility/failure evidence，不是 arm effect
calibration，也不得用來選 E1 effect floor。

---

## 4. 具名 $\Sigma_{C7/E3}$ active wrong-support mapping

support-mapping identity 固定為 `sigma-c7-e3-null-support-map-v0.1`。它是 L4 evaluator-side
test-function mapping，不加入、替換或重排 $\Sigma_{C8}$ 的 11 members，也不得回流候選構造。

固定 flat $\theta=0$ unit diamond、canonical $(U/R,V/L)$ output legs、normalization 1 與

$$
r_{\lambda,s}(x,y)=s\exp\{\lambda(u_x-u_y)\},
\qquad 2\le\lambda\le\frac52,
\tag{9}
$$

其中 $s$ 使用 §3 的同一 scale domain。correct support 使用
$u_y\le u_x$、$v_y\le v_x$；active intervention 保持 frame、test function、normalization、
output legs 全部不變，只把 support relation 反轉為 $u_y\ge u_x$、$v_y\ge v_x$。完成
characteristic delta 積分後：

$$
M_C=s\operatorname{diag}(R(\lambda),1/2),\quad
R(\lambda)=\frac{e^\lambda-1-\lambda}{\lambda^2},
$$

$$
M_W=s\operatorname{diag}(A(\lambda),1/2),\quad
A(\lambda)=\frac{\lambda-1+e^{-\lambda}}{\lambda^2}.
\tag{10}
$$

### 4.1 Gate O

對 $\lambda>0$，Taylor remainder 給 $R(\lambda)>1/2>A(\lambda)$。$G=T^2\rtimes S_2$
對 diagonal matrix 只能保留或交換 unordered diagonal spectrum；故式 (10) 在完整 domain
均不在同一 $G$-orbit，Gate O PASS。此判決使用完整 typed provenance，不把孤立矩陣命名為
wrong direction。

### 4.2 Gate E

令 $F(x)=(x-1/2)^2/(x^2+1/4)$，則兩邊 endpoint 均為 $(F(x),0)$，且
$F'(x)=(x^2-1/4)/(x^2+1/4)^2$。$R$ 隨 $\lambda$ 增、$A$ 隨 $\lambda$ 減；因此兩個
endpoint images 都在 domain boundary 取 extrema。executable source-of-record 以式 (10)
直接驗證

$$
\max_{\lambda\in[2,5/2]}F(A(\lambda))
<
\min_{\lambda\in[2,5/2]}F(R(\lambda)),
\tag{11}
$$

gap 為由解析式導出的正值（約 $0.0513032$），不是事後選的 threshold。故 deterministic
continuum support-mapping 的完整-domain Gate E PASS。未來 finite-causet E3 的 simultaneous
statistical region 必須沿用同一 orientation，且 success rule 固定為 wrong-support region 的
第一分量上界**嚴格小於** correct-support region 的第一分量下界；相等或交疊均 `FAIL`，
不得挑 projection 或改方向。item 2 尚須交付這些 simultaneous regions 的 joint matched law，
items 8–10 尚須交付 error allocation、power、fresh confirmation 與 runner；式 (11) 本身不
宣告 scientific E3 PASS。

direct Gauss–Legendre correct／reversed integrators各自對照式 (10)；correct branch 另對照
item-1 production retarded pairing。這三角錨定把 common geometry/support error 與單純雙路
agreement 分開。

---

## 5. Global swap exact-relabel／trace certificate

global swap 不重跑 pairing、不反轉 support、不重新累加。唯一 construction 是對同一個已累加
matrix 作 index permutation

$$
M\longmapsto\sigma_xM\sigma_x=M[\{1,0\},\{1,0\}].
\tag{12}
$$

source-term digest 與 `pairing-accumulate-fixed-order-binary64-v0.1` trace 必須前後相同，
`reaccumulated=false`；否則 certification stage 立即記
`INCONCLUSIVE/SWAP-NUMERICS-UNCERTIFIED`，scientific swap gate 為 `NOT-EVALUATED`。

primary endpoint source-of-record 改用 `stage5c-primary-endpoint-canonical-v0.1`：四個 norm
terms 先按 complex binary64 bit key canonical sort 後以 `fsum` reduction；$(a,d)$ 與 $(b,c)$
各自 canonical ordering，$|W|=|b||c|$。因此式 (12) 只排列同一 multiset，不改變 subtraction、
multiplication 或 reduction order。planted full grid 與另加的 10,000 個 fixed-seed finite-matrix
regression 均要求 `np.array_equal`，不是 tolerance equality。

trace failure suite 對 source digest mismatch、任何 reaccumulation、endpoint trace identity
mismatch、非 exact index permutation 與 bitwise endpoint mismatch 分別 fail closed。item 10
仍須把同一 typed record 接入 runner／ledger；在 item 10 完成前，本證明不構成 execution
authorization。

---

## 6. Closure 邊界

本 PR 將 items 3 與 6 標成 `REVIEW-PENDING`，只表示具名交付物已可供獨立檢查。只有獨立
review、green CI 與 merge 後，另以 state-only closeout 才可轉為 `CLOSED`。

仍未交付者包括：joint matched law（2）、E1／E2 statistical regions（4–5）、E4 live
validated error producers與 well-posedness（7）、lineage-wide multiplicity／power（8）、fresh
manifests（9）、runner／ledger／runtime trace（10）、與 runner 逐列一致的 final decision table
（11）及整體 review/merge closure（12）。因此不得生成 6a-E seed、開 arm numerical ledger、
或形成任何 arm endpoint。
