# X-C2-R3-SHARED-MVPD-v0.1 — 共享撒點雙段讀值的紙上研究

狀態：**【探索／完整解析稿待 exact-head 獨立複核】**。
Study ID `X-C2-R3-SHARED-MVPD-v0.1`；Readout ID `X-C2-R3-RELAY-READOUT-v0.1`。
實例化定案契約的同一泛函，不新增傳播核、回應法則、權重或裝置前提。
本稿分別提出M、V、P、D的證明，尚未獨立確認；沒有科學執行或scientific PASS。

## 1. 定案身分、作用域與六欄

PR #86 r2在head `b4e3deb1d948645fac5f1efc527c5dabdc0a04be`、tree
`435fc3e8f1ad402b99f124011fa509fa1d74d43b` 獲Claude GO；CI #276成功後，
原樣squash合併為main **`7bc202b586167ac2eb15a12a8846ec59e90d2a9f`**，tree相同。
[問題契約](c2_r3_response_bridge_problem_contract_v0_1.md) blob
`79c34b887d645bf0555f31492d22a7dbf66f8f04` 全文不改；具名文件在合併後建立。
作者在實際合併操作前已有紙上證明策略推理，未嚴格遵守「合併後才開始推導」的先後；
此時間偏差記於EXP-0051，不以文件建立時間冒充最早推理時間，供獨立複核判斷。
ACT-X-0001生效SHA仍 `0c386716701589c9a6b0b799636a808aacb9ade5`，僅紙上。

| 六欄 | 本研究 |
| :--- | :--- |
| 命題 | 定案雙段原生點讀值的M、絕對V、固定輸入機率收斂P及單次判定D；四項構造性law比較不當作成果 |
| 定義域 | 契約全部固定輸入：3+1維m=0、bounded因果凸D、固定p／L、時間分離的W_B／W_A、任意實值光滑緊支持φ_B／φ_A；同一Π兼端點與阻擋點。D判定另限既定I_+ |
| 證據 | §3補良定性證明；§4給一致單段矩／誤差；§5精確期望與M；§6共享配置的L²比較與V；§7分別推P、D。均為紙上推導，待複核 |
| 未證橋接 | r3配對可識別性、穩定性／擾動及完整failure模型、物質器件／來源／背景實現仍OPEN；本題不報時間、延遲或距離 |
| 否定條件 | 若任一界或轉用前提不成立，保留本稿並逐項記否定／未決，不更改既定泛函、窗口或判準 |
| 後續驗證 | exact-head逐式核對，特別是一致矩、Mecke插回端點、過去／未來的有限域獨立性及Hölder指數；未授權任何新科學計算 |

來源是已核准的[單段原生點研究](c2_native_detector_mv_study_v0_1.md)與
[Lebesgue基線](c2_johnston_link_mv_study_v0_1.md)。Claude r1對M／V的粗估、r2對P→D的
推理均已接觸，記於EXP-0048／0050；提示不是證明。本稿補齊論證，不稱盲推導或新物理。

## 2. 被動換單位與同一讀值

只作Y=(y−p)/L、Z=(z−p)/L、κ=ρL⁴，D′=(D−p)/L，
f_B(Y)=φ_B(p+LY)、f_A(Z)=φ_A(p+LZ)，零延伸到整個R⁴。
設c₀=1/(2π√6)、β=π/24，Π是同一配置在D′的像，強度κ。
仍用χ_{U,V}表示完整開區間的link指標；原生端點以外所有Π點均留作阻擋。
源0固定外加。省略有零權重的窗口限制，可把和寫在Π全域：

$$
 S_\kappa^u[f]=\frac{c_0}{\sqrt\kappa}
       \sum_{Z\in\Pi}f(Z)\chi_{u,Z}(\Pi),
 \qquad B_\rho(q)=qS_\kappa^0[f_B],
$$

