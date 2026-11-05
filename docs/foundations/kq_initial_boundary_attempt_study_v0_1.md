# IB-01 v0.1 — 固定初值試作的紙上研究與失敗紀錄

狀態：**【探索／待exact-head獨立複核】**。研究稿交付：2026-11-05 Asia/Taipei。
Problem ID `X-KQ-COND-TA-P0.2`；model ID `X-KQ-IB-01-v0.1`。
探索軌，不具 §5.2.1(v) 依據資格；所有結論只限外加 Ξ=(L,R₀) 與已固定 B-01。
本稿使用已合併的 [IB-01規格](kq_initial_boundary_attempt_spec_v0_1.md) 的原係數、七格、
全部合法面與固定判準。先交§2的完整固定目錄（含FAIL／undefined），再於§3起解釋原因。
先行接觸漏登在本地三帳commit `30adb53f`（本地Git時間台北2026-11-04；公開Git無法驗證該時間）
事後更正；公開重建commit `1f71e8b9` 的時間為台北2026-11-05 14:47:45，同tree而不同SHA。
不冒稱規格前已在Git登記。#105合併與方向討論發生於11/3，研究稿在其後撰寫。
本地／公開兩層commit對照及程序更正見接觸帳§61與開發帳末段。
規格前作者曾在腦中預算C₃的非unitary／Green風險，見原規格§1／EXP-0122；本稿不是盲發現。
Claude於#105複核提出的六點提示已見，均在§1、§2、§4–6具名定位，不冒稱作者獨立發現。

## 1. 記號、判準與事前結構分類

沿用規格的T、J、D_C、B₀、I、ρ、ι、D、M、G_R與G_A。此處以
\(W_C=E_CE_C^\dagger\) 表示規格§6的 \(L_C\)，避免與線性延伸 \(L\) 同名；
這只是研究稿的記號別名，**不修改已固定規格**。\(A_C(f,g)=h_P(f,W_Cg)\)。
\(F_C=\gamma_CG_R\iota_B:D_{B_0}\to D_C\)。若F_C不可逆，該面E_C、W_C、A_C及
涉及該面的比較為undefined，不能用廣義逆或刪面；其他已定義面的失敗照判FAIL。
\(n_{\rm cov}\)、\(n_{\rm ind}\)沿B-01。
矩陣式一律以共同h₀正交表述；\(\eta=\eta_0\)有正負各一維，I及η線性獨立。

**先於任何輸出、只看B與原P的分類。** 兩端均在I的strict可比對，在固定六例中
只有C₃、C₄與diamond有；三葉star、2×C₂、3×C₂沒有。跨尺寸固定族中，
鏈C_N（N≥3）有，三葉一般化的向下star、dual star及Φ族k×C₂均沒有。
這個分類不依K、G_R或A；空族不算獨立Green識別成功。星形方向固定：
「向下三葉star」是三片**minimal**葉子同指一個上方頂點，與dual star分開。

本版實際試作t=1。規格§5的t=2只用作預定比較對象：
\(K_{int}(t)=\rho_I(I-tD)\)，**整個D（包括由全部七格M產生的L統計）同乘t**；
t=2不是另一個候選，也不能事後用來替換t=1的失敗。

## 2. 固定目錄的完整結果：先列FAIL

表中「型別」指全部合法C均有E_C；「守恆」指全部C,C′的W完全相等；
「微因果」指原P全部不可比對、全部合法面；「S2」指規格IB.S2的全部strict對與面。
「空」表示該項在此輸入沒有判別力，並非實質PASS。所有L均量化；下述對稱代表不是挑L。

| 固定P | N,q,k,d_B | c,n_cov,n_ind | I內strict對 | 全面型別 | 守恆 | 微因果 | IB.S2／獨立Green |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 鏈C₃ | 3,3,1,2 | 3,0,0 | 有 | PASS | **FAIL** | 空（無不可比） | **FAIL**（2≺3） |
| 鏈C₄ | 4,6,1,2 | 4,0,0 | 有 | **FAIL**（面{4}奇異） | **FAIL**（{3}非unitary；{4}未定義） | 空／全域未完成 | **FAIL**於B₀面；全域undefined |
| 向下三葉star | 4,3,3,6 | 1,3,0 | 無 | PASS | 空（c=1） | PASS（葉對） | S2按構造；獨立內部檢查空 |
| diamond | 4,5,1,2 | 2,0,1 | 有 | PASS | **FAIL** | **FAIL**（b∥c） | **FAIL**（內部對） |
| 不交2份C₂ | 4,2,2,4 | 4,4,0 | 無 | PASS | **FAIL（每個L）** | PASS | **FAIL**於某合法面；內部檢查空 |
| 不交3份C₂ | 6,3,3,6 | 8,12,0 | 無 | PASS | **FAIL（每個L）** | PASS | **FAIL**於某合法面；內部檢查空 |

