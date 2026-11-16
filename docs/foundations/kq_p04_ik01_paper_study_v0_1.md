# IK-01 v0.1 紙上研究：固定目錄、無界族與原 P 義務

狀態：**【研究稿／待 exact-head 獨立複核；不是研究 GO】**。
2026-11-16 Asia/Taipei。規格基線：#117 squash main
`6f8b4a17b5067ef62b43e15617ec623a489b84f3`，tree
`97b5b67b4471b8c587f42e3052e84ed0a2141121`。
只依已 GO 的 [P0.4](kq_conditional_internal_innovation_problem_contract_v0_4.md)、
[Q-02](kq_p04_correlated_innovation_data_registration_v0_1.md) 及
[IK-01 固定規格](kq_p04_internal_innovation_attempt_spec_v0_1.md) 計算。
先行三帳 §86 單獨 commit；研究在後。未改資料、$t$、判準、面或輸入域。
本稿不使用數值／符號程式、RNG、producer、raw／sealed 或 formal 證據。

## 1. 記號與全目錄的共同判法

記 $I$ 為 $2\times2$ 單位矩陣、$\eta=\eta_0$，$\eta^2=I$、
$\eta$ Hermitian 且非純量；以 $t=1/2$ 為實際候選，$s=2/3$
**只**為固定比較。$D_t(x,y)=I+t[p(x)-p(y)-1]\eta$ 於 $y\prec x$；
$G_t=(I-D_t)^{-1}$。以 $h_0$ 正交座標計，$G_t$ 的所有 block
是 $I,\eta$ 的實係數線性組合，故彼此交換並自伴。全部 $L$
均給**同一** $K_t,G_t,F_C,A_C$；各個 $L$ 的結果可由這個
等式精確共用，但 (4.2) 的逐 $L$ 量詞並未省略。
在鏈上 $p(x)-p(y)-1$ 恰是區間內點數，所以本 law 的
「讀 past cone 而非區間」差別只可能在非鏈輸入顯現；
鏈上的係數結構與舊 IB-01 同型，但固定 $t$ 不同。

每個 $C$ 都使用 Q-02 的唯一配對 $j_C$。若 $T_C$ 可逆，
$F_C=R_Cj_C$；在邊界／通道 counting 座標，$h_Q^{-1}$
是 $I_B\oplus C_\Gamma$，所以完整兩點 block 可以逐對由

$$A_C(x,y)=F_{C,x}(I_B\oplus C_\Gamma)F_{C,y}^{\mathrm H}.
\tag{R.1}$$

下文逐類給出**全部** $F_{C,x}$ 行，故 (R.1) 同時指定全部
事件對、全部 fiber 及全部合法面；再另列指定的判別式。
無通道時省去 $C_\Gamma$。在所有已定義的面，CAR 正性、
rank $=\dim Q$、(IK.S2–S4)、charged Fock 的正性／歸一化
與 Wick 高點均**按構造成立**，不計作物理成功。$j_C$ 的每個
通道由 $R_C$ 的 injectivity 進入 $F_C$，因而可在 CAR 中被檢出；
其同源 $R_J$ 於本目錄的各 $u\in U$ 有對角 source 響應 $I$。
跨面 field/source 僅當要求的共同 $h_Q$-unitary 存在才另判 PASS。

## 2. 先列固定目錄全部結果（含 FAIL）

表中 $q$ 是原 P 的 strict 可比對數；「面」為 Q-02 的 $c_Q$。
Green 指 (IK.S1) 全部 strict pairs／全部面；source-sensitive
欄指兩端在 $I$ 的 strict pair；若無此 pair 標「落空」。
「守」在單面標「無判別力」，絕不記 PASS；「微」逐對在原 P 查。
比較欄的兩個 $t$ 均按同一資料／面，所列有限目錄的面可逆；
$A$ 在 strict 對確有不同且候選有非零 block。全型別合法性
在**全域**的未列 P 上不能由本表推得。

