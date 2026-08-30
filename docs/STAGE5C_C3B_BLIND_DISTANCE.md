# Stage 5C — C3b Blind-Variety Distance Contract

狀態：**【已確認之 evaluator form／v0.3；尚未 freeze】** — primary endpoint 已由後續獨立交付物選定。

前置：fork B 已定案（$h=p\mathbb 1$、$G=T^2\rtimes S_2$）；ambient norm $\|M\|_F$ 已交付
（`753d9ea`）；invariant algebra 已交付（`2f48fd04`）。
驗證於 main `2f48fd04`：56 檔、integrity 通過、155 passed。（歷史快照。）

---

## 0. 命名與範圍

**不稱 quotient contract。** $\mathcal B_1=\{A\otimes f\}$ 一般**不是線性子空間**，而是
rank-one 的 **Segre cone**，故 $V/\mathcal B_1$ 無定義。本文件改以對 blind variety 的
**距離**建構，名稱為 *blind-variety distance contract*。

**本文件同時修正 acceptance spec v0.8 的另一個型別錯誤。** 不呼叫 sector／realizer API
是一個 program／provenance class，不是輸出值的線性空間。若允許任意 fixed endomorphisms
與任意 scalar functions 的有限線性組合，四個 matrix units 已張成整個 $V$；其 quotient
為零，不能成為 gate。故 C3b v0.9 分成兩軸：source／capability preflight 與本文件的
rank-one value diagnostic。**兩軸都必須通過，且不得互相替代。**

本文件**不**選定 primary $\mathfrak I_G$，**不**設計候選 $K$，**不**主張 C3b 通過蘊涵任何
chiral physics（見 §8）。

---

## 1. Ambient typed space 與 admissible pair domain

### 1.1 型別

依 observable contract §1.1，C3b 作用於 $\mathcal K$ 或 $G_R$（Stage 5C-1 不得用 $W,\rho$）。
固定 causet $\mathcal C$ 與其 admissible pair domain $\mathcal D$ 後，物件為

$$V=\mathrm{End}(F)\otimes\mathbb C^{\mathcal D}\ \cong\ \mathbb C^{4\times D},
\qquad D=|\mathcal D|,$$

row（第一軸）為 fiber slot $(a,b)\in\{U,V\}^2$，column（第二軸）為 pair
$(x,y)\in\mathcal D$。固定 row-major slot 次序 $(UU,UV,VU,VV)$。

### 1.2 Admissible pair domain（Freeze-1a 固定）

$\mathcal D$ 必須由 order 資料唯一決定、**與候選無關**。宣告項：

- $\mathcal D$ 的定義（例如全部有序對、或全部因果相關對）；
- 是否含 $x=y$；
- 邊界處理（$\mathcal D$ 是否隨 causet 大小變動，以及 §6 的密度序列如何對應）。

$D=0$ 時 evaluator 無定義，須由事前 cohort／domain gate 記 INCONCLUSIVE；不得以空矩陣
取得 C3b PASS。$D$ 太小時 §3.3 的可達上界亦隨 $D$ 改變。

**不得**以候選的 support 定義 $\mathcal D$。retarded 候選在 acausal 位置的結構性零
只是 $V$ 中的零分量，不改變 $\mathcal D$。

---

### 1.3 Program-level blind class（不能由 SVD 取代）

令 $\mathcal P_{\rm blind}$ 表示不具 sector／realizer capability 的 admissible construction
program class。它由註冊 API boundary、source dependency、taint／module rules 與禁止的內部
重算／lookup 定義；不是 $V$ 的子集或線性空間。rank $>1$ 只表示存在多個 pair profiles，
完全可能由 API-free 的 $\sum_i A_i\otimes f_i$ 產生。因此：

- $\rho>0$ **不能**證明 construction 使用了 $\{U,V\}$；
- source audit 通過也**不能**證明 sector effect 在輸出中非裝飾性；
- C3b PASS 要求兩者皆過，C4 再承擔更強的 domain-valid information-path evidence。

