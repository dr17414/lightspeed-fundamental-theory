# X-SIGNAL-RESPONSE-P0.1 — 訊號回應問題契約（只定問題）

狀態：**【提案／問題契約待 exact-head 複核；未構造模型】**。
操作者在本輪選擇「訊號回應」，作為 B4／B6 的第一個紙上目標。
Problem ID 為 `X-SIGNAL-RESPONSE-P0.1`；這不是 X model ID、正式候選或 attempt ID。
目前 **model ID NONE**，無 K／傳播子／作用量／動力學／state prescription。

## 1. 生效身分與問題的六欄契約

本工作引用 **ACT-X-0001 生效 commit**
`0c386716701589c9a6b0b799636a808aacb9ade5`，其 tree 為
`c8e4e6ffae89718f77cc70431423244b88b53e79`，與 Claude 核准的 PR #78
head `69e57e4183792c02ba17615b1afce89ee2c71e57`／tree 完全相同。
實際生效時間為 Git committer 時間 **2026-10-12 09:57:23 UTC／17:57:23 Asia/Taipei**，
不是 09:46:37 的批准時間。本契約不更改該 immutable activation 的權限。

| 六欄 | 本契約 |
| :--- | :--- |
| 命題／研究問題 | 哪些明示條件足以讓一次 A→B→A 的準備、傳輸、接收、回應與回讀，成為可辨識、依賴實際準備操作的訊號紀錄？未來能否給出完整實現論證，或找到限定反例／no-go？這是目標，不是存在性結論 |
| 定義域 | 兩個具名裝置 A／B、一個本地準備請求、有限宣告的紀錄窗口；有回應、未收到、延遲與歧義皆須納入未來允許紀錄類，不先假設完美或唯一回波 |
| 證據 | B4／B6 審計的 Q、Z、R、L 與 R0／R2／R5 義務；它們只給資訊必要條件、sampling 限制與條件式解碼，不給本問題的裝置動力學 |
| 未證橋接 | identity／配對／prepare-to-readout law、response 的非平凡性、support、穩定性與 failure／error，以及 B1–B7 原 OPEN 項；若給背景／裝置標記／時鐘，均是條件式輸入 |
| 否定條件 | 對已宣告輸入仍有不可識別紀錄、回讀與操作無關、只能靠 oracle／隱藏 lookup、法則不完整或矛盾，則限定否定／未決；不擴張成所有訊號或物質模型不存在 |
| 後續驗證 | 先獨立複核本契約；之後在此域內提交具名紙上模型及解析義務，或精確反例。沒有 RNG／新 producer／量測；需要執行時另案事前授權 |

## 2. 第一階段的主張範圍：條件式訊號，尚非時空湧現

首份實現研究先走 **X-C 的條件式問題**：容許明示外加裝置身份、可操作的準備／
讀出語意，以及具名背景／因果關係。這只是列出可申報的前提類別，**尚未選定**
任何背景、材料、初態、方程式、operator family 或參數。
必要的物質／傳輸／接收規律仍待提出與證明，不能把「會收到」作為輸入後再證明會收到。

若日後研究 X-I，需另寫 intrinsic 輸入與 forgetful map 的完整契約；本 X-C 的額外
marks／背景不可刪標籤後改稱由 L0 湧現。原 1+1D S5C-Claim、C0–C11、正式 freeze、
core／gate／closure 和 3+1D firewall 都不改，本問題不提供它們的 PASS。

## 3. 要識別的紀錄與容許輸入

下列是未來模型必須解釋或明示條件化的**目標欄位**，不是一份模型或實作 schema。

| 紀錄需求 | 來源／不可省略的義務 |
| :--- | :--- |
| A 的準備、B 的首次接收、B 的回應發出、A 的最終回讀 | 各操作與讀出事件的 device identity／事件身份；不能把任意 chain 當物質軌跡或接收紀錄 |
| 請求／回應的配對與方向 | 若用 request tag、額外 mark 或外部配對資料，列為 conditional input；tag 本身不證明訊號傳輸、相互作用或 intrinsic 識別 |
| 是否收到、回應是否唯一、是否在宣告窗口內 | 模型須涵蓋無接收、無回應、延遲、multipath／誤配對等可能性及其語意；不為得到單值而事後排除困難紀錄 |
| 準備操作對回讀的影響 | 明訂可比較的準備／未準備操作及其共同非控制輸入；證明 response 依賴操作，而非預置回讀、暗藏答案或 oracle lookup |
| propagation support 與先後 | 指明 strict chronology、weak causal relation 或模型內有效 support 的型別；相容性不等於非零傳輸或實際 detection |
| 若要報時間：刻度、讀值、回應延遲、窗口與誤差 | 分別申報幾何 proper time、實際 tick、顯示值的來源；不能由 bare order 直接給 duration，不能把 B_in／B_out 合成同一事件以消除未知延遲 |