| 固定輸入 | $N,q,k,c_Q;n_{cov},n_{ind};m,\dim Q;|\mathcal O|$ | $I$–$I$ strict | 逆（$t,s$）／守 | 原 P 微／Green | (4.2) 雙 span；§7(a)；比較 | field 接合／rank |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $C_3$ | $3,3,1,3;0,0;0,2;3$ | 有 | 全面可逆／**FAIL** | 空／**FAIL** | PASS；PASS；PASS | **FAIL**／2 |
| $C_4$ | $4,6,1,4;0,0;0,2;6$ | 有 | 全面可逆／**FAIL** | 空／**FAIL** | PASS；PASS；PASS | **FAIL**／2 |
| 向下三葉 star | $4,3,3,1;3,0;0,6;1$ | 無 | 可逆／無判別力 | PASS／PASS（初值欄；內部落空） | N/A；PASS；PASS | 單面／6 |
| 三葉 dual star | $4,3,1,1;0,3;3,8;1$ | 無 | 可逆／無判別力 | PASS／PASS（初值欄；內部落空） | N/A；PASS；此 P 兩 $t$ 相同 | 單面／8 |
| diamond | $4,5,1,2;0,1;2,6;3$ | 有 | 兩面可逆／**FAIL** | **FAIL**（$\{d\}$）／**FAIL** | PASS；PASS；PASS | **FAIL**／6 |
| $K_{2,2}$ | $4,4,2,1;1,1;0,4;1$ | 無 | 可逆／無判別力 | **FAIL**（$c_1\parallel c_2$）／PASS（初值欄；內部落空） | N/A；PASS；PASS | 單面／4 |
| $2\times C_2$ | $4,2,2,4;4,0;0,4;1$ | 無 | 全面可逆／PASS | PASS／PASS（初值欄；內部落空） | N/A；PASS；兩 $t$ 相同 | PASS／4 |
| $3\times C_2$ | $6,3,3,8;12,0;0,6;1$ | 無 | 全面可逆／PASS | PASS／PASS（初值欄；內部落空） | N/A；PASS；兩 $t$ 相同 | PASS／6 |

本表中的「空」表示鏈沒有不可比對；不把空域當微因果的
鑑別證據。最後一欄單面的 field/state 构造按構造成立，
但沒有跨面一致性的判別力。各欄的 FAIL 均獨立保留。

### 2.1 鏈 $C_3,C_4$：全部面和全部 block

標序位置 $1<\cdots<N$，令 $g_j=G_t(j,1)$，$g_1=I$。
Q-02 無 $U$，每個合法面是單點 $C=\{c\}$，
$T_C$ 可逆當且僅當 $g_c$ 可逆；其全部 field 行為
$F_{C,x}=g_xg_c^{-1}$，$A_C(x,y)=g_x(g_c^\dagger g_c)^{-1}g_y^\dagger$。
對 $C_3$，$(g_1,g_2,g_3)=(I,I,2I+t\eta)$；
對 $C_4$，另有 $g_4=4I+4t\eta$。
$t=1/2$ 的 $g_3$ eigenvalues 為 $5/2,3/2$，
$g_4$ 為 $6,2$；$s=2/3$ 的分別是 $8/3,4/3$
與 $20/3,4/3$，所以表中的兩套全部面均可逆。
面 $\{3\}$ 的 $g_3^\dagger g_3\ne I$，故兩條鏈守恆 FAIL；
若需 $C_4$ 的 $\{4\}$ 面，它在本版**可逆**，
不能沿用 IB-01 的舊 undefined。

在 canonical 面，$A_B(3,2)=g_3$，但
$G_t(3,2)=I$，差 $I+t\eta\ne0$；兩端在 $I$ 的
Green 識別 FAIL。其餘非 canonical 面也依上式逐對查，
全稱義務已由 canonical 失敗。候選 $A_B(3,1)=2I+t\eta$
非零且與 $s$ 不同。兩項 span 同對 $(1,2),(1,3)$
為 $-I,-(I+t\eta)$，對唯一 $L$ PASS。

### 2.2 向下三葉 star 與 dual star：全部 block

