# IB-01 v0.1 — 固定初值試作與獨立 Green-sum 識別規格

狀態：**【規格提案／待exact-head GO；未開始研究輸出】**。2026-11-03 Asia/Taipei。
Problem ID `X-KQ-COND-TA-P0.2`；探索model ID `X-KQ-IB-01-v0.1`。
**探索軌，不具 §5.2.1(v) 依據資格；只在外加Ξ和B-01之下。**
本稿固定一個可失敗的校準型試作，不交案例研究、證明、輸出矩陣或義務通過判定；事前腦中預算另披露於§1。
規格本身須先取得exact-head GO、CI成功、原樣合併及tree核對；完成前不做實例化K、研究推導、枚舉或科學執行。

## 1. 依據、程序與已見資訊

基線main `a8fb088463ee7717e48e6c6640ad6e3107176a3b`，tree `3473d31410db2a045fd6598e026ae838150e1924`，
唯一parent `fe24bf31`，Git committer台北2026-11-03 12:28:38。
[P0.2](kq_conditional_initial_data_problem_contract_v0_2.md)及
[B-01](kq_conditional_boundary_beta_registration_v0_1.md)均已GO／原樣合併／tree核對，全文保留。
第一commit只追加三帳EXP-0120、0121及合併事實，本稿是第二個獨立規格commit；
母契約§1的資料門檻已滿足，操作者本輪另要求本規格先GO再開始構造／研究輸出。
失敗後不修改本版係數、B、面族、Green式或判準；新版本須另審並保留失敗版。

**L作用域對齊。** reviewer本輪建議「K不讀L」是比現行契約更窄的類別，不是P0.2 §4原文。
作者對讀P0.1 §4.2–4.5、P0.2 §4與既有star障礙後提出差異；操作者在選項中選擇
「沿用契約 (Recommended)」。所以本規格沿用K的限定線性L入口，沒有採全面order-only限制。
β、初值配對、trace不讀L；下游只讀列名上游，不再直接讀L。K不因換合法面C而改變。
請reviewer特別核對這項已由操作者選定的對齊，不把它誤認為偷偷放寬契約。

本規格不是盲選：
- 已見OP-01與CF-01限定障礙、CF-01全域sector校準、P0.2初值Gram正性按構造，以及reviewer的守恆／unitary與共同面覆蓋提示。
- 作者讀了[CF-01規格](kq_conditional_foliation_attempt_spec_v0_1.md)的係數與下游規則；本版保留其七格線性count的數學常數，改內部方程與Green識別，不宣稱新sector機制。
- 已預想有限order的單位diagonal配合strict支撐可能給初值/source inverse，但這不保證其他合法面可參數化同一解空間。
- 已預想counting初值配對的守恆、branching的microcausality、獨立Green等式可能失敗。起草時作者也在腦中代入過C₃的初值傳播，預見其可能非unitary、Green關係可能失敗；不能聲稱完全沒有案例預算，沒有據此調係數修復。
- 曾在腦中考慮order-only、path／cover型規則、order incidence／反演型規則及boundary-flux類恆等式，沒有固定或求解那些版本。本版只採下面明列的一條規則。
- 本版選Green的**和式**及固定contact，作為初值Gram以外的獨立假說；不是從所得A找其因子或事後令Green form等於A。

這些是來源及事前預想，不是成功證據，也不是規格GO後的獨立研究驗證；公開Git只證版本內容與先後，不證盲性。
本次交付止於規格與這項事前接觸披露，不繼續案例代入或完整研究；請reviewer一併核對其程序定位。
沒有新文獻檢索／閱讀；文獻與物理解讀只保留母契約的上限，不預認證新穎性。

## 2. 全部輸入、型別與B不變量

