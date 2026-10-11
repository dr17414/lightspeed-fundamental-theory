# B2＋B5：有限區間體積、抽樣強度與錐體結構的前提審計

狀態：**【探索／解析審計待獨立複核】**。
基線：PR #71 squash main `f574e06b4fa058e363519ee02a0de11632bc8fb6`，
tree `d54d3f2b47582a0b27675230cd5ce8cfee2494b4`。
承接 [T1＋T5 審計](t1_t5_premise_audit.md) §2、§5、§8。
本稿是外部 continuum countermodel／必要條件的紙上研究，不從 poset 構造時空，
不提出候選 K、order ansatz 的採用方案、weight 或 phase law。
沒有抽樣、量測、seed、E4／selector witness、主機或 arm ledger。
既有 regression suite 僅檢查 repo 變更。

## 0. 六欄契約與本輪結論

| 欄位 | 內容 |
| :--- | :--- |
| 命題 | 在哪個限定類別中，finite interval volume 等價於何種 cone 性質？它能否給出 finite speed、quadratic cone 或 invariant c？ |
| 定義域 | 給定有限維 R^D、affine translations、閉凸滿維 cone、Lebesgue measure／明訂 Poisson intensity；不是任意 finite poset 的定理 |
| 證據 | §2–§6 的完整短證明與兩個 countermodels；§8 作者教材的術語核對 |
| 未證橋接 | B1–B7 均保留；特別是 continuum／measure／scale homogeneity、operational clock、spatial isotropy、observer group 尚未由 L0 導出 |
| 否定條件 | 超出限定類別時不使用 equivalence；不把 infinite expected count 當作任意 law 下 almost-sure infinite count |
| 後續驗證 | 獨立核對 quantifiers、strict／closed cone、時計反例及 isotropy 的作用域；不需要新數值資料 |

**有限而有內容的前進：** 在 §1 的類別中，對 interior-separated endpoints，
finite Lebesgue interval volume **等價於 cone closure pointed**；positive homogeneous
Poisson 因而與 LF_o 的 almost-sure 判斷相接。這給出 §3 的可複核必要且充分條件。
它也保證存在一個使 velocity section 有界的 linear functional，但沒有替物理選出時計。
只有再給定一個 future clock／rest decomposition 與完整 spatial O(d) isotropy，
才有 §6 的 Lorentz-shaped cone；尚未導出 observer group、physical c 或 signal dynamics。

## 1. 限定模型與 primitive 帳

用 **𝒞** 表示幾何 cone，避免與候選 kernel K 混淆。
給定 D=d+1≥2、E=R^D，及用於分析的 Euclidean norm／Lebesgue measure μ。
𝒞 是 closed convex cone，`int 𝒞≠∅`、`𝒞≠E`；**不預先要求 pointed**。
定義

$$p\prec q\iff q-p\in\operatorname{int}\mathcal C,
\qquad I(p,q)=(p+\operatorname{int}\mathcal C)\cap(q-\operatorname{int}\mathcal C).$$

因 𝒞 是 proper subset 的 convex cone，0 不在 interior；interior 對加法封閉，
故 ≺ irreflexive、transitive，即使 closure 含直線也可能是 strict order。
定義 lineality `L=𝒞∩(−𝒞)`；**pointed** 指 L={0}。
「strict order 無 cycle」不等於「closure pointed」：Galilean half-space
`𝒞={ (t,x):t≥0 }` 的 interior order 正是上一稿的 absolute-time order。

本稿不稱未假設 pointed 的 𝒞 為教材中的 proper cone；該詞通常已含 pointed，
若提前使用，就會把欲證條件放進定義。

| 前提 | 在證明中做什麼 | 未由 L0 取得的部分 |
| :--- | :--- | :--- |
| 有限維 affine E、固定 D | 差向量、平移、compact sphere、Lebesgue volume | B1；不是 manifold 存在／3+1D 選擇 |
| 單一 translation-invariant cone prescription | 把全部 intervals 寫成同一 𝒞 的兩個 translates | B3／B5；curved、inhomogeneous geometry 不在此定理中 |
| exact positive dilation homogeneity | 同一方向所有正尺度可用 | 額外 continuum 前提；不是 bare count 的性質 |
| closed、convex、full dimensional | closure limits／lineality／positive-volume interior balls | 正則性須宣告，不能只憑小圖的 LF_o 推出 |
| μ=Lebesgue、positive constant density ρ | cone volume 與 point-process intensity 相接 | B2／B4；物理 measure 與 density calibration 尚未導出 |
| clock、rest split、spatial O(d) | §6 才加入，用來把 section 定成 ball | 額外 B3–B5 前提；不是 §3 的推論 |

