# Stage 5C C8.4 — 定義域內困難對照可行性與預登記草案

狀態：**【已確認／核心可構造性成立；尚未構成 Freeze-1a】**

本文件處理 `STAGE5C_ACCEPTANCE.md` 附錄 D.1 第 5 項，並給出第 4 項
matching protocol 的第一個完整可執行實例。結論是：**在不設計、讀取或執行任何
候選 kernel $K$ 的前提下，確實可以構造一組位於 1+1D／order-dimension-$\le2$
定義域內、低階 order statistics 可匹配、但 continuum massless-chiral target
預先已知不同的困難對照。** 因此目前不應判
`BOUNDED-SEARCH-EXHAUSTED` 或 `SPEC-INFEASIBLE`。

這只是 Freeze-1a 前的 candidate-independent feasibility artifact。依定稿規格，
附錄 D.1 九項仍須全部完成，並在一個明確引用
`docs/STAGE5C_ACCEPTANCE.md` v0.8 定稿 commit 的單一 freeze commit 中固定，才算
Freeze-1a；本文件與本輪程式 commit 本身都**不是** freeze。

---

## 1. 對照族

在 null square $(u,v)\in[0,1]^2$ 定義

$$
q(z)=6z^2-6z+1,
\qquad
p_\theta(u,v)=1+\theta q(u)q(v),
\qquad
\theta\in\{+0.4,-0.4\}.
$$

連續 metric 與體積形式取為

$$
ds_\theta^2=-2p_\theta(u,v)\,du\,dv,
\qquad
dV_\theta=p_\theta(u,v)\,du\,dv.
$$

兩個 target 分別稱為 $T_+$（$\theta=+0.4$）與 $T_-$（$\theta=-0.4$）。
有限 control causet 是在 $dV_\theta$ 上做 Poisson sprinkling、再條件化於固定元素數
$N$；等價地，條件化後的點為從 $p_\theta$ 抽出的 iid 樣本。程式以 rejection
sampling 實作，不把 $\theta$ 或座標交給未來候選。

選 $|\theta|=0.4$ 不是讀取候選後調參。它在候選存在前固定，並同時保有：

1. 嚴格正密度：$q\in[-1/2,1]$，故 $p_{+0.4}\ge0.8$、
   $p_{-0.4}\ge0.6$；
2. 足夠重疊的低階統計分布，可做非平凡 matching；
3. 明確且方向相反的 continuum chiral-transfer target。

---

## 2. 為何兩側都在定義域內

### 2.1 解析 domain proof

$p_\theta>0$ 只改變 volume density，不改變 causal cones。任一有限樣本定義

$$
x\prec y
\quad\Longleftrightarrow\quad
u_x<u_y\ \text{且}\ v_x<v_y.
$$

令 $U$、$V$ 分別為依 $u$、$v$ 排序的兩個線性序，則
$P=U\cap V$。因此每個樣本都有顯式二元 realizer，
$\dim(P)\le2$；不可能像舊的 $D=3$ control 那樣因 dimension $>2$ 被標為
OUT-OF-DOMAIN。連續抽樣下座標 tie 的機率為零。唯一可能的低維退化是所有點
恰成一條 chain，此時 $\dim(P)=1$；若 Freeze-2a domain 要求「恰為 2」而不是
「至多 2」，chain 必須以 candidate-independent predicate 標記 OUT-OF-DOMAIN，
不得靜默保留。source-of-record 四個 pools 的 chain count 均為 0。

若未來候選在 Freeze-2a 把 domain 限縮至 $\kappa=1$，則必須先以同一
candidate-independent predicate 過濾兩側，再在 $\kappa$ stratum 內匹配。固定
$N=96$ 的補充稽核結果為：

| 稽核 | $T_+$ | $T_-$ |
| :--- | ---: | ---: |
| seeds `710000000..710000127` / `720000000..720000127` | $116/128$ 為 $\kappa=1$ | $127/128$ 為 $\kappa=1$ |
| calibration seeds `730000000..730000255` / `740000000..740000255` | $245/256$ | $249/256$ |
| validation seeds `750000000..750000255` / `760000000..760000255` | $243/256$ | $249/256$ |

