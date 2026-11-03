# B-01：P0.2 的 order-cut 初值資料 β 獨立登記

狀態：**【B資料提案／待exact-head GO】**。2026-11-03 Asia/Taipei。
依據 [X-KQ-COND-TA-P0.2](kq_conditional_initial_data_problem_contract_v0_2.md) §1、§3；β版本 `B-01 v0.1`。
**探索軌，不具 §5.2.1(v) 依據資格。** 新model ID：NONE。
本稿只固定B資料規則與集合證明，沒有K、K輸出、係數、Green、state或下游構造／證明策略。
母契約全文不改；本資料取得GO、原樣合併並核對tree之前，不固定K。

## 1. 基線、量詞與事前來源披露

基線main `fe24bf3181c8561cd447d066d89032eb97e6574e`，tree `57530e315914bffc400e1451e290b8b269b135da`，
即#103核准原樣合併；唯一parent `950c4ea6`，Git committer台北2026-11-03 00:44:28。
第一commit僅三帳追加EXP-0117、0118及合併事實；本稿在後一commit，不倒填資料選定時間。
公開Git只能證各版內容與commit先後，不能證「從未預想任何結果」或盲性。

沿用原域 D_KQ={P∈D₁:q(P)≥2}。D₁、R₂的定義見
[原始輸入契約](kq_1p1_construction_problem_contract_v0_1.md) §2。
以下是一條跨P、跨N有限規則，對**每個**P∈D_KQ固定B；所有合法L共用相同B。
後文Φ只供母契約§3.3增長witness，不改全域、不挑成功輸入。

已見提示及其實際用途：

| 來源 | 本資料登記如何使用 |
| :--- | :--- |
| Claude #103提示3：minimal元素滿足集合門檻 | 作者採用這個B₀，於§3自行給完整集合證明；不是盲選，也不是reviewer代選β |
| 提示2：共同合法集合可覆蓋部分microcausality | §7預先列出覆蓋predicate及數量；只做B的組合分類，未交CAR或守恆結果 |
| 提示1：守恆與初值轉換unitary | 已接觸，保留為日後核對提示；本稿不指定轉換、不在本輪證這項動力學命題 |

作者在本輪文字起草中也考慮過「所有大小k的反鏈」及「所有大小k的極大反鏈」。
前者可能漏掉一整條極大鏈；後者也不保證與每條極大鏈相交。
最終採下述更窄的**與每條極大鏈恰交一次**的規則，理由只來自order上的完整橫截意義，
不來自任何K、trace可逆性、守恆、Green、A或譜的嘗試；本輪未有這些輸出。
已在紙上預想不交的二點鏈族可給多個trace、diamond可有未覆蓋對；這些是B資料證明，不稱盲驗證。
沒有新文獻檢索／原文閱讀；不以這些組合結果宣稱新穎性或minimal physical primitive。

## 2. β的完整規則：只用order／count

設N=|P|，M(P)為全部minimal元素，k=|M(P)|。
一條**極大鏈**是按包含關係極大的非空全序子集，不是「長度最長的鏈」。記其全體為Ch_max(P)。

固定

$$B_0(P)=M(P),\qquad I(P)=P\setminus M(P),$$
$$\mathcal C_\beta(P)=\{C\subseteq P:\ |C|=k,\ C\text{是反鏈},\quad
      \forall H\in\operatorname{Ch}_{\max}(P),\ |H\cap C|=1\}.$$

每個合法C稱order-cut trace集合；全體都保留，不再選一個偏好的面或為面排序。
這個合法性predicate不得補上「trace可逆」「守恆」「正性」等下游條件。
反鏈條件雖可由每條極大鏈恰交一次推出，仍明列，避免把橫截誤認為任意同基數子集。
所有量詞均由有限order決定；無連續參數、無逐P常數、無每事件配對係數、無L的入口。
R₀只用其母契約既定的二維fiber型別及固定h₀；不選新的R₀或fiber基底。

