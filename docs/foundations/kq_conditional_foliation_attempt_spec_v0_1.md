# CF-01 v0.1 — 固定線性foliation計數與η-adjoint的紙上試作規格

狀態：**規則固定／校準型試作；本檔不交研究證明**。2026-10-28 Asia/Taipei。
Problem ID `X-KQ-COND-TA-P0.1`；探索model ID `X-KQ-CF-01-v0.1`。
**探索軌，不具 §5.2.1(v) 依據資格。所有主張只在外加Ξ=(L,R₀)之下。**

## 1. 基線、程序與事前已見資訊

依[定案契約](kq_conditional_time_adjoint_problem_contract_v0_1.md)，基線main
`5e5e819ff76cedac84b1be9c20cac5eb1a047842`，tree
`e925b0e4be083478f0372b98994e9b837d45ab53`，parent be55a80a；
#99 r3 exact-head GO、CI #308 success、操作者合併授權、原樣合併及tree核對已完成。
第一個交付commit只在三帳逐字登記EXP-0101／0102；本檔屬第二個、獨立規格commit。
之後才把正式計算、證明與義務判定寫進研究稿。失敗不回改本規格，改規則須另版保留失敗版。

**這不是盲預註冊。** 固定本檔以前已接觸：
- OP-01的order-polynomial／nilpotent inverse及ordinary-adjoint零對角障礙；
- Claude在#99複核中提示的star線性count／span、三種order型別及L位置限制；
- #99 r3合併後的方向提示：逐項檢查η及K／Green實際改變了哪個障礙前提。

作者在本規格commit以前已腦中設計下述公式，並預算過：用1、√2、√3的整數線性分離，
可能以「有三點鏈／height≤2」的分情形證sector判準；也已預想η-協變會讓K與η交換，
從而η-adjoint可能退回ordinary adjoint、Green-difference仍有零對角及負方向。
這些包含初步的腦中論證，不把正式證明寫在之後就宣稱先前完全沒看過結果。
曾考慮過非Hermitian contact／diagonal可能改變零對角前提，**本版沒有採用**，也不在失敗後補入。
本版目的在檢查這個明列類別，不是宣稱已找到可完成整條鏈的新機制。
未寫科學程式、未執行數值／symbolic／toy，未查新文獻；文字／Git時序只證文件版本順序，
不能證內部思考時序或盲性。本檔不用本地commit SHA作公開可查核的承重證據。

## 2. 輸入、型別與不變的完整domain

P遍歷契約的全部D_KQ，L遍歷每個P的全部LE(P)，不挑L、不縮P子類。
N=|P|；R₀=(E₀,h₀,η₀)全問題固定，dim E₀=2，η₀*=η₀、η₀²=I、正負線各一維。
*此處是h₀-adjoint；後文代數的*另列。*
令T=C^P⊗E₀，h是h₀的counting Hermitian pairing，第一槽共軛線性。
令H=I_{C^P}⊗η₀，Π_±=(I±H)/2。符號Π_±只用於型別／證明，不縮test或刪模。
event注入ι_x:E₀→T、取值ev_x:T→E₀均為free linearization的標準映射。

Z(x,y)=1_{y≺x}；Z²是事件矩陣composition，不是新增輸入。
其block方向固定為source y→target x。diagonal及不可比pair不讀L。
保留契約所有primitive容量、來源、formal及UNKNOWN隔離，不給額外frame、transport、
metric、時間間隔、Clifford、spatial shift、positive CAR或covariance。

## 3. K^ord及M_τσ的全部固定值

固定

$$K^{ord}=I_T+Z\otimes I_{E_0}+Z^2\otimes\eta_0.$$

只為契約中實際可能的七個(τ,σ)指定矩陣；其他型別不作可調項。
型別可出現性的正式證明留待研究稿，不把不可能型別計作獨立參數。

