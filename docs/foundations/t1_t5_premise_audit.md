# T1＋T5：輸入、湧現目標與運動學前提的紙上審計

狀態：**【探索／解析審計待獨立複核】**，不是新物理理論或正式驗證結論。
基線：PR #70 squash main `92bbc473b7d873fe556ef019e6453216ec714503`，
tree `5e1504136dec9f9839890d6441407ddccd3f3a6b`。
依 [理論優先路線圖](../THEORY_FIRST_ROADMAP_DRAFT.md) §2、§4 交付 T1＋T5。

本輪只寫定義、解析證明、反例與未證橋接。反例使用外部座標模型來檢查假設的邏輯
強度，不是從 poset 構造模型，也不為候選 K 提供材料。沒有新 K、量測、抽樣、seed、
E4 診斷、witness 或 arm ledger；既有回歸測試只用於 repo 變更檢查。

## 0. 六欄主張契約與結論範圍

| 欄位 | 本札記的內容 |
| :--- | :--- |
| 命題 | 哪些目標由已定義的輸入推出？裸偏序能否排除 Euclidean metric？局部有限與 number–volume 能否排除 Galilean unlimited propagation？ |
| 定義域與輸入 | 區分有限／可數 poset、連續反例、full noncompact 空間及 compact 空間；區分 order-interval 與拓撲局部有限 |
| 證據 | §3–§6 的完整短證明；§7 的原作者文獻前提核對；repo §1 的來源對照 |
| 未證橋接 | B1–B7（§8）：流形存在、抽樣／density、symmetry、時計／尺規、cone／metric、dynamics、維度／signature 的連接仍未完成 |
| 否定條件 | 反例只否定所列弱前提的蘊涵；增加前提後須重查，不把其擴為整個主題的 no-go |
| 後續驗證 | 先形式化 B1–B5 與選定可證命題；本輪不用新數值資料，不安排計算預算或候選設計 |

**結論先列明：** 裸偏序不足以排除「Euclidean ambient metric 加獨立 order」；
局部有限＋number–volume＋均勻性仍不足以在 compact 空間排除 unlimited Galilean
propagation。另一方面，**full 無界空間的 absolute-time order 與正密度 homogeneous
Poisson 抽樣，確實不可能同時具有 order-interval 局部有限性**（§5.2）。
若另要求非平凡 order 對完整 Euclidean spacetime rotations 等變，則可排除此群（§4.2）。
這兩個有條件排除結果不等於已導出 Lorentzian metric、有限不變 c、3+1D 或量子 dynamics。
它們待獨立複核；不把 Gate 0 或任何 scientific closure 標為 CLOSED。

## 1. T1：primitive 與目標分帳

來源：[README](../../README.md)、[Layer 0 提案](invariant_projection_hypothesis.md)、
[acceptance](../STAGE5C_ACCEPTANCE.md) §1、§3–4、附錄 D.1，以及
[typed continuum pairing](../STAGE5C_6A_E_TYPED_PAIRING.md) §1–2。

| 量／結構 | repo 中的實際角色 | 尚不能報為湧現的部分 |
| :--- | :--- | :--- |
| 事件集合 C、偏序 ≺ | Stage 5C 的 L0 輸入；Layer 0 則希望日後解釋它們的來源 | 從 C 開始的研究不是已導出事件或因果關係 |
| # | L0 的 counting；有限 subset 的元素數可由 C 計算 | count 本身不定義物理體積、dimension 或 dimensionful density |
| global {U,V}/S₂ | L1 導出資料，仍有 realizer orbit 義務 | 不等於 local spinor／Clifford representation，不提供 3+1D 橋接 |
| complex amplitudes／phases、pairing、adjoint、state、CAR | L2 quantum scaffolding 須宣告；phase 有 derived／drawn 來源規則 | 不能稱 quantum mechanics 或 phase law 已從 poset 推出 |
| smearing、regulator、normalization、尺度、自由函數與參數 | L3 須來源／容量審計 | O(1) 參數不自動成為導出常數；dimensionful scale 需物理解釋 |
| coordinates、Lorentzian metric、gamma／微分結構、continuum targets | L4 evaluation oracle；只能留在 evaluator | 經已知 Lorentzian target 校準不等於從無背景導出其 signature／c |
| diamond (0,1)²、null coordinates、p_θ、massless S_θ | item-1 的明訂 continuum target 與 sampling／pairing prescription | target 已選 1+1D null structure，不能拿它來證明此結構被選出 |
| 1+1D massless propagation | Stage 5C §1.1 的 restricted claim | 未交付 K／limit；即使成功，也不提供 massive 3+1D／gravity 結論 |
| 3+1D、mass、geometry selection、gravity | README 的總目標 | 需要額外存在性／動力學／極限證明，非現有前置工具的結果 |

