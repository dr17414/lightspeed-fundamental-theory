# X-T6-QUANTUM-OBLIGATION-AUDIT-v0.1 — CAR必要條件與量子資料來源審計

狀態：**【已確認／限定解析：任意已給 CAR 資料下的條件式必要界（A=Q+R、0≤Q≤A、Riesz 表示、charged／self-dual 必要式、正部分障礙、form 保留與逐對極限）】**。
**探索軌，不具 §5.2.1(v) 依據資格。**
Problem ID `X-T6-QUANTUM-NECESSITY-P0.1`；Study ID `X-T6-QUANTUM-OBLIGATION-AUDIT-v0.1`。
新 model ID **NONE**；不提出K、state、pairing、物理test space、projector或量子模型。
本稿的代數、form與S均是條件式定理中**任意已給定資料的變數**；
不選任何物理實例，不把正部分當作本題state，也不設正式C9 criterion。

## 1. 定案、研究先後與六欄

[定案契約r2](t6_quantum_necessity_problem_contract_v0_1.md) blob
`ce332f5f3b7b999ca2a8c4836540085a0560b886` 全文保留。
#92 exact head `ada4b41238af8e93551a1a4cbdd9f8b4fb4b209b`／tree
`12634a4a80ee9b5aa11d2353da419249c972d767` 獲Claude增量GO，0068已在原ID逐字補齊。
CI #290 run39444635314在該head success，job118703171118及全部steps success後，
原樣squash為main **`865d74a37960a76e1585ec5065ff21ff76395e2d`**，tree與GO相同。
Git committer UTC **2026-10-20 17:14:49／台北2026-10-21 01:14:49**。
三項開始條件與merge tree核對後，才開始本輪策略／推導，沒有本輪提前推導偏差。
ACT-X-0001生效SHA仍0c386716，僅紙上；C2暫停、T2／T3限定確認與全部OPEN不變。

| 六欄 | 本研究 |
| :--- | :--- |
| 命題 | 條件式CAR正性／互補界、退化form的表示、charged／self-dual分型、positive-part轉用障礙與抽象極限轉用；交QO1–9資料義務表，不證本專案量子實現 |
| 定義域與輸入 | 任意已給unital *-algebra、複測試空間與CAR form；各段另列正state、Hilbert／Γ、dynamics或固定mapping。不是從I6-ORD／NUM／UV／PHASE已導出這些資料 |
| 證據 | §2–7的紙上證明與§8分項表，均待複核；Araki等來源只作已知代數／型別校準，無新穎性主張 |
| 未證橋接 | 實際K／G_R→CAR form→W的同源對接、state／pairing來源、物理test space、正能量與unitarity、1+1 massless quantum continuum極限仍OPEN |
| 否定條件 | 僅在總CAR form及*已正確對接後，負方向才觸發§2的限定no-go；裸i(G_R−G_A)或covariant矩陣的負譜不是該前提 |
| 後續驗證 | exact-head核對sesquilinearity、Riesz／Γ互補、charged異常兩點與極限量詞；如需具體K／state／pairing或正式判準選擇，停在OPEN，另立先審契約 |

契約§2.1完整繼承：本稿即使獲解析GO、合併或寫入STATUS，未完成另案handoff、曝光對應
與合資格審查前，不能作§5.2.1(v)的既有STATUS／數學必要條件依據或完成D.1第8項A聲明。
原文閱讀不是路徑B mapping，不提升文獻承重資格；acceptance／C9／C10及prereg皆不改。
原文與reviewer提示已接觸，見EXP-0069／0071；本稿不稱盲推導，新增範圍記EXP-0074。

## 2. QN2與QN1的共用起點：任意正state的CAR必要界

### 2.1 固定型別與最小前提

令T為任意複向量空間，𝔄為unital *-algebra，a:T→𝔄為複線性映射。
A:T×T→C是第一槽共軛線性、第二槽線性的有限sesquilinear form，滿足

