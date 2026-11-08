# X-KQ-COND-TA-P0.3 — 內部自由度與同源量子過程問題契約草稿

狀態：**【修約提案／draft／待 exact-head 獨立複核；未取得契約 GO】**。2026-11-06 Asia/Taipei。
Problem ID `X-KQ-COND-TA-P0.3`；新 model ID **NONE**。探索軌，不具 §5.2.1(v) 依據資格。
本稿只選擇「內部事件可帶入量子自由度」這一個修約方向，固定問題的型別、來源限制及可失敗義務；
不登記新的資料規則、不指定 K／Green／CAR／state 實現，不宣稱這個問題有解。
P0.1、[P0.2](kq_conditional_initial_data_problem_contract_v0_2.md)、
[B-01](kq_conditional_boundary_beta_registration_v0_1.md)與已封存 IB-01 全文保留，
不得把舊版 FAIL 改稱新版 PASS。

## 1. 修約的理由：現行 P0.2 的任何 β 都不能只靠換初值面避障

令 $P_r=\{a,v_1,\ldots,v_r\}$，$r\ge3$，只有 $a\prec v_j$，各葉兩兩不可比。
[已獨立複核的限定紙上稿](kq_dual_star_initial_data_obstruction_study_v0_1.md) §2
證 $P_r\in D_{KQ}$，並在 B-01 的 $B_0=\{a\}$ 下，由 P0.2 的初值同構、P0.1 §4.4 的
仿射 $L$ 計數、正 Gram 微因果與 P0.2 §7(a) 推出全域完成不可能。
下面是**比該稿作用域更廣、由本修約稿新列出的短引理**；尚待獨立複核，
不能倒填為 #108 原證明的已審結論。

**β 剛性引理。** 對任何滿足 P0.2 §3.1、§3.4 的 β，$B_0(P_r)=\{a\}$。

**證明。** β 不讀 $L$ 且對所有原 order 同構自然，故對每個
$f\in\operatorname{Aut}(P_r)\cong S_r$，$f(B_0(P_r))=B_0(P_r)$。
葉子是 $S_r$ 的一個傳遞軌道，因此不變的 $B_0$ 要麼不含葉子，要麼含全部葉子。
$B_0$ 非空；若只含 $a$ 已得所求，若含任一葉子，past-set 性質迫使含 $a$，
加上不變性便等於整個 $P_r$，違反「非全 $P$」。故只有 $\{a\}$。∎

P0.2 另固定每個初值空間 $D_{B_0}=\mathbb C^{B_0}\otimes E_0$、
$\dim_{\mathbb C}E_0=2$，及每個解只由 $\gamma_{B_0}$ 唯一參數化。
因此在這個輸入上任何合法 β 都只有兩維的**全部齊次解**資料；更換合法 trace 集合也不增加
$\dim Sol_K$。將上引理接到 #108 的後續代數（不動其證明稿）可見：只替換 P0.2 所容許的 β
並不能解除 dual star 障礙。此推論仍限於 P0.2 其餘前提的聯合，不是整條因果序先行路線的 no-go。

本修約選擇改變「量子自由度都必須是起點齊次解資料」這個型別，保留原 order 的微因果、
逐輸入非零傳播及完整輸入域。以下型別沒有給出通過它們的具體構造。

## 2. 版本差異、全域量詞與三道門檻

沿用 P0.1 的 $D_1$、$q(P)$、$D_{KQ}=\{P\in D_1:q(P)\ge2\}$、全部 $L\in LE(P)$，
共同固定 $R_0=(E_0,h_0,\eta_0)$ 且 $\dim_{\mathbb C}E_0=2$。
**dual star、向下 star、鏈及其餘非流形輸入一律保留；不能為通過而刪 P 或挑 L。**