L0–L4 是 Stage 5C provenance 分類，不是 Layer 0 底層存在性定理。
現有 oracle 使用背景幾何作校準是合法分工；只有把其輸入當 construction 的輸出，
才造成循環論證。不能因 evaluator 有 metric 就宣稱整個專案已循環，也不能把 oracle
測試通過升格為 spacetime emergence。

## 2. T5：先定義四種不同的「有限」與三種速度問題

對 strict poset，寫 `I_C(p,q)={r:p≺r≺q}`。

| 定義 | 明確條件 | 不等於什麼 |
| :--- | :--- | :--- |
| order-interval 局部有限（LF_o） | 每個 comparable p,q 的 #I_C(p,q) 有限 | 不要求每點 finite degree，也不單獨規定速度 |
| 點過程拓撲局部有限（LF_top） | 每個 bounded／compact region 的點數有限 | 無界 causal interval 的點數可以無限 |
| finite causal-interval volume（FV） | 相應 continuum I(p,q) 的 measure 有限 | 這是已指定 continuum measure／order 的性質，非 bare count 定義 |
| number–volume law（NV_P） | 已指定 (M,μ)、ρ>0，互不相交有限 measure regions 的 counts 獨立 Poisson(ρμ(A)) | 是額外 sampling law，不是每次 realization 都 #A=ρμ(A) |

本文一切 Poisson 是紙上 probability model，沒有生成任何 realization。
對 infinite measure set 的 count 以 increasing finite-measure exhaustion 定義。
「均勻」在本文指 density 相對明訂 μ 為 constant；「非緊緻」要再區分整個 spacetime
非緊緻、spatial slice 非緊緻與 spatial measure 無限，不能互換。

速度問題也分開：**存在 proper causal cone**、**cone 對某 inertial group 保持不變**、
**c 的有量綱數值與實際 signal propagation**。裸 poset 沒有 Δx／Δt，連速度的單位
都未定義；order 可達性也不自動等於某 equation 的 signal support。
在指定 clocks／rods 後改用 `t'=a t,x'=b x`（a,b>0），c 變為 `(b/a)c`；
有限與無限的區別保持，但 numerical value 沒有從無單位資料被決定。

## 3. 反例 A：裸偏序不指定 signature 或 volume

**受檢命題 A：** nontrivial past/future order＋LF_o 就排除 Euclidean signature。
取 `C=Z`、`n≺m iff n<m`，則 `#I_C(n,m)=m−n−1`，非平凡且 LF_o。
把相同元素外部表示為 `(t,x)=(n,0)`，可同時配上

$$g_E=dt^2+dx^2,\qquad g_L=-dt^2+dx^2.$$

在 g_E 模型中，order 是額外指定的 t-order，不是由 g_E 的 timelike cones 定義；
在 g_L 模型中，此 chain 也與 timelike precedence 相容。兩者的抽象 poset 與 counts
完全相同，故 **受檢命題 A 在未要求 metric–order compatibility 的版本下為假**。

本例不滿足 full homogeneous 2D Poisson sampling；不否定加入此條件後的其他命題。
也不宣稱 Euclidean metric 能內生產生 Lorentzian causal cone。正是這個 compatibility
缺口，使 bare-order 排除語句尚未成為完整定理。未證橋接：B1、B3、B5。

### 3.1 Count 與 conformal scale 的識別缺口

已給定 Lorentzian metric g 時，positive conformal rescaling `g'=Ω²g` 保持 chronology，
但 D-dimensional volume form 變為 `dμ_g'=Ω^D dμ_g`。所以只知道 order 不會固定 scale。
若 Ω=s>0 為 constant，且 density 未固定，取 `ρ'=ρ/s^D`，則

