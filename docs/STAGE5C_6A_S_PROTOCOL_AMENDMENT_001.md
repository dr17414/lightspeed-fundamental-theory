# Stage 5C — 6a-S Protocol Amendment 001

狀態：**【Amendment-001 frozen；DEV-0012 已合併；1.5B replacement plus 已執行並待
DEV-0013 獨立複核／合併；1.4B minus 尚未執行】**。

本 amendment 只修正 DEV-0011 所定位的 runner／adjudicator implementation defect，並固定
replacement 6a-S 的 seed lifecycle。它不改 C8 selector family、pair weight、normalization、
smearing、Fourier grid、S1/S5/S6 floor 或 threshold，也不重判 1.3B plus ledger。它不讀
$T_+$ vs $T_-$ 數值 contrast、不計算 primary endpoint，且不設計、import 或執行候選 $K$。

source of record：`analysis/stage5c_6a_s_runner.py`；regression：
`tests/test_stage5c_6a_s_runner.py`；amendment ledger：
`docs/stage5c_protocol_amendment_log.md` 的 `AMEND-0001`；burn registry：
`docs/stage5c_6a_s_burn_registry.json`。

---

## 1. 觸發事件與修改邊界

首次 reserved plus arm 依 runner v1 完整生成 1.3B manifest 後，凍結 adjudicator 以共用
$10^{-12}$ **絕對**容差檢查

$$|\operatorname{ESS}-|\Sigma(C)||,$$

使 pair count 約數百至數千時的正常 floating-point roundoff 觸發
`PROTOCOL-INVALID`。DEV-0011 的最大差為 $1.8645\times10^{-11}$，但該數值**不得**用來
挑選新容差。本 amendment 採用原 prereg 已存在、事故前已固定且與 pair-count scale 無關的
ESS fraction contract；沒有從事故資料導入任何新 threshold。

下列項目保持原值：

- $\varphi=1$、$\mathcal N_C=|\Sigma(C)|$、$\epsilon=1/16$；
- 40 個 complex half-shell modes；
- $d_{\rm mean}\le0.20$、$d_{\rm law}\le0.20$；
- selected pairs／Kish ESS floor 32、coverage floor 0.005、ESS fraction floor 0.95；
- $N=64,96,128$、4 blocks × 64 causets、11 個 selector parameter points；
- 所有 scientific FAIL、INCONCLUSIVE 與 contrast-firewall semantics。

1.3B 的正式 verdict 永久維持原樣；本 amendment 不把它重算、重跑或升格為 evidence。

---

## 2. Adjudicator tolerance classification

全域共用 tolerance 不再被誤用於不同型別的量。runner v2 依下列三類檢查，並保存不同的
protocol reason；三類 mismatch 都是 prereg §5.4 明文新增的 internal-recomputation
`PROTOCOL-INVALID`，但原因不可互相替代。

### 2.1 A 類：已存欄位的確定性純函數／精確恆等式

下列值由 ledger raw fields 以 writer 相同的 deterministic operation 重算：

- `coverage == selected_pairs / domain_pairs`；
- `normalization == selected_pairs`；
- `d_law == sqrt(max(0, signed_energy_u))`。

Python float 的 JSON representation 精確往返，且 writer／adjudicator 使用同一 frozen
operation；因此要求 exact equality，不另設 data-derived tolerance。mismatch reason 分別為
`stored pure transform mismatch: ...` 或
`stored exact identity mismatch: normalization`，表示 ledger／implementation integrity 失配，
不是 S1/S5/S6 scientific FAIL。

### 2.2 B 類：從 raw diagnostics 的無因次獨立重算

ESS relation 改以

$$
\left|f_{\rm ESS}-\frac{\operatorname{ESS}}{|\Sigma(C)|}\right|\le10^{-12}
$$

檢查，其中 $f_{\rm ESS}$ 是 ledger 的 `ess_fraction`。這個 quantity 為 $O(1)$；容差沿用
原 prereg 的 `MASS_TOLERANCE=10^{-12}`，沒有新增常數。mismatch reason 為
`dimensionless recomputation mismatch: ESS fraction`。

### 2.3 C 類：$\varphi=1$ 理論恆等式