在最終 11 維 baseline 下重跑最後一組 validation，取兩側前 243 個
$\kappa=1$ 樣本後只保留 60 對：coverage $0.2469$、max SMD $0.2146$、
max KS $0.1334$。但這個 raw pool 只有 256；同 seeds 的**未過濾** control 也只得
60/256 對、coverage $0.2344$、max SMD $0.2139$。故該失敗不能歸因於
$\kappa=1$，它只證明 256-per-target 不足以承重任何 domain 的可行性結論。

以 source-of-record seeds 將 raw pool 增至 512，$\kappa=1$ retained counts
（calibration $T_+/T_-$、validation $T_+/T_-$）為
$490/496/492/493$；依固定規則在各 split 取兩側前
$\min(n_+,n_-)$ 個 retained samples（retained seeds 依整數 seed 升序，不依任何
feature 或 target-local quantity 排序），filter-then-match 得 194/492 對、coverage
$0.3943$、max SMD $0.1297$、max KS $0.1340$，已通過全部 gate。正式 768 raw-pool
基準的 retained counts 為 $733/746/732/738$，取 $733$ calibration 與 $732$
validation per target 後得：

| 指標 | $\kappa=1$ 結果 | threshold |
| :--- | ---: | ---: |
| matched pairs | 343 | $\ge192$ |
| coverage | 0.468579235 | $\ge0.35$ |
| max absolute SMD | 0.168554669 | $\le0.20$ |
| max KS distance | 0.113702624 | $\le0.18$ |

同一 768-pool 的兩個 splits 合計 retention 為 $T_+$ 的 $1465/1536=0.9538$
與 $T_-$ 的 $1484/1536=0.9661$；兩比例 z-test 的 $|z|=1.75$（雙尾
$p\approx0.080$），未檢出 target-dependent retention，但這不是二者相等的證明。
**結論改為：完整 dimension-$\le2$ 與 $\kappa=1$ 限縮 domain 均已證實在固定
protocol 下可執行；256-pool 負結果保留為 sample-size sensitivity，不再作
$\kappa$ 的負面證據。**

### 2.2 三個「容易量」在解析上已匹配

shifted Legendre mode $q$ 滿足

$$
\int_0^1q(z)\,dz=0,
\qquad
\int_0^1zq(z)\,dz=0.
$$

因此兩側都具有：

1. 總體積 $\int p_\theta\,du\,dv=1$；
2. 完全均勻的 $u$、$v$ marginal；
3. 兩個 iid 點的 comparability／ordering fraction 期望值精確為 $1/2$。

第三項不是模擬觀察。將 joint CDF
$F_\theta(u,v)=uv+\theta Q(u)Q(v)$（$Q'=q$）代入
$2\int p_\theta F_\theta$；所有含 $\theta$ 的項分別由
$\int zq=0$、$\int Q=-\int zq=0$ 與
$\int qQ=[Q^2]_0^1/2=0$ 消去，只剩 $1/2$。

這使 control 不會退化成「看 $N$、marginal 或 relation density 就知道答案」。

---

## 3. 外部 continuum prediction

### 3.1 固定 primary control endpoint

令 $g_\theta=p_\theta\eta$，即 conformal factor
$\Omega_\theta=p_\theta^{1/2}$。二維 massless Dirac operator 的 conformal
covariance 為

$$
D_{g_\theta}\!\left(p_\theta^{-1/4}\psi_\eta\right)
=p_\theta^{-3/4}D_\eta\psi_\eta.
$$

因此沿同一 flat-null chiral characteristic，固定 source
$s=(0.05,0.05)$ 與 sink $t=(0.50,0.05)$，預登記 evaluator target

$$
L_\theta
=\log\frac{\psi_\theta(t)}{\psi_\theta(s)}
=\frac14\log\frac{p_\theta(s)}{p_\theta(t)}.
$$

得到

| target | $L_\theta$ | 預登記方向 |
| :--- | ---: | :--- |
| $T_+$ | $+0.08509340030565$ | 正 |
| $T_-$ | $-0.09060706134643$ | 負 |
| 差 $L_+-L_-$ | $+0.17570046165208$ | 嚴格正 |

