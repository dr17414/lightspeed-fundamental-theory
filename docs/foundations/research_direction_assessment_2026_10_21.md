# 研究方向評估：從必要條件審計轉向具名構造

狀態：**【提案／方向評估，待獨立複核】**。2026-10-21 Asia/Taipei。
Assessment ID `X-DIRECTION-20261021`；新 model ID **NONE**。
這是操作者「你來研究並建議方向」授權的文獻／選題評估，不是T6後續推導、
構造契約定案、formal criterion選擇或科學執行。
**探索軌，不具 §5.2.1(v) 依據資格。**

## 1. 建議與基線

建議主線：**原始輸入限制下，1+1 massless非局域傳播與量子資料的同源構造可行性**。
短期文獻對照服務這個問題；不再把一般必要條件重述當成下一輪主要成果。
目前沒有找到可直接符合S5C來源限制、並已交出完整量子資料鏈的現成方案；
這是本輪有限搜尋的結果，不是完整文獻不存在證明。

main `630d4628b7e8603a08d2167a92122b3073dc9759`／tree
`1a85110bc0e3d44a64efa2a9f6df24deff5c0208`已合併#93。
本評估接在尚待複核的#94 head `8dceb4b3afec47fe2e7e3abbbc4d1ac121897036`／tree
`e6eb52f66dbc1789cbbf2b00eb71a9f61c7ccb3b`之後；不把#94當作已獲GO或已合併。
ACT-X-0001生效SHA仍`0c386716701589c9a6b0b799636a808aacb9ade5`，限紙上。

| 六欄 | 本評估 |
| :--- | :--- |
| 問題 | 下一個理論工作應補哪個實質缺口，與既有文獻有何關係？ |
| 輸入 | 目前公開路線圖、T1/T5、T2/T3、T6、C2/r3的限定結論；下列原始文獻的實際閱讀範圍 |
| 證據 | repo文件與§3來源對照；排序與可行性判斷屬作者推論，不是新定理 |
| 未證橋接 | 沒有K、實際Green→CAR、state/dynamics實現或continuum證明；未完成新穎性查全 |
| 否定／修正條件 | 若需額外physical primitive才可繼續，須明示改成conditional問題；不能悄悄放寬原主張 |
| 後續 | 先交一份具名構造問題契約供exact-head複核；本評估不開始構造、算例、數值或formal回用 |

## 2. 為何現在改變工作重心

[T1/T5](t1_t5_premise_audit.md)已區分order/count與metric、sampling及physical c；
[T2](t2_class_sum_audit_v0_1.md)已釐清class總振幅、分母與物質改善比；
[T3](t3_sector_capability_audit_v0_1.md)已區分sector、fiber、Spin及Clifford資訊；
[T6](t6_quantum_obligation_audit_v0_1.md)已給任意已給CAR資料的必要界。
上述審計沒有否定全部intrinsic構造，但也沒有交出一個可承擔原主張的K。
[C2/r3](c2_r3_shared_mvpd_study_v0_1.md)的共享配置讀值有嚴格的條件式結果，
仍使用外加背景與線性介面，不能直接補成物質裝置或fermionic量子實現。

因此下一個有辨識力的交付，應是實際資料來源與相容性的構造性結果，或對明定構造類的
限定障礙。繼續擴寫一般「需要什麼」清單，對目前最上游的存在性問題增益已下降。
這是研究資源排序判斷，不宣稱紙上審計在數學上已窮盡所有可能。

## 3. 原始文獻給出的路線與限制

