# Q-01 v0.1：P0.3 的唯一配對 trace 與關聯內部通道純資料登記

狀態：**【資料提案／draft／待 exact-head 獨立複核；未取得資料 GO】**。2026-11-08 Asia/Taipei。
依據 [P0.3 問題契約](kq_conditional_internal_innovation_problem_contract_v0_3.md) §2–6；
資料版本 `Q-01 v0.1`，新 model ID **NONE**。探索軌，不具 §5.2.1(v) 依據資格。
本稿只固定 $\beta,U,Q_P,h_Q,j_C$ 的一條跨全部 $D_{KQ}$ 的有限資料 law，
給集合／容量／自然性證明及事前審核目錄。**沒有選 K、source 算符、Green、CAR、state、
kinetic 比較對象或任何輸出。** 資料 GO、原樣合併與 tree 核對之前不得寫 K 規格；
其後仍須獨立 K 規格 GO 才能研究。P0.2 的 B-01 與 IB-01 FAIL 保留原樣。

## 1. 基線、已見提示與資料選擇的代價

基線是 #109 合併 main `59926a64b89f0750729b588ceae33a9c64aa55c9`，tree
`c13f9b9ef4c00499b70c98568e02b56f322c53a2`；P0.3 問題契約已獲獨立 GO。
先行三帳 commit 只記已見接觸與選擇意圖；本稿在其後獨立 commit。
公開 Git 可以查內容和 commit 順序，不能證作者從未預想下游結果。

已見 Claude 對 dual star 的初值容量障礙、共同起點葉對交叉項、資料自然性及
「容量只數 CAR 中實際非零事件響應」的更正。本稿的圖關聯是針對這些已見提示
提出的**事前量子 primitive**，不是從 order 自動導出的物理定理或盲發現。
作者在紙上考慮過直接沿用 B-01 全部面與簡單祖先 incidence transport：
例如兩個互不可比最小元都在兩個互不可比極大元之前時，祖先 incidence 是全 1，
不能給初值座標的可逆配對。本版改用「唯一完美因果配對」的 order predicate；
它會刪掉該輸入的極大面，**這是 P0.3 的新 $\beta$，不是 B-01 的事後修補或
對 P0.2 的追認**。所有 P 仍在域內，且有 B 面；多面無界族在 §5 事前證明。
合法面變少可能使守恆比較落空，不能把這點算作成功，亦不能於 K 輸出後再改 predicate。

## 2. 一次固定的 $\beta$ 與唯一配對

對每個 $P\in D_{KQ}$，令 $N=|P|$，$B=M(P)$ 是全部 minimal 元素，$k=|B|$，
$I=P\setminus B$。$H$ 遍歷按包含極大的鏈；$b\preceq c$ 包含 $b=c$。
先定 order-cut 候選 $\mathcal C_{B01}(P)$ 為全部大小 $k$ 的反鏈，且與**每條**
極大鏈恰交一次（B-01 §2 的原 predicate）。對候選 $C$，造二部圖
$\Lambda_C=(B,C;\{(b,c):b\preceq c\})$。

$$\mathcal C_Q(P)=\{C\in\mathcal C_{B01}(P):
             \Lambda_C\text{ 恰有一個完美配對}\}.$$

若 $C\in\mathcal C_Q$，記唯一配對 $\mu_C:B\to C$。全部合法面都保留，
不再按 K／trace 可逆性／CAR／成功／$L$ 選面。$D_C=\mathbb C^C\otimes E_0$，
$h_C$ 為既有 $h_0$ counting 配對，$\gamma_C$ 是座標限制；$I$ 對全部面固定。
在 $C=B$ 時，minimal 元素之間不可比，$\Lambda_B$ 只有 identity 邊，
所以 $B\in\mathcal C_Q$，$\mu_B=id$。B-01 §3 的有限下降證明給
$1\le k\le N-1$、$B$ 為非空非全 past-set、$q_I=q(P)\ge2$；
這些結論在縮小面族後原封成立。任何 $P$ 均至少有一個合法面，
但**不**保證某個後續 $K$ 使所有 $R_C$ 可逆。

