# Stage 5C — 6a-E endpoint-evaluator preregistration review draft

狀態：**【review draft／PREREGISTRATION-INCOMPLETE／不可執行】**。

本文件把 6a-E 的既有硬約束、完整型別鏈、first-past-the-post lifecycle、判決閉包與仍缺的
承重欄位整理成單一 review surface。它**不是** selector-prereg freeze、不授權生成任何
6a-E seed、不授權讀取任何 6a-S arm numerical field，也不完成 active wrong-support、D.1
第 3 項或 Freeze-1a。

歷史基準：main `3397940b751870aae8ab83a99d503cb48b3e393c`（STATUS v1.43；98 tracked
files）。本文件只使用該 commit 上的 candidate-independent 規格與公開 categorical
custody facts；沒有開啟 1.5B／1.4B／3.1B ledgers，沒有計算 between-target 數值，沒有
設計、import 或執行候選 kernel $K$。

---

## 0. 本輪裁決

6a-S 已完整封存為 11/11 `6a-S PASS`，所以 11 個 selector parameter points 全部**有資格**
進入 6a-E。這只解除進場前置，不提供任何 endpoint effect、排序或 viability 資訊。

現行 source-of-truth 尚未給出一份可執行 6a-E preregistration。item 1 已 `CLOSED`；items
3＋6 現有共同 `REVIEW-PENDING` 交付物，但在獨立 review、CI、merge 與 state closeout 前仍
不算 `CLOSED`。至少下列四組仍是 blocking：

1. $\Pi_{\mathcal M}$ joint matched law、paired covariance schema 尚未交付；
2. near-zero／ratio certification 與 active wrong-support 雖已有共同 candidate-independent
   source-of-record，仍待獨立複核與 merge；
3. E4 的 contact／boundary leakage、fixed-$\epsilon$ continuum sequence、validated numerical
   error 與兩個獨立 implementation agreement 尚未固定；
4. E1／E2／E3 的二維 statistical regions、power、multiplicity、fresh seed manifests 與
   ledger／runner schema 尚未固定。

因此本 draft 的合法結論只有：

> `PREREGISTRATION-INCOMPLETE` 是 Freeze-deliverable 狀態，不是 selector gate verdict。
> 在 §8 的 closure matrix 全部轉為 `CLOSED`、可執行 source-of-record 與 runner 經獨立 review
> 合併前，任何 6a-E numerical access 均為 `PROTOCOL-INVALID`。

不得以 6a-S arm data、3.1B rehearsal pattern、reference-probe effect 或任何候選輸出填補
上述欄位。

---

## 1. 6a-E 必須繼承且不得默改的輸入

下表只列目前已存在的 candidate-independent 決議。它不表示尚缺欄位已自動決定。

| 項目 | 既有決議 | 6a-E 限制 |
| :--- | :--- | :--- |
| selector family | 11 個有序 parameter points，closed capacity 11 | 保持 `STAGE5C_SELECTOR_FAMILY.md` §3 的原始順序；不得依 6a-S 或 6a-E effect 重排 |
| 進場資格 | 11/11 `6a-S PASS` | PASS 只表示可進場；不得當作 endpoint evidence |
| pair domain | $\{(x,y):x\prec y\}$，source-first | 不得事後加 coordinate trimming／contact exclusion |
| pair weight／normalization | $\varphi_C=1$，$\mathcal N_C=|\Sigma(C)|$ | 任何更改須先走明文 amendment；不得用來放大 contrast |
| linear regulator | ordered pair space $\mathbb R^4$ 上 $\epsilon=1/16$ mass-one Gaussian | fixed-scale convention；box boundary leakage 與 pairing 適切性由 E4 承重，6a-S PASS 不提供佐證 |
| basis group | $G=T^2\rtimes S_2$，ambient Frobenius norm | 最終 endpoint 每分量須 $G$-invariant；global sector swap 是 invariance arm |
| primary endpoint | $\mathfrak I_G(M)=((Q-2|W|)/N^2,S/N^2)$ | 先 linear smear 成有限 $2\times2$ matrix，再取 invariant；不得交換次序 |
| targets | $p_\theta(u,v)=1+\theta q(u)q(v)$，$\theta=\pm0.4$ | matching 必須保留 joint two-arm law／paired covariance；不得以獨立 marginals 取代 |
| stage separation | 6a-S 與 6a-E streams 不相交 | 1.3B／1.4B／1.5B／3.1B 全部不得進 6a-E selection、confirmation、power 或 calibration |
| construction firewall | planted objects可用登記的 L4 evaluator oracle | 對 order-only 候選 $K$ 的存在性零蘊涵；任何 planted material 不得回流 construction |