$$\rho'\,d\mu_{g'}=\rho\,d\mu_g.$$

同一 continuum 上的 Poisson intensity measure、因而完整 point-process law 相同，
causal relation 又相同；這是 scale／density 的確切不可識別性。
不能藉相同 samples 的 counts 分辨這兩個聯合參數。若 density 已以獨立物理單位固定，
本 scale 反例就不能使用；仍需從 finite noisy counts 到 volume／metric 的估計與極限論證。
nonconstant Ω 而仍堅持同一 constant density 時，抽樣 law 通常改變，不得稱兩者仍等 law。
否定範圍是「order＋count 無需 density／measure／limit 就給唯一 metric」，不是
order＋充分 volume information 在既有 manifold 類內的重建。未證橋接：B1、B2、B4。

## 4. 反例 B 與有條件排除：Euclidean metric 和 Euclidean symmetry 不同

### 4.1 LF_o＋full homogeneous sampling 也不單獨選出 quadratic cone

在 `R×R²` 定義 strict relation

$$ (t,x)\prec(t',x')\iff t'-t>\|x'-x\|_\infty. $$

irreflexivity 直接成立；triangle inequality 使 relation transitive。
對 comparable endpoints、Δt=T>0，所有 interval points 的 t 在長度 T 的 slab 內，
spatial position 在一個邊長 2T 的 square 內，故 interval volume ≤4T³。
相對 `dt dx₁ dx₂` 的 homogeneous Poisson 過程在 bounded boxes 幾乎必然有限；
以 rational bounding boxes 的可數 cover 即同時得到所有 sampled intervals 的 LF_o。
這個全非緊緻模型也滿足 NV_P、translation homogeneity，並可配獨立 positive-definite g_E。

但 t=1 的 future-cone section 是 square，不是 nondegenerate Lorentz quadratic cone 的
elliptic section；它也不具 continuous spatial rotation isotropy，更沒有證明 relativity
principle。此例只證明以上弱前提不足，不排除另加 isotropy／group／metric compatibility
後的 Lorentzian 結論。cone 的「速度」已在外部定義中放入，不能算 finite c 的湧現。
未證橋接：B3、B4、B5。

### 4.2 引理 E：完整 Euclidean spacetime rotations 與非平凡 oriented order 不相容

**前提：** R^D、D≥2 上的 strict order 對 translations 與整個 SO(D) invariant，
且至少存在 `p≺p+z`、z≠0。注意 SO(D) 旋轉的是 **全部 spacetime directions**，
不只是 spatial rotations。

**證明：** 存在旋轉 A 將 z 送成 −z。繞 p 旋轉，得到 `p≺p−z`；平移 z，得到
`p+z≺p`。與 `p≺p+z` 合成即 `p≺p`，違反 irreflexivity。故不存在此 relation。□

引理不使用 Poisson、不構造 K，也不證明 Lorentz group 必存在。反例 A／B 的 g_E
附帶 clock／order，並未滿足完整 spacetime SO(D) invariance，與此引理沒有矛盾。
因此 G0-B 有一個可複核的 **symmetry-relative no-go**，但不能寫成「一切 Euclidean
ambient metric 均被 bare causal order 排除」。未證橋接：B3、B5。

## 5. Galilean：compact 反例與 full-space 排除都要保留

本文的 Galilean **absolute-time causal order** 定為 `(t,x)≺_G(t',x') iff t<t'`。
它表示沒有 spatial propagation restriction。不是所有 Newtonian／Galilean equation
的普遍 causal prescription；排除這個 order 不等於排除一切 Newtonian theory。

### 5.1 反例 C：compact 空間保留 unlimited propagation 與 LF_o

