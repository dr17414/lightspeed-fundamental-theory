# X-KQ-OP-01 — order-polynomial首次試作與兩項限定障礙

狀態：**【探索／紙上定義與證明已交，待exact-head獨立複核】**。
Problem ID `X-KQ-1P1-P0.1`；Attempt ID `X-KQ-OP-01`。
**探索軌，不具 §5.2.1(v) 依據資格。**

本次有一個實際K公式，不是只列待補型別。結果是**試作失敗**：K有retarded inverse，
且有無統一Hasse-hop cutoff的支撐，但sector span在原工作域內的star上不足；
固定ordinary-adjoint CAR prescription也有明確負方向，不能有正歸一化state。
不改K、pairing、test domain、CAR prescription或工作域補救。
另證自然global swap的限定比較類G_swap在同一star上也不可能滿足§4.1(b)。
這不是對所有合法構造、所有二維表示或原S5C-Claim的全面不可能定理。

## 1. 身分、來源與時序

[契約](kq_1p1_construction_problem_contract_v0_1.md)保持原樣；D_KQ、§4.1(a)–(d)、
§4.2及新增physical primitive停止條款不變。#95 main3387d732／tree16bb788a、
#97 main `1ac30ceb14887d8c4d24636bc9ad17a0baa913e7`／tree
`3350d8bdb86dddd5dd7d1f13393e20ba9e65c563`均經GO、CI、原樣合併與tree核對。
#97 Git committer UTC2026-10-23 02:27:57／台北10:27:57。
首次交付的第一commit `eeb5ea6d1e46cb227890a5aa1ff6dd43fe01c3db` 逐字記0089／0090；
第二commit `1bd15a5ef57d1f60906cf9b0d619f9980f92770f` 固定
[試作規則](kq_order_polynomial_attempt_spec_v0_1.md)§1–6，之後才將完整證明寫成本稿。
內部預想已於0091披露，不稱盲預註冊／新穎性結果；本稿不隱藏已預期的失敗風險。

| 六欄 | 本次交付 |
| :--- | :--- |
| 命題 | 具名試作K／Green、兩個明確失敗及G_swap限定障礙 |
| 定義域 | 整個已固定D_KQ；star與鏈都是域內解析witness，不另選工作子類 |
| 輸入 | order／count、明示L2 two-slot／linearization／pairing／CAR及有限L3公式選擇 |
| 證據 | §3–6有限代數與群作用的紙上證明，無模型／symbolic執行 |
| 未證橋接 | 一般I-UV實際sector來源、G_swap外方案、物理fermion／massless／continuum仍OPEN |
| 否定／後續 | OP-01不能完成契約；保留失敗，不縮D_KQ、不由限定類障礙宣稱全域無解 |

來源沿既有T3的orbit／two-set區別及T6正state必要界；本輪沒有新文獻檢索或原文閱讀。
原規則§2的L1標籤需作來源分類更正：order及count屬L0；free linearization屬L2；
本試作沒有使用L1 realizer導出量。規則末尾§7追加此更正，§1–6及所有數學選擇原樣。
這不是新增資料、換K或依負譜換pairing；也不修改acceptance中的任何定義。

## 2. 固定物件及來源／容量帳

H_P=T_P=C^P⊗C[S]，S是明示的anonymous two-element bookkeeping set；
J交換其兩元素。counting pairing第一槽反線性，†為其ordinary adjoint。
Z_P(x,y)=1_{y≺x}，Z²(x,y)=#{z:y≺z≺x}。固定

$$B=Z\otimes I_S+Z^2\otimes J,\qquad K=I+B.\tag{KQ.1}$$

| 來源層／項 | 使用與容量 |
| :--- | :--- |
| L0 | P、strict order、N與finite interval count；沒有coordinates、metric或physical density |
| L1 | 未使用realizer代表、rank、左右物理方向或其自由選擇 |
| L2 | C、free linearization、S與J、counting pairing、†、下述CAR prescription；不是湧現量子力學 |
| L3 | 一個明列的二次多項式、全部係數固定為1、完整domain與unit contact、單一CAR prescription；零可調參數、沒有表或optimizer |
| L4 | 不使用evaluator、planted、probe、sealed或UNKNOWN私人材料 |

固定公式的描述長度及可調容量不隨N增長；矩陣尺寸與資料計數隨N增加，不等同可調容量。
inverse的N項有限級數由nilpotence強制，不是為擬合結果選出的截斷。
S尚不是由I-UV唯一orbit導出的實際order two-set；本試作明示借用允許的L2 bookkeeping。
沒有選realizer代表，因此代表變動不改K；這不等於已解決T3的一般intrinsic sector來源。
I的contact無物理mass詮釋，J無Clifford／chirality／frame詮釋；未新增physical primitive。

