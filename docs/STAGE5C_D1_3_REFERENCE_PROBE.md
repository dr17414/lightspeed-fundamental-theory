# Stage 5C D.1 第 3 項 — Reference-Probe Feasibility 預登記

狀態：**【已確認／預登記完成；尚未執行】**。本文件所列 protocol 必須先 commit，
且該 commit hash 必須寫入執行 manifest，才可執行任何一次 probe run。

基準：`docs/STAGE5C_ACCEPTANCE.md` v0.8、`docs/STAGE5C_C8_4_HARD_CONTROLS.md`（修訂後）。

---

## 0. 本文件是什麼、不是什麼

**是**：判定目前 C8.4 control 在 matching 之後**是否仍保有可被 order-only 構造偵測的
資訊**的一份預登記檢定計畫。它屬於「出考卷」，不屬於「寫答案」。

**不是**：

- 不提出、不暗示、不評估任何候選 kernel $K$；
- 不宣稱任何 probe 的輸出是 Dirac propagation、chirality、spinor 或任何物理量；
- 不產生可供候選設計參考的 feature、權重或成功模式。

執行本計畫後只公開 §6 的判決與 arm-level 樣本數、效應量、$p$ value；feature 權重、
族別貢獻、逐樣本分數及任何成功模式均留在 evaluator-side sealed artifact，**不得**以
任何形式進入候選設計。不存在額外 binary 或摘要回流通道。

---

## 1. 要回答的問題

C8.4 已確認 **matchability**：存在固定 protocol 能把 $T_+$、$T_-$ 在 11 維 global
baseline 上平衡到門檻。但匹配前的 signed SMD 顯示，local density 差異大量洩漏進全域
統計（`height_over_sqrt_n` 達 $0.43$–$0.51$ SD，四組同號），而 matching 正是把它們
配平掉。

因此未知的是 **residual discriminability**：

> 條件於 11 維 baseline 之後，matched cohort 是否仍保留 $T_+$ 與 $T_-$ 的可偵測差異？

**為什麼必須先答**：若殘餘 power 實為零，則每一個候選都會拿到 Axis B FAIL，而該失敗
會被誤記為候選的失敗。這是本專案反覆致命的失效模式的新變體——不是「$R$ 進不去」，
而是「$R$ 被 matching 吃掉」。

---

## 2. 技術前提：Layer 1 不能用 $L_\theta$ 本身

$L_\theta=\frac14\log\frac{p_\theta(s)}{p_\theta(t)}$ 是**純 continuum 常數**，對同一
target 的每個樣本完全相同、與抽樣無關。因此「$L_+-L_-$ 在 matched cohort 上是否仍
存在」若照字面理解，答案恆為是，而該問題是空洞的。

Layer 1 必須改用**樣本層級的 oracle estimator**：由該樣本自身的 sealed 座標估計同一個
continuum 對比量。只有這樣，「matching 是否把物理對比本身選掉了」才是一個可證偽的問題。

---

## 3. Layer 1 — Continuum-oracle probe

**目的**：確認 matched cohort 上，**連續物理對比本身**仍然存在。這是 Layer 2 的必要前提。

**估計量（預登記，執行前不得更改）**：對每個 causet，用其 sealed 座標 $\{(u_i,v_i)\}$
計算

$$
\widehat L=\tfrac14\bigl[\log\hat\rho(s)-\log\hat\rho(t)\bigr],
$$

其中 $\hat\rho$ 的定義完全固定如下。令

$$B_h(x)=\{(u,v)\in[0,1]^2:|u-x_u|\le h,\ |v-x_v|\le h\},\qquad h=0.12,$$

$A_x$ 為該截斷矩形的解析面積、$C_x$ 為 causet 的 $N=96$ 個點落入 $B_h(x)$ 的個數，
並取 Jeffreys-smoothed histogram density

$$\hat\rho(x)=\frac{C_x+1/2}{(N+1)A_x}.$$

$s=(0.05,0.05)$、$t=(0.50,0.05)$ 與 C8.4 §3.1 相同。矩形為閉集；連續抽樣下邊界
命中機率為零。$+1/2$ 明確處理零計數；截斷面積校正明確處理 $s,t$ 鄰近邊界。
$h$、kernel、平滑與面積公式在執行前固定，不得依結果調整。此 estimator 只需作
candidate-independent control diagnostic，不宣稱是最優或無偏的 $L_\theta$ estimator。

**檢定**：對 witness split 的 matched pairs $\{(A_i,B_i)\}$ 取
$\Delta_i=\widehat L(A_i)-\widehat L(B_i)$，以 paired sign-flip randomization
（$200{,}000$ 次，加一修正 $p=(b+1)/(200001)$）檢定 $\mathbb E[\Delta]=0$。

