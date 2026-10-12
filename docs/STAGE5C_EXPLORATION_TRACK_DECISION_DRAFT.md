# 探索軌道協定修訂決策草案：理論構造與正式驗證分離

**條款來源與 current activation：** 本文件是 PR #75／#76 已審核的提案來源，原時點
狀態與「merge 不生效」指草案合併。操作者其後於 2026-10-12 09:46:37 明確批准
僅紙上啟動，獨立 [ACT-X-0001／E0 記錄](STAGE5C_EXPLORATION_ACTIVATION.md) 在
其 activation PR 經新 exact-head 複核並合併到 main 時才生效；此前 NOT-ACTIVE。
下列未生效／待審文字保留原時點，不用來否定其後合法 activation，也不擴張受審權限。

狀態（#77 時點）：**【PR #75／#76 已審核、未生效；本次事實性接觸補充待複核】**。
Claude 核准 #75 head `d57d3cb661d168f56cc8d04cbcd8315ea41b400e`、tree
`4353c6f065f674c200e7f0e50f0ae28b00ba04a6`；依操作者授權原 head 合併 main
`83b54e051c4339594f48dbe2858b4f7e6fb00a2b`，tree 完全相同。沒有 activation commit。
其後 Claude 核准 #76 head `450a7cfdd9c6a844a9dd08993ea8f7d196ab440d`、tree
`4c198ce75bfee1f92fb59e417b75ba116bdc9c12`，涵蓋審查工具釐清、禁令定位與三方
有界申報；原 head 合併為 `8d16f9b2ccbbcd74d727694b2770024a91f30616`，tree 相同。
（#77 時點）本次只追加操作者提供的歷史轉交／終端閱覽補充（EXP-0020）；不把 #76 GO 擴成
對新文字的核准，亦不提交 activation。
操作者於 2026-10-12（Asia/Taipei）選擇 B，授權起草本案，**沒有授權開始構造**。
原稿基線為 PR #74 合併後 main `87ff77a1a3c44bef4f3c33ade91c3ef0e0623acd`，
tree `91aa84112329bdee017c7d7dddc44a53e1d67afa`。
本次只交 Markdown、接觸盤點與逐項修改方案；既有候選 K 禁令繼續有效。

## 0. 要裁決的問題與生效方式

[B4＋B6 審計](foundations/b4_b6_clock_rod_signal_record_realization_audit.md) 已獨立核對
紀錄的可識別性與條件式比較公式；實際 tick、訊號、響應與尺規的實現仍 OPEN。
它不證明任何模型存在，也沒有證明所有 B6 路線必須用 Stage 5C 的 K。
本案建議允許另軌的紙上實現研究，保留原正式主張、所有反例與驗證義務。

**本案的 merge、CI 成功或 reviewer GO 都不等於生效。** 狀態依序為：

1. `DRAFT`：本案；只許盤點、複核、修改協定文字，不許新模型構造。
2. `REVIEWED-NOT-ACTIVE`：Claude 核對 exact head／tree、操作者接受草稿保存；仍未生效。
3. `ACTIVE-PAPER-ONLY`：操作者明確批准具名版本的權限與範圍，完成 §8 的同步文字與
   §3 的接觸申報，在 activation commit 記錄批准版本、審核版本、操作者決定及生效範圍；
   activation 的改動限於受審條款和事實性申報，新增實質條款須再複核。
4. `PAUSED`／`CLOSED`：依 §9 停止；不得以舊 ACTIVE 記錄繼續工作。

不得倒填生效時間。生效前的未授權構造不能靠後來批准變成合規。
每次工作開始前引用 operative activation commit；沒有該記錄，預設 `NOT-ACTIVE`。
操作者可以拒絕、縮小或延後生效。選擇 B 是方向決定，這次交付仍是供審草案。

## 1. 建議權限：先限定為紙上研究

以下是**生效後擬議**權限，不是當前授權。每份交付先列研究 ID、命題、定義域、
輸入／前提、證據、未證橋接、否定條件與後續驗證；沿用路線圖六欄契約。

