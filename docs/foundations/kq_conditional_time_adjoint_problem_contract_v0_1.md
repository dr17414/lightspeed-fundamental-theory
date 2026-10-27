# X-KQ-COND-TA-P0.1 — 外加時間序與Hermitian資料下的同源構造問題

狀態：**【提案／只定問題，待exact-head獨立複核】**。2026-10-25 Asia/Taipei。
Problem ID `X-KQ-COND-TA-P0.1`；新model ID **NONE**。
**探索軌，不具 §5.2.1(v) 依據資格。**
本檔不給K、Green／CAR公式、state、物理adjoint的具體實現、材料／ansatz或證明策略。
固定的是新增primitive的型別、來源限制、工作域與可失敗的交付要求。

## 1. 與原問題分帳、起草來源與開始條件

原始輸入問題[X-KQ-1P1-P0.1](kq_1p1_construction_problem_contract_v0_1.md)保持**OPEN**；
本輪停止沿它新增試作，依其§5另立本conditional問題，不回改其工作域或答案。
[OP-01](kq_order_polynomial_attempt_study_v0_1.md)的失敗與G_swap／ordinary-adjoint限定障礙
經#98 r2 exact-head `ae8d0d3b91d6fc3248f22fc18b362b451aba8c41`／tree
`6b9cf7d32bee0a30f006d820e225aaea558e28c0`取得GO，CI #304成功並原樣合併main
`be55a80a8bbc80f1d5d371ada9c081f78789e094`，merge tree相同，parent1ac30ceb。
Git committer UTC2026-10-24 17:09:47／台北2026-10-25 01:09:47；不是授權或研究開始時間。

操作者同意上述合併授權，並轉交Claude同意conditional方向及四項起草意見。
本稿承接兩側障礙、primitive反補洞、非平凡性及結論隔離四點；不把方向意見當成本契約GO。
隨本提案提交的追加接觸帳以EXP-0095逐字記#98 r2本人申報，
0096記合併、來源、原文閱讀及本稿起草範圍；其整合審查也屬下述開始條件。
ACT-X-0001仍引用生效SHA `0c386716701589c9a6b0b799636a808aacb9ade5`，限紙上X-C。

**本契約及其primitive／接觸登記取得exact-head GO、必要CI成功、原樣合併main並核對tree前，
不開始本題的K／state／CAR橋接實作選擇、證明策略或構造推導。**
只涉紀錄PR的reviewer申報沿既定程序隨下一交付追加，不形成遞迴門檻；
此程序規則不豁免科學曝光、primitive事前固定或UNKNOWN來源審查。

## 2. 六欄與事前固定的conditional輸入域

| 六欄 | 本題 |
| :--- | :--- |
| 問題 | 在且僅在本稿明列的新增資料Ξ下，能否交出非局域K→同一K的retarded inverse→總CAR form→同源正state的完整鏈？ |
| 定義域 | 下述D_Ξ；底層投影涵蓋整個原D_KQ，不依未來輸出縮域 |
| 輸入 | P的order／count，外加preferred時間序L，以及全問題一次固定的二維Hermitian參考資料R₀ |
| 證據 | 後續須交全輸入規則、型別／容量／自然性、完整同源識別及紙上證明；本稿不預填存在性 |
| 未證橋接 | primitive是否足夠、sector非平凡性、物理adjoint／CAR／state、dynamics及continuum全部未交 |
| 否定／停止 | 僅按明定類別報障礙；超出Ξ或需執行時停止另審，不把conditional答案當原問題答案 |

沿用原契約的D₁與q(P)：D₁由唯一realizer orbit定義，
q(P)=#{(y,x):y≺x}，D_KQ={P∈D₁:q(P)≥2}。
**底層P不再刪減**，包括三葉star與鏈等非流形輸入。

