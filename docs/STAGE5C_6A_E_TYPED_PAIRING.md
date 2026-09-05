# Stage 5C 6a-E closure item 1 — typed continuum pairing

狀態：**【提案／v0.2；REVIEW-PENDING】**。本文件只交付
`STAGE5C_6A_E_PREREGISTRATION_DRAFT.md` closure item 1 的 candidate-independent
型別、公式與兩個實作；在獨立 review、CI 與 merge 前不得標為 `CLOSED`。

範圍：1+1D evaluator-side continuum oracle。本文不設計候選 $K$，不讀 6a-S arm
numerical ledger，不生成 6a-E seed，也不形成 $\mathfrak I_G$ 或任何 E1–E5 endpoint。

---

## 1. 唯一型別鏈

令 diamond interior 為 $D=(0,1)^2$，null coordinates 依序為 $(u,v)$，

$$
ds_\theta^2=-2p_\theta(u,v)\,du\,dv,
\qquad dV_\theta=p_\theta(u,v)\,du\,dv,
$$

$$
q(z)=6z^2-6z+1,
\qquad p_\theta(u,v)=1+\theta q(u)q(v),
\qquad -1<\theta<2.
$$

連續 spin fiber 是 trivial bundle $D\times W$、$W=\mathbb C^2$。canonical
representative 的 ordered frame 記為 $(e_R,e_L)$；evaluator 宣告

$$
\iota_{\rm sf}:U\mapsto e_R,\qquad V\mapsto e_L.
$$

這是 L4 evaluator identification，不是從 poset 推導。Stage 5A 只給無序對，故同步交換
$U\leftrightarrow V$ 與 $e_R\leftrightarrow e_L$ 是 gauge relabeling，不產生可報告方向。
本條完全限於 1+1D，不提供 3+1D spin structure。

fiber pairing 固定為 declared L2 Hermitian scaffold

$$
h(\psi,\phi)=\psi^\dagger\phi,
$$

第一槽 conjugate-linear、第二槽 linear。endomorphism adjoint 因而是
$A^\dagger=\overline A^{\,T}$；kernel adjoint 是

$$
S^\dagger(x,y)=S(y,x)^\dagger.
$$

沒有另加 Majorana／charge-conjugation real structure。scalar complex conjugation只用於
上述 Hermitian adjoint；不得把它算成由 order 湧現的 primitive。整體正尺度已依
`STAGE5C_D1_4_BASIS_GROUP.md` 吸收到 normalization，故 canonical representative 取
$h=\mathbb 1$。容許 global fixed-slot group 仍為
$G=T^2\rtimes S_2$，kernel 以 mixed-index similarity 變換

$$
S(x,y)\longmapsto B S(x,y)B^{-1}.
$$

---

## 2. Propagation representation 與 retarded inverse

本文固定的是 acceptance contract C7 所容許的 **propagation representation**，不是把
Clifford-Dirac operator 的某組 matrix entries 當成同一物件。flat massless operator 為

$$
\mathscr D_0=
\begin{pmatrix}\partial_u&0\\0&\partial_v\end{pmatrix},
$$

所以 $R$ sector 滿足 $\partial_u\psi_R=0$，$L$ sector 滿足
$\partial_v\psi_L=0$。其 retarded fundamental solution（相對於
$du_y\,dv_y$）固定為

$$
S_0(x,y)=
\begin{pmatrix}
H(u_x-u_y)\,\delta(v_x-v_y)&0\\
0&\delta(u_x-u_y)\,H(v_x-v_y)
\end{pmatrix}.
$$

共形 operator 與 retarded inverse 定義為

$$
\mathscr D_\theta
=p_\theta^{-3/4}\,\mathscr D_0\,p_\theta^{1/4},
$$

$$
\boxed{
S_\theta(x,y)=
p_\theta(x)^{-1/4}S_0(x,y)p_\theta(y)^{-1/4}}
\tag{1}
$$

（$p_\theta$ 是 scalar，左右乘法在 canonical frame 中可交換。）相對於 source-side
physical volume，式 (1) 滿足

$$
\mathscr D_{\theta,x}S_\theta(x,y)
=\delta_{g_\theta}(x,y)\mathbb 1,
\qquad
\delta_{g_\theta}(x,y)=p_\theta(x)^{-1}\delta^{(2)}(x-y).
$$

