# Handoff v2.0 — 交接文件（Stage 5B 完成 → Stage 5C 開始前）

初稿基準（本文件建立前的 main）：`40105831802909c4b3386b6e29249f1c149d1359`
首次併入 main：`4693aba86a5e7c04bbbe4b082db2b6d9e10963f3`；合併後 repo 40 檔。
初稿基準的驗證狀態：STATUS v1.10，全庫 104 passed，`verify_integrity.py` 通過。

**`docs/STATUS.md` 是唯一的 source of truth。** 本文件只補 STATUS 沒有、
但下一階段需要的東西：已評估但未採用的替代方案、未決項、以及方法學規則。

---

## 0. 給新對話的第一段指示（可直接貼）

> 這是延續中的研究專案 https://github.com/dr17414/lightspeed-fundamental-theory
> 請先完整讀 `docs/STATUS.md`（唯一 source of truth）、`README.md`、
> `HOW_THIS_WAS_MADE.md`、`docs/STAGE5B_RESULT_B.md`，以及本 handoff。
> 已否定路線見 STATUS，不要重啟。目前停在 Stage 5B 完成、Stage 5C 尚未開始。
> 下一份產物應是 **Stage 5C 驗收條件表**，不得包含任何候選 kernel K 的公式。

**版本核對規則**：GitHub UI 的 retrieval 可能是舊快取。宣告「某檔案不存在」之前，
必須先用 GitHub API / raw / tarball 重抓 main HEAD 確認。此規則已進 STATUS，
而且已經被違反過一次（我曾據過期 checkout 誤稱 4D 測試不存在）。

---

## 1. 目前位置（一句話）

原始問題「因果關係 + 量子振幅 ⇒ 時空幾何 + 物質」**未被解決**。
已完成的是工具校準（Track A/B）與兩個關於 1+1D 的新結果（Stage 5A 正面、5B 限定否定）。

- **Stage 5A**：$(\mathcal C,\prec)\to\{U,V\}/S_2$ 為 canonical（$\kappa=1$，finite-$N$）。
  這是 **candidate chiral precursor**，不是 chirality。
- **Stage 5B**：metric 意義的 link channel **不是純 order observable**；
  rank-based $\chi$ **不是** microscopic link-local rule；
  BHS 排除 Lorentz-equivariant finite-valency nearest-neighbour 建構。
  **但沒有證明任何 local two-state internal space 都不可能存在。**

---

## 2. 只在對話中、尚未入庫的內容（**最容易掉的部分**）

### 2.1 已評估但不採用的替代 primitive（建議寫成 STATUS 附錄）

若 Stage 5C/6 逼出「結果 B：需要新的原始自由度」，這是現成的候選清單。

