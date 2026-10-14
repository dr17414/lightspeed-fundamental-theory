# X-CAUSAL-TRANSPORT-C2-P0.3 — 原生撒點探測讀值的問題契約

狀態：**【提案／只定問題，待 exact-head 複核】**。
本稿事前固定離散讀值、權重、校準域與量詞；不開始 M_D／V_D 推導，
不提出新傳播核、物質或裝置 law，不作可執行模型。**本問題新 model ID NONE**；
既有 `X-C2-JOHNSTON-LINK-v0.1` 參照實例與兩個回訊模型不因這句而消失。

## 1. 生效與來源身分、六欄契約

- ACT-X-0001 生效 commit `0c386716701589c9a6b0b799636a808aacb9ade5`、tree
  `c8e4e6ffae89718f77cc70431423244b88b53e79`，仍為 ACTIVE-PAPER-ONLY。
  生效時間 UTC 2026-10-12 09:57:23／台北17:57:23；本稿不擴張權限。
- Claude 核准 PR #82 head `1e067c63e34e9afa8909f6604698beeff8b1f80e`、tree
  `3b53b07af0691de2b2d19056afc17469b698761b`；CI #266 綠後原樣合併 main
  **`f43762f2917a3b2ce86782d1b4de033b2075da3f`**，tree 與 GO 相同。
  這是本稿基線，不是新的 activation。
- [P0.2 原契約](causal_transport_c2_problem_contract_v0_2.md) blob
  `7c228e6c6d586fc458310697234d7cacb9470936` 全文不改。
  [M／V 研究](c2_johnston_link_mv_study_v0_1.md) 的已核准結果，只限 fixed-source、
  augmented-endpoint 的 **Lebesgue 積分**；不直接授予本稿的離散求和任何結論。
- 本題承接操作者轉交的 Claude 建議：把接收點改為同一次撒點中的原生點。
  不改核、不抽樣來源，不把這個讀值稱已實現的物理探測器；接觸來源見 EXP-0035–0036。

| 六欄 | 本契約 |
| :--- | :--- |
| 命題／問題 | 下述原生點求和是否具有同一連續推遲分布的期望極限，以及絕對方差趨零？兩項各自可證、限定否定或未決，不預填成功 |
| 定義域 | 明給3+1維Minkowski、m=0、固定因果凸diamond／來源／尺度／測試函數；同一Poisson配置同時作接收點與阻擋點，密度趨無限 |
| 證據 | 已複核的P0.2校準積分、原文DHS §3.2的不同source-detector問題，以及Poisson Mecke工具的適用前提；均不當本題的矩／收斂證明 |
| 未證橋接 | 可測性、矩、原生點一／二點聯合法則、M_D／V_D與誤差；來源／裝置動力學、r3回訊、L0／物理橋接另列，互不代替 |
| 否定條件 | 任一義務不成立或無法證明，逐項記限定否定或OPEN；不得以改權重、測試類、窗口、歸一化或收斂型別製造成功 |
| 後續驗證 | 契約exact-head GO並合併後，才另交具名紙上研究；本輪沒有推導、撒點、RNG、新數值／符號診斷、producer、seed、主機或量測 |

## 2. 固定背景、來源及接收點

使用 (+---)、`□=∂_t²−∇²`、ℏ=c=1，m固定為0。
固定 bounded causally convex Minkowski diamond D、x∈int D、L>0，
以及實值、無量綱 `φ∈C_c^∞(int D)`；全部不依ρ、配置或結果改變。
測試類包含 φ(x)≠0、跨光錐及有正負號的函數；不排除來源頂點以方便證明。

Πρ 是 D 內相對 d⁴y 強度為ρ的 homogeneous Poisson 配置。
**只有來源 x 是外加的固定端點**；接收點恰為 Πρ∩D，不另加 probe grid，
不使用獨立的探測器Poisson配置，不條件化「接收點已存在」或「已有連結」。
同一ρ的全部讀值共用同一Πρ，不把每個點或每對點重抽。
密度ρ是外加已知強度，不從點數或讀值估計；κ=ρL⁴只作無量綱密度。
未指定跨ρ的coupling，不能據此宣稱幾乎必然收斂。

