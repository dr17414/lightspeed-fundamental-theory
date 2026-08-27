# Stage 5C — Derived Two-Sector Nonlocal Kernel Acceptance Specification (v0.8)

狀態：**【已確認／規格定稿；Freeze-1a 未完成】** — v0.8 納入 C8.4 獨立復檢所發現的 covariate-addition 繞道。本文件只固定 acceptance contract；附錄 D.1 九項尚未在單一 freeze commit 全部完成，故目前**不構成 Freeze-1a**，不得開始候選設計或 confirmatory evaluation。

修訂基準：`docs/STAGE5C_ACCEPTANCE_AUDIT.md`（STATUS v1.12）的獨立審計判決「規格需修訂」，v0.2–v0.7 的後續獨立 review，以及 `docs/STAGE5C_C8_4_HARD_CONTROLS.md` 的跨 seed 復檢。

驗證於 main `d9b13dd`：41 檔、`verify_integrity.py` 通過、104 passed。
（依 handoff §0 版本核對規則，本行為**歷史快照**，不隨 HEAD 更新。）

`docs/STATUS.md` 仍為唯一 source of truth。

---

## 0. 本文件的地位與明確排除

本文件**不包含任何候選 kernel $K$ 的公式、構造、材料選擇或參數化**。

排除清單（v0.4 釐清 construction 與 evaluator）：

- 不寫 $K$ 的任何顯式定義。
- 不寫、也不暗示任何可供候選 $K$ 使用的 order ansatz、weight 或構造材料。為使 Freeze-1a/1b/1c 可執行，**evaluation-only** 的 matching covariates、diagnostics 與 continuum targets 可以具名，但必須明標用途、在候選存在前固定，且不得被描述成候選材料或推薦方向。
- 不預設 Stage 5C 會成功，也不預設會失敗。

---

## 1. Claim contract（主張契約）

### 1.1 被檢驗的主張

