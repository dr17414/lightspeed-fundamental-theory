# T2＋T3 — 物質選幾何與全域 sector 能力的問題契約 v0.1

狀態：**【提案／只定問題，待 exact-head 獨立複核】**。
本問題的新 model ID：**NONE**；沒有提出 K、作用量、算子、場方程或構造。
兩個獨立 Problem ID：`X-T2-MATTER-GEOMETRY-P0.1`、`X-T3-SECTOR-SPINOR-P0.1`。
一題的否定／未決不自動否定另一題；本契約不預填兩題的研究答案。

## 1. 決定、版本與共同邊界

操作者選題時間：**2026-10-19 14:44 Asia/Taipei／06:44 UTC**（只知分鐘，不補秒）。
操作者於台北14:46:13／UTC06:46:13轉交題目說明：採Claude方向建議中的T2＋T3，
依[路線圖](../THEORY_FIRST_ROADMAP_DRAFT.md) §3–4；**C2線暫停新增研究**。
已確認的單段／雙段結果及全部OPEN橋接保留，不撤回或擴大其作用域。

PR #88 head `bde2ca038b0170692048fc0ee04528b8f933e6cf`／tree
`06bae466a0c3b71551664c994a260fec63f51ef9` 獲Claude GO，CI #280 success後原樣合併。
本契約基線改為合併後main **`b80ef2fd566ffabb43b5a77581087ef37938ebc7`**，tree相同；
Git committer UTC2026-10-19 06:47:32／台北14:47:32。
選題在此merge之前，契約在merge及tree核對後起草，不把merge時間當選題時間。
ACT-X-0001生效SHA仍 `0c386716701589c9a6b0b799636a808aacb9ade5`，僅紙上。

本輪只作定義／問題／文獻作用域定位，不作新證明、反例構造或機制選擇。
全部文獻只是來源對照，不把他人構造導入本問題或宣稱已取得其證明。
EXP-0056逐字保存#88複核申報；EXP-0057保留給未取得原句的上一則方向建議申報，
EXP-0058逐字保存本輪題目說明申報，EXP-0059記作者讀取／檢索／契約scope。
在0057本人原句補齊並完成來源審查、本契約獲exact-head GO及原樣合併之前，
不開始任何一題的具名研究推導；不把本次選題或draft發布當成上述條件已完成。

## 2. 共用輸入帳：定義不是已導出結構

以下是能力審計的輸入／外加項分類，不是採用一組物理模型。

| ID | 型別與本題角色 | 引用限制 |
| :--- | :--- | :--- |
| I-ORD | 有限strict poset；T3的BHS對照另使用可數、order-interval locally finite的配置 | 不由有限poset自動得到流形、拓撲、維度或Poisson law |
| I-NUM | 有限子集的元素數 | 不直接等同物理體積、密度或尺度 |
| I-PHASE | 已給定的複數振幅／相位資料；每個具體命題須指明附著於事件、關係還是history，及重標記作用 | 本契約不選phase law或其分布；附加場不能當作order導出資訊，也不能暗中帶入frame／矩陣指標 |
| I-UV | 既有Stage 5A的global realizer sector pair及其交換／orbit資料 | 只在原本已證／已測的域引用；κ>1與realizer選擇義務保留，不假設所有poset都有唯一pair |
| P3-FIB | 複向量空間、維數、標量體、dual／adjoint、grading或內積的選擇 | 給每點兩個標籤與指定向量空間是不同資料；若需外加，逐項記此ID及子項 |
| P3-GEO | 外部Minkowski背景、維度、metric、時間／空間定向、Poisson密度與邊界 | 只作條件式比較域，不稱由I-ORD／NUM推出；有限diamond及其boundary明記為外加 |
| P3-REP | Lorentz／Spin作用、Clifford乘法與fiber間的識別／傳輸資料 | 作待審能力的目標或外加primitive；不因使用標準名稱就視為已存在於global sector |
| P3-MASS | 質量耦合的配對、conjugation／adjoint及物理尺度 | 只列型別／義務，不選耦合矩陣、質量值、動力學或K |
| P2-CLASS | 固定N的history類別predicate與其來源 | 流形類、KR類及其他非流形類分開，不由「不是KR」推出流形性 |
| P2-MEASURE | history權重、物質場積分的測度／邊界／零模處理與歸一化 | 若不由既有輸入推出，就是額外假設；本契約不採用具體物質作用量 |