推導只用已宣告的 operator 與 distribution identity：$\mathscr D_0S_0=\delta^{(2)}I$；
在 contact support 上 $p_\theta(y)=p_\theta(x)$，兩個 $-1/4$ 權重與
$p_\theta^{-3/4}$ 合成 $p_\theta^{-1}$。這是本專案內部的 typed 定義／驗算，
不把尚未完成 equation／signature mapping 的外部文獻升格為承重來源。

令

$$
\operatorname{Dom}_0(\mathscr D_\theta)=
\{\psi\in C^1(\overline D,W):
\psi_R(0,v)=0,\ \psi_L(u,0)=0\}.
$$

以 $dV_\theta(y)$ 作 source integration，$S_\theta$ 同時滿足

$$
\mathscr D_\theta(S_\theta f)=f,
\qquad
S_\theta(\mathscr D_\theta\psi)=\psi
\quad(\psi\in\operatorname{Dom}_0).
\tag{2}
$$

第二式逐 sector 只是 fundamental theorem of calculus。例如 $R$ sector 為

$$
p_\theta(x)^{-1/4}\int_0^{u_x}
\partial_{u_y}\!\left[p_\theta(u_y,v_x)^{1/4}\psi_R(u_y,v_x)\right]du_y
=\psi_R(x),
$$

其中 incoming boundary term 由 $\psi_R(0,v)=0$ 消失；$L$ sector同理。這也明確排除
兩個 characteristic zero modes；不另設 outflow boundary condition。

---

## 3. Boundary、contact 與 advanced adjoint

retarded domain 固定為：$R$ sector 在 incoming face $u=0$ 取零資料；$L$ sector在
incoming face $v=0$ 取零資料。kernel 不作 boundary reflection，也不作 periodic
identification。$S_\theta$ 先作 $D\times D$ 上的 distribution，再以零延拓成
$\mathbb R^4$ 上的 distribution；因此 fixed-$\epsilon$ Gaussian 落在 box 外的質量不會
被悄悄 renormalize 回 box。其 leakage 大小與 E4 acceptance bound 仍屬 closure item 7，
本文不替它選 threshold。§2 的 inverse identities只在 diamond interior成立；零延拓只定義
pairing，不宣稱對零延拓後的 distribution 在整個 $\mathbb R^4$ 再作用 $\mathscr D_\theta$
時沒有 boundary distributions。

採 canonical representative $H(0)=1/2$。對本文允許的 smooth test density，characteristic
上的 contact intersection 是較低維集合，故此代表值不改變 pairing；contact normalization
由 $\partial H=\delta$ 唯一固定。任何額外 $\delta^{(2)}(x-y)$ contact term、image term、
boundary counterterm 或 Gaussian renormalization 均不在本 contract 中，加入即須 protocol
amendment。

retarded adjoint固定為 advanced kernel

$$
S_A(x,y)=S_R(y,x)^\dagger.
$$

故 $S_R$ 不被宣稱 self-adjoint；把 retarded 與 advanced 靜默混用屬 object-type error。

---

## 4. 與 induced test measure 的線性 pairing

座標排列唯一固定為

$$
z=(u_x,v_x,u_y,v_y).
$$

executable input 是 vectorized scalar density：輸入 shape `(...,4)` 必須輸出 shape `(...)`
的有限 complex values；錯 shape 或 non-finite value 立即拒絕，不作 scalar fallback、broadcast
或缺值替換。

令 $\nu$ 是 `STAGE5C_D1_3_OBSERVABLE_CONTRACT.md` §4 的 finite measure；在
fixed-$\epsilon$ 後，其相對於 $d^4z$ 的 smooth density 記為 $r(z)$。pairing 是

$$
M_\theta[r]=\langle S_\theta,r\rangle
=\int_{D\times D}S_\theta(x,y)r(x,y)\,d^2x\,d^2y.
\tag{3}
$$

注意式 (3) 是 distribution 對 scalar test density 的逐 matrix-entry 線性作用；不是
spinor inner product、不是 pointwise determinant，也不另乘 $dV_xdV_y$。$S_\theta$ 作為
physical-volume normalized inverse所需的 metric factors 已在式 (1) 固定；$r$ 則是
induced measure 相對於 coordinate Lebesgue measure 的 density。兩者不得重複加權。

以 characteristic delta 完成一個積分後，唯一公式為