在另已指定 translation-invariant、positive-dilation-invariant 的 continuum order 中，
其 future set F 因 transitivity 有 F+F⊂F；dilation 再使 F convex。
這說明 convexity 可在那個**加強類別**中取得，而不是裸 poset 的新定理。
本稿直接採 `F=int 𝒞` 的正則形式，不聲稱此 prescription 已由 L0 選出。

## 2. B2：控制點數的是 intensity，不只是「體積」一個詞

令 Π 為 σ-finite、locally finite intensity measure Λ 的 Poisson point process；
counts on disjoint finite-intensity sets independent，`N(A)~Poisson(Λ(A))`。
這是紙上 law，沒有生成 realization。

### 2.1 命題 P：固定 measurable A 的 finite／infinite intensity

若 Λ(A)<∞，則 N(A)<∞ 幾乎必然。若 Λ(A)=∞，取 increasing exhaustion A_n
且 Λ(A_n)=λ_n<∞、λ_n→∞。對任意 integer k≥0，

$$\Pr\{N(A_n)\le k\}=e^{-\lambda_n}\sum_{j=0}^k\lambda_n^j/j!\longrightarrow0.$$

counts 單調，故 `Pr(N(A)≤k)=0`；再對 k 可數 union，得到 N(A)=∞ 幾乎必然。□
這是 **固定 A** 的命題，不能直接把隨機 sampled endpoints 代入後省去同時性證明；
§3.3 另以 countable covers／nested rational intervals 處理。

在 `Λ=ρμ`、constant ρ∈(0,∞) 時，finite intensity 與 finite μ-volume 等價。
若一般 `dΛ=λ(y)dμ` 且有全域常數 `0<a≤λ(y)≤b<∞` 幾乎處處，則
`a μ(A)≤Λ(A)≤b μ(A)`，同一等價仍成立。**constant density 不是唯一可用條件**。
只有 λ(y)>0，或只在每個 compact set 有界，卻不足以給這個全域逆推。

`E[N(A)]=ρμ(A)` 的均值說法本身不指定 Poisson law。有限期望可排除 N(A)=∞
的正機率，但 infinite expectation 不自動意味 N(A)=∞ 幾乎必然。
例如以機率 1/2 取 empty configuration，否則取 intensity 2ρμ 的 homogeneous Poisson：
有限 A 的期望仍為 ρμ(A)，infinite-volume A 卻以機率 1/2 沒有點。
本例只否定「mean number–volume 自動給出命題 P」；它不是替代物理抽樣方案，
也不宣稱此混合 law 幾乎必然滿足 LF_o。

### 2.2 反例 W：無界空間、處處正 density 仍可有 finite slab counts

在 `R×R^d` 採 absolute-time order，令

$$d\Lambda=\rho e^{-\|x\|^2}\,dt\,d^dx,\qquad \rho>0.$$

一個 finite-time slab 的 Λ 為 `ρ(t'−t)π^{d/2}<∞`，即使其 Lebesgue volume 為∞。
以 countably many integer-time slabs 的有限性得到所有 sampled intervals 的 LF_o。
order 仍沒有 spatial propagation cap；失去的是 spatial translation homogeneity
及全域 positive lower density，不是空間變成 compact。
可把 weight 吸進 μ 的定義後稱「相對 μ constant density」，但這不會把 μ 變成
translation-invariant Lebesgue volume。故「uniform」必須附其 measure。
本反例保留上一稿的 full homogeneous 排除，沒有與它矛盾。

## 3. B5：interval volume 的 exact cone criterion

### 3.1 定理 V（限定類別中的等價）

對 §1 的 𝒞，以下三件事等價：

1. 𝒞 pointed。
2. 每個 z∈int 𝒞 的 `I(0,z)` 有 finite μ-volume。
3. 至少一個 z∈int 𝒞 的 `I(0,z)` 有 finite μ-volume。