$$a(f)^*a(g)+a(g)a(f)^*=A(f,g)1,\qquad f,g\in T.\tag{T6.1}$$

本節**不**要求{a(f),a(g)}=0，也不要求quasi-free、gauge invariance、真空或時間結構。
假設ω為線性functional，ω(1)=1、ω(X*X)≥0對所有X∈𝔄成立，且所用積的值有限。
這是正歸一化algebraic state的必要設定；不指定任何一個ω。
不直接套用於domain／乘積尚未定義的無界場分布；那類對接另屬P6-TEST／STAR／STATE。

使用ID：P6-TEST／STAR／CAR／STATE。I6資料本身未提供這四項。
本稿約定a複線性只是抽象記號；若物理文獻用反線性annihilation慣例，須先對接，不能沿用符號便算同型。

正functional的兩個基本性質如下，附證以固定慣例。
對H=H*，ω((H+t1)*(H+t1))在所有實t皆為非負實數，t=0及t=±1相減可知ω(H)實。
把任意X分解成兩個self-adjoint部分，即得ω(X*)=overline{ω(X)}。
對任意X,Y，ω((X+zY)*(X+zY))≥0；當ω(Y*Y)>0，取使二次式最小的z，得到
|ω(X*Y)|²≤ω(X*X)ω(Y*Y)。若ω(Y*Y)=0而交叉項非零，選相位及足夠大|z|即使二次式負，
矛盾；故同一界也適用零對角。這些是標準正性校準，不是新的物理假設。□

### 2.2 定理A：總form必為半正定，且0≤Q≤A

定義既有ω的兩種ordering form

$$Q(f,g)=\omega(a(f)^*a(g)),\qquad
R(f,g)=\omega(a(g)a(f)^*).\tag{T6.2}$$

兩者皆為Hermitian sesquilinear form，且Q(f,f)、R(f,f)≥0。
由(T6.1)及ω(1)=1，對所有f,g有

$$A=Q+R,\qquad A\succeq0,\qquad 0\preceq Q\preceq A.\tag{T6.3}$$

證明：Hermiticity由ω(X*)=overline{ω(X)}；對角非負分別是ω(a* a)、ω(a a*)。
對(T6.1)取ω即為A=Q+R，故其餘逐向量成立。□
這裡「≤」是**在同一T上的form次序**，不是裸kernel逐entry大小，也不是先選某個投影。

**推論A−（QN2）：** 若給定的A有f∈T使A(f,f)<0，不存在任何滿足上述前提的正歸一化state，
不只是不存在quasi-free state。非Hermitian的A也不能滿足(T6.3)。
這個一般state分支已由reviewer在r1複核時草算提示；本稿補齊型別及form證明，不稱新發現。

否定僅作用於固定T、*與已識別的**總CAR form A**。不能藉改pairing、刪負方向、
挑有利子空間或改normalization，把同一命題變成成功；那些是不同輸入／另案構造。
本稿並未給出S5C路徑的A，因此沒有由此得到本專案quantum FAIL或全面fermion no-go。

## 3. QN1：何時才有正規化的0≤S≤1

### 3.1 半正定form與null quotient

現在假設A已給定且A≥0，Q是已給定、滿足0≤Q≤A的sesquilinear form；不需先宣稱它來自state。
令N_A={f:A(f,f)=0}。正form的Cauchy–Schwarz由§2.1相同二次式論證得到，故
A(n,g)=0對n∈N_A、g∈T成立；因此N_A為線性radical，A下降至T/N_A成為正內積。
又Q(n,n)=0，對Q用Cauchy–Schwarz得Q(n,g)=Q(g,n)=0，所以Q也下降。

令H_A是**這個已給A的商之完成化**，內積第一槽反線性。由

$$|Q(f,g)|^2\le Q(f,f)Q(g,g)\le A(f,f)A(g,g)\tag{T6.4}$$

可將Q唯一連續延拓到H_A。Riesz表示給唯一bounded S，使