探測窗口是事前固定的 `K=supp φ⊂int D`，用給定背景座標定義，
並非只由order給出的鐘窗口或可操作器件。仍可把求和寫在全部D上，K外φ=0。
**K內和K外的所有Πρ點均保留為可能的區間阻擋點**，不能只在K中判link。
D因果凸使完整 `I(x,y)={w:x≺w≺y}` 落在D內，不截短區間。
≺是給定Minkowski causal order的嚴格部分，端點不在I中。

## 3. 構造前固定的離散讀值與權重

只沿用P0.2固定文獻核：因果未來、y≠x時為 `aρ` 乘link指標，
其他點核為0；`aρ=√ρ/(2π√6)`，停止權重b=0。沒有長鏈項、identity、
mass、cutoff、額外smearing或可擬合自由參數。核的結構部分只看order／link；
ρ與單位是外加校準，φ是外部讀值權重，不回傳進核以改傳輸法則。

令原生點的指標為

$$
\chi^{\mathrm{nat}}_{x,y}(\Pi_\rho)
=\mathbf 1\{x\prec y\}\,
 \mathbf 1\{(\Pi_\rho\setminus\{y\})(I(x,y))=0\},\qquad y\ne x,
$$

並令y=x時為0。`Πρ\{y}`只明示排除該讀值自己的接收端點；
其他所有原生接收點留在配置中。若y′位於I(x,y)，它會阻擋x→y；
不能將全部接收點先刪掉再判link。來源x也不作求和中的接收點。

本題的隨機讀值**固定定義**為

$$
S_\rho[\varphi]
=L^{-2}\frac{a_\rho}{\rho}
 \sum_{y\in\Pi_\rho\cap D}\varphi(y)
       \chi^{\mathrm{nat}}_{x,y}(\Pi_\rho).
$$

這是新問題的誤差對象規格，並非本稿已計算的期望或方差。
`ρ⁻¹`是事前指定的體積求積歸一化；它與L⁻²、aρ使Sρ無量綱。
不以隨機點數N、實現的link數或成功回應數代替ρ，不除以N或條件化N>0。
空配置讀值為0；未連結的點以0貢獻保留，不按有無接收挑選配置。
φ可有符號，Sρ是校準的scalar讀值，不是計數機率、量子測量或可讀裝置law。
測試函數、窗口、歸一化及單一／聯合配置的規則一律不能依結果調整。

## 4. 連續目標與逐項量詞

沿用同一外加連續目標：令z=y−x、s=z_t²−‖z_space‖²，

$$
G^{(4)}_{R,0}(z)=\frac{\theta(z_t)}{2\pi}\delta(s),\qquad
F[\varphi]=L^{-2}\langle G^{(4)}_{R,0}(\cdot-x),\varphi\rangle.
$$

不重新調正規化，也不換到1+1維或m>0。目標是3+1維無質量的錐面支持；
因果支持的「不超過c」與此錐面弱極限分開，均不推出背景或c已湧現。

### 4.1 M_D：離散讀值的期望收斂

$$
\forall(D,x,L,\varphi)\ \forall\epsilon>0\ \exists\kappa_M<\infty
\ \forall\rho>0:\quad
\rho L^4\ge\kappa_M\ \Longrightarrow
|\mathbb E_\rho S_\rho[\varphi]-F[\varphi]|\le\epsilon.
$$

輸入域為§2的全部固定合法輸入；門檻可依該組輸入、ε，不依配置／結果。
下一份須證此原生點讀值的期望公式與交換是否合法，不能直接把隨機求和
當Lebesgue積分。若確實可接回P0.2的M，須先證這一橋接；本稿不先作等同。
解析誤差界 `e_M(D,x,L,φ;κ)→0` 與其適用門檻需給出；若只得到定性極限，
須把可檢查速率另列OPEN，不虛構有限密度或資源cap。

### 4.2 V_D：同一次撒點的絕對方差

$$
\forall(D,x,L,\varphi)\ \forall\nu>0\ \exists\kappa_V<\infty
\ \forall\rho>0:\quad
\rho L^4\ge\kappa_V\ \Longrightarrow
\operatorname{Var}_\rho(S_\rho[\varphi])\le\nu.
$$

V_D是獨立義務；不預設成立，不由M_D或已證Lebesgue V代答。
要求絕對方差，不用相對變異係數，因為F可能為0且φ可能變號。
後續須提出可檢查的上界／速率，或明列只證定性極限、速率OPEN；
若趨零不成立，給指定讀值／合法輸入的限定否定，不能改成較弱目標以稱成功。

