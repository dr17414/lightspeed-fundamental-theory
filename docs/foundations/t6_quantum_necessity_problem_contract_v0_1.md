# T6 — 量子一致性必要條件的問題契約 v0.1

狀態：**【提案／只定問題，待 exact-head 獨立複核】**。
Problem ID `X-T6-QUANTUM-NECESSITY-P0.1`；新 model ID **NONE**。
不提出K、state、算子、pairing、物理test space或projector的具體構造。
本契約只登記探索軌的型別／來源／必要條件問題，不提供新推導或新判決。

## 1. 選題、版本與研究開始條件

操作者於 **2026-10-20 11:00 Asia/Taipei／03:00 UTC** 選T6（只知分鐘，不補秒），
採Claude方向選項中的首選；題目說明於台北11:30:42／UTC03:30:42轉交。
選題由操作者決定，Claude提供建議並保留獨立複核角色，GPT起草契約。

main基線 **`a288dc6429495951679925f1a96698eea651a392`**，tree
`ac9600e8721852e193fd77a17b6a17ddc45fb7cc`，等於#91 GO的tree。
本PR**從紀錄分支head `8fa273158e7da9dd9e3f628330b62135e2f571fe` 接續**，
其parent正是上述main；EXP-0066／0067與全部既有紀錄保留，不重新編號。
ACT-X-0001生效SHA仍 `0c386716701589c9a6b0b799636a808aacb9ade5`，ACTIVE-PAPER-ONLY。
T2／T3限定解析交付已完成；其物理OPEN及C2暫停均不變。

r1受審head `aeca9033fadf87defde1a91468369a2be1500f09`／tree
`530a7d9f2fcf83957143d0caee437ed7211122e9` 保留原版。Claude本輪暫不GO，要求點名
§5.2.1(v)／D.1第8項依據管道及補齊0068；本r2只修該邊界與申報，不改研究問題。
r1當時0068原句未取回的紀錄保留於接觸帳§32；本輪操作者已提供本人原句，
在§33完成**原保留ID EXP-0068**，不另編ID或覆寫舊待補行，也不以0069替代。
0069／0070原紀錄保留；0071逐字記本輪複核申報，0072記作者只修訂／收錄的scope。
0068收件缺項已解除，來源補齊與本r2仍交新exact-head增量複核；
**本契約取得exact-head GO並原樣合併前，不開始具名T6研究推導。**
選題、原句收件或r2發布不等於審查與合併條件已完成。

## 2. 與正式C9／C10的隔離：本契約不設定驗收

[acceptance](../STAGE5C_ACCEPTANCE.md) §1.1–1.2限定本比較路徑為
**1+1維、massless、平凡two-sector fiber**；這不是spinor／chirality或3+1維主張。
T3沒有證明一般intrinsic spinor不可能；本題不擴張到3+1維，也不以T3拼出全面no-go。

acceptance §3的K／kinetic operator、G_R、W、spectral object ρ只作既有**型別引用**。
必要時以符號區分原文的演化kernel與kinetic operator，不靜默把G_R叫W。
本題不起草、不修改、不提議C9／C10的任何criterion、test-space／projector、
evaluator、norm／margin、排除predicate、prescription選擇或容差形式／數值。
本題也不提出可供formal採用的候選方案或「推薦的量子判準」。

原規格已有分層：§5.2.1(i)、(iii)與D.1第7項把core及能使其失效的形式／規則留給
Freeze-1a；D.2留給1b的是依該規則的實例化。只讀C9.1的舊簡述不能越過此限制。
Freeze-1a仍PENDING；本題不修規格中的歷史措辭或代替任何freeze交付物。

抽象數學中的「測試向量空間」或「正性」僅為問題型別，不是正式test-space／gate。
未來研究的必要條件或精確反例也永不直接產生C9 PASS／FAIL或SPEC-INFEASIBLE。
若研究者打算把T6的任何產出用於選擇core、test space、projector或evaluator，
**在選擇／回用前停止並記帳**；不得以「這只是必要條件」免除criterion污染審查。
回formal或Freeze-1b須另案handoff、exposure mapping與原§5.2.1／activation §5要求的
新版prereg及合資格獨立／blinded審核；換seed不補救，也不能把本PR當作form已凍結。
C9／C10、acceptance、prereg及所有formal檔案本次一個位元不改。

### 2.1 §5.2.1(v)／D.1第8項的依據使用隔離（r2增補）