| 類別 | ACTIVE-PAPER-ONLY 擬允許 | 必須保留的限制 |
| :--- | :--- | :--- |
| X-I：intrinsic 方向 | 在另軌文件提出 order-only 的紙上模型／toy objects，包含探索 K 的定義、材料與參數化；作解析存在性、相容性與 no-go 研究 | 明列 L0–L3、容量、非 canonical 選擇與來源；不稱正式候選，不進 C0–C11 判決；禁用 §2 的 evaluator／sealed 輸入 |
| X-C：conditional 方向 | 在明示的連續背景、度規、邊界、物質／狀態前提下，研究鐘／尺／訊號的紙上模型與解析性質 | 新 primitive 是條件式假設，不改稱 L0 湧現；與原 1+1D massless S5C-Claim 分帳，不用其成功替 C0 PASS |
| 解析比較 | 人工明寫有限 toy 定義、精確反例、符號推導，或對已有文獻模型作具名條件分析 | toy／論文例不是正式樣本；不把一個例子推成典型性或全域結論；文獻若承重須完成適用域／convention mapping |
| 模型選擇與撤回 | 比較具名版本、記錄否定／未完成方向與前提改動 | 全部保留；每個選擇有來源／接觸依賴，不能只留下成功版本 |

本案**不**授權新的程式模型實作、用於模型探索／篩選的 symbolic／toy 診斷、研究 RNG／seed 生成、selector／
E4 witness、抽樣、量測、主機、雲端消費、receipt、正式 arm ledger 或 scientific PASS。
「紙上 toy」是文件中的定義與推導，不包括執行 toy ensemble。既有 regression suite
只可作 repo 檢查，不能呼叫正式 runner 或產生新科學資料；新增執行工作須另案具名
計畫、預算、資料隔離與適用的 receipt／preflight，不能由本案自動繼承。

X-C 可以研究另給背景的物質；它不是把原 S5C-Claim 改成背景給定，也不解除 C11 的
3+1D output firewall。每個背景、時鐘刻度、狀態、裝置 mark、作用量或概率律都須逐項
列為假设或已證輸入，並將 B1–B7 的未證橋接帶到下游。

### 1.1 審查工具與模型探索計算的界線（補充提案，待複核）

**數學複核可用有限的本機數值／符號 spot check**，包括人工矩陣或 reviewer 自定
RNG 檢查已寫出的 BdG 行列式、cone／Lorentz 等變性、體積或回波恆等式，以及
嘗試找固定命題的反例。這類工具不因使用 NumPy／RNG 就變成模型探索；判別依據是
是否檢查**事先已存在、具名、固定前提與 source version 的命題**，以及輸入／輸出的用途。
本條釐清獨立複核的方法，不啟動 X 的模型構造；本次沒有新 spot check 執行。
§1 已允許的既有 regression suite 仍限 repo 檢查；不能用它的既有 producer tests
推論新的直接 E4／selector 診斷亦已獲准。

允許的審查報告須列：被檢命題／版本、人工定義域、程式／算法、matrix sizes／
cases／精度／資源的有限邊界、review RNG／draw policy（若使用）、失敗／反例與
全部嘗試摘要。這些是 review-only randomness，**不是 scientific seed／formal manifest**。
不得呼叫 causet／selector／E4 producer、讀 raw arm／sealed artifact，亦不能重算
reference probe 或使用禁止回流的 planted material。若 reviewer 檢查需要超出此邊界，
先另案授權；Claude 已申報的歷史人工 E4 接觸仍是 evaluator-development，不由本條
倒改為純恆等式檢查或恢復其資料盲性。

數值 agreement 只檢查已給等式／實作、可發現錯誤；它不證全稱定理、典型性、
power、coverage、物理可實現性，也不產生 scientific PASS。找到反例應修正／撤回
該具名命題並留版本；不能依觀察調 model／weight／phase／projector／margin，或
改輸入／抽樣直到得到有利圖樣。若結果促成**新模型或參數選擇**，它已跨到 exploration：
停止該用法、追加 exposure／decision，檢查 ACTIVE scope；可執行模型探索仍需另案。
不得把 reviewer 的反例搜尋／修正論證偷偷用作新候選搜尋。

