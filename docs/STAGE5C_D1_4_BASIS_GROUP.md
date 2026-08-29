# Stage 5C §1.4 — 可容許基底群 $G$ 與 invariant-family 分析

狀態：**【交付物草案／v0.3；fork B 已定案，尚未 freeze】** — basis-group 子決策已完成；primary invariant family 仍待固定。

範圍：observable contract v0.3 §1.4 的 candidate-independent 交付物。
驗證於 main `8ae8e7d`：52 檔、integrity 通過、130 passed。（歷史快照。）

---

## 0. 本文件不建立的事

- **不選定 primary endpoint $\mathfrak I_G$。** 只交付可容許 invariant family 與其限制。
- **不由想要的 invariant 反推 $G$。** §1 的推導方向嚴格是
  Stage 5A 結構 $\to$ $G$；任何「因為想用 $\operatorname{tr}/\det$ 所以取 $G=GL(2)$」的論證
  在本文件中判為無效。
- **不設計候選 $K$。**
- **E3 planted controls 不得用於證明 $G$、合格 $\Sigma$ 或 order-only $K$ 存在**（見 §8）。
- **不把 basis-group 決議誤寫成整份 D.1 第 3 項完成。** §7 只定案 $G$ 與 pairing 的
  provenance；primary endpoint $\mathfrak I_G$、smearing／normalization 與統計門檻仍未 freeze。

---

## 1. 由 Stage 5A 推導 $G$ 的上下界

### 1.1 Stage 5A 實際導出什麼

Stage 5A 導出的是：causal order $(\mathcal C,\prec)$ 決定一個**高度 canonical 的無序對**
$\{U,V\}/S_2$（$P(\kappa=1)=0.765,0.907,0.963,1.000,0.975$，$N=20\dots400$）。

三點必須精確：

1. 導出的是**兩個 total order**，不是兩個向量。線性化後得到的是 $W\cong\mathbb C^2$ 中
   **兩條直線**（sector lines），不是兩個有範數的基向量。
2. 導出的是**無序**對。從未導出有序對。
3. **未**導出任何 pairing、reality structure 或範數。$\mathcal I_0$ 的
   "complex amplitudes/phases" 給出係數體，不給出 fiber 上的內積。

### 1.2 先區分兩種「換基」〔避免 category error〕

令 $W=L_U\oplus L_V$，並以 $P_U,P_V$ 表示兩條 sector lines 的 projectors。

1. **一般被動座標變換**可取任意 $B\in GL(W)$，但必須同時搬動
   $M,P_U,P_V$ 及 pairing／reality tensors。這不會把 sector decomposition 變成 pure gauge；
   它只是把同一組幾何資料改寫到另一組座標。
2. 本文件要分類的是 **fixed-slot stabilizer**：在 $P_U,P_V$ 所代表的無序分解保持固定時，
   只對 $M$ 作共軛的 representation redundancies。只有這個群的 invariants 才能作
   §2 的 $M$-only endpoint。

因此 observable contract §1.4 的群必須補精確為

$$
G=\operatorname{Stab}_{GL(W)}(\{L_U,L_V\})
  \cap\operatorname{Aut}(\text{pairing},\text{reality},\text{basis conventions}).
$$

若日後要用 full passive $GL(W)$ covariance，endpoint 必須把 $P_U,P_V$ 等結構張量一起
納入 typed functional；不得仍只對裸矩陣 $M$ 取 invariant。這是另一份 contract，不是
本文件中的 $G$。

### 1.3 上下界：$S_2\subseteq G\subseteq N$

令

$$
N=\operatorname{Stab}_{GL(W)}(\{L_U,L_V\})
=\{B:B\text{ 每列每行恰一個非零元}\}
=(\mathbb C^\times)^2\rtimes S_2.
$$

因為 Stage 5A 導出的是無序對，acceptance spec C3 要求 sector swap $\sigma_x\in G$；
這也反過來要求所有 pairing／reality／basis declarations 必須與 swap 相容，不相容的宣告
不是較小 fork，而是 **PROTOCOL-INVALID**。另一方面，任何在 fixed-slot 意義下保持
$\{L_U,L_V\}$ 的變換必屬 $N$。故

