# CF-01 v0.1 — 全域sector判準成立，但固定η-adjoint橋接失敗

狀態：**【具體紙上試作／限定解析待exact-head逐式複核】**。2026-10-28 Asia/Taipei。
Problem ID `X-KQ-COND-TA-P0.1`；探索model ID `X-KQ-CF-01-v0.1`。
**探索軌，不具 §5.2.1(v) 依據資格。所有結果只在外加Ξ=(L,R₀)之下。**

## 1. 結果、固定規格與證據等級

依[定案契約](kq_conditional_time_adjoint_problem_contract_v0_1.md)及先行獨立提交的
[CF-01規格](kq_conditional_foliation_attempt_spec_v0_1.md)，本稿不改任何規則。
基線為#99合併後main `5e5e819ff76cedac84b1be9c20cac5eb1a047842`／tree
`e925b0e4be083478f0372b98994e9b837d45ab53`。交付順序：三帳先登EXP-0101／0102，
再獨立固定規格與作者EXP-0103，之後才提交本研究及EXP-0104。
本稿不用本地checkpoint SHA作公開證據；公開後須逐stage回報可抓取的commit與tree。
Git只能證版本先後，不能證盲性；§1及EXP-0103已披露作者先有腦中論證與reviewer提示。

本版在**每個P∈D_KQ及每個L∈LE(P)**交出自然K與同一K的retarded inverse，
契約§6(a)(b)(c)成立；(b)不限於star單例。固定總form C=iH(G_R−G_A)有正負方向，
故(d)失敗，沒有任何正歸一state，固定Wick trial也失敗。這不是完整同源構造。
另證：在本契約的global R₀自然性下，K必與H交換；若G_A選η-adjoint，便退回ordinary adjoint。
該觀察只排除明列的adjoint／Green-difference類，不是所有F、所有Ξ或spinor的不可能定理。

## 2. 記號、實際型別與來源

全程用規格的完整T=C^P⊗E₀、counting h、H=I⊗η₀，h第一槽共軛線性。
η₀的正負線是已給R₀資料，不由所得form的譜挑選。†是h-adjoint，sharp是HX†H，
CAR代數的*是另一個形式involution；不能把三者混同。

### 2.1 七種(τ,σ)的證明

固定y≺x，z∉[y,x]且與至少一端不可比。
若z∥y，則不可能x≺z，否則y≺z；所以rel(z,x)只能是≺或∥。
若z∥x，則不可能z≺y，否則z≺x；所以rel(z,y)只能是≻或∥。
因此τ只有(∥,∥)、(∥,≺)、(≻,∥)。第二種有z<_Lx，只可pre／between；
第三種有y<_Lz，只可between／post；第一種三位置皆容許，共七格。

這些格確可在原工作域內出現：(∥,≺)用二葉star及兩種葉序，(≻,∥)用其order dual；
兩者q=2，兩個realizer的葉序相反，在葉交換及S₂下orbit唯一。
(∥,∥)用三點鏈與一個孤立點的disjoint union，q=3；其二序realizer中孤立點不能插鏈中，
否則另一序要反轉它與兩側鏈點的關係而破壞鏈，故只能在兩序中分居鏈的兩端，orbit唯一。
外加L只需是linear extension，可以把該孤立點放在選定causal pair之前、之間或之後。
所以七格均有D_KQ內的輸入，而不是27個獨立矩陣。規格的七格已固定，無重新選值。

### 2.2 CF-01的實際來源與容量

K^ord=I+Z⊗I+Z²⊗η₀；M只有規格列出的√2η₀、√3η₀與0，沒有可調scalar。
這是作者固定的L3 law，非從P推出的物理定律或最少primitive定理。
L的新增資訊照契約上界log₂(N!)披露，R₀全問題一次固定；不用任何成功probe、raw／sealed、
physical lattice／shift、per-event frame或per-edge transport。
Π_±只標給定η線；沒有譜截斷、test縮減、加入正W或η逐P調整。

## 3. 自然性、完整inverse與§6(a)(c)

### 3.1 全部structured isomorphisms