對任意同構f:P→P′，令U_f e_x=e_{f(x)}，在S上用id。
由order保持性，Z_{P′}U_f=U_f Z_P；平方同樣交換。因而

$$K_{P′}(U_f\otimes I_S)=(U_f\otimes I_S)K_P.\tag{KQ.2}$$

sector換名由J實現；I與J均與J交換，所以K也與global swap交換。
任意two-set bijection也交織其swap及counting pairing。
這給完整isomorphism自然性，非只核對Aut(P)；U_f⊗I亦保持完整test pairing。
一旦inverse存在，同一等式對inverse與adjoint成立。CAR relation由T上映射誘導：
a_P(f)↦a_{P′}((U_f⊗I)f)，故固定的代數prescription亦自然。
沒有逐N另外調rule；nested-region／加點inverse相容性未在此證明，仍OPEN。

## 3. 同一K的retarded two-sided inverse與非局域性

### 3.1 完整domain上的inverse

B的非對角非零blocks僅在y≺x。B^j的一個非零項須有j條strict-order步驟，
即j+1個不同事件形成鏈；N個事件不可能有N條這樣的步驟，故B^N=0。
不需要選出canonical linear extension；若以某一extension表示，只是驗算三角性的座標。
固定

$$G_R=\sum_{j=0}^{N-1}(-B)^j.\tag{KQ.3}$$

由有限幾何級數的逐項相消，(I+B)G_R=G_R(I+B)=I。
因此這是同一K在完整H_P上的唯一two-sided inverse，不是只交evolution kernel。
source是任意η∈H_P，解ψ=G_Rη，contact identity是I_{H_P}；無外加boundary資料。
各非對角項仍沿strict order，G_R(x,x)=I_S，故是此有限order意義下的retarded inverse。
G_A=G_R†為advanced支撐，但未證它是同一非自伴K的inverse；它是K†的inverse。
本稿不將兩者混同，也不稱已得到physical causal propagator。

### 3.2 傳播：契約§4.1(a)

D_KQ的每個P有可比對。有限性保證至少有一個cover y≺x，即二者間無事件。
此處Z²(x,y)=0，且B^j(x,y)=0對j≥2，所以

$$K(x,y)=I_S,\qquad G_R(x,y)=-I_S.\tag{KQ.4}$$

G_R確有非對角非零block，且其全部非對角支撐沿order。因此(a)逐P成立。
這沒有導出物理傳速、c、Dirac或1+1維流形。

### 3.3 K本身的非局域：契約§4.1(c)

對任意y≺x，K(x,y)=I_S+n(x,y)J，其中n是strict interval count。
此block的trace為2，所以不為零；不是只讓局域K的inverse變dense。
取契約已證在D_KQ內的全序鏈C_m，m≥3。兩端點的最短directed Hasse path長m−1，
且K在該對上非零。對任意有限r，選m>r+1且m≥3，便有d>r的K支撐。
因此全D_KQ族上不存在統一Hasse-hop cutoff，(c)成立。
鏈只作原域內witness，沒有把它事後改選成成功工作子類。

## 4. Sector最低非平凡性：明確失敗與限定類障礙

### 4.1 OP-01在原域內失敗

令P_*含三個minimal事件a_1,a_2,a_3及一個maximal事件b，唯一strict關係為a_i≺b。
任意total-order extension都將b置末，葉子的次序可任選。
若U與V的交集恰為P_*，任一葉對在兩個orders中的方向必須相反，所以V的葉次序
恰為U的反向；反之這樣的orders確實realize P_*。Aut(P_*)≅S₃在葉子的任意排列上傳遞，
因此R₂(P_*)/(Aut×S₂)只有一個orbit。q(P_*)=3，故P_*∈D_KQ。

P_*沒有長度2的strict-order路徑，故Z²=0；全部非對角K blocks只有
K(b,a_i)=I_S，其complex span恰為一維。這違反契約§4.1(b)。
即使另有成功的CAR／state也不能補救此逐P義務；本稿不排除這個輸入來維持成功。

作為分辨：在C₃上，兩個cover blocks為I_S，端點block為I_S+J，兩者線性獨立。
因此二次式的block span不是在每個輸入上都一維；但單一鏈通過(b)不能代替全域量詞，
也不能把block span當作I-UV來源或physical spinor的證明。