$$\boxed{\,S_2\ \subseteq\ G\ \subseteq\ N=(\mathbb C^\times)^2\rtimes S_2\,}.$$

> **命題 1（作用域限定）.** $U(2),SU(2),GL(2,\mathbb C)$ 等含真正 sector-mixing
> 元素的群，不能作為只讓 $M\mapsto BMB^{-1}$、而把 sector projectors 固定的 $M$-only
> gauge group。它們仍可作一般被動座標變換，前提是 $P_U,P_V$ 與其他 tensors 一起變換。

因此「full similarity 所以 $\operatorname{tr},\det$ 生成全部 endpoint invariants」不能
套用到目前的 $M$-only contract；不是因為一般 $GL(2)$ 座標變換被物理禁止，而是因為
目前被固定的 sector structure 使相關 stabilizer 嚴格較小。

### 1.4 有效作用與殘餘自由度

sector lines 是導出資料；每條 line 上的 basis normalization／phase 是否固定，則由
object／basis contract 宣告並進 C0 ledger。不能從「沒有導出基向量」自動推出所有
$\mathbb C^\times$ rescaling 都必須視為 gauge，也不能從 free vector space 的 canonical
slot basis 自動推出它們全都物理可觀測。

另有一個必須商掉的 kernel：中心純量 $Z=\{\lambda\mathbb 1\}$ 在 similarity action 下
對所有 $M$ 作用平凡。因此 invariant 與 orbit 問題真正只看
$\bar G=G/(G\cap Z)$。例如 $S_2$ 與 $Z\cdot S_2$ 對 $M$ 的有效作用相同；
$T^2\rtimes S_2$ 的有效連續部分是 $U(1)$，$N$ 的有效連續部分是 $\mathbb C^\times$。

只靠上述群論區間不能唯一固定 subgroup；§7 另以 C3b 的正定 invariant-norm gate 與
C0 的最小 primitive／完整 stabilizer 紀律完成選擇。這兩項前提均具名，不冒充純群論定理。

---

## 2. 現行 contract 採 global-only：沒有 connection primitive

Stage 5C-1 的 fiber 是平凡 product fiber $F_x=\{(x,U),(x,V)\}$——每個事件上是**同一個**
兩元素集合。它給出 canonical global trivialization，因此本專案目前選擇以 **global**
basis action 作驗收群。

$\mathcal I_0$ 中**沒有 connection primitive**：沒有 parallel transport、沒有 local frame
bundle、沒有 Clifford 表示。因此：

> 在現行 Stage 5C-1 contract 中，只允許 $B_x=B_y=B$ 的 global action。若要把 local
> frame changes 升格為驗收 symmetry，必須先交付 transport／composition 與 endpoint
> contraction contract；否則以 local covariance 為 scalarity 依據判 PROTOCOL-INVALID。

數學上，平凡 bundle 當然可以寫出 local frame change
$G_R(x,y)\mapsto B_xG_R(x,y)B_y^{-1}$；缺少的不是這個公式，而是讓不同 fibers 的 indices
可被比較、收縮並形成 $M$-only scalar 的既定結構。故本節是**專案 contract 的限制**，
不是「平凡 bundle 無法做 local change of frame」的 no-go theorem。

**這不是 local spin-frame 結構的推導。** 平凡 product fiber 支持 global action，正是因為
它平凡；這恰好對應 contract §1.1 中「$F_x$ 幾乎不帶物理資訊」的聲明，也正是 C11 firewall
所指的 1+1D-only 之處。3+1D 的 local Lorentz/Clifford 結構**不能**由此得到。

---

## 3. 變換律

### 3.1 Global（現行 contract 唯一驗收者）

$$\mathcal K(x,y)\mapsto B\,\mathcal K(x,y)\,B^{-1},\qquad
G_R(x,y)\mapsto B\,G_R(x,y)\,B^{-1},\qquad
M_C\mapsto B\,M_C\,B^{-1},$$

