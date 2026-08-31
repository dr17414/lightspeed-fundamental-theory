# Stage 5C D.1 第 3 項 — Unified Observable／Selector／Smearing／Norm Contract

狀態：**【提案／v0.10 草案；尚未 freeze】** — fork B、ambient norm、完整 invariant algebra、C3b blind-variety distance form、primary 二維 invariant endpoint 與 wrong-direction 的 gauge 邊界已交付；selector／measure／smearing／normalization、active wrong-support control 與統計 contract 仍待完成。

路線：**B（distributional selector）**。依 review 意見，A 為**暫不採用**，不是被排除。

基準：`docs/STAGE5C_ACCEPTANCE.md` v0.9+、`docs/STAGE5C_C8_4_HARD_CONTROLS.md`、
`docs/STAGE5C_D1_3_REFERENCE_PROBE.md`、`docs/STAGE5C_D1_3_PROBE_RESULTS.md`。
驗證於 main `b5a1b79`：50 檔、integrity 通過、128 passed。（歷史快照，不隨 HEAD 更新。）

---

## 0. 本文件不建立的事

三條由 review 指出、必須寫在最前面：

1. **`CONTROL-VIABLE` 不蘊涵合格 $\Sigma$ 存在。** reference probe 證明的是一組固定 43 維
   全域摘要能區分 matched ensembles。合格 $\Sigma$ 另需 intrinsic selector、two-point
   $K$-observable mapping、sector covariance 與可計算 $\mu_\theta$；四者皆不由前者推出。
   本文件**不得**引用 probe 結果作為 $\Sigma$ 存在性的證據。
2. **路線 A 未被否證。** 因果集理論本以 order + cardinality 統計恢復幾何尺度
   （Myrheim–Meyer；BLMS, *Phys. Rev. Lett.* **59**, 521；Surya, *Living Rev. Rel.* 22:5）。
   「單一 Alexandrov interval 無法分離 $\rho$ 與 $\tau$」推不出「無法定位指定 $s,t$」。
   選 B 是**工程選擇**，不是 no-go。若 B 失敗，A 仍是開放路線。
3. **共形權重公式只是起草基礎，不是 contract。**
   $S_\theta(x,y)=p_\theta(x)^{-1/4}p_\theta(y)^{-1/4}S_{\text{flat}}(x,y)$ 是 **bi-spinor**
   陳述，其成立需要 spin-frame identification、signature、adjoint、Green-function
   prescription 與 boundary condition 全部宣告（Dirac 算子的共形協變性見
   Clerc–Ørsted, arXiv:1409.4983，僅作非承重 cross-check）。兩個 scalar conformal weights **不**構成
   basis-invariant propagator contract。§1 列出必須補齊的宣告。

本文件採 acceptance spec §5.2.1(v) 的**非承重文獻路徑**：上述 BLMS／Surya／
Clerc–Ørsted 只界定已知背景或作 cross-check，不決定本文件的 observable、selector、
formula、prescription 或 threshold。若要升格承重，必須先完成 D.1 第 8 項 mapping。

本文件亦不提出任何候選 $K$。

---

## 1. Object 與 type chain

補齊 acceptance spec §3 對 C6/C7/C8 的部分。

### 1.1 階段可用性約束〔關鍵一致性要求〕

C8 在 **Stage 5C-1** 執行，而 $W$（Wightman）與 $\rho$（spectral）的 evaluator／
derivation chain 延後至 Freeze-1b／Freeze-2b。因此：

> C6/C7/C8 的 primary observable **必須只依賴 $\mathcal K$ 與 $G_R$**，不得依賴 $W$、
> $\rho$ 或任何狀態宣告。任何需要 $W$ 的端點形式在 Stage 5C-1 判 PROTOCOL-INVALID。

### 1.2 連續側宣告（evaluator-side）

- **Signature** $(-,+)$；null 座標 $ds_\theta^2=-2p_\theta(u,v)\,du\,dv$，$p_\theta>0$。
- **Clifford**：coordinate indices 用 $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}$；frame indices
  則用 $\{\gamma^a,\gamma^b\}=2\eta^{ab}$，兩者不得混寫。它只存在於 evaluator side，依 spec §3
  列為 **L4 evaluation oracle**；不得進入 $K$ 的構造路徑。
- **Spin frame**：宣告一組全域 null spin frame $(o,\iota)$，與 $U/V$ 兩個 null 方向對齊。
- **Green-function prescription**：**retarded**。$G_R$ 的 left／right inverse 或明定
  composition/contact law、domain、zero modes 與 diamond 上的零過去資料須寫入 dossier；
  只驗 $\mathcal K G_R=\mathbb 1$ 的單側有限矩陣等式不足。
- **Bi-spinor 型別**：$G_R(x,y)$ 在 $x$ 帶一個 fiber index、在 $y$ 帶一個 co-fiber index；
  兩者的變換律由 §1.4 的 pairing 決定，**不得**當成兩個獨立純量權重相乘。

### 1.3 離散側沒有 spin frame——identification 是宣告，不是推導

離散側只有 bookkeeping fiber $F_x=\{(x,U),(x,V)\}$，**沒有 local Lorentz 結構、沒有
Clifford 表示**。把 $F_x$ 與連續 spin frame 對應起來是 evaluator 中的一個**宣告映射**
$\iota_{\text{sf}}$，不是從 $\mathcal I_0$ 導出的。

$\iota_{\text{sf}}$ 的合法性完全依賴 1+1D 的兩個 global null total orders（Stage 5A），
因此**這正是 C11 firewall 在本 contract 中的落點**：$\iota_{\text{sf}}$ 必須在 dossier
中逐項標為 1+1D-only，且不得作為 3+1D 可外推的證據。

### 1.4 Pairing、adjoint、fiber trivialization 與可容許基底群

