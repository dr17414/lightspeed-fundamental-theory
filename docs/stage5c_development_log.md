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
| DEV-0003 | 2026-08-27 | C8.1／C8.4 independent robustness review | 重驗 256-pool $\kappa=1$ 負結果是否其實由 pool size 造成；對完整 domain 做 512 與 768 raw-pool 跨 seed replication；以 Stage 5A `kappa()` 正式 predicate 重跑 512／768 filter-then-match；審查「covariate 只能增加」是否可加入 local target proxy 殺掉 Axis-B power | PCG64DXSM；source 四段擴至 `510000000..510000767`、`520000000..520000767`、`530000000..530000767`、`540000000..540000767`；額外 512 block 為 `810/820/830/840M` 各 512；768 replication blocks 為 `910–913M`、`920–923M`、`930–933M`、`940–943M` 各段 768；test/API-smoke ranges `670000000..670000007` 與 `680/681/682/683M` 各 64；本列所有 ranges 均為 development-only | 256 時未過濾亦失敗，故 DEV-0002 的 $\kappa$ 負面歸因撤回。完整 domain 的 512 blocks 僅 2/5 同時通過 pairs/coverage；768 的四個獨立 blocks全通過。768 source-of-record 得 361 pairs、coverage 0.4701、max SMD 0.1616、max KS 0.1080。$\kappa=1$ 在 512 得 194/492 pairs 且全 gate PASS；768 得 343/732、coverage 0.4686、max SMD 0.1686、max KS 0.1137。規格 v0.8 另加入 global-scalar/provenance/power-preservation qualification，吞掉 local continuum contrast 的新增 covariate 判 PROTOCOL-INVALID | none；未定義、未執行、未觀察任何 $K$ | none；上述全部 seeds 已 burned，不得作 confirmatory holdout；舊 512 單次正結果不再承重 | DEV-0002 的數據保留，但結論由「$\kappa=1$ 未解」更正為「256 對任何 domain 都不足」 | `docs/STAGE5C_ACCEPTANCE.md` v0.8；`docs/STAGE5C_C8_4_HARD_CONTROLS.md` §§2.1, 4–6；`analysis/stage5c_hard_controls.py` |
| DEV-0004 | 2026-08-27 | C8.4 out-of-sample feasibility 與 matched-cohort signal audit | 補做設計點固定後的 768-pool out-of-sample 驗證（因 `910–943M` 曾用於選擇 768，依 acceptance spec §5.3 不得回充可行性證據）；量測匹配前 signed SMD 以檢驗「global matching 不吃 local signal」是否成立；bootstrap 估 max-over-columns SMD 的維度效應 | PCG64DXSM；全新 out-of-sample blocks 為 `960/961/962/963M`、`970/971/972/973M`、`980/981/982/983M`，每段各 768；signed-SMD 與 bootstrap 診斷重用既有 `510/520/530/540M`、`910/911/912/913M`、`920/921/922/923M`、`960/961/962/963M` 的 768 pools，未新增抽樣；本列所有 ranges 均為 development-only | 三組 out-of-sample blocks 全部通過四道門檻：344/0.4479/0.1574/0.1076、335/0.4362/0.0905/0.0716、332/0.4323/0.1741/0.0843。匹配前 signed SMD 顯示 local density 差異大量洩漏進全域統計：`height_over_sqrt_n` 為 $+0.430/+0.463/+0.512/+0.366$（四組同號），`height_cdf_0.4/0.6` 與 `interval_abundance_2/4` 亦同號，`relation_density` 在零附近抖動。故「global matching 不會吃掉 local signal」的推論撤回；本文件確認範圍收窄為 matchability，residual discriminability 未確認。max-SMD 維度效應以 44 個 per-column 值 bootstrap：欄數 $11\to20$ 時 $E[\max]$ 由 0.105 升至 0.113、$P(\max>0.20)\approx0$，記為非阻塞診斷 | none；未定義、未執行、未觀察任何 $K$ | none；上述 12 段新 seeds 均已 burned，不得作 confirmatory holdout；`910–943M` 由 replication evidence 降級為選擇 768 的 exploratory evidence，同樣 burned | none；不消耗 candidate confirmatory budget | `docs/STAGE5C_C8_4_HARD_CONTROLS.md` §§4, 5.2–5.4, 8 |
| DEV-0005 | 2026-08-27 | C8.4 oracle attenuation 與 D.1-3 power audit | 以 like-for-like standardized effects 更正「matching 大量吃掉 local contrast」的推論；量化 Layer-1 estimator finite-$N$ 收縮；補查 arm N 等效性 claim 在保證樣本下界的 power | 重用已 burned 的 `960/961/962/963M`、`970/971/972/973M`、`980/981/982/983M` development pools；N cohort 診斷使用已 burned 的 development seeds；TOST power 另以不接觸任何登記 seed 的純分布計算／模擬；保留的 1.1B／1.2B ranges 未生成、未讀取 | 同 pair-count 的 random-vs-matched $d$ 為 $0.3859/0.4000$、$0.3598/0.3459$、$0.4269/0.4105$，平均只衰減約 $1.4\%$；先前 $0.552$ unpaired Cohen's $d$ vs $0.386$ paired $d$ 的比較因尺度不同而作廢。$\widehat L$ 的 expectation 約 $+0.057/-0.051$，相對 $L_\theta$ 向零收縮約 $38\%$。N 在 $\delta_N=0.15,n=576$ 時最保守 TOST power 約 $0.572$，故新增 $n_N\ge900$ gate（power 約 $0.910$；development 預期 $n\approx1041$ 時約 $0.958$），不放寬 equivalence margin | none；未定義、未執行、未觀察任何 $K$ | none；只用 burned development data 與純模擬，未觸及 1.1B／1.2B reserved witness ranges | none；不消耗 candidate confirmatory budget | `docs/STAGE5C_C8_4_HARD_CONTROLS.md` §4/§8；`docs/STAGE5C_D1_3_REFERENCE_PROBE.md` §§3, 4.6–4.7 |
| DEV-0006 | 2026-08-27 | D.1-3 residual-discriminability reference probe execution | 依 commit `49b5cf32` 凍結的 protocol 一次揭露 witness split，執行 Layer 1 與 P/N/Q 四個 claims；執行者另做兩項不改變判決、但未預登記的 baseline-leakage diagnostics | PCG64DXSM；P/Q 24 段為 `1_100_000_000 + 10^7 b + 10^6 j`、N 24 段為 `1_200_000_000 + 10^7 b + 10^6 j`，$b=0..5,j=0..3$，每段 768；randomization streams 依 frozen SHA256 rule；全部 48 段首次生成後 burned | 12 blocks 全過 gates；Layer1 $n=1014,d=+0.3801,p_{MC}=1/200001$；P 每側 $2304,d=+1.1311,p_{MC}=1/200001$；N $n=1140,d=+0.0015,p=3.074\times10^{-7}$ 且 TOST 等效；Q $n=1014,d=+0.8510,p_{MC}=1/200001$；四者皆過 Holm，adjudicator 判 **CONTROL-VIABLE**。兩項事後 diagnostics 未進 Holm、未改判；依 frozen §0 的 output-only rule 隔離其數值，不得作 evidence 或回流 construction | none；未定義、未執行、未觀察任何 $K$ | witness blocks $b=3,4,5$ 已揭露一次；全部 48 段永久 burned，不得作 future candidate holdout | none；candidate-independent development，不消耗 candidate confirmatory budget | `docs/STAGE5C_D1_3_PROBE_RESULTS.md`; `analysis/stage5c_reference_probe.py`; `tests/test_stage5c_reference_probe.py` |
| DEV-0007 | 2026-09-01 | C8 smearing／normalization／6a-S prereg | 在不生成任何新 control sample 的前提下，固定 C8 11 點共同使用的 probability-measure normalization、linear regulator、同 target finite-resolution random-measure metric、S1/S5/S6 門檻、finite-$N$ grid、seed manifest 與 failure semantics | 無 sampling；只作解析／結構設計。預留但尚未生成 PCG64DXSM seeds：plus `1_300_000_000 + 10^6 i + 10^4 j + k`、minus `1_400_000_000 + 10^6 i + 10^4 j + k`，$i=0..2,j=0..3,k=0..63$ | prereg 交付：$\varphi=1$、$\mathcal N=|\Sigma|$、$\epsilon=1/16$ Gaussian、80-mode Fourier signature、mean／energy margins 0.20、pair／ESS floor 32、coverage floor 0.005、$N=64,96,128$、4×64 blocks。未執行 6a-S，不報任何 selector PASS／FAIL | none；未定義、未執行、未觀察任何 $K$ | none；1536 個 reserved seeds 尚未生成或 burned，必須等 prereg commit 固定後才可一次執行 | none；不消耗 6a-E contrast 或 candidate confirmatory budget | `docs/STAGE5C_6A_S_PREREGISTRATION.md`; `analysis/stage5c_measure_prereg.py`; `tests/test_stage5c_measure_prereg.py` |
| DEV-0008 | 2026-09-01 | PR #12 pre-execution feasibility／null-bias audit | 在 1.3B／1.4B reserved streams 未生成前，獨立檢查 S1/S6 floor 可達性、energy-law estimator null bias、Fourier conjugation redundancy、$\epsilon$ sensitivity scope 與 Gaussian boundary mass statement；比較原 source-only depth band 與 order-dual pair-mass修法 | 外部 review 使用未完整列式的 2.6B development-only 區段，整段視為 burned、只作觸發審查的非 source-of-record evidence；本 repo 獨立核對使用 PCG64DXSM：plus `2_700_000_000 + 10^6 i + k`、minus `2_800_000_000 + 10^6 i + k`，$i=0..2,k=0..31$，共 192 seeds，全部 burned。兩 target 只各自做 floor feasibility，未形成或檢視 between-target contrast | 原 `source_depth_band(.8,1]` 在 $N=64/96/128$ 的兩個 target 各得 min pairs `2/4/8` 與 `2/3/6`，低於 32 比例 `1.000/.938/.625` 與 `1.000/.969/.531`，min coverage 約 `0.00136–0.00235`；Finding A 確認。改用 $d_-(x)+d_+(y)$ score-level pair-mass midquantile 後，五 bands 跨全部 audit cells 的 min pairs 於 $N=64/96/128$ 分別皆不低於 `106/216/397`，min coverage 皆不低於 `0.103/0.103/0.109`；不據此宣稱 reserved 6a-S PASS。解析確認 V-statistic 含 diagonal 產生 positive null bias，改 signed U-statistic；完整 80 shell 為 40 complex 自由度，改 nonredundant half-shell。S5 對 $\epsilon$ 的鑑別力不足，明文把 scale／boundary 驗收留給 E4；Gaussian mass preservation 限於 ambient $\mathbb R^4$ | none；未設計、import、執行或觀察任何 $K$；未計算 primary endpoint | none；1.3B／1.4B 仍完全未生成；2.6B external-review 區段與上述 2.7B／2.8B exact ranges 全部永久 burned | 修正發生於 prereg merge／reserved execution 前；不消耗 6a-E contrast 或 candidate confirmatory budget | `docs/STAGE5C_SELECTOR_FAMILY.md`; `docs/STAGE5C_6A_S_PREREGISTRATION.md`; `analysis/stage5c_selector_family.py`; `analysis/stage5c_measure_prereg.py`; `tests/test_stage5c_selector_family.py`; `tests/test_stage5c_measure_prereg.py` |
| DEV-0009 | 2026-09-02 | corrected PR #12 independent power／floor-risk audit | 在 correction head `a4c4887` 上獨立重驗全部 11 點的逐 causet floor、signed U-statistic null bias、$d_{\rm law}$ power scope 與最緊 floor cell；不更動任何 frozen constant、family member 或 capacity | 外部 review 使用與所有既有 development／reserved ranges 不相交的 PCG64DXSM 2.9B development-only 區段；因 exact seed manifest 未完整列入 repo，整個 2.9B 區段保守視為 permanently burned。11 點 × 3 個 $N$ × 2 targets × 64 causets 共 4224 次 floor evaluation；另對 `interval_exact(4)`, $N=64$ 每 target 各 384 causets。兩 targets 只逐臂檢查，未形成或解讀 between-target contrast | 全部 4224 evaluations 為 0 floor／coverage violations，overall min coverage $\ge0.0385$；五個 `endpoint_depth_mass_band` 在 $N=64$ 的已報 min pairs 為 101 以上，Finding A discharged。signed $\widehat E_U$ exact-null averages 約 $-3\times10^{-5}$ 至 $+9\times10^{-5}$，確認 V-bias 已移除；但 cross-$N$ stress comparison 的 $d_{\rm law}$ 多數僅約 `0.032–0.067`、最大已報 `0.165`，不足以接近 0.20，故該 gate 降級為 gross-breakage tripwire，通過不構成 law-stability 獨立證據。`interval_exact(4)`, $N=64$ 為已知 floor-binding cell：384 causets／target 的 minima `38/43`；development normal approximation 估正式 512 causets 至少一次低於 32 約 $3\%$，只作 pre-execution risk registration，觸發仍判 FAIL、不得改 floor 或排除 sample | none；未設計、import、執行或觀察任何 $K$；未計算 primary endpoint | none；1.3B／1.4B reserved streams 仍完全未生成；2.9B development segment 永久 burned | doc-only claim correction；不消耗 6a-E contrast 或 candidate confirmatory budget，不把 development audit 寫成 6a-S PASS | `docs/STAGE5C_6A_S_PREREGISTRATION.md`; `docs/STATUS.md` |
| DEV-0010 | 2026-09-02 | 6a-S $d_{\rm mean}$ tail-risk audit／runner freeze | 在 reserved execution 前登記 $d_{\rm mean}$ 最緊 null cell，並固定單臂 runner、write-ahead burned-seed ledger、contrast firewall 與 S1–S6 executable adjudicator | 外部 review 使用與 1.3B／1.4B、2.6–2.9B 及既有登記 ranges 不相交的 PCG64DXSM 3.0B development-only segment；exact manifest 未完整列入 repo，故整個 3.0B segment 保守視為 permanently burned。$N=64$ signature pool 每 target 768 causets；最緊 depth band 各做 5000 次同分布 64+64 block draws。runner freeze 本身只作 code／synthetic structural tests，不呼叫任何 preregistered seed | `endpoint_depth_mass_band(0.8,1.0)`, $N=64$ 的兩 target null $d_{\rm mean}$ mean `0.0628/0.0636`、p99 `0.122/0.123`、p99.9 `0.146/0.151`、5000 draws max `0.172/0.171`，0 次超過 0.20；登記為 binding cell 但不改 margin，正式超標仍 FAIL。新增 one-arm-only runner API；每 seed 在 generator 前先 append＋fsync burned claim；ledger 以 exclusive-create NDJSON 與 SHA256 chain 固定；per-causet／block-pair raw fields、signed $\widehat E_U$、arm／final verdict schema 完整；跨臂 combine 只接收 categorical verdicts；adjudicator 重算 S1–S6 並固定 `PROTOCOL-INVALID > FAIL > INCONCLUSIVE > PASS` precedence | none；未設計、import、執行或觀察任何 $K$；未計算 primary endpoint | none；1.3B／1.4B reserved streams 完全未生成；3.0B development segment 永久 burned | runner freeze precedes reserved execution；不消耗 6a-E contrast 或 candidate confirmatory budget | `docs/STAGE5C_6A_S_RUNNER_FREEZE.md`; `analysis/stage5c_6a_s_runner.py`; `tests/test_stage5c_6a_s_runner.py`; `docs/STAGE5C_6A_S_PREREGISTRATION.md`; `docs/STATUS.md` |
| DEV-0011 | 2026-09-02 | 6a-S reserved plus-arm execution incident／post-execution protocol audit | 依 frozen main `3bdc062a` 一次執行 plus arm；在 categorical `PROTOCOL-INVALID` 後，只讀該單臂 ledger 重算被 precedence 遮住的 S1／S5／S6，定位 identity-check defect 並決定 amendment blocker | PCG64DXSM；plus manifest `1_300_000_000 + 10^6 i + 10^4 j + k`，$i=0..2,j=0..3,k=0..63$，共 768 seeds，全部先 durable claim 再生成；raw NDJSON SHA-256 `32338ee83000c198747c1bd9cd5c9e98a5d054abde25e804be83533fe7de81e1`。minus 1.4B manifest 未 claim、未生成、未讀取；未形成 between-target contrast | 凍結 adjudicator 對 uniform-weight Kish ESS 的理論整數恆等式使用共用 $10^{-12}$ 絕對容差；roundoff 最大 $1.8645\times10^{-11}$，故 `all_relations` 與五個 depth bands 正式為 `PROTOCOL-INVALID`，其餘五點單臂 PASS。post-execution raw-field audit 對六個 invalid selectors 得 S1／S5／S6 failure counts 全為 0：min pairs `99`、min coverage `0.1009`、max $d_{\rm mean}=0.07763$、max $d_{\rm law}=0.04117$；mass／TV 最大誤差 $6.67\times10^{-16}$，無 non-finite 或 S2／S3／S4 false row。這不改判既有 verdict，只證明沒有被 precedence 隱藏的 scientific floor／margin failure；6a-S 未完成 | none；未設計、import、執行或觀察任何 $K$；未計算 primary endpoint | plus 1.3B 全部永久 burned 並依使用者明確授權公開完整 ledger；minus 1.4B 保持未揭露。不得重跑 plus、從原 ledger 靜默重判或把單臂 audit 回流成候選輸入 | 原 6a-S protocol-invalid；不消耗 6a-E contrast／candidate confirmatory budget。任何 replacement plus 或 minus 執行前，必須先 commit／review／merge protocol amendment，固定尺度穩健 ESS check 與 fresh-seed lifecycle | `docs/STAGE5C_6A_S_EXECUTION_INCIDENT.md`; `results/README.md`; `results/stage5c_6a_s_plus_protocol_invalid.ndjson.gz.part00`–`part17`; `docs/STATUS.md` |
| DEV-0012 | 2026-09-04 | 6a-S runner v2 full-arm development dress rehearsal | 依已 review／merge 且 main CI 通過的 commit `9504abf3989a57a75ebb1359c872a36ba4190549`，以正式 `run-arm` code path 一次執行 3.1B plus-target rehearsal；只封存 custody、record counts 與 categorical verdict，不公開或解讀 per-causet／block-pair 數值 | PCG64DXSM；manifest `3_100_000_000 + 10^6 i + 10^4 j + k`，$i=0..2,j=0..3,k=0..63$，共 768 seeds，均先 durable claim 再生成並永久 burned。實際 runtime：`sys.version=3.12.13 (main, Aug  7 2026, 02:25:39) [Clang 22.1.3 ]`、NumPy `2.3.5`、SciPy `1.17.0`。raw external NDJSON 6,842,118 bytes、SHA-256 `cf5f3584f3a8e193f0ef49a812c8acd41c1250c982581acb256ae7cbe03e352c`；protocol digest `1343eb8eeaa6c7fe22c0d0f12a01f5d080c3e76dc5014aabafb69b5e66629707`；start-registry hash `cfea86cf3d1aa827fad9daee8648bc07eb57a49cc48626b493f8a713fe90f2f2` | hash chain 與 schema 重驗通過；10,196 records：header 1、seed claims 768、generated 768、causet-selector 8,448、block-pair 198、arm-data-complete 1、arm-selector-verdict 11、arm-complete 1。categorical adjudication 為 11/11 `6a-S PASS`（`all_relations`、`links`、`interval_exact(1..4)`、五個 `endpoint_depth_mass_band`）；0 `PROTOCOL-INVALID`、0 `INCONCLUSIVE`。此結果只證 runner v2 dress rehearsal mechanically clean，不是 between-target 或 selector-viability 結論 | none；未設計、import、執行或觀察任何 $K$；未計算 primary endpoint | 3.1B plus-development manifest 全部永久 burned；raw ledger 留在 checkout 外，未獲明確授權前不公開。不得重跑、不得與任何 minus ledger 配對，不得作 replacement control／comparison／calibration／power input | development custody milestone；不消耗 6a-E contrast 或 candidate confirmatory budget。DEV-0012 attestation／registry commit 經 CI 與獨立 review／merge 前，1.5B replacement plus 仍鎖定；1.4B minus 亦未 claim／未生成 | `docs/stage5c_6a_s_dress_rehearsal_attestation.json`; `docs/stage5c_6a_s_burn_registry.json`; external ledger SHA-256；`docs/STATUS.md` |
| DEV-0013 | 2026-09-04 | 6a-S replacement-reserved plus execution | 在 DEV-0012／attestation／registry 經 review、CI、merge 後，依 main `1e867e7a86640afd963f362482acf69ef3605823` 與同一 formal runtime 一次執行 1.5B replacement plus；其 categorical verdict 只依自身 ledger 與 frozen adjudicator，不引用 3.1B pattern 作解釋、校正或重判 | PCG64DXSM；manifest `1_500_000_000 + 10^6 i + 10^4 j + k`，$i=0..2,j=0..3,k=0..63$，共 768 seeds，均先 durable claim 再生成並永久 burned。prerequisite 為外部 DEV-0012 ledger SHA-256 `cf5f3584f3a8e193f0ef49a812c8acd41c1250c982581acb256ae7cbe03e352c`。實際 runtime：`sys.version=3.12.13 (main, Aug  7 2026, 02:25:39) [Clang 22.1.3 ]`、NumPy `2.3.5`、SciPy `1.17.0`。raw external NDJSON 6,843,989 bytes、SHA-256 `1e515ca81c3e32fb11ff7e3a90d810a1e5264ce5217fc722775f3765165696cc`；protocol digest `1343eb8eeaa6c7fe22c0d0f12a01f5d080c3e76dc5014aabafb69b5e66629707`；start-registry hash `cb18709d0024f4e4d58de870b8537491885b848a948c84dc87d079a2e3feabda` | hash chain 與 schema 重驗通過；10,196 records：header 1、seed claims 768、generated 768、causet-selector 8,448、block-pair 198、arm-data-complete 1、arm-selector-verdict 11、arm-complete 1。此 arm 自身 categorical adjudication 為 11/11 `6a-S PASS`（`all_relations`、`links`、`interval_exact(1..4)`、五個 `endpoint_depth_mass_band`）；0 `PROTOCOL-INVALID`、0 `INCONCLUSIVE`。這是單臂正式 verdict，不形成 combined verdict 或 selector viability 結論 | none；未設計、import、執行或觀察任何 $K$；未計算 primary endpoint | 1.5B replacement-plus manifest 全部永久 burned；raw ledger 留在 checkout 外，未獲明確授權前不公開。不得重跑、不得引用 DEV-0012 解釋本 arm、不得在 1.4B 前形成 between-target contrast | replacement-plus custody milestone；不消耗 6a-E contrast 或 candidate confirmatory budget。DEV-0013 attestation／registry commit 經 CI 與獨立 review／merge 前，1.4B minus 仍鎖定 | `docs/stage5c_6a_s_replacement_plus_attestation.json`; `docs/stage5c_6a_s_burn_registry.json`; external ledger SHA-256；`docs/STATUS.md` |
| DEV-0014 | 2026-09-04 | 6a-S replacement-reserved minus execution | 在 DEV-0013／plus attestation／registry 經 review、CI、merge 後，依 main `ce8bd8b0fd2930ddc746604588e807c79825e8be` 與相同 formal runtime 一次執行 1.4B replacement minus；本 milestone 只封存 minus 單臂 custody 與 categorical verdict，未呼叫 combiner、未形成或讀取 between-target numerical contrast | PCG64DXSM；manifest `1_400_000_000 + 10^6 i + 10^4 j + k`，$i=0..2,j=0..3,k=0..63$，共 768 seeds，均先 durable claim 再生成並永久 burned。prerequisite 為外部 DEV-0013 plus ledger SHA-256 `1e515ca81c3e32fb11ff7e3a90d810a1e5264ce5217fc722775f3765165696cc`。實際 runtime：`sys.version=3.12.13 (main, Aug  7 2026, 02:25:39) [Clang 22.1.3 ]`、NumPy `2.3.5`、SciPy `1.17.0`。raw external NDJSON 6,851,483 bytes、SHA-256 `61139d83b2ad361073150c293b87883e12cdc6a148e49de72cb3eb9e9944d853`；protocol digest `1343eb8eeaa6c7fe22c0d0f12a01f5d080c3e76dc5014aabafb69b5e66629707`；start-registry hash `f80267225ac11b491c273ee13914489c0fa3ba1cb134dec35cc1aa353d71fc77` | hash chain 與 schema 重驗通過；10,196 records：header 1、seed claims 768、generated 768、causet-selector 8,448、block-pair 198、arm-data-complete 1、arm-selector-verdict 11、arm-complete 1。minus arm 自身 categorical adjudication 為 11/11 `6a-S PASS`（`all_relations`、`links`、`interval_exact(1..4)`、五個 `endpoint_depth_mass_band`）；0 `PROTOCOL-INVALID`、0 `INCONCLUSIVE`。兩臂皆通過臂內 6a-S 不預示任何 contrast 方向或大小 | none；未設計、import、執行或觀察任何 $K$；未計算 primary endpoint | 1.4B replacement-minus manifest 全部永久 burned；raw ledger 留在 checkout 外，未獲明確授權前不公開。不得重跑；不得評論 plus／minus ledger size 差異；DEV-0014 複核前不得執行 combined adjudication | replacement-minus custody milestone；不消耗 6a-E contrast 或 candidate confirmatory budget。DEV-0014／final registry commit 經 CI 與獨立 review／merge 前，不執行 combiner或任何 endpoint 計算 | `docs/stage5c_6a_s_burn_registry.json`; external ledger SHA-256；`docs/STATUS.md` |
| DEV-0015 | 2026-09-05 | 6a-S replacement categorical combine | 在 DEV-0014／final registry 經 review、CI、merge 後，於 clean main `4342b6af2917373ff549cc9084e6cb7966c431ea` 手動重算並核對兩份 registered input hashes，再一次執行 frozen categorical-only combiner；不修改 runner、不開啟 6a-E、不形成 numerical contrast | inputs：1.5B plus SHA-256 `1e515ca81c3e32fb11ff7e3a90d810a1e5264ce5217fc722775f3765165696cc`、1.4B minus SHA-256 `61139d83b2ad361073150c293b87883e12cdc6a148e49de72cb3eb9e9944d853`。combiner 重新驗證兩臂 hash chain／schema／categorical adjudication、plus→minus positional order、共同 protocol digest `1343eb8eeaa6c7fe22c0d0f12a01f5d080c3e76dc5014aabafb69b5e66629707` 與逐字相同 runtime。external combined NDJSON 4,718 bytes、SHA-256 `3bc4c643aca21fd7f8cf7695fe0af0720ddd0c760b78830bf1cfb0101cf02b20` | combined ledger 共 12 records：header 1、selector-verdict 11；11/11 final verdict 均為 `6a-S PASS`。header 固定 `target=categorical-verdicts-only`、`between_target_numeric_data=ABSENT_BY_SCHEMA`，rows 只含 selector／parameters、plus／minus categorical verdict 與 final categorical verdict。此結果完成 6a-S batch prefilter，只表示 11 selectors 可進 6a-E，不是 `SELECTOR-VIABLE`、target separation 或 primary-endpoint 證據 | none；未設計、import、執行或觀察任何 $K$；未計算 $\mathfrak I_G$ 或 primary endpoint | 沒有生成或重用 seed；三份 raw ledgers 均留在 checkout 外，未獲明確授權前不公開。未直接檢視 per-causet／block-pair 數值，未形成 between-target numerical contrast | 6a-S prefilter milestone；不消耗 6a-E contrast 或 candidate confirmatory budget。下一步必須先凍結含 $\mathfrak I_G$ 完整路徑、near-zero gate 與 selector 進場規則的 6a-E preregistration，並經獨立 review／merge，之前不得打開 arm numerical fields | `analysis/stage5c_6a_s_runner.py`; external input／combined ledger SHA-256；`docs/STAGE5C_6A_S_PREREGISTRATION.md`; `docs/STATUS.md` |
| DEV-0016 | 2026-09-06 | 6a-E item-2 joint-law calibration | 在任何正式 6a-E manifest、arm ledger 或 endpoint 存在前，以 known 4D Gaussian joint law 分開驗 matched-cohort cluster covariance consistency 與 finite-sample null coverage／type-I calibration；另用刪除 cross-arm blocks 的錯誤 schema 作 falsifier，並以 planted feature pools觸發 matching attrition／failure paths | PCG64DXSM development-only streams；每格 identity 由 `development-only-item2-null-calibration-not-6a-e`、$m$、$\rho$、32 independent clusters、2048 replications 的 SHA-256 唯一導出。$m\in\{192,384\}$、$\rho\in\{-3/4,0,3/4\}$；不是 item-9 manifest，沒有 claim 或保留正式 seed。matching suite 是 deterministic arrays、無 RNG、無 endpoint | 六個正確-schema cells 的 covariance maximum standardized discrepancy $\le2.505$，0.95 coverage 為 0.9404–0.9517，全部落在事前 99.9% binomial acceptance interval；錯誤 independent-marginals schema 於 $(192,-3/4)$ coverage 0.8418、type-I 0.1582，明確被拒。256/256 clean、191/256 cohort failure、192/600 coverage failure、zero-match 與 zero-scale 均得預期 typed verdict | none；未設計、import、執行或觀察任何 $K$ | none；未讀任何 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；development simulation stream 不得回充 selection／confirmation／power | none；純 candidate-independent protocol calibration，不配置 scientific alpha、effect floor、equivalence margin 或 confirmatory budget | `docs/STAGE5C_6A_E_JOINT_MATCHED_LAW.md`; `analysis/stage5c_joint_matched_law.py`; `tests/test_stage5c_joint_matched_law.py` |
| DEV-0017 | 2026-09-07 | DEV-0016 falsifier capability-boundary correction | 依 PR #26 initial-head 獨立複核，區分「刪除 nonzero cross-arm blocks」與「covariance target 正確但 reference df 錯置」兩類 falsifier；保留 DEV-0016 原列，追加其能力邊界，不把低檢定力的未拒絕寫成認證 | 獨立 reviewer 重寫 exact-Gaussian Hotelling simulation，只借用 planted covariance 定義，使用未列入 repo、不得回充正式 6a-E 的 development-only 200,000 replications；本修訂本身不新增 repo RNG stream、不生成 seed | correct paired schema 在 $\rho=-3/4,0,3/4$ 的 coverage 為 0.9494–0.9500，符合 exact 0.95；`independent-marginals` 在 $\rho=-3/4$ 為 0.8378、$\rho=3/4$ 為 0.99997，重現 cross-block falsifier。$\rho=0$ 為 0.9591：因 cross blocks 真為零，covariance target 正確，錯誤只在 reference df；DEV-0016 的 2048-rep／99.9% band 無力穩定檢出這個約 0.009 shift。故 $\rho=0$ 未拒絕不構成 falsifier-success 證據；items 4／5 須另交付有事前 power 或解析 oracle 的 df-only falsifier | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；review simulation 不得作 selection／confirmation／power input | none；doc-only capability correction，不改 scientific alpha、effect floor、equivalence margin 或 confirmatory budget | `docs/STAGE5C_6A_E_JOINT_MATCHED_LAW.md`; `docs/STAGE5C_6A_E_PREREGISTRATION_DRAFT.md`; `docs/STATUS.md` |
| DEV-0018 | 2026-09-07 | 6a-E item-7 E4 fixed-scale well-posedness feasibility | 在任何正式 6a-E manifest、arm ledger 或 candidate endpoint 存在前，固定 $\epsilon=1/16$ Gaussian-mixture topology、contact／box／causal leakage、pairing existence、continuum enclosure與兩個 independent numerical paths；另注入 resource exhaustion 與 estimated-error undercoverage capability check | deterministic three-atom interior mixture、two-atom near-boundary／near-contact mixture及 malformed synthetic inputs；無 RNG、無 seed、無 candidate data。$\theta=(-0.4,0,0.4)$；enclosure pair-axis levels $(16,32,64)$、transverse cells $n/4$、64-ULP outward margin；GL order 32；Genz–Malik `rtol=2^{-14}`、`atol=2^{-30}`、cap 4096 | 完整 $\theta$ suite 中 GL32 與 Genz–Malik 均落在 analytic positive-cell enclosure 並通過 item-3 closed-ball／strict-nonzero certification；near-boundary／near-contact case leakage 非零但不 renormalize 且 pairing clean。SciPy algorithm error 明確只作 diagnostic；validated $\eta_Q$ 由 enclosure farthest-corner distance 產生。注入 non-converged adaptive status 得 `INCONCLUSIVE/ADAPTIVE_RESOURCE_CAP`；boundary/contact centres、非 probability weights、超 cap atoms與未登記 $\theta$ 均在 pairing 前拒絕 | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；deterministic planted matrices不得作 selection／confirmation／power input | none；純 candidate-independent protocol feasibility，不配置 scientific alpha、effect floor、equivalence margin、df-only falsifier 或 confirmatory budget | `docs/STAGE5C_6A_E_WELLPOSEDNESS.md`; `analysis/stage5c_e4_wellposedness.py`; `tests/test_stage5c_e4_wellposedness.py`; `docs/STATUS.md` |
| DEV-0019 | 2026-09-08 | DEV-0018 review-finding correction | 依 PR #28 automated review，補齊 adaptive diagnostic 的 non-finite fail-closed 分支，並消除 sub-ULP strict geometry 被 CDF limiting-value 捨入誤判的路徑；保留 DEV-0018 原列，不把獨立 reviewer 對舊 head 的 GO 延伸到修訂 head | deterministic positive subnormal geometry 與 monkeypatched backend outputs；無 RNG、無 seed、無 candidate data，不變更任何 frozen E4 數值常數 | finite matrix 搭配 non-finite algorithm-error diagnostic 現固定為 `INCONCLUSIVE/NONFINITE_BACKEND`；strict topology 由 pairing 前的 exact binary64 coordinate inequalities 驗證，CDF retained/leakage 只作有限 probability diagnostic，故正 sub-ULP 座標／gap 即使顯示 limiting retained masses $1/16$／$1/4$ 仍不被誤拒。兩條精準 regression 鎖定此行為 | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；修訂 head 仍須重新 review／CI | none；review correction，不配置或消耗 scientific alpha、effect floor、equivalence margin、df-only falsifier 或 confirmatory budget | `docs/STAGE5C_6A_E_WELLPOSEDNESS.md`; `analysis/stage5c_e4_wellposedness.py`; `tests/test_stage5c_e4_wellposedness.py`; `docs/STATUS.md` |
| DEV-0020 | 2026-09-08 | DEV-0019 analytic leakage-bound correction | 在 revised head exact-merge 前依 refreshed automated review 重驗 finite-box Gaussian mass；確認 opposite-boundary tail 使「strict interior 推出 box leakage $<15/16$」本身為假，而不只是 binary64 CDF 判定問題；保留 DEV-0018／0019 原列並再次撤回對舊 head 的合併資格 | deterministic smallest-positive-binary64 geometry；400-digit `mpmath` analytic oracle；無 RNG、無 seed、無 candidate data，不變更任何 frozen E4 數值常數 | 一維 open-boundary retained-mass infimum 為 $b_*=\Phi(16)-1/2=1/2-\Phi(-16)$，故四維 box leakage 的正確 strict bound 是 $1-b_*^4$，略大於 $15/16$。high-precision regression 確認 sub-ULP plant 的 exact box leakage 嚴格大於 $15/16$ 且嚴格小於 $1-b_*^4$；causal leakage $<3/4$ 不受 opposite-box tail 影響。binary64 diagnostics 仍不得重新裁決已驗證 topology | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；再次修訂 head 仍須重新 review／CI | none；analytic-contract correction，不配置或消耗 scientific alpha、effect floor、equivalence margin、df-only falsifier 或 confirmatory budget | `docs/STAGE5C_6A_E_WELLPOSEDNESS.md`; `analysis/stage5c_e4_wellposedness.py`; `tests/test_stage5c_e4_wellposedness.py`; `docs/STATUS.md` |
| DEV-0021 | 2026-09-08 | DEV-0020 constraint-preserving hardening | 重驗把正確 universal boundary-limit 界寫回契約是否會意外放寬原 $15/16$ gate；決定保留原 gate，將 strict topology validity 與 leakage admissibility 分開，並以 cancellation-safe arithmetic 實際裁決 mixture mass | deterministic interior／smallest-positive-binary64 mixtures；`erf` near-boundary gain、`erfc` opposite-tail、`log1p`／`expm1` 與 `math.fsum`；400-digit oracle 不變；無 RNG、無 seed、無 candidate data | 新 `box_leakage_bound_validated` 在 rounded retained mass 等於 $1/16$ 時仍能保留約 $10^{-58}$ 尺度的負 excess，故 sub-ULP plant 為 topology-valid 但 `STRUCTURAL_LEAKAGE_INVALID`。一般 interior、near-boundary／near-contact plants 仍 clean，原 $<15/16$ gate 未放寬；universal $1-b_*^4$ 只保留為解析背景，不作替代 acceptance threshold | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；再次修訂 head 仍須重新 review／CI | none；constraint-preserving review hardening，不配置或消耗 scientific alpha、effect floor、equivalence margin、df-only falsifier 或 confirmatory budget | `docs/STAGE5C_6A_E_WELLPOSEDNESS.md`; `analysis/stage5c_e4_wellposedness.py`; `tests/test_stage5c_e4_wellposedness.py`; `docs/STATUS.md` |
| DEV-0022 | 2026-09-09 | DEV-0021 weight-normalization correction | 依 PR #28 head `996ceb24` automated review，檢查 cancellation-safe mixture excess 是否與 validator 的 $10^{-12}$ probability-sum tolerance 一致；確認只加權 per-atom excess 會漏掉 normalization offset | deterministic single boundary-near atom；unit weight 與 `1-5e-13` underweight inputs；無 RNG、無 seed、無 candidate data，不改既有 tolerance 或 gate | 完整 retained-mass excess 改為 $\sum_iw_i(B_i-1/16)+(\sum_iw_i-1)/16$，兩部分進同一 `math.fsum`。regression 確認 atom 在 unit weight 時通過，但 accepted underweight mixture 的 rounded retained mass 不大於 $1/16$ 且固定 `STRUCTURAL_LEAKAGE_INVALID`；舊缺項會在此案例誤過 | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；再次修訂 head 仍須重新 review／CI | none；fail-closed completeness correction，不配置或消耗 scientific alpha、effect floor、equivalence margin、df-only falsifier 或 confirmatory budget | `docs/STAGE5C_6A_E_WELLPOSEDNESS.md`; `analysis/stage5c_e4_wellposedness.py`; `tests/test_stage5c_e4_wellposedness.py`; `docs/STATUS.md` |
| DEV-0023 | 2026-09-09 | DEV-0022 causal normalization correction | 依 PR #28 head `f622404f` exact-head automated review，檢查 causal leakage gate 是否也完整納入 validator 容許的 probability-sum tolerance；確認 strict per-atom causal gaps 不足以在 $\sum_iw_i<1$ 時推出 mixture retained mass $>1/4$ | deterministic single atom with one-ULP positive causal gaps；unit weight 與 `1-5e-13` underweight inputs；無 RNG、無 seed、無 candidate data，不改既有 tolerance 或 gate | 新增 cancellation-safe causal excess：以 `erf(gap/(2*epsilon))`、`log1p`／`expm1` 保存 one-ULP gain，並將 $(\sum_iw_i-1)/4$ 與 weighted per-atom excess 放入同一 `math.fsum`。regression 確認 box gate 仍通過，但 accepted underweight mixture causal retained mass 不大於 $1/4$ 時固定 `STRUCTURAL_LEAKAGE_INVALID` | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；再次修訂 head 仍須重新 review／CI | none；fail-closed completeness correction，不配置或消耗 scientific alpha、effect floor、equivalence margin、df-only falsifier 或 confirmatory budget | `docs/STAGE5C_6A_E_WELLPOSEDNESS.md`; `analysis/stage5c_e4_wellposedness.py`; `tests/test_stage5c_e4_wellposedness.py`; `docs/STATUS.md` |
| DEV-0024 | 2026-09-09 | DEV-0023 exact weight-sum correction | 依 PR #28 head `8b4e5009` exact-head automated review，檢查 `math.fsum` 最終捨入是否仍可消掉小於半 ULP 的真實 normalization deficit；確認 `[0.5,nextafter(0.5,0)]` 的精確 binary64 總和為 $1-2^{-54}$，但 `fsum` 回傳 1 | deterministic duplicated atom with one-ULP causal gaps；兩個 weights 的普通總和捨入為 1；100-digit `mpmath` oracle；無 RNG、無 seed、無 candidate data，不改既有 tolerance 或 gate | probability-sum validation 與 box／causal mixture-excess 判號改用輸入 binary64 的 exact dyadic rationals；normalization offset 不再先捨入成 binary64。regression 確認 box gate 通過，但高精度 causal retained mass 低於 $1/4$，故固定 `STRUCTURAL_LEAKAGE_INVALID` | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；再次修訂 head 仍須重新 review／CI | none；fail-closed arithmetic correction，不配置或消耗 scientific alpha、effect floor、equivalence margin、df-only falsifier 或 confirmatory budget | `docs/STAGE5C_6A_E_WELLPOSEDNESS.md`; `analysis/stage5c_e4_wellposedness.py`; `tests/test_stage5c_e4_wellposedness.py`; `docs/STATUS.md` |
| DEV-0025 | 2026-09-12 | 6a-E items 4／5 statistical-region forms | 在任何正式 6a-E seed、arm ledger 或 candidate endpoint 存在前，固定 E1／E2 二維 simultaneous region、E2 same-target null-pair identities、E3 ordered component rules、item-3 numerical-error propagation與 df-only falsifier；避免以 observed covariance 選 projection 或以 matched-pair count冒充 inferential df | 無 RNG、無 seed、無 candidate data。region 使用 endpoint sharp widths $(3,1)$、Bonferroni–Student rectangle、independent-cohort df $B-1$、$B\ge32$、item-2 calibrated matched-count domain $[192,384]$、local $\alpha\le0.01$；E2 A/B spec 不接受 seed且不呼叫 generator；df-only oracle 固定 $B=32,m=192$ 的 exact Gaussian Student law | E1 complete region 須嚴格離開 closed $1/20$ normalized effect box；兩個 E2 null regions須各自嚴格進入 open $1/20$ box。E3 chiral／diffusion floors固定為解析最小 effect $1/5$ 的一半；wrong-support 以保留 cross-arm covariance 的 paired contrast region嚴格清除完整域 gap $0.0513032\ldots$ 的一半，明確取代 item-6 早期 marginal-region 不相交寫法。item-3 per-endpoint error只沿 matched indices以 triangle inequality向外加入。df-only falsifier保持 covariance target 不變、只把 df $31\to6143$，解析 per-component coverage $0.995\to0.991453\ldots$，故無 Monte Carlo power ambiguity | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint；本 delivery 待獨立 review／CI／merge | none；只固定 region forms與既有 $\alpha$ 上限；item 8 仍須配置完整 claim-family spending、successor reserve及 detection／equivalence power-derived cohort floors | `docs/STAGE5C_6A_E_STATISTICAL_REGIONS.md`; `analysis/stage5c_statistical_regions.py`; `tests/test_stage5c_statistical_regions.py`; `docs/STAGE5C_6A_E_PREREGISTRATION_DRAFT.md`; `docs/STATUS.md` |
| DEV-0026 | 2026-09-13 | DEV-0025 interval/provenance hardening | 依 PR #30 initial head `2f97f84e` exact-head automated review，檢查 strict region boundaries 的 directed rounding、item-3 error provenance及多步 numerical-radius rounding；確認三者均可在原 API 造成 false PASS 或無法證明輸入身分 | reviewer raw $3\\times0.05$ boundary、192 identical pairs 的 binary64 errors `2.1286740303373657`／`0.8897833198641344`，以及 failed／錯 certification ID／錯 pool／錯 arm／錯 endpoint typed injections；無 RNG、seed或 candidate data | statistical／total widths向上捨入，region lower／upper與 normalization分別向外捨入；`CertifiedEndpointPool` 綁定 CLEAN item-3 result、frozen ID、pool、arm與 matched endpoint row；pair addition、總和與除以 $M$ 以 exact rationals完成後向上捨入，並由綁定 IDs／arms／$B$／$M$ 的 `ValidatedNumericalHalfWidth` 進入 builder，拒絕裸 vector或跨 comparison 移用。原 head GO 被 supersede，修訂 head須重新 review／CI | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint | none；不改 $B\\ge32$、$\\alpha\\le0.01$、effect／equivalence floors、df-only oracle或 item-8 multiplicity／power義務 | `docs/STAGE5C_6A_E_STATISTICAL_REGIONS.md`; `analysis/stage5c_statistical_regions.py`; `tests/test_stage5c_statistical_regions.py`; `docs/STAGE5C_6A_E_PREREGISTRATION_DRAFT.md`; `docs/STATUS.md` |
| DEV-0027 | 2026-09-13 | DEV-0026 producer-bound provenance／E3 normalization correction | 依 PR #30 head `42cc356f` exact-head automated review，檢查 typed wrappers 是否仍可由 caller 手造或 relabel，以及 E3 direction-zero equivalence 是否完整沿用 directed normalized bounds；確認公開 numerical-width constructor、事後 pool labels與 raw binary64 margin 均可造成 false PASS | direct CLEAN `CertificationResult`／direct zero `ValidatedNumericalHalfWidth` injections、另一 pool／arm／row provenance，及 reviewer binary64 upper `0.15 < 3*0.05` 但 directed normalization 恰為 `0.05` 的 strict-boundary case；無 RNG、seed或 candidate data | `certify_pairing` 現把 `EndpointCertificationProvenance` 與 result 同時 producer-seal；pool adapter 不收 caller labels，只從 sealed rows 推導 identities。numerical width 無公開建構路徑，只由 matched aggregation 的 private token 產生。E3 equivalence 直接比較 outward normalized bounds，恰觸 `0.05` 固定 `FAIL`。`42cc356f` 的 GO 被 supersede，修訂 head須重新 review／CI | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint | none；不改 $B\\ge32$、$\\alpha\\le0.01$、effect／equivalence floors、df-only oracle、closure matrix或 item-8 multiplicity／power義務 | `docs/STAGE5C_6A_E_CERTIFICATION.md`; `docs/STAGE5C_6A_E_STATISTICAL_REGIONS.md`; `analysis/stage5c_numerical_certification.py`; `analysis/stage5c_statistical_regions.py`; `tests/test_stage5c_statistical_regions.py`; `docs/STAGE5C_6A_E_PREREGISTRATION_DRAFT.md`; `docs/STAGE5C_D1_3_OBSERVABLE_CONTRACT.md`; `docs/STATUS.md` |
| DEV-0028 | 2026-09-16 | DEV-0027 source-row custody／ensemble-binding correction | 依 PR #30 head `e10c6d37` exact-head automated review，檢查 producer seal 是否只是認證 caller 自報 labels，以及同 arms／$B$／$M$／law ID 的不同 matched ensembles 能否互換 authenticated numerical width；兩者均可造成較小 error radius 被套到錯誤 source | arbitrary `provenance=` keyword與直接 `EndpointCertificationSourceRow` construction；兩個 counts／arms／law ID 完全相同但 pool／calibration identities 不同的 deterministic ensembles；無 RNG、seed或 candidate data | `certify_pairing` 移除任意 provenance keyword；完整 implementation pool 先由 private-token producer綁成 payload＋identity同體的 source rows，row index只由 enumeration產生。numerical width與 region input另各自綁定 canonical source-ensemble SHA-256，納入 matching identities／indices、matched endpoints與 ensemble statistics，fingerprint 不同即拒絕。`e10c6d37` 的 GO 被 supersede，修訂 head須重新 review／CI；item 9仍須把 pool identity與正式 custody manifest鎖定 | none；未設計、import、執行或觀察任何 $K$ | none；未讀 arm ledger、未生成或 claim 正式 6a-E seed、未形成 arm endpoint | none；不改 item-3 error calculus、$B\\ge32$、$\\alpha\\le0.01$、effect／equivalence floors、df-only oracle、closure matrix或 item-8 multiplicity／power義務 | `docs/STAGE5C_6A_E_CERTIFICATION.md`; `docs/STAGE5C_6A_E_STATISTICAL_REGIONS.md`; `analysis/stage5c_numerical_certification.py`; `analysis/stage5c_statistical_regions.py`; `tests/test_stage5c_statistical_regions.py`; `docs/STAGE5C_6A_E_PREREGISTRATION_DRAFT.md`; `docs/STAGE5C_D1_3_OBSERVABLE_CONTRACT.md`; `docs/STATUS.md` |

