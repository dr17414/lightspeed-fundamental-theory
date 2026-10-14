# X-C2-LINK-MV-v0.1 — 定案 P0.2 的 M 覆核與 V 紙上研究

狀態：**【已確認／限定解析結果：固定來源 augmented-endpoint Lebesgue M／V；物理橋接仍 OPEN】**。
模型及物理詮釋仍【探索】；複核與合併身分見§9。
Study ID `X-C2-LINK-MV-v0.1`；具名文獻參照實例 `X-C2-JOHNSTON-LINK-v0.1`。
這是契約定案後對固定文獻核的具名實例化與分析；本輪不能再稱 model ID NONE。
不是新的權重 ansatz、物質 law 或正式候選 K；沒有 scientific PASS。
全文只作紙上推導，沒有 RNG、撒點、數值／symbolic 執行或 producer。

## 1. 定案身分、定位與六欄契約

- ACT-X-0001 生效 SHA `0c386716701589c9a6b0b799636a808aacb9ade5`，僅紙上。
- [P0.2](causal_transport_c2_problem_contract_v0_2.md) 經 Claude 對 PR #81 r2
  head `b0f53948747e8770f79519396d5bce1ebbee03c6`／tree
  `3e415ff465eb08ff9c75724ee1d8e7678f579d00` 給 GO；CI #264 綠，556 passed／
  5既有warnings、integrity通過。核准 tree 原樣合併 main
  `c5bc9c6533f34c3121f793e68e3710cc9f67f6e5`；此時契約才定案。
- 受審契約 blob `7c228e6c6d586fc458310697234d7cacb9470936` 原樣保留。
  本稿遵守其全部φ、固定域、端點插入、共同Π、m=0與係數，不改M／V判準。

**M 是 Johnston 結果的覆核**，本稿補齊固定測試函數、來源頂點與可檢查誤差。
**V 才是本次主要研究義務**：以下提出共享撒點下的協方差、重疊界及趨零上界。
上述M／V已由Claude逐式複核，僅在本稿固定域與讀值內確認；
不能以M的既有文獻結果替代V，也不宣稱V是文獻上首次結果。
若任何推導不成立，保留未決／限定否定，不換權重、窗口或抹平尺度。

| 六欄 | 本研究 |
| :--- | :--- |
| 命題 | 定案P0.2的M、V是否成立？提出固定φ的平均誤差及方差上界，再推機率收斂；不是逐點、a.s.或器件實現 |
| 定義域 | 明給3+1維Minkowski、m=0；fixed bounded causally convex diamond D、x∈int D、L>0、實值φ∈C_c∞(int D)，包含φ(x)≠0；每個密度內共用同一Poisson配置 |
| 證據 | §2具名核／可測性；§3–4平均與頂點控制；§5–6聯合void law、幾何重疊與方差；§7機率量詞。均為解析，未執行 |
| 未證橋接 | 速率最優性、sampled-pair／Poisson quadrature／moving-source／器件readout、r3兩段與串接、物質／Lorentz／L0橋接仍未完成 |
| 否定條件 | 接觸來源不合法、任一步不成立或超出指定域即停止相關claim；只處理這個核／泛函，不推成所有傳輸或物質no-go |
| 後續驗證 | 逐式exact-head複核；尤其常數、單側delta質量、共用Π之joint law、近同方向／頂點及積分上界。沒有量測計畫或執行授權 |

## 2. 固定文獻實例、端點語義與矩存在

對y在x的因果未來且y≠x，令 `I_y={w:x≺w≺y}`（不含端點）；
`χ_y(Πρ)=1{Πρ(I_y)=0}`。其中≺是已給Minkowski causal order的嚴格部分。
不相關／過去／y=x時核為0。定案係數、m=0和零停止權重使參照核恰為

$$
Q_\rho(x,y;\Pi_\rho)=a_\rho\chi_y(\Pi_\rho),\qquad
a_\rho=\frac{\sqrt\rho}{2\pi\sqrt6}.
$$