P遍歷全部D_KQ，L遍歷LE(P)，R₀=(E₀,h₀,η₀)固定；dim E₀=2，η₀為母契約給定的Hermitian involution。
T=C^P⊗E₀，J=C^I⊗E₀，D_C=C^C⊗E₀；各空間使用固定h₀ counting配對，第一槽共軛線性。
記†為這些正配對的數學adjoint；不是fermionic代數的*，也不使用η不定配對定義正性。

B₀=min(P)、I=P\\B₀、全部合法C、Φ、c(P)、Cov／Ind均嚴格照B-01，不改predicate或縮域。
ρ_B=γ_B₀、ρ_I為coordinate restriction；ι_B=ρ_B†、ι_I=ρ_I†為零延拓注入。
ρ_B與ρ_I分別標記初值與source，不能互換；選C≠B₀不改I或source位置。
每個C仍使用B-01的γ_C與h_C，不選每面norm、權重、frame、phase或transport。
全部維數、B容量與L容量沿母契約／B-01如實記帳，不給新的physical primitive。

## 3. K規則、全部係數與合法L入口

令Z(x,y)=1_{y≺x}，Z²是原P事件矩陣的composition。對y≺x，S_xy、τ、σ、n_τσ逐字照P0.1 §4.4，
用原P計數，不因B₀移出方程domain而重算；不讀全域rank或L中z彼此的順序。
固定七個可能型別的係數如下；未列的型別一律0，不留調參項。

| τ=(rel(z,y),rel(z,x)) | σ | M_τσ |
| :--- | :--- | :--- |
| (∥,∥) | pre | −√2 η₀ |
| (∥,∥) | between | 0 |
| (∥,∥) | post | −√3 η₀ |
| (∥,≺) | pre | −√2 η₀ |
| (∥,≺) | between | 0 |
| (≻,∥) | between | 0 |
| (≻,∥) | post | −√3 η₀ |

固定L不參與的部分，對x∈I、y∈P為

$$K^{ord}_{int}(x,y)=\delta_{xy}I_{E_0}-1_{y\prec x}\big(I_{E_0}+Z^2(x,y)\eta_0\big).$$

對strict order block加上上述Σ n_τσ M_τσ；diagonal為I，其他非對角block為0。
這完整定義K_int:T→J。只用active rows，不在B₀另施齊次方程，也不靠未施加的rows提供sector span。
為簡記，定義T上的strict-order矩陣D，其order block為

$$D(x,y)=I_{E_0}+
 \big(Z^2(x,y)+\sqrt2(n_{(\parallel,\parallel),pre}+n_{(\parallel,\prec),pre})
 +\sqrt3(n_{(\parallel,\parallel),post}+n_{(\succ,\parallel),post})\big)\eta_0,$$

非strict-order block為0。於是本規格的同一規則也寫成K_int=ρ_I(I_T−D)。
D只作係數law的簡記，不是多一個physical kinetic或邊界方程；不輸出任何實例矩陣。
相對CF-01，這是反號off-diagonal及內部row限制，沒有新的自由scalar或per-P／per-pair係數。
1、√2、√3及七格零值是作者沿用的L3數學常數，不是order導出的物理常數或擬合結果。
全問題只取這些值，無參數搜索、normalization補救、count乘積、奇偶／模／lookup或譜依賴。

## 4. 初值/source response與每條下游分解式

定義augmentation M=ι_Bρ_B+ι_I K_int:T→T，它是初值加source方程的event索引表述，
**不是**在B₀也施Kψ=0。記D_I=ι_I(ρ_I−K_int)，即ι_Iρ_I D；本版固定的response規則為

$$G_R=\sum_{j=0}^{N-1}D_I^j,\qquad G_A=G_R^\dagger.$$

研究須核對MG_R=G_RM=I_T、order-retarded、G_A為M†的advanced inverse，以及
ρ_B G_Rι_B=I、K_int G_Rι_B=0、ρ_B G_Rι_I=0、K_int G_Rι_I=I_J。
不把G_A稱為同一非self-adjoint M的另一個inverse；它更不是未交physical Dirac advanced解。