---

## 2. Rank-one blind variety 與距離

### 2.1 定義

$$\mathcal B_1=\{A\otimes f:\ A\in\mathrm{End}(F),\ f\in\mathbb C^{\mathcal D}\}
=\{\text{rank}\le1\ \text{矩陣}\}\subset\mathbb C^{4\times D}.$$

$$d_{\mathcal B_1}(K)=\inf_{A,f}\|K-A\otimes f\|_w .$$

$\mathcal B_1$ 是閉錐，故 inf 可達（為 min）。$f$ 的定義域是**整個** $\mathbb C^{\mathcal D}$，
不得加限制——限制 $f$ 會縮小 $\mathcal B_1$ 並虛增 $d_{\mathcal B_1}$。若確需限制，屬
protocol amendment。

### 2.2 可計算形式

> **命題 C1.** 在（加權）Frobenius norm 下，由 Eckart–Young，
> $$d_{\mathcal B_1}(K)^2=\sum_{i\ge2}\sigma_i^2=\|K\|_w^2-\sigma_1^2,$$
> $\sigma_i$ 為加權後 $4\times D$ 矩陣的奇異值。因 fiber 維度為 4，至多四個非零。

回歸驗證：固定 seed 的 $4\times120$ 隨機矩陣上，對 $A\otimes f$ 的 3000 次隨機搜尋
最小殘差 $25.070481$，解析值 $\sqrt{\sum_{i\ge2}\sigma_i^2}=24.975423$；搜尋為上界，
且相差約 $0.38\%$。

### 2.3 為什麼必須用距離而非投影

$\sigma_1=\sigma_2$ 時最佳 rank-one 逼近**不唯一**。回歸見證：某構造給
$(\sigma_1,\sigma_2)=(7.071,7.071)$，最佳分解為一整族，但 $d_{\mathcal B_1}$ 與 $\rho$ 唯一。

> **硬性規定.** 只使用距離 $d_{\mathcal B_1}$（或 §3 的 $\rho$）。**不得**依任一最佳分解
> $(A^\star,f^\star)$ 解讀 sector 結構、方向或通道歸屬。違反者判 PROTOCOL-INVALID。

---

## 3. Norm、normalization 與退化處理

### 3.1 加權 Hilbert norm

$$\|K\|_w^2=\sum_{(x,y)\in\mathcal D}w(x,y)\sum_{a,b}|K_{ab}(x,y)|^2,\qquad w>0.$$

fiber slot 上的 norm 即已交付的 $G$-不變 Frobenius $\operatorname{tr}(MM^\dagger)$。

> **v0.2 修正.** 任意純 fiber 左乘 $L(A\otimes f)=(LA)\otimes f$ 與純 pair 右乘
> $(A\otimes f)R=A\otimes(fR)$ 都保持 rank one；原稿聲稱「逐 slot 縮放破壞
> $\mathcal B_1$」是錯的。真正會破壞 Segre cone 的是**不可分離**的 slot–pair entrywise
> weighting $w_{ab}(x,y)$。

本 contract 仍只授權逐 pair 權重 $w(x,y)$：fiber metric 已由 fork B 的 L2 pairing 固定為
Frobenius，另加 slot metric 會重開 primitive／$G$-invariance audit。$w$ 必須隨 relabeling
共變、與候選輸出／target label 無關，並有 Freeze-1a 固定的
$0<w_{\min}\le w(x,y)\le w_{\max}<\infty$ 與 ratio／coverage 規則；不得以極小權重實質排除
pair modes。只有 separable weighting 才可保留 $\mathcal B_1$ 的 rank-one 語意。

$w$ 由 order 資料決定、Freeze-1a 固定形式與上界規則（spec §5.2.1(iii-a)）。

### 3.2 不變性