向下 star 的 minimal 葉為 $a_1,a_2,a_3$，頂點 $b$。
只有 $C=B$、$U=\varnothing$。令 $H_r=I+t(r-1)\eta$；
三葉時 $H_3=I+\eta$。全部 $F_B$ 行是
$F_B(a_j)=e_j$、$F_B(b)=H_3(e_1+e_2+e_3)$。
所以 $A_B(a_i,a_j)=\delta_{ij}I$、
$A_B(b,a_j)=H_3=G_t(b,a_j)$、
$A_B(b,b)=3H_3^2$。三葉的三個不可比葉對為零；
候選與 $s$ 在 strict block 分別為 $I+\eta$、
$I+\tfrac43\eta$，確實不同。只有一個 active 軌道，
(b′) N/A，沒有內部 Green pair。

dual star 為 $a\prec v_1,v_2,v_3$。只有 $C=B=\{a\}$，
$U=\{v_1,v_2,v_3\}$；$D_t(v_i,a)=I$ 與 $t$ 無關。
$F_B(a)=(I,0)$、$F_B(v_i)=(I,e_i)$；
$C_\Gamma=4I_3-\mathbf1\mathbf1^*$。
故 $A_B(a,a)=I$、$A_B(v_i,a)=I=G_t(v_i,a)$、
$A_B(v_i,v_i)=4I$、異葉
$A_B(v_i,v_j)=I+(C_\Gamma)_{ij}I=0$。
三對 Ind 全在**原 P**直接 PASS，$R_J(v_i,v_i)=I$；
span N/A，兩比較對象在本 P 退化為同一 K，不能把這一列
算成 kinetic 鑑別成功。

### 2.3 $K_{2,2}$：多根共享的 FAIL

$B=\{a_1,a_2\}$、$I=\{c_1,c_2\}$，$U=\varnothing$、
唯一 $C=B$。每個根到頂點的 strict block 是
$H=I+t\eta$；$F_B(a_j)=e_j$、
$F_B(c_i)=H(e_1+e_2)$，兩個頂點行完全相同。
因此全部 block 由 (R.1) 定，特別是

$$A_B(c_1,c_2)=2H^2=	frac52I+2\eta\ne0
\quad(t=1/2).\tag{R.2}$$

兩個 eigenvalues 是 $9/2,1/2$，故 full-fiber
微因果直接 **FAIL**；這對在 Q-02 是 $n_{ind}=1$，
不能因無共同面或 (b′) N/A 略去。所有 strict 初值欄
$A_B(c_i,a_j)=H=G_t(c_i,a_j)$，Green 識別 PASS，
§7(a) 非零傳播 PASS。比較 $s$ 時 strict $H$ 改變，
而本 P 單面且無通道，field/state 形式構造不能抵銷 (R.2)。

### 2.4 diamond：兩個面均計，不能只報 canonical

$B=\{a\}$、$I=\{b,c,d\}$，$U=\{b,c\}$，
$C_\Gamma=\begin{psmallmatrix}2&-1\\-1&2\end{psmallmatrix}$。
令 $H=I+t\eta$、$g=3I+4t\eta=G_t(d,a)$；
$G_t(d,b)=G_t(d,c)=H$。canonical 面 $B$ 的全部行是

$$F_B(a)=(I,0,0),\quad F_B(b)=(I,I,0),\quad
F_B(c)=(I,0,I),\quad F_B(d)=(g,H,H).\tag{R.3}$$

這使 $A_B(b,c)=I-I=0$，但
$A_B(d,b)=g+H=4I+5t\eta$，與 $G_t(d,b)=H$
相差 $g\ne0$，故 canonical 面的內部 strict Green **FAIL**。
另一合法面 $C=\{d\}$ 必須計。兩個 $t$ 上 $g$ 可逆：
$t=1/2$ eigenvalues $5,1$，$s=2/3$ 為 $17/3,1/3$。
記 $Z=g^{-1}$、$X=ZH$。從 $\psi_d=b_0$ 和
$K\psi=u$ 解得 canonical 初值 $a=Z(b_0-Hu_b-Hu_c)$，
故全部非 canonical 行為