| τ=(rel(z,y),rel(z,x)) | σ | 固定M_τσ |
| :--- | :--- | :--- |
| (∥,∥) | pre | √2 η₀ |
| (∥,∥) | between | 0 |
| (∥,∥) | post | √3 η₀ |
| (∥,≺) | pre | √2 η₀ |
| (∥,≺) | between | 0 |
| (≻,∥) | between | 0 |
| (≻,∥) | post | √3 η₀ |

S_xy及n_τσ完全照契約§4.4，不另讀rank／比較表或任意L特徵。記

$$p_{xy}=n_{(\parallel,\parallel),pre}+n_{(\parallel,\prec),pre},\qquad
 s_{xy}=n_{(\parallel,\parallel),post}+n_{(\succ,\parallel),post},$$
$$u_{xy}=Z^2(x,y)+\sqrt2\,p_{xy}+\sqrt3\,s_{xy},\qquad y\prec x.$$

本版K的規則是

$$K(x,x)=I_{E_0},\qquad K(x,y)=I_{E_0}+u_{xy}\eta_0\ (y\prec x),\qquad
 K(x,y)=0\ (x\ne y,\ y\not\prec x). \tag{CF.S1}$$

1、√2、√3及七格的零值是作者這次RΞ-L3 law的固定數學常數，不稱由P推出的物理常數。
它們用來分離不同整數count的線性貢獻，並沒有由A正負、譜或逐P擬合取得。
沒有可調continuous參數、per-P／per-event矩陣、normalization、查表、非線性count運算或乘積。
固定M_τσ只在R₀共同換基下共軛表述；不獨立選η本徵向量作新physical frame。
這些矩陣只提供同一η方向的權重；不宣稱sector mixing、spin或chirality。

## 4. 全部下游規則及§4.5分解式

令B=K−I_T。以下都是固定規則，不是待看到結果後挑選的選項。

| 下游物件D | 固定的widehat D(P,R₀;列名上游)／來源 |
| :--- | :--- |
| 完整source／test、smearing | T及h照§2；smearing Id_T，source取T；無projection、boundary selector或test縮減 |
| contact與boundary | contact Id_T；有限P上不額外給boundary資料，聲稱在完整T上的two-sided identity |
| G_R | widehat G_R(P,R₀;K)=Σ_{j=0}^{N−1}(−B)^j，須驗證KG_R=G_RK=I_T及原order retarded |
| indefinite pairing與η-adjoint | b(f,g)=h(f,Hg)；X^sharp=H X† H，其中†是counting h-adjoint，不是CAR代數* |
| G_A | widehat G_A(P,R₀;G_R)=G_R^sharp；須驗證為K^sharp的advanced two-sided inverse，不稱它是同一非self-adjoint K的另一inverse |
| 總form的矩陣C | widehat F(P,R₀;G_R,G_A)=iH(G_R−G_A)；A(f,g)=h(f,Cg) |
| CAR代數及field | 下述charged關係及標準形式代數*；不先給δ-CAR，不宣稱h已是物理CAR |
| state trial | Q(f,g)=A(f,g)/2及下述固定gauge-invariant Wick prescription；不另取正部分或state替代品 |
| dynamics | 不給演化公式，不聲稱unitarity／time-translation／vacuum；全部OPEN |

所有表中widehat D只讀P／R₀及列名上游，沒有L或n_τσ參數。
固定P／R₀、上游相同即輸出相同；不能從K／Green解碼L再造係數。
G_R的矩陣乘冪用於inverse恆等式，G_A的adjoint用於dual kinetic，F的乘法用於Green pairing；
不是把count重建後作奇偶／模數／查表／門檻／feature乘積。每項仍須在研究稿證實來源。

CAR trial固定為unital *-algebra的線性生成元a(f)與關係

$$\{a(f)^*,a(g)\}=A(f,g)1,\qquad \{a(f),a(g)\}=0. \tag{CF.S2}$$