只有M_D、V_D及矩前提都證明後，才另推
`∀固定輸入 ∀ε>0 ∀δ>0 ∃κ_P ∀ρ>0: ρL⁴≥κ_P ⇒
Pρ(|Sρ−F|>ε)≤δ`。門檻可依輸入、ε、δ，不依配置。
不聲稱a.s.、光錐逐點值、對全部φ共同門檻、增長D或變動來源的uniform收斂。

## 5. 下一份研究必須補的機率與誤差義務

1. 先證配置／端點的可測性、一階及二階矩與所有求和／積分／期望交換；
   固定ρ矩存在不代替ρ→∞時的控制。正負φ須有絕對可積或正負部分的處理。
2. 若使用單點／多點Mecke或Palm工具，明訂加入端點後的配置與完整區間。
   同一個原生點在自己的link中是端點，在另一個link中可能是阻擋點；
   不沿用P0.2逐pair加入probe而不阻擋其他pair的約定。
3. 二階矩須分清同一接收點 `y=z` 的自相關與不同點 `y≠z` 的項。
   後者不能省略兩個接收端點彼此阻擋，以及共有區間／背景點的相關；
   不假設獨立link、獨立方向或獨立探測點。這裡不先寫本題的矩公式／上界。
4. 必須包含來源頂點、近同方向、近光錐、所有支持及有符號φ，不能以
   排除頂點、縮窗口或density-dependent測試函數替代既定量詞。
5. 若原結果確可轉用，逐項證轉用條件；將所得定位為校準延伸／文獻覆核。
   不為使研究顯得困難宣稱有新no-go，不以V_D尚未證明推斷它不成立。

本契約不提供上述問題的解答。若出現需要改讀值／取樣域／權重的證據，先保留
本題原規格與否定／未決，再在新構造前另立版本；不覆寫P0.2或本題結果。

## 6. 物理上限、資料隔離與停止條件

原生點求和比連續probe積分更接近因果集合內的接收點，仍只是條件式X-C校準。
固定來源、背景／體積單位、Poisson law、φ及ρ⁻¹讀值均外加；本題未選出器件、
時鐘、狀態、接收／回應法則或物質。即使M_D／V_D成立，也不等於粒子軌跡、
完整訊號或r3回訊；若用於取代回訊研究C2，仍須另證兩段依賴、同一無回應
對照、串接、完整紀錄及其來源。C1／C3–C6與B1–B7未證橋接保留。

僅紙上；不撒點、不用RNG、不作新數值／symbolic探索、不呼叫E4／selector／
causet producer，不產生seed、開主機、量測、receipt或formal attempt。
既有回歸測試、integrity與文件保留檢查只作repo驗證，不作本題證據。
保留E0的禁止資料、oracle、sealed／planted禁回流及UNKNOWN隔離；
若無法排除禁止／未知來源的影響，暫停相關分支並記帳，不能以純紙上免除。
任何正式候選資格／判準變更另依E0、新版prereg、曝光mapping及合資格審查處理。
item7仍不可ADOPT、item8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING；
本題沒有scientific PASS或任何正式資格授予。

## 7. 文獻與複核順序

- [DHS，arXiv:1009.3058v2](https://arxiv.org/pdf/1009.3058)，本輪只重讀§3.2的
  接收端點、阻擋與相關漲落處理。其來源世界線及探測讀值不同，不搬其近似／
  方差界作本題證明，不加入其來源／器件參數，也未做完整novelty盤點。
- [Last–Penrose，Lectures on the Poisson Process（2017作者稿）](https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf)，
  本輪限第4章Theorem 4.1、4.4陳述：Poisson、s-finite intensity、非負可測
  integrand與factorial tuples的Mecke框架。此處僅列工具前提；對本題有符號
  讀值的可積性及應用、二階端點約定仍是§5義務，不稱已證。

先複核讀值型別、端點／阻擋、自相關、deterministic歸一化、完整測試類、
目標／量詞、零值與空配置、物理上限及資料隔離。契約GO並合併後才開始
具名紙上M_D／V_D研究；本輪沒有預寫該研究或執行結果。
