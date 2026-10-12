# Stage 5C 探索接觸帳：初始盤點與追加規則（草案，未生效）

本帳服務 [探索軌道決策草案](STAGE5C_EXPLORATION_TRACK_DECISION_DRAFT.md) §2–3；
不啟動探索、不授權讀取 sealed artifact，不替代 development／confirmatory ledger，
也不改既有 burn registry。基線 main `87ff77a1a3c44bef4f3c33ade91c3ef0e0623acd`，
tree `91aa84112329bdee017c7d7dddc44a53e1d67afa`。

## 1. 記錄的證據等級與未完成申報

- `REPO-CUSTODY`：repo 原有公開 custody 事實；不表示每位研究者讀過原始資料。
- `READ-THIS-TURN`：GPT 本輪實際讀取的公開文件／metadata／紀錄，程度按 §2 列。
- `OPERATOR-REPORTED-REVIEW`：操作者轉述 Claude exact-head／原包複核，不能當成
  GPT 本輪直接看過原包，更不代表 Claude 所有私人接觸已完整盤點。
- `POSSIBLY-EXPOSED`／`UNKNOWN`：保守風險範圍；未知絕不填作「未接觸」。

目前沒有 actor-complete attestation。操作者／GPT 的跨舊對話接觸、Claude 私人
重現的 exact seeds／fixtures／diagnostics、各人的其他本機檔案與原包接觸仍需本人
或可信舊紀錄補充；本表不能證明任何人 blinded。對缺 manifest 的區段沿用原
development log 的整段 burned，而不是擅造較小精確名單。
未知禁止資料不為盤點而開啟；所有基線 tracked 公開內容先保守列為可能已暴露。
原有接觸不會因 model 改名、換研究者、重新生成或刪除主機消失。

## 2. 初始 inventory（2026-10-12 Asia/Taipei）

下表只索引範圍與限制；原數值／失敗紀錄保留在 source-of-record，不重新轉錄
protected pattern。`NONE` 表示本稿沒有模型，不是宣稱歷史沒接觸。