在本題層面、任何構造輸出之前一次固定參考資料
R₀=(E₀,h₀,η₀)：dim_C E₀=2，h₀正定Hermitian，
η₀為h₀-self-adjoint involution，正負eigenspaces各一維。
它是外加資料，不由P導出；所有P與N使用同一R₀，沒有per-P／per-event的η調整。
R₀的共同unitary換基只是同一資料的表述，不能用不同N的換物理資料冒充換基。

令LE(P)是延伸strict P的全部strict total orders。固定

$$D_\Xi(R_0)=\{(P,L,R_0):P\in D_{KQ},\ L\in LE(P)\},\qquad
\Xi=(L,R_0).$$

L被明示解讀為**外加preferred時間序**，包括原P不可比事件間的新排序；
這是conditional physical primitive，不是從I-UV orbit免費選出的代表。
L沒有時間間隔、單位或proper time，也不是已證的Cauchy面／foliation或空間格點。
有限P有linear extension，因此此擴充未因額外成功條件刪掉底層P；
非空與尺寸無界仍由原契約的C_m（m≥3）輸入族支撐，不是K存在性證明。

**主問題完成量詞：** 一條有限描述、來源與容量已固定、跨N一致的規則，
對每一個P∈D_KQ、**每一個**L∈LE(P)及R₀的全部共同換基表述，
交出§5第1–4項與§6非平凡性，並對§4的全部structured isomorphisms自然。
失效狀態／OPEN不算正面完成。不存在「先替每個P挑一個有利L」的成功量詞。

跨N要求同一規則及R₀，不逐N換law、配對或state；明列的自然count依賴可被審查。
不預設induced embedding／nested-region inverse或state相容，仍須逐項列OPEN。
若要減少P、限制L或改R₀型別，須在新構造之前修契約另交exact-head審查，
不得看過失敗後改domain維持成功；只報事前登記子類時須明標局部結果。

## 3. Primitive、來源與容量：不把physical資料改稱免費scaffolding

| ID | 型別／來源規則 | 容量與禁止選擇 |
| :--- | :--- | :--- |
| CΞ-ORD／NUM | P的strict order、count；原L0 | 不含coordinates、physical尺度或hidden evaluator資料 |
| PΞ-TIME | 外部在K／form之前給定一份L∈LE(P)；本題對全部L量化，不設挑選器 | 至多N!種次序，輸入資訊上界log₂(N!) bits；是實際新增資訊，不能報零容量／由P湧現 |
| PΞ-HERM | 全問題一次固定的R₀；η₀是新增的conditional Hermitian／adjoint方向資料 | O(1)個固定維度物件，沒有per-P／per-event矩陣表；不得從K、Green或A的符號／譜求得η₀ |
| QΞ-L2 | C、free linearization、以下完整test的數學pairing及合法unital *-algebra型別 | 明示L2，不能從其存在推出fermion物理；不把PΞ-HERM藏進「標準L2」 |
| RΞ-L3 | 後續K、contact、smearing／CAR、state等規則的完整有限描述 | 次數／function family／參數／prescription來源須先申報；無逐P擬合、lookup、負模依賴或自由per-edge表 |
| CΞ-COMPARE | §8的原文比較只作假設對照 | 不把其現成coin／shift／格點K當作已完成本題來源審計或formal資格 |

PΞ-TIME的來源協定是：把L作外加已給資料，對**全部合規輸入**證同一主張。
不是由作者以某個最佳化目標逐P產生L；沒有RNG／抽樣／篩選或依A挑選的分支。
若後續主張某種實際資料取得／測量協定，須另交其時序、獨立性與容量，不由本稿預先批准。
輸入O(N log N)資訊與可調模型容量分帳；即使沒有可調scalar，也要披露額外時間序的容量。

η₀所給的indefinite pairing不是正Hilbert內積；h₀在固定二維空間的正性，
不證明總CAR form正性或fermionic adjoint已導出。h₀用於定義型別與換基，
η₀的正負方向不作A的正負譜資訊。
本題**不額外給**per-event frame、per-edge transport、spatial adjacency／shift、Clifford乘法、
Hamiltonian、metric、density、physical時間步、boundary state、positive CAR form或covariance W。
需要任何一項作新的獨立輸入時，停止本版本，先另立／修訂conditional契約。
若能由Ξ按明文規則導出，仍須交來源與容量證明，不能僅改名為derived。