| 來源與本輪讀取 | 可支持的定位 | 對下一步的影響 |
| :--- | :--- | :--- |
| Arrighi–Nesme–Forets, [1307.3524v1](https://arxiv.org/html/1307.3524v1)，摘要、引言、§I–VI的工具回傳／收斂段 | 在指定格點與Dirac資料下，unitary quantum walk有嚴格的連續解逼近結果 | 是解析參照；規則格點、時間步、表示不是由本專案poset已導出。其單粒子收斂不能代替任意causet的CAR/state來源 |
| Farrelly–Short, [1303.4652v1](https://arxiv.org/abs/1303.4652v1)，只核摘要與出版資訊；HTML正文讀取失敗 | 研究unitary、有限傳播的離散fermionic系統、local-unitary分解與QCA | 說明有可參照的構造路線；本輪沒有核定其定理前提或搬用到非局域poset |
| Gupta–Short, [2412.03466v3](https://arxiv.org/html/2412.03466v3)，摘要、§1–4與工具回傳Appendix A起段；[出版頁](https://quantum-journal.org/papers/q-2025-09-03-1845/) | 離散時間能量的模性，對填充Dirac sea提出額外邊界及可能pair creation的問題，並提出修改方案 | 必須區分unitarity、CAR、正state與physical vacuum。§4明言還需explicit interacting模型計算，不能寫成所有QCA真空必不穩的已證no-go |
| Noldus, [1305.0443v3](https://arxiv.org/html/1305.0443v3)，摘要、§1–3與工具回傳有限例／譜分解片段 | 另引generating structure，bar與Hermitian adjoint分型；出現mixed norm／ghost問題 | 可定位Green到總CAR的危險環節，不把其generating structure當作本題現成合法K，也不據此否定所有causet fermion |
| Markopoulou, [hep-th/9904009v5](https://arxiv.org/abs/hep-th/9904009v5)，只核摘要；HTML正文讀取失敗 | quantum causal histories另在事件附Hilbert spaces及evolution maps | 「因果結構加量子資料」已有明確先例；新穎性不能僅主張把Hilbert空間掛到poset。沒有核定全文composition／complete-pair定理 |
| Carlip–Carlip–Surya, [2209.00327v1](https://arxiv.org/html/2209.00327v1)，摘要、§1–4及工具可得片段 | KR等不良類在其重力path integral/action下的抑制；更廣類別的證據與限制需區分 | 幾何抑制已有重力機制。未來「物質選幾何」必須與相同重力baseline比較，不能把重力相消當fermion效果；本輪不重證其組合計數 |
| CFS作者網站[基本定義](https://causal-fermion-system.com/theory/math/basic-definitions/)與Finster–Fischer [2605.30199v1](https://arxiv.org/html/2605.30199v1)摘要、引言、§4定位；另見[2026出版版本](https://link.springer.com/article/10.1007/s11005-026-02168-3)工具回傳§4–5片段 | CFS另給Hilbert space、spin dimension與operator measure；該曲時空分析以globally hyperbolic Lorentzian spin背景及quasi-free Hadamard資料起步 | 值得作長期比較，不能把這篇的continuum分析稱作從裸poset導出幾何。兩版本未逐式比較或獨立驗證，亦不搬用其高維重力結果到1+1題 |

搜尋另見Johnston的scalar傳播／量子場摘要、Sverdlov spinor摘要、Mathur–Singh–Surya
link-action摘要及部分2026相關條目；未讀其全文，不給模型優劣或新穎性判決。
搜尋／工具也回傳二手頁與無關條目；它們不是本評估的證據來源。
本輪已見公開文獻公式，不聲稱未來構造會是盲發現；沒有採用其模型或作equation mapping。

## 4. 方向比較：作者的工作排序

| 方向 | 可望補的缺口 | 目前代價／主要風險 | 建議 |
| :--- | :--- | :--- | :--- |
| 原始輸入的1+1非局域K及同源量子對接 | 從實際資料鏈開始回答存在性；最接近Stage 5C目前未交付物 | 高理論風險；沒有現成構造或成功保證，不能先用正W補洞 | **主線**，先縮成有限域解析存在性問題 |
| 規則格點QW／QCA或附Hilbert資料的conditional實例 | 提供已知可工作的參照，辨認新增前提 | 基本思路已有；新增frame／nearest-neighbour等不符合原S5C-Claim | 限定參照；另案才可作conditional分支，不能升格原主張 |
| 物質選幾何／class振幅抑制 | 直接對README長期目標有價值 | 缺物質因子、兩類predicate、分母與完整類別控制；已有重力抑制baseline | 延後至有可用物質動力學後再立題 |
| 全面轉向causal fermion systems | 提供另一套物質／幾何共同描述架構 | 改變基本輸入與主張，學習及對接成本高；不繼承本repo成果資格 | 長期比較，不建議立即換框架 |
| 優先完成Freeze-1a／6a-E | 正式驗證基建與合法性 | 不直接提供K；仍有功效與資源義務，不能靠本輪閱讀解除 | 保留正式軌待辦，暫不作理論主線 |
| 泛用新穎性／必要條件盤點 | 避免重述已知結果 | 容易不斷擴張而仍沒有研究對象 | 把盤點限於主線的來源、假設與可用定理，不作無界獨立專案 |

排序不是成功概率、費用報價或證明某方向不可行。主線不追求一次完成3+1、質量、
重力或流形選擇；這些都不由1+1成功自動推出。

## 5. 建議下一個問題如何收斂

以下只是**待起草契約的問題輪廓**，不是已定案構造類或新的驗收門檻。

1. 在原合法輸入與預先明列的有限domain中，能否定義一份真正使用sector資訊、
   代表／重標記處理清楚的非局域kinetic資料，並交同一資料鏈的retarded inverse？
2. 同一資料能否給有來源的test／adjoint／總CAR form，且支持正歸一化state？
   state未必由K唯一決定；所有額外state選擇須逐項宣告，不能另塞一個無關正W。
3. 若聲稱dynamics，實際給出何種algebra作用與相容性？正性、unitarity、stationarity、
   正能量與vacuum分項；有限域無時間對稱時不硬填energy。
4. 連續1+1目標只作後續比較，先列所需極限與來源，不把有限矩陣相容稱為Dirac恢復。
   有限尺寸之間的相容／boundary依賴須列缺口，不能只選單一容易causet報成功。

第一階段的有用結果可以是：一份有完整來源的具名解析構造，或一個**精確限定類內**的
障礙。尚無答案時就保留OPEN；沒有構造類的completeness，不稱全稱no-go。
新增metric、local frame、spin representation或nearest-neighbour等physical primitive時，
必須先停止原問題，另立conditional契約；不把它們悄悄歸為通用CAR scaffolding。

這些是探索研究目標，不是C0–C11 core、projector、test-space、evaluator或門檻。
不從既有probe／planted控制的成功模式選材料，不根據run1、witness或endpoint輸出選law。
下個契約必須先固定domain、來源、有限構造範圍、非平凡性主張及停止條件，再送複核；
本輪沒有開始該契約定案後的構造、符號診斷、RNG、撒點或科學執行。

## 6. 新穎性與完成界線

本輪能排除的過強說法是：格點Dirac walk、poset上附Hilbert資料、以及一般CAR必要界，
都不能僅憑其名稱作本專案新穎性主張。真正**可能**有辨識力的成果，是更少輸入下的
具體構造、對明定類的障礙，或新的來源／極限對接；是否新穎仍需對實際結果查全。

本評估已完成方向比較，未完成系統性文獻回顧、任何新定理／候選或文獻承重mapping。
不改T6契約、acceptance、formal來源、6a-E／Freeze-1a、E0與UNKNOWN／禁止資料隔離。
本輪來源與推薦申報見[獨立補充檔](research_direction_exposure_supplement_2026_10_21.md)；
擬登記0077／0078，尚未整合進canonical三帳，整合前須核對ID。無Claude本輪申報，不代填。