$M_C$ 為 contract §2.3 的 smeared matrix（linear smearing 與共軛可交換，故
smearing 前後變換律一致）。

寫 $M=\begin{pmatrix}a&b\\c&d\end{pmatrix}$：

- $B=\sigma_x$：$(a\,d)(b\,c)$ 對換，即 $M\mapsto\begin{pmatrix}d&c\\b&a\end{pmatrix}$；
- $B=\mathrm{diag}(\alpha,\beta)$：$a,d$ 不變，$b\mapsto(\alpha/\beta)b$，
  $c\mapsto(\beta/\alpha)c$。

### 3.2 Conjugate pairing 的情形

若 dossier 宣告第二個 index 為 conjugate，作用改為 $M\mapsto BMB^\dagger$。此時
§4 的全部結果**必須重算**，不得沿用。特別是 $\det M\mapsto|\det B|^2\det M$，僅在
$|\det B|=1$ 時不變。

### 3.3 Local（僅供 falsification，非可容許）

若強行採 $M\mapsto B_xMB_y^{-1}$ 且 $B_x=\mathrm{diag}(\alpha_x,\beta_x)$、
$B_y=\mathrm{diag}(\alpha_y,\beta_y)$，符號計算給出

$$ad\ \mapsto\ w\,ad,\qquad bc\ \mapsto\ w\,bc,\qquad w=\frac{\alpha_x\beta_x}{\alpha_y\beta_y}.$$

因此：

- $ad/bc$ 在 $bc\ne0$ 的 open set 上**不變**（torus 部分）；它是 rational invariant，
  不是全域定義的 polynomial endpoint；
- $\det M=ad-bc$ 是**相對不變量**，權重 $w$，不是純量；
- $\operatorname{tr}M=a+d$ **連相對不變量都不是**（$a,d$ 的權重分別為
  $\alpha_x/\alpha_y$ 與 $\beta_x/\beta_y$，一般不同）。

若兩端的 swap 亦獨立，$ad/bc\mapsto bc/ad$，故只有無序對 $\{ad/bc,\ bc/ad\}$
或其對稱函數才不變。

---

## 4. Invariant algebra

以下區分**全純不變量**（僅用 $M$ 的元素）與**實不變量**（涉及 $M^\dagger$）。
除 §4.4 明示的 unitary identity $B^{-1}=B^\dagger$ 外，本節採 mixed-index similarity
$M\mapsto BMB^{-1}$；若選 §3.2 的 genuinely conjugate-index action，以下 fork 表不得沿用，
必須另行重算。

### 4.1 $G=S_2=\{1,\sigma_x\}$（最小群）

作用是 $\mathbb Z_2$ 以 $(a\,d)(b\,c)$ 置換 $\mathbb C^4$。全純不變環由

$$a+d,\quad ad,\quad b+c,\quad bc,\quad (a-d)(b-c)$$

生成（五個生成元，帶一條關係；非多項式環）。

若記 $s_a=a+d,p_a=ad,s_b=b+c,p_b=bc,q=(a-d)(b-c)$，關係為

$$q^2=(s_a^2-4p_a)(s_b^2-4p_b).$$

> **命題 2（分離性）.** 上述五元組分離 $S_2$ 軌道。
> *證明.* $\{a+d,ad\}$ 決定重集 $\{a,d\}$；$\{b+c,bc\}$ 決定重集 $\{b,c\}$；四種配對中
> $(a-d)(b-c)$ 的值恰選出 $\{M,\sigma_xM\sigma_x\}$ 這一條軌道。$\square$

隨機連續樣本幾乎不會產生相同 invariant tuple，故「隨機碰撞為零」不是有效的
分離性證據。回歸測試改用小整數矩陣的**有限窮舉碰撞檢查**與退化重根 cases；承重者仍是
上面的解析證明。

**$\operatorname{tr},\det$ 在此不完備**：$0$ 與 $\begin{pmatrix}0&1\\0&0\end{pmatrix}$
的 $\operatorname{tr}$ 與 $\det$ 皆為 $0$，但 $b+c$ 分別為 $0$ 與 $1$。

### 4.2 $G=N$（monomial，含 torus），全純不變量

