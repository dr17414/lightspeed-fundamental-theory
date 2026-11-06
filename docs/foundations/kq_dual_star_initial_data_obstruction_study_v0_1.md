# P0.2／B-01 dual star 初值容量障礙：限定紙上證明 v0.1

狀態：**【探索／待 exact-head 獨立逐式複核】**。2026-11-06 Asia/Taipei。
Problem ID `X-KQ-COND-TA-P0.2`；資料規則 `B-01 v0.1`。
本稿證明的是已固定資料與容許依賴類下的**條件式不相容命題**，不是另一個K試作，
不修改已封存的IB-01，也不宣稱整條因果序先行路線不可能。
論證起點是Claude在#106合併後提出、於接觸帳§62 EXP-0132逐字登記的腦中提示；
作者已在先行三帳commit的EXP-0135披露相關閱讀與事前思考，**不稱盲發現**。
本文在該提示之上明列前提、補齊型別及兩個缺口：輸入域身分、augmented Green的全部off-diagonal。

## 1. 命題與每項前提的來源

令 $P_r=\{a,v_1,\ldots,v_r\}$ 為dual star，只有 $a\prec v_j$（$r\ge3$），
各葉子兩兩不可比；下標僅供證明，實際輸入沒有葉子標籤。
每個合法線性延伸 $L$ 都把 $a$ 放在第一位，以下按其葉子先後將葉子記為
$v_1,\ldots,v_r$。需同時滿足下表全部前提的規則才在本命題量詞內。

| 前提 | 已固定來源 | 本證明的用途 |
| :--- | :--- | :--- |
| $P\in D_{KQ}=\{P\in D_1:q(P)\ge2\}$；主問題對每個合法輸入與L量化 | [P0.1 §2](kq_1p1_construction_problem_contract_v0_1.md) | §2證明dual star沒有被工作域排除 |
| 初值面 $B_0=M(P)$、內部 $I=P\setminus B_0$、$D_C=\mathbb C^C\otimes E_0$，固定正配對 $h_C$ | [B-01 §2](kq_conditional_boundary_beta_registration_v0_1.md)、[P0.2 §3](kq_conditional_initial_data_problem_contract_v0_2.md) | $B_0=\{a\}$，初值容量為2；葉子彼此沒有初值copy |
| $K_{int}:T_P\to J_P$ 的非order非對角block為0，diagonal不讀L；$\gamma_B|_{Sol_K}$及 $(\gamma_B,K_{int})$須為同構 | [P0.2 §4](kq_conditional_initial_data_problem_contract_v0_2.md) | 每葉只有自己的diagonal與從a來的block；奇異diagonal先判型別FAIL |
| strict order block的L入口只能是固定 $n_{\tau\sigma}M_{\tau\sigma}$ 線性和；$K^{ord}$不讀L且對原P同構自然 | [P0.1 §4.4–4.5](kq_conditional_time_adjoint_problem_contract_v0_1.md)、P0.2 §4繼承 | 葉子的初值響應隨L位置呈仿射矩陣列 |
| $S_C=E_C^\dagger$，$A_C(f,g)=h_C(S_Cf,S_Cg)$，$h_C$正定 | [P0.2 §3、§5](kq_conditional_initial_data_problem_contract_v0_2.md) | 原P上葉對的CAR block是兩個初值響應矩陣的乘積 |
| 原P不可比事件的全部point-supported fiber block須為0 | [P0.2 §6.2](kq_conditional_initial_data_problem_contract_v0_2.md) | 葉子響應的row spaces兩兩正交 |
| 每個輸入的同源 $G_R$ 至少有一個非對角原P傳播block | [P0.2 §4、§7(a)](kq_conditional_initial_data_problem_contract_v0_2.md) | 全部葉響應為0即FAIL |

本文主命題使用原契約的 $n=\dim_{\mathbb C}E_0=2$。§6另給**條件式**固定
有限 $n$ 的同一引理；那不是擅自把P0.2的fiber改大。
沒有用IB-01的七格係數、特定adjoint的Green和式、作用量、state或任何數值樣本。

