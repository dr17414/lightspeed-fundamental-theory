# P0.4＋Q-02 下一版 K 的必要條件：K₂,₂、鏈與 diamond 紙上盤點 v0.1

狀態：**【探索／待 exact-head 獨立複核；不是 IK-02 規格或研究 GO】**。
2026-11-18 Asia/Taipei。基線為 #119 squash main
`7884ec87b4f295a118729bbe20a3d7810212683d`，tree
`3c1b975fc3bfa7e080e5b41d7e046f76f6779f59`。
先行三帳 §91 單獨 commit，本文在後。已見 [IK-01 固定研究稿](kq_p04_ik01_paper_study_v0_1.md)
的 FAIL、[#119 限定障礙](kq_p04_k22_order_only_obstruction_paper_v0_1.md)
與 Claude 的方向提示，不稱盲推導。本稿只從已固定的
[P0.4](kq_conditional_internal_innovation_problem_contract_v0_4.md)、
[Q-02](kq_p04_correlated_innovation_data_registration_v0_1.md) 抽出
必要式；凡用 [IK-01 規格](kq_p04_internal_innovation_attempt_spec_v0_1.md)
的特定 Green 式 (IK.S1)，都另標「**若沿用 IK.S1**」。
P0.4 §5 要求事前具名、同源、可失敗的 Green 識別，但**沒有**
把 IK.S1 固定為所有未來 K 必選的唯一式。

## 1. 共同前提與判定層級

固定全域 $D_{KQ}$、每個合規 $L$、二維正 fiber $E_0$；
Q-02 的 $B=M(P)$、合法面 $\mathcal C_Q$、$U$、正配對 $h_Q$、
接合 $j_C$ 一字不改。對每個 $P,L$，設
$T_P=\mathbb C^P\otimes E_0$、$J_P=\mathbb C^{P\setminus B}\otimes E_0$。
由 P0.3 §4 及 P0.4 §1，須有同一原序支撐
$K_{int}:T_P\to J_P$、每個合法面的雙射
$(\gamma_C,K_{int})$ 與逆 $R_C$；同源 $G_R$ 是 canonical
$R_B$ 的固定事件索引識別。令 $F_C=R_Cj_C$，在共同
$h_0$ 正交座標寫

$$A_C(x,y)=F_{C,x}H_Q^{-1}F_{C,y}^{\dagger},\qquad
H_Q=\operatorname{Gram}(h_Q)>0.\tag{N.1}$$

P0.3 §5 的**契約層**要求同一 $T_P$ 上全部合法面
$A_C=A_{C'}$、每個原 $P$ 不可比對全 fiber 的 $A_C(x,y)=0$，
並保留 P0.2 §7(a) 每個完整輸入至少一個非零同源 strict Green
傳播 block。若任一面的逆不存在，該輸入先判未完成，
不以 undefined 的 $A_C$ 延續以下等式。

下表分清必要式的層級；正性與模式 rank 按構造成立，
不能用來抵銷任何 FAIL。

| 輸入 | 契約＋Q-02 必要式 | 若沿用 IK.S1，額外必要式 |
| :--- | :--- | :--- |
| $K_{2,2}$ | (N.2) 兩頂點的根響應行正交，且至少一個非零傳播；#119 排除不讀 $L$ 子類 | 唯一面的 strict $A_B=G_R$ 亦須逐對核對 |
| 鏈 $C_N$ | (N.3) 每個切面的根響應 $g_m$ 可逆且 unitary | (N.4) 所有兩端在內部的 $g_xg_y^\dagger=G_R(x,y)$ |
| diamond | (N.7) 守恆令兩個中間事件到頂點的 source 響應為零；(N.9) 微因果令兩個根到中間點的響應可逆 | (N.10) 連同前兩項即在 $(d,b)$ 上矛盾，屬**沿用 IK.S1 的條件式障礙** |

## 2. $K_{2,2}$：讀 L 是必要但不足的出口

令 $B=\{a_1,a_2\}$、$I=\{c_1,c_2\}$，兩個頂點彼此不可比。
Q-02 §5 事前固定唯一合法面 $B$、$U=\varnothing$、
$Q_P=D_B$ 的 counting 配對。若 canonical 逆存在，兩個頂點
的 diagonal 可逆。對每個 $L$ 分別定
$H_{ij}(L)=G_R(c_i,a_j;L)$。則

$$ A_B(c_1,c_2;L)
 =H_{11}(L)H_{21}(L)^\dagger
  +H_{12}(L)H_{22}(L)^\dagger=0.\tag{N.2}$$

這是原 $P$ 的完整 fiber 微因果，不因 (b′) 在單軌道輸入
記 N/A 而豁免。§7(a) 同時要求至少一個 $H_{ij}(L)\ne0$；
這裡沒有其他 strict comparable pairs。對所有 $L$ 要求兩式，
不能跨 $L$ 相加或只選有利的排序。#119 已證：若完整 K 作為
law 不讀 $L$，自然性使四個 $H_{ij}$ 同為 $H$，
(N.2) 成為 $2HH^\dagger=0$，與 §7(a) 衝突。因此
在**現行 Q-02** 下，下一版若保持契約及希望全域完成，
完整 K 在此輸入必須有實際的 $L$ 區分能力。即使只在此 $P$
的全部 $L$ 上 K 恰好相同，structured 自然性仍將 $L$
與 $f(L)$ 對接，迫使四個 blocks 相同而撞上 (N.2)。
這只是必要條件，**沒有**證 P0.1 §4.4 的固定線性 count 類
能同時使 (N.2) 成立，也沒有構造任何 $H_{ij}$ 或 K。
若要改 Q-02 的共享多根資料，必須重新走資料門檻。

## 3. 鏈 $C_N$：每一切面的 unitary 根響應

令 $C_N=\{1\prec\cdots\prec N\}$、$N\ge3$；唯一 $L$，
Q-02 的 $B=\{1\}$、$U=\varnothing$，每個單點 $C_m=\{m\}$
均合法。canonical 逆若存在，定同源根響應
$g_x=G_R(x,1)$，$g_1=I$。切面 $m$ 的逆存在當且僅當
$g_m$ 可逆；因為零 source 齊次解的所有 root 初值由
$g_x$ 傳播，而同一 $K$ 的 source 部分與 trace 一起是方陣。
Q-02 的 $j_{C_m}$ 只搬運根初值、沒有通道，故

$$F_{C_m,x}=g_xg_m^{-1},\quad
 A_{C_m}(x,y)=g_x(g_m^\dagger g_m)^{-1}g_y^\dagger,\quad
 A_B(x,y)=g_xg_y^\dagger.\tag{N.3}$$

在 $x=y=1$ 代入嚴格守恆 $A_{C_m}=A_B$，
得 $(g_m^\dagger g_m)^{-1}=I$，即每個 $m$ 的
$g_m^\dagger g_m=I$。反過來，在逆存在前提下，
這個 unitary 條件也使 (N.3) 的全部事件對相等；
此等價只針對本鏈的**守恆**，不代替 Green、field 或
(b′)。它是跨全部 $C_N$、全部 $N\ge3$ 的必要式，
不是只避開 IK-01 在 $C_3$ 的那一個失敗面。

**若沿用 IK.S1**，原 P 的 strict Green 識別還要求

$$G_R(x,y)=g_xg_y^\dagger\quad
(1\le y<x\le N),\tag{N.4}$$

其中 $y=1$ 按構造成立；$2\le y<x$ 才是額外的
source-sensitive 檢查。IK-01 在 $(3,2)$ 的失敗
不能推出任何其他 Green typed 式也失敗。鏈是 P0.4
(4.3) 的無界多軌道審核族；任何新版 K 還須獨立通過
(4.2) 對每個 $N,L$ 的兩個 span 條件，不能用
$g_m$ unitary 冒充 sector 非化約。

## 4. diamond：第二面守恆逼出的 source 限制

令 $a\prec b,c\prec d$，$b\parallel c$。Q-02 的
$B=\{a\}$、$I=\{b,c,d\}$、$U=\{b,c\}$，合法面
$C_B=\{a\}$、$C_d=\{d\}$；在 $(a;u_b,u_c)$ 座標

$$H_Q^{-1}=\operatorname{diag}(I,C_\Gamma\otimes I),\qquad
C_\Gamma=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}>0.\tag{N.5}$$

所有下式對**每一個** $L$ 分別成立。先假設 canonical 逆
存在，記 $D_b=G_R(b,b)$、$D_c=G_R(c,c)$，
$B_b=G_R(b,a)$、$B_c=G_R(c,a)$、$D=G_R(d,a)$，
$J_b=G_R(d,b)$、$J_c=G_R(d,c)$。$D_b,D_c$ 是
內部 diagonal 的逆，故可逆。Q-02 的 $j_B$ 給

$$\begin{aligned}
F_B(a)&=(I,0,0),&F_B(b)&=(B_b,D_b,0),\\
F_B(c)&=(B_c,0,D_c),&F_B(d)&=(D,J_b,J_c).
\end{aligned}\tag{N.6}$$

$F_B$ 由前三行可見單射。若 $C_d$ 的 inverse 存在，
則 homogeneous trace $D$ 可逆。定 $Z=D^{-1}$、
$X_b=ZJ_b$、$X_c=ZJ_c$。因 Q-02 在 $C_d$ 仍以
同一 source 注入 $u_b,u_c$，而 $M_{C_d}:D_B\to D_{C_d}$
搬運唯一一個根初值，解同一方程給出

$$F_{C_d}=F_B T,\qquad
T=\begin{pmatrix}
Z&-X_b&-X_c\\0&I&0\\0&0&I
\end{pmatrix}.\tag{N.7}$$

由 (N.1) 與 $F_B$ 單射，完整 $T_P$ 上的守恆
$A_{C_d}=A_B$ **等價於** $T H_Q^{-1}T^\dagger=H_Q^{-1}$。
該矩陣的「根行／通道列」塊必為零，即
$(-X_b,-X_c)(C_\Gamma\otimes I)=0$。因 $C_\Gamma>0$
可逆，得到

$$X_b=X_c=0\quad\Longleftrightarrow\quad
J_b=J_c=0,\qquad Z Z^\dagger=I.\tag{N.8}$$

最後一式來自根對角塊；所以 $D$ 亦 unitary。
這是**P0.4 守恆＋Q-02 資料層**的必要條件，
沒有使用 IK.S1、特定 $t$ 或 $L$ 不依賴。它揭示：
若想在此資料下守恆，$b,c$ 的 innovation 不能再經
source response 傳到 $d$；它們在自身事件的 diagonal
source response 仍可非零，不等於把兩個通道從 CAR 刪除。

canonical 面的原 P 微因果另要求

$$A_B(b,c)=B_bB_c^\dagger-D_bD_c^\dagger=0.\tag{N.9}$$

由 $D_b,D_c$ 可逆，右端乘積可逆，因此 (N.9) 迫使
$B_b,B_c$ 都可逆。這仍是**必要式**，未宣稱存在完整 K。

**若沿用 IK.S1**，在 canonical 面的 $(d,b)$ strict 對
還要 $A_B(d,b)=G_R(d,b)=J_b$。由 (N.5)–(N.6)，

$$A_B(d,b)=D B_b^\dagger+(2J_b-J_c)D_b^\dagger.
\tag{N.10}$$

守恆 (N.8) 令 $J_b=J_c=0$，於是 IK.S1 右端是零，
左端變為 $D B_b^\dagger$，因兩者可逆而**不可能**為零。
所以在 diamond，**P0.4＋Q-02＋完整守恆＋原 P 微因果＋
「沿用 IK.S1」這一組條件相互矛盾**，即使 K 讀 $L$
也無法同時成立。這個條件式結論不等於 P0.4 對任意
Green 識別或任意資料的 no-go；是否能事前提出另一個
符合 P0.4 §5 同源及 source-sensitive 要求的 typed 式，
仍待另行審查，不能因本式失敗而在本稿臨時替換。

## 5. 對下一步的精確影響與未決事項

1. 在 Q-02 原樣資料下，$K_{2,2}$ 必須逐 $L$ 滿足 (N.2)
   且有非零傳播；#119 已排除完整不讀 $L$ 的子類。
2. 鏈的每個合法切面要求 (N.3) 的 unitary 根響應。
   若未來規格沿用 IK.S1，還須履行 (N.4)；跨尺寸
   (4.2) 的 witness 與 §7(c) 另需查，不由本稿保證。
3. diamond 的兩面嚴格守恆要求 (N.8)，微因果要求
   (N.9)。若沿用 IK.S1，(N.10) 給出明確矛盾，
   因此不能在新規格中同時承諾這些條件並期待通過。

本文**沒有**選替代 Green 式、K 的 $L$ 係數、source
重定義、面選擇或資料修改，亦沒有證明所有 P0.4 可允許的
Green 式都與 (N.8)–(N.9) 衝突。這三組必要條件能否在
既有 P0.1 §4.4 固定線性依賴類下由**同一**跨尺寸 K
同時履行，仍未決。若需修改 Q-02、P0.4 或 Green 判準，
須在新版本的資料／契約／規格門檻事前明列；IK-01 和
#119 的各自限定 FAIL 不回填為 PASS。本文待獨立
exact-head 複核，不作正式物理資格或外部同行評審。
