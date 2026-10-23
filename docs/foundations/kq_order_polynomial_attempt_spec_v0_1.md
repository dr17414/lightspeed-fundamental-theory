# X-KQ-OP-01 — 首次order-polynomial試作的固定規則

狀態：**【探索／試作規則；不是成功構造】**。
Problem ID `X-KQ-1P1-P0.1`；Attempt ID `X-KQ-OP-01`。
**探索軌，不具 §5.2.1(v) 依據資格。**

## 1. 生效來源、順序與範圍

依[已合併契約](kq_1p1_construction_problem_contract_v0_1.md)，工作域保持整個
D_KQ，不縮成子類。#95 main3387d732及#97 main1ac30ceb的核准tree已核對。
第一個紀錄commit `eeb5ea6d1e46cb227890a5aa1ff6dd43fe01c3db` 已收EXP-0089／0090，
並以0091披露本輪內部紙上預想；本規則不是盲預註冊，不否認先有零對角與對稱性風險的提示。
本檔在後續研究稿之前獨立commit固定；後續不改本版本來修補失敗。
ACT-X-0001仍引用生效SHA `0c386716701589c9a6b0b799636a808aacb9ade5`，限紙上。

| 六欄 | 固定內容 |
| :--- | :--- |
| 問題 | 一個不依realizer代表的order-count多項式，能否完成契約§4的同源鏈？ |
| 定義域 | 每一個P∈D_KQ；不宣稱全體posets有two-order表示 |
| 輸入 | strict order、事件count、下述L2自由線性化與anonymous two-slot bookkeeping |
| 證據 | 後續只交紙上公式、自然性、inverse、非平凡性及固定CAR試作的證明／障礙 |
| 未證橋接 | 實際I-UV的two-set來源、物理spinor／Dirac／massless、量子與連續極限均未證 |
| 否定／停止 | 任一必需項失敗就不報完成；不改pairing、取正部分、縮域或另加physical primitive救此試作 |

## 2. 來源、容量與全部自由選擇

L0：P的strict order。L1：有限count與函數空間的集合索引。
L2：給定複數域C、free complex linearization、anonymous two-element set S、
其交換J、下述counting Hermitian pairing與*／CAR prescription。
這些是明示的數學scaffolding，不是從order推得complex quantum mechanics；
S也不是已由唯一realizer orbit導出的實際兩個orders。I-UV的代表不被選取或輸入。
L3：本次選擇唯一一條固定的K及CAR試作規則；係數與多項式次數如下，無可調參數，
無per-event／per-pair自由表、逐N擬合、coordinates、密度或physical scale。
J不是gamma矩陣、chirality、物理frame或transport；I的contact不是物理質量的主張。
本試作不使用任何evaluator、planted／probe／run1輸出或未知私人材料選公式。
既有公開T3與T6提供型別與必要界提示；不作§5.2.1(v)合資格輸入。

## 3. 固定K、domain與isomorphism作用

令H_P=C^P⊗C[S]，Z_P(x,y)=1若y≺x，否則0。Z²指ordinary composition，
所以Z²(x,y)計數y≺z≺x的事件z；它不是額外選出的nearest-neighbour資料。
I_P與I_S為identity，J交換S的兩元素。固定

$$B_P=Z_P\otimes I_S+Z_P^2\otimes J,\qquad
K_P=I_{H_P}+B_P.\tag{OP.1}$$

所有P及N均使用同一公式。定義與source domain都為完整H_P，無邊界條件、
選取子空間、anchor、boundary vector或新增physical時間方向。
f:P→P′誘導U_f e_x=e_{f(x)}，sector部分為id；sector重新枚舉由同一J作用。
任意實際two-set的bijection誘導相同free linearization／swap識別。
自然性與代表不依賴須在後續證明；不把未使用I-UV當作已交出其物理sector來源。

G_R只按同一K在完整H_P的two-sided inverse定義；存在性及retarded支撐須證。
K與inverse都沿order的聲稱不能只靠選了linear extension作座標便當作證明。

## 4. 在form檢查前固定test／adjoint／CAR橋接

完整test space固定T_P=H_P，counting pairing
⟨f,g⟩₀=Σ_{x,s}overline{f(x,s)}g(x,s)，第一槽反線性。
固定ordinary conjugate transpose †作adjoint，G_A=G_R†。
這是有限自由線性化的數學pairing；不稱它是Lorentz metric、Cauchy面或已導出的fermion adjoint。

待inverse存在後，固定本試作的CAR prescription為

$$A_P(f,g)=\langle f,i(G_R-G_A)g\rangle_0.\tag{OP.2}$$

具體是以複線性符號a(f)生成unital *-algebra，施加
{a(f)*,a(g)}=A_P(f,g)1及{a(f),a(g)}=0。此處是明文選定的試作關係，
不是僅憑Green便唯一推得物理CAR；若它不允許正state，整個此橋接分支失敗。
未先給無關的W或另選「好」的矩陣作總form。

不選projection／test restriction／quotient，不做譜截斷或刪負模。
不依A的符號更改†、pairing、contact、normalization、source或K。
若A不正，不定義H_A為正Hilbert空間，也不做零radical商來掩蓋負方向。
state尚未選定：先判斷任何正歸一化state是否可能；generic Fock存在性不算來源機制。
即使A正，仍須另交同源state規則才算實質第4項；本規則未承諾用S=0完成它。

## 5. 固定比較類G_swap（只作限定障礙）

後續若分析不只(OP.1)，只及以下明定類：
每個P有相同global複二維slot空間E_P及自然的J_P，J_P²=I，
dim ker(J_P−I)=dim ker(J_P+I)=1；各事件使用同一E_P及同一識別。
每個isomorphism f有單一global V_f:E_P→E_P′，可逆且
V_f J_P=J_P′ V_f，V_{gf}=V_g V_f，V_id=I。
K的非對角support沿strict order，且

$$K_{P′}(f(x),f(y))=V_fK_P(x,y)V_f^{-1}.\tag{OP.3}$$

允許任意來源合規的K公式及全部diagonal blocks，不限定為多項式；V_f可為GL(2,C)，
不只置換。這些是假設，不由「orbit唯一」自動推出。
不包括per-event fibers／識別、projective composition、非全域sector transport，
或不保留此natural swap的其他二維表示。若要談那些路徑，須另交來源與契約適用性，
不能將本類障礙稱為所有可能K／spinor／quantum構造的no-go。

## 6. 審查與執行界線

後續逐項核對契約§4.1(a)–(d)、同一K的inverse及(OP.2)，保留失敗。
不以有限反例宣稱typicality，不改工作域。鏈若出現，只作原工作域內的解析witness，
不另宣告「鏈子類已完成主問題」。全程不執行模型／symbolic／toy程式、RNG或producer。
若需physical primitive或改輸入，停止原分支另立契約；本規則不預先授權該分支。