> **S5C-Claim.** 在不新增 metric、coordinates、vierbein、$\gamma^\mu$、spinor index、chirality、preferred frame、nearest-neighbour rule 的前提下，僅由 $\mathcal I_0=\{\mathcal C,\prec,\#,\text{amplitudes/phases}\}$ 與 Stage 5A 導出的 $\{U,V\}/S_2$，可在平凡 fiber $F_x=\{(x,U),(x,V)\}$ 上建立本質非局域的 two-sector kernel，其連續極限回復 **1+1D** massless Dirac 的雙通道傳播。

### 1.2 本規格**不**授權的主張

即使全部 gate 通過，以下**不**成立且不得書寫：

- 「已導出 spinor」「已導出 chirality」「已得到 local two-state internal space」。
- 任何 3+1D 陳述（見 C11）。
- 「$\{U,V\}$ 是 chirality」。Stage 5A 的上限仍是 **candidate chiral precursor**。
- 「已得到 local fiber」作為進展。$F_x$ 在每個事件上是同一個兩元素集合、無 $x$ 依賴，即平凡 product fiber；對 1+1D 這恰好正確（該處 spinor 叢本可平凡化、左右行進模本就全域定義），但**代價是 fiber 幾乎不帶資訊，全部內容都在 $K$ 上**。該句為真但接近空洞。

### 1.3 為什麼不要求 finite valency

BHS (gr-qc/0605006, Thm 1)：full Minkowski Poisson sprinkling 不存在到 spacetime direction 的 measurable Lorentz-equivariant map；有限方向集合與 finite-valency intrinsic graph 受同一阻礙。

故非局域在 Stage 5C 是**設計原則而非缺點**。任何回到「每 event intrinsic 選一個 $U$ 鄰居、一個 $V$ 鄰居」的構造在規格層次即 **CONDITIONAL-FORK**（因此 S5C-Claim FAIL），不進本主張的數值階段；這是候選新增了 nearest-neighbour primitive，不是樣本落在定義域外。該構造可另立 conditional project 保存，但不得記為 C0 PASS。

作用域註記：該定理嚴格針對 full Minkowski sprinkling；**有限 diamond 可含 boundary-induced direction**，有限區域的成功不能當作 intrinsic full-spacetime 性質的證據。

---

## 2. Verdict taxonomy（判決分類）

每個 gate 的結果必須落入且僅落入下列之一。**不得**以任何方式把非 PASS 記為 PASS。

| 判決 | 意義 | 後續 |
| :--- | :--- | :--- |
| **PASS** | 在宣告 domain 內達到事前登記門檻 | 進入下一 gate |
| **FAIL** | 在宣告 domain 內未達門檻 | 停止；封存為該候選的限定否定結果 |
| **INCONCLUSIVE** | 計算上限（enumeration cap、精度 floor、樣本不足）或 evaluator 缺失 | **既非 PASS 亦非物理 No-Go**；必須列為未決項並說明所需資源 |
| **OUT-OF-DOMAIN** | 某個 input instance／樣本落在候選事前宣告的定義域外 | 從該 gate 的統計中排除並報告排除率；候選層仍須滿足 C1 coverage 門檻 |
| **PROTOCOL-INVALID** | object、evaluator、門檻、資料切分或 gate 對照未在規定的 freeze 時點完成 | 不得執行或解讀該 gate；先修規格／dossier，不能包裝成物理 INCONCLUSIVE |
| **CONDITIONAL-FORK** | 候選新增了未獲 S5C-Claim 允許的 physical primitive | **S5C-Claim 判定 FAIL**；可另立 conditional project 保存，但不得記為 C0 PASS |

CONDITIONAL-FORK 是審計指出的 loophole 的封堵：新增 $\gamma^\mu$、metric 等 construction primitive 之後的成功是**另一個主張**的成功。OUT-OF-DOMAIN 是 sample-level 標記；候選要取得 gate-level PASS，仍須達到 C1 事前登記的 domain coverage 與穩定性門檻，不能靠把困難樣本全排除來通過。

**每個 gate 對每個候選版本恰有一個 verdict**，取自上表。INCONCLUSIVE 必須附 `reason=`，其中一個合法值是 `BOUNDED-SEARCH-EXHAUSTED`（見 §2.1）。

### 2.1 Freeze-deliverable status（規格層，非 gate verdict）〔v0.7 新增〕

v0.6 把 `BOUNDED-SEARCH-EXHAUSTED` 與 `SPEC-INFEASIBLE` 列進 gate verdict 表，造成型別衝突：它們描述的是**某項 Freeze-1x 交付物**的狀態，不是某個 gate 對某個候選的判決，而且後者根本先於任何候選存在。v0.7 移出，另立本表。

| 狀態 | 意義 | 後續 |
| :--- | :--- | :--- |
| **DELIVERED** | 該交付物已完成並凍結 | 相應階段可開始 |
| **PENDING** | 尚未完成 | 相應階段的 confirmatory evaluation 不得開始；若強行執行，該 gate 判 PROTOCOL-INVALID |
| **BOUNDED-SEARCH-EXHAUSTED** | 在明定的有限構造類 $\mathcal G$ 內窮盡搜尋仍無法構造 | 記錄 $\mathcal G$、搜尋界與資源；**不得**推論到 $\mathcal G$ 以外。依賴它的 gate 記為 `INCONCLUSIVE(reason=BOUNDED-SEARCH-EXHAUSTED)` |
| **SPEC-INFEASIBLE** | 已就 $\mathcal G$ 對**全部 admissible constructions** 證明 completeness，且該類內不可構造 | 關於**規格前提**的結果；依 §9.4.2 封存為 specification-level 限定結論 |

三個「做不到」必須分清：**PROTOCOL-INVALID**（gate verdict）是「該做而未做」；**BOUNDED-SEARCH-EXHAUSTED**（deliverable status）是「在某個明定類內做了、沒找到」；**SPEC-INFEASIBLE**（deliverable status）是「證明了在全部 admissible constructions 內都做不到」。前兩者都不得記為候選 FAIL；後者不得在缺 completeness 論證時使用——沒有 completeness 就只能停在 BOUNDED-SEARCH-EXHAUSTED。

---

## 3. Object contract（物件契約）

**這是 v0.1 最重的缺失。** v0.1 的 C5 測 retarded support、C7 混用 propagator／Green function、C9 測 Wightman/spectral object——三個不同的數學物件在 gate 之間靜默切換。

候選 dossier 必須在任何數值之前宣告下列**型別鏈**，並指明每個 gate 作用在哪一個物件上：

| 代號 | 物件 | 型別 |
| :--- | :--- | :--- |
| $\mathcal K$ | kinetic / difference operator | fiber endomorphism valued kernel on $\mathcal C\times\mathcal C$ |
| $G_R$ | retarded inverse | 與 $\mathcal K$ 的左／右 inverse 或 composition law（含 contact term 與邊界條件）須明定；不得與一般 evolution kernel 混稱 |
| $W$ | quantum two-point object（Wightman） | 附 adjoint / pairing / state 宣告 |
| $\rho$ | spectral object | 只在連續 evaluator 中定義 |
| $\mathcal O$ | reported observables | 明列 |

**強制宣告項：**

1. 上述哪些物件是**基本定義**、哪些是**導出**，以及導出所用的每一步（求逆、極限、平均、smearing）。**若要取得 Stage 5C-2 quantum-viability PASS，$W$ 必須由同一候選的 $\mathcal K/G_R$ 經 Freeze-2b 凍結的 state、pairing 與 quantum prescription 導出，$\rho$ 必須再由該 $W$ 導出。**獨立基本定義一個與候選無關的正定 $W$ 屬 CONDITIONAL-FORK，不能用來替候選通過 C9。
2. **basis contract**：fiber 的基底慣例（diagonal null-sector basis？chiral basis？）與 $2\times2$ 分量的意義。此項承重——sector 資訊落在 diagonal 或 off-diagonal **完全取決於此宣告**（見 C3b）。
3. **pairing / adjoint contract**：$W$ 的內積、共軛、state、basis-phase convention，以及 fermionic 反交換慣例；任何物理上不等價的選擇都須列入 C0 ledger。
4. **evaluator oracle 宣告**：外部連續 evaluator 允許使用 Clifford / gamma / 微分結構（C7 本來就在用），但必須列為 **evaluation oracle**，且必須證明其不回流到 $K$ 的構造路徑（見 C0 的 no-oracle-leakage）。
5. **primary-observable contract**：C7/C8 用來決定 PASS 的 primary observable、smearing、norm 與 continuum target 必須在 Freeze-1a 固定；C9 的 evaluator form 在 Freeze-1b 固定；C10 的 massive target／evaluator form 在 Freeze-1c 固定。C6 的 nested-region／boundary selectors 亦須在 Freeze-1a 固定。候選 dossier 只能增加 secondary diagnostics，不能更換 primary endpoint。

**gate ↔ 物件對照表**必須逐條填寫。任一 gate 若無法指明其作用物件，dossier 判 **PROTOCOL-INVALID**，該 gate 不得開始；這不是物理 INCONCLUSIVE。

---

## 4. Provenance contract（來源契約）＝ C0 的實體

五分類 ledger。每一個進入 $K$ 的量必須歸入且僅歸入一類：

| 類別 | 內容 | 規則 |
| :--- | :--- | :--- |
| **L0 Layer-0** | $\mathcal C,\prec,\#$ | 允許 |
| **L1 derived non-canonical** | $\{U,V\}$、realizer 導出量 | 允許，但必須通過 C1 的 orbit 處理 |
| **L2 quantum scaffolding** | complex linear combinations、amplitudes/phases、pairing/adjoint、state、CAR、basis-phase convention | **見 §4.1，必須宣告；不得報為由 poset 湧現** |
| **L3 free / calibrated structure** | 自由函數族、參數、lookup、regulator/prescription、截斷、smearing／非局域尺度、歸一化、optimizer、RNG/seed policy | 必須做容量與來源審計，見 §4.2 |
| **L4 evaluation oracle** | 連續 evaluator 所用的 metric / gamma / 微分結構 / sealed coordinates | 只許在 evaluator 端，**不得回流** |

### 4.1 unrestricted phase 足以編碼整個答案

$\mathcal I_0$ 含 "complex amplitudes/phases"，但**逐 pair 自由的相位有 $O(N^2)$ 個自由度，足以編碼任意目標**。若不約束，S5C-Claim 會被瑣碎地滿足而不構成任何推導。

**規則.** 相位必須二擇一：

- **(a) derived**：由 $(\prec,\#,\{U,V\})$ 經一個明寫的映射決定；映射的 source hash、來源、自由函數族與 dependency path 全部入 ledger，且受 C0–C4（含 C3b）約束。不得含以 holdout isomorphism class、sealed seed 或 target metadata 為鍵的 lookup。
- **(b) drawn**：自一個明寫的分布抽取，其**分布自由參數個數必須為 $O(1)$，不得隨 $N$ 增長**。RNG algorithm、seed derivation 與 stream 隔離須在相關 candidate-specific freeze（Freeze-2a/2b/2c）固定；seed 不得校準、挑選或依輸出重抽。結論必須對 phase ensemble 陳述並附 seed sensitivity，不得只報最有利 realization。

任一相位自由度隨 $N$ 增長的方案，**C0 判 FAIL**。

### 4.2 free / calibrated structure 的容量與來源

L3 不只計數 scalar parameters，也必須列出 function family、lookup table、canonical-labeling routine、optimization objective、regulator／analytic prescription、enumeration cutoff、tolerance、dimensionful scale、RNG 與 seed policy。每一項須附來源、容量如何隨 $N$ scaling、以及是否經 calibration。

- per-event／per-pair 可調自由度或容量隨 $N$ 增長的 lookup／function family：**FAIL**。
- 新增未由 L0/L1 導出、也非明定 universal scaffolding 的 physical scale／prescription：**CONDITIONAL-FORK**。
- $O(1)$ 校準參數：只可使用 calibration split，且 family、objective 與取值規則必須在接觸相應 holdout 前完成相關 Freeze-2a/2b/2c。
- 僅把複雜規則寫成「零參數函數」不能免除容量審計；其 source hash 與設計／資料來源仍須記錄。

### 4.3 No-oracle-leakage dataflow

必須提供**結構性**保證，而非口頭保證：計算 $K$ 的模組在程式層次不可存取 sealed coordinates 或任何 L4 物件。

可接受形式：模組分離 + import 禁令 + 測試斷言；或 runtime taint 檢查。

**免費的必要條件（保留自 v0.1，理由已依審計收窄）**：純 $(P,\prec,\#,\{U,V\})$ 的量在 Stage 5B 的 monotone re-embedding 下**逐位元不變**，因為得到的是同一個抽象標號 poset。`tests/test_stage5b_link_channel.py::test_monotone_reparameterisation_preserves_order_and_rank_channel` 已實作此 witness。Stage 5C 必須加同型測試。候選若在該操作下改變，即已讀取座標。

---

## 5. Continuum / statistical contract（連續與統計契約）

### 5.1 連續恢復主張的正確作用域〔依審計收窄〕

Stage 5B 的 witness 證明的是：**同一抽象 poset 的 pure-order functional 不可能逐 pair 回復兩個互相衝突的 coordinate-defined targets。**

由此得到的限制**只作用於 continuum recovery claim**：

> 連續恢復主張必須相對於**明定的 sprinkling probability measure**，並表述為 ensemble expectation、convergence in probability 或 almost-sure convergence；**不得**要求每個有限 embedded causet 都逐 pair 等同於 coordinate-defined target。
>
> **單一 causet 上的 intrinsic algebraic tests（symmetry、support、代數恆等式、退化性）不受此限制**，仍應逐 pair 驗收。

**witness 的正確身分.** 該操作是**相對於固定 metric / volume rule 的 active re-embedding**，不是被動座標變換。被動 diffeomorphism 若連 metric measure 一起推送，不會使物理均勻 sprinkling 失效；active re-embedding 則把同一抽象 poset 放進不同密度剖面，因而 coordinate-defined target 改變。此區分必須寫在 C7 的解讀中。

**直接後果.** Stage 5B 的 97.4% per-link 一致率是**均勻 sprinkling 的性質，不是原理性對應**，因此不得作為 C7 的通過條件。sealed continuum coordinates 全程為 L4 evaluation oracle，只作 diagnostic，永不作 input。

### 5.2 分階段 freeze〔取代 v0.1 §2.2 與 v0.3 的單體 Freeze-1/2〕

把所有 evaluator 強迫在 Stage 5C-1 前一次完成，會讓尚未啟動的 C9/C10 阻塞 massless feasibility；反過來把 evaluator form 留給候選 dossier，又會形成循環。故按階段拆為三組 candidate-independent / candidate-specific freeze：

| Freeze | 凍結內容 | 最遲完成時點 |
| :--- | :--- | :--- |
| **Freeze-1a** | C0–C8（含 C3b，下同）的 verdict taxonomy；C3b blind-space／projection 與 invariant-norm **形式**；C5 diagnostic 的選擇與形式；C6 selectors；C7/C8 primary observable、massless target、smearing、norm、planted alternatives；C8.1 matching protocol；C8.4 controls；batch lifecycle；全域 confirmatory ledger 與跨版本 multiplicity/attempt budget | 任何候選設計及 Stage 5C-1 confirmatory evaluation 前 |
| **Freeze-2a** | 該候選的 $K$、object/basis contract、normalization、C0–C8（含 C3b）的 L3 family／參數、domain、blind-space／norm 的 object-specific instantiation、數值門檻、樣本數、RNG/seed | 接觸 Stage 5C-1 fresh holdout A 前 |
| **Freeze-1b** | C9 finite test-function space／projector 的形式、spectral criteria、CAR/sum-rule/analytic-stability criteria、獨立 pipeline 的結構要求 | Stage 5C-2 confirmatory evaluation 前；不阻塞 Stage 5C-1 |
| **Freeze-2b** | 同一候選的 $W$ 導出、state、pairing、quantum prescription、representation mapping、pipeline 實例與 C9 數值容差 | 接觸 Stage 5C-2 fresh holdout B 前 |
| **Freeze-1c** | C10 massive target、dispersion、primary observable、smearing、norm 與 evaluator form | Stage 5C-3 confirmatory evaluation 前；不阻塞 Stage 5C-1/2 |
| **Freeze-2c** | mixing rule、E1/E2/E3 source class、參數、zero-mixing path、scaling 與 C10 數值門檻 | 接觸 Stage 5C-3 fresh holdout C 前 |

**不可逆規則.** 後段 freeze 不得修改已通過的 $K$、object/basis contract 或早期 evaluator。若 C9/C10 顯示必須改 $K$ 或較早契約，必須建立新 candidate version，返回 Freeze-2a，使用全新的 holdout A，並消耗全域 confirmatory budget。重新 freeze 絕不恢復既有資料的盲性。

本規格定稿 commit 是後續 Freeze-1a 的 immutable baseline；只有附錄 D.1 九項交付物全部完成、在單一 freeze commit 中固定並明確引用本規格 commit，才構成 Freeze-1a。Freeze-1b/1c 可在前一階段 PASS 後另行完成，不得追溯修改 Freeze-1a。

### 5.2.1 Freeze-1b/1c 的 candidate-independence〔v0.6 重寫〕

分階段 freeze 換來 5C-1 不被 C9/C10 阻塞，但引入一個必須明說的代價：

> Freeze-1b 依表定在 **5C-1 PASS 之後**完成。屆時候選 $K$ 已存在、已跑完 C0–C8。撰寫 Freeze-1b 的人**必然知道候選長什麼樣**。

v0.5 曾以「provisional 草稿 + 修改要消耗 attempt budget」處理，**該方案作廢**：草稿若可粗糙、可預期修改，核心判準仍然可以在看過候選之後調整，循環並未封住；而讓 protocol 修改消耗統計預算，也與 §5.3「預算只由 holdout revelation 消耗」自相矛盾。

v0.6 改為**兩層切分**。

#### (i) Immutable core — 在 Freeze-1a 固定，事後不可變

C9/C10 的**判準本身**——即「什麼必須為真」——必須在 Freeze-1a 寫定並凍結，且不得於 1b/1c 放寬、刪除或替換。至少涵蓋：

- **C9 core**：須存在明定的 spectral representation；須滿足的 positivity 結構種類（含分量間不等式的**存在要求**，非其數值）；CAR／normalization／sum-rule chain 須成立；analytic stability（不得有 unstable poles）；須以獨立 pipeline 交叉驗證。
- **C10 core**：massive consistency、massless limit 連續性、units/scaling 非自由校準、post-mixing revalidation 範圍（§C10.2 第 4 項的逐項清單）。

#### (ii) Implementation layer — 留給 Freeze-1b/1c

只允許「**怎麼量**」，不允許「**什麼必須為真**」，也不允許「**什麼要被拿去量**」：

- test-function space 與 projector 依 object contract 的**實例化**（其**形式與規則**已在 Freeze-1a 固定，見 (iii-b)）；
- convention／dimension／signature mapping 的**具體對應表**（其 equivalence 判準已在 1a 固定）；
- pipeline 的**具體架構**（其 independence 判準已在 1a 固定）；
- 數值容差的**數值**（其形式與上界規則已在 1a 固定，見 (iii-a)）；
- planted-failure family 的**實例**。

#### (iii) implementation 不得吞掉 core

(i)/(ii) 的界線本身可被規避。**通則：**

> 任何名義上屬 implementation、但有能力使某條 core criterion 失效的自由度，其**形式與規則**必須在 Freeze-1a 固定；1b/1c 只能在已固定的規則下實例化。

目前辨識出兩類這樣的自由度。

##### (iii-a) 容差

夠鬆的容差等同於刪除該條 criterion。故任何能使 core criterion 失效的容差，其**形式與上界規則**在 Freeze-1a 固定，即使數值留到 1b/1c。可接受形式例如「容差 $\le$ 事前給定的常數」或「容差由 calibration split 的 noise floor 依固定公式導出」。**不得**在 1b/1c 自由選定無上界規則的容差。

##### (iii-b) test-function space 與 physical projector〔v0.7 新增〕

**這一類比容差更徹底**：容差只是把門檻放低，而 projector／test space 決定**哪些模態根本不進場受檢**。若看過候選後才決定，就能把負模劃出「非物理子空間」而使 C9 positivity 自動通過。這與容差繞過同型，且更難事後察覺。

因此下列各項**移至 Freeze-1a 固定**：

1. **admissible test-space／projector 的形式**（允許的函數類、$\ell^2$/Sobolev 型別、離散化方式）；
2. **coverage／completeness 規則**——必須涵蓋哪些模態、以及「完整」的判定方式；
3. **允許排除模態的條件**（見下）；
4. **mapping-equivalence 判準**——兩組 convention／representation 何時算等價；
5. **pipeline-independence 判準**——兩條 pipeline 何時算真正獨立（比照既有反循環紀律：不得比較 $A$ 與 $B$ 而 $B$ 的定義由 $A$ 反推）。

Freeze-1b 只能依 object contract 在上述規則下**實例化**。

**排除模態的三條硬性規則：**

- **預設為不排除。** 排除任何模態都需要在 Freeze-1a 就寫明的、**先驗的物理理由**（例如 gauge 模、邊界人為模），不得事後補理由。
- **排除判準必須「盲於候選」〔v0.7 補，較「不得依 spectrum 選擇」更可操作〕。** 排除某模態的 predicate 必須**僅由 object contract 可計算**，不需要對候選求值。若一條排除規則必須先算出候選的 spectrum 才知道要排除誰，它就是被候選決定的，該 gate 判 **PROTOCOL-INVALID**。
- **被排除集合仍須報告。** 必須一併報告排除集合上的 norm／positivity 診斷結果。這使「排除集合恰好裝著全部負模」在報告中直接可見，是成本極低且極有效的稽核。

**明文禁止**依候選的 spectrum、eigenvalue sign、norm 分布或任何實際輸出選擇或調整 projector 與 test space。違反者該 gate 判 **PROTOCOL-INVALID**。

無法在 Freeze-1a 提前決定者，沿用 (iv) 的 blinded-reviewer fallback。

#### (iv) Blinded-reviewer fallback

若某條 core criterion 確實無法在 Freeze-1a 決定（例如須先知道 object contract 的型別），則該條必須由**看不到任何候選輸出**的獨立 reviewer 制定，並在 protocol-amendment ledger 記錄其 blinding 條件。不得由已見過候選結果的人制定。

#### (v) External-justification-only rule〔v0.6 依 C9.3 收緊〕

core criteria 的採用、放寬或刪除，只許以外部依據論證，且外部依據**分兩級**：

| 級別 | 可用於 | 條件 |
| :--- | :--- | :--- |
| **承重（load-bearing）** | 決定 criteria、公式、prescription、門檻形式 | 必須先完成並記錄 equation／dimension／signature／adjoint／convention mapping |
| **動機性（motivational）** | 只能論證「該設這道 gate」，**不能**論證其內容或門檻 | 無須 mapping |

依 C9.3 的現況：**Noldus (1305.0443) 為動機性**；**BBMM 與 ASS 是 $d>2$／4D 結果**，未完成 dimension mapping 前同樣只能是動機性；**Potting (1112.5739)** 僅其 $c^{\mu\nu}\to0$ 的 Lorentz-invariant reduction 可作 secondary cross-check，其 LV-dependent 分解與 sum rules 不得移植。

> **直接後果.** 目前**沒有任何外部文獻具備承重資格**。因此 Freeze-1a 的 C9/C10 immutable core 目前只能由**數學上的必要條件**與**既有 STATUS 結論**論證；若要引用上述文獻決定內容，必須先完成 mapping —— 該 mapping 工作已列為 D.1 第 8 項。

**明文禁止**以「候選滿足此條件」「候選在此判準下表現較好」或任何援引候選實際輸出的理由，作為採用、放寬或刪除任一 criteria 的依據。違反者該 gate 判 **PROTOCOL-INVALID**。

#### (vi) Protocol-amendment ledger〔與統計預算分離〕

對 Freeze-1b/1c implementation layer 的每次修改，記入 `docs/stage5c_protocol_amendment_log.md`：時間、修改項、修改前後、外部依據、blinding 狀態、以及當時是否已見過任何 confirmatory 結果。

**此帳本不消耗統計 attempt budget**（統計預算只由 §5.3 的 holdout revelation 消耗）。它的作用是**可稽核性**：core 已被凍結，implementation 的修改本身不威脅統計效力，但反覆修改的模式是 tailoring 的信號，必須留下痕跡供 review。

殘餘風險必須在 Freeze-1a 明列，不得因為已寫了以上條款就視為已消除。

### 5.3 calibration / holdout

- calibration 與每一批 holdout ensemble 以獨立 RNG stream 生成；切分／batch 規則與 hash manifest 在相關 Freeze-1a/1b/1c 固定，未輪到的 holdout metadata 保持 sealed。Stage 5C-1/2/3 分別使用 fresh holdout A/B/C，後一階段不得重用前一階段已揭露的 confirmatory data。
- 所有 L3 校準只許用 calibration split。
- 每一批 holdout 只許**揭露一次**，揭露後即 burned。若候選、門檻或 evaluator 因結果而修改，舊 holdout 可降級為 development data，但下一次 confirmatory evaluation 必須使用新的獨立 holdout batch；重新 Freeze-2a/2b/2c 不能讓舊資料恢復盲性。
- 必須維護跨 batch、跨 candidate version、跨 Stage 5C 階段的唯一帳本 `docs/stage5c_confirmatory_ledger.md`。每次 confirmatory attempt 在揭露前登記 candidate id/version/source hash、stage、holdout batch id/hash、Freeze-1x/2x protocol hashes、planned test family 與預算；揭露後追加 verdict、已消耗的 $\alpha$／e-value／attempt budget 與 burned 狀態。版本改名或換 fresh batch **不得重置**全域預算。
- Freeze-1a 必須事前選定全域 attempt cap，或對所有候選版本與階段有效的 family-wise $\alpha$ / e-value spending rule。預算耗盡後，不得再宣告 confirmatory PASS；若要啟動新一輪，須先有明確版本化的新 protocol 與獨立 data-generating plan，且既有 exploratory 結果仍不得升格為 confirmatory evidence。
- **exploratory 不佔統計預算，但必須留紀錄〔v0.6 修正〕.** 在 calibration／development split 上的探索——試候選、調 L3、看診斷、丟掉不行的方向——**不限次數、不消耗 attempt budget、不進 confirmatory ledger、無須事前登記**。只有「揭露某一批 fresh holdout」的 confirmatory attempt 計入預算。
  這一點決定本規格是可執行還是自我癱瘓：若誤以為所有評估都吃預算，attempt cap 一設小專案就無法運作。設計意圖是**把絕大部分工作推到 calibration 側**，只讓真正有把握的候選版本去碰 holdout。
  **但「不需登記」在 v0.5 寫得過寬**：完全無紀錄會違反 C0 的 provenance 要求與可重現性。修正為——exploratory 必須進 **`docs/stage5c_development_log.md`**，記錄 candidate id／source hash、所用 data split、以及做了什麼決策（採用／丟棄／調整何項）。
  該 log 與 confirmatory ledger 的差別是刻意的，不可混淆：

  | | development log | confirmatory ledger |
  | :--- | :--- | :--- |
  | 登記時點 | 事後 append-only | **揭露前**事前登記 |
  | 消耗統計預算 | 否 | 是 |
  | 目的 | provenance／可重現性 | 統計效力控制 |

  保持 append-only 且事後登記，是為了讓探索維持低成本；要求事前登記才會重建癱瘓。
  紀律仍是單向的：exploratory 結果可以決定「要不要做 confirmatory」，但**永遠不能反過來充當 confirmatory evidence**，也不能用來事後調整已 freeze 的 form 或 core criteria。

### 5.4 密度／區域序列與收斂

連續極限必須指定序列：固定物理區域提高 $\rho$、或固定 $\rho$ 放大區域，並報告收斂率與外插。

### 5.5 統計紀律

- 獨立單位必須明確定義。Clopper–Pearson 只對獨立 Bernoulli 有效。
- 不得對非獨立單位（同一 parent 的多個 child）套 child-level CI。
- 不得把不同 $N$ 的頻率 pooled 成單一機率（$p=p(N)$ 未必是同一參數）。
- **stop-rule family**（固定樣本或事前指定的 sequential design、within-analysis multiplicity correction、最大資源上限）在相關 Freeze-1x 固定；candidate-specific 樣本數、power target 與效應門檻在相關 Freeze-2x 固定。不得依中途結果追加樣本而無預先規則。
- 單次 analysis 內的 multiplicity correction 不足以處理反覆換版本／換 batch；跨 attempt 的 error/evidence spending 以 §5.3 的全域 ledger 為準。

---

## 6. 驗收條件 C0–C11

格式：**T** = test，**P** = pass threshold，**F** = failure meaning，**E** = evidence artifact。

每個 P 必須明確標示由相關 Freeze-1x 或 Freeze-2x 固定：candidate-independent primary endpoint、norm、matching/evaluator form 屬 Freeze-1x；只有 candidate-specific normalization、effect、tolerance、sample size 與 mapping 數值可留到 Freeze-2x。未標來源或把 Freeze-1x 項目延後者判 PROTOCOL-INVALID。

---

### C0 — Provenance / allowed-input ledger

依 §4 的五分類 ledger。

- **T** — (1) 完整五分類 ledger；(2) no-oracle-leakage 的結構性保證與測試；(3) monotone re-embedding 逐位元不變性測試；(4) L2 相位／RNG 與 L3 capacity audit；(5) source／data provenance 與 hash manifest。
- **P** — ledger schema 與 capacity rule 在 Freeze-1a 固定；candidate-specific ledger／L3／seed 實例在 Freeze-2a 固定。ledger 無 L4 回流；不變性測試逐位元通過；相位與 L3 容量符合 §4.1–4.2；所有 calibration、seed、scale 與 prescription 皆有允許來源。
- **F** — 新增未允許的 construction primitive $\Rightarrow$ **CONDITIONAL-FORK，S5C-Claim FAIL**；相位或 L3 可調容量隨 $N$ 增長、挑選 seed、或使用 holdout-keyed lookup $\Rightarrow$ FAIL。
- **E** — `docs/stage5c_dossier_<id>.md` ledger 章節 + `tests/test_stage5c_provenance.py`。

---

### C1 — Domain / quotient contract

Stage 5A source-of-record：$P(\kappa=1)$ 在 $N=20,50,100,200,400$ 為 $0.765,0.907,0.963,1.000,0.975$——finite-$N$ 下 $\kappa>1$ 確實發生。

**必須處理的四種情形**（v0.1 缺，審計指出）：

| 情形 | 處理 |
| :--- | :--- |
| $\kappa>1$（多 orbit） | 對**全部** orbit 求值並證明在已宣告 quotient action 下等價，或以無偏、來源明定的 orbit prescription 產生 quotient-level observable；該 prescription／measure 須進 L3 ledger，物理上不等價的新選擇依 C0 判定；否則只能聲明定義在 $\kappa=1$ 並報告佔比與 $N$ 依賴 |
| $\dim(P)>2$ | 判 **OUT-OF-DOMAIN**，報告排除率；不得靜默丟棄 |
| enumeration cap | `realizer_permutations` 的 `max_classes=14`、`max_combos=4096` 會 bail；此時判 **INCONCLUSIVE**，不得判 PASS 也不得判 FAIL |
| automorphism / sector swap | 依 C2、C3 |

- **T** — (1) 對 $\kappa=2,3$ 的 pinned 實例（`tests/test_stage5a_realizer.py::test_pinned_instances`）逐 orbit 求值並套用已宣告的 automorphism／sector action；(2) cap 觸發時 fail loudly；(3) 在 Freeze-2a 先固定 domain、各 $N$ 最低 retained fraction 與 restriction／extension stability 測試。
- **P** — quotient／coverage evaluator form 在 Freeze-1a 固定，candidate domain 與數值門檻在 Freeze-2a 固定。orbit-level output 在宣告 quotient 下等價（不是未定義的「逐位元相同」），或候選的受限 domain 在每個 $N$ 達到預先門檻、排除率已報告且 coverage 不隨 continuum sequence 消失；domain 必須足以執行 C6–C8。
- **F** — 暗中任選 realizer 代表、或以 index 順序 tie-break $\Rightarrow$ FAIL。
- **E** — orbit 等價性測試 + domain 統計表（含 OUT-OF-DOMAIN 與 INCONCLUSIVE 各自比率）。

**$N\ge40$ 的地位〔依審計更正〕**：這是 **pilot floor**，來自 Stage 5A 的 small-$N$ 假陽性警告（$N=20$ 時 $D=4$ 假陽性 0.300、$D=3$ 為 0.075，非單調；到 $N\approx40$ 才清楚分離）。**它不是 continuum acceptance rule**；連續驗收由 §5.4 的密度／區域序列決定。

---

### C2 — Relabel equivariance

- **T** — 隨機置換元素標號並加入 pinned automorphism cases，斷言各 gate 所作用物件依對應 action **共變**（非不變）。相位場必須隨置換一起搬動，不得綁在 ID 上。
- **P** — exact arithmetic 下逐位元；浮點下以 Freeze-2a 固定、scale-aware 的 norm 與 tolerance 判定，不以含糊的「看似機器精度」取代門檻。
- **F** — 相位或權重隱含綁定 index。此坑已踩過並修過（STATUS「附加相位場的標籤不變性」一列）。
- **E** — `tests/test_stage5c_symmetry.py`。

**若候選為隨機構造**：共變性須以分布層次陳述（equality in distribution），並在 Freeze-2a 宣告 coupling／共用隨機源、檢定統計量與 power；單次抽樣相同不構成證明。

---

### C3 — Sector-swap covariance

- **T** — 全域 $U\leftrightarrow V$ 交換下斷言每個相關物件依 basis contract 的 action 共變（在標準 slot basis 為 $K\mapsto\sigma_xK\sigma_x$）。三分法判斷必須保留第三值 $\bot$。若 basis contract 含允許的 global sector rephasing，也須測其 covariance；不得在沒有 connection primitive 時擅自提升為 local rephasing。
- **P** — exact arithmetic 下逐位元；浮點／隨機情形沿用 C2 在 Freeze-2a 固定的 norm、tolerance 與 distributional protocol。
- **F** — 以嚴格不等式二分而不保留 tie 通道，會破壞全域 covariance（Stage 5B 已確立）。
- **E** — 同 C2 測試檔。

---

### C3b — Sector non-degeneracy〔依審計重寫〕

**v0.1 版本作廢。** $K_{UU}\neq K_{VV}$ 作為普遍條件是錯的：它會錯殺「sector 資訊只在 off-diagonal」的合法表示，而 diagonal 或 off-diagonal 完全取決於 §3 的 basis contract。此外 $S(f\mathbb 1)S^{-1}=f\mathbb 1$ 使 v0.1 的第二個排除式字面上冗餘；精確 $\neq$ 也會被任意小雜訊通過。

**修訂陳述.** 因為 $\{U,V\}$ 本身由 $P$ 導出，C3b **不是**「sector 帶入了額外資訊」的 information-theoretic 主張，也不能靠任意替換 $U,V$ 製造物理反事實。它是較便宜的**表示／來源 preflight**：在 object / basis contract 固定後，排除候選只是把 pure-order scalar objects 經固定 fiber matrices 抬升成 $2\times2$ 外觀，而沒有非平凡使用 realizer-derived structure。

Freeze-1a 必須在任何候選存在前定義 basis-covariant 的 **sector-blind lift space、projection／quotient construction 與 invariant-norm family**：blind space 包含所有不呼叫 sector／realizer API 的 pure-order scalar coefficient functions 與固定 fiber endomorphisms 的有限線性組合，不能只排除單一 tensor product。Freeze-2a 只能依已宣告的 object/basis contract 實例化該空間與 norm，並固定數值門檻；不得讓候選反過來選擇衡量自身非退化性的空間或 norm。

- **T** —
1. 驗證 Freeze-1a 的 sector-blind lift space、projection／quotient 與 invariant norm 涵蓋固定 endomorphisms 的有限線性組合並具 basis covariance，再依 Freeze-2a 的 object/basis contract 作無歧義實例化；
2. 以 static dependency／taint、module boundary 或 source-level proof 證明候選確實使用 realizer-derived API，且不能在內部繞過介面由 $P$ 偷偷重算後偽裝成 ablation；
3. 以登記的 invariant norm 計算 sector-sensitive 分量的相對大小；
4. 沿 §5.4 的密度序列重算，檢查**renormalized、dimensionless** sector-sensitive effect 不趨零；
5. 只有在存在合法、仍位於 domain 內的介入時才使用 C4 perturbation。任意塞入不是 $P$ realizer 的 $U,V$ 只能作 software diagnostic，不能作物理 acceptance evidence。

- **P** — Freeze-1a 的 blind-space／norm form 與 source dependency audit 通過；renormalized norm 比值 $>$ Freeze-2a 登記門檻，且在密度序列上不衰減至零（candidate-specific scaling form 與容許區間在 Freeze-2a 登記）。
- **F** — 「我們建了 two-sector kernel」，實際上是 scalar kernel 戴上 $2\times2$ 的帽子；或 sector slot 被用到但其內容與 $\{U,V\}$ 的 order 來源無關。
- **E** — blind-space 定義／basis-covariance proof + source dependency evidence + norm 表 + 密度序列曲線；合法時再附 C4 擾動對照。

**$\phi$ 的地位.** v0.1 的計數比例 $\phi$ 降級為：**僅在已宣告 diagonal chiral propagation 表示時**的**可選充分 witness**，不是通用必要條件。

---

### C4 — Information-path audit

- **T** — 產出**書面依賴圖**：對每個矩陣分量明寫
$$P\ \longrightarrow\ (\prec,\#,U,V,\text{phase})\ \longrightarrow\ K_{ab}(x,y),$$
並在建造完整 observable **之前**分析該路徑是否被代數結構吃掉：三角性、$\pm\lambda$ eigenvalue pairing、Hermitian 相消、determinant 恆等式、trace 恆等式、gauge redundancy、similarity invariance。

對每條宣稱路徑選擇下列一種**合法**驗證方式，並在 Freeze-2a 前指定：

1. 對可獨立操控的 primitive，構造只改變該上游量的 controlled perturbation；
2. 對由 $P$ 相關導出的 $U,V$ 等資料，若不存在合法獨立 perturbation，改用 symbolic dependency、static taint／module ablation、以及 domain 內的 matched-causet evidence。不得把無效 realizer 或 artificial input 當成物理反事實；
3. 若只能作 artificial software diagnostic，必須明標，且不能單獨支持物理 dependency claim。

- **P** — evidence family 在 Freeze-1a 固定，candidate-specific dependency plan 在 Freeze-2a 固定；依賴圖完整，每條宣稱路徑至少有一項 domain-valid evidence，且沒有 evaluator oracle 回流。
- **F** — 合法擾動不產生反應，或只能以 invalid/artificial input 支持物理路徑 $\Rightarrow$ 該 dependency claim 不成立；路徑為裝飾性或未證實。
- **E** — 依賴圖文件 + `tests/test_stage5c_infopath.py`。

**〔依審計修正〕擾動結果不得回頭修改 protocol。** v0.1 寫「若某路徑不起作用就刪除該路徑並更新 C8 匹配清單」——那是看完結果後改 protocol。修正為：

> 裝飾性路徑的發現**只作為報告項**。C8 baseline 由 C8.1 在 Freeze-1a 固定，**永不因 C4 的結果而縮減**。候選只能依 C8.1 的限制提議增加 nuisance covariates；新增項必須先通過 C8.1 的 provenance 與 power-preservation qualification，否則不得加入。

**為何 C4 存在.** 本專案三次失敗（單向三角行列式 $\det D_C$ 為定值、$Q_{\rm test}$ 的 $\pm\sqrt{m^2+\sigma_k^2}$ 配對固定行列式相位、$Q_{\rm test}$ 敏感性）全部是「$R$ 進不去」，且都是算完之後才發現。

---

### C5 — Causal / support condition

作用物件：由 §3 的 gate ↔ 物件表指定（通常為 $\mathcal K$、$G_R$ 或由 $W$ 導出的 causal／anticommutator object；**三者條件不同，必須分開陳述**）。

- **T** — (1) 對宣告 retarded 的物件，完整枚舉或以覆蓋率有證明的方式檢查 acausal entries 為零；(2) 驗證 object contract 對應的 inverse/composition、contact term、boundary/initial condition，或 $W$ 的 causal/anticommutator identity；(3) 報告權重相對於 Freeze-1a 已固定其選擇與形式、且僅供 evaluation 使用的 pure-order diagnostic；候選不得換 diagnostic，也禁止用座標距離回流到構造。
- **P** — support／identity evaluator 與 diagnostic form 在 Freeze-1a 固定，object-specific tolerance 在 Freeze-2a 固定；support 與 causal identity 成立，diagnostic 分布與邊界條件完整報告。
- **F** — support、composition/contact、boundary 或 anticommutator 條件失敗。**單靠 support mask 只表示通過必要的 support test，不因而自動通過或自動失敗整個候選**；其資訊是否足夠由 C4、C7、C8 決定。
- **E** — support matrix 測試 + object-specific identity residual + diagnostic 分布表。

---

### C6 — Nonlocality / boundary / scaling control

- **T** — 報告三組量及其 ensemble mean／single-causet fluctuations：(1) **influence range**——依 Freeze-1a 固定的 nested-region selector，比較 sub-region 與 full-region output；(2) **boundary dependence**——依 evaluation-only oracle 定義 bulk／boundary strata；(3) **density / region scaling**——依 §5.4 的序列。nested-region 與 strata 可使用 L4 oracle 來評估，但不得回流到候選。
- **P** — bulk stability、bias、variance／concentration 與 scaling 門檻在 Freeze-2a 登記並全部通過；報告完整 causet-level uncertainty。
- **F** — 兩項明確禁止：
  - 若結果只在固定 whole box 成立、在 domain extension／bulk limit 無穩定極限，則 FAIL。使用全域 normalization 本身不自動失敗，但其 continuum scaling 與 boundary independence 必須通過。
  - **不得**把 Hasse hop 數當成 physical locality。STATUS 已否定 Hasse/link graph diffusion 作為 continuum dimension probe。
- **E** — 三組收斂／漲落曲線 + selector/oracle manifest + causet-level uncertainty table。

---

### C7 — Massless physics contract

作用物件：由 §3 指定（$G_R$ 或 $\mathcal K$；**不得**在本 gate 內途中換物件）。Stage 5C-1 的物理條件是**兩個 massless chiral sectors 以 basis-invariant 方式解耦**；只有在 object/basis contract 已證明對應後，才可把它翻譯成特定 matrix blocks 為零。不得把 $K_{UV}=K_{VU}=0$ 當成普遍條件。

**對原 brief 的明示技術修正.** 原 brief 的 literal $K_{UV}=K_{VU}=0$ 只有在已固定、且已證明這兩個 blocks 表示 propagation mixing 的 diagonal null-sector representation 中成立。本規格的 object domain 同時允許 kinetic operator；在合法 Dirac 表示中，kinetic operator 可為 off-diagonal，若把 block-zero 當普遍條件會錯殺正確表示。因此本規格以 basis-invariant decoupling 取代 literal block-zero。若要恢復原句，必須先把 Stage 5C object contract 限縮到該特定 propagation representation；不得在目前較廣的 object domain 中直接套用。

- **T** — 依 §5.1，連續恢復必須表述為對明定 sprinkling measure 的 ensemble expectation／convergence in probability／almost-sure convergence。至少檢查：
  1. **representation-independent chiral decoupling**——criterion form 與允許的 invariant projector／commutator／intertwiner family 在 Freeze-1a 固定，object-specific instantiation 在 Freeze-2a 固定；不得只在某一組基底下看起來對角；
  2. **propagation**——回復 null 方向的傳播（$\partial_u\psi_R=0$、$\partial_v\psi_L=0$ 的兩個解耦方程）；
  3. **normalization**——歸一化常數必須在 calibration split 上定，並在 holdout 上檢驗；
  4. **single-sprinkling fluctuation control**——報告單一 sprinkling 的漲落幅度，並證明結論不依賴單一實現。
- **P** — primary observable、target、smearing 與 norm 在 Freeze-1a 固定；candidate-specific 收斂率、bias 與 fluctuation 容差在 Freeze-2a 登記。benchmark 必須先以 planted alternatives 示範能區分「兩個沿相反 null 方向的傳播」與「兩個各自對稱擴散的通道」。
- **F** — 以 per-link sealed-coordinate 一致率作為通過條件 $\Rightarrow$ 規格違反（§5.1）。
- **E** — ensemble 收斂表 + 漲落報告 + 判別力示範。

---

### C8 — Two-axis control contract〔依審計拆分〕

v0.1 只有「必須給出不同結果」一軸，審計正確指出：**單純要求結果不同會獎勵噪音**。

#### C8.1 Baseline matching protocol（Freeze-1a 固定，永不縮減）

匹配 protocol 在**任何候選存在之前**固定，候選只能在 Freeze-2a **增加合格的 nuisance covariates**、不能減少。這是對 v0.1 循環性的封堵——baseline 不得由候選自身的 dependency graph 決定。

Freeze-1a baseline 至少含：元素數 $N$、relation density（ordering fraction）、link density、height 分布、以及 interval abundance 的低階項。C8.4 的獨立交付物必須把「分布／低階項」展開為精確函數、階數、binning、距離、容差、matching algorithm、未配對處理與成功率門檻；只列名稱不構成 Freeze-1a。

baseline matching 主要作用於 Axis B 的 target pairs；Axis A 若比較固定物理區域的不同密度，$N$ 本來就不同，不得誤要求跨密度匹配 $N$。

候選在 Freeze-2a 提議的新增 covariate 必須同時滿足以下**先於候選輸出求值**的資格條件：

1. 它是從整個 causet 計算的 permutation／label-invariant **global scalar summary**，不是 local profile、指定 evaluation point／region 的 statistic，亦不是以 target 差異的空間位置為基準的量；
2. 它不得是 $K$／reported observable 的 descendant、sealed target label、L4 oracle、target-definition proxy，或看過 holdout 後才選出的量；
3. 必須在 Freeze-1a 指定的 candidate-independent covariate-qualification split 上，**不讀取任何候選輸出**地重跑 matching，且仍同時滿足既定 coverage、matched-pair、SMD、KS 與 Axis-B power floor；qualification split 揭露後即 burned，不得反覆換 split 挑到通過；
4. 若新增項解析上或在上述 qualification 中把預登記的 continuum contrast 當成 nuisance 配平、使 $L_+-L_-$ 的既定 sensitivity test 失去可執行性，該新增項判 **PROTOCOL-INVALID 並不得加入**；不得把它造成的失配記為 C8 的 INCONCLUSIVE。

只有已通過上述資格的新增項，在之後 fresh confirmatory batch 因普通抽樣變異未達 cohort conditions 時，才記 INCONCLUSIVE。這個區分封住「合法增加一個 local target proxy，主動殺掉 Axis B，再以 INCONCLUSIVE 退場」的繞道。

#### C8.2 Axis A — Universality（同一 continuum target）

- **T** — 同一 continuum target 的**不同 sprinkling 實現與不同密度**，由 Freeze-1a primary observable 所定義的物理輸出必須收斂到相同結果。
- **P** — target、norm 與 equivalence criterion 在 Freeze-1a 固定；candidate-specific bias／variance 收斂容差在 Freeze-2a 登記。
- **F** — 不收斂 $\Rightarrow$ 輸出是實現雜訊而非物理量。
- **E** — density-indexed universality curves + within-target causet-level covariance／concentration report。

#### C8.3 Axis B — Sensitivity（不同 continuum target）

- **T** — 對**外部預先知道應該不同**的 target 對，primary observable 必須依 Freeze-1a 固定的方向／關係給出差異，且超過 Axis A 所測得的 within-target 漲落。
- **P** — 差異方向／關係與 primary endpoint 在 Freeze-1a 固定；效應量與樣本數在 Freeze-2a 登記；差異必須顯著大於 Axis A 的漲落尺度。
- **F** — 分得開但差異落在 within-target 漲落內 $\Rightarrow$ 不算通過。
- **E** — matched-pair manifest + coverage／power table + between-target effect 與 Axis-A noise 的 joint report。

#### C8.4 對照組交付要求與目前狀態

審計指出 v0.1 建議的 $D=2$ vs $D=3$ 對照與 domain 衝突：若候選只定義在 order-dimension-2／$\kappa=1$，多數 $D=3$ 樣本直接 **OUT-OF-DOMAIN**，不能作為主要 discrimination pass。

同時：**KR orders vs sprinkling 太容易**（高度差 $3$ vs $\sqrt N$ 量級），不算通過。

因此需要**定義域內的困難對照**。在候選存在前設計 candidate-independent control 正是 Freeze-1a 的工作，並不構成循環；禁止的是看過候選輸出後才挑對照。該獨立交付物不得參考任何候選。

交付物至少須含：兩側 target 的 domain proof、外部預測的 primary-observable 差異與方向、C8.1 精確 matching protocol、matching coverage／OUT-OF-DOMAIN rate、Axis A/B 的 power analysis、RNG/hash manifest，以及 target metadata 不回流到 construction 的隔離測試。

candidate-independent 核心交付物現已見 `docs/STAGE5C_C8_4_HARD_CONTROLS.md`：完整
dimension-$\le2$ domain 與 $\kappa=1$ stratum 都能在固定 11 維 global-scalar
baseline 下通過足夠樣本量的 filter-then-match benchmark，且跨 seed replication
已把 raw pool 從 512 提升為 768。設計點固定後另有三個全新 out-of-sample blocks
通過全部 matching gates；先前用來選擇 768 的 blocks 只列 exploratory evidence，
不再回充為可行性證據。這解決了 matchability，但匹配前稽核亦顯示 local density
差異會洩漏進 global height／interval 統計，故 **residual discriminability 尚未確認**。
在 reference-probe 預登記完成並取得判決前，不得把 Axis-B 無差異記為候選失敗。
這些進展仍**不等於 Freeze-1a 已完成**：該文件的 continuum endpoint 尚須與 D.1 第 3 項的
basis-invariant primary observable／smearing／norm 合法對接，並與第 6 項的全域
multiplicity rule 一起在單一 freeze commit 固定。此前 C8 仍不得執行 confirmatory
evaluation，Stage 5C-1 仍不得宣告通過。

---

### C9 — Quantum contract〔依審計改為兩層〕

**v0.1 的理由作廢並更正。** v0.1 以「$\gamma^\mu$ 被 C0 禁止」為由刪除協變分解 $S(p)=\not p\,S_1+\mathbb 1S_2$，**此推理不成立**：C0 禁止的是 $\gamma^\mu$ 作為 **construction input**，不禁止外部 continuum evaluator 使用 Clifford notation——C7 本來就在使用連續微分結構。evaluator 的 Clifford 用法依 §3 列為 **L4 evaluation oracle** 即可。

同時，裸的 $\rho_{ab}(\mu^2)\succeq0$ 也**不是**完整條件：它已預設 Wightman object 與 adjoint/pairing、Hilbert-space positivity、translation invariance 與 positive-energy spectral support、可只用 $\mu^2$ 參數化、以及 null sectors 已可識別為 fermionic components——這些全都必須先在 §3 宣告。

#### C9.1 Layer 1 — finite causet

- **T** — 先確認 $W$ 依 §3 由同一候選的 $\mathcal K/G_R$ 導出。對宣告的**完整** finite-dimensional test-function space（或以明定 projector 選出的完整物理子空間）建立 Gram/operator matrix，驗證 Hermiticity 與 smeared quadratic-form positivity。使用全譜 eigenvalue、具 residual bound 的 factorization 或等價的完整證明；隨機 test functions 只能作 regression，不能作 acceptance proof。
- **P** — 完整 test-function space／projector 與 acceptance-criterion form 在 Freeze-1b 固定；Hermiticity residual 與最小 eigenvalue／factorization residual 在 Freeze-2b 的 scale-aware tolerance 內；若 CAR 對該 covariance 要求 complementary bound，須一併通過。
- **F** — 完整允許子空間出現超過 tolerance 的負模，或只以抽樣未見負值就宣稱 positivity。
- **E** — test-space/projector 宣告 + 全譜／factorization residual 表 + 隨機 regression 對照。

#### C9.2 Layer 2 — continuum evaluator

- **T** — **只有在由同一 $W$ 導出 spectral representation 之後**才執行，逐項檢查：

1. spectral support；
2. positivity 條件（含**不同 spectral components 之間的不等式**，非單一矩陣 PSD）；
3. residue 與 **CAR / equal-time anticommutator normalization**；
4. sum rules；
5. poles / branches 與完整 analytic stability（比照 Track B Stage 2 的 argument principle 作法，**含 planted-zero 對照**以確保計數器非恆回 0）；
6. **以獨立表示交叉驗證**（交叉驗證必須真正獨立——本專案曾出現循環測試：比較 $A$ 與 $B$，而 $B$ 在該區的定義就是由 $A$ 反推）。兩條 pipeline 的結構性獨立要求與 planted-failure family 在 Freeze-1b 固定；實際 pipeline、共同依賴與 mapping 在 Freeze-2b 明列。

- **P** — spectral support、positivity/CAR/sum-rule 與 analytic-stability criteria 的形式在 Freeze-1b 固定；candidate-specific representation mapping、numerical tolerances 與 independent-pipeline implementation 在 Freeze-2b 登記並全部通過。
- **F** — 取矩陣某個對角元檢查正性即宣稱 positivity 成立 $\Rightarrow$ 不算通過。
- **E** — spectral 報告 + 零點計數 + 獨立交叉驗證。

#### C9.3 文獻使用限定〔v0.4 補 equation mapping 與適用域〕

- **Potting, arXiv:1112.5739 (PRD 85, 045033)**：Eq. (26) 是含常數背景 $c^{\mu\nu}$ 的 fermion–scalar model；Eqs. (29)–(31) 定義 spectral matrix 與依賴 $p\!\cdot\!c^k\!\cdot\!p$ 的多重 spectral functions；Eq. (37) 給 Feynman propagator；Eqs. (46)–(49) 給 positivity 與 spectral-component inequalities；Eqs. (50)–(54) 由 canonical anticommutator 導出 normalization／sum rules。**可引用的是結構性教訓**：fermionic viability 不等於單一矩陣 PSD，還需要 component inequalities 與 normalization/sum-rule chain。
  **作用域警告**：上述 model 是 SME 型常數背景 LV 理論；LV-dependent decomposition／sum rules 不得直接移植成驗收公式。本專案只允許在完成 object、signature、dimension、adjoint 與 convention mapping 後，把文中 $c^{\mu\nu}\to0$ 的 conventional Lorentz-invariant reduction 作 secondary cross-check：Eq. (47) 在此極限給 $\rho_1\ge0$，Eq. (49) 給 $\rho_1\ge |\rho_0|/\sqrt{s}$。這兩式不能當本專案公式的來源或 construction input。
  **Clifford-basis 限定**：Eq. (30) 的結構基底在該文的 $\mathcal P/\mathcal{PT}$ 真空假設下刻意排除 $\gamma^5$、$\sigma^{\mu\nu}$ 與 $\gamma^5\gamma^\mu$。Stage 5C 的離散 $\{U,V\}$ 在 C7 通過前仍只稱 candidate precursor；但其外部 1+1D chiral target 以 $(1\pm\gamma^5)/2$ 表示。故 Eq. (30) 的 tensor basis 排除了本專案 continuum target 的核心 chiral structure，**不得移植**為 C9 的分解完備性假設。
- **Noldus, arXiv:1305.0443**：目前只作非承重的動機性引用——該 causal-set free-fermion construction 出現 mixed-norm／negative-norm ghost 問題，支持另設 fermionic viability gate。若未來用它決定公式、prescription 或 threshold，必須另建 equation／convention mapping。

#### C9.4 不得預設答案

BBMM 指出 $d>2$ 時這類 causal-set-derived operator 的譜函數非正定；ASS 指出 minimal 4D operator 有兩個 unstable zeros。Stage 5C 不得預設 fermionic 版本會通過或會失敗——**算出什麼記什麼**。

---

### C10 — Mixing contract〔v0.1 缺可執行段，此處補齊〕

**前置條件**：C7 與 C9 **都** PASS。不得提前。

#### C10.1 Mass-source taxonomy 與 evidence axes

必須先宣告 mass-like quantity 的**來源**；不得把 explicit deformation 說成 emergence：

| 來源 | 允許主張 |
| :--- | :--- |
| **E1 explicit** | 外加的 mass／mixing deformation；可測 massive consistency，但不得稱湧現 |
| **E2 order-derived effective** | mass scale／mixing rule 由允許的 order data 導出，須通過 C0/C4 與 units/scaling audit |
| **E3 dynamical/spontaneous** | 由明定 dynamics/state 產生，須另給 order parameter、phase structure 與非手工選定的 vacuum/state 論證 |

證據另分四軸，不能與來源混成單一階梯：massive propagation／dispersion、massless limit、units/scaling、post-mixing quantum viability。每一軸各自 PASS/FAIL。

#### C10.2 驗收

- **T** —
  1. **massive benchmark**：與已知 1+1D massive Dirac propagation 比對（ensemble 陳述，同 §5.1）；
  2. **massless limit**：沿 basis contract 所定義的 zero-mixing family 必須連續回到 C7 的結果，且不得重新校準。若 E2/E3 的 mass-like quantity 不可直接調，須在 Freeze-2c 指定可操作的 ensemble／deformation path；不能只寫形式上的 $m\to0$；
  3. **units / scaling**：mass-like quantity 對 $\rho$、nonlocality scale、L3 參數的依賴必須明寫。E1 可保留為 explicit deformation；若只是一個自由校準常數，則 E2/E3 emergence claim FAIL；
  4. **post-mixing revalidation**：加入 representation-independent mixing 後，逐項重跑 **C0、C1、C2、C3、C3b、C4、C5、C6、C8、C9**；C7 則在 zero-mixing member 重驗 massless recovery，並由本 gate 的 massive benchmark 驗證非零 mixing。mixing rule、mass scale 或 state 改變均須重新進 C0 ledger/capacity audit；C3b 必須在 mixing 後重新檢查 blind-space quotient，不能讓 mixing 把 sector-blind lift 偽裝成 sector-sensitive。若 basis contract 將 mixing 放在特定 blocks，可使用該表示，但不得把 off-diagonal 當普遍定義。
- **P** — massive target、dispersion relation、primary observable、smearing 與 norm 在 Freeze-1c 固定；candidate-specific effect、scaling、massless-path 與 quantum tolerances 在 Freeze-2c 登記並全部通過。
- **F** — 外加 $m$ 或 mixing matrix 本身不使 E1 失格；但把 E1 重新命名為 E2/E3「質量湧現」，或在 nonzero mixing 上誤套原 massless-decoupling PASS，均判 FAIL。
- **E** — massive benchmark 表 + zero-mixing 極限曲線 + C0／C1／C2／C3／C3b／C4／C5／C6／C8／C9 逐項 revalidation report + zero-mixing C7 regression。

#### C10.3 解讀上限

STATUS 已否定「質量 = 客觀轉向頻率／次數」與「checkerboard zigzag = 真實電子軌跡」。C10 若產生任何 mass-like 量，其解讀**不得**回到這兩條。

#### C10.4 為何順序不只是流程

null 座標下無質量 Dirac 是兩個**解耦**方程，質量項正是耦合兩者的那一項。先驗證解耦極限、再開耦合，對應的是方程結構本身。

---

### C11 — 4D / output firewall〔依審計擴大到輸出端〕

**全程有效**，非階段性。

#### C11.1 兩條獨立的不可外推理由

1. $\mathbb R^{1,1}$ 的 timelike posets **恰好**是 order-dimension-2 的（Stanley）；$n\ge2$ 變成 sphere orders，無同樣簡單的兩線性序表示。**整個 Stage 5A/5B/5C 的 realizer 機器只在這裡成立。**
2. 即使 3+1D Minkowski 中 spinor bundle 本身可平凡化，Weyl/Dirac 的物理內容仍來自 **local Lorentz / Clifford representation structure**；一對 global null total orders 不能直接提供這個局部結構。

**措辭警告.** 障礙**不是**「4D spinor 叢一般不平凡」——那是叢的拓樸問題，真正的障礙是表示論問題。兩者不同層次，混用會讓外推看起來只差一步。

#### C11.2 輸出端約束〔審計新增〕

firewall 不只限制構造，也限制**每一份輸出**：

- Stage 5C 產生的每一條 STATUS 結論列，標題或分類欄必須帶 **1+1D** 限定詞（比照 Stage 4 對 $d_s$ 的處理）。
- README、abstract、commit message、PR 描述同樣受限。
- 逐項標示哪些步驟依賴 1+1D 的兩個 global null total orders。

- **T** — 對全部輸出文字做 checklist 審查。
- **P** — 無任何未限定的 4D 或 spinor 陳述。
- **F** — 1+1D 成功被讀成「已得到 spinor precursor」。
- **E** — firewall checklist。

---

## 7. 分階段 gating

| 階段 | 內容 | 通過條件 |
| :--- | :--- | :--- |
| **Freeze-1a** | 本規格基線 + C3b/C5/C6/C7/C8 candidate-independent evaluator forms + C8.4 controls + 全域 confirmatory ledger/budget | 附錄 D.1 九項在單一 freeze commit 中完成、並引用本規格 commit 後生效；完成前不得設計候選 |
| **Freeze-2a** | 候選 $K$、object/basis、C0–C8（含 C3b）instantiation 與門檻 | 接觸 fresh holdout A 前完成 |
| **Stage 5C-1** | Massless feasibility；basis-invariant chiral decoupling | C0–C8（含 C3b）全部 PASS |
| **Freeze-1b / 2b** | C9 evaluator form / 同一候選的 quantum instantiation | 5C-1 PASS 後、接觸 fresh holdout B 前完成 |
| **Stage 5C-2** | Quantum viability | C9 PASS |
| **Freeze-1c / 2c** | C10 massive evaluator form / mixing instantiation | 5C-2 PASS 後、接觸 fresh holdout C 前完成 |
| **Stage 5C-3** | Mass mixing | C10 PASS；依 C10.2 逐項重驗 C0、C1、C2、C3、C3b、C4、C5、C6、C8、C9，並在 zero-mixing member 重驗 C7 |
| **C11** | 4D / output firewall | 全程有效 |

任一階段非 PASS 即停在該處並依 §2 的判決分類封存，**不得**跳過或放寬條件續行。

**附錄 D 的 Freeze-1a 項目未完成前，Stage 5C-1 不得開始 confirmatory evaluation，更不得宣告通過。Freeze-1b/1c 未完成只阻塞各自的後續階段，不追溯阻塞 5C-1。**

---

## 8. 交付物與 source-of-record

沿用既有紀律：

1. **source-of-record** = `analysis/stage5c_*.py` 的 `__main__` 印出的表。文件引用的數字必須來自執行該檔案。
2. **各 benchmark 區塊使用獨立 RNG stream。** 共用 RNG 會讓新增一列 silently 改掉既有表格（已發生過）。
3. **fail loudly，不要 silent skip.** 數學上不可能的情況用 `assert` 而非 `continue`。enumeration cap 必須拋出並記為 INCONCLUSIVE。
4. **交叉驗證必須真正獨立.** 禁止循環測試與 evaluator floor 假象。
5. **`verify_integrity.py` 在 CI 的 pytest 之前執行。** `mergeable=true` 與檔案完整性、CI 綠燈無關。
6. **來源歸屬.** 本專案導出的結果與原文陳述分開標記；不自行發明 regularization / prescription；跨論文使用前先建 mapping，不得預設係數值。
7. **版本核對.** 宣告「某檔案不存在」前，先用 GitHub API / raw / tarball 重抓 main HEAD 確認。
8. **confirmatory source-of-record.** `docs/stage5c_confirmatory_ledger.md` 是所有 candidate version、holdout batch 與全域 error/evidence budget 的唯一帳本；analysis 輸出與 dossier 必須引用相同 attempt id。

每個候選對應一份 `docs/stage5c_dossier_<id>.md`，含 §3 物件契約、§4 ledger、Freeze-2a/2b/2c 記錄、每個 gate 的四欄結果，以及 confirmatory ledger attempt id。

---

## 9. 結果語意〔依審計收窄〕

### 9.1 PASS 的意義

若 Stage 5C-1 全部 PASS：得到的是「在 1+1D，某個明定的候選 $K$ 僅由 order + number + 受限相位 + sector pair 建立非局域雙通道 kernel，其 ensemble 連續極限回復 massless Dirac 傳播」。

這是**限定於 1+1D、限定於該候選**的正面結果。依 §1.2 不授權任何 spinor / chirality / 4D 陳述。

### 9.2 FAIL 的意義〔v0.1 過強，此處更正〕

v0.1 寫「若所有合理的 fermionic 結構都無法取得足夠的 Clifford / chiral 資訊，那會是有價值的 No-Go」——**這個推論不成立**。

本規格能做的是**拒絕某個候選，或拒絕某個明定的候選類**。在沒有 completeness theorem、也沒有封閉的搜尋類的情況下，**不得**從「候選失敗」推出「所有合理 fermionic structures 失敗」。

這與 Stage 5B 已經修正過的同型錯誤是同一類：5B 曾寫成「任何 order+number construction 必然 nonlocal」，後已撤回為限定陳述。同樣的紀律適用於此。

因此正確的 FAIL 語意是：

> 候選 $\mathcal A$（或明定候選類 $\mathcal A^*$）在 gate $C_k$ 上 FAIL，原因為 $R$。此結果**不**主張其他候選必然失敗。

若累積足夠多的候選類 FAIL 且能證明其涵蓋範圍，才可能升格為結構性結論——那需要另一份文件與另一套論證。

### 9.3 INCONCLUSIVE／PROTOCOL-INVALID 的意義

計算上限或已凍結 evaluator 的技術缺失屬 INCONCLUSIVE，**既非 PASS 亦非物理 No-Go**。若 object/evaluator/threshold/split 根本未依 freeze 完成，則是 PROTOCOL-INVALID：不得執行或解讀結果，不能用 INCONCLUSIVE 掩蓋規格未完成。

### 9.4 BOUNDED-SEARCH-EXHAUSTED 與 SPEC-INFEASIBLE 的意義〔v0.6 重寫，v0.7 修正型別，v0.8 更新現況〕

附錄 D 的 Freeze-1x 交付物有可能經認真嘗試後仍無法構造。D.1 第 5 項原本是主要例子；v0.8 已有完整 dimension-$\le2$ 與 $\kappa=1$ 的 candidate-independent control family，故該項的「對照族不存在」風險已解除。現存風險是 D.1 第 3 項能否把其 continuum endpoint 合法對接到 basis-invariant primary observable／smearing／norm。下列兩種狀態仍適用於此項及其他 Freeze deliverables。

**這不是候選的失敗，也不是流程卡關。** 但 v0.5 在此犯了與 §9.2 同一型、只是高一層的錯誤：從「某個有限嘗試類找不到」直接推到「規格前提不可行」。v0.6 分成兩級。

**型別提醒（v0.7）**：兩者都是 §2.1 的 **Freeze-deliverable status**，不是 gate verdict。依賴該交付物的 gate 記為 `INCONCLUSIVE(reason=BOUNDED-SEARCH-EXHAUSTED)`；`SPEC-INFEASIBLE` 永不作為 gate verdict 出現。

#### 9.4.1 BOUNDED-SEARCH-EXHAUSTED（預設落點）

在明定的構造類 $\mathcal G$ 內窮盡搜尋而未找到，即記為此狀態。宣告需要：

1. $\mathcal G$ 的精確定義（構造家族、參數範圍、可用材料）；
2. 該類內窮盡性的說明——完全枚舉、或有界搜尋並指明界在哪、以及所耗資源；
3. 指出放寬**哪一項前提**（定義域、matching protocol、外部已知差異的來源）可能使其變可行。

**結論模板：**

> 在定義域 $\mathcal D$、matching protocol $\mathcal M$ 與構造類 $\mathcal G$ 之下，窮盡搜尋未找到滿足 C8.3 的 in-domain target pair；搜尋界為 $B$。此結果**不**主張 $\mathcal G$ 之外不存在，亦不主張其他 $\mathcal D$ 或 $\mathcal M$ 下不存在。

#### 9.4.2 SPEC-INFEASIBLE（需 completeness）

只有在**額外**證明 $\mathcal G$ 對全部 admissible constructions 具 **completeness**——即任何合乎規格的對照必落在 $\mathcal G$ 內——時，才可升格為 SPEC-INFEASIBLE。缺此論證一律停在 9.4.1。

**結論模板：**

> 在定義域 $\mathcal D$ 與 matching protocol $\mathcal M$ 之下，$\mathcal G$ 涵蓋全部 admissible controls（completeness 論證為 $R_1$），且 $\mathcal G$ 內不存在滿足 C8.3 的 target pair（論證為 $R_2$）。此結果**不**主張在其他 $\mathcal D$ 或 $\mathcal M$ 下亦不存在。

#### 9.4.3 兩者共通的後續紀律

無論落在哪一格，正當的後續都是**修改規格前提並版本化**（放寬定義域、改變 matching protocol、或承認 C8 需要不同形式的 sensitivity 證據），而不是降低 C8 的門檻讓現有對照勉強通過。前者誠實，後者就是本專案已經反覆付過代價的那種失效。

兩者都必須進 STATUS，且都不得記為候選 FAIL、不得包裝成單純的技術性 INCONCLUSIVE。

---

## 附錄 A — 審計 findings 的處置對照

| 審計 finding | v0.3 狀態 |
| :--- | :--- |
| C3b 公式錯誤（錯殺 off-diagonal 表示、冗餘排除式、精確 $\neq$、正比例不保證 continuum 存活、syntactic 使用） | **全部接受**；v0.3 再補 blind lift space、有限線性組合、source dependency 與「derived sector 不能任意獨立擾動」限定；$\phi$ 只作可選 witness |
| §2.1 過強 | **接受**，收窄為只約束 continuum recovery claim；補 active re-embedding vs passive diffeomorphism 區分（§5.1） |
| C9 以 C0 為由刪除協變分解，邏輯不成立 | **接受並更正**，evaluator 的 Clifford 用法列為 L4 oracle（§3） |
| 裸 $\rho_{ab}\succeq0$ 預設過多且不完整 | **接受**，C9 改兩層 + 列出全部預設為 §3 宣告項 |
| Object contract 缺失 | **接受**，新增 §3 型別鏈 + gate↔物件對照表 |
| C0 ledger 太粗 / unrestricted phase | **接受**，五分類 ledger（§4）+ 相位／RNG 規則（§4.1）+ L3 capacity/source audit（§4.2） |
| C0 conditional loophole | **接受**，新增 CONDITIONAL-FORK 判決 = S5C-Claim FAIL（§2） |
| C1 未處理 $\dim>2$、cap、verdict 分類 | **接受**，C1 四情形表 + $N\ge40$ 降為 pilot floor |
| C4/C8 循環 | **接受**，v0.3 將 C8.1 matching protocol 於單體 Freeze-1 固定且**永不縮減**；v0.4 對應為 Freeze-1a；C4 的裝飾性路徑發現只作報告項 |
| C8 應拆兩軸 | **接受**，Axis A universality / Axis B sensitivity，B 的差異須超過 A 的 within-target 漲落 |
| $D=2$ vs $D=3$ 對照與 domain 衝突 | **接受**，列為 C8.4 **blocking open item**；v0.3 明列 control 交付物最低內容 |
| 缺 calibration/holdout、stop rule、獨立單位；§2.2 不實際 | **接受**，兩次 freeze（§5.2）+ holdout batch burned/fresh 規則 + split stop-rule discipline |
| C10 無可執行驗收 | **接受**，補 mass-source taxonomy + 四 evidence axes + massive benchmark + massless path + post-mixing revalidation |
| v0.1 No-Go 過強 | **接受**，§9.2 收窄為拒絕候選／候選類 |
| v0.1 第 205 行把候選方向放回 evaluator 段 | **接受**，C5 改為不具名 evaluation-only diagnostic；§0 同時釐清 candidate-independent freeze 的 matching covariates 可為可執行性而具名，但不得作候選推薦 |
| 每條需 test/threshold/failure/evidence 四欄 | **接受**，§6 全面採用 |
| 文獻引用 | **限定完成**：C9.3 補 Potting Eqs. (26)、(29)–(31)、(37)、(46)–(54) mapping、LV scope 與 $c^{\mu\nu}\to0$ secondary-cross-check 邊界；Noldus 維持非承重動機引用 |

## 附錄 B — v0.2 第二輪 review 的新增處置

| v0.2 殘留問題 | v0.3 處置 |
| :--- | :--- |
| $W$ 可與候選脫鉤、缺 gate-object mapping 被誤判 INCONCLUSIVE | 強制 $\mathcal K/G_R\to W\to\rho$ 導出鏈；新增 PROTOCOL-INVALID |
| C7 又寫回 $K_{UV}=K_{VU}=0$ | 改為 basis-invariant chiral decoupling；block-zero 只可作已證明表示下的翻譯 |
| finite-causet positivity 只抽樣 test functions | 改為完整允許子空間的全譜／factorization + residual bound |
| C3b 單一 tensor-product 漏洞與 C4 invalid counterfactual | blind lift space 納入固定 endomorphism 有限線性組合；derived data 只接受 domain-valid evidence |
| 同一 holdout 可在重新 Freeze-2 後再用 | v0.3 已規定 holdout 揭露即 burned；v0.4 分流為 Freeze-2a/2b/2c，修改後必須 fresh independent batch |
| phase seed 與 L3 零參數複雜規則可偷渡容量 | seed 不得挑選；結論對 phase ensemble；L3 加 function/source/capacity audit |
| C8 baseline 名稱不夠可執行、Axis A/B 適用範圍未分 | C8.1 要求精確函數、binning、距離、容差、algorithm；matching 主要限 Axis B |
| C10 把 mass 來源與證據混成 M1–M4 | 分為 E1 explicit／E2 order-derived／E3 dynamical 與四個獨立 evidence axes |
| 內部 §7.4／§9.3 等與頂層章號衝突 | 統一改為 C8.4／C9.3／C10.x／C11.x |

## 附錄 C — v0.3 review 的新增處置

| v0.3 殘留問題 | v0.4 處置 |
| :--- | :--- |
| C3b blind space 與 invariant norm form 留在 Freeze-2，允許候選自訂退化性尺度 | **接受**；form 移至 Freeze-1a，Freeze-2a 只允許 object-specific instantiation 與數值門檻 |
| 單體 Freeze-1 與附錄內容不一致，且 C9/C10 會阻塞 5C-1 | **接受**；拆為 Freeze-1a/2a、1b/2b、1c/2c，分別在 5C-1/2/3 前生效 |
| C10 post-mixing 漏重驗 C0、C1、C3b，且 `C2–C6` 對 C3b 有語法歧義 | **接受**；改為 C0、C1、C2、C3、C3b、C4、C5、C6、C8、C9 逐項列舉 |
| nearest-neighbour 違規被記為純 FAIL | **接受**；改為 CONDITIONAL-FORK，因此 S5C-Claim FAIL，但可保存為另一 conditional project |
| C5 diagnostic form 被留到 Freeze-2 | **接受**；選擇與形式移至 Freeze-1a，候選不得事後更換 |
| burned holdout 沒有封住跨 batch／跨版本無限嘗試 | **接受**；新增全域 confirmatory ledger 與 Freeze-1a 預先固定的 attempt cap 或 family-wise $\alpha$/e-value spending rule |
| Potting 的 conventional-limit 內容未寫明 | **接受**；明列 Eq. (47) 的 $\rho_1\ge0$ 與 Eq. (49) 的 $\rho_1\ge\lvert\rho_0\rvert/\sqrt{s}$ |
| Potting Eq. (30) 的 Clifford basis 與本專案 chiral target 不相容 | **接受**；明列其 $\mathcal P/\mathcal{PT}$ 假設排除 $\gamma^5$、$\sigma^{\mu\nu}$、$\gamma^5\gamma^\mu$，不得移植為分解完備性假設 |
| C7 對原 brief 的 literal block-zero 有未揭露偏離 | **明示保留技術修正**；basis-invariant decoupling 適用於目前較廣的 object domain。恢復 literal block-zero 必須先限縮為特定 diagonal propagation representation |

## 附錄 D — v0.4 尚未完成的 staged-freeze 項目

### D.1 Freeze-1a blockers（阻塞候選設計與 Stage 5C-1）

1. **C3b evaluator form**：sector-blind lift space、projection／quotient construction、basis-covariant invariant-norm family。
2. **C5 diagnostic form**：明定 evaluation-only pure-order diagnostic 的選擇、定義與不回流測試。
3. **C6/C7/C8 evaluator contract**：nested-region／boundary selectors、primary observable、massless target、smearing、norm、planted alternatives。
4. **C8.1 exact matching protocol**：低階項、binning、距離、容差、matching algorithm、未配對處理、coverage threshold。
5. **C8.4 domain-internal difficult controls**：domain proof、外部預測差異、power analysis、RNG/hash manifest。candidate-independent 可構造性與跨 seed matching 已交付於 `docs/STAGE5C_C8_4_HARD_CONTROLS.md`；仍須與第 3、6 項在單一 freeze commit 對接後才算 DELIVERED。
6. **全域 confirmatory control**：`docs/stage5c_confirmatory_ledger.md` schema、attempt id 規則，以及跨 candidate version／batch／stage 的 attempt cap 或 family-wise $\alpha$/e-value spending rule。
7. **C9/C10 immutable core 與反繞道規則**〔v0.6 新增，v0.7 擴充〕：依 §5.2.1(i)，C9 與 C10 的**判準本身**必須在此固定並凍結。另依 §5.2.1(iii)，兩類能使 core 失效的自由度一併固定：
   - **(iii-a)** 任何能使 core criterion 失效的容差，其**形式與上界規則**；
   - **(iii-b)** admissible test-space／projector 的**形式**、coverage／completeness 規則、**允許排除模態的條件**、mapping-equivalence 判準、pipeline-independence 判準。

   1b/1c 只保留實例化。**core 或上述任一規則未凍結，即視為 Freeze-1a 未完成。**
8. **外部依據路徑聲明**〔v0.6 新增，v0.7 更名〕：v0.6 把此項寫成「mapping」，但正文同時允許不做 mapping 而改走數學必要條件／STATUS 路徑，使它同時是 blocker 又是可選項。v0.7 改為**聲明**，二擇一即完成：
   - **路徑 A（不承重文獻）**：聲明 Freeze-1a 的 core criteria 全部僅由數學必要條件與既有 STATUS 結論論證，不引用任何外部文獻決定其內容或門檻形式。
   - **路徑 B（完成 mapping）**：對所引用的每一篇（Potting／Noldus／BBMM／ASS 等）完成並記錄 equation／dimension／signature／adjoint／convention mapping，取得承重資格。

   **未作出聲明**才是 PENDING。依 §5.2.1(v)，在 mapping 完成前這些文獻一律只有動機性資格。路徑一經聲明即凍結；事後改採路徑 B 屬 protocol amendment，須進 amendment ledger。
9. **兩本帳的 schema**〔v0.6 新增〕：`docs/stage5c_development_log.md`（append-only、事後登記、不佔統計預算）與 `docs/stage5c_protocol_amendment_log.md`（implementation 修改紀錄、不佔統計預算），與第 6 項的 confirmatory ledger 三者分離，職責不得混用。

本規格 v0.8 已定稿；但九項交付物全部完成、在單一 freeze commit 中固定並引用本規格定稿 commit 前，Freeze-1a 仍為 **PENDING**，不得開始候選設計或 Stage 5C-1 confirmatory evaluation。

**風險註記.** 第 5 項原先的「對照族能否構造」風險已由獨立交付物解除；目前其最高實質存活風險移到第 3 項：evaluation-only $L_\theta$ 能否合法下降為同一個 basis-invariant primary observable／smearing／norm。若此 mapping 失敗，必須在候選存在前版本化修改或撤回 control，不得硬接，也不得降低 C8 門檻。

### D.2 Freeze-1b deferred items（只阻塞 Stage 5C-2）

1. C9 finite test-function space／projector 的**實例化**——依 object contract 在 Freeze-1a 已固定的形式、coverage/completeness 規則與排除條件之下具體構造（§5.2.1(iii-b)）。**形式與規則本身不在此項**。
2. spectral support、positivity-component、CAR/sum-rule、analytic-stability 判準的**數值與具體對應表**。**判準本身屬 Freeze-1a immutable core**（§5.2.1(i)），此處不得放寬、刪除或替換。
3. independent-pipeline 的**具體架構**與 planted-failure family 的**實例**。**independence 判準本身已在 Freeze-1a 固定**（§5.2.1(iii-b) 第 5 點）。

### D.3 Freeze-1c deferred items（只阻塞 Stage 5C-3）

1. massive target／dispersion relation。
2. primary observable、smearing、norm 與 evaluator form。

Freeze-1b/1c 可在前一階段 PASS 後完成；它們不得追溯修改 Freeze-1a、既有 $K$ 或已 burned 的資料。
以上 D.2／D.3 各項均**只屬 implementation layer**（§5.2.1(ii)）——「怎麼量」，而非「什麼必須為真」。對應的 core criteria 已於 Freeze-1a 凍結（D.1 第 7 項），1b/1c 不得放寬、刪除或替換之。每次修改須進 protocol-amendment ledger（不佔統計預算），且只許以承重級外部依據或數學必要條件論證，不得援引候選的實際輸出（§5.2.1(v)、(vi)）。

---

## 附錄 E — v0.4 review 的新增處置〔v0.5；部分條目已被 v0.6／v0.7 取代，見各列註記〕

| v0.4 殘留問題 | v0.5 處置 |
| :--- | :--- |
| 分階段 freeze 使 Freeze-1b/1c 的 candidate-independence 只剩名義（撰寫時候選已存在且已跑完 C0–C8） | v0.5 以 provisional 草稿 + 消耗 budget 處理，**已於 v0.6 作廢並重寫**（見附錄 F 第 1、2 項）；external-justification-only 規則保留並於 v0.6 收緊為兩級 |
| 無判決可容納「Freeze-1x 交付物證明做不出來」，特別是 C8.4 | 新增 **SPEC-INFEASIBLE** 判決（§2）與 §9.4：界定它是關於規格前提的結果而非候選 FAIL 或流程卡關；規定三項宣告條件（構造類界定、不可能論證、指出放寬哪一項前提）；語意依 §9.2 同一紀律收窄；明禁以降低 C8 門檻繞過；**已於 v0.6 修正：拆為 BOUNDED-SEARCH-EXHAUSTED 與 SPEC-INFEASIBLE，並於 v0.7 移出 gate verdict 表，見附錄 F 第 3 項、附錄 G 第 2 項** |
| 全域 attempt budget 只寫了反面，未寫 exploratory 是否計入 | §5.3 補正面規則：calibration／development split 上的探索不限次數、不佔預算、不需登記；只有揭露 fresh holdout 的 confirmatory attempt 計入。並說明設計意圖是把工作推到 calibration 側，以及單向紀律（exploratory 可決定要不要做 confirmatory，永不可充當 confirmatory evidence）；**已於 v0.6 修正：exploratory 仍須進 development log，見附錄 F 第 4 項** |
| `C0–C4`、`C0–C8` 等區間未標注是否含 C3b（與 v0.4 已在 C10.2 修掉的缺陷同類） | 全文統一標注（§4.1、§5.2 表、§7 表）；C10.2 與 §7 的重驗清單維持逐項列舉 |

v0.5 未改動任何 v0.4 已通過的實質條款。其中第 1、2 項的處置方式已於 v0.6 作廢重寫，第 3 項已收緊，第 4 項維持。

---

## 附錄 F — v0.5 review 的新增處置〔v0.6〕

| v0.5 阻塞問題 | v0.6 處置 |
| :--- | :--- |
| **1. attempt budget 自相矛盾**：§5.2.1 說修改 provisional 1b/1c 消耗 attempt budget，§5.3 說只有 holdout revelation 消耗 | **接受**。統計預算**只**由 holdout revelation 消耗；另設 `docs/stage5c_protocol_amendment_log.md`（§5.2.1(vi)）記錄 implementation 修改，**不佔統計預算**。並補說明：移除預算成本後，嚇阻力改由可稽核性承擔——core 已凍結故修改不威脅統計效力，但反覆修改的模式是 tailoring 信號，須留痕供 review |
| **2. provisional drafting 未封住循環**：可粗糙、可預期修改 $\Rightarrow$ 核心判準仍可能看過候選後調整 | **接受，v0.5 方案作廢**。改為兩層切分：**immutable core**（C9/C10 的判準本身）於 Freeze-1a 凍結、事後不可放寬刪除替換（§5.2.1(i)，列為 D.1 第 7 項）；**implementation layer**（test space、mapping、pipeline、容差數值）才留 1b/1c（§5.2.1(ii)）。若某條 core 確實無法在 Freeze-1a 決定，須由**看不到候選輸出的獨立 reviewer** 制定並記錄 blinding 條件（§5.2.1(iv)）。**另補 GPT 未提及的一項**：容差名義屬 implementation，但夠鬆的容差等同刪除 criterion，故任何能使 core 失效的容差，其**形式與上界規則**必須一併在 Freeze-1a 固定（§5.2.1(iii)） |
| **3. SPEC-INFEASIBLE 作用域過寬** | **接受**。這是 §9.2 同一型錯誤高一層的版本——v0.5 從「某有限嘗試類找不到」推到「規格前提不可行」。拆為 **BOUNDED-SEARCH-EXHAUSTED**（INCONCLUSIVE 子型，預設落點）與 **SPEC-INFEASIBLE**（須另證 $\mathcal G$ 對全部 admissible constructions 的 completeness）。§2 加列兩格；§9.4 重寫為 9.4.1／9.4.2／9.4.3，兩個結論模板均帶構造類 $\mathcal G$ 與搜尋界 $B$ |
| **4. exploratory「不需登記」過寬** | **接受**。改為：不進 confirmatory ledger、不佔統計預算、無須事前登記，**但必須進** `docs/stage5c_development_log.md`，記錄 candidate id／source hash、data split、決策紀錄（§5.3）。並以對照表固定兩本帳的差別（事後 append-only vs 揭露前事前登記），保持探索低成本而不犧牲 C0 provenance 與可重現性 |
| **5. external justification 與 C9.3 衝突** | **接受**。外部依據分兩級（§5.2.1(v)）：**承重級**須先完成 equation／dimension／signature／adjoint／convention mapping，方可決定 criteria、公式、prescription 或門檻形式；**動機性**只能論證「該設這道 gate」。依 C9.3 現況，Noldus 為動機性、BBMM/ASS 為 $d>2$／4D 結果未完成 dimension mapping 故同為動機性、Potting 僅 $c^{\mu\nu}\to0$ reduction 可作 secondary cross-check。**直接後果：目前無任何外部文獻具承重資格**，故 Freeze-1a 的 core 目前只能由數學必要條件與既有 STATUS 結論論證；欲改變此狀況須完成 mapping，已列為 D.1 第 8 項 |
| **6.（非阻塞）D.1 稱 C8.4 為「唯一」有不可構造風險** | **接受**，改為「**目前辨識出的最高風險項**（不排除其他項亦有風險）」，§9.4 開頭同步 |

**Freeze-1a blocker 由六項增為九項**（新增第 7 項 C9/C10 immutable core、第 8 項外部文獻 mapping、第 9 項兩本新帳的 schema）。v0.6 未放寬任何 gate。

---

## 附錄 G — v0.6 review 的新增處置〔v0.7〕

| v0.6 問題 | v0.7 處置 |
| :--- | :--- |
| **1.（阻塞）implementation 仍能吞掉 core**：test-space、projector、mapping、pipeline 留在 Freeze-1b，但 projector／test space 決定「哪些模態需要接受檢驗」，看過候選後才定就能把負模劃為非物理子空間，與容差繞過同型 | **接受**。§5.2.1(iii) 由「容差不得吞掉 core」擴為通則——**任何名義屬 implementation、但能使 core criterion 失效的自由度，其形式與規則必須在 Freeze-1a 固定**——並分為 (iii-a) 容差與 **(iii-b) test-space／projector**。(iii-b) 將五項移至 Freeze-1a：admissible 形式、coverage／completeness 規則、允許排除模態的條件、mapping-equivalence 判準、pipeline-independence 判準；1b 只能依 object contract 實例化。明禁依候選 spectrum／eigenvalue sign／norm 分布／任何輸出選擇或調整 projector 與 test space，違者判 PROTOCOL-INVALID；無法提前決定者沿用 blinded-reviewer fallback。D.1 第 7 項、D.2 第 1–3 項同步改寫 |
| **1b.（v0.7 補，GPT 未提及）排除規則的可操作判準** | 「不得依 spectrum 選擇」是意圖陳述，不易稽核。補三條硬性規則：**預設不排除**（排除須有 Freeze-1a 就寫明的先驗物理理由）；**排除 predicate 必須僅由 object contract 可計算、不需對候選求值**——若一條排除規則得先算出候選 spectrum 才知道排除誰，它就是被候選決定的，判 PROTOCOL-INVALID；**被排除集合仍須報告其 norm／positivity 診斷**，使「排除集合恰好裝著全部負模」在報告中直接可見 |
| **2. verdict taxonomy 型別衝突**：每 gate 僅一 verdict，但 BOUNDED-SEARCH-EXHAUSTED 被稱 INCONCLUSIVE 子型，且兩者實為 specification-level 狀態 | **接受**。兩者移出 gate verdict 表，另立 **§2.1 Freeze-deliverable status**（DELIVERED／PENDING／BOUNDED-SEARCH-EXHAUSTED／SPEC-INFEASIBLE）。gate 層改記 `INCONCLUSIVE(reason=BOUNDED-SEARCH-EXHAUSTED)`；**SPEC-INFEASIBLE 永不作為 gate verdict**。§9.4 加型別提醒並移除「INCONCLUSIVE 子型」措辭 |
| **3. D.1 第 8 項同時是 blocker 又是可選項** | **接受**。更名為**外部依據路徑聲明**，二擇一即完成：路徑 A（聲明不承重文獻，core 僅由數學必要條件與 STATUS 論證）或路徑 B（完成 mapping 取得承重資格）。**未作出聲明**才是 PENDING。路徑一經聲明即凍結，事後改採 B 屬 protocol amendment |
| **4. 附錄 E 表格損壞**（兩列多出第三欄） | **接受**，兩列的補註合併回第二欄；全表已驗證每列均為兩欄 |

v0.7 未放寬任何 gate。Freeze-1a blocker 仍為九項，其中第 7 項擴充、第 8 項由 mapping 改為路徑聲明。

---

## 附錄 H — C8.4 獨立復檢處置〔v0.8〕

| 復檢發現 | v0.8 處置 |
| :--- | :--- |
| 512-per-target source run 位於 matching gate 邊緣，跨 seed 只有 2/5 同時通過 pair-count 與 coverage | 接受。C8.4 source pool 提升為 768；四組獨立 replication blocks 全部通過，且結果與 seeds 寫入獨立交付物。512 結果保留為 sample-size sensitivity evidence，不再承重 |
| 256-per-target 的 $\kappa=1$ 失敗被誤歸因於 domain restriction | 接受。等 pool 的未過濾 control 同樣失敗；$\kappa=1$ 在 512 與 768 raw pools 皆通過 filter-then-match。結論改為小 pool 不足，非 $\kappa$ 本身不可行 |
| 「covariate 只能增加」允許新增 local target proxy，合法消滅 Axis-B power | 接受。C8.1 新增 covariate 限為 label-invariant global scalar summary，排除 local profile／target proxy，並須在 candidate-independent qualification split 上保持既定 cohort 與 power floor；故意或實質吞掉 continuum contrast者判 PROTOCOL-INVALID，不得把結果轉記為 C8 INCONCLUSIVE |

v0.8 未降低任何 C8 門檻，也未設計或評估任何候選 kernel。C8.4 對照族的
candidate-independent 可構造性已確認；Freeze-1a 仍須完成 D.1 第 3、6 項整合及
其餘 blockers。
