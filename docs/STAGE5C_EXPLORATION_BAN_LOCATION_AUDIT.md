# 探索 activation 前的禁令定位與處置清單（待複核，未生效）

基線：PR #75 squash main `83b54e051c4339594f48dbe2858b4f7e6fb00a2b`，
tree `4353c6f065f674c200e7f0e50f0ae28b00ba04a6`。
本文件只定位／分類；**沒有改動任何被定位的 operative 文件，也沒有 activation**。
行號只指上述 immutable 基線，未來檔案增行後以章節與原文錨點核對，不以舊行號套用。

## 1. 三處 reviewer 指出的限制：原文與保留理由

| 位置（基線行號） | 原文／文句錨點 | activation 處置 |
| :--- | :--- | :--- |
| [hard controls](STAGE5C_C8_4_HARD_CONTROLS.md) 461–463，§尚未完成第1項 | reference-probe feasibility「其預登記 freeze 且完成判決之前本 control 不得用於任何候選評估」 | 保留 control qualification／evaluation 禁令；已執行 probe 的歷史後續不能直接授權模型評估，統一 mapping／其他 closure 仍須對照。E0 只許紙上構造，不能豁免此條 |
| [results README](../results/README.md) 30–34 | PROTOCOL-INVALID ledger 不得事後重判、跨 target contrast，或「作候選設計輸入」；replacement 不得作 control／calibration／power input | 全部保留，包括 X；burned／公開可下載不解除禁用，不能重組／重算作探索材料 |
| [reference probe](STAGE5C_D1_3_REFERENCE_PROBE.md) 18–24、§5 234–256 | 不產生候選 features／weights／成功模式；sealed artifact「不得以任何形式進入候選設計」；ridge／族別／scores／有效模式不回流 | 全部保留，包括 X、摘要與重算。基線construction禁令實際在這些文句；review提到的169行在此版本是統計程序，依原文定位不因行號差異漏掉禁令 |

## 2. 必須逐項審查的現行操作性限制

`E0-scope` 是**擬議**明訂X紙上例外的時序／權限提示；`KEEP` 是不得因X改寬的
來源／證據／oracle／criterion／執行限制；`HISTORY` 保留原時點的事實与未授權聲明。
同一文件可以兼具三類。以下表格不表示全部行都是禁令：no-go／claim範圍亦需保留。