## 2. 雙軌、oracle 與資訊流

| 項目 | X 探索軌道 | F：原 Stage 5C 正式驗證軌道 |
| :--- | :--- | :--- |
| 產物／ID | `X-<problem>-<version>` 的文件與 development 記錄；只作探索／限定定理 | 只有完成 freeze／審核／資料授權後，才有正式 candidate／attempt ID |
| 證據 | 已披露且允許使用的開發材料、明示文獻前提、解析證明 | frozen evaluator／estimand／gate／power 下的真正新資料及適用的解析證明 |
| 判決 | 【探索】／限定解析狀態，無 scientific PASS | 原 verdict taxonomy、C0–C11、closure／global spending 不變 |
| 帳本 | 接觸帳＋既有 development log；不佔 formal attempt budget | confirmatory ledger 的事前 attempt、揭露後 burn／spending；不得改名重置 |
| 執行 | 本案只擬允許紙上；無 seed／host／runner 權限 | Freeze-1a／1b／1c、2a／2b／2c 及 execution firewall 仍須履行 |

**禁止輸入 X，亦禁止透過提示、摘要、記憶、重算或代理人間接輸入：**

- 保留／未揭露 holdout 的資料、seed、metadata、target label、sealed coordinates；
  未批准的 6a-E 樣本／arm numerical fields、6a-S raw arm ledgers（1.3B／1.4B／1.5B／3.1B）。
- reference probe §0 sealed features、weights、逐樣本 scores、族別貢獻與成功模式；
  兩項未登記 baseline diagnostics 及其衍生摘要。公開 seed／程式可重算，**也不得重算**。
- 正式／planted evaluator 內 L4 oracle payload、support mapping、gamma／metric／target
  資料作為 X-I 的設計、參數、lookup 或調整依據；不得 import／執行 probe／control
  generator 以取得構造材料，不得把 oracle-built planted object 改名 intrinsic toy。

已披露的 categorical 結果與能力邊界可以幫助決定「還需證什麼」，不能把同一觀察
重包成模型的獨立驗證。原規則不許回流的數值／pattern，不能因現在標【探索】而解禁。
對舊 Stage 5C core 的採用、放寬、刪除，仍受 acceptance §5.2.1(v) 約束。

**X-C 的外加背景與 L4 leakage 不同，但不能靠改名混淆。** 可以在獨立條件文獻或
明寫公理下給定通用背景，記來源、適用域和此新增前提；不能開啟 sealed artifact，
抄 probe／planted 的成功模式，再稱它是公理。若定義或參數受到已見 evaluator 內容
影響，記為 evaluator-informed conditional branch，**禁止轉成原 S5C-Claim 的構造**。
只有另立主張／新版 prereg 可審其條件式意義，不獲 order-only 身分。

研究者已讀過公開規格的事實不能抹除。可達到的是可稽核的來源隔離，而非宣稱
GPT／Claude 心理上「忘記了」。X-I 文件／dependency graph 列出每個輸入與推導來源，
獨立 reviewer 查有無 oracle 推回公式；無法排除回流者標 `ORACLE-EXPOSURE-UNRESOLVED`，
該分支暫停。若日後開放程式，才另審 import／runtime capability 與 taint 防護；
本案不把尚未實作的 sandbox 說成已存在。

## 3. 接觸帳、舊資料與未知項

初始盤點見 [探索接觸帳草案](stage5c_exploration_exposure_log.md)。它保留既有 DEV-0001–
0028、6a-S burn registry、run1／witness 的 source anchors，不讀 raw arm ledger，
也不改原 JSON。**repo 公開不等於每位研究者實際看過**；初始表分開可達、repo custody、
本輪讀取、操作者轉述 Claude 複核和尚待本人申報。