## 另軌 X 紙上開發的 current 權限對照

[ACT-X-0001／E0](STAGE5C_EXPLORATION_ACTIVATION.md) 經核准合併 main 後，才允許
另軌紙上 X-I／X-C。上方 DEV 列的 candidate-independent scope／數字是原時點歷史，
不改寫為探索候選結果。日後 X 新 entry 須另列 X problem／model version、active SHA、
來源與 EXP 依賴、定義域／條件前提、採用／失敗／撤回及對 criterion 的影響；
不冒稱 candidate-independent，不能因不佔統計預算就執行 RNG／producer／正式 runner。
本次尚無 X model／新 DEV 科學 entry；權限決定在 activation register、接觸在 EXP-0021。

## 紙上 X 問題登記（不冒稱模型或科學結果）

| Problem ID | 操作者選擇／權限 | 產物與來源 | 模型／執行／判決 |
| :--- | :--- | :--- | :--- |
| X-SIGNAL-RESPONSE-P0.1 | 本輪選擇訊號回應；ACT-X-0001 生效 SHA `0c386716701589c9a6b0b799636a808aacb9ade5` | [只定問題契約](foundations/signal_response_problem_contract_v0_1.md)，依公開 B4／B6 的必要條件、Q／Z／R／L；EXP-0022。有限宣告紀錄窗口、準備／接收／回應／回讀的識別與實現義務 | model ID NONE；未定 operator／law／state／材料／參數，未有推導結果或 scientific PASS；無新 RNG／seed／producer／主機／量測。契約待 exact-head 複核，失敗或後續改版仍另追加 |