**主命題。** 對任意 $r\ge3$ 和任意合法 $L$，在上述既定規則類中，
不存在一個 $K_{int}$ 可在 $P_r$ 同時通過 P0.2 §4 的初值／source型別、
§5–6.2的固定Gram微因果性與§7(a)的非零傳播。因 $P_r\in D_{KQ}$，
固定B-01時P0.2在**整個** $D_{KQ}$ 上的正面完成因而不可能。
若候選的§4型別先失敗，本命題同樣判整體未完成；不假裝還有可定義的CAR供測試。

## 2. dual star 的域身分與B-01資料

兩個total orders的交集要恰為 $P_r$，則a必在兩者均先於全部葉子；
對每對葉子 $v_i\parallel v_j$，兩個orders中的相對方向必相反。
故一個realizer完全由第一個total order的葉排列決定，第二個恰是其逆序。
$\operatorname{Aut}(P_r)\cong S_r$ 可傳遞地置換所有這些排列；
$R_2(P_r)/(\operatorname{Aut}(P_r)\times S_2)$只有一個orbit，$P_r\in D_1$。
又 $q(P_r)=r\ge3\ge2$，故 $P_r\in D_{KQ}$。此證明對每個r成立，
不依K的輸出或挑選某個L。

B-01給 $B_0=\{a\}$、$I=\{v_1,\ldots,v_r\}$，初值空間
$D_B\cong E_0$ 且 $d_B=2$。極大鏈恰為每條 $\{a,v_j\}$；
大小為1且與**每條**極大鏈恰交一次的合法面只有 $C=\{a\}$。
因此守恆面比較在此P沒有判別力；所有 $\binom r2$ 個葉對均是原P不可比對，
仍須在唯一合法面上直接檢查微因果。這不是以面覆蓋的推論代替檢查。

## 3. 初值型別強迫共同可逆diagonal與仿射響應

記 $V=E_0$，$n=\dim V=2$。每葉的內部方程只可寫為

$$
 (K_{int}\psi)(v_j)=d\,\psi(v_j)+Q_j\,\psi(a).
$$

因沒有葉子之間的order，非order非對角block必為0。diagonal不讀L，
且原P的葉子在order automorphism下可遞，故所有葉子共用同一矩陣
$d=d(P_r,R_0)$；它可依整個P與R₀而變，不被假設為scalar或IB-01的I。
若 $d$ 有非零kernel，取 $\psi(a)=0$，只在其中一葉放非零 $w\in\ker d$，
便有 $K_{int}\psi=0$ 而 $\gamma_B\psi=0$。這違反
$\gamma_B|_{Sol_K}$ 的injectivity及augmented $(\gamma_B,K_{int})$同構。
因此任何聲稱通過§4的候選必有可逆d。

固定這樣的候選與L。令 $E_B:D_B\to Sol_K$ 是 $\gamma_B$ 的逆，
$U_j=\pi_{v_j}E_B\in\operatorname{End}(V)$。上式逐葉解得

$$
 U_j=-d^{-1}Q_j.
$$

對 $(a,v_j)$，其他 $r-1$ 片葉z均在閉區間外，且
$\tau_P(z;a,v_j)=(\succ,\parallel)$。在L中先於 $v_j$ 的 $j-1$ 片
屬between，晚於它的 $r-j$ 片屬post；pre格為0。由P0.1 §4.4，
$K^{ord}$在葉子自同構下有相同block $X_r$，而固定係數記為$Y_b,Y_p$，故

$$
 Q_j=X_r+(j-1)Y_b+(r-j)Y_p.
$$

即使 $X_r$與d依P_r而變，固定r的整列仍是

$$
 U_j=U+(j-1)V_1,\qquad
 U=-d^{-1}\bigl(X_r+(r-1)Y_p\bigr),\quad
 V_1=-d^{-1}(Y_b-Y_p).
$$

這裡的 $V_1$ 是矩陣斜率，不是fiber V。證明只用**L位置的仿射性**；
不以共同換基、sector或係數值挑選某個有利L。上述推理對每個L的葉序重作皆成立。

## 4. 正Gram微因果的有限維引理

固定B₀面，$E_B$在a的block為I，在葉子為$U_j$。
P0.2固定正配對與 $S_B=E_B^\dagger$ 給出

$$
 A_B(v_i,v_j)=U_iU_j^\dagger\quad(i\ne j)
$$

作為完整fiber的point-supported CAR block；等式在共同h₀正交基底中表述。
P0.2 §6.2對原P葉子的兩兩不可比要求 $U_iU_j^\dagger=0$。
這意味 $U_j$ 的row spaces在n維正定Hermitian空間中兩兩正交。
非零矩陣有非零row space，所以最多n個 $U_j$ 可以非零。