## 4. 自然性與兩側障礙分帳

### 4.1 Structured isomorphism，不能冒充原始輸入的自然性

f:P→P′須保持原order，且是L→L′的order isomorphism。
參考資料換表述由共同unitary V:E₀→E₀′給出，保持h並滿足Vη₀=η₀′V。
各事件使用同一global V，映射須滿足identity與composition法則。
後續須明寫這些映射在field、source、test、K／Green、CAR代數與state上的誘導作用與交換圖。
不只檢查Aut(P)。依reviewer在#99 r1的提示：有限total order的事件自同構平凡，
兩個(P,L)間若有事件同構，也只能是依L排名的唯一對應。因此事件重標記自然性
無法排除任意排名演算法，不再對此類演算法提供實質限制；共同V的fiber協變義務仍在。
本題不准以排名生成sector差異，L進入K的方式限於下列§4.4，仍須交完整交換圖。
這項限制與§6的實際證明共同把關，不能宣稱自然性或限制本身已保證非平凡性。
只對(P,L,R₀)自然，比只給P的原要求使用更多輸入，不能把這個結果升回原問題。

### 4.2 Sector側：本題選擇的是明示增強輸入，沒有刪掉star

G_swap障礙使用了未附時間序P_*的完整S₃ automorphism作用。
本題的L區分三片葉子的時間序位置，原三循環不保持同一L，故不是該structured物件的automorphism。
這只指出原障礙的一個前提已改變，**不證**某K可有二維block span、所選R₀足夠，
也不稱由原始資料得到intrinsic sector。所有L仍須涵蓋，不能挑選某個時間排序維持成功。
sector義務仍是§6(b)，其來源可用到明示PΞ-TIME／HERM，但必須交出其實際作用與自然性。
本版本不另加local fiber或transport；如確需它們，先停止並另審，不能只說「已conditional」就任意加資料。

### 4.3 量子橋接側：有η不等於已逃出ordinary-adjoint障礙

OP-01的另一障礙前提是：G沿order retarded、diagonal Hermitian、ordinary adjoint及固定的總form prescription。
本題保留原order上的retarded要求；後續須逐項列出該障礙的其餘前提是否仍成立、哪一項改變、來源何在。
η或時間序的存在本身不解除障礙，單純換基／改名字也不構成解法。
indefinite pairing的矩陣、未識別的裸Green差、或η-adjoint，都不能直接當成正CAR form。
unital *-algebra的*、物理field adjoint、數學Hermitian adjoint及總form必須型別分開並交同源識別。
只處理這一側，不能宣稱§4.2的sector義務也已完成；反向亦然。

### 4.4 r2事前選定的非局域時間序依賴類

本題選reviewer所列(ii)，不選只看因果區間內L的類別，亦不縮D_Ξ。
以下只限定容許的規則類，沒有選任何係數、K、adjoint／CAR實現或state。
對原order pair y≺x，令閉區間[y,x]_P={z:y≼z≼x}，並定義

$$S_{xy}(P)=\{z\notin[y,x]_P:(z\parallel_P y\ \text{或}\ z\parallel_P x)\}.$$

只容許讀取這些z與兩端點的L先後關係；不讀z彼此的L順序或全域rank。
對每個z以σ_L(z;y,x)∈{pre,between,post}記z<_L y、y<_L z<_L x或x<_L z。
用τ_P(z;y,x)=(rel_P(z,y),rel_P(z,x))分類，其中rel∈{≺,≻,∥}，
令n_τσ(P,L;x,y)是S_xy中同時屬該order型別與時間位置的事件數。
L對K的**全部**依賴限定為

$$K(P,L,R_0)(x,y)=K^{\rm ord}(P,R_0)(x,y)
  +\sum_{\tau\in\{\prec,\succ,\parallel\}^2}\sum_{\sigma\in\{pre,between,post\}}
  n_{\tau\sigma}(P,L;x,y)\,M_{\tau\sigma}(R_0),\qquad y\prec x.$$

