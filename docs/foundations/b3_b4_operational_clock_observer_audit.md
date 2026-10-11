# B3＋B4：可操作的時鐘與觀察者等價之前提審計

狀態：**【探索／限定解析待獨立複核；物理橋接 OPEN】**。
基線：PR #72 squash main `044879b8532d5ff89752fd221dc3271bf425a4a7`，
tree `7c4341e2e650682d23150c151203a945ba3a2bb4`。
承接 [B2＋B5](b2_b5_interval_volume_cone_audit.md) §4–§7 與
[T1＋T5](t1_t5_premise_audit.md) 的 B3／B4 義務。
這是給定 continuum countermodel 的紙上審計；所有座標、metric 和 marked observer
均是檢查蘊涵的外部輸入，不是 L0 模型、新 order ansatz 或候選 K 的構造材料。
不抽樣、不量測、不產生 seed、不開主機、不執行 E4／selector witness 或讀 arm ledger。

## 0. 六欄契約與主要結論

| 欄位 | 內容 |
| :--- | :--- |
| 命題 | pointed cone 是否選出唯一時計？保序／保體積是否足以取得物理 observer equivalence？什麼額外資料才能使各 observer 的速度刻度可比較？ |
| 定義域與輸入 | 給定有限維 affine E=R^(d+1)、d≥1、closed convex full-dimensional pointed cone；§3 起另限已給 Lorentz cone、固定 Lebesgue measure；§5 另給 calibrated metric |
| 證據 | §2 時計非唯一與 tilted-clock 反例；§3 線性 cone automorphism 的完整短證明；§4 boost 下無 invariant positive clock；§5 等變時計族；§6 外部記錄反例 |
| 未證橋接 | B1 continuum；B2 density／scale；B3 實際可用 inertial observers／laws；B4 clock／rod／synchronization calibration；B5 圓錐的來源；B6 signals／matter；B7 dimension／gravity |
| 否定條件 | 只否定由較弱輸入推出唯一時計或完整物理等價的蘊涵；不否定有物質／boundary／marked observer 後的時計，也不否定整個湧現問題 |
| 後續驗證 | 獨立核對證明、資料 action 和 countermodel 的 scope；下輪先審 operational record 所需資訊，不構造 K 或投入統計計算 |

**本稿沒有選出一個物理時鐘。** finite interval volume 在前稿限定類中給出許多
strictly positive linear clocks；甚至固定一個 rest vector 並令 h(e)=1，仍不唯一。
在已給 Lorentz cone 的 affine 類中，保 cone 加保固定 volume 確實可把**最大數學群**
限制為 future-preserving Lorentz group 加 translations；它不強迫實際物理 law 使用
整個群，也不生成鐘錶或尺規。完整 boost 對稱反而禁止唯一 invariant positive clock。
可以構成等變的 observer／clock **族**，但要把它說成可操作的物理，仍需 §7 的前提。

## 1. 先分開四種資訊，避免換一個名稱就當作導出

沿用幾何 cone **𝒞**，不使用候選 kernel 的符號 K。對 pointed 𝒞 定義

$$\mathcal H=\{h\in E^*:h(w)>0\ \text{for every }w\in\mathcal C\setminus\{0\}\}.$$

有限維 compact unit section 使這等同於 dual cone 的 interior。
一個數學 clock／rest pair 是 `e∈int 𝒞, h∈𝓗, h(e)=1`；每個位移分解為
`w=h(w)e+x, x∈ker h`。這只給線性 coordinate time／rest split，
沒有讓一個物質系統真的沿 e 運動、穩定 tick 或同步遠處時計。

| 層次 | 精確問題 | 不能自動升格的部分 |
| :--- | :--- | :--- |
| order／cone | 哪些位移因果可及？ | 實際 signal 是否存在、走到邊界或具有 universal speed |
| coordinate clock／rest split | 哪個 h,e 用來分解位移？ | 運動中的真鐘如何 tick；h(w) 一般不是該路徑的 proper time |
| calibrated metric／rod | 哪種 time／length interval 和 unit 可互相比較？ | 裝置的可實現性、誤差、加速時的 clock law |
| physical observer equivalence | 同樣的操作／準備在不同 observer 中是否有相同 law？ | 只保幾何不保裝置、matter state、boundary 或 probability law 的變換 |