對契約的(f,V)，令U:T→T′為U(ι_xv)=ι_{f(x)}Vv。U是h→h′的unitary，H′U=UH。
f同時保持P、L，所以Z、Z²、S_xy及七種count在f下對應；M亦隨V共軛。
故K′U=UK，B′U=UB。由固定多項式得G_R′U=UG_R，由adjoint得G_A′U=UG_A，
再得C′U=UC。因此A′(Uf,Ug)=A(f,g)，source／contact／smearing Id也相容。
生成元映射a(f)↦a′(Uf)保持CF.S2與*，且固定Q=A/2的moment prescription同樣協變；
這只是關係／候選moments的相容，不宣稱它正。identity及composition由U的定義直接成立。

reviewer提示的事件側弱化也可直接驗證：total order同構必把第k元素送到第k元素，
故事件自同構平凡、若有同構也唯一。本版的自然性證明不據此偷渡任意rank演算法；
實際law只用規格的線性count，沒有排名奇偶／模數／查表。

### 3.2 同一K的two-sided inverse

B=K−I僅沿原strict order支撐。B^j非零項須有j步strict鏈，至少j+1個不同事件，故B^N=0。
因此

$$G_R=\sum_{j=0}^{N-1}(-B)^j,\qquad KG_R=G_RK=I_T. \tag{CF.1}$$

這是完整T的identity，不縮domain、不加boundary輸入。乘冪仍沿原order，
G_R diagonal為I；L在不可比事件間的排序沒有變成傳播edge。
若y≺x是cover，則B^j(x,y)=0（j≥2），所以

$$G_R(x,y)=-(I+u_{xy}\eta_0),\qquad \operatorname{tr}G_R(x,y)=-2. \tag{CF.2}$$

有限P只要有可比對就有cover；D_KQ的q≥2更保證這一點。故每個完整輸入都滿足(a)。

### 3.3 K自身的非局域witness

對每個y≺x，tr K(x,y)=2，因tr η₀=0；所以K在每個原causal pair上非零。
取C_m（m≥3）。鏈的total-order extension唯一，realizer orbit唯一，q=m(m−1)/2≥2，
所以它在D_KQ。首尾的directed Hasse-hop距離m−1無上界，K首尾block仍非零。
這證(c)，不是僅inverse變dense，也不使用L rank差冒充原Hasse距離。

## 4. §6(b)：對整個工作域的二維block span

記r_xy=Z²(x,y)，p_xy與s_xy均為規格count的非負整數；u=r+√2 p+√3 s。
1、√2、√3在Q上線性獨立：若a+b√2+c√3=0，c=0時立即得a=b=0；c≠0時平方得
3c²=a²+2b²+2ab√2，故ab=0。a=0或b=0均由2、3的質因數次數矛盾排除非零解。
因此兩個整數三元組(r,p,s)不同，就有不同u。

若P有三點strict鏈，某causal pair有r≥1，另一方面任一cover的r=0。
兩者三元組不同，故u不同。

若P沒有三點strict鏈，則所有causal pair都是cover；每個source y為minimal，每個target x為maximal。
對minimal y，每個z<_Ly都與y不可比，亦不在[y,x]，所以p_xy正是y之前的L事件數；
對maximal x，每個x<_Lz都與x不可比，所以s_xy正是x之後的L事件數。
此處只是證明count差異的等式，不是把rank讀取加入規則。
因q≥2有兩個不同causal pairs：若sources不同，它們的p不同；若sources相同，targets必不同，s不同。
由整數線性獨立仍得u不同。

η₀有正負本徵線，所以I、η₀線性獨立；u₁≠u₂時I+u₁η₀與I+u₂η₀也線性獨立。
全部非對角blocks本來都在span_C{I,η₀}，所以

$$\dim_{\mathbb C}\operatorname{span}\{K(x,y):x\ne y\}=2
\quad\text{對所有 }(P,L,R_0)\in D_\Xi. \tag{CF.3}$$

因此(b)全域成立，不只star。這個證明甚至不需D₁的額外性質，但本題量詞仍照D_KQ，
不把外加L的結論升為原始輸入結果。
在三葉star的pair(a_i→b)上，r=0、s=0、p是其前面的葉數，故block為I+√2 pη₀。
它使用的正是契約允許的線性foliation位置；不是spin／chirality，也沒有正負sector mixing。
star觀察的方向來自reviewer，作者在規格前已有分情形預想，非盲發現。

## 5. η-adjoint、總form與同源檢查