資料型別不變：D_C=C^C⊗E₀，γ_C為原完整event空間的coordinate restriction，
h_C(b,c)=∑_{x∈C}h₀(b(x),c(x))。這些是母契約固定的初值型別及正配對，不是下游映射的候選。
γ_C只是取值，無權重、相位、transport、插值或L排序；不加spectator自由度。
I對同P的全部C固定，更換C不更換內部方程位置。

物理解讀的上限：M是order的過去端點集合，合法C沿每條極大因果鏈截取一次。
它是有限order的全域橫截資料；**不是**已取得的連續Cauchy面、等物理時間面、度規或守恆流。
尤其不保證初值問題可解或唯一；這些仍是母契約後續可失敗義務。

## 3. 整個D_KQ上的集合條件

**B₀非空。** 有限非空poset任取一點，若非minimal便沿strict predecessor向下；
strict下降不重複且P有限，必停在minimal元素，故k≥1。

**B₀非全體，且是past-set。** q≥2使P至少有一個strict可比對y≺x；x非minimal，故k≤N−1。
若x∈M，沒有y≺x，故past-set條件成立。M也是反鏈，否則可比對的上端不是minimal。

**B₀本身合法。** 任一極大鏈H的最小元素必為P的minimal：若有更小元素可加進H，違反極大性。
H不可能含兩個minimal元素，因鏈內必可比。因此|H∩M|=1，M∈C_β(P)。
這也處理isolated元素：其singleton是極大鏈，每個合法C都必須包含它。

**面族非空、同基數。** 上段給出M；所有其他合法C按定義大小恰為k。
故1≤|C_β(P)|，且每個D_C的複維數都等於2k>0。

**q_I≥2。** 每一strict可比對(y,x)的上端x都不屬於M，故x∈I。
所以q_I=|{(y,x):y≺x,x∈I}|=q(P)≥2，沒有少算任何可比對。
這只核對active位置有足夠order對，沒有證任何sector、傳播或非零解空間。

這些論證對所有有限P滿足q≥2成立，故特別涵蓋整個D_KQ，不需用Φ排除star、鏈或非流形輸入。

## 4. 容量：精確數量、生成規則與編碼上界

令w_P(C)是§2三項predicate的0／1指標；以下都是紙上有限和，未用程式枚舉。

$$c(P)=|\mathcal C_\beta(P)|=\sum_{C\subseteq P,\ |C|=k}w_P(C),\qquad
 1\le c(P)\le {N\choose k}={N!\over k!(N-k)!}\le 2^N.$$

| 項目 | 本版本實際數量／上界 |
| :--- | :--- |
| β的自由參數 | 0個逐P／逐N／逐事件可調參數；只用§2固定predicate，Φ中的整數2固定，不擬合 |
| B₀、I | B₀有k個事件，I有N−k個事件；B₀的membership編碼N bits，I由補集決定，無第二份獨立選擇 |
| 初值維數 | d_B=2k complex coordinates，即4k real coordinates；這是量子初值容量，不是O(1)輸入 |
| 每個合法C | k個事件；membership向量N bits，或在外部序列化下用k⌈log₂N⌉ bits的索引列 |
| 面族基數 | 上式c(P)為精確值；不是只寫Big-O。全部predicate生成，沒有逐P面表primitive |
| 選一個面所需資訊 | 固定外部編碼枚舉時⌈log₂ c(P)⌉ bits（c=1時0）；枚舉順序不成為物理資料或規則輸入 |
| 若顯式儲存全族 | c(P)個N-bit mask，共N c(P) bits；此數可指數增長，不宣稱O(1)儲存或有效率枚舉 |
| 正配對 | 每面恰k份同一h₀；0個額外每面Hermitian矩陣／norm／權重 |

編碼依外部檔案索引描述，不為P選canonical標號，不讀L，也不能把編碼順位回送成科學輸入。
合法C是全部受檢對象；上表的「選面」只說明若傳遞其標記的容量，不授權挑一個有利C。
面族數量取決於order，不能只從N、k唯一決定；有限和是一般精確規則，下一節給closed-form族。

## 5. 事前固定Φ、D₁身分與每個m的witness