`docs/STAGE5C_C8_4_HARD_CONTROLS.md` 的 scalar $L_\theta$ 已被 observable contract 降級為
oracle motivation／cross-check，**不是**本二維 primary endpoint，也不得直接當作 E1。

---

## 2. 必須凍結的單一路徑

每個 selector、每個 split 都必須走同一條 typed pipeline；但 pipeline 的 selector 欄位須依
gate 顯式路由，而不是強迫所有 gate 共用同一個 literal selector：E1／E2／E4 使用目前按
原始順序評測的 $\Sigma_{C8}$ member；E3 discrimination arms 使用另行事前登記的
$\Sigma_{C7/E3}$／test-function support mapping。後者是 evaluator-side L4 control，不增加、
替換或重排 closed $\Sigma_{C8}$ family，也不得回流 construction。

1. 由 fresh 6a-E manifest 生成兩 target 的 control causets；
2. 依 C8.1 frozen matching lifecycle 形成 joint matched cohort $\mathcal M$；
3. gate router 逐位元記錄本 gate 登記的 selector／support-mapping identity；C8 路徑只把
   `BlindedCase(case_id, order)` 交給目前的 $\Sigma_{C8}$ member，E3 則依 frozen L4 權限呼叫
   $\Sigma_{C7/E3}$／test-function support mapping；
4. 登記的 selector／support mapping 回傳 typed causal pairs 後，evaluator 才取回 sealed coordinates；
5. 形成 $\widetilde\nu^C_{\Sigma,\varphi}$，再線性套用 $R_{1/16}$；
6. 以已凍結的 bi-spinor distribution／test-measure pairing形成
   $M^C_{\theta,\Sigma}=\langle S_\theta,\nu^{C,1/16}_{\Sigma,\varphi}\rangle$；
7. 先執行 §3 nontriviality gate；通過後才可形成 $\mathfrak I_G(M)$；
8. 由 matched-pair joint law 計算事前固定的二維統計量、regions 與 simultaneous uncertainty；
9. 目前 $\Sigma_{C8}$ member 與固定的 gate-specific E3 evaluator tuple 共同依 E1–E5 全部 gate
   產生一個 split-level categorical verdict；不得以 E3 tuple 改變 member identity或 family 順序；
10. 依 §6 的 sequential state machine 決定停止、confirmation 或下一 member。

離散與 continuum 可以有兩個獨立 implementation，但必須共用同一份形式規格，並在 planted
finite cases 上證明 mapping equivalence。任何一步的物件、orientation、normalization、pairing、
adjoint、branch 或 boundary prescription若未在 freeze commit 唯一化，execution gate 必須
fail closed。

**明禁捷徑：**

- 不得計算 $\mathbb E[M]$ 後才套 $\mathfrak I_G$，除非已按 observable contract §4.2
  證明 concentration、continuity、uniform integrability 與 nonlinear-bias bound；
- 不得從兩個 arm marginals 重建 paired variance；
- 不得挑 endpoint 的一個分量、依 data 選 projection／sign／norm 或把二維結果壓成未登記 scalar；
- 不得把 6a-S Fourier signatures、$d_{\rm mean}$ 或 $d_{\rm law}$ 當作 6a-E endpoint input；
- 不得把任何舊 ledger 路徑設為 6a-E runner argument。

