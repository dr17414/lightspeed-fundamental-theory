# Stage 5C E3 — Wrong-Direction 類別邊界

狀態：**【candidate-independent active control／v0.2；REVIEW-PENDING】**。全域 sector swap
的 gauge/invariance 判決與 active wrong-support 的 typed support mapping、完整參數域及解析
Gate O/E 現由 `STAGE5C_6A_E_CERTIFICATION.md`／
`analysis/stage5c_planted_certification.py` 交付；獨立 review、CI 與 merge 前不得標為
`CLOSED`。本文件不設計候選 $K$，不接觸 holdout 或 arm ledger。

歷史基準：main `36605dc`（62 檔、integrity 通過、177 passed）。

---

## 0. 結論

1. $\sigma_x$ 共軛的全域 sector swap 屬 $G$-gauge，必須作 **invariance control**，不得作
   discrimination class。
2. 「不在同一 $G$-orbit」只是一道 **orbit-admissibility 必要條件**，不保證既定二維端點
   $\mathfrak I_G$ 能分離；原草案的 `iff` 撤回。
3. wrong direction 不是孤立矩陣 $M$ 的內在標籤，而是 typed smearing pipeline 上的
   **active support intervention**。$M$ 可以保留 intervention 的結果，但僅看 $M$ 無法重建其
   support provenance。
4. 真正的 E3 control 必須同時通過 orbit gate 與完整參數域上的 endpoint-law separation gate；
   具名 `sigma-c7-e3-null-support-map-v0.1` 現已在 candidate-independent continuum domain
   通過兩者，狀態維持 **REVIEW-PENDING** 至獨立複核與合併。
5. 本文件保留兩個矩陣作 algebraic stress witnesses；它們不是 wrong-direction controls，亦未被
   加入 planted family。

---

## 1. WD-1：全域 sector swap 是 gauge

設 reference chiral matrix

$$M=\operatorname{diag}(m_U,m_V).$$

則

$$\sigma_xM\sigma_x=\operatorname{diag}(m_V,m_U),\qquad \sigma_x\in G.$$

相位 torus 對對角元作用平凡，所以在 $m_U\ne m_V$ 時，完整軌道恰為

$$G\cdot M=\{\operatorname{diag}(m_U,m_V),\operatorname{diag}(m_V,m_U)\}.$$

因此任何合規 $G$-invariant endpoint 均須逐位元滿足

$$\mathfrak I_G(\sigma_xM\sigma_x)=\mathfrak I_G(M).$$

這不是 evaluator 缺陷。Stage 5A 只導出無序對 $\{U,V\}/S_2$；若端點能辨識單純的全域
swap，反而代表它讀入了未導出的 ordered assignment。

**登記用途。** 對每個已登記 planted class，$\sigma_x$ 共軛必須作 arm-N 型 invariance
control。若不相等，判 evaluator/C3 失效；不得把相等解讀為 wrong direction 已可辨識。

---

## 2. WD-2：兩道 gate，不是 orbit `iff`

相對於 correct reference family $\mathcal R$，一個 proposed control family $\mathcal X$ 要承擔
E3 discrimination，至少要依序通過：

### 2.1 Gate O — orbit admissibility

在全部凍結參數域上，$X\notin G\cdot R$。若 $X\in G\cdot R$，任何 $G$-invariant evaluator
都不能分離兩者，該比較只能作 invariance control。

### 2.2 Gate E — endpoint-law separation

即使 $X\notin G\cdot R$，選定的 primary endpoint 也未必是完整 orbit separator。必須在同一
selector、smearing、normalization、regulator 與統計 pipeline 下，證明 $\mathfrak I_G(X)$ 與
$\mathfrak I_G(R)$ 的**完整 endpoint laws** 落入事前登記的不相交 region，並達到 effect、power
與 multiplicity gates。代表點不同不足以通過；完整參數域中存在碰撞亦不足以通過。

故正確邏輯是

$$\text{E3-admissible}\Longrightarrow\text{Gate O PASS and Gate E PASS},$$

而不是 $X\notin G\cdot R\iff X$ 可作 discrimination class。

一個顯式反例是

$$T=\begin{pmatrix}1&0.9\\0&i\end{pmatrix},\qquad
  C=\begin{pmatrix}\sqrt2&0\\0.9&0\end{pmatrix}.$$

兩者對角重集不同，故不在同一 $G$-orbit；但 primary endpoint 完全相同：

$$\mathfrak I_G(T)=\mathfrak I_G(C)=(0.71174377,0.28825623).$$

這同時鎖住「orbit 外」不是「endpoint 可分」的充分條件。

---

## 3. WD-3：active support intervention 的型別

「沿錯誤 null 方向傳播」必須定義在 smearing 之前的 typed evaluator tuple 上，例如

$$\mathcal T=(\Sigma,\varphi,\mathcal D,\iota_{\rm sf},\text{continuum frame/mapping}).$$

需嚴格區分兩種操作：

- **Passive/global relabeling**：同時交換 fiber slots、sector labels 與相應 selector labels。
  這是 §1 的 gauge operation，結果必須 invariant。
- **Active wrong-support intervention**：固定已宣告的 continuum frame、test-function instance、
  normalization 與 covariant output legs，只交換哪一組 null-support pairs 餵入各 leg，或依正式
  contract 反轉其 support relation。

第二種操作可能改變 smeared matrix 或其分布；所以不能說方向在 smearing 後「完全不可見」。
正確說法是：**孤立的 $M$ 沒有足夠 provenance 可被命名為 correct/wrong direction**；方向判決
必須引用生成 $M$ 的 typed intervention。

