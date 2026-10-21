# X-KQ-1P1-P0.1 — 原始輸入下非局域傳播與量子資料同源構造問題

狀態：**【提案／只定問題，待exact-head獨立複核】**。
Problem ID `X-KQ-1P1-P0.1`；新model ID **NONE**。
**探索軌，不具 §5.2.1(v) 依據資格。**
本契約不含K公式、構造材料／ansatz、state／pairing選擇或新的證明策略。

## 1. 操作者選題、定案與開始條件

操作者於2026-10-21 Asia/Taipei表示：「好。照你的建議進行。哪些要貼給claude」。
只知日期，不補時間。所承接的是[方向評估](research_direction_assessment_2026_10_21.md)
的原始輸入下1+1 massless非局域構造與量子對接方向，不是批准任意新增physical primitive。

基線main `630d4628b7e8603a08d2167a92122b3073dc9759`已合併#93。
依賴尚待複核的#94 head `8dceb4b3afec47fe2e7e3abbbc4d1ac121897036`；
#95 r1 head `80457d5a591bd6791f4baf74e66316094c6a50b0`／tree
`f486a852baa64a412ec46c89f6b794bbac993553`保留為本契約前的方向評估版本。
本契約併入#95 r2供新exact-head審查，不把操作者選題當作reviewer GO。
ACT-X-0001生效SHA仍`0c386716701589c9a6b0b799636a808aacb9ade5`，限紙上。

在#94及含本契約的最終#95取得各自exact-head GO、必要CI通過並原樣合併main，
核對merge tree且本輪接觸申報已完成可追溯的整合審查之前，**不開始具名K／state／pairing
的選擇、證明策略或構造推導**。r2發布不代表已定案；若契約需改，先修訂再審，不回改答案。

## 2. 六欄與量詞

| 六欄 | 本題 |
| :--- | :--- |
| 問題 | 能否交出一個具名、來源合規的有限域非局域kinetic構造，並由同一資料鏈對接retarded inverse、總CAR form及正state？ |
| 定義域 | 下述D1上的有限資料規則；1+1 massless僅是後續連續比較目標，不是有限poset已具維度／質量的結論 |
| 輸入 | I-KQ-ORD／NUM／UV，及須逐項申報的L2 quantum scaffolding；本題先限derived amplitude，不採drawn phase分支 |
| 證據 | 後續須交顯式定義、型別與來源鏈、完整紙上證明；本契約不預填任何存在／否定結果 |
| 未證橋接 | K、Green、test／adjoint／CAR、state及dynamics全部尚未構造；連續極限、physical vacuum、質量與幾何選擇不在第一階段完成義務內 |
| 後續／停止 | 先審定本契約。其後逐項交構造／限定障礙／OPEN；新增physical primitive、需執行或回formal時停止，另案審查 |

固定D1為所有非空有限strict posets P，使R2(P)/(Aut(P)×S2)只有一個orbit；
R2(P)是交集恰等於P的成對total orders。這只引用既有Stage5A／T3定義，
不是宣稱D1涵蓋全部撒點、所有posets或任意3+1背景。
**主問題的正面完成量詞：** 一條在看任何構造輸出之前已固定的規則，定義在整個D1上，
對所有同構f:P→P′自然，且對**每個**P∈D1都實質交出§4第1–4項。
須明寫f在事件／sector／test／algebra資料上的誘導映射，所有物件與identities與之交換；
只核對Aut(P)或S₂下降不足。失效狀態、OPEN或僅按構造成立的state不算正面完成。
最低非平凡性另依§4.1逐P與family量詞檢查，不以刪掉小N或不利輸入維持全D1成功。

局部結果的子類必須在查看其構造輸出前，以明文、只用order／count的predicate刻畫，
並列非空性與適用量詞；子類成功只能記局部結果。本r3不另選工作子類或變更D1。
D1包含鏈、單點等不像流形的輸入；全D1上的資料／代數成功不代表1+1維流形性質。
單點無非對角order對，不能滿足§4.1(a)；這種尺寸退化不得獲豁免後又稱強全域問題完成。
若全域要求因退化輸入而不相容，僅記精確作用域的障礙，不當作有分量的物理no-go，
也不藉此聲稱已解決後續非平凡局部構造問題。

**第一階段跨N一致性：要求規則層的一致性。** 使用同一條已固定來源／容量的規則，
不得逐N另選law、pairing、state或擬合表；明寫的自然count依賴不等同逐尺寸調參。
§4.1的非局域性與form維數增長也是跨N要求。第一階段**不要求**任意加點、induced
embedding或nested-region限制都與inverse／state嚴格交換；該較強相容性仍逐項OPEN，
不能把單一規則稱為已證projective／continuum limit。

