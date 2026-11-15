# IK-01 v0.1：P0.4＋Q-02 的同源 K／source／Green／CAR／state 固定試作規格

狀態：**【第三道規格草稿／待 exact-head 獨立複核；未取得規格 GO、未開始研究】**。
2026-11-15 Asia/Taipei。基線 main `aa9d2fd3d20d0df588a74961ca45ea21811fd67e`，
tree `853fc46c448d84249274db875aff22ecfeb30baa`。Problem ID
`X-KQ-COND-TA-P0.4`；探索試作 ID `X-KQ-IK-01-v0.1`。
本稿只固定事前可失敗的規則與判定式，不報任何具體輸入的 K、G_R、A 或 PASS。
先行三帳 §84 單獨 commit，規格在後一 commit。規格 GO、CI、合併及 tree 核對
前不代入案例、做科學程式或研究。探索軌，不具 §5.2.1(v) formal 資格。

## 1. 來源、既有資料和預先承認的風險

以已 GO 的 [P0.4](kq_conditional_internal_innovation_problem_contract_v0_4.md)、
[Q-02 v0.1](kq_p04_correlated_innovation_data_registration_v0_1.md) 為唯一
現行契約／資料版本；P0.3、Q-01 v0.1 與 #111 的舊判定不回填。
全部 $P\in D_{KQ}$、全部 $L\in LE(P)$、共同
$R_0=(E_0,h_0,\eta_0)$ 且 $\dim_{\mathbb C}E_0=2$。
Q-02 的 $B=M(P)$、$I=P\setminus B$、$\mathcal C_Q(P)$、
$U(P)$、$Q_P$、$h_Q$、$j_C$ 逐式原樣使用；任何面、圖邊、
$C_\Gamma$、matching 或相關係數都不得以輸出調整。

作者已見 dual star 的 #111 障礙及 P0.4 (b′) 的修約，故本選擇不盲。
亦已見 IB-01 在 $t=1$ 類型的鏈 $C_4$ 面奇異；本版事前改選
$1/2$ 與 $2/3$，不宣稱這能保證其他面的可逆性。這是根據公開舊 FAIL
做的下一版選擇，審核須將它視為已受先前輸出影響。
本版以**整個原 P 的 past-cone 基數差**作 $K^{ord}$ 係數來源，
而非只讀區間型別；這直接面對 #115 的已知代價。
此 order 統計仍未保證把每個不同的 active 軌道區分開；若有多軌道
輸入在本統計上全部相同，(4.2) 會 FAIL，按原狀封存，不能改用
逐軌道編碼、排名或查表補救。選定零 $L$ 係數是 P0.1 §4.4 的
合法子類，並不聲稱 $L$ 不可能有物理效應。

## 2. 型別與固定 K 法則

所有正數學 adjoint 記 $\dagger$，基於 $h_0$ counting、$h_Q$；
fermionic 代數 involution 記 $*$，不把 $\eta_0$ 的不定配對
當正 CAR 配對。$T_P=\mathbb C^P\otimes E_0$、
$J_P=\mathbb C^I\otimes E_0$、$D_C=\mathbb C^C\otimes E_0$。
$\rho_B=\gamma_B:T\to D_B$、$\rho_I:T\to J$、
$\iota_B=\rho_B^\dagger$、$\iota_I=\rho_I^\dagger$。
$\eta_0$ 是共同的非純量 Hermitian involution；所有 fiber
變換是同一 global $h_0$-unitary $V$，且 $V\eta_0=\eta'_0V$。

對 $y\prec x$，令 $p(z)=|\{w:w\prec z\}|$、
$d_P(x,y)=p(x)-p(y)-1\ge0$。**此 $d_P$ 是 past-cone
基數差，不是 Hasse 最短距離或區間內點數。** 固定候選 $t=1/2$，
其唯一 order block 及方程為

$$D_t(x,y)=\begin{cases}I_{E_0}+t\,d_P(x,y)\eta_0,&y\prec x,\\
0,&\text{otherwise},\end{cases}\qquad
K_t=\rho_I(I_T-D_t):T\longrightarrow J.\tag{IK.1}$$

