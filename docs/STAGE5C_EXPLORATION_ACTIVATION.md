# ACT-X-0001 — 僅紙上探索的批准與 activation 記錄

本記錄是**activation PR 的生效條件**，不是先行執行的憑證。它只在本 PR 的 exact
head／tree 獲 Claude 獨立複核、且核准內容合併到 `main` 後成為
**ACTIVE-PAPER-ONLY**。在分支、draft PR 或未核准版本中仍為 **NOT-ACTIVE**。
一般文件 PR 的 merge、CI 綠燈與草案 GO 不啟動本軌；此處特指經核准的 activation merge。

## 1. 操作者批准、受審版本與實際生效身分

| 欄位 | 記錄 |
| :--- | :--- |
| 決策 ID | `ACT-X-0001` |
| 操作者原句 | 「啟動」 |
| 批准時間 | 2026-10-12 09:46:37 Asia/Taipei；UTC 2026-10-12 01:46:37 |
| 批准範圍 | 前述對話具名的 `ACTIVE-PAPER-ONLY`；批准起草 activation PR 並送 exact-head 複核，合併前不開始構造 |
| 已審核的權限來源 | PR #76 head `450a7cfdd9c6a844a9dd08993ea8f7d196ab440d`、tree `4c198ce75bfee1f92fb59e417b75ba116bdc9c12`；原樣 squash main `8d16f9b2ccbbcd74d727694b2770024a91f30616` |
| 條款來源 | 該受審 tree 的 [決策草案](STAGE5C_EXPLORATION_TRACK_DECISION_DRAFT.md) §1–6、§8 E0、§9 停止條件；不是依日後任意修改的同名檔取得擴張權限 |
| 接觸補充 | 本 PR 包含 PR #77 head `023e18a0a844614ac9d79ba54b443744b48ac54d`／tree `7ea3f4e7c2dc531f0af8ee339602d335fcadd077` 的事實性 EXP-0020；該補充與本 activation 同交新 exact-head 複核，不稱已由 #76 GO 核准 |
| activation 的 exact head／tree | 以本 activation PR 的最終獨立 GO 所具名 head／tree 為準；目前未取得，不能用一般草案 GO 代替 |
| 生效 commit／時間 | **首次把該核准 activation tree 合併到 main 的 commit 與 Git committer 時間**；不得使用批准時間或分支 commit 時間倒填。合併前不存在已生效 commit |
| 首次研究開始前 | 從 main 取得上述 merge SHA／tree，核對與 GO 相同，將 SHA 記入首次問題契約及接觸／決策追加紀錄。找不到證據或文件衝突即 NOT-ACTIVE／停止 |

commit 無法包含自己的 hash；因此 ACT-X-0001 是文件中的穩定識別碼，**不是**
用來替代 Git SHA 的任意別名。所有 E0 引用指向同一記錄；只有可回溯至獨立 GO
及 main merge 的那個 activation commit 有效。後續 PAUSED／CLOSED 或實質修訂須
另案記錄，不能只引用歷史 ACTIVE 繼續工作，也不能追認批准前的模型構造。

## 2. E0 — 統一作用域條款

> Freeze-1a 完成前，原 Stage 5C 正式候選資格與 confirmatory evaluation 仍不得開始。
> 僅已生效的 X 探索軌道可在其紙上範圍內設計探索模型／探索 K；這些不是正式
> 候選，不產生 scientific PASS，不修改任何正式 gate／core，不授權資料或執行。
> X 權限、來源隔離、接觸帳與回到正式驗證的條件以具名 activation commit 為準；
> 沒有 ACTIVE 記錄，沿用原 Freeze-1a 前全面候選設計禁令。

E0 只調整「正式 freeze 前一律不得設計」的時序範圍；**不**豁免本文以下限制或
各 evaluator 的 output-only／禁止資料／no-oracle／candidate-independent 條款。
被探索影響的 mapping／core／projector／test-space／margin 不能仍聲稱候選獨立，
也不能只把「候選前」改成「正式候選前」來延用舊資格。

## 3. 有效時的紙上權限與執行邊界

