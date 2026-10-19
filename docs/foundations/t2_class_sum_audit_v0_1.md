# X-T2-CLASS-SUM-AUDIT-v0.1 — 物質選幾何的總量與必要條件審計

狀態：**【探索／完整紙上稿待 exact-head 獨立複核】**。
Problem ID `X-T2-MATTER-GEOMETRY-P0.1`；Study ID `X-T2-CLASS-SUM-AUDIT-v0.1`。
新 model ID **NONE**；沒有提出K、物質作用量、effective factor公式或候選算子。

## 1. 定案、先後與六欄

[契約v0.1](t2_t3_problem_contract_v0_1.md) blob
`434e85fcd10a0f5b8590f556ec9a60e9469750de` 全文保留。
#89 r2 exact head `0f56e95103611613cef4b7c0e7135365271e7229`／tree
`3ec3353628cc57d6230ea891f358013226a89bc8` 獲Claude GO；CI #283的run39222282955
與job117960164574均成功，原樣squash為main **`cae0f69e24e3ca0bcf4820deaa284efec5749819`**，tree相同。
Git committer UTC2026-10-19 **12:48:54／台北20:48:54**。
本推導在merge及tree核對後開始；EXP-0057已於原保留ID逐字補齊並獲增量GO。
ACT-X-0001生效SHA仍0c386716，僅紙上；T3為獨立問題，不由本稿判決。

| 六欄 | 本研究 |
| :--- | :--- |
| 命題 | 精確換算標記／同構類measure，給純phase抑制的等價尺度、上下界各自的必要／充分角色，以及物質改善的有界條件；不證實際選幾何 |
| 定義域與輸入 | 定案Ω_N、μ_N=1/N!、重標記不變且在證明前固定的K_N／M_N與有限複數F_N；各命題另列非空／分母正值／漸近假設 |
| 證據 | §2 orbit–stabilizer及正量squeeze；§3原文作用域；§4精確比值恆等式與雙側界；§5同重力baseline比較。均紙上，待複核 |
| 未證橋接 | 具體P2-CLASS、物質積分／F_N、流形類分母下界、全部非流形類與機率詮釋仍OPEN；未導出mass或器件 |
| 否定條件 | 若class、measure、分母或極限假設不滿足，對應命題不可用；不以改class／norm／權重來維持成功 |
| 後續驗證 | exact-head核對§2換算及§4不等式方向、零值與邊界速率；若需具體K／作用量，先另立契約，本稿不構造或執行 |

§4的相消提示及KR計數記憶性提示已接觸，見EXP-0060；不是本稿的證明來源或盲推導。
原文閱讀及作者scope見EXP-0063；所有新結論仍待獨立複核。

各命題實際輸入如下；P-ID只標額外資料的型別，不代表本稿選了具體模型。

| 命題／段落 | 實際使用的ID與額外條件 |
| :--- | :--- |
| (T2.1)–(T2.3) | I-ORD／I-NUM、P2-CLASS（任意重標記封閉類）、P2-MEASURE的定案1/N!；f為任意同構不變有限複數函數；漸近式另需非空及已證leading計數 |
| §3原文換算 | 同上；KR原文的具體class不能替代未申報P2-CLASS |
| (T2.5)–(T2.9) | I-PHASE附著history、P2-CLASS／MEASURE；固定純phase子題與最終正分母，各上下界／極限條件另列於命題 |
| (T2.10)–(T2.11) | P2-CLASS／MEASURE及I-PHASE的history因子；一般有限F_N與同一重力baseline，指定的非零分母／模長界；不引入新物質公式 |

## 2. 標記、automorphism與正計數

對任意重標記封閉的A_N⊂Ω_N，記其同構類集合為U(A_N)，L_N=|A_N|、
U_N=|U(A_N)|，a(C)=|Aut(C)|。對同構不變的有限複數函數f，有精確恆等式

$$\frac1{N!}\sum_{C\in A_N}f(C)
     =\sum_{[C]\in U(A_N)}\frac{f(C)}{a(C)}.\tag{T2.1}$$

證明：S_N作用在標記posets上；一個同構類的stabilizer是Aut(C)，
故該orbit有N!/a(C)個標記版本。把左和逐orbit分組即可，複數或零f均合法。□
所以改用同構類且保留1/a(C)是**同一振幅**；改成每個同構類等權則不是。