這個 matching 是完整有限 order 演算法：列出 $k!$ 個雙射，逐個檢查
$b\preceq\mu(b)$，恰一個通過才合法。它不是外加每面挑選的 frame 或 phase；
若有兩個通過就刪**該面**而不刪 P。若同構 $f:P\to P'$，則
$f(B)=B'$、$f(I)=I'$、$f(\mathcal C_Q)=\mathcal C_Q'$，且
$f\mu_C=\mu_{f(C)}f$。每個原 P 的所有 $L$ 使用同一面族。

## 3. 內部事件通道 $U$ 與正關聯配對 $h_Q$

令 $R(x)=\{b\in B:b\preceq x\}$。對 $x\in I$ 若 $|R(x)|=1$，
其唯一元素記 $r(x)$。定義簡單無向圖 $\Gamma_P$：頂點先取 $I$ 中具有
唯一根 $r(x)$ 的事件；當 $x\parallel y$ 且 $r(x)=r(y)$ 時連一條邊。
$U(P)$ 是**所有至少有一條邊的頂點**，$m=|U|$；
$\Gamma_P$ 在 $U$ 上不含孤立頂點。這一條 rule 對所有 P 相同，
只讀原 order／count，不讀 $L$、K、Green、CAR、state 或某面成敗。
在 dual star $P_r$，$U=\{v_1,\ldots,v_r\}$；在鏈與向下 star，$U=\varnothing$。

令 $L_\Gamma$ 為 $U$ 上的無向圖 Laplacian（每條邊加
$(e_x-e_y)(e_x-e_y)^*$），固定 $C_\Gamma=I_U+L_\Gamma$。
**唯一新增的相關 primitive** 是在通道座標上使用 $C_\Gamma$ 作 covariance；
無另外的逐邊權重、相位、每 P 常數或自由正矩陣。$E_0,h_0$ 仍是全域固定的二維型別。
資料空間與正定配對一次固定為

