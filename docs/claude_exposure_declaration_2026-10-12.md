# Claude 接觸申報（供探索接觸帳追加；actor 自行申報）

- Actor／角色：Claude（獨立數學／證據 reviewer）
- 申報日期：2026-10-12（Asia/Taipei）
- 依據：本 Claude 工作階段（2026-10-06 起）可回溯的指令與輸出紀錄
- 範圍界線：Claude 不保留跨工作階段記憶。本工作階段以前的 Claude 接觸，例如 repo DEV-0016／0017 記載的「Claude 外部 200,000-rep simulation」等，一律申報為 **UNKNOWN**，並依草案 §3 以「可能已暴露」保守隔離。本申報不構成 blinded 資格。

## A. 公開 repo 文件與程式（讀取）

- STATUS、README、6a-E prereg draft（§0–§2、§8 closure 表）、acceptance（以 grep 讀取部分條文）、item 7 manifest／results／amendment 文件、PR #64–#75 的全部新增文件、foundations 審計（T1+T5、B2+B5、B3+B4、B4+B6）、探索草案與接觸帳草案。
- 程式碼：`benchmarks/stage5c_e4_v02_resource_{campaign,methods,characterization}.py`、`stage5c_e4_v02_container_launch.py`、`analysis/stage5c_{continuum_pairing,e4_wellposedness,e4_wellposedness_v02,primary_invariant,statistical_regions}.py` 的相關段落，以及相關 tests。
- 程度：公開文字、公式與程式碼；未開啟 6a-S raw arm ledgers、reference probe 的 sealed features／weights／scores、burn registry 的內容細節、任何 6a-E arm 或 holdout 資料。

## B. 原始證據包（皆為資源／執行層級，不含 scientific endpoint 值）

| 證據包 | SHA-256 | 看到的內容 |
| :--- | :--- | :--- |
| managed-session stub bundle（GPT 環境） | （未記錄 zip hash） | 心跳、boot ID、throttle；無數值 producer |
| vultr_stub_evidence.tar.gz | bcd74b52…5adf | 三輪 90 分鐘 stub 心跳；無數值 producer |
| campaign-image-evidence tar.gz | 25089234…4911f91 | 建置紀錄、套件 lock、smoke 結果（import／BLAS／掛載）；無 endpoint |
| pf3-evidence.tar.gz | 6187e794…f33e | launch proof、docker inspect、假 receipt |
| run1-evidence.tar.gz | 8c26b657…06bf | 139 job 的 phase CPU／wall、RSS、outcome、stress 計時；production 紀錄只有 status／subdivisions，**無 endpoint 數值** |

## C. Claude 自行執行的數值計算（DEVELOPMENT，非正式資料）

1. **E4 producer 直接呼叫（PR #68 複核，2026-10-10）**：以 `numpy.random.default_rng(0)` 對兩個 repo 測試 fixture atoms `[.8,.8,.2,.2]`、`[.7,.3,.05,.2]` 加 ±0.04 均勻擾動，組成 1–4 個 atoms 的人工混合（權重正規化），θ∈{−0.4,+0.4}，共 6 組，分別呼叫 v0.1 與 v0.2 `evaluate_e4_wellposedness`。看到：完整 2×2 矩陣（非對角恆為 0）、對角元素值、certification endpoint（第一分量約 0.34–0.9999999，第二分量 0）。**沒有使用 selector、causet generator 或任何 seed manifest**；這些 atoms 不是 target-law 樣本。exact atoms 可由上述 RNG 與程序重建。
2. **witness JSON（PR #69）**：讀取 metadata 及 2 筆已存 rows 的部分欄位（包括 adaptive 矩陣的對角 hex 值），以及 execution note；未解碼 fixture coordinates，未重跑。
3. **run1 判讀重播**：以 repo `assess_held_out` 對 run1 records 重算；看到全部 34×37 的 prediction／observed／verdict。
4. **Hoeffding／成本算術**：純規劃算術。
5. **數學 spot check（不涉及物理樣本）**：隨機矩陣驗證 BdG 行列式（rng 1）、ℓ∞ 錐遞移性（rng 3）、Lorentz 群／BHS 升指標／觀察者族等變性（rng 5）、各審計中的體積與回波公式。只用於驗證已寫出的代數恆等式，不用於選擇模型。
6. **一次未完成的匯入**：一個以錯誤名稱匯入 `bind_endpoint_certification_rows` 的腳本，在任何計算前失敗。

## D. 外部文獻

- Nicholas (2026) arXiv:2606.25993v1：透過 WebFetch 讀取摘要，以及 §2.1、§5、§6 的摘要式引文。
- Anker–Ziegler (2020) v2：兩次讀取皆因權限確認逾時失敗，**未讀**。
- 其餘文獻（BHS、Malament、Perlick 等）在本工作階段未直接讀取原文，只讀 repo 內的引用。

## E. 對模型／criterion 的影響

- 本工作階段**沒有設計任何候選 K、order ansatz、weight 或 phase law**。
- C1 的 E4 呼叫曾讓我提出「第一分量可能接近 1」的觀察（已記錄為 O2／O13 OPEN）。這屬於 evaluator 層的診斷接觸，日後若有 X-I 模型以第一分量行為作為設計依據，應引用本條作為可能的影響來源。