六例的c分布 \(\{1:1,2:1,3:1,4:2,8:1\}\)，n_cov分布
\(\{0:3,3:1,4:1,12:1\}\)，n_ind分布 \(\{0:5,1:1\}\)。這是六個固定同構類的
逐類計數，沒有對所有P或L抽樣。diamond的唯一Ind對b∥c是直接核對後FAIL；
沒有用共同面覆蓋推論代替它。star的c=1只令守恆比較空洞，不刪其他條件。

**同一目錄的其餘欄位。** 六例的canonical初值/source逆M、原P retarded G_R、
zero-boundary source response、IB.S3–4皆由§3的有限代數成立；後兩式是**按構造成立**。
各個E_C一旦存在，rank A_C=d_B與Gram正性亦按構造成立；C₄的{4}面不得稱已得到A。
每例有非零strict響應。active off-diagonal block的complex span在六例、全部L至少為2
（disjoint族的論證見§4）；這只是固定數學sector判準，非physical spin。
三葉star的守恆欄是空；鏈的不可比對檢查是空。任一FAIL、undefined或空欄都不能
由其它按構造欄抵消，也不能將目錄結果冒稱全D_KQ證明。

固定t=2比較的型別在六例也逐項列清：C₃、向下三葉star、diamond、2×C₂、3×C₂
的t=1／2均有全部合法面初值逆，且canonical面上至少一個strict CAR block在兩t間
不同且t=1非零；C₄的t=1已有合法{4}面奇異，**比較不合法／未完成**。
這五例的局部非恆定只驗§5的比較型別，不使任何守恆、microcausality或Green的FAIL消失，
也不能取代全部P、L上的比較義務。

## 3. 同一初值/source鏈與哪些式子自動成立

\(D_I=\iota_I\rho_ID\) 的每個非零block仍是原P的strict order。有限無環P使
\(D_I^N=0\)，\(M=I-D_I\)。所以固定規格的有限和滿足
\(G_R=(I-D_I)^{-1}=\sum_{j=0}^{N-1}D_I^j\)，且原P retarded；
\(G_A=G_R^\dagger=(M^\dagger)^{-1}\) 是advanced，不宣稱為同一M的另一逆。
因\(\rho_BD_I=0\)、\(K_{int}=\rho_IM\)，四項分塊關係精確為
\(\rho_BG_R\iota_B=I\)、\(K_{int}G_R\iota_B=0\)、
\(\rho_BG_R\iota_I=0\)、\(K_{int}G_R\iota_I=I\)。
\(R_I=G_R\iota_I\)是零B₀初值的source response；它未被初值傳播取代。
這些均為**按構造成立的代數恆等式**，不算Green與CAR的獨立橋接。

\(\ker K_{int}=G_R\iota_BD_{B_0}\)，故dim Sol=d_B、canonical
\(E_B=G_R\iota_B\)且\(\gamma_BE_B=I\)。其它C的初值同構恰好等價於F_C可逆，
成立時\(E_C=E_BF_C^{-1}\)，\(S_C=E_C^\dagger\)，
\(W_C=E_B(F_C^\dagger F_C)^{-1}E_B^\dagger\)。
由\(\rho_BE_B=I\)，\(W_C=W_B\)恰好等價於\(F_C^\dagger F_C=I\)。
所以可逆性、守恆（unitarity）與Gram正性是不同的檢驗。

從\(MG_R=G_RM=I\)直接展開得到
\(MC_GM^\dagger=M^\dagger+M-MM^\dagger\)（IB.S3）；
限制在I上得到\(\rho_IC_G\iota_I=\rho_IR_I+(\rho_IR_I)^\dagger-I_J\)（IB.S4）。
兩式均**按構造成立**，不能作為IB.S2已通過的獨立證據。
對y∈B₀且C=B₀，\(W_B(x,y)=E_B(x,y)=G_R(x,y)\)；
在strict對上G_A(x,y)=0且contact=0，故此部份IB.S2亦**按構造成立**。
這不保證別的面C有同一A，也不保證兩端都在I的比較。

## 4. 六例的紙上推導及全L量詞