而 pointed 時 closed order interval `J_z=𝒞∩(z−𝒞)` compact；不 pointed 時，
**每一個** interior interval 都有 infinite μ-volume。所有此類 I 都是非空且正體積。
不對 boundary-separated／lower-dimensional intervals 主張同一等價。

**pointed⇒compact⇒finite：** 若 J_z unbounded，可選 y_n∈J_z、norm→∞。
取 subsequence 使 y_n/norm→v、norm v=1。closed cone 使 v∈𝒞；
`(z−y_n)/norm→−v` 又使 −v∈𝒞，違反 pointed。J_z closed bounded，故 compact。
I(0,z)⊂J_z，μ 因而有限。由 z/2∈int 𝒞，可選 ε>0，
`B(z/2,ε)⊂I(0,z)`，所以體積不是零。

**不 pointed⇒infinite：** 選 nonzero v∈L，則 `𝒞+tv=𝒞` 對所有 real t；
interior 與 I(0,z) 也沿此 line invariant。前述 ε-ball 的 translates
`B(z/2+n a v,ε)` 全在 I 中，取 a norm v>2ε 即得 countably many disjoint
等半徑 balls。它們的 positive Lebesgue volumes 加總為∞。□

### 3.2 各前提的限制

full dimensional／interior endpoints 保證 positive-volume balls；退化 ray／面可能
有 unbounded 零體積 intervals，不能用 full-D Lebesgue sampling 去驗證其因果內容。
closedness 用於 normalization limit；convexity／cone 加法用於 lineality translation。
有限維用於 sphere subsequence 與 closed bounded⇒compact。
以上是**本證明使用的前提**，不是已證它們對所有可能的因果理論都不可少。
在非 cone、curved 或非 Lebesgue measure 類別，finite volume 也不等於 boundedness。

positive homogeneity 另外給 `I(0,s z)=s I(0,z)`，故
`μ(I(0,s z))=s^D μ(I(0,z))`（s>0）。指數 D 已放入 affine dimension／measure，
不能把這個公式倒用為由 bare counts 選出 3+1D 的證明。

### 3.3 同時適用於 sampled pairs：不省略 random-endpoint 問題

採 full-space `Λ=ρμ` homogeneous Poisson。
pointed 時，每個 I bounded；所有 integer bounding boxes 的 counts 同時有限，
故同時涵蓋 **所有** sampled pairs，LF_o 幾乎必然成立。

不 pointed 時，對每個 rational-coordinate a,b 且 b−a∈int 𝒞，I(a,b) 的 volume
由定理 V 為∞；命題 P 與這些 pairs 的可數性，給所有此 intervals 同時 infinite counts。
對任意 comparable sampled p,q，openness 允許選 rational a,b，使
`p≺a≺b≺q`：先取線段上的 p+(q−p)/3、p+2(q−p)/3，再取足夠近的 rationals。
transitivity 給 `I(a,b)⊂I(p,q)`，所以任意這種 sampled interval 都含無限點。

comparable pair 也幾乎必然存在：選 e∈int 𝒞、足夠小的 balls A_n、B_n，
centers 分別為 `3n e`、`(3n+1)e`，使全部 balls disjoint，且任意 A_n 中的點都
precede B_n 中的點。每組兩球非空的機率是固定 `r=(1−e^{−ρ μ(A_n)})²>0`；
各組獨立，前 M 組都未成功的機率 `(1−r)^M→0`。故 LF_o 的失敗非 vacuous。□

因此在本**明訂 law 與 cone 類別**中，LF_o 幾乎必然成立 iff closure pointed。
這比只排除 absolute-time half-space 多了一項分類結果，仍不是 poset generation theorem。

## 4. Pointed closure 可給一個 bounded section，但還沒有選出物理時計

### 4.1 命題 H：存在嚴格正 linear functional 的完整短證明

對 closed pointed 𝒞，令 S=𝒞∩unit sphere。S compact nonempty。
其 convex hull H compact：R^D 的任何 convex combination 可縮到至多 D+1 個點。
理由是更多點的 `(s_i,1)` 線性相依；沿該相依調整係數，保持總和與向量不變，
直到至少一個非負係數成零，反覆消去即可。故 H 是 compact
`S^{D+1}×simplex` 的 continuous image。