本契約及T6後續產出一律標記：**探索軌，不具 §5.2.1(v) 依據資格**。
即使已獲解析複核、合併到main、寫進STATUS或被其他頁面轉述，在另案handoff、
完整exposure mapping與合資格獨立／blinded審查完成之前，**不構成**該條可採用的
「既有STATUS結論」，也不得以「數學上的必要條件」或其他轉述名義，用來完成
**D.1第8項路徑A**的聲明或決定C9／C10 core。合併與STATUS登記不提升依據資格。
這是T6探索來源的使用邊界，不更改acceptance對其他既有獨立依據的規定。

T6對Potting、Noldus及其他原文的閱讀／作用域定位**不是D.1第8項路徑B的mapping**，
不完成equation／dimension／signature／adjoint／convention對接，不取得承重資格。
既有動機性分級不變；Potting依C9.3原有的受限secondary cross-check也不因本題
升級或擴大。Araki等新增定位亦不自動成為formal承重依據。
未來若要轉用，必須另案按原規格處理並記錄其資格，不能以本契約、STATUS更新、
讀過原文或探索結果已確認來代替A路徑聲明、B路徑mapping或其合資格審查。

## 3. 六欄與輸入／型別帳

| 六欄 | X-T6-QUANTUM-NECESSITY-P0.1 |
| :--- | :--- |
| 命題 | 在既有1+1 massless two-sector比較路徑中，量子一致性每項義務需要哪些型別／額外資料？只登記來源與條件式必要性問題，不證量子實現或完整極限 |
| 定義域與輸入 | I6-ORD／NUM／UV／PHASE及下表逐項申報的比較資料；有限抽象代數問題與連續背景比較域分開，無具體K或state |
| 證據 | 路線圖§4 T6、acceptance §1.1–1.2／§3及C9既有定義、T3限定能力表；§6原文只用來定位適用條件，不作新證明或formal依據 |
| 未證橋接 | Hilbert／test space、adjoint／pairing、CAR形式、state來源、positive-energy與unitary dynamics、continuum mapping全部待分項審計；無operator不能完成極限 |
| 否定條件 | 若某前提不足、型別不能對接或存在限定反例，只否定精確命題／資料路徑；不由純量警告或裸矩陣符號推斷本路徑必敗 |
| 後續驗證 | 契約定案且來源缺項解除後，交具名紙上義務表及條件式證明／OPEN；任何具體K、state、pairing或正式criterion選擇需求，停止本題並另立先審契約 |

以下只是能力審計分類，不是本題採用的一組物理輸入。每個後續命題必須列實際使用的ID，
不能把新增primitive在下游改稱湧現。

| ID | 型別／待申報資料 | 限定 |
| :--- | :--- | :--- |
| I6-ORD／NUM | 有限strict poset及元素計數 | 不直接提供物理metric、時間平移、Hilbert norm或state |
| I6-UV | 原合法域內global realizer orbit／sector資料 | 平凡二標籤不等於量子module、局部chirality或CAR |
| I6-PHASE | 已給定complex amplitudes/phases及其附著位置／來源 | 不選law，不由複數數值自動得到正state或field algebra |
| P6-TEST | 抽象複測試向量空間、domain／topology、零向量關係及其物理來源 | 不指定任何實際C9子空間、projector或排除規則 |
| P6-HILB | 正Hilbert pairing、完成化、norm與representation的來源 | 與indefinite covariant pairing分型；不在本題選一個pairing |
| P6-STAR | 共軛、algebra *、covariant bar、basis及反線性慣例／可能的self-dual Γ | *、transpose、bar及Hilbert adjoint不能靜默互換 |
| P6-CAR | CAR代數型別、state-independent總反對易子sesquilinear form、normalization | 不把純量i(G_R−G_A)自動宣告為此form；不選形式公式 |
| P6-STATE | 正且歸一化的state、quasi-free／gauge-invariant／self-dual條件及來源 | state存在、quasi-free、純態、真空互不等同，不構造或挑選state |
| P6-GREEN | 同一未指定K的G_R／G_A型別、左／右inverse、contact term與boundary | retarded inverse不等於W；不選K、求逆法或邊界公式 |
| P6-TIME | 時間定向、平移／動力群、stationarity及其連續性／實現 | 正能量／Fourier spectral support所需的背景不能由偏序名稱補出 |
| P6-LIMIT | 1+1 massless外部比較域、分布型別、smearing／embedding mapping、極限順序與機率域 | 只列缺項，不選正式observable／evaluator、撒點方案或誤差容差 |

## 4. 固定交付：義務表（本契約的能力判定全部OPEN）

後續每個子命題只能判：①由明列既有I輸入及前提推出並附證明；
②本路徑需外加primitive，附P-ID及來源；③OPEN。
含多個子命題的格先拆列；「需外加」不等於所有其他來源路徑都不可能。
任何限定否定也須寫明其全稱範圍與輸出型別，不能合成全面量子no-go。