### X-SIGNAL-RESPONSE-P0.1 r2：模型前修訂（2026-10-12）

r1 保留在 PR #79 舊 head `373607d4d9f3314845f44b1356affa9ac6aaaa97`，未獲 GO。
Claude 發現「A 回讀依賴 A 準備」可以只靠 A 的本地記憶滿足，故不承擔回訊判別。
r2 要求 A→B 的 B 完整接收分布依賴合法 A 準備干預；固定 A 準備／記憶後，B→A
的 A 回讀依賴 B 回應，且事前合法無回應對照中該依賴消失。共同初態／事後挑選、
外部標籤直入 A、只靠 A 記憶均不充數；窗口型別與 B 自動／可選回應必須申報。
來源／閱讀申報見 EXP-0023–0024。這是未構造模型、未有輸出前的問題契約修訂；
model ID NONE，不是正式 gate／core／margin 變更、科學結果、attempt 或模型搜尋。

### X-SIGNAL-RESPONSE-P0.1 r3：請求串接（2026-10-13）

r2 保留在 PR #79 舊 head `7722b0fe5c226b1a35b8023edbc812d6965eda0e`，未獲 GO。
Claude 本輪指出兩段可由不相干的單向通道滿足（其提出的獨立信標例），不保證 B
回應 A。GPT 未實作或運算此例；在 model ID NONE 時追加回訊欄位來源分隔與串接：
固定 B 設定／自動規則，正常時 A 回訊欄位分布隨 A 合法準備不同，同一合法無回應
對照中相同。A 的準備記憶另記，不要求兩欄統計獨立；完整 law 仍須說明實際路徑。
兩段、對照與其他 r2 限制保留，無串接不構成回訊；來源 EXP-0025–0026。
沒有模型、law／材料／state／參數、診斷／RNG／seed／量測或正式 criterion 改動。