後續每個命題附一張實際使用的ID清單；引入新資料必須新增子ID及來源，不能在下游省略。
comparison target所需資料不算intrinsic derivation的輸入，除非明確把結果改稱條件式。

## 3. T3：global sectors的資訊能力

### 3.1 六欄與交付

| 六欄 | X-T3-SECTOR-SPINOR-P0.1 |
| :--- | :--- |
| 命題 | 在明列輸入及局部性／等變型別下，global sector提供哪些結構、哪些需要新primitive？只交能力矩陣、必要條件與限定no-go的問題審計，不聲稱K或spinor存在 |
| 定義域與輸入 | I-ORD／NUM／PHASE與在其合法域內的I-UV；1+1與3+1分帳。有限poset／finite diamond與full Minkowski Poisson域不可混用；比較目標依§3.2–3.4 |
| 證據 | Stage 5B Result B §1–6、handoff v2 §2.2及路線圖§3為既有約束；§5原文閱讀只作定位。本契約不提供新證明 |
| 未證橋接 | P3-FIB／GEO／REP／MASS的來源、可測性／等變性、fiber與spacetime表示的連結、非trivial傳輸／質量詮釋仍須分項交代 |
| 否定條件 | 反例或no-go只否定其精確輸入／維度／輸出型別；若只能外加結構，登記需primitive，不寫所有spinor或物質不可能 |
| 後續驗證 | 契約定案後才作紙上能力審計；逐格交出證明／primitive ID／有作用域的no-go／OPEN。不得產生或測試K，也不啟動既有numerical witness |

能力矩陣的固定四列、兩個維度如下；**本次全部OPEN，不預填新研究答案**：

| 能力列 | 1+1維 | 3+1維 |
| :--- | :--- | :--- |
| a. 全域標記及global交換／orbit | OPEN | OPEN |
| b. 每事件的內部fiber及其局部資料 | OPEN | OPEN |
| c. Lorentz／Clifford表示 | OPEN | OPEN |
| d. 質量耦合（手徵混合） | OPEN | OPEN |

後續每格只能有一種有界判定：①由所列I輸入推得，附完整證明；②需外加primitive，
附P-ID及缺的資料；③在明列作用域下的no-go；④OPEN。
若一格含多個不同子命題，先編子ID分列，各自判定，不能用一個正面子結果覆蓋整格。
既有有限域結果可在其原作用域作證據，不把一格OPEN解讀為撤回既有Result B。

### 3.2 「局部」先分型別

主要審計型別是 **L-EQ：可測且等變的輸出賦值**；它可以依賴整個配置，
因此不能僅因輸出寫成F_x就稱microscopic locality。
另列 **L-FIN：由一個規則選定的有限pointed induced suborder決定**。
使用L-FIN時須給該子序的選擇規則、重標記自然性、可測性，以及是否有統一大小上限；
本契約不預設這種選擇規則存在。兩種型別的判定不得互相代用。

order-interval局部有限不保證Hasse圖的有限半徑鄰域是有限集合；
有限graph-hop半徑、有限事件數、compact continuum window須各自申報，不能同名為局部。
若需要第二anchor、boundary或frame才能指定鄰域，記為額外輸入，不歸因於單點order。

### 3.3 等變性與BHS比較域

固定D=2或4、完整Minkowski空間、正的固定密度ρ，令Ω_D為局部有限點配置空間，
Σ為由bounded Borel sets的計數生成的σ-algebra，μ_ρ為homogeneous Poisson law。
這是**紙上機率域**，不實際撒點。固定來源原點只作BHS的比較錨點。
G_D=SO⁺(1,D−1)作用於配置，μ_ρ對其不變。

「BHS型等變映射」在本契約指可測F及已明訂的target G_D作用，滿足

$$F(\Lambda\omega)=\Lambda\cdot F(\omega),\qquad\Lambda\in G_D.$$