令Sol=ker K_int。每個合法C都須核對γ_C|Sol為同構；只有成立時，E_C才定義為其唯一逆。
若任何合法面失敗，該版FAIL；不換面、不使用廣義逆、不選較小Sol或另挑embedding。
canonical E_B₀必須與G_Rι_B一致；零初值source response必須是R_I=G_Rι_I，不得省略。
若型別／inverse失敗，後續相依物件記undefined／未完成，不拿零映射當完成。

| 物件 | 只依賴列名上游的固定規則 |
| :--- | :--- |
| M、D_I | P、R₀、固定B₀/I、K_int；D只作§3公式的簡記，不是另給的上游資料；沒有可換C選擇器 |
| G_R | P、R₀、B₀/I、D_I；上述有限和，只作同一初值/source方程的inverse |
| G_A／adjoint | P、R₀、B型別、G_R；counting adjoint G_R†，無另讀L的η選擇器 |
| E_C | P、R₀、B、C、K_int；γ_C在同一Sol上的唯一逆，不以成功反定義合法C |
| S_C | P、R₀、B、C、E_C；強制S_C=E_C†，無自由smearing／projection |
| A_C | P、R₀、B、C、S_C；A_C(f,g)=h_C(S_Cf,S_Cg) |
| Green form C_G | P、R₀、B型別、G_R、G_A；§5固定和式及contact |
| CAR、state trial | P、R₀、B、C、A_C；§8固定charged關係與Q=A_C/2，不讀其他資料 |

每列固定P、R₀、B與列名上游後，兩個L若給相同上游，必須給相同輸出。
所有規則不得再直接讀L、n_τσ或從K／Green解碼rank；inverse／adjoint／composition僅作表中代數用途。
structured自然性、共同R₀-unitary與全部交換圖留待GO後逐項證；本稿不宣稱已通過。

## 5. 獨立typed Green識別假說與source檢查

固定完整T上的Green form算子及contact為

$$C_G=G_R+G_A-I_T. \tag{IB.S1}$$

I_T是固定counting型別中的contact，不是外加的positive CAR；A仍只能由母契約的初值拉回定義。
IB.S1是作者在任何案例輸出前選定的獨立假說，不依A正負改符號、係數或contact。
不是CF-01的iH(G_R−G_A)，不宣稱只改成和式便能完成量子橋接。

**事前識別式：** 對原P每個strict comparable pair y≺x、全部v,w∈E₀、全部合法C，要求

$$A_C(\iota_x v,\iota_y w)=h_P(\iota_x v,C_G\iota_y w). \tag{IB.S2}$$

反向pair由Hermitian相容性另核對。IB.S2只識別strict可比blocks；不把C_G的diagonal
默認當成A的diagonal，也不以這條比較域要求偷渡全部T上已正或已microcausal。
完整T上的A及其所有diagonal仍由初值規則決定，不能為配合IB.S2重新歸一化。

須同時直接核對同鏈source/contact恆等式

$$M C_G M^\dagger=M^\dagger+M-MM^\dagger, \tag{IB.S3}$$
$$\rho_I C_G\iota_I=\rho_I R_I+(\rho_I R_I)^\dagger-I_J. \tag{IB.S4}$$

IB.S3–4使用同一augmented初值/source方程及零初值R_I，不是定義C_G:=A或重寫A=S†S。
它們單獨成立不算IB.S2通過。IB.S2必須對**兩端都在I的strict可比對**另列source-sensitive檢查，
不能只核對一端在B₀的初值欄就聲稱獨立Green對接。預定C₃、C₄與diamond的這類對均須檢查，
不得挑其中成功者替代其他例子；完整全域義務仍保留。
若某P沒有這類internal-source對，須標為該項獨立檢驗空洞，不把結構性等式當非平凡證據。
任何IB.S2失敗都保留FAIL，即使A按構造正、IB.S3–4可驗也不得交差。