| 項目 | P0.2 的基線 | 本提案的改題與保留義務 |
| :--- | :--- | :--- |
| 動力學 | $K_{int}:T_P\to J_P$，齊次解由 $D_{B_0}$ 全部參數化 | 保留原內部方程／source 型別作比較基線；允許**具名的內部量子通道**，不可再把齊次解維數當全部 CAR 自由度 |
| 量子資料 | 正初值配對 $h_C$、$S_C=E_C^\dagger$、$A_C$ 為齊次初值 Gram | 資料登記另固定事件通道空間、正配對與注入／接合型別；A 必須由同源動力學及這些事前資料取得 |
| 不可退讓 | 原 P 微因果、P0.2 §7(a) 每個輸入至少一個非對角同源 $G_R$ 傳播 | **逐字保留原 P 與逐輸入量詞**；不能以增加獨立 contact 冒充傳播或以 $L$ 改寫不可比性 |
| 其他比較 | 嚴格守恆、Green 識別、state、§7(b)(c)及跨尺寸增長 | 仍是可失敗義務；若因型別改變須調整公式，須明列其新式與舊義務對照，不以「改題」默默刪除 |

**三道門檻按順序：**（1）本問題契約 exact-head GO、必要 CI、合併及 tree 核對；
（2）再交**純資料**登記，固定 §3 所述來源／容量／自然性，先 GO、合併及 tree 核對；
（3）再交 K／source／Green／CAR／state 的獨立可失敗規格，先 GO 後研究。
契約草稿未 GO 前不登記資料、不固定 K 規格、不做案例試算或研究輸出。
失敗版照實保存；新版本不得回填為舊版成功。操作者對草稿的撰寫授權不是科學門檻的 GO。

## 3. 待登記的新增資料型別與容量，不預選資料規則

在完整 event test 空間 $T_P=\mathbb C^P\otimes E_0$ 上，後續純資料登記須一次固定
$\mathfrak D(P)$ 的有限跨 $P,N$ 規則：

1. $\beta$ 的 order/count 邊界集合及合法 trace 家族，保留 P0.2 §3.1–3.4：
   不讀 $L$、對原 order 同構自然，$B_0$ 是非空、非全 $P$ 的 past-set，
   $q_I\ge2$，合法面同基數、含 $B_0$ 且只按事前 predicate 選定。
   若沿用 B-01 的集合，須明說並重登與新增通道的相容性。
   $I=P\setminus B_0$、所有合法 $C$ 及 $D_C=\mathbb C^C\otimes E_0$ 的角色須分開。
   不得用輸出的成功／譜挑選集合。
2. 由 $I$ 中的事件索引的內部通道集合 $U(P)\subseteq I$ 及**對全部合法面共同**的
   量子資料空間 $Q_P=D_{B_0}\oplus (\mathbb C^{U(P)}\otimes E_0)$。
   $U$ 的選取只讀原 order/count，
   不讀 $L$、K、Green、CAR 或 state；跨尺寸使用同一條有限 law，對原 order 同構自然。
   每個新增通道的 fiber 仍是共同**固定的二維 $E_0$**；沒有隨 P 變大的單點 fiber。
   $U=\varnothing$ 在 dual star 上會回到 #108 的容量問題，不得宣稱已逃出該障礙。
3. 同一 $Q_P$ 上的正定 Hermitian 配對 $h_Q$，及把各通道接到 §4 的邊界／內部 source
   型別的線性資料接合 $j_C:Q_P\to D_C\oplus J_P$。
   後續資料登記須給明確的 order/count 來源、跨面關係、參數／bits 容量上界、
   正定性及所有 structured isomorphism 交換圖；這些**不得**由事後的 K、A、譜、
   微因果是否成功或 particular $L$ 回填。容許不同通道的事前相關或混合時，
   必須逐項申報為新增 primitive，不能藏在「正配對」四字中。

本節定的是**資料規則可交的型別及審查要求**，未選 $U$、$h_Q$ 或 $j_C$ 的值／law。
後續要交 $\dim Q_P=2(|B_0|+|U|)\le2|P|$、在 dual star 等高分叉輸入上
內部通道是否足以解除兩維上界、以及沿無界輸入族的實際增長證明。
容量隨事件數增長是明示外加量子資料，不稱從純因果序湧現；不能使用逐 $P$ 任意正矩陣表、
任意 per-event frame、事後成功 selector，或把完整事件 $\delta$-CAR 當作資料直接指定。