2026-10-12 補充：Claude 的[自行申報原檔](claude_exposure_declaration_2026-10-12.md)
逐位元保存，GPT 亦提交[目前可回溯範圍的自行申報](gpt_exposure_declaration_2026-10-12.md)，
接觸帳追加 EXP-0016–0018／§5；不覆寫初盤，也不代替操作者申報。
Claude 的人工 E4 endpoint 接觸記為 evaluator-development；舊階段 UNKNOWN 保留。
操作者其後提交[本人文字與截圖的有界申報](operator_exposure_declaration_2026-10-12.md)：
下載四份具名證據包、未打開 raw 檔，其餘 UNKNOWN；接觸帳追加 EXP-0019／§6，
不覆寫 §5 的收件前狀態。三方的有界申報現已收存，未知與隔離仍須審查，
不宣稱全歷史完整、盲性或 activation 條件已滿足；本輪不提交 activation。

生效條件：操作者、GPT、Claude 分別列出其可回溯的接觸範圍、取得途徑、程度、
相關模型／criterion 決策及未知項；不得由 GPT 代替 Claude 宣稱未見資料。
不能證明完整歷史時，以基線全部公開 repo 材料保守視為**可能已暴露**，並隔離未知
私人材料；這不把禁止資料降級成「可探索」。缺精確 manifest 的 development seed
區段沿用既有整段 burned 規則，不縮小為剛好記得的 seeds。

每次**新增接觸或模型選擇**，在下個交付前 append 記錄，至少含：UTC／台北日期、
actor／role、取得途徑、artifact path／commit／hash、公開／sealed、看到內容的程度
（metadata／categorical／數值／raw／未完成）、data law／split／seed identity 或
`NONE`／`UNKNOWN`、相關 X version、採用／丟棄／改動、對 core／gate 的影響、
burn／quarantine／正式重用資格及證據。轉給另一位 reviewer／GPT 也新增接觸列。
未知內容只登 metadata／custody；不為「盤點完整」去讀禁止 artifact。
更正只追加並引用原 entry，歷史列不能覆寫；未完成和失敗結果同樣入帳。

四類處置不能混用：

1. **允許的已披露 development／公開解析材料**：可依 §2 使用，永久不能作同一後續
   claim 的新 confirmatory instance；依賴這些材料設計的 model 必須承認其適應性。
2. **已 burned 但內容仍受限制的材料**：burned 不等於解除 sealed／output-only／禁回流。
   6a-S raw arms、probe protected artifacts 仍拒絕探索；保留舊 burn，不開啟。
3. **未揭露正式／保留資料**：不接觸、不生成、不預覽，不為本草案配置新 seed range。
4. **歷史未知／意外接觸**：記 `QUARANTINED-UNKNOWN`，在來源與影響釐清前暫停相關
   分支，不能斷言 fresh／blind。若無法釐清，相關結果不能申請原正式資格。

接觸帳不能替代 global statistical ledger。若意外揭露已有登記的正式 holdout，依原
spending／burn 規則處理，不能改叫探索以逃避；若尚未配置正式 attempt，仍 quarantine
該資料並記事故，由 reviewer 判定適用影響，不虚構不存在的 statistical spending。

## 4. 標記、定理與升格

探索模型、toy 行為、未完整推導與所有模型選擇均標 **【探索】**，想法尚無支持則
【提案】。每次引用帶上定義域、額外假設、未證 B-bridges 與 exposure ID。
不把「沒找到反例」写成存在定理，也不把 no-go 擴至未證涵蓋的類別。

完整解析證明或精確反例經**獨立 exact-head 數學複核**後，只可將具名命題在原
定義域／前提下升為【已確認／限定解析】；模型的物理解讀、典型性、装置實現與
未證橋接不隨之升格。獨立數學 reviewer 可看證明；這不等於其有資格擔任
看不到候選輸出的 blinded criterion reviewer，兩種角色分別記接觸狀態。

探索永不產生 scientific PASS、C0 PASS、6a-E PASS、item 7 ADOPT 或 Freeze 完成。
定理已確認也不自動授權任何 seed／量測／主機。既有規則下的正式 PASS 不改判，
不得把它對照探索模型重新挑選而成為新 claim 的證據。