| 類別 | 允許的紙上工作 | 限制 |
| :--- | :--- | :--- |
| X-I | 另軌文件中的 order-only 模型、探索 K 的定義／材料／參數化、解析存在性或 no-go | 明列 L0–L3、容量、非 canonical 選擇及來源；不是 F 候選，不進 C0–C11 評測 |
| X-C | 明示背景、度規、邊界、狀態／物質前提下的鐘、尺、訊號模型與解析性質 | 每個新 primitive 都是條件式前提；不稱由 L0 湧現、不改原 S5C-Claim 或 3+1D firewall |
| 解析比較／撤回 | 文件中的有限 toy 定義、精確反例、符號推導、具名文獻的條件分析，保存選擇與失敗版本 | 不執行 toy ensemble；文獻承重須 convention／適用域 mapping；有限例不證典型性 |

沒有授權新的程式模型、模型探索／篩選用 symbolic／toy 執行、研究 RNG／seed、
selector／E4 witness、抽樣、量測、雲端主機、消費、receipt、正式 runner／arm 或
scientific PASS。這些都需另案具名計畫、預算、來源隔離與事前審查／授權。

原決策 §1.1 的有限 review-only numerical／symbolic／review RNG 可檢查**已寫出**的
具名固定命題及前提；先固定 source version、有限 cases／draw policy、算法、精度與
資源邊界，記錄全部嘗試。它不證普遍性、coverage／power 或裝置實現。
審查不呼叫新 causet、selector、E4 producer，不讀禁止資料或重算 probe。
若結果用於新的模型／參數／criterion 選擇，即停止回用，先記曝光與決策，再另案
授權所需執行；歷史 Claude 人工 E4 接觸仍屬 evaluator-development，不倒改。
既有 regression suite 只作 repo 檢查，不是新科學樣本或正式 attempt。

## 4. 來源隔離與三方有界申報

申報來源為 [接觸帳](stage5c_exploration_exposure_log.md) EXP-0016–0020、
[Claude 原申報](claude_exposure_declaration_2026-10-12.md)、
[GPT 申報](gpt_exposure_declaration_2026-10-12.md)、
[操作者原句與追加](operator_exposure_declaration_2026-10-12.md)。
原 Claude 檔 SHA-256 為 `20f79f3b3ad0201dc42c9dab4d68f696543560ebf663f11c9465a7a62b1edb23`。
三方有界申報已收件；沒有全歷史完整或 blind／fresh attestation。

- 6a-S 四份 raw arm ledgers／數值，reference probe sealed features／weights／scores／
  有效模式、post-hoc diagnostics、未揭露 formal holdout／保留資料仍禁止
  X 使用；不能以摘要、轉換、公開 seed 重算或 lookup 繞過。
- 正式／planted evaluator 的 L4 payload、support mapping、gamma／metric／target
  不作 X-I 的設計／調整輸入；不執行 probe／control generator 取得構造材料。
  X-C 可以在獨立條件文獻或明寫公理下給定通用背景，但不能開 sealed／抄成功模式。
  若受已見 evaluator 內容影響，記為 evaluator-informed conditional branch，禁止
  轉成原 S5C-Claim 構造；其條件式意義只能另立主張／新版 prereg 審查。
- 只用原決策 §2 已允許的公開解析／合法 development 材料；burned 不解除禁回流。
  planted 控制與 oracle 可達，不代表可拿來構造模型。
- Claude 人工 E4 endpoint、witness 2/12、run1 outcomes／stress 結果均已暴露，不能
  稱新確認或用來 refit／挑模型／cap。任何受第一分量觀察影響的分支都須引用
  EXP-0016/C1、0017 及相應血緣，先釐清回流；無法排除即暫停。
- 舊工作階段／私人材料未知保留 `QUARANTINED-UNKNOWN`；公開基線保守視為可能
  已暴露。申報收件只完成有界來源紀錄，不准任意使用未知材料；受其影響的分支
  在釐清前不得開始／繼續，不能以更換 ID 續行。
- 操作者未開 raw 的本人申報與已看部分終端截圖分開；轉交不推定已讀內容。
  不為清除 UNKNOWN 新開禁止包或重放 producer。

每份新問題契約先列研究 ID、命題／定義域、輸入前提、證據、未證橋接、否定條件、
後續驗證，附 actor／來源／接觸依賴及 active SHA。每次新接觸、模型選擇、失敗、
撤回皆 append；未知隔離的審查是 claim-specific，不能靠本記錄一概判定污染已消除。

