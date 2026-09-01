# Stage 5C — C8 Selector Family $\Sigma$：結構定義

狀態：**【candidate-independent 結構交付物；尚非完整 selector prereg／尚未 freeze】**。

本段只固定 C8 intrinsic selector 的型別、有限 family、順序、capacity 與 provenance。不執行
6a-S、不讀 between-target contrast、不設計候選 $K$。完整 6a-S 尚需 $\varphi$、$\mathcal N$、
induced-measure metric、effective-sample-size 與數值門檻另行凍結。

歷史基準：main `e5a6f2b`（64 檔、integrity 通過、184 passed）。

---

## 0. 本輪裁決與原草案更正

1. **不把 $\Delta r_U,\Delta r_V$ 引入 C8 selector。** 它們仍是 handoff §2.3 記錄的
   candidate materials；現行 STATUS 沒有授權把它們加入 acceptance path。若未來要用，須
   明文 protocol amendment，不得以「只用來出考卷」作默示豁免。
2. **active wrong-support 不要求 C8 $\Sigma$ sector-aware。** E3 planted control 可使用 L4
   oracle，應在 gate-specific test-function／support／continuum-frame tuple 上定義；不能把
   C8 intrinsic selector 與 C7/E3 oracle selector 合併。
3. 原實作聲稱只接受 `BlindedCase`，實際卻接受裸 `ndarray`。本版把 API firewall、poset
   validation 與 payload falsifier放進 source-of-record。
4. 原 coverage 帶 $[0.005,0.60]$ 沒有 provenance，且 $0.60$ 上限會排除最小 primitive
   `all_relations`。本版只報 raw coverage；數值 floor 等待 $\varphi/\mathcal N$ 與 power
   contract 一起預登記。
5. 「誘導測度必須偏離均勻」不是 selector 的必要條件，且與 observable contract §6.2 的
   明文禁令衝突。concentration/divergence 只能作不改判的 secondary diagnostic。

---

## 1. 型別與介面

### 1.1 簽名

$$\Sigma:\ \texttt{BlindedCase}\longrightarrow\mathcal S\subseteq\mathcal D,$$

$$\mathcal D(C)=\{(x,y):x\prec y\}.$$

輸入只有 opaque `case_id` 與 square Boolean transitive-closure relation matrix。輸出是無重複的
ordered-pair 集合，不含權重。裸矩陣、座標、$\theta$、target、seed、候選輸出或額外 payload
一律拒絕。

### 1.2 與 $\varphi,\mathcal N$ 的介面

$$\mathcal S=\Sigma(C),\qquad
M_C=\sum_{(x,y)\in\mathcal S}\varphi_C(x,y)G_R^C(x,y),\qquad
\mathcal O_C=\mathfrak I_G(M_C).$$

$\Sigma$ 只決定 pair membership；$\varphi$ 給權重；$\mathcal N$ 進入 $\varphi$/measure 的
正規化。若日後改成 selector 自己輸出權重，屬 protocol amendment，不是介面澄清。

### 1.3 結構錯誤與 verdict 的界線

- malformed／leaky payload、未登記 member 或 parameter：`SelectorProtocolError`；若進入 gate，
  對應 `PROTOCOL-INVALID`。
- $\mathcal D=\varnothing$：`SelectorDomainError`；是否列 OUT-OF-DOMAIN 及其排除率門檻，須在
  完整 6a-S prereg 固定。
- $\mathcal D\ne\varnothing$ 但某 member 選不到 pair：`SelectorSelectionError`，是 S1/S6
  feasibility failure，不得偷換成 OUT-OF-DOMAIN。
- raw coverage 只報告，不在本輪用未證成的上下界改判。

---

## 2. 不變性與防回流

- **Relabel covariance**：若 $O'[i,j]=O[\pi(i),\pi(j)]$，則新 pair $(i,j)$ 對應舊 pair
  $(\pi(i),\pi(j))$。反推用 $\pi$，不是 `argsort(π)`；測試含非 involution falsifier。
- **Sector swap**：本輪 C8 family 完全不讀 $\{U,V\}$，故為 sector-blind。
- **禁止讀取**：候選 $K$／$G_R$ 值、$\mathfrak I_G$、target／$\theta$、coordinates、seed、
  reference-probe bank／weights／scores、realizer ranks。
- **Firewalls**：`analysis/stage5c_selector_family.py` 的 public evaluator 只接受現有
  `analysis.stage5c_hard_controls.BlindedCase`；額外欄位或裸 `ndarray` 皆會失敗。

---

## 3. 凍結的 C8 family

評測順序如下；member 內按參數列順序。capacity 是參數點數，不是四個名稱。