| ID／義務 | 必須先交代的事項／可能涉及的P-ID | 本次 |
| :--- | :--- | :--- |
| QO1 test space／Hilbert | 抽象domain、正pairing與完成化的關係；domain是否全體、何種零模關係有先驗來源；不替formal選子空間（TEST／HILB） | OPEN |
| QO2 adjoint／pairing | *、Hilbert adjoint、covariant bar及kernel legs如何對接，含符號、共軛線性與basis conventions（STAR／HILB） | OPEN |
| QO3 state來源 | state是何種algebra上的正歸一化functional、如何與同一未指定K／G_R相關；quasi-free是否額外假設（STATE／GREEN／CAR） | OPEN |
| QO4 Hermiticity／正性 | 被檢查的究竟是form、kernel還是Riesz表示；何種pairing下、對哪些完整domain向量陳述；正性與形式Hermiticity不混用（TEST／HILB／STAR） | OPEN |
| QO5 CAR／互補條件 | charged CAR、self-dual或Majorana型別；總form與兩種field ordering、state covariance之關係；zero-mode與無界domain另列（CAR／STAR／STATE） | OPEN |
| QO6 normalization／sum rules | form與場／來源的單位、equal-time語意及contact terms；不能靠rescale或刪模補成正規化（CAR／GREEN／TIME） | OPEN |
| QO7 正能量譜 | 若有stationary時間平移，誰的generator／Fourier支撐、何種state不變性；有限diamond沒有平移時不能直接寫p⁰≥0（TIME／STATE／LIMIT） | OPEN |
| QO8 unitarity／動力相容 | 若主張unitary evolution，需哪些algebra dynamics、state／GNS實現與連續性；不以二點正性代替全部動力義務（TIME／HILB／STATE） | OPEN |
| QO9 continuum對應 | K／G_R、CAR form、W與spectral object各自的mapping、量綱、收斂型別及依賴；平均G_R收斂不當作W／state已收斂（GREEN／STATE／LIMIT） | OPEN |

QO9只登記未來主張必須提供的完整量詞：固定哪些輸入、對每個或一致於哪些測試函數、
是distributional／operator／expectation／probability／a.s.的哪一種收斂、密度／窗口／IR極限順序。
沒有實際object及來源就維持OPEN；本題不替未構造的operator承諾收斂，也不選數值計畫。

## 5. 登記待證問題：不是本題預填答案

下列是定案後可在明確型別下研究的問題族，本契約不給新證明、不填能力格。
它們的scope是抽象必要條件，不是新的C9 evaluator／acceptance criterion。

1. **QN1 — CAR covariance的型別與互補性。** 對事前明列的抽象測試空間、*與總CAR
   form A，什麼條件下可把state兩點form Q表成「0≤Q≤A」？若以一個已給定正Hilbert
   結構正規化成operator S，原文「0≤S≤1」需哪些識別／有界性／normalization？
   若採self-dual型別，Γ與其互補關係需另交哪些前提？形式退化或無界時，
   null quotient／完成化是否合法及其來源均須另證；不在此預設quasi-free sufficiency。
   charged情形須把gauge-invariant與不作此假設的支系分開；後者的anomalous兩點／完整
   covariance資料義務另列，不以單一normal Q的上下界代替全部條件，也不省略self-dual Γ。
2. **QN2 — 不定號反對易子form的限定障礙。** 在*與正Hilbert意義均已固定、且某form
   **確實已對接為CAR總form**的條件下，不定號是否排除正歸一化quasi-free state？
   是否有更一般state層級的結論？每個量詞與前提都須明寫，不能只看一個表示矩陣的符號。
   特別對i(G_R−G_A)，須先證與該form的同一性，否則不適用此問題的否定分支。
3. **QN3 — scalar SJ與fermionic比較的缺口。** 純量CCR的Pauli–Jordan object與CAR
   form在哪些型別／adjoint條件下不同？正部分prescription能否保留所需fermionic
   總反對易子及互補normalization？只審計必要條件，**不採用正部分來構造本題state**。
4. **QN4 — 單段Green資料到量子／continuum的缺項。** 在既有1+1 massless比較範圍，
   哪些state／boundary／IR／time與mapping假設尚無來源？可證的抽象轉用命題需哪些
   固定domain與量詞？若必須提出具體K、state、pairing或spectral projection，停在OPEN，
   另立構造契約，不能藉「補一個例子」跨過本問題的邊界。