## 5. 標記、正式軌道與停止規則

模型及選擇標【探索】，未有支持的想法標【提案】。完整證明／精確反例經獨立
exact-head 複核只升格具名命題的限定解析結果；物理實現／湧現／未證橋接不升格。
X 永不產生 scientific PASS、C0／6a-E PASS、item7 ADOPT 或 Freeze 完成。

回 F 須另案 handoff，逐項遵守原決策 §5：主張與 provenance／capacity／oracle 審計、
D.1 九項及 closure mapping、完整 candidate／evaluator／estimand／law／matching／
gate／margin／power／failure／資源／spending freeze、真正 fresh 資料與另授權執行。
若探索影響 core／projector／test-space／margin 等，舊資格不沿用；須新版 prereg、
exposure mapping、external／mathematical justification 與合資格獨立／blinded review。
換 seed 不補救 criterion 污染；core 不可放寬、holdout 一次揭露、burn／spending 繼承。

禁止來源／未知回流、criterion 污染、精確反例、scope 超界、沒有實現論證，或操作者
要求停止時，依原決策 §9 暫停／關閉相關分支、封存版本與紀錄；恢復需具名審查。
Gate0／B1–B7 OPEN、item7 不可 ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、
Freeze-1a PENDING 與既有科學結果／數值契約不因 activation 改變。

## 6. 同步驗收與下一步

[逐文件同步驗收](STAGE5C_EXPLORATION_ACTIVATION_SYNC_AUDIT.md) 對原禁令定位的每一
來源列 E0-scope／KEEP／HISTORY、基線 blob 與 diff 處置。正式規格實質時間條款須
改為 E0 作用域；禁止資料、core、controls、舊審計證明與歷史快照不改寫。
任何新發現限制仍須追加審查，不能以 keyword 計數當完整性證明。

本記錄不占 AMEND-0001 的 implementation scope，不建造空 confirmatory ledger，
不虛構 DEV 科學結果、candidate attempt 或 burn。權限決策、接觸、模型決策及正式
attempt 各帳分開。實質權限擴張須新版本與獨立複核，不能只改此檔原地生效。

本次 **X model ID NONE、實現目標尚未選定**。生效後由操作者從 B4／B6 選一個
目標（tick／signal response／rod comparison），再寫只定問題的契約；本 PR 不選
算子形式、不指定 order ansatz／weight／phase，不構造模型。

## 7. 生效核對與首個目標追加（2026-10-12）

前述「尚未取得 GO／未選目標」是 activation PR 提交時點。其後操作者轉交 Claude
對 PR #78 head `69e57e4183792c02ba17615b1afce89ee2c71e57`、tree
`c8e4e6ffae89718f77cc70431423244b88b53e79` 的獨立 GO；CI #255 為
556 passed／5 個既有 warnings，integrity 通過。

原 head squash 合併 main **`0c386716701589c9a6b0b799636a808aacb9ade5`**，
merge tree **`c8e4e6ffae89718f77cc70431423244b88b53e79`** 與核准 tree 相同。
Git committer 時間為 **2026-10-12 09:57:23 UTC／17:57:23 Asia/Taipei**；
這是 ACT-X-0001 的生效 commit／時間，現為 **ACTIVE-PAPER-ONLY**。
後續工作引用此 immutable SHA／E0；本次事實性追加不是新的 activation，亦不擴張權限。

操作者在本輪選擇「訊號回應」。首份交付為
[X-SIGNAL-RESPONSE-P0.1 問題契約](foundations/signal_response_problem_contract_v0_1.md)，
只定問題、不構造模型，另交 exact-head 複核。Problem ID 不是 model ID；model ID
仍為 NONE。tick／rod comparison 未加入，資料／執行限制與所有 OPEN 義務不變。

## 8. 問題契約定案後的模型登記（2026-10-13）

PR #79 r3 核准 head `ea48729578941cf6938699a9d2fe6698989a7398` 原樣合併 main
`ac2226ee08a8babf71e326a7aabcd71388e24515`，tree `312e3142add7460ddeab129bc8c090bf4b8f1f7e`
與 GO 相同；CI #259 為556 passed／5既有warnings。契約此時定案，ACT-X-0001
生效身分仍是 `0c386716701589c9a6b0b799636a808aacb9ade5`，不是這個後續文件merge。