對線性 A，數學資料的 action 是 `(e,h)↦(Ae,h∘A⁻¹)`，故新 pair 仍滿足
`(h∘A⁻¹)(Ae)=1`。把 observer 連同資料一起變換是 **equivariance**；
要求同一個 h 對全部 A 不變，是較強而不同的 **invariance**。
passive coordinate change 同時改所有 component descriptions／units；active symmetry
須在明訂哪些背景固定、哪些 fields／states 被變換後仍保持完整 law。
沒有這個帳，就不能把「保序」與「兩個物理實驗等價」畫等號。

## 2. B4：存在 bounded-section 時計，仍沒有唯一選法

### 2.1 命題 N：固定 rest vector 與 normalization 仍有無限多個時計

在上述 D=d+1≥2 類中，前稿 H 給出 h₀∈𝓗。固定任意 e∈int 𝒞，
先 rescale 到 h₀(e)=1。因 unit section compact，有 δ>0 使
`h₀(w)≥δ‖w‖`（w∈𝒞）。取非零 k∈E*、k(e)=0；D≥2 保證存在。
以 dual norm ‖k‖，對 `|ε|‖k‖<δ` 有

$$h_\varepsilon(w)=h_0(w)+\varepsilon k(w)
\ge(\delta-|\varepsilon|\|k\|)\|w\|>0\quad(w\in\mathcal C\setminus\{0\}),
\qquad h_\varepsilon(e)=1.$$

不同 ε 給不同 h，且都具有前稿的 bounded velocity section。□
這證明**約束本身**不唯一，不證明所有規則都不能額外選擇 h；例如分析用 Euclidean
inner product／optimization rule 可以選一個，但須入帳為額外資料，不能冒充 order
已選物理時計。volume normalization 也不會消除此多重性，見 §3–§4。

### 2.2 反例 T：同一 Lorentz cone 的正時計給不同 coordinate speed

給定 1+1D `𝒞={t≥|x|}`、e=(1,0)、fixed measure `dt dx`，分析 units 中 c=1。
對任意 `|β|<1`，令 `τ=t+βx, ξ=x`。它的 Jacobian 為 1，且
`hβ(w)≥(1−|β|)t>0` 對所有非零 future-causal w 成立，hβ(e)=1。
同一兩條 null rays x=±t 在新描述的斜率為

$$\frac{\xi}{\tau}=\frac{1}{1+\beta}\quad\text{或}\quad
-\frac{1}{1-\beta}.$$

時計 positive、interval volume 有限、甚至座標 volume element 相同，仍不使兩方向
coordinate cap 相同。β→±1 時其中一個 cap 可任意大。
metric 的完整變換是

$$dt^2-dx^2=d\tau^2-2\beta\,d\tau\,d\xi+(\beta^2-1)d\xi^2.$$

因此這是**同一資料的 passive 重描述**，不是保持標準 component cone 不變的 active
Lorentz transformation，也不是 physical superluminal counterexample。原來 e 的
g-orthogonal simultaneity 是 ker dt，通常不同於 ker hβ；未改 rod／synchronization
契約就不能稱 tilted hβ 是同樣校準的 Einstein observer clock。這個精確例只證明
「positive h＋volume」不足以指定那個契約。未證 B4／B6 不因此消失。

## 3. B3：給定 quadratic cone 後，最大 affine 幾何群可以精確算出

本節**另外輸入** `𝒞L={(t,x):t≥‖x‖}`，J=diag(1,−I_d)，q(w)=wᵀJw，
與固定 Lebesgue μ；這是前稿 S 已條件化的 Lorentz-shaped 分支，在既定 units 設 c=1。
不從一般 pointed cone、裸 poset 或任意非線性 order automorphism 推此結果。

### 3.1 命題 A：線性 cone automorphisms 是 positive dilation × future Lorentz

若 A∈GL_D(R)、A𝒞L=𝒞L，則存在 λ>0，

$$A^TJA=\lambda^2J,\qquad A=\lambda L,
\quad L^TJL=J,\quad L\mathcal C_L=\mathcal C_L.$$

**完整短證明：** 可逆線性 homeomorphism 保 interior 和 boundary。對每個 unit n∈R^d，
(1,n) 在 boundary，故令 symmetric M=AᵀJA、以 blocks M=[[a,bᵀ],[b,H]]，有

$$a+2b\cdot n+n^THn=0.$$

比較 n 與 −n 得 b=0；因所有 unit n 的 quadratic value 都是 −a，
用 basis vectors 得 H 的 diagonal 是 −a，d≥2 再用 (e_i+e_j)/√2 得 off-diagonal 為零。
d=1 已由兩個 n=±1 完成，故 M=aJ。A(1,0)∈int 𝒞L，使 a=q(A(1,0))>0。
取 λ=√a，L=A/λ 即得上述式，亦保持 future cone。反向直接成立。□

