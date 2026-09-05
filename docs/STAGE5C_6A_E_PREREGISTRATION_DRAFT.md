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

現行 source-of-truth 尚未給出一份可執行 6a-E preregistration。至少下列四項仍是 blocking
open item：

1. continuum bi-spinor distribution $S_\theta$、其 retarded prescription／boundary condition，
   以及與 regulated pair measure 的線性 pairing 尚未形成單一 typed source-of-record；
2. active wrong-support 仍缺完整 typed intervention、參數域與 Gate O／Gate E 實例；
3. E4 的 contact／boundary leakage、fixed-$\epsilon$ continuum sequence、validated numerical
   error 與兩個獨立 implementation agreement 尚未固定；
4. E1／E2／E3 的二維 regions、near-zero rule、power、multiplicity、fresh seed manifests 與
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

每個 selector、每個 split 都必須走同一條 typed pipeline：

1. 由 fresh 6a-E manifest 生成兩 target 的 control causets；
2. 依 C8.1 frozen matching lifecycle 形成 joint matched cohort $\mathcal M$；
3. 只把 `BlindedCase(case_id, order)` 交給 $\Sigma$；
4. selector 回傳 causal pairs 後，evaluator 才取回 sealed coordinates；
5. 形成 $\widetilde\nu^C_{\Sigma,\varphi}$，再線性套用 $R_{1/16}$；
6. 以已凍結的 bi-spinor distribution／test-measure pairing形成
   $M^C_{\theta,\Sigma}=\langle S_\theta,\nu^{C,1/16}_{\Sigma,\varphi}\rangle$；
7. 先執行 §3 nontriviality gate；通過後才可形成 $\mathfrak I_G(M)$；
8. 由 matched-pair joint law 計算事前固定的二維統計量、regions 與 simultaneous uncertainty；
9. 同一 selector 依 E1–E5 全部 gate 產生一個 split-level categorical verdict；
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

### 3.2 不得預設的 default

- `minimum_norm_squared=0` 只處理 exact zero，不構成 near-zero gate；
- `1e-12` 或「machine precision」沒有量級／累加長度／condition-number mapping，不可直接採用；
- 以看到的最小 $\|M\|$ 倒推 floor、或把 floor 設在 arm data 之下，均為 post-hoc tuning；
- 統計 confidence region 未達門檻是 `FAIL`，不能因結果接近邊界改稱 numerical
  `INCONCLUSIVE`；只有事前定義的 numerical certification 本身失敗才可記 `INCONCLUSIVE`。

最終文件必須把本節改為唯一公式與可執行判準。現在維持 `OPEN`，所以禁止 endpoint 求值。

---

## 4. E1–E5 的 closure requirements

| Gate | 最終 prereg 必須唯一化的內容 | 現況 |
| :--- | :--- | :---: |
| **E1 continuum contrast** | $S_\theta$ typed formula／prescription；paired 2D estimand；contrast orientation；joint metric；simultaneous region；effect floor；integration uncertainty；boundary equality rule | `OPEN` |
| **E2 target-null equivalence** | $T_+$ vs $T_+$、$T_-$ vs $T_-$ 的完整 same-pipeline generator／matching；2D equivalence region；TOST 或等價程序；兩 null arms 各自 cohort floor | `OPEN` |
| **E3 planted alternatives** | correct chiral、symmetric diffusion、sector blind 的完整參數域；active wrong-support typed intervention；Gate O；Gate E joint-law regions／逐分量規則；global swap exact-invariance arm | `OPEN` |
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

### 6.1 Member-level gate aggregation

每個 split 對一個 selector 只產生一個 verdict，precedence 為：

`PROTOCOL-INVALID > FAIL > INCONCLUSIVE > PASS`，沿用已凍結 6a-S 的保守聚合順序；一個
well-defined scientific failure 不會被同一 split 的次要 resource shortfall 隱藏。

- `PASS`：E1–E4 與適用的 E5-D／E5-E 全部通過；
- `FAIL`：run well-defined 且 numerical certification clean，但任一預登記 scientific
  effect／equivalence／planted／well-posedness acceptance criterion 未達；
- `INCONCLUSIVE`：只有預登記的資源、cohort、non-finite backend、validated numerical error
  或 implementation-agreement failure；不得拿來遮蔽 statistical boundary miss；
- `PROTOCOL-INVALID`：任何 leakage、未登記 metadata／branch、schema mismatch、重用／早生
  seed、錯序、runtime／digest mismatch、開啟 6a-S numerical ledger或未凍結欄位被求值。

### 6.2 Split／member transition

| 目前狀態 | 結果 | 唯一下一步 |
| :--- | :--- | :--- |
| member $j$ selection | `PASS` | 鎖定同一 member；啟動其 fresh confirmation；不得先看 member $j+1$ |
| member $j$ selection | `FAIL` | burn selection data；按原始順序進 member $j+1$ |
| member $j$ selection | `INCONCLUSIVE` | 全 protocol 停止並記 `INCONCLUSIVE`；不得跳過 unresolved earlier member |
| member $j$ selection | `PROTOCOL-INVALID` | 全 protocol 停止；修規格須 fresh protocol／fresh streams |
| member $j$ confirmation | `PASS` | 記 `SELECTOR-VIABLE`，採用 member $j$，停止；永不評測後續 member |
| member $j$ confirmation | `FAIL` | burn selection＋confirmation；按原始順序進 member $j+1$，不得引用 selection estimate解釋 |
| member $j$ confirmation | `INCONCLUSIVE` | 全 protocol 停止並記 `INCONCLUSIVE`；不得改把 member $j$ 當 FAIL 以便續跑 |
| member $j$ confirmation | `PROTOCOL-INVALID` | 全 protocol 停止；不得重跑同一 streams |
| member 11 結束仍無 confirmation PASS | — | 記 `BOUNDED-SEARCH-EXHAUSTED`；不是 no-go，也不是 selector gate `FAIL` |