主要版本採逐配置等變；若某命題改用a.s.版本，須明定共同不變滿測度定義域，
並另核定理是否支持。僅要求F(ω)的law不變或兩邊同分布，不冒稱上述逐配置等變。
Poisson law的分布不變性與F的等變性是兩個前提，不說BHS只有「分布意義」的要求。
spinor target的作用使用Spin⁺(1,D−1)及其到G_D的覆蓋，須申報中心作用；
不把spin representation誤寫成普通vector representation，也不要求非緊群有限維表示unitary。
表示欄審計的是module結構及其frame／gauge等價，不要求從撒點選出一個非零spinor、
唯一spin frame或preferred section。若另問這類section選擇，須分列新子問題，
不能用該選擇的中心作用障礙替整個fiber／表示問題作no-go。

BHS只約束其文中方向輸出及相關有限方向／valency推論；
不能直接替任意abstract internal fiber下no-go。
finite diamond或附加boundary可帶方向，與full-space問題不同，不算繞過定理。
若額外phase marks參與方向選擇，須先說明其joint law／等變作用並重核定理前提，
不得把unmarked Poisson定理原封套到任意帶標記模型。

### 3.4 表示與質量能力的比較目標

「fiber」至少區分集合標籤、複向量空間與具表示結構的module。
本契約的Clifford比較目標是在外部參考Minkowski背景下，
每點複向量空間E_x上有線性的Clifford乘法c_x，對任意covectors ξ、ζ滿足

$$c_x(\xi)c_x(\zeta)+c_x(\zeta)c_x(\xi)
       =2g_x^{-1}(\xi,\zeta)\,\mathrm{id}_{E_x}.$$

signature convention是(+,-,…,-)。Dirac比較空間維數分別為D=2的2、D=4的4；
Weyl子空間及其Spin作用另列，不能把Weyl二分量當成完整4維Clifford module。
這是**目標的型別定義**，沒有給任何γ矩陣、表示選法、離散算子或構造；
g、E_x、Spin作用、chirality grading及其識別的來源均屬能力審計，不預設已導出。

質量欄只問是否有明確的左右手徵分解、dual／adjoint與Lorentz scalar的跨手徵配對型別，
以及這些資料是否由輸入提供。任意two-slot mixing不等於物理質量；
不在本題選質量值、mixing matrix或動力學，也不僅以改變基底後的off-diagonal命名質量。
後續若要主張mass shell或massive continuum propagation，必須另立問題契約。

## 4. T2：物質選幾何的總量定義義務

### 4.1 六欄與問題類型

| 六欄 | X-T2-MATTER-GEOMETRY-P0.1 |
| :--- | :--- |
| 命題 | 任何「物質／費米子使KR類相對流形類受抑制」主張，須先有什麼history、measure、weight、class sum與漸近比較？交付定義義務及可待證的必要條件，不證選幾何成功 |
| 定義域與輸入 | 固定N的全標記有限strict posets；§4.2固定共同計數與歸一化慣例，§4.3–4.5固定抽象權重型別及比較量。類別predicate／物質因子為命題必須申報的輸入，這輪不選其具體模型 |
| 證據 | STATUS的Q_test固定相位／結構敏感性／KR熵列、handoff v1 §7.1–7.3、路線圖§3.1；§5只比較既有重力抑制文獻的作用域 |
| 未證橋接 | P2-CLASS／MEASURE、物質積分的良定性、相位／模長、流形類振幅的下界與相消、其他非流形類、量子機率詮釋均未交付 |
| 否定條件 | 單history的phase或log模長、class entropy而無共同class sums、分母未定／可能為零、重力與物質作用未分離，均不足以支持選幾何；不足記OPEN，不把BdG限定no-go推廣 |
| 後續驗證 | 契約定案後只做紙上定義與必要條件審計；若需具體K／作用量／物質積分構造，停止此題並另立先審契約，不在本題挑公式 |

這是對**一類主張之定義與必要條件**的審計，不是預登一個尚未給定作用量的抑制實驗。
下列未指定函數是帶型別的占位輸入，沒有給它們公式或預填答案。
任一後續具體命題必須在證明前列明全部輸入與N依賴；缺項時只能交缺口表，不能稱定理。

### 4.2 Histories、標記與歸一化