---

## 3. Near-zero／numerical-certification contract 必填欄位

Primary endpoint 在 $M=0$ 為 $0/0$；非零但數值上無法證明遠離零時也不得報 ratio。最終
prereg 必須固定一個**尺度穩健**的 nontriviality contract，而不是裸的全域絕對常數。

### 3.1 必須同時固定

1. $M$ 的計算精度與 validated Frobenius error bound $\eta_M$ 的定義；
2. error bound 如何涵蓋 quadrature／sampling representation、regulator、boundary／contact
   treatment 與 floating-point rounding；
3. 第二個獨立 implementation 的輸出及 agreement norm；
4. 證明 $\|M\|_F$ 遠離零的 scale-aware predicate；
5. ratio uncertainty 如何傳播到兩個 endpoint components 與 joint region；
6. exact zero、certified nonzero、uncertainty interval跨零、non-finite output 四種 case 的判決；
7. equality-at-boundary 的開／閉區間 convention。
8. candidate-independent planted feasibility suite：在不讀任何 arm ledger、也不以結果調整常數的
   前提下，以 intended matrix scale、pair-count／accumulation scale 與 condition-number range
   端到端證明正常 case 可通過 certification，並證明每個已登記 failure mode 會 fail closed；
   global sector swap 另須在此 suite 證明它是 canonical exact relabeling、兩側使用相同 canonical
   ordering 與逐操作 arithmetic trace，且不因重新累加／重新收縮而改變 floating-point 運算次序。
   該證明與 executable trace test 未交付時，不得以逐位元相等作 scientific gate。

### 3.2 不得預設的 default

- `minimum_norm_squared=0` 只處理 exact zero，不構成 near-zero gate；
- `1e-12` 或「machine precision」沒有量級／累加長度／condition-number mapping，不可直接採用；
- 以看到的最小 $\|M\|$ 倒推 floor、或把 floor 設在 arm data 之下，均為 post-hoc tuning；
- 統計 confidence region 未達門檻是 `FAIL`，不能因結果接近邊界改稱 numerical
  `INCONCLUSIVE`；只有事前定義的 numerical certification 本身失敗才可記 `INCONCLUSIVE`。

唯一公式、可執行判準、shared planted feasibility/failure suite 與 exact-swap trace proof 現由
`STAGE5C_6A_E_CERTIFICATION.md`／`analysis/stage5c_numerical_certification.py`／
`analysis/stage5c_planted_certification.py` 以 `REVIEW-PENDING` 狀態交付。這不等於 `CLOSED`，
也不授權 arm endpoint 求值。

---

## 4. E1–E5 的 closure requirements

| Gate | 最終 prereg 必須唯一化的內容 | 現況 |
| :--- | :--- | :---: |
| **E1 continuum contrast** | $S_\theta$ typed formula／prescription；paired 2D estimand；contrast orientation；joint metric；simultaneous region；effect floor；integration uncertainty；boundary equality rule | `OPEN` |
| **E2 target-null equivalence** | $T_+$ vs $T_+$、$T_-$ vs $T_-$ 的完整 same-pipeline generator／matching；2D equivalence region；TOST 或等價程序；兩 null arms 各自 cohort floor | `OPEN` |
| **E3 planted alternatives** | correct chiral、symmetric diffusion、sector blind 的完整參數域；active wrong-support typed intervention；Gate O；Gate E joint-law regions／逐分量規則；global swap exact-invariance arm | `REVIEW-PENDING` |
| **E4 distributional well-posedness** | fixed-$\epsilon$ continuum sequence；test-function topology；contact／box-boundary leakage；pairing existence；convergence rate／error bound；兩個獨立 implementations 與 agreement criterion | `OPEN` |
| **E5-D detection power** | E1／E3 每個承重 directional claim、effect model、adjusted error allocation、cohort floor與 power $\ge0.90$ 的計算 | `OPEN` |
| **E5-E equivalence power** | E2 每個 null claim、equivalence margin、最壞 null variance／distribution、adjusted error allocation、cohort floor與 power $\ge0.90$ 的計算 | `OPEN` |