### 5.1 Dual kinetic與Hermitian型別

所有K blocks為I、η₀的線性組合，所以[K,H]=0，亦有[G_R,H]=[G_R†,H]=0。
η-adjoint X^sharp=HX†H為involutive anti-automorphism，故

$$G_A=HG_R^\dagger H=(K^sharp)^{-1},\quad K^sharp G_A=G_AK^sharp=I,
\quad G_A=G_R^\dagger. \tag{CF.4}$$

G_A是advanced，diagonal I。它是dual K^sharp的inverse，不是對非self-adjoint K硬稱第二個inverse。
本版所謂η-adjoint因交換性，**實際沒有改變ordinary-adjoint前提**。

即使不用上述交換性，規格總form也滿足

$$C=iH(G_R-G_A)=iHG_R-iG_R^\dagger H=C^\dagger. \tag{CF.5}$$

所以CF.S2是Hermitian型別相容的charged CAR trial；但正性尚須獨立檢查。
用同一inverse可得

$$K^\dagger C K=iK^\dagger H(G_RK)-i(K^\dagger G_R^\dagger)HK
 =i(K^\dagger H-HK). \tag{CF.6}$$

這實現規格的Green恆等式檢查，沒有另插正W。它是L3識別的代數驗證，
不等於物理CAR已從P或微觀場導出；完整正性／state更不能從此等式推出。

### 5.2 F真的依賴同一K，仍不代表正性

在先定比較類K_t=tI+B、1≤t≤2，用同一規則得G_R(t)=Σ(−1)^jt^{-j-1}B^j。
cover上G_R(t)(x,y)=−t^{-2}(I+uη₀)，故

$$C(t)(x,y)=-it^{-2}(\eta_0+uI). \tag{CF.7}$$

η₀+uI不可能為零，故C(1)與C(2)不同。P、L、R₀、test及M全不變，F也全不變，
只依同一K_t的Green變動；不是語法上帶Green卻忽略它。
合法比較指kinetic／primitive／依賴規則合規，不把正性當比較類的篩選條件。
這證必要的非恆定；不能藉此聲稱完整鏈、物理識別或實質state來源已解。

### 5.3 每個輸入都有正負方向，§6(d)與state失敗

G_R、G_A diagonal都為I，故C(x,x)=0。對任一cover y≺x，advanced G_A(x,y)=0，
由CF.5得

$$C(x,y)=-i(\eta_0+u_{xy}I),\qquad C(y,x)=i(\eta_0+u_{xy}I). \tag{CF.8}$$

取任一0≠v∈E₀的η₀=+1線；這條線來自固定R₀，未依C譜選取。
令f_±只有f_±(x)=v、f_±(y)=±iv，其餘0。兩者皆在原完整T中，且u_xy≥0，所以

$$A(f_\pm,f_\pm)=\pm2(1+u_{xy})\,h_0(v,v). \tag{CF.9}$$

故每個D_Ξ輸入的A都非半正定。不能取正部分、縮test或把indefinite rank報成dim H_A，(d)失敗。
對任一正歸一functional，CAR給
ω({a(f)^*,a(f)})=ω(a(f)^*a(f))+ω(a(f)a(f)^*)≥0，
但左邊=A(f,f)；代入f_-矛盾。因此不存在**任何**相容正歸一state（亦即T6的A−必要障礙）。
固定Q=A/2的trial更在二階moment就給ω_trial(a(f_-)^*a(f_-))<0，
不需先證全套高階Wick moments的一致性即可判其正性失敗。
本稿不宣稱已構造一個良定的高階state再失去正性；state交付在必要二階條件即停止。

同一負方向也適用先定1≤t≤2比較類，只多t^{-2}因子；它不是可調t的修復路線。

## 6. 限定類障礙：global R₀自然性使η-adjoint退回ordinary

上述交換性不只對CF-01的係數成立。對本契約同一global fiber／共同換基自然性的任意K，
取structured automorphism f=id_P、V=η₀。V是h₀-unitary、保持η₀且不改P或L，
其T上作用即H。自然性遂要求KH=HK；若有two-sided G_R，則G_R、G_R†也與H交換。
所以只要仍選G_A=HG_R†H，就必有G_A=G_R†。這不使用K的order-polynomial形式。