## 首份具名紙上 X-C 模型（2026-10-13；契約定案後）

PR #79 r3 原 head GO 後合併 `ac2226ee08a8babf71e326a7aabcd71388e24515`，tree
`312e3142add7460ddeab129bc8c090bf4b8f1f7e` 相同。此時問題契約已定案，才提出以下
紙上構造；舊 model ID NONE 列是各次模型前時點，原文保留。來源 EXP-0027–0028。

| X model ID | 問題／法則與來源 | 紙上結果／採用與限制 | 執行／formal 狀態 |
| :--- | :--- | :--- | :--- |
| X-SIGNAL-DELAY-RELAY-v0.1 | [X-C 延遲回訊研究](foundations/conditional_delay_relay_signal_study_v0_1.md)，依定案 P0.1 r3目標設計：外加同步tick、字母表⊥／0／1、雙向有向移位鏈、正延遲、B局部 XOR、靜默η=0、A回訊只讀返回末端。全部參數於law中事前聲明，無量測挑選 | 待複核歸納給出 B接收在m、回應發出在m+d、A返回在T=m+d+n；H≥T時兩段／同一對照／串接滿足，短窗口不延長。採作條件式有限符號law存在／自洽例，理想無串音等輸入未由物質實現，不稱物理裝置或L0湧現 | 新紙上模型已構造，未實作／執行／RNG／seed／producer／量測；沒有formal K、attempt、scientific PASS，條件結果待獨立複核 |
| X-SIGNAL-BEACON-CONTROL-v0.1 | 同研究的限定變體，只將B輸出改成外加clock在固定m時發b、不讀接收內容；源自Claude r2信標反例，此時才作具名law與解析 | H≥T時兩段與無回應對照成立，但固定b不依A準備，故無串接，不構成回訊；負結果保留，不能只列成功模型或改r3容納它。不推成所有自動回應器no-go | 只紙上定義／推導，無新計算／數據／formal verdict |