**提早檢查的陷阱。** 單把獨立、兩兩正交的來源模式接在葉子上，再原樣保留起點的
正 Gram，並不自動消除它們共有起點產生的葉對交叉 block。資料登記必須在不看 K 輸出
的前提下，明示它提供何種可檢驗的接合／相關能力；後續規格及研究仍要在**原 P 全 fiber**
對 dual star 逐對檢查。若只能藉 K 之後調資料或讓 K 在 CAR 中失去作用，判未完成。

## 4. 同一方程、source、量子通道與 Green 的型別

後續獨立 K 規格須在任何輸出前固定同一
$K_{int}:T_P\to J_P$，$J_P=\mathbb C^I\otimes E_0$，
及 canonical $B_0$ 的 $\gamma_B$／source 良定性與原 P retarded
$R_B=(\gamma_B,K_{int})^{-1}:D_B\oplus J_P\to T_P$，交左右 composition identities。
非 order 非對角 K block 為零，diagonal 不讀 $L$；K 的全部 $L$ 依賴仍受 P0.1
§4.4 的固定線性 count 類約束，不能借新量子通道暗讀 ranking。
可比對上的 $K^{ord}$ 仍須對原 P 同構自然，與 P0.1 §4.1 的 structured 自然性分帳。
保留齊次空間 $Sol_K=\ker K_{int}$、$\gamma_C|_{Sol_K}$ 的舊型別作具名對照；
**但 $Sol_K$ 不再被宣稱等於全部量子模式**。

對每個合法 $C$，須先證 $R_C=(\gamma_C,K_{int})^{-1}$ 有型別並與同一方程相容，
再由事前已登記的 $j_C$ 定義候選量子 response
$F_C=R_C\circ j_C:Q_P\to T_P$，及 $S_C=F_C^\dagger$；
必須交出 $R_C$、$F_C$ 的左右 composition／source identities 和與 $R_B$ 的同源關係。
這裡 $j_C$ 只是待登記的資料接合**型別**，不是已選的映射；
若後續資料規則選別的具名過程組合實現，須在資料 GO 前另修本型別，不能在 K 輸出後換式。
每個新通道是進入動力學的量子 innovation／source，而非 $K_{int}\psi=0$ 的另一個
齊次初值；聲稱它是物理場時，規格須同時給出場代數上的帶源方程、source 算符與
state 的相容型別。不能把任意外加 classical source 重新命名為 free vacuum 模式。

$G_R$ 仍是同一 $R_B$ 經固定索引識別得到的完整 response，且沿原 P retarded；
P0.2 §7(a) 的**每個完整輸入**至少一個 $x\ne y$、$y\prec x$ 的非零
同源傳播 block 原樣保留。額外 $Q$ 維數、對角 contact 或 $j_C$ 的裸矩陣不算此 block。
若要具名 $G_A$／dual、contact、boundary 或 source/test pairing，須先在 K 規格中固定，
不以事後 $A$ 定義它們。

## 5. 可失敗的正 CAR、守恆、微因果與 Green 識別

以完整 $T_P$ 的共同 $h_P$ 和**全部合法面同用**的已登記 $h_Q$ 定義 $F_C$ 的數學 adjoint，
後續若採此型別，總 form 為

$$A_C(f,g)=h_Q(S_C f,S_C g),\qquad f,g\in T_P.$$

半正定性在正 $h_Q$ 下**按構造成立**，不是成功證據；$F_C$／$S_C$ 必須
真的由同一 $K_{int}$、$R_C$ 與已凍結資料接合取得，不能由目標 $A$ 反因子分解。
以實際 rank 而非寫出的模式數報 $\operatorname{rank}A_C$、$\operatorname{rank}F_C$、
每個通道是否真的進入 CAR 與 Green，防止用 spectator 模式補容量。