uniform weights 的 identity 只以無因次形式

$$|f_{\rm ESS}-1|\le10^{-12}$$

檢查，mismatch reason 為
`dimensionless phi=1 identity mismatch: ESS fraction`。原本有因次且量級隨 pair count
增長的 $|\operatorname{ESS}-|\Sigma||\le10^{-12}$ **刪除**。Kish ESS 本身仍須 finite 且
$\ge32$；這個 S6 floor 沒有放寬。

total mass／total variation 對 1 的既有 $10^{-12}$ 檢查不變。stored S1/S5/S6 boolean 仍由
raw fields 重算；不一致仍為 `PROTOCOL-INVALID`。

### 2.4 Cross-commit protocol invariant

attestation commit 必須夾在 dress／plus／minus 執行之間，所以兩臂的 `protocol_commit` 可以
不同；這不再等同於允許 scientific rules 改動。runner v2 對下列四個承重檔案依固定順序，
以 path UTF-8 bytes 與 file bytes 各加 8-byte big-endian length prefix 後串接並取 SHA-256：

1. `analysis/stage5c_measure_prereg.py`；
2. `analysis/stage5c_selector_family.py`；
3. `analysis/stage5c_hard_controls.py`；
4. `analysis/stage5c_6a_s_runner.py`。

所得 `protocol_invariant_digest` 必須寫入每個 `run_header` 與 prerequisite attestation。
`_assert_prerequisite_ledger()` 要求 prerequisite ledger digest 與當前 checkout 逐字相同；
`combine_arm_adjudications()` 要求 plus／minus digests 相同。如此允許中間只增加 DEV log、
attestation、burn-registry 等 custody metadata 的 commits，但禁止 selector、smearing、Fourier
grid、hard controls、threshold 或 adjudicator code 在兩臂之間漂移。digest mismatch 在 claim
前拒絕啟動或拒絕 combine，不形成新的 scientific threshold。

上述 digest 精確保證的是 **first-party code bytes**。數值 runtime 另由每個 `run_header` 與
attestation 的 `runtime_environment` 固定 `sys.version`、`numpy.__version__`、
`scipy.__version__`；prerequisite 與當前 process、plus 與 minus 的三欄必須逐字相同，否則在
claim 前拒絕或禁止 combine。CI 同時 pin Python 3.12.13、NumPy 2.3.5、SciPy 1.17.0、pytest
9.1.1 與 mpmath 1.4.1，避免 dependency resolver 在 staged commits 間漂移。這個版本鎖不宣稱
不同 CPU／BLAS implementation 逐位元等價；它只封住未登記的 interpreter／library-version
變動，且不構成新的 scientific threshold。

---

## 3. 新 seed manifests 與永久除役

三個可執行 manifest 固定為：

| execution profile | target | base | 用途 |
| :--- | :--- | ---: | :--- |
| `development-dress-rehearsal` | plus | 3,100,000,000 | runner v2 端到端機械 rehearsal |
| `replacement-reserved` | plus | 1,500,000,000 | fresh replacement plus arm |
| `replacement-reserved` | minus | 1,400,000,000 | 原未生成 minus arm，保留並加鎖 |

每個 base $b$ 對 $i=0,1,2$、$j=0,1,2,3$、$k=0,\ldots,63$ 均使用

$$\operatorname{seed}=b+10^6i+10^4j+k.$$

每臂 768 seeds。runner v2 不接受 1.3B profile；1.3B 全部永久 retired，不能作
replacement 的 control、comparison、calibration、power estimate，也不能與 1.4B 配對。

3.1B／1.5B／1.4B 同樣採 write-ahead claim：claim 一旦 fsync 即 burned，無論 generator、
ledger 或 adjudication 後來是否中斷。不得 resume、補樣、換 seed 或重跑。

### 3.1 Committed append-only burn registry

`docs/stage5c_6a_s_burn_registry.json` 固定 `schema_version=1`，每筆只有
`execution_profile`、`target`、`seed_base`、`ledger_sha256`、`development_log_entry`。初始列為
DEV-0011 的 `original-reserved-v1`／plus／1.3B 與公開 ledger hash。其後只可按下列 prefix
順序 append，不得刪除、改寫、重排或跳號：