本契約固定Ω_N為集合[N]上**所有**strict partial orders，不限naturally labelled orders。
每history的共同bare measure取μ_N(C)=1/N!；這是計數慣例，不是已導出的物理測度。
改用同構類時須明記相應的automorphism權重，不能把「每個無標記poset等權」當同一問題。
後續須交出兩種記法的換算及N² leading entropy是否受影響；本次不作該證明。

K_N、M_N分別是Ω_N中KR與目標流形類的**明確、重標記不變predicate**，作為量化命題的輸入。
本題不挑某個有利predicate；定義義務必須寫出精確KR family、有限N容差、
流形類維度／boundary／嵌入或近似判準、兩類是否相交及非空性。
若該資料未固定，對應比較維持OPEN；不把「由某次撒點得到」當未定容差的membership test。
排除KR不等於排除全部非流形類；每增加一類，須另列總量義務。

STATUS的熵尺度exp[(ln2/4)N²]只作來源待核對的leading尺度。
後續必須對**同一K_N與measure**給精確漸近敘述／上或下界及o(N²)餘項用途；
不能把原文≈當所有N的數值界，亦不能忽略naturally labelled、任意標記與無標記的差別。

### 4.3 權重與作用量的型別，不給候選

令s_G,N(C)為尚未指定的實值無量綱重力作用量占位輸入，
F_N(C)為尚未指定、重標記不變、有限的複數物質有效因子。
前者可固定為0作「純物質」的條件式子問題；不能以此宣稱真實重力不存在。
F_N不是本契約提出的determinant、K或任何作用量；本輪不選其公式、參數或場積分。
若後續以物質積分定義F_N，必須先列物質自由度／Grassmann代數、measure、
boundary條件、regulator、零模／零det及branch處理，並證有限性與重標記不變性。
把複數因子改寫成effective action還須另處理零點與log分支，不能默認其存在。

作為比較量的**定義**，記同一類A⊂Ω_N的有／無物質總振幅：

$$Z_N^{(0)}(A)=\frac1{N!}\sum_{C\in A}e^{i s_{G,N}(C)},\qquad
Z_N^{(1)}(A)=\frac1{N!}\sum_{C\in A}e^{i s_{G,N}(C)}F_N(C).$$

共同N依賴耦合、尺度、boundary與regulator在比較前固定；不能分別對KR與流形類調參。
物質因子的modulus可能不是1；純phase情形只是額外限定子類，不能代替所有費米子機制。

### 4.4 「壓低／選中」固定看什麼

主要比較量固定為R_N=|Z_N^(1)(K_N)|／|Z_N^(1)(M_N)|。
本題的「KR相對受抑制」目標語意是：分母對充分大N非零，且R_N→0。
這僅是兩個已指定類的**振幅比**，不稱流形類被機率1選中或整個path sum已由流形支配。
若需「指數抑制」，另外要求存在固定γ>0與N_0使所有N≥N_0有R_N≤exp(−γN²)，
另列子命題，不把較弱比值極限自動稱此速率，也不要求所有輸入共用γ／N_0。

共同1/N!是本契約的歸一化慣例，不用各類自身大小再各除一次而抹掉熵。
不預設總partition function非零，也不以Z(A)／Z(Ω_N)自行建立機率；
若要機率主張，需另有state／decoherence／measurement或其他明確規則，超出本題。
流形類分母的非零性及可用下界是獨立義務，不能以Σ|weight|的上界代替。

「物質造成改善」還須與相同s_G,N及classes下的R_N^(0)比較；
當相關分母非零時才可定義改善比R_N／R_N^(0)。
若重力baseline已相消為0，該改善比未定，不把既有重力抑制算作物質的功勞。
任一分母零或無法下界時，保留未決或改列有明確作用域的其他主張，不能偷偷換類或norm。

### 4.5 純phase必要條件：只登記待證問題

限定F_N=e^{iθ_N}且s_G,N=0，對A=K_N或M_N定義
W_N(A)=μ_N(A)，以及相消比例χ_N(A)=|Z_N^(1)(A)|／W_N(A)（W_N(A)>0時）。
待證問題是：給定同一measure下的KR熵敘述及流形類總振幅的獨立下界，
上述相對抑制／指數抑制分別對χ_N(K_N)要求什麼必要速率？
必須保留對M_N的相消與分母義務，不只比較單個history或KR類自己的平均phase。
**本契約不填臨界指數、隨機相位剩餘量或任何「足夠」答案**，不假設phases獨立或隨機。

