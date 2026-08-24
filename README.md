# 零時光網／因果相位網 (Causal Phase Network)

> [!WARNING]
> **本專案狀態**：探索性研究筆記與思想實驗，**不是**已發表或已驗證的物理理論。  
> **當前結論**：不知道可行性，且**已找到至少一個具體的數學死路**。我們非常歡迎任何形式的檢驗與挑戰。

---

## 這是什麼 / What this is
一個公開、可被檢驗、允許任何人挑戰的思想實驗：**能不能不預設時空背景，只靠因果偏序關係和量子振幅，同時湧現出 3+1 維時空與有質量物質？**  
目前的答案是：**不知道，且已經發現了嚴重的退化死路**（詳見 [STATUS.md](docs/STATUS.md) 的【已否定】部分與 `tests/test_appendix_b.py` 迴歸測試）。

## 這不是什麼 / What this is not
- **不是**同儕審查過的物理學研究。
- **不宣稱**推翻或取代標準模型、廣義相對論或任何已確立的物理學。
- **不是**「AI 發現新物理」的宣傳。本專案是人類提出物理直覺、多個 AI 系統交叉校對數學與文獻、並在大量推導被否定後留下的殘骸。詳細誕生過程請見 [專案產出過程說明 (HOW_THIS_WAS_MADE.md)](HOW_THIS_WAS_MADE.md)。

## 目前研究進度 / Current Status
### 目前已完成：
- **Finite causal-set diagnostic testbed** (診斷測試台)
- **Numerical validation infrastructure** (不變量與防溢位數值驗證)
- **1+1D and 2+1D smeared causal-set d'Alembertian benchmarks** (smeared 算子連續極限校準)
- **First continuum momentum-space calibration in 1+1D** (動量空間 IR/UV 飽和分析)

### 目前正在進入：
- **Literature-faithful regularization / spectral-dimension benchmark** (文獻一致性正則化與譜維度基準建立)

### 尚未完成：
- **Emergent Dirac operator** (湧現自旋/手徵 Dirac 算子)
- **Manifold selection** (流形選擇/幾何相消機制)
- **Emergent spacetime** (時空湧現)
- **Gravity** (重力與愛因斯坦方程式極限)
- **Falsifiable new prediction** (可否證的物理預測)

## 專案目錄結構 / Directory Structure

```
├── README.md               # 專案介紹與入口說明
├── HOW_THIS_WAS_MADE.md    # 誠實記錄專案產出過程（人類直覺 + AI 交叉校對）
├── LICENSE-CODE            # 程式碼授權條款 (MIT License)
├── LICENSE-DOCS            # 文件內容授權條款 (CC-BY-4.0 License)
├── docs/
│   ├── handoff_v1.0.md     # 歷史完整交接與背景文件
│   ├── STATUS.md           # 目前研究狀態的最新事實來源 / current source of truth
│   └── foundations/        # Layer 0 / Gate 0 基礎研究與假說層
│       ├── README.md       # 基礎假說層目錄索引
│       ├── invariant_projection_hypothesis.md # 前時空不變量／投影假說提案
│       └── kinematic_selection.md             # Gate 0 入口：運動學選擇（Lorentzian 與有限 c 的選擇問題）
├── tests/                  # 測試程式夾（含 invariants、Q_test 與迴歸測試）
├── benchmarks/             # 基準效能與收斂驗證腳本夾（含 smeared d'Alembertian 2D/3D 與 order 驗證）
└── analysis/               # 分析腳本夾（含 2D 動量空間運算特徵分析）
```

## 為什麼公開 / Why this is public
因果集理論 (Causal Set Theory)、Feynman checkerboard 類模型、因果費米子系統等真實學術研究已存在數十年，本專案很可能只是在重新發現（或弄錯）已知的物理。  

公開專案是為了讓懂這個領域的物理學者或研究者能立刻指出「這在某某論文中已做過／已被排除」，這比讓它留在私有的 AI 對話記錄中更有價值。

## 如何參與與交流 / How to contribute
- **提提案或修正**：請先閱讀 [交接文件 (docs/handoff_v1.0.md)](docs/handoff_v1.0.md) 與 [狀態表 (docs/STATUS.md)](docs/STATUS.md)。
  > [!TIP]
  > 新對話、新協作者或 AI 應優先閱讀 `docs/STATUS.md` 取得目前最新研究狀態，再用 `docs/handoff_v1.0.md` 補足歷史背景。
- **進行修改**：任何修改或提案提交 PR 前，必須先通過本地的 `tests/` 迴歸測試。
- **六道關卡 Issues**：我們使用 GitHub Issues 對應研究路線圖的「六道關卡」（含 Gate 0 前置與 Gate A~E），每個關卡都有對應的 Issue 與 Checklist（參見 Issues 頁面，Gate D 已概念拆分為 D1/D2 但保留原 Issue 4 編號）。
- **直覺探討**：未成形的直覺、物理聯想或大膽猜想，請發布在 **GitHub Discussions**，不要與正式提案混在 Issues 或代碼庫中。

## 授權條款 / License
- **文字與文件內容**：採用 [CC-BY-4.0](LICENSE-DOCS) 授權。
- **程式碼與演算法**：採用 [MIT License](LICENSE-CODE) 授權。
*(注意：此授權聲明不構成法律建議，正式採用前請自行確認條款符合需求。)*