## 5. 探索回到正式驗證：須通過的審查點

本案不保證任何 X model 能轉為 F candidate。轉入前另提交具名 handoff PR：

1. **主張與來源審计**：確定是原 1+1D S5C-Claim 還是 conditional 新主張；逐項
   C0/L0–L4、capacity、object／basis／state／adjoint、oracle dependencies、額外前提，
   完整 exposure graph 與失敗版本。X-C 不能只刪前提標籤就轉成 intrinsic。
2. **既有資格逐項對照**：原 D.1 九項與 6a-E closure 各列有效／待重驗／被新版
   supersede 的理由及 source hash；不得把 exploratory proof 填成 closure CLOSED。
   保留 item 7 不可 ADOPT、v0.2 items 3–5 重驗、item 8 的 coverage／matching／effects／
   power 義務。完成全部相關 freeze 與 resource qualification 才可申請執行。
3. **候選與完整測試契約凍結**：正式接觸新資料前固定 candidate source／version、
   evaluators／estimands／primary endpoints／targets／sampling law／matching／independent
   units／projector／test-space／margins／gates／power／failure accounting／stop rules／
   numerical certification／資源界／global spending，給出獨立審核與 freeze hashes。
   第一個正式批次不得先跑再补欄位；後續 staged 1b/1c 僅保留原已凍結形式下的
   implementation instantiation，不能以本條放寬 acceptance §5.2.1。
4. **criterion 已被探索影響時**：若任何 model／輸出／已見資料影響 core、projector、
   test-space、margin、estimand 或 selection rule，舊資格不沿用。須新版 prereg、
   變更對照、exposure mapping、external／mathematical justification 與適當独立／blinded
   criterion review。原 core 禁回流與不可放寬規則不被新版自動解除；若要更改，須
   另行明確裁決新主張，不能倒填原 Stage 5C PASS。找不到合資格 blinded reviewer 的
   fallback 項目維持 OPEN，GPT 與 Claude 若已見相關輸出不能互稱 blinded。
5. **真正新資料**：已看過 instances／seeds、重跑同一 batch、改 target 配對、衍生
   summaries、選過的 fixtures 均不能當 fresh confirmation。custodian 在上述 freeze 後
   才依新 data-generating plan 配置／生成獨立 streams，登記 disjointness、血緣與 hash；
   authors／reviewers 在合法揭露前無資料、seed 或 metadata 存取權。
   只換 seed 不能修復 criterion 污染。允許明訂 sampling law 下的新獨立樣本偶然與
   舊有限 poset 同構；不能為「避開已見形狀」事後剔除而默改分布。clone／lookup
   重用與偶然同構分開，去重／排除规则若需要，須事前定義並納入 law／power。
6. **另授權執行與回報**：完成 receipt／preflight／runner review／相關新資格後，才由
   操作者另授權正式 attempt。holdout 只揭露一次、burn／spending 跨版本繼承；任何
   發現與 verdict 必要前提衝突的診斷保留 `POSTHOC-CONFLICT`，不維持正面承重。

前述 freeze 應使所有會決定判決的規則唯一化；candidate-dependent 層不可自訂
evaluator form，implementation 不能刪掉負模或吞掉 core。新 data 本身不能證明
oracle-informed 模型「從未回流」，也不能恢復研究者對舊結果的盲性。

## 6. 開發與決策紀錄的分工

接觸帳保存「誰看過什麼」；既有 development log 保存候選版本／採用／丟棄，
formal confirmatory ledger 保存事前 attempts／spending。三者相互引用，不互相代填。
本案沒有新的 attempt、burn registry 更新或 seed manifest。

現有 [protocol-amendment log](stage5c_protocol_amendment_log.md) 的 scope 是
implementation-layer 修改。本案是**尚未生效的權限修訂**，不能偽裝成已執行的
AMEND entry。若生效，另設 decision-register 區塊或具名 activation record，與既有
AMEND-0001／DEV entries 逐位元保留並分帳；引用本案的 exact reviewed tree。
future implementation amendments 仍依原 §5.2.1(vi) 記錄，不佔 statistical budget。