固定Φ(P)：P的Hasse圖每個無向連通分量恰為一條二點鏈，且分量數k≥2。
等價地，P是不交的k份C₂；沒有isolated元素或額外跨分量order關係。
這只讀order／count，不讀L或任何下游資訊；不同輸入中的分量無須具名或排序。

### 5.1 此族屬於D_KQ

記分量為a_i≺b_i只是證明用記號，不是新增標籤。任何realizer(L₁,L₂)都保留各分量的a_i≺b_i，
而每個跨分量事件對在兩個total orders中的方向必相反，否則交集會多出order。
在L₁中不可能有其他分量的z插入a_i與b_i之間：若a_i<₁z<₁b_i，則L₂必有b_i<₂z<₂a_i，
與a_i<₂b_i矛盾。因此每份C₂在L₁中都是連續block；L₂也如此。
跨分量方向反轉，故L₂的block順序必為L₁的逆序，block內仍為a_i,b_i。
反過來，任何block排列配上逆排列確實實現P，因跨分量方向相反。
故R₂(P)恰由k!個第一block排列決定；Aut(P)包含任意分量置換，且在這些排列上可遞。
於是Aut(P)×S₂商只有一個orbit，P∈D₁。又q(P)=k≥2，故P∈D_KQ。
這是輸入域的紙上證明，不涉及K的自然性或輸出。

### 5.2 精確面數與無界量詞

極大鏈就是各份C₂；合法C在每份恰選一點，跨分量總不可比，故這些選擇全部合法。
因此

$$N=2k,\quad |B_0|=k,\quad d_B=2k,\quad q_I=q=k,\quad c(P)=2^k.$$

每個整數m≥1，取k=max(2,m)，令P為不交k份C₂。
則Φ(P)、P∈D_KQ，|P|=d_B=2k≥m；c(P)=2^k≥4。
B₀取每份的minimal，另取每份的maximal即為不同合法面；沒有選某K成功的面。
這正好交母契約§3.3的輸入／初值容量witness，不是H_A或守恆的結果。
Φ不保證或代替原契約active K非局域(c)；原域全部其他輸入仍保留。

## 6. 對所有order同構的自然性與L隔離

任意order同構f:P→P′將minimal元素雙射到minimal元素，故f(B₀)=B₀′，f(I)=I′，k′=k。
它也將極大鏈雙射到極大鏈：若f(H)還能延伸，逆像便延伸H而矛盾。
反鏈、基數和交點數均被保持，因此C合法當且僅當f(C)合法。
所以f(C_β(P))=C_β(P′)，不是只驗同一P的Aut。
q_I、c(P)、Φ以及§7的覆蓋關係也逐項由此保持。

共同R₀-unitary V下，定義(U_{f,V}u)(f(x))=Vu(x)，在D_C上同樣定義U^C_{f,V}。
γ_{f(C)}U_{f,V}=U^C_{f,V}γ_C由coordinate restriction逐點成立；
h_{f(C)}(U^C b,U^C c)=∑_{x∈C}h₀(Vb(x),Vc(x))=h_C(b,c)。
B的集合本身不依賴fiber基底，故不因換基新添資料。
這些只核對B／trace／pairing，沒有宣稱未交的下游物件也已自然。

β的每個定義只讀原P的order與count，故同一P上更換任意L不改B₀、I、C族、h或γ。
不透過序列化、Φ或面標記暗藏L；母契約及P0.1 §4.4–4.5的下游隔離一字不放寬。

## 7. microcausality的預定覆蓋表：純B分類

只計unordered、distinct、原P不可比事件對。定義

$$\mathcal U(P)=\{\{x,y\}:x\ne y,\ x\parallel y\},\qquad
 |\mathcal U(P)|={N\choose2}-q(P),$$
$$c_{xy}(P)=\sum_{C\subseteq P,\ |C|=k,\ x,y\in C}w_P(C).$$

一對被覆蓋的**充要order判準**是：存在k元素反鏈，包含x、y，且與每條極大鏈恰交一次，
也就是c_xy>0。這是一個事前有限order/count predicate，不能以後改為「某C的trace成功」。
同基數的限制不能省略；僅知x∥y不代表能擴充成一個合法C。