本版實際 K 僅 $K_{1/2}$；$t=2/3$ 是 §6 的**固定比較對象**，
不是第二套候選、可調參數或按 P 選擇器。$K^{ord}_{1/2}=K_{1/2}$
的 strict block；diagonal $I$、其餘非 order off-diagonal
皆為零。P0.1 §4.4 所有可實現的 $M_{\tau\sigma}$
**一次固定為零矩陣**，所以完整 K 不讀 $L$，source 與下游
也不直接或間接解碼 $L$。$d_P$ 只用原 P 的全域 past cone，
可跨區間讀取原序但不讀任何 $L$ 排名、$n_{\tau\sigma}$、
Q-02 的通道或成功資訊。係數 $1,t$、$\eta_0$ 以外沒有
逐 P、逐 pair 的權重、相位或矩陣表。

若 $f:P\to P'$ 是 order 同構，$p(fz)=p(z)$，
$f(B)=B'$、$f(I)=I'$；由共同 $V\eta_0=\eta'_0V$
得 $K' U_T=U_J K$。同一式對 $L\mapsto fL$ 仍成立，
而且所有 $L$ 用同一 K。只有共同 global fiber 換基，
不引入逐事件 frame。$D_t$ 在嚴格序上支撐，故冪零。

## 3. Canonical inverse、合法面與同源 response

令 $M_t=\iota_B\rho_B+\iota_I K_t=I_T-\iota_I\rho_I D_t$。
令 $N_t=\iota_I\rho_I D_t$；它僅在 strict order 上有 block，
$N_t^{|P|}=0$。固定

$$G_{R,t}=M_t^{-1}=\sum_{j=0}^{|P|-1}N_t^j,\qquad
G_{A,t}=G_{R,t}^{\dagger}\quad\text{作 }M_t^\dagger\text{ 的 advanced inverse}.\tag{IK.2}$$

研究須逐式核 $M_tG_{R,t}=G_{R,t}M_t=I$、原 P retarded，
$\rho_BG_R\iota_B=I_B$、$K G_R\iota_B=0$、
$\rho_BG_R\iota_I=0$、$K G_R\iota_I=I_J$。
同源齊次初值 $E_B=G_R\iota_B$、零初值 source response
$R_J=G_R\iota_I$；$G_A$ 不是同一非自伴 M 的另一 inverse。

對**每個** Q-02 合法 $C$，先核
$T_C=(\gamma_C,K_t):T\to D_C\oplus J$ 是雙射。
若不是，該面的 $R_C$、$F_C$、$S_C$、$A_C$ 標 undefined，
並使本試作全域 FAIL；不刪面、不選 generalized inverse。
若是，唯一 $R_C=T_C^{-1}$，要求
$\gamma_C R_C=\pi_{D_C}$、$K_tR_C=\pi_J$、
$R_C(\gamma_C,K_t)=I_T$，與同一 K 的 canonical $R_B$
的兩側 composition 關係。由**凍結的** Q-02 $j_C$ 定義

$$F_C=R_Cj_C:Q_P\to T_P,\quad
S_C=F_C^\dagger:T_P\to Q_P,\quad
A_C(f,g)=h_Q(S_Cf,S_Cg).\tag{IK.3}$$

不能另給 $F$、自由 smearing、逐面正矩陣、裸 source contact
或從想要的 A 反因子分解。$j_C$ 單射且 $R_C$ 雙射時，
$F_C$ 單射、$S_C$ 滿射，$\operatorname{rank}A_C=\dim Q_P$
按構造成立，正性亦按構造成立，兩者均不算物理成功證據。
若任一前提失敗，不能用這些結論遮蓋 FAIL。

## 4. 獨立 Green、source 與場的 typed 假說

固定 $C_G=G_R+G_A-I_T$；$I_T$ 只作對角 contact，
不是新增 CAR。對每個 strict $y\prec x$、每個合法 C、
全 $v,w\in E_0$ 要求