K^ord完全不讀L，須對原P同構自然；非order非對角block仍為零，diagonal亦不讀L。
M_τσ是全問題只固定一次的endomorphism，跨P、N、pair、L皆相同，依共同V作共軛協變；
允許型別至多27個2×2矩陣，即至多108個complex scalar entries的上界，
這只是表述容量上界，不把不可能型別或共變限制算成已獨立參數。
其實際來源、參數及值須在後續任何構造輸出之前另行完整登記；本契約不預選它們。
不得把M_τσ改成逐P／逐pair的表、讓K^ord暗讀L，或把其他L依賴藏進normalization。
依賴n_τσ只可用上述固定線性和；禁止奇偶、模k、count／rank查表、非線性門檻、
依輸入挑矩陣、n_τσ的乘積或再以輸出調整係數。不得由這些統計重建排名後作上述算術；
准許的只有這份已明列的order型別／時間位置線性彙總，而非任意全域rank演算法。

這個conditional物理解讀是：兩個因果端點之前、之間、之後的preferred切片環境，
只以因果鑽石外、與至少一個端點類空的事件之order型別作固定線性彙總。
即使兩端點之間沒有其他L事件，也不能據此把切片前後環境默認刪去；三種位置在此一次列全。
它刻意容許鑽石外的preferred foliation資訊，是新增的非局域時間序自由度，
不是由P導出的局域時間或已證物理機制；不增加原P的causal propagation edges。
固定線性／型別彙總是事前選定的探索限制，不稱由物理原理唯一導出，亦不保證§6(b)成立。
L原有容量仍是§3的log₂(N!)上界，容許讀取的統計限制不把primitive容量改報為零。

reviewer另提示：若block只依賴(P限制於[y,x], L限制於[y,x], R₀)的同構型，
三葉star的三個兩點區間型別相同，會重現一維span障礙；這個命題另要求區間型別自然性，
不能把「只限制L的讀取、卻另允許區間外P資料」混稱同一假設。
本段與§4.1的數學觀察來源均為reviewer提示，本稿只據此限定問題，未交正式證明。
後續研究稿若採用這些觀察作承重論證，須先列完整假設並補正式證明，不記盲發現。
更改本依賴類，包括讀取更多L資料或改彙總方式，須在新構造前修約並重新exact-head審查。

### 4.5 r3：所有下游規則共用的、更窄的L依賴類

針對reviewer指出的下游漏洞，本版選(i)的**更窄子類：不再直接讀L**。
§4.4是整條鏈唯一容許將原始L轉為規則資料的入口，且只能在K的明列線性彙總中使用。
K以後的規則不另讀L、其rank／comparison table，亦不重新取得n_τσ或其他L統計。
它們只可經由合規K及下表的同鏈上游物件承接L的影響，不新增時間序特徵通道。
這是事前的規則類限制；沒有選定任何下游公式，也不保證此更窄類能完成主問題。

| 規則 | 除P／R₀外，容許承接L影響的上游物件 |
| :--- | :--- |
| G_R與contact／boundary／source規則 | 同一合規K；須滿足§5的inverse／composition與來源義務 |
| G_A及物理adjoint／pairing規則 | 同一K、G_R及已按本節取得的source／contact；不另給L-adjoint表 |
| smearing／test、projection／quotient規則 | 同一K及已按本節取得的Green／source物件；完整T及§7反補洞要求不變 |
| F及總CAR關係 | 同一G_R、G_A及已按本節取得的adjoint／pairing／smearing／contact；不能另帶L或時間統計參數 |
| state規則與額外dynamics主張 | 上述同鏈K／Green／CAR物件及已按本節取得的資料；不能由L另造covariance或state選擇器 |