| 提案 | 評估 | 不採用的理由 |
|---|---|---|
| Connes spectral triple：把 Dirac 算子 $D$ 與代數 $\mathcal A$ 當 Layer 0 primitive | 正當研究方向 | 等於把 ledger 從 $\{\prec,\#,\text{phase}\}$ 換成 $\{\prec,\text{phase},D,\mathcal A\}$——**靠改變問題來回答問題**。若採用必須明標「只有 order + phase 的版本已被放棄」。 |
| Lorentz 對稱作為 IR fixed point（Hořava–Lifshitz 式） | 有已知強反例 | Collins–Perez–Sudarsky–Urrutia–Vucetich：微觀 LV 經一般 QFT 輻射修正被放大到只受標準模型耦合壓抑（約高 20 個數量級），與觀測衝突，除非極端微調。**且**若接受微觀 LV 就不需要因果集——BHS 正是採用 Poisson sprinkling 的唯一理由。 |
| 惠更斯原理選出 3+1 維 | 做不到宣稱的事 | 嚴格惠更斯在**奇數**空間維 $3,5,7,\dots$ 成立，選不出 3；且它是**連續**波動方程的性質，用作 Layer 0 原則會預設待導出物；更嚴重的是本專案算子按構造就有非局域拖尾（BHS 強制），「無拖尾」準則會反過來排斥 Track A/B。 |
| 糾纏面積律作為幾何選擇準則 | **重塑後可用，列為 Stage 7 候選** | 簡單版本已被否定：Sorkin–Yazdi 在**流形性** 1+1D causal diamond 上未截斷即得**時空體積律**，只有投影掉 Pauli–Jordan 小特徵值後才回復面積律；de Sitter 與 Belenchia–Benincasa–Letizia–Liberati 獨立重現。故面積律**非** manifoldlike 的自動性質。可用的重塑版本：「是否存在**幾何上有動機的**截斷，使面積律以正確係數出現？」**注意**：截斷方案是為了讓面積律出現而選的，直接當判準會是把答案裝進判據。BBLL 用的正是以 $l_k$ 參數化的非局域 Green function（即我們手上的算子族），機器相鄰。**前提**：需要 Stage 3 刻意未實作的 SJ construction。 |
| 量子行走取代熱核 | 部分收編進 Stage 5B/5C | 1+1D 量子行走的 coin 自由度**就是** chirality（Feynman checkerboard）。但 (a) 更新規則是新 primitive 除非導出；(b) 不可走 Hasse diagram——STATUS 已否定兩個圖擴散探針；(c) BHS 已排除最近鄰步進。故 checkerboard 式主線**已撤除**。 |
| Nielsen–Ninomiya / fermion doubling | 保留為 Stage 5D gate | 標準 no-go 依賴週期格與 Brillouin zone，sprinkling 兩者皆無，故標準證明不適用——**但這不等於 doubling 不存在**（irregular lattice 上仍有 doubling-like soft modes，加入規範作用後 doubler 可能重現）。正確做法：不預設定理適用也不預設被繞開，等有 fermion propagator 後**直接數近零模的數目**。 |

### 2.2 Stage 5C 規格第一頁必須寫的兩件事

1. **$F_x=\{(x,U),(x,V)\}$ 是平凡叢**，在每個事件上是同一個兩元素集合，
   無 $x$ 依賴。對 1+1D **恰好正確**（該處 spinor 叢本來就平凡、左右行進模本就全域定義），
   所以平凡不是缺陷。**但代價是 fiber 幾乎不帶資訊，全部內容都在 $K$ 上。**
   不得把「我們得到了 local fiber」當作進展報告——該句為真但接近空洞。
2. **兩個獨立的「不可外推 4D」理由**（現在就寫，避免 1+1D 若成功時被誤讀，
   比照 Stage 4 對 $d_s$ 的處理）：
   - $\mathbb R^{1,1}$ 的 timelike posets **恰好**是 order-dimension-2 的（Stanley）；
     $n\ge2$ 變成 sphere orders，無同樣簡單的兩線性序表示。
   - 即使在 3+1D Minkowski 中 spinor bundle 本身可平凡化，Weyl/Dirac 結構的物理內容仍來自
     **local Lorentz/Clifford representation structure**；1+1D 的一對 global null total orders
     不能直接提供這個局部結構。故不可把 $P\times\{U,V\}$ 的 1+1D 成功當成 4D spinor precursor。

### 2.3 Stage 5C 驗收條件表（草案，尚未成文）

問題：在不新增 vierbein、$\gamma^\mu$、preferred frame、nearest-neighbour rule 的前提下，
能否只用 $(P,\prec,\{U,V\},\#)$ 在導出 fiber 上建立**非局域** two-sector kernel

$$K(x,y)=\begin{pmatrix}K_{UU}&K_{UV}\\K_{VU}&K_{VV}\end{pmatrix}$$

**先寫驗收條件，不寫任何 $K$。** 現行規格為 C0–C11：

1. **C0 Allowed-input ledger**：逐項列出 $K$ 真正使用的 primitive。只允許已批准的
   $P,\prec,\#,\{U,V\}$ 與量子振幅／相位；metric、coordinates、vierbein、$\gamma^\mu$、
   preferred frame、手工 link orientation 等若出現，必須明標新增 primitive。
2. **C1 $\kappa>1$ domain handling**：finite-$N$ 仍存在 $\kappa>1$。候選必須對所有 realizer
   orbit 給等價結果，或明確聲明只定義在 $\kappa=1$ 子類；不得暗中任選 realizer 或 tie-break。
3. **C2 Relabel invariance**：$P\simeq P'\Rightarrow K\simeq K'$。
4. **C3 Sector covariance**：全域 $U\leftrightarrow V$ 時 $K\to\sigma_x K\sigma_x$；
   sector 交換只能是 basis swap，不得改變物理。
5. **C4 Information-path audit**：每個矩陣分量明寫
   $P\to(U,V,\#)\to K_{ab}$ 的資訊路徑，並在造完整 observable 前分析是否會被
   三角性／$\pm\lambda$ 配對／Hermitian 相消／determinant 或 trace 恆等式／
   gauge redundancy／similarity invariance 等代數結構吃掉。
6. **C5 Causal/retarded support**：若建 retarded kernel，$K(x,y)=0$ 於 $y\not\prec x$。
   非局域不等於任意 all-to-all；support 與權重必須可物理解釋。
7. **C6 Nonlocality / boundary / scaling control**：量化 influence range、boundary dependence、
   density/$N$ scaling 與 continuum limit；不得只在固定 finite diamond 上靠 whole-box population
   才得到結果，也不得把 Hasse hop 當成 physical locality。
8. **C7 1+1D massless external benchmark**：先令 $K_{UV}=K_{VU}=0$，
   continuum limit 必須回到已知左右行進的 massless Dirac propagation。
9. **C8 判別性對照**：$K$ 必須在一組**刻意匹配低階統計量**的 causal set 對上給出不同結果。
   匹配清單由 C4 的依賴圖決定，不得事先瞎猜。KR vs sprinkling 太容易；
   應優先用兩個都 manifoldlike/sprinkling-like 的對照並匹配 relation density 等低階量。
10. **C9 Fermionic positivity / quantum viability**：Dirac two-point function 是矩陣值的，
    $S(p)=\not p\,S_1(p^2)+\mathbb 1S_2(p^2)$，有多個譜分量。Stage 3 可遷移的是
    **方法**（spectral representation、positivity、argument principle、branch 分析），
    **不是** $\mathrm{Im}\,g/|g|^2$ 的 scalar 公式。positivity 必須從 fermionic two-point
    function 重新導出，並檢查 ghost／unstable poles。
11. **C10 Mass mixing separation**：只有 C7 massless sector 通過，且 C9 quantum viability 通過後，
    才允許研究 $K_{UV},K_{VU}$ 的 mixing 是否可扮演 mass。不得一開始把 $m$ 或 mixing matrix
    塞進去再宣稱「質量湧現」。
12. **C11 4D extrapolation firewall**：逐項標示哪些步驟依賴 1+1D 的兩個 global null orders。
    3+1D 的 Weyl/Dirac 結構需要 local Lorentz/Clifford representation structure，
    不得把 $P\times\{U,V\}$ 的成功直接外推為 4D spinor precursor。

**分階段**：
- **Stage 5C-1 — Massless feasibility**：先過 C0–C8，且固定 $K_{UV}=K_{VU}=0$。
- **Stage 5C-2 — Quantum viability**：只有前段通過後才做 C9。
- **最後才開 C10 mass mixing**。C11 從 Stage 5C 第一天就一直有效。

這不只是方法論乾淨——它也對應 1+1D 方程本身：null 座標下無質量 Dirac 是
$\partial_u\psi_R=0$、$\partial_v\psi_L=0$ 兩個解耦方程，質量項正是耦合兩者的那一項。

**待評估候選材料**（記錄方向，不是設計）：既然通道是**體積**概念，
$K(x,y)$ 的自然 order+number 材料是 $|I(x,y)|$、$\Delta r_U$、$\Delta r_V$。
其中 $|I(x,y)|$ 正是 Track A/B 已驗證算子的核心材料——
這是 Track A/B 機器與費米子路線第一個具體接點，不只是「都非局域」的氣質相似。

---

## 3. 未決項（按優先序）

| # | 項目 | 狀態 |
|---|---|---|
| 1 | **Stage 5C 驗收條件表**尚未成文 | 下一份產物 |
| 2 | Stage 5A 中 0–3% 的「非 UPO 但無 twin pair」案例：是較大的 module（仍是 automorphism，無害）還是**真正**與真值不同的 realizer？$N=200$ 的 40 樣本為 0 但樣本太小 | 未決 |
| 3 | $\kappa=1$ 的**解析**證明（Gallai / modular decomposition；Ille–Rampon 2006 可計算 dimension-2 poset 的 minimal realizations，El-Zahar–Sauer 的 unique-realization characterization 由此結構得出）。目前只是**數值結果** | 未決 |
| 4 | Stage 3 的 Sorkin–Johnston 交叉檢查（1502.01655 Eq.72–73）**刻意未實作** | 若走糾纏路線則成為 prerequisite。**嚴禁**由 Eq.(55) 端反推近似——那是循環論證 |
| 5 | Stage 4 的「BBMM Eq.(5) 可套用於 Track B」是**本專案推論**，非任一原文陳述 | 整個 Stage 4 比較的公平性以此為上限 |
| 6 | $N=20$ 時 D=4 假陽性率（0.300）**高於** D=3（0.075），非單調 | 【數值觀察】，原因未驗證 |

---

## 4. 方法學規則（本專案付過代價換來的）

1. **不自行發明 regularization / prescription。** 公式必須有原始文獻出處、
   equation number、以及該論文的**約定**（$\rho$/$\Lambda$ 冪次、無因次變數定義、
   coefficient convention）。跨論文使用前先建 mapping，**不得預設係數值**。
2. **來源歸屬**：本專案導出的結果必須與原文陳述分開標記，且在作者發布 erratum 前
   不得把「我們的高信度判定」寫成「作者已承認」（例：BBMM Eq.(15) 的 $\gamma_2$）。
3. **$R\to\mathcal D\to O$ 路徑**：提出任何可觀測量前，先寫出因果資訊從哪條數學路徑進入，
   並分析該路徑會不會被代數對稱性封死。歷史上三次失敗（單向三角行列式、
   $Q_{\rm test}$ 相位、$Q_{\rm test}$ 敏感性）都是「$R$ 進不去」。
4. **source-of-record**：程式 `__main__` 印出的表就是記錄；任何在別處引用的數字
   必須來自執行該檔案。**各 benchmark 區塊使用獨立 RNG stream**——共用 RNG 會讓
   增加一列 silently 改掉所有既有表格（已發生過）。
5. **統計紀律**：CP 區間只對獨立 Bernoulli 有效。不得對非獨立單位（如同一 parent 的
   多個 child）套 child-level CI；不得把不同 $N$ 的頻率 pooled 成單一機率
   （$p=p(N)$ 未必是同一參數）。
6. **fail loudly，不要 silent skip。** 數學上不可能的情況應 `assert` 而非 `continue`。
7. **交叉驗證必須真正獨立。** 曾出現循環測試（比較 `u_series` 與 `a - g_direct`，
   而後者在該區的定義就是 `a - u_series`）與 evaluator floor 假象
   （截斷誤差 $10^{-8}$ 冒充成內插誤差 $10^{-9}$）。
8. **位元完整性**：`verify_integrity.py` 在 CI 的 pytest **之前**執行。
   `mergeable=true` 只表示無 merge 衝突，與檔案完整性、CI 綠燈**無關**。
   曾發生 `ValueErro\x16` 導致整組 Stage 2 測試靜默未執行。
   大檔傳輸用分片 + 寫入端 hash 驗證。
9. **看起來越合理的錯誤越危險。** Stage 4 的 `0.0067`（明顯壞掉）比 `2.000000`
   （合理且剛好等於預期答案）安全得多。無外部基準的領域尤其需要提高交叉檢查密度。

---

## 5. Go/No-Go 判決（已議定）

**GO**，但下一步不是造 Dirac operator。

Track A/B 完成後手上握有的是「這類 operator 可穩定、positivity 可約束之、
$d_s$ 對 operator 選擇敏感」以及一條乾淨的文獻比較結果——
但這仍屬**基礎工具校準**，尚未觸及原始核心問題。

若 Stage 5C 最終發現在只允許 order + number + phase 的情況下，
所有合理的 fermionic 結構都無法取得足夠的 Clifford/chiral 資訊，
那會是**有價值的 No-Go**：它會明確指出最初理論缺少**哪一層**底層自由度
（見 §2.1 的候選清單），而不是讓我們靠增加公式掩蓋這件事。