1. DEV-0011：original 1.3B plus；
2. DEV-0012：3.1B dress-rehearsal plus；
3. DEV-0013：1.5B replacement plus；
4. DEV-0014：1.4B replacement minus。

每次 `run-arm` 在建立 ledger、durable claim 或呼叫 generator **之前**讀取 registry，驗證每列
manifest metadata、DEV entry 與 ledger hash 均已進 development log，並要求目前 entries
恰為所請 lifecycle stage 的完整 prefix；若該 `(execution_profile,target)` 已登記即拒絕啟動。
每個 `run_header` 另保存啟動時 registry bytes 的 `burn_registry_sha256_at_start`，attestation
必須逐字保存該值。

此 registry 能機械阻止已 committed execution 的重跑，並讓跨 commit lifecycle 可稽核；它
不能在第一次執行完成與其 registry entry commit 之間，跨另一個全新 checkout 排除蓄意重跑。
該窗口仍由「一次執行、立即封存、獨立 review」的程序禁令約束，不得把 registry 誇大為
全域 distributed lock，也不得從多份 ledger 選一份最乾淨者。

---

## 4. Development dress rehearsal 硬性前置

在任何 1.5B／1.4B seed 生成前，必須先於本 amendment 與 runner v2 已 review、merge、CI
通過的 clean `main` 上執行一個完整 3.1B plus-target arm。它使用與 reserved execution
相同的 `run-arm` code path、generator、selector、$N$ grid、4×64 block structure、ledger
schema 與 `adjudicate_arm_records()`；唯一差異是 frozen execution profile 與 seed manifest。

命令形狀：

```bash
python -m analysis.stage5c_6a_s_runner run-arm \
  development-dress-rehearsal plus DRESS_LEDGER \
  --protocol-commit MAIN_COMMIT
```

機械 clean 的必要條件是 11 個 selector 均不得為 `PROTOCOL-INVALID` 或 `INCONCLUSIVE`。
預登記 S1/S5/S6 若產生 `6a-S FAIL`，仍如實保留；不能因 rehearsal 目的而改判，也不能用
該 FAIL／PASS 或任何 `d_mean`、`d_law`、pair-count summary 調整 floor、margin、threshold、
selector family、sample grid 或 power estimate。

3.1B ledger 是 plus-distribution development data；不得與 1.4B 或任何其他 minus ledger
配對，不得以任何直接讀取／另寫分析程式形成 between-target numerical contrast，也不得作
replacement arm 的 control、comparison、calibration 或 power-estimate input。
1.5B 的 categorical verdict 必須獨立成立：無論其 PASS／FAIL pattern 是否與 DEV-0012 相同，
均不得引用 3.1B 的 11/11 PASS 作 seed-fluctuation 解釋、語意重判、門檻校正、重跑理由或
任何「本來應該通過」的脈絡證據。

執行後必須：

1. 全部 3.1B claims 記為 burned；
2. 將 ledger SHA-256、protocol commit、protocol-invariant digest、record counts 與 categorical
   verdict 寫入 DEV-0012；
3. 同步 append DEV-0012 burn-registry entry，並在獨立 commit 新增
   `docs/stage5c_6a_s_dress_rehearsal_attestation.json`；
4. 該 commit 經 CI／review／merge 後，1.5B replacement plus 才取得執行資格。

3.1B、1.5B 與 1.4B 必須在同一套凍結的執行環境完成；DEV-0012 須逐字保存 rehearsal
實際使用的 `sys.version`、NumPy 與 SciPy version strings，不得把 CI pin 誤寫成 formal
ledger 的實際環境。若 3.1B rehearsal 完成後發現必須修改四個 protocol-invariant files，或
當前 process 的三個 runtime version strings 已與 DEV-0012 不同，既有 digest／environment
gate 與 registry ratchet 會同時禁止就地修改或升級後進入 1.5B、也禁止重跑 3.1B。兩種情形
的唯一合法出口都是先立 AMEND-0002，登記全新的 dress execution profile 與未使用 seed base
（例如 3.2B），經 review／merge 後重走完整 rehearsal；不得刪改 DEV-0012／registry、降級
既有環境紀錄，或挑選既有多份 ledger。

