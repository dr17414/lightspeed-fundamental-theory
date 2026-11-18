# P0.4／Q-02 的 K₂,₂ 不讀 L 障礙：限定紙上證明 v0.1

狀態：**【探索／待 exact-head 獨立逐式複核；不是新 K 規格或研究 GO】**。
2026-11-17 Asia/Taipei。基線為 #118 squash main
`0fda7d366161ea541d43b58e2836ef092606bce8`，tree
`9437cfe02c5b6722d0c58134f3acc2611d47e9f6`。
先行三帳 §89 單獨 commit，然後才撰寫本稿。Claude 於 #118 複核後提出
尚未證明的提示（EXP-0188），並於合併後限定不讀 $L$ 的範圍
（EXP-0191）；本文不稱盲發現，也不回填 IK-01 的結果。

## 1. 命題、前提及來源

令 $P=K_{2,2}$，底層為 $a_1,a_2$，頂層為 $c_1,c_2$，
且四個 $a_j\prec c_i$，同層元素各自不可比。每個 $L\in LE(P)$
都在量詞內；標籤只供證明，不是資料的新輸入。

| 前提 | 已固定的來源 | 用途 |
| :--- | :--- | :--- |
| $D_{KQ}=\{P\in D_1:q(P)\ge2\}$，全部合規 $L$ 同時受檢 | [1+1 構造契約 P0.1 §2](kq_1p1_construction_problem_contract_v0_1.md)、[P0.4 §1](kq_conditional_internal_innovation_problem_contract_v0_4.md) | §2 核對這個 $P$ 在域內 |
| 固定 $B,I,\mathcal C_Q,U,Q_P,h_Q,j_C$ | [Q-02 §§2–4、§5 目錄](kq_p04_correlated_innovation_data_registration_v0_1.md) | §2–3 算唯一面的 CAR，不能改資料 |
| $K_{int}:T_P\to J_P$ 只在 $I$ 施方程，非 order 非對角 block 為零，diagonal 不讀 $L$；$R_B=(\gamma_B,K_{int})^{-1}$ 須存在 | [P0.2 §4](kq_conditional_initial_data_problem_contract_v0_2.md)、[P0.3 §4](kq_conditional_internal_innovation_problem_contract_v0_3.md)、[P0.4 §1](kq_conditional_internal_innovation_problem_contract_v0_4.md) | §3 的方程、可逆性及同源 $G_R$ |
| $K^{ord}$ 不讀 $L$ 且對原序自同構自然；**本命題再限制完整 $K$ 作為 law 不讀 $L$**，即其 block 對每個 $P$ 的所有 $L$ 相同；全部 $M_{\tau\sigma}=0$ 是充分而非必要的實現 | [時間序契約 P0.1 §§4.1、4.4](kq_conditional_time_adjoint_problem_contract_v0_1.md)、[P0.4 §3 單軌道引理](kq_conditional_internal_innovation_problem_contract_v0_4.md) | §3 四個 strict blocks 相同；不把引理套用到讀 $L$ 的完整 $K$ |
| $F_C=R_Cj_C$、$S_C=F_C^\dagger$，$A_C$ 是同一 $Q_P,h_Q$ 的正 Gram；原 $P$ 不可比點的全 fiber block 須為零 | [P0.3 §§4–5](kq_conditional_internal_innovation_problem_contract_v0_3.md)、[P0.2 §6.2](kq_conditional_initial_data_problem_contract_v0_2.md)、[P0.4 §1](kq_conditional_internal_innovation_problem_contract_v0_4.md) | §4 在 $c_1\parallel c_2$ 直接檢查 |
| 每個完整輸入的同源 $G_R$ 至少有一個沿原 $P$ strict order 的非零 off-diagonal 傳播 block | [P0.2 §7(a)](kq_conditional_initial_data_problem_contract_v0_2.md)、[P0.4 §1](kq_conditional_internal_innovation_problem_contract_v0_4.md) | §4 排除 $H=0$ |

