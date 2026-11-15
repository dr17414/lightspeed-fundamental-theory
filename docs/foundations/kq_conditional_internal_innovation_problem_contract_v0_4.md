# X-KQ-COND-TA-P0.4 — 原序軌道與非單一矩陣法則的契約修約草稿

狀態：**【契約草稿／待 exact-head 獨立複核；未取得契約 GO】**。
2026-11-15 Asia/Taipei。基線 main
`4a543e6768b5d488718762194ea34c46708fd29c`，tree
`d7666db71d8531325670369bf20c23fe22503272`。
Problem ID `X-KQ-COND-TA-P0.4`；新 model ID **NONE**。探索軌，
不具 Stage 5C §5.2.1(v) 正式依據資格。本稿是操作者選擇
「採納 (b′)，起草 P0.4」後的**待審文字**；選擇起草並非契約 GO。
在契約 GO、必要 CI 成功、原樣合併 main 並核對 tree 前，
仍以已定案的 [P0.3](kq_conditional_internal_innovation_problem_contract_v0_3.md)
為現行契約；本稿不可用來重判 #111 或啟動新資料、K 或研究。

## 1. 版本差異與不改的全域問題

本稿**全文繼承 P0.3 §§1–6**，唯獨把 P0.3 §5 末段援引的
P0.2 §7(b)「每個完整輸入的實際 active order blocks span ≥ 2」
**在本版本**替換為下述 §3 的 (b′)，並在 §4 增加先行資料的
非真空性證明。若 P0.3 任一句與此精確替換衝突，以本稿 §3–4
為 P0.4 的特則；其餘不作概括放寬。P0.1、P0.2、P0.3、
B-01、IB-01、Q-01 舊版和已合併的 #111 證明均**保留原文與
各自的 PASS／FAIL／未決作用域**，不追認為 P0.4 的結果。

| 義務或來源 | P0.4 處置 |
| :--- | :--- |
| 定義域 | 原 $D_{KQ}=\{P\in D_1:q(P)\ge2\}$ 全部 $P$、每個 $L\in LE(P)$、共同 $R_0=(E_0,h_0,\eta_0)$ 且 $\dim_{\mathbb C}E_0=2$；不刪 dual star、向下 star、鏈、diamond 或 $K_{2,2}$ |
| 資料 | P0.3 §3 的 $\beta,B_0,I,\mathcal C,U,Q_P,h_Q,j_C$ 型別、容量與自然性不變；§4 新增一項可失敗的事前審核族條件，不預選資料值 |
| 方程與來源 | P0.3 §4 的同一 $K_{int}:T_P\to J_P$、$R_C,F_C,S_C$、$G_R$；原 order 支撐、對角不讀 $L$、$K^{ord}$ 原序自然及 P0.1 §4.4 的唯一固定線性 $L$ 類不變 |
| 核心物理義務 | P0.3 §5 的全 test 正 CAR、嚴格守恆、**原 P 全 fiber 微因果**、Green typed 識別、同源 field／state、實際 rank 真增長全保留；P0.2 §7(a) **每個完整輸入非零同源 Green 傳播**全保留 |
| 非平凡性 | **只替換**舊 §7(b) 為本稿 §3 (b′)；P0.2 §7(c) 無統一 Hasse-hop 截斷及其他比較量詞原樣保留 |
| 來源與隔離 | P0.3 §6 全部禁止事後調資料、看譜選規則、刪失敗面、縮域、暗讀 $L$、formal／E0 回用等限制不變 |

仍要求一條事前固定、跨 $P,N$ 有限描述的法則對**所有**完整
conditional 輸入成功，對所有 structured 同構自然；單一族群
或某個有利 $L$ 的局部成功不構成全域完成。

## 2. 原始目的、已見證據與修約的代價

修約的原始目的逐字保留為：**「排除純量核 ⊗ 單一矩陣法則化約」**。
[1+1 構造契約 P0.1 §4.1(b)](kq_1p1_construction_problem_contract_v0_1.md)
排除每個輸入的所有非對角 blocks 都可由各自的 scalar event kernel
乘一個可隨該輸入選擇的 $2\times2$ 矩陣的整條 law。
[時間序契約 P0.1 §6(b)](kq_conditional_time_adjoint_problem_contract_v0_1.md)
事前把 (b) 定為**每個**完整 conditional 輸入的門檻；
[P0.2 §7(b)](kq_conditional_initial_data_problem_contract_v0_2.md)
指定只數 $K_{int}$ **實際施加**的原 order 非對角 blocks。
本稿不能倒寫舊契約本來只要求跨輸入兩種矩陣。