其後才構造 [首份 X-C 紙上研究](foundations/conditional_delay_relay_signal_study_v0_1.md)：
`X-SIGNAL-DELAY-RELAY-v0.1` 與限定負模型 `X-SIGNAL-BEACON-CONTROL-v0.1`，待獨立
解析複核。前節 model ID NONE 為模型前歷史，現在已存在紙上模型；仍未有正式候選K。
這是原有 ACTIVE-PAPER-ONLY 範圍內的工作，不擴張 E0／formal／資料／執行權限。


## 9. PR #80 限定複核與 C2 目標追加（2026-10-13）

Claude 核准 PR #80 head `f1017f88f94d2c4c10f6af7d8ce89b6a08650dc7`／tree
`429da9a1282369b3b6039fdf53d4e74119546177`；CI #261 綠（556 passed／5既有warnings、
integrity通過）後原樣合併 main `0f88bf2e46e0864bdffba865e81eeefce0cc428f`，tree相同。
ACT 生效 commit 仍是 §7 的 `0c386716701589c9a6b0b799636a808aacb9ade5`。
在 C1–C6 與 H≥T 子域，主模型滿足 r3 及獨立信標無串接的解析結果限定已確認；
不升格物理實現、湧現或 formal 科學判決。本人 review-only 窮舉申報原句見 EXP-0029。

操作者本輪另選 C2 因果傳輸；[支持問題契約](foundations/causal_transport_c2_problem_contract_v0_1.md)
只定問題、待 exact-head 複核，不構造新模型／law／反例。本問題 model ID NONE；
原兩個紙上模型仍存在。E0、資料與執行限制、停止規則及回 F 條件均不改。


## 10. C2 原題退回與方向1追加（2026-10-13）

PR #81 r1 head `02645caed8bfbb98ca89fdc19c94c4fa22c33d9e`／tree
`6d4436e75f1ffc979f9e7b1816656f9438028630` 未 GO、未合併。§9 的待審原題是
該時點紀錄；Claude 提出星形反例，P0.1 限定否定與來源保存在原稿尾部。
操作者選方向1；[P0.2 契約](foundations/causal_transport_c2_problem_contract_v0_2.md)
只固定文獻參照／背景、目標、參數與量詞，另待 exact-head 複核。
沒有構造新模型、求解傳播子或執行；本問題 model ID NONE，不改原兩模型。
ACT生效仍 `0c386716701589c9a6b0b799636a808aacb9ade5`，E0／formal／資料及執行
限制全保留；本次不是新的activation，也不取得科學PASS或量測授權。


## 11. P0.2定案後的文獻核實例與M／V研究（2026-10-13）

Claude對PR #81 r2 head `b0f53948747e8770f79519396d5bce1ebbee03c6`／tree
`3e415ff465eb08ff9c75724ee1d8e7678f579d00` GO；CI #264綠（556 passed／5既有
warnings、integrity通過）後原核准tree合併 main
`c5bc9c6533f34c3121f793e68e3710cc9f67f6e5`，tree相同。契約此時定案。
ACT生效身分仍 `0c386716701589c9a6b0b799636a808aacb9ade5`，不是這份後續merge。

定案後才交 [X-C2-LINK-MV-v0.1 紙上研究](foundations/c2_johnston_link_mv_study_v0_1.md)，
具名參照實例 `X-C2-JOHNSTON-LINK-v0.1`：固定文獻無質量link核，沒有新權重，
提出M與V完整短證明／界，待獨立exact-head。前節model ID NONE為問題前歷史，
現在有此文獻核紙上實例；原兩模型保留，正式K未構造，沒有執行或scientific PASS。
本追加不改E0、formal、資料／執行限制或停止／回F規則。


## 12. PR #82 限定解析核准與 P0.3 問題追加（2026-10-14）