## 7. 啟動後的第一份交付（只定問題，不給模型）

建議先由操作者在生效範圍內選**一個** B4／B6 實現目標，提交問題契約：
要實現 tick、signal response 或 rod comparison 的哪個明確性质，定義域為何，
允許的 primitives、欲證存在／no-go、誤差或 failure 語意及退出條件為何。
先限定解析可判定問題，再裁定是否需要執行。這一段沒有指定算子形式、材料、
order ansatz、weight 或 phase prescription；不是第一個模型的 construction brief。

## 8. 同步文字修改方案與相容性清單

**本 PR 的 operative 文件只附「pending／未生效」連結；下列替換文字是待決方案，
不是現在的規則。** activation PR 必須檢索所有現行禁令，逐項給 diff 與審查結果；
歷史快照／舊版本 changelog 原文保留並標其時間，不全域替換歷史「未設計 K」。

具體位置、原文錨點與基線 blob 見[禁令定位清單](STAGE5C_EXPLORATION_BAN_LOCATION_AUDIT.md)。
它另點名 hard controls §尚未完成第1項、results README 的候選輸入禁用，以及
reference probe §0／§5 的 features／weights／patterns；三處都保留，不是 E0 豁免。
activation 前仍需重跑搜尋、逐列 current／KEEP／HISTORY 核對；本次未修改其原文。

統一擬議條款 **E0**（各 current 文件引用同一 activation commit）：

> Freeze-1a 完成前，原 Stage 5C 正式候選資格與 confirmatory evaluation 仍不得開始。
> 僅已生效的 X 探索軌道可在其紙上範圍內設計探索模型／探索 K；這些不是正式
> 候選，不產生 scientific PASS，不修改任何正式 gate／core，不授權資料或執行。
> X 權限、來源隔離、接觸帳與回到正式驗證的條件以具名 activation commit 為準；
> 沒有 ACTIVE 記錄，沿用原 Freeze-1a 前全面候選設計禁令。

| 文件／current 位置 | 現行限制 | activation 必須怎麼改、哪些保留 |
| :--- | :--- | :--- |
| acceptance 首段、§0 排除清單 | 本規格不含 K；Freeze-1a 前不得候選設計，不供材料 | 本 acceptance 本身仍不給公式／材料；加 E0 的外部 X 例外與禁止回流，不把 matching／diagnostics 改成材料許可 |
| acceptance §5.2 Freeze-1a timing、§7 freeze 表／末段 | 「任何候選設計前」；九項完成前不得設計候選 | timing 改為「正式候選資格／正式評測前；另軌 X 紙上設計僅依 E0」；1a/2a/1b/2b/1c/2c hashes、不可逆規則及所有正式前置保留 |
| acceptance D.1 標題／末段／風險註記 | 阻塞候選設計及 Stage5C-1；mapping 須候選前確定 | 加 E0 作用域；九 blockers 不刪，mapping 若已受 X 影響不能繼續稱 candidate-independent，走 §5 新版／blinded review，不僅改成「正式候選前」掩蓋污染 |
| acceptance §3、§4.3、§5.2.1、§5.3、C0/C9/C10/C11、D.2–D.3 | object／oracle／core／holdout／output 與反繞道 | 保留全部正式約束，附 X 不享豁免的交叉引用；§5.3 development 工作只在相關 phase／X 授權存在時可做，不從「不佔 budget」推導構造權限 |
| STATUS §2 研究排序及 Stage5C current 列 | 現行 K 禁令、Freeze-1a PENDING | 記 ACTIVE 的精確紙上範圍、activation hash、正式 freeze PENDING；一旦 X 存在，不再全稱「未設計任何 K」，改為正式候選未成立並連結 X 清單 |
| 6a-E prereg 首段、§0、§1 firewall、§8／§9 | 不可執行、不得6a-E numerical access，planted 零存在性蘊涵 | 加 E0／X→F handoff 連結；seed／arm／selection／closure 的禁止不變；歷史基準未設計 K 原樣保留，不把 X 當6a-E資格或 power input |
| 理論路線圖 §5、README current progress、handoff v2 current 提示 | amendment 尚待提交／目前禁令／歷史候選材料 | 路線圖連 ACTIVE 範圍；README 與 handoff 加 current 作用域，歷史 §2.3 仍非自行有效的候選材料許可；未批准者不得重新取用 |
| development／amendment logs、接觸帳、未來 formal ledger schema | 三本帳 scope／provisional schema | append X 決策／曝光來源、activation decision-register；歷史列不動，不虛構 candidate attempt／burn，也不宣称 schema 已 Freeze |
| foundations audits／Gate0／索引 | 已證必要條件、物理橋接 OPEN、待修訂 | 只加 current activation 連結；限定定理與 B1–B7／Gate0 OPEN 不被權限決定升格 |