取 `M=R×S¹_L`，L>0 為圓周長，μ=`dt dx`，NV_P density ρ>0 constant，採 ≺_G。
對任何 finite t<t'，interval 是 `(t,t')×S¹_L`，measure `L(t'−t)`；
count 為 Poisson(ρL(t'−t))，幾乎必然有限。所有 bounded-time slabs 的有限性由
可數 integer slabs 同時成立，因而任意 sampled pair 的 interval 都有限。
這個 realization 是 locally finite poset，卻允許任意兩個 spatial positions 以任意
正時間差相連，沒有 finite propagation cap。

translations 與 `t'=t,x'=x−vt mod L`（所有 real v）的 Jacobian determinant 為 1，
保持 μ 及 ≺_G，故 sampling law 和 order 都有此 Galilean boost invariance。
一個 realization 不必 invariant；此處區分 deterministic order 的 covariance 與
process law 的 invariance。反例也有 time／space translations 與 1D spatial reflection。

整個 spacetime 是 noncompact（t∈R），但 spatial volume 有限。故只寫「均勻、
非緊緻」仍不足以排除它；若另外要求 **spatial infinite volume**，此反例被排除。
它不是 full R^{d+1}、也不提供 3D continuous rotation symmetry。受否定的是缺少這些
限定的 G0-C 蘊涵，不是任何已完整指定的加強版。未證橋接：B1–B5。

### 5.2 引理 G：full 無界空間的 absolute-time Poisson order 不是 locally finite causet

**前提 G：** M=`R×R^d`、d≥1，μ=`dt d^d x`，ρ∈(0,∞) constant，full-space
NV_P 抽樣，並把 ≺_G 限制到 sampled points。要求 LF_o。

**證明：** 任意 rational a<b 的 slab `(a,b)×R^d` 可分成 countably many disjoint
spatial unit cubes。前 M 個 cubes 的總 count 為 Poisson(λM)，λ=ρ(b−a)>0。
對任何固定 integer k≥0，

$$\Pr\{N_M\le k\}=e^{-\lambda M}\sum_{j=0}^k(\lambda M)^j/j!\longrightarrow0.$$

由 N_M 單調，slab 的總 count 幾乎必然無限；所有 rational slabs 可數，故這個結論
同時成立。對任意 sampled p≺_G q，選 `t_p<a<b<t_q` 的 rationals，該 infinite slab
全在 I_C(p,q) 中。因此幾乎必然每個此類 interval 都無限，LF_o 失敗。□

這不是沒有 comparable pair 的真空情況：兩個時間上分離的 rational slabs 都有點，
從各取一點即可得到 comparable endpoints。

同一過程在每個 bounded box 仍幾乎必然有限，所以 LF_top 不會修復 LF_o。
compact truncation 或 integrable nonuniform spatial density 可避開證明，因為它們
違反 full infinite-volume／homogeneous 前提；不能偷偷用截斷模型代表前提 G。
本引理的 paper probability limit 不是進行了抽樣或估計 failure frequency。

**可用的前進方向：** 若有獨立論證要求這整組前提 G，確實可排除這個 Galilean
unlimited order。然而 full R×R^d、continuum measure、positive homogeneous density
與 order prescription 並非由 L0 已導出，不能把條件式排除報成前時空證明。
未證橋接：B1–B5。

## 6. 「排除伽利略」到 finite invariant c 還差什麼

為避免名稱碰撞，這裡用 κ 表示運動學參數；不是候選 kernel K。
在已限定的一個 affine boost family，可用 (t,x) 形式表示為

$$B_\kappa(v)=\frac{1}{\sqrt{1-\kappa v^2}}
\begin{pmatrix}1&-\kappa v\\-v&1\end{pmatrix}.$$

κ>0 有 invariant speeds ±1/√κ；κ=0 為 Galilean boosts；κ<0 的完整群對應
rescaled Euclidean rotations。這只是 **已假設該 family** 後的分類，不是從 poset
證明 transforms 必屬它。formula 使用原點固定、共線 boost、適用 chart 的 conventions。
Gate 0 舊文件把 Lorentz branch 記為 K_G0<0，尚未固定同一個矩陣公式；若另定義
`K_G0=−κ`，兩者的 branch signs 相符。這不是從舊文導出其數值 normalization，
不能把不同來源的 K 符號直接混用。

在 κ>0、|u|,|v|<c=1/√κ 的正時間定向 chart，direct matrix multiplication 給

$$B_\kappa(u)B_\kappa(v)=\gamma_u\gamma_v
\begin{pmatrix}1+\kappa uv&-\kappa(u+v)\\-(u+v)&1+\kappa uv\end{pmatrix},
\qquad w=\frac{u+v}{1+\kappa uv}.$$

其中 `1−κw²=(1−κu²)(1−κv²)/(1+κuv)²`，所以乘積確為 B_κ(w)。
對 trajectory 的 coordinate speed s，單次允許的 boost 給
`s'=(s−v)/(1−κvs)`；代入 s=±c 即 s'=±c。這只用 |v|<c 的 boost，
**沒有使用奇異的 B_κ(c)**。κ=0 時 s'=s−v，非零 finite c 不會對所有 v invariant。
κ<0 的 partial chart 不可當完整 closed group；§4.2 要求的是完整 rotation
symmetry，不以任意砍掉會反轉 time 的 rotations 規避。

**條件式串接，而非已完成推導：** 若先證得所選公理確實只留下這個 family，且
非平凡 oriented order 排除完整 Euclidean branch，再以與該 Galilean branch 相容的
前提 G 排除其 absolute-time sampling model，就能在該 restricted class 選出 κ>0。
但 presently 尚未證明：poset 推出 affine spacetime／inertial group、其表示與本 family
一致、sampling assumptions 是必要的、或別的 kinematics 已窮盡。即使 κ>0，也還
沒有其 physical value、signal dynamics、dimension 3+1 或 Hilbert／quantum consistency。
排除一個類別不會自動提供剩下類別的存在性。未證橋接：B1–B7。

## 7. 原作者文獻：前提矩陣與不可倒用的結果

2026-10-11 核對以下原作者來源；只採核對到的作用域。不是指定新 acceptance gate。

| 原作者來源／定位 | 已預設的結構 | 可引用的結果與界線 |
| :--- | :--- | :--- |
| [Malament (2005), Classical General Relativity](https://arxiv.org/pdf/gr-qc/0506065v2), §3.3、Eq.(58)、printed pp.53–55 | review 中已定義的 temporally oriented relativistic spacetimes；past **and** future distinguishing；bijection 雙向保持 chronology ≪ | causal isomorphism 重建到 conformal equivalence；不是任意有限 poset 的 manifold 存在定理。本文核對的是作者 review 版本，未以完整 1977 原文重做證明，也不將 4D review 直接套到 1+1D |
| [Hawking–King–McCarthy (1976)](https://authors.library.caltech.edu/records/6apqj-ep466), 原文 repository abstract | strongly causal spacetime 與所定義的 path topology | 與 causal／differential／conformal structure 的關聯；本輪原 PDF 未成功取得，**只核對 abstract**，不據此宣稱已核完整定理或以 bare order 取代 topology |
| [Llosa (2014)](https://arxiv.org/html/1401.6568v1), §§2–4.1、6 | 既有 inertial frames、law of inertia、Euclidean **spatial** geometry、rest／velocity assumptions、非平凡 invariant time precedence | 在該版本前提下留 Lorentz-like 或 Galilean；前提不來自 bare poset。其 K>0 為 Lorentz，與 Gate 0 舊符號相反，見 §6 |
| [Anker–Ziegler (2020)](https://arxiv.org/pdf/2007.09301v2), Theorem 1、Eq.(4)、Introduction cases (a)–(e) | spatial n>2；G⊂GL_{n+1}(R) 的明訂 block-intersection condition | 該較不同的定理有 Lorentz／Galilei／orthogonal／Carroll／Aristotle 五種可能，故不能跨公理版本宣稱只存在三種運動學；不直接適用 spatial n=1 的 Stage 5C |
| [Nicholas (2026)](https://arxiv.org/html/2606.25993v1), §2.1、§5 的 nondegeneracy／extension、§6 | 已給 R^n、n≥3，invariant interval function D、smoothness／homogeneity／isometry／determinism | 作者明列 signature 未被唯一決定，包含 definite、Lorentzian 與 ultrahyperbolic。其排除 degenerate interval 是在既定 D 框架內的作者結論；本輪不獨立認證全篇證明，不作 pre-spacetime／finite c 承重依據 |

「沒有光速 postulate」不等於「沒有 background geometry、clocks 或 inertial structure」。
Anker–Ziegler Eq.(4) 是 `G∩diag(GL_n(R),R×)=diag(O_n,±1)`，明含 time reversal。
因此不能要求其完整 G 同時保持一個有方向的 chronology，再拿 §4.2 作分支選擇；
若要討論 time-oriented observers，必須另外固定相應 subgroup 與它保持的 relation。
§6 的條件式 family 並未宣稱已由該定理取得這一組前提。
Malament/HKM 的 reconstruction 和 Nicholas 的 interval classification 都不能逆向當作
Layer 0 的 generation theorem。smoothness、continuum dimension、volume measure
若要成為導出量，就另需 B1–B5；若決定採為物理公理，則承認問題範圍已條件化。

## 8. 未證橋接帳與下一個低成本交付

| ID／義務 | 已有支持 | 缺口／可先做的證明方法 | 不充分時怎麼處理 |
| :--- | :--- | :--- | :--- |
| B1 manifold／continuum／dimension | 已有 finite diagnostics 與 continuum benchmarks | 具名何種 poset law 有 manifoldlike limit，定義 existence、dimension 與辨別準則；不以有限圖能嵌入代替 | 維持「給定 continuum 類別的條件研究」，不稱已湧現 |
| B2 number–volume／density | count 是 intrinsic；evaluator 有指定 sampling law | 指定 measure、ρ、均勻性／ergodicity、是否獨立 Poisson，及 scale 的校準角色；§3.1 可先查識別性 | 不以裸 # 當已知物理 volume；不把 NV_P 默認為 L0 定理 |
| B3 admissible symmetry／inertial group | 有 BHS 限制與既有 U/V 診斷 | 從 primitive 到 observer equivalence／group action 的必要條件；先明定 invariant order 是哪種 relation | 不能把 SO(D)／Galilean／Lorentz group 放進前提後稱已生成 |
| B4 clocks／rods／速度單位 | 暫有 evaluator units | 區分 dimensionless ratios、density scale 與 operational units；證明同一速度對全部允許 observers 不變 | 不從無單位數字推出 299792458 m/s；不以選 c=1 當推導 |
| B5 order–cone–metric compatibility | §4.2／§5.2 的 narrow exclusion；文獻 reconstruction | 定義 proper cone、continuity、isotropy、finite interval volume 與 metric class 的連接；先檢查哪些前提不可少 | 反例 A/B/C 只否定弱版本；不能拿它們否定已限定強版本 |
| B6 signal／mass／quantum dynamics | Stage 5C acceptance 已列回復義務 | 區分 causal accessibility 與實際 propagation，列存在性／positivity／CAR／continuum-limit 義務 | 本輪不設計 K，不報質量或物理傳播已導出 |
| B7 3+1D、單一 time signature、gravity | README 明列尚未完成 | 證哪個結構排除其他 dimension／多 time directions，及真正 dynamics 選擇，而非再命名 | 維持 OPEN；1+1D success 不外推 |

**下一份建議：B2＋B5 的 finite-interval-volume／cone 前提審計。** 固定一個已承認
背景假設的 restricted continuum problem，尋哪些 cone／measure conditions 足以有 FV，
哪些反例仍保留；同時列出將來若要由 poset 導出它們所需的 B1／B3 工作。
不推薦新 K、weight、order ansatz 或 phase law；這是運動學必要條件的問題。
若希望改採某個額外 physical primitive，另記 conditional scope，不冒充原主題已解。

## 9. 狀態與否定結果的保存

本審計給出四類反例／識別缺口及兩個 narrow conditional exclusions；它們有完整
紙上推導，仍待 exact-head 獨立複核。Gate 0 G0-B／G0-C 的總目標維持 OPEN，
Layer 0 尚無模型；no-go 只限於列明的假設組。沒有把量測預算或 E4 數值改成結論。

PR #70 的【提案】措辭修訂是專案證據規則的明文改動：允許完整可核的解析證明，
不是讓未證敘述免驗。這一輪運用該規則提出紙上命題，不新增較寬鬆的 scientific gate。
6a-S 封存、run1、O19、witness、item 7 不可 ADOPT、items 3–5 v0.2 重驗待辦、item 8 OPEN、
6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING 與 K 禁令均不變。