## PR #80 解析複核與下一問題登記（2026-10-13）

Claude 對 `f1017f88…`／`429da9a1…` 給 GO；CI #261 綠後原樣合併
`0f88bf2e46e0864bdffba865e81eeefce0cc428f`，tree相同。舊表的待複核是提交時點。
兩項解析現僅在 C1–C6／H≥T 限定已確認，物理模型／詮釋仍探索；短窗口、
未發送／靜默及信標否定均保留，沒有重跑模型或改 law／公式／r3。
reviewer 的確定性窮舉與作者接觸另見 EXP-0029–0030，不列新的 DEV 科學結果。

| Problem ID | 操作者選擇／權限 | 產物與來源 | 模型／執行／判決 |
| :--- | :--- | :--- | :--- |
| X-CAUSAL-TRANSPORT-C2-P0.1 | 本輪選 C2 因果傳輸；ACT-X-0001 僅紙上，生效 SHA `0c386716701589c9a6b0b799636a808aacb9ade5` | [只定問題契約](foundations/causal_transport_c2_problem_contract_v0_1.md)，由回訊研究外加 C2、公開 B2／B5、B3／B4、B4／B6 與 BHS 原文作用域啟發；先問所有有限無標記偏序上確定性非空有向同構等變統一有界出支持的存在性，物理傳輸橋接另列 | 本問題新 model ID NONE；沒有選擇法、K／law、具名反例、參數值、數值結果或新執行。契約待獨立複核；無 scientific PASS、seed／producer／主機／量測授權。若窄類否定，不擴張為所有訊號 no-go |

補明既有研究 C4 的可選 b／靜默 η 與無回應替換，README 改為現行 ACTIVE；
只是回應模式與狀態校正，不在此登記新的模型變體或放寬回訊判準。


## C2 P0.1 退回、小結論與 P0.2 登記（2026-10-13）

PR #81 r1 `02645cae…`／`6d4436e7…` 未 GO。Claude 在複核、任何新模型構造之前
提出 p 加 k+1 個互不可比未來的星形反例；自同構使非空支持必為全部，超過 k。
原四項聯立限定否定已由作者紙上覆核，舊題／量詞保留，不擴張成物理no-go。
上段原題待複核列是歷史，不能據它再開始那份存在性研究。沒有改模型或新運算。

| Problem ID | 操作者決策／來源 | 研究義務 | 模型／執行／判決 |
| :--- | :--- | :--- | :--- |
| X-CAUSAL-TRANSPORT-C2-P0.2 | 本輪明選方向1；Claude提出方向與星形反例，作者讀Johnston2008v2全文及1701.07212v5限定§2.1–2.2；EXP-0031–0032 | [只定問題契約](foundations/causal_transport_c2_problem_contract_v0_2.md)：固定3+1維m=0、外加Minkowski／Poisson校準、文獻link-path係數、完整測試類及平均／方差量詞；平均文獻基線不當新發現，單次漲落不能以平均代答 | 新model ID NONE；未構造新kernel／law、求解、撒點、RNG、數值診斷／seed／producer／主機／量測。原r3不變；契約待exact-head，沒有scientific PASS |

下一份只在契約定案後作紙上參照類／誤差與漲落研究。若權重或尺度要改，先保留
指定類的失敗／未決，另立問題，不在結果後擬合或放寬；正式資格與OPEN不變。


## P0.2定案後的具名文獻實例與M／V研究（2026-10-13）

#81 r2 head b0f53948／tree3e415ff4原核准內容經CI #264後合併
`c5bc9c6533f34c3121f793e68e3710cc9f67f6e5`，tree相同。契約定案後才作本項
紙上實例化與推導；舊待審／model ID NONE列保留為提交時點。

| 具名研究／參照 ID | 問題與選擇 | 本次解析／限制 | 執行與狀態 |
| :--- | :--- | :--- | :--- |
| X-C2-LINK-MV-v0.1；X-C2-JOHNSTON-LINK-v0.1 | [P0.2 M／V研究](foundations/c2_johnston_link_mv_study_v0_1.md)，固定m=0之文獻aχlink核，外加Minkowski／Poisson／D／x／L／φ，零擬合；來源EXP-0033–0034 | M是文獻覆核，給null座標、來源點與平均誤差界；V為主要義務，用共享Π的精確covariance、不同方向重疊上界與全部近方向／vertex／tails分割，提出Var→0及粗上界、機率量詞。不是field-first、sampled detectors、器件回訊、Dirac或L0湧現 | 已有具名紙上參照實例，不是formal候選。全部新解析待exact-head，未執行／撒點／RNG／數值／symbolic診斷／producer／seed／主機／量測；沒有新DEV科學結果、attempt或scientific PASS |

M／V提出的證明若有缺口，保留此版本與未決／否定，不依結果改核、φ或criterion。
相關DHS2010source-detector漲落文獻只作作用域對照，不搬用其讀值／近似／參數。
原P0.1／P0.2契約、#80兩模型／r3、formal／burn／凍結來源均不改。


## PR #82 限定M／V確認與P0.3問題登記（2026-10-14）

Claude對1e067c63／3b53b07a逐式手算GO；CI #266綠後原核准tree合併
`f43762f2917a3b2ce86782d1b4de033b2075da3f`，tree相同。舊待審列保留為歷史。
M／V及機率收斂僅在固定來源、augmented-endpoint Lebesgue泛函限定已確認；
不是原生點探測器或物理實現。原核、P0.2及證明§2–7不改，沒有重跑或新科學結果。

| Problem ID | 選題／來源 | 構造前規格 | 模型／執行／狀態 |
| :--- | :--- | :--- | :--- |
| X-CAUSAL-TRANSPORT-C2-P0.3 | 操作者轉交Claude建議，承接#82的讀值作用域限制；EXP-0035–0036 | [只定問題契約](foundations/causal_transport_c2_problem_contract_v0_3.md)：外加3+1維m=0固定來源／D／L／φ；同一Π兼接收及阻擋，以aρ／ρ原生點求和，固定完整測試類、M_D／V_D與機率量詞；需另證端點、自相關及相關矩 | 待契約exact-head，未開始推導或新模型law；新model ID NONE，既有實例保留。無撒點／RNG／新數值／符號診斷、producer／seed／主機／量測、DEV科學結果、正式attempt或scientific PASS |

若後續研究發現失敗／缺口，保留本題與否定／未決，不結果後改讀值或收斂目標。
既有regression／integrity只作repo驗證；原formal／禁止資料／UNKNOWN／r3／凍結來源不改。


## P0.3定案後的原生點讀值M_D／V_D（2026-10-14）

#83核准head7271b215／treeaa53f2b1經CI #268綠後原樣合併
`8a8524cdfdd34934d629547449c92d0668a34cc6`，tree相同。
P0.3此時定案，前列待審／model ID NONE為提交時點；契約全文不改。

| 具名研究／讀值／核ID | 來源與固定規格 | 本次解析／限制 | 執行與狀態 |
| :--- | :--- | :--- | :--- |
| X-C2-NATIVE-MV-v0.1；X-C2-NATIVE-READOUT-v0.1；X-C2-JOHNSTON-LINK-v0.1 | [原生點M_D／V_D研究](foundations/c2_native_detector_mv_study_v0_1.md)，P0.3固定同一Π兼接收／阻擋、aρ／ρ與完整φ類；Claude良設性草算列為來源EXP-0037，作者推導EXP-0038 | 單點Mecke期望精確接回已證M；有序不同點Mecke插回端點，得Var S=Var F+D−J，區分自相關與有符號阻擋。兩項絕對界≤K₁/√κ，傳遞舊V／固定輸入機率量詞；有限域Mecke附短證。校準延伸，不稱新物理機制、器件或L0／c | 具名紙上讀值實例，沒有新kernel／law或正式K；全部新解析待exact-head，未作撒點／新RNG／數值／符號診斷、producer／seed／主機／量測；沒有新的DEV科學執行、attempt或scientific PASS |

原P0.1／P0.2／P0.3、已核准M／V、r3／兩舊模型與formal／凍結來源保留。
研究若有缺口，保留head與否定／未決，不結果後改讀值、窗口或criterion。
既有regression／integrity及檔案比對只作repo驗證，不代替新解析的獨立複核。


## PR #84 限定解析確認（2026-10-14）

Claude對head577ea0e3／tree1ddfc5fd逐式手算GO，另對照#82的e_M、e_V與常數。
CI #270綠後原樣合併main `8839df0eb8bff88dd6e040b8c81ee60117932445`，tree相同；
556 passed／5既有warnings、integrity通過。前列待審是提交時點，原文保留。

`X-C2-NATIVE-MV-v0.1` 現限定已確認定案原生點校準求和的M_D／V_D與機率收斂；
模型／讀值物理詮釋仍探索，非器件／回訊或L0／c湧現，沒有scientific PASS。
§2–7、附錄A、所有公式、原P0.2／P0.3、基線M／V／r3與formal／凍結來源全不改。
只有本人申報EXP-0039與作者文件scope EXP-0040，沒有新的DEV科學結果、attempt、
新推導／選題、模型／權重、數值／symbolic／RNG／撒點或producer／seed／主機／量測。
既有regression／integrity與檔案比對只作repo驗證；全部未證物理／formal義務保留。


## r3回訊與C2串接的問題登記（2026-10-16）

承接main f1a33070及申報鏈4cd99590→34bfd9a0。操作者明選方向1，
時間先後與本地版本批准者依接觸帳§21只追加，不改寫原「未選定」歷史句。

| Problem ID | 待審規格 | 新結果／限制 |
| :--- | :--- | :--- |
| X-C2-R3-BRIDGE-P0.1 | [問題契約](foundations/c2_r3_response_bridge_problem_contract_v0_1.md)：共同Π、原生B接收／再發射、線性幅度回應與同一零輸出替換；準備／接收／回應／回訊欄位分開，雙段泛函／連續參照、M與絕對V及r3串接量詞事前固定 | 只有定義／外加介面，沒有矩／收斂或實現證明；不直接沿用單段P0.3方差。新完整裝置model ID NONE，舊ID保留。EXP-0045本人全文待補，EXP-0046作者scope；draft不得稱可合併 |

沒有新的DEV科學結果、正式attempt、seed／主機／量測／receipt或producer執行。
既有regression／integrity只作repo驗證；原P0.2／P0.3／r3、全部證明、formal與凍結檔不改。


## PR #86申報原句補齊（2026-10-16）

EXP-0045已按操作者台北15:19:00／UTC07:19:00轉交的Claude原句，逐字追加於接觸帳§22。
上列「待補」是收件前的歷史，未改寫；EXP-0047只記作者收件／同步scope。
本次只更新申報與現行狀態，不更動X-C2-R3-BRIDGE-P0.1的§2–6規格／公式／判準，
也不新增推導／模型／DEV科學結果。PR #86仍需新exact-head獨立複核，沒有合併GO。


## PR #86 r1退回與r2問題修訂（2026-10-16）

Claude對r1 head9dd6710e／tree4660f45e未GO：線性介面的四項law比較按構造成立，
不得當成回訊證據。操作者明選方案b，契約r2另登記固定單次判定a>gC/2、
等號判0、兩準備最壞誤判趨零與固定輸入量詞；配對可識別性、穩定性／failure仍OPEN。
報時間條款直接對應r3 §3，本題不報時間／延遲，不以同點介面消除未知延遲。
舊head、原M／V及所有舊帳保留；EXP-0048逐字本人申報、0049作者修訂scope只追加。
只有問題修訂，沒有矩／收斂／P／D推導、新DEV科學結果或模型實現；r2待exact-head。


## PR #86定案與共享配置M／V／P／D紙上稿（2026-10-18）

#86 r2核准b4e3deb1／435fc3e8，CI #276後原樣merge 7bc202b5，tree相同；契約blob79c34b88不動。

| Study／Readout ID | 規格與紙上進展 | 未解與執行狀態 |
| :--- | :--- | :--- |
| X-C2-R3-SHARED-MVPD-v0.1／X-C2-R3-RELAY-READOUT-v0.1 | [具名研究](foundations/c2_r3_shared_mvpd_study_v0_1.md)：補連續目標平滑性／良定性；一致單段bias給M；高階矩與共享Π的加權L²比較給保守V界，再分別給P及固定單次D | 新解析全部待exact-head；四項構造law不作成果，物質／配對識別／穩定性OPEN，不報時間／延遲／距離。EXP-0050逐字本人申報，0051作者來源及合併前策略推理的時間偏差待審 |

沒有新核／回應／權重／窗口、DEV科學執行或正式attempt。原文件／凍結來源保留，
既有regression／integrity只作repo驗證；無數值／符號程式、RNG／撒點、producer／seed／主機／量測。