determinant identity 給 `|det A|=λ^D`。因此 **保同一 μ** 的 subgroup 恰有 λ=1。
若准 affine maps p↦Ap+b，translations 任意，最大 order＋volume group 是
`R^D ⋊ O⁺(1,d)`；這裡 ⁺ 只指 future-preserving，仍包括 spatial reflections。
不是把整個 O(1,d) 的 time reversal 算成保持 directed chronology；connected
proper-orthochronous subgroup／parity 是否物理可用，都另需 B3。

這給出一段實質條件式推導：**已給 cone、affine class 和 fixed volume ⇒ 最大數學群**。
它沒有證明所有物理 observers 實現此最大群；identity subgroup、rotations subgroup
或另有 marked rest direction 的 laws，同樣可使用這組幾何資料（§6）。
affinity／inertial motion 也還是輸入，本節不是所有 order bijections 的分類定理。

### 3.2 process law、realization 與 metric scale 必須分帳

若另已給 homogeneous Poisson `Λ=ρμ`、ρ fixed 且正，affine map push-forward 的
intensity 是 `ρ|det A|⁻¹μ`。counts 的 Poisson law 與 independence 因此在
`|det A|=1` 時保持；在此 affine 類中反向也由任意 positive finite-volume set 的均值
得到 determinant 的絕對值必須為 1。這是**整個 process law** 的 invariance，沒有生成樣本。
不代表某個 realization 自己固定於每個 boost，也不證明物理裝置的 law invariant。
若容許同時改 ρ／units，dilation 是跨資料的重描述，不能再說保 fixed Λ。

q 與 κq（κ>0）有相同 cone 和上述群；僅知「某固定 μ 被群保持」仍不選 κ。
在已給 metric 類中若**另訂** `μ=vol_g`，則 gκ=κJ 的 volume density 是 κ^(D/2)，
才可用這個校準約定固定 κ。若只知道 NV_P 的 ρμ 而 ρ 未校準，scale 仍混淆。
metric 的單位與 physical density 不由無單位 count 自動取得，B2／B4 仍 OPEN。

## 4. 唯一 preferred clock 與 observer 族不能混為一談

### 4.1 命題 I：完整 boost 群沒有 invariant strictly positive linear clock

在 §3 類中，假設正時計 h=a dt+Σb_j dx_j 對所有 future Lorentz L 滿足 h∘L=h。
只需考慮 (t,x₁) plane 的 boost

$$B(r)=\begin{pmatrix}\cosh r&\sinh r\\\sinh r&\cosh r\end{pmatrix},$$

其他 coordinates 固定。對 hB(r)=h 在 r=0 微分，得到 b₁=0、a=0。
但 h 在 future interior vector (1,0) 必須為 a>0，矛盾。□
這些 B(r) 的 determinant 是 1，故即使加入 fixed volume／fixed positive density，
也不提供唯一 invariant h。若一個確定性規則只由 (𝒞L,μ) 指派 h 並要求在該最大群下
equivariant，因輸入被 B(r) 固定，輸出必須 invariant；故這個**具名規則類**不可能。
加 marked observer、boundary 或 break boost symmetry 會改輸入，不被此命題排除。
不需也不得將此結果改說成「時間不存在」或「任何時鐘都不能湧現」。

### 4.2 對 sprinkling-selected clock 的限制：只作有條件文獻推論