compact fork B 的 $T^2$ 在 $(\mathbb C^\times)^2$ 中 Zariski dense，故 B 與 noncompact
fork C 的**全純 polynomial** invariant ring 相同；差異只會在涉及 complex conjugation
的 real invariants 與 orbit topology 出現。

> **命題 3.** torus $\mathrm{diag}(\alpha,\beta)$ 的全純不變環為
> $\mathbb C[a,d,bc]$；再取 $S_2$ 不變得
> $$\mathbb C[a+d,\ ad,\ bc].$$
> *證明.* 單項式 $a^{p}d^{q}b^{r}c^{s}$ 的權重為 $(\alpha/\beta)^{r-s}$，不變 $\iff r=s$，
> 故 torus 不變單項式由 $a,d,bc$ 生成。$S_2$ 交換 $a\leftrightarrow d$ 且固定 $bc$，
> 取對稱化得 $a+d,ad,bc$。$\square$

由 $\det=ad-bc$ 得 $\mathbb C[a+d,ad,bc]=\mathbb C[\operatorname{tr},\det,bc]$。

> **推論.** 即使對 monomial 群，$\operatorname{tr}$ 與 $\det$ **仍不生成**全部全純不變量；
> 必須補上 $bc$（等價地 $ad$）。
> 見證：$M_1=\begin{pmatrix}1&0\\0&2\end{pmatrix}$ 與
> $M_2=\begin{pmatrix}0&1\\-2&3\end{pmatrix}$ 同有 $\operatorname{tr}=3,\det=2$，但
> $bc=0$ 與 $bc=-2$，屬不同 monomial 軌道。（兩者在 $GL(2)$ 下同軌道——正說明
> fixed-slot stabilizer 小於 $GL(2)$ 後，不變量嚴格變多。）

**Massless diagonal special case.** $b=c=0$ 時 $bc=0$，環退化為
$\mathbb C[\operatorname{tr},\det]$，即 $\{m_U,m_V\}$ 的初等對稱函數。**這只是特例**，
不得外推到含 off-diagonal 的情形（C10 mixing 後尤其不成立）。

### 4.3 軌道閉包障礙（全純不變量的根本限制）

torus 在 $(b,c)$ 上的軌道：$bc=k\ne0$ 時為閉的雙曲線；$b\ne0,c=0$ 時軌道
$\{(\lambda b,0)\}$ **不閉**，其閉包含 $(0,0)$。

> **命題 4.** 全純不變量只分離閉軌道。$0$ 與 nilpotent 有相同的
> $(\operatorname{tr},\det,bc)=(0,0,0)$，但屬不同軌道，故**任何**全純不變量都無法分離。

### 4.4 實不變量（涉及 $M^\dagger$）

若 $G$ 為**緊**群（相位型 torus $T^2\rtimes S_2$，此時 $B^{-1}=B^\dagger$），
$M\mapsto BMB^\dagger$ 且 $M^\dagger\mapsto BM^\dagger B^\dagger$，可用實不變量如

$$|a|^2+|d|^2,\quad |a|^2|d|^2,\quad |b|^2+|c|^2,\quad |b|^2|c|^2,\quad \operatorname{tr}(MM^\dagger).$$

$|b|^2+|c|^2$ 對 $0$ 與 nilpotent 分別為 $0$ 與 $1$，**分離 §4.3 的反例**。
上列只是 witnesses，**不是**完整生成族的宣稱。

> **命題 5.** 緊線性群的軌道皆閉，且存在分離其軌道的 real polynomial invariant family；
> 非緊群
> $(\mathbb C^\times)^2\rtimes S_2$ 的軌道未必閉，**任何連續不變量都無法分離**
> 非閉軌道與其閉包中的退化點。

> **推論（continuous invariant norm no-go）.** 令
> $J=\left(\begin{smallmatrix}0&1\\0&0\end{smallmatrix}\right)$，
> $D_t=\operatorname{diag}(t,1)$。則 $D_tJD_t^{-1}=tJ\to0$。
> 若 $\|\cdot\|_G$ 是全 $M_2(\mathbb C)$ 上連續、正定且 $N$-不變的 norm，便有
> $\|J\|_G=\|tJ\|_G\to\|0\|_G=0$，矛盾。因此 full noncompact fork C
> **不存在**這種 invariant norm。

