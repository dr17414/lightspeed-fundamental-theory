# Stage 5C D.1 第 3 項 — Primary Invariant Endpoint $\mathfrak I_G$

狀態：**【已確認之 candidate-independent 代數交付物／尚未 freeze】**。

範圍：只固定 smeared $2\times2$ matrix 的 primary invariant endpoint；不設計候選 $K$，
不設定 selector、smearing、normalization、統計門檻或 holdout。

前置：fork B（$G=T^2\rtimes S_2$）、ambient Frobenius norm、完整 invariant algebra 與
C3b blind-variety distance form均已交付。

---

## 0. 定位與本輪更正

$\mathfrak I_G$ 是 D.1 第 3 項的重要前置，**不是最後一塊**。原草案另有兩個承重錯誤：

1. 「chiral 與 blind-Jordan 兩支共享極限，所以任意連續純量必在兩支碰撞」不成立。
   反例 $\phi=Q/N^2-S/N^2$ 在 chiral 支為正、Jordan 支為負，只在共同極限為零。
   原測試只試四組正權重，無法支持 universal claim。
2. 三個座標各自不能從**那個三向量**刪除，只證明 coordinate-deletion minimality；不證明
   不存在另一個二向量。下文給出顯式二向量，因此原「三分量極小」結論作廢。

---

## 1. 判決：最小維度為二

令

$$
M=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
Q=|a-d|^2,\quad S=|b|^2+|c|^2,\quad |W|=|bc|,
$$

$$N^2=\operatorname{tr}(MM^\dagger)>0.$$

primary endpoint 固定為

$$
\boxed{\quad
\mathfrak I_G(M)=
\left(\frac{Q-2|W|}{N^2},\ \frac{S}{N^2}\right).
\quad}
$$

兩分量依序稱 `split_minus_coupling` 與 `off_diagonal_power`。$|W|$ 使用唯一的非負
平方根 $\sqrt{W\bar W}$；它在 $W=0$ 連續但不必可微，本 contract 不要求可微性。

### 1.1 單一連續純量確實不夠，但正確理由是三叉結構

> **命題 PI-1.** 若連續實值 invariant $\phi$ 要把 sector-blind 點與至少三個已登記、
> 參數域連通且以該點為共同極限的非平凡 planted branches 全部互相分離，則不可能。

*證明.* 固定 $f\ne0$，取三支

$$
\operatorname{diag}(f,f+q),\qquad fI+\lambda E_{12},\qquad
\begin{pmatrix}f&g\\g&f\end{pmatrix},\qquad q,\lambda,g>0.
$$

令共同極限 $fI$ 的純量值為 $c$。每支的連續像是連通區間，且 $c$ 在其閉包。若某支在
非零參數已取 $c$，立即與 blind 類碰撞；否則整支像必落在
$\mathbb R\setminus\{c\}$ 的左或右其中一個連通分支。三支而只有兩側，鴿籠原理使兩支
落在同側；兩個連通像都含任意靠近 $c$ 的同側區間，故值域重疊。$\square$

此證明需要三支，不能收窄成原草案錯誤的「任意指定兩支必碰撞」。它是解析拓撲命題，
有限抽樣不能證明；測試只鎖住共同極限等前提與已知反例。

### 1.2 二分量已足夠

對五個目前登記的**代數** planted classes，非零參數下的符號樣式為：

| class | 第一分量 | 第二分量 | 樣式 |
| :--- | ---: | ---: | :---: |
| sector-blind $fI$ | $0$ | $0$ | `00` |
| chiral diagonal，$m_U\ne m_V$ | $+$ | $0$ | `+0` |
| symmetric diffusion，$g\ne0$ | $-$ | $+$ | `-+` |
| blind Jordan，$\lambda\ne0$ | $0$ | $+$ | `0+` |
| chiral triangular，$m_U\ne m_V,\lambda\ne0$ | $+$ | $+$ | `++` |

symmetric diffusion 時 $Q=0$、$S=2|g|^2$、$|W|=|g|^2$，故第一分量等於第二分量的
負值。Jordan 與 triangular 的 $W=0$。因此五個樣式互異，二分量構造性地足夠。
結合命題 PI-1，對這組連續 planted-family separation requirement，最小維度恰為二。