[BHS (2006), §2 Theorem 1](https://arxiv.org/html/gr-qc/0605006v1) 的域是 full
Minkowski homogeneous Poisson、D>1、固定 origin、connected Lorentz action；它排除
measurable equivariant map 到 unit future-timelike direction。不是任意 poset 的定理。
在本節已給 J 下，若存在同樣 measurable、equivariant 的 strict positive covector
h(ω)=a dt+b·dx，則 a>‖b‖，且

$$u(\omega)=\frac{J^{-1}h(\omega)^T}
{\sqrt{h(\omega)J^{-1}h(\omega)^T}}$$

是 unit future-timelike vector；raising index 和 normalization 與 Lorentz action 交換，
會產生被定理排除的 direction map。因此該**full-space 指定 law** 不允許只由
sprinkling 選出此種單一時鐘。這是文獻定理的限定推論，非新數值證據。
原文 §3 明限 full Minkowski；finite region 的 boundary、選定 worldline／matter
或額外 marks 提供新資訊，不能忽略也不能用來宣稱原 no-go 已失效。
observer 族或關係式時計不等於單一 preferred direction；本節沒有排除它們。

## 5. 可成立的條件方向：等變的 calibrated observer／clock 族

**另給** flat metric g(v,w)=vᵀJw 及其 time／length calibration，不把它當 L0 推導。
令 `𝓤={u∈int 𝒞L:g(u,u)=1}`。每個 u 給

$$h_u(w)=g(u,w),\qquad V_u=\{x:g(u,x)=0\},\qquad
\|x\|_u=\sqrt{-g(x,x)},\qquad w=h_u(w)u+x.$$

### 5.1 命題 F：這個族等變，每個同校準 observer 的 cone cap 為 1

任何 u=(a,b)∈𝓤 有 a=cosh r、b=sinh r n（b=0 時 r=0）；沿 n 的上述 boost
把 (1,0) 送到 u。故可在 Lorentz-related basis 中計算：V_u 的 g negative definite，
h_u 對非零 future cone 嚴格為正，且

$$w\in\mathcal C_L\iff h_u(w)\ge0,\quad
\|x\|_u\le h_u(w);\qquad
g(w,w)=h_u(w)^2-\|x\|_u^2.$$

對非零 boundary w，ratio 恰為 1；對非零 interior w，ratio <1。
對所有 future Lorentz L，

$$h_{Lu}(Lw)=h_u(w),\qquad V_{Lu}=LV_u,\qquad\|Lx\|_{Lu}=\|x\|_u.$$

三式由 L 保 g 直接得到，故是一個等變族，沒有指定唯一 u。□
恢復共用時間／長度 units 時 cap 記作 c；units 改為 t′=at、x′=bx 時，數值變為
(b/a)c。以上證的是**calibrated causal cone cap**，不證任何 signal 實際達到它，
也不從中得質量、quantum law、3+1D 或某裝置的觀測紀錄。

### 5.2 coordinate time 不等於任意路徑的 tick time

對 smooth future-timelike curve z(s)，給定 metric 後可定義幾何 functional

$$\tau_g[z]=\int\sqrt{g(\dot z,\dot z)}\,ds.$$

它對 Lorentz transformation invariant；reparametrization 的 Jacobian 在根號內外
相消（取 orientation-preserving reparametrization）。沿 z(s)=p+su、u∈𝓤，τ_g 等於
s 的差；一般 future-timelike tangent w=ż(s) 則 `sqrt(g(w,w))≤h_u(w)`，等號只在
w 與 u 平行時成立。積分得到路徑 tick functional 不大於該 observer 的 coordinate
time 差；不把一般曲線的 τ_g 誤當作端點位移的 sqrt(g(Δz,Δz))。
這些是幾何公式。要把真鐘 ticks 等同 τ_g，還須真鐘的 dynamics、適用運動／加速域、
calibration 與 error law。類似地，‖x‖_u 只是幾何 rod prescription，沒有製造尺規。
把它們命名「操作定義」不能代替 B4／B6 的實現證明。

## 6. 反例 M：完整幾何群不強迫完整記錄的對稱

給定同一 (𝒞L,μ)、固定 unit future u₀=(1,0)，並在外部模型中加一個 scalar 記錄
`F_{u₀}(w)=g(u₀,w)²`。這是分離資訊的 countermodel，不是物理 law／weight／K 提案。
在 w=u₀ 時 F=1；同一 fixed u₀ 下 boost 後 `F_{u₀}(B(r)w)=cosh²r`。
所以 B(r) 保 order、volume、q，仍不保這個**固定 mark 的完整記錄**。
若連 u₀ 一起變換，`F_{Lu₀}(Lw)=F_{u₀}(w)`，則是新資料間 covariance。

因此幾何輸入不能決定額外記錄是否有 fixed preferred frame。實際 theory 須明訂 mark
是 law 的固定 background、會變換的 matter state、還是 observer label；不能先忽略
它，再由 maximal cone automorphism 推「所有物理實驗完全等價」。
反例沒有說 covariant matter state 不能有 rest frame，也沒說 full Lorentz symmetry
不可行；它只否定從 order＋volume **單獨**推完整 law／observer equivalence 的蘊涵。

## 7. 什麼資訊賦予操作／物理資格：未證義務與停止條件

目前的可操作答案是**待證的資料契約**，不是已實現時鐘。
若採某外部 primitive，要另案說清楚 conditional scope，不在本稿採用。

| 義務／橋接 | 已有條件支持 | 尚缺資訊／紙上方法 | 停止或改稱條件研究的條件 |
| :--- | :--- | :--- | :--- |
| continuum／affinity（B1／B3） | 前稿的固定 affine cone 類；§3 的 affine classification | 哪種 L0 結構產生 inertial paths、affine difference／dimension；定義 limit 與 relation preservation | affine 座標或 inertial group 作輸入時，不宣稱 pre-spacetime 生成 |
| observer 的來源（B3／B4） | §2 正時計多重性；§4 單一 invariant 時計障礙 | 選定 worldline／matter／boundary 的來源與 exposure；區分單一 preferred clock 和 equivariant family | 只靠 full-space invariant Poisson 選單一 equivariant 時計，遇 BHS 就停止此類方案 |
| clock ticks／rod／同步（B4／B6） | §5 的幾何 family／proper-time functional | 不同裝置的穩定性／共同 calibration、simultaneity 或 signal protocol、運動適用域；先列 observable record，不設計 K | 若用假定 τ_g 的鐘作證 τ_g，撤回導出；若無裝置定義，不能報 operational c |
| density／unit scale（B2／B4） | §3.2 的 determinant 與 κ 自由；T1 的 scale／density 反例 | 分開 ρμ、metric volume、時間與長度 unit；指定哪個 ratio intrinsic，哪個額外標定 | 未知 ρ／units 時不報 physical c 數值；c=1 僅記 normalization |
| physical equivalence（B3／B6） | 最大數學群已可算；§6 表明它不足 | 對 fields、states、preparations、records 的 action 與完整 law／probability covariance；boundary 和固定背景明列 | 群只保 geometry、不保具名 law 或 device，不能升格全體 observer 等價 |
| causal cap 與 signal（B6） | §5 的每個同校準 observer cap | 哪些實際支援達邊界、是否 universal；穩定性／positivity／continuum correspondence | 只有可及 cone，不宣稱測到光或質量／能量關係 |

**B3／B4 仍 OPEN。** 這輪將它們分成可證的幾何 subgroup、不能唯一選 clock 的具名
限制，以及缺少的 operational record；沒有由 lemma 名稱代替物理機制。
B1／B2／B5 與其他橋接沿用；沒有修改 item 7／8、統計 gate 或任何協定。

## 8. 下一個低成本交付與複核重點

建議下一份先做 **B4＋B6 的 clock／rod／signal「紀錄與實現必要條件」審計**：
列出一次時間／長度比較所需的準備、事件關係、計數、readout 和 synchronization
資訊，逐項標示來自 intrinsic order、額外 matter／boundary 或外部 metric。
先檢查是否 circular、是否需要一個 forbidden preferred direction；不能在未定義裝置
前，以大規模時計／signal 量測填補缺口。這是必要條件分析，不構造 K、matter law
或新的 order／weight／phase prescription；若實質工作需要候選構造，再另案 amendment。

獨立複核重點：N 的定義域與 perturbation；T 的 passive／active 區別；A 在 d=1 的
boundary proof 與 fixed μ；I 的 invariant／equivariant 資料；BHS domain 與 index raising；
F 的 calibrated family 與 operational gap；M 的固定／變換 mark。不得將其中任何
條件結果寫成 L0 已生成物理時計、Lorentz observers 或 signals。

## 9. 作者文獻與歷史邊界

2026-10-11 讀取作者原文：

- [BHS v1](https://arxiv.org/html/gr-qc/0605006v1)，§2 Theorem 1、§3：§4.2 的唯一
  外部 no-go 依據；其 full Minkowski／Poisson／measurability／equivariance 前提全保留。
- [Anker–Ziegler v2](https://arxiv.org/pdf/2007.09301v2)，§1.1–1.3：只對照 affine
  與 physical transformations／passive unit changes 的區分。其 Theorem 1 的 n>2、
  block-intersection／time reversal 不用於本稿 A；A 是自己的短證明，且包含 d=1。

Nicholas 的讀取狀態已依操作者 PR #72 複核修正：Claude 已讀摘要及 §2.1、§5、§6，
引用範圍一致；Anker–Ziegler 仍未由 Claude 讀取。這不表示全篇證明已獨立雙方認證。
本稿 N／A／I／F 與 T／M 待 exact-head 獨立數學複核；不先升格【已確認】。

6a-S 封存、run1、O19、witness 2/12／exit137、item 7 不可 ADOPT、items 3–5 v0.2
重驗待辦、item 8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING 與
候選 K 禁令全部保留。程式、測試、CI、manifest、registry、evidence／assessment 不變。
