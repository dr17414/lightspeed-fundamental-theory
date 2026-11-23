# 量子過程先行：局部進出方向的有界文獻盤點

狀態：探索軌；本版先固定問題、來源和判讀規則，結果欄尚未填寫。
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

## 4. 原文核讀及結論（待填）

本節在本次事前固定提交中保持空白；後續獨立提交按上表填寫，
並在三帳追加實讀位置與 incidental exposure。標準、分類與八份
來源不得因閱讀結果而悄悄變動。
