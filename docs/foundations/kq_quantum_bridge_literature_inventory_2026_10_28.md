# KQ 量子橋接：有界文獻盤點（2026-10-28）

狀態：**【探索／文獻定位與作者分類，待原文抽查及 exact-head 複核】**。
**探索軌，不具 §5.2.1(v) 依據資格。**
基線 main `74b012db50ee1d7ac3e4288284ff3a28686a3cf2`，tree `81c0105a10186352bfe36d2a0f8e05589c01c9ee`。
這是有界盤點，不是構造、CF-02 規格或新問題契約；不選 K、adjoint、F、state 或工作域。
[原始輸入問題](kq_1p1_construction_problem_contract_v0_1.md)與
[conditional 問題](kq_conditional_time_adjoint_problem_contract_v0_1.md)都維持 OPEN。

## 1. 範圍、判讀與主要發現

操作者轉交的選題紀錄為台北 2026-10-28 17:39：先盤點，暫不開 CF-02。
本交付第一 commit 只追加三帳、逐字登 EXP-0105／0106／0107；本稿與實讀申報在後一 commit。
公開 Git 至多證明版本順序，不證閱讀或思想的盲性。先前 CF-01 與 reviewer 的提示都是已見資訊。

每項文獻判斷用下列一個標籤，來源 ID 的版本與實讀範圍見 §2：

- **原文明確陳述**：在所列原文位置讀到定義、命題或限制；不代表本輪獨立重證。
- **作者推論**：本稿作者對來源型別、KQ 對接或新穎性的比較判斷；不是原文的 KQ 結論。
- **未查到**：只在本輪有限搜尋／已讀範圍未找到，不是不存在的證明。

**作者推論〔S1 Def.3.1、Thm.3.22；S2 §4.3.1；S3 §III.D；S8 §II〕：**
「有限維可逆矩陣的雙邊 inverse 唯一」沒有被這些文獻推翻。它們分別使用不同型別的
Green 映射、轉置／dual 定義、含邊界資料的方程或事先給定的 CAR，不能統稱為
「同一有限完整 test space 上、同一可逆 K 的兩個不同雙邊 inverse」。
這項型別區分是盤點結論，不是新增不可能定理。

**作者推論〔本庫 CF-01 §4、§6、§7；S1–S9〕：**
CF-01 已通過的是在外加 Ξ 下的探索 sector span 判準，並未解物理 spinor、混合、dynamics 或 continuum。
因此不採用「其他物理義務都已解、只剩一個問題」的擴大敘述；本稿只聚焦尚缺來源的量子橋接。
同樣不把兩個限定障礙改稱原始輸入不足的全面證明。

## 2. 版本、原文入口與本輪實讀範圍

以下是**選讀**，沒有任何一列聲稱全文逐頁驗算。頁數依所列版本；章節／式號優先於 PDF 頁碼。
所有入口於 2026-10-28 存取。無版本網址的 PDF 以當時讀到的頁首版本為準；讀者應核對頁首。
搜尋服務的 open／find 會回傳相鄰正文；這些額外曝光也列在範圍欄，不稱只讀摘要。