BdG固定相位結果只約束路線圖§3.1的特定unshifted square block；
零det時無相位。不能外推為所有費米子權重、有效作用量或物質－重力耦合皆無用。
Q_test結構敏感性亦不能替代本題class總量義務；本輪不重跑其既有測試產生研究證據。

## 5. 文獻定位：本輪實際讀取的作用域

以下於2026-10-19讀原文指定段落，不是完整文獻盤點、重證或新穎性主張。
沒有把文獻中的模型／算子公式採為本題候選。舊repo引用及外部新閱讀分別記帳。

| 來源、版本與實際閱讀位置 | 本契約採用的有限定位 | 不能據此宣稱 |
| :--- | :--- | :--- |
| Bombelli–Henson–Sorkin (2006)，[gr-qc/0605006v1](https://arxiv.org/html/gr-qc/0605006v1)，§2 Theorem 1及延伸(1)–(5)、§3 | full Minkowski Poisson、可測方向映射的逐配置Lorentz等變要求；finite-region boundary例外需保留 | 所有internal fiber不存在，或僅有不變law就滿足該映射假設 |
| S. P. Loomis、S. Carlip (2017預印本v2)，[1709.00064v2](https://arxiv.org/pdf/1709.00064v2)，§1、§3–5，式(3.1)–(3.3)、(4.14)–(4.15) | Lorentzian重力path sum的two-level orders抑制有耦合參數域；§5的KR延伸仍是當時的待辦 | 該篇已證全部KR／全部非流形類被壓低，或已證費米子作用 |
| Abhishek Mathur、Anup Anand Singh、Sumati Surya (2020預印本v2)，[2009.07623v2](https://arxiv.org/pdf/2009.07623v2)，摘要、§1、§2開頭標記定義、§3.1與§3.4末／§4 | 以link action將相關leading分析延伸至KR等層狀類；§3.4展示子類限制會影響總和結論，須帶class定義 | link action等於一般BDG／Einstein–Hilbert作用，或所有子類／物質機制皆已受控 |
| Roman Sverdlov (2008)，[0808.2956v1](https://arxiv.org/pdf/0808.2956v1)，摘要、§1與§2中vierbein／scalar-field定義段、式(9)–(15) | 原文引入holonomy、vierbein及額外scalar資料表述spinor；用作primitive來源比較 | 單靠本專案global U/V已導出spinor，或本輪已驗證該篇整套構造／Lorentz性 |
| Steven Johnston (2010博士論文)，[1010.5514v1](https://arxiv.org/html/1010.5514v1)，§6.1–6.3開頭及§7.1 | 分開continuum Clifford／spinor條件與causal-set spin-half構想，後者原文定位為speculative suggestions | 已有純order＋phase導出的3+1維Dirac結構，或本輪採用checkerboard／square-root模型 |

上述重力文獻與本題「物質／費米子作用」不同；本題不重做其抑制計算。
文獻結果不自動提供本契約measure、classes或weight的相容性，後續必須逐項mapping。

## 6. 交付、停止與獨立審查

本契約可交付物只有：兩個問題的六欄、定義型別、能力矩陣schema、class總量義務與來源表。
契約合併後的研究依兩ID獨立判定，不因T3無法從sector得到spinor就否定所有T2機制，
也不因重力path sum有抑制就判定T2的物質假說成立。

以下情形停止該子問題並記錄：需要設計K／作用量／具體operator或新數值資料；
需要正式／sealed／禁止oracle；發現新primitive未記帳；改變了受審的target、measure、
class predicate語意、比較norm或no-go量詞。先另立修訂契約，不在研究後補選判準。
定義不足、文獻未核或無法證明都可交OPEN；不是為取得正面答案放寬範圍。

只限紙上：不撒點、不用RNG、不作數值／符號診斷、不呼叫producer，不產生seed、
不開主機、不量測。既有regression／integrity與Git／文字比對只驗證repo。
E0、formal、item7不可ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、
Freeze-1a PENDING，以及UNKNOWN／禁止資料與回F限制全部保留，沒有scientific PASS。