沒有額外diagonal identity、長鏈貢獻、cutoff、尾部扣除或可擬合參數。
每個probe pair只向同一基礎Πρ加入該pair端點；其他probe y′不作I_y中的人造
阻擋點。這正是契約的augmented-endpoint校準族，不是一次安裝所有接收端點的器件。
Πρ本身的點若恰等於probe只涉及Lebesgue零集，不能將此泛函改稱sampled receivers。

D因果凸，使y∈D時完整I_y⊂D；沒有把區間截短。配置在bounded D內幾乎必然有限，
計數／區間指標對配置與y可測。固定配置下χ是有限個Borel條件的乘積；標準計數
measurability給聯合可測性。邊界的零volume不影響下面fixed-pair void probabilities；
不假設未來邊界有實際取樣的精確null pair。
對每個固定ρ，`|Fρ|≤L⁻²aρ∫D|φ|`，所以積分、期望與二階矩有限。
以下Fubini使用此固定ρ的絕對可積界；漸近交換另給density-independent dominator。

### 2.1 只作被動換單位，不引入新抹平尺度

取無量綱 `Y=(y−x)/L`、`κ=ρL⁴`（即契約r），並把
`f(Y)=φ(x+LY)`平滑地零延伸至R⁴。D、x、L、φ皆原先固定。
寫Y=(t,ξ)、R=‖ξ‖；令 `c₀=1/(2π√6)`、`β=π/24`。
這裡c₀是係數，非新的物理光速。

$$
F_\rho=c_0\sqrt\kappa\int_{J^+(0)} f(Y)\chi_Y\,d^4Y,
\qquad \mathbb E\chi_Y=e^{-\kappa\mathcal V_Y},\quad
\mathcal V_Y=\beta s_Y^2,\quad s_Y=t^2-R^2.
$$

點核／期望公式限Y≠0；Y=0依前述核0定義，不影響Lebesgue積分。
僅f非零處需要原D內的χ；零延伸後的幾何公式在其他點只是無貢獻的積分記號。
取事前由bounded域給出的T≥1，使所有f非零的未來點滿足t+R≤T。
T不依κ／結果；`A=‖f‖∞`、`B=sup(|∂_t f|+‖∇f‖)`為固定有限常數。

## 3. M：null座標、測試類與正規化

在未來錐內取 `u=t−R≥0`、`v=t+R≥u`、`n∈S²`，故s=uv且

$$
d^4Y=\frac{(v-u)^2}{8}\,du\,dv\,d\Omega
=\frac{(v-s/v)^2}{8v}\,ds\,dv\,d\Omega.
$$

對v>0定義

$$
H(v,s,n)=\frac{(v-s/v)^2}{8v}
f\!\left(\frac{v+s/v}{2},\frac{v-s/v}{2}n\right)
\quad(0\le s\le v^2),
$$

其餘s>v²令H=0；v=0亦令H=0。此延伸在s=v²連續，因前置Jacobian為0。
`|H|≤Av/8`，且 `H(v,0,n)=(v/8)f(v/2,vn/2)`。
令 `q=√κ s`，得到沒有遺失vertex或cross-cone測試的公式

$$
\mathbb EF_\rho=c_0\int_{S^2}\!d\Omega\int_0^T\!dv
\int_0^\infty\!dq\ e^{-\beta q^2}H(v,q/\sqrt\kappa,n).
$$

對v>0逐點極限H→H(v,0,n)；`Av e^(−βq²)/8`可積。
因此dominated convergence涵蓋v→0的來源頂點，不要求φ在來源消失。
直接Gaussian積分給 `I₀=∫₀∞e^(−βq²)dq=√6`，所以 `c₀I₀=1/(2π)`。
極限為

$$
\frac1{2\pi}\int_{S^2}\!d\Omega\int_0^T\frac v8 f(v/2,vn/2)\,dv
=\frac1{4\pi}\int_{S^2}\!d\Omega\int_0^\infty R f(R,Rn)\,dR
=F[\varphi].
$$