$$A_C(\iota_xv,\iota_yw)=
h_P(\iota_xv,C_G\iota_yw).\tag{IK.S1}$$

反向配對另由 Hermitian 條件核；不可比對不在此識別式的
比較域，仍須 §5 直接查。因 $G_A$ advanced、contact
僅 diagonal，strict 下方 (IK.S1) 即 $A_C(x,y)=G_R(x,y)$。
這是**規格前固定的獨立 Green 假說**，不是定義 $C_G:=A$。
canonical $C=B$ 且 $y\in B$ 的初值欄若按構造成立，須
明標自動；兩端均在 I 的 strict pairs 另列逐對檢查，
不讓初值欄冒充 source-sensitive 證據。鏈 $C_N$ ($N\ge3$)
與 diamond 有這種 pair；dual star、向下 star、$K_{2,2}$
及 $k\times C_2$ 無此類，逐項記檢驗空洞而不記 PASS。

同一 M 的 composition 另交

$$M C_G M^\dagger=M^\dagger+M-MM^\dagger,\qquad
\rho_I C_G\iota_I=\rho_I R_J+(\rho_I R_J)^\dagger-I_J.\tag{IK.S2}$$

它們由 (IK.2) 按構造成立，單獨不能使 (IK.S1) PASS。
任何 C 的 $F_C$ 及 A 都只經 $R_Cj_C$ 取得；
不得以 $C_G$、$A$ 或 source 的成功反定義 K。