$$\begin{aligned}
F_{\{d\}}(a)&=(Z,-X,-X),\\
F_{\{d\}}(b)&=(Z,I-X,-X),\\
F_{\{d\}}(c)&=(Z,-X,I-X),\\
F_{\{d\}}(d)&=(I,0,0).
\end{aligned}\tag{R.4}$$

代入 $t=1/2$：$Z=(3I-2\eta)/5$、
$X=(4I-\eta)/10$；(R.1) 給

$$A_{\{d\}}(b,c)=Z^2-I-2X+2X^2
=-\frac{47I+22\eta}{50}\ne0,\tag{R.5}$$

兩 eigenvalues 為 $-69/50,-25/50$。因此原 P 的
$b\parallel c$ 在 canonical 面 PASS、在 $\{d\}$ 面 **FAIL**。
又 $A_{\{d\}}(a,a)=Z^2+2X^2=(43I-32\eta)/50\ne I=A_B(a,a)$，
守恆 **FAIL**。非 canonical 面的 strict
$A_{\{d\}}(d,b)=Z\ne H=G_t(d,b)$，Green **FAIL**。
兩種 $L$ 共用上述全部 block；(4.2) 同一 witness
$(a,b),(b,d)$ 的 blocks $-I,-(I+t\eta)$，兩項 PASS；
比較對象在 $A_B(d,a)=g$ 和 $A_{\{d\}}(d,b)=Z$ 均與候選不同。

### 2.5 $2\times C_2$、$3\times C_2$：全部面

第 $i$ 分量 $a_i\prec b_i$，$d_P(b_i,a_i)=0$，
故 $D_t(b_i,a_i)=I$，$G_t$ 是各分量的兩點逆。
$U=\varnothing$，每個合法面各分量選 $a_i$ 或 $b_i$；
Q-02 唯一配對將該根資料搬到所選面。任一面、任一 $t$，
**相同的** $F_C(a_i)=F_C(b_i)=e_i$；全部跨分量
$A_C=0$，同分量四個 $A_C$ blocks 為 $I$。
所有 $2^k$ 面可逆、$A_C$ 完全相同，故守恆、原 P
微因果、strict Green、unitary field 接合（$U_{CB}=I_Q$）
均 PASS。$\dim Q=2k=\operatorname{rank}A$ 隨 $k$ 無界，
但兩個 $t$ 在此族完全同 law，不能把它當 kinetic 鑑別族。

## 3. 跨尺寸族：解析判定與全稱量詞

| 事前族 | $q,k,c_Q;n_{cov},n_{ind};m,\dim Q;|\mathcal O|$ | 全尺寸結果 |
| :--- | :--- | :--- |
| $C_N$，$N\ge3$ | ${N\choose2},1,N;0,0;0,2;{N\choose2}$ | 所有面兩 $t$ 可逆；(4.2)、§7(a)、§7(c) PASS；守恆、內部 Green、跨面 field **FAIL**；微因果空域，rank 2；strict 比較有別 |
| dual star $P_r$，$r\ge2$ | $r,1,1;0,{r\choose2};r,2(r+1);1$ | 唯一面，所有葉對微因果及 strict Green PASS，§7(a) PASS、(b′) N/A；守恆無判別力，rank $2(r+1)$；兩 $t$ 同 law |
| 向下 $r$ 葉 star，$r\ge2$ | $r,r,1;{r\choose2},0;0,2r;1$ | 唯一面，葉對微因果及 strict Green PASS，§7(a) PASS、(b′) N/A；守恆無判別力，rank $2r$；兩 $t$ strict 比較有別 |
| $k\times C_2$，$k\ge2$ | $k,k,2^k;2k(k-1),0;0,2k;1$ | 全部面可逆，守恆、微因果、Green、field 接合 PASS；§7(a) PASS、(b′) N/A；rank $2k$，兩 $t$ 同 law |

對鏈的「全部面可逆」不是從小尺寸外推。令 $g_m$ 是
鏈中距離 $m$ 的 $G_t$ block，$g_0=I,g_1=I$、
$g_2=2I+t\eta$；$m\ge3$ 滿足

