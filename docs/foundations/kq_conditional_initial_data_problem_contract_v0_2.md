# X-KQ-COND-TA-P0.2 — 初值結構、守恆型正性與Green識別問題

狀態：**【提案／只定問題，待exact-head獨立複核】**。2026-11-02 Asia/Taipei。
Problem ID `X-KQ-COND-TA-P0.2`；新model ID **NONE**。
**探索軌，不具 §5.2.1(v) 依據資格。**
本稿固定問題型別、資料來源限制與可失敗的義務；不給K、係數、Green-difference實現、state、
候選邊界規則或構造／證明策略。下列映射是待交物件的型別及驗收等式，不是已交構造。

## 1. 版本、來源與開始條件

基線main `950c4ea6d80a0525d3e61ff42046d9f5376b690b`／tree `2ac1013de219d1a1a857d7772caffd27cad98c64`。
[P0.1](kq_conditional_time_adjoint_problem_contract_v0_1.md)全文保留，
[CF-01規格](kq_conditional_foliation_attempt_spec_v0_1.md)與[研究稿](kq_conditional_foliation_attempt_study_v0_1.md)
繼續只在P0.1下保存，不重算成P0.2的成功或失敗。
原始輸入問題、P0.1及其物理橋接均維持**OPEN**；P0.2不是把既有結果升格。

操作者轉交的選題紀錄為台北2026-11-02 16:49；reviewer把(a)更正為(a′)，提示來源逐字登於EXP-0115。
其中初值正配對、有限inverse、取商及守恆的觀察是**已見reviewer提示**，不是作者盲推導或已完成的本題證明。
本輪只讀既有契約、#101盤點及其repo引用定位，沒有新原文檢索／閱讀。
S3的scalar bracket-null不能不經型別對接就等同fermion CAR的radical；本題不以S3的取商修負方向。
S6的正解空間／Cauchy配對只作已讀盤點的比較，不宣稱該連續資料已由Ξ提供。

本交付第一commit僅三帳追加：EXP-0113／0114及題目申報0115逐字、EXP-0109的Markdown跳脫更正、
0c386716對四份前提審計的權限標頭補記；本契約在後一commit。既有逐字性錯誤不刪改。

**兩道先行門檻，不准以問題GO跳過資料固定：**

1. 本問題契約及其接觸登記取得exact-head GO、必要CI成功、原樣合併main並核對tree。
2. 另交一份**只含B資料規則的獨立登記**，按§3完整固定β、合法trace集合、容量及增長／非空性，
   不含K或K輸出；取得exact-head GO、合併並核對tree後，才可固定K及其下游規格或開始構造推導。

本稿沒有選β；這是明示的下一道資料固定義務，不把「合法B」留到看到K／A後再定義。
β未交或未GO時，只能報「問題契約已定／邊界資料未定」，不能報構造開始條件已齊。
其後還須先有獨立K／Green／S／CAR／state規格commit，再有研究輸出；失敗版與事前預想照實保存。
紀錄PR的reviewer申報沿既定程序在下一交付追加，不產生無限遞迴門檻。
操作者允許後續指定範圍直接執行，不取消這些科學開始／停止條件。

## 2. 問題與量詞：不是完整可逆K的齊次核

沿用P0.1的D₁、q(P)、D_KQ={P∈D₁:q(P)≥2}、全部L∈LE(P)，以及全問題一次固定的
R₀=(E₀,h₀,η₀)，dim_C E₀=2；Ξ=(L,R₀)。底層P不刪減，star、鏈及非流形輸入均保留。

| 六欄 | 本題 |
| :--- | :--- |
| 命題 | 能否在Ξ及事前固定的B結構之下，得到同一內部kinetic／初值解空間、保守的正初值配對拉回、microcausality、非平凡Green識別及同源state？ |
| 定義域 | 每個P∈D_KQ、每個L∈LE(P)、已GO的同一β所列全部合法trace面；不依正性／成功挑P、L或面 |
| 輸入 | 原order／count、Ξ，另加§3的B結構及正初值配對；它們是明列的conditional量子／邊界資料 |
| 證據 | 後續須交§4–7全部型別、恆等式、容量／自然性與可失敗義務的數學證據；正性本身按構造成立 |
| 未證 | β與kinetic是否存在、資料是否物理、守恆／causality／Green識別、非平凡增長、state及continuum皆未交 |
| 失敗／停止 | 任一必要義務失敗即保留該版失敗；新增輸入、縮域、換β或規則須先修約／另版審查 |