覆蓋集合Cov_β={p∈U:c_p>0}；未覆蓋集合Ind_β={p∈U:c_p=0}。
精確對數為

$$n_{\rm cov}=\sum_{\{x,y\}\in\mathcal U(P)}\mathbf1[c_{xy}>0],\qquad
 n_{\rm ind}={N\choose2}-q(P)-n_{\rm cov}.$$

這列出每個輸入的完整、可檢查分類，不要求先取得任何K。它不是科學枚舉執行結果。
「Ind」只指**未由共同合法面覆蓋**，不宣稱這些block方程在所有其他恆等式下線性獨立。
按已見reviewer提示，若將來同一完整test上的初值同構與守恆均成立，Cov中的microcausality
可由面上的counting配對與守恆推出；這仍是有前提的提示，不是本稿已取得的microcausality。
Ind中的對仍須額外逐對核對；即使Ind為空，守恆本身仍是未完成且可失敗的義務。

| 輸入 | D_KQ身分／k與合法面 | 被覆蓋／未覆蓋 |
| :--- | :--- | :--- |
| Φ族：不交k份C₂，k≥2 | §5已證；c=2^k | 所有跨分量不可比對都覆蓋；每對c_xy=2^(k−2)。n_cov=4·binom(k,2)=2k(k−1)，n_ind=0 |
| 三點鏈C₃ | 唯一total order使realizer唯一；q=3，k=1；三個singleton都是合法面，c=3 | 無不可比對，n_cov=n_ind=0；不把空檢驗叫microcausality成果 |
| 三葉star a_i≺b | realizer的葉序必反序、S₃置換可遞；q=3，k=3；唯一合法面是三葉，c=1 | 三個葉對全覆蓋，n_cov=3，n_ind=0；單面守恆比較在此輸入空洞，未當全域證據 |
| diamond：a≺b≺d、a≺c≺d，b∥c | 兩個linear extensions只交換b,c；交集即P、realizer orbit唯一；q=5，k=1；合法面僅{a}、{d}，c=2 | 唯一不可比對{b,c}未覆蓋，n_cov=0，n_ind=1 |

表中star、鏈、diamond身分皆由所列order論證，不曾用程式建poset／撒點或計算kernel。
diamond的{b}漏掉鏈a≺c≺d，{c}漏掉另一鏈，所以它們不合法；這顯示Ind可非空。
Φ中的任意跨分量指定兩點後，其餘k−2份各二選一，給c_xy的精確值。
其他輸入用上列同一predicate與有限和，不另列逐P查表或以成功分類。

## 8. 邊界、待審範圍與第二道門檻

本稿固定B₀、I、全部合法trace、h_C、γ的既定型別、容量、Φ及覆蓋predicate。
紙上證據只及B資料門檻；不能由此推出非零解空間、任意trace的參數化、守恆、Green識別、
CAR／state或H_A實際維數。尤其Φ上的2k是初值維數，不是已交的physical自由度。
P0.2正性按構造、不算成果；母契約全部可失敗義務不因此放寬。

本版本GO後不准依下游失敗刪掉合法C、縮P、換Φ、改初值配對或用譜選B。
如需修改β，必先保留此版，修訂資料登記並重新exact-head複核、合併／tree核對，再開始新嘗試。
本登記未GO／合併／tree核對前不固定K；其後也須獨立規格先於研究輸出。
原始輸入問題、P0.1及P0.2科學問題均OPEN；本稿不改既有契約、研究稿或新穎性分類。
結論只限「在外加Ξ和B-01資料規則之下」的資料核對，不回流formal、C9／C10或§5.2.1(v)。
formal／E0、A／B、UNKNOWN及item7不可ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、
Freeze-1a PENDING全部維持。
無模型程式、數值／符號科學計算、RNG／撒點、producer或raw／sealed；只有B的紙上論證與文件／Git核對。

請reviewer重點核對§2–3的全域集合條件、§4容量、§5的D₁／無界witness、§6所有同構自然性、
§7一般覆蓋predicate及四類例子，以及§1的來源／替代方案披露；本輪不請reviewer選K或證動力學。