以上例子可推廣到任何有效對角子群 $H\le\mathbb C^\times$ 的非緊情形：模長映射
$|\cdot|:H\to\mathbb R_{>0}$ 無界；利用群的取逆封閉性，可取 $r_n\in H$ 使
$|r_n|\to0$，故 $r_nJ\to0$。因此只要完整矩陣 domain 含 $J$，任何非緊 $H$ 都沒有
全域連續正定 invariant norm。這個結論**不需要**先窮盡 $\mathbb C^\times$ 的全部閉子群。

特別注意，清單
$\{1,\mu_n,U(1),\mathbb R_{>0}\!\cdot\!\mu_n,\mathbb C^\times\}$
並不窮盡 topologically closed subgroups；例如
$\langle 2e^{i\vartheta}\rangle=\{2^ke^{ik\vartheta}:k\in\mathbb Z\}$
在 $\mathbb C^\times$ 中閉，卻一般不在該清單。若改稱 complex algebraic subgroup，
$U(1)$ 與 $\mathbb R_{>0}$ 本身又不屬該分類。因此 §7 使用上面的通用 compactness 論證，
不以錯誤的閉子群清單承重。

這使 fork C 不只是「分離力較弱」：若 C3b 的 invariant-norm family 指的是上述連續正定
scalar norm，且 object domain 含 nilpotent direction，fork C 與既有 gate **不相容**。
若要保留 C，只能在 Freeze-1a 事前限制 domain，或把 norm 改成 relative／projective
quantity 並重寫 gate；兩者都不得在候選出現後才做。

---

## 5. Planted classes 的可分離性

以 smeared matrix $M$ 表示（**不是** kernel 設計，只是 evaluator 端的分類）：

| planted class | 形式 | fork A：$S_2$ 全純族 | fork B/C：monomial 全純族 | compact A/B：完整 real family |
| :--- | :--- | :--- | :--- | :--- |
| sector-blind | $M=f\,\mathbb 1$ | 可分離 | **不可與** $f\mathbb 1+\lambda E_{12}$ **分離** | 可分離 |
| chiral（解耦、不等） | $M=\mathrm{diag}(m_U,m_V)$，$m_U\ne m_V$ | 可分離 | **不可與** $M+\lambda E_{12}$ **分離** | 可分離 |
| symmetric diffusion | $M=\begin{pmatrix}f&g\\g&f\end{pmatrix}$，$g\ne0$ | 可分離 | 其 $bc=g^2\ne0$ 軌道為閉，可與其他閉軌道分離 | 可分離 |
| wrong-direction | 由方向約定決定 | 需 §7 定案後才可判定 | 同左 | 同左 |
| nilpotent 型退化 | $\begin{pmatrix}0&\lambda\\0&0\end{pmatrix}$ | 可分離 | **不可與零矩陣分離**（命題 4） | 可分離 |

其中 $\Delta=(\operatorname{tr}M)^2-4\det M$ 為判別式，$S_2$-不變且屬 §4.2 的族。
原表把「可辨識 planted class 的理想代表」誤寫成「能把該軌道與全部 admissible matrices
分離」；命題 4 正好否定後者。E3 若要以全 object domain 承重，必須按修正版表格驗收，
不能只在四個理想 representatives 間做分類。

**兩點限制**：

1. $\Delta$ 分離 sector-blind 與 chiral 這件事，只在**已知 $M$ 可對角化**時可讀成
   $(m_U-m_V)^2$；一般 $\Delta=0$ 僅表示重根，**不蘊涵** $M=f\mathbb 1$（nilpotent 即反例）。
   邏輯方向必須寫清楚：$M=f\mathbb 1\Rightarrow\Delta=0$，所以
   $\Delta\ne0$ 是「非純量」的**充分 witness**；但它不是 sector non-degeneracy 的必要條件，
   而 $\Delta=0$ 也不得單獨判 C3b FAIL。
