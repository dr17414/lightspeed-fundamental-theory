# X-C2-NATIVE-MV-v0.1 — P0.3 原生點讀值的 M_D／V_D 紙上研究

狀態：**【探索／完整解析推導草稿，待 exact-head 獨立複核】**。
Study ID `X-C2-NATIVE-MV-v0.1`；Readout ID `X-C2-NATIVE-READOUT-v0.1`，
實例化定案P0.3的Sρ；核仍是 `X-C2-JOHNSTON-LINK-v0.1`。
本輪已有具名紙上研究／讀值，不再稱全部實例NONE；沒有新kernel、物質／器件law或正式K。
全文只作紙上解析，沒有撒點、RNG、新數值／symbolic執行或producer，無scientific PASS。

## 1. 定案身分、定位與六欄

- ACT-X-0001生效commit仍 `0c386716701589c9a6b0b799636a808aacb9ade5`，僅紙上。
- Claude核准PR #83 exact head `7271b215ab630b6b892ddc9886aab974b40a272c`／tree
  `aa53f2b1111064f6fc0efd0815576eefd956b1ce`；CI #268綠，556 passed／5既有warnings、
  integrity通過後原樣合併main **`8a8524cdfdd34934d629547449c92d0668a34cc6`**，tree相同。
  [P0.3契約](causal_transport_c2_problem_contract_v0_3.md)此時定案，blob
  `6c77995b93e03e9090a2aef6f17ab6ff6f6e1c7f` 全文保留；合併後才開始本推導。
- [P0.2的已複核M／V](c2_johnston_link_mv_study_v0_1.md)作限定解析基線，
  不能直接等同原生讀值。本稿先證期望橋接與精確二階矩，再給新項上界。
- Claude良設性草算指出Mecke期望、同點與互相阻擋項；作者已接觸該提示，
  不稱盲推導。提示本身不是證明，來源與本人申報分別保存於EXP-0037–0038。

**定位為校準延伸，不宣稱困難的新機制或首次結果。** 本稿保留既定核、ρ⁻¹、
固定來源、完整φ類及量詞；新義務是原生點端點語義與兩個矩修正，解析待複核。

| 六欄 | 本研究 |
| :--- | :--- |
| 命題 | 定案P0.3的M_D、V_D及固定φ的機率收斂；不是a.s.／逐點／全φ一致或裝置實現 |
| 定義域 | 外加3+1維Minkowski、m=0、bounded因果凸D、x∈int D、L>0、實值φ∈C_c∞(int D)，包括φ(x)≠0／變號；同一Π兼接收及阻擋 |
| 證據 | §2可測／矩與Mecke；§3期望恆等式；§4精確二階矩；§5–6同點／阻擋絕對界；§7傳遞收斂量詞。全部紙上，未執行 |
| 未證橋接 | 本稿獨立複核、最優速率、可操作探測器／訊號／r3回訊、物質／來源動力學及背景／L0橋接仍OPEN |
| 否定條件 | 任何步驟或作用域不成立，保留本稿／理由，記限定否定或未決；不以改讀值、權重、窗口或criterion補救 |
| 後續驗證 | exact-head逐式複核，特別是Mecke端點、ordered distinct pairs、變號φ、阻擋區域與factor2；不授權量測或執行 |

## 2. 固定讀值、可測性與有限域Mecke

只作被動換單位 `Y=(y−x)/L`、κ=ρL⁴；D′=(D−x)/L，
`f(Y)=φ(x+LY)`零延伸，`c₀=1/(2π√6)`、`β=π/24`。
Π以下記此rescaled D′內強度κ的同一次Poisson配置，不是另抽的探測配置。
令E=D′∩(J⁺(0)\{0})、`I_Y={W:0≺W≺Y}`，
`𝒱_Y=|I_Y|=βs_Y²`、s_Y=t²−R²；E外指標為0。
來源0是固定插入端點，不在求和中；源／終點皆不在嚴格區間。
定案讀值與基線Lebesgue泛函恰為

$$
S_\rho=\frac{c_0}{\sqrt\kappa}\sum_{Y\in\Pi\cap E}
 f(Y)\mathbf1\{(\Pi\setminus\{Y\})(I_Y)=0\},\qquad
F_\rho=c_0\sqrt\kappa\int_E f(Y)\mathbf1\{\Pi(I_Y)=0\}\,d^4Y.
$$