0 不在 H：若 `Σλ_i s_i=0`，取 λ_j>0，則
`−s_j=Σ_{i≠j}(λ_i/λ_j)s_i∈𝒞`，與 s_j∈𝒞、nonzero 矛盾。
取 H 中 norm 最小的 a≠0。對任意 s∈S，minimality 沿
`a+ε(s−a)`、ε≥0 的右導數給 `a·s≥norm(a)²`。
令 `h(w)=a·w`、`δ=norm(a)²>0`，便有

$$h(w)\ge\delta\|w\|\quad(w\in\mathcal C).$$

反方向，若有 h 對 𝒞 的每個 nonzero w 都嚴格正，則不可能同時 w、−w∈𝒞，
所以 pointed。□

### 4.2 有界速度的「存在」與 physical c 的差別

選 e∈int 𝒞 且 h(e)=1；每個 w=τ e+x，τ=h(w)、x∈ker h。
對 nonzero w∈𝒞，τ>0，且

$$\frac{\|x\|}{\tau}\le\delta^{-1}+\|e\|.$$

因 `norm(w)≤τ/δ`、`norm(x)≤norm(w)+τ norm(e)`，此界直接成立。
`𝒞∩{h=1}` 也 closed bounded，故 compact。
這是 **至少存在一組 linear clock／rest split 有有限 section** 的條件性結論。
它未指定哪個 h 由實際 clocks 測量，也未指定 norm 的 rods／units，更未證 observer
changes 保持同一 speed。h 通常不唯一；δ 是分析界而非測出的 universal constant。
若改用 `t'=a t,x'=b x`，speed 改成 b/a 倍；B4 與 B3 均不能消失。

## 5. 反例 U：finite volume 不保證相對既定 coordinate clock 的 finite speed

在外部 R²=(t,x)，取 `𝒞={t≥0,x≥0}`、strict order 為 Δt>0 且 Δx>0，
並採 full homogeneous Poisson。𝒞 closed convex full dimensional pointed。
對 endpoint difference (T,X)、T,X>0，

$$I(0,(T,X))=(0,T)\times(0,X),\qquad\mu(I)=TX<\infty.$$

每個 interval 都有限，但以 t 作 coordinate clock、x 作 coordinate position，
允許 X/T 任意大，沒有一個共同有限 cap。t 在 closure 的 nonzero ray (0,X)
上為 0，雖然在 strict interior 為正。§4 的 h=t+x 則有 bounded section。

本例缺 spatial reflection isotropy；也可以把 (t,x) 重新當 null coordinates，
寫成 1+1D Lorentz cone。**它不否定 Lorentzian 描述**，而只否定：沒有 clock–cone
compatibility 就把任意標成 t 的 coordinate 當 operational time，再從 FV 推有限 speed。
它不是候選 order 的推薦。未證橋接仍是 B4／B5，而不是算力或統計精度。

## 6. 何時能取得 Lorentz-shaped cone：所加前提全部攤開

另給定 E=`R e⊕V`、linear clock τ、τ(e)=1、V=ker τ、V 的 Euclidean norm，d≥1。
要求 e∈int 𝒞、`𝒞⊂{τ≥0}`，並要求所有
`(τ,x)↦(τ,Rx)`、R∈O(d) 都保持 𝒞。這包括 d=1 的 reflection，
不是只用 trivial SO(1)；也不是完整 spacetime Euclidean rotations。

### 6.1 命題 S：FV＋這組 clock／spatial isotropy 前提的 cone 形狀

由定理 V，FV⇒pointed。若 nonzero (0,x)∈𝒞，O(d) 可送 x→−x，
於是 (0,−x)∈𝒞，違反 pointed。故 τ 在 nonzero closure directions 上嚴格正。
在 compact `𝒞∩unit sphere` 上 τ 有 positive minimum，所以
`P={x:(1,x)∈𝒞}` 是 compact convex、含 0 的 interior、O(d)-invariant set。

令 c=max_{x∈P} norm(x)。compactness／full interior 給 0<c<∞。
rotations 給整個 radius-c sphere 都在 P，convexity 給 ball 在 P；最大值定義
又給 P⊂ball。因此 P=closed ball(c)，而 cone scaling 給

$$\mathcal C=\{(\tau,x):\tau\ge0,\ \|x\|\le c\tau\}.$$

這是 `q(τ,x)=c²τ²−norm(x)²` 的 future Lorentz-shaped cone，signature 為 (1,d)。□

