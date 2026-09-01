# Stage 5C — 6a-S runner／ledger／adjudicator freeze

狀態：**【candidate-independent runner 已凍結；reserved execution 尚未開始】**。

本文件固定 `analysis/stage5c_6a_s_runner.py` 的執行邊界、append-only ledger schema、
中斷語意與 S1–S6 adjudicator。它不生成 1.3B／1.4B samples、不形成 target contrast、
不計算 primary endpoint，也不設計、import 或執行候選 $K$。

runner freeze 的 base main commit 是 `672335300527373b2bc428b51b489b8bef8c7119`。
正式執行時 ledger 必須記錄本 runner PR 合併後的實際 `main` commit，且 runner API／CLI
只允許在 clean checkout、`HEAD == origin/main == protocol_commit` 時啟動。

---

## 1. 單臂執行與 contrast firewall

正式 runner 一次只接受一個 target token：`plus` 或 `minus`。`run_target_arm()` 只有
`target`、`ledger_path`、`protocol_commit` 三個外部參數；generator、selector family、
normalization、Fourier grid、thresholds 與 seed mapping 都由已凍結 module 直接 import，
caller 不能覆寫。

每個 target 各產生一份獨立 ledger，並各自得到 11 個 categorical arm verdict。唯一可同時
接收兩臂輸出的 `combine_arm_adjudications()` 只接受 `ArmAdjudication`；其 schema 只含
target、protocol commit、selector id、categorical verdict 與 reasons，沒有 signature、
coordinates、seed-level diagnostics 或任何 real-valued target summary。因此 combine 階段
無法形成 $T_+$ vs $T_-$ numerical contrast。

combined ledger 只保存每個 selector 的 plus／minus categorical verdict 與最終 verdict；
若兩臂 protocol commit 不同、target 重複或 selector schema 不完整，直接
`PROTOCOL-INVALID`／拒絕 combine。

---

## 2. Write-ahead burned-seed semantics

每個 reserved cell 的固定順序是：

1. 以 exclusive-create、append-only NDJSON ledger 寫入 `seed_claim`；
2. `seed_claim` 標記 `BURNED_ON_CLAIM_BEFORE_GENERATION`，寫入後立即 `fsync`；
3. 只有 durable claim 成功後才呼叫 `sprinkle_control()`；
4. generator 回傳且 schema 驗證成功後再 append＋`fsync` `sample_generated`。

所以 crash 若發生於 2 與 4 之間，該 seed 仍保守視為 burned；不會出現「可能已生成、但
ledger 沒記」的歧義。ledger path 必須原先不存在，runner 拒絕 overwrite 或 resume。
中斷後只能對現存 ledger 執行 adjudicator；不得重跑、換 seed 或補齊另一批 samples。

每列另含遞增 `sequence`、`previous_sha256` 與本列 `record_sha256`。讀取時逐列重算完整
hash chain；修改、刪列、插列、重排或 non-finite JSON 都使 ledger invalid。

---

## 3. Frozen ledger schema

| record type | 必要內容 | 寫入時點 |
| :--- | :--- | :--- |
| `run_header` | schema version、protocol tag／commit、單一 target、expected counts、contrast forbidden marker | exclusive-create 時第一列 |
| `seed_claim` | target、$N$/index、block、case、seed、burned state | generator 前且已 `fsync` |
| `sample_generated` | 同一 cell 與 seed | generator/schema 成功後 |
| `causet_selector` | selector／parameters、cell／case id／seed、selected/domain pairs、coverage、normalization、mass、TV、Kish ESS／fraction、S1/S2/S3/S4/S6 flags | 每 causet × 11 點 |
| `block_pair` | selector／parameters、target、$N$、兩個 block ids、$d_{\rm mean}$、signed $\widehat E_U$、$d_{\rm law}$、S5 flag | 每 selector × target × $N$ × 6 pairs |
| `terminal_error` | target、`protocol` 或 `backend` category、error class/message | 可稽核中斷時 |
| `arm_selector_verdict` | 單一 target、selector／parameters、verdict、reasons | arm adjudication 後 |
| `arm_complete` | target、11 verdict count | 單臂正常收尾 |
| `selector_verdict` | selector／parameters、兩個 categorical arm verdicts、final verdict | 獨立 combined ledger |

一個完整 arm 必須恰有 768 個 unique seed claims、768 個 generated rows、每 selector 768 個
unique causet rows，以及每 selector 18 個 unique block-pair rows。任何 excess、duplicate、
unregistered cell、wrong seed、mixed target、forged gate flag 或 stored verdict 與重算結果不符，
都不交由人工裁量。

---

## 4. S1–S6 executable gate map

| gate | runner evidence | adjudication |
| :--- | :--- | :--- |
| S1 | 每個 `causet_selector.selected_pairs` | 任一 `<32` → selector arm `FAIL` |
| S2 | 每個 causet 固定 cyclic relabel 後逐 pair covariance | 任一 mismatch → `PROTOCOL-INVALID` |
| S3 | selector 只收到欄位恰為 `case_id, order` 的 `BlindedCase`，無 sector payload | boundary mismatch → `PROTOCOL-INVALID` |
| S4 | `BlindedCase` schema、family capacity＝evaluation ledger＝11 | mismatch → `PROTOCOL-INVALID` |
| S5 | 每個同-target block pair 的 $d_{\rm mean}$、signed $\widehat E_U$、$d_{\rm law}$；adjudicator 從數值重算 flag | 任一 threshold failure → `FAIL`；non-finite／backend failure → `INCONCLUSIVE` |
| S6 | coverage、normalization、mass、TV、Kish ESS／fraction，從 raw diagnostics 重算 | 任一 floor failure → `FAIL` |

adjudicator 不信任 ledger 內既存 boolean 或 verdict：所有可重算 gate 都由 raw fields 重算，
並驗證 stored flag。verdict precedence 固定為：

$$
\texttt{PROTOCOL-INVALID} > \texttt{6a-S FAIL} >
\texttt{INCONCLUSIVE} > \texttt{6a-S PASS}.
$$

因此已觀察到的正式 floor／threshold failure 不會因後續中斷被洗成 `INCONCLUSIVE`；但
protocol violation 優先於所有數值結果。兩臂 final combine 使用同一 precedence，且只處理
categorical verdicts。

---

## 5. CLI 與執行前條件

runner freeze 合併後，正式單臂命令形狀固定為：

```bash
python -m analysis.stage5c_6a_s_runner run-arm TARGET LEDGER \
  --protocol-commit MAIN_COMMIT
```

`TARGET` 必須是 `plus` 或 `minus`。兩份 ledger 必須放在 checkout 外，避免第一臂輸出使
第二臂的 clean-checkout gate 失敗。兩臂完成後才可執行：

```bash
python -m analysis.stage5c_6a_s_runner combine \
  PLUS_LEDGER MINUS_LEDGER COMBINED_LEDGER
```

在 runner freeze commit 合併、CI 通過且重新核對 `main` 前，禁止執行 `run-arm`。本文件與
runner commit 本身不授權 6a-E、target contrast、candidate design 或任何 holdout access。