**門檻**：方向必須為 $T_+>T_-$；標準化 paired effect
$\mathbb E[\Delta]/\mathrm{sd}(\Delta)\ge0.30$，且通過 §4.6 的 multiplicity gate
（與 C8.4 §6 的 Axis-B floor 一致）。

**注意**：Layer 1 讀取座標，屬 L4 evaluation oracle。它**只**用於判斷 control 是否還活著，
**不**能作為「未來只讀 order 的 $K$ 看得見」的證據。這正是必須有 Layer 2 的理由。

---

## 4. Layer 2 — Order-only information witness

**目的**：確認**只用候選可取得的 order data**，matched cohort 是否仍保留可偵測資訊。

### 4.1 允許的輸入

只有 relation matrix $R$。不得接觸座標、$\theta$、target label、seed、$\widehat L$、
Layer 1 的任何輸出。以 C8.4 §7 既有的 `BlindedCase(case_id, copy_of_R)` 介面取樣。

### 4.2 Order-feature bank（預登記，執行前固定，此後不得增刪）

刻意選為**通用、非幾何動機**的 label-invariant 全域摘要，且明確**不是** kernel 形式：

1. `interval_abundance_5..12`（baseline 只到 4）；
2. past-set 大小 $|{\downarrow}x|/N$ 的 empirical quantiles at $0.1,\dots,0.9$；
3. future-set 大小的同樣 9 個 quantiles；
4. 每個元素 past-depth $h_x/H$ 的 quantiles at $0.1,\dots,0.9$（baseline 只取 4 個 CDF 點）；
5. 對稱化矩陣 $R+R^{\mathsf T}$ 的前 8 個最大特徵值，除以 $N$。

共 $8+9+9+9+8=43$ 維。所有 quantile 使用 NumPy `method="linear"`；past-depth 是從
minimal elements 到 $x$ 的最長鏈所含關係數（minimal elements 為 0），$H$ 使用同一
慣例；八個 eigenvalues 依代數值遞減排序並計重數。選這 5 族的理由只有「通用且易
計算」；**不得**以任何物理動機描述之。實作若無法逐位元重現這些定義，判
PROTOCOL-INVALID，不得臨場換定義。

### 4.3 對 baseline 正交化（關鍵步驟）

matched cohort 的 11 維 baseline 仍有殘餘失衡（max SMD $\approx0.11$–$0.17$）。若不處理，
probe 可能只是撿到殘餘失衡，而非新資訊。

因此每個 arm 各自在其 **calibration split** 上，把 43 維 bank 的每一維對含截距的
11 維 baseline 做 ordinary least squares，保存係數；在該 arm 的 **witness split**
上只套用凍結係數取殘差。不得用 witness 資料重估係數。這保證 calibration-sample
內的線性正交，並把同一預先固定的 residualization map 外推至 witness；**不得誇稱
witness sample 的 empirical correlation 必然精確為零**。

### 4.4 Probe 形式（固定，不得調參）

對殘差化後的 43 維做 ridge least-squares linear score。每欄先用該 arm calibration
split 的 mean 與 population SD（`ddof=0`）標準化；零 SD 判 INCONCLUSIVE，不得刪欄。
令 label $y\in\{+1,-1\}$，以不懲罰截距、懲罰係數的

$$\min_{a,\beta}\sum_i(y_i-a-z_i^{\mathsf T}\beta)^2+\lambda\lVert\beta\rVert_2^2,
\qquad\lambda=1.0$$

唯一解定義 $s(z)=a+z^{\mathsf T}\beta$。只在 calibration split 擬合，再原封不動
套到 witness split。**沒有 hyperparameter search、模型選擇、threshold tuning 或
早停。** 三個 arms 各有自己的凍結 residualizer／standardizer／score；不得共用
witness 資訊。

### 4.5 三個 arm（缺一不可）

| arm | 內容 | 預期 | 作用 |
| :--- | :--- | :--- | :--- |
| **N（null）** | 兩個獨立 $T_+$ pseudo-arms（不同 seed blocks），以 pseudo-arm 身分套用同一 matching | 不應偵測到 | 校準 false-positive；確認 matching 本身不會製造結構 |
| **P（positive）** | $T_+$ vs $T_-$，**未匹配** | 應強烈偵測到 | 儀器可用性檢查 |
| **Q（question）** | $T_+$ vs $T_-$，**已匹配** | 未知 | 真正要回答的問題 |

**Arm P 是必要的.** 沒有它，Q 的 null 結果無法區分「殘餘資訊為零」與「儀器壞掉」——
本專案已有 evaluator-floor 假象的前例。

### 4.6 檢定與門檻