這不是對所有可能K的窮盡搜尋計畫。若只能排除一個明定構造類G，須先記其定義、
全部自由選擇與來源，再對該G立精確命題；不把「沒有找到」寫為原S5C-Claim不存在。
本契約不預選G的公式或材料，不給BOUNDED-SEARCH-EXHAUSTED／SPEC-INFEASIBLE判決。

## 3. 來源與額外資料帳

| ID | 角色／限制 |
| :--- | :--- |
| I-KQ-ORD／NUM | P、strict order與count；不自帶coordinates、physical density、metric、scale或time slices |
| I-KQ-UV | 唯一realizer orbit及其global swap；不是已選代表、左右物理方向或local chirality。若在代表上書寫，必須給交換／automorphism下的轉換與下降證明 |
| Q-KQ-L2 | complex linearization、dual／*、pairing、CAR及state的逐項來源。需區分通用代數scaffolding與新增physical結構；不能以「標準」免除容量／來源審查 |
| A-KQ-DER | amplitude／phase只能由合法輸入經明寫、固定來源規則導出；不以自由per-event／per-pair表、目標查表或隱藏函數容量編碼答案。此處不選規則 |
| B-KQ-BOUNDARY | 如inverse需boundary／source domain，逐項交其order來源及與K的關係；不是免費新增anchor、foliation、frame或物理邊界資料 |
| E-KQ-COMPARE | 1+1 massless連續背景只可留在外部比較端，不作構造輸入；本契約不選smearing、mapping、norm或evaluator |

來源規則沿用acceptance與E0，沒有提高舊handoff、文獻或既有evaluator材料的使用資格。
本輪已讀公開文獻及既有STATUS部分數值摘要，血緣見[申報補充](research_direction_exposure_supplement_2026_10_21.md)；
後續不稱盲研究，不以probe、planted、witness、run1成功模式或任何禁止資料選構造。
無法排除UNKNOWN／禁止來源回流時停止對應分支；不得靠換名或換seed恢復。

## 4. 第一階段交付：實際同源資料鏈

1. **K與domain。** 交具名kinetic物件、全輸入規則與來源／容量帳，分析sector資料如何進入。
   區分實際sector能力與只附加固定二乘二矩陣；rank或單例非零不能代替來源證明。
   這是探索分析，不執行C3b／C8，也不新增其formal判準。
2. **Green。** 交同一K的retarded inverse或所聲稱的明確composition identity，包含source、
   contact term、boundary及適用domain。若只有evolution kernel，就維持inverse義務OPEN。
3. **總CAR form。** 交實際test資料、adjoint、field ordering及K／Green到form的已證識別。
   不能把裸i(G_R−G_A)、indefinite pairing下的譜或任意正矩陣當成已完成對接。
4. **State。** 只有實際state由同一資料鏈、依事先宣告的規則決定，並證其正性／
   歸一化與同一K／Green／CAR相容，才算實質結果；規則的額外資料與選擇須逐項申報。
   K不必唯一決定state，但不能用無關的正W補洞。若只由A≥0援用有限維Fock／
   quasi-free存在性（包括S=0），僅記**「A≥0時按構造成立」**，不算已交state來源。
5. **相容與未完成項。** 若主張dynamics，交實際algebra作用及相容性。CAR、正性、
   unitary實現、stationarity、正能量與vacuum各自分帳；無對稱資料時不硬填energy。
   對跨尺寸／nested regions／boundary依賴列已證與OPEN，不把單一容易例提升成一般可行性。

每個交付分項只記：①具體定義與證明已交、待複核；②明定前提／類別下的障礙、待複核；
③OPEN。局部成功只按其量詞記錄。沒有完整1–4同源鏈時，不稱已完成本階段構造。
不強制有限poset已有唯一物理真空，不以此改成寬鬆量子viability或scientific PASS。
連續極限只列精確未證義務；如要真正展開其新研究問題，另立後續契約。


### 4.1 事前固定的探索最低非平凡性

以下是可失敗的探索要求，**不是C3b／C5／C6或C9**，不使用其evaluator／controls，
也不得回流為formal判準、projector、排除規則或容差；§5隔離完整適用。
(a)、(b)、(d)對每個聲稱完成的P要求；(c)只能對跨尺寸family要求，不能要求單一有限P
有無限hop距離。主問題按全D1檢查；局部主張只按§2事前order predicate的子類檢查，
並須證該子類非空及(c)所需的無界輸入族，不以空域／有限例使要求真空成立。

(a) **傳播。** G_R至少有一個x≠y的非零block，且所有非對角非零block均須y≺x。
只有對角contact項不合格。這是order傳播支撐，不證physical c、Dirac或continuum。

