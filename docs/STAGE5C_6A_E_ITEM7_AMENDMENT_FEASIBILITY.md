# Stage 5C 6a-E item-7 amendment feasibility assessment

**狀態：`ASSESSMENT-ONLY`。本文件不重開 item 7、不修改 frozen producer，亦不選定 replacement constant／criterion。**

本評估只回答：已查明的 frozen absolute-tolerance scale mismatch 是否有可行修法、
4096-subdivision 上限在已測 deterministic cases 中是否立即阻塞，以及若正式修訂
item 7，哪些已 `CLOSED` 下游必須重新複核。所有探查均為 candidate-independent、
無 RNG／seed／generator／arm data／matching／candidate kernel；數值不得用於選 cap、
cohort floor 或宣稱 Gate A／Gate B 已關閉。

## 1. Frozen surface 與兩個候選方向

現行 item 7 凍結：

| 欄位 | frozen value |
|---|---:|
| `E4_CUBATURE_RTOL` | $2^{-14}$ |
| `E4_CUBATURE_ATOL` | $2^{-30}$ |
| `E4_MAX_SUBDIVISIONS` | $4096$ |
| `E4_MAX_ATOMS` | $8128$ |
| `E4_ENCLOSURE_LEVELS` | $(16,32,64)$ |

本評估分開比較：

1. **固定較小 absolute tolerance**：development value $2^{-50}$。這只移動
   scale-mismatch 門檻；更小 pairing scale 仍會重現相同結構，因此不是對稱修法。
2. **尺度感知 candidate**：先計算既有 validated analytic enclosure，令

   $$
   a_{\rm eff}
   =\min\left(2^{-30},\;2^{-14}\max_k U_k\right),
   $$

   其中 $U_k$ 是兩個 diagonal pairing components 的 enclosure upper endpoints。
   這只是 development candidate；不是 item-7 amendment。正式提案還必須定義
   $\max_kU_k=0$ 的分支、計算順序、producer identity 與 source-row fingerprints。

直接取 `enclosure width` 或 fixed-rule validated error 作 `atol` 並不足夠：在
$(0.70,0.70,0.05,0.05)$ witness 上，兩者分別約為
$8.83\times10^{-14}$ 與 $6.35\times10^{-14}$，adaptive solver 仍零次細分，
item 3 仍回報 `NORM-INTERVAL-TOUCHES-ZERO`。必須另給相對尺度係數；上式以既有
$2^{-14}$ 作事前 candidate，避免再引入一個未解釋常數。

## 2. 已知 Gate-A／Gate-B witnesses

下表沿用 production E4、item-3 certifier 與 production selector adapter；只有
adaptive `atol` 在記憶體中暫時改動。wall time 是本開發容器
(Python 3.12.14／NumPy 2.3.5／SciPy 1.17.0) 的單次觀察，不是 resource cap。

| witness／policy | effective `atol` | subdivisions | 結果／normalized endpoint error |
|---|---:|---:|---|
| Gate A $(.70,.70,.05,.05)$，frozen | $2^{-30}$ | 0 | `INCONCLUSIVE/NORM-INTERVAL-TOUCHES-ZERO` |
| 同列，固定 $2^{-50}$ | $2^{-50}$ | 37 | `CLEAN`；約 $(0.02412,0.02895)$ |
| 同列，$a_{\rm eff}$ | $4.0123\times10^{-16}$ | 49 | `CLEAN`；約 $(0.02322,0.02786)$ |
| Gate B $(.80,.80,.20,.20)$，frozen | $2^{-30}$ | 0 | `CLEAN`；約 $(3.7855,4.5426)$ |
| 同列，固定 $2^{-50}$ | $2^{-50}$ | 118 | `CLEAN`；約 $(0.01139,0.01366)$ |
| 同列，$a_{\rm eff}$ | $2.7401\times10^{-14}$ | 68 | `CLEAN`；約 $(0.01138,0.01365)$ |
| wide-cell $(.55,.55,.45,.45)$，任一 policy | frozen cap active | 158 | `CLEAN`；約 $(0.08454,0.10145)$ |

因此兩種修法都能改善共同的 near-zero adaptive mismatch，但都**不**改善由
analytic cell enclosure 寬度主導的另一個 Gate-B 機制。尺度感知 candidate
用較少 subdivisions 達到與固定 $2^{-50}$ 同階的 Gate-B error，且對一般尺度
案例維持 frozen cap。

更重要的是 amendment 並非只做 `INCONCLUSIVE` $\to$ `CLEAN`。Gate-B witness
原本已是 `CLEAN`，其 certified endpoint error 仍顯著改變；現有真實
selector→E4 regression 的 screen category 亦由 `CLEAN-OVER` 變成
`CLEAN-NEAR`。所以不能把下游複核縮成 status-only diff。

## 3. Suite compatibility 與 4096 上限

Frozen baseline 為 `384 passed, 5 warnings`。以暫時 probe 套入固定 $2^{-50}$
時為 `379 passed, 5 expected failures`；套入 $a_{\rm eff}$ 時為
`380 passed, 4 expected failures`。失敗全部落在以下已知契約斷言：