$$
 C_\kappa=\frac{c_0^2}{\kappa}
       \sum_{Y,Z\in\Pi}f_B(Y)f_A(Z)
       \chi_{0,Y}(\Pi)\chi_{Y,Z}(\Pi),
 \qquad A_\rho(q,g,\eta)=qg\eta C_\kappa.
$$

時間分離使有非零權重的Y、Z不同；這不是獨立撒點。
固定κ下，|Cκ|≤c₀²‖f_B‖∞‖f_A‖∞N²/κ，N為有限域Poisson計數；
所有固定階矩有限。區間計數是Borel可測，故讀值可測；有限域有符號Mecke、
求和／積分交換可先用此多項式絕對界。空配置仍為0，沒有條件化N>0。

令K_B、K_A是兩個函數的固定緊支持。選K_B的一個緊閉包鄰域U⊂int D′，
固定T≥1，使0到K_B、以及任意u∈U到K_A的未來位移都滿足v=t+|x|≤T。
有界性保證可選，T只依固定輸入；不是密度依賴窗口或新模型參數。
以下A_i=‖f_i‖∞、B_i=sup(|∂_t f_i|+‖∇f_i‖)，i=A,B。

## 3. 連續目標的正式良定性證明

r1複核給出良定性的論證，**本稿補成正式證明**；不把reviewer的一行論證冒稱
先前已有完整獨立確認的定理。令G(w)=θ(w_t)δ(w_t²−|w_space|²)/(2π)。
由其錐面配對，定義

$$
 H(Y)=\langle G(Z-Y),f_A(Z)\rangle
     =\frac1{4\pi}\int_{S^2}\int_0^\infty
          r f_A(Y+(r,rn))\,dr\,d\Omega.
$$

對Y的任一緊集，f_A的緊支持令積分只需一個共同有限r區間；
所有階導數可由同區間上的有界導數支配而移入積分。
故H∈C∞(R⁴)。在U上可取r≤T/2，所以

$$
 |H|\le h_0:=A_A T^2/8,\qquad
 |\partial_tH|+\|\nabla H\|\le h_1:=B_A T^2/8.
$$

ψ=f_B H是C_c∞(int D′)函數；A_ψ≤A_Bh₀、B_ψ≤B_Bh₀+A_Bh₁。
因此

$$
 C=\langle G(Y),\psi(Y)\rangle
   =\frac1{4\pi}\int_{S^2}\int_0^\infty r\psi(r,rn)\,dr\,d\Omega
$$

是有限、明確的分布配對，恰為契約先Z後Y的連續目標，沒有相乘同變數的兩個delta。
不需φ非負；即使C=0亦良定。ψ僅是證明中的比較函數，不替換實際f_B或讀值。

## 4. 移動固定端點的一致單段界與高階矩

### 4.1 舊界的逐項轉用

對每個**固定**u∈K_B，Sκ^u[f_A]只使用Π在J⁺(u)內的點。
u∈int D′，D′因果凸，所有區間完整，ρ已知，f_A確定且光滑緊支持。
故定案P0.3的固定來源結果適用。這不是把隨機來源直接代進原定理。

為明示一致性，令m(A,B;κ)、v(A;κ)為舊研究的單段bias／方差上界，取同一T：

$$
 m(A,B;\kappa)=\frac{4\pi c_0}{\sqrt\kappa}
 \left[\frac{A\sqrt6}{8}+
 \frac{12}{\pi}\left(\frac A4\log(T\kappa^{1/4})+\frac{BT}{16}\right)\right],
 \quad \kappa\ge1.
$$

設K₀=A²T⁴/(16π)、K₁=A²T²/(16π√6)、B₀=16π/3、κ_*=max{1,B₀^(5/2)}。
κ<κ_*時e_V=K₀；κ≥κ_*時

$$
 e_V=K_0\left[2\kappa^{-1/10}/T^2+\kappa^{-1/20}
          +e^{-\beta\kappa^{1/10}}+eB_0\kappa^{-2/5}\right],
 \qquad v(A;\kappa)=e_V+2K_1/\sqrt\kappa.