$$g_m=3g_{m-1}-(2I-t\eta)g_{m-2}.\tag{R.6}$$

$\eta=+1$ 分量的每個 path 權重為正，故 $g_m^+>0$。
$\eta=-1$ 分量於 $t=1/2$，令 $h_m=2^{m-1}g_m^-$，
$h_1=1,h_2=3$、$h_m=6h_{m-1}-10h_{m-2}$，
故 $h_m\equiv3\pmod5$ 對 $m\ge2$，從不為零。
於 $s=2/3$，令 $h_m=3^{m-1}g_m^-$，
$h_1=1,h_2=4$、$h_m=9h_{m-1}-24h_{m-2}$，
故 $h_m\equiv4\pmod8$ 對 $m\ge2$，也從不為零。
每個鏈面的 $g_c$ 都可逆。任意 $N\ge3$ 包含面 $\{3\}$，
$g_3^\dagger g_3\ne I$ 已使守恆 FAIL；canonical
$(3,2)$ 的差 $I+t\eta\ne0$ 已使 Green FAIL。
不論 $N$ 多大，鏈的 $(1,2),(1,3)$ 仍是 (4.2)
雙 span witness；候選有任意長 Hasse hop 的非零 block。

在 dual star $P_r$，$C_\Gamma=(r+1)I_r-\mathbf1\mathbf1^*$，
$F_B(v_i)=(I,e_i)$，故異葉 $I- I=0$，對所有 $r$
成立，rank $=2(r+1)$。向下 star 的
$F_B(b)=H_r\sum e_j$，葉對為 $0$，strict 為
$H_r=I+t(r-1)\eta\ne0$；$s$ 取代 $t$ 時對 $r\ge2$
確有不同。$k\times C_2$ 的全部面、rank 和等式
已在 §2.5 逐分量證明，沒有用未觀測 K 輸出選族。

§7(a) 其實對本固定 $K$ 的**全部** $D_{KQ}$ 都 PASS：
在非空非全 minimal past-set $B$ 後，取 $I$ 的一個
minimal 事件 $x$，其至少一個 predecessor $b\in B$
必是 cover；$G_t(x,b)=D_t(x,b)$，而
$I+t d_P(x,b)\eta\ne0$（$I,\eta$ 線性獨立）。
此論證沒有把源的裸 block 或 diagonal 算成傳播。

## 4. (4.2) 的全域作用與結論

對本固定 law，任兩 active blocks 為
$-[I+t d_1\eta]$、$-[I+t d_2\eta]$。因 $t\ne0$
及 $\eta$ 非純量，兩個 complex span 為 2 **當且僅當**
$d_1\ne d_2$；$K^{ord}$ 與完整 $K$ 的 active blocks
相同。這是每個 $L$ 都能用原 P 計數判定的精確條件，
不把鏈上的 witness 偷換成全域 PASS。固定目錄的鏈、
diamond 已有兩個不同 $d$；其餘列只有一條 active 軌道，
按 P0.4 記 N/A 而不是 PASS。

在**先列完上述固定目錄及無界族結果之後**，全域判斷是：
IK-01 v0.1 **FAIL**。$K_{2,2}$ 在唯一面違反原 P
全 fiber 微因果；$C_3,C_4$ 和全部 $C_N$ 違反守恆與
內部 Green；diamond 的第二面另違反微因果、守恆與 Green。
因此即使 (4.2)、§7(a) 及部分無界 rank 義務成立，
也不能相抵。這是固定資料 Q-02＋固定 IK-01 law 的
失敗，不宣稱 P0.4 全面 no-go、Q-02 任意 K 都不行，
也不改 #108、IB-01、#111 的各自作用域。

本稿沒有把全 $D_{KQ}$ 的每個非目錄 P／C 的可逆性、
守恆或 (4.2) 逐一列值；它們不是 PASS。若日後另證
更廣的障礙，須另立作用域與審核。此版封存 FAIL，
不得在同一版調 $t$、重做 Q-02、改 (4.2) 或刪輸入。
本次是兩個 AI 協作角色待完成的文件複核流程，
不是外部同行評審；formal／E0 等來源隔離不變。