- frozen constant 必須等於 $2^{-30}$（只有固定-$2^{-50}$ 方案觸發）；
- frozen witness 必須零 subdivision／non-`CLEAN`；
- near-zero witness 必須零 subdivision／大 relative error；
- screen 接縫案例必須分類 `CLEAN-OVER`。

沒有出現與這些預期行為無關的新失敗。這不等於可直接更新測試後關閉 item 7；
它只說現有 suite 沒有顯示第三種未預期退化。

probe 對真實 converged 測試輸入觀察到的最大 subdivisions 在 frozen 與
$a_{\rm eff}$ 下均為 480。唯一的 4096 記錄來自既有
`test_adaptive_resource_exhaustion_is_inconclusive` 故意注入的
`not_converged` backend，不是 candidate 造成的 cap hit。

另外以兩個 deterministic 8128-atom inputs 探查最大 atom count：

| input | $a_{\rm eff}$ | subdivisions | cubature wall | `ru_maxrss` |
|---|---:|---:|---:|---:|
| $90\times91$ grid 截取 8128 個 strict causal pairs | $6.3164\times10^{-10}$ | 124 | 48.23 s | 123056 KiB |
| 8128 個重複 $(.70,.70,.05,.05)$ | $4.0123\times10^{-16}$ | 49 | 18.24 s | 120724 KiB |

兩者都在 4096／900 s／32 GiB 內；這只是兩個 input，不是完整 admissible
support 的 resource theorem。特別是更嚴格的 tolerance 可能把原本 premature
`converged` 轉成真正的 resource exhaustion。因此 adaptive finite-output／resource
bucket 仍須獨立解析界或 validated tail，不能因本表而 `CLOSED`。

## 4. 下游重審範圍

正式 amendment 至少涉及：

1. **item 7 producer**：`stage5c_e4_wellposedness.py` 的計算順序、adaptive
   identity、contract 文件、resource regressions 與 frozen constants。
2. **item 3 certification**：certifier 公式本身可不變，但兩個 implementation
   estimates、agreement、norm interval、endpoint error 與 source-row fingerprint
   都可能改變；既有 `CLEAN` rows 不能假定逐位元不變。
3. **items 4–5 regions**：`stage5c_statistical_regions.py` 會把 item-3 error
   逐 matched row 相加；region form 可保持不變，但 numerical half-width、
   source ensemble seal 與 boundary classification 必須重跑／複核。
4. **screen／custody**：歷史 authorization 與 attestation 屬已 burned namespace，
   必須保持逐位元不動。若未來另開 namespace，新 runner／authorization 必須
   pin amendment 後的 E4 blob 與當時 current adapter，並重新完成真實接縫回歸。

`stage5c_planted_certification.py` 不直接呼叫 E4；它提供 item-3／item-6 的獨立
planted arithmetic controls。因此它需要重跑作為 certification regression，
但不是 E4 numerical payload 的直接 runtime consumer。直接 executable consumer
是 `stage5c_e5_screen.py`，而 region 的實際數值 downstream 是
`stage5c_statistical_regions.py`。

目前沒有正式 6a-E arm ledger、endpoint 或 scientific verdict，故沒有已記錄
arm 判決可被 amendment 回溯改寫；這不免除 items 3–5 的 closed-delivery review。

## 5. 對 Gate A／Gate B 的實際效益

- **Gate A item-3 bucket**：已知 $R_{\rm geo}$ witness 可由 non-`CLEAN` 轉為
  `CLEAN`，證明 amendment 有實質效益；但單點仍不給 failure-tail 上界，該桶
  保持 `OPEN`。
- **Gate A adaptive backend bucket**：沒有被本 amendment 關閉。candidate
  要求更多 subdivisions，可能降低 premature convergence，卻不能證明全 support
  finite output／resource success；該桶保持 `OPEN` 且不得與 item-3 桶互借。
- **Gate B near-zero mechanism**：known witness 的 normalized error 下降兩個以上
  數量級並低於 $1/40$，是明確改善。
- **Gate B wide-cell mechanism**：完全不變，仍須 enclosure refinement、不同的
  deterministic bound 或 matched-law 證明。

所以「同一 solver 修一次同時關兩個 Gate-A buckets」不成立；準確結論是它同時
改善 Gate A 的 item-3 bucket 與 Gate B 的 near-zero mechanism，但 adaptive
resource bucket 與 wide-cell mechanism 仍各自存在。

## 6. 評估結論與下一個合法步驟

固定 $2^{-50}$ 在已知 witnesses 上可行，卻只把錯配門檻往下移。尺度感知
$a_{\rm eff}$ 在相同 probes 上以較少 Gate-B subdivisions 得到同階改善，並保留
一般尺度的 frozen cap；因此它是較值得形成**正式 amendment candidate** 的方向。
本評估仍不足以核准該公式，尤其缺少：

- zero-scale branch 與 underflow semantics；
- 完整 admissible support 的 4096-subdivision／finite-output 證明或事前 tail；
- amendment 後 producer identity、source-row fingerprint 與 items 3–5
  downstream regression plan；
- Gate A item-3 failure probability 與 Gate B matched-null law。

下一個合法交付若選 amendment，必須先以獨立 PR 明文重開 item 7、固定 candidate
criterion／版本 identities／resource obligations，再改 production code。不得把本文件
的 development formula、timings 或 witnesses 直接接入正式 6a-E runner。