$$Q(f,g)=\langle[f],S[g]\rangle_A,\qquad 0\le S\le I.\tag{T6.5}$$

證明：給定第二槽向量，(T6.4)使第一槽functional有Riesz向量，且其norm不超過第二向量norm；
sesquilinearity使所得S線性且有界。Q的Hermiticity給S自伴，Q≥0與A−Q≥0分別給S≥0、I−S≥0。□
H_A為零空間時結論照常，不推出非平凡物理自由度。

這不是另選物理pairing、test space或state：A及Q都是定理的任意已給資料，S是Q的唯一數學表示量，
不提出本專案的A、Q或S。這回答contract中退化form的條件式合法性，沒有把P6-HILB的物理來源補出。
若要在**另給的**Hilbert空間H上寫(T6.5)，須額外證明A等於該內積normalization，
或給適當的form識別／有界性；未證時不能把A的表示矩陣直接換成I。
本稿不處理任意無界operator的Riesz／self-adjoint extension；僅對上述有界延拓作結論。

A的radical商由已固定A唯一決定，與「看到負譜後排除」不同；A有負方向時不能用這個正商前提。
0≤S≤I只校準兩點必要界，不證quasi-free、Wick高點、純態、真空或與同一K／G_R的相容。

### 3.2 charged CAR：異常兩點還有獨立義務

另加charged關係{a(f),a(g)}=0，記既有state的L(f,g)=ω(a(f)a(g))。
則L複雙線性且反對稱。§2.1對X=a(f)*、Y=a(g)的Cauchy–Schwarz給

$$|L(f,g)|^2\le\bigl(A(f,f)-Q(f,f)\bigr)Q(g,g).\tag{T6.6}$$

交換f,g並用反對稱，亦有對應交換後上界。這都是**同一已給ω**的必要式。
更完整地，任意有限組B_i（取自這些既有generators及其adjoints）之M_ij=ω(B_i*B_j)
滿足Σoverline{z_i}M_ij z_j=ω((Σz_iB_i)*(Σz_jB_j))≥0。
因此已指定異常兩點時，不能只驗normal Q的一個block便宣稱完整資料相容。

若**另給且ω對其不變**的gauge automorphism滿足a(f)↦e^{iθ}a(f)，則
L=e^{2iθ}L對所有θ，取e^{2iθ}≠1知L=0。未給該不變性時不刪L。
這不宣稱符合normal界的Q不能有gauge-invariant延伸；本稿沒有作延伸／state存在性構造，
也沒有為本專案選gauge、charge或任何異常pairing。使用ID另含P6-STATE／STAR／CAR。

### 3.3 self-dual CAR：Γ條件不是可省的標籤

此分支另給complex Hilbert H、antiunitary involution Γ，及複線性B(f)，滿足
B(f)*=B(Γf)、{B(f)*,B(g)}=〈f,g〉1。這裡**不**額外套入charged的{B(f),B(g)}=0；
實際由兩條已給關係得{B(f),B(g)}=〈Γf,g〉1。

對任意正state，§2及§3.1給Q(f,g)=ω(B(f)*B(g))=〈f,Sg〉、0≤S≤I。
並有

$$Q(\Gamma g,\Gamma f)=\omega(B(g)B(f)^*)
 =\langle f,g\rangle-Q(f,g).\tag{T6.7}$$

由antiunitarity及S=S*，左式等於〈f,ΓSΓg〉，故

$$S+\Gamma S\Gamma=I.\tag{T6.8}$$

沒有使用quasi-free假設；兩點的必要條件並不證任意高點已由Wick rule決定。
這是在原文已有的型別下重述Araki §3 Lemma 3.2的必要性，屬文獻校準；
其Lemma 3.3的quasi-free存在定理本稿不重證、不用來挑本專案state。
Γ與H是P6-STAR／HILB的外加比較資料，不從two-sector名稱導出；也不建立physical Majorana解讀。

## 4. QN2的承重前提：G_R到總CAR form尚未對接