| Exposure ID | artifact／歷史範圍 | 接觸依據與 actor 程度 | 後續用途與限制 |
| :--- | :--- | :--- | :--- |
| EXP-0001 | 基線 README、handoff v1/v2、STATUS、Stage 1–5 已有理論／plots／analysis／tests；包括既有 BdG／Stage5B 失敗與撤回 | REPO 公開可達；GPT 本輪讀 current STATUS、roadmap 與 handoff v2 相關段；其他歷史內容 POSSIBLY-EXPOSED，非完整重讀 | 公開既有定理／反例按作用域引用；不得把歷史 plots／fixtures 作新 confirmation；handoff 候選材料不因可達而許可 |
| EXP-0002 | DEV-0001–0005：hard-control 搜尋、pool-size／kappa 失敗、replications、效果尺度更正；全部登記 exploratory streams／510–980M 等 pools | REPO-CUSTODY；GPT 本輪讀公開 DEV 列／摘要，actor 個別 raw 接觸 UNKNOWN | burned／development-only；不把 control 的可匹配或 probe evidence 當 order-only K 存在證據；精確 ranges 以 DEV 原列為準 |
| EXP-0003 | DEV-0006／reference probe：48 段 1.1B／1.2B burned、公開 CONTROL-VIABLE、未登記 baseline diagnostics | REPO-CUSTODY；GPT 本輪讀 output-only 條款、公開 outcomes／custody；sealed weights／scores／模式未在本輪開啟；過往 actor 接觸待申報 | 公開 categorical／樣本數／效應／p 的合法範圍不擴大；features／weights／scores／成功模式及 diagnostics 仍不得回流、也不得重算 |
| EXP-0004 | DEV-0007–0010：6a-S pre-execution failures、floor／null-bias／tail-risk；2.6B–3.0B development segments 與 2.7B／2.8B exact ranges | REPO-CUSTODY；GPT 本輪盤點 DEV ID／scope，未新抽樣；external-review actors 與未完整 ranges 依舊記錄保守處置 | 所有既有 burned facts 保留；未知 exact manifests 不縮小 burned 範圍；原 reserved 宣告是各列歷史時點，不能讀成今天仍未用 |
| EXP-0005 | DEV-0011–0015、AMEND-0001：original plus 1.3B PROTOCOL-INVALID、3.1B rehearsal、1.5B replacement plus、1.4B minus、11/11 combined 6a-S PASS | GPT READ-THIS-TURN：公開 incident、burn-registry metadata、log／STATUS 的 categorical custody；四份 raw arm ledgers 本輪未開啟；過往 actor raw 接觸 UNKNOWN | 四組都 burned；raw numerical fields 仍禁止 X；不重判6a-S，不配對舊arm、不由rehearsal pattern取得效果／power |
| EXP-0006 | DEV-0016–0017、joint-law／df-only falsifiers：correct／wrong covariance、df-only review 與低 power 限制 | REPO-CUSTODY；GPT 本輪讀文件公開相關段；Claude 的外部200,000-rep simulation 依DEV原列，exact RNG manifest 不在本帳 | 僅 evaluator calibration／能力邊界，不作真實效果／功效；外部 review simulation 不回充正式資料 |
| EXP-0007 | DEV-0018–0028、E3 wrong-support／typed pairing／certification、近邊界／dyadic／provenance failures、stats regressions | REPO 公開 source／tests／fixtures 可達；GPT 本輪盤點 DEV scope、prereg／acceptance 的公式與 L4 權限；未執行新diagnostic | planted materials／oracle 不能變 X-I construction；既有 deterministic fixtures 不是 formal holdout；失敗原列不覆寫 |
| EXP-0008 | item7 v0.2／training／held-out／fixture bytes／mixtures／subdivision plans、Vultr OpenBLAS preflight failure與修正 | REPO 公開；GPT prior-authored PR records 與 current summary；Claude 依操作者報告獨立重現 OpenBLAS bug，個別私有 witness 待申報 | 只是 runtime／resource development；不提供科學 endpoint law，不再開主機／映像／新diagnostic |
| EXP-0009 | run1 139 outcomes、78 production、34 MODEL-INVALID、INSUFFICIENT-EVIDENCE；evidence／assessment／results | GPT 本輪讀公開結果／hash表；原包曾由 PR作者直接核對與 Claude 獨立核對屬 source-of-record／操作者報告，非本輪重讀原包 | 全部已觀察，不可refit／挑模型／資格化；原包SHA-256 8c26b657…06bf。主機已刪除、映像消失不使 exposure 消失 |
| EXP-0010 | pf3、launch proof／inspect／方法 preflight、receipt／host metadata | Claude 於10/8核對依操作者報告及公開結果；GPT 未直接持有pf3原包；本輪只讀custody | 原包SHA-256 6187e794…f33e；只作來源／執行核對；未取得的私有原包與receipt細節不推測、不再公開 |
| EXP-0011 | PR68 O19／PR69 structural proposal、真實v0.1/v0.2六組atoms×兩theta獨立重現、第一座標近1人工例 | GPT 本輪讀roadmap／STATUS公開證明範圍；Claude重現依操作者報告，人工atoms exact manifest UNKNOWN | O19只限source-bound路徑；飽和觀察不作效果／variance／cap；私有人工例不能默認成新未見輸入 |
| EXP-0012 | witness JSON：12計畫、2結果、對稱chain u=v、exit137/signal9、writer曾修正／重啟、未記錄下一request | REPO-CUSTODY；GPT 本輪讀 metadata／embedded runner／execution note，未重跑；Claude PR69 exact-head複核為操作者報告 | 未完成requests不是結果；不追加預算／換case；kill cause未獨立確證；2筆不支撐O2/O13分布、效果或coverage |
| EXP-0013 | PR70–74：T1/T5、B2/B5、B3/B4、B4/B6 countermodels／proofs與外加幾何／Perlick等有限文獻引用 | GPT authored-history／本輪讀相應current索引與B4/B6段；Claude逐篇exact-head数学GO由操作者提供；文獻全文閱讀不得超過各篇已報scope | 已核對限定解析可引用；不使 B1–B7／Gate0／裝置湧現結案；公開反例及條件式背景已可能影響研究排序 |
| EXP-0014 | 原正式candidate／6a-E保留資料與metadata；尚未完成的item9／runner／confirmatory ledger | 依repo current契約不存在已授權正式6a-E執行；本輪無seed生成、arm讀取或candidate構造；不能替所有私人歷史保證NONE | 未授權資料一律禁止；不列／挑新seed。若事後發現生成或接觸，追加事故與quarantine，不能改原紀錄 |
| EXP-0015 | 本次 PR74 GO／B方向決定、決策草案及接觸帳 | GPT READ-THIS-TURN：使用者提供的Claude複核摘要、B方向及純紙上草案指示；當前X model ID NONE | 方向選擇不等於ACTIVATION；傳給Claude供審時由接收方追加其實際read scope，不由GPT代填 |