**鏈C₃、C₄。** 以1≺2≺3（≺4）標記，B₀={1}；唯一L等於原順序。
\(D_{xy}=I+(x-y-1)\eta\)（x>y）。C₃的canonical初值傳播是
\(E_Bb=(b,b,(2I+\eta)b)\)。三個singleton面均可逆，因2I+η的eigenvalues是3、1。
面{3}的F₃=2I+η不是unitary，故W_{\{3\}}≠W_B；此為守恆FAIL。
canonical面上的內部對2≺3給\(W_B(3,2)=2I+\eta\)而\(G_R(3,2)=I\)，
差I+η≠0，IB.S2 FAIL。這是規格前曾預想風險的正式紙上例，未據此改規則。
對C₄，\(F_{\{3\}}=2I+\eta\)可逆但非unitary，{1}與{3}的守恆比較已**FAIL**。
\(E_B(4,1)=4(I+\eta)\)，其負η方向為零；合法{4}面F₄奇異，
所以該面的E、A、state仍undefined；不能以此掩蓋已定義兩面間的FAIL。
canonical面的2≺3亦令S2 FAIL。

**向下三葉star。** 三minimal葉\(a_1,a_2,a_3\prec b\)，B₀為全葉，I={b}，
唯一合法面C=B₀。按L中葉子的先後名次j=1,2,3，
\(D(b,a_j)=I+\sqrt2(j-1)\eta\)。L的六種選擇只是此有標記公式的置換，
不存在需挑選的有利L。葉對上的\(W_B(a_i,a_j)=0\)（i≠j），故原P微因果PASS；
S2只有y∈B₀的對，按構造成立。I僅一個事件，沒有獨立內部source比較；
c=1時守恆比較沒有判別力，不能稱此例完成完整量子橋接。

**Diamond。** a≺b≺d、a≺c≺d、b∥c，B₀={a}，I={b,c,d}，C={a}或{d}。
以L=(a,b,c,d)為例，較早的b到d其D-block為I，較晚的c到d因b在pre格
而為I+√2η；D(d,a)=I+2η。對(a,b)，c排在b之後且屬(≻,∥)post格，
所以\(D(b,a)=I+\sqrt3\eta\)，而\(D(c,a)=I\)。故
\(E_B(b,a)=I+\sqrt3\eta\)、\(E_B(c,a)=I\)，
\(F_{\{d\}}=E_B(d,a)=3I+(2+\sqrt2+\sqrt3)\eta\)。
其eigenvalues \(5+\sqrt2+\sqrt3\)、\(1-\sqrt2-\sqrt3\)均非零，
故兩面型別成立，但F†F≠I：守恆FAIL。
原P唯一Ind對b∥c的\(W_B(b,c)=I+\sqrt3\eta\ne0\)，故微因果直接FAIL。
對內部對b≺d及c≺d，\(W_B(d,b)=F_{\{d\}}(I+\sqrt3\eta)\)、
\(W_B(d,c)=F_{\{d\}}\)，而\(G_R(d,b)=I\)、\(G_R(d,c)=I+\sqrt2\eta\)，
兩對均不相等，IB.S2 FAIL。另一個L只需交換b、c的角色，結論相同。

**不交k份C₂（k=2、3）。** 第i份為\(u_i\prec v_i\)，B₀={u_i}，I={v_i}。
一個L固定後令p_i、s_i是其它分量落在u_i以前、v_i以後的事件數；
其餘在兩端之間。全部strict block只有
\(D(v_i,u_i)=H_i=I+a_i\eta\)，\(a_i=p_i\sqrt2+s_i\sqrt3\ge0\)。
此式同時量化全部合法L與兩個固定k，不選某一個L。a_i不可能等於1（含0的整數係數
與√2、√3）；所以每個H_i及所有合法面F_C（H_i與I的直和）均可逆。
對不同i、j，不可能彼此分量的所有事件既都在i的區間內、又都在j的區間內；
故至少一個a_i>0，每個L都有非unitary H_i。選取該分量的maximal作合法面就得守恆FAIL。
所有Sol及W_C按分量直和，跨分量不可比對block為零，微因果PASS。
在該非unitary分量選maximal面時，strict對的W_C(v_i,u_i)=H_i^{-1}，
而G_R(v_i,u_i)=H_i；二者不同，S2 FAIL。I中的不同v_i互不可比，
因此內部source-sensitive strict比較在整個Φ族都空洞。
此外，最早minimal與最晚minimal的p_i不同，故相應a_i不同；active blocks
H_i的span為2（η與I兩方向），但這不修復守恆或S2。

## 5. 跨尺寸族、比較對象與其它義務