更精確地，限定類G_η由以下全部條件組成：
- 契約相同的global R₀自然性、完整counting test與h；
- 同一K有order-retarded G_R，diagonal blocks為h₀-Hermitian，並有非零strict propagation；
- 下游**固定選**G_A=HG_R†H與C=iH(G_R−G_A)，沒有另換F或test。

在此類中G_A=G_R†，C diagonal為0，retarded非零block又使某C(x,y)=iη₀G_R(x,y)≠0。
Hermitian半正定form的零對角方向須為radical（Cauchy–Schwarz），所以零diagonal的正form
所有blocks都必為0，矛盾。因此G_η中不可能同時有傳播與正總form。
這是OP-01零對角障礙對此類的延伸；η的引入本身未改變它的承重前提。

**作用域上限：** 此結果不排除不同F、非Hermitian Green diagonal、其他已審型別或future新契約；
不許反推整個conditional問題不可能，更不許反推原始輸入問題或一般spinor不可能。
CF-01已固定且失敗，不在本版換contact、adjoint、F、state或primitive補救。

### 6.1 與OP-01障礙前提的逐項實際對照

| 前提／規則 | CF-01的實際判定與依據 |
| :--- | :--- |
| G_R沿原P retarded | 成立，CF.1；沒有沿L添加causal edges |
| G_R diagonal Hermitian | 成立，diagonal I，CF.1 |
| G_A=ordinary G_R† | 成立，雖命名η-adjoint，交換性給CF.4 |
| 字面上的F=i(G_R−G_R†) | 不沿用；本版左乘H，但CF.5／CF.8仍為Hermitian且零diagonal |
| 原完整T與非零傳播 | 都保留；CF.2及CF.9的test均未刪減 |
| 正CAR／正state | 不成立；CF.9與CAR必要性直接否定 |
| L再直接進入下游adjoint或F | 不允許，也未使用；H固定，其他影響只經K／Green |

所以真正改變的字面form規則不足以解除零對角障礙；不能以η或時間序的存在冒充已改變前提。

## 7. 完成度、比較與停止位置

| 契約義務 | CF-01結果（全部只在Ξ之下，待複核） |
| :--- | :--- |
| 全域量詞／structured自然性／來源 | 明列全D_Ξ；K、inverse與關係協變，沒有挑L或縮域 |
| §5第1–2項K／同一K的Green | 具體規則及完整two-sided identity已交；actual physical來源解讀未證 |
| §6(a)傳播 | 每個輸入cover非零，成立 |
| §6(b)非單一tensor | 每個輸入span恰2，成立；不等於spin／sector mixing |
| §6(c)K自身非局域 | 鏈族原Hasse距離witness，成立 |
| §5.3 Green→CAR | 具體F、Hermitian、同鏈恆等式及非恆定已交；L3識別不是物理導出，正性失敗 |
| §6(d)正Hilbert商增長 | A非正，前提不成立，不報rank成功 |
| §5第4項state | 不存在任何相容正歸一state；fixed trial二階即失敗 |
| dynamics／能量／vacuum／Dirac／continuum | OPEN，本版不提供公式或主張 |
| 完整同源主問題 | CF-01失敗並停止；conditional與原始輸入問題仍OPEN |

本輪沒有重讀文獻或查新穎性。格點／quantum-walk比較僅沿用契約§8及EXP-0096已披露的
有限原文定位，不冒充新的全文核對：本版未輸入spatial lattice／shift／unitary walk或先給正CAR，
但確實輸入L與R₀，且正CAR／state在本版失敗；故不是那些正CAR演化構造的推廣或反例。
完整原文mapping、最少輸入與新穎性判定仍未完成，不能宣稱已滿足§8的全部實質完成要求。
本稿的價值限於全域sector校準及G_η的精確失敗位置；CAR必要性與零對角論證是已知代數事實。

無科學程式／數值／symbolic／toy執行，無RNG、撒點、producer、raw／sealed、seed或主機量測。
全部符號推導在紙上完成；既有regression／integrity僅作repo檢查。
主契約、原始輸入契約、OP-01與formal均不改；E0、A／B、6a-E／Freeze-1a及UNKNOWN隔離不變。
此交付須另經操作者推送授權、draft exact-head逐式複核；不自行合併或升格為確認結果。