> **命題 C2.** $d_{\mathcal B_1}$ 與 $\rho$ 對下列作用不變：
> (i) $G$：在 §1.1 的 row-major $(UU,UV,VU,VV)$ convention，$A\mapsto BAB^\dagger$
> 即 $\mathrm{vec}_{\rm row}$ 上的 $B\otimes\bar B$；$B$ 為 $h$-unitary，
> 故此表示 unitary，為左乘 unitary，奇異值不變；
> (ii) relabeling：pair columns 與其 weights 一起置換，奇異值不變；
> (iii) 整體尺度：見 §3.3。
>
> 回歸驗證：phase、swap$\times$phase，以及 pair columns 與 weights 共置換下 $\rho$ 皆不變；
> 另逐項核對 row-major 表示與直接 $BAB^\dagger$ 完全一致。

### 3.3 正規化統計量

整體尺度屬 L3 normalization，故報告量取**無量綱比值**

令 $r=\min(4,D)$。對 $K\ne0$，

$$\rho(K)=\frac{d_{\mathcal B_1}(K)}{\|K\|_w}
=\sqrt{1-\frac{\sigma_1^2}{\sum_i\sigma_i^2}}
\in\left[0,\sqrt{1-\frac1r}\right].$$

- $\rho=0\iff K\in\mathcal B_1$（rank $\le1$）；
- 只有 $D\ge4$ 時上界才是 $\sqrt3/2\approx0.8660$，並在四個奇異值相等時達到；
  $D=1,2,3$ 的上界分別為 $0,1/\sqrt2,\sqrt{2/3}$。門檻必須對照實際 $r$，不得固定對照 1
  或 $\sqrt3/2$。回歸驗證涵蓋 $D=1,2,3,\ge4$。

### 3.4 $K=0$ 與近零

$K=0$ 時比值公式為 $0/0$，但 $0\in\mathcal B_1$ 是精確事實；故 exact zero 直接判
**C3b FAIL (`ZERO-IS-BLIND`)**，不得藉未定義比值轉為 INCONCLUSIVE。

對非零但近 noise／precision floor 的物件，先過**非平凡性 gate**。$\tau_0$ 必須作用於已凍結
normalization 後的 scale-aware signal／noise ratio；裸 $\|K\|_w$ 會被任意整體重標度通過，
不能單獨承重。其形式、允許上／下界與 calibration rule 在 Freeze-1a 固定，數值於 Freeze-2a
接觸 holdout 前登記。未過者記 **INCONCLUSIVE (`BELOW-NONTRIVIALITY-FLOOR`)**，既不得 PASS，
亦不得用來主張 rank-one 物理退化；整個 Stage 5C-1 因非 PASS 而不能前進。

### 3.5 奇異值簡併

$\sigma_1=\sigma_2$ 不影響 $\rho$ 的良定性，**不**構成 INCONCLUSIVE。它只觸發 §2.3 的
分解禁令。須在報告中列出全部四個 $\sigma_i$ 與簡併狀態，供稽核。

---

## 4. 參考值（由宣告的目標類導出，非對候選的預測）

下式是已固定 slot basis 中的 **evaluator-side planted calibration class**，不是候選形式，亦不是
所有合法表示的必要 block pattern。對 massless decoupled representative
$K=e_{UU}\otimes K_U+e_{VV}\otimes K_V$，秩至多為 2。
設 Gram 矩陣

$$\mathcal G=\begin{pmatrix}\|K_U\|^2&\langle K_U,K_V\rangle\\ \langle K_V,K_U\rangle&\|K_V\|^2\end{pmatrix},
\qquad \lambda_-\le\lambda_+\ \text{為其特徵值},$$

則 $\sigma_{1,2}^2=\lambda_\pm$，故

$$\boxed{\ \rho=\sqrt{\frac{\lambda_-}{\lambda_-+\lambda_+}}
=\sqrt{\frac{\lambda_-}{\|K_U\|^2+\|K_V\|^2}}\ }$$