### 6.3 未涵蓋狀況

若 runtime 出現本表沒有唯一下一步的狀況，記
`PREREGISTRATION-UNSPECIFIED` 並立即停止。這是 specification-level defect；不得現場補規則、
不得把它映成最接近的 verdict、不得開新 seeds。後續只能版本化修訂並使用 fresh streams。

---

## 7. 結果語意的完整對照

| 觀察形狀 | 預登記語意 |
| :--- | :--- |
| E1 effect 為 null／方向相反／未達 joint floor | 該 selector split `FAIL`；不得稱 target 或 family 失敗 |
| E1 confidence region只碰到或跨過 effect boundary | 依最終固定的開／閉 convention機械判定；不得稱 numerical `INCONCLUSIVE` |
| E2 只有一個 target-null arm 通過 | 該 selector split `FAIL` |
| E3 只有部分 planted alternatives通過 | 該 selector split `FAIL`；不得只報成功類別 |
| global sector swap 在 well-defined computation 中超出 frozen agreement bound | 該 selector split `FAIL`；若差異來自 schema／stored-field recomputation mismatch 才是 `PROTOCOL-INVALID` |
| proposed active wrong-support 在 pre-execution Gate O 落入 correct $G$-orbit | `DIRECTION-GAUGE` control status；prereg 維持 incomplete、不得生成 E3 seeds，也不得硬設 discrimination claim |
| Gate O 通過但 Gate E 不分離 | 該 evaluator/control pairing `FAIL`；不得推論所有方向 evaluator no-go |
| E4 pairing不存在或 regulator／boundary limit不收斂 | 該 selector split `FAIL`；若只因預登記 numerical resource cap 無法裁決才是 `INCONCLUSIVE` |
| cohort 未達事前 power floor | `INCONCLUSIVE`；不得補樣本或借用其他 member／split |
| selection PASS、confirmation FAIL | 依 §6 續測下一 member；該成員不 viable，selection estimate 不承重 |
| 多個 member 看似會通過 | first confirmation PASS 即停；後續 member 保持未觀察，禁止 argmax |
| 全部 member無 confirmation PASS | `BOUNDED-SEARCH-EXHAUSTED`，只限 closed family 11 |
| 出現本表未涵蓋 case | `PREREGISTRATION-UNSPECIFIED` 並停止 |

任何 PASS 都只對 1+1D evaluator／selector contract 有效；不證明 order-only $K$ 存在、不等於
Stage 5C-1 PASS、不授權 3+1D 或「已導出 spinor／chirality」敘述。

---

## 8. Freeze closure matrix

只有每一列都有具名文件、source-of-record、tests、numerical constants／bounds、seed manifest
與獨立 review，狀態才可由 `OPEN` 改為 `CLOSED`。

| # | Closure item | 必要交付物 | 狀態 |
| :---: | :--- | :--- | :---: |
| 1 | typed $S_\theta$／pairing／adjoint／boundary prescription | 文件＋兩個 independent implementations＋mapping tests | `OPEN` |
| 2 | $\Pi_{\mathcal M}$ joint matched law | generator／matcher source-of-record＋paired covariance schema | `OPEN` |
| 3 | near-zero／ratio numerical certification | scale-aware formula＋error propagation＋boundary tests | `OPEN` |
| 4 | E1 joint contrast | estimand／2D region／effect floor／uncertainty | `OPEN` |
| 5 | E2 null equivalence | two null generators／region／TOST／cohort floor | `OPEN` |
| 6 | E3 planted family | complete domains＋active wrong-support Gate O/E＋swap arm | `OPEN` |
| 7 | E4 well-posedness | fixed-scale sequence／contact／boundary／agreement criteria | `OPEN` |
| 8 | E5-D／E5-E multiplicity與 power | complete claim family＋spending＋power audit | `OPEN` |
| 9 | selection／confirmation manifests | fresh disjoint bases＋burn lifecycle＋non-recycling | `OPEN` |
| 10 | runner／ledger／adjudicator freeze | fail-closed executable implementation＋end-to-end dress test | `OPEN` |
| 11 | exhaustive decision table | §6–§7 與 runner state machine逐列一致 | `DRAFT` |
| 12 | independent review／CI／merge | review record＋green CI＋main commit | `OPEN` |

Closure rule：**12 列全部 `CLOSED` 才能把文件狀態改為「preregistration frozen」。** 若只完成
部分列，STATUS 必須逐列保留 `PENDING`，不得以百分比或「接近完成」暗示執行授權。

---

## 9. 下一段工作的合法順序

1. 先由獨立 review 檢查本 draft 是否完整捕捉既有 hard constraints，尤其 §6–§7 是否仍有
   未列出的分支；
2. 分別交付 typed continuum pairing／active wrong-support／E4 numerical certification；
3. 在前述 objects 全部固定後，才作不讀 arm data 的 power／multiplicity preregistration；
4. 再凍結 runner、ledger、adjudicator與一次性 fresh lifecycle；
5. 全部 review／CI／merge 後，才可生成第一個 6a-E seed。

本文件合併本身**不**讓上述任何一項從 PENDING 變為 DELIVERED，也不授權開啟現有 raw
ledgers。若後續發現本 draft 漏列情形，唯一合法動作是先修 draft；不是在執行時補判準。