上述不把「GPT 讀過摘要」寫成看過全部 raw data。沒有個人完整 attestation 前，不能
給任何特定 fresh／blind 資格；formal handoff 再做完整 claim-specific exposure graph。

## 3. 來源身分快照

以下 Git blob ID 全部取自**上述基線 commit**，不用本草案後改動的工作樹代替。
完整公開 inventory 以該 immutable tree 為界；下列是關鍵 anchors，不是全部已見
資料的聲明。raw包的 SHA-256 與 Git blob 是不同 hash，不能互換。

| 基線 artifact | Git blob ID |
| :--- | :--- |
| [stage5c_development_log.md](stage5c_development_log.md) | `186d9790ad534414750f46106071cf28270b3e49` |
| [stage5c_protocol_amendment_log.md](stage5c_protocol_amendment_log.md) | `765f4e94a918a6bebbbfca5f8855bf886d3d0045` |
| [STAGE5C_D1_3_REFERENCE_PROBE.md](STAGE5C_D1_3_REFERENCE_PROBE.md) | `fda7bb3671bde0c7aaaa79a4a5b0d1a169c01154` |
| [STAGE5C_D1_3_PROBE_RESULTS.md](STAGE5C_D1_3_PROBE_RESULTS.md) | `829a76bb8cb372ef0bc4dd2f850ba0688dffedc9` |
| [STAGE5C_6A_S_EXECUTION_INCIDENT.md](STAGE5C_6A_S_EXECUTION_INCIDENT.md) | `4b717ad0a6442d3dfef2276bda1cc8ae7ca78bb2` |
| [stage5c_6a_s_burn_registry.json](stage5c_6a_s_burn_registry.json) | `74a0299fd251e598beb34293c2f9b0880c2b3368` |
| [STAGE5C_6A_E_JOINT_MATCHED_LAW.md](STAGE5C_6A_E_JOINT_MATCHED_LAW.md) | `6ab327b047fb66ef838fb1efaaa975407a537dc1` |
| [stage5c_e4_v02_resource_fixture_bytes.json](stage5c_e4_v02_resource_fixture_bytes.json) | `2f9b2eb3c3980f17722811a445c957b4cee32ddb` |
| [stage5c_e4_v02_resource_measurement_manifest.json](stage5c_e4_v02_resource_measurement_manifest.json) | `21fc314c0abdbb1b76caa062208e86d0d8b2a2a2` |
| [stage5c_e4_v02_resource_run1_assessment.json](stage5c_e4_v02_resource_run1_assessment.json) | `4a7ab63d069caac9fa880ee24977b5659db3b4ff` |
| [stage5c_e4_v02_resource_run1_evidence.json](stage5c_e4_v02_resource_run1_evidence.json) | `cd9f35d56028e9f1912033e55365b6c731dba400` |
| [stage5c_e4_v02_resource_run1_results.json](stage5c_e4_v02_resource_run1_results.json) | `8407f6213b5add567bc82c0d7058e3593b6b2c03` |
| [stage5c_structural_coordinate_design_witnesses.json](stage5c_structural_coordinate_design_witnesses.json) | `e1d18ba1ec5ff74ba19e93ffef89c77b481ee054` |
| [foundations/b4_b6_clock_rod_signal_record_realization_audit.md](foundations/b4_b6_clock_rod_signal_record_realization_audit.md) | `aa01fa2ba48becd04736ecbbeb05f297294ad61a` |

