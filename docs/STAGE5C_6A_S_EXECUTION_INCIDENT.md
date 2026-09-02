# Stage 5C — 6a-S reserved execution incident

狀態：**【正式 plus arm `PROTOCOL-INVALID`；minus arm 未生成；6a-S 未完成】**。

本文件是 6a-S runner freeze 合併後首次 reserved execution 的不可逆事件紀錄。它不修改
`docs/STAGE5C_6A_S_PREREGISTRATION.md` 或
`docs/STAGE5C_6A_S_RUNNER_FREEZE.md`，也不把既有資料事後重判。

---

## 1. 執行邊界與事前核對

- protocol／`main` commit：`3bdc062a206f2ba35b04d2eadb59b83413e6be31`；
- clean checkout：`HEAD == refs/remotes/origin/main == protocol_commit`，工作樹為空；
- tracked files：73；`docs/STATUS.md`：v1.35；
- `python verify_integrity.py`：通過；
- runner：`analysis/stage5c_6a_s_runner.py`，依凍結 CLI 執行單一 `plus` arm；
- 執行前 1.3B／1.4B reserved streams 均未生成。

執行命令的形狀為：

```bash
python -m analysis.stage5c_6a_s_runner run-arm plus PLUS_LEDGER \
  --protocol-commit 3bdc062a206f2ba35b04d2eadb59b83413e6be31
```

沒有 generator override、selector override、threshold override 或 resume。ledger 位於 checkout
外，且在執行前不存在。

---

## 2. 不可逆 ledger 事實

plus arm 程序正常退出並完整寫入：

| record type | count |
| :--- | ---: |
| `run_header` | 1 |
| `seed_claim` | 768 |
| `sample_generated` | 768 |
| `causet_selector` | 8,448 |
| `block_pair` | 198 |
| `arm_data_complete` | 1 |
| `arm_selector_verdict` | 11 |
| `arm_complete` | 1 |

全部 768 個 1.3B manifest seeds 均已 write-ahead claim 並生成，故永久 **burned**。原始
NDJSON 為 6,839,409 bytes，SHA-256：

```text
32338ee83000c198747c1bd9cd5c9e98a5d054abde25e804be83533fe7de81e1
```

末列 `record_sha256` 為：

```text
2cb781fce848e321f4e523b004cd2e3e2166c974fdf44e9abe553417e45469fd
```

另生成 deterministic gzip（不含原檔時間戳）；其 SHA-256 為：

```text
520c42f8c523031763dde10f1086c1a6c43f855950afc1fae5097933729ccd63
```

本次 public-repo incident commit 只公開 counts、hashes、正式 categorical verdict 與根因
稽核，不公開逐 seed／逐 selector ledger payload；完整 ledger 的公開披露必須另有明確授權，
且不得藉此改變本 incident 的正式語意。

1.4B minus manifest **未 claim、未生成、未讀取**。發現 plus protocol-invalid 後沒有啟動
第二臂，避免在已無法依原 freeze 形成有效 combined verdict 時額外消耗 reserved seeds。

---

## 3. 凍結 adjudicator 的正式輸出

| selector | plus arm verdict |
| :--- | :--- |
| `all_relations` | `PROTOCOL-INVALID` |
| `links` | `6a-S PASS` |
| `interval_exact(1)` | `6a-S PASS` |
| `interval_exact(2)` | `6a-S PASS` |
| `interval_exact(3)` | `6a-S PASS` |
| `interval_exact(4)` | `6a-S PASS` |
| `endpoint_depth_mass_band(0.0,0.2)` | `PROTOCOL-INVALID` |
| `endpoint_depth_mass_band(0.2,0.4)` | `PROTOCOL-INVALID` |
| `endpoint_depth_mass_band(0.4,0.6)` | `PROTOCOL-INVALID` |
| `endpoint_depth_mass_band(0.6,0.8)` | `PROTOCOL-INVALID` |
| `endpoint_depth_mass_band(0.8,1.0)` | `PROTOCOL-INVALID` |

正式 reason 為 `causet diagnostics violate phi=1 normalization`。依凍結 precedence，這些
不是 `6a-S FAIL`，也不能因下節的根因分析而事後改成 PASS。minus 未執行，因此不存在
combined ledger 或 6a-S final verdict。

---

## 4. Candidate-independent incident analysis

adjudicator 以共同的 `MASS_TOLERANCE = 1e-12` 絕對容差檢查

$$
|\operatorname{ESS}-|\Sigma(C)||\le10^{-12}.
$$

但 uniform weights 的 Kish ESS 是浮點除法結果；pair count 變大後，理論恆等式
$\operatorname{ESS}=|\Sigma(C)|$ 的 roundoff 會超過固定絕對容差。單臂 ledger 的重算顯示：

| selector | 超出 `1e-12` 的 causet rows | 最大 $|\mathrm{ESS}-|\Sigma||$ |
| :--- | ---: | ---: |
| `all_relations` | 477 / 768 | $1.8645\times10^{-11}$ |
| depth band `(0.0,0.2)` | 14 / 768 | $1.8190\times10^{-12}$ |
| depth band `(0.2,0.4)` | 27 / 768 | $1.8190\times10^{-12}$ |
| depth band `(0.4,0.6)` | 24 / 768 | $1.8190\times10^{-12}$ |
| depth band `(0.6,0.8)` | 16 / 768 | $1.7053\times10^{-12}$ |
| depth band `(0.8,1.0)` | 24 / 768 | $1.5916\times10^{-12}$ |

同批 rows 的 normalization 與 coverage 重算差為 0；ESS fraction 的最大差約
$4.7\times10^{-15}$。所以 incident 是 runner/adjudicator 對理論整數恆等式使用不具尺度
穩健性的浮點絕對比較，不是已登記 floor／margin 的科學失敗。

這項分析只讀取 plus 單臂 diagnostics，用來辨識 protocol failure；沒有形成或檢視
plus/minus numerical contrast，沒有計算 primary endpoint，也沒有設計、import 或執行候選
$K$。

---

## 5. 判決與後續限制

1. 本次 plus arm 永久記為 `PROTOCOL-INVALID`；原 frozen runner 下的 6a-S **未完成**。
2. 不得修 runner 後重跑 1.3B、從同一 ledger 靜默重判、排除 rows 或把 protocol-invalid
   改寫為 scientific PASS／FAIL。
3. 在執行 minus 或任何 replacement plus seeds 前，必須另立顯式 protocol amendment，固定
   尺度穩健且可機械驗證的 ESS identity check、fresh seed lifecycle 與對現存 1.4B manifest
   的處置；amendment 必須先 commit、review、merge，才能再次生成 reserved samples。
4. 本 incident 不授權 6a-E、active wrong-support、候選設計或 holdout access。