attestation schema 固定為：

```json
{
  "schema_version": 1,
  "protocol_tag": "stage5c-6a-s-runner-v2-amendment-001",
  "execution_profile": "development-dress-rehearsal",
  "target": "plus",
  "protocol_invariant_digest": "64-lowercase-hex",
  "burn_registry_sha256_at_start": "64-lowercase-hex",
  "runtime_environment": {
    "python": "exact sys.version string",
    "numpy": "exact numpy.__version__ string",
    "scipy": "exact scipy.__version__ string"
  },
  "ledger_sha256": "64-lowercase-hex",
  "ledger_protocol_commit": "40-lowercase-hex",
  "seed_manifest": "development-3.1b",
  "seed_base": 3100000000,
  "verdict_constraint": "NO_PROTOCOL_INVALID_OR_INCONCLUSIVE",
  "development_log_entry": "DEV-0012"
}
```

runner 會先把 prerequisite ledger 讀成單一 immutable byte snapshot，再以**同一份 bytes**重算
hash 與 adjudication，避免兩次 open 間的 replacement／symlink-swap race；並核對 committed
attestation 與 development log。只靠操作者口頭確認不會解鎖 1.5B。

---

## 5. Replacement plus 與 minus 的順序鎖

### 5.1 Replacement plus

3.1B attestation 合併後，1.5B plus 的命令形狀為：

```bash
python -m analysis.stage5c_6a_s_runner run-arm \
  replacement-reserved plus PLUS_LEDGER \
  --protocol-commit MAIN_COMMIT \
  --prerequisite-ledger DRESS_LEDGER
```

runner 在建立 plus ledger、claim 任何 1.5B seed **之前**驗證 DEV-0012、attestation、ledger
SHA-256、manifest 與機械 clean condition。任一不符即拒絕啟動，不生成 seed。

### 5.2 Minus

1.5B plus 完成後，必須另在 DEV-0013 記錄 ledger hash／categorical verdict，並於獨立
commit append DEV-0013 burn-registry entry，並新增
`docs/stage5c_6a_s_replacement_plus_attestation.json`，schema 與 §4 相同，但
profile=`replacement-reserved`、manifest=`replacement-plus-1.5b`、base=`1500000000`、
development entry=`DEV-0013`。只有該 plus ledger 全部 selector 無 `PROTOCOL-INVALID`／
`INCONCLUSIVE`，且 attestation commit 經 CI／review／merge，1.4B minus 才可啟動：

```bash
python -m analysis.stage5c_6a_s_runner run-arm \
  replacement-reserved minus MINUS_LEDGER \
  --protocol-commit MAIN_COMMIT \
  --prerequisite-ledger PLUS_LEDGER
```

若 replacement plus 再次 `PROTOCOL-INVALID` 或 `INCONCLUSIVE`，1.4B 仍不得生成；必須停止
並另立 amendment。scientific `6a-S FAIL` 不被改寫，且不解除其他 selector 的 categorical
記錄需求。兩臂因中間 attestation commit 可有不同 `protocol_commit`；但 prerequisite 與
當前 checkout、plus 與 minus 之 `protocol_invariant_digest` 必須相同。combined ledger 必須
保存 plus／minus 各自 commit 與共同 digest，且仍只接收 categorical arm verdict，不能形成
數值 contrast。combiner 的引數順序固定為 plus、minus，反向傳入直接拒絕，避免 positional
provenance 錯標。minus 執行後須以 DEV-0014 與其 ledger hash append 最終 burn-registry entry。

---

## 6. `PROTOCOL-INVALID` 對齊與執行授權

prereg §5.4 的 `PROTOCOL-INVALID` 明文增加第五類：ledger stored field／gate flag／verdict 與
依 frozen schema、raw fields、deterministic transform 所作的 internal recomputation 不一致。
runner 不得再單方面擴張此集合。

本 amendment commit 只授權 merge 後執行 §4 的 3.1B development dress rehearsal；它**不**
直接授權 1.5B plus 或 1.4B minus。每道 committed attestation 是下一步的必要條件，不是
scientific PASS 證據。任何 between-target numerical access、6a-E、active wrong-support、
candidate holdout 或候選 $K$ 仍禁止。