**取得／尚未取得的邊界：** 取得的是給定 affine／clock／spatial metric 前提下的 cone
形狀與一個 relative cap。quadratic form 是此 cone 的一種表示，scale 未固定。
q 所有 time-oriented isometries 可在外部數學上定義，但沒有證明它們就是實際 observers
的允許變換，也沒有證明 sampling／物理 law 在其下 invariant。
更沒有任何 field equation、null signal、mass、quantum dynamics 或 3+1D 選擇。
因此不得把命題 S 寫成「從 causal set 導出狹義相對論」或所有 observers 的 physical c。

### 6.2 可核的 rest interval 算術與不能反推的量

在此特定 cone 中，z=T e、T>0，time slice radius 為 `c min(t,T−t)`。
令 v_d 為 unit d-ball 的 Lebesgue volume，直接積分得

$$\mu(I(0,T e))=2v_dc^d\int_0^{T/2}t^d\,dt
=\frac{v_dc^d}{2^d(d+1)}T^{d+1}.$$

這使 finite／infinite 的差別可明算，但若 count 的 law 只給 ρμ，coefficient
仍含 density、spatial units 與 time units。它不自行辨識 c 的 physical value。
anisotropic pointed cone 也可有 finite intervals；上一稿 ℓ∞ 方錐已是反例，
證明 isotropy 是本次 quadratic-cone 推導的額外內容，非 FV 自帶的結論。

## 7. 對 B2／B5 的結案程度與下一步

| 義務 | 本輪支持 | 尚缺／不可倒用 |
| :--- | :--- | :--- |
| finite count 對 physical volume 的橋 B2 | intensity criterion；uniform／bounded-comparable density 下與 μ-volume 相接 | 不能把 mean law 當 Poisson，也不能把 μ／ρ 由命名變成導出量 |
| finite interval volume 對 cone B5 | 定理 V 在明訂類別給 pointed iff FV；命題 P 接 LF_o | continuum、scale／translation homogeneity、cone prescription 均未由 L0 取得 |
| finite speed 的存在 B4／B5 | pointed 給至少一個 strictly positive h 與 bounded section | 反例 U 排除對任意指定 clock 的無條件推論；physical clocks／rods 尚缺 |
| quadratic cone／signature B3–B5 | 命題 S 在明訂 clock、spatial metric／O(d) 之下成立 | isotropy、observer action、單一 time 與 d 已條件化；不證 3+1D |
| signal、mass、quantum、gravity B6／B7 | 本輪無新的承重證據 | kinematic cone 不等於 equation 的 signal support；未設計 K |

本輪沒有證明哪些前提對**所有**物理理論必不可少；只完成具名類別中的等價與反例。
G0-C 整體仍 OPEN。可考慮的下一個低成本交付是 **B3＋B4：operational clocks 與
observer equivalence 的前提審計**，先回答什麼資訊能選出 h、哪些變換有物理資格。
若選擇把 continuum、時計或 isotropy 當新 physical primitive，須另立 conditional scope，
不能悄悄記為前時空湧現，也不需要因此立即構造 K 或跑大規模驗證。

## 8. 來源、歷史與協定邊界

cone／dual cone 的標準術語對照：Boyd–Vandenberghe,
[Convex Optimization（作者版）](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)
§2.4、§2.6.1（printed pp.43、51–53）：proper cone 已含 closed、solid、pointed；
pointed closure 對應 dual cone 有 interior。本文 §3–§6 自行寫出需要的證明，
不把 optimization 教材當物理生成機制；Euclidean norm 是分析 scaffolding。

上一稿兩篇可另行複核的作者原文：
[Nicholas v1](https://arxiv.org/html/2606.25993v1)（§2.1、§5.4–5.5、§6），
[Anker–Ziegler v2](https://arxiv.org/pdf/2007.09301v2)（Theorem 1、Eq.(4)）。
2026-10-11 再讀作者頁面，與上一稿有限的前提對照一致；不新增對全篇證明的認證，
本稿的命題 P／V／H／S 不依賴這兩篇。操作者轉述 Claude 已獨立核准 PR #71 的數學，
其文獻讀取受阻亦保留紀錄，不能改寫成兩篇已經雙方獨立認證。

6a-S 封存、run1、O19、witness、item 7 不可 ADOPT、items 3–5 v0.2 重驗待辦、
item 8 OPEN、6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING 與候選 K 禁令不變。