### 4.2 G_swap的限定障礙

使用固定規則§5的全部假設：同一global二維E、自然swap J、其±1 eigenspaces各一維，
honest functorial V_f、V_f交織J、order-supported K及(OP.3)。
在P_*上，automorphisms給representation ρ:S₃→GL(E)，每個ρ(g)都與J交換。
因J的兩個eigenspaces各一維，所有與J交換的operators在同一分解上都是對角scalar，
所以ρ(S₃)是abelian，不需假設unitary或只准置換矩陣。

取三循環c=(123)與transposition t=(12)。群中tct⁻¹=c⁻¹；
由image abelian，ρ(c)=ρ(c)⁻¹，故ρ(c)²=I。又c³=e給ρ(c)³=I，合得ρ(c)=I。
這個三循環固定b，並在三個a_i間傳遞。自然性因此給

$$K(b,a_{c(i)})=\rho(c)K(b,a_i)\rho(c)^{-1}=K(b,a_i).\tag{KQ.5}$$

其他非對角blocks由order支撐假設為零，所以全部非對角blocks的span至多一維。
不論diagonal blocks如何選，均不能滿足(b)。□

**作用域。** 這排除整個G_swap在完整D_KQ上的正面完成，不僅是(KQ.1)。
它不由D1唯一orbit自動成立：必須有此global fiber、自然J及honest action等額外假設。
不保留J的GL(2)作用、per-event纖維／transport、projective action等不在本定理內；
本稿沒有構造它們，也沒有證明它們一定需要新增physical primitive或一定能由原資料導出。
若下一步研究那些路徑，須先交其來源／型別與契約相容性；若需新增physical primitive，
遵契約停止另立conditional問題。不能以此有限star障礙宣稱一般fermion／S5C不可能。

## 5. 固定ordinary-adjoint CAR橋接：有負方向

完整test T、pairing、†及A=i(G_R−G_R†)均按固定規則§4，沒有projection或quotient。
這是同源矩陣與明文CAR prescription的數學試作，不是已導出物理smearing／fermion adjoint。
以下失敗作用於這個已固定的總form／relations，不把裸kernel之負性擴張到其他對接。

由G_R(x,x)=I_S，A的全部diagonal blocks為零。
對任意cover y≺x，由(KQ.4)及retarded支撐，

$$A(x,y)=-iI_S,\qquad A(y,x)=iI_S,\qquad A(x,x)=A(y,y)=0.\tag{KQ.6}$$

選任意非零v∈C[S]，定義完整T中的兩個測試向量f_±，僅x與y分量非零：
f_±(x)=v，f_±(y)=±iv。這是展示既有T內的向量，不是事後縮test space。
直接代入固定pairing得到

$$A(f_+,f_+)=2\langle v,v\rangle_0>0,\qquad
A(f_-,f_-)=-2\langle v,v\rangle_0<0.\tag{KQ.7}$$

所以每一個P∈D_KQ的此A都有正、負方向，特別不半正定。
不靠數值譜、容差或選取最壞樣本。依T6 §2的A=Q+R必要界，
任何ω(1)=1且ω(X*X)≥0的state都會迫使A≥0；故本試作的CAR關係沒有任何正歸一化state。
不僅是S=0或quasi-free選擇失敗。

一般化僅及另一個明定類：任何finite order-retarded G，其diagonal blocks皆為Hermitian，
在同一ordinary-adjoint prescription下A的diagonal為零。
若有任一非對角G(x,y)≠0，A亦非零；positive form若所有basis對角為零，
由Cauchy–Schwarz必全部matrix entries為零，矛盾。
因此此類不能同時有非零傳播及正A；**不及**不同contact、其他來源合規的pairing／CAR橋接。
這是標準正form性質的應用，不主張新文獻結果。

不取正部分、不換pairing、不刪負方向、不外加W或無關自由度。
由於A不正，H_A不作正Hilbert空間定義；其radical商不能合法消除負方向。
普通矩陣rank即使較大也不能算契約(d)的H_A維數，本稿不以此偷渡非退化性。

## 6. 義務表與停止位置