**限定命題。** 在這些前提及 Q-02 的原樣資料下，任意對
$L$ 完全不依賴的合規 $K$，都無法在 $K_{2,2}$ 上同時滿足
augmented source／初值同構、原 $P$ 微因果及 §7(a) 非零傳播。
因此此**不讀 $L$ 子類**不能全域完成 P0.4＋Q-02。
這不是 P0.4 對任意 $K$、Q-02 對讀 $L$ 的 $K$，或因果序路線的 no-go。

## 2. 域身分與 Q-02 資料

任何兩條線性延伸的交集若恰是 $P$，每條延伸必把兩個 $a$
排在兩個 $c$ 之前；要使同層兩元素仍不可比，兩條延伸在
$a_1,a_2$ 上的先後必相反，在 $c_1,c_2$ 上也必相反。
第一條延伸的兩個層內順序各有兩種選擇，第二條即逐層反序，
所以共有四個標號 realizer。$\operatorname{Aut}(P)=S_2\times S_2$
能傳遞地交換這四個選擇，故只有一個 realizer 軌道，$P\in D_1$；
$q(P)=4\ge2$，所以 $P\in D_{KQ}$。這不取決於 $L$ 或 $K$。

Q-02 §2 給 $B=\{a_1,a_2\}$、$I=\{c_1,c_2\}$。
兩條極大鏈的所有四種 $a_j\prec c_i$ 要由大小 $|B|=2$ 的
反鏈各交一次；候選只有 $B$ 與 $\{c_1,c_2\}$。
後者的二部圖為 $K_{2,2}$，有兩個完美配對，被唯一配對
predicate 刪去；故唯一合法面為 $C=B$，而**原輸入 $P$ 不刪**。
對兩個 $c_i$，$R(c_i)=B$、$|R(c_i)|=2$，Q-02 §3 的
$U(P)=\varnothing$。因此

$$Q_P=D_B\cong E_0\oplus E_0,\qquad
  h_Q=h_B=\text{counting }h_0,\qquad
  j_B:Q_P\to D_B\oplus J_P,\quad j_B(b)=(b,0).$$

$j_B$ 的邊界分量是 identity；不把 $D_B$ 與
$D_B\oplus J_P$ 錯認為同一空間。
唯一面令守恆跨面比較沒有判別力，卻不免除 $c_1\parallel c_2$
在原 $P$ 上的微因果檢查。$\dim_{\mathbb C}Q_P=4$。

## 3. 不讀 L 的方程、逆與共同響應

$P$ 的四個 strict comparable pairs 恰是四條根到頂點的邊，
在 P0.4 §3 的 $\mathcal E_P$ 中成一個 $S_2\times S_2$ 軌道。
當全部 $M_{\tau\sigma}=0$，完整 strict block 就是 $K^{ord}$，
P0.4 單軌道引理直接適用。更一般地，若容許的固定 $M$ 項在
**整條 law** 上抵銷到完整 $K$ 不讀 $L$，P0.1 §4.1 的 structured
自然性對任一 $f\in\operatorname{Aut}(P)$ 及 $L\mapsto f(L)$
給 $K(P,f(L))(f(x),f(y))=K(P,L)(x,y)$（共同 fiber 取
$V=id_{E_0}$）；因左、右各自不依 $L$，同一引理的證法仍
推出四個 block 同為某個 $k\in\operatorname{End}(E_0)$。
diagonal 不讀 $L$，又對交換 $c_1,c_2$ 自然，因此兩頂點
共用某個 $d\in\operatorname{End}(E_0)$。不假定 $d,k$ 為純量，
也不借用 IK-01 的特定係數。內部方程恰為

$$ (K_{int}\psi)(c_i)=d\psi(c_i)+k\psi(a_1)+k\psi(a_2),
\qquad i=1,2. \tag{K22.1}$$