宣告 fiber 上的雙線性 pairing $\langle\cdot,\cdot\rangle$、reality structure，以及
是否存在把所有 $F_x$ 識別為同一 model fiber 的**全域 trivialization**。令
$W=L_U\oplus L_V$；對目前只以裸 smeared matrix $M$ 作 endpoint 的 fixed-slot contract，
可容許群須精確寫為

$$
G=\operatorname{Stab}_{GL(W)}(\{L_U,L_V\})
\cap\operatorname{Aut}(\text{pairing},\text{reality},\text{basis conventions}).
$$

$G$ **必須包含** sector swap $\sigma_x$（Stage 5A 的 $S_2$ 商）。若 dossier 只允許
global basis change，必須明寫其物理與離散來源；在此已證明的全域 trivialization 下，
$\mathcal K$ 作為 kernel 在 $B\in G$ 下

$$\mathcal K(x,y)\ \longmapsto\ B\,\mathcal K(x,y)\,B^{-1},
\qquad G_R(x,y)\ \longmapsto\ B\,G_R(x,y)\,B^{-1}.$$

若 dossier 宣告的 pairing 使第二個 index 為 conjugate，則變換律改為 $B\cdot B^\dagger$，
且 §2.2 的不變量集合必須同步重算——**不得沿用本文件的結論而不重算**。

若宣稱容許端點各自獨立的 local basis change，正確型別律是

$$G_R(x,y)\longmapsto B_xG_R(x,y)B_y^{-1}$$

（conjugate convention 亦須相應修改）。此時單一 cross-fiber matrix 的 trace／determinant
一般**不是** scalar；必須先提供合法的 transport／pairing／composition 把兩端 indices
收縮。沒有 connection primitive 時，不得一面宣稱 local covariance，一面使用 global
similarity 的不變量。

此處必須區分：任意 $B\in GL(W)$ 仍可作**被動座標變換**，但須同時搬動 sector
projectors、pairing 與 reality tensors；它不等於上述把 sector slots 固定、只對 $M$
作用的 gauge group。若要採 full passive covariance，endpoint 必須把這些 tensors 一起
納入 typed functional，不能仍引用裸 $M$ 的 invariant family。

`docs/STAGE5C_D1_4_BASIS_GROUP.md` 已證明 fixed-slot 群只可落在
$S_2\subseteq G\subseteq(\mathbb C^\times)^2\rtimes S_2$，並以兩項具名前提完成 fork B：
C3b 的 norm 是完整 object domain 上連續正定的 invariant norm；C0 最小 primitive 紀律要求
只宣告該 norm 所需的最小結構，並採其完整 stabilizer。據此宣告

$$h=p\mathbb 1\quad(p>0),\qquad G=T^2\rtimes S_2,
\qquad G_{\mathrm{eff}}=U(1)\rtimes S_2.$$

$h/\mathbb R_{>0}$ 是 **declared L2 pairing／adjoint scaffold**，不是 poset-derived 亦不是
L4 oracle；整體尺度 $p$ 吸收到 $\mathcal N$，只有其數值若被保留才按 L3 normalization
計入。basis-group 決議本身沒有選定 primary $\mathfrak I_G$；其後
`docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md` 已另行選定二維 real invariant vector。這仍不表示
§1.4 或本 contract 已 freeze。

fork B 的 ambient norm 已有顯式見證
$\|M\|_F=\sqrt{\operatorname{tr}(MM^\dagger)}$；其連續性、正定性與
$T^2\rtimes S_2$-invariance 由 basis-group 文件命題 6 證明。這只 discharge ambient-norm
existence。`docs/STAGE5C_C3B_BLIND_DISTANCE.md` 另已固定 value-level rank-one Segre
blind-variety 的 SVD 距離形式，並修正「任意 fixed endomorphism 有限和」其實張成整個
pointwise output space、不能取 quotient 的型別錯誤。C3b 的 program／capability schema、
pair domain／weights、非平凡性與 effect-size／noise／continuum thresholds 仍未具體固定；
不得把 ambient norm 或距離形式升格為 C3b 已完整交付。

`docs/STAGE5C_D1_4_INVARIANT_ALGEBRA.md` 已交付 fork B 的完整 complexified-real invariant
ring：生成集由
$A=a+d,P=ad,W=bc,S=|b|^2+|c|^2,Q=|a-d|^2,
R=(a-d)(|b|^2-|c|^2)$ 及其共軛構成，final relation ideal 由 symmetric rank-one
$3\times3$ matrix 的六個 $2\times2$ minors 生成。該代數交付物本身不選 primary；後續
primary endpoint 交付物已依其限制固定

$$
\mathfrak I_G(M)=\left(\frac{Q-2|W|}{N^2},\frac{S}{N^2}\right),\qquad
N^2=\operatorname{tr}(MM^\dagger).
$$

它是二維 real invariant vector，不是單一純量；完整證明、sharp bounds 與推論上限見
`docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md`。第一分量中 $|W|$ 的係數 $2$ 是具名 evaluator
convention，不是代數定理；更改須走 protocol amendment。其符號只作記帳，不得解讀為
物理方向。wrong-direction E3 仍未完成。

---

## 2. Primary observable

### 2.1 型別要求

primary observable $\mathcal O$ 是由 $G_R$（或 $\mathcal K$）建構的**有限維實值向量**，且

> 離散側與連續側必須是**同一個 typed、basis-covariant 數學泛函**。可有兩個獨立
> implementation，但須共用一份形式規格、以 planted finite cases 逐項證明 mapping
> equivalence；不要求把離散 sum 與 continuum distribution 強塞進同一程式函數。
> 事後更換 mapping 判 PROTOCOL-INVALID。

### 2.2 $S_2$ 商真正強制的形式〔修正過強 invariant claim〕

