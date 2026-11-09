# P0.3 dual star 的正 CAR 微因果與逐輸入 span 障礙：Q-01 及條件式資料類

狀態：**【限定紙上證明草稿／待 exact-head 獨立複核】**。2026-11-09 Asia/Taipei。
探索軌，model ID **NONE**，不具 §5.2.1(v) 依據資格。
本稿不固定 K、source、Green、CAR 或 state 的新規格，不修改
[P0.3 契約](kq_conditional_internal_innovation_problem_contract_v0_3.md)、
[Q-01 資料](kq_p03_correlated_innovation_data_registration_v0_1.md)、
P0.1／P0.2 或已封存試作。它從已固定型別推出兩個不同作用域的障礙；
第二個**明列額外的邊界滿射前提**，不宣稱 P0.3 全部允許資料已被排除。

## 1. 前提、出處及尚未取得的強主張

令 $P_r=\{a,v_1,\ldots,v_r\}$（$r\ge3$）為 dual star，只有
$a\prec v_i$，葉子兩兩不可比。由[已複核的 #108 稿](kq_dual_star_initial_data_obstruction_study_v0_1.md)
§2，$P_r\in D_{KQ}$，所有合法 $L$ 均須檢查。下標只代表固定 $L$ 的葉排列，
不構成外加葉標籤或挑選輸入。以下每項是本稿使用的前提，並非推論後補設：

| 前提 | 定案來源及用途 |
| :--- | :--- |
| $B=\{a\}$、$I=\{v_i\}$；$U\subseteq I$ 對原 order 同構自然；$Q_P=D_B\oplus(\mathbb C^U\otimes E_0)$，$\dim E_0=2$ | P0.3 §1、§3；$S_r$ 傳遞作用只允許 $U=\varnothing$ 或 $U=I$ |
| $K_{int}:T_P\to J_P$，非原 order 的非對角 block 為零，diagonal 不讀 $L$；$R_B=(\gamma_B,K_{int})^{-1}$ 必須存在 | P0.3 §4、P0.2 §4；共同可逆葉 diagonal $d$ |
| $K$ 唯一的 $L$ 入口是 P0.1 §4.4 的固定線性 count 類；order 部分及 diagonal 不讀 $L$ | P0.3 §4、P0.1 §4.1、§4.4–4.5；一般資料版本的仿射 $H_i$ |
| $h_Q$ 正定，$j_B:Q_P\to D_B\oplus J_P$ 對原 order 同構自然且不讀 $L$；$F_B=R_Bj_B$，$S_B=F_B^\dagger$，$A_B(f,g)=h_Q(S_Bf,S_Bg)$ | P0.3 §3–5；一般版本的正 Gram 與對稱係數 |
| 每對葉子在原 P 全 fiber 上 $A_B(v_i,v_j)=0$；每個輸入的實際施加 strict-order K blocks 的 complex span 至少 2 | P0.3 §5 的微因果與保留的 P0.2 §7(b)；不是跨輸入的 span 要求 |

P0.3 §3 **沒有明文要求一般 $j_C$ 單射，更沒有要求 $\pi_Dj_B$ 滿射**。
Q-01 §4 另外固定了單射 $j_C$；二者不能偷換。
Claude 的 Q-01 複核、較強的腦中提示與後來的滿射補強已由操作者轉交，
逐字見接觸帳 §71 EXP-0155–0156；GPT 的先行閱讀與更正見 EXP-0154、0157。
這不是盲發現，也不把 Claude 尚未寫成證明的強版本當成已審定理。

## 2. 共通的 augmented 方程與 source 響應

固定任何 $L$。葉方程必為
$$ (K_{int}\psi)(v_i)=d\,\psi(v_i)+k_i\,\psi(a). \tag{1} $$
葉子在 $S_r$ 下可遞，diagonal 不讀 $L$，故共用 $d$。
若 $d$ 奇異，令根資料和 source 為零，只在一片葉子放非零
$\ker d$ 向量，則 $(\gamma_B,K_{int})$ 不單射；所以聲稱通過
P0.3 §4 的候選必有可逆 $d$。若該型別失敗，整體已 FAIL，
後文不假設存在一個偽 inverse。

定義根到葉的齊次響應 $H_i=-d^{-1}k_i$，共同葉 source 自響應
$D=d^{-1}$。$R_B$ 對邊界／source 座標的葉 row 為
$$\pi_{v_i}R_B(b,s)=H_i b+D s_i.\tag{2}$$
這只是解同一方程的 block 代數，不是選一組 K 的係數或代入案例求輸出。
已固定的 $L$ 計數類若被使用，在 §4 才需要仿射性；§3 的 Q-01 證明不需它。

## 3. 命題一：已登記 Q-01 全類的限定障礙

**命題。** 對每個 $r\ge3$、每個合法 $L$，在 Q-01 §2–4 的資料不變下，
任何滿足 §4 augmented inverse 與原 P 微因果的 $K_{int}$，其在
$P_r$ 實際施加的 strict-order blocks span 至多 1。故無法同時通過
P0.3 保留的逐輸入 §7(b)；這只封堵 **P0.3＋Q-01** 的全域正面完成。

**證明。** Q-01 在 dual star 固定 $U=I$、唯一合法面 $C=B$、
$j_B(b,u)=(b,u)$。在 counting 座標，$h_Q^{-1}$ 的根 block 是 $I_{E_0}$，
根／葉 cross blocks 為零，異葉 covariance blocks 是 $-I_{E_0}$
（Q-01 §3 的 $I+L_{K_r}$）。由 (2) 和正 Gram 的 adjoint 定義，
對 $i\ne j$ 有精確 block 式
$$ A_B(v_i,v_j)=H_iH_j^*-DD^*.\tag{3} $$
此處 $*$ 是 $h_0$ 的**數學 adjoint**，不是 field *。
微因果強制所有異葉對 $H_iH_j^*=DD^*$。
$D$ 可逆，故右邊正定；每個 $H_i$ 因至少參與一個可逆乘積而可逆。
對相異 $i,k,j$，$H_iH_j^*=H_kH_j^*$，右乘 $(H_j^*)^{-1}$
得 $H_i=H_k$。$r\ge3$ 保證可選第三片葉，故所有 $H_i=H$。
由 (1) $k_i=-dH$，且 dual star 唯一實際施加的 order 非對角 blocks
就是這些 $(v_i,a)$；它們全相同，complex span 至多 1，違反
每個輸入至少 2 的 P0.2 §7(b)。∎

本命題不使用 P0.1 §4.4 的仿射 $L$ count、不使用 Green 識別、
守恆（此輸入只有一面）、state 或特定 kinetic 係數；它**使用**
Q-01 的根／葉配對分離、異葉 covariance $-I$ 及 $j_B=(id,id)$。
換資料可能不再給式 (3)，所以本命題不能單憑自己升格成 P0.3 契約 no-go。

## 4. 命題二：一般自然資料在邊界滿射下的條件式障礙

設一般 P0.3 合法資料的 $j_B$ 任意（不讀 $L$），但保留 §1 的
正配對與 structured 自然性。將 $j_B$ 的 boundary/source 分量記為
$B_*:=\pi_Dj_B:Q_P\to E_0$、$S_i:=\pi_{v_i}\pi_Jj_B:Q_P\to E_0$。
令 $G$ 是 $h_Q$ 相對固定 counting $h_0$ 座標的正定 inverse matrix。
由 (2)，量子 response 的第 $i$ 葉 row 為
$$F_i=H_iB_*+DS_i.\tag{4}$$
定義根 covariance
$$P_*:=B_*G B_*^*.\tag{5}$$
為免與 poset $P_r$ 混淆，以下用 $P_*$ 表示 Claude 提示中的 $P$。
因 $G>0$，對 $z\in E_0$ 有
$\langle z,P_*z\rangle=\|G^{1/2}B_*^*z\|^2$，故
$$P_*>0\quad\Longleftrightarrow\quad B_*\text{ 滿射}.\tag{6}$$

$S_r$ 置換任意葉子，$B_*$ 不變、$S_i$ 隨葉子換位，$G$ 與置換交換，
共同 $D$ 不變。對所有 ordered $i\ne j$，以下矩陣各自與 $i,j$ 無關：
$B_*G S_j^*D^*$、$DS_iG B_*^*$、$DS_iG S_j^*D^*$。
令它們依序為 $Q_1,Q_2,R$（不預設 $Q_1=Q_2$）。
從 (4) 展開，所有異葉 block 具有**同一組係數**：
$$A_B(v_i,v_j)=H_iP_*H_j^*+H_iQ_1+Q_2H_j^*+R.\tag{7}$$
這裡的 $A$ 仍由原本 $F_B,h_Q$ 取得，沒有用目標微因果反選資料。

依 P0.1 §4.4，其他葉子對 $(a,v_i)$ 的 count 只能按 $L$ 的葉位置
分成 between $i-1$ 與 post $r-i$；$K^{ord}$ 不讀 $L$，
所以 $k_i=k_0+i k_1$，且 $d$ 共同不讀 $L$。
於是 $H_i=H+iV$，$H,V$ 對固定完整輸入為兩個矩陣。
將它代入 (7)，可寫成 $f(i,j)=a+bi+cj+d_2ij$，
四個係數都是矩陣，尤其 $d_2=VP_*V^*$。
當 $r\ge3$，微因果要求六個 ordered pair
$(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)$ 都有 $f=0$。
以下**只在這六點上作差分**，不假定對角 $(i,i)$ 的方程：

$$\begin{aligned}
f(1,3)-f(1,2)&=c+d_2=0,\\
\tfrac12[f(2,3)-f(2,1)]&=c+2d_2=0,\\
f(3,1)-f(2,1)&=b+d_2=0,\\
f(1,2)&=a+ b+2c+2d_2=0.
\end{aligned}$$

逐個矩陣項相減先得 $d_2=c=0$，再得 $b=a=0$；
因此六點確實足以決定雙線性多項式的全部係數，特別是
$VP_*V^*=0$。若**額外有 $B_*$ 滿射**，(6) 給 $P_*>0$，
故 $VP_*^{1/2}=0$，進而 $V=0$。所有 $H_i$ 和 $k_i=-dH_i$
相同；§3 同理給出逐輸入 §7(b) FAIL。∎

**何時滿射已被固定資料保證？** 在 Q-01 的 $P_r$，$U=I$、
$\dim Q_P=2(r+1)=\dim(D_B\oplus J_P)$，且 Q-01 §4 明文使
$j_B$ 單射；故它是雙射，$\pi_Dj_B$ 滿射。
這是 Q-01 的事實，**不是 P0.3 一般資料的公設**。
對一般 $U=I$，若另有 $j_B$ 單射，同一維數理由亦成立；
但 P0.3 §3 只規定線性接合的型別，未強制單射。
對 $U=\varnothing$，$\dim Q_P=2$，不論 $j_B$ 是否單射都
不能單憑總空間的維數推出 $B_*$ 滿射。

## 5. 非滿射的明確未決範圍與下一步

當 $\operatorname{rank}B_*=1$ 時，差分仍給
$VP_*V^*=0$，但只推出 $VP_*^{1/2}=0$，不能推出 $V=0$；
$V$ 在根資料未進入 CAR 的方向仍可能非零。
當 $B_*=0$ 時，(4) 的 $F_i=DS_i$ 與 $H_i$ 無關，
微因果本身不能限制 $H_i$；這時根到葉 K block 對該輸入的 CAR
不可見。P0.3 §3 說若只能讓 K 在 CAR 中失去作用則「判未完成」，
§5 又要求兩個 kinetic 比較對象給不同可比 $A$，不能只改不可見 source sector。
但這些條款是否**逐個 dual star 輸入**足以排除所有 $B_*=0$、
或 rank 1 的資料，需要另證；不能將全域可見性直接代入逐輸入量詞。
本稿**不**宣稱非滿射類一般不可能，也不將 §4 的條件命題稱為
完整 P0.3 契約層 no-go。

Q-01 v0.1 已取得資料 GO，而 §3 在它下給出與任何選 K 無關的
逐輸入矛盾。若獨立複核確認，固定 Q-01 版本不能以第三道 K 規格
求得全域成功；不能事後調 $U,h_Q,j_C$、放寬逐輸入 span、
縮掉 dual star 或把原 P 微因果改為依 $L$ 的比較。
是否修約 §7(b)、重走資料門檻或作階段整理，由操作者在證明複核後決定。
本交付只請 reviewer 核對兩個作用域、(3) 的 adjoint／正配對、
(6) 的滿射充要性、(7) 的 $S_r$ 對稱係數與六點差分；
不要求選 K 或在未取得規格 GO 前代入案例求值。
沒有科學數值／符號程式、RNG、撒點、producer、raw／sealed、seed、
主機量測或新文獻檢索；探索軌、formal／E0與全部來源隔離維持。