若 $d$ 不可逆，取非零 $w\in\ker d$，令 $\psi(c_1)=w$
而其他座標為零。則 $\gamma_B\psi=0$ 且由 (K22.1)
得 $K_{int}\psi=0$，違反 $(\gamma_B,K_{int})$ 的單射；
此時完整型別已 FAIL，不能宣稱仍有已定義的 $A_B$。
故以下只考慮 $d$ 可逆。令 $H=-d^{-1}k$，則

$$ R_B(b,s)(a_j)=b_j,\qquad
 R_B(b,s)(c_i)=H(b_1+b_2)+d^{-1}s_i.\tag{K22.2}$$

直接代入方程得 $(\gamma_B,K_{int})R_B=id$，反代回亦得
$R_B(\gamma_B,K_{int})=id$。沿 $D_B\oplus J_P\cong T_P$
的固定事件座標，同源 $G_R$ 的全部非對角 block 僅有
$G_R(c_i,a_j)=H$；不可比的 $c_1,c_2$ 之間沒有 block。

## 4. 微因果與逐輸入傳播不能兼得

Q-02 的 $j_B(b)=(b,0)$，所以 $F_B=R_Bj_B$ 由 (K22.2) 給出

$$F_B(a_1)=(I,0),\quad F_B(a_2)=(0,I),\quad
  F_B(c_1)=F_B(c_2)=(H,H).\tag{K22.3}$$

$h_Q$ 是兩個根的正 counting 配對。以 $h_0$ 正交座標取
Hermitian adjoint $\dagger$，CAR 的異頂點 block 為

$$A_B(c_1,c_2)=(H,H)\begin{pmatrix}I&0\\0&I\end{pmatrix}
  \begin{pmatrix}H^\dagger\\H^\dagger\end{pmatrix}
 =2HH^\dagger.\tag{K22.4}$$

$c_1\parallel_P c_2$，P0.2 §6.2 對**全 fiber**要求
$A_B(c_1,c_2)=0$。對任意 $w\in E_0$，
$\langle w,2HH^\dagger w\rangle=2\|H^\dagger w\|^2$；
故 (K22.4) 為零當且僅當 $H=0$。然而 $H=0$ 時 §3 列出的
**全部** strict off-diagonal $G_R$ blocks 都是零，違反
P0.2 §7(a)「每個完整輸入」的非零同源傳播。
若 $H\ne0$，(K22.4) 在原 $P$ 的不可比對上非零，微因果 FAIL。
兩種情況已窮盡；$d$ 不可逆則更早型別 FAIL。
此結論不使用守恆、Green 識別、(b′)、IK-01 的 $t$、
任何 state 或其他尺寸的案例。

## 5. 精確作用域：讀 L 的類仍未決

P0.1 §4.4 允許完整 $K$ 含固定線性 $L$ 計數。
單軌道引理只控制 $K^{ord}$，不能在固定 $L$ 下據此認定
四個完整 blocks 相同。若仍有可逆的共同 $d$，記
$H_{ij}=G_R(c_i,a_j)=-d^{-1}K_{int}(c_i,a_j;L)$，
則 Q-02 同一唯一面上的**必要**微因果條件變為

$$H_{11}H_{21}^\dagger+H_{12}H_{22}^\dagger=0.
\tag{K22.5}$$

即兩個頂點對 $D_B=E_0\oplus E_0$ 的響應行
$(H_{11},H_{12})$、$(H_{21},H_{22})$ 在 counting Gram
意義下正交。只有當四個 $H_{ij}$ 同為 $H$，它才退化成
$2HH^\dagger=0$。本稿**沒有**判定 P0.1 的 $L$ 計數類能否
在每個 $L$ 達成 (K22.5)，也沒有構造候選或宣稱正交足以通過
守恆、Green、field/state、§7(a) 或其餘全域義務。
若下一步要研究讀 $L$ 的 K，仍須另立規格、先 GO 再算；
若要改 Q-02，則須重新走資料門檻。本證明只封住已列出的
Q-02＋**不讀 $L$** 子類，不封存 P0.4 或整個 Q-02。