$$

平移不改A_A、B_A，且所有u共用T，故舊公式直接給

$$
 \sup_{u\in K_B}\mathbb E|S_\kappa^u[f_A]-H(u)|^2
 \le r_A(\kappa):=v(A_A;\kappa)+m(A_A,B_A;\kappa)^2\longrightarrow0.
$$

一致性來自公式的相同參數，不是未經證明地交換∀u與∃密度門檻。
同理，以ψ及來源0得到r_ψ=v(A_ψ;κ)+m(A_ψ,B_ψ;κ)²→0。

### 4.2 一致高階矩引理（保留原生端點互擋）

先對任意固定來源u、|f|≤A且未來支持v≤T，證κ≥1時

$$
 \mathbb E|S_\kappa^u[f]|^k\le H_k(A,T):=
 (c_0 A)^k\sum_{j=1}^k
       \left\{{k\atop j}\right\}(J_T\sqrt j)^j,
 \qquad J_T=\pi T^2\sqrt6/4.
$$

大括號是把k個位置分成j個非空區塊的數目，不作數值計算。
證明：以c₀A/√κ乘link數上界絕對值；展開k次方，按j個不同原生端點分組。
j點Mecke把端點插回後，若互擋則乘積為0；否則需Π在各I(u,Z_i)的聯集無點。
若其體積為V_i，聯集體積≥max V_i≥(ΣV_i)/j，因此聯合機率至多
exp[−(κ/j)ΣV_i]。不能假設links獨立；這只是上界。

用單段已用的null座標s=t²−R²、v=t+R，有d⁴Z≤(v/8)ds dv dΩ、V=βs²，故

$$
 \int_{J^+(u),\,v\le T}e^{-\lambda V(u,Z)}d^4Z
 \le J_T/\sqrt\lambda,\qquad\lambda>0.
$$

j點Mecke的κ^j、j個積分及前因子κ^(−k/2)，合給
κ^((j−k)/2)(c₀A)^k(J_T√j)^j，κ≥1時不超過所列常數，求和即得。
有限域j點Mecke亦可直接證：條件化N=n後有序不同點數為(n)_j，
Poisson機率滿足(n)_j p_n=λ^j p_{n−j}，λ=κ|D′|；積分其餘iid均勻點即得。
非負式先成立；有符號應用用§2矩界拆正負部分。

特取k=6，令E_u=Sκ^u[f_A]−H(u)、E₆=2⁵(H₆(A_A,T)+h₀⁶)。
由|a−b|⁶≤2⁵(|a|⁶+|b|⁶)，一致有E|E_u|⁶≤E₆。
Cauchy–Schwarz再給

$$
 \sup_u\mathbb E|E_u|^4
 \le [r_A(\kappa)E_6]^{1/2}.
$$

這一步補足加權二階誤差所需的高階矩，沒有從單段V直接聲稱雙段V。

## 5. M：精確期望與誤差

兩點Mecke中，Y早於Z，故插回Z不阻擋0→Y；Y是Y→Z的端點。
在0≺Y≺Z時，I(0,Y)與I(Y,Z)不相交，所以聯合void體積為兩者之和。
因此精確地

$$
 \mathbb EC_\kappa=c_0^2\kappa\iint f_B(Y)f_A(Z)
       \mathbf1_{0\prec Y\prec Z}
       e^{-\kappa(V(0,Y)+V(Y,Z))}\,d^4Yd^4Z.
$$

這不宣稱所有Y、Z的link或尾讀值互相獨立。
內積分是固定來源Y的單段期望。用§4.1的一致bias與第一段核質量界，得到

$$
 |\mathbb EC_\kappa-C|
 \le m_C(\kappa):=
 c_0 A_BJ_T\,m(A_A,B_A;\kappa)+m(A_\psi,B_\psi;\kappa)
 \longrightarrow0.