**只有在 $K_U\perp K_V$ 時**才化簡為

$$\rho=\frac{\min(\|K_U\|,\|K_V\|)}{\sqrt{\|K_U\|^2+\|K_V\|^2}},$$

正交且等範數時 $\rho=1/\sqrt2\approx0.70711$（回歸驗證：$0.707106781$）。

**草案曾把此化簡式寫成無條件成立，並把偏差誤稱為有限樣本漲落——那是錯的。**
兩個獨立高斯向量在 $D=400$ 下並不正交，偏差是**系統性**的：實測 $\rho$ 分別為
$0.681695/0.457890/0.197318$（$\|K_V\|/\|K_U\|\approx1.0/0.5/0.2$），與 Gram 公式
逐位吻合，而與正交化簡式相差 $0.0029/0.0027/0.0000$。回歸測試鎖 Gram 公式。

$\lambda_-=0\iff K_U\propto K_V$，此時秩降為 1、$\rho=0$——即「兩個 sector 傳播相同
（至多差常數）」的退化情形，$\rho$ 正確判其為 blind。

**這些是參考錨點，用於設定 §5 的門檻尺度，不是對任何候選的預測，也不得回流構造。**

---

## 5. Effect-size threshold 與 noise calibration

### 5.1 門檻形式（Freeze-1a 固定 form／界限規則；數值 Freeze-2a）

C3b value-axis PASS 需 $\rho\ge\rho_{\min}$ 且顯著超過 §5.2 的 null upper bound。
$\rho_{\min}$ 的 form、**不得低於的規則**與相對 §3.3 實際 $D$-dependent 上界的位置在
Freeze-1a 固定；只有依既定 calibration formula 得到的數值可留到 Freeze-2a。若數值寬鬆到
使 rank-one core criterion 失效，依 acceptance spec §5.2.1(iii-a) 判 PROTOCOL-INVALID。

### 5.2 Noise calibration

精確的 finite-causet $A\otimes f$ 仍有 $\rho=0$；「離散化必然產生 $\rho>0$」不是定理。
只有當事前定義的 continuum planted-blind object 經宣告的 discretizer／measurement pipeline
後產生偏離時，才有非零 null distribution。故必須宣告：

1. 一個 **candidate-independent、planted-object 明定**的 null family 與 discretization／
   perturbation pipeline（形式、容量、seed lifecycle 於 Freeze-1a 固定）；
2. 由完整 null family 導出的 simultaneous upper bound
   $\rho_{\text{noise}}(D,\text{scale})$，不得只選對候選最有利的 noise arm；
3. PASS 條件為 $\rho$ 顯著超過 $\rho_{\text{noise}}$ 與 $\rho_{\min}$，而非僅超過 0；
4. null model、noise scale 與 pair weights 不得讀取候選 spectrum、$\rho$ 或任何 holdout 輸出。

**注意方向**：純隨機矩陣的 $\rho$ 接近上界，故危險方向是「blind + 噪音」被誤判為
sector-sensitive，不是反向。noise floor 必須據此校準。

### 5.3 Null control

必須有 null arm：對已知 blind 的構造施加同一 pipeline，確認 $\rho$ 落在 noise floor 內
（等效性檢定，$\delta$ 與 power 於 Freeze-1a 固定）。比照 reference probe 的 arm N；
**等效性 power 須單獨陳述並自帶 cohort floor**，不得沿用偵測型 claim 的 power。

### 5.4 Continuum survival

依 observable contract §5.2.1(iii)，$\rho$ 必須沿 Freeze-1a 宣告的密度／區域序列
**不衰減至零**。scaling-statistic form、fit window、容許上界規則與 multiple-testing treatment
在 Freeze-1a 固定；candidate-specific 數值於 Freeze-2a、接觸 holdout 前登記。單一 causet
上的 $\rho>\rho_{\min}$ **不足**，亦不得看過曲線後更換序列或 fit window。