## 4. 生效前 actor 申報與未來追加格式

| Actor／角色 | 現有已知範圍 | 待申報／未知 | 当前資格 |
| :--- | :--- | :--- | :--- |
| 操作者 | 轉交原包／assessment、執行與review摘要；主機刪除依公開結果 | 個人已開啟raw檔案、私人notes、舊對話與未記diagnostics的完整範圍 | 不宣稱未見／blinded；生效前需補 scope |
| GPT／作者及舊對話代理 | 公開repo、已合併PR的作者紀錄；本轮 §2 READ／摘要 | 跨對話實際raw接觸、scratch中舊artifact及未在repo保存的診斷manifest | 本輪不是actor-complete attestation；按public baseline可能暴露隔離 |
| Claude／獨立數學reviewer | 操作者報告的PR67–74、原run1／pf3及real-producer／人工例核對 | 私人重現的exactinputs／streams、完整文獻／raw接觸与影响 | 可核對數學不等於blinded criterion角色；不能由GPT保證blind |

此表是 pending 申報，不要求為證明「沒看過」去新開檔案；由actor以可回溯紀錄聲明
有界scope與未知項，對未知採保守隔離。補充原entry用追加更正，不覆寫上述初盤。

每個新entry用以下欄位（本稿不虛構尚未發生的探索／activation）：

| 欄位 | 必須記錄 |
| :--- | :--- |
| ID／時間／actor | 唯一EXP-ID、UTC／台北日期、作者／reviewer／custodian角色 |
| 來源／內容程度 | path／commit／blob或SHA-256、取得途徑、public／sealed、metadata／categorical／numeric／raw／incomplete；未知明寫UNKNOWN |
| 資料血緣 | law／split／seed range／generator identity、原EXP／DEV／burn record；無資料寫NONE，不用未生成的seed佔位 |
| 影響 | X problem/version/source hash、看到前後的模型／criterion決策；未採用／失敗也列 |
| 隔離／回用 | output-only／禁止回流／burned／quarantine／formal eligibility、誰複核、補充哪些缺口 |

更正、撤回、轉交、誤接觸皆append；不保存被禁止payload／私人ID，只記可核對
custody metadata。新X模型決策仍另進development log；formal揭露仍另依正式帳本，
不能靠本帳「已登記」變成合法或免除budget。此帳合併後也不是生效批准。

## 5. Actor 自行申報追加（2026-10-12；初盤不覆寫）

本節以申報人原文和有界scope補充 §1–4；舊 UNKNOWN 不刪，亦不將原 actor-specific
事實改成GPT的獨立核對。§4是初盤歷史，現在申報狀態以下表為準。