固定完整event field／test空間T_P=C^P⊗E₀及counting h₀配對作數學型別。
本題改變的是**方程式／初值domain的安排**，不是看到負譜後縮小T_P。
不再要求一個作用於完整T_P的可逆K同時有非零齊次解，也不將不同domain的逆混稱同一方陣的兩個inverse。
所用kinetic只施加在§3固定的內部方程位置，初值trace另列；非零齊次解的存在／參數化是§4義務。

**正面完成**要求：先一次固定β與跨N規則，對上述每個完整輸入交§4–7及§9比較義務，
對全部structured同構自然。單一容易poset、某個有利L／trace面或事後選出的子類不算全域完成。
局部結果必須以構造前固定的order/count predicate標明；不得事後縮域而沿用全域成功名稱。
跨N使用同一規則，不預設nested-region／continuum或physical time相容性。

## 3. 新primitive B：型別、來源、容量與凍結

### 3.1 B是有共同內部方程domain的初值結構

β是一條全問題一次固定的有限描述規則；它只讀P的order／count及共同R₀的型別，**不直接讀L**，
不讀K、Green、S、A、C、state或任何譜／成功資訊。β不是逐P物件／矩陣查表。
對每個P，它給出B結構

$$\mathscr B_\beta(P)=(B_0(P),\,I(P),\,\mathcal C_\beta(P)),\qquad I(P)=P\setminus B_0(P).$$

- B₀是非空、非全P的order-past-set：x∈B₀且y≺x時y∈B₀。內部方程只在I上施加。
- C_β(P)是事前列明、非空的trace集合族；含B₀，每個C⊂P且|C|=|B₀|。
  「合法」只由β的order/count predicate決定，**不能**由K的trace可逆性、守恆或A是否正定決定。
- 更換C到C′是對**同一內部方程與同一解空間**換初值表述，不重新刪掉C′上的方程、改I、重選K或contact。
  B₀/I決定方程domain，C決定trace；兩種角色分帳，不能都叫「邊界」而混用。
- 對C定義初值空間D_C=C^C⊗E₀及coordinate restriction γ_C:T_P→D_C。
  不附加spectator modes、每事件新fiber或任意transport。

β登記須對整個D_KQ證其輸出滿足上述集合條件，並列
q_I(P)=#{(y,x):y≺x且x∈I}≥2；這只是(a)/(b)能非真空受檢的order/count門檻，不保證有合格K。
需交清楚的初值／邊界物理解讀；trace集合不因命名便已是連續Cauchy面或physical foliation。
若這個B型別或β來源類不能覆蓋整個域，記失敗／局部結果，不能改稱已完成P0.2。

### 3.2 正初值配對與容量

本版本固定各面的正配對為

$$h_C(b,c)=\sum_{x\in C}h_0(b(x),c(x)).$$

這是新增的**初值正量子配對**，不是從order導出的fermionic正性；不以η₀的不定配對替代它。
不准逐P／逐面重新選權重、正矩陣、相位、norm或frame，使守恆／A成立。
其容量與來源如下，β登記必須給實際數量，不能只報Big-O而不列實現：

| 項目 | 容量與來源 |
| :--- | :--- |
| β及合法面predicate | 跨P／N的一份有限law；全部常數、分支、參數與來源一次披露，無逐P表／擬合 |
| B₀與C的索引 | 都是P的子集；若將當前C視為外加選面標記，其membership至多N bits；B₀也至多N bits的索引表述。規則確定索引不等於其physical角色免費由order湧現 |
| 合法面族 | 必須由同一predicate生成，給其基數／編碼上界；不把一份逐P列好的巨大面表藏成O(1) primitive |
| 初值自由度 | d_B(P)=dim_C D_C=2|B₀(P)|，對同P的所有合法C相同；這是可隨P增長的實際量子資料，不是O(1)的R₀ |
| 配對 | 由上述固定h₀ counting law給出，無額外每P／每面Hermitian係數；若需別的正配對，先停止改契約 |

### 3.3 非空守恆比較及增長的預定量詞

β登記還須在**任何K輸出之前**固定一個只用order/count的predicate Φ(P)，並證：
對每個整數m≥1，存在P∈D_KQ滿足Φ、|P|≥m、d_B(P)≥m且C_β(P)至少含兩個不同trace集合。
Φ不能用「某K／守恆／microcausality成功」定義。這確保守恆與增長不只在空族／單一trace面上受檢。
對其他P仍須履行全域義務，不能因Φ只及部分輸入就刪掉其餘P。
本稿只固定這項門檻，不提供β、Φ或其witness／證明；它們是第一道資料登記的實質交付。

### 3.4 同構與L隔離