操作間的可比較性也須列前提：若存在不同 state／boundary／先前記憶，不能把其影響
誤稱為準備操作的效果。單一請求是問題範圍，不表示資料只有成功的一次；重複性或
「一般情況」將來仍須具名擴域，不由單次存在推得。

## 4. 實現論證需回答什麼（尚未給出答案）

1. **完整 law：** 給出準備、傳輸、接收、回應與讀出之間的完整條件關係／狀態法則。
   如使用機率／量子 law，須有 state、pairing、positivity／normalization 與 operational
   record 的對應；本契約不選這些形式。只畫幾個因果箭頭不足以證裝置存在。
2. **非平凡 response：** 在已明訂可比較的操作類中，receiver／final readout 確實受
   本地準備操作影響。證明須排除操作無關的預錄訊息；不能以 tag 已相同代替機制。
3. **可識別性：** 對完整允許紀錄類說明配對何時單值，以及不知道／多值時如何保留。
   若主張只用 intrinsic input，須按 Q 查同一 forgetful fiber 的目標值是否一致。
4. **穩定性與 failure：** 指明所有稱為可用的適用域及 perturbation／誤差前提；先寫
   欲證界的對象與 quantifiers，再給證據，不憑未來觀測挑數值 cap。機率 tail 不是
   本契約已獲授權的量測；未有 law 或證明即維持 OPEN，不稱可靠訊號。
5. **若用幾何 benchmark：** R 的 ideal rest echo 是已給 metric、刻度、null legs、
   零延遲與唯一回波的條件式參照，不能承擔本次實現。L 已示未知 response latency
   與距離無法由總回返時間分離；不得直接把回返時間稱距離。本問題不做 rod comparison。
6. **離散與連續的分界：** Z 的 uniform sprinkling 幾乎必然無精確 null point pairs，
   不等於不存在有效 light propagation；也不能要求每個訊號 leg 必是 sampled exact
   null pair，再把由此失敗誤報所有 B6 no-go。若聲稱 continuum 對應，另列其極限義務。

這些是探索設計的證明義務，**不是新 acceptance gates、numeric thresholds 或 verdict
taxonomy**。沒有符合條件的完整 law 時只報缺口；有條件模型也不等於真物質或 intrinsic 湧現。

## 5. 證據、暴露與禁止回流

目前直接來源是生效 tree 中的 [B4／B6 審計](b4_b6_clock_rod_signal_record_realization_audit.md)
§1–2、§4–6，以及 ACT-X-0001。該審計當時的 external ideal-echo／Perlick 定位只按其
已報範圍引用；本契約沒有新讀或借未核對的文獻作實現證據。
來源 scopes／基線身份沿原審計與 [接觸帳](../stage5c_exploration_exposure_log.md)
EXP-0013、0016–0021；本次目標選擇與讀取追加 EXP-0022。

不依賴人工 E4 第一分量、witness 2/12、run1／stress 計時、6a-S raw、reference-probe
features／weights／成功模式來選 law、材料、參數、effect 或 cap。這是本契約的來源
界線，不保證作者對其他舊資料有心理盲性；既有接觸與 UNKNOWN 全保留。
日後若發現上述內容影響此分支的構造，停止並追加 provenance／影響審查，不能只
在文中宣稱「未用」消除回流。禁止 payload／重算／正式資料一律依 immutable E0。

## 6. 停止、交付與下一步

未來只能在具名域內報「已確認／限定解析」「限定反例／no-go」「未決」，並保留
每個未證前提；它們都不是 scientific PASS。收到後續反例、發現 oracle／未知來源、
須更改 formal criterion 或超出紙上範圍時，按 ACT-X-0001 暫停相關分支並記帳。
要求新的計算、RNG、producer、seed、主機或量測，停在執行前另案授權。

本契約獲審後，下一份交付可在此域內提出一個**具名紙上實現研究**：逐項寫前提、
模型與證明義務，給解析進展或限定反例。此刻不預選形式，不要求先保證成功，也不
先開新 validation。若欠缺條件只能作幾何重描述，應明列而非報物理實現。

本 PR 至此只選目標與定問題，沒有任何新模型、數值結果、seed、正式 attempt 或
候選評測；tick／rod comparison 不同時擴進首個問題。