Claude核准PR #82 head `1e067c63e34e9afa8909f6604698beeff8b1f80e`／tree
`3b53b07af0691de2b2d19056afc17469b698761b`，CI #266綠（556 passed／5既有
warnings、integrity通過）後原樣合併 main
`f43762f2917a3b2ce86782d1b4de033b2075da3f`，tree相同。
merge Git committer UTC 2026-10-14 01:50:55／台北09:50:55；
這不是activation，生效SHA仍 `0c386716701589c9a6b0b799636a808aacb9ade5`。
前節待審是歷史；現僅確認固定來源augmented-endpoint Lebesgue M／V及機率收斂，
不確認原生點讀值、物理訊號／器件／物質或L0湧現，formal OPEN不改。

承接操作者轉交的reviewer建議，追加[P0.3問題契約](foundations/causal_transport_c2_problem_contract_v0_3.md)。
僅固定同一Π的原生接收點求和、既有核／權重、ρ⁻¹及M_D／V_D量詞，待exact-head；
不開始推導、新構造或執行。本問題新model ID NONE，既有三個參照／模型ID保留。
本人申報與作者來源見EXP-0035–0036；不改E0／formal／禁止資料、停止／回F條件、
seed／producer／主機／量測限制或原r3。


## 13. P0.3定案後的原生點M_D／V_D登記（2026-10-14）

Claude對PR #83 exact head `7271b215ab630b6b892ddc9886aab974b40a272c`／tree
`aa53f2b1111064f6fc0efd0815576eefd956b1ce` GO，CI #268綠（556 passed／5既有warnings、
integrity通過）後按原核准tree合併main
`8a8524cdfdd34934d629547449c92d0668a34cc6`，tree相同。
Git committer UTC 2026-10-14 03:26:52／台北11:26:52；P0.3此時定案，
前節未定案／不開始推導為歷史。ACT生效commit仍
`0c386716701589c9a6b0b799636a808aacb9ade5`，本次不是activation或權限擴張。

合併後才交[X-C2-NATIVE-MV-v0.1紙上研究](foundations/c2_native_detector_mv_study_v0_1.md)，
Readout ID `X-C2-NATIVE-READOUT-v0.1`，原核仍 `X-C2-JOHNSTON-LINK-v0.1`。
現在有具名讀值實例，不再把本輪全部實例稱NONE；沒有新kernel／物質／裝置law。
M_D／V_D新解析待exact-head，屬校準延伸，不確認器件、r3回訊或c／L0湧現。
來源見EXP-0037–0038，原本人申報／UNKNOWN／禁止資料保留；E0／formal／seed／
producer／主機／量測限制、停止／回F條件、原r3與全部OPEN不改。


## 14. PR #84 原生點校準求和的限定複核（2026-10-14）

Claude核准exact head `577ea0e3ab687f39b820ee895c59ee5659cee250`／tree
`1ddfc5fda603985712fe9eb41e644db4b39d32f7`，CI #270綠後原樣合併main
`8839df0eb8bff88dd6e040b8c81ee60117932445`，tree相同；556 passed／5既有warnings、
integrity通過。Git committer UTC 2026-10-14 05:14:55／台北13:14:55。
前節待審是提交時點；現在只限定確認定案P0.3原生點校準求和的M_D／V_D與機率收斂。
物理詮釋仍探索，不確認器件／r3回訊、c／L0湧現或formal資格。

ACT生效commit仍 `0c386716701589c9a6b0b799636a808aacb9ade5`，本次不是activation，
不改E0、formal／禁止資料、停止／回F、seed／producer／主機／量測限制或原r3。
本人申報及作者文件scope見EXP-0039–0040；全歷史UNKNOWN保留。
原生點研究只更新審核狀態／追加記錄，原契約、全部證明／公式不改；
本次沒有新研究、構造或執行授權。


## 15. 方向1的問題契約登記（2026-10-16；未擴張權限）

#85已原核准tree合併main `f1a33070cf1c3bc1153e870e12cb34993ca92069`；
其後申報鏈4cd99590→34bfd9a0併入本交付，舊帳不覆寫。
操作者本輪明示選定「r3回訊與C2串接」，時間與本地版本批准者分開記在接觸帳§21。
新增[X-C2-R3-BRIDGE-P0.1問題契約](foundations/c2_r3_response_bridge_problem_contract_v0_1.md)，
只固定待檢驗的雙段原生點泛函、共享Π、外加線性回應與零輸出替換、完整紀錄及量詞。
這些介面是GPT的待審規格，不是物質實現或已證的r3回訊；不自動轉用P0.3方差界。
本問題尚無新的具名完整裝置實現；既有模型／核保留，沒有新矩／極限推導。