固定比較對象為K_int(t)=ρ_I(I_T−tD)，t∈{1,2}；實際試作只取t=1。
同一B、h、係數型別、inverse、E／S及Green規則重求，不能直接把t乘在既有A上。
兩者均須先過來源／support、初值/source良定性與全部合法trace的型別條件，才可稱合法比較對象。
若某個不合法，記比較義務未完成，不改t、不擴候選池、不按成功另挑輸入。
非恆定檢查固定先在C₃、C₄、diamond逐項報告；至少一個預定輸入有兩個合法對象，
在strict可比full-fiber block給不同A，且實際t=1至少一個非零可比CAR block，才算交到此項證據。
不能只用K-dependent scalar乘無關正W、邊界欄Gram或generic state存在性充作Green識別。

## 6. 三項可失敗義務：判定與邏輯依賴

以A_C的counting矩陣L_C=E_C E_C†作**判定表述**，不以它作新的Green定義。

| 義務 | 固定判定方法／失敗處理 |
| :--- | :--- |
| 嚴格守恆 | 全部合法C,C′在同一T上要求L_C=L_C′；逐元素全fiber的精確等式，沒有scalar／容差／有限probe替代。任一失敗即FAIL |
| Microcausality | 原P每個x∥y直接核對ev_x L_C ι_y=0，全部fiber及全部合法C；不以L改order。Ind中的對不得由共同面提示略過 |
| Typed Green | IB.S2逐strict可比pair核對；另交IB.S3–4、source-sensitive內部對及預定合法比較。Gram正性／非恆定本身不算通過 |

各面初值轉換γ_C′E_C及其composition／unitary條件須另列，但本規格不以任選unitary代替同一方程的trace。
c=1時守恆對角自比按定義成立，單列「守恆比較不提供判別力」；不把該P整體稱無判別力或刪除。
共同合法面覆蓋的microcausality，只有在初值同構與守恆已交之後才可引用reviewer提示的推論。
未覆蓋Ind中的每一對必須直接檢查；守恆失敗時，Cov也不能當已通過。
IB.S2的比較域不含不可比對，所以Green識別不能代替Ind的獨立原P檢查。
各項依賴關係必明記，不把相互推出的等式重複算成獨立成功證據。

## 7. 紙上評估目錄、B分布與非平凡性

主量詞仍是全部P／L／合法C。以下固定目錄只是必報的校準／反例檢查，不是縮域或抽樣。
有限目錄𝒯₆固定為C₃、C₄、三葉star、diamond、不交2份C₂、不交3份C₂，各一個order同構類。
同一order型必須涵蓋全部L，不以任選label或L挑成功代表。
每項均報N、q、k、d_B、c、n_cov、n_ind、是否有internal-source可比對，及每一義務的PASS／FAIL／undefined。
其中B數據依已定B-01公式報告；不得依K輸出更換分類。下面只抄列／代入B的紙上數量，不是K輸出。

| 固定目錄項 | c | n_cov | n_ind | 守恆比較 |
| :--- | ---: | ---: | ---: | :--- |
| C₃ | 3 | 0 | 0 | 須檢查全部面 |
| C₄ | 4 | 0 | 0 | 須檢查全部面 |
| 三葉star | 1 | 3 | 0 | 不提供判別力；其他義務保留 |
| diamond | 2 | 0 | 1 | 須檢查全部面；唯一未覆蓋對直接檢查 |
| 不交2份C₂ | 4 | 4 | 0 | 須檢查全部面 |
| 不交3份C₂ | 8 | 12 | 0 | 須檢查全部面 |