2. wrong-direction class 的可分離性依賴方向／orientation、chiral identification、adjoint／
   reality 與 continuum-target mapping；在這些宣告及 fork 未定前無法判定。

---

## 6. 為何 $\operatorname{tr}/\det$ 的直覺會失效——三層各自獨立的理由

供未來讀者避免重犯：

1. **fixed-slot stabilizer 較小**：$G\subseteq N\subsetneq GL(2)$，故裸 $M$ 的不變量比
   full-similarity invariants 多（§4.2 推論）。
2. **軌道不閉**：全純不變量原則上無法分離非閉軌道（命題 4）。
3. **型別**：若採 local action，$\operatorname{tr}$ 連相對不變量都不是（§3.3）。

三者互相獨立；修掉任何一個都不能救回原推論。

---

## 7. 判決：fork B（兩項具名前提下唯一）

對目前 fixed-slot、$M$-only contract，已確定
$S_2\subseteq G\subseteq N$；一般 sector-mixing matrix 只能作同時搬動 projectors 的被動
座標變換，不能偷換成裸 $M$ 的 gauge action。歷史上需比較的代表性 fork 如下；表格不宣稱
窮盡全部 abstract subgroups：

| fork | $G$ | 何時成立 | 全純不變量 | 分離能力 |
| :--- | :--- | :--- | :--- | :--- |
| **A** | 有效作用 $S_2$ | basis contract 固定 relative normalization／phase；可以是宣告 convention，不冒充 derived physics | $\mathbb C[a{+}d,ad,b{+}c,bc,(a{-}d)(b{-}c)]$ | 分離全部 $S_2$ 軌道（命題 2） |
| **B** | $T^2\rtimes S_2$（緊；有效連續部 $U(1)$） | 宣告 swap-compatible positive Hermitian structure，固定模、保留 relative phase | $\mathbb C[\operatorname{tr},\det,bc]$ | 全純僅分離閉軌道；存在分離全部軌道的 real polynomial family（命題 5） |
| **C** | $(\mathbb C^\times)^2\rtimes S_2$（非緊；有效連續部 $\mathbb C^\times$） | 不固定 relative norm | 同 B | 非閉軌道不可由 continuous invariants 分離；全域 continuous positive invariant norm 不存在 |
| **D** | 其他 $S_2\subseteq G\subseteq N$ | 額外 swap-compatible pairing／reality／basis declarations | 必須重算 | 必須重證 |

### 7.1 前提 P1：C3b 的 norm 是連續正定 invariant norm

Acceptance spec C3b 已要求預先登記 basis-covariant invariant-norm family 與 effect size。
本決議把「norm」照字面固定為完整 object domain 上的**連續、正定** scalar norm；若改成
seminorm、relative／projective quantity，或事後刪掉 nilpotent directions，均屬 protocol
amendment，不能沿用本判決。

由 §4.4 的一般 orbit-closure 論證，有效對角子群 $H\le\mathbb C^\times$ 必須緊。
任何 $\mathbb C^\times$ 的緊子群都包含於 $U(1)$；$U(1)$ 的閉子群只有有限循環群
$\mu_n$ 與 $U(1)$ 本身。故 P1 把可行有效作用縮到

$$H\in\{1,\mu_n,U(1)\}.$$

### 7.2 前提 P2：只宣告 norm 所需的最小 L2 結構，並取其完整 stabilizer

Stage 5A 給的是兩條無序 complex sector lines，沒有 preferred relative phase。為實作 P1，
本決議宣告一個與 swap 相容的正定 Hermitian pairing $h$，但**不**另宣告 relative-phase
標記；$G$ 定義為這些已宣告結構的完整 automorphism group，不可任意再挑一個較小 subgroup。
這是 C0 最小 primitive／capacity ledger 在本子問題的具體含義，不是群論定理。

在 sector slot representatives 中，一般 swap-compatible positive Hermitian form 為

$$h=\begin{pmatrix}p&q\\q&p\end{pmatrix},\qquad p>|q|,\quad p,q\in\mathbb R.$$