---

## 6. 與其他 gate 的關係

- **C2/C3**：$\rho$ 的不變性由命題 C2 提供，但 C2、C3 仍須各自獨立驗收。
- **C3b source axis**：capability graph、static taint／dependency 與禁止內部重算的 audit
  是同一 gate 的另一必要軸；$\rho$ 抓不到 API-free 的 rank-$>1$ fixed lifts。
- **C4**：即使 C3b 兩軸皆過，該 sector 敏感度是否有 domain-valid information path 仍由
  C4 的 symbolic／matched-causet／合法擾動證據承擔。人工 sector-erasure 只能證明軟體路徑，
  不能單獨支持物理 dependency claim。
- **C6**：$\rho$ 的 influence-range／boundary／scaling 依 C6 同一 protocol 報告。
- **$\mathfrak I_G$**：$\rho$ 是 $K$ 的不變量，但**不是** primary endpoint 的候選；
  endpoint 選定屬另一交付物。

---

## 7. 交付格式

- source-of-record：`analysis/stage5c_blind_distance.py` 的 `__main__`；
- 報告項：至多四個 $\sigma_i$（不足者補零）、$\|K\|_w$、$d_{\mathcal B_1}$、$\rho$、
  實際 $D$ 與上界、簡併狀態、非平凡性 gate 結果、capability audit verdict、
  noise floor 與 null arm 結果、密度序列曲線；
- **不報告** $(A^\star,f^\star)$ 或任何最佳分解衍生量（§2.3）。

---

## 8. 推論上限

> C3b PASS 只同時證明：construction 通過登記的 source／capability preflight，且其有限輸出
> 不落在 rank-one blind variety。它不排除所有可能的 API-blind 等價重寫。

它**不**證明：$K$ 描述 chiral physics；兩個 sector 對應左右行進模；$\rho$ 的大小與任何
物理量成比例；或 C7／C8 會通過。**C7 與 C8 仍須完全獨立通過。**

$\rho$ 與 observable contract v0.7 §5 的判別式 $\Delta$ 是**不同**的量：
$\Delta\ne0$ 是「非純量矩陣」的充分見證但非 sector non-degeneracy 的必要條件；
$\rho>0$ 是「非 rank-one」的充要條件，但不是 program-level sector dependence 的充要條件，
亦不蘊涵 sector 內容有物理意義。兩者不得互相替代。

全部結論限 **1+1D**（C11），並依賴 fork B 的 L2 宣告。

---

## 9. 尚未完成

- $w$、$\tau_0$、$\rho_{\min}$、擾動模型與 noise floor 的**具體形式**未定（本文件只固定
  它們必須在 Freeze-1a 固定這件事）；
- $\mathcal D$ 的具體選擇未定；
- null arm 的等效性 $\delta$、power 與 cohort floor 未定；
- capability API boundary、taint／ablation schema 與禁止的 reimplementation rule 尚未具體固定；
- primary $\mathfrak I_G$ 已由後續交付物選定，但它不完成本節上述 calibration／capability
  項；D.1 第 3 項與 Freeze-1a 仍為 PENDING。

---

## 附錄 — 回歸測試對應

`tests/test_stage5c_blind_distance.py` 鎖住：命題 C1（Eckart–Young 等價、隨機搜尋為上界）、
命題 C2（$G$、swap、weights-covariant relabel 與逐 pair 加權下 $\rho$ 不變）、不可分離
slot–pair weighting 破壞 $\mathcal B_1$ 的反例、$D$-dependent 上界與其達成、
rank-one $\Rightarrow\rho=0$、
$\sigma_1=\sigma_2$ 簡併下 $\rho$ 仍唯一、§4 的 decoupled Gram 公式（含非正交情形），以及正交等範數退化為 $1/\sqrt2$。