| 新EXP-ID／actor | 來源、hash與本次實際接觸 | 影響／隔離／資格 |
| :--- | :--- | :--- |
| EXP-0016／Claude | [actor自行申報原檔](claude_exposure_declaration_2026-10-12.md)，操作者2026-10-12轉交；SHA-256 `20f79f3b3ad0201dc42c9dab4d68f696543560ebf663f11c9465a7a62b1edb23`，與附件逐位元一致。A公開文本／code；B五包resource／execution；C1人工atoms的v0.1/v0.2 E4矩陣與endpoint；C2 witness欄位；C3 run1重播；C4規劃；C5review spot checks；C6匯入失敗；D文獻；E影响。 | 補充EXP-0003、0006、0008–0013的Claude scope，**由Claude申報、未由GPT重建raw或atoms獨立驗證**。C1含endpoint，與B的資源包無endpoint申報分開；不能因此把整份申報寫成「無endpoint接觸」。本工作階段以前UNKNOWN、無blinded資格。 |
| EXP-0017／GPT | [GPT有界自行申報](gpt_exposure_declaration_2026-10-12.md)：可回溯current文本／工具、#75文件起草／測試／合併、本次禁令查找與Claude原檔讀取；沒有據C1重建atoms或跑新producer。跨舊對話raw／私人歷史UNKNOWN。 | 收到Claude申報後GPT也已見人工E4配置與endpoint範圍，不能說未見此觀察。沒有新model ID／模型構造；未知保守隔離，不代替其他actor。 |
| EXP-0018／操作者pending／GPT current接收 | 操作者轉交Claude原檔與#75核准／未生效決定，證實本次transfer；**不能推定操作者已開啟任何特定raw包／endpoint**。 | 操作者下載／轉交／terminal／raw／舊對話的本人申報仍PENDING，尚無actor-complete scope。留待其自行提供，記不清楚者UNKNOWN；不提交activation。 |

Claude C1 申報用人工 fixture atoms、RNG0、均勻擾動、正規化mix、两theta呼叫E4，
看過完整矩陣、第一分量約0.34–0.9999999、第二分量0，非selector／target-law樣本。
這是已見 evaluator 行為，不承重O2/O13一般分布／variance／cap／power；日後若X-I
以第一分量行為設計，必須引用EXP-0016/C1、檢查回流並暫停未釐清分支。
原檔說exact atoms可重建是actor說明，GPT本次**未重建、未宣稱已獨立恢復精確manifest**。

五份原包的完整讀取與「無scientific endpoint」範圍由Claude申報，GPT本次只讀申報。
原檔partial hashes維持原文，不補猜成full SHA；run1／pf3已存在的full hashes仍在原
source-of-record。宣告不保留跨工作階段記憶，不能据此取消以前DEV／review的暴露風險。
Claude讀Nicholas的範圍、未讀Anker–Ziegler及本階段未直接讀BHS／Perlick，依原文保存；
repo曾有作者讀原文紀錄，不等於Claude自己已讀。獨立數學GO仍不等於blinded criterion資格。

| 目前actor申報狀態 | 已有材料 | 仍待處理 |
| :--- | :--- | :--- |
| Claude | 本工作階段的本人A–E申報已收存 | 階段以前UNKNOWN保守隔離；新接觸append，不能承諾blind |
| GPT | 目前可回溯工作範圍的本人申報已保存 | 舊對話／私人raw UNKNOWN保守隔離；不是全歷史attestation |
| 操作者 | 本次transfer與決定已記，尚無本人接觸清單 | 自行列下載／轉交哪些包、terminal看過哪些輸出、是否打開raw、其他舊對話；不確定填UNKNOWN |

本補充仍待exact-head複核。申報收件不自動判定所有分支可用、正式資料fresh，
或activation條件已滿足；三方scope／未知隔離仍须依決策草案逐項審查。

## 6. 操作者本人申報追加（2026-10-12 02:39:47 Asia/Taipei）

本節補充 §5 的收件前 PENDING 狀態，原 entry 與歷史表不覆寫。

| 新EXP-ID／actor | 來源與實際申報 | 影響／隔離／資格 |
| :--- | :--- | :--- |
| EXP-0019／操作者；GPT 接收文字與截圖 | [操作者有界申報](operator_exposure_declaration_2026-10-12.md) 保留本人原句；截圖可辨識 `vultr_stub_evidence.tar.gz`、`pf3-evidence.tar.gz`、`run1-evidence.tar.gz`、`vultr_campaign_image_v1.zip`。本人申報已下載、沒有打開 raw 檔、其他不知道。GPT 僅核對截圖檔名，未開包或驗證下載副本 hash。 | 下載不等於內容閱讀；未開 raw 是本人聲明，不延伸為未見摘要／終端／endpoint。其他接觸 UNKNOWN，既有確知 transfer 保留；不推定 zip 與舊 image tar.gz 相同。本輪沒有新模型或 criterion 決定；新接觸仍追加，未知保守隔離，不授予 blind／fresh 資格。 |