f:P→P′保持原order及L→L′，共同unitary V保持R₀，沿用P0.1 §4.1。
β須對所有order同構自然：f(B₀(P))=B₀(P′)，f(C_β(P))=C_β(P′)；不是只驗Aut。
f及共同V誘導D_C、T_P、source與內部方程domain的映射，配對／γ／K／Green／S／CAR／state均須給交換圖。
本版選較窄來源類：B₀、面族、γ及h_C不直接讀L。不能以P0.2新增B為理由另開L排名通道。
若要以L決定B或另加時間面資料，必須先改本條並重新exact-head複核，不能在構造時例外放行。

## 4. 同一內部K、非零齊次解與初值映射

後續須先固定同一order-supported block law，再得到內部kinetic
K_int:T_P→J_P，J_P=C^I⊗E₀；它只有內部方程，沒有在B₀加Kψ=0的要求。
K_int的全部L依賴逐字繼承P0.1 §4.4的order型別／pre-between-post固定線性彙總限制；
非order非對角blocks為零，diagonal不讀L。只刪方程位置，不藉B新造未列的K係數。
n_τσ仍以原P及原S_xy計數，不刪除B₀事件後另算時間統計；M_τσ仍跨P／N／pair固定一次，
其值與K^ord規則須在後續獨立規格固定，本稿未選。

定義待研究的共同齊次空間Sol_K=ker K_int⊂T_P。後續須對每個合法C證

$$\gamma_C|_{Sol_K}:Sol_K\longrightarrow D_C\quad\text{為線性同構},\qquad
E_C:D_C\longrightarrow Sol_K\quad\text{為其逆}.$$

這要求同一解空間由每個合法初值面完整且唯一參數化，並交Sol_K≠{0}；不能把零空間的正性當完成。
不能另選一個較小的解子空間來滿足trace／守恆，也不能以成功的trace面反過來定義「合法」。
E_C只能由同一K_int及已固定γ_C的這項初值問題決定，不是自由的isometric embedding或正矩陣因子。

canonical B₀還須交初值加source的良定性：
(γ_B₀,K_int):T_P→D_B₀⊕J_P為同構，並交其解算映射R_B₀及左右composition identities。
R_B₀(b,0)須等於E_B₀b；R_B₀(0,j)是零B₀初值的source response。這兩種輸入不能混同。
以B₀/I的既定event索引識別D_B₀⊕J_P與T_P，所得完整response記G_R。
G_R須沿**原P** retarded；不是沿L新增因果edges，也不是將初值evolution直接改名為kinetic inverse。
任何G_A／dual operator、source、contact、boundary或test pairing均須在K規格中具名列出並證所聲稱的恆等式。
本契約不選這些公式，不斷言有任何K符合以上要求。

## 5. 總form：初值拉回，但正性本身不算成果

用完整T_P上的固定counting h₀配對定義E_C的數學adjoint，要求test→初值映射
S_C:T_P→D_C是E_C的該adjoint：h_C(b,S_Cf)=h_P(E_Cb,f)。
這固定smearing／dual的型別來源，不授權另選S_C、額外projection或per-input pairing。

本題總form的定義方式固定為

$$A_C(f,g)=h_C(S_Cf,S_Cg),\qquad f,g\in T_P.$$

**正性因此按構造成立，不是本題成果、不是新正性定理，也不能作主要成功判準。**
尚須交實際field／CAR *與此數學adjoint的識別、完整關係及state來源；不因寫出Gram form就稱物理CAR已導出。
初值正pairing本身就是新增的量子結構，不宣稱本題從純order推出量子論。
最低代數型別沿T6：複線性a:T_P→unital *-algebra，要求
{a(f)*,a(g)}=A_C(f,g)1對所有f,g成立；各面使用同一test、field與*，其一致性另須通過§6.1。
charged或self-dual的額外關係／conjugation須在後續規格分型固定，不能混用；本稿不選其中的物理實現。

定義變更時，不得先算一個想要的A，再取因子命名為S_C，或由其正部分重建初值空間。
P0.1 §4.5的factorization／同上游同輸出判準沿用，僅新增已固定B物件作具名上游：
S、Green／adjoint、A、state都不能再直接讀L、n_τσ或解碼排名作係數／選擇器。
β、h_C的來源不含L，故B不能成為間接的排名算術／查表補洞。

## 6. 可失敗的核心義務：守恆、microcausality、Green識別

### 6.1 守恆採嚴格相等，不預留事後容差

對同一P、L、R₀、β及K_int的每對合法C、C′，必須在**同一完整T_P**上有

