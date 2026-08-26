# Stage 5C C8.4 — 定義域內困難對照可行性與預登記草案

狀態：**【已確認／核心可構造性成立；尚未構成 Freeze-1a】**

本文件處理 `STAGE5C_ACCEPTANCE.md` 附錄 D.1 第 5 項，並給出第 4 項
matching protocol 的第一個完整可執行實例。結論是：**在不設計、讀取或執行任何
候選 kernel $K$ 的前提下，確實可以構造一組位於 1+1D／order-dimension-$\le2$
定義域內、低階 order statistics 可匹配、但 continuum massless-chiral target
預先已知不同的困難對照。** 因此目前不應判
`BOUNDED-SEARCH-EXHAUSTED` 或 `SPEC-INFEASIBLE`。

這只是 Freeze-1a 前的 candidate-independent feasibility artifact。依定稿規格，
附錄 D.1 九項仍須全部完成，並在一個明確引用 acceptance-spec commit
`3b1fb48c51a2b6e608d526a993b103ec4ab2cba9` 的單一 freeze commit 中固定，才算
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
max KS $0.1334$。它同時未達 coverage $\ge0.35$ 與 max SMD $\le0.20$，所以
**目前對 $\kappa=1$ 限縮 domain 的結論是未通過／待更大 pool 的
candidate-independent 驗證，不得寫成可執行性已確認**。這不影響下文對完整
dimension-$\le2$ control domain 的正結果；但未來候選若自行限縮至 $\kappa=1$，
在該候選存在前沒有另一個通過的固定 protocol，就只能對 C8 記 INCONCLUSIVE，
不得放寬 caliper。

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
所有量都 label-invariant，且不讀 target metadata：

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

候選在 Freeze-2a 只能增加符合 acceptance spec C8.1 provenance 限制的 nuisance
covariates；新增後匹配失敗仍是 INCONCLUSIVE，不能回頭移除 baseline。

---

## 5. Source-of-record feasibility run

`analysis/stage5c_hard_controls.py::benchmark(n=96,pool_size=512)` 使用四個互不重疊
的 PCG64DXSM seed ranges：

| split | target | seed range |
| :--- | :--- | :--- |
| calibration | $T_+$ | `510000000..510000511` |
| calibration | $T_-$ | `520000000..520000511` |
| validation | $T_+$ | `530000000..530000511` |
| validation | $T_-$ | `540000000..540000511` |

結果：

| 指標 | 結果 | feasibility threshold |
| :--- | ---: | ---: |
| matched pairs | 205 | $\ge192$ |
| coverage | 0.400390625 | $\ge0.35$ |
| max absolute SMD | 0.150219436 | $\le0.20$ |
| max KS distance | 0.141463415 | $\le0.18$ |
| median standardized distance | 1.701926936 | pair caliper $\le2$ |
| p90 standardized distance | 1.918984193 | pair caliper $\le2$ |

所以這不是 KR-vs-sprinkling 那種不匹配就能分出的 easy control；近 60% 樣本因
嚴格 pair caliper 未配對，保留下來的 cohort 才達到預定低階平衡。

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

對完整 dimension-$\le2$ control domain，source-of-record 已保有 205 對，足以
支撐上述 192-pair power floor。對 $\kappa=1$ 限縮 domain，不能只用 retention
比例乘上 nominal coverage 推算，因為 $\kappa$ 與 nuisance features 可能相關；
必須另做實際 filter-then-match 的較大-pool benchmark。在該 benchmark 通過前，
不預登記一個看似足夠但未驗證的 raw-pool 數字。

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
6. matching benchmark 必須保持非零 coverage 與低階 balance。

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
- 完成 source-of-record matching、$\kappa=1$ audit、power 下界與 RNG/hash manifest；
- 全程未設計或評估任何候選 $K$。

### 尚未完成

1. D.1 第 3 項尚須把 C6/C7/C8 primary observable、smearing 與 norm 統一；若其
   object contract 與本文件的 $L_\theta$ 無法形成合法 mapping，必須在看見候選前
   修改或撤回本 control，不得硬接；
2. D.1 第 6 項尚須提供全域 multiplicity rule，之後才能確定局部 $\alpha=0.01$
   是否足夠保守；
3. 本輪沒有產生或揭露任何 confirmatory holdout；上述 seeds 全屬
   candidate-independent protocol development，未來不得冒充 candidate holdout；
4. Freeze-1a 仍為 PENDING，候選設計禁令不變。
5. $\kappa=1$ 限縮 domain 的 256-per-side audit 未達 matching gate；此負結果已
   保留，後續只能在候選出現前增加 development pool 重新驗證，不能改門檻。