a線性，代數*為共軛線性的involution。這是本試作明示的RΞ-L3識別規則，
須證Hermitian相容與同一inverse的Green恆等式；不宣稱已由微觀物理導出charged CAR。
不強加a(Kf)=0這種在可逆完整有限domain上會消滅全部field的homogeneous on-shell關係。
source解讀、physical adjoint與continuum仍須另證，不能由定義關係本身說已完成。

固定state trial的normal-ordered moments：ω_trial(1)=1，creation／annihilation數不同時為0，

$$\omega_{trial}\big(a(f_1)^*\cdots a(f_m)^*a(g_m)\cdots a(g_1)\big)
 =\det[Q(f_i,g_j)]_{i,j=1}^m. \tag{CF.S3}$$

其他排列按CF.S2處理。研究須先檢查其一致性／正性；若A或這些必要moments不正，
state交付記FAIL，不換Q、不縮test、不刪負方向、不改F。沒有第二個補救分支。
即使正A下這只是Q=A/2的通用Wick態，也只能記「按構造成立」，不算物理state來源機制。

## 5. 同一K／Green→form的可檢查義務與比較類

除了A Hermitian及完整T正性，固定要檢查的同鏈恆等式為

$$K^\dagger C K=i(K^\dagger H-HK). \tag{CF.S4}$$

它是用同一two-sided inverse與其dual改寫Green pairing的檢查，不能用無關正W代替。
若本規則有負方向，CF.S4不把它變正；若不能證識別，也不得只以F非恆定充作完成。

依契約§5.3事前固定counterfactual比較類K_t=tI_T+B，1≤t≤2；實際試作仍且只取t=1。
M_τσ與B不變，只變L-independent diagonal；以同一inverse／adjoint／F規則重求

$$G_R(t)=\sum_{j=0}^{N-1}(-1)^j t^{-j-1}B^j,\quad
 G_A(t)=H G_R(t)^\dagger H,\quad C(t)=iH(G_R(t)-G_A(t)).$$

此比較類不依正性篩選，也不作優化或第二個構造版本；只用於辨別F是否真正隨同一K變動。
必須證有兩個合法t給不同form；不能把t變動當作修復失敗之授權。

## 6. Ordinary-adjoint障礙的事前分項表

以下是規則及**已預想、待研究稿正式核對**的判定，不充作已交證明。

| OP-01障礙前提／環節 | 本版固定選擇與預期判定 |
| :--- | :--- |
| 原order retarded | 保留；CF.S1及inverse規則須證成立 |
| G_R diagonal Hermitian | K diagonal I；預想G_R diagonal I，故前提成立 |
| ordinary G_A=G_R† | 名義改用η-adjoint；但預想[K,H]=0，則實際仍成立，不能以改名聲稱逃出 |
| 總form i(G_R−G_R†) | 規則不相同：本版左乘H，C=iH(G_R−G_A)；須檢查零對角與負方向是否仍在 |
| 完整T上的positivity | 不刪原test，不預設通過；已預見零對角風險 |
| 下游重新讀L | 不成立／禁止；只有K帶入的影響與固定H |

## 7. 預定交付與停止

研究稿須逐式檢查：七種型別、自然性／換基與完整inverse、§6(a)(b)(c)(d)、
CF.S4與counterfactual非恆定、state必要正性、上述障礙前提，以及global R₀協變是否迫使與H交換。
不以star單例代替全域(b)，不以block span代替spin，不以indefinite rank代替(d)。
若量子橋接失敗，停止本版；conditional主問題與原始輸入問題均保持OPEN。
只報明定類別的障礙，不報所有Ξ下全面不可能。完整文獻mapping／新穎性及physical結果未完成。

本檔及後續研究只限紙上，無模型程式、symbolic／toy執行、RNG、撒點、producer、raw／sealed，
不讀禁止摘要選law，不發seed、不做科學主機消費／量測或receipt。
formal／E0、A／B、6a-E／Freeze-1a與UNKNOWN隔離不變。