申報EXP-0045全文未取得，保留PENDING-VERBATIM，不能代填；EXP-0046為作者scope。
契約PR維持draft，須補齊本人原句並取得exact-head GO後才可合併、開始下一份紙上研究。
ACT-X-0001生效SHA、E0、formal／禁止資料／UNKNOWN、停止／回F與執行限制不改。
未授權RNG、撒點、新數值／符號診斷、producer、seed、主機、量測或receipt。


## 16. EXP-0045原句收錄（2026-10-16；權限不變）

操作者於台北15:19:00／UTC07:19:00轉交Claude對紀錄commit34bfd9a0的完整本人申報。
接觸帳§22已逐字追加為原保留ID EXP-0045；前節及§21的待補描述保留為歷史。
本人事前沒有批准本地版本，不影響操作者事前批准的事實；此申報不等於PR #86複核GO。
僅解除原句待補項，EXP-0047登記作者同步scope；問題契約仍待新exact-head複核與CI。
ACT生效SHA、E0、所有formal／資料／執行限制不變，不授權開始推導或任何科學執行。


## 17. PR #86 r1未GO與r2方案b（2026-10-16；權限不變）

Claude對r1 head9dd6710e／tree4660f45e未GO，要求在推導前校正四項law差異的地位。
操作者本輪明選方案b；[問題契約r2](foundations/c2_r3_response_bridge_problem_contract_v0_1.md)
把四項只記為介面構造下成立，另固定單次判定a>gC/2及最壞誤判機率趨零目標。
不改原核／回應介面／泛函／M／V量詞；補明r3配對可識別性、穩定性／failure OPEN，
本題不報時間或延遲。r1原head與未GO理由保留，沒有開始矩／極限或單次判定證明。
本人申報EXP-0048及作者修訂scope EXP-0049只追加於接觸帳§23。
這次操作者選b不是r2 exact-head GO；仍須獨立複核與CI後才可合併。
ACT生效SHA／E0、formal／資料隔離、停止條件及全部執行限制均不改。


## 18. PR #86 r2定案與具名共享配置研究（2026-10-18）

Claude對head b4e3deb1／tree435fc3e8給GO，CI #276 success後原樣合併main
`7bc202b586167ac2eb15a12a8846ec59e90d2a9f`，tree與核准版本相同。
Git committer UTC 2026-10-18 15:34:54／台北2026-10-18 23:34:54；契約此時定案，舊待審列保留為歷史。
ACT生效commit仍0c386716，本次不是activation或執行／formal權限擴張。

新增[X-C2-R3-SHARED-MVPD-v0.1](foundations/c2_r3_shared_mvpd_study_v0_1.md)，
Readout ID X-C2-R3-RELAY-READOUT-v0.1；同一契約介面與泛函，不換核、窗口或判準。
新稿補良定性及M／V／P／D的紙上證明，全部探索／待exact-head，不先升格或稱物理回訊。
EXP-0050本人申報、0051作者來源與合併前已有紙上策略推理的時間偏差，只追加於接觸帳§24；
不把具名文件合併後建立說成所有推理都在合併後，留待reviewer判斷。
原契約、r3／P0.2／P0.3、既有證明、formal／資料／執行限制與停止條件不改。


## 19. PR #87原樣合併與限定解析確認（2026-10-19；權限不變）

操作者於台北14:00:20／UTC06:00:20轉交Claude對head
`924c90c1bb89d887fd140d3795c6bec147c6f865`／tree
`e7d4c476e762d2b091c010e5f2d8a19269ed1233` 的exact-head GO。
CI #278 success後原樣squash為main `6cd3eb4386582eb80e528b631673b6b8aebca647`，
tree相同；Git committer UTC06:00:56／台北14:00:56。
[X-C2-R3-SHARED-MVPD-v0.1](foundations/c2_r3_shared_mvpd_study_v0_1.md)限定升格為
【已確認／定案共享配置雙段讀值（外加線性介面）的M、絕對V、P與單次判定D】；
物理詮釋、r3配對可識別性／穩定性與器件實現仍OPEN。