操作者的有界本人申報現已收存；GPT 也已讀取此申報及四個檔名的截圖。
三方皆有本人有界申報，不表示完整歷史已知或隔離審查通過。終端畫面、其他 raw／私人
材料、舊對話等未知項不要求以新開檔案消除；依協定保守處置。
本次是申報紀錄更新，仍待 PR #76 exact-head 複核；沒有 activation 或候選構造許可。

## 7. PR #76 複核與操作者已知接觸追加（2026-10-12）

PR #76 head `450a7cfdd9c6a844a9dd08993ea8f7d196ab440d`、tree
`4c198ce75bfee1f92fb59e417b75ba116bdc9c12` 已獲 Claude exact-head GO，依操作者
轉交的批准原 head 合併為 main `8d16f9b2ccbbcd74d727694b2770024a91f30616`，
merge tree 相同，狀態仍 REVIEWED-NOT-ACTIVE。§5–6 的收件／待審是當時狀態，原文保留。

| 新EXP-ID／actor | 來源、程度與補充已知範圍 | 影響／隔離／資格 |
| :--- | :--- | :--- |
| EXP-0020／操作者歷史接觸；GPT 本次接收 reviewer 補充 | 操作者 2026-10-12 09:09:08 Asia/Taipei 轉交 Claude 的 PR #76 複核文字。詳見[操作者申報追加](operator_exposure_declaration_2026-10-12.md)：已轉交 audit JSON、managed-session bundle、stub v1、image v1 zip、stub／campaign-image-evidence／pf3／run1 四類證據包；已透過截圖／貼文看過 run1 最後 stress 計時与 PLAN-COMPLETE（依補充無 endpoint）、preflight PASS JSON、image smoke JSON、stub PREPARED／STARTED。 | 已知轉交／部分終端閱覽補充 EXP-0018–0019，不再僅作 UNKNOWN；不推定開 raw／完整 records、包副本身分或 sealed 數值。其餘未知仍隔離。GPT 僅讀補充、未新開包或重播；未構造模型或調整 criterion，不聲稱 blind／fresh。 |

這是操作者提供的 reviewer 接觸紀錄補充，不由 GPT 代寫新的全歷史本人保證。
若有具體更正，另 append；不覆寫原申報、接觸帳或 burn。收件與 PR #76 GO 不等於
探索 activation；本次沒有決定啟動，也未選 B4／B6 實現目標。

## 8. 操作者僅紙上啟動批准（2026-10-12；activation 待審合併）

| 新EXP-ID／actor | 來源／接觸與決定 | 隔離／生效範圍 |
| :--- | :--- | :--- |
| EXP-0021／操作者；GPT 接收與起草 | 2026-10-12 09:46:37 Asia/Taipei（UTC 01:46:37），操作者原句「啟動」，承接前述 ACTIVE-PAPER-ONLY 選擇。GPT 讀取此决定及公開禁令／受審規則以作文件同步。具名 [ACT-X-0001](STAGE5C_EXPLORATION_ACTIVATION.md)，權限來源為 PR #76 exact head；#77 事實補充仍同交新複核。 | 原 UNKNOWN／禁回流／burn 不解除；未使用私人或 sealed payload。核准 activation 合併 main 才生效，批准不授權提前構造。X model ID NONE，無 target 選擇、seed、主機、量測或 formal attempt；不声稱 blind／fresh。 |

本帳舊列全部保留；未完成的 raw／私有歷史不由「啟動」變成完整或可用。
生效後每次新接觸／模型選擇照原规则 append，正式披露另走其帳，不以此規避 spending。