E3 目前特別受 `STAGE5C_E3_WRONG_DIRECTION.md` 約束：全域 $\sigma_x$ swap 只能作 invariance
control；active wrong-support 必須固定 continuum frame、test-function instance、normalization與
covariant output legs，再主動改變 support feeding。孤立矩陣或「orbit 外」都不構成替代品。

任一 `OPEN` 欄位不得以 runner 中的隱藏 default、CLI fallback、人工裁量或未版本化 notebook
補上。若完整構造嘗試在明定有限類中無法完成，合法狀態是
`BOUNDED-SEARCH-EXHAUSTED`；缺 completeness proof 時不得升格為 `SPEC-INFEASIBLE`。

---

## 5. Statistical family 與資料 lifecycle 必填契約

最終 freeze 必須在生成任何 6a-E seed 前固定：

- selection 與 confirmation 各自的 fresh seed formula、target／member／cohort index mapping；
- calibration／power-only streams（若有）與兩個 confirmatory splits 完全不相交；
- matched cohort 的 raw pool、caliper、unmatched handling、minimum pairs／coverage；
- 11 個原始 family positions 的 family-wise $\alpha$ 或 e-value spending；
- E1、E2、E3 內多個承重 claims 的 within-member multiplicity；
- selection 與 confirmation 之間的 allocation；
- 不使用未進場／已失敗位置預算的 non-recycling rule，或事前證明的唯一 recycling rule；
- seed claim、append＋fsync、hash chain、runtime、protocol digest、burn registry 與 attestation schema；
- dress rehearsal（如需要）的 fresh development base、用途限制與不可回流條款；
- 全域 selector ledger 與 `docs/stage5c_confirmatory_ledger.md` 的寫入順序。

禁止以「固定樣本應該夠」取代 E5-D／E5-E power calculation。對等效性 claim 必須從
$\delta_E$、adjusted error 與最壞 null variance反推 cohort floor；不得沿用 detection power。

Selection effect estimate 永遠不能成為最終承重數值。Confirmation 必須以同一 form、同一
threshold、同一 member parameter 與 fresh data 獨立重跑全部承重 gates。

---

## 6. Sequential first-past-the-post 的封閉判決表

以下 state machine 是本 draft 提議交付給獨立 review 的唯一 lifecycle。最終 prereg 若修改
任何一列，必須在第一次 6a-E seed 生成前完成 review／merge。

### 6.1 Member-level staged adjudication

每個 split 對一個 selector 只產生一個 verdict，而且 scientific quantities 的形成本身受
numerical certification gate 約束；不得採「全部計算完再 adjudicate」的流程。唯一合法順序是：

1. **Custody／schema stage**：先檢查 leakage、metadata、schema、seed lifecycle、執行順序、
   runtime、protocol digest 與禁止資料來源。任一違反立即為 `PROTOCOL-INVALID`，後續數值
   不得承重；
2. **Certification precondition stage**：只有 custody clean 才檢查 §3 的 near-zero predicate、
   finite backend、validated numerical error、independent-implementation agreement 與事前資源／
   cohort floor；global swap 另須檢查 canonical exact-relabel construction 與 runtime operation-trace
   identity。任一項未能認證即為 `INCONCLUSIVE`；若 swap trace 無法證成相同，或差異仍可能歸因
   於 floating-point evaluation order，reason code 為 `SWAP-NUMERICS-UNCERTIFIED`，不得記 scientific
   `FAIL`。上述情形都必須在形成 $\mathfrak I_G$ ratio、endpoint
   law、effect、region 或任何 E1–E4 scientific comparison **之前** short-circuit，scientific
   gates 保持 `NOT-EVALUATED`，不得在 ledger 寫入或向操作者顯示任何 scientific output；
