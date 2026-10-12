# 理論優先路線圖與探索／正式驗證分離草案

狀態：**【提案／待獨立複核】**。操作者於 2026-10-11 選擇先推進理論，
優先處理容易證明或否定的問題，再考慮必要的大規模驗證。
基線：main `1839f6bb4104c3c74a9aea19552d4064f9194a85`，
tree `dc895f8f0e724685c7156a542de22001574e637b`（PR #69）。

本文件交付問題清單、證據分級與協定調整方案，不提供候選 K 的公式、材料或參數化。
本輪不跑新的 E4 診斷／witness／量測、不產生 seed、不開主機、不讀 arm ledger；
只執行既有 regression suite 作 repo 變更檢查，不產生新研究結果。
不把理論優先改寫成 Freeze-1a 完成或 6a-E 執行授權。

## 1. 研究目的與這次選擇

[README](../README.md) 的總問題是：不預設時空背景，只靠因果偏序和量子振幅，
能否同時湧現 3+1 維時空與有質量物質？目前沒有此結論。
[Stage 5C claim](STAGE5C_ACCEPTANCE.md) §1.1 則只問特定限制下的 **1+1D massless**
雙通道傳播；即使成功，也不等於導出質量、3+1D spinor、引力或幾何選擇。

研究順序改為：先查資訊與對稱性是否足夠、是否已有代數障礙、是否把答案放進假設；
再決定哪個候選問題值得構造；最後才選需要統計量測的主張。6a-E 的校準義務保留，
不再把優化其成本當成所有理論工作的前置條件。

這不是一律採用較弱證據。完整解析證明可以在有限成本下得到嚴格的條件性結論；
小例子可否定真正的全稱命題，但不能證明一般性、典型性或連續極限。
若核心問題仍缺證明，先標為缺口，不能用「探索性」把矛盾變成可接受。

## 2. 證據標示與前提帳

沿用 STATUS 的【已知／已確認／提案／已否定】，新增【探索】用於有實際推導片段或
精確例支持、但尚缺完整橋接或複核的方向；它不是較低門檻的 scientific PASS。
「已確認」必須限於完整證明或已複核驗證的作用域，不自動推及物理詮釋。
只有想法、尚無可檢查支持者仍是【提案】。

每份後续理論札記須列以下六項；缺任何一項，不得聲稱已完成該問題：

| 欄位 | 要記什麼 |
| :--- | :--- |
| 命題 | 有量詞的目標；究竟是存在性、全稱限制、典型性或近似結果 |
| 定義域與輸入 | 維度、有限／無限、boundary、order／number／phase、額外 primitive |
| 證據 | 原始文獻定位、完整推導、精確反例或既有 regression 的實際範圍 |
| 未證橋接 | 每個額外假設的 ID；下游引用時一起攜帶，不能消失 |
| 否定條件 | 哪個矛盾或反例足以停止這條路；否定的是哪個類別 |
| 後續驗證 | 哪些是紙上義務、哪些須 exact toy check、哪些才需 fresh 統計資料 |

不要求為純文字修改或每個猜想新增測試；有可執行的精確性主張時，測試應檢查真正的
反例或邊界，不能代替證明。所有嘗試，包括失敗和未完成者，保留版本與開發紀錄。

## 3. 已有約束：保留作用域，不把未被排除當成可行