$$Q_P=D_B\oplus(\mathbb C^U\otimes E_0),\qquad
 h_Q((b,u),(b',u'))=h_B(b,b')+
 \sum_{x,y\in U}(C_\Gamma^{-1})_{xy}h_0(u_x,u'_y).$$

$m=0$ 時第二項為零。對非零 $w\in\mathbb C^U$，
$w^*C_\Gamma w=\|w\|^2+\sum_{\{x,y\}\in E(\Gamma)}|w_x-w_y|^2>0$，
故逆存在、$h_Q$ 正定。$C_\Gamma$ 的相異相鄰點 off-diagonal 恰為 $-1$；
這是可檢驗的通道相關，不藏在「正配對」的名稱中。
此配對是外加量子資料，**不**是 order 單獨產生的正性。

在每個同源 dual star 的 $r$ 片葉子上，$\Gamma=K_r$，
$C_\Gamma=(r+1)I_r-\mathbf1\mathbf1^*$，其 eigenvalues 為
$1$（均勻方向）與 $r+1$（其餘 $r-1$ 維），
$C_\Gamma^{-1}=(I_r+\mathbf1\mathbf1^*)/(r+1)$。
因此 $\dim_\mathbb C Q_{P_r}=2(r+1)$，隨分叉無界增長；
此時 $\dim Q=\dim T_P$ 是容量相等，**並沒有在資料層宣告 $A=\delta$-CAR**。

## 4. 全部合法面的固定接合 $j_C$

對 $C\in\mathcal C_Q$，令 $M_C:D_B\to D_C$ 按唯一配對搬運座標：
$(M_Cb)(\mu_C(x))=b(x)$。令 $\iota_U:\mathbb C^U\otimes E_0\to
J_P=\mathbb C^I\otimes E_0$ 為零延拓。資料接合是

$$j_C:Q_P\longrightarrow D_C\oplus J_P,\qquad
                     j_C(b,u)=(M_Cb,\iota_Uu).$$

它不以 $K$、$R_C$、$A$ 或 $L$ 定義；它只讓內部 innovation 進入**source 槽**，
不把它偽裝成新的齊次初值。$M_C$ 是 $h_B$ 到 $h_C$ 的 counting isometry，
$j_C$ 為 injective；不同面共用同一 $Q_P,h_Q$，source 分量恆為 $\iota_Uu$，
且 $j_{C'}=(M_{C'}M_C^{-1}\oplus id_{J_P})j_C$。
這是資料槽的跨面關係，**不是** $R_Cj_C=R_{C'}j_{C'}$ 或守恆。

對任意 order 同構 $f:P\to P'$ 和共同 $R_0$ 的 $h_0$-unitary $V$，
座標映射送 $B,I,C,U$ 與圖邊到像集合，$C_{\Gamma'}$ 與 $C_\Gamma$
置換共軛；因此 $h_Q$ 保持且
$U^{D\oplus J}_{f,V}j_C=j_{f(C)}U^Q_{f,V}$。
這些圖、matching、線性映射不讀 $L$；所謂交換圖只限**資料**，
不宣稱後續 K 的 structured 自然性、其他面的 inverse 或 field * 已證。

### dual star 的共同起點交叉項：資料提供什麼、尚缺什麼

此輸入 $C=B=\{a\}$，$j_B$ 將根資料放在邊界槽、葉通道放在各自 source 槽，
而 $h_Q$ 的 inverse covariance 葉對為 $-I_{E_0}$。僅以日後若存在的
$R_B$ 之**符號型別**記根到第 $i$ 葉的齊次響應 $H_i$，
及第 $i$ 葉 source 到自身的響應 $D_i$。在標準 counting 座標，
$F_B=R_Bj_B$ 導出的葉對 Gram block 必有型別

$$A_B(v_i,v_j)=H_iH_j^* -D_iD_j^*,\qquad i\ne j.$$

星號在此只表示 $h_0$ 數學 adjoint；正式型別依 P0.3 的 $S=F^\dagger$。
負項來自**本稿預先固定**的通道相關；如果後續 $K$ 給
$H_iH_j^*=D_iD_j^*$，它才可能抵銷共有根的交叉項。
本稿沒有選 $H_i,D_i$、沒有代入任何 K、更沒有宣稱等式成立。
此條件仍可 FAIL；若它僅能藉 K 輸出後改 $h_Q$ 或把可比的根響應設為零才成立，
第三門檻應如實判 FAIL。只加相互獨立葉模式會缺少上述負項，
所以本資料 primitive 的作用是可明確檢查的抵銷**容量**，不是驗收結果。

## 5. 容量、無界族及固定審核目錄

對全部 P，$\dim Q_P=2(k+m)\le2N$；$U$ 與圖都由有限 predicate 生成。
若逐項序列化，$B,U,C$ 各至多 $N$ membership bits，圖的 adjacency 至多
${N\choose2}$ bits；合法面數
$1\le c_Q(P)\le {N\choose k}\le2^N$，逐面唯一配對至多
$O(k\log N)$ bits 表述，但它由圖唯一決定，**不是**逐面外加資料。
$C_\Gamma$ 為整數矩陣，對角不超過 $N$、非對角為 $0/-1$；
逆矩陣可由同一矩陣的 adjugate／determinant 精確生成，沒有 per-P
係數表。逐項輸出所需有理數 bits 可由行列式的有限 Hadamard 界估計為
$O(N\log N)$；不以「有限描述」隱藏無限精度自由參數。
新量子模式數 $2m$ 是明示的條件輸入，並非免費物理預測。

令 $\Phi(P)$ 是「不交 $k\ge2$ 份二點鏈」的 order predicate。
B-01 §5 已證它在 $D_{KQ}$，$N=2k$；每條極大鏈恰交一次的
$2^k$ 個 cut 都有唯一的逐分量匹配，所以在本版仍是 $c_Q=2^k$。
此族 $U=\varnothing$、$\dim Q=2k$，可讓資料容量隨 $N$ 無界，
且每個輸入有至少兩個面。它**不**證 $\operatorname{rank}A$ 真增長、
守恆、active K 或 field/state；這些是後續可失敗義務。

只用原 P 定義 $\mathcal I(P)=\{\{x,y\}:x\parallel y\}$，
$w_Q(C)=1$ 當且僅當 §2 的 cut 與唯一配對條件同時成立，並定
$c_{xy}^Q=\sum_{C\subseteq P,|C|=k,\,x,y\in C}w_Q(C)$、
$n_{cov}^Q=\sum_{\mathcal I(P)}1[c_{xy}^Q>0]$、
$n_{ind}^Q=|\mathcal I(P)|-n_{cov}^Q$。這是資料覆蓋分類，
**未覆蓋的不可比對在後續仍直接於原 P 全 fiber 檢查**。

| 固定輸入（方向） | $N,k,c_Q$ | $n_{cov}^Q,n_{ind}^Q$ | $m,\dim Q$ | 事前限制 |
| :--- | :--- | :--- | :--- | :--- |
| $C_3$ | $3,1,3$ | $0,0$ | $0,2$ | 無不可比對 |
| $C_4$ | $4,1,4$ | $0,0$ | $0,2$ | 多面，仍需守恆 |
| 三葉向下 star（葉為 minimal） | $4,3,1$ | $3,0$ | $0,6$ | 單面不判守恆 |
| dual star（單根在下、三葉在上） | $4,1,1$ | $0,3$ | $3,8$ | 三對葉全屬 Ind |
| $K_{2,2}$（$a_1,a_2\prec c_1,c_2$） | $4,2,1$ | $1,1$ | $0,4$ | 多根共享、無通道；$\{c_1,c_2\}$ 在原 P 直接檢查 |
| diamond $a\prec b,c\prec d$ | $4,1,2$ | $0,1$ | $2,6$ | $b,c$ 在原 P 直接檢查 |
| $2\times C_2$ | $4,2,4$ | $4,0$ | $0,4$ | 全部跨分量對覆蓋 |
| $3\times C_2$ | $6,3,8$ | $12,0$ | $0,6$ | 同上 |

無界鏈 $C_N$ 有 $c_Q=N,m=0,\dim Q=2$；無界 dual star $P_r$
有 $c_Q=1,m=r,\dim Q=2(r+1),n_{ind}^Q={r\choose2}$；
$\Phi$ 的 $k\times C_2$ 有 $c_Q=2^k,m=0,\dim Q=2k$、
$n_{cov}^Q=2k(k-1),n_{ind}^Q=0$。向下 $r$ 葉 star 有
$c_Q=1,m=0,\dim Q=2r,n_{cov}^Q={r\choose2}$。
全部是 order／圖的紙上分類，不以 K 或 CAR 結果定義審核輸入。

**CAR 容量必要條件，不預判 active 事件。** 後續若在某面有正 Gram 且
原 P 微因果，任一兩兩不可比事件集 $W$ 的真正 CAR 區塊必滿足
$\sum_{x\in W}\operatorname{rank}A_C(x,x)\le\dim Q_P$；
故其中 $A_C(x,x)\ne0$ 的事件數也不超過 $\dim Q_P$。
這由各 $S_C(E_x)$ 在正 $Q_P$ 中兩兩正交推出。
資料稿不知道哪些 $A_C(x,x)$ 非零；只在事前檢查 dual star
即使全部 $r$ 葉有 rank 2，$2r\le2(r+1)$，沒有被容量**先行**排除。
**只有 Green block 非零但 CAR 區塊為零的事件，不計入此界。**
容量通過不是微因果、非零傳播或物理 state 的證明。

## 6. 隔離、停止點與 reviewer 核對題

本稿沒有完整事件 $\delta$-CAR、逐 P 正矩陣表、per-event frame、獨立
contact、取 K 輸出後再調參，或將 $L$ 排名偷偷寫進資料。
在 dual star 即使 $\dim Q=\dim T_P$，資料只給**相關的** $h_Q$ 與 source 接合；
$A$ 必須日後由同一 K 的 $R_Cj_C$ 算出，不能在本稿先行指定。
圖相關的物理來源、創生算符及帶源 field/state 尚未交，不能叫自由真空已構造。
對任意 P、L、C，$R_C$ 是否存在、守恆、逐對微因果、Green 識別、§7(a)
逐輸入非零傳播、§7(b)(c)、rank 真增長與 state 均保持**可獨立 FAIL**。
尤其本稿縮小 B-01 面族可能使某些 P 只剩一面，不可把空洞守恆比較列 PASS。

請 reviewer 先核 §2 的唯一 matching 是否與 P0.3 的 $\beta$ 類相容，
尤其全域非空、自然性及 $\Phi$ 多面；再核 §3 正定性和
dual star 的 $-I$ 交叉 covariance、§4 的 $j_C$ injective／跨面圖，
以及 §5 的所有容量／覆蓋數和「只數 active CAR」量詞。
若資料來源或 $j_C$ 型別有問題，本版保持 draft／修訂，不改 P0.3 合約；
若後續 K 失敗，保留本資料版本與失敗，須另版資料 GO 或先修約。
正式審核前不把本稿當作資料 GO，亦不啟動第三道 K 規格或研究。
formal／E0、A／B、UNKNOWN、item7／8、6a-E、Freeze-1a 及來源隔離不變。