3. **Scientific stage**：只有 certification `CLEAN` 才評估 E1–E4 acceptance criteria與明定的
   E5 power requirements。任一 scientific criterion 未達即為 `FAIL`；全部通過才為 `PASS`。

因此可執行 adjudicator 必須實作上述 staged short-circuit，而不是對四個 verdict 直接取
`PROTOCOL-INVALID > FAIL > INCONCLUSIVE > PASS` 的最大值。`PROTOCOL-INVALID` 仍是全域最高
precedence；certification clean 之後，scientific `FAIL > PASS`。E4 內必須把「數學／分布
well-posedness acceptance criterion 未達」（certified computation 下為 `FAIL`）與「數值管線
無法認證該 criterion」（`INCONCLUSIVE`）分成不同 typed fields 與 reason codes。

- `PASS`：E1–E4 全部通過；E1 與每一個 E3 discrimination claim 的 E5-D 全部通過；E2 的
  $T_+$ null arm 與 $T_-$ null arm 各自通過 E5-E；
- `FAIL`：run well-defined、custody clean 且 numerical certification clean，但任一預登記
  scientific effect／equivalence／planted／well-posedness acceptance criterion 未達；
- `INCONCLUSIVE`：只限 certification stage 已預登記的資源、cohort、non-finite backend、
  validated numerical error、near-zero、implementation-agreement failure 或 global-swap
  exact-relabel／operation-trace certification failure（含 `SWAP-NUMERICS-UNCERTIFIED`）；不得拿來遮蔽
  certification-clean computation 的 statistical boundary miss；
- `PROTOCOL-INVALID`：任何 leakage、未登記 metadata／branch、schema mismatch、重用／早生
  seed、錯序、runtime／digest mismatch、開啟 6a-S numerical ledger、未凍結欄位被求值，
  或執行中斷後 ledger 不完整／沒有 terminal verdict。

E4 不另套 detection／equivalence power label；它由已凍結的數學 existence／convergence criterion
與 numerical proof obligation 承重。global swap arm 是 gauge operation，必須依逐位元完全相等
裁決，但此 gate 只有在 §3.1.8 的 exact-relabel／identical-operation-trace obligation 與本次 runtime
trace certification 均 `CLEAN` 後才可進入；未認證時依上段記 `INCONCLUSIVE`。不得套用 E4 的
independent-implementation agreement bound，也不得由執行者臨時替它選 E5-D 或 E5-E。以上
applicability 對所有 member／split 固定，
沒有 per-member discretion。

### 6.2 Split／member transition

| 目前狀態 | 結果 | 唯一下一步 |
| :--- | :--- | :--- |
| member $j$ selection | `PASS` | 鎖定同一 member；啟動其 fresh confirmation；不得先看 member $j+1$ |
| member $j<11$ selection | `FAIL` | burn selection data；按原始順序進 member $j+1$ |
| member 11 selection | `FAIL` | burn selection data；不授權後繼，記 `BOUNDED-SEARCH-EXHAUSTED` |
| member $j$ selection | `INCONCLUSIVE` | 全 protocol 停止並記 `INCONCLUSIVE`；不得跳過 unresolved earlier member |
| member $j$ selection | `PROTOCOL-INVALID` | 全 protocol 停止；修規格須 fresh protocol／fresh streams |
| member $j$ confirmation | `PASS` | 記 `SELECTOR-VIABLE`，採用 member $j$，停止；永不評測後續 member |
| member $j<11$ confirmation | `FAIL` | burn selection＋confirmation；按原始順序進 member $j+1$，不得引用 selection estimate解釋 |
| member 11 confirmation | `FAIL` | burn selection＋confirmation；不授權後繼，記 `BOUNDED-SEARCH-EXHAUSTED` |
| member $j$ confirmation | `INCONCLUSIVE` | 全 protocol 停止並記 `INCONCLUSIVE`；不得改把 member $j$ 當 FAIL 以便續跑 |
| member $j$ confirmation | `PROTOCOL-INVALID` | 全 protocol 停止；不得重跑同一 streams |
| member 11 結束仍無 confirmation PASS | — | 記 `BOUNDED-SEARCH-EXHAUSTED`；不是 no-go，也不是 selector gate `FAIL` |