Sρ是契約既定的密度歸一化求和，不除以N。D′／K′外部窗口不會移除I_Y中的點；
其他原生接收點全部留在配置中，可能阻擋另一連結。D′因果凸使完整I_Y⊂D′。
Fρ在此只作對照，不能把其人工probe插入另一pair以改基線。

取 `A=‖f‖∞`，`B=sup(|∂_t f|+‖∇f‖)`，固定T≥1使所有f非零的未來點
有v=t+R≤T，皆由事前固定輸入給定。N=Π(D′)服從Poisson(κ|D′|)，
所以 `|Sρ|≤c₀A N/√κ`，`E N²=κ|D′|+(κ|D′|)²`。
固定κ時一、二階矩有限；Fρ則有確定的有界域積分上界。這不是漸近控制。
關係 `{(W,Y):0≺W≺Y}` 是Borel；配置對其計數聯合可測，有限點和／積分
亦可測。Poisson強度無原子，配置幾乎必然simple且不含固定來源；源點值為0的
約定不要求f(0)=0。全部固定κ的有符號交換可由A、N²或有限域積分絕對界支配。

本有限域使用以下Mecke的「先移除所求和點」形式，m=2求和為**有序不同點**：

$$
\mathbb E\sum_{Y\in\Pi}g(Y,\Pi\setminus\{Y\})
=\kappa\int_{D'}\mathbb Eg(Y,\Pi)\,d^4Y,
$$

$$
\mathbb E\sum_{Y,Z\in\Pi,\ Y\ne Z}
 g_2(Y,Z,\Pi\setminus\{Y,Z\})
=\kappa^2\iint_{D'^2}\mathbb Eg_2(Y,Z,\Pi)\,d^4Yd^4Z.
$$

非負可測形式對應Last–Penrose Thm4.1／4.4；本稿的有符號應用先用上列可積性，
再拆正負部分。附錄A在本finite homogeneous域直接證這兩式，不靠記憶的定理編號。

## 3. M_D：期望橋接與已核准M的傳遞

單點Mecke移除接收點後，剩餘配置仍以原Π取期望。
來源／接收端點不在I_Y內；Poisson void law給 `pκ(Y)=e^(−κ𝒱_Y)`。故精確地

$$
\mathbb ES_\rho=c_0\sqrt\kappa\int_E f(Y)e^{-\kappa\mathcal V_Y}\,d^4Y
=\mathbb EF_\rho.
$$

對每個固定κ、全部合法有符號f均成立，沒有條件化N>0或先選link。
這才是把P0.2的M接到M_D的橋，不是將隨機求和直接替換為連續積分。
由基線研究§3–4，連續目標F[φ]及正規化不變，且κ≥1時

$$
|\mathbb ES_\rho-F[\varphi]|\le e_M(\kappa)
=\frac{4\pi c_0}{\sqrt\kappa}
\left[\frac{AI_0}{8}+I_1\left(\frac A4\log(T\kappa^{1/4})+\frac{BT}{16}\right)\right],
\quad I_0=\sqrt6,\quad I_1=\frac{12}{\pi}.
$$

e_M→0，故正是P0.3的M_D與可檢查誤差；不是新平均傳播機制。
包含來源頂點及完整φ類的控制由**已證橋接後**的原M傳遞，不刪φ(0)≠0的情形。

## 4. V_D：原生端點的精確二階矩

以下雙積分在E²，對角Y=Z的Lebesgue measure為0；其原生同點項另算。
令 `W(Y,Z)=|I_Y∩I_Z|`、`U(Y,Z)=𝒱_Y+𝒱_Z−W`，
以及阻擋集合 `𝒞={(Y,Z):Z∈I_Y 或 Y∈I_Z}`。
雙點Mecke移除Y、Z後，測試Y的link須把Z插回，測試Z的link須把Y插回。

- 在𝒞上，插回的另一接收點已是阻擋點，兩個link不可能同時成立，乘積為0。
- 在𝒞外，兩個插回端點都不阻擋，乘積為同一Π在I_Y∪I_Z的void指標，
  其期望為 `e^(−κU)`，沒有獨立link假設。
- 同一接收點的指標平方等於本身，單點Mecke給自相關項。

因此二階矩及方差恰為

$$
\mathbb ES_\rho^2
=c_0^2\int_E f(Y)^2p_\kappa(Y)\,d^4Y
 +c_0^2\kappa\iint_{E^2}f(Y)f(Z)\mathbf1_{\mathcal C^c}e^{-\kappa U}\,d^4Yd^4Z,
$$

$$
\operatorname{Var}S_\rho=\operatorname{Var}F_\rho+D_\kappa-J_\kappa,
\qquad D_\kappa=c_0^2\int_E f(Y)^2p_\kappa(Y)\,d^4Y,
\qquad J_\kappa=c_0^2\kappa\iint_{\mathcal C}f(Y)f(Z)e^{-\kappa U}\,d^4Yd^4Z.
$$

最後一式使用§3的相同期望，以及基線的joint void `e^(−κU)`；所有固定κ交換
已由§2支配。Dκ≥0，但**有符號f的Jκ不先假定非負**。不能宣稱阻擋必然降低
完整方差；下面給|Jκ|上界，也不把原生不同點covariance誤稱全為非負。

## 5. 同點自相關：涵蓋頂點的明確界

用基線的null座標u=t−R、v=t+R、s=uv，0≤s≤v²、v>0，

$$
d^4Y=\frac{(v-s/v)^2}{8v}\,ds\,dv\,d\Omega
\le\frac v8\,ds\,dv\,d\Omega.
$$

f非零處的未來支持v≤T；上界時把s積分延伸至∞，q=√κs。
來源頂點v=0為零measure，鄰域由v dv可積控制，沒有移除其周圍。

$$
0\le D_\kappa\le\frac{c_0^2 A^2\pi T^2}{4\sqrt\kappa}
\int_0^\infty e^{-\beta q^2}\,dq
=\frac{K_1}{\sqrt\kappa},\qquad
K_1=\frac{c_0^2 A^2\pi T^2 I_0}{4}
=\frac{A^2T^2}{16\pi\sqrt6}.
$$

使用4π的角積分與 `∫₀^T v dv/8=T²/16`，因而係數為πT²/4。
不要求固定角間距、遠離來源或f為正；Dκ就是新增的同點shot-noise項。

## 6. 互相阻擋：用完整區間體積控制

在 `Z∈I_Y` 子域，order的遞移性給I_Z⊂I_Y，故U=𝒱_Y。
另一個方向Y∈I_Z與它互換；兩方向不重合，因偏序無環。
Jκ用有序pair，所以下面的factor2恰是這兩種方向，不是再乘兩次。
用絕對值與|f|≤A，並保留較遠端點的f支持v≤T，得到

$$
|J_\kappa|
\le2c_0^2\kappa\int_E |f(Y)|e^{-\kappa\mathcal V_Y}
          \int_{I_Y}|f(Z)|\,d^4Z\,d^4Y
\le2c_0^2\kappa A^2\int_{0\le u\le v\le T}
          \mathcal V_Y e^{-\kappa\mathcal V_Y}\,d^4Y.
$$

內積分以**完整**I_Y體積上界；即使某點不在φ窗口也未被移除作阻擋點。
因果凸保證區間不截短；把外積分擴到完整null座標域只是正函數上界。
由𝒱_Y=βs²、同一Jacobian上界、q=√κs，

$$
|J_\kappa|\le
\frac{c_0^2 A^2\pi T^2}{2\sqrt\kappa}\,
\beta\int_0^\infty q^2e^{-\beta q^2}\,dq
=\frac{K_1}{\sqrt\kappa}.
$$

此處 `2β∫₀∞q²e^(−βq²)dq=I₀` 由積分
`∫₀∞(q e^(−βq²))′dq=0` 得到，邊界0及∞都為0。
這證明草算所指的O(κ⁻¹ᐟ²)，並給明確常數；不依賴links／方向／接收點獨立。

## 7. V_D與機率量詞、結論上限

令e_V為基線研究§6已核准的Lebesgue上界：K₀=A²T⁴/(16π)、B₀=16π/3，
κ_* = max{1,B₀^(5/2)}；κ<κ_*時取e_V=K₀，κ≥κ_*時取

$$
e_V(\kappa)=K_0\left[\frac{2\kappa^{-1/10}}{T^2}
 +\kappa^{-1/20}+e^{-\beta\kappa^{1/10}}+eB_0\kappa^{-2/5}\right].
$$

§4–6現在才把該界轉到原生讀值：

$$
0\le\operatorname{Var}S_\rho
\le e_{V_D}(\kappa):=e_V(\kappa)+\frac{2K_1}{\sqrt\kappa}
\longrightarrow0.
$$

對每個固定合法輸入和ν>0，存在κ_V使**所有**κ≥κ_V的方差≤ν，
是定案V_D。新兩項界更快趨零，但整體保守界仍是O(κ⁻¹ᐟ²⁰)，不稱最優。
沒有事後改核、φ、窗口、ρ⁻¹或放寬目標。
給任意ε,δ>0，因e_M、e_(V_D)都趨零，可選κ_P≥max{1,κ_*}使所有κ≥κ_P
有e_M≤ε/2及e_(V_D)≤δε²/4。由§3與Chebyshev，

$$
\mathbb P_\rho(|S_\rho-F[\varphi]|>\epsilon)
\le\frac{4\operatorname{Var}S_\rho}{\epsilon^2}\le\delta.
$$

κ_P只依固定D、x、L、φ、ε、δ，不依配置；沒有跨ρcoupling，不報a.s.，
不對無限制全部φ取共同門檻，也不報光錐逐點值或增長域／變動來源的uniform結果。

若本稿獲GO，限定確認的是**定案密度歸一化、固定來源、原生點校準求和**的
M_D／V_D及機率收斂，已比連續probe泛函多處理同點／互相阻擋，仍不是器件實現。
背景、單位、強度、來源、平滑權重及讀值全外加，不生成鐘、接收／回應law、
物質、量子measurement或c／signature／時空。r3兩段依賴、無回應對照與串接
均未證，C1／C3–C6、B1–B7、item7／8、6a-E、Freeze-1a與所有formal OPEN不關閉。
界不作有限密度資源資格、power、seed／主機／量測或scientific PASS授權。

## 8. 文獻、接觸與複核清單

- [Last–Penrose 2017作者稿](https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf)，
  Thm4.1／4.4的有限域工具。沿用EXP-0036已讀的限定陳述；本輪嘗試重讀PDF逾時，
  不稱新讀全文，另讀[作者書頁](https://stoch.math.kit.edu/english/297.php)核對版本。
  本稿附錄A直接證所用finite-domain形式，所有有符號應用另證可積。
- Johnston／DHS不在本輪重讀，沿用P0.3與基線的有限作用域；沒有挪用DHS
  source-worldline／器件的近似或方差結論，不做完整novelty宣告。

原P0.2／P0.3、基線M／V、r3與全部actor申報保持原版本。
Claude本人良設性草算按原句記為接觸，沒有事後寫成其完整證明；新對話不重置舊曝光／
UNKNOWN。作者紙上推導及有限文獻／檔案接觸見EXP-0038；無新raw／sealed／endpoint、
producer、RNG、撒點、數值／symbolic診斷。既有regression／integrity只作repo驗證。

複核請檢查：simple／端點與可測性；signed Mecke的可積性；有序pair及同點；
兩端點插回的阻擋；Var S=Var F+D−J；full interval nesting及factor2；
K₁的null Jacobian／Gaussian矩與頂點；傳遞舊M／V的作用域及Chebyshev量詞。
不以CI代替數學複核；若發現缺口保留head／理由及未決，不改criterion補成功。

## 附錄 A. 所用Mecke形式的有限域短證明

令λ=κ|D′|>0，p_n=e^(−λ)λ^n/n!。條件N=n時，Π是n個獨立uniform(D′)點；
無原子強度使重複點為零機率。對非負可測g，條件和的n項同分布；
`n p_n=λ p_(n−1)`把刪掉一點後的n−1點配置重新混合成同一Poisson law。
被刪點的uniform積分 `λ dY/|D′|=κ dY`，即§2第一式。
不同點**有序**和有n(n−1)項；`n(n−1)p_n=λ²p_(n−2)`同樣重新混合
剩餘n−2點，而兩個被刪點給κ²dYdZ，即第二式。零／一點情形自然無相應項。
非負形式可用Tonelli；有符號g、g₂須先有絕對可積，再由正負分解得到。
本稿§2的固定κ界與有限域保證每次應用合法，不把該證明當密度極限的支配界。