本交付首輪本地regression為1 failed／555 passed／5warnings（113.44秒）；
既有test_worker_kernel_parent_death_guard在確認/proc狀態檔存在後讀取時遇到ProcessLookupError。
檢視既有測試第216–218行：exists與read分開，程序可在兩者之間消失。
單項原樣重跑1 passed（0.09秒）；未修改程式／測試。全庫重跑另記，首輪失敗不隱去。

全庫原樣重跑結果：556 passed／5既有warnings（109.01秒）；integrity與diff格式檢查通過。
首輪失敗及單項重跑結果均保留，沒有改動程式／測試來取得通過。


## PR #87原樣合併、限定升格與來源釐清（2026-10-19）

Claude對exact head924c90c1／treee7d4c476給GO；CI #278成功，
556 passed／5既有warnings與integrity通過，原樣squash為main
`6cd3eb4386582eb80e528b631673b6b8aebca647`，tree相同。
Git committer UTC06:00:56／台北14:00:56；GO轉交時間為台北14:00:20／UTC06:00:20。

限定確認X-C2-R3-SHARED-MVPD-v0.1的定案共享配置雙段讀值（外加線性介面）
M、絕對V、P與單次判定D；只改研究審核狀態並追加§9，§2–8全部證明不變。
保守非最優O(κ⁻¹ᐟ⁸⁰)、四項law比較的構造性、原量詞及所有物理／formal OPEN保留。
物理詮釋仍探索；r3 §4.3配對可識別性、§4.4穩定性與器件實現仍OPEN。

EXP-0054逐字保存本人申報，0055記作者來源與文件同步；公開推送是操作者批准，
Claude預讀只是建議。2247edb4／7adb918b僅本地、未公開，
外部不能由Git直接驗證其與公開tree的差異；reviewer比對的是上傳檔與公開版本。
EXP-0051流程時間偏差及首輪/proc競態／重跑紀錄保留；Claude正式裁定時間偏差不阻擋，
理由是r2判準及merge blob固定，不把文件建立時間當作最早推理時間。

本次只同步狀態與追加三本帳；不改契約／舊研究／凍結來源、程式／JSON／tests／CI。
沒有新推導、研究選題、DEV科學執行、attempt、RNG／撒點、producer、
raw／sealed、seed／主機／量測／receipt或scientific PASS。


## PR #88定案與T2＋T3問題契約（2026-10-19）

#88 head bde2ca03／tree06bae466獲Claude GO，CI #280成功後原樣合併main
`b80ef2fd566ffabb43b5a77581087ef37938ebc7`，tree相同；
Git committer UTC06:47:32／台北14:47:32。這次不重寫已確認研究或凍結契約。

操作者在台北14:44／UTC06:44（只知分鐘）選定路線圖T2＋T3，採Claude建議，
C2線暫停新增研究；來源／先後與EXP-0056–0059見接觸帳§27。
[問題契約v0.1](foundations/t2_t3_problem_contract_v0_1.md)有兩個獨立ID／六欄：
T3只固定四列能力矩陣、局部性／等變／維度及表示型別；
T2只固定history／measure／weight型別與類總振幅比，純phase速率留作待證問題。
本問題新model ID NONE；沒有K、作用量、算子、場方程、反例構造或新證明。

作者讀五份外部原文的指定段落作來源定位，沒有把其公式採為候選或重做抑制計算；
能力矩陣各格OPEN，沒有從文獻摘要冒稱費米子選幾何或所有fiber no-go。
上一則方向建議申報缺原句，保留0057 PENDING-VERBATIM，0058是另一份實際收到的申報；
不讓記憶檢索的摘要代替本人原句，不以本輪契約為研究已開始。
無新數值／符號診斷、RNG／撒點、producer／raw／sealed、seed／主機／量測／receipt。
既有regression／integrity與Git／文字比對只驗證repo；全部formal及物理OPEN保留。

本交付首輪全庫回歸為1 failed／555 passed／5既有warnings（116.78秒）。
失敗在既有test_worker_kernel_parent_death_guard的/proc exists→read間，
程序被回收時觸發ProcessLookupError，位置仍為tests第218行。
保留首輪失敗與trace，不改程式／測試；既有單項及全庫原樣重跑結果後補，
不把這個repo驗證失敗改寫成研究結果或跳過失敗項。

既有parent-death單項原樣重跑：1 passed（0.09秒）。首次全庫失敗不隱去。

全庫原樣重跑：556 passed／5既有warnings（115.36秒），integrity與diff格式檢查通過。
沒有改動程式／測試、未跳過失敗項；首輪1 failed紀錄與單項重跑結果並存。


## PR #89 r2定案與T2／T3具名紙上審計（2026-10-19）

#89 r2 head0f56e951／tree3ec33536獲GO，補取CI #283 run39222282955與
job117960164574的exact-head成功證據後原樣合併main
`cae0f69e24e3ca0bcf4820deaa284efec5749819`，tree相同，UTC12:48:54／台北20:48:54。
第一次merge自動審查因缺CI證據未批准，補證據後才通過，未繞過。
EXP-0057補齊且獲增量GO；核對三個開始條件完成後才作本輪新策略／推導。

新增兩份獨立紙上稿，狀態均探索待exact-head：

- X-T2-CLASS-SUM-AUDIT-v0.1：共同measure與orbit換算、純phase比值的必要且充分條件、分母上下界方向、leading熵邊界及同重力baseline改善；不選具體class／F／作用量。
- X-T3-SECTOR-CAPABILITY-AUDIT-v0.1：orbit／代表與two-order作用域、S₃障礙、fiber型別、中心／Clifford維數與尺度分帳；不構造K或物質law。

新原文讀取BHS、KR原文的作者上傳轉錄、Noldus指定片段，限制詳兩稿與EXP-0063。
0062逐字保留本輪Claude增量申報；三本帳只追加，定案契約及其他凍結來源不動。
README／STATUS同步當前待審狀態，不提前升格任何新結果，C2與formal限制不變。
驗證結果將在本節後追加；不使用測試作科學量測或新研究診斷。

本輪repo驗證：既有全庫 `pytest tests/ -q` 首輪即 **556 passed、5 warnings，247.40秒**；
未發生上一輪的/proc競態，也未修改程式／測試。`verify_integrity.py`、`git diff --check`、
三帳byte-prefix、EXP-0062逐字、固定契約／凍結協定blob及七份Markdown範圍檢查皆通過。
兩份新研究稿的本地連結存在；其他定案契約與既有證明diff為零。
這些是repo回歸／保全結果，不是新科學執行或解析證明已獨立確認。


## PR #90原樣合併與T2／T3限定升格（2026-10-19）

#90 exact head81f1a260／treebc579c93獲GO；直接核對CI #285 run39257616818的head／success、
job118076754933與全部steps success後，轉ready並原樣squash為main
`a5f584a679911f13eb3e4a1909407856e203d39d`，tree相同；UTC15:42:54／台北23:42:54。
本輪只做七份Markdown的狀態／來源同步：兩稿首段／§1審核句與證據格、檔尾限定複核紀錄，
README／STATUS與三本帳；T2 §2–6、T3 §2–7的推導／矩陣全文不改。
T2確認measure換算與條件式相消／改善，一般F充分界不變成任意F的iff；
T3各格判定限定於各自路徑，不能合併成全面spinor no-go，物理詮釋仍探索。
STATUS明記契約§4.5原問的必要／充分方向已由研究§4.2釐清，契約原blob434e85fc保留。
EXP-0064逐字追加，0065作者只合併／紀錄scope，原作者原文責任不改。
未另選題、未重讀原文、未新增推導／構造／科學執行，C2與formal／隔離限制保留。
本增量交新的exact-head複核，不把#90 GO當作本PR已批准；驗證結果於下方追加。

本輪repo驗證：全庫既有回歸首輪 **556 passed、5 warnings，116.72秒**；integrity通過。
Git diff格式、三帳byte-prefix、EXP-0064逐字、契約／凍結協定blob、兩稿原證明／矩陣
逐位元保全、七份Markdown範圍及研究稿本地連結檢查皆通過。沒有改程式／測試／JSON／CI，
也沒有重跑任何新科學或數值／符號診斷。


## T6問題契約：量子一致性必要條件（2026-10-20；不推導）

操作者台北11:00／UTC03:00選T6，採Claude首選建議；從紀錄分支8fa27315接續，
parent main a288dc64／treeac9600e8，保留0066／0067。
只新增一份問題契約、六欄／輸入帳／QO1–9全OPEN及QN1–4待證問題，不預填答案，model ID NONE。
限1+1 massless two-sector比較；不提出K、state、pairing或具體物理test space構造，
不選／改正式C9／C10 criterion、projector或evaluator，不變更任何formal來源。
新讀Araki、Johnston、Sorkin、Afshordi–Aslanbeigi–Sorkin、Potting、Noldus的指定原文段落，
僅定位CAR／CCR／adjoint／dimension作用域，閱讀程度詳契約§6與EXP-0070，沒有新證明。
0068上一則本人申報未取回，保留待補；0069題目說明本人原句及0070作者scope只追加，
缺項解除／契約GO／原樣合併前不開始研究。C2、T2／T3及全部formal／隔離限制不變。
README／STATUS同步本契約待審；三帳只追加，舊契約／證明／程式／JSON／tests／CI不改。
驗證結果於下方追加，既有回歸僅作repo驗證，不作T6新科學證據。

本輪repo驗證：全庫既有回歸首輪 **556 passed、5 warnings，107.02秒**；integrity及diff格式通過。
三帳相對8fa27315的byte-prefix、EXP-0069逐字、0066／0067保留、acceptance／C9／prereg、
T2／T3契約與兩稿及凍結協定逐位元不變、六份Markdown範圍與新契約連結皆通過。
未改程式／JSON／tests／CI，也沒有用回歸測試來推導T6答案或形成科學判決。


## PR #92 r1未GO與r2依據管道修訂（2026-10-20；不推導）

r1 head aeca9033／tree530a7d9f保留；Claude要求點名§5.2.1(v)／D.1第8項管道及補0068。
同一r2 commit：契約§2.1明訂T6合併／寫入STATUS不自動取得依據資格，handoff／曝光／
合資格審查前不能完成A聲明；原文閱讀不是B mapping，不提升文獻資格；STATUS／README同步。
契約§1記r1身分／退回與其後0068收件，原保留0068與0071本人原句逐字追加，0072作者scope；
三帳只追加，不刪§32舊待補行。QN／QO與原文定位原樣，reviewer非約束草算只記曝光，不轉用。
未新讀文獻／檢索、未新增證明／構造／科學執行；acceptance／formal、舊契約／兩稿、
程式／JSON／tests／CI不改。r2仍待增量GO與原樣合併，不開始T6研究。
驗證結果於下方追加。

本輪repo驗證：全庫既有回歸首輪 **556 passed、5 warnings，120.92秒**；integrity與diff格式通過。
三帳相對r1的byte-prefix、0068／0071原句逐字、T6 §3–7（含QN／QO）全文、formal／
acceptance／prereg、T2／T3及凍結來源逐位元保全、六份Markdown範圍皆通過。
沒有改程式／測試以取得通過，也沒有把回歸當作T6必要條件證明或科學判決。


## T6契約原樣合併與具名義務審計（UTC2026-10-20／台北2026-10-21）

#92 r2 exact head ada4b412／tree12634a4a在Claude增量GO與CI #290 run39444635314、
job118703171118全步success後原樣合併main865d74a3，tree一致；UTC17:14:49／台北次日01:14:49。
契約blob ce332f5f與三項開始條件核對後才開始本輪策略／推導，無本輪提前推導偏差。
新稿X-T6-QUANTUM-OBLIGATION-AUDIT-v0.1完成條件式正CAR form／互補、null quotient與Riesz、
charged／self-dual分型、positive-part轉用障礙、已給dynamics相容與逐對form極限證明，並分列QO來源。
這是已知代數校準，沒有選具體K／state／物理pairing／test space，不給S5C量子判決。
實際Green到總form、state／pairing／time與continuum來源仍OPEN，全部新稿待exact-head複核。
0073本人原句逐字追加；0074披露已知reviewer提示、Araki／Noldus／Sorkin重讀範圍與未讀界線。
三帳只追加，README／STATUS僅同步現況；契約、acceptance／formal、前份研究、程式／JSON／tests／CI皆不改。
探索軌，不具 §5.2.1(v) 依據資格；A聲明與B mapping管道隔離原樣，不以STATUS更新繞過。
沒有新數值／符號診斷、RNG、撒點、producer、raw／sealed、seed、主機、量測／receipt或科學執行。
驗證結果於下方追加。

本輪repo驗證：全庫既有回歸首輪 **556 passed、5 warnings，120.58秒**；integrity與diff格式通過。
六份Markdown範圍、三帳對main865d74a3的byte-prefix、EXP-0073原句逐字、定案契約ce332f5f與
所有formal／前份來源逐位元保全、新稿本地連結及章節／式號檢查通過。
章節檢查腳本初次用substring誤計三級標題，改用行首二級標題匹配後通過；文件未因該檢查改寫。
沒有首輪測試失敗、沒有改程式／tests／CI；回歸結果不作T6量子一致性證據。


## PR #93限定解析複核與合併封存（2026-10-21；只追加）

【已確認／限定解析：任意已給 CAR 資料下的條件式必要界（A=Q+R、0≤Q≤A、Riesz 表示、charged／self-dual 必要式、正部分障礙、form 保留與逐對極限）】

