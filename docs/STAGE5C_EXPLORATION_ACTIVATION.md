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