目前 repo 並沒有完成的 `stage5c_confirmatory_ledger.md`；它是 D.1-6 的待交付物。
不能在本案造空 ledger 假裝完成。future 新 prereg 必須對其統計 schema 與全域预算
另作交付。版本衝突時**停止工作**並查 activation／STATUS／operative contracts，
不能自行選較寬鬆的一份。本案不是讓 STATUS 單一句話覆寫所有正式約束。

## 9. 停止、恢復與關閉

| 觸發條件 | 立即處置 | 恢復所需 |
| :--- | :--- | :--- |
| 發現 sealed／禁止 oracle 接觸、來源不明或未記新 exposure | 暫停相關分支、封存版本與接觸 metadata；不再讀 payload 來調模型 | 事故／影響審查、追加接觸帳；排除不掉污染則該分支不得轉原 F |
| X 輸出已用來調 formal core／projector／test-space／margin | 停止舊 formal 資格承重，不以 fresh seed 補救 | §5 的新版 prereg／適當 independent／blinded review；不能回填舊 PASS |
| 證明矛盾、精確反例或先驗 device 語意無法滿足 | 停止相應命題／版本，標限定否定或未決，留失敗依據 | 新定義／前提須新版本，不能加 jitter、刪難例或抹去反例維持原結論 |
| 要超出紙上 scope、動用探索用 RNG／測試新模型／量測／主機 | 停在執行前，提出具名另案；§1.1 有限審查工具分帳 | 操作者授權＋事前審查的方案與適用的執行保護；不能拿 activation 代 receipt |
| 模型只是在重述給定 metric／tick／null legs 而無實現論證 | 不報裝置存在／湧現；將成果限為條件式分析 | 明寫尚缺實現橋接；可另案研究，不保證續做有價值 |
| 找不到可判定問題、超出操作者投入上限，或操作者決定結束 | 暫停／關閉 X；不預設用加錢或加樣本續命 | 操作者另決定範圍；本案不自行設定費用／一週成功承諾 |

關閉不抹去資料暴露或失敗歷史，不使舊資料重獲盲性，不消除任何已消耗的正式預算。
暫停中的 model 不能轉到另一個 ID 繼續同一被禁止的工作。

## 10. Exact-head 複核與決策清單

Claude 複核：E0 是否完整對照所有 current 禁令；paper-only 權限是否可操作；
§2 是否保留 output-only／L4 邊界；接觸盤點是否誠實區分未知與未見；§5 是否防止
seed freshness／改名／projector 繞道；標記升格是否僅對限定命題；停止規則是否留痕。
操作者裁決：批准哪個 exact reviewed 版本、是否只允許紙上、actor 接觸申報是否充分、
以及何時另案做 activation。CI／integrity 不證明隔離成立，GO 不自動啟動模型。

本案依 repo operative 契約起草，不新增承重物理／統計定理，不借外部文獻降低標準。
run1／assessment、witness 2/12／exit137、6a-S 原判決、burn registry、manifest、
程式／tests／CI 全不變；Gate0 OPEN、B1–B7 OPEN、item7 不可 ADOPT、item8 OPEN、
6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING 及現行候選禁令持續有效。