表中的「全 protocol 停止」均指**目前這一個已登記 protocol instance 永久終止**；不得在原
instance 內補樣本、續跑、不改檔重跑或把 `INCONCLUSIVE` 改記為 `FAIL` 以解鎖下一 member。

### 6.3 中斷、INCONCLUSIVE 與後繼 protocol

- 任一 selection／confirmation 在建立 execution ledger 後 crash、被 kill、磁碟寫入失敗、
  hash chain／terminal record 不完整或無法產生唯一 terminal verdict，均記
  `PROTOCOL-INVALID`；所有已 claim／生成的 seeds 永久 burned，目前 protocol instance 停止，
  不得 resume 或以同一 streams retry；
- `INCONCLUSIVE` 同樣永久終止目前 protocol instance，且不授權任何後續 member；
- 中斷或 `INCONCLUSIVE` 後若仍要研究，只能先提交具名、版本化的 successor protocol／amendment，
  經獨立 review、CI 與 merge 後使用全新 disjoint streams。amendment 必須在新 seed 生成前固定
  中斷原因、resource／backend／certification 修法與新的 lifecycle；
- successor 不從 member 1 任意重置，也不直接跳到下一 member；它從 protocol lineage 中**最早
  未解決的 operation** 重新開始：selection 未完成／`INCONCLUSIVE` 時回到同 member selection，
  confirmation 未完成／`INCONCLUSIVE` 時回到同 member confirmation。若 amendment 使更早的
  terminal categorical verdict 失效，最早未解決點回退到最早受影響 operation。所有此前仍有效、
  已 committed 的 terminal categorical `FAIL`／selection `PASS` 與原始 member 順序一併承接；
  不得承接其 endpoint、effect、region 或其他 scientific numerical output；
- family-wise／within-member budget 以整個 protocol lineage 記帳，不因 successor 重置。所有已完成
  scientific test 的 allocation，以及任何已進入 scientific stage 但未留下完整 terminal record 的
  allocation，均保守視為永久 spent；在 certification stage short-circuit、scientific gates 全為
  `NOT-EVALUATED` 的 operation 則不虛構 scientific spend。重作未解決／失效 operation 只能使用
  genesis 前已凍結的 successor reserve，不得回收既有 spend、未使用 member budget或失敗位置預算；
  reserve 不足即不得啟動 successor。exact allocation／reserve formula 仍屬 §8 item 8 `OPEN`，
  在其 CLOSED 前本條只固定語意，不授權任何執行；
- 舊 instance 的 endpoint、effect、region、pair-count 或其他 scientific numerical output
  永久不得用來選 threshold、effect floor、equivalence margin、power model、member 順序、
  successor claim 或候選設計。只容許 custody／operational root-cause facts承擔說明為何需要
  successor；不得藉 root-cause 名義重判舊 scientific result。

### 6.4 未涵蓋狀況

若 runtime 出現本表沒有唯一下一步的狀況，記
`PROTOCOL-INVALID` 並立即停止，同時以獨立 reason code 記錄 `PREREGISTRATION-UNSPECIFIED`
specification-level defect。不得現場補規則、不得映成其他 scientific verdict、不得開新 seeds；
所有已 claim／生成的 seeds 永久 burned。後續只能版本化修訂並使用 fresh streams。

---

## 7. 結果語意的完整對照

