# P0.4＋Q-02 階段整理：IK-01、K₂,₂ 與三種輸入的必要條件

狀態：**探索軌階段整理草稿，待 exact-head 獨立複核；不是 Q-03 或 IK-02 GO**。2026-11-18 Asia/Taipei。
基線 #120 squash main `ff446fd067bfb16cfdb536cfbdb2787a8f0db8e2`，
tree `50ebf04eb89629e4e72a8ade43138d231e07e792`。
先行三帳 §93 只追加 commit，本文在後。本文參照
[#112 前一階段整理](kq_p03_stage_checkpoint_2026_11_09.md) 的來源表寫法，
整理已見的結果及未決問題；不選 K、Green 式、資料法則或修約，不做新試算。
舊 FAIL 不因 P0.4 的新量詞被追認為 PASS。早期 `codex/…` 分支不在本輪範圍。

## 1. 問題版本及來源對照

[P0.4 契約](kq_conditional_internal_innovation_problem_contract_v0_4.md)
與 [Q-02 資料登記](kq_p04_correlated_innovation_data_registration_v0_1.md)
已分別取得契約 GO、資料 GO；Q-02 重登了 Q-01 的資料 law，
不是資料可行性的結論。[IK-01 規格](kq_p04_internal_innovation_attempt_spec_v0_1.md)
在 #117 GO 後，才有以下固定試算與紙上證明。
P0.4 的 (b′) 對單軌道輸入記 N/A，**不**免除原 P 微因果、
逐輸入 §7(a) 非零傳播、守恆或事前具名的 Green 識別。
表中「不能推出」欄與結論具有同等地位。

| 已有交付與審查身分 | 嚴格作用域與結論 | 不能推出的結論 |
| :--- | :--- | :--- |
| [IK-01 固定研究](kq_p04_ik01_paper_study_v0_1.md) §2–7，#118 main `0fda7d36` | 在 **P0.4＋Q-02＋已 GO 的 IK-01 v0.1 固定 K／source／Green／CAR 規格**下，固定目錄先列全部 PASS、FAIL 和 undefined，再判此版全域 FAIL。dual star 的葉對微因果 PASS；K₂,₂ 的多根共享微因果 FAIL；鏈的守恆及 IK.S1 Green 識別 FAIL；diamond 第二面亦 FAIL。係數、`t` 和判準不改。 | 一版固定 K 失敗不排除別的 K；dual star PASS 不是 P0.4 全域 PASS；鏈的 IK.S1 FAIL 不能排除所有 typed Green 式。 |
| [K₂,₂ 不讀 L 障礙](kq_p04_k22_order_only_obstruction_paper_v0_1.md) §2–5，#119 main `7884ec87` | **P0.4＋Q-02，且完整 K 不讀 L**時，K₂,₂ 的唯一合法面 B、無內部通道；自然性使四個根到頂點響應相同。原 P 微因果使 `2HH†=0`，與每輸入至少一個非零 strict Green block 的 §7(a) 衝突；奇異 diagonal 則先使逆失敗。不限 IK-01 的係數。 | 不涵蓋讀 L 的 K，不是 Q-02 對任意 K 的 no-go，更不是因果序先行路線的否證。 |
| [下一版 K 必要條件](kq_p04_next_k_necessary_conditions_paper_v0_1.md) §2–3，#120 main `ff446fd0` | **P0.4＋Q-02、每個 L、所需面逆存在**時，K₂,₂ 的兩頂點根響應行須正交，且須有非零傳播；若在這個 P 上 K 對所有 L 恰相同，自然性仍導致 #119 的衝突。對所有鏈 `C_N` 的每個合法單點面，嚴格守恆使根響應 `g_m=G_R(m,1)` 可逆且 `g_m†g_m=I`。 | 讀 L 的 K 不因此有解；unitary 根響應不保證 Green、field、(4.2) 或整條跨尺寸 law 成功。 |
| [同一必要條件稿](kq_p04_next_k_necessary_conditions_paper_v0_1.md) §4 (N.5)–(N.9)，#120 | **只在 Q-02 的 diamond** `a≺b,c≺d`，每個 L 的 canonical B 面與 `{d}` 面逆都存在，且完整 CAR 守恆時，`J_b=G_R(d,b)=J_c=G_R(d,c)=0`，根響應 `D=G_R(d,a)` 必須 unitary。原 P 的 `b∥c` 微因果另使 `G_R(b,a)`、`G_R(c,a)` 可逆。依下文 §2，`J_b=J_c=0` 等價於該 diamond 上 `K(d,b)=K(d,c)=0`。 | 不表示其他形狀的 innovation 都不能往後傳；不表示 Q-02 全面不可行、P0.4 全面 FAIL，亦不把此物理詮釋當成已證的資料設計缺陷。 |
| [同一必要條件稿](kq_p04_next_k_necessary_conditions_paper_v0_1.md) §4 (N.10)，#120 | **另外沿用 IK-01 特定 Green 式 IK.S1** 時，diamond 的 canonical `(d,b)` 識別與上一列守恆、微因果矛盾；此條件式障礙不依 K 的係數或 L 是否被讀取。 | P0.4 §5 並未把 IK.S1 指為所有未來 K 唯一可用的式子；不排除另立且事前審查的同源、source-sensitive typed Green 式。 |

#120 經 Claude 逐式 exact-head GO、CI #355 首次同 head 成功；
公開 head `8591ee92` 的 tree 與 main `ff446fd0` 同為
`50ebf04e`。這是兩個 AI 協作角色的獨立文件複核，
不是外部同行評審或物理實驗。#119 兩段此前缺漏的 Claude 原句
於本輪先行帳 EXP-0198–0199 作更正追加；不改寫原帳。

## 2. diamond 的零傳播只限哪裡

#120 (N.6)–(N.8) 在 Q-02 的 diamond 使用同一正 covariance、
兩個面的同源解及完整事件空間上的 `A_{\{d\}}=A_B`。
canonical 面的 `F_B` 單射、`{d}` 面逆存在，使
`D=G_R(d,a)` 可逆；通道 covariance 可逆的根／通道
off-diagonal 塊迫使 `J_b=J_c=0`。若有面逆不存在，
那個輸入先因 inverse 義務 FAIL，不能把未定義的 `A_C`
當作上述推理的前提。

這個響應結論還可在同一 diamond 上改寫為 K 的 cover block
條件。令 `d_d` 為頂點 d 的 equation diagonal；
由 augmented inverse 與原序 retarded 支撐，`d_d` 和
`D_b=G_R(b,b)`、`D_c=G_R(c,c)` 均可逆。
b 到 d、c 到 d 都是 cover，故沒有嚴格中間事件；block 方程給
`J_b=-d_d^{-1}K(d,b)D_b`、
`J_c=-d_d^{-1}K(d,c)D_c`。
因左右因子可逆，在**每個** L 分別有

`J_b=J_c=0 ⟺ K(d,b)=K(d,c)=0`。

這是從 #120 (N.8) 與同源逆方程的直接代數改寫，
本稿明列推理以供複核；並未把 #120 的嚴格作用域加大。
中間事件的通道在自身事件仍可有非零響應；
其他 P、其他面族或重新登記的資料可能不同。
「Q-02 的資料設計值得重新審查」是方向判斷，**不是**
本稿宣告的一般資料 no-go。

## 3. 尚未決定的四個問題

1. **K₂,₂ 的 L 類。** 讀 L 的 K 能否對每個 L 同時滿足
   #120 (N.2) 的根響應行正交、§7(a) 的非零傳播，以及
   P0.1 §4.4 的固定線性 count 類與所有其他義務，未決。
2. **Green typed 式。** 除 IK.S1 外，能否事前提出
   同源、source-sensitive、可失敗且與 P0.4 §5 相容的式子，
   同時經受鏈與 diamond 的逐對檢驗，未決；不能從
   IK.S1 失敗倒推一條必過的新式。
3. **其他形狀的 innovation。** Q-02 在 diamond 的
   `J_b=J_c=0` 沒有說明其他 P 中新自由度可否
   影響後繼事件，亦未證其不能影響；需有各自的輸入與義務。
4. **單一跨尺寸 K。** K₂,₂ 的正交、所有鏈的每面 unitary
   與 diamond 的守恆／微因果必要式，能否由**同一**事前固定、
   對全部 `D_{KQ}` 與合規 L 適用的 K 同時履行，未決。
   三組局部必要式各自成立不構成存在證明。

原 P 微因果、§7(a)、(b′) 的多軌道逐 L witness、
無界審核族及完整工作域仍保留；#120 只列部分必要式，
並非其餘義務的 PASS。P0.4 未因此封存為全面 FAIL。

## 4. 可選下一步及代價（本稿不替操作者選）

| 可能問題版本 | 需要先承擔與說明的代價 | 本稿處置 |
| :--- | :--- | :--- |
| 重做資料門檻（Q-03） | 事前處理 K₂,₂ 多根共享無通道的缺口，並審查 diamond 上守恆所迫的零響應如何與 innovation 的物理角色相容；新資料須重走自然性、正性、面、容量、原 P 微因果的資料 GO，不能回填 Q-02 的舊結果。 | OPEN；不提出 U、`h_Q`、`j_C` 的新構造，也不保證改資料即能解決。 |
| IK-02：仍用 Q-02，改寫讀 L 的 K 並事前選另一 Green 式 | 須先取得獨立規格 GO，正面處理 K₂,₂ 的逐 L 正交、鏈的全切面 unitary、diamond 的零 cover blocks、Green 識別與 P0.1 §4.4 限制；在看過 IK.S1 FAIL 後換 Green 式，須明說選擇理由以便審查。 | OPEN；不在本稿指定 L 係數、typed 式、witness 或試算。 |
| 重新評估因果序先行與量子過程先行 | 須另外定義可比較的輸入 primitive、局部進出方向、幾何維數、時間箭頭及可檢驗義務；現有局部障礙不足以證明哪條本體路線正確。 | 方向紀錄，未取得轉向 GO。 |

目前停在**整理點**：本稿不啟動 Q-03、IK-02、修約或新研究。
formal／E0、ACT-X-0001、A／B、UNKNOWN、raw／sealed、
producer、seed 與來源隔離不變，Stage 5C 資格不因本稿提升。
作者只整理已合併文件與 Git 身分，並把 #120 的 diamond
等價式展開為一行 block 方程；沒有讀新文獻原文、使用
數值／符號科學程式、RNG、撒點、producer 或 raw／sealed 資料。
文字及三帳仍待另一位 exact-head 複核。