經 #113 獨立複核的[理由短稿](kq_span_two_on_symmetric_inputs_rationale_v0_1.md)
和 #114 獨立複核的[修約提案](kq_span_amendment_review_proposal_v0_1.md)
只支持有原則的審查與此後的操作者明示選擇，不是 (b′)
有解的證明。#99 在 Q-01／#111 之前已提示**若只讀區間型別**，
三葉 star 會有一維 span 風險，當時仍保留逐輸入 (b)，
並容許 $L$ 的非局域位置計數作探索補救；P0.1 §4.4 也明說
$L$ 是新增時間序自由度，並非已證物理機制。三葉 star 的
條件式提示不能偷換成後來 dual star 的事前 no-go。
現在降低單軌道輸入的本地 §7(b) 門檻，確屬**事後放寬驗收**；
若審查者不接受原 order 對稱等價作獨立的物理來源理由，應否決
這份草稿，保留 P0.3 舊條款，不因 #111 的 FAIL 而自行改判。

同時 (b′) 在多軌道輸入**增加** $K^{ord}$ 也須非比例的要求，
可能排除本來只靠具有真實物理意義的 $L$ 才有兩個矩陣方向的
未來模型；這是具名代價，並非 #111 推出的必要定理。

## 3. 取代 §7(b) 的精確條款 (b′)

在後續**另版、先 GO** 的資料登記 $\mathfrak D$ 下，令
$B_0(P)$、$I(P)=P\setminus B_0(P)$ 是不讀 $L$、對原序同構
自然的共同初值／內部方程集合。定義**實際施加**的 strict order
pair 集合與軌道：

$$\mathcal E_P=\{(y,x): y\prec_P x,\ x\in I(P)\},\qquad
\mathcal O_P=\mathcal E_P/\operatorname{Aut}(P).\tag{4.1}$$

$\operatorname{Aut}(P)$ 是**不帶 $L$** 的原 strict order 自同構，
它因 $I$ 的自然性而作用在 $\mathcal E_P$ 上。不得改用
$\operatorname{Aut}(P,L)$，也不得由 K、CAR、譜、選面成功或
葉片排名來「分裂」原序軌道。P0.3 §3 容許的 $\beta,U,h_Q,j_C$
都是同一條對原序同構自然、跨尺寸固定的資料 law；其輸出在
同構誘導的座標／通道作用下等變，**不能**替同一軌道的某個
事件或 pair 增加獨立標籤，故在此類資料中
$\operatorname{Aut}(P,\mathfrak D_{ord})=\operatorname{Aut}(P)$
作為 pair 軌道的記法。若要以外加方向、transport、per-event
frame 等非自然資料區分同軌道 pair，須另立新的資料來源／
問題契約，不能在 P0.4 事後選出；$L$ 本身雖是 conditional
primitive，也**不計入**本條的原序軌道分類。

以共同 $E_0$ 的固定 fiber 識別，$K^{ord}_P(e)$ 表示 P0.1
§4.1 的**不讀 $L$、對原序同構自然**的 order block；
$K_{int}(e;L)$ 表示在 $x\in I$ 方程 row **實際施加**的完整
strict order block，包含 P0.1 §4.4 准許的固定線性 $L$ 項。
兩者皆只取 $e\in\mathcal E_P$；未施加邊界 rows、diagonal、
不同面或不同輸入的 blocks 不計入。