### 3.1 定案後的判決順序

1. 在同一 frozen parameter domain 構造 correct 與 active-intervention objects。
2. 先驗 Gate O。若 active object 對全部允許參數皆落在 correct $G$-orbit，記
   `DIRECTION-GAUGE`；不得硬設 discrimination gate。
3. 若 Gate O 通過，再驗 Gate E。endpoint law 無法分離時，表示**這個 evaluator/control
   pairing 不足**；不得反推所有方向 evaluator 不可能。
4. 只有兩道 gate、null controls、power 與 fresh confirmation 均通過，wrong-direction E3
   control 才可由 PENDING 改為 DELIVERED。

$\Sigma$ 未必單獨承載 sector-labelled direction；因此原草案「只對調 $\Sigma$」的寫法撤回。
實際 intervention 必須在整個 $\mathcal T$ 型別定案後逐欄列明，且不得由候選結果反推。

### 3.2 與 C8 intrinsic selector 的隔離

`docs/STAGE5C_SELECTOR_FAMILY.md` 固定的是 sector-blind $\Sigma_{C8}$，只服務 C8
distributional test。active wrong-support 不要求它 sector-aware；E3 應另行登記 evaluator-side
$\Sigma_{C7/E3}$／test-function support mapping，並可依既定 L4 權限使用 continuum frame、
$\iota_{\rm sf}$ 與 planted object。這些 oracle 只可出考卷，對合規 order-only $K$ 的存在性
零蘊涵且不得回流 construction。

handoff §2.3 記錄的 $\Delta r_U,\Delta r_V$ 仍是未採納 candidate materials，不列入 C8
selector，也不因 E3 需要方向控制而獲得默示豁免。若未來另案把它們用作 order-only
sector-aware selector，須先走 protocol amendment，處理 $\kappa>1$ orbit、enumeration cap、
sector-swap covariance 與 capacity；本文件沒有作此授權。

---

## 4. 非採納的 algebraic stress witnesses

以下矩陣只用來測試 §2 的邏輯邊界：

| 名稱 | 形式 | 限制 |
| :--- | :--- | :--- |
| `sector_transposing` | $\begin{pmatrix}0&m_U\\m_V&0\end{pmatrix}$ | 是 mixing-like matrix，不是方向定義；不得偷渡進 C7 E3 |
| `co_propagating` | $\begin{pmatrix}m_U&0\\m_V&0\end{pmatrix}$ | 沒有 typed operator/Green-function provenance，不是 evaluator control |

它們不屬已登記 planted family。單一參數點的七類兩兩分離不承重，也不記為 E3 成果。
上節的 $T/C$ 碰撞則保留為 primary endpoint 非完整 orbit separator 的 executable falsifier。

若未來另案採納任何新 family，必須先凍結完整參數域並解析或以有 power 的程序證明全域
separation；不得只掃三個正實代表點。以 triangular 與 co-propagating 為例，

$$I_1(T)+I_2(T)=1-\frac{2\operatorname{Re}(m_U\bar m_V)}{N^2},
\qquad I_1(C)+I_2(C)=1.$$

正實非零參數只證此一對 family 在該域上分離，不證新 family 與所有其他 planted families
均分離。

### 4.1 已採納 control 與上述 witnesses 的隔離

已採納物件不是本節任何孤立 matrix proposal。它固定 flat unit diamond、canonical
$(U/R,V/L)$ output legs、normalization 1 與 test density
$r_{\lambda,s}=s e^{\lambda(u_x-u_y)}$，只把 correct retarded support 主動反轉；
$\lambda\in[2,5/2]$，scale 使用 items 3＋6 共用的 binary64-derived domain。

correct／wrong pairings 的封閉形式、完整域 Gate O 證明、endpoint-image Gate E 嚴格分離、
direct quadrature oracle 與 global-swap trace tests 全部以
`STAGE5C_6A_E_CERTIFICATION.md` 為 source-of-record。這是 typed pipeline intervention，
不會把「orbit 外」重新誤寫成任意 matrix 都可 discrimination。

---

## 5. 推論上限與未完成項

- WD-1 只證全域 swap 是 gauge；不證物理 wrong direction 已排除或已可辨識。
- Gate O PASS 只表示 gauge 沒有禁止辨識；不證 primary endpoint 足夠。
- Gate E 若失敗，只拒絕該已登記 evaluator/control pairing；無 completeness theorem 時不得升格
  為方向性 No-Go。
- planted objects 可使用 L4 oracle，所以其通過對 order-only 候選 $K$ 的存在性零蘊涵。
- primary 第一分量的符號仍只是代數記帳，不能用來定義 correct/wrong direction。

仍未完成：finite-causet joint matched law、E4 live numerical bounds、E3 simultaneous
statistical region／multiplicity／power、fresh manifests 與 runner。故 active control 本身為
`REVIEW-PENDING`，D.1 第 3 項及 Freeze-1a 仍 **PENDING**；這不是 scientific E3 PASS。

---

## 附錄 — 回歸範圍

`tests/test_stage5c_wrong_direction.py` 直接呼叫 primary endpoint 的 source-of-record，鎖住：
全域 swap invariance、對角 chiral orbit 的兩點形式、orbit gate 非充分的顯式碰撞、正實參數
公式，以及 matrix proposals 不得被誤報為已登記 planted family。
`tests/test_stage5c_numerical_certification.py` 另鎖住現已具名的 typed intervention、解析
support integrals、完整域 Gate O/E、shared planted scale／condition domain 與 exact swap trace。