$G\ni\sigma_x$，故任何**被報告的**端點必須是 $\sigma_x$-不變的。但「$G$ 包含
$\sigma_x$」**不能**推出全部 $G$-不變量由 $\operatorname{tr}M$ 與 $\det M$ 生成。
反例是只取 $G=\{1,\sigma_x\}$：$M_{12}+M_{21}$ 在 swap conjugation 下不變，卻不由
trace／determinant 決定（零矩陣與 $\left(\begin{smallmatrix}0&1\\0&0\end{smallmatrix}\right)$
已有相同 trace／determinant）。

因此 Freeze-1a 必須引用 §1.4 已定案的 fork B、pairing、global basis convention、完整
invariant algebra 與已選定的二維 real $\mathfrak I_G$，並補完 reality／adjoint 細節及
尚缺的 planted-family proof。
現行 fixed-slot contract 的 $G$ 嚴格落在 monomial stabilizer 內，故 full
$GL(2,\mathbb C)$ similarity 的 trace／determinant 生成捷徑**不可用**；若作用涉及
$M^\dagger$、只含 sector swap，或選其他中間 subgroup，皆須使用該文件相應結果或重算。

在已證明的 massless diagonal special case
$M=\operatorname{diag}(m_U,m_V)$，任何 polynomial sector-symmetric endpoint 可由

$$\operatorname{tr}M=m_U+m_V,\qquad \det M=m_U m_V,$$

即 $\{m_U,m_V\}$ 的初等對稱函數生成。這只是一個**特例 witness**，不是本 contract
在 object/basis contract 尚未固定前的通用結論。

真正的硬條件是：

> 被報告的 C6/C7/C8 向量 $\mathfrak I_G(M)$ 的每個分量必須對已宣告的 $G$ 不變，特別是對
> $U\leftrightarrow V$ 不變。任何單獨指認「$U$ 通道」或「$V$ 通道」的最終端點
> **不可容許**；但可用的 invariant family 不得在 $G$ 固定前預先冒充為 trace／determinant。

這不是設計選擇，是 Stage 5A 上限 $\{U,V\}/S_2$ 的直接後果：離散側從未導出有序對，
只導出無序對。

**允許 covariant 中間量.** 內部可使用有序對或非不變中間量，但必須宣告其變換律，
且**最終報告的向量分量必須不變**。covariant 中間量不得被引用為結果。

### 2.3 端點的一般形式：先 linear smearing，再取 invariant

continuum $G_R$ 是 bi-spinor-valued **distribution**。先逐點形成
$\det G_R(x,y)$ 再積分，一般會要求未定義的 distribution 乘積。因此 primary endpoint
必須先作 linear smearing：

對每個 causet $C$ 先定義

$$M_C[K;\Sigma,\varphi]
=\mathcal N_C^{-1}\!\!\sum_{(x,y)\in\Sigma(C)}\varphi_C(x,y)\,G_R^C(x,y),
\qquad
\mathcal O_C[K;\Sigma,\varphi]=\mathfrak I_G(M_C).$$

continuum 側以 §4 的同一 weighted test measure pairing 得到 $M_\theta^{\rm cont}$，再取
$\mathfrak I_G$。$\mathfrak I_G$ 已固定為具 §2.2 proof 的二維、實值、
dimensional-consistent vector map；若含 determinant、absolute value、complex phase、
branch、截斷或 regulator，其定義域與上界規則一併固定。任何確實需要 nonlinear
pointwise product 的替代端點，必須先交付合法的 distribution-product／renormalization
prescription，否則判 PROTOCOL-INVALID。

現行 $|W|=\sqrt{W\bar W}$ 採唯一非負 branch，且作用在 linear smearing 後的有限矩陣，
不涉及 distribution 的 pointwise product。任何報告用 scalar aggregation 只可在 Freeze-1a
事前固定，且不得取代二維 law 或逐分量 planted separation。

reported quantity 是 causet-level $\mathcal O_C$ 的 ensemble law、mean、variance／concentration
與 continuum extrapolation。一般 $\mathbb E[\mathfrak I_G(M_C)]\ne
\mathfrak I_G(\mathbb E[M_C])$；continuum target 必須依 §4.2 的 candidate-independent
random-measure law 事前固定。invariant-of-mean 只可在 §4.2 的 concentration／continuity／
uniform-integrability theorem 已證時作為同一 target 的計算簡化，不得依 $K$ 的結果換型。

---

## 3. Selector $\Sigma$

### 3.1 型別