若 $q\ne0$，$h$ 會固定兩條 sector lines 的相對 phase：對
$D=\operatorname{diag}(e^{i\phi},e^{i\psi})$，條件 $D^\dagger hD=h$ 迫使
$e^{i(\psi-\phi)}=1$。這正是 Stage 5A 未給出的額外 basis-phase primitive。
P2 因而排除 $q\ne0$，留下

$$\boxed{h=p\,\mathbb 1,\qquad p>0.}$$

反之，$h=p\mathbb 1$ 的完整 fixed-line isometry group 恰為
$T^2\rtimes S_2$；商掉作用平凡的共同相位中心後，

$$\boxed{G=T^2\rtimes S_2,\qquad G_{\mathrm{eff}}=U(1)\rtimes S_2.}$$

因此 $\mu_n$ 或有效 $S_2$ 不是「較少 primitive」：要把完整 $U(1)$ stabilizer 人為縮小，
必須再宣告離散或完整的 relative-phase convention。A 比 B 多固定 relative phase；以
「B 的 pairing 是額外結構」為理由改選 A 並不融貫，因 A 含有 B 所需的 norm scaffold，
還另加 phase structure。

### 7.3 Ledger 分級與決議範圍

Claude review 正確排除了 L4，但把 $h$ 改列 L3 仍與 frozen acceptance spec 衝突：spec §4.1
明列 **pairing／adjoint／basis-phase convention 為 L2 quantum scaffolding**。故本決議登記：

- $h/\mathbb R_{>0}$（兩條 sector lines 正交、等長）是 **declared L2**，不是 poset-derived；
- 整體正尺度 $p$ 不作獨立物理參數，吸收到 §4 的 normalization $\mathcal N$；若保留其數值，
  該數值才按 **L3 normalization** 計入；
- 這些結構不是 evaluator-only oracle，亦不得誤列 L4。

在 P1、P2——均為現行 acceptance discipline 的具名實例——下，**fork B 定案**。
這只完成 basis-group／pairing 子決策；$\mathfrak I_G$ 的完整 real invariant family、primary
endpoint、wrong-direction E3、smearing／normalization 與統計門檻仍待固定，D.1 第 3 項及
Freeze-1a 仍為 **PENDING**。本節沒有設計候選 $K$。

---

## 8. 推論上限

- 本文件**不**證明合格 $\Sigma$ 存在，也不證明 order-only $K$ 存在。
- §5 的 planted classes 只是 evaluator 端的**分類與可分離性分析**；E3 controls
  得使用 L4 oracle，**其通過不蘊涵任何關於合規 $K$ 存在性的結論**。
- 命題 1 只限制 fixed-slot、$M$-only gauge group；它不禁止同時搬動 sector projectors 的
  一般被動 $GL(W)$ 座標變換。若未來撤回 Stage 5A sector decomposition，stabilizer contract
  本身也須重寫。
- fork B 的唯一性是相對於 §7 的 P1/P2；若正式修改 C3b 的 norm 型別，或新增有 provenance
  的 relative-phase primitive，必須重開此決議，不得稱為推翻純群論定理。
- 全部結論限於 **1+1D**（C11）。

---

## 附錄 — 回歸測試對應

`tests/test_stage5c_basis_group.py` 鎖住：命題 2 的 exact finite-grid 分離與生成元關係、
命題 3 的 compact／noncompact torus invariance 與 $\operatorname{tr}/\det$ 不完備、
命題 4 的 blind／chiral orbit-closure 反例、命題 5 的 compact witness 與 noncompact norm
no-go、§3.3 的 local 權重、similarity 中心 kernel、被動 $GL(2)$ 搬動 projectors 與
fixed-slot monomial stabilizer 的區分，以及 §5 判別式的正確邏輯方向。
v0.3 另鎖住：遺漏於簡化清單的 closed spiral subgroup 仍觸發非緊 orbit-closure no-go、
swap 加完整 relative-phase invariance 迫使 $h=p\mathbb 1$，以及該 $h$ 的完整 fixed-line
isometry group 為 $T^2\rtimes S_2$。