$$

故雙段M有明確bias界，非最優O(κ^(−1/2)logκ)。
Bρ的M是原單段結果乘q；Aρ的bias界乘qgη。
全體有符號權重、零目標均保留，沒有以觀測挑正效果子域。

## 6. V：共享Π下的加權L²比較

### 6.1 比較量與依賴性

定義

$$
 \widetilde C_\kappa=S_\kappa^0[\psi],\qquad
 Z_\kappa=S_\kappa^0[|f_B|]\ge0,
 \qquad
 \Delta_\kappa=C_\kappa-\widetilde C_\kappa
 =\frac{c_0}{\sqrt\kappa}\sum_{Y\in\Pi}
 f_B(Y)\chi_{0,Y}E_Y.
$$

各E_Y使用原Π的完整未來區間；沒有獨立第二配置。由加權Cauchy–Schwarz逐配置有

$$
 |\Delta_\kappa|^2\le Z_\kappa\frac{c_0}{\sqrt\kappa}
          \sum_{Y\in\Pi}|f_B(Y)|\chi_{0,Y}|E_Y|^2.
$$

下文Mecke積分只需E_B={Y∈K_B:0≺Y}；其他Y的χ_{0,Y}=0，貢獻為0。
對Y∈E_B，單點Mecke移除Y後，χ_{0,Y}=1{Π(I(0,Y))=0}，
機率p_Y=e^(−κV(0,Y))；不把spacelike Y當成機率1的空區間連結。
移除／插回Y不改其自身尾讀值：Y是尾核來源，χ_{Y,Y}=0，且f_A(Y)=0；
所以Sκ^Y(Π∪{Y})=Sκ^Y(Π)。這裡沒有把其他原生端點移除。
尾讀值E_Y只依賴Π在J⁺(Y)的限制；I(0,Y)與該域不交，
故**對固定Y**，E_Y與此incoming void事件獨立。
這個有限域Poisson獨立增量結論不包含Zκ：別的B端點仍會阻擋第二段，
Zκ與E_Y一般相關，不可把它們的期望相乘。

### 6.2 插回端點與混合矩控制

插回Y只會阻擋別的incoming links，另至多加一個自身貢獻，因而

$$
 Z_\kappa(\Pi\cup\{Y\})\le Z_\kappa(\Pi)+c_0 A_B/\sqrt\kappa,
 \quad
 \mathbb E Z_\kappa(\Pi\cup\{Y\})^4\le
 Q_4:=8[H_4(A_B,T)+(c_0A_B)^4].
$$

取Z′=Zκ(Π∪{Y})、χ=χ_{0,Y}。兩次Cauchy–Schwarz及§4.2給