1. **守恆。** 對同一 P、L、K、資料及全部合法 $C,C'$，在共同完整 $T_P$ 上逐元素
   嚴格要求 $A_C=A_{C'}$；交共同 $Q_P$ 下的面轉換、composition 及正配對保存證據。
   單一面不提供守恆判別力；資料登記仍需給出無界且至少兩面的事前族群。
2. **微因果。** 對原 P 的每一對不可比 $x\parallel y$ 和完整 $E_0$ fiber，
   在每個合法面逐對直接要求 $A_C(x,y)=0$；不因 $L$ 排序而改可比性，不略過未由共同面覆蓋者。
   這是嚴格、可失敗的總 CAR 義務，不能只查某個 state 或單一分量。
3. **Green 識別。** 在 K 規格中事前給具體 typed 式，將相同 $G_R$、具名 dual／contact
   與 $F_C$ 所得 $A_C$ 在原 P 可比 full-fiber test 上聯繫；不得用 $A=SS^\dagger$
   或「存在某 Green」當作獨立識別。要區分初值傳播、零初值 source response、innovation
   及其可觀察 CAR；至少兩個事前合法 kinetic 比較對象須給不同可比 $A$，且有非零可比
   off-diagonal CAR block，不能只讓 K 的不可見 source sector 改變。
4. **field／state。** 必須另給同源 charged 或 self-dual 的 *／CAR 型別、帶源方程、
   state／兩點與高點規則、正性與歸一化；不以抽象 Fock 存在冒充物理真空，
   不把數學 adjoint、field *、$\eta_0$ adjoint 混用。

任一項失敗都判該版未完成；不可刪失敗面、事後換配對或以正性／dim 增長抵銷。
保留 P0.2 §7(b) 實際 active order blocks span 至少 2、§7(c) 無統一 Hasse-hop 截斷的
非平凡性要求，及同一規則跨尺寸的真實 $\operatorname{rank}A$ 增長。
資料登記須預列 dual star、向下 star、鏈及至少一個多合法面的固定審核目錄與
容量／覆蓋數；K 規格 GO 後研究須完整列出 PASS、FAIL、undefined，才可寫結論。

## 6. 來源隔離、反補洞與下一份交付

新自由度是明示的**conditional 量子輸入**，不推出時空、相對論性、Dirac 連續極限、
physical vacuum 或比既有 canonical／open-system 範式更少 primitive。
帶源方程改變了 P0.2 的「全部 CAR 自由度由齊次初值解提供」的物理解讀；
若無法把 innovation 的 source 算符、守恆與相容 state 給出，不得降格為形式正 Gram 的成功。
本稿沒有閱讀新文獻原文；對 Sorkin–Johnston 的方向比附僅是已見討論線索，
不以它當作本契約的正性／可行性定理。

資料不得讀 K／A 結果、成功與否、raw／sealed、producer、seed 或 formal 的 UNKNOWN；
後續 K／Green／CAR/state 只能沿已登記資料的具名型別進入，不能再解碼 $L$ 排名、
補每事件獨立 frame、用 $A$ 的譜／正部分事後重配對或逐 P 表調參。
若需變更來源、$j_C$ 型別、比較量詞、微因果、§7(a) 或縮 $D_{KQ}$，停止並再修約；
不能把測試失敗當成事後例外。探索軌不具 §5.2.1(v) 資格，formal／E0、A／B、UNKNOWN、
item7／8、6a-E及 Freeze-1a 的既有隔離與狀態不變。

**給 reviewer 的核對點：** §1 的 β 剛性引理是否對所有 P0.2 合法 β 成立；
§3 是否讓內部自由度真的可隨事件增長而未暗給全事件 $\delta$-CAR；
§4 的 source 與量子 innovation 是否型別分明且保有同源 Green；
§5 的守恆、原 P 微因果、§7(a) 與 Green 識別是否仍能獨立 FAIL；
三道門檻是否禁止在契約 GO 前登記資料／固定 K；所有負面結果是否保持原作用域。
本契約未替資料登記或 K 規格選出可成功的規則，**P0.3 仍是 OPEN 問題草稿**。