| ID／原文與版本 | 實際閱讀及用來承重的位置 | 沒有完成的閱讀／驗證 |
| :--- | :--- | :--- |
| S1 Christian Bär, *Green-hyperbolic operators on globally hyperbolic spacetimes*, [1310.0738v2](https://arxiv.org/pdf/1310.0738v2)，2014-07-14 | Def.3.1、3.7，Lemma3.21，Thm.3.22／exact sequence (4)；連帶摘要與 §3.6、§4.1／Thm.4.3 片段 | 非全 26 頁；不搬用未讀的 Dirac 正性證明 |
| S2 Steven Johnston, *Quantum Fields on Causal Sets*, [1010.5514v1](https://arxiv.org/html/1010.5514v1)，2010-10-26／學位論文 2010-09 | §4.3.1 (4.6)–(4.8)、§4.5.1 (4.23)–(4.29)、§6.1–6.5 選段，重點 (6.13)–(6.19)、(6.25)–(6.26) 及 footnote4；亦見目錄、相鄰 §4.2.3／4.4.2 與 §7.1 片段 | 非整本論文；未讀其所引 Feynman–Hibbs 原書 |
| S3 E. Dable-Heath, C.J. Fewster, K. Rejzner, N. Woods, *Algebraic Classical and Quantum Field Theory on Causal Sets*, [1908.01973v3](https://arxiv.org/pdf/1908.01973v3)，2020-02-25 | §III.B.1 (33)–(36)、III.B.4 (64)–(67)、III.C.2 (81)–(83)、III.D (89)–(92)，IV.C 定義IV.7／(121) 開頭；連帶摘要、§I–II.B 正文、III.E／Wick (135) 與正性段落的搜尋回傳片段 | 非全 42 頁；未核全套 interacting／state 證明；本篇是純量場 |
| S4 Johan Noldus, *Free Fermions on causal sets*, [1305.0443](https://arxiv.org/pdf/1305.0443)，頁首 **v3，2015-01-26** | 摘要／§1、§2 generating structure、involution／adjoint 定義與 footnotes5–9，§3 CAR／模式／負範數及 ghosts；連帶 §4 例子與 eigenvalue 片段 | 非逐頁重證 8 頁；未計算任何例子的譜；內頁排版日期不充作 arXiv 版本日期 |
| S5 Roman Sverdlov, *Spinor fields in Causal Set Theory*, [0808.2956](https://arxiv.org/pdf/0808.2956)，頁首 **v1，2008-08-21** | 摘要，§1 (1)–(3)、(9)–(18)，§2.1／§2.2 開頭 (18)–(21) 的 Lagrangian／holonomy；連帶後段 time-axis 片段 | 非全 21 頁；未核整套離散 Lagrangian，未讀到正 CAR／state 定理 |
| S6 C.J. Fewster, B. Lang, *Pure quasifree states of the Dirac field from the fermionic projector*, [1408.1645](https://arxiv.org/pdf/1408.1645)，頁首 **v2，2014-09-26** | 摘要／引言，§2.2 (1)–(4)、§2.4 的 Green 映射／Hilbert 空間 (9)–(16) 及 Lemma2.2 相鄰證明，§2.5 CAR 定義；§3 建構的 (21)、(25)–(30) 與 positive projection，§4 結論；另見 §2.3、§3.1 Thm.3.4 的片段 | 非全 26 頁；未完整核 Hadamard 證明；內頁較晚排版日期不改 v2 身分 |
| S7 E. Hawkins, C. Minz, K. Rejzner, *Quantization, dequantization, and distinguished states*, [2207.05667v2](https://arxiv.org/pdf/2207.05667v2)，2024-09-13 | PDF 摘要、§1、§2.1 (1)–(9)、§6 結論；連帶 §2.2–2.3 開頭、§5 結尾／Appendix A 的回傳正文；另讀出版社搜尋回傳 §2.4 Defs11–13／(33) 片段 | 非全 34 頁；未讀完 geometric quantization 證明；出版社直接開啟受阻，以上主張核回 arXiv |
| S8 T.C. Farrelly, A.J. Short, *Causal Fermions in Discrete Spacetime*, [1303.4652v1](https://arxiv.org/pdf/1303.4652v1)，2013-03-19 | 摘要／§I、§II (II.1)、(II.4)–(II.5)，§III Def.1、Lemma1／III.A 開頭；§IV.A 的 shift／mass／continuum 式 (IV.5)–(IV.10)、IV.D (IV.30)–(IV.35)；連帶 IV.C、§V 開頭及參考文獻／appendix 搜尋片段 | 非全 16 頁；未核所有 localizability 或 infinite-lattice 證明 |
| S9 P. Arrighi, V. Nesme, M. Forets, *The Dirac equation as a quantum walk: higher dimensions, observational convergence*, [1307.3524v1](https://arxiv.org/pdf/1307.3524v1)，2013-07-12 | 摘要／引言、§I (2)–(4)、§II Cauchy problem、§III consistency 開頭，另見 §IV norm-stability 片段 | 非全 8 頁；未完整核 §V convergence proof；讀到的是單粒子 walk，不能稱已讀 CAR 建構 |
| S10 C. Biró, P. Hamburger, A. Pór, W.T. Trotter, *Forcing Posets with Large Dimension to Contain Large Standard Examples*, [1402.5113v3](https://arxiv.org/pdf/1402.5113v3)，2015-08-24 | 摘要及 §1.1 standard example 定義／dim；find 另回傳後續定理及隨機 poset 片段 | 不核那些後續證明；不以本文作者取代其追溯的 Dushnik–Miller 原創歸屬 |
| S11 Toronto／Meinrenken 課程站，*Clifford algebras*, [Chapter2 PDF](https://www.math.toronto.edu/mein/teaching/LieClifford/cl2.pdf)，**檔內未見版本日期** | §2.3 Prop.2.5、§2.4 Prop.2.6 及相鄰實分類 Prop.2.4；另見開頭 exterior-algebra 定義 | 作者課程材料，不冒稱原始發現論文；非全 13 頁，沒有替無日期檔案編出版年 |
| S12 D.J. Kleitman, B.L. Rothschild, *Asymptotic Enumeration of Partial Orders on a Finite Set*, Trans.AMS205 (1975),205–220，[DOI](https://doi.org/10.1090/S0002-9947-1975-0369090-9)／[作者上傳正文](https://www.researchgate.net/publication/243778189_Asymptotic_Enumeration_of_Partial_Orders_on_a_Finite_Set) | 作者上傳的原文 OCR：摘要、§1、§2 開頭，pp205–206；上傳頁記 Kleitman 2014-07-22 | AMS PDF 取用失敗；OCR 排版不佳，不藉此認證精確 prefactor 或未讀 §3 證明 |
| S13 Steven Johnston, *Particle propagators on discrete spacetime*, [0806.3083v2](https://arxiv.org/pdf/0806.3083v2)，2008-10-01 | 摘要，§3 (3.1)–(3.5)、§3.2 結尾 (3.33)–(3.44) 選段、§3.3 fluctuations | 非全 14 頁；未重算 Fourier transform 或數值圖 |
| S14 F. Dowker, J. Henson, R.D. Sorkin, *Discreteness and the transmission of light from distant sources*, [1009.3058v2](https://arxiv.org/pdf/1009.3058v2)，2010-10-07 | 摘要／引言，§3.1 結尾 (30)–(31)、§3.2 開頭 (32)–(36) 的二階矩與 blocking | 非全 16 頁；未完整核所有 fluctuation bound 或器件近似 |
| S15 H. Araki, *On Quasifree States of CAR and Bogoliubov Automorphisms*, Publ.RIMS6 (1970/71),385–442，[出版社原文](https://ems.press/content/serial-article-files/41673?nt=1) | 摘要／引言，§2 pp386–387、§3 Lemmas3.2–3.3／(3.3)–(3.5) pp388–389；連帶 Thm.1 敘述 | 非全 58 頁；不把 quasifree state 定理當作由 order 導出 CAR |

### 2.1 搜尋邊界與沒有讀到的原文

搜尋主題含 causet fermion／Dirac propagator、finite inverse／Peierls、fermionic SJ／fermionic projector、
checkerboard、discrete Dirac walk／causal fermion QCA，以及各新穎性項目的具名詞。
使用兩個網路搜尋引擎及 arXiv／作者站／出版社原文定位，沒有作系統綜述或窮盡引文網絡。

**未查到〔本輪檢索與 S2 §6.5、S4 §3、S6 §2–3、S7 §6〕：**
沒有核到一個在任意本題有限 causet／完整 T 上，從同一 K 導出正總 CAR 並滿足現行全部量詞的
「費米子 SJ」定理；這不是宣告文獻不存在。S6 是已讀到的連續 fermionic SJ 類比；S7 的
§6 明將 fermionic extension 列為後續挑戰，不能據一篇論文推出整個領域的否定結論。

Feynman–Hibbs (1965) 原書 pp35–36 **未讀**，只經 S2 §6.3 讀其 checkerboard 描述。
Skopenkov–Ustinov *Feynman checkers*（arXiv:2007.12879）PDF 過大、HTML 取用失敗，
沒有讀正文或核版本；Jacobson checkerboard 相關項目僅見摘要／書目搜尋片段，不承重。
Fewster–Verch 1206.1562、Finster–Murro–Röken 1501.05522、Minz 2021 thesis／2024 DIAS slides、
Noldus 其他版本等只見摘要／引文或搜尋片段，沒有聲稱讀其正文。
二手綜述、百科與書目網站也曾出現在搜尋結果，未用作技術結論依據。
指定版號 URL／ar5iv 曾取用失敗的 S4–S6，後改由 arXiv PDF 頁首核版本；失敗請求不算原文閱讀。

## 3. 「有限 inverse 唯一」：文獻實際改了哪個型別

### 3.1 連續 Green 映射：不是同一有限向量空間的兩個 inverse

**原文明確陳述〔S1 Def.3.1、Def.3.7、Lemma3.21、Thm.3.22／(4)〕：**
Green maps 從 compactly supported tests 到 smooth sections，並帶相反的因果支撐條件；
causal propagator 是兩者之差。其 exact sequence 分開 compact 與 spacelike-compact 空間。
dual Green 關係涉及 formal dual operator，不能把 dual 無條件換成 ordinary Hilbert adjoint。
S1 將帶 J⁺ 支撐的 G⁺ 稱 advanced、J⁻ 的 G⁻ 稱 retarded；本稿按支撐型別比較，不移植名稱符號。

**作者推論〔同上；S6 §2.2、2.4〕：**
因此連續結果不與有限 square matrix inverse 的唯一性衝突。所需 bundle、時空幾何、支撐／domain
及 pairing 才是承重資料，不是「選另一個 inverse」這一句話。這不替 KQ 選 boundary 或 test quotient。

### 3.2 有限 causet：轉置 prescription 與動力學的差別有原文明說

**原文明確陳述〔S3 §III.B.1 (33)–(36)、III.B.4 (64)–(67)、III.C.2 (81)–(83)、III.D (89)–(92)〕：**
文中離散方程用 kinetic **P** 和 source kernel **K**，有 E⁺=P⁻¹K、E⁻=(E⁺)ᵀ、E=E⁻−E⁺。
有 past-infinity data 的初值式不是全域 Pφ=0。§III.D 直接指出 transpose 通常不是 P 的 inverse、
EP 通常不為零，因此按方程式理想取商會破壞 Peierls bracket；改按 (90) 的 bracket-null functionals 取商。

**作者推論〔S3 同上〕：**
這是有限離散問題的直接對照，但屬**純量 Poisson／CCR**，不是費米子正 CAR 解法。
文中 K 是 source kernel，不能與本庫 kinetic K 同名等同。其取商不是按負譜刪模；
也不能因此宣稱現行完整 T／反補洞契約已容許同一取商。

### 3.3 Johnston：path propagator、transpose、scalar SJ 分開處理

**原文明確陳述〔S2 §4.3.1 (4.6)–(4.8)、§4.5.1 (4.23)–(4.29)〕：**
嚴格 triangular、零對角的 path K_R 不可逆，作者討論 contact／對稱組合等另行取得 d'Alembertian 的方式。
scalar 部分定 K_A=K_Rᵀ、Δ=K_R−K_A，並以 iΔ 的正部分定二點函數 Q。

**作者推論〔同上；S2 §6.5〕：**
這裡 K_R 是 propagator，並非本庫 kinetic K；Q 是 scalar covariance，不是 fermion 的總 CAR form。
不能將 scalar SJ 的正部分直接抄作正總 CAR，或認為這裡已給同一有限可逆 kinetic 的兩個 inverse。

### 3.4 符號與 adjoint 不是免費選項

**原文明確陳述〔S4 §2 footnotes5–9、§2 結尾、§3；S6 §2.2 (4)、§2.4 (15)–(16)〕：**
S4 的 radiative propagator 為 Δ_m=−A_m+A_m†，† 由 Clifford involution／不定內積實現，
普通矩陣 Hermitian conjugate 另記 H。S6 的 † 是 spinor→cospinor 的 Dirac adjoint，含 γ⁰，
正解空間內積則由 Green 配對等於 Cauchy L² 範數來建立。

**原文明確陳述〔S4 §2、footnotes5–9〕：**generating K 另受 K⋆=−K 的要求；
這個 Clifford ⋆、† 和 ordinary H 是不同的操作。**未查到〔上述實讀範圍〕：**
一個可直接在現行 Ξ 全工作域套用、由 kinetic 的反自伴符號關係保證正總 CAR 的定理。

**作者推論〔同上〕：**
兩篇都不能簡化成對 CF-01 加減號的任意翻轉。「formal dual」「Dirac adjoint」「ordinary †」
及其 domain 不同；本輪不提出符號替代公式，也不聲稱反自伴性單獨足以保證正 CAR。

## 4. 因果集費米子與 SJ：adjoint／正性的逐篇上限

| 來源與精確位置 | 證據等級與所讀到的 CAR／adjoint 來源 | 正性／缺口與額外結構 |
| :--- | :--- | :--- |
| S2 §6.4–6.5，(6.13)–(6.19)、(6.25)–(6.26)、footnote4 | **原文明確陳述**：fermion 章採 tentative 定位；以 combined event／spinor indices 的轉置差定 Δ，提出反對易關係；footnote4 說 † 或需改為 Dirac adjoint ψ†γ⁰；square root 選擇也未唯一 | **作者推論**：這是 proposal，未讀到可直接填 KQ 正 state 欄的定理；spinor／gamma／square root 與正性仍須辨識，不能把 tentative 句寫成已完成費米子 SJ |
| S4 §2 adjoint footnotes5–9；§3 模式關係與末段（pp6–7） | **原文明確陳述**：給 Clifford generating structure；barψ=ψ^Hγ，ordinary-H 反對易矩陣為 iΔγ；建構需所用 spectral decomposition 存在 | **原文明確陳述**：作者明留正、負範數粒子及 complex ghosts，退化時可能無所需譜分解。**作者推論**：不是現行正 Hilbert／正歸一 state 的無條件解；Clifford／γ 生成資料也多於 bare order |
| S5 §1 (1)–(3)、(9)–(18)，§2.1–2.2 (18)–(21) | **原文明確陳述**：用 vierbein／holonomy 類資料與 Grassmann 積分規則寫 spinor Lagrangian；標準 gamma／bar 配對作比較輸入 | **未查到**：在實讀段落未讀到由同一 Green 鏈建立正 CAR／state 的定理，不推論全篇沒有。signed Berezin measure 是積分工具，不等於 S4 的負 Hilbert norm |
| S6 §2.4 (15)–(16)、§2.5；§3 (25)–(30)、§4 | **原文明確陳述**：在正 solution Hilbert 上先定 self-dual CAR，再以 fermionic-projector spectral projection 選 quasifree covariance；Dirac adjoint 已給 | **原文明確陳述**：其場景是 massive Dirac、具 spin／gamma 的 globally hyperbolic ultrastatic slab、compact spatial section；softened 與 unsoftened 的 Hadamard 行為不同。**作者推論**：這是連續 SJ 類比，不是有限 causet 正總 CAR 定理 |
| S7 §2.1 (1)–(9)、§6 | **原文明確陳述**：由 scalar symplectic space 加 inner product 處理 SJ；結尾將 fermionic extension 列為待做 | **未查到**：本篇沒有交付本題所需的有限費米子版本；不能由它推論其他作者也沒有 |

**作者推論〔S6 §2.4–3；S15 §3 Lemmas3.2–3.3；本庫 T6 §3.1、§3.3、§4〕：**
「已正的總 CAR 上，選 0≤S≤I 的 covariance」與「從 K 得到正的總 CAR」是兩道義務。
S6 的正投影只做前者，沒有以投影修補一個不定號總 form。正性並不等於 Hadamard／物理真空條件；
後者也不能由有限維 Fock 態存在自動獲得。本稿不使用任何譜切除來改 KQ 的完整 T。

## 5. Checkerboard、Dirac walk、QCA：與 CAR 的接點

**原文明確陳述〔S2 §6.3–6.3.1；原 Feynman–Hibbs 原書未讀〕：**
Johnston 轉述的 checkerboard 使用 1+1 Minkowski null zigzags、離散時間／lightcone lattice
及 mass corner weights，並指出在 causet 中只用 links 不足以辨識 corners。
**未查到〔該段〕：**沒有在此讀到由這個單粒子 path amplitude 同時建立正 field CAR 的定理。
這是對 S2 的引用，不冒充核實 Feynman 原始文本。

**原文明確陳述〔S8 §II (II.1)、§III Def.1、§IV.A (IV.5)–(IV.10)、§IV.D (IV.30)–(IV.35)〕：**
Farrelly–Short 先設 spatial lattice／fermionic modes／δ-CAR／Fock 空間，再研究 causal unitary。
其離散 Dirac 例子含 conditional shifts 與 mass rotation。§IV.D 特別區分場模式、電子／正電子分量
及 naive vacuum／physical vacuum，後者的詳細離散討論留待未來。

**作者推論〔S8 同上〕：**
這是「先給 CAR 再演化」；所讀原文沒有把所有 spacetime events 上的 δ-CAR 稱作 kinetic inverse 導出物。
與 propagator 路線的接點是演化／Green 對場與 smearing 的作用，不能把演化定理倒置成 CAR 來源定理。
本輪不另推 unequal-time kernel。正 Fock 表示的存在也不等於選好了物理真空。

**原文明確陳述〔S9 §I (2)–(4)、§II；完整 convergence proof 未核〕：**
Arrighi–Nesme–Forets 使用規則 grid、spinor／Clifford matrices、conditional shifts 與單粒子 unitary walk，
討論其 Dirac 近似與收斂。**作者推論〔同上〕：**單粒子 norm 的么正性不等於從 causet K 得正總 CAR；
本輪沒有把其 coin／shift 納入 Ξ，也不把未完整核過的收斂率當 KQ 結果。

## 6. 已確認項目的新穎性初對照

新穎性欄的「已知／部分已知／可能是新的」是**作者推論**，不是優先權認證。
「可能是新的」只指尚未在本輪有限讀物找到同一精確命題；與證據標籤「未查到」一起讀。

| 本庫對象與定位 | 文獻證據（原文明確陳述） | 新穎性判斷與界線（作者推論／未查到） |
| :--- | :--- | :--- |
| T3 §2.3 的六點 crown／standard example S₃，order dimension=3 | S10 §1.1 明列 standard example S_d 與 dim S_d=d，並追溯 Dushnik–Miller | **已知**：order-dimension 事實。不要與 OP-01 的四點三葉 star 混同；T3 特定 Minkowski witness／來源論證不能據此自稱原創或全面 spinor no-go |
| T3 §4.3：非退化完整複 Clifford 模的維數下界 | S11 Ch.2 §2.3 Prop.2.5 的複 Clifford 分類；§2.4 Prop.2.6 的代數基底 | **已知**：模維數約束的標準代數內容；套回「兩個 slots 不能承完整 3+1 Clifford」是本庫型別校準，不是新 Clifford 定理 |
| T2 §§2–3：KR 計數與 measure 換算 | S12 §1 pp205–206：log base2、既定 labelled set 上 P_N 的 log₂ 漸近 n²/4+3n/2+O(log n) | **已知**：KR 主計數。**部分已知**：labelled／unlabelled／1/Aut 與複相位的條件式換算，是標準計數及本題 measure 審計；原文不是任意被稱 KR 子類的定理，未查到完全相同的整套應用，不認證新穎 |
| C2 兩稿 §§3–7：固定 source smeared link mean／variance、native detector blocking 修正 | S13 §3.2–3.3 已有 continuum mean 與 fluctuation 討論；S14 §3.1–3.2 已處理 source worldline／有限 detector／二階相關及 mutual blocking | **部分已知**：mean 極限與 fluctuation 問題早已有。**可能是新的／未查到**：本庫固定 test／端點語義下的明確保守界及量詞，尚未在所讀原文定位同一命題；S14 的 source proper-time 積分不是 C2 fixed-source Lebesgue functional，未核其全證明，不能宣稱首個 variance 收斂 |
| T6 §2–3：A=Q+R、0≤Q≤A、Riesz／charged／self-dual 必要界 | S15 §2、§3 Lemmas3.2–3.3／(3.3)–(3.5)；S6 §2.5、§3 的 positive contraction／self-dual covariance | **已知**：CAR／正 functional 的標準內容，本庫也是條件式校準；未從 I6 推出物理來源，不能以記號換寫認證新結果 |
| OP-01 §§4–6 的 G_swap／ordinary-adjoint 限定障礙；CF-01 §6 的 G_η 限定障礙 | 已合併研究稿給精確假設；S15／T6 的正性條件與標準 commutant／零對角半正定線性代數是已知背景；S2–S9 沒有替這兩個具名類提供同一來源定理 | **部分已知**：承重代數不是新工具。**可能是新的／未查到**：特定自然性群、完整 T、contact 與 prescription 的合併排除敘述，在此有限讀物未定位同式命題；不宣稱原創，更不擴為一切 Ξ 的 no-go |

C2 的比較只核對已合併稿聲明的對象／量詞：link 稿 §4、§6 的 mean 保守界
O(κ⁻¹ᐟ²logκ)、variance 保守界 O(κ⁻¹ᐟ²⁰)，以及 native 稿 §§6–7 的
O(κ⁻¹ᐟ²) 修正項；未在本輪重證其界、重跑其科學模型或選新的 smearing。
這份表不是對 CF-01 契約 §8「最低差異的完整數學證據」交付新構造成果；它只做文獻定位。

## 7. 本輪接觸、驗證與後續使用界線

全部 S1–S15 的上述實讀範圍、搜尋／取用失敗及 incidental exposure 登於 canonical 接觸帳
§50／EXP-0108；此表是可讀索引，不取代 canonical 登記。EXP-0105–0107 的 reviewer 原句保留原樣。
另重讀／定位了本庫 STATUS 的目前狀態、兩份 KQ 契約、CF-01／OP-01 的結果與限定類、
T2／T3／T6 對應節、兩份 C2 稿的目標／文獻／誤差及量詞、既有方向評估與 exposure supplement 的引用位置；
文字搜尋也回傳其相鄰內容，不稱未接觸。

本輪有檢索、原文閱讀、型別比較及新穎性**分類**；沒有選新構造或完成新數學證明，
沒有執行本題的新數值／符號計算、RNG、撒點、producer、raw／sealed 或新科學程式。
文件／Git hash／prefix／連結檢查與既有 repo 回歸，若執行，僅作交付驗證，不充當科學證明。
後續若依此選 CF-02 規則，須另作事前獨立規格與引用披露；本稿不授權任何方案。
formal／E0、A／B、6a-E／Freeze-1a、UNKNOWN 與既有禁止資料隔離不變。

## 8. 最後分類：文獻中的 adjoint／CAR 來源放入現行 Ξ 時如何記帳

以下每列都是**作者推論**；文獻事實的版本／位置沿用列內來源，契約比較以基線的
X-KQ-COND-TA-P0.1 §§3、4.3–4.5、5.3、7 及 CF-01 §6 的 **G_η 精確前提**為準。
「G_η 之外」只表示少了該限定類的一項前提，**不表示已正、已合規或已可完成主問題**。
若只是一段通用數學定義，不把定義本身叫 physical primitive；實際資料的來源仍要交代。

| 已出現的來源類型／原文定位 | 相對 Ξ=(L,R₀)：新增 primitive 或型別改變？ | 與 G_η／現行鏈的關係，僅分類 |
| :--- | :--- | :--- |
| 支撐／domain 與 formal dual 的 Green maps；S1 Def.3.1、Lemma3.21、Thm.3.22 | 連續 bundle、幾何、test／solution／boundary 型別不是一份 L 加固定 R₀；若實際引入，須另審，不能只改名稱 | 不在有限完整 T 上同一雙邊 inverse 的比較類；沒有由此逃過 KQ positivity 的定理 |
| 有限 scalar path transpose／Peierls／bracket-null quotient；S2 §4.3.1、4.5.1，S3 §III.B–D | counting transpose 作數學操作未必增 physical primitive；但 source／contact／past data 的來源與取商必須另審；不能預設均由 Ξ 給出 | scalar CCR，不直接是 CAR。只用 ordinary transpose difference 並不自動逃過零對角障礙；換 test quotient 不能冒充原完整 T 結果 |
| Clifford／Krein adjoint 與 γ；S4 §2 footnotes5–9、§3 | generating structure／Clifford 模／具體 γ 配對不是既有 R₀ 自動附送。γ 外形像 η₀ 不等於來源與自然性群相同 | S4 的 involution／生成類不等於 G_η；是否與其交疊須逐一核假設。保留負 norm／ghost 不滿足現行正 state 要求 |
| Dirac conserved Cauchy form、spinor→cospinor adjoint；S6 §2.2、2.4–2.5 | spin structure、gamma、metric、Cauchy 幾何與解空間資料超過現行 Ξ；L 不能自動當有空間幾何的 Cauchy 面 | CAR 建在正 solution Hilbert，非全部 events 的 counting T；不是 CF-01 的 G_η prescription。輸入／domain 改動不在本盤點採納 |
| 已正 CAR 上的 fermionic-projector covariance；S6 §3、S15 §3 | 需先有正 CAR／conjugation；S6 還有 spacetime pairing／weight。通用 covariance 定理不能提供缺失的總 form | 選 state 與從 K 導出總 CAR 分帳；若按 A 的負譜修總 form，觸發現行反補洞，不能借 SJ 名稱豁免 |
| lattice kinematic CAR＋causal unitary；S8 §II、III、IV.D | lattice、每片 modes／正 CAR、unitary 及 physical-vacuum 資料不是 Ξ 已含物件 | 不是 G_η Green-difference 鏈；與 K 無關的 δ-CAR 在現行 §5.3 明確被排除，要換鏈須另立契約 |
| checkerboard／單粒子 Dirac walk；S2 §6.3，S9 §I–II | null lattice／grid、方向／coin／Clifford／mass／time-step 等須來源記帳；不能把 L 視作全套 shift | 單粒子振幅／norm 不自行給總 CAR，故還沒有可直接放入 G_η 內或外的完整 CAR 規則 |
| vierbein／holonomy／Grassmann Lagrangian；S5 §1、§2.1–2.2 | 具體 holonomies／vierbein／場變數超過 Ξ；形式 Grassmann 運算本身不證 physical 來源 | 所讀範圍未交正 CAR／state 對接，不能歸作已避開 G_η 的成功案例 |

本節不排序、不選方案，不改兩份契約，也不由文獻讀取結果直接固定下一個構造。