若定案後只重現已知CAR定理，須標文獻校準；實質待查的是本路徑的型別對接與資料來源，
不能把重述已知不等式當成新的量子實現結果。
這些問題已受reviewer記憶性提示啟發，來源見EXP-0069；不稱盲選題。
正性、CAR相容與譜支撐是不同義務，不能用其中一項替全部quantum viability背書。

## 6. 原文定位（作者讀取；只作作用域對照）

本輪新讀的原文定位如下；不是formal equation mapping或新研究結果，
更不表示Claude也讀了原文。未完成本專案1+1、adjoint／signature／normalization
對接的公式不得直接套用；原文構造不因此獲准成為本題候選材料。

| 原文／實際讀取 | 本次只用來界定的範圍 |
| :--- | :--- |
| Araki，*On Quasifree States of CAR and Bogoliubov Automorphisms*，Publ. RIMS 6 (1970/71), 385–442；[出版社](https://ems.press/journals/prims/articles/2511)與[原PDF](https://ems.press/content/serial-article-files/41673?nt=1)，§2及§3 Lemmas 3.2–3.3，pp.386–389；OCR不清處查看p.388頁圖 | 原文是給定complex Hilbert及antiunitary involution的self-dual CAR。其covariance條件含正contraction與Γ互補條件；不能只摘「0≤S≤1」當作任意kernel的結論。本契約不重證其state存在定理 |
| Johnston，[0909.0944v2](https://arxiv.org/html/0909.0944v2)，§I及§II／II.1 Eqs.(18)–(30)，工具亦回傳§III開頭與數值討論 | 有限causet的**實bosonic scalar／CCR**與所宣告Hilbert結構；正部分是其scalar prescription，不是本題CAR公式或預選state |
| Sorkin，[1107.0698v2](https://arxiv.org/html/1107.0698v2)，§2、§3開頭及Eqs.(1)–(7)相鄰段 | histories與operator的scalar QFT，commutator、state及Green資料分層；不把其正／負頻率替代機制直接搬到fermion |
| Afshordi–Aslanbeigi–Sorkin，[1205.1296v4](https://arxiv.org/html/1205.1296v4)，§2–3、Eqs.(3)–(12)與工具回傳的引言段 | scalar SJ在其volume／L²、self-adjointness條件下的正部分；Hermitian form與self-adjoint operator不能無條件等同。此ASS與Track A所指的1403.1622不是同一篇 |
| Potting，[1112.5739v2](https://arxiv.org/html/1112.5739v2)，§III Eqs.(26)–(31)、(46)–(54)與相鄰段；工具亦回傳(32)–(45) | 原文LV背景、4D fermion／scalar與Dirac adjoint。spectral matrix、positivity及equal-time normalization的型別須分開；沿C9.3不移植其basis／sum rules，不把4D結果當1+1證據 |
| Noldus，[1305.0443v3](https://arxiv.org/html/1305.0443v3)，§3及前接§2末；工具另回傳§2例子與§4 ghost例子片段 | 原文分開bar與Hermitian adjoint並討論mixed／negative norm。其generating structure與vacuum未採用；不把ghost警告擴成所有causet fermions的no-go，也不把indefinite表示當本題正C* state |

Track B的4D純量正性、BBMM原作用域的負模警告、spectral-dimension曲線及先前C2的
Green讀值收斂均不能替代QO1–9。本文只讀STATUS的既有紀錄，不重跑那些結果。
原文的相位、符號、measure、spacetime dimension及bar／*未完成對接時，明記OPEN。

## 7. 驗收、歷史與停止條件

本契約的交付是：一個問題ID、六欄、輸入帳、全OPEN義務表、待證問題與原文作用域。
**沒有新必要條件證明、反例、物理判決或具名模型。** 定案後才可交具名紙上研究；
任何舊版與退回原因須依head保留，不看研究答案後回改本契約。
若審計發現問題型別需改，在推導前先修契約供新exact-head複核，不能事後放寬。

若需要新增K／state／pairing構造、選擇正式criterion、接觸L4 oracle或禁止資料、
對數值作診斷／參數選擇，立即停止對應工作並記帳；不得用「只是探索」豁免。
只限紙上，不撒點、不用RNG、不作數值／符號診斷、不呼叫producer，不產生seed、
不開主機、不量測／receipt。既有regression與integrity只作repo驗證，不算科學證據。
review-only工具亦不能被用來開始QN1–4的新探索或改正式判準。

E0、formal／C9／C10、item7不可ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、
Freeze-1a PENDING、C2暫停及T2／T3所有限定確認／OPEN、UNKNOWN／禁止資料隔離全部保留。
本契約即使GO並合併，也不授權量子模型或正式C9實作，不消耗或恢復任何holdout資格。