本人申報EXP-0054與作者同步scope EXP-0055只追加於接觸帳§26。
公開推送批准人是操作者，Claude只作預讀及後續複核；舊本地commit未公開，
不能把上傳檔比對說成外部直接驗證了本地tree；原時間偏差及reviewer不阻擋裁定並存。
本次不是activation，不改E0、生效SHA、formal、禁止資料／UNKNOWN、停止及回F條件。
沒有新研究選題、模型／窗口／權重／判準、新推導或任何科學執行授權。


## 20. PR #88定案、T2＋T3選題與只定問題（2026-10-19；權限不變）

操作者於台北14:46:13／UTC06:46:13轉交#88 GO；核准head
`bde2ca038b0170692048fc0ee04528b8f933e6cf`／tree
`06bae466a0c3b71551664c994a260fec63f51ef9`，CI #280 success後原樣squash為main
`b80ef2fd566ffabb43b5a77581087ef37938ebc7`，tree相同；
Git committer UTC06:47:32／台北14:47:32，不是新的activation。

操作者另於 **2026-10-19台北14:44／UTC06:44** 選路線圖T2＋T3，
只知分鐘不補秒；採Claude方向建議，操作者為決定人，選題早於#88合併。
C2暫停新增研究，三項既有校準確認與全部物理／r3 OPEN保留。
新增[只定問題契約](foundations/t2_t3_problem_contract_v0_1.md)，
Problem IDs X-T2-MATTER-GEOMETRY-P0.1、X-T3-SECTOR-SPINOR-P0.1，
新model ID NONE，各有六欄；沒有K／作用量／operator構造或新推導。
原文文獻只作作用域核對，不採用其構造、不擴張為L0湧現或formal資格。

接觸帳§27逐字追加EXP-0056與0058、0059作者scope，0057保留上一則方向建議待本人原句；
未取得全文不代填，未宣稱全申報已齊。契約須exact-head GO、原樣合併，
且0057原句與來源審查完成後，才開始具名紙上研究。
本次不改E0／生效SHA、formal、禁止資料／UNKNOWN、停止／回F及全部執行限制。


## 21. PR #89定案與T2／T3具名紙上審計（2026-10-19；權限不變）

#89 r2 head `0f56e951`／tree `3ec33536` 獲exact-head GO，CI #283成功後原樣合併
main `cae0f69e24e3ca0bcf4820deaa284efec5749819`，tree相同；
UTC12:48:54／台北20:48:54。EXP-0057在原ID補齊並獲增量GO，契約blob434e85fc保留。
完成三條件與tree核對後才開始兩份獨立具名研究：
[T2總量審計](foundations/t2_class_sum_audit_v0_1.md)、
[T3 sector能力](foundations/t3_sector_capability_audit_v0_1.md)。
本條只登記【探索／待exact-head】紙上推導，不將任一新結論升格。
T2實際class／分母與物質機制、T3一般intrinsic spinor／L-FIN／動力學仍OPEN。
EXP-0062逐字記Claude本輪增量申報，0063記作者來源／原文／推導範圍。
不構造K、作用量、動力／傳播算子或mass law；新model ID NONE。
C2暫停與既有限定結果／全部OPEN保留，ACT-X-0001仍以0c386716生效且僅紙上；
本條不重新activation、不改E0／formal／item7／8／6a-E／Freeze-1a，
亦不授權科學執行、seed、主機、量測／receipt或任何禁止資料回流。


## 22. PR #90原樣合併與T2／T3限定解析確認（2026-10-19；權限不變）

#90 exact head81f1a260／treebc579c93獲Claude GO，CI #285 run39257616818與
job118076754933在同一head success後原樣合併main
`a5f584a679911f13eb3e4a1909407856e203d39d`，tree相同，UTC15:42:54／台北23:42:54。
[T2總量審計](foundations/t2_class_sum_audit_v0_1.md)限定確認measure換算及條件式相消／改善式；
一般F的充分上界不升格為必要且充分定理。
[T3能力審計](foundations/t3_sector_capability_audit_v0_1.md)限定確認§6分格no-go與「需外加」判定，
不擴張為所有intrinsic spinor都不可能；物理詮釋與既有OPEN保留。
只改兩稿狀態／§1及追加複核紀錄，證明／矩陣與契約不改；
STATUS記T2契約§4.5提問方向已由研究§4.2釐清，不修改定案契約。
EXP-0064逐字保留本人申報，0065記作者只合併／紀錄scope；沒有新研究題、推導或構造。
ACT-X-0001仍以0c386716生效且僅紙上，C2暫停與原確認／OPEN保留；
本條不activation、不改E0或formal／item7／8／6a-E／Freeze-1a、UNKNOWN與禁止資料隔離，
不授權seed／主機／量測／receipt或其他科學執行。