| 文件／章節與基線位置 | 類別／activation 修改或保留 |
| :--- | :--- |
| acceptance 3、14、20–25；§5.2 177–194；§7 657、668；D.1 803–825 | E0-scope：首段／排除清單／freeze時序／D.1標題末段統一對照；規格本身仍無K公式，九blockers不刪 |
| acceptance §3 91–107、§4／4.3 151；§5.2.1 198–276；§5.3 280–305 | KEEP：物件鏈、L4／no-oracle回流、core／projector／test-space／容差、blinded reviewer、external justification、holdout／budget；不得因改成「正式候選前」掩蓋criteria已受X影響 |
| acceptance C5/C6/C8 451、460、490–529；C9/C10/C11 541–643；D.2–3 829–839 | KEEP：只許evaluation的diagnostics、coordinate輸入禁止、matching baseline／control的候選獨立性、量子／mass／output範圍。X污染須新版prereg／合資格criterion review，不能靜默scope替換 |
| STATUS §2 29–46、Stage5C current列144–146；README 27；roadmap §5 105–138 | E0-scope：current research permission引用單一activation hash；formal PENDING保留；STATUS舊changelog是HISTORY，不能全域改「未設計K」 |
| prereg 首段6–17、§0 43、§1 63、§2 76、§6 284、§8／9 | E0-scope僅加X→F handoff；KEEP：不可執行、planted不回流、oldarm／rehearsal／effect不得填power、numerical access／closure／successor隔離。歷史基準未設計K是HISTORY |
| hard controls §1／§4 169、§尚未完成461–471 | KEEP：L4／conformal targets不進construction、qualification／candidate-independent mapping、未來holdout不可重用development；471可加E0-scope，不刪前四項 |
| results README 30–34；probe §0 18–24／§5 234–256／§6 271–275／§7 292 | KEEP：raw arms、sealed features／weights／pattern與output-only，無binary回流；control判決不是candidate PASS／FAIL |
| probe results §4 82、§6 128–143 | KEEP：post-hoc diagnostics隔離／新計畫新資料；原CONTROL-VIABLE與burned紀錄為HISTORY，不開payload |
| observable contract §1 57、§3 247–253、§5 536–546、§6 561–596、latest frozen-form狀態 | KEEP：L4不進K、selector禁讀target／coordinates／seed／K值；矩陣／weights／test functions／success patterns不是材料，C8不對候選执行；可附X無豁免引用 |
| selector family §1 75、§2 100–101、136、結尾181–185 | KEEP：BlindedCase能力、planted support不回流、family順序／權限；原本無候選交付只屬HISTORY，不改source |
| C3b blind distance §2 52、§5 198／220–222、§6 230–251／結尾286–291 | KEEP：不以candidate support改domain、不用spectrum挑null／weights、不回流reference錨點；X不能以此evaluator結果選構造 |
| primary invariant §5 162–174；basis-group §5 270–271、298／308、結尾441 | KEEP：primary不可依candidate挑方向／權重，basis-gate改寫須候選獨立性；舊「候選前」條款若已有X接觸，需明寫新版／independent審核，不能默改時點 |
| E3 wrong-direction §3 121–129／§6 179–184；certification §3 221／closure286 | KEEP：L4 support mapping、不依candidate反推、zero existence implication；structural controls不得轉construction |
| statistical regions 27、§6 241、§7 277；joint matched law 首段11／§1 32–34 | KEEP：projection／sign／ridge禁選、未freeze不得用regions評候選、development streams不當selection／confirmation／power；舊無candidate聲明HISTORY |
| wellposedness 8／結尾278；typed pairing 7／結尾217；item7 proposal 8–14／216 | HISTORY：各交付不觸candidate／不執行；KEEP：其frozen數值契約／scope。只附當前X權限提示，非藉X重新跑producer |
| 6a-S prereg 9–26／222／329–336；runner freeze 9；incident149／169；amendment001 9／288 | KEEP：無endpoint／contrast／seed重跑／runner權限；historical single-use執行紀錄保留，不改protocol／burn registry |
| E5 budget-power audit 7／366／445；frozen E4 screen 9／30／51／115；screen authorization review 13–77 | KEEP：未授權screen／formal seeds／candidate access；X審查spot check不得冒充screen、resource measurement或power simulation；歷史authorization候選不promote |
| resource measurement manifest 6／75／81／273；resource amendment review27／100／108；run1結果131；item7 feasibility11；item7/8 feasibility7／257；structural-coordinate draft12／327／369 | KEEP：資源diagnostics範圍／receipt／未授權執行、witness限制與OPEN義務；HISTORY保留已執行／未完成事實。X不新增profile／cap／measurement |
| foundations T1/T5 13／202／253–284、B2/B5 293、B3/B4 285–286、B4/B6 §7 241–257／279；Gate0 24 | HISTORY：受審交付未構造與原時點禁令；current索引可引用activation；KEEP：限定定理與OPEN橋接不升格裝置／物理主張 |
| handoff v2 §0 18／§2.3 120–180；handoff v1 247／285；Stage5B result 79–104；foundations hypothesis5–68 | HISTORY／限定前提／舊提案，不是新的操作許可；handoff加current提示，舊材料不可因文獻可達而自動啟用 |
| development log 3／9、DEV-0006行18、DEV-0011行23；amendment log9；接觸帳30／36 | KEEP：append-only／burn／output-only／三帳分工；初盤UNKNOWN不能作blind證明，新增申報只append |

## 3. 搜尋範圍與未來驗收

本次只讀公開文字，不重組ledger、讀sealed欄位或執行producer。兩層搜尋：

```bash
rg -n '不得.*候選|禁止.*候選|候選.*禁令|不得.*construction|不作.*候選|不.*候選.*輸入|不得.*構造|candidate.*forbid|forbid.*candidate' docs README.md results/README.md
rg -n -i '候選|construction|construct.*(forbid|input)|Freeze-1a' docs README.md results/README.md
```

第一層定位明文禁令；第二層含跨行禁止、freeze時點、historical與claim-scope提及。
不能把命中數當作已證完整，activation前仍須讀相鄰條文、重跑搜尋與獨立語意核對。
activation reviewer須在diff逐列標「E0引用已同步／KEEP未改／HISTORY原文保留」，
新發現的操作性條款追加處置。不得只改acceptance而漏掉其他正式evaluator限制。
下列基線檔案覆蓋keyword命中來源（含無操作禁令者），不是全部都要替換的清單。