這六個order型的c分布為{1:1,2:1,3:1,4:2,8:1}，n_cov分布{0:3,3:1,4:1,12:1}，
n_ind分布{0:5,1:1}。只是固定目錄的計數，無抽樣分布／統計權重，也不代表全D_KQ頻率。
後續研究必將固定目錄逐項列出並報同欄位；不能事後刪FAIL、換成功例或只給總通過率。
額外案例只能追加為明標探索，不替代本目錄、預定比較對象或全域量詞。
跨尺寸檢查另固定全部鏈C_N（N≥3）、全部star及dual star（葉數r≥2）、B-01的Φ族（k≥2）。
需先給其輸入身分與B分類，再處理義務；族上的符號論證不能冒充已跑有限枚舉。

母契約§7(a)–(d)逐字保留：真實原order off-diagonal response、active block span≥2、
active K本身無統一Hasse-hop cutoff，以及H_A／d_B的非零與Φ無界增長關係。
不以dense inverse替代(c)，不以initial dimension替代實際H_A，不將正性或自動rank等式當成果。
即使固定目錄全通過，也不能宣稱全D_KQ／continuum／physical spinor已完成。

## 8. CAR與state trial：明示按構造部分

在共同A已由全部trace相容識別之前，不宣稱已取得單一物理CAR。
型別核對用charged unital *-algebra：複線性a:T→𝔄，
{a(f)*,a(g)}=A(f,g)1、{a(f),a(g)}=0；*是共軛線性involution，不混self-dual Γ條件。
若各A_C不同，不能以挑一面、換field或*來補救守恆。

固定Q=A/2的gauge-invariant Wick trial：ω(1)=1，creation／annihilation數不同的normal-ordered moments為0，

$$\omega(a(f_1)^*\cdots a(f_m)^*a(g_m)\cdots a(g_1))
 =\det[Q(f_i,g_j)]_{i,j=1}^m.$$

其他排列按同一CAR處理；須核對一致性、正性與歸一化，不另選正部分、vacuum或covariance。
母契約的Gram正性、generic CAR／Fock／Wick存在性都只記「按構造成立」，不是本題研究成果。
Q由同一A固定，不是新調參state；本版仍未提供能量、physical vacuum、Dirac dynamics或continuum來源機制。
即使Wick trial存在，也不能抵消守恆、microcausality或Green失敗。

## 9. 舊障礙前提、反補洞與停止

| 舊障礙前提／環節 | 本版固定選擇；不是完成判定 |
| :--- | :--- |
| 原P的retarded支撐 | 保留，必須證同一初值/source response符合 |
| 全T可逆K又有非零齊次核 | 不採；K_int只在I施方程，M是初值加source augmentation，兩者不能混稱 |
| G_A=G_R† | 明採數學counting adjoint，非靠η換名逃避 |
| iH(G_R−G_A)的零對角form | 不採該form；獨立假說為IB.S1，A則由固定初值配對拉回，兩者仍須IB.S2對接 |
| Sector／η方向混合 | 沒有新增fiber或transport；沿用CF-01係數不表示已導出spin或mass mixing |
| L入口 | 只在§3固定線性統計；β及所有下游不另讀L，不能從上游解碼排名 |

所有inverse／trace／smearing／contact／comparison規則在本版固定，不得依A或C_G的譜、sign、正部分、
是否守恆或成功挑B、面、pairing、test、Sol、t、domain或norm；不用譜projection／容差刪模。
不得新增time間隔、metric、frame／transport、spatial lattice／shift或邊界state；需要時先停止並另審primitive。
規格GO之前不做本試作研究；GO後任何必要義務失敗即保留本版FAIL，不在同版換式補救。
本次只請審規則是否完整／合規、判準是否可失敗及來源披露；不請reviewer提前驗算案例或代選替代K。
沒有新的數值／符號科學計算、程式枚舉、RNG／撒點、producer、raw／sealed、seed、主機量測或receipt。
原始輸入、P0.1、P0.2問題均OPEN，既有研究稿／契約／B-01不改，formal／E0、A／B、UNKNOWN隔離不變。