最後一式是契約給定 `θ(t)δ(t²−R²)/(2π)` 的作用：R>0的正根為t=R，
delta因子1/(2R)與球體measure R²相乘；R=0附近留下R dR可積，不多出接觸項。
**單側Gaussian質量已由I₀計入**，不再乘一個θ(s)δ(s)的慣例半因子。
這是Johnston無質量平均的文獻覆核，不是新的傳播機制。

## 4. M：可檢查平均誤差，包含來源點

對0≤s≤v²，Jacobian的s導數絕對值≤1/(4v)，而f沿s的導數≤B/(2v)。
故H的s導數絕對值≤`A/(4v)+B/16`。
在s=v²連續接零的延伸仍給所有s≥0的界

$$
|H(v,s,n)-H(v,0,n)|\le s\left(\frac A{4v}+\frac B{16}\right).
$$

為控制v=0，對κ≥1只在**證明積分**分割 `d=κ^(−1/4)≤1≤T`，
不修改物理讀值、φ、D或kernel。在0<v<d用`|H−H₀|≤Av/4`；
在d≤v≤T用上式與 `I₁=∫₀∞q e^(−βq²)dq=1/(2β)=12/π`。
兩部分積分給明確上界

$$
|\mathbb EF_\rho-F[\varphi]|\le e_M(\kappa):=
\frac{4\pi c_0}{\sqrt\kappa}
\left[\frac{AI_0}{8}+I_1\left(
\frac A4\log(T\kappa^{1/4})+\frac{BT}{16}\right)\right].
$$

小v項使用∫₀^d v dv=d²/2；大v項使用∫d^T dv/v=log(T/d)，
並以T上界T−d。因此e_M→0；每個固定合法(D,x,L,φ)都可對任意ε選r₀，
依序適用全部更高密度，正是定案M。來源附近沒有事後刪除或縮窗口。
此保守界是O(κ⁻¹ᐟ²logκ)，不聲稱最優或所有未限制φ共同的density cap。

## 5. V：共享Π的精確聯合law與幾何重疊

以下聯合law限於rescaled D內的未來Y、Z；零延伸後只在f(Y)f(Z)非零處使用，
其餘乘積記0。以無量綱volume記 `W(Y,Z)=|I_Y∩I_Z|`。
兩個χ同時為1恰是**同一Π**在I_Y∪I_Z中無點，所以

$$
\mathbb E(\chi_Y\chi_Z)=e^{-\kappa(\mathcal V_Y+\mathcal V_Z-W)},\qquad
C_\kappa(Y,Z):=\operatorname{Cov}(\chi_Y,\chi_Z)
=e^{-\kappa(\mathcal V_Y+\mathcal V_Z)}(e^{\kappa W}-1).
$$

因此Cκ≥0，且聯集至少包含較大的單區間，給

$$
0\le C_\kappa(Y,Z)\le e^{-\kappa\max(\mathcal V_Y,\mathcal V_Z)}.
$$

沒有獨立link假設。即使Y、Z可比較，上式仍屬契約的pairwise endpoint insertion；
若把另一probe插進同一augmented causet作阻擋點，會換joint law，不能搬用此證明。
由§2矩存在，

$$
\operatorname{Var}F_\rho=c_0^2\kappa\iint f(Y)f(Z)C_\kappa(Y,Z)\,d^4Yd^4Z.
$$

### 5.1 重疊引理：不同null方向只有來源附近可重疊

寫Y=(t,Rn)、Z=(t′,R′n′)，u=t−R、u′=t′−R′。
對w=(τ,ξ)∈I_Y∩I_Z，future causality給‖ξ‖≤τ，且

$$
\tau-n\!\cdot\xi\le u,\qquad
\tau-n'\!\cdot\xi\le u'.
$$

這由 `t−τ≥‖Rn−ξ‖≥R−n·ξ` 及另一式直接得出。
令 `h=2−‖n+n′‖`；不同n,n′時h>0。相加得到hτ≤u+u′，
故重疊區包含在 `0≤τ≤(u+u′)/h, ‖ξ‖≤τ`，volume最多