| 契約項 | OP-01的交付／結果（均待複核） |
| :--- | :--- |
| K與domain、自然性 | (KQ.1)全H_P定義，所有isomorphisms自然；L2／L3來源已列，actual I-UV來源未解 |
| Green | 同一K的完整two-sided retarded inverse(KQ.3)；G_A僅為K†的inverse |
| (a)傳播 | 每P由cover給G_R非對角block，成立 |
| (b)sector span | P_*失敗；另證整個G_swap皆有同一障礙 |
| (c)非局域 | K本身在鏈任意大Hasse-hop距離非零，成立 |
| (d)正form與維數 | 固定橋接A不正，正H_A前提失敗，不能報rank門檻通過 |
| 總CAR／state | 試作關係型別已列，但有負方向，無正歸一化state；physical橋接仍未導出 |
| dynamics／vacuum／massless | 未給動力學、energy或物理vacuum；全部OPEN，不以有限代數代替它們 |
| 跨N／nested／continuum | 同一規則逐N；更強nested／continuum相容性未證，主問題未完成 |

本次不是D_KQ上已完成的構造，也不是某個縮域上的成功同源鏈。
真正的下一個決策是是否研究G_swap之外、仍只由合法資料導出的fiber／intertwiner型別，
以及具有物理來源的Green→CAR對接；此處只定位未證義務，不提供新方案或放寬契約。
OP-01的兩個失敗分開保存：改量子橋接不會解除star的sector障礙，
改sector也不自動解除unit-contact ordinary-adjoint障礙。
沒有實際同源1–4鏈，因此沒有physical viability、scientific PASS或formal資格。

## 7. 審查與來源邊界

請reviewer逐式核對nilpotence／two-sided inverse、cover的blocks、鏈的K支撐、
star的D1身分、G_swap假設及三循環論證、f_±的符號與state不可能性，並核對不誇大作用域。
S／C／counting pairing／CAR prescription皆是披露的數學scaffolding，不宣稱由orbit湧現。
來源為本repo已核准T3、T6及契約／activation文字，未讀文獻原文、未作新穎性搜尋。
沒有執行模型、symbolic／toy程式、RNG、撒點、producer、raw／sealed、seed、主機消費或receipt。
Python／Git如出現，只作文件編輯、逐字／prefix／hash與既有integrity檢查，不求值任何科學公式。
既有公開摘要曝光與UNKNOWN血緣沿0091／0092保留；不以禁止資料選K或輸出規則。
acceptance、正式C9／C10、T3／T6、定案契約與原隔離不改，全部結論仍待獨立exact-head複核。


## 8. 公開版本對照與時序證據等級（2026-10-24；只追加）

**本地checkpoint與公開commit的對照、可查核範圍。**

| 本地checkpoint（作者保留） | 所報tree | 公開可抓取commit | 公開tree |
| :--- | :--- | :--- | :--- |
| eeb5ea6d1e46cb227890a5aa1ff6dd43fe01c3db | 6a4858d0851d8065817b12a924034c0eae64acd4 | a01c4ea6103306335e4c48c5f36972276c09352b | 6a4858d0851d8065817b12a924034c0eae64acd4 |
| 1bd15a5ef57d1f60906cf9b0d619f9980f92770f | eb594400860abcf1399432a006126b6db7ae97cb | e30d9bd9eb970295786748463b5573b72cb3a7c1 | eb594400860abcf1399432a006126b6db7ae97cb |
| ac83c4e666a26dcc1df99523001c2a97c0eee4bd | 0f7e1e4e6c72d51fff34d5b5926904ba3430a3e8 | 8176f9848ba892119f757c2b2d6414c1d7871d46 | 0f7e1e4e6c72d51fff34d5b5926904ba3430a3e8 |

這是API發布後的內容對照，不是同一個commit物件。作者本地可見上述checkpoint；
reviewer向公開repo抓取eeb5ea6d與1bd15a5e失敗（not our ref），因此這兩個本地SHA
**不能作公開可查核的承重證據**。表中本地身分／對應是作者披露，不能代替取得那些物件的獨立查核。

公開可查的鏈是main1ac30ceb → a01c4ea6 → e30d9bd9 → 8176f984：
a01只追加紀錄，e30包含固定規格§1–6，8176才包含研究稿，且在規格末尾只追加§7。
公開Git證據只證明這個commit層面的先後順序與各版內容，不獨立證明作者私下何時思考、
看到或預期科學輸出，更不能證明「看任何輸出之前」的盲固定。原文的規格先固定說法
只按此公開版本化順序理解；超出它的本地時序／內部思考僅為作者申報。
EXP-0091已披露固定規格前的零對角／對稱性風險預想，本追加不提高其證據等級或盲性資格。
不以API commit時間倒填研究開始或內部規則選定時間；本地SHA、原句與數學全文均保留。

本節只補追溯性；§1–7的定義、公式、證明、失敗、作用域及OPEN均不改，未增加新推導。