把D記成一份文獻中的i(G_R−G_A)，不等於(T6.1)中的A。
例如[Noldus §3](https://arxiv.org/html/1305.0443v3)分別寫bar與Hermitian conjugate H，
其原文從{ψ,barψ}=iΔ改寫到{ψ,ψ^H}=iΔγ。這只說明**leg／adjoint會改變待測form**，
本稿沒有採用該γ、generating structure或其state，更不把它當1+1 S5C的對應公式。

在把任何D的負譜拿去用推論A−之前，至少還缺下列已定案型別的實際來源：

| 缺的對接 | 必須交代；本稿均未完成 |
| :--- | :--- |
| GREEN | 同一K的G_R／G_A、inverse／contact term／boundary與兩個legs；不能把evolution kernel當kinetic inverse |
| STAR／HILB | bar、*、transpose與正Hilbert adjoint之間的已宣告識別；不能拿indefinite pairing的譜替正form的符號 |
| TEST／CAR | 所有允許測試向量、smearing／measure、密度與單位normalization，以及總反對易子是否真為A1 |
| STATE | 要求的state型別與W的field ordering，是否由同一資料鏈導出，而非另外放一個正W |

這是契約內的物件對接缺口，**不是formal路徑B mapping成果**，也不是本稿推薦的mapping。
即使裸D恰為普通Hermitian矩陣，未證其代表A仍不能下結論；若D只有covariant adjoint性，
連「普通Hermitian／正負譜」的使用意義也須先核對。實際S5C代入全部維持OPEN。

## 5. QN3：scalar SJ不能當成CAR總form的修復

scalar文獻的已知關係是CCR下D=iΔ=W−overline{W}；其SJ prescription在相應
self-adjoint／domain前提下取正部分。這與(T6.3)的**總和**A=Q+R是兩個不同型別。
此定位沿[Sorkin Eqs.(5)–(7)](https://arxiv.org/html/1107.0698v2)，不把scalar結果當fermionic證據。

一個純條件式障礙可不選任何模型而證明。給定有限維Hilbert上的self-adjoint D，
或已給有界self-adjoint D可用譜定理，令D_+、D_-為其正／負部分的數學記號，
D=D_+−D_-。若**另已證A由D表示**且D_-≠0，則把Q假定為D_+會使

$$A-Q\ \hbox{由}\ -D_-\ \hbox{表示},\tag{T6.9}$$

違反(T6.3)。此外任何其他Q也不能修復固定的不定號A，因推論A−已排除所有正state。□
這只是對假定prescription的必要性檢查，不把D_+選為本題state，不定義具體D或projection。
若D不是已映射的總A，(T6.9)的前提不成立；不能據此否定所有fermionic SJ推廣。
正的兩點資料也未自動給出CAR normalization、state的高點規則、正能量或動力學。

## 6. QO6–8：normalization、動力學與正能量分帳

(T6.3)用到ω(1)=1及**固定的**(T6.1)常數／measure。改場的normalization會改A，
不能把舊A當I或以rescale聲稱原主張已滿足；本稿不選normalization公式。
equal-time anticommutator還需P6-TIME、contact term及來源／邊界的語意，抽象form界不提供它。

有一條可核對的條件式動力相容性。若**已給定**線性可逆D_t:T→T與unital *-automorphism α_t，
並宣告α_t(a(f))=a(D_t f)，對(T6.1)施α_t得到

$$A(D_tf,D_tg)=A(f,g).\tag{T6.10}$$

若同一ω另對α_t不變，再得Q(D_tf,D_tg)=Q(f,g)。證明只是*、乘積與1的保留及取ω。□
沒有在此構造D_t、α_t或state；這是對任意已宣告dynamics的必要式，使用P6-TIME／CAR／STATE。
它不等於存在strongly continuous unitary實現，也不給generator的正能量譜。

本資料帳沒有從I6取得時間平移／stationarity、其強連續實現、state不變性或positive-energy
spectral support，因此QO7與QO8的物理部分仍OPEN。有限diamond一般不帶全時平移對稱；
不能在未給對稱作用時為它寫p⁰≥0。這是缺少定義／證明，不是所有finite-region量子理論的no-go。
正Hilbert／CAR兩點界不能代替unitarity、完整analytic stability或1+1 massless量子極限。

## 7. QN4：一個有完整量詞的抽象極限轉用命題

本節不選實際continuum test space或evaluator。假設已給固定複空間T_∞，每個參數λ的
空間T_λ、**已固定**線性mapping J_λ:T_∞→T_λ，以及form A_λ、Q_λ滿足0≤Q_λ≤A_λ。
若對每一固定f,g∈T_∞均有有限複數極限

$$A_\lambda(J_\lambda f,J_\lambda g)\to A_\infty(f,g),\qquad
Q_\lambda(J_\lambda f,J_\lambda g)\to Q_\infty(f,g),\tag{T6.11}$$

則極限為Hermitian sesquilinear form，且0≤Q_∞≤A_∞。
證明：加法／數乘與共軛在逐對有限極限下保留；對每個固定f，將三個非負對角量
Q_λ、A_λ−Q_λ、A_λ取極限即得次序。若另有已給反線性involution Γ_λ、Γ_∞，
J_λΓ_∞=Γ_λJ_λ，且對所有u,v∈T_λ有
Q_λ(Γ_λv,Γ_λu)=A_λ(u,v)−Q_λ(u,v)，則代u=J_λf、v=J_λg，
對固定f,g取極限亦得Q_∞(Γ_∞g,Γ_∞f)=A_∞(f,g)−Q_∞(f,g)。□

這只保留代數form條件，**不證存在limit state或Wick高點、pure vacuum、operator-norm／
uniform／a.s.收斂**。也沒有從此推出以固定外部inner product表示的S_λ會以任何operator topology收斂。
各f,g的門檻可依該對向量；若要一致控制一族向量，必須另證，不能交換量詞。
機率／期望型敘述、隨機分母與窗口／IR／密度的不同極限順序亦不包含在本命題中。
使用ID為P6-TEST／LIMIT及已給的CAR forms；若附Γ條件再用P6-STAR。

本專案沒有提供此處J_λ、A_λ、Q_λ及其兩條極限，更沒有實際W／ρ的對應。
先前C2的Green讀值收斂只在其原型別成立，不能當成(T6.11)已滿足；
本稿未證從任一G_R收斂假設可推本題W收斂，也未證所有這類轉用都不可能。
若要補具體K、state、pairing或spectral prescription，依契約停在此處，另立構造問題。

## 8. QO1–9義務表：條件式代數結果與實際來源分列

下表每格只給契約允許的一種資料帳判定；細分避免一個定理覆蓋整個物理義務。
本稿未從I6輸入導出完整量子資料。**需外加**表示本路徑尚未提供該型別／來源，
不證明所有其他intrinsic方案都無法導出它；一般可導出性仍OPEN。
所引定理均為本稿待複核的條件式校準，不是C9判準或formal依據。

| 義務／子項 | 本稿限定進展 | 本資料帳判定（非formal gate） |
| :--- | :--- | :--- |
| QO1a 物理domain與總form來源 | 需先提供T／A；一旦已給A≥0，§3才導出H_A，不再假裝還需獨立選一個Hilbert norm | **需外加P6-TEST／CAR來源資料** |
| QO1b H_A的物理識別 | 商定理不證它就是所需物理Hilbert；另採pairing須說明識別 | **OPEN** |
| QO1c 實際資料是否可由I6導出 | 未給intrinsic規則，商定理不能代替來源 | **OPEN** |
| QO2 *／bar／adjoint識別 | §4列同型義務，不把Noldus γ套到本題 | **需外加P6-STAR／HILB識別資料** |
| QO3a state型別與同源來源 | 正state／quasi-free／vacuum不同，§2不提供state | **需外加P6-STATE／GREEN來源資料** |
| QO3b 同一K能否有該正state | 沒有K／實際A；未應用推論A− | **OPEN** |
| QO4 form必要正性／Hermiticity | §2證A=Q+R、0≤Q≤A；尚無實際leg／domain對接 | **需外加P6-TEST／STAR／CAR對接資料** |
| QO5a charged／self-dual型別 | §3.2／3.3給各自必要式，Γ不能省，不能合併兩種algebra | **需外加P6-CAR／STAR／STATE型別資料** |
| QO5b 物理CAR實現 | 已知必要界不證存在性、Wick或與K相容 | **OPEN** |
| QO6 normalization／equal-time sum rules | §2與§6分清form常數、單位／接觸項，未給公式 | **需外加P6-CAR／GREEN／TIME資料** |
| QO7 positive-energy support | 沒有可供本題使用的stationary group／generator／state | **需外加P6-TIME／STATE／LIMIT資料** |
| QO8a 動力實現的資料型別 | §6只證已給automorphism的A／Q保留，不造dynamics | **需外加P6-TIME／HILB／STATE資料** |
| QO8b unitarity／完整量子穩定性 | 沒有具體dynamics、domain與analytic資料 | **OPEN** |
| QO9a 比較mapping與量詞 | §7給逐對form轉用定理，不選J_λ | **需外加P6-LIMIT／GREEN／STATE資料** |
| QO9b 實際1+1 massless quantum continuum | 未有同源W／ρ、state與轉用前提；C2不能代替 | **OPEN** |

因此沒有某個已構造S5C候選被判成功或失敗，也沒有完成量子一致性實現。
能交付的是已知代數必要條件的型別化覆核，以及每個缺口現在位於哪個來源／mapping。

## 9. 原文、提示來源與停止點

- [Araki原PDF](https://ems.press/content/serial-article-files/41673?nt=1) §2與§3 Lemmas 3.2–3.3本輪重讀，工具亦回傳引言、相鄰§4片段。§3.3是其必要性的有界型別校準；不重證quasi-free存在定理，不採原文state構造。
- [Noldus 1305.0443v3](https://arxiv.org/html/1305.0443v3) §3及工具回傳§2末本輪重讀，只核bar／Hermitian legs；看見其generating structure與vacuum符號，未採用或驗證模型。
- [Sorkin 1107.0698v2](https://arxiv.org/html/1107.0698v2) §2附近Eqs.(3)–(7)本輪重讀，工具亦回傳histories相鄰段，只對照scalar CCR／SJ型別。
- Johnston、AAS與Potting的來源定位沿定案契約§6／EXP-0070，本輪未重讀其原文，不稱本輪新增獨立核實。Track B／BBMM原作用域與本題不同，不重跑／套用其positivity結果。

reviewer QN2一般state分支的草算已在EXP-0071公開，非本稿盲發現；其他記憶性提示與
原文閱讀也均保留。這是文獻校準／必要條件審計，不稱新穎性盤點或新的物理機制。
所有新證明仍待exact-head獨立複核，物理詮釋維持探索，實際K／state／pairing實現全部未交付。
正式C9／C10、test space／projector／evaluator、criteria與容差形式／數值一個位元不改，
不把本稿或STATUS更新用作D.1第8項A依據，讀原文不是B mapping。

本輪不構造物理K／state／算子／pairing、不作數值／符號診斷、不用RNG、不撒點、
不呼叫producer、不讀raw／sealed、不產生seed、不開主機、不量測／receipt；
既有regression／integrity只作repo驗證。若要實現上述資料鏈或回formal，依契約另案先審。
E0、item7不可ADOPT、item8 OPEN、6a-E／Freeze-1a、全部UNKNOWN／禁止資料隔離不變。


## 10. exact-head複核與原樣合併封存（2026-10-21）

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

正文中的待審用語保留為提交時點歷史；§2–9證明、公式與來源記錄不改。