| 觀察形狀 | 預登記語意 |
| :--- | :--- |
| E1 effect 為 null／方向相反／未達 joint floor | 該 selector split `FAIL`；不得稱 target 或 family 失敗 |
| E1 confidence region只碰到或跨過 effect boundary | 依最終固定的開／閉 convention機械判定；不得稱 numerical `INCONCLUSIVE` |
| §3 certification 未 clean | 記 `INCONCLUSIVE`；在計算時 short-circuit，E1／E2／E3／E4 scientific gates 為 `NOT-EVALUATED`，不得形成、保存或顯示 endpoint／effect／region |
| E2 只有一個 target-null arm 通過 | 該 selector split `FAIL` |
| E3 只有部分 planted alternatives通過 | 該 selector split `FAIL`；不得只報成功類別 |
| global sector swap 的 canonical exact-relabel／identical-operation-trace certification 未 clean，或差異仍可能來自 floating-point evaluation order | `INCONCLUSIVE`／`SWAP-NUMERICS-UNCERTIFIED`；swap scientific gate 為 `NOT-EVALUATED`，不得 burn member 為 scientific `FAIL` |
| 上述 swap certification clean 後仍不是逐位元完全相等 | 該 selector split `FAIL`；此時才可歸因為 exact gauge invariance failure；不得套用 E4 agreement tolerance |
| swap 差異來自 schema／stored-field recomputation mismatch | `PROTOCOL-INVALID`；不是 scientific `FAIL` |
| proposed active wrong-support 在 pre-execution Gate O 落入 correct $G$-orbit | `DIRECTION-GAUGE` control status；prereg 維持 incomplete、不得生成 E3 seeds，也不得硬設 discrimination claim |
| Gate O 通過但 Gate E 不分離 | 該 evaluator/control pairing `FAIL`；不得推論所有方向 evaluator no-go |
| E4 pairing不存在或 regulator／boundary limit不收斂 | 該 selector split `FAIL`；若只因預登記 numerical resource cap 無法裁決才是 `INCONCLUSIVE` |
| cohort 未達事前 power floor | `INCONCLUSIVE`；不得補樣本或借用其他 member／split |
| execution 中斷、ledger／hash chain 不完整或沒有 terminal verdict | `PROTOCOL-INVALID`；已 claim／生成 seeds burned；依 §6.3 停止，不得 resume／retry |
| selection PASS、confirmation FAIL | 依 §6 續測下一 member；該成員不 viable，selection estimate 不承重 |
| selection／confirmation `INCONCLUSIVE` | 目前 protocol instance 永久停止；只有 §6.3 的 fresh successor protocol 路徑，不得直接續測 |
| 多個 member 看似會通過 | first confirmation PASS 即停；後續 member 保持未觀察，禁止 argmax |
| 全部 member無 confirmation PASS | `BOUNDED-SEARCH-EXHAUSTED`，只限 closed family 11 |
| 出現本表未涵蓋 case | `PROTOCOL-INVALID` 並停止；另記 `PREREGISTRATION-UNSPECIFIED` specification-defect reason code |

任何 PASS 都只對 1+1D evaluator／selector contract 有效；不證明 order-only $K$ 存在、不等於
Stage 5C-1 PASS、不授權 3+1D 或「已導出 spinor／chirality」敘述。

---

## 8. Freeze closure matrix

只有每一列都有具名文件、source-of-record、tests、numerical constants／bounds、seed manifest
與獨立 review，狀態才可由 `OPEN` 改為 `CLOSED`。

