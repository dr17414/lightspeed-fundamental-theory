# B4＋B6：時鐘、尺規、訊號的紀錄與實現必要條件審計

狀態：**【探索／限定解析待獨立複核；實現與物理橋接 OPEN】**。
基線：PR #73 squash main `4ff0227e853e9c07c8a9fb49ea8ede13f87134dd`，
tree `e6cec988a365a62f10b964a9af2cf3773918232f`。
承接 [B3＋B4](b3_b4_operational_clock_observer_audit.md) §5–§8 的 calibrated family
與裝置缺口；[B2＋B5](b2_b5_interval_volume_cone_audit.md) §2、§6 的 Poisson／volume。
本稿定義研究所需的**紀錄契約**及外部 countermodels，不給任何產生物質、時計或
訊號的 dynamics、candidate K、order ansatz、weight、phase law 或構造材料。
沒有新抽樣、量測、seed、主機、E4／selector witness、正式資料或 arm ledger。

## 0. 六欄契約與結論

| 欄位 | 內容 |
| :--- | :--- |
| 命題 | 一次時間／長度比較需要什麼紀錄？bare order＋count 是否識別 tick、proper-time calibration 或訊號／延遲？哪些義務才跨入模型實現？ |
| 定義域與輸入 | §1–2 任意具名 poset 及其裝飾紀錄；§3–5 另限已給 calibrated flat Lorentz metric／worldlines／指定 Poisson law 或 ideal echo 的外部比較類 |
| 證據 | Q 的 fiber 判準與有限鏈反例；J 的標準時計與 nonlinear regraduation；C 的單 count 非精確識別；Z 的 Poisson 無 exact null pairs；R 的回波／延遲反例及 error bound |
| 未證橋接 | B1 continuum／dimension；B2 density／measure；B3 observer action；B4 stable tick／rod／calibration／sync；B5 causal relation；B6 preparation／propagation／interaction／readout；B7 gravity／dimension |
| 否定條件 | 限定反例只否定所列輸入的蘊涵；不將 missing law 當所有物質模型不存在，不將無 exact null pairs 當無有效 light propagation |
| 後續驗證 | exact-head 數學與 scope 複核；若要回答裝置是否存在，下一步須具名模型與適用域，先另案處理探索軌道權限／資料分離 |

**目前能結案的是資訊需求，不是裝置存在性。** order 可檢查已具名紀錄的先後一致性，
但不能把任意 chain 直接指派為穩定鐘錶，把可及性當作實際 emission／detection，或把
回波總時間全部算成幾何距離。幾何 proper time、實際 tick、校準後顯示值是不同物件。
單靠「更多點／更多記錄」不會補上未定義的 interaction／readout law。
這也不證明物質是唯一可能的新 primitive；boundary／marks 可加入資訊，但須入帳。
B1–B5 仍有獨立義務，不能因研究碰到 B6 就當作全部已解。

## 1. 一次比較的最小語意帳：order 可核對什麼，還缺什麼