**單軌道引理（在 P0.3 的自然性類下）。** 若
$|\mathcal O_P|=1$，則
$\dim_{\mathbb C}\operatorname{span}\{K^{ord}_P(e):e\in\mathcal E_P\}\le1$。
更一般地，同一軌道上各 $K^{ord}$ block 相同。
**證明。** 任取同軌道 $e,e'$，有 $f\in\operatorname{Aut}(P)$
使 $f(e)=e'$；P0.1 §4.1 的 $K^{ord}$ 原序自然性，取共同
fiber 變換 $V=id_{E_0}$，在固定 fiber 識別下得
$K^{ord}_P(e')=K^{ord}_P(e)$。$I$ 自然，兩個 row 均是
實際施加的方程 row；資料也不破壞該 $f$ 的等變性。∎
這是對 $K^{ord}$ 的引理，**不**聲稱含 $L$ 的完整 $K_{int}$
在固定 $L$ 下也逐 pair 相同；不能把 $K^{ord}$ 的結論
移植到 CAR、Green 或 state。

**P0.4 §7(b′) 可失敗義務。** 對每個 $P\in D_{KQ}$、每個
$L\in LE(P)$ 及共同 $R_0$ 的全部等價表述，在同一已登記資料
版本上按以下兩格判定：

1. 若 $|\mathcal O_P|\ge2$，必須存在**同一對**
   $e,e'\in\mathcal E_P$，使

   $$\dim_{\mathbb C}\operatorname{span}
     \{K^{ord}_P(e),K^{ord}_P(e')\}=2
   \quad\text{且}\quad
   \dim_{\mathbb C}\operatorname{span}
     \{K_{int}(e;L),K_{int}(e';L)\}=2.\tag{4.2}$$

   由引理，同一原序軌道上的 $K^{ord}$ blocks 相同，故
   成立的 witness **自動**分屬不同軌道；此非額外限制。
   每個 $L$ 各自檢查，witness 可隨 $L$ 改變，但不能跨 $L$
   合併、挑一個有利排序、讀 A／譜選 pair／law 或調整系數。
   $K^{ord}$ 的非比例性阻止僅憑 $L$ 排名取得 span 2；
   完整 block 的非比例性阻止 $L$ 項把它抵銷。
   任一多軌道輸入及任一 $L$ 沒有同一對 witness，即 (b′) FAIL。
2. 若 $|\mathcal O_P|=1$，在該輸入對 (b′) 記
   **N/A（不提供本地 sector 非化約判別力）**，絕不標 PASS。
   即使完整 K 因 $L$ 排名有兩個方向，也不能拿來填此格。
   該輸入仍屬全工作域，所有其他逐輸入義務照常可 FAIL；
   特別是 dual star 的原 P 葉對微因果與 §7(a) 非零傳播，
   以及 $K_{2,2}$ 的多根共享交叉項，都不得以 N/A 略過。

**整條 law 的非真空性。** 任一 P0.4 資料版本須在 K 輸出之前
按 §4 另證一個尺寸無界的多軌道 active 子族。全域規則在該
子族每個輸入的全部 $L$ 均要滿足 (4.2)，不能以某一個
容易的小 P 代替全域檢驗。若資料無法提供此子族，資料門檻
FAIL／未完成，不可用一律 N/A 宣稱 (b′) 成功。
若整條 K law 在每個完整輸入上可寫為
$K_{int}(e;L)=h_{P,L}(e)M_{P,L}$，即使每個輸入可有不同
$M_{P,L}$，任一多軌道輸入的實際 block span 仍至多 1，
故 (4.2) 必 FAIL。這**精確保留**排除純量核 ⊗ 單一矩陣
法則化約的原目的；跨輸入湊足兩種矩陣不算。共同 global
$GL(2,\mathbb C)$ 換基保持兩個 span 的維數，不允許逐事件
改 fiber 基底來偽造差異。兩個方向仍只是具名化約排除，
並非 spin、chirality 或物理表示已導出的證據。

## 4. 第二道純資料門檻新增的事前檢查

在 P0.3 §3 的全部原有資料義務**之外**，資料登記須只憑
原 order/count、既定自然的 $B_0,I$，在 K／Green／A／state
任何輸出之前固定一條有限、跨 $P,N$ 的 predicate $\Phi_{orb}(P)$，
定義 $\mathcal F_{orb}=\{P\in D_{KQ}:\Phi_{orb}(P)\}$；證明

$$\forall m\ge1\ \exists P\in\mathcal F_{orb}:\quad
|P|\ge m\quad\text{且}\quad |\mathcal O_P|\ge2.\tag{4.3}$$

須列出 $\mathcal E_P$ 的生成方法、軌道的自然性與至少兩個
事前 order 可區分的 active pair 類，並給跨 $m$ 的解析證明；
不能把 $\Phi_{orb}$ 定義為「某個 K 滿足 (4.2)」或回看成功
再改資料。$C_N$（$N\ge3$）在最小元面、內部方程設於其餘
事件的**既有 Q-01 v0.1 例子**中有 cover 與跨多個 Hasse hops
的不同 active 軌道，說明這項條件不因輸入域而空洞；
這不是預選 P0.4 的 $\beta$ 或資料 GO。若新資料在鏈上
不足兩軌道，須另找自然、無界的族並事前證明。

第三道 K／source／Green／CAR／state 規格在任何研究輸出前，
須固定同一 K 法則及 (4.2) 的判定方法，在完整的事前
審核目錄上對每個 $L$ 分別列 K^ord 和完整 active K 的
span、N/A／PASS／FAIL，並在 $\mathcal F_{orb}$ 上交無界
解析 witness 方案和證明；指定哪兩個 pair 的可計算選法或
同等的全稱檢驗，不得在看到 CAR／正性結果後只展示有利 pair。
資料門檻的 (4.3) **只是讓測試非真空**，不保證後續 K 能過 (4.2)。

固定目錄至少列 dual star、向下三葉 star、鏈 $C_3,C_4$
及無界鏈、diamond、$K_{2,2}$；以下的軌道數只是以
**舊 Q-01 的 $B_0=M(P)$ 作比較**，新版資料需重算 active set。

| 原 P | 舊 Q-01 比較用的 active 軌道 | P0.4 (b′) 在同型資料下的檢查 |
| :--- | :--- | :--- |
| dual star $a\prec v_j$，$r\ge3$ | 一條，所有根葉對等價 | (b′) N/A；每對葉子原 P 微因果及非零 Green 照查 |
| 向下三葉 star $a_1,a_2,a_3\prec b$ | 一條，葉根對由 $S_3$ 互換 | (b′) N/A；不能靠 $L$ 葉排名充作原序差異 |
| 鏈 $C_N$，$N\ge3$ | rigid；相鄰 cover 與多 hop 對分屬不同軌道 | (4.2) 逐輸入檢查，無界族候選；不得預判 K PASS |
| diamond $a\prec b,c\prec d$ | **三條**：$a\to\{b,c\}$、$\{b,c\}\to d$、$a\to d$ | 兩個 $L$ 各查同一對 order／完整 blocks 的獨立性，並另查 $b\parallel c$ |
| $K_{2,2}$，$a_1,a_2\prec c_1,c_2$ | 一條，四個根到頂點的對由 $S_2\times S_2$ 互換 | (b′) N/A；$c_1\parallel c_2$ 多根交叉項原 P 直接檢查 |

其他所有 $P,L$ 仍受全域量詞；此表不是只做五類的縮域。
單軌道 N/A 不是任何 $K,A,G_R$ 的局部成功證據。

## 5. 版本、來源隔離與停止條件

**三道門檻重新依序：** (1) 本契約 exact-head 獨立 GO、
必要 CI success、原樣合併 main 並核對 tree；(2) 另交
**純資料新版**，完整重登 $\beta,\mathcal C,U,Q_P,h_Q,j_C$，
加上 §4 的 (4.3)，取得資料 GO、合併、tree 核對；
(3) 另交 K／source／Green／CAR／state 規格 GO，才可研究。
舊 Q-01 v0.1 的資料 GO **只屬 P0.3**；若要沿用相同法則，
亦須以新版本事前重登、證明 P0.4 相容性並由 reviewer 另給 GO。
不以這份契約草稿或 #114 提案的 GO 跳過任何一關。

#108 P0.2＋B-01 的限定障礙、IB-01 全域 FAIL、
#111 在 **P0.3＋Q-01 v0.1＋舊 §7(b)** 下的命題一 FAIL，
以及邊界滿射條件命題與非滿射類未決，均照原作用域封存。
P0.4 的單軌道 N/A 不倒改 #111 的舊 FAIL，也**不**宣稱
新版本在 dual star 已滿足微因果、非零傳播、Green 識別或
field/state。任一新版義務 FAIL 就按新版如實記 FAIL，
不能看結果回填 $\Phi_{orb}$、縮 $D_{KQ}$、改 $L$ 類、
資料相關或 (b′) 的兩種 span 計法。

本修約是明示的 conditional 探索，未推出時空、物理
Spin／Dirac、正真空或 continuum；
[T3 §§3–6](t3_sector_capability_audit_v0_1.md) 的「需外加」
仍只在其已審來源作用域內成立，不是 P0.4 全類 no-go。
formal／E0、A／B、UNKNOWN、item7／8、6a-E、Freeze-1a
及 raw／sealed／producer／seed 隔離全部維持。契約 GO 前
不得登記新版資料或寫 K 規格，更不得做案例計算或研究。

**給 reviewer 的核對點：** (i) §3 的自然性引理是否只對
$K^{ord}$，且自然資料不能分裂 $\operatorname{Aut}(P)$ 軌道；
(ii) (4.2) 是否要求同一對 blocks、每個 $L$，並且
單軌道明列 N/A 而非 PASS；(iii) (4.3) 在資料門檻
可獨立 FAIL；(iv) diamond 的三條軌道與其他四類是否正確；
(v) §1 全部其他義務、三道門檻、舊失敗版和來源隔離是否保留。
本稿沒有選資料、K 係數或構造／證明輸出；P0.4 是否可行仍 OPEN。