這裡的座標、metric、$\theta$、source/sink 與 continuum Dirac formula 全是 L4
evaluation oracle；它們不得進 construction。此式由文件內完整的 conformal-weight
identity 承重，不依賴外部論文的未映射 prescription。Juhl et al.
[arXiv:1405.7304](https://arxiv.org/abs/1405.7304) 所列 Dirac conformal
bidegree $((n-1)/2,(n+1)/2)$ 只作公式 cross-check，不在本項取得 Freeze-1a
承重文獻資格。

### 3.2 不是被動 diffeomorphism 假差異

兩側不是把同一個 sprinkling 做 monotone re-embedding。它們是相對於各自
$dV_\theta$ 獨立抽樣的兩個 continuum ensembles。更強地說：兩側 $u,v$
marginal 都精確均勻；任何保持時間方向、分別單調作用於 $u,v$、又把均勻 marginal
推回均勻 marginal 的 map 幾乎處處只能是 identity。全域 sector swap
$u\leftrightarrow v$ 也保持 $q(u)q(v)$，不會把 $+\theta$ 變成 $-\theta$。
故兩 target 不是由允許的座標重命名或 $S_2$ sector swap 產生的同一個物理 target。

---

## 4. C8.1 精確 matching protocol 實例

同一 $N$ 內，對每個 causet 從 relation matrix $R$ 計算下列 11 維 nuisance vector；
所有量都是 whole-causet global scalars、label-invariant，且不讀 target metadata：

1. `relation_density`：$|R|/\binom N2$；
2. `link_density`：$N_0/\binom N2$，$N_0$ 為 open interval 空的 related pairs；
3. `height_over_sqrt_n`：whole-causet height $H/\sqrt N$，保留絕對高度尺度；
4. `height_cdf_0.2,0.4,0.6,0.8`：每個元素的最長鏈 past-depth $h_x$，除以
   whole-causet height $H$ 後，在四個固定 bin endpoint 的 empirical CDF；
5. `interval_abundance_1..4`：
   $N_m/\binom N2$，其中 $N_m=|\{(x,y):x\prec y,\ |I(x,y)|=m\}|$。

`link_density` 即 $m=0$，因此 interval abundance 不重複放 $m=0$。interval
abundance 作為 manifoldlike causal-set 診斷的文獻只作選擇此 nuisance family 的
動機；本項的定義與門檻由上列明文和 executable tests 承重。

這個 control 能同時保持低階平衡與非零 continuum contrast 的關鍵是：上述 11 項
只量 whole-causet global scalars，而 $T_+$／$T_-$ 的已知差異是 local conformal
density inhomogeneity。故 matching 不把定義 control 的 local profile 本身當成
nuisance 配平。未來不得為了改善表面平衡而加入 local profile、指定
source/sink/region 的 statistic，或任何 target-definition proxy。

匹配演算法固定為：

1. $N$ 與已宣告 domain stratum（例如 $\kappa=1$）做 exact matching；
2. 使用與 validation／confirmatory pools 分離的 calibration pools，計算每一維
   pooled sample SD $s_j$；$s_j=0$ 判 protocol failure，不可刪欄；
3. pair distance
   $d_{ab}=\sqrt{\sum_j[(x_{aj}-y_{bj})/s_j]^2}$；
4. 任一 component $|(x_{aj}-y_{bj})/s_j|>1.0$ 或 $d_{ab}>2.0$ 的 edge 無效；
5. 以 Hungarian assignment 先最大化有效配對數，再在此集合內最小化總距離；
   不重複使用樣本；
6. unmatched 樣本保留並完整報告，不得重新分類；
7. feasibility／confirmatory 最低 cohort conditions：coverage $\ge0.35$、
   matched pairs $\ge192$、每欄 absolute SMD $\le0.20$、每欄 two-sample
   KS distance $\le0.18$。任一不符即 INCONCLUSIVE，不得放寬或刪除變數。

候選在 Freeze-2a 只能**提議**增加符合 acceptance spec C8.1 provenance 限制的
nuisance covariates。新增項須為 label-invariant global scalar，並在不讀候選輸出的
candidate-independent qualification split 上仍通過全部 cohort／balance／power
門檻；若它解析上或實際上把 local continuum contrast 配平、使 Axis B 失去
可執行性，該新增判 PROTOCOL-INVALID 並不得加入，不能把它造成的失配轉記為 C8
INCONCLUSIVE。只有已先通過 qualification 的新增項，在 future fresh batch 因普通
抽樣變異失配時，才可記 INCONCLUSIVE。baseline 永不移除。

---

## 5. Source-of-record feasibility run

`analysis/stage5c_hard_controls.py::benchmark(n=96,pool_size=768)` 使用四個互不重疊
的 PCG64DXSM seed ranges：

| split | target | seed range |
| :--- | :--- | :--- |
| calibration | $T_+$ | `510000000..510000767` |
| calibration | $T_-$ | `520000000..520000767` |
| validation | $T_+$ | `530000000..530000767` |
| validation | $T_-$ | `540000000..540000767` |

結果：

| 指標 | 結果 | feasibility threshold |
| :--- | ---: | ---: |
| matched pairs | 361 | $\ge192$ |
| coverage | 0.470052083 | $\ge0.35$ |
| max absolute SMD | 0.161585461 | $\le0.20$ |
| max KS distance | 0.108033241 | $\le0.18$ |
| median standardized distance | 1.665519034 | pair caliper $\le2$ |
| p90 standardized distance | 1.904361143 | pair caliper $\le2$ |

所以這不是 KR-vs-sprinkling 那種不匹配就能分出的 easy control；超過一半樣本因
嚴格 pair caliper 未配對，保留下來的 cohort 才達到預定低階平衡。

### 5.1 為何 512 不再承重

原 512-pool source run 雖得 205 pairs／coverage 0.4004，但四組額外獨立 seed
blocks 顯示該設計點在門檻邊緣：

| raw pool | seed block | pairs | coverage | pairs gate | coverage gate |
| ---: | :--- | ---: | ---: | :---: | :---: |
| 512 | `510/520/530/540M` | 205 | 0.4004 | PASS | PASS |
| 512 | `810/820/830/840M` | 197 | 0.3848 | PASS | PASS |
| 512 | `910/911/912/913M` | 181 | 0.3535 | FAIL | PASS |
| 512 | `920/921/922/923M` | 174 | 0.3398 | FAIL | FAIL |
| 512 | `930/931/932/933M` | 173 | 0.3379 | FAIL | FAIL |

只有 2/5 blocks 同時通過，因此 512 的單次正結果不能作 freeze 可行性的承重證據。
這不是 seed 挑選指控：原 seeds 在開跑前固定且自然；問題是未留 sampling-variation
餘裕。

### 5.2 768 的跨 seed replication

將唯一設計變更限制為 raw pool 由 512 增至 768；$N$、$\theta$、11 維 baseline、
calipers、matching 與所有門檻均不變。四個獨立 replication blocks 結果為：

| seed block（cal $+/-$；val $+/-$） | pairs | coverage | max SMD | max KS |
| :--- | ---: | ---: | ---: | ---: |
| `910/911/912/913M` | 356 | 0.4635 | 0.1360 | 0.0871 |
| `920/921/922/923M` | 305 | 0.3971 | 0.1269 | 0.0852 |
| `930/931/932/933M` | 312 | 0.4062 | 0.1055 | 0.0609 |
| `940/941/942/943M` | 330 | 0.4297 | 0.1328 | 0.0788 |

四組全部同時通過 pairs、coverage、SMD、KS，且最差值仍有可見餘裕。這些 seeds
只屬 development replication，全部 burned；表格證明的是 protocol feasibility，
不是 future candidate 的 confirmatory evidence。

---

## 6. Axis A／B power plan

此處只提出 candidate-independent 的效力下界預登記草案；候選的實際 Axis-A noise
$\sigma_\Delta$ 仍須在 Freeze-2a 登記並從獨立 calibration split 估計。

- **Axis A**：每個 target／density 至少 384 個 causets。以暫定雙側局部
  $\alpha=0.01$ 的常態近似，對兩個 density cells 各 384 個獨立
  causets，可用 power $>0.90$ 偵測 $0.30$ pooled-SD 的標準化 drift。
- **Axis B**：至少 192 個 C8.1 matched pairs。以 matched-pair SD 標準化，雙側
  $\alpha=0.01$ 下可用 power $>0.90$ 偵測 $0.30\sigma_\Delta$ 的平均差。
- 最終判決仍須同時滿足 C8.3：方向為 $T_+>T_-$，且 between-target effect
  顯著大於 Axis-A within-target fluctuation。單有 $p$ value 不構成 PASS。

上述數字來自
$\sqrt n\,0.30-z_{0.995}$ 的預登記 normal-approximation lower-bound check；
正式 Freeze-1a 整合時還須與 D.1 第 6 項的全域 multiplicity／spending rule 對齊。
若全域規則要求更小的局部 $\alpha$，只能增加樣本數，不得降低 effect floor。

對完整 dimension-$\le2$ control domain，768-pool source-of-record 保有 361 對；
對 $\kappa=1$ 限縮 domain，實際 filter-then-match 保有 343 對。兩者都超過
192-pair power floor；這裡沒有用 retention 比例外推。future Freeze-2a 若宣告其他
更窄 domain，仍須在候選輸出被求值前另做該 predicate 的 filter-then-match audit，
不得由本結果外推。

---

## 7. RNG／hash manifest 與 oracle isolation

RNG 明定為 NumPy `PCG64DXSM`；每個 causet 使用獨立整數 seed，不共享可變 RNG
stream。hash 是 sorted JSON header（`n,seed,theta`）、一個 LF、再接 little-endian
float64 coordinates 的 SHA-256。source-of-record validation 首樣本為：

| target | seed | SHA-256 |
| :--- | ---: | :--- |
| $T_+$ | 530000000 | `25d01daed468657e4bbbf646cba8ec2b6b4c74e2d2df356de3c9e204d1ee7795` |
| $T_-$ | 540000000 | `a0bffe5ee999152688750469c36d779c3735a4148e415cd38d67a65b10db8970` |

隔離契約：evaluator 先用獨立 blinding RNG 將兩 target 與所有 split 混合排序，
為每個 case 產生不含 seed／target 意義的 opaque id；future construction runner
只能接收 `BlindedCase(case_id, copy_of_R)`。opaque-id-to-sample mapping 必須保持
sealed，直到 construction outputs 已不可變地寫入 artifact。單樣本 API
`construction_payload(sample)` 同樣只回傳 `{"order": copy_of_R}`。`theta`、target
label、seed、coordinates、continuum metric、source/sink 與 $L_\theta$ 只存在
evaluator side。confirmatory blinding seed 在輸出 commit 前不得公開；上列
development seeds 公開不會被重用於 confirmatory。
CI 已固定以下 falsifiers：

1. construction payload key 集合嚴格等於 `{"order"}`；
2. blinded cases 只含 opaque id 與 order，且固定測試證明 invocation order 已打散；
3. baseline features 對事件任意 relabelling 不變；
4. 每個 control causet 都通過 dimension-$\le2$ comparability-graph 檢查；
5. RNG 首樣本 hash 固定；
6. 768-pool matching benchmark 必須保持預登記 coverage／pair-count／SMD／KS gates；
7. $\kappa=1$ filter 使用 Stage 5A 的 `kappa()` observable，而非 implication-class
   數量的替代 predicate。

這是 API-level isolation，不宣稱已完成 D.1 第 2／3 項所要求的完整 static taint／
module-boundary proof；後者仍是 Freeze-1a blocker。

---

## 8. 本輪結論與剩餘限制

### 已完成

- 找到 candidate-independent、domain-internal 的困難對照族；
- 給出兩側解析 domain proof；
- 給出不靠候選、方向預定的 continuum target；
- 將 C8.1 的低階項、binning、距離、caliper、matching、unmatched handling 與
  coverage/balance threshold 全部具體化；
- 完成 768-pool source-of-record、四組跨 seed replication、$\kappa=1$
  filter-then-match audit、power 下界與 RNG/hash manifest；
- 全程未設計或評估任何候選 $K$。

### 尚未完成

1. D.1 第 3 項尚須把 C6/C7/C8 primary observable、smearing 與 norm 統一；若其
   object contract 與本文件的 $L_\theta$ 無法形成合法 mapping，必須在看見候選前
   修改或撤回本 control，不得硬接；
2. D.1 第 6 項尚須提供全域 multiplicity rule，之後才能確定局部 $\alpha=0.01$
   是否足夠保守；
3. 本輪沒有產生或揭露任何 confirmatory holdout；上述 seeds 全屬
   candidate-independent protocol development，未來不得冒充 candidate holdout；
4. Freeze-1a 仍為 PENDING，候選設計禁令不變；
5. 256-per-side 的完整與 $\kappa=1$ audits 都不足；負結果保留為 sample-size
   sensitivity，不能再被解讀成 $\kappa=1$ domain 不可行。