Arm Q 與 N 在 **witness split** 的 matched pairs 上取
$\Delta_i=s(A_i)-s(B_i)$，作 $200{,}000$ 次 paired sign-flip randomization。
Arm P 不做 matching，兩側樣本獨立，故以 witness labels 的 $200{,}000$ 次
equal-size label permutation 檢定兩側 mean-score difference；**不得**為了共用程式
而把未匹配樣本任意配成 pairs。所有 Monte Carlo $p$ values 使用加一修正。預登記：

- Arm P：必須偵測到（方向 $T_+>T_-$、以 witness pooled SD 標準化的 unpaired
  mean difference $\ge0.30$，且通過 multiplicity gate）。**未通過即
  儀器不可用，整份計畫判 INCONCLUSIVE，不得對 Q 作任何解讀。**
- Arm N：不是以「$p>0.01$」接受虛無。預登記等效界 $\delta_N=0.15$；以 paired
  standardized mean 的 two-one-sided $t$ tests（TOST）檢定
  $H_0:d_N\le-0.15\ \text{or}\ d_N\ge0.15$。只有通過 multiplicity gate 才證成
  operational equivalence。未通過一律判 INCONCLUSIVE；若另有方向差異證據，只能
  標為疑似 protocol bias，Q 結果仍作廢。
- Arm Q：方向 $T_+>T_-$、標準化 paired effect $\ge0.30$，且通過 multiplicity gate，
  才算偵測到。

多重性：本計畫共 4 個預登記 claims（Layer 1 difference、P difference、N equivalence、
Q difference）。N 的 claim $p$ 是兩個 one-sided $p$ 的較大者；其餘三者用上述
randomization $p$。以 Holm–Bonferroni 在 family-wise $\alpha=0.01$ 下控制；PASS 使用
Holm-adjusted 判決，不以各自 raw $p<0.01$ 取代。此為完整 claim 清單，執行後不得新增。
方向條件與 effect floor 仍須另行同時滿足。

Monte Carlo streams 亦預先固定：對 claim name `layer1`, `P`, `Q` 分別計算
`SHA256("stage5c-d1-3-v1|" + claim_name)`，取 digest 前 8 bytes 作 little-endian
unsigned integer，初始化 NumPy `PCG64DXSM`。N 使用解析 $t$ distribution，不耗用
randomization stream。不得因 Monte Carlo 邊界結果更換 seed 或增加 draws。

### 4.7 資料切分

C8.4 已 burned 的 blocks 不得使用。P/Q 共用同一批 raw samples（P 在 matching 前、
Q 在 matching 後），N 使用完全獨立的 $T_+$ pseudo-arm samples：

- P/Q calibration：3 個 C8 blocks；P/Q witness：3 個 C8 blocks；
- N calibration：3 個 null blocks；N witness：3 個 null blocks。

每個 C8 block 有四段、每段 768 seeds（matching-scale $+/-$、evaluation $+/-$）；每個
null block 亦有四段、但四段均由 $T_+$ 生成，前兩段提供 matching scale，後兩段是
兩個 evaluation pseudo-arms。令 `M=1_100_000_000`：P/Q 的 block $b=0,\dots,5$、
segment $j=0,\dots,3$ 使用

$$[M+10{,}000{,}000b+1{,}000{,}000j,\ M+10{,}000{,}000b+1{,}000{,}000j+767].$$

令 `M_N=1_200_000_000`，N blocks 依同一公式替換 $M$ 為 $M_N$。$b=0,1,2$ 為
calibration，$b=3,4,5$ 為 witness。RNG 固定為 PCG64DXSM；生成、matching 與 opaque
blinding 全沿用 C8.4。以上 48 段在本文件 commit 後即視為 reserved，首次生成後全部
burned；不得替換失敗 block。

每個 Q/N witness block 必須各自先通過 C8.4 的 pairs／coverage／SMD／KS gates；三個
blocks 合併後至少有 $3\times192=576$ pairs。P 每側固定使用三個 witness evaluation
pools，共 2304 samples。以最保守 Holm 首階 $\alpha=0.0025$ 的常態近似，$n=576$ 的
paired test 對 $d=0.30$ 具 power $>0.999$；因此原文件所稱「power 已固定」現在有
明確的樣本下界。若 cohort gate 未達，判 INCONCLUSIVE，不得縮小 effect floor。

witness split **揭露一次即 burned**；若需第二次，必須另立 protocol amendment、
重新 freeze，且不得重用任何上述 seed。

依 acceptance spec §5.3，本計畫全部為 candidate-independent protocol development，
**不消耗** candidate confirmatory budget，但必須完整寫入 `docs/stage5c_development_log.md`。

---

## 5. 防止 reference probe 變成偷渡的候選答案

以下為硬性規定，違反者相應 gate 判 **PROTOCOL-INVALID**。

1. **不輸出、不建議任何 kernel 公式或 kernel 形式的物件。** probe 是純量分數函數，
   不是 $\mathcal C\times\mathcal C$ 上的 kernel，也不得被改寫成一個。
