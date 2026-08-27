# Stage 5C D.1 第 3 項 — Reference-Probe 執行結果

狀態：**已執行；witness split 已揭露並 burned。**

Protocol：`docs/STAGE5C_D1_3_REFERENCE_PROBE.md`（於 commit `49b5cf32` freeze）。
Source-of-record：`analysis/stage5c_reference_probe.py` 的 `__main__`；其
`adjudicate()` 逐項執行 12 個 block gates、$n_Q/n_N$、P/N 儀器 gates、方向、effect
floor 與 Holm 判決，而非只列出統計量後由人工判讀。

原始執行環境驗證：`verify_integrity.py` 通過、全庫 `126 passed`；獨立審計補入
payload-boundary／adjudicator tests 後為 `128 passed`。本文件所有 aggregate 數字皆由
上述 `__main__` 產生並已重跑確認逐位元重現。

---

## 1. 判決

| 項目 | 結果 |
| :--- | :--- |
| Layer 1（continuum-oracle） | **PASS** |
| Layer 2 arm P（儀器可用性） | **PASS** |
| Layer 2 arm N（等效性） | **PASS** |
| Layer 2 arm Q（殘餘資訊） | **PASS** |
| **§6 判決** | **CONTROL-VIABLE** |

依 §6，後續為：繼續撰寫統一的 observable／selector／smearing／norm contract。

---

## 2. Cohort gates

12 個 block（P/Q 六個、N 六個）全部通過 C8.4 的 pairs／coverage／SMD／KS gates。

| block | pairs | coverage | max SMD | max KS |
| :--- | ---: | ---: | ---: | ---: |
| pq0 | 344 | 0.4479 | 0.1432 | 0.0988 |
| pq1 | 346 | 0.4505 | 0.1287 | 0.0723 |
| pq2 | 321 | 0.4180 | 0.1217 | 0.0966 |
| pq3 | 345 | 0.4492 | 0.1143 | 0.0841 |
| pq4 | 315 | 0.4102 | 0.1689 | 0.0889 |
| pq5 | 354 | 0.4609 | 0.1472 | 0.0791 |
| null0 | 395 | 0.5143 | 0.0368 | 0.0506 |
| null1 | 332 | 0.4323 | 0.0833 | 0.0602 |
| null2 | 321 | 0.4180 | 0.0470 | 0.0498 |
| null3 | 364 | 0.4740 | 0.0449 | 0.0632 |
| null4 | 368 | 0.4792 | 0.0900 | 0.0897 |
| null5 | 408 | 0.5312 | 0.0886 | 0.0809 |

null blocks 的 max SMD 明顯低於 pq blocks，與兩側同分布的預期一致。

專屬 cohort gates：$n_Q=1014\ge576$ ✓；$n_N=1140\ge900$ ✓。

---

## 3. 四個預登記 claims

| claim | $n$ | 效應量 | $p$ | Holm (FWER 0.01) | 方向 | effect floor |
| :--- | ---: | ---: | ---: | :---: | :---: | :---: |
| layer1 | 1014 | $+0.3801$ | $5.000\times10^{-6}$ | 通過 | ✓ | ✓ |
| P | 2304/側 | $+1.1311$ | $5.000\times10^{-6}$ | 通過 | ✓ | ✓ |
| N | 1140 | $+0.0015$ | $3.074\times10^{-7}$ | 通過 | — | 等效 |
| Q | 1014 | $+0.8510$ | $5.000\times10^{-6}$ | 通過 | ✓ | ✓ |

**$p$ 值解析度註記.** layer1／P／Q 的 $5.000\times10^{-6}$ 即 $1/200001$，是加一修正下
$200{,}000$ 次 randomization 的**下限**：沒有任何一次 draw 達到觀測統計量。因此不得把
它讀成「真實 $p$ 恰為或小於 $5\times10^{-6}$」。正確陳述只有：20 萬次抽樣中
zero exceedances，加一 Monte Carlo estimate 到達本次設計的最小可報值
$1/200001$；此設計無法解析更小的 underlying $p$。N 為解析 $t$ 檢定，其值不受此限制。