對每個規則D須在獨立規格中列明typed factorization
D=widehat D(P,R₀;已逐項列名的合法上游物件)，並交完整公式、來源及依賴圖。
若兩個L在固定P／R₀下給出相同的該規則上游輸入，D必須相同；不能暗中保留L參數。
L仍可用於輸入域／structured morphism的敘述與全量詞證明，這不授權規則重新讀取它。
primitive容量仍照§3披露，不因下游不再直接讀取而改報零。

**禁令適用整條鏈**：不得直接或從K／Green／其他上游物件解碼／重建L排名、
時間位置count或標籤，再作奇偶、模k、查表、非線性門檻、count特徵乘積，
或據此挑adjoint、smearing、test、F、state或其係數。把違禁資料藏進上游物件名稱不算合規。
後續須逐式審計所有係數／選擇器的來源，不能只以「透過K」宣稱通過。
禁令針對額外的排名／count特徵處理；它不把同一inverse、adjoint、CAR／state恆等式所需的
矩陣composition／inverse一概禁止，但每一運算須事前列明其型別與代數用途。
展開合法上游算式後出現count乘積，不因此自動合規或違規；須檢查是否在履行上述同鏈恆等式，
而非解碼時間序後產生新的規則係數。無法交代這項來源區別時，停止該規則，不補設例外。
§5.3的非恆定／同源識別與§7的不看譜均另行適用；事前固定、不看譜不能豁免本節禁令。

更改任何一項下游依賴類，包括重新直接讀L／n_τσ、增加時間特徵或放寬本表，
必須在新構造之前修契約並重新交exact-head複核；失敗版本保留，不得在同版中放寬補洞。

## 5. 第一階段實質交付：仍須完成整條同源鏈

固定完整field／test型別T_P=C^P⊗E₀，dim_C T_P=2|P|；
以h₀作counting Hermitian pairing來敘述數學型別，不預填物理adjoint或A的公式。
source／domain、物理smearing及所有projection／quotient規則依§7事前明列，不能看輸出後選。

1. **K與型別／來源。** 同一有限描述規則對整個D_Ξ給具名kinetic物件，
   明列全部自由選擇、primitive的作用及原order支撐；說明R₀／時間序沒有偷帶K或已知正W。
   區分物理Hermitian資料的外加與真正由P導出之量，不以block rank代替來源證明。
2. **同一K的Green。** 交retarded inverse或精確聲稱的composition identity，
   source、contact、boundary與適用domain全部明寫。L不增加原P的因果關係，
   不能因兩事件在L有先後就把原本不可比者當成傳播pair。evolution kernel不能冒充inverse。
3. **總CAR form。** 交事前固定test／adjoint／smearing／field ordering與實際CAR關係，
   證它們符合下述可檢查的同源條件。在完整T上證A≥0，不能以投影或外加positive自由度造假。
4. **同源state。** 實際state由同一輸入鏈的事前固定規則決定，證正性、歸一化及與同一K／Green／CAR的相容。
   有正A時generic Fock／S=0或任意contraction的存在性，只記「按構造成立」，不算state來源機制。
5. **額外主張分帳。** 若聲稱dynamics，交實際代數作用與相容性；unitarity、stationarity、
   正能量、vacuum、Dirac／massless及continuum各自列證據／OPEN，不能由有限矩陣正性自動推出。

主問題正面完成須實質交出1–4、§6以及§8的差異證據；不能只把前提寫到足以包含答案。
部分結果記「具體定義／限定障礙已交、待複核」或OPEN，不由§5某一項通過升格整條鏈。
只排除一個構造類G時，先明定G及全部假設，不報所有Ξ下構造均不可能。

### 5.3 總form與Green的同源條件（r2明定）

後續須在看所得form的符號／譜之前，完整宣告一個有型別、可計算及可審查的規則
A=F(G_R,G_A;Ξ)。須寫出F的定義域、值域、全部配對／adjoint／smearing／contact資料，
及G_A由同一K、G_R與Ξ取得的規則；不在本稿選定F的具體實現。
此處Ξ記號不授權直接使用L：G_A、F及所有配對／smearing／test／state一律受§4.5限制；
F的實際依賴須展開為該節所列的P／R₀及合法上游物件，不能以Ξ作隱藏的時間序入口。
只寫「存在F」或把事後得到的A重新命名為F不合格。每次換K，必須從該K重求Green，
再用**同一F**決定A，不能把獨立的kinematic CAR沿用並聲稱已對接。