令 U(R)=(P,≺,#) 忘掉紀錄 R 中所有額外 marks／readout，保留 intrinsic poset。
這是紙上 forgetful map，不是 repo runner／schema 或新的資料檔。
若給刻度，顯示值記 t_A；未校準的 integer tick label 記 n_A；幾何 proper time 記 τ_g。
三者不得以同一個「時間」欄混用。

| 紀錄欄位／一次比較要知道什麼 | order／count 已能做的事 | 額外資訊與來源義務 |
| :--- | :--- | :--- |
| 物件 A／B 與兩次讀值發生在哪些事件 | 已選 events 的 equality／precedence／interval count | 哪些 events 屬同一裝置或 worldline，identity 如何維持；chain 不自動是物質軌跡 |
| tick events、整數 n_A、起迄與漏讀紀錄 | 已標 tick 的排序／差值 | tick 是哪種可重複 process、如何 detection、漏／重複的 error law；標記不在 bare order 中 |
| calibration n_A↦t_A、參考刻度與單位 | 保存已給的 dimensionless tick ratio | 常數或漂移函數的來源、state／運動適用域、裝置間一致性；不是事後令 t_A=τ_g |
| emission、response、reception 的配對 | 在已宣告 relation 下查箭頭是否相容 | signal identity、source／detector interaction、background／medium、實際 support、延遲、failure／ambiguity |
| rod 兩端、同步與長度比較 | 查已具名 endpoint events／messages | 端點是什麼物件、simultaneity／rest frame、穩定 separation 或 return-time prescription；沒有預設 rigid rod |
| preparation、state、boundary、observer action | 維持 relabeling／isomorphism consistency | 全部資料如何 transform；比較的是 law、state 或裝置，不把 passive description 當 active physical equivalence |

這些欄位是**要由未來理論解釋的目標語意**，不是現在增加進 L0 的公理。
若某欄僅靠外部 metric、座標或裝置 mark 定義，標為 conditional input；不得借此
反證「它已從 poset 湧現」。本稿只用它們檢查 logical sufficiency。

### 1.1 relation 的型別：chronology、causality 與 signal record

前兩稿的 continuum strict relation 是 `q−p∈int 𝒞`（chronology），不包含 null boundary。
在**已給 continuum** 中另外可定義 weak causal relation `q−p∈𝒞`；它與 strict order
不同。裸 finite poset 沒有既定 topology，不可悄悄用 closure 產生新的 null relation。
訊號紀錄 S 是實際宣告／推導的傳輸配對，須相容於模型明訂的 causal relation，
但 relation 的存在不代表 S 包含所有可及對，也不證任一 pair 有 signal amplitude。
§5 的 ideal null echo 使用外部 weak relation，**不用 strict chronology 把 null legs
誤標成 interior pairs**；裝置沿 timelike worldline 的 readings 仍可依 strict order 排序。

## 2. 命題 Q：內在可識別性必須在忘掉額外資訊後仍單值

對具名允許紀錄類 𝓡、forgetful U:𝓡→𝓘、目標讀值 F:𝓡→𝓥，
存在只靠 intrinsic input 的 f:U(𝓡)→𝓥、滿足 F=f∘U，**當且僅當**

$$U(R_1)=U(R_2)\ \Longrightarrow\ F(R_1)=F(R_2).$$

必要性由 f 的單值性立即得到；充分性則對每個 i∈U(𝓡)，以其 fiber 共同值定義 f(i)。
這是 set-level factorization，**不保證** f 可計算、measurable、穩定或符合 physics；
isomorphism classes 上也必須以 relabel-invariant 目標／輸入作同樣判準。□
一個反例只否定指定 𝓡 的 sufficiency。將來新增 dynamics／state law 若排除其中一份
紀錄，必須明列新增前提；不能說 Q 禁止所有由更豐富 intrinsic law 得到的裝置。

**反例 E：** 固定五事件 chain `p₀≺p₁≺p₂≺p₃≺p₄`，兩紀錄都讀 p₀ 至 p₄。
R₁ 的 tick set 是 {p₀,p₂,p₄}、labels 0,1,2；R₂ 是全部五點、labels 0,1,2,3,4。
兩者 ticks 都單調，U 完全相同，卻有 Δn=2 或 4。沒有假定兩者 tick-spacing 均勻；
這正是裸 order 沒有給的條件。故 tick 數本身不由此 U 唯一決定。
它也不證這兩個裝置已被某種物質 law 實現；只是一個 missing-mark countermodel。
事件總數與 tick 數不是同義詞，任意最長鏈或 canonical label 亦不能無證明代換。

## 3. B4：幾何 standard clock 與真鐘校準的差別

### 3.1 命題 J：給定 worldline／metric 後的標準刻度只差正 affine 變換

**另給** calibrated flat metric g（signature +−…−）、smooth future-timelike curve
z(τ)，以幾何 proper time 參數化，`g(dz/dτ,dz/dτ)=1`（units c=1）。
取 connected interval 上的 C² regraduation `s=φ(τ), φ′>0`，chain rule 給

$$g\!\left(\frac{dz}{ds},\frac{dz}{ds}\right)=\frac{1}{\phi'(\tau)^2}.$$

右側為 constant **iff** φ′ 為 positive constant **iff** `s=aτ+b, a>0`。
因此 geometric standard-clock class 唯一到 unit／zero 的 affine 自由；order
只保 φ 單調，並沒有 φ′ constant 的條件。□
這不是新 oscillator／matter law，也不是從 bare order 導出 g 或 z。

**反例 D：** 即使某顯示已在兩端對準 proper time，也不能保證中間均勻。
給 T₀>0、0<|ε|<1、τ∈[0,T₀]，

$$s_\varepsilon(\tau)=\tau+\varepsilon\tau(1-\tau/T_0),\qquad
s_\varepsilon'=1+\varepsilon(1-2\tau/T_0)>0.$$

兩端 s(0)=0、s(T₀)=T₀，卻有 `s(T₀/2)=T₀/2+εT₀/4`；metric norm 不為常數。
它保 readings 的 order，不保 standard-clock property。未有 rate law／error bound，
一個 calibration interval 不足以證 uniform ticking 或跨運動、state 的 universality。
已校準 integer ticks 通常只給有限 resolution；J 的 smooth s 是幾何比較類，
不得把有限 tick 樣本當成 φ′ 已被逐點證成常數。

### 3.2 命題 C：單一 Poisson interval count 不能精確讀出 proper duration

另限已給 Lorentz cone、positive fixed ρ、dimension D=d+1≥2、calibrated metric，
取**外部指定**兩 timelike-separated endpoints、proper duration τ>0。
前稿的 rest-interval formula 與 calibrated Lorentz symmetry 給

$$N(I)\sim\operatorname{Poisson}(k\tau^D),\qquad
k=\rho\,\frac{v_dc^d}{2^d(d+1)}>0.$$

假設只靠這一個 N 有 deterministic f(N)=τ 幾乎必然，且對此類每個 τ 都成立。
任取 τ₁≠τ₂，兩個 law 的 `Pr(N=0)=exp(−kτ_j^D)>0`，故需要
f(0)=τ₁ 同時 f(0)=τ₂，矛盾。□
本命題只否定**單 count 的 exact readout**；不否定 noisy estimator、多份資料或
帶更多結構的統計重建。`(N/k)^(1/D)` 即使拿來作估計，也需 k／dimension／sampling
law 和 error analysis，且不是裝置已產生 ticks。N 的 expectation 與 interval volume 成比例，
非沿 worldline 以固定速率發生的事件數。本稿不實作或測試任何 estimator。

## 4. B6：可及 relation 不等於 signal，exact null edge 也不能默認存在

### 4.1 命題 Z：full homogeneous Poisson 的不同撒點幾乎必然沒有 exact null pair

在給定 full Minkowski R^D、D≥2、normalized Lorentz coordinates（c=1）、
positive constant density 的 Lebesgue Poisson law 中，
幾乎必然不存在不同撒點 p,q 使 `g(q−p,q−p)=0`。
這是過程 law 的解析命題，不生成 realization。

**證明（含 random-endpoint 同時性）：** 取 positive finite-volume bounded box Q。
conditional on N(Q)=n，n 個點的 unordered joint law 是 iid uniform on Q。
可從 Poisson 定義核對：任意有限 measurable partition Q=⊔Q_i 的 independent counts
在總數 n 條件下為 multinomial，cell probabilities μ(Q_i)/μ(Q)；這正是 iid uniform
位置的無序 law，所有這類 partitions 確定該 point-process restriction。
對 fixed p∈Q，null-separated q 的 set 有 D-dimensional Lebesgue measure 0：
給定 spatial q，time q 必須取兩個 `p_t±‖q_x−p_x‖` 值，以 Fubini 得零。
再對 p 積分，任一 iid pair exact null 的機率零；對有限 n 的所有 pairs finite union
仍為零，再對 n 的 Poisson mixture 得同一結論。用可數 boxes Q_m=[−m,m]^D
涵蓋全空間，任意 pair 皆在某 Q_m，countable union 得全域幾乎必然結論。□

**作用域：** 固定 g／continuum／Poisson 已是前提；不是所有 posets 的定理。
此 full-volume sampling law 下，沿連續光錐精確傳輸的端點不能直接聲稱是兩個既有
撒點之間的 exact null edge。另選／加入 emission／detection marks、有限寬 detector、
coarse-grained records 或某有效 continuum correspondence 都需要新的具名義務；
本稿不提出其中任一機制或構造材料。
Z **不排除**透過多點、非局域 quantum object 或極限形成有效傳播，也不授權這些
方案；它只撤去「已有 order 所以已有 null signal path」這個無證據代換。

### 4.2 真正承重的是完整 signal／record law

要識別一次 transmission，至少要明訂 source 的 preparation、signal 支援、response、
detector interaction 與 readout；還要知道 signal 是否丟失、multipath 或誤配對。
給 causal arrow 的可及性不等於存在 propagator／signal，更不等於一個機率 1 可讀出
的 channel。若使用 probability／quantum law，state、pairing、positivity、normalization
和 operational record 的對應需各自有證據；不是任意正 scalar record 就等於物質。
這是 B6 義務清單，**不增加 acceptance gate 或提供 K／inverse／state prescription**。
將來若用既有文獻裝置作 conditional benchmark，其所有 background／materials 仍入帳。

## 5. 一次長度比較：先定義回波讀值，再審查何時等於距離

### 5.1 命題 R：ideal flat rest echo 下的 geometric 解碼是條件式的

另給 flat 1+1D `ds²=c²dt²−dx²`、c>0；A 在 x=0、B 在 x=L>0 都保持 rest，
A 的 calibrated reading 等於 t（同 unit／zero）。**再給** freely travelling null legs、
B 在同一事件零延遲反射、已正確配對的唯一回波：t₋ emission、t₊ reception。
這是既有 geometry 的 external ideal-echo 比較，不是生成此 signal 的 dynamics。
兩條 null equations 是 `x=c(t−t₋)` 與 `x=c(t₊−t)`，因此

$$t_B=\frac{t_-+t_+}{2},\qquad
L=\frac c2(t_+-t_-).$$

在以上條件中它等於 B 的 rest separation；inverse 代入兩條 equations 即驗證。□
單 observer 的 echo coordinate 不等於一般 curved／accelerating situation 的 proper
rod length，更不提供不同 device 的 clock calibration。實際不存在／不唯一的 signal
須記為 unavailable／ambiguous，不能先默認唯一值再報為測量成功。

### 5.2 反例 L：未知 response latency 與長度不可由總 return time 分離

仍給 A／B flat rest、兩條 speed-c legs，但 B 在收到後等待 δ≥0 再送回；
δ 與 A 的 time unit 相同（因兩者 rest 且同校準），其他 source／detector 延遲先設零。
從接收 B_in 的 t₋+L/c 到發送 B_out 的 t₋+L/c+δ，有

$$T=t_+-t_- =2L/c+\delta,\qquad D_{\rm naive}=cT/2=L+c\delta/2.$$

對 fixed T>0，任取 `0<L≤cT/2` 與 `δ=T−2L/c` 都給同一 T。
例如 `(L,δ)=(cT/4,T/2)` 或 `(cT/8,3T/4)`，兩者都 δ>0，四個事件的
弱 causal chain 與 strict timelike／null 關係型別相同，幾何長度不同，T 相同。
即使兩者的 emission／response／reception sequence 相容，仍不可由 T 唯一解 L。
**δ>0 時 B_in 與 B_out 是不同 events；不能把它們硬合成 R 的單一 reflection event。**
若先有 `0≤δ≤δ_max`，才得 `L∈[c(T−δ_max)/2,cT/2]∩(0,∞)`。
這是 conditional uncertainty interval，不是本專案的採用 cap 或測試門檻。

對同一 rest 模型，若已給讀值 `t̂_±=t_±+e_±, |e_±|≤ε`，定義
`D̂=c(t̂_+−t̂_-)/2`，triangle inequality 得

$$|\widehat D-L|\le c\varepsilon+c\delta_{\max}/2.$$

此 bound 另假定 c 精確、legs 理想；共同常數 clock offset 在差值中相消。ε 必須
涵蓋所宣告的 reading 誤差（包括 drift，如其已受界）；c 的 calibration error、motion、
medium 或 multipath 不在此模型中。若那些也存在，必須另加具名界；
本稿沒有替未知量指定有利數值，亦未設新的 numerical protocol。

### 5.3 rod 與兩地 clock 比較仍要指定 simultaneity／identity

在給定 metric 與 observer u 下，前稿 `V_u,‖·‖_u` 能定義同時切片上的 separation。
但要把它叫 rod length，需要知道兩個端點屬於什麼物質、如何保持／判斷 rest，
以及哪些 endpoint events 同時。bare order 對 incomparable pairs 不自動選 simultaneity。
多 clock 的比較還需 transmission pairing 和其延遲／同步契約；只把兩邊 labels 都設為
相同數字，不會證成 rates 相同。本稿既沒有 rigid-rod dynamics，也沒有同步裝置設計。

## 6. 從紀錄一致到裝置實現：不能省去的證明義務

下表不是新 prereg／runner gate，亦不是決定採用任何 model family。

| 義務 | 已可解析核對 | 裝置／B6 仍需什麼 | 缺少時允許的結論 |
| :--- | :--- | :--- | :--- |
| R0 可識別性 | Q 檢查額外 marks 被忘掉後目標是否同值；E／L 反例 | 完整輸入／state law 是否限制了 fibers；不能用 hidden lookup 解歧義 | 只報需要額外資訊，不報 intrinsic readout |
| R1 tick 的實現 | J 識別 geometric standard parameter；D 阻止單 calibration 推普遍 rate | 穩定可重複 process、readout mapping、resolution、drift／運動適用域 | geometrical target 或條件 benchmark |
| R2 signal support／response | relation 型別、Z 的 sampling 限制、R／L 的解碼條件 | preparation、傳輸、接收、response、概率／quantum law、error／failure、continuum correspondence | causal accessibility；不報真 signal 或測到 c |
| R3 rod／同步／刻度 | observer family 已有；rest echo 可以有條件解碼 | 端點物件、state、rest／rigidity 域、clock／rod unit 與 cross-device calibration | observer-dependent coordinate assignment |
| R4 observer equivalence | 記錄 contracts 的 relabeling／covariance 可檢查 | 操作、state、boundary 和完整 law 的 group action；固定 mark 不會被偷偷忽略 | 數學 covariance；不報全部 physical devices 等價 |
| R5 未證前提與有限誤差 | 給定 bounds 才能傳播 uncertainty | 哪些由 L0／L1 導出、哪些額外 physical primitive、哪些是 L4 evaluator；每項適用域與誤差證據 | 條件結果＋OPEN ledger，不把假定 readout 反證成湧現 |

因此現階段的欠缺不只是「多做一輪 statistical validation」。沒有具名 mechanism，
validation 甚至沒有要驗哪個裝置／state／record law；沒有完整模型，也不能由本稿
反例斷言其不存在。幾何相容、模型 existence、穩定性、readout、誤差、跨 observer 的
law 是不同 proof obligations；一張合格紀錄不會自動全部承擔。

## 7. 已碰到的協定決策點與下一步

本稿完成必要條件的有限交付，B4／B6 仍 OPEN。若下一步只再問「還缺哪些資訊」，
可以繼續紙上審計；但若要回答「有沒有一個可運作的鐘／尺／signal」，就必須有
**具名的實現問題**。可以選既有模型的 conditional analysis，也可能需新 dynamics；
它是否觸及候選 K／order／weight／構造材料，須先與 operative 規格逐項對照。
沒有證明所有 B6 路線都必須用本專案的 K，更不能把 B6 OPEN 當作 K existence 的證據。

**建議的下一份是探索軌道協定修訂的決策草案，供操作者裁決，尚不在本稿啟動。**
先在 [理論優先路線圖](../THEORY_FIRST_ROADMAP_DRAFT.md) §5 的框架下明訂：

1. 允許的實現問題／scope：原 Stage 5C 1+1D massless claim 與 clock／rod 裝置是不同
   主張；新 physical primitive／conditional background 要明列，不靠重命名獲得權限。
2. 探索許可及 exact forbidden boundary：允許何種紙上模型／toy objects；正式凍結前
   候選 K 禁令若需修訂，需同步審 acceptance §0／D.1、STATUS、prereg，不能只改標籤。
3. 暴露與資料隔離：研究者已看過的 fixtures／controls／失敗結果完整記帳；哪些
   evaluator oracle 永不回流，哪些資料可以探索，正式確認需要何種新凍結與獨立審查。
4. 交付／停止條件：具名定義域、existence／no-go、有限誤差或適用域；探索模型／觀察
   標【探索】，完整解析證明可依獨立複核限定升格；不產生 scientific PASS 或自動授權
   seed／host／量測。

草案獲審並得到操作者明確決定之前，繼續遵守現行禁止候選設計的規則。
本稿**沒有 amendment、沒有新執行授權，也沒有模型公式或材料供 K 使用**。
這是把下一個 research decision 做成可審對象，不在紙上偷偷跨過禁令。

## 8. 文獻定位、複核重點與保存邊界

2026-10-12 讀取 [Perlick (2007), arXiv:0708.0170v1](https://arxiv.org/pdf/0708.0170v1)，
§1–3、Eqs.(1),(2),(5)：作者已給 4D smooth time-oriented Lorentzian manifold、
parametrized timelike clock、freely propagating null geodesics；clock 不先要求 uniform。
standard clock 在既定 g 下限到 positive affine parametrization。這只對照 §3、§5 的
術語和背景；本文 J／R 自行短證，Q／C／Z／反例自行給證據。
Perlick §2 的局部 radar-neighborhood 討論不作 bare poset 的存在定理，也不把其
§3 的 free-particle clock test 當成已從 L0 實現：其中的 particles／reflection 是額外輸入。
本文 signature 為 +−…−，作者為 −+…+；本稿不引用其太陽系估值或未複核的完整定理。

請獨立核對 Q 的 set-level／計算性 scope；J 的 monotone 與 affine；C 的單 count
限定；Z 的 conditional iid／random-endpoint simultaneous argument；R 的弱 causal
relation／零延遲；L 的雙 response events／identifiability 與 error bound；以及紀錄
contract 並非物質／K 構造。N／A／I／F 的既有已核準結論照原前提使用。

本輪既有程式、tests、CI、manifest、registry、run1 evidence／assessment、witness、
closure 全保留。6a-S 封存、item 7 不可 ADOPT、items 3–5 v0.2 重驗待辦、item 8 OPEN、
6a-E PREREGISTRATION-INCOMPLETE、Freeze-1a PENDING 與候選 K 禁令不變。
