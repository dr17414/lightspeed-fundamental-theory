# Stage 5C development log

狀態：**provisional append-only schema；尚未構成 Freeze-1a**

本帳記錄 candidate-independent exploratory／protocol-development 工作。它不要求
事前登記、不消耗 confirmatory budget，也不得保存或揭露 confirmatory holdout
結果。既有 entry 只可追加更正，不得覆寫或刪除。正式 schema 將與
`stage5c_protocol_amendment_log.md`、`stage5c_confirmatory_ledger.md` 一併在
Freeze-1a commit 固定；三本帳不得混用。

| entry id | UTC date | scope | question / action | inputs and RNG | result | candidate contact | holdout revelation | budget effect | artifacts |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| DEV-0001 | 2026-08-26 | C8.1／C8.4 | 在任何候選存在前，搜尋 order-dimension-$\le2$ 內、可匹配低階統計且 continuum chiral target 已知不同的 control；比較 $\lvert\theta\rvert=0.3,0.4,0.5,0.6,0.8$，最後選 $p_{\pm0.4}=1\pm0.4q(u)q(v)$；自我審計後把 $H/\sqrt N$ 加入 height baseline，避免 normalized CDF 吞掉絕對高度差 | PCG64DXSM；exploratory streams `1`, `20260826`, `20260875`, `20260876`, `20260891`, `20260892`, `20260923`, `20260924`, `982451717`, `982451749`, `982451781`；主 benchmark 四段 seeds `510000000..540000511`；$\kappa$ audits `710000000..760000255`，詳見 control 文件 | 可行性確認：$N=96$、每側 512 validation pool 在最終 11 維 baseline 得 205 matched pairs，coverage 0.4004，max SMD 0.1503，max KS 0.1415。完整 dimension-$\le2$ domain 未觸發 bounded-search exhaustion；$\kappa=1$ 限縮結果另記 DEV-0002 | none；未定義、未執行、未觀察任何 $K$ | none；所有列出的 exploratory／benchmark／audit seeds 均已 burned 為 development-only，不得改稱或重用為 confirmatory holdout | none | `docs/STAGE5C_C8_4_HARD_CONTROLS.md`; `analysis/stage5c_hard_controls.py`; `tests/test_stage5c_hard_controls.py` |
| DEV-0002 | 2026-08-26 | C8.1／C8.4 domain audit | 在加入 $H/\sqrt N$ 後，重驗 $\kappa=1$ 限縮 domain，並以 $\lvert\theta\rvert=0.3$ 做一次較弱擾動的 candidate-independent sensitivity check | $\theta=0.4$ 使用 `730000000..760000255`；$\theta=0.3$ 使用 `830000000..860000255`；全部 PCG64DXSM | $\theta=0.4$ 的 $\kappa=1$ filter-then-match 只得 60/243 pairs、coverage 0.2469、max SMD 0.2146，未達門檻；$\theta=0.3$ 亦只得 52/237、coverage 0.2194，故不以縮小 effect 迴避。完整 dimension-$\le2$ domain 的 source-of-record 仍通過。$\kappa=1$ 路徑明記未解，不得報 PASS | none | none；上述 seeds 全部 burned | none | `docs/STAGE5C_C8_4_HARD_CONTROLS.md` §2.1 |