可核查的必要條件包括：列明K→Green→F各步的定義／恆等式及structured自然性交換圖；
在事前固定、保持Ξ與test型別的合法K比較類上，交F經Green對K非恆定的數學證據。
比較類及變化不得依A是否正來篩選；至少須有兩個合法比較對象使所得form不同。
這不要求F對K單射，也不要求每個K變化都改A；但語法上帶Green參數而實際忽略它不合格。
非恆定仍只是必要條件，不替代實際CAR／field adjoint與同一inverse的代數識別證明；
只把某個K-dependent scalar乘在無關正W上，也不能以此取代該識別或規避§3／§7。

**所有與K無關的CAR prescription均算外加positive CAR form**，包括對全部事件直接指定
{ψ(x),ψ†(y)}=δ_xy I_E、再只讓K控制演化的作法；它會觸發§3停止條件，
不得改稱RΞ-L3或以A=I／rank=2|P|充作本題的§6(d)成果。
若採「kinematic CAR先給、K只控制動力學」的同源概念，那是另一條問題鏈，
必須另立契約說明，不得在本題混用。本條不先判定任何具體F能否通過。

## 6. 探索最低非平凡性：至少保留原契約強度

以下仍不是C3b／C5／C6／C9，也不回流formal；(a)(b)(d)對每個完整conditional輸入要求，
(c)在整個D_Ξ的跨尺寸family要求，無單例／空域豁免。

(a) **傳播。** G_R至少一個x≠y非零block；全部非對角非零block僅在原P的y≺x。
只有contact或沿L新增原P不存在的causal edges不算通過。

(b) **非單一tensor化約。** K非對角blocks的complex span維數至少2。
排除存在scalar kernel h_Ξ及單一2×2 M_Ξ使全部K(x,y)=h_Ξ(x,y)M_Ξ，
即使M可依完整輸入或N選擇也不放行。只改diagonal不能補救。
共同global GL(2,C)換基保留此維數；不允許新增per-event基底調整來偽造差異。
L依賴必須逐項符合§4.4；藉排名奇偶／模數／查表得到span≥2仍判失敗，不能只報維數。
仍須另交primitive／sector來源解釋，兩個數值獨立blocks不是Spin／chirality已導出的證據。

(c) **K自身非局域。** 使用原P的最短directed Hasse-hop距離d_P。
不存在與P／N無關的有限r使所有非對角K支撐均在d_P≤r；每個r須有D_Ξ內解析witness，
在d_P>r的原order pair上K≠0。不能只讓inverse變dense，也不把L的rank差叫成原Hasse距離。

(d) **正form的非零與增長。** 在完整T上證A≥0之後，正Hilbert商H_A的維數至少|P|，
有限維等同rank A≥|P|。須明列test維數、radical／零方向，不外加無關自由度補rank。
A不正時不能將其indefinite rank或刪負方向後的維數報成通過。

## 7. Primitive與所有下游規則的不看譜原則

L、R₀的來源與容量先於構造輸出；後續K／contact、source／test、物理adjoint、
pairing、smearing／CAR與state規則均須在相應輸出之前書寫並版本化固定。
不能依A的正負號、譜、負模位置或個數逐P改primitive、換pairing、縮test、改normalization或挑L。
配對的來源理由不能僅是「這樣A就變正」。另挑一個正W、以譜截斷或刪負模補洞仍禁止。
canonical零radical商也只能在完整T已證A≥0後使用，不消除原完整T的正性與(d)義務。

失敗版與已見資訊均保留；新規則須另版事前登記並說明曝光，不能改寫同一成功主張。
新增輸入／改工作域／更換primitive型別或需要數值／symbolic／toy執行時先停，另交契約／授權。
同為conditional不代表可以免審增加gamma、Cauchy面、spatial frame、density或任意transport。