PR #93 exact head `9c26d4729462ae03688b24341b019c05e443a54a`／tree
`1a85110bc0e3d44a64efa2a9f6df24deff5c0208`取得操作者轉交的Claude GO；
CI #292（run39466497029）success後轉ready並原樣squash合併main
`630d4628b7e8603a08d2167a92122b3073dc9759`，merge tree與核准tree完全相同。
Git committer時間為2026-10-21 12:10:52 Asia/Taipei（UTC04:10:52）。
限定確認已知CAR代數必要條件與抽象轉用；物理詮釋、同一K的Green到總CAR form、
state／pairing／time來源與量子continuum對接仍OPEN。沒有新的量子實現或新穎性結論。
探索軌，不具 §5.2.1(v) 依據資格；D.1第8項A／B、E0、全部formal、
item7不可ADOPT、item8 OPEN、6a-E／Freeze-1a及UNKNOWN／禁止資料隔離不變。
本輪只封存複核與同步狀態；下一研究方向尚未選定，不開始構造或文獻盤點。

EXP-0075逐字收錄reviewer本人申報；EXP-0076記本輪作者接續範圍。


## KQ r3量詞／非平凡性／反修補與canonical整合（2026-10-22；只追加）

#94經CI #294與exact-head GO後原樣合併main7f782bb6，treee6eb52f6與核准一致；
Git committer UTC2026-10-21 20:07:11／台北2026-10-22 04:07:11。
#95 r2 aa43fb2c／8fa9ccff需修訂；r3修X-KQ-1P1-P0.1的全D1自然性／逐P量詞、
跨N規則、局部order predicate要求與四項探索非平凡性、form不得依正負譜修補及同源state規則。
D1含單點，不能以豁免退化輸入維持全域成功；局部結果先列order predicate，不另選工作域。
探索定義不作formal criterion，A／B及§5.2.1(v)隔離原樣。
接觸帳§36已逐字整合EXP-0077–0079及Claude本人原句0080，0081記作者r3範圍；
兩份補充檔既有內容保留原樣；權威登記以canonical本節為準。本r3尚待增量exact-head複核與原樣合併，
model ID NONE，沒有K／state／pairing選擇或推導、數值／符號診斷或科學執行。
定案T6契約／研究、acceptance／所有formal、程式／tests／CI不改；E0、item7／8、
6a-E／Freeze-1a、UNKNOWN與禁止資料隔離不變。


## KQ r4工作域與canonical補漏整合（2026-10-22；只追加）

#95 r3 5d060cb1／d71d6bc1仍未GO，CI #297 success；本r4依reviewer最小條件事前固定
D_KQ={P∈D1:至少兩個strict comparable pairs}，補全序鏈的非空／無界性證明。
§4.1只同步工作域量詞，四項探索最低要求及反補洞規則不改；全D1退化不可能性
記為已知作用域事實，不作研究成果。沒有K／state／pairing／ansatz／策略或科學執行。
本版本把#96已核對追加內容及漏掉的§36開頭授權原句整合進canonical接觸帳，
0077–0081保留，0082逐字收錄Claude本輪申報，0083記GPT r4範圍；補充檔／研究稿原樣。
#96只作核對紀錄，patch檔不合併。完整blob發布仍待操作者明確授權；本地整合不算
main登記或開始構造。待#95 r4的GO、必要CI、原樣main合併與tree核對後才可依契約進行。
formal／E0、§5.2.1(v)及A／B隔離、6a-E／Freeze-1a與UNKNOWN／禁止資料限制不變。


## PR #95 r4 GO收件與構造前本人申報（2026-10-22；只追加）

操作者轉交#95 r4 exact-head9517c4b3／tree16bb788a的GO，CI #298
run39713083804 success。接觸帳§38逐字追加Claude本人申報EXP-0084，
EXP-0085記GPT本輪核對／轉ready被自動核准審查拒絕與本地紀錄範圍。
受審r4已有0077–0083，main7f782bb6仍止於0076；本地追加不算main已登記。
#95保持draft，未合併，沒有merge tree可核對；待操作者明確解除原draft／不合併限制。
本commit只有三帳追加，保留完整byte-prefix，不改契約、STATUS／README、研究稿、
補充、formal、程式、測試或CI。未選K／state／pairing，未開始構造或證明策略，
無新科學執行；既有integrity與文字／Git核對僅作repo檢查。後續須先核對#95原樣合併tree，
再銜接本紀錄，不能倒填研究開始時間。探索軌／§5.2.1(v)、E0、A／B及既有資料隔離不變。


## PR #97 r2：其後授權／#95合併與構造前申報追溯（2026-10-23；只追加）

**其後事實：授權、原樣合併與紀錄位置。**

操作者明確授權原句（節錄）：

> **授權（操作者）**：我解除先前對 #95 設下的「保持 draft、不合併」限制，並授權以下動作：

授權日期依本對話當時的Asia/Taipei日期為2026-10-22；原訊息未提供時分秒，
故只記日期，不以工具執行或Git committer時間倒填授權時間。授權發生在下述合併之前。
授權範圍僅三個動作：①核對#95完整head、tree及該head的CI #298成功；
②轉ready，以expected head9517c4b3原樣squash至main；③核對merge tree並回報main SHA。
原授權亦明列head變動即停止，EXP-0084紀錄不在該次合併授權內、須另行推送與複核，
且0084完成canonical登記並經複核前不得開始構造。此處不擴張該授權。

GitHub紀錄確認CI #298（run39713083804）在完整head
`9517c4b35d8593335ce80c7b699a2f2573c77954`上completed／success。
#95依此expected head轉ready後原樣squash合併為main
`3387d73241876edd8ed79e26cf6149bbf118cd0d`，唯一parent
`7f782bb64ad30abd42032b3a82e476fd409607a6`；merge tree
`16bb788a45924e3b257a845a18eaeabc7179ac53`與核准r4 tree完全一致。
Git committer為GitHub，時間2026-10-22T12:31:30Z，
即2026-10-22 20:31:30 Asia/Taipei；這是合併時間，不是授權或研究開始時間。
契約X-KQ-1P1-P0.1及EXP-0077–0083由此進入main。

原紀錄6f62c417的寫作基線是合併前r4，保留該內容後重接到上述合併後main，
本地重接head07c5bb36；操作者另以「同意授權」同意將三帳既有公開原文＋
限定追加以完整Git blob推到新分支並建立draft PR，不合併、不開始構造。
API發布的#97 r1 head為`3a98ee3890eb609c20b4f2fc21f6a5cafec12516`，
tree `ce381af343c17f8fc033de28f10428c28d4a90b3`，唯一parent就是main3387d732；
其tree與原紀錄相同，main→r1 patch SHA-256為
`c7c34267695153e4c6280ca44936c7fbfc2b0a90b3bb5be60697b90356f65de2`。
因此上文「#95保持draft／未合併」「main7f782bb6仍止於0076」及
「不能聲稱構造開始條件已滿足」只記原紀錄寫作當時的狀態，不代表此後現況。
本r2追加這條時序鏈，不修改、覆蓋或倒填那些原句，也不改寫任何上游commit。

目前#95合併與tree核對已完成；#97 r1的CI #300（run39803777138）success，
但reviewer要求本r2補充後再作增量複核，故#97及0084尚未完成GO／原樣合併／tree核對。
在#97最終exact-head GO、必要CI、原樣合併並核對tree之前，
不宣稱構造開始條件全部完成，也不開始任何K／Green／state／pairing選擇、證明策略或構造推導。

接觸帳§39逐字追加EXP-0086（Claude #95合併後核對）與0087（Claude #97 r1複核），
EXP-0088記作者本輪來源／發布及只追加範圍。0084原句與三帳既有文字完整保留，
其他檔案不改；探索軌不具§5.2.1(v)依據資格，E0、A／B及全部既有資料隔離不變。


## #97合併後接續：首份KQ交付的先行紀錄（2026-10-23；只追加）

#97 exact-head451044ed經GO、CI #301及操作者同意授權，原樣squash main1ac30ceb，
tree3350d8bd與核准相同，parent3387d732；Git時間UTC02:27:57／台北10:27:57。
#94／#95／#97追溯及0077–0088 canonical整合已完成。
採用「只涉紀錄PR的reviewer申報隨下一份交付追加，不再形成遞迴開始門檻」的程序規則；
不放寬科學接觸、來源、契約、UNKNOWN或新增physical primitive的停止條件。
本分支第一commit在接觸帳§40逐字登記EXP-0089／0090，0091披露作者接續與少量內部
紙上預想；不宣稱盲預註冊。後續先版本化固定試作規則再寫完整證明，所有失敗保留。
三帳只追加，主契約與其固定工作域／四項非平凡性／反補洞條款及formal不改。
探索軌不具§5.2.1(v)依據資格；E0、A／B、6a-E／Freeze-1a及原資料隔離不變。


## X-KQ-OP-01首次紙上試作：失敗保留、待逐式複核（2026-10-23；只追加）

首次交付第一commit逐字收EXP-0089／0090，0091披露開始來源與內部預想；
其後獨立commit固定OP-01規則，再交完整研究稿；0092申報實際新讀文字／模型選擇與失敗。
工作域D_KQ、契約§4.1／4.2與停止條款不改。試作K=I+Z⊗I+Z²⊗J有同源retarded inverse，
(a)傳播、(c)無統一Hasse-hop cutoff成立，但(b)在三葉star失敗；固定ordinary-adjoint
CAR prescription有負方向，不能有正state，(d)前提不成立。主問題未完成，結果待複核。
G_swap限定障礙只及honest global二維fiber保留natural swap的明文類，不擴成所有K／spinor不可能。
規則§7只追加L0/L1分類更正，不改既有數學規則。失敗不補洞，不縮工作域，不另給新primitive。
三帳只追加、目前狀態同步；已定案契約、T3／T6、acceptance／formal、程式與科學資料皆不改。
無模型／symbolic／toy執行、RNG或producer；所有推理在紙上。探索軌不具§5.2.1(v)依據資格，
E0、A／B及全部既有資料隔離不變。本分支保持draft、不合併。


## PR #98 r2：公開版本證據與發布追溯補充（2026-10-24；只追加）

**本地checkpoint與公開commit的對照、可查核範圍。**

| 本地checkpoint（作者保留） | 所報tree | 公開可抓取commit | 公開tree |
| :--- | :--- | :--- | :--- |
| eeb5ea6d1e46cb227890a5aa1ff6dd43fe01c3db | 6a4858d0851d8065817b12a924034c0eae64acd4 | a01c4ea6103306335e4c48c5f36972276c09352b | 6a4858d0851d8065817b12a924034c0eae64acd4 |
| 1bd15a5ef57d1f60906cf9b0d619f9980f92770f | eb594400860abcf1399432a006126b6db7ae97cb | e30d9bd9eb970295786748463b5573b72cb3a7c1 | eb594400860abcf1399432a006126b6db7ae97cb |
| ac83c4e666a26dcc1df99523001c2a97c0eee4bd | 0f7e1e4e6c72d51fff34d5b5926904ba3430a3e8 | 8176f9848ba892119f757c2b2d6414c1d7871d46 | 0f7e1e4e6c72d51fff34d5b5926904ba3430a3e8 |

這是API發布後的內容對照，不是同一個commit物件。作者本地可見上述checkpoint；
reviewer向公開repo抓取eeb5ea6d與1bd15a5e失敗（not our ref），因此這兩個本地SHA
**不能作公開可查核的承重證據**。表中本地身分／對應是作者披露，不能代替取得那些物件的獨立查核。

公開可查的鏈是main1ac30ceb → a01c4ea6 → e30d9bd9 → 8176f984：
a01只追加紀錄，e30包含固定規格§1–6，8176才包含研究稿，且在規格末尾只追加§7。
公開Git證據只證明這個commit層面的先後順序與各版內容，不獨立證明作者私下何時思考、
看到或預期科學輸出，更不能證明「看任何輸出之前」的盲固定。原文的規格先固定說法
只按此公開版本化順序理解；超出它的本地時序／內部思考僅為作者申報。
EXP-0091已披露固定規格前的零對角／對稱性風險預想，本追加不提高其證據等級或盲性資格。
不以API commit時間倒填研究開始或內部規則選定時間；本地SHA、原句與數學全文均保留。

**EXP-0092發布補記的其後事實（不改原句）。**

操作者推送授權原句（節錄）：「同意授權」。授權日期為2026-10-23 Asia/Taipei；
原訊息未提供時分秒，不用API或Git時間補填。該答覆針對已核對patch
`e50617c29594b5dd0d631cbef37081effae522d5fb143e43a3c6345aa846086e`的七個檔案，
允許把既有公開原文＋限定增量以完整Git blob回傳dr17414/lightspeed-fundamental-theory，
包括規則檔已寫成的K／pairing／CAR prescription／G_swap與研究稿推導及失敗證明，
連同其餘五份紀錄／狀態檔，只建draft PR，不合併、不新增構造。
這裡範圍是授權上下文的轉述，不把助手所擬條文冒充操作者的逐字原句。