$$
W\le\frac\pi3\left(\frac{u+u'}h\right)^4.
$$

使用同一rescaling `q=√κ uv`、`q′=√κ u′v′`，得到

$$
\kappa W\le\frac\pi{3\kappa}
\left(\frac{q/v+q'/v'}h\right)^4.
$$

固定正v,v′、有限q,q′、不同方向時右側→0。完全同方向、v=0等零measure集
不能當作獨立性理由；下面先給integrable dominator，再量化其鄰域。

### 5.2 全域可積界與V的定性結論

將兩份volume都轉換為q、v、n，κ與兩個κ⁻¹ᐟ² Jacobian抵消：

$$
\operatorname{Var}F_\rho=c_0^2\int HH' C_\kappa\,
dq\,dq'\,dv\,dv'\,d\Omega\,d\Omega'.
$$

H或H′為0的點無貢獻；其餘 `κ𝒱_Y=βq²`、`κ𝒱_Z=βq′²`。
不要求f非負；用絕對值後的dominator為

$$
c_0^2\frac{A^2vv'}{64}\,e^{-\beta\max(q^2,q'^2)}.
$$

它可積，因
`∫∫₀∞e^(−βmax(q²,q′²))dq dq′=2∫₀∞q e^(−βq²)dq=1/β`。
配合§5.1的κW→0，幾乎處處Cκ→0，dominated convergence給Var Fρ→0。
注意「幾乎處處」此處指積分變數的Lebesgue／sphere measure，**不是撒點a.s.收斂**。

## 6. V：近同方向與頂點的明確上界

先積分上面dominator，取得所有κ的保守全域界

$$
K_0=\frac{c_0^2A^2}{64}\left(\frac{T^2}{2}\right)^2
\frac{(4\pi)^2}{\beta}=\frac{A^2T^4}{16\pi},
\qquad \operatorname{Var}F_\rho\le K_0.
$$

對κ≥1，僅為證明分割取 `d=κ^(−1/20)`、`g=κ^(−1/20)`、`Q=κ^(1/20)`。
不是新的smearing／nonlocality scale：原kernel與φ完整保留。
先以|HH′|Cκ上界方差，再用壞區域的union上界拆分積分；各行的比值均相對K₀：

| 區域 | 相對上界與理由 |
| :--- | :--- |
| v<d 或 v′<d | ≤2d²/T²；∫₀^d v dv=d²/2，另份≤T²/2 |
| h<g | ≤g；固定n的sphere cap面積為2π(2g−g²/2)≤4πg，因h=2−2cos(θ/2) |
| max(q,q′)>Q | ≤e^(−βQ²)；max-q尾積分為2∫Q∞q e^(−βq²)dq=e^(−βQ²)/β |
| 剩餘core | v,v′≥d、h≥g、q,q′≤Q；§5.1給κW≤16π Q⁴/(3κd⁴g⁴)=(16π/3)κ⁻²ᐟ⁵ |

令 `B₀=16π/3`。κ≥κ_*:=max{1,B₀^(5/2)}時core的κW≤1，故
`e^(κW)−1≤e κW`，Cκ≤e B₀κ⁻²ᐟ⁵ e^(−β(q²+q′²))。
以全域dominator積分上界core，得到

$$
\operatorname{Var}F_\rho\le K_0\left[
\frac{2\kappa^{-1/10}}{T^2}+\kappa^{-1/20}
+e^{-\beta\kappa^{1/10}}+eB_0\kappa^{-2/5}\right]
\quad(\kappa\ge\kappa_*).
$$

以此右側定義大κ的e_V，較小κ取K₀，即得明確e_V(κ)→0。
可與K₀取最小值收緊，但不需它證V。這是非最優O(κ⁻¹ᐟ²⁰)界，
**沒有把有限度數、典型links獨立或固定角間距加進模型**；近同方向和來源仍在內。
因此對每個原固定合法輸入、每個ε>0，存在r₁使全部更高κ的Var≤ε²。

## 7. M、V的共同後果與結論上限

對任意固定合法(D,x,L,φ)及ε,δ>0，因e_M,e_V→0，可選r₂使所有κ≥r₂
同時有e_M≤ε/2、e_V≤δε²/4。由Chebyshev及bias分離，

$$
\mathbb P_\rho(|F_\rho-F[\varphi]|>\epsilon)
\le\mathbb P_\rho(|F_\rho-\mathbb EF_\rho|>\epsilon/2)
\le\frac{4\operatorname{Var}F_\rho}{\epsilon^2}\le\delta.
$$

這恰是定案契約的機率量詞。沒有跨密度coupling，不報a.s.；
沒有對無限制的全部φ共同一個r₂，也不把scalar分布的弱收斂升格為逐點或sampled-pair。
所有T、A、B、L及尺度都來自已固定外部校準，沒有density或kernel參數擬合。
粗上界不能用於主機／資源資格化、item7 ADOPT或formal power；沒有執行預算。

本稿若獲數學GO，可限定確認此**固定文獻核＋augmented-endpoint Lebesgue泛函**
的M、V與上述機率收斂。它不證獨立器件、single-shot operational response、
sampled源／探測器、量子state／measurement、moving source、有限ρ可用誤差、
spinor／Dirac、物質選幾何、背景／維度／c湧現。只由這個泛函的V不能關閉B6。
替換回訊研究C2仍須重證r3兩段、同一無回應對照、串接、完整紀錄及來源，
C1／C3–C6仍為外加。Gate0／B1–B7、item7／8、6a-E、Freeze-1a現狀不變。

## 8. 文獻、來源與複核清單

- [Johnston 2008，arXiv:0806.3083v2](https://arxiv.org/pdf/0806.3083)，本輪重讀
  §3.1–3.3／(3.33)、(3.35)–(3.44)：用於固定核與平均基線，M明列為覆核。
- 本輪另外搜得並讀 [Dowker–Henson–Sorkin，arXiv:1009.3058v2](https://arxiv.org/pdf/1009.3058)
  §2–3.2及結論相關文字；該文已討論source／detector的links與漲落。
  它的worldline／sampled detector讀值不同於本稿fixed-source Lebesgue泛函，
  不搬用它的近似／variance界當本稿證明，不引入其器件、參數或source法則。
  不宣稱本稿是因果集無質量傳輸／低漲落的首次發現；完整novelty文獻盤點未做。

本稿M／V每一步有上述直接短證明，不以文獻摘要或初步simulation替代。
研究由定案契約與操作者指示而選，解析分割常數為作者證明策略，非模型調參；
新來源與決策見EXP-0033–0034。既有endpoint／witness／probe／UNKNOWN不覆寫，
沒有用這些資料選核、φ、bound或cap；不宣稱blind／candidate-independent。

複核需檢查：kernel／endpoint語義；Borel／矩與Fubini；null Jacobian及vertex；
單側質量與M導數界；聯合void law／union；重疊hτ界與volume；近同方向cap、
q尾與K₀常數；core threshold及Chebyshev量詞。若出錯保留受審head／理由，
不在看到計算後換model或criterion。本稿沒有作數值、RNG或新的symbolic檢查。


## 9. PR #82 複核與限定升格（2026-10-14）

Claude對head `1e067c63e34e9afa8909f6604698beeff8b1f80e`／tree
`3b53b07af0691de2b2d19056afc17469b698761b` 給GO，逐式手算核對M／V，
未另作數值／符號檢查；本人申報原句見EXP-0035。CI #266綠，556 passed／
5個既有warnings及integrity通過，原樣合併 main
`f43762f2917a3b2ce86782d1b4de033b2075da3f`，tree與GO相同。
本次只更正審核狀態與追加作用域，不改§2–7任何證明、公式或原契約。

限定確認的是fixed-source、augmented-endpoint Lebesgue泛函的M、V與機率收斂。
連續probe積分對不同方向細區間作平均，是V趨零機制的一部分；
它不是原生撒點探測器求和的證明，也沒有生成物質、裝置、r3回訊或背景／c。
模型／物理詮釋仍探索，原物理與formal OPEN不關閉。
下一份[P0.3問題契約](causal_transport_c2_problem_contract_v0_3.md)只固定原生點求和
及M_D／V_D量詞，尚未定案或推導；不從本稿直接挪用矩或方差界。