$$
 \begin{aligned}
 \mathbb E[\chi Z'|E_Y|^2]
 &\le(\mathbb E[\chi Z'^2])^{1/2}
       (\mathbb E[\chi|E_Y|^4])^{1/2}\\
 &\le p_Y^{1/4}Q_4^{1/4}\,
       p_Y^{1/2}[r_A(\kappa)E_6]^{1/4}.
 \end{aligned}
$$

第一因子用E[χZ′²]≤p_Y^(1/2)(EZ′⁴)^(1/2)；
第二因子才使用上一節已證的χ與E_Y獨立性。
所以Mecke與核質量界（指數係數3/4）給

$$
 \mathbb E|\Delta_\kappa|^2
 \le t_C(\kappa):=
 \frac{2c_0A_BJ_T}{\sqrt3}\,Q_4^{1/4}E_6^{1/4}r_A(\kappa)^{1/4}
 \longrightarrow0.
$$

所有共享端點、自相關與互擋仍在原和中；此不等式控制它們的總效應，
無須把四點二階矩分解成假定獨立的links，也沒有丟掉近相切光錐。
若A_B或A_A為0，兩邊的零因子照算，原讀值為0，不以除法排除這些輸入。

### 6.3 完成V

由單段ψ結果，E|C̃κ−C|²≤r_ψ(κ)。因此

$$
 \mathbb E|C_\kappa-C|^2\le d_C(\kappa):=2t_C(\kappa)+2r_\psi(\kappa)
 \longrightarrow0,\qquad
 \operatorname{Var}C_\kappa\le d_C(\kappa).
$$

這證明原雙段讀值的**絕對V**，不是相對變異係數。
保守界為非最優O(κ^(−1/80))，來自r_A的四次根；沒有把舊O(κ^(−1/20))
直接寫成雙段速率。Bρ方差≤q²v(A_B;κ)，Aρ方差≤(qgη)²d_C。
界只依固定輸入及設定，趨零即給契約「所有更高密度」的門檻；
不要求所有測試函數、所有來源或所有C共同一個門檻。

## 7. P與D分別交代

### 7.1 P：固定輸入機率收斂

由§6的均方界，對ε>0有

$$
 \mathbb P(|C_\kappa-C|>\epsilon)\le d_C(\kappa)/\epsilon^2.
$$

任意固定輸入、ε、δ>0可取κ_P，使全部κ≥κ_P的右側≤δ。
Bρ用單段均方界、Aρ乘固定qgη同理；零設定直接為0。
這完成P，不聲稱跨密度a.s.、逐點、成長域或全函數一致收斂。

### 7.2 D：固定單次閾值，不換規則

限契約I_+、正常η=1，沿用d(a)=1{a>gC/2}，等號判0。
q=0時誤判機率恆0是構造性結果，不當新證據。
q=1時g>0可約去，誤判事件恰為{Cκ≤C/2}。故兩準備最壞誤判滿足

$$
 e_D(I,g;\rho)=\mathbb P(C_\kappa\le C/2)
 \le\mathbb P(|C_\kappa-C|\ge C/2)
 \le4d_C(\kappa)/C^2\longrightarrow0.
$$

最後一步對非負|Cκ−C|²用Markov，包含閾值等號。
這正式補出r2複核已提示的P→D連結，並給固定輸入的保守界；可對兩個g共用門檻，
但不要求所有C>0共用門檻。空配置／無返回照算，沒有重試、平均配置或成功條件化。
η=0時同一判定器輸出0；它不被要求在無回應時辨認q=1。

## 8. 結論的分量、來源與複核重點

本稿提出M、V、P、D各自的解析證據；不是把四項按構造成立的law比較當實質結果。
真正新增的數學橋接是：在同一配置、原生B來源與互擋保留時，
以一致單段誤差及高階矩控制雙段均方誤差；D隨後是固定閾值的後果。
全部待exact-head獨立複核，不能提前升格【已確認】。

界與已知單段校準有依賴，不稱新傳播機制或完整新穎性盤點；本輪未讀新文獻原文。
固定背景、密度、來源、線性即時回應、孔徑／讀出、增益、無雜訊／串音都仍是外加X-C前提。
即使本稿成立，也不證可操作校準未知C／g、器件或物質存在、配對可識別性、穩定性／
完整failure、時間／延遲／距離或c湧現；原r3 §4.3／4.4與其他物理橋接保留OPEN。
item7不可ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING不變。

作者接觸與證明策略見EXP-0051；EXP-0050逐字保存reviewer本人申報。
無RNG、撒點、數值／符號程式診斷、producer、raw／sealed、seed／主機／量測／receipt。
既有regression／integrity及版本比對只作repo驗證，不當數學證據。

複核須檢查：換單位與權重；H的所有階平滑性；移動固定來源的一致公式前提；
高階矩的分組係數與插回阻擋上界；尾讀值的未來可測性；Mecke後incoming void的獨立範圍；
Z′四階矩、兩次Cauchy–Schwarz的p^(3/4)及r_A^(1/4)；M／V／P／D量詞與等號處理。
若有缺口，保留本稿及未決／否定，不在結果後改模型、窗口、權重或判準。