$$A_C(f,g)=A_{C'}(f,g)\qquad\text{對所有 }f,g\in T_P.$$

需同時交初值轉換T_C′C=γ_C′E_C的型別／composition，以及它保留上述固定初值配對的證據。
換C不換K、Sol_K、source、h_C law、test或state規則；不能只在不同空間上各自重新歸一化。
本版不允許「差一個未定scalar」「按輸出調unitary」「只在部分probes相等」或事後誤差帶。
合法面族及§3.3非真空比較在K前已固定；只驗一個面、刪掉失敗面或先挑等距面均不算完成。

### 6.2 Microcausality採原P的不可比關係

若f、g的支撐中每一對x、y皆是原P的不同且不可比事件，必須A_C(f,g)=0。
等價的point-supported block檢查須覆蓋完整fiber與所有這類事件，不只檢查某一state期望值。
L的先後不能把不可比者改算可比；不准因microcausality失敗而改order、test或合法面。
這是本題對總CAR form的明文條件，不等於已交Dirac／physical locality。

### 6.3 Green同源：不接受只有初值Gram的同義重寫

後續獨立規格須在任何K／S／A輸出前，給一條**具體、typed的Green識別式**：
以同一G_R、具名G_A／dual、source/contact與固定B資料，在原P可比對上的全fiber test，
把A_C與Green響應的sesquilinear配對聯繫起來。只寫「存在某個F」不合格。
式子可屬Green-difference等事前明列類，但本問題契約不替作者選公式或符號。

識別式必須履行以下要求：
- 不以算完A後定義C_Green:=A；也不以A=S* S、E_C是某個Green的邊界列等定義性Gram重寫充作獨立對接。
- 必須交零初值source response及homogeneous初值傳播的composition關係，說明Green式確實使用同一內部方程，
  不是讓K只存在於一個無關演化欄。若Green式根本忽略內部source response，需判未完成，不另設例外。
- 同一K變更時，所有Green／E_C／S_C與A依同一規則重求。比較類在事前固定、保持β與輸入型別；
  至少兩個合法kinetic比較對象在原order可比pair上給不同A，並有至少一個非零可比off-diagonal CAR block。
- 不能用一個K-dependent scalar乘無關正W、只改contact或直接指定全事件δ-CAR來交差。
  非恆定本身仍不代替實際field *／CAR及Green恆等式的識別。

只有generic Gram非恆定、抽象state存在性或初值拉回正性，均不算本節成果。
守恆、microcausality或Green式任何一項失敗，該版(a′)不成立；不能退回先給全事件CAR的另一條問題鏈。

## 7. 探索非平凡性：保留(a)–(c)，重定(d)

以下不是C3b／C5／C6／C9，也不回流formal。P0.1的(a)–(c)至少同等強度保留，且只用實際內部方程：

(a) 每個完整輸入的G_R至少有一個原P的非對角非零傳播block，且所有非對角支撐沿y≺x。
只有contact不合格；須註明該block是初值到內部或source到內部的真實響應。

(b) 每個輸入中，K_int的原order非對角、**實際施加的方程blocks**之complex span至少2。
不能只在未施加的邊界rows放不同矩陣；排除scalar kernel⊗單一2×2矩陣化約。
共同GL(2,C)換基下的同一判準與P0.1的來源／L限制照舊，不把span稱Spin／chirality。

(c) K_int本身沒有全輸入／跨N統一的有限原P directed Hasse-hop cutoff。
每個r須交合法輸入的active block：y≺x、x∈I、d_P(x,y)>r且K_int(x,y)≠0。
不能只靠inverse／初值extension變dense，也不能用被丟掉的邊界row或L排名差作witness。

(d) 初值規模與H_A增長分開記：
- 在完整T_P上，以共同A的**精確零radical**取正Hilbert商H_A，不用譜容差／負模截斷。
- 每個輸入需交dim H_A與rank S_C、d_B(P)的關係，目標為dim H_A=d_B(P)>0；
  不附加與初值無關的自由度補rank。若此等式隨已交的初值同構自動成立，須明記「按構造成立」，不當獨立新結果。
- 真正的跨尺寸規模要求採§3.3：同一β、Φ及規則，對任意m有合法輸入使dim H_A≥m，且有不同面可檢守恆。
  不要求每個P的rank都≥|P|，也不聲稱沿鏈／每條輸入族都線性增長；這是對P0.1(d)的**明示改題**，不是已滿足舊(d)。

β未通過增長／非空登記時，不得用固定有限維初值空間或零代數當完整成功。
整體完成仍須§6可失敗義務及全域量詞；(d)自動的部分不能抵消其失敗。

## 8. 反補洞、state與停止

B₀、合法面族、γ、h_C、S_C的定義與初值／source型別，及Green／CAR／state全部規則須先寫明並版本化固定。
禁止使用A或任何候選C_Green的譜投影、sign function、正部分／負部分等函數演算來定義或改造B、S、A或test。
禁止依A的符號／譜、負模數、是否守恆／causal挑B或合法面、換pairing、縮Sol／T或改normalization。
任何精確radical商只在已定義的正A之後記其物理識別，不是修改K的方程或刪負方向的方法。
P0.1 §4.4–4.5的L限制逐項適用；矩陣composition／inverse只可作事前列明的同鏈代數用途，不能作排名解碼例外。

若聲稱state，仍須獨立規格固定state／兩點資料／高點規則及same-source來源，交正性、歸一化與同一CAR相容性。
在已正CAR上generic Fock或任意contraction的存在性只記按構造成立；不等於physical vacuum、正能量或Green來源。
本稿不選state，不以初值正pairing冒稱已完成量子實現。

新增metric、gamma／Clifford、spatial lattice／shift、local frame／transport、任意邊界state、density、
physical時距或另一配對，都須先停並另審primitive；不能以「在Ξ和B之下」任意增資料。
變更β來源類、Φ／合法面predicate、增長量詞、Green式類別或任何非平凡門檻，要在新嘗試前修約另審。
不因失敗而刪面、縮P或回寫已固定版本；全部失敗與已見提示保留。

## 9. 與文獻及運動學CAR的界線

僅沿已合併[#101盤點](kq_quantum_bridge_literature_inventory_2026_10_28.md) §§3–5、8，沒有新原文閱讀：

| 來源 | 本題的界線 |
| :--- | :--- |
| S3 scalar Peierls／bracket-null | 本題改列初值domain，不直接套其scalar取商；不把Poisson kernel當已正fermion CAR，不把移除kernel說成修負譜 |
| S6 continuum solution CAR／Cauchy正範數 | 只作初值正配對及守恆義務的來源提示，不認為其spin／metric／Cauchy資料已在有限P取得；不是本題可直接引用的正性存在定理 |
| S8 Farrelly–Short | 先給空間格點fermionic modes的δ-CAR，再談causal unitary演化。不能改寫成原文明說「所有時空事件的δ-CAR」；本題P0.1所禁的全事件δ-CAR是另一個待排除prescription |

(a′)只把固定初值面上的正量子配對當primitive，其餘完整event test的A必須經同一K_int、E_C、S_C取得，
且另過§6守恆／microcausality／Green識別。它並非完全不給CAR型量子輸入，也**不預宣稱比S8用更少primitive**。
一般「初值CAR＋演化」可能與既有canonical／QCA範式重疊；後續必須作逐項輸入／domain／作用域mapping，
不能藉初值一詞宣稱已避開所有既有做法或已新穎。未通過§6時，不能把另一路線的演化成功當本題成功。
實質交付至少要有全域不規則P的同源對接或精確限定障礙及完整證據，不以generic Gram／Fock存在性作新發現。
新穎性、minimal primitive及1+1 Dirac continuum仍是另列OPEN義務。

## 10. 結論標示、formal隔離與複核清單

所有結果一律標「**在外加Ξ和B結構之下**」，列明β版本、全部P／L／合法面量詞及未完成義務。
本題不回答原始輸入或P0.1的存在性／不可能性，不改CF-01，不回流成C9／C10、§5.2.1(v)或D.1第8項A／B依據。
formal使用仍須另案handoff、曝光mapping、新prereg及合資格獨立審查。
只限紙上：無模型程式、數值／符號／toy執行、RNG、撒點、producer、raw／sealed、seed、主機或量測。
不以既有probe／planted／witness／run1成功模式選β、K或law；UNKNOWN回流無法排除就停止相關分支。
E0、item7不可ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING及既有隔離不變。

請reviewer核對：B資料獨立凍結是否足夠先於K；合法面與Φ是否禁止事後縮選；I與trace C是否分帳；
完整test／初值／source型別與非零Sol義務；正性及rank的按構造部分是否坦白；守恆是否非真空且同K／同test；
microcausality是否用原P；Green義務是否排除Gram同義反覆；(a)–(c)是否保留並只用active rows；
(d)改題與容量是否明示；S3／S6／S8比較是否不誇大；P0.1／歷史稿／formal及所有接觸是否保全。
本次只審問題，不要求reviewer替作者選β、K、Green式、state或證明策略。