$\Sigma$ 從 causet $(\mathcal C,\prec,\#)$ 選出一個**有序對的集合**（或其加權），
供 §2.3 求和。

### 3.2 硬性禁令

本節禁令作用於 C8 distributional selector $\Sigma_{C8}$。$\Sigma_{C8}$ **不得**使用：
座標；$\theta$；target label；seed；`ControlSample` 中除
`order` 以外的任何欄位；reference probe 的 feature bank、權重、分數或任何成功模式；
候選 $K$ 的任何輸出；任何 source/sink oracle 或外部指定的區域。

實作上只接受 `BlindedCase` 介面，並以 payload falsifier 測試涵蓋（比照
`tests/test_stage5c_reference_probe.py::test_feature_bank_rejects_non_blinded_payloads`）。

C6 的 nested-region／bulk-boundary strata 依 acceptance spec C6 可使用 L4 evaluation oracle；
它們必須另列為 $\Sigma_{C6}$，只供 evaluator、不得回流 construction，也不得冒充為
C8 的 intrinsic selector。C7 若使用 gate-specific test-function selector，亦須獨立明列
其 L4 權限。不得用「共用 contract」把 C6/C7 的 oracle 權限偷偷帶入 $\Sigma_{C8}$。

### 3.3 不變性

- **relabeling-invariant**：元素標號置換下，$\Sigma$ 隨之共變（選出的對集合被同一置換搬動）。
- **sector swap**：$\Sigma$ 必須對全域 $U\leftrightarrow V$ 交換**不變**，或宣告明確的
  covariance 律；若宣告 covariance，§2.2 的最終純量仍必須不變。

### 3.4 Form、capacity 與 provenance 在 Freeze-1a 固定

- **Form**：$\Sigma$ 的函數形式與可調自由度在候選 $K$ 出現前寫定。
- **Capacity**：宣告一個**有限的** selector family $\mathcal F_\Sigma$，並固定 $|\mathcal F_\Sigma|$。
  無界 family 使 $\Sigma$ 變成一次隱蔽搜尋，判 PROTOCOL-INVALID。**有限成員數仍不足**：
  每個成員須另列 source dependency、description length、自由參數數、lookup／table 大小、
  branch count、optimizer 與 RNG；單一任意程式或無限制 lookup 即使只算「一個成員」，
  仍屬無界容量。此 ledger 沿用 acceptance spec §4.1–4.2 的 L2/L3 capacity audit。
- **Provenance**：$\mathcal F_\Sigma$ 的每個成員必須有書面來源理由，且只許引用
  數學必要條件、既有 STATUS 結論，或依 spec §5.2.1(v) 具**承重資格**的外部文獻。

### 3.5 選取規則：first-past-the-post，不得 argmax〔反擬合〕

「$\Sigma$ 不得為放大 $T_+-T_-$ 而擬合」與「$\Sigma$ 必須通過 effect floor」表面衝突。
解法是**不許最佳化，只許依序取第一個合格者**：

> $\mathcal F_\Sigma$ 的成員在**任何成員求值前的 selector-prereg commit** 固定一個
> 評測順序。先依 §6a-S 作 contrast-free batch prefilter，再保持原始順序依次執行
> §6a-E selection-split feasibility，取第一個完整通過者；
> **不得**評測全部成員再取效應量最大者。

first-past-the-post **不會自行消除 selection bias**。第一個通過者必須在完全 fresh、
事前保留的 selector-confirmation split 上，以不重擬、不改 threshold 的方式重跑 §6；
confirmation 亦全過後才可記 `SELECTOR-VIABLE` 並寫入最終 Freeze-1a commit。若失敗，
該成員與資料 burned，再依事前規則決定是否續測下一成員；每個進入 6a-E 的成員都依
原始 family 位置使用預登記的 family-wise $\alpha$／e-value spending。不得用 selection split 的 effect estimate 作端點
承重數值。

因此時間順序是：selector-prereg commit $\to$ sequential selection／fresh confirmation
$\to$ 最終單一 Freeze-1a commit。已評測成員、兩種 split、判決與 spending 均記入
獨立 selector ledger；不得混入 protocol-amendment log，也不得回充 candidate holdout。

**6a-S 與 6a-E 的資料與多重性分工必須分開。** 6a-S 全部是 contrast-free 的
selector／measure prefilter，只能在**同一 target 內**的獨立 blocks 上批次執行，且其
data streams 必須與 6a-E 的 between-target streams 不相交。通過 6a-S 的成員仍保留
selector-prereg commit 中的原始順序；只有會讀取 $T_+$ vs $T_-$ contrast 的 6a-E
採嚴格 sequential first-past-the-post、fresh confirmation 與 family-wise spending。
6a-S 淘汰本身不消耗 contrast family 的 $\alpha$，但也**不得**把被淘汰位置的配置
靜默重分配給後續成員；除非 selector-prereg commit 已固定一個具有效性證明的 recycling
rule，否則 6a-E 的配置以原始有序 family 為準。日後若任何 6a-S 檢定改為讀取
between-target contrast，它自動改列 6a-E，受相同序列、fresh-confirmation 與 spending
管制；不得只改名稱保留 batch screening。

---

## 4. 誘導 weighted test measure、$\mu_\theta$ 與 smearing

### 4.1 型別正確的 induced measure

$\Sigma$ 不需定位任何座標點。先以 raw ensemble 說明型別：對離散樣本 $C$ 及其 sealed embedding coordinates
$X_i=(u_i,v_i)$，先定義隨機 weighted pair measure 及其完整機率律

$$
\widetilde\nu^{C}_{\Sigma,\varphi}
=\mathcal N_C^{-1}\!\!\sum_{(i,j)\in\Sigma(C)}
\varphi_C(i,j)\,\delta_{(X_i,X_j)},
\qquad
\nu^{C,\epsilon}_{\Sigma,\varphi}=R_{\epsilon,g}
  \widetilde\nu^{C}_{\Sigma,\varphi},
\qquad
\Pi^{(N,\epsilon)}_{\theta,g}=\operatorname{Law}_{C\sim T^{(N)}_{\theta,g}}
  (\nu^{C,\epsilon_g}_{\Sigma_g,\varphi_g}),
\qquad
\Pi^{\mathrm{cont}}_{\theta,g}
=\lim_{(N,\epsilon)\to(\infty,0)}\Pi^{(N,\epsilon)}_{\theta,g},
\qquad
\bar\nu^{\mathrm{cont}}_{\theta,g}
=\mathbb E_{\nu\sim\Pi^{\mathrm{cont}}_{\theta,g}}[\nu].
$$

$g\in\{C6,C7,C8\}$ 指 gate-specific sampling／selector instance；上式的 limit 是弱收斂
或 contract 另行指定的更強 topology，且必須在 §6a-E 證明存在。下文簡寫
$\Pi_{\theta,g}=\Pi^{\mathrm{cont}}_{\theta,g}$；$\bar\nu^{\mathrm{cont}}_{\theta,g}$
只是其第一矩。
$R_{\epsilon,g}$ 是在 selector-prereg commit 固定的**線性** mollifier／regulator；
$N\to\infty$、$\epsilon_g\to0$（或固定 physical smearing scale）的聯合順序、rate 與
admissible test-function topology 必須一併預登記。
$\bar\nu^{\mathrm{cont}}_{\theta,g}$ 是位於 ordered spacetime-pair space（四個 coordinate components）上的
有限 signed／complex measure；其 base measure、orientation、是否排除 diagonal／contact
set、以及 total variation bound 必須明寫。要與 distribution $S_\theta$ pairing，它在固定
mollifier／regulator 後必須收斂到 admissible smooth compactly-supported test density（或
另證明 $S_\theta$ 對該較弱 measure class 為 order-zero distribution）。finite empirical
delta measure $\widetilde\nu^C$ 本身不自動屬於 test-function space。只有在 $\varphi=1$ 且再作明定 normalization
時，才把對應的非負 measure 稱為 $\mu_\theta$。不得把 variable pair count 的 raw intensity、
conditional-on-selection probability 與 normalized density 靜默混用。

**C8 必須使用 matched induced-measure law。** Axis B 的 continuum target 不是上式的 raw
$\Pi_{\theta,C8}$ 或 $\bar\nu^{\mathrm{cont}}_{\theta,C8}$，而是 matching lifecycle 誘導的 joint two-arm law
$\Pi_{\mathcal M}$ 及其 arm marginals $\Pi_{\theta\mid\mathcal M}$；expectation 必須涵蓋 C8.1 的
兩臂 pool generation、calibration scale、matching、calipers、unmatched handling 與 pair
weights，再條件於樣本被納入 matched cohort。其 continuum 第一矩才記為
$\bar\nu^{\mathrm{cont}}_{\theta\mid\mathcal M}$。$\mathcal M$ 是 joint two-arm procedure，不能以兩個
獨立 raw marginals 代替。$T_+$ vs $T_+$／$T_-$ vs $T_-$ null controls 亦須走
同一 $\mathcal M$ lifecycle。C6/C7 的 gate-specific measures 則按各自預登記 sampling
design 另記，不得與 C8 measure 靜默混用。

兩個 arm-specific marginals 只足以算 mean contrast；C8 的 paired effect／power 還須保留
$\mathcal M$ 誘導的 joint matched-pair law 與 covariance。不得把 paired variance 以兩個
獨立 marginal variances 相加取代。

計算流程（**evaluator-side、獨立、固定**）：由 $p_\theta$ 抽 sprinkling $\to$ 只把
`order` 交給 $\Sigma$ $\to$ 取回被選中元素的 sealed 座標 $\to$ 累積經驗分布。

**硬性規定**：

- 該流程在 selector-prereg commit 固定，**不得**為放大 $T_+-T_-$ 而調整 bin、bandwidth、
  樣本數、measure normalization 或任何步驟；
- 使用**專屬且與候選評估不相交**的 seed 段；
- 其實作與候選評估路徑分離，$\Sigma$ 在此流程中仍只看得到 `order`。

### 4.2 連續預測

continuum target 從一開始就由 §4.1 的**完整、candidate-independent induced-measure law**
定義。令

$$
Z^{\mathrm{cont}}_{\theta,g}(\nu)
=\mathfrak I_G\!\left(\left\langle S_\theta,\nu\right\rangle\right),
\qquad \nu\sim\Pi_{\theta,g},
$$

並以其 joint law、mean vector、covariance／marginal quantiles 作登記的 continuum predictions；
若 primary statistic 是 mean vector，則

$$
\mathcal O^{\mathrm{cont}}_{\theta,g}
=\mathbb E_{\nu\sim\Pi_{\theta,g}}
 \left[\mathfrak I_G\!\left(\left\langle S_\theta,\nu\right\rangle\right)\right].
$$

只有在 selector-prereg contract 指定的 continuum sequence 上，另證
$\Pi_{\theta,g}$ concentration、$\mathfrak I_G$ 在 relevant domain 連續、所需矩具
uniform integrability，且 nonlinear bias 在登記容差內時，才可使用簡化式
$\mathfrak I_G(\langle S_\theta,\bar\nu^{\mathrm{cont}}_{\theta,g}\rangle)$。此簡化是已證 theorem 的
計算捷徑，**不是**依 candidate 表現選擇的替代 target。若條件不成立，完整 law-based
target 仍原封不動；不得在 Freeze-2a 從 invariant-of-mean 靜默切換成 mean-of-invariant，
或反向切換。

C8 時上式必須對 $\Pi_{\mathcal M}$ 的 joint matched-pair law 計算 paired contrast 與
variance，不能只用兩個 $\Pi_{\theta\mid\mathcal M}$ marginals 重建獨立-arm variance。

此處 $\langle\cdot,\cdot\rangle$ 是 bi-spinor distribution 對 §4.1 test measure 的**線性**
pairing，不是 pointwise determinant。$S_\theta$ 依 §1 的 bi-spinor 宣告構造；contact／boundary
singularity 若使 pairing 不存在，必須在候選前修正 test space 或交付 regulator proof。

$T_+$ 與 $T_-$ 的預測差可以來自 $\bar\nu_\theta$、$S_\theta$，或兩者共同作用；本 contract
**不要求** $\mu_+\ne\mu_-$。完整 $\mathcal O^{\rm cont}_+-\mathcal O^{\rm cont}_-$ 的方向、
最小差距與 numerical uncertainty 必須在最終 Freeze-1a 前由 §6 的 fresh confirmation 承重。
Freeze-1a 固定 $\Pi$、continuum sequence、允許的 concentration theorem、統計 functional
與誤差門檻；6b 只檢查 candidate 的離散 endpoint law／moments 是否收斂到這個既定 target，
不得替 contract 選 target。

### 4.3 Smearing $\varphi$

$\varphi_C$ 必須：relabeling-invariant；只依賴 order 與 $\#$；在 selector-prereg commit
固定形式與所有尺度參數的上界規則；且其與 $\Sigma,\mathcal N$ 共同誘導的
$\Pi^{(N,\epsilon)}_{\theta,g}$ 存在穩定 continuum limit。若 $\varphi$ 可為負或複數，須另報 total variation／phase
cancellation 與數值穩定性，不能只報 signed mean。

---

## 5. Normalization $\mathcal N$

$\mathcal N$ 的作用是讓端點跨 causet、跨密度、跨連續／離散可比。要求：

1. **只由 order + $\#$ 構成**（離散側），且有明確的連續對應；
2. 形式與上界規則在 selector-prereg commit 固定，最終寫入 Freeze-1a；**不得**在
   calibration 上擬合以放大對比；
3. 必須宣告整體尺度重標度 $p_\theta\to c\,p_\theta$ 時，固定的是 physical region、
   sprinkling density、expected cardinality 或哪一組無因次量，並推導 $\mathcal O$ 的
   dimensional covariance。**不得**預設常數 conformal factor 在 order+number 下不可觀測：
   cardinality 正是 continuum volume 的離散對應。只有在已宣告的 matched-$N$／ratio
   endpoint 中證明 scale cancellation 後，才可要求 invariance；
4. $\mathcal N=0$ 或數值不穩定時判 INCONCLUSIVE，不得改換 $\mathcal N$。

---

## 6. Selector／evaluator feasibility（候選前必須通過）

### 6.1 可測與不可測的切分〔誠實聲明〕

$\mathcal O$ 的 candidate realization 是 $K$ 的泛函，而 Freeze-1a 時 $K$ 尚不存在；
但這**不允許**把 evaluator 自身的 power／well-posedness 全部推到 Freeze-2a。切分為：

- **6a-S — selector／induced-measure feasibility（候選前必須通過）**：不需要 $K$；
- **6a-E — endpoint-evaluator feasibility（候選前必須通過）**：用 continuum target 與
  planted operator／Green-function objects，不使用任何候選；
- **6b — candidate endpoint realization（Freeze-2a，需要 $K$）**：判準形式在 Freeze-1a
  固定，candidate-specific tolerance／sample size 在 Freeze-2a 固定後執行。

宣稱 6a-S 通過即等同 evaluator 或 candidate endpoint 可行，判 PROTOCOL-INVALID；
反之，聲稱「因為 $K$ 尚不存在，所以 6a-E 無法測」同樣判 PROTOCOL-INVALID。

### 6.2 6a-S：selector／measure 檢定

| 檢定 | 內容 | 通過條件 |
| :--- | :--- | :--- |
| **S1 well-definedness** | $\Sigma$ 在宣告 domain 內恆有輸出、選中對數在預登記區間內 | 全部樣本成立 |
| **S2 relabel** | 隨機置換下共變 | 逐位元 |
| **S3 sector swap** | 不變，或符合宣告 covariance | 逐位元 |
| **S4 blinding／capacity** | payload falsifier；L2/L3 ledger 與 family bound | 全部通過 |
| **S5 $\Pi_{\theta,g}$／$\bar\nu_{\theta,g}$ 穩定性** | **同一 target 內**獨立 blocks 間 random-measure law／weighted mean measure 的預登記距離、total mass／variation | 在容差內 |
| **S6 coverage／well-conditioning** | pair coverage、contact/boundary exclusion、$\mathcal N$、effective sample size | 全過 floor |

**不得**把 $\mu_+\ne\mu_-$ 或其他 induced-distribution divergence 設為 selector 的普遍
必要條件：完整 endpoint 差可以只由 $S_\theta$ 產生；反之 measure 有差也可能在
$\mathfrak I_G\circ\langle S_\theta,\cdot\rangle$ 下完全抵消。distribution divergence
可作 secondary diagnostic，但不能替代 6a-E。

S1–S6 皆不得讀取 between-target contrast；可在各 target 內批次執行。其資料必須與
6a-E selection／confirmation streams 分離。若修改後有任何 S 檢定接觸 between-target
contrast，依 §3.5 自動改列 6a-E 並納入 sequential spending。

### 6.3 6a-E：candidate-independent endpoint-evaluator 檢定

在 §2–§5 的完整形式固定後，對每個通過 6a-S 的 selector 執行：

| 檢定 | 內容 | 通過條件 |
| :--- | :--- | :--- |
| **E1 continuum contrast** | 完整 $\mathcal O^{\rm cont}_+-\mathcal O^{\rm cont}_-$，含 integration uncertainty | 通過預登記的二維 contrast region／joint effect floor |
| **E2 target-null equivalence** | $T_+$ vs $T_+$ 與 $T_-$ vs $T_-$ 的同 pipeline multivariate equivalence test | 各自落入預登記 equivalence region |
| **E3 planted alternatives** | 預先固定的 correct chiral、symmetric-diffusion、sector-blind 與 active wrong-support objects 經同一 typed pipeline／endpoint；全域 sector swap 另作 invariance arm | discrimination arms 先過 orbit-admissibility，再按預登記二維 joint-law regions／逐分量規則可分；swap arm 逐位元相同 |
| **E4 distributional well-posedness** | smearing 前後、regulator removal、contact/boundary、兩個獨立 implementation | pairing 存在、收斂且互相吻合 |
| **E5-D detection power／multiplicity** | E1／E3 的 directional detection claims，在預登記樣本量與 multiplicity-adjusted $\alpha$ 下 | 每個承重 detection claim power $\ge0.90$ |
| **E5-E equivalence power／multiplicity** | E2 各 null arm 的 TOST／等效性 claim；由預登記 margin $\delta_E$、null variance／最壞分布與 multiplicity-adjusted $\alpha$ 反推 cohort floor | 每個承重 equivalence claim power $\ge0.90$ 且實際 cohort 達 floor |

E2 的必要性與 reference probe arm N 相同；E3 則是 acceptance spec C7 明定的 planted-
alternative 要求。E1–E4 與 E5-D／E5-E 的統計量、effect floor、equivalence margin、sample size、seed 段、
regulator sequence 與 failure semantics 全部在 selector-prereg commit 固定，不得在看過
任何成員結果後修改。selection split 通過後仍須依 §3.5 以 fresh confirmation 重驗。
E4 是 analysis／numerics 的 well-posedness claim，依預登記 error bound、coverage／convergence
criterion 與 implementation agreement 驗收；不得用「power $\ge0.90$」這個不適用的標籤
取代其誤差證明。6a-E 是唯一讀取 between-target contrast 的 selector 階段，必須依 §3.5
按原始 family 順序執行並納入 family-wise spending。

因 $\mathfrak I_G$ 為二維，E1／E2 的 joint metric、covariance handling、simultaneous region
與 multiplicity 必須在 selector-prereg commit 固定；不得把兩個分量事後挑一個報告，亦
不得用候選資料選 projection。E3 的五類代數符號樣式只完成部分 form proof。依
`docs/STAGE5C_E3_WRONG_DIRECTION.md`，全域 $\sigma_x$ sector swap 是 $G$-gauge，只能作
invariance arm；真正的 wrong direction 必須是固定 continuum frame 與 output legs、改動
support feeding 的 active typed intervention。它須先通過 orbit-admissibility，再以完整參數域的
endpoint-law separation 承重；$X\notin G\cdot R$ 本身不保證本二維 endpoint 可分。
selector tuple 與 active intervention 尚未定案，故此項仍是 blocking open item。

planted objects 僅為 evaluator-side positive／negative controls，**容許使用 L4 oracle**
（含 sealed coordinates、$\gamma$ 與 $\theta$）來構造，並須與 construction module 隔離；
其矩陣、權重、test functions 與成功模式不得列為候選材料或回流 C0 construction。
正因 planted family 可使用 C0 禁止進入 construction 的 oracle，**E3 PASS 只證明 evaluator
能區分這些 oracle-built objects；對是否存在合規的 order-only $K$、或該 $K$ 能否產生
相同物件，沒有任何蘊涵，也不得作為 Stage 5C-1 可行性證據。**

### 6.4 6b：candidate endpoint realization（Freeze-2a 執行）

端點層級另需：$\mathcal O_C$ 的離散 joint endpoint law 及其承重 moments／quantiles 收斂到
§4.2 固定的 $Z^{\mathrm{cont}}_{\theta,g}$ law（收斂率預登記）；
$T_+$ 與 $T_-$ 的離散端點差落入預登記二維 acceptance region 並達 joint effect floor；
null control 通過預登記 multivariate equivalence region；
且該差異在 §2.2 已證明的 invariant 層次成立，而非依賴任何 covariant 中間量。
§4.2 的 concentration 簡化若獲准，只是 continuum target 的 theorem-backed 計算法；
6b 不得依 candidate 重新開啟或撤回該選擇。收斂不成立時依事前規則記 candidate-level
FAIL，數值解析度不足則記 INCONCLUSIVE，**不得**改用另一 endpoint definition。6b 的
實質失敗是 candidate-specific FAIL；6a-S／6a-E 未完成或失敗時則 control／protocol
尚不可用，**不得**把風險轉嫁成候選 FAIL。

---

## 7. 與 C6／C7 的共用

三個 gate 共用同一個 base object、linear-smearing $\to\mathfrak I_G$ architecture、
dimensional／normalization convention 與 invariant proof；但**不強迫使用字面相同的
$\Sigma$**。C6 的 nested-region／boundary selector 與 C8 的 distributional selector
任務不同，須作為同一個 Freeze-1a selector family 中的具名、事前固定 instances：

- **C6**：influence range／boundary／scaling 三條曲線以同一 $\mathcal O$ 量測；
- **C7**：massless benchmark 的 ensemble 收斂以同一 architecture 陳述，chiral decoupling
  依 §2.2 的已證明 invariant family 表述，**不得**預設 determinant，亦不得只在某組基底下看起來對角；
- **C8**：Axis A／B 以同一 $\mathcal O$ 執行。

三個 gate 不得暗換 base object、pairing、smearing order 或 invariant semantics；允許的
gate-specific selector／test-function instances 必須在同一 contract 明列並一起通過
§6a-E planted tests。若某 gate 需要不同型別的物件，必須回到 acceptance spec §3
修改 object contract 並重新 freeze。

---

## 8. $L_\theta$ 的地位

$L_\theta=\frac14\log\frac{p_\theta(s)}{p_\theta(t)}$ 即日起**降級為 oracle motivation
與 cross-check**：

- 可用於論證兩個 target 的共形權重確有差異、方向為何；
- 可作為 §4.2 連續預測的**獨立健全性檢查**（量級與方向應相容）；
- **不再**是 C8 的 primary endpoint。

替代端點 $\mathcal O$ **只有在本 contract 全部條款（含 §6a-S／6a-E 的 fresh
confirmation 通過、§6b 判準固定）完成
並 freeze 之後**，才正式取代 $L_\theta$。在此之前 C8.4 的 §3.1 仍為現行登記端點，
且 C8 不得對任何候選執行。

reference probe 的 `CONTROL-VIABLE` 判決**不隨端點更換而自動延續**：它是對
`reference probe bank` 的陳述，不是對 $\mathcal O$ 的陳述。端點更換後，C8 的
residual-power 前提必須依 §6 重新建立。

---

## 9. 判決

| 情形 | 判決 |
| :--- | :--- |
| 依 §3.5 順序評測，第一個成員在 selection 與 fresh confirmation 均通過 §6.2–§6.3 | **SELECTOR-VIABLE**，採用該成員並停止評測 |
| $\mathcal F_\Sigma$ 全部成員評測完畢仍無通過者 | **BOUNDED-SEARCH-EXHAUSTED**（依 spec §2.1，為 Freeze-deliverable status），須記錄 $\mathcal F_\Sigma$、評測順序與資源；**不得**判 no-go |
| 算力不足、$\mathcal N$ 不穩定、cohort gate 未達 | **INCONCLUSIVE** |
| 未依 freeze 完成即執行，或違反 §3.2／§3.5／§4.1 任一禁令 | **PROTOCOL-INVALID** |

**明禁**：以放寬 effect floor、擴大 $\mathcal F_\Sigma$、改 $\bar\nu_\theta$ 流程或改 $\mathcal N$
的方式繞過 BOUNDED-SEARCH-EXHAUSTED。擴大 $\mathcal F_\Sigma$ 屬 protocol amendment，
須重新 freeze 並重新計 multiplicity。

若判 BOUNDED-SEARCH-EXHAUSTED，**路線 A 仍為開放選項**（§0 第 2 點），且應與
「修改 control」「修改 target 對」並列評估。

---

## 10. 本文件刻意不固定的事

- $\mathcal F_\Sigma$ 的**具體成員**——需與 GPT 議定後才寫入，且一經寫入即凍結；
- §1.4 fork B、完整 invariant algebra 與 primary 二維 real $\mathfrak I_G$ 雖已交付，仍須把
  global fiber trivialization、reality／adjoint 與 endpoint 寫成單一 frozen typed contract；
- $\varphi$、$\mathcal N$ 的具體函數形式與 dimensional covariance，以及二維 endpoint 的
  joint-law metric／只供報告使用的 scalar aggregation；
- $\Pi_{\theta,g}$／$\bar\nu_{\theta,g}$ 的 base measure、joint matched law、contact／boundary treatment、continuum／regulator sequence；
- E1–E4、E5-D／E5-E 的統計量、分開的 detection／equivalence floors 與 cohort gates、planted-alternative family、power 與 seed ranges；
- selector-prereg／ledger schema、family-wise spending 與 fresh-confirmation lifecycle；
- C3b program／capability boundary，以及 blind-variety contract 尚未固定的 pair domain、
  weights、nontriviality／effect-size／noise／continuum calibration；
- 任何 $K$ 的形式；
- C9／C10 的 immutable core（屬 D.1 第 7 項）。

上列 candidate-independent 項目全部寫定、預登記並通過 §6a-S／6a-E fresh confirmation
之前，D.1 第 3 項仍為 **PENDING**。因此本草案目前不是「只剩三個數值待填」，更不能
被引用為 Freeze-1a 已接近自動完成。

---

## 附錄 A — v0.2–v0.3 獨立 review 處置

| 發現 | 處置 |
| :--- | :--- |
| 只由 $G\ni\sigma_x$ 推出 trace／determinant 生成全部 invariants | 撤回；改為先固定 $G$ 與作用，再交完整 invariant-family proof；保留 diagonal polynomial special case |
| bi-fiber map 在 local basis change 下不是 similarity | §1.4 分開 global trivialization 與 $B_x\cdot B_y^{-1}$；無 transport 不得以 trace／det 冒充 scalar |
| 對 continuum distribution 逐點取 determinant | §2.3 改為先 linear smear 成有限矩陣，再取 $\mathfrak I_G$ |
| 有限 family 仍可藏入單一無界程式／lookup | §3.4 加入逐成員 L2/L3 capacity ledger |
| first-past-the-post 被誤當成消除 selection bias | §3.5 加 fresh selector-confirmation split 與 family-wise spending |
| raw intensity、conditional distribution、smearing 與 normalization 型別混用 | §4 改用 jointly normalized weighted pair measure $\bar\nu_\theta$ |
| C8 continuum target 以 raw marginals 取代 matched cohort | §4.1 改用 $\bar\nu_{\theta\mid\mathcal M}$ 並保留 joint matched-pair covariance |
| 把 $\mu_+\ne\mu_-$ 當 selector 必要條件 | 刪除；改驗完整 continuum endpoint，因差異可來自 $S_\theta$ 或 measure，亦可能互相抵消 |
| 因候選尚不存在而把全部 endpoint feasibility 推到 Freeze-2a | §6 拆 6a-S／6a-E／6b；continuum contrast、null、planted alternatives、distributional well-posedness 與 power 均須候選前通過 |
| 把常數 conformal factor 稱為 order+number 不可觀測 | 撤回；改要求宣告 continuum sequence 與 dimensional covariance |
| 強迫 C6/C7/C8 使用字面相同 selector | 改為共用 typed architecture，但允許事前固定的 gate-specific selector instances |
| E3 planted controls 被誤讀為 order-only $K$ 的存在性證據 | 明定 planted objects 可用 L4 oracle；E3 PASS 對 Stage 5C-1 construction feasibility 零蘊涵 |
| E2 等效性沿用 detection-power 宣稱 | E5 拆成 detection 與 equivalence；後者須由 margin、adjusted $\alpha$ 與 null variance／最壞分布反推自己的 cohort floor |
| 6a-S／6a-E 的批次、序列與 spending 邊界不清 | S 限於同 target、contrast-free batch prefilter；E 才能讀 contrast，依原始 family 順序接受 FPTP、fresh confirmation 與 family-wise spending |
| concentration 依 candidate 決定 continuum endpoint 型別 | 改以完整 candidate-independent law $\Pi_{\theta,g}$ 定義 mean-of-invariant；只有 theorem 條件成立時才允許 invariant-of-mean 作等價簡化，6b 不得換 target |
| 把一般被動 $GL(2)$ 換基與 fixed-slot gauge group 混同 | §1.4 改以 sector-line stabilizer 與 declared structures 之交定義 $G$；full passive covariance 必須同步搬動 projectors／pairing／reality tensors |
| 非緊 monomial fork 被當成只稍弱的合法選項 | §1.4 交付物以 nilpotent orbit closure 證明完整 domain 不存在 continuous positive invariant norm，與 C3b gate 有條件衝突 |
| $\Delta$ 被誤列為 C3b non-degeneracy 必要條件 | 改為 $\Delta\ne0$ 只是非純量的充分 witness；$\Delta=0$ 不得單獨判 FAIL |
| ideal planted representatives 被誤當成全 domain 可分離 | monomial 全純族不能分離 blind／chiral 代表與其單側 triangular degeneration；E3 必須驗完整 admissible domain |