其後發布完成：分支 `docs/kq-op01-first-paper`，draft PR
https://github.com/dr17414/lightspeed-fundamental-theory/pull/98 。
三個公開commit及tree逐一如上表，parent鏈由main1ac30ceb起，沒有改寫上游歷史。
r1 head8176f984／tree0f7e1e4e；main→r1的完整patch SHA-256為
`e50617c29594b5dd0d631cbef37081effae522d5fb143e43a3c6345aa846086e`，
遠端重新fetch後的patch與當時核准本地版逐位元組一致。CI #303（run39979065472）
在該head上success；這是repo回歸，不是新科學執行。
上文「尚未建立遠端commit／分支／PR」只記首次阻擋當時，並非其後的r1發布現況。
#98仍未GO／合併；main仍1ac30ceb，本r2只是追加追溯紀錄，不新增構造或更改已核數學。

ACT blob `65496ad5ec59acaf57adaf18276b1fcc0fef4085`最初僅被建立、未掛接時，
該次create-blob動作沒有改動任何tree、commit或ref；不影響當時main。
其後依核准內容發布時，a01c4ea6與e30d9bd9的ACT路徑合法引用同一blob，
所以不能把「當時未掛接」擴成「此blob永遠未在tree出現」。r1最終8176f984的ACT blob
是 `c98d5904728816433f51226d03e71e565b35c6d9`；main1ac30ceb的ACT blob仍是
`ff7ca60320ddae34c0d2e524cdcd6a676d3b6b1d`。單獨blob建立與後續明確tree引用分帳，
沒有隱藏或未核准的tree變更；既有七檔範圍及patch hash不因此改變。

接觸帳§42逐字登記Claude本輪EXP-0093，0094為作者僅追加的追溯範圍。
本r2只追加規格／研究稿§8及三帳，所有r1原文作完整byte-prefix；數學與其餘檔案不改。
#98未GO／未合併，不開始新構造或conditional契約；探索軌不具§5.2.1(v)依據資格，
formal／E0、A／B及全部既有資料隔離不變。


## #98原樣合併與conditional問題起草（2026-10-25；只追加）

操作者「同意授權」後，#98 head ae8d0d3b經GO及CI #304 success，expected-head原樣squash
為main be55a80a8bbc80f1d5d371ada9c081f78789e094，tree6b9cf7d3與核准相同，parent1ac30ceb。
Git committer UTC2026-10-24 17:09:47／台北2026-10-25 01:09:47；不是授權或研究開始時間。
OP-01封存失敗及限定障礙，原始輸入主問題仍OPEN；停止該題新增試作，另立conditional契約。
接觸帳§43逐字登EXP-0095，0096記操作者／Claude方向、兩篇原文的有限實讀與起草範圍。
新題擬固定外加preferred時間序L與跨尺寸固定二維Hermitian參考資料，底層不縮D_KQ，
對所有合規L量化；不以primitive補正譜，不假裝兩側障礙已解除。只定問題、無新model／K／state。
conditional構造須待新契約GO、必要CI、原樣合併與tree核對；formal／E0及全部資料隔離不變。
本稿不具§5.2.1(v)依據資格，不提高OP-01或文獻承重資格；無新科學執行。


## PR #99 r2：限定時間序讀取與同源CAR條件（2026-10-26；只追加）

r1公開鏈main be55a80a → 1fa6ce70（紀錄）→ 40e14003（契約），treeb440dec3；
main→r1 patch SHA-256為fcbb4a03a1259ac091f49e0f2d26bcf5e81a1c2b00bba709128d6ee0ada1d84c。
CI #306（run40188991114）在r1 completed／success，#99仍draft且未合併，main仍be55a80a。
操作者轉交Claude「需修訂（r2）」；本輪只改conditional契約§4、§5.3、§6(b)，不動其他文件。
接觸帳§44逐字追加EXP-0097，0098登作者修約／來源及未開始構造的範圍。
選(ii)：明列L只能透過區間外類空事件的order型別／pre-between-post位置count固定線性和進入K，
跨P／N固定matrix family，禁止任意rank算術、非線性count處理與逐P調整；不選具體係數或K。
事件自然性不足及區間型別star觀察標為reviewer提示，承重使用前須另補完整假設／證明。
總form須有事前宣告A=F(G_R,G_A;Ξ)及同一K的依賴／代數識別證據，不能以獨立δ-CAR補洞。
不預判新限制足夠；D_Ξ及全部L量詞、§6(a)(c)(d)、primitive型別與停止條件不改。
三帳完整保留r1及main的byte-prefix；README／STATUS、原契約、OP-01及formal全不改。
新model ID NONE；r2尚待exact-head增量複核，保持draft、不合併、不開始conditional構造。
探索軌不具§5.2.1(v)依據資格；formal／E0、A／B及全部資料隔離不變。無新科學執行。


## PR #99 r3：整條下游鏈的時間序依賴限制（2026-10-26；只追加）

r2 head a33cb211b65bcc9a712e7479096233624edb5090／tree0b2fc8c6e7f57feb5ddbcd79fb6399b8866bb64c，
parent為r1 40e14003；r1→r2 patch SHA-256為
051c20bf83ddfccb6238c9c35162232b5ed93a68d6d4a448b260d702e953a85c，遠端與驗證版相同。
CI #307（run40217430617）在r2 success；#99仍draft且未合併，main仍be55a80a。
操作者轉交r2「需修訂（r3）」；接觸帳§45逐字追加EXP-0099，0100登作者修約範圍，下一ID0101。
只新增契約§4.5及§5.3兩行限制：選(i)的更窄子類，下游不直接讀L或重取時間序統計，
只經合規K／Green／同鏈物件承接影響。逐規則列合法上游與factorization，禁止解碼排名／count
後作奇偶、模數、查表、非線性門檻、特徵乘積或係數選擇；合法代數運算仍須逐式交型別／用途。
Ξ記號不能藏直接L入口；變更任何下游依賴類須在新構造前修約、重新exact-head複核。
既有§4.4、M_τσ值、§6與原域／量詞不改；不選K、F、pairing、state或證明策略，不預判存在性。
三帳在r2及main的byte-prefix保持不變；README／STATUS、原契約、OP-01及formal均不改。
保持draft、不合併；r3須GO、必要CI、原樣合併與tree核對後才可開始conditional構造。
新model ID NONE；探索軌不具§5.2.1(v)依據資格，formal／E0、A／B與全部隔離不變，無新科學執行。


## #99合併後與conditional首份交付的紀錄起點（2026-10-28；只追加）

#99經r3 GO、CI #308成功及操作者2026-10-27「同意授權」，expected-head7fbc53d3原樣squash
為main5e5e819ff76cedac84b1be9c20cac5eb1a047842，treee925b0e4be083478f0372b98994e9b837d45ab53，
唯一parent be55a80a；Git committer台北2026-10-27 13:37:57，不作授權或研究開始時間。
操作者轉交合併後核對及分段交付建議；契約§1的GO／CI／原樣合併／tree與登記條件已齊。
本分支第一commit只追加三帳，接觸帳§46逐字登記EXP-0101／0102，下一ID0103。
下一獨立規格commit須先固定全部規則、來源與預想，再有研究輸出；Git只證版本順序，不證盲性。
尚未推送；後續交付須操作者核准具體payload，保持draft，不以本紀錄授權合併。
探索軌不具§5.2.1(v)依據資格；formal／E0及全部既有隔離不變，無科學程式執行。


## CF-01 v0.1獨立規格（2026-10-28；只追加）

第一commit已先逐字登EXP-0101／0102；本第二commit新增CF-01獨立規格並追加作者EXP-0103。
基線main5e5e819f／treee925b0e4；conditional契約§1開始條件已滿足，僅進行E0範圍紙上X-C。
K^ord、七個實際允許M格、全部§4.5分解、CAR／state trial及counterfactual比較類均固定，
不縮D_Ξ、不另給primitive；ordinary-adjoint前提表明列已預想而待正式證明的判定。
作者已腦中預算sector分情形及η-adjoint／零對角風險，來源包括OP-01與reviewer提示；
不稱盲或fresh，Git只證文件版本順序。此commit沒有研究稿、沒有科學程式執行。
規格固定後失敗原樣保存，不在同版改K、pairing、F、state或domain補洞。
主契約、formal及其他歷史內容不改；尚未推送，探索軌不具§5.2.1(v)依據資格，全部隔離不變。


## CF-01紙上研究與固定橋接失敗（2026-10-28；只追加）

先有紀錄commit、獨立規格commit，後有本研究稿；規格完整不改，接觸帳§48追加EXP-0104。
所有P∈D_KQ、全部合規L下，inverse／自然性及契約§6(a)(b)(c)成立，sector span恰2。
固定η-adjoint因[K,H]=0退回ordinary；C Hermitian、同鏈恆等式與F非恆定成立，仍有零對角／負方向，
故(d)與任意正歸一state均失敗，Wick trial二階即停止，不稱已完成高階state。
G_η限定類障礙明列全部假設，不排除其他F／Hermitian diagonal前提之外的類，不擴為全面不可能。
CF-01停止，失敗原樣保留；conditional與原始輸入主問題均OPEN，沒有新增primitive或補洞。
本階段新增研究稿、三帳追加、README／STATUS只改目前狀態；主契約及其他歷史檔不改。
作者已有規格前腦中預想與reviewer提示，非盲研究；紙上代數不是科學程式執行。
本地交付供操作者核准具體payload後推draft，尚待獨立exact-head逐式複核，不自行推送／合併。
探索軌不具§5.2.1(v)依據資格；formal／E0、A／B及全部資料隔離不變。


本地既有回歸：CI指定Python3.12.13／依賴pin的uv隔離環境，556 passed、5 warnings；
integrity及diff --check通過，七檔／prefix／原句／規格保全／目前狀態段範圍核對通過。
這不取代exact-head獨立數學複核，沒有新增科學執行或scientific PASS。


## #100封存與有界文獻盤點起點（2026-10-28；只追加）

#100經GO及CI #310同head重跑成功（556 passed、5 warnings），操作者授權原樣squash，
main74b012db50ee1d7ac3e4288284ff3a28686a3cf2／tree81c0105a10186352bfe36d2a0f8e05589c01c9ee，
parent5e5e819f；Git committer台北2026-10-28 17:24:45，不作授權或盤點開始時間。
操作者選題紀錄2026-10-28 17:39台北：先做有界量子橋接文獻盤點，暫不開CF-02。
本分支第一commit僅追加三帳，接觸帳§49逐字登EXP-0105／0106／0107；下一ID0108。
盤點不是構造或新契約，不能直接選CF-02規則；引用實讀範圍與證據等級另行記帳。
兩主問題OPEN，不升格sector成physical spin；探索軌不具§5.2.1(v)資格，formal／E0及全部隔離不變。


## KQ量子橋接有界文獻盤點交付（2026-10-28；只追加）

基線main74b012db／tree81c0105a；#100已GO、CI成功及原樣合併，CF-01限定失敗正式保存。
前commit已逐字登EXP-0105–0107；本階段接觸帳§50追加EXP-0108與S1–S15完整選讀範圍、
未讀／取用失敗及搜尋片段披露。新增docs/foundations/kq_quantum_bridge_literature_inventory_2026_10_28.md，
逐項附版本／章節／式號及原文明確陳述／作者推論／未查到，附新穎性初對照與Ξ來源分類。
finite inverse／domain、transpose／formal dual、scalar CCR／fermion CAR、總form／covariance及
kinematic CAR／unitary分帳；不把Johnston tentative、Noldus ghosts或continuum FP當本題正state解答。
沒有選CF-02、改契約或新證明，無數值／符號／RNG／撒點／producer／raw／sealed科學執行。
本交付六檔：新盤點稿、三帳追加、README／STATUS只換目前狀態段；其他歷史文件與formal皆不改。
兩主問題OPEN；sector span不是physical spin。探索軌不具§5.2.1(v)資格，全部隔離不變。
本地準備不冒充已發布；後續任何公開傳輸依操作者限定payload授權，draft exact-head由reviewer抽查原文。


本地交付驗證完成（2026-10-28）：CI指定Python3.12.13與numpy2.3.5／scipy1.17.0／
threadpoolctl3.6.0／pytest9.1.1／mpmath1.4.1的uv隔離環境跑既有tests：556 passed、5 warnings，
119.34s。這是既有回歸（含其原有數值測試），不是新文獻模型／符號／數值驗算，未改程式或tests。
integrity、diff --check、六檔範圍、三帳相對main及第一commit的逐位元組prefix、0105–0107原句、
0105–0108唯一ID、README／STATUS只動目前段及新增稿相對連結檢查通過。
這些檢查不證原文引用／分類正確，也不取代reviewer自行讀原文抽查。


## #101封存與T1–CF-01公開階段總結的先行紀錄（2026-10-30；只追加）

#101在核准head9b01f658經GO、CI #312 success及操作者授權，原樣squash為main7c4b5d3a098d7d4952bdcbb111575ebf21fc1ace，
merge tree41ae5e19fecdbd2f4f29166812a3c2c0328a5f18，parent74b012db；Git committer台北2026-10-30 01:48:22，非授權時間。
操作者選題時間依轉交紀錄為台北01:49；起草前已選英文主文＋中文摘要。
第一commit僅三帳追加，接觸帳§51逐字登EXP-0109–0111，並記S2／S7的reviewer取用被截斷、未獨立核實，
以及S4版本號未獨立確認的閱讀上限；不新讀原文補洞。下一ID0112。
總結將只對回已合併稿與#101分類，不新研究、不升格、不改契約／研究稿；兩主問題、G0-B／G0-C及formal維持原狀。
探索軌不具§5.2.1(v)資格，全部隔離不變；本commit沒有主文，發布須操作者另核准具體payload，保持draft。