## 8. 什麼才算學到東西：預定比較與最低差異證據

本題不以「給了Hilbert空間」「有CAR」或「引用既有unitary walk」本身當新結果。
預定只用兩份原始文獻作第一輪比較；下表限於已讀段落，不是完整文獻回顧：

| 原文與本輪實讀 | 已核對的前提定位 | 本題先固定的差異／剩餘義務 |
| :--- | :--- | :--- |
| Arrighi–Nesme–Forets，[arXiv:1307.3524v1](https://arxiv.org/pdf/1307.3524v1)，摘要／引言、§I開頭 | 給定格點、時間步、Dirac矩陣資料，討論均勻unitary walk與連續解比較 | 本題沒有spatial grid／shift、完整Clifford資料或physical步長；須交所有不規則P及全部L的同源鏈，不是單粒子walk即算CAR／state已解 |
| Farrelly–Short，[arXiv:1303.4652v1](https://arxiv.org/pdf/1303.4652v1)，摘要、§I、§II起段 | 給定離散lattice與fermion modes／CAR，考慮causal unitary演化 | 本題不把unitary或正CAR先放入primitive；需由同一K識別總form與state，不能用已給CAR的演化定理代替該識別 |

本題已新增preferred L與固定Hermitian資料，並不因此比文獻的全部輸入「更少」。
上表只是具體輸入欄位差異；沒有最小性定理、資訊量偏序或新穎性查全。
原文工具回傳也含公式，已記EXP-0096；本稿不採其coin／K／shift公式作本題構造。

後續的**實質完成**至少必須提供：
- §5完整同源鏈及§6，而非只在規則格點／單一容易poset重述既有構造；
- 覆蓋全部D_Ξ的同一規則，並交spatial lattice／shift／已給正CAR等未輸入物件確實沒有被暗中加入的來源審計；
- 與上述原文逐項假設／物件mapping，指出新的uniform不規則域對接、可證的輸入差異或精確限定障礙，至少一項有完整數學證據。

若其實只是已知格點模型的重標記或通用CAR存在性，必須記「已知構造轉寫／校準」，
不計為本題的實質研究完成。若靠導出格點／adjacency才能引用既有模型，須真的證明導出及適用域，
不能把所需空間資料偷偷變成primitive。未用到η或L也必須如實報告冗餘，不能稱已證它們必要或最少。
完整新穎性判定與physical continuum結果是另行義務，不由本題成功自動取得。

## 9. 結論標示、formal隔離與停止

所有成功／失敗／局部結果一律標「**在外加Ξ=(L,R₀)之下**」，附實際量詞與來源。
不得回寫為原始輸入的存在／不可能答案；原問題保持OPEN，OP-01兩項障礙各保留原作用域。
本題及其產出不決定C9／C10的core、test、projector、evaluator、prescription、排除規則或容差。
formal回用仍需另案handoff、exposure mapping、新prereg及合資格獨立／blinded審查；
讀原文或與其作mapping不提高D.1第8項A／B資格，不能作§5.2.1(v)依據。

只限紙上。無模型程式、symbolic／toy執行、RNG、撒點、producer、raw／sealed、seed、
科學量測、主機消費或receipt；既有regression／integrity僅作repo檢查。
不使用既有probe／planted／witness／run1成功模式選primitive或law；UNKNOWN回流無法排除時停止對應分支。
E0、item7不可ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING及原資料隔離不變。

## 10. Exact-head複核要求

請reviewer核對：兩側障礙是否分帳；底層D_KQ與全部L的量詞；R₀一次固定的型別／容量；
structured isomorphisms與原始自然性的差別；是否真能禁止逐P補洞；§6是否至少保留原強度；
§8的來源定位與實質完成是否非真空；結論／formal隔離、接觸申報及構造開始的先後。
本次只審問題，不要求reviewer替作者選K、state、CAR公式或證明策略，也不預判Ξ足夠。