「去掉第一分量則 blind 與 chiral 碰撞；去掉第二分量則 blind 與 Jordan 碰撞」只用來
鎖住所選 coordinate pair；全域二維下界由命題 PI-1 承擔。

---

## 2. $G$-不變性、實性與尺度

fork B 下 $Q,S,W\bar W$ 與 $N^2$ 都是 $G=T^2\rtimes S_2$ invariants。
$|W|=\sqrt{W\bar W}$ 取非負根，亦為 real continuous invariant。故兩分量對全部
$B\in G$ 滿足

$$\mathfrak I_G(BMB^\dagger)=\mathfrak I_G(M).$$

$Q,S,|W|,N^2$ 在 $M\mapsto tM$ 下全部為二次齊次，所以兩分量統一除以 $N^2$ 後
尺度不變。這也修掉原三向量必須混用 $N^2/N^4$ 的不必要型別複雜度；不是把四次量
$|W|^2$ 錯除以 $N^2$，而是選擇同樣可用、二次的 $|W|$。

---

## 3. Sharp bounds 與零點

$$
-1\le\frac{Q-2|W|}{N^2}\le2,qquad
0\le\frac{S}{N^2}\le1.
$$

下界由 $2|bc|\le |b|^2+|c|^2=S\le N^2$；上界由
$Q\le2(|a|^2+|d|^2)\le2N^2$。三個端點都有精確見證：

- $\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)$ 給 $(-1,1)$；
- $\operatorname{diag}(1,-1)$ 給 $(2,0)$；
- $E_{12}$ 給 $(0,1)$。

$M=0$ 時為 $0/0$，primary endpoint 不報值，依 endpoint nontriviality gate 記
**INCONCLUSIVE**。這不改變 C3b 對 exact-zero kernel 因 $0\in\mathcal B_1$ 而判 FAIL；
兩者是不同 gate，不得互相援引。非零但低於事前 norm floor 的輸入同樣不報值。

---

## 4. 與完整 invariant algebra 的關係

本端點是完整 real invariant algebra 的一個刻意選定子映射，不主張生成完整 invariant ring
或分離全部 $G$-orbits。它含 $S$ 與 $\sqrt{W\bar W}$，不是 holomorphic-only。

holomorphic family $\{a+d,ad,bc\}$ 對兩組退化對仍完全相同：

- $fI$ 與 $fI+\lambda E_{12}$；
- $\operatorname{diag}(m_U,m_V)$ 與其上三角退化。

本端點以第二分量 $S/N^2$ 分開兩組，符合 invariant-algebra 文件 IA-5／IA-6 的硬性限制。
非線性仍意味一般
$\mathbb E[\mathfrak I_G(M_C)]\ne\mathfrak I_G(\mathbb E[M_C])$；兩邊不得靜默替換。

---

## 5. 推論上限與仍未完成項

- 五類分離只對上表已登記的代數 planted families；不主張全軌道分離。
- **wrong-direction control 仍未完成。** 它需要 orientation／continuum mapping；本文件的
  五類代數分離不能冒充 observable contract E3 已完整交付。
- planted objects 是 evaluator-side L4 controls；其可分不蘊涵合規 order-only $K$ 存在。
- 任一 scalar aggregation 只可在 Freeze-1a 事前固定後作報告 effect size；不得替代
  二維 law／逐分量 planted separation，也不得從候選結果選方向或權重。
- selector $\Sigma$、smearing $\varphi$、normalization $\mathcal N$、continuum law 接合、
  planted family 完整化、數值門檻、power 與 fresh confirmation 均未完成。

因此 D.1 第 3 項與 Freeze-1a 仍為 **PENDING**。

---

## 6. Provenance 與回歸邊界

選定只使用已交付的 fork-B invariant algebra、事前登記的 algebraic planted classes 與上述
解析證明；未讀任何候選 spectrum／輸出、C8 表現、probe feature weights 或 holdout。

`tests/test_stage5c_primary_invariant.py` 直接呼叫
`analysis/stage5c_primary_invariant.py`，鎖住群不變性、尺度、sharp bounds、輸入型別、
五類符號樣式、coordinate-deletion witnesses、holomorphic falsifiers 與原兩支 P1 的反例。
命題 PI-1 的 universal lower bound 由解析證明承擔；測試不冒充 completeness proof。