固定 charged CAR 型別，不另給 self-dual conjugation。
令 $\mathfrak A(Q_P)$ 是由同一正 $Q_P,h_Q$ 的 fermionic
exterior Fock 表示所生成的 unital $*$-代數，令
$c^\dagger(q)$ 對 $q$ 複線性、$c(q)=c^\dagger(q)^*$，
$\{c(q),c^\dagger(q')\}=h_Q(q,q')1$，
$\{c^\dagger,c^\dagger\}=\{c,c\}=0$。
每個合法 C 的**試作 field** 固定為

$$a_C(f)=c^\dagger(S_C f),\qquad
\{a_C(f)^*,a_C(g)\}=A_C(f,g)1,\quad
\{a_C(f),a_C(g)\}=0.\tag{IK.S3}$$

代數 $*$ 不是 $h_0$ adjoint $\dagger$，亦不是
$\eta_0$-adjoint。由 $K R_C=\pi_J$ 的 adjoint
$R_C^\dagger K^\dagger=\iota_J$，得**帶源 test 方程**

$$S_C K^\dagger g=j_C^\dagger\iota_Jg,\qquad
a_C(K^\dagger g)=c^\dagger(j_C^\dagger\iota_Jg),\quad g\in J.\tag{IK.S4}$$

$\iota_J:J\to D_C\oplus J$ 是 source 槽注入。
右側由 Q-02 固定 source 部分，對 C 不變；在 $U=\varnothing$
時它可能是零，應如實記錄，不把 classical source 改名為
free vacuum 模式。若 $R_C$ undefined，field/source 亦 undefined。

固定 normalized vacuum $\Omega_P$ 在 $\Lambda Q_P$；
$c(q)\Omega_P=0$，$\omega_P(X)=\langle\Omega_P,X\Omega_P\rangle$。
兩點 $\omega_P(a_C(f)^*a_C(g))=A_C(f,g)$、
$\omega_P(a_C(f)a_C(g)^*)=0$；高點以此 charged
quasi-free Wick／determinant 規則，奇數點為零。
正性、歸一化、CAR algebra 及高點規則在此表示中按構造成立，
不當物理真空、正能量、spin 或 continuum 的證明。
同一 P 的不同合法面須另過 §5 守恆／field 接合；
不能以各面各自一個 Fock vacuum 代替共同物理 field。

## 5. 全 fiber 判定、跨面一致性與四個關鍵輸入

在共同 $h_0$-orthonormal fiber 座標令 $H_Q$ 為 Q-02
$h_Q$ 的正 Gram，$F_{C,x}=\operatorname{ev}_xF_C$；
以 $^{\mathrm H}$ **只**記矩陣共軛轉置，則 $A_C$ 的
counting block 是 $A_C(x,y)=F_{C,x}H_Q^{-1}F_{C,y}^{\mathrm H}$。
這是 (IK.3)
的**判定表述**，不是新增獨立 $A$。全部 $P,L,C$
須以下列精確等式逐元素核對，零 tolerance：

| 義務 | 事前判定及失敗處理 |
| :--- | :--- |
| 逆與來源 | 每個 $T_C$ 雙射、(IK.2) 左右 composition、原 P retarded；任一面奇異即 undefined 且全域 FAIL |
| 守恆 | 同一完整 $T$ 上每對合法面 $A_C=A_{C'}$；$c_Q=1$ 單列不提供比較判別力，仍查其他義務 |
| 微因果 | 對原 P 每個 $x\parallel y$、每個 C 及全部 $E_0$，直接查 $A_C(x,y)=0$；Ind 不略過 |
| Green 識別 | (IK.S1) 每個 strict pair、全部 C；(IK.S2) 標按構造，兩端在 I 的對單列 |
| 非零傳播 | 每個完整輸入至少一個 $y\prec x$ 的非零同源 $G_R(x,y)$；contact／source 裸 block 不算 |
| field/state | (IK.S3–S4)、同源 source、跨面 field 接合、正性歸一化與高點；按構造部分不得抵銷別項 FAIL |

對跨面 field，若 A 守恆且 F 均單射，唯一的
$U_{CB}:Q\to Q$ 須滿足 $F_CU_{CB}=F_B$；
逐式檢查其存在、$h_Q$-unitarity、identity／composition。
固定在同一 $\mathfrak A(Q)$ 上由 $U_{CB}$ 的第二量子化
識別各面 $a_C$，並核 source 向量
$j_C^\dagger\iota_J$ 在識別下相容。
具體查 $j_B^\dagger\iota_J=U_{CB}^\dagger j_C^\dagger\iota_J$
作 $J\to Q$ 的等式，並核 $U_{DC}U_{CB}=U_{DB}$。
不因形式 Gram 相等就省掉 field/source 的同一性檢驗；
若不存在、非 unitary 或 source 不相容，field/state 義務 FAIL。

四個不可事後選擇的特別式在**研究前**鎖定。記
$H_{x,b}=G_R(x,b)$，$D_x=G_R(x,x)$；它們是同一 K 的
homogeneous／source 響應，不是新輸入：

1. dual star $a\prec v_i$：唯一 C=B，Q-02 給葉間
   inverse covariance $-I$；逐 $i\ne j$ 查
   $A_B(v_i,v_j)=H_{v_i,a}H_{v_j,a}^\dagger-D_{v_i}D_{v_j}^\dagger=0$。
   同時另查 §7(a)；(b′) N/A 不代表這些 PASS。
2. $K_{2,2}$：$U=\varnothing$、唯一 C=B；逐
   $c_1\parallel c_2$ 查
   $A_B(c_1,c_2)=\sum_{a\in\{a_1,a_2\}}
   H_{c_1,a}H_{c_2,a}^\dagger=0$。多根交叉項
   在原 P 直接查，不能因沒有共同合法面或 (b′) N/A 略過。
3. diamond $a\prec b,c\prec d$：每個 $L$、
   Q-02 兩個合法面 C=B 與 C={d} 都查
   $A_C(b,c)=F_{C,b}H_Q^{-1}F_{C,c}^{\mathrm H}=0$；
   canonical B 的圖邊 inverse covariance 是 $-I$，
   但非 canonical 面不得套用同一簡化式而不計其 source。
   守恆、(IK.S1) 及 (4.2) 分別另查。
4. 鏈 $C_3,C_4$ 及全部 $C_N$：所有 N 個合法面
   逐對守恆，strict Green 與內部對另查；
   (b′) 固定 §7 的同一對 witness，兩項 span 各自核對。

這些是**判定公式**，不是已代入本 K 的案例結果。
任一式 FAIL 就保留原值／原資料，不換 K 係數、面或判準。

## 6. 事前 kinetic 比較、非恆定與來源

兩個事前固定的 kinetic 對象是 (IK.1) 的 $t=1/2$（唯一
實際候選）及 $t=2/3$（僅比較）；兩者共享 P0.4、Q-02、
全域 $E_0$、全部 C、source／Green／CAR／state 公式。
二者的 K 支撐、原序自然、對角及 P0.1 §4.4 的零係數
均合法，canonical $M_t$ 由冪零結構可逆。
**這尚不保證**每個非 canonical C 上 $T_C$ 可逆；
比較對象的完整 trace 合法性須各自先核，任一不合法則
比較義務 FAIL／undefined，不挑新 t 或跳過該輸入。

預定 $C_3,C_4$、diamond 及無界鏈，對同一合法 C
逐 strict $y\prec x$ 比較
$A_C^{(1/2)}(x,y)$ 與 $A_C^{(2/3)}(x,y)$ 的 full-fiber block。
至少兩個全型別合法的 kinetic 對象須在預定可比對上給
不同 A，且實際 $t=1/2$ 至少一個非零 strict 可比
off-diagonal CAR block；只變 K 的不可見 sector、
只變對角 contact 或單一總 scalar 不算。若這些要求
在固定輸入失敗，須照實列 FAIL，不得據此換 t。
比較自身不替代 (IK.S1) 的 Green 同源識別。

除 $R_0$ 的固定二維 $\eta_0$ 與 Q-02 唯一相關
primitive 外，本規格沒有新 field-frame、transport、
per-edge phase、外加時序、逐 P 表或譜選擇器。
past-cone $p(x)$ 可由 P 直接計數，逐對整數不超過 $N$，
所需位元 $O(\log N)$；完整矩陣輸出自然需要 $O(N^2)$
block 記錄，但只有一次固定的算法而無可調逐對數值。
下游只從 P、Q-02 資料和列名上游 K、R、F 取值；
不重讀或解碼 L、$n_{\tau\sigma}$，兩個 L 若給相同
上游必給相同輸出。合法 inverse／adjoint／composition
只用於同鏈代數恆等式，不作排名選擇。

## 7. P0.4 (4.2)、(4.3) 與非平凡性預定判定

對每個完整 $P,L$，事前由 Q-02 的 $B,I$ 造
$\mathcal E_P=\{(y,x):y\prec x,x\in I\}$，
只按原 $\operatorname{Aut}(P)$ 求 $\mathcal O_P$。
單軌道一律 (b′) **N/A**，不記 PASS；其他義務全留。
多軌道時**不以 A 或 Green 選 witness**：枚舉
$\mathcal E_P$ 的全部無序兩 pair 子集，對每一對
在固定 $L$ 下把兩個 $2\times2$ blocks 展為
$\mathbb C^4$ 列向量；有非零的 $2\times2$ minor
當且僅當 complex span 為 2。對同一對分別計
$K^{ord}$ 及完整 $K_{int}$，兩者皆為 2 才是 (4.2)
的 witness。列出全部 witness 的原序自同構軌道，
不按某個標籤或有利 $L$ 選單一成功者。
任一 $L$ 沒有同一對 witness 即 FAIL。此版本完整
$K=K^{ord}$，但仍兩欄分別列數、不可跨 L 合併。

Q-02 (4.3) 固定 $\mathcal F_{orb}=\{C_N:N\ge3\}$。
對每個 N，令 $e_N=(1,2)$、$e'_N=(1,3)$，其中
1、2、3 是鏈的由小到大**序位置**，只讀 P；鏈有
唯一 L 且原序自同構為 identity。$p(1)=0$、
$p(2)=1$、$p(3)=2$，所以 $d_P(2,1)=0$、
$d_P(3,1)=1$；(IK.1) 的兩個 active blocks 是
$-I$ 與 $-(I+\tfrac12\eta_0)$。因 $\eta_0$ 非純量，
二者線性獨立；完整 K 與 $K^{ord}$ 相同，
故同一 pair 對每個 N、唯一 L 同時滿足 (4.2)。
這是**規格前**的解析 witness 方案與代數檢查，
不是守恆／微因果／Green／state 或全域 PASS。
diamond 的固定事前展示對為 $(a,b)$ 與 $(b,d)$
（另有對稱的 $(a,c),(c,d)$）；仍照全 pair 枚舉
與每個 L 查，不能以展示對代替全稱要求。

對 §7(c) 不統一截斷，事前族仍是鏈：給任意
Hasse-hop 門檻 $r$，取 $N>r+1$ 的 $C_N$，
$y=1,x=N$ 為 active 且 Hasse 距離 $N-1>r$。
$K_{1/2}(N,1)=-[I+\tfrac12(N-2)\eta_0]\ne0$，
因 $I,\eta_0$ 獨立；這一項按 law 的結構證明，
不把它與 (4.2) 或 Green 當相互獨立成功證據。
§7(a) 對所有完整輸入仍須查同源 $G_R$ 的非零
strict block；(4.2) 不會代替它。

Q-02 的 $k\times C_2$ 多面無界族另用於守恆及
真實 $\operatorname{rank}A_C$ 增長：每個 $k\ge2$
須先核全部面逆，再報 $c_Q=2^k$、
$\dim Q=2k$、$\operatorname{rank}A_C$ 及
跨面精確等式；若任一面失敗，全域 FAIL。
鏈族 $\dim Q=2$ 不被冒稱 rank 隨 N 增長。

## 8. 固定目錄、完整輸出順序與停止

固定目錄為 $C_3,C_4$、三葉向下 star、三葉 dual star、
diamond、$K_{2,2}$、$2\times C_2$、$3\times C_2$；
跨尺寸另列 $C_N$、dual star $P_r$、向下 r 葉 star、
$k\times C_2$。全部 $L$、全部 Q-02 合法 C 都在
主量詞內，目錄不是縮域。先逐列報 $N,q,k,c_Q,m,\dim Q$、
$n_{cov},n_{ind},|\mathcal O_P|$、是否有 I-to-I strict
pair、每個 L 的兩項 span 與 N/A，再按 §5 逐對
報逆、守恆、原 P 微因果、Green、非零傳播、
比較、field/source/state、rank 的 PASS／FAIL／undefined。
逐通道另報 $F_C|_{E_x}$ 是否進入可觀察 CAR、
$R_J$ 的同一 source 響應是否非零，不能用總 rank 遮蔽
某個 spectator 通道；source 與 CAR 的涵義分開報。
**先列固定目錄全部結果（含 FAIL）才寫任何整體結論。**
對同一 P 的不同 L，即使 K 相同仍分別列出或精確證明
等同，不能只挑一個 L。沒有兩面時守恆比較標
不提供判別力；沒有 I-to-I strict pair 時獨立 Green
source-sensitive 子檢驗標落空，但其他義務照查。

任何固定義務 FAIL 即本版全域未完成，不能改 Q-02、
調 $t$、擴 $M_{\tau\sigma}$、改 (4.2) 量詞、刪 P
或回頭挑 C。若需新資料或契約，另版事前審核，
保留 IK-01 的 FAIL。#108、IB-01、#111 舊結果
維持原作用域，不稱本試作已逃出其餘障礙。
formal／E0、A／B、UNKNOWN、item7／8、6a-E、
Freeze-1a、raw／sealed／producer／seed 隔離均維持。
規格未獲 exact-head GO、CI、原樣合併和 tree 核對前，
不得代入固定目錄或作研究輸出。

給 reviewer 的重點：核 (IK.1) 的 past-cone 來源與
零 L 係數、(IK.2–4) 同源和 field/source 型別、
(IK.S1) 的獨立性、dual star／$K_{2,2}$／diamond
的原 P 交叉式、鏈族同一 pair 的雙 span 證明、
兩比較對象、完整目錄與 FAIL 順序。規格 GO 只
授權後續研究，不是此試作的物理 PASS。
