# 量子過程先行：局部進出方向的有界文獻盤點

狀態：探索軌有界盤點；§1–3 在前一獨立 commit 固定，§4–6 在其後填入，待 exact-head 複核。
基線：#123 rebase main `e39da6c395b769493ee5c3deb00401aeeff7d7de`，
tree `87c7d880b74ecc960033064b7939e14b04213357`。
這不是新路線的契約、資料、規格或科學模型 GO。

## 1. 事前固定的問題及詞義

**唯一主問題：** 已有量子過程理論是否在局部操作／區域的接合處，
不預設「輸入端／輸出端」的時間方向？如果有，起始 primitive、
為此付出的限制或新條件是什麼；近似 3+1 維的局部幾何與
紀錄／熱力學時間箭頭是作為輸入、限定輸出、未處理，還是不能判定？
逐項對照 [#122 比較框架 §1](kq_two_routes_comparison_framework_2026_11_19.md)
的八條共同標準。時間反演對稱、不預設**全局**因果先後、
局部連線不帶**時間**方向、以及由無方向底層**導出**局部進出端，
是四個不同命題，不可互相冒充。

事前分類：A 已在每個操作／端口預設局部輸入與輸出；B 接合／
邊界不預設時間方向，但仍預設系統、區域、端口或操作，或需要
額外邊界／postselection／normalization；C 明確提出由無方向底層
導出局部方向的條件和證明；D 來源所讀範圍不能判定。分類是
**作者推論**，不是來源作者自稱，遇到語意不確定標 D，不湊 C。
各來源另逐格標「原文明載／作者推論／未查到（限本輪）」並記
原文頁、章節或式號；不把摘要、搜尋片段、後續構想算成已核全文。

## 2. 固定文獻清單與閱讀邊界

下列選讀在任何指定章節核讀之前固定。選題前曾檢索題名、
arXiv 識別碼和摘要，搜尋結果亦回傳少量出版社正文片段；
此曝露見接觸帳 EXP-0217，不宣稱事前盲性。只讀以下八份原始
研究來源的定義、組合規則、因果／方向宣稱與結論／限制；
不追讀其引用文獻作為第九份證據。連結是固定入口，實際讀到的
版本及位置待實讀後逐一補記；如原文不能取得，記「未讀到」。

| ID | 原始來源與固定入口 | 固定抽查重點 |
| :--- | :--- | :--- |
| S1 | Abramsky、Coecke，*A categorical semantics of quantum protocols*，[quant-ph/0402130](https://arxiv.org/abs/quant-ph/0402130) | 範疇中的物件、morphism 箭頭、tensor／串接，局部方向從何處進入。 |
| S2 | Coecke、Kissinger，*Categorical Quantum Mechanics I: Causal Quantum Processes*，[1510.05468](https://arxiv.org/abs/1510.05468) | process theory 定義、系統與組合、causality／no-signalling 的前提。 |
| S3 | Chiribella、D’Ariano、Perinotti，*Informational derivation of Quantum Theory*，[1011.6451](https://arxiv.org/abs/1011.6451) | 操作機率理論的輸入／輸出、causality 公設及推導的實際作用域。 |
| S4 | Hardy，*Towards Quantum Gravity: A Framework for Probabilistic Theories with Non-Fixed Causal Structure*，[gr-qc/0608043](https://arxiv.org/abs/gr-qc/0608043) | causaloid 的局部區域、操作資料與組合，非固定因果的意義。 |
| S5 | Oreshkov、Costa、Brukner，*Quantum correlations with no causal order*，[1105.4464](https://arxiv.org/abs/1105.4464) | process matrix 的局部實驗／端口前提與全局先後未定的區分。 |
| S6 | Oreshkov、Cerf，*Operational quantum theory without predefined time*，[1406.3829](https://arxiv.org/abs/1406.3829) | time-neutral 連線／boundary、局部操作定義、postselection 與時間方向來源。 |
| S7 | *Generalised Process Theories*，[2502.10368](https://arxiv.org/abs/2502.10368) | operad／time-neutral 的組合型別、預設端口與物理實現範圍。 |
| S8 | Hardy，*Operational General Relativity: Possibilistic, Probabilistic, and Quantum*，[1608.06940](https://arxiv.org/abs/1608.06940) | op-space、agency／time direction 輸入或有效性、3+1 幾何的狀態。 |

## 3. 固定抽取表與不能推出的結論

逐來源同填：① 系統／操作／區域／端口及組合是否 primitive；
② 局部方向、全局因果、時間反演各自的前提與結論；
③ 額外的邊界、postselection、normalization、metric 或維度條件；
④ 近似 3+1 局部幾何、紀錄／時間箭頭的具體處理；
⑤ 有無事前固定的可失敗義務、輸入域與 FAIL 處置；
⑥ 依 #122 §1 八條標準可核的證據等級、不能推出的結論。
若原文沒有處理某項，寫「本輪所讀範圍未查到」，不能寫
「該理論不可能處理」。答案是否為 C 須有具體定義／推導位置；
僅有 B 也不能宣告新路線已經導出因果序或時空。

此清單不是全面系統性綜述；沒有找到 C 不能推出所有過程理論
都預設局部方向。即使找到 B／C，也不能推出 3+1 幾何、時間箭頭、
正性或模型可行，更不能借此修改 #122 的事前標準或把因果序路線
的限定 FAIL 擴大成路線 no-go。最後只列來源事實、作者分類、
本輪空白與下一步可審問題，不排名、不中途增刪來源、不選構造。
formal／E0、A／B、UNKNOWN、raw／sealed／producer／seed 隔離維持。

## 4. 原文核讀範圍與逐項分類

下表只核所列章節／式與搜尋回傳的相鄰正文，沒有逐頁重證八篇。
版本取 arXiv 閱讀頁當時所示；S4 PDF 頁內另印 2024 日期，
不據此改稱 2024 arXiv 修訂。分類 A／B／D 依 §1，屬作者推論；
「本輪未查到」不等於原文全文沒有。以下以自己的話轉述，
「原文明載」僅指所標位置寫有該前提或結論。

| ID／版本及核讀位置 | 原文明載的 primitive、局部方向及成本 | 本稿分類；3+1、箭頭及不能推出 |
| :--- | :--- | :--- |
| S1，[quant-ph/0402130v5](https://arxiv.org/html/quant-ph/0402130v5) §§3.1、8–9，尤其 Def.3.2 與 §8 的 preparation／measurement | 預設 category 的 objects、帶型別的 morphisms `A→B`、composition／tensor、compact closure 和 biproducts；可表述 teleportation 等量子協議，不是從無方向結構推導 morphism 的 source／target。 | **A**。所讀段落未給近似 3+1 幾何或熱力學時間箭頭。抽象圖的可彎曲性不能推成物理輸入／輸出已湧現。 |
| S2，[1510.05468v3](https://arxiv.org/html/1510.05468v3) §2 Def.2.1 及其前後的接線定義 | system-types、各有 input／output types 的 processes、把 output 接 input 的規則是定義的三部分；其 causality／no-signalling 論證在這些輸入之上。 | **A**。所讀定義未產生 3+1 或記錄的單向累積。推得 no-signalling 不表示局部端口方向從無方向基底長出。 |
| S3，[1011.6451v3](https://arxiv.org/html/1011.6451v3) §II 的 `Transf(A,B)`／並排與串接，Axiom 1 | 操作事件起初帶 A→B 系統型別；causality 公設使準備的機率不依賴往後觀測選擇。量子理論的資訊推導建立在這套操作公設上。 | **A**。所讀範圍未推近似 3+1 或宇宙低熵起點。公設中的「往後」不能記成從無方向底層導出。 |
| S4，[gr-qc/0608043v1](https://arxiv.org/pdf/gr-qc/0608043) §§2–4、量子電路例子 §6 | 以標記 `x` 的 elementary regions、觀察結果／設定的 cards、機率及 physical compression 組合區域，不先指定所有區域的固定因果關係；作為量子理論例子的 superoperator 仍寫 `ρ(t)→ρ(t+1)`。 | **B（僅抽象區域關係）／D（局部方向的導出）**。所讀部分沒有無方向底層導出局部端口的定理，也未建立 3+1 幾何或熱力學箭頭。因果關係未固定，不代表區域、標記、設定均已導出。 |
| S5，[1105.4464v3](https://arxiv.org/html/1105.4464v3) Results 與補充 `.2 Definition of process matrices` | 局部實驗室先接收系統、操作後送出，局部量子操作帶 input／output；**實驗室之間**不預定全局因果序。文中給可違反固定因果序的 causal inequality；其經典極限因果序敘述限該框架。 | **A**。有具體可失敗的全局因果檢驗，不能把它當成局部方向已湧現，也不能由經典極限直接讀出 3+1 幾何與熱力學箭頭。 |
| S6，[1406.3829v4](https://arxiv.org/html/1406.3829v4) Introduction、`Dropping the assumption of predefined time`、(25)–(26) 與末段 QFT 討論 | 明確取消 boundary systems 的過去／未來二型區分；區域上的 events 是有限維邊界 Hilbert spaces 的正算子，匹配維度的邊界以 entangled state 接線，網絡的機率依含分母的 contraction 規則。允許 pre／postselection；time-reversal 結構編在連線態中；分母為零另有處置。 | **B**：確有不預設局部**連線的時間方向**的量子操作框架，但區域、邊界分解、Hilbert 維度、連線態及規一化仍作輸入。§末 QFT／light-cone 的討論以既有 spacetime／lattice 為直觀例，不是由此推得近似 3+1 或紀錄箭頭的證明。不能把「無預設」升格成「已從無方向導出方向」。 |
| S7，[2502.10368v2](https://arxiv.org/pdf/2502.10368) Def.1.2、§3 Example 3.3／Def.3.4 | time-neutral processes 的系統列表不分 input／output，按可接線性組合；operad 的 objects／wirings／代數結構是外給的。Example 3.3 把有限維矩陣代數與正元素（按非零實數比例取類）用作 time-neutral quantum theory 例子。 | **B（組合語法和有限維例）**。沒有在所讀處從此構造近似 3+1、紀錄箭頭或必然的局部輸入／輸出選取法。它擴大可表達的接線類，不等於已有物理動力學挑出我們的時空。 |
| S8，[1608.06940](https://arxiv.org/pdf/1608.06940) 引言、§12.5 `Time direction field` 及相鄰 agency 段 | GR 的 operational space 依標量場巧合、metric 與 region 構造；加入有效 agency 時引入 time-direction field `τ` 以選 forward light cone，作者稱其有效概念。 | **D（不是無向量子過程的直接構造）**。這是對照案例：在所讀 §12.5，方向以額外有效 field 給入，metric 光錐已在；不能將「effective」解讀為已由該稿的無方向量子底層推得 3+1 或低熵時間箭頭。 |

## 5. 按 #122 §1 八條標準回填

| 共同標準 | 本輪有界證據和空白 |
| :--- | :--- |
| 1 相同問題 | S6、S7 回答「接線可無時間方向」的存在問題；S1–S3、S5 說明通常在何處先給局部型別；八份均未給完整的「由無方向物理底層導出局部方向、3+1、箭頭」鏈。 |
| 2 證據等級 | 原文的定義／算式與 causal inequality 是來源的明載陳述，不是本 repo 已複核的新構造或新實驗 PASS；以上 A／B／D 是作者分類，未查到的格仍空白。 |
| 3 primitive 帳 | S6 仍需 boundary Hilbert spaces、正算子、連線 entangled state、time-reversal 結構、規一化；S7 需系統類型和 operad 接線法。舊路線 P0.4 的 L／Q-02 不直接移入新路線。 |
| 4 障礙帳 | 本輪不重證任何候選 no-go；舊 #108／#111／#119／#120 的限定障礙不適用於此不同型別的模型。沒有在此樣本見到 FAIL，不能記 PASS。 |
| 5 欠帳與可檢驗性 | S5 有對全局固定因果序的 causal inequality；S6 說連線態編碼的對稱可原則上測試。兩者都不是事前登記的「無方向→局部方向→3+1／時間箭頭」全鏈檢驗；輸入域、資料、判定式及 FAIL 處置需新契約。 |
| 6 下一步成本 | 若選 S6 類方向，要逐一審邊界／連線態來源、正性／規一化及導出局部方向的條件；若選 S7 類方向，還須給物理概率與幾何動力學。這是**作者推論的文件工作**，非建議直接照抄任何來源。 |
| 7 重新評估條件 | #122 所列兩條當時是「部分」與「未滿足／未盤點」；本輪定位了 B 類具體形式，**沒有**在本 repo 登記並複核一個滿足同標準的競爭構造，不能回寫轉向的理由為條件觸發。 |
| 8 對稱決策 | 不排名 S1–S8，不宣告新路線成功；因果序先行的已證結果與暫停義務仍照 #123 封存。下一步只可選具體問題／來源後另走契約、資料、規格門檻。 |

## 6. 限定結論與未解問題

**原文明載（S6、S7 的上述位置）：** 至少有兩種不同層次的
「局部接線不預設輸入／輸出時間方向」形式，一是有限維邊界量子
操作及其接線機率，一是容納 time-neutral 量子例子的 operad 語法。
所以把所有過程理論都說成必定在每個局部連線預設進出，是錯的。

**作者推論：** 這是固定來源集合中的 B 類答案，且共同代價是系統
／區域／邊界／接線規則仍作 primitive。所讀範圍沒有 C 類的完整
方向導出，也沒有同一組 primitive 生出近似 3+1 局部幾何及
紀錄的熱力學箭頭的可核證明。**未查到**僅限本輪八來源與所讀
章節，不宣稱整個文獻不存在。下一個可審問題是：
若以 B 類為出發點，何種不依賴既有時間排序的附加條件，
能選出局部方向，且給出具名輸入與可失敗判準？此處不提出
模型或答案。#123 的操作者轉向仍只是方向決定，盤點不構成
新契約或試作 GO。