| 基線 path | keyword 命中行號（非全為禁令） | Git blob |
| :--- | :--- | :--- |
| `README.md` | 27 | `56773238299c3fed95dfb2e09fb97e3cb7525ade` |
| `docs/STAGE5B_RESULT_B.md` | 79,83,92,102,104 | `02ba4e8d283c960cb2683910e26f91f6a698485c` |
| `docs/STAGE5C_6A_E_CERTIFICATION.md` | 9,10,221,286 | `ea5efd68872bf5188b0c847a9ccc8fb8677c0d27` |
| `docs/STAGE5C_6A_E_E5_BUDGET_POWER_AUDIT.md` | 7,366,445 | `04e4b27a09cdb2fe4faf6fe77c7982e343dc097f` |
| `docs/STAGE5C_6A_E_FROZEN_E4_SCREEN_PROTOCOL_DRAFT.md` | 9,30,51,115 | `59c23e2ce45a45bb02f12bdc88e9d78b5bd85a95` |
| `docs/STAGE5C_6A_E_ITEM7_AMENDMENT_FEASIBILITY.md` | 11 | `33148e32a8f43e1cd6b63340c60569a60abef1fb` |
| `docs/STAGE5C_6A_E_ITEM7_AMENDMENT_PROPOSAL.md` | 8,11,14,35,94,122,134,216 | `bff42499072e1def929c110f4330a968e1e40901` |
| `docs/STAGE5C_6A_E_ITEM7_ITEM8_FEASIBILITY_DECISION_DRAFT.md` | 7,257 | `4a91f1121d608161f6e6f274a23f0214dbfec53c` |
| `docs/STAGE5C_6A_E_ITEM7_RESOURCE_AMENDMENT_REVIEW.md` | 27,100,108 | `c0341ece0d00f8aa96d2e3797ba4bdeeb3123535` |
| `docs/STAGE5C_6A_E_ITEM7_RESOURCE_MEASUREMENT_MANIFEST.md` | 6,75,81,273 | `87b8788e991f31744552cab026948f53f563113a` |
| `docs/STAGE5C_6A_E_ITEM7_RESOURCE_RUN1_RESULTS.md` | 131 | `ae2daf1281f2fbb7351b01751429c7c260c400a1` |
| `docs/STAGE5C_6A_E_JOINT_MATCHED_LAW.md` | 11,32,34 | `6ab327b047fb66ef838fb1efaaa975407a537dc1` |
| `docs/STAGE5C_6A_E_PREREGISTRATION_DRAFT.md` | 6,12,17,43,63,76,205,284,336 | `01f5358e16861b620e54bd1f044eca2156ef413f` |
| `docs/STAGE5C_6A_E_SCREEN_AUTHORIZATION_REVIEW.md` | 13,15,19,27,33,34,45,46,53,70,71,77 | `994895d195c744ab450fc20d5563a1d65ef3bf5a` |
| `docs/STAGE5C_6A_E_STATISTICAL_REGIONS.md` | 12,27,241,277 | `e65da01e94afff334aa4904954502d500eba7d29` |
| `docs/STAGE5C_6A_E_STRUCTURAL_COORDINATE_STATISTICAL_AMENDMENT_DRAFT.md` | 12,54,114,192,198,219,327,336,369 | `1fa197b4468d363fff5d694a6cf5c91918ecdf57` |
| `docs/STAGE5C_6A_E_TYPED_PAIRING.md` | 7,217 | `5733706829e771fe41d92b0ca0022c0be94f5af0` |
| `docs/STAGE5C_6A_E_WELLPOSEDNESS.md` | 8,278 | `ccdafb0067c9d42fb9efede1ddf68cf5bd95df8b` |
| `docs/STAGE5C_6A_S_EXECUTION_INCIDENT.md` | 149,169 | `4b717ad0a6442d3dfef2276bda1cc8ae7ca78bb2` |
| `docs/STAGE5C_6A_S_PREREGISTRATION.md` | 9,10,26,222,329,330,336 | `7bf4ec53fd0ee41902933695b832e73cff4cbfcb` |
| `docs/STAGE5C_6A_S_PROTOCOL_AMENDMENT_001.md` | 9,288 | `00a30be99e4cc7bd701d9a317d9d7ee403cfed3e` |
| `docs/STAGE5C_6A_S_RUNNER_FREEZE.md` | 9 | `3eb86e432391e7caecd552c2f09dab30a9c15adb` |
| `docs/STAGE5C_ACCEPTANCE.md` | 3,14,20,22,25,49,62,64,66,68,70,74,81,83,91,103,107,151,173,177,178,180,186,192,194,198,200,209,219,225,229,231,243,244,247,249,253,266,268,276,280,282,284,285,286,326,327,346,361,378,387,391,398,401,414,435,441,451,452,453,460,476,480,490,492,494,498,502,509,510,516,517,523,527,529,541,542,551,557,580,582,657,658,660,668,685,693,695,701,703,707,709,719,737,747,763,768,769,777,791,792,795,796,803,815,817,823,825,829,830,831,838,839,847,848,861,862,864,867,875,876,881,893,894,911 | `f59e51090037fb8743fbefc26a184ac546716194` |
| `docs/STAGE5C_ACCEPTANCE_AUDIT.md` | 25,35,39,55,69,96,106,116,118 | `88c3df4624f47bbbe2f59ae636427fcd14723e55` |
| `docs/STAGE5C_C3B_BLIND_DISTANCE.md` | 23,41,43,52,59,64,118,122,158,169,171,198,204,208,218,220,222,230,235,237,251,268,286,291 | `0cecbdbf36119a5ae5744e8fa219ca76333b3a43` |
| `docs/STAGE5C_C8_4_HARD_CONTROLS.md` | 3,7,12,15,42,44,73,169,172,254,255,257,278,279,380,393,399,416,418,419,425,435,445,451,461,463,465,471 | `31bf6cea34061464b32d41fb84321d4582841cb2` |
| `docs/STAGE5C_D1_3_OBSERVABLE_CONTRACT.md` | 36,176,224,247,253,268,270,304,310,391,392,427,431,432,456,471,475,478,479,480,481,536,544,545,546,561,570,596,656,672,675 | `055f941195e45dd94be55c649d7f62d06590a65b` |
| `docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md` | 5,162,163,167,174 | `d8548b41fca2b3469ffe3e623ec4b8d4e121aa9d` |
| `docs/STAGE5C_D1_3_PROBE_RESULTS.md` | 82,105,128,136,140,143 | `829a76bb8cb372ef0bc4dd2f850ba0688dffedc9` |
| `docs/STAGE5C_D1_3_REFERENCE_PROBE.md` | 18,20,24,39,40,104,234,240,242,271,272,273 | `fda7bb3671bde0c7aaaa79a4a5b0d1a169c01154` |
| `docs/STAGE5C_D1_4_BASIS_GROUP.md` | 16,270,271,298,308,441 | `6a32b47a5213ec014164aa8ad75e30c65079e24f` |
| `docs/STAGE5C_E3_WRONG_DIRECTION.md` | 7,121,129,179,184 | `c5eb261079013b580e685f458bb6fb2b0d225996` |
| `docs/STAGE5C_EXPLORATION_TRACK_DECISION_DRAFT.md` | 7,36,59,131,148,177,193,203,205,207,211,212,213,215,217,251 | `c6b8f219d15f0a3754bae8b10959595255a373a8` |
| `docs/STAGE5C_SELECTOR_FAMILY.md` | 6,46,75,100,101,136,181,185 | `0397e0a2bfb02983c94854efd483acf1c39d27e6` |
| `docs/STATUS.md` | 29,30,38,46,58,84,98,108,124,142,143,144,145,146,147,150,153,171,224,405；history 485起 | `a9e41bdc3b965fed894756fd4c9074e6f8b56cf5` |
| `docs/THEORY_FIRST_ROADMAP_DRAFT.md` | 8,11,21,57,105,112,120,128,130,131,132,163,174,179,180 | `a11c63e02cc1863fda2f8df40abf200a118e6af8` |
| `docs/foundations/b2_b5_interval_volume_cone_audit.md` | 10,34,216,293 | `93fe3eb08adaa5163fb0237a2716284261e90040` |
| `docs/foundations/b3_b4_operational_clock_observer_audit.md` | 11,34,262,285,286 | `bc827317132e98987ed16f908188106d57cbc74b` |
| `docs/foundations/b4_b6_clock_rod_signal_record_realization_audit.md` | 241,250,257,279 | `2dd55f5b04953f88e86372cc6dc2208504e7a591` |
| `docs/foundations/invariant_projection_hypothesis.md` | 5,21,25,31,68 | `0fd2513db7a7b2f4d01c9d37c4fa8ecd3a7c05c1` |
| `docs/foundations/kinematic_selection.md` | 24 | `807ce55c46765f39e4fc57e1d769116330ddab07` |
| `docs/foundations/t1_t5_premise_audit.md` | 13,25,54,202,253,265,284 | `908cbba3c07c2834223638dc99b9ad94d2d5bd8e` |
| `docs/handoff_v1.0.md` | 247,285 | `2941fc750c9c91ab866ade17563eb17832f5f6e2` |
| `docs/handoff_v2.0.md` | 18,44,51,81,120,180 | `e14b8b92ee5296f672811f96b414c638b5600f94` |
| `docs/stage5c_development_log.md` | 3,9,13,18,23,40 | `186d9790ad534414750f46106071cf28270b3e49` |
| `docs/stage5c_exploration_exposure_log.md` | 30,36 | `1ab75618fd2f8e09496faf72a353ee7889f64988` |
| `docs/stage5c_protocol_amendment_log.md` | 9 | `765f4e94a918a6bebbbfca5f8855bf886d3d0045` |
| `results/README.md` | 31 | `a9b1932c28f2f972c26d959c81b732d5380be3d1` |
