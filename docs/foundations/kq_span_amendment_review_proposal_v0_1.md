# §7(b) 的修約審查提案：按可比對軌道檢驗矩陣非平凡性

狀態：**純紙上修約提案／待 exact-head 獨立複核；不是契約 GO**。
2026-11-13 Asia/Taipei。基線 main `93b75dc598e3ca83a66205fd18599fac317c7b1e`，
tree `8d8e6b3abac044bd970520ff8e1e85f7dcb376b7`。
Problem ID 尚未分配；新 model ID **NONE**。本稿不修改 P0.1／P0.2／P0.3、
Q-01、K、Green、CAR、state 或正式驗收；不把討論稿的 GO 當作修約 GO。

## 1. 要審的原則與既有代價

[1+1 構造契約 P0.1 §4.1(b)](kq_1p1_construction_problem_contract_v0_1.md)
原本要**「排除純量核 ⊗ 單一矩陣法則化約」**：若對每個完整輸入，
全部實際 order 非對角 block 都是各自的 scalar event kernel 乘同一
$2\times2$ 矩陣，即使矩陣可隨輸入／尺寸改變，也不合格。
[時間序契約 P0.1 §6(b)](kq_conditional_time_adjoint_problem_contract_v0_1.md)
已明定**每個**完整 conditional 輸入要有 span ≥ 2；
[P0.2 §7(b)](kq_conditional_initial_data_problem_contract_v0_2.md)
將對象細化為 $K_{int}$ 原 order 非對角、**實際施加**的方程 blocks，
[P0.3 §5](kq_conditional_internal_innovation_problem_contract_v0_3.md)
明文保留。不得用未施加的邊界 rows、diagonal 或不同輸入各自的矩陣
拼出某一輸入的 span。這個現行逐輸入條款仍生效。

