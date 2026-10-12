# ACT-X-0001 — 逐文件 E0 同步驗收（activation 待審）

不可變 main 基線：`8d16f9b2ccbbcd74d727694b2770024a91f30616`，tree `4c198ce75bfee1f92fb59e417b75ba116bdc9c12`。
權限來源是 PR #76 受審版本；另包含 PR #77 事實補充，與本 activation 同交 exact-head 複核。
[ACT-X-0001／E0](STAGE5C_EXPLORATION_ACTIVATION.md) 只有核准 activation 合併 main 後生效；本表是作者驗收，不代替獨立 GO。

## 1. 逐來源處置

原[禁令定位表](STAGE5C_EXPLORATION_BAN_LOCATION_AUDIT.md) 48 個 keyword 來源逐一列出；命中不代表都是禁令。
E0-scope 改現行時序文字；KEEP 的禁止資料／core／candidate-independent／執行限制不刪；HISTORY 的原證明與原時點聲明保留。
未凍結的一般來源只在標題後附 current 引用；凍結檔不改原檔，append-only 帳只於末尾追加，無全域替換歷史「未設計 K」。

| 基線檔案 | 分類 | 本 activation diff 處置 | 基線 Git blob |
| :--- | :--- | :--- | :--- |
| [README.md](../README.md) | E0-scope + KEEP | current Stage5C progress 改為 formal PENDING／紙上 E0；其餘主張與完成項保留 | `56773238299c3fed95dfb2e09fb97e3cb7525ade` |
| [docs/STAGE5B_RESULT_B.md](STAGE5B_RESULT_B.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `02ba4e8d283c960cb2683910e26f91f6a698485c` |
| [docs/STAGE5C_6A_E_CERTIFICATION.md](STAGE5C_6A_E_CERTIFICATION.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `ea5efd68872bf5188b0c847a9ccc8fb8677c0d27` |
| [docs/STAGE5C_6A_E_E5_BUDGET_POWER_AUDIT.md](STAGE5C_6A_E_E5_BUDGET_POWER_AUDIT.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `04e4b27a09cdb2fe4faf6fe77c7982e343dc097f` |
| [docs/STAGE5C_6A_E_FROZEN_E4_SCREEN_PROTOCOL_DRAFT.md](STAGE5C_6A_E_FROZEN_E4_SCREEN_PROTOCOL_DRAFT.md) | KEEP／FROZEN | 凍結檔：不改原檔，現行說明以 STATUS／ACT-X-0001 為準；授權 JSON 與既有測試的 pin 原樣保留 | `59c23e2ce45a45bb02f12bdc88e9d78b5bd85a95` |
| [docs/STAGE5C_6A_E_ITEM7_AMENDMENT_FEASIBILITY.md](STAGE5C_6A_E_ITEM7_AMENDMENT_FEASIBILITY.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `33148e32a8f43e1cd6b63340c60569a60abef1fb` |
| [docs/STAGE5C_6A_E_ITEM7_AMENDMENT_PROPOSAL.md](STAGE5C_6A_E_ITEM7_AMENDMENT_PROPOSAL.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `bff42499072e1def929c110f4330a968e1e40901` |
| [docs/STAGE5C_6A_E_ITEM7_ITEM8_FEASIBILITY_DECISION_DRAFT.md](STAGE5C_6A_E_ITEM7_ITEM8_FEASIBILITY_DECISION_DRAFT.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `4a91f1121d608161f6e6f274a23f0214dbfec53c` |
| [docs/STAGE5C_6A_E_ITEM7_RESOURCE_AMENDMENT_REVIEW.md](STAGE5C_6A_E_ITEM7_RESOURCE_AMENDMENT_REVIEW.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `c0341ece0d00f8aa96d2e3797ba4bdeeb3123535` |
| [docs/STAGE5C_6A_E_ITEM7_RESOURCE_MEASUREMENT_MANIFEST.md](STAGE5C_6A_E_ITEM7_RESOURCE_MEASUREMENT_MANIFEST.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `87b8788e991f31744552cab026948f53f563113a` |
| [docs/STAGE5C_6A_E_ITEM7_RESOURCE_RUN1_RESULTS.md](STAGE5C_6A_E_ITEM7_RESOURCE_RUN1_RESULTS.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `ae2daf1281f2fbb7351b01751429c7c260c400a1` |
| [docs/STAGE5C_6A_E_JOINT_MATCHED_LAW.md](STAGE5C_6A_E_JOINT_MATCHED_LAW.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `6ab327b047fb66ef838fb1efaaa975407a537dc1` |
| [docs/STAGE5C_6A_E_PREREGISTRATION_DRAFT.md](STAGE5C_6A_E_PREREGISTRATION_DRAFT.md) | E0-scope + KEEP | 首段 E0／X→F 及 §8 closure scope 引用；§0／§1／§2／§6／§9 和全部 matrix rows 原文保留，不准 numerical access | `01f5358e16861b620e54bd1f044eca2156ef413f` |
| [docs/STAGE5C_6A_E_SCREEN_AUTHORIZATION_REVIEW.md](STAGE5C_6A_E_SCREEN_AUTHORIZATION_REVIEW.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `994895d195c744ab450fc20d5563a1d65ef3bf5a` |
| [docs/STAGE5C_6A_E_STATISTICAL_REGIONS.md](STAGE5C_6A_E_STATISTICAL_REGIONS.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `e65da01e94afff334aa4904954502d500eba7d29` |
| [docs/STAGE5C_6A_E_STRUCTURAL_COORDINATE_STATISTICAL_AMENDMENT_DRAFT.md](STAGE5C_6A_E_STRUCTURAL_COORDINATE_STATISTICAL_AMENDMENT_DRAFT.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `1fa197b4468d363fff5d694a6cf5c91918ecdf57` |
| [docs/STAGE5C_6A_E_TYPED_PAIRING.md](STAGE5C_6A_E_TYPED_PAIRING.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `5733706829e771fe41d92b0ca0022c0be94f5af0` |
| [docs/STAGE5C_6A_E_WELLPOSEDNESS.md](STAGE5C_6A_E_WELLPOSEDNESS.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `ccdafb0067c9d42fb9efede1ddf68cf5bd95df8b` |
| [docs/STAGE5C_6A_S_EXECUTION_INCIDENT.md](STAGE5C_6A_S_EXECUTION_INCIDENT.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `4b717ad0a6442d3dfef2276bda1cc8ae7ca78bb2` |
| [docs/STAGE5C_6A_S_PREREGISTRATION.md](STAGE5C_6A_S_PREREGISTRATION.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `7bf4ec53fd0ee41902933695b832e73cff4cbfcb` |
| [docs/STAGE5C_6A_S_PROTOCOL_AMENDMENT_001.md](STAGE5C_6A_S_PROTOCOL_AMENDMENT_001.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `00a30be99e4cc7bd701d9a317d9d7ee403cfed3e` |
| [docs/STAGE5C_6A_S_RUNNER_FREEZE.md](STAGE5C_6A_S_RUNNER_FREEZE.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `3eb86e432391e7caecd552c2f09dab30a9c15adb` |
| [docs/STAGE5C_ACCEPTANCE.md](STAGE5C_ACCEPTANCE.md) | E0-scope + KEEP | 首段／§0、§5.2 Freeze-1a 時點、§7 freeze 表、D.1 標題／末段同步 E0；九項內容、§5.2.1／core、gates、holdout 保留，mapping 污染另走新版審查 | `f59e51090037fb8743fbefc26a184ac546716194` |
| [docs/STAGE5C_ACCEPTANCE_AUDIT.md](STAGE5C_ACCEPTANCE_AUDIT.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `88c3df4624f47bbbe2f59ae636427fcd14723e55` |
| [docs/STAGE5C_C3B_BLIND_DISTANCE.md](STAGE5C_C3B_BLIND_DISTANCE.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `0cecbdbf36119a5ae5744e8fa219ca76333b3a43` |
| [docs/STAGE5C_C8_4_HARD_CONTROLS.md](STAGE5C_C8_4_HARD_CONTROLS.md) | KEEP + HISTORY | current 引用與 §尚未完成第5項 formal／X scope；原461–463 control資格和mapping／L4禁回流保留 | `31bf6cea34061464b32d41fb84321d4582841cb2` |
| [docs/STAGE5C_D1_3_OBSERVABLE_CONTRACT.md](STAGE5C_D1_3_OBSERVABLE_CONTRACT.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `055f941195e45dd94be55c649d7f62d06590a65b` |
| [docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md](STAGE5C_D1_3_PRIMARY_INVARIANT.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `d8548b41fca2b3469ffe3e623ec4b8d4e121aa9d` |
| [docs/STAGE5C_D1_3_PROBE_RESULTS.md](STAGE5C_D1_3_PROBE_RESULTS.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `829a76bb8cb372ef0bc4dd2f850ba0688dffedc9` |
| [docs/STAGE5C_D1_3_REFERENCE_PROBE.md](STAGE5C_D1_3_REFERENCE_PROBE.md) | KEEP + HISTORY | 只附 E0 不豁免 current 提示；raw／sealed／output-only 禁用及原控制判決原文保留 | `fda7bb3671bde0c7aaaa79a4a5b0d1a169c01154` |
| [docs/STAGE5C_D1_4_BASIS_GROUP.md](STAGE5C_D1_4_BASIS_GROUP.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `6a32b47a5213ec014164aa8ad75e30c65079e24f` |
| [docs/STAGE5C_E3_WRONG_DIRECTION.md](STAGE5C_E3_WRONG_DIRECTION.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `c5eb261079013b580e685f458bb6fb2b0d225996` |
| [docs/STAGE5C_EXPLORATION_TRACK_DECISION_DRAFT.md](STAGE5C_EXPLORATION_TRACK_DECISION_DRAFT.md) | 受審條款來源／HISTORY | 首段區分已審提案與 current activation；#77 原事實性補充同交審，原受審權限正文不修改 | `5d8196fc72c34e68d7f4d92e6cfb91e520a78a09` |
| [docs/STAGE5C_SELECTOR_FAMILY.md](STAGE5C_SELECTOR_FAMILY.md) | KEEP + HISTORY | 只附 current E0 不豁免提示；原數值／資料／評測契約與原交付 scope 原文保留 | `0397e0a2bfb02983c94854efd483acf1c39d27e6` |
| [docs/STATUS.md](STATUS.md) | E0-scope + KEEP | current 權限列、研究排序作用域與 Stage5C acceptance current row 更新；新增 v2.24；v2.23 以前歷史不動 | `aadeeef6a911e989856a99cfe7d86f086f531760` |
| [docs/THEORY_FIRST_ROADMAP_DRAFT.md](THEORY_FIRST_ROADMAP_DRAFT.md) | E0-scope + KEEP | §5 current amendment 狀態更新，原兩階段排序標歷史；不構造模型 | `a11c63e02cc1863fda2f8df40abf200a118e6af8` |
| [docs/foundations/b2_b5_interval_volume_cone_audit.md](foundations/b2_b5_interval_volume_cone_audit.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `93fe3eb08adaa5163fb0237a2716284261e90040` |
| [docs/foundations/b3_b4_operational_clock_observer_audit.md](foundations/b3_b4_operational_clock_observer_audit.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `bc827317132e98987ed16f908188106d57cbc74b` |
| [docs/foundations/b4_b6_clock_rod_signal_record_realization_audit.md](foundations/b4_b6_clock_rod_signal_record_realization_audit.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `2dd55f5b04953f88e86372cc6dc2208504e7a591` |
| [docs/foundations/invariant_projection_hypothesis.md](foundations/invariant_projection_hypothesis.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `0fd2513db7a7b2f4d01c9d37c4fa8ecd3a7c05c1` |
| [docs/foundations/kinematic_selection.md](foundations/kinematic_selection.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `807ce55c46765f39e4fc57e1d769116330ddab07` |
| [docs/foundations/t1_t5_premise_audit.md](foundations/t1_t5_premise_audit.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `908cbba3c07c2834223638dc99b9ad94d2d5bd8e` |
| [docs/handoff_v1.0.md](handoff_v1.0.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `2941fc750c9c91ab866ade17563eb17832f5f6e2` |
| [docs/handoff_v2.0.md](handoff_v2.0.md) | HISTORY + KEEP | 只附 current／歷史分界；原限定定理、no-go、反例、OPEN、舊材料與原時點文字全保留 | `e14b8b92ee5296f672811f96b414c638b5600f94` |
| [docs/stage5c_development_log.md](stage5c_development_log.md) | KEEP／append-only | 只於末尾追加 X scope／獨立權限 register／EXP-0021；DEV、AMEND、EXP 原列不動，不生成 fake attempt／burn | `186d9790ad534414750f46106071cf28270b3e49` |
| [docs/stage5c_exploration_exposure_log.md](stage5c_exploration_exposure_log.md) | KEEP／append-only | 承接 #77 的 EXP-0020，再末尾追加批准決策 EXP-0021；原 EXP 列不动，不生成 fake attempt／burn | `9215ca053a66333759ee0ee9bae036c89c802dbf` |
| [docs/stage5c_protocol_amendment_log.md](stage5c_protocol_amendment_log.md) | KEEP／append-only | 只於末尾追加 X scope／獨立權限 register／EXP-0021；DEV、AMEND、EXP 原列不動，不生成 fake attempt／burn | `765f4e94a918a6bebbbfca5f8855bf886d3d0045` |
| [results/README.md](../results/README.md) | KEEP + HISTORY | 只附 E0 不豁免 current 提示；raw／sealed／output-only 禁用及原控制判決原文保留 | `a9b1932c28f2f972c26d959c81b732d5380be3d1` |

## 2. 後續新增來源與保留檔案

| 檔案 | 處置 |
| :--- | :--- |
| [原禁令定位](STAGE5C_EXPLORATION_BAN_LOCATION_AUDIT.md) | 只末尾加 current 提示，舊48來源及基線表不覆寫 |
| [Claude 原申報](claude_exposure_declaration_2026-10-12.md) | 逐位元未改 |
| [GPT 有界申報](gpt_exposure_declaration_2026-10-12.md) | 原申報未改；本次接觸在 EXP-0021 另記 |
| [操作者申報](operator_exposure_declaration_2026-10-12.md) | 僅承接 PR #77 已知接觸追加，本 activation 不再改原句 |
| [ACT-X-0001](STAGE5C_EXPLORATION_ACTIVATION.md) | 新增批准／受審來源／E0／合併生效／scope／隔離／退出條件，無模型 |

## 3. 搜尋、作者檢查與獨立複核要求

在此 working tree 重跑原兩層查找：

```bash
rg -n '不得.*候選|禁止.*候選|候選.*禁令|不得.*construction|不作.*候選|不.*候選.*輸入|不得.*構造|candidate.*forbid|forbid.*candidate' docs README.md results/README.md
rg -n -i '候選|construction|construct.*(forbid|input)|Freeze-1a' docs README.md results/README.md -g '*.md'
```

本表以原48來源及新增申報／activation／定位表為界。新增命中若具有操作性，须读上下文另列；
keyword數目不能證明完備。reviewer逐行核對 E0／KEEP／HISTORY，不由作者表直接判 GO。

作者檢查包括：E0 五行與 PR #76 源完全相同；acceptance C0–C11／core、D.1九項、prereg
matrix rows、一般文件原正文、三帳 prefix、STATUS v2.23 以前歷史與科學檔案保存；local
links／headings／fences／tables、integrity、diff 格式。CI／機械檢查不證隔離成立。

**被測試或授權 JSON 固定版本的檔案不得修改。** 對照已凍結來源的實際 Git blob，
包含 frozen E4 screen protocol，逐位元保存原 pin；不能加 current 提示、更新 pin 或
改測試來容納 activation。現行作用域只在未凍結的 STATUS／ACT-X-0001 說明。

activation 的 exact head／tree 由 PR 身分與新 GO 指定；合併時必須核對 main tree 相同。
沒有舊 GO 自動延伸、空 confirmatory ledger、scientific PASS、模型、seed、主機或量測。
