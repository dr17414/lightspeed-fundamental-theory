# Stage 5C protocol-amendment log

本表依 `docs/STAGE5C_ACCEPTANCE.md` §5.2.1(vi) 保存 implementation-layer 修改。它與
development log、6a-E confirmatory ledger 分離，不消耗 statistical attempt budget。每筆必須
記錄時間、修改前後、依據、blinding／已見資料狀態與 seed impact；既有列不得刪改。

| Amendment ID | 日期 | 修改項 | 修改前 | 修改後 | 依據 | blinding／已見資料 | seed／budget impact | source of record |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| AMEND-0001 | 2026-09-03 | 6a-S runner／adjudicator ESS identity check、internal-recomputation semantics、fresh seed lifecycle、cross-commit protocol/runtime invariant 與 anti-rerun custody | runner v1 對 `kish_ess` 與 selected-pair integer 使用共同 $10^{-12}$ 絕對容差；prereg §5.4 未列 internal recomputation mismatch；1.3B plus／1.4B minus 原設為兩臂 manifest，沒有 reserved 前端到端 dress rehearsal 硬門；v1 protocol-commit equality 不適用於 staged attestations，未有 committed burn registry，CI numerical dependencies 未 pin | 刪除有因次 `kish_ess-selected` 絕對比較；沿用既有 $10^{-12}$ 無因次 `ess_fraction` relation／$\varphi=1$ identity，exact pure transforms 分帳；internal recomputation mismatch 明列為第五類 `PROTOCOL-INVALID`；3.1B full-arm dress rehearsal → DEV-0012/hash attestation → 1.5B replacement plus → DEV-0013/hash attestation → 1.4B minus 的順序由 runner v2 機械鎖定；四個承重 code files 的 content digest 與 Python／NumPy／SciPy runtime identity 須跨 prerequisite／兩臂一致，CI versions pin，且 claim 前驗證 DEV-0011→0014 append-only burn-registry prefix並拒絕已執行 profile／target | 數學尺度分類與 DEV-0011 root-cause audit；未依事故最大誤差選新 tolerance，沒有修改任何 S1/S5/S6 floor、margin 或 threshold；cross-commit digest、runtime versions 與 registry 只固定 custody／code identity | amendment 撰寫時已見公開 1.3B plus 的正式 categorical verdict 與 DEV-0011 單臂 root-cause diagnostics；未生成、讀取或比較 1.4B；未見任何 between-target contrast、primary endpoint、candidate output 或候選 $K$ | 1.3B 維持永久 burned／retired；本 commit 不生成 3.1B、1.5B、1.4B。3.1B 將於合併後 dress rehearsal 首次 claim 時 burned；其 ledger 不得與任何 minus ledger 配對或回流成 replacement input；若 rehearsal 後需改四檔，只能 AMEND-0002＋fresh dress profile／base；6a-E／candidate confirmatory budget 不變 | `docs/STAGE5C_6A_S_PROTOCOL_AMENDMENT_001.md`; `docs/stage5c_6a_s_burn_registry.json`; `.github/workflows/ci.yml`; `analysis/stage5c_6a_s_runner.py`; `tests/test_stage5c_6a_s_runner.py` |

## 權限決策登記（與 implementation AMEND 分帳）

| Decision ID | 操作者批准 | 受審來源／範圍 | 生效與限制 |
| :--- | :--- | :--- | :--- |
| ACT-X-0001 | 2026-10-12 09:46:37 Asia/Taipei；原句「啟動」 | PR #76 exact head `450a7cfdd9c6a844a9dd08993ea8f7d196ab440d`／tree `4c198ce75bfee1f92fb59e417b75ba116bdc9c12`；[activation E0](STAGE5C_EXPLORATION_ACTIVATION.md) 僅紙上 X-I／X-C | activation exact-head GO ＋ main 合併才生效；合併前 NOT-ACTIVE。實際 commit 由該核准 merge 定位，批准時間不倒填。不是 implementation AMEND、statistical attempt 或執行授權；AMEND-0001／burn 原樣保留。 |

### ACT-X-0001 生效事實追加

PR #78 的獨立 GO head `69e57e4183792c02ba17615b1afce89ee2c71e57`、tree
`c8e4e6ffae89718f77cc70431423244b88b53e79`；CI #255 為556 passed／5既有warnings。
原樣 merge main `0c386716701589c9a6b0b799636a808aacb9ade5`，tree 相同，Git committer
時間 UTC 2026-10-12 09:57:23／台北17:57:23，於此時生效 ACTIVE-PAPER-ONLY。
原批准列保留；本追加不是 AMEND-0002、formal attempt／budget 或新的執行授權。