已合併的 [#113 理由短稿](kq_span_two_on_symmetric_inputs_rationale_v0_1.md)
給了獨立於 Q-01／#111 失敗的**啟動審查**理由，並沒有證明應修約。
歷史反方必須正面保留：#99 在已知「只依賴區間型別」時三葉 star
可能退成一維的風險下，仍刻意保留逐輸入要求，另容許 $L$ 的固定線性
位置計數。P0.1 §4.4 又承認 $L$ 是新增非局域時間序自由度，
不是從 $P$ 導出的局域時間或已證的物理機制。這個提示有其限定，
三葉 star 也不是 #111 的 dual star；不能倒稱 #99 已證後來的障礙。
現在重新審查量詞確實有**補救手段未成功後改驗收**的風險。

提案理由是較早即存在的來源與等價性問題：只憑 $L$ 給同一原 order
可比對軌道的成員不同矩陣，不說明為何這些在原 order 下等價的
事件對有不同物理耦合。這個質疑足以審核一條具名**探索驗收**規則，
不等於證明矩陣多樣性在每個可區分輸入都是物理定律。

## 2. 待審的替代判準（精確量詞；不是現行規則）

對完整輸入 $(P,L,R_0,\mathfrak D)$，資料版本 $\mathfrak D$ 先於 K
固定自然的內部方程集合 $I(P)$。令

$$\mathcal E_P=\{(y,x):y\prec_P x,\ x\in I(P)\},\qquad
  \mathcal O_P=\mathcal E_P/\operatorname{Aut}(P,\mathfrak D_{\rm ord}).$$

此處 $\mathfrak D_{\rm ord}$ 只指**不讀 $L$**、在 K 前登記的
order/count 資料；自同構須保持這些資料的法則與內部方程集合。
每個 event fiber 仍以共同 $E_0$ 識別，只許全域共同換基。
在 $\mathcal E_P$ 上，以 $K^{ord}_P(x,y)$ 表示 P0.1 §4.1 的
原 order 部分，以 $K_{int}(x,y;L)$ 表示實際施加的**完整** block。
非 order block 仍為零，$L$ 仍只可依 P0.1 §4.4 的固定線性類進入；
本提案沒有增設 K 的自由係數或 per-event frame。

**候選 §7(b′)：** 對每個 $P\in D_{KQ}$、每個 $L\in LE(P)$、
共同 $R_0$ 的全部等價表述，以及已 GO 資料的所有合法面，
若 $|\mathcal O_P|\ge2$，須有兩個分屬**不同原 order 軌道**的
$e,e'\in\mathcal E_P$，使

$$\dim_{\mathbb C}\operatorname{span}
   \{K^{ord}_P(e),K^{ord}_P(e')\}=2
\quad\text{且}\quad
\dim_{\mathbb C}\operatorname{span}
   \{K_{int}(e;L),K_{int}(e';L)\}=2.\tag{b′}$$

對每個 $L$ 均須分別給出 witness；不能只挑一個有利 $L$，
也不能把兩個不同 $L$ 的 blocks 相加。兩個 witness 可隨 $L$ 改變，
但它們必須來自同一事前固定、跨 $P$ 的 K 法則；不得依 A、譜、
Green 識別是否通過來選子域或換係數。$K^{ord}$ 的獨立性使
**僅靠 $L$ 排名**造出的兩個方向不能充作非化約證據；完整 block
的第二次檢驗則防止合法 $L$ 項把差異抵銷。若 $L$ 將來取得
另一種已審物理來源，須另修此來源條款，不能默認本稿已證。

若 $|\mathcal O_P|=1$，此輸入對 (b′) 記**不適用／不提供
sector 非化約判別力**，絕不記為局部 PASS；其傳播、正 CAR、
守恆、原 P 微因果、Green 識別、state、非局域及增長義務仍按原量詞
逐項可失敗地檢查。不得從域中刪除此輸入，或把 $L$ 排列造成的
分裂當作新的原 order 軌道。

**全法則不能真空過關：** $D_{KQ}$ 中有 $C_N$（$N\ge3$），
且其最小元資料規則下有不同的 active 軌道。任何聲稱全域完成的
資料版本，須在登記時事前證明，存在一個僅依 order/count 選定、
尺寸無界的子族 $\mathcal F\subset D_{KQ}$，其每個成員
$|\mathcal O_P|\ge2$，並在 K 規格**輸出前**固定該子族的有限
predicate 與解析 witness 方案。全法則須在每個 $P\in\mathcal F$
及其全部 $L$ 滿足 (b′)；不能只在一個幸運的小例子通過。
例如 $C_N$ 的 cover 與跨兩個以上 Hasse hops 的對是**可作來源
檢驗的先行輸入類型**，不是本稿指定的 K witness 或成功值。
若某資料版本使鏈不再有兩個 active 軌道，必須另證其無界子族
存在；不得把這一前提當作自動成立。

這兩條是可獨立 FAIL 的：任一多軌道輸入在任一 $L$ 無此兩個
非比例 order 與實際 blocks，或找不到事前固定的無界審核族，
就判 (b′) FAIL／資料前提未完成。若整條法則處處可分解為
$K_{int}(x,y;L)=h_{P,L}(x,y)M_{P,L}$（$M_{P,L}$ 甚至可逐輸入選），
它在任何多軌道審核輸入的實際 block span 至多 1，必 FAIL。
共同 $GL(2,\mathbb C)$ 換基保留兩個 span 的維數；逐事件基底變換
仍不允許。這**保留原排除目的**，也比只要求「跨輸入一共出現兩個
矩陣」更嚴格。跨面若 K 不變，不能拿不同面重算同一 witness。

本方案同時增加 $K^{ord}$ 非化約的要求，可能排除一種僅由有物理
意義的 $L$ 提供 sector 差異的未來模型；這是**明示代價**，
並非從 #111 推出的定理。逐輸入放寬只及單軌道情形；在多軌道
輸入上仍要求兩個方向，未保證有任何 K 能同時滿足其餘義務。

## 3. 事前目錄：在哪裡實際檢查

下表的 active 軌道數以 Q-01 v0.1 的 $B=M(P)$、$I=P\setminus B$
**僅作既有資料的比較範例**；修約若獲 GO，Q-01 仍須作為新版本
重走資料門檻，軌道數要在該版本重新核對。表內的「應檢查」
是候選 (b′) 的**適用性**，不是任何 K 的 PASS／FAIL 或構造輸出。

| 原 P | active 可比對軌道的事前區分 | 候選 (b′) 的處置 |
| :--- | :--- | :--- |
| dual star $a\prec v_1,\ldots,v_r$，$r\ge3$ | 根葉對被 $S_r$ 傳遞，只有一軌道 | 本地不適用；所有葉對原 P 微因果、逐輸入非零 Green 等仍要檢查；不以此宣告 #111 的舊 FAIL 消失 |
| 向下三葉 star $a_1,a_2,a_3\prec b$ | 葉根對被 $S_3$ 傳遞，只有一軌道 | 本地不適用；不能以 $L$ 葉排名差單獨報 sector 成功 |
| 鏈 $C_N$，$N\ge3$ | order rigid；cover 與跨多個 Hasse hops 的對分屬不同軌道 | 每個 $L$（鏈只有一個）檢查兩種 blocks；可作事前無界審核族，仍須在新版資料門檻證 active 覆蓋 |
| diamond $a\prec b,c\prec d$ | cover 對與 $a\prec d$ 跨 hop 對不同軌道；中間互換不改其區分 | 兩個 $L$ 都檢查，且成對的 $K^{ord}$ 與完整 blocks 都須獨立；$b\parallel c$ 微因果另查 |
| $K_{2,2}$，$a_1,a_2\prec c_1,c_2$ | 四個根葉對被 $S_2\times S_2$ 傳遞，只有一軌道 | 本地不適用；$c_1\parallel c_2$ 的多根交叉項仍要在原 P 查，不得用「不適用」遮蔽 |

即使單軌道輸入出現兩個數值獨立的 $L$ blocks，也不作本準則的
非化約 witness。反過來，鏈／diamond 有兩個可區分軌道不代表
自然定律**必然**給兩個 matrices；它們正是會讓候選判準失敗的輸入。
此審核目錄不刪原工作域的其他 P／L，也不代替全域證明。

## 4. 反方、T3 與能否改約的判斷

**維持原 §7(b) 的最強理由：** #99 早就知道三葉 star 在特定
區間來源類會落成 span 1，仍選 L 保留逐輸入要求。若此刻為了
Q-01／#111 改用單軌道豁免，會讓原本最簡單、最能暴露 sector
退化的形狀失去本地非化約驗收；多軌道檢查也可被人為限制在
特定 family，而其餘全域輸入局部退化。物理上還可能有事前
登記的方向／transport，使原 order 單軌道分裂成真的物理類型。
以上不是程序瑕疵，足以讓 reviewer **否決**本提案。

**提案的回應及成本：** 不以 #111 的失敗作理由，改用原 order
對稱等價與矩陣來源原則；在可區分的 active pair 類上仍逐輸入、
逐 L 要求實際和 order-only 各兩方向，並增加無界族證明，
所以不把標準降為只看一次偶然成功。但單軌道局部退化的確被
放行；此點必須明記為**放寬驗收**，不是把 #99 當作早已同意
的修正。若 reviewer 認為即使無可辨來源，每個形狀也必須有
兩矩陣，或認為 order 軌道不是恰當物理分類，應維持原文並停止
本修約，而不是用「等價」一詞掩蓋分歧。

[T3 §§3–6](t3_sector_capability_audit_v0_1.md) 的「需外加」
只說目前 two-set fiber 與置換不給出 Weyl／Spin 表示及 intertwining；
並不證 (b′) 有解。通過兩矩陣檢查也僅排除具名 tensor 化約，
**不等於**已得到 spin、chirality、相對論傳播或物理 state；
這些來源及同源量子鏈仍須各自交證。

**本稿建議：把 (b′) 作為可供 exact-head 審查的修約候選，
不在本稿判為已採納。**審查者應特別決定：(i) 單軌道局部豁免
是否值得以無界、多軌道嚴格檢查交換；(ii) order-only 獨立性
是否不當排除了有物理意義的 $L$；(iii) 新版資料能否事前保證
無界 active 多軌道族。任一項無法獨立辯護，應維持原 §7(b)，
依 #113 的分歧回到兩條路線的比較，而非直接拿失敗重寫標準。

若將來修約提案取得獨立**契約 GO** 並合併，仍須把 Q-01 當
**新版本**重新走資料登記 GO、合併與 tree 核對；之後才可交
K／source／Green／CAR／state 的第三道獨立規格並待 GO，然後
才研究。#108 的 P0.2＋B-01 限定障礙、IB-01 FAIL，以及 #111
在原 P0.3＋Q-01＋**舊 §7(b)** 下的 FAIL 均原樣保留，
不得追認為新版 PASS。現行微因果、§7(a) 非零傳播、全部 $D_{KQ}$
與 $L$、正 CAR、守恆、Green 識別、state 和來源隔離均不放寬。

本稿只讀 repo 既有文件和已見 Claude 提示；不檢索新文獻、
不計算任何具體 K／Green／A，沒有數值或符號科學程式、RNG、
撒點、producer、raw／sealed、seed、formal／E0 回用。