| 順序 | member | 凍結參數點 | capacity | 獨立 provenance |
| :---: | :--- | :--- | ---: | :--- |
| 1 | `all_relations` | `()` | 1 | $\mathcal D$ 本身；最少額外 primitive、完整非局域 baseline |
| 2 | `links` | `()` | 1 | C8.1 已凍結的 link-density 診斷；選全部 links，不選單一鄰居 |
| 3 | `interval_exact` | $m=1,2,3,4$ | 4 | C8.1 已凍結的 interval-abundance orders |
| 4 | `source_depth_band` | $[0,.2),[.2,.4),[.4,.6),[.6,.8),[.8,1]$ | 5 | C8.1 已凍結的 height-CDF endpoints |

總 capacity **11**，closed limit 亦為 **11**，不保留可事後填入的 12–24 空位。任何新增、
刪除、改順序或改 grid 都是 protocol amendment。

### 3.1 Candidate-material firewall

`interval_exact` 的 provenance **不是** handoff §2.3。interval orders $1\ldots4$ 已在 C8.1
matching protocol 中以 evaluation-only nuisance covariates 獨立凍結；本輪只沿用該既有
evaluator 定義。這不授權候選 construction import $|I(x,y)|$，也不得把 selector 成敗或
member 順序回流成候選建議。

`valency_band` 自原草案移除：其唯一具體來源靠近已隔離的 reference-probe bank，違反 §2 的
no-bank-input 規則。原 quartile depth grid亦改回既有 C8.1 的 $0.2$ endpoints，避免另造沒有
provenance 的 constants。

### 3.2 完整 capacity ledger

每個 member 除參數點數外，source-of-record 另固定：form 字串及 byte-length、source
dependencies、branch count、free-parameter count、lookup entries、optimizer 與 RNG。四個
member 均無 optimizer、RNG、lookup 或連續自由參數。固定 grid 的每一點已各計一次 capacity。

---

## 4. Tier 2 與 active wrong-support 的裁決

原草案主張「wrong-support 必須有 sector-aware C8 selector 才有著力點」。這把 unified typed
architecture 誤讀成所有 gate 必須使用同一 selector，與 observable contract §3.2、§7 衝突。

正確分工是：

- $\Sigma_{C8}$：本文件的 intrinsic、sector-blind family；只負責 C8 distributional test。
- $\Sigma_{C7/E3}$／test-function support mapping：可依已登記 L4 continuum frame、
  $\iota_{\rm sf}$ 與 planted object 定義 passive swap 及 active wrong-support；不得回流 construction。

因此 `sector_rank_band`／`sector_asymmetry_band` **不列入**本 family，也不預留名稱或 capacity。
這不是證明它們不可能；只是依現行規格不授權。若日後另案提議 order-only sector-aware
selector，必須先走 protocol amendment，另解 $\kappa>1$ orbit、enumeration cap、sector-swap
covariance、capacity 與 candidate-material firewall。

active wrong-support E3 仍 PENDING，但不再被錯誤地綁成 C8 selector 的 tier 2。

---

## 5. Concentration 與 coverage 的正確角色

observable contract §6.2 已明定：$\mu_+\ne\mu_-$ 或 relative-to-uniform divergence 不是普遍
必要條件。即使 induced measure 相同，continuum $S_\theta$ 仍可能讓 endpoint 不同；反之，
measure 不同亦可能經 $\mathfrak I_G$ 抵消。

所以本輪只許報告：selected-pair count、raw coverage、各 target 內 block stability，以及未來
weighted measure 的 total variation／ESS。任何 relative-to-uniform concentration 指標若保留，
只能是**不參與淘汰、不改順序、不承重**的 secondary diagnostic。

---

## 6. 現在能測什麼

本輪  structural regressions 鎖定：

- `BlindedCase` firewall、poset 型別、domain/subset/uniqueness；
- relabel covariance，並證測試會拒絕錯誤的 inverse permutation；
- family/grid/order、half-open boundary convention、capacity 與完整 ledger；
- `all_relations` coverage 恰為 1，避免以無 provenance 上限排除最小 selector；
- empty domain 與 empty selection 的不同型別。

這些只是 6a-S 的**結構前置**，不能記成 6a-S PASS。完整 6a-S 還要先凍結 $\varphi$、
$\mathcal N$、induced-measure distance、ESS、coverage/exclusion thresholds、cohort floor、seeds
與 failure semantics，且使用與 6a-E 不相交的資料流。

因此下一個 commit **不得直接執行完整 6a-S**。下一步應先完成 smearing／normalization／
6a-S numerical prereg；只有其 commit 固定後才可執行 6a-S。

---

## 7. 範圍與狀態

本文件未使用候選輸出、target contrast、holdout、reference-probe success pattern 或
handoff candidate materials 來選 member。它不證明 selector viable、不證明 E3 viable，也不
蘊涵 order-only $K$ 存在。

D.1 第 3 項、active wrong-support E3、完整 selector prereg 與 Freeze-1a 均維持 **PENDING**。