$$
[M_\theta(r)]_{RR}=
\int_0^1du_x\int_0^{u_x}du_y\int_0^1dv\,
[p_\theta(u_x,v)p_\theta(u_y,v)]^{-1/4}
r(u_x,v,u_y,v),
\tag{4a}
$$

$$
[M_\theta(r)]_{LL}=
\int_0^1dv_x\int_0^{v_x}dv_y\int_0^1du\,
[p_\theta(u,v_x)p_\theta(u,v_y)]^{-1/4}
r(u,v_x,u,v_y),
\tag{4b}
$$

且 $[M]_{RL}=[M]_{LR}=0$。式 (4) 的對角性是這個 massless planted continuum object的
性質，不是對任何未來候選 $K$ 的 block constraint。

對 $B\in G$，先被動搬動 kernel 再 pairing 給
$M\mapsto BMB^{-1}$；因此後續才可把同一個已選定的 $\mathfrak I_G$ 作用在 $M$ 上。
本文與 executable module 刻意不 import／呼叫 $\mathfrak I_G$。
executable 的 `transform_global_basis` 只接受 $G=T^2\rtimes S_2$ 的 unitary monomial
matrix，不是一般 $GL(2)$ 工具：monomial slot pattern 是型別條件，unitarity residual 以
matrix norm 做 scale mapping，另要求 2-norm reciprocal condition number 通過由 unitary
群結構導出的 frozen bound；輸出亦須 finite。不得用裸的 `det == 0` 把病態 basis 當成
合法 gauge operation。

---

## 5. 兩個 independent implementations

source-of-record 是 `analysis/stage5c_continuum_pairing.py`：

1. `pair_retarded_gauss_legendre`：把兩個 characteristic triangles 各自映到 unit cube，
   以固定階 Gauss–Legendre tensor product求積，triangle Jacobian 明寫在 integrand；
2. `pair_retarded_adaptive`：獨立建立 characteristic-cube integrand，以 adaptive
   Genz–Malik cubature 求積；不使用第一個實作的 Gauss–Legendre nodes／weights／accumulator，
   未達 caller 要求的 error target 時 fail closed。

兩條積分路徑彼此不呼叫，但它們刻意共用本文件唯一允許的 characteristic geometry、
unit-cube parameterization、triangle Jacobian $a$、boundary prescription、conformal biweight
與 density validation。因此 implementation agreement **只認證 quadrature／accumulation**；
它不獨立認證上述共用幾何、Jacobian、support、boundary 或 biweight。那些共用部分必須由
與兩路 agreement 分離的解析／planted regressions 錨定，item 3 與 item 7 不得把 agreement
bound 單獨升格為整個 continuum mapping 的 certification。

`tests/test_stage5c_continuum_pairing.py` 固定下列 mapping regressions：

- flat constant、$u_x$、$u_y$ 與 $u_xu_y$ density 的封閉解析值，獨立錨定
  characteristic domain 與 Jacobian；
- 與既有 `stage5c_hard_controls.py` 的 $q,p_\theta$ 定義逐位元 mapping；
- $p_\theta^{-1/4}(x)p_\theta^{-1/4}(y)$ curved／flat reweighting identity；
- retarded／acausal support與 incoming-boundary convention；
- 直接在 advanced support 上另行參數化的積分 oracle，對照 retarded-adjoint 實作；
- global phase與 sector-swap covariance；
- 對 candidate-independent planted Gaussian measure，兩個獨立實作互相吻合。

這些 tests 只驗 mapping／型別與 planted numerics。它們不固定 E4 的 quadrature order、
validated error bound、implementation-agreement acceptance threshold、contact／boundary leakage
threshold或 resource cap；上述仍分屬 closure items 3 與 7。故本 PR 即使通過，也不授權
形成 arm endpoint。

---

## 6. Closure 邊界

item 1 只有在本文件、兩個 implementations、mapping tests、CI、獨立 review 與 merge全數
完成後才可由 `REVIEW-PENDING` 改成 `CLOSED`。下列項目明確仍未交付：

- $\Pi_{\mathcal M}$ joint matched law（item 2）；
- near-zero／ratio certification（item 3）；
- E1–E3 scientific regions與 active wrong-support（items 4–6）；
- E4 fixed-scale sequence、leakage／convergence／agreement bounds（item 7）；
- power、fresh manifests 與 runner（items 8–10）。

因此本文件封閉的是「要算哪一個 typed linear pairing」，不是「數值已可算」或
「6a-E 已接近可執行」。