(b) **sector化約排除類。** 在已宣告且完成orbit下降的global兩slot型別下，
非對角blocks的complex span須有維數至少2。精確排除的是：存在scalar event kernel h_P
及單一固定2×2矩陣M_P，使全部x≠y都滿足K_P(x,y)=h_P(x,y)M_P。
M_P即使可依P／N選擇也排除；h_P即使允許使用sector導出量，仍不放行此單一tensor化約，
故也排除其sector-independent子類。僅調diagonal block不補救。
共同global GL(2,C)基底變換／sector swap保留此span維數；本條不排除一般有限和，
也不對任意per-event基底變換宣稱更強不變性。若新增local fiber識別，另審其來源，
不能藉新增physical資料偽造block差異。這只是具名value化約的排除，實際source／sector
能力仍須另證；不使用formal blind-distance norm或把rank當來源證據。

(c) **非局域。** 對y≺x，d_P(y,x)是最短directed Hasse path的edge數。
在聲稱的輸入family上，不存在一個與P、N無關的有限整數r，使所有K_P非對角support
都包含於{(x,y):y≺x且d_P(y,x)≤r}；並要求K非對角support本身沿order。
即每個r均須有該family內的P與y≺x，使d_P(y,x)>r且K_P(x,y)≠0。
須附解析witness族，不能只展示單一有限尺寸；僅使局域K的inverse變dense不合格。
這只定義「無統一Hasse-hop cutoff」的order非局域性，不等同物理距離、衰減長度、
BHS定理或全部可能的非局域概念。

(d) **非零且增長的總form。** 在完整事前test domain上證A_P≥0後，
H_A的維數須至少|P|；有限test domain下即rank A_P≥|P|。
這個線性下界是事前的探索目標，不是已推得的物理自由度定律或formal門檻。
A=0、H_A=0或隨N有界的rank不能通過；明報test維數、radical、零方向與實際rank。
不得外加無關的正自由度增加rank；總form與有效smearing須由同一K資料鏈識別。

### 4.2 不看譜的規則與state來源分界

在推導／查看相應form輸出前，明寫並版本化固定adjoint／pairing、test space與所有
projection／quotient規則，交來源、參數及自然性；不得參考所得form的正負號、譜或
負模位置／個數，或以讓A變正為目的挑pairing。依譜截斷、刪負模或挑有利pairing，
等同以無關正W補洞，不能解除原規則失敗。改規則須另版事前登記且保留失敗與曝光；
涉及契約輸入／作用域改變時先停止另審，不能事後改寫同一成功主張。

若使用T6的canonical零radical商，該規則也必須事前固定，且只可在**完整T上已證A≥0**
之後作表示／完成化；不得先刪負方向再宣稱A≥0。商不改完整T的正性義務，且仍須滿足
§4.1(d)的維數下界。其他projection／quotient需獨立事前來源，不能冒用零商名義。
如pairing／test／state需要類似額外時間方向、Cauchy面／foliation或frame的physical資料，
而非原合法輸入已導出，記為新增physical primitive並觸發§5停止／conditional條件。

state規則也在相應輸出前固定；依同源資料給出的實際state與通用的存在性校準分開。
任何正A都可採的Fock存在性或任意contraction（例如S=0），只能記「按構造成立」，
不能當作state來源機制或physical vacuum的新結果；正能量與dynamics仍分項OPEN。

## 5. 與T6／formal及conditional分支的界線

本題是另案構造問題，不延長或改寫已定案T6契約。T6條件式必要界可作探索中的
數學檢查，但不因本題使用而取得§5.2.1(v)或D.1第8項的A／B資格。
本題及全部後續產出即使合併／寫入STATUS，也不能直接決定C9／C10 core、test space、
projector、evaluator、prescription、排除規則或容差形式。formal回用仍須另案handoff、
exposure mapping、新版prereg及原規格要求的合資格獨立／blinded審查；讀原文不是B mapping。

新增metric、coordinates、vierbein、Clifford／Spin表示、physical spinor index、chirality、
preferred frame／foliation或nearest-neighbour等physical primitive時，停止原始輸入問題。
若確有價值，另立conditional契約，不能在本題事後補例或把它改稱L2以維持原主張。
原規格允許的two-sector bookkeeping與真正新增physical spinor structure須分辨，不混為禁令。
局域QW／QCA文獻僅作條件比較；沒有將其公式或成功模式採為本題材料。

## 6. 執行與審查界線

本題第一階段限紙上。無新模型程式、symbolic／toy執行、RNG、撒點、seed、producer、
raw／sealed、科學量測、主機消費或receipt；既有regression／integrity僅作repo檢查。
若需執行，先另案固定計畫／資源／來源與授權，不能以review-only名義探索新構造。

請reviewer核對：D1／orbit量詞、來源與L2界線、同一K／Green到CAR與state的要求、
局部結果與全域主問題的區別、conditional停止條件、曝光申報與開始先後。
沒有要求reviewer現在替作者設計K、替其選state或制定formal criterion。
E0、item7不可ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING、
C2暫停、既有T1–T6限定結論及全部UNKNOWN／禁止資料隔離不變。