**arm N.** 標準化 paired effect $+0.0015$，遠在 $\pm\delta_N=0.15$ 之內，TOST 證成
operational equivalence。matching 程序本身未製造可偵測結構。

**arm P.** 未匹配時效應 $+1.1311$，儀器可用。

---

## 4. 事後診斷的隔離

執行者另計算了兩項未預登記的 baseline-leakage diagnostics。它們不屬 §4.6 的四個
claim family，未參與 Holm、未改變判決；但 frozen protocol §0 又明定公開輸出**且僅**
限 verdict 與 arm-level $n$/effect/$p$。因此這些診斷的數值不進 source-of-record、
不得引用為 `CONTROL-VIABLE` 的補強證據，也不得回流 construction。若未來認為此類
診斷是必要 gate，必須在 fresh protocol／fresh seeds 下事前登記，不能用本次已揭露
witness 追認。

**反證優先例外。** 上述 output-only firewall 不得用來壓低與登記判決衝突的
事後證據。若未登記診斷顯示某項登記判決的必要前提可能失效，source-of-record
必須公開且僅公開 `POSTHOC-CONFLICT`（不得公開數值、方向、feature family 或權重），
並同步在 development log 記錄、暫停該 verdict 的承重資格、開立 protocol amendment；
只有 fresh protocol／fresh seeds 的預登記檢驗可以解除衝突。與判決相容的事後診斷
仍維持隔離，不得另記 `NO-CONFLICT` 或作正面佐證。這是一條不對稱的 falsification
規則：禁止未登記佐證升格，但不容許輸出限制消音已知反證。

---

## 5. 語意上限

依 §5 第 5 項，本結果只能表述為：

> 在明定的 probe bank $\mathcal G_{\text{probe}}$ 之下，matched cohort 於 11 維
> baseline 之外仍保有可偵測的 order-only 資訊（residual information detected）。

**不得**表述為 Dirac propagation、chiral transfer、幾何辨識或任何物理陳述。

本結果亦**不**主張：任何候選 $K$ 必能看見此資訊；此 bank 為最優；或此資訊與
$L_\theta$ 對應同一自由度。它只排除了 `CONTROL-UNFAIR-RISK` 與 `CONTROL-DEAD`。

---

## 6. Burned seeds 與 firewall

全部 48 段（每段 768）已首次生成並 **burned**：

- P/Q：`1_100_000_000 + 10⁷·b + 10⁶·j`，$b=0..5$、$j=0..3$；
- N：`1_200_000_000 + 10⁷·b + 10⁶·j`，$b=0..5$、$j=0..3$。

witness split（$b=3,4,5$）已揭露一次，依 §4.7 永久 burned；若需第二次必須另立
protocol amendment 並改用全新 seeds。

依 §5 第 3 項，ridge 權重、各族貢獻、逐樣本分數與任何「哪一族有效」的資訊
**未**出現在本文件、程式輸出或 commit message 中，留在 evaluator-side。本文件只公開
§0 允許的判決與 arm-level 樣本數、效應量、$p$ 值。Layer-2 feature extractor 的公開
API 只接受 `BlindedCase(case_id, copy_of_R)`，且新增 falsifier 拒絕直接傳入 sample／
coordinate-bearing payload。

**隔離能力的精確範圍.** 這是 API／程序層 firewall，不是 cryptographic secrecy：
repo 公開了 feature family、演算法與已 burned seeds，刻意修改 runner 的人理論上仍可
重算 calibration-derived weights。故未來候選設計必須在 clean construction process
中進行，禁止 import／執行本 probe module、讀取 evaluator-side artifacts，並以 C0
provenance／module-boundary audit 留證。不能把「正常輸出未顯示 weights」誇稱為其在
資訊論上不可取得。

依 acceptance spec §5.3，本次執行屬 candidate-independent protocol development，
**不消耗** candidate confirmatory budget，已記入 `docs/stage5c_development_log.md`。

全程未定義、未評估、未觀察任何候選 $K$。

---

## 7. 對 Freeze-1a 的影響

D.1 第 3 項的**前置可行性判決**完成，但該項**尚未交付**：統一的
observable／selector／smearing／norm contract 仍待撰寫。Freeze-1a 仍為 PENDING。