| 約束 | 已有依據 | 不能由它推出的結論 |
| :--- | :--- | :--- |
| 特定 BdG block 的行列式相位固定 | STATUS 的 Q_test 列；`tests/test_gate_a_testbed.py::test_eigenvalue_symmetry_and_fixed_phase`；見 §3.1 | 所有費米子算子都不能選幾何，或任意改掉 block 就能產生有用相消 |
| intrinsic finite-direction／finite-valency 受 BHS 限制 | [Stage 5B result](STAGE5B_RESULT_B.md) §4–5；原論文 §2 Theorem 1 與 §3 | 所有 internal two-state fiber 都不存在，或任何非局域構造都可行 |
| global U/V 不等於 local chirality | [handoff v2](handoff_v2.0.md) §2.2；Stage 5B result | 1+1D 的 global bookkeeping 已提供 3+1D Clifford／Lorentz representation |
| O19 的 C8 第二座標恆零 | [PR #69 草稿](STAGE5C_6A_E_STRUCTURAL_COORDINATE_STATISTICAL_AMENDMENT_DRAFT.md) §2.1.1 | 任意 K／E3 的第二座標都為零，或物理本身只有一個可測自由度 |
| 6a-E／Freeze-1a 仍未完成 | [prereg](STAGE5C_6A_E_PREREGISTRATION_DRAFT.md) §8；acceptance 附錄 D.1 | run1 production 全完成就可 ADOPT item 7，或可開始正式候選評測 |

BHS 原始來源：Bombelli–Henson–Sorkin (2006),
[arXiv:gr-qc/0605006v1](https://arxiv.org/html/gr-qc/0605006v1)，
2026-10-11 核對 §2 Theorem 1、其延伸 (4) 及 §3 的 finite-region 限定。
定理針對 full Minkowski Poisson sprinkling 的 measurable Lorentz-equivariant direction map；
finite-valency 是其後果。有限 diamond 的 boundary 提供方向，不能用它宣稱繞過此限制。
此引用只核對既有 no-go 的作用域，不為新 acceptance 門檻取得承重資格。

### 3.1 既有 BdG 結果的純代數核對

這裡重述歷史 Q_test 的結構，不是新增 K。對 square complex R、real m，

$$
Q=\begin{pmatrix}mI&R\\R^\dagger&-mI\end{pmatrix},\qquad
Q^2=\operatorname{diag}(m^2I+RR^\dagger,m^2I+R^\dagger R).
$$

由 R 的 SVD 對兩個 blocks 分別作 unitary 變換，每個 singular value σ_j 對應
`[[m,σ_j],[σ_j,−m]]`，故 eigenvalues 為 `±sqrt(m²+σ_j²)`，

$$\det Q=(-1)^n\prod_{j=1}^n(m^2+\sigma_j^2).$$

在 fixed n、非零 determinant 的域，其相位固定；m=0 且 R singular 時 determinant
為零，相位未定，不能稱仍有相消相位。結論只排除這個 unshifted square block 的
determinant 作為網絡間 variable complex phase。其他 determinant prescription、完整
path-sum 或耦合重力作用量不由此式判定；更不能把 abs(det) 的結構敏感性稱作量子相消。

## 4. 優先問題：重要性與低成本判定能力同時排序

「高／中／低」是工作排序，不是成功機率或已有證明。排序優先解除最上游的含混。

| 次序／問題 | 對總主題的重要性 | 低成本能確定什麼 | 已有證據／缺口 | 下一份交付與停止條件 |
| :--- | :--- | :--- | :--- | :--- |
| T1：哪些量是輸入，哪些真要湧現？ | 高 | 高：查循環定義、同一資訊的不同實現、必要額外假設 | README；[Gate 0](foundations/kinematic_selection.md)；[Layer 0](foundations/invariant_projection_hypothesis.md)。尚無 Layer 0 數學模型 | 一張 primitive→目標的前提表，區分共形重建與時空生成、體積抽樣與裸 event count。若待導出的 metric／signature／c 已在輸入，撤回「已導出」，或明列為新增 primitive |
| T2：物質選幾何究竟要壓低哪個總量？ | 高 | 高：核對 fixed-phase 障礙與不充分推論；不能廉價保證選幾何成功 | 既有 BdG no-go、STATUS 附錄 C 的 KR entropy 紀律。尚缺 history measure、完整振幅與總量界 | 在不構造 K 下列出定義義務：同 N 的 history classes、權重／作用量、歸一化、比較量。若只有單個網絡 phase 或 log|det| 而無 class 總量，保持 OPEN |
| T3：global sectors 究竟提供多少 spinor 資訊？ | 高 | 高：前提與 symmetry／equivariance 不相容可先排除；存在性仍未知 | Stage 5B limited result；BHS；handoff §2.2。兩元素 bookkeeping 不是 Clifford representation | 逐項 capability 表：global labeling、local fiber、Lorentz representation、mass coupling 的來源。新增結構必須入帳；任何 no-go 限定量詞／域，不聲稱窮盡「所有合理」構造 |
| T4：C8 尺的零座標是工具限制還是總理論限制？ | 高 | 高：source-bound algebra；一般效果／飽和概率不能由兩例判定 | O19 已證；O2／O13 OPEN；不完整 witness 2/12 | 檢查 evaluator 的可識別性與不同 planted profiles 的域。不刪第二座標、不加 jitter、不換 endpoint；若要改 observable，另作版本化設計，舊通過不沿用 |
| T5：kinematics 是否真的選出了 finite c／signature？ | 高 | 中：可先否定過強公理主張，不能保證推得所有目標 | Gate 0 明列 local finiteness 不單獨推出 finite c；Malament/HKM 是既有流形類中的重建 | 把 G0-B／G0-C 改寫為明確公理→命題，尋 exact counterexample；與 T1 合併第一份前提帳，未證不填為定理 |
| T6：量子一致性和 continuum limit 的必要條件 | 高 | 中：定義域、adjoint／positivity／CAR 相容性可先查；無 operator 就不能完成極限 | STATUS Track A/B 的 positivity 警告；acceptance C9/C10；massless 1+1D 路徑 | 已知物理回復義務表：Hilbert／test space、時間與因果 prescription、positivity、unitarity、continuum mapping。不能以刪負模、調 projector 或 spectral dimension 曲線代替此證明 |
| T7：3+1D、質量與重力由哪個新橋接產生？ | 高 | 低：本輪只能識別缺口，不能廉價證明總主題 | README 尚未完成清單；C11；Layer 0 仍是提案 | 明列與 1+1D massless 的差別，逐個 primitive／limit／dynamics 義務；無橋接則維持 OPEN，不寫「自然外推」 |
| T8：正式統計與資源是否可負擔？ | 正式主張時高 | 中：先核定 estimand、依賴與計數，成功界未知 | PR #69 §4–5；joint matched law；budget-power audit | 在值得驗證的具名主張成立後，再作完整 cost／failure／power 設計；保留 item 7/8 缺口，現在不量測 |

第一份實質理論交付應是 **T1＋T5 的 primitive／公理／反例審計**。
第二份才是 **T2＋T3 的必要條件與 no-go 作用域表**。這兩份都可以在不設計 K、
不讀正式資料、不做大量數值計算的情況下開始。若得到反例，只否定所列命題及前提，
不自動否定整個主題；若沒有反例，也不宣稱存在性已獲支持。

## 5. 協定調整方案：先做無候選的理論，再決定是否開啟候選探索

**2026-10-12 現行決策：** PR #75／#76 的權限與隔離草案已獨立複核。操作者於
09:46:37 Asia/Taipei 明確批准僅紙上啟動；具名[ACT-X-0001／E0](STAGE5C_EXPLORATION_ACTIVATION.md)
只在 activation PR 獲 exact-head GO 並合併到 main 後生效，此前不開始構造。
正式候選資格／評測、資料與執行仍受原限制；X→F handoff 和 criterion 污染依該記錄，
不得以舊 closure 或新 seed 繞過。以下兩階段是原排序紀錄；第二階段權限已另案提出，
實際工作開始需引用有效 activation SHA。

原兩階段方案（歷史排序；第一階段仍可繼續）：

1. **現在的理論審計階段**：做定義、必要條件、已有構造的 no-go 與精確反例；
   不提出新 K／order ansatz／weight／構造材料，不操作 science data。
   先把 T1–T5 中能紙上排除的問題做清楚。大規模驗證留到有具名且值得檢驗的目標。
2. **另案的候選探索 amendment**：若審計顯示需要構造才能前進，獨立提交決定，
   同步修改 acceptance §0／D.1、STATUS 與 prereg 的相關 wording，具名建立 exploratory
   track，與原 confirmatory track 分離；複核版本相容後才可在該 track 設計。

第二階段的 amendment 至少須回答以下問題，而不是只加一個【探索】標籤：

| 義務 | 必須明訂的內容 |
| :--- | :--- |
| construction 權限 | 允許哪種理論工作／toy objects／額外 primitives；哪些 oracle 永不得回流 |
| 接觸帳 | 所有研究者已看過的資料、公開 fixtures、planted controls、失敗嘗試和證據，不能聲稱「沒用 seed 就未接觸」 |
| 開發保存 | 候選版本、選擇理由、否定／未完成結果保留；探索不得產生正式 scientific PASS |
| 確認邊界 | 先凍結具名候選及 evaluators／estimands／gates／power，再取得真正 fresh 資料；seed freshness 只是必要條件 |
| criterion 污染 | 若候選輸出已影響 core／projector／test-space／margin，舊 confirmatory 資格不能靠新 seed 恢復；需新 prereg 版本、完整 exposure mapping 與適當獨立／blinded review |
| 恢復方式 | 解完原 closure 或明訂被 supersede 的義務，完成版本 mapping、資源資格化與審查後才另授權 runner；不倒填舊 ledger |

不能把理論優先當作取消 certification、receipt 或 preflight：純紙上工作不會觸發
那些執行條件；將來有實際診斷／正式計算時，仍使用適用且事前審查的執行方案。
任何新定理依附的假設若未證，引用時保留條件；不以「之後再嚴謹」容忍既有反例。

## 6. 統計成本留待後續，但先修正計算單位的推論

1 CPU 年是核心累計 CPU 時間；本 repo 的規劃算術按 365 日為 31,536,000 CPU s。
多核心只有在任務可並行且實際機型效率足夠時才縮短等待時間；不能由此直接推雲端
費用或線性加速。本階段不需操作者先承諾 1 CPU 年，因為沒有量測／購機授權。

日後以「獨立 E4 endpoint 評估數」列 workload graph：全池 certification、matching、
claims／members／splits、是否共享輸入與 producer identity、合法 cache、失敗路徑與
overhead 分別入帳。PR #69 的 `3349×192×2`／2.3 CPU 年只是條件式規劃，
不能直接再乘每個 claim，也不能以 run1 fixture 平均成本作正式成本界。

尤其不能由「單一配對 contrast 變異數小」直接推出 cohort 方差減為 `σ²/m`。
在 fixed m 的已指定條件律 C 下，若 `Y=m^{-1}Σ_i D_i`，則

$$
\operatorname{Var}(Y\mid C)=\frac{1}{m^2}
\sum_{i,j=1}^{m}\operatorname{Cov}(D_i,D_j\mid C).
$$

matching 與 cohort-level CLEAN conditioning 可能引入依賴；沒有 covariance 控制就
不能刪掉 i≠j 的項。完全相關的 D_i 即不會有 `1/m` 節省。
random m 的 ratio estimand 還須處理分母、局部／全域條件律以及
`Z_b=m_b(Y_b−μ)`，不能將 pair-level empirical Bernstein 直接套上。
依據：[budget-power audit](STAGE5C_6A_E_E5_BUDGET_POWER_AUDIT.md) §3 與
[PR #69 候選定理](STAGE5C_6A_E_STRUCTURAL_COORDINATE_STATISTICAL_AMENDMENT_DRAFT.md) §4。

因此未來成本研究的承重量應是 **cohort 加權 contrast 的 tail／variance 和依賴界**；
單配對 variance 可以是子義務，不能單独承擔。改固定 m 亦須重新審 matching／item 2
與 estimand；O2／O13 的 observed saturation 不能作事前 support／variance 證明。
不為了 log(1/α) 的小幅節省改原 family budget。

## 7. 本稿的完成與審查標準

本稿完成的是研究順序與決策邊界，不是物理結論、K 存在性或新統計協定實作。
請獨立 reviewer 檢查：優先問題是否對總主題有用、現有 no-go 是否限於正確類別、
理論結論是否攜帶前提、候選探索與 confirmatory 是否真正分離、恢復驗證的條件是否
可操作。任何更改 core 的方案，不能沿用原 freeze 的資格。

6a-S 封存、run1 結果、O19、原 witness 2/12／exit 137 與 PR #69 的成本文字全部保留。
item 7 仍不能 ADOPT；items 3–5 v0.2 重驗待辦、item 8 OPEN、6a-E
`PREREGISTRATION-INCOMPLETE` 與 Freeze-1a PENDING 均不變。
本輪唯一建議的下一步是上述理論審計，並不授權重跑 witness、正式樣本或候選 K。