定義W_N(A_N)=L_N/N!=Σ_[C]1/a(C)。由1≤a(C)≤N!得

$$L_N/N!\le U_N\le L_N,\qquad W_N\le U_N\le N!W_N.\tag{T2.2}$$

若A_N最終非空，且log L_N=hN²+o(N²)，因
0≤log N!≤N log N=o(N²)，(T2.2)給

$$\log W_N=hN^2+o(N^2),\qquad\log U_N=hN^2+o(N^2).\tag{T2.3}$$

這不需假設poset rigid。只證**正計數leading entropy**相同，
不能把三種measure中的複數總和視為可互換，或聲稱其相對誤差很小。
例如對兩個形式項，正係數a≠b與複數值b、−a使a·b+b·(−a)=0，
但等權和b−a≠0；此兩項代數例只否定「正係數可任意換」的推論，
不是給任何history指定物質權重或新作用量。

## 3. KR原文究竟核實了什麼

Kleitman–Rothschild (1975), *Asymptotic enumeration of partial orders on a finite set*,
Trans. AMS 205, 205–220，DOI [10.1090/S0002-9947-1975-0369090-9](https://doi.org/10.1090/S0002-9947-1975-0369090-9)。
AMS PDF本輪返回403；實際讀的是[第一作者上傳的原文轉錄](https://www.researchgate.net/publication/243778189_Asymptotic_Enumeration_of_Partial_Orders_on_a_Finite_Set)，
§1–3及工具回傳的§4片段；沒有重證全文技術lemma，也不使用OCR不清的精細prefactor。
原文§1明言其log以2為底，對固定N元素集合上的全部partial orders P_N寫出

$$\log_2 P_N=N^2/4+3N/2+O(\log N).\tag{T2.4}$$

原文§3 Theorem比較的是P_N與其具體Q_N；不能把式(T2.4)套給任意被稱作KR的子類。
因此對**本契約任意待申報K_N**，h_K仍是需證的假設，不因文獻名稱相同就填ln2/4。
在已另行核對同一class的leading h_K=ln2/4時，§2才允許把該leading值帶到契約measure。
這是來源／換算界線，不是本稿選出一個新的K_N或M_N。

實際主張前仍須補：兩類的精確predicate、N依賴容差、維度／boundary、交集／非空性，
以及與引用原文class的mapping。M_N本輪未選；沒有實際selection verdict。
naturally labelled orders也不能冒充全部標記orders；本稿未對前者建立新漸近公式。

## 4. 純phase：精確條件與上下界方向

本節只用契約限定子題s_G,N=0、F_N=e^{iθ_N}，不選θ_N或其law。
在充分大N假設W_K:=W_N(K_N)>0、d_N:=|Z_N^(1)(M_N)|>0，定義
χ_N:=|Z_N^(1)(K_N)|/W_K。三角不等式給0≤χ_N≤1及d_N≤W_N(M_N)。
定案的比較量有精確式

$$R_N=\frac{W_K\chi_N}{d_N}.\tag{T2.5}$$

### 4.1 不用leading近似的答案

直接除以正量即得

$$R_N\to0\quad\Longleftrightarrow\quad
       \chi_N=o(d_N/W_K).\tag{T2.6}$$

對事先指定的γ>0，R_N≤e^(−γN²)（最終所有N）等價於
χ_N≤e^(−γN²)d_N/W_K（最終所有N）。這是逐N的精確必要且充分條件，
包含χ_N=0，不要求相位隨機或獨立。

### 4.2 只有分母下界，不能得到尖銳必要速率

若獨立證據只給0<d_N^-≤d_N≤d_N^+，則

$$\frac{W_K\chi_N}{d_N^+}\le R_N
                  \le\frac{W_K\chi_N}{d_N^-}.\tag{T2.7}$$

因此χ_N=o(d_N^-/W_K)是**充分**條件，
而R_N→0的**必要**條件是χ_N=o(d_N^+/W_K)。
契約提到的流形類獨立下界只能支撐前者；不能把其方向倒過來稱必要條件。
只有實際d_N、匹配的雙側尺度或可用上界，才能補足所需必要資訊。
若只有正下界但不知道實際d_N增長多快，不能填一個唯一的必要臨界指數。
純phase下d_N^+=W_N(M_N)是合法但未必緊的選擇；其class entropy也要另證。

### 4.3 N²速率的條件式判讀

當χ_N>0時定義h_N=N⁻²log W_K、a_N=−N⁻²logχ_N、b_N=N⁻²log d_N；
χ_N=0時用a_N=+∞、log R_N=−∞。則(T2.5)給

$$N^{-2}\log R_N=h_N-a_N-b_N.\tag{T2.8}$$

「存在某固定γ>0的最終指數抑制」等價於

$$\liminf_{N\to\infty}(a_N+b_N-h_N)>0.\tag{T2.9}$$

證明：若有最終γ界，右量至少γ；反之選比正liminf小的γ，最終即有該界。□
特別在h_N→h_K、a_N→a、b_N→b且三者有限時，a+b>h_K給指數抑制，
a+b<h_K給指數增長；a+b=h_K僅消掉leading項，不能決定R_N是否趨零。
若只問較弱R_N→0，在上述有限極限下a+b≥h_K是必要條件，通常不是充分條件。

邊界的純尺度示例：正數序列W=e^(hN²)、d=e^(bN²)及h>b時，
分別取χ=e^(−(h−b)N²)/N、χ=e^(−(h−b)N²)，其leading a相同，
但形式比值分別為1/N與1。這只說明leading資訊的邏輯不足；
沒有宣稱這些序列由任何history相位或費米子模型實現。
本節沒有從run1、fixture或phase樣本估計a、b，也不填其物理數值。

## 5. 一般物質因子與同重力baseline

回到契約一般有限複數F_N。若同一K_N上|F_N(C)|≤u_N，且另證
|Z_N^(1)(M_N)|≥d_N^->0，因重力因子模為1，三角不等式給

$$R_N\le u_NW_N(K_N)/d_N^-.\tag{T2.10}$$

右式趨零是充分條件，不是必要條件；複數相消可能使左式更小。
單history的結構敏感性、bounded modulus或log|det|本身都不提供所需分母下界。

在Z_N^(0)(M_N)、Z_N^(1)(M_N)、Z_N^(0)(K_N)非零時
（Z_N^(1)(K_N)允許為零），同重力基線的改善比有精確式

$$\frac{R_N}{R_N^{(0)}}=
 \frac{|Z_N^{(1)}(K_N)|\,|Z_N^{(0)}(M_N)|}
 {|Z_N^{(1)}(M_N)|\,|Z_N^{(0)}(K_N)|}.\tag{T2.11}$$

若另證|Z_K^(1)|≤η_N|Z_K^(0)|且|Z_M^(1)|≥c_N|Z_M^(0)|，c_N>0，
則改善比≤η_N/c_N；只控制KR分子不足。baseline的KR振幅為零時，此改善比未定，
不能把已存在的重力相消記成物質改善。這裡沒有選η_N、c_N的模型公式。

既有BdG限定no-go及零det邊界依契約保留；不擴為所有F_N的no-go。
Loomis–Carlip／Mathur–Singh–Surya的重力／link-action定位沿用契約§5及EXP-0059，
本輪沒有重證或將其算作費米子效果；更沒有因排除KR就聲稱全部非流形類已受抑制。

## 6. 本題交付與仍OPEN

| 定義義務 | 本稿的結果／缺口 |
| :--- | :--- |
| histories、共同measure與同構類寫法 | 已給精確(T2.1)，正計數leading換算(T2.3)；全部待獨立複核 |
| 權重／作用量型別 | 沿用定案占位型別；不選F_N、K或物質積分，良定性實現仍OPEN |
| 歸一化與比較總量 | 沿用共同1/N!與R_N；精確比值及分母義務已分清，不稱機率 |
| 熵與相消速率 | 給條件式(T2.6)–(T2.9)；下界只給充分資訊，必要條件需要上側控制 |
| KR／流形class與分母 | 具體predicate、引用class mapping及實際上下界仍OPEN，本稿沒有選幾何結論 |
| 物質的獨立貢獻 | (T2.11)要求同重力baseline與兩類控制；尚無物質機制實現 |

這是必要條件與定義審計，非一個新作用量方案或物理no-go；不稱原創性已盤點。
若下一步要提供具體物質因子或K，須依契約停止並另立先審問題，不在本稿直接構造。
無新數值／符號計算、RNG／撒點、producer、raw／sealed、seed／主機／量測／receipt。
既有regression／integrity只作repo驗證；E0、formal及全部OPEN／UNKNOWN限制不變。