**仿射正交引理。** 若 $U_j=U+(j-1)V_1$（$j=1,\ldots,r$），
$r\ge\max(3,n+1)$，且 $U_iU_j^\dagger=0$ 對所有 $i\ne j$，
則 $U_j=0$ 對所有j。

**證明。** 因r>n，至少有一個 $j_0$ 滿足 $U_{j_0}=0$。
因r≥3，另取兩個不同位置 $p,q\ne j_0$。仿射式使
$U_p=(p-j_0)V_1$、$U_q=(q-j_0)V_1$。兩數係數非零，微因果式給
$(p-j_0)(q-j_0)V_1V_1^\dagger=0$，即 $V_1V_1^\dagger=0$。
正定h₀下 $V_1V_1^\dagger=0\Rightarrow V_1=0$；再由
$U_{j_0}=0$ 得U=0。∎

原P0.2的n=2、r≥3滿足引理；故若§4型別及§6.2微因果成立，
所有從a到葉子的初值響應 $U_j$ 均須為0。這一步比「不能讓每片葉子都有響應」
更強：契約§7(a)只需**至少一個**非零off-diagonal，故仍須檢查source response。

## 5. augmented Green的全部非對角block與§7(a)矛盾

P0.2 §4將 $(\gamma_B,K_{int})^{-1}$ 依 $D_B\oplus J_P\cong T_P$ 識別為
同源完整響應 $G_R$。在B與葉子的block順序中，上述方程的精確矩陣是

$$
 (\gamma_B,K_{int})=
 \begin{pmatrix}I&0\\ Q&I_r\otimes d\end{pmatrix},\qquad
 G_R=
 \begin{pmatrix}I&0\\ U_{\rm leaves}&I_r\otimes d^{-1}\end{pmatrix},
 \qquad U_{\rm leaves}=\begin{pmatrix}U_1\\\vdots\\U_r\end{pmatrix}.
$$

所以 $G_R(v_j,a)=U_j$；source到本葉的 $d^{-1}$ 只在事件對角，
不同葉間的source response為0，葉到a也為0。**沒有別的非對角block**可替代
全部為0的 $U_j$。引理因而迫使G_R所有off-diagonal blocks為0，
直接違反P0.2 §7(a)在**每個輸入**至少有一個原P非零傳播block的要求。
這也說明不能把非零diagonal contact、任意另指定Green或只靠source-to-self
稱作通過傳播。若d原本奇異則§4已FAIL；若d可逆且微因果成立則§7(a)FAIL。
因此主命題成立，且對該P的**所有L**與所有允許K係數成立。∎

## 6. 量詞、一般化與未涵蓋的出口

對固定P0.2的n=2，任取一個r≥3的dual star即足以反駁「同一規則在全
$D_{KQ}$每個輸入完成」；證明實際涵蓋全部r≥3。若另案把fiber改為某個
**跨輸入固定的有限n**而保留同一B、正Gram、微因果、§4與§7(a)型別，
引理於 $r\ge\max(3,n+1)$ 照樣給出矛盾。這是條件式推廣，**不是**
P0.2已容許改fiber或物理自由度的結論；若n隨r增加，本文不排除。

本證明沒有要求每片葉子都有非零響應，沒有用守恆（dual star只有一面）、
IB.S2–4、IB-01特定係數、state來源或§7(b)／(c)；它只在既定前提的聯合下
排除完整正面完成。B-01的集合／容量登記本身仍正確，失敗是它與上述下游義務
同時施加於整個D_KQ的不相容；換β、放寬L依賴、改Gram／微因果或改§7(a)
都超出本文，若要嘗試須依各自契約另案修訂，不能事後救回本版。

**程序結論：** 這是待獨立exact-head逐式複核的紙上限定障礙。
在GO之前，P0.2＋B-01不得被狀態文件標為已證no-go，也不以此直接設計替代規則；
IB-01仍是已封存的固定版FAIL，原始輸入／formal／E0及全部來源隔離不變。
本稿沒有新科學程式、數值／符號執行、RNG／撒點、producer、raw／sealed、seed、
外部文獻檢索或主機量測；既有repo檢查不算本數學證明的獨立驗證。