## 23. T6問題契約登記（2026-10-20；權限不變）

操作者於台北11:00／UTC03:00選T6，採Claude建議，由GPT起草
[只定問題契約](foundations/t6_quantum_necessity_problem_contract_v0_1.md)。
Problem ID X-T6-QUANTUM-NECESSITY-P0.1，model ID NONE，限1+1 massless two-sector路徑。
只交六欄、型別／來源與全OPEN義務表、待證問題及文獻範圍，不構造K／state／pairing。
C9／C10的正式criterion、test space／projector／evaluator形式或實例本次皆不選、不改；
原文讀取不構成formal mapping或Freeze交付物。日後若要用結果選formal判準，
先停止回用／記曝光，再按§5及原正式協定另案處理，換seed不能補救。
從8fa27315接續保留0066／0067，0068方向建議申報保留待原句、0069本輪原句及0070作者scope只追加。
來源缺項解除、本契約exact-head GO及原樣合併前，不開始具名T6研究推導。
本條不activation、不改E0／formal／item7／8／6a-E／Freeze-1a或UNKNOWN／禁止資料隔離，
C2暫停及T2／T3限定確認與物理OPEN保留，亦不授權任何科學執行／seed／主機／量測／receipt。


## 24. T6 r1退回與r2依據隔離（2026-10-20；權限不變）

#92 r1 head aeca9033／tree530a7d9f暫不GO，原版與退回理由保留。
T6契約r2點名§5.2.1(v)／D.1第8項：探索結果即使合併／寫入STATUS，在另案handoff、
曝光對應與合資格審查完成前，不構成該條可用的既有STATUS或數學必要條件依據，
不能完成路徑A聲明；原文讀取不是路徑B mapping，不提升原文現有資格。
STATUS標「探索軌，不具 §5.2.1(v) 依據資格」，不改acceptance或其他formal檔案。
0068本人原句已在原保留ID逐字補齊，舊待補行保留；0071本人複核與0072作者scope只追加。
r2仍待新exact-head增量GO與原樣合併，不開始具名研究；QN／QO及model ID NONE不變。
本條不activation、不修改formal規格或其他獨立依據的資格；E0／全部禁止資料／UNKNOWN、
C2暫停與T2／T3限定確認／OPEN、item7／8／6a-E／Freeze-1a及執行限制不變。


## 25. T6契約原樣合併與具名研究待審（UTC2026-10-20／台北2026-10-21；權限不變）

#92 r2 exact head ada4b412／tree12634a4a取得增量GO、CI #290全步成功後，
原樣合併main `865d74a37960a76e1585ec5065ff21ff76395e2d`，tree與GO相同；
UTC17:14:49／台北次日01:14:49。契約blob ce332f5f保留，三項開始條件核對後才開始本輪推導。
新增[具名T6義務審計](foundations/t6_quantum_obligation_audit_v0_1.md)，只交條件式代數證明與QO資料來源表，
全部待exact-head獨立複核，model ID NONE。總CAR form若有負方向可排除正state，
但實際Green／adjoint／pairing到總form的對接未交付，不構成本專案quantum判決。
0073本人原句與0074作者scope只追加；原文閱讀／已知提示來源與停止點均已披露。
探索軌，不具 §5.2.1(v) 依據資格；不得以STATUS或必要條件名義完成D.1第8項A，
讀原文亦非B mapping，轉用仍須另案handoff／曝光／合資格審查。
本條不activation、不改E0或formal／item7／8／6a-E／Freeze-1a，不授權任何科學執行。
C2暫停、T2／T3限定確認、全部OPEN與UNKNOWN／禁止資料隔離不變。


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