| 固定族 | B／覆蓋、內部對 | IB-01的限定結果 |
| :--- | :--- | :--- |
| 全部鏈C_N，N≥3 | B₀={1}；c=N；無不可比對；N≥3有內部對 | 每個N的{1}與{3}已使守恆FAIL、canonical 2≺3使S2 FAIL；N≥4另含合法{4}奇異面，全面型別FAIL且該面undefined |
| 向下star，r≥2 | B₀為r片minimal葉；c=1；n_cov=binom(r,2)、n_ind=0；無內部對 | 只一面且葉對微因果PASS；守恆與獨立內部Green檢查空。L中葉序給D(b,a_j)=I+√2(j−1)η |
| dual star，r≥2 | B₀={a}，r片maximal葉；c=1；n_cov=0、n_ind=binom(r,2)；無內部對 | L中第j葉的D(v_j,a)=I+√3(r−j)η，均可逆；任兩不同葉上的W_B=D_iD_j†≠0，原P微因果FAIL。不可把它與向下star混同 |
| Φ族：不交k份C₂，k≥2 | B₀為k個minimal，c=2^k；n_cov=4binom(k,2)、n_ind=0；無內部對 | 全部合法L及面型別PASS、微因果PASS；每個L至少一個非unitary H_i，故守恆FAIL，某合法面S2 FAIL |

原規格t=2比較：C₃的全合法面對t=1、2皆可逆；t=2時
\(F_{\{3\}}=6I+2\eta\)，兩個t的canonical strict CAR block不同且非零。
Diamond的t=2末端trace為\(10I+(4+4\sqrt2+4\sqrt3)\eta\)（兩個eigenvalues非零）；
disjoint族各選maximal的trace block為\(2H_i\)，star仍只有canonical面。
故§2所列其餘四例也有局部合法且非恆定的比較；t=1已有其它義務FAIL或獨立
內部檢查空洞，C₄的t=1全面型別失敗，不能據此宣告全域比較義務完成。
本研究沒有調t或係數。t乘整個D，含所有L-count項，不把t=2當補救候選。

對鏈C_N，active block D(N,1)=I+(N−2)η在正η方向為N−1≠0，
原P directed Hasse距離為N−1；故固定K_int本身沒有跨N統一有限hop cutoff。
每個固定輸入有非零strict G_R block；固定目錄的active block span≥2已於§2、§4分別說明。
對所有初值同構成立的單一面，rank A_C=d_B>0及精確radical商的維數按構造成立；
Φ族令d_B=2k無界，但共同守恆form不成立。這些局部代數性質不能覆蓋§6的FAIL。

每個**已定義的**A_C都是正Gram，charged CAR及Q=A_C/2的gauge-invariant Wick
quasifree state在抽象代數上可按構造取得，並非physical vacuum／能量或Green來源。
由於C₃、diamond與Φ族的A_C不同，不能在那些輸入上以挑某一面、換field或換*宣稱
同一完整test上的單一共同CAR／state。C₄的奇異面更沒有E_C可供定義此試作的A_C。

## 6. 判定、作用域與停止

**本版IB-01對P0.2全域量詞FAIL。** C₃的所有面已可定義，但嚴格守恆與
兩端在I的IB.S2均失敗；diamond再給原P未覆蓋不可比對的直接微因果FAIL；
C₄給合法trace的型別FAIL。這些是本版固定係數、Green和式與初值配對的反例，
不是對全部因果序先行理論、P0.2所有可能K或量子過程先行假設的no-go。
已見Claude六點提醒的作用域逐一落實：canonical B₀的y∈B₀比較與IB.S3–4按構造；
內部比較空洞先列；W_C消除與線性延伸L的撞名；star方向及dual區分；t=2只比較。
§2的六例每個FAIL與undefined先於本結論保留，不在此版換law、面、Green、state或縮域。

本稿只作紙上代數，沒有新科學程式枚舉、數值／符號診斷、RNG、撒點、producer、
raw／sealed、seed、主機量測或新外部原文閱讀。已合併IB-01規格與所有母契約／B-01
逐字保留；原始輸入、P0.1、P0.2主問題仍OPEN。formal／E0、A／B、UNKNOWN與
§5.2.1(v)隔離不變。本研究須exact-head獨立逐式複核，不能因文件存在就升格已確認。
本地只作既有tests的回歸（Python3.12.14，NumPy2.3.5、SciPy1.17.0等CI pin）：
556 passed、5 warnings；CI指定Python3.12.13，故本次不冒稱與CI逐位元同一環境，
也不把既有數值測試當本稿的獨立數學證明。