| # | Closure item | 必要交付物 | 狀態 |
| :---: | :--- | :--- | :---: |
| 1 | typed $S_\theta$／pairing／adjoint／boundary prescription | `STAGE5C_6A_E_TYPED_PAIRING.md`＋兩個 independent implementations＋mapping tests | `CLOSED` |
| 2 | $\Pi_{\mathcal M}$ joint matched law | generator／matcher source-of-record＋paired covariance schema | `OPEN` |
| 3 | near-zero／ratio numerical certification | `STAGE5C_6A_E_CERTIFICATION.md`＋scale-aware formula＋error propagation＋boundary tests＋candidate-independent planted feasibility／failure suite | `REVIEW-PENDING` |
| 4 | E1 joint contrast | estimand／2D region／effect floor／uncertainty | `OPEN` |
| 5 | E2 null equivalence | two null generators／region／TOST／cohort floor | `OPEN` |
| 6 | E3 planted family | `STAGE5C_6A_E_CERTIFICATION.md`＋具名 $\Sigma_{C7/E3}$／test-function support-mapping source-of-record＋complete domains＋active wrong-support Gate O/E＋canonical exact-relabel swap construction／identical-operation-trace proof與 planted trace tests | `REVIEW-PENDING` |
| 7 | E4 well-posedness | fixed-scale sequence／contact／boundary／agreement criteria | `OPEN` |
| 8 | E5-D／E5-E multiplicity與 power | complete claim family＋lineage-wide spending／successor reserve＋power audit | `OPEN` |
| 9 | selection／confirmation manifests | fresh disjoint bases＋burn lifecycle＋earliest-unresolved successor mapping＋non-recycling | `OPEN` |
| 10 | runner／ledger／adjudicator freeze | fail-closed executable implementation＋gate router 的 typed selector／support-mapping identity record＋swap runtime operation-trace certification＋end-to-end dress test＋committed predecessor-ledger prerequisite chain | `OPEN` |
| 11 | exhaustive decision table | §6–§7 與 runner state machine逐列一致 | `DRAFT` |
| 12 | independent review／CI／merge | review record＋green CI＋main commit | `OPEN` |

Closure rule：**12 列全部 `CLOSED` 才能把文件狀態改為「preregistration frozen」。** 若只完成
部分列，STATUS 必須逐列保留 `PENDING`，不得以百分比或「接近完成」暗示執行授權。
item 11 依定義必須與 item 10 的實際 runner state machine 逐列比對；item 10 尚為 `OPEN` 時，
item 11 必須維持 `DRAFT`，不得只憑文件表面完整而提前改為 `CLOSED`。
item 1 已由 PR #22 交付，經兩輪獨立 code review、CI 與 merge commit `1acd1771` 完成，
故可單獨記為 `CLOSED`。items 3＋6 的 `REVIEW-PENDING` 只表示共同 planted infrastructure
與具名公式正在等獨立複核；在 review、CI、merge 與 state closeout 前不等於 `CLOSED`。
items 2、4–5、7–10、12 仍為 `OPEN`、item 11 仍為 `DRAFT`，因而不解除任何 execution firewall。

---

## 9. 下一段工作的合法順序

1. 先由獨立 review 檢查本 draft 是否完整捕捉既有 hard constraints，尤其 §6–§7 是否仍有
   未列出的分支；
2. 分別交付 typed continuum pairing／active wrong-support／E4 numerical certification；certification
   同時須以 candidate-independent planted cases 在 intended scale 完成可通過性與 fail-closed
   feasibility demonstration，不得用 arm data 選常數；
3. 在前述 objects 全部固定後，才作不讀 arm data 的 power／multiplicity preregistration；
4. 再凍結 runner、ledger、adjudicator與一次性 fresh lifecycle。runner 在建立 ledger、claim seed
   或呼叫 generator **之前**，必須驗證上一個已完成 operation 的 committed／registered ledger
   snapshot、SHA-256、terminal adjudication、protocol digest、runtime 與 transition authorization：
   genesis 只授權 member 1 selection；selection `PASS` 只授權同 member confirmation；對 $j<11$，
   selection `FAIL` 或 confirmation `FAIL` 只授權下一 member selection；member 11 的 selection／
   confirmation `FAIL` 不授權任何後繼並終局為 `BOUNDED-SEARCH-EXHAUSTED`；confirmation `PASS`、任何
   `INCONCLUSIVE` 或 `PROTOCOL-INVALID` 均不授權後繼。member $j+1$ 不得與 $j$ 並行，也不得
   在 predecessor registry／attestation commit 前啟動；
5. 全部 review／CI／merge 後，才可生成第一個 6a-E seed。

本文件合併本身**不**讓上述任何一項從 PENDING 變為 DELIVERED，也不授權開啟現有 raw
ledgers。若後續發現本 draft 漏列情形，唯一合法動作是先修 draft；不是在執行時補判準。