2. **不使用任何候選輸出。** 本計畫執行時，候選尚不存在；若未來重跑，仍不得讀取候選輸出。
3. **不回流.** probe 的 ridge 權重、各族貢獻、混淆矩陣、逐樣本分數、
   任何「哪一族有效」的資訊，**不得**出現在候選設計者可見的任何文件、對話或 commit
   message 中。執行後這些數值封存於 evaluator side。
4. **座標、$\theta$、target label、seed、$\widehat L$ 只存在 evaluator side.** Layer 2
   的執行路徑只能接收 `BlindedCase`。須以 C8.4 §7 既有的 payload-key falsifier 測試涵蓋。
5. **語意上限.** Layer 2 的結果只能回答「殘餘資訊是否存在」。**不得**被稱為 Dirac
   propagation、chiral transfer、幾何辨識或任何物理陳述。撰寫結論時只許使用
   「residual information detected / not detected」。
6. **執行前固定.** probe family、正交化方式、$\lambda$、$h$、三個 arm、門檻、power、
   多重性規則、切分與失敗判決，全部由本文件固定；freeze 後不得更改。
7. **失敗的語意上限.** 若 Layer 2 失敗，結論只能是「目前的 C8 control 未證明具有
   residual power（相對於本文件所宣告的 probe bank $\mathcal G_{\text{probe}}$）」。
   依 acceptance spec §9.4.1 記為 **BOUNDED-SEARCH-EXHAUSTED**，**不得**宣稱不存在
   任何可行 evaluator，也不得宣稱不存在能看見該差異的 $K$。

### 5.1 不設 binary 回流通道

先前草案擬揭露「殘餘資訊是否屬 C8.1 可新增 global-scalar 類」的 binary；本版刪除。
該 bit 仍會縮小未來構造搜尋空間，而且沒有執行必要性：C8.1 已要求**每一個**新增
covariate 在 candidate-independent qualification split 證明不會消滅 contrast，無須先
知道 residual information 落在哪一類。任何依 probe 結果決定新增 covariate、matching
清單或 qualification test 的行為均判 PROTOCOL-INVALID。

---

## 6. 第一個判決點

| Layer 1 | Layer 2 (arm Q) | 判決 | 後續 |
| :--- | :--- | :--- | :--- |
| PASS | PASS | **CONTROL-VIABLE** | 繼續撰寫統一的 observable／selector／smearing／norm contract |
| PASS | FAIL | **CONTROL-UNFAIR-RISK** | 連續物理對比仍在，但 order-only 通道未證明可見。C8 對候選可能不公平，**必須修改或撤回 control**；語意依 §5 第 7 項為 BOUNDED-SEARCH-EXHAUSTED |
| FAIL | — | **CONTROL-DEAD** | matching 已把物理 contrast 本身吃掉，**立即撤回目前 protocol**，不得再用於任何候選 |
| arm P 失敗，或 arm N 未證成等效，或算力不足 | — | **INCONCLUSIVE** | 記為未決項並說明所需資源；**不得**當作候選 FAIL，也不得當作 control 的負面證據 |

四個 claims 必須在同一次 sealed witness revelation 中全部計算，才能套用預登記的
Holm family；判決時才依本表 gatekeeping。Layer 1 FAIL 時 arm Q 雖已機械計算，仍不得
解讀或公開為 residual-power 證據。

**任一非 CONTROL-VIABLE 的判決都不得以放寬 caliper、放寬門檻或更換 probe bank 的方式
繞過。** 更換 probe bank 屬 protocol amendment，須進 amendment ledger 並重新 freeze。

---

## 7. 執行順序

1. freeze 本文件（與 C8.4 修訂一併 commit）；
2. 依 §4.7 已固定的 seed ranges 產生 calibration／witness blocks，寫入 RNG/hash manifest；
3. 擬合三個 arms 各自的正交化係數與 ridge score（僅 calibration split）；
4. 一次揭露 sealed witness split，計算 Layer 1 與 P/N/Q 四個預登記 claims；
5. 套用 Holm correction，再依 §6 的 gatekeeping 解讀；P/N 或 Layer 1 未通過時，Q
   不作實質解讀；
6. 記錄判決、arm-level $n$/effect/$p$ 與 burned seeds；其餘輸出封存且不回流；
7. 依 §6 決定是否進入統一 evaluator contract 的撰寫。

---

## 8. 本文件刻意不固定的事

- 統一 observable／selector／smearing／norm contract 的內容——那是 §6 判 CONTROL-VIABLE
  之後才動筆的東西，先寫會浪費，也可能被本計畫的結果推翻；
- 任何 $K$ 的形式；
- C9/C10 的 immutable core（屬 D.1 第 7 項）。
