# 專案結論與研究狀態 (STATUS.md)

本文件為「零時光網／因果相位網」專案的常駐更新狀態頁。每次有新結論、新提案或否定結果時，應優先更新此處，避免每次都大幅修改主交接文件。

---

## 1. 標記與狀態定義

在專案文件與討論中，所有結論、猜想與模型均採用以下四種標記分類：

| 標記 | 英文對應 | 意思 | 後續處理方式 |
| :--- | :--- | :--- | :--- |
| **【已知】** | **Known** | 現有物理或數學已有可靠學術文獻與理論依據。 | 可以當作限制條件與基底，但引用時仍須精確。 |
| **【已確認】** | **Confirmed** | 本專案中的特定推導與數值模擬已經過核對無誤。 | 可以繼續沿用；若未來有改動必須說明理由。 |
| **【提案】** | **Proposed** | 目前看來合理、但尚未被證明的全新構想或假說。 | 必須通過計算或數值模擬驗證，不能用文字當證明。 |
| **【已否定】** | **Rejected** | 已找到明確的物理／數學矛盾，或被證明必然失效的方案。 | **不得再作為後續理論設計的支柱**。 |

---

## 2. 結論與核心主張狀態清單

本清單條列了本專案目前累積的所有具體論斷及其狀態：

| 主張 / 結論內容 | 分類狀態 | 詳細說明與物理根據 | 關聯章節 / 程式檔案 |
| :--- | :--- | :--- | :--- |
| **光狀虛歷史量子總和可表現有質量傳播** | **【已知】** | 在 1+1 維 Feynman Checkerboard 模型中，以光速前進的鋸齒路徑經疊加後可重現 Dirac 傳播子。 | `handoff_v1.0.md#4.1` |
| **因果集 Order + Number = Geometry** | **【已知】** | 離散因果偏序關係加上事件數量可以對應時空幾何，且其隨機離散化與勞侖茲對稱相容。 | `handoff_v1.0.md#4.5` |
| **光折返一次就累積一點固有時間** | **【已否定】** | 錯誤。每一段光速路徑固有時間為零。轉彎不會增加固有時間。非零時間是端點有效類時間隔。 | `handoff_v1.0.md#4.2` |
| **質量是客觀的折返頻率或次數** | **【已否定】** | 錯誤。質量是 Dirac 方程中手徵通道混合的複數振幅演化參數，不能解釋為真實折返事件。 | `handoff_v1.0.md#4.3` |
| **Checkerboard 鋸齒是電子真實軌跡** | **【已否定】** | 錯誤。這些鋸齒路徑是路徑積分中的虛歷史疊加，不代表粒子真實運動軌跡。 | `handoff_v1.0.md#4.1` |
| **單向延遲傳播核行列式可作幾何選擇** | **【已否定】** | 錯誤。單向延遲矩陣 $D_C$ 在因果偏序排序下必然為嚴格下三角矩陣，其行列式為定值，看不到網絡結構。 | `handoff_v1.0.md#8` |
| **物質選幾何核心假說** | **【提案，範圍已限縮】** | 非時空因果網因無法承載穩定的費米子傳播而量子相消；類流形網絡則獲得相對增強。**注意**：此假說原本設想的機制（費米子行列式的相消相位壓低 KR）已因下一列「Q_test 特徵值對稱與行列式相位固定」而受限——任何 BdG 型算子 $\begin{pmatrix} mI & R\\ R^\dagger & -mI \end{pmatrix}$ 在代數結構上都不可能提供可相消的複數相位，這與 $R$ 內部裝的具體因果結構無關（已用任意隨機 $R$ 驗證）。因此本假說若要以「相位相消」的原始形式成立，需要換一種不是這個對稱形狀的候選算子；目前 Gate C 已改為聚焦「費米子如何與因果集重力作用量互動」，不再單靠費米子相位獨立相消。 | `handoff_v1.0.md#7.3`, `tests/test_gate_a_testbed.py` |
| **雙區塊 Q_test 診斷算子** | **【提案】** | 將傳播核與伴隨矩陣結合為 $Q_{\text{test}} = \begin{pmatrix} mI & R_C \\ R_C^\dagger & -mI \end{pmatrix}$ 可以解除三角退化，提供非平凡特徵譜。 | `handoff_v1.0.md#9.2` |
| **Q_test 特徵值對稱與行列式相位固定** | **【已確認】** | $Q_{\text{test}}$ 的特徵值成對出現（$\pm\sqrt{m^2 + \sigma_k^2}$），因此行列式實虛相位和正負號固定。各網絡間無可互相抵消的量子相位，無法單獨作為幾何選擇的相消機制。 | `tests/test_gate_a_testbed.py` |
| **附加相位場的標籤不變性** | **【已確認】** | 當隨機相位 $U_{ij}$ 從數字 ID 分離並定義為隨時空置換的附加物理場資料時，重新標記事件編號後 $Q_{\text{test}}$ 的特徵值與行列式嚴格不變。 | `tests/test_gate_a_testbed.py` |
| **Q_test 的結構敏感性（而非幾何選擇）** | **【已確認】** | $Q_{\text{test}}$ 的特徵譜與 $\log|\det|$ 在不同因果網絡間（如鏈、反鏈、KR、Poisson 灑點）具備結構敏感性，可作為幾何結構的診斷工具，但不能證明物質能選出幾何。 | `tests/test_gate_a_testbed.py` |
| **區間大小 $|I(j,i)|$ 足以描述自旋傳輸** | **【已否定】** | 錯誤。區間大小僅為純量，自旋傳輸必須具備 Clifford 代數結構或框架傳輸規則。 | `handoff_v1.0.md#9.4` |
| **Ignatowski 類無光相對論限制** | **【已知】** | 可以在不假設光速不變下限制慣性系變換；不同公理化版本假設不同，不宣稱存在唯一「公認五條最小公理」。 | `docs/foundations/kinematic_selection.md` |
| **因果共形重建 (Malament/HKM)** | **【已知】** | 在適當條件下決定 continuum metric 的 conformal structure；Malament/HKM 是在既有 Lorentzian spacetime 類別中的重建定理，不能誤寫成「任意偏序會產生 Lorentzian spacetime」。 | `docs/foundations/kinematic_selection.md` |
| **非平凡因果偏序排除歐氏特徵 (G0-B)** | **【提案】** | 非平凡、有一致過去/未來方向的 causal partial order 是否可以排除 Euclidean signature。 | `docs/foundations/kinematic_selection.md` |
| **多公理融合排除伽利略極限 (G0-C)** | **【提案／條件式論證】** | causal order + local finiteness + number-volume correspondence + 適當均勻性/非緊緻條件，是否可以排除 Galilean K=0，從而要求有限 invariant causal speed。此提案尚未獲得證明，且 local finiteness 單獨不得寫成可推出有限 c。 | `docs/foundations/kinematic_selection.md` |
| **前時空不變量／投影假說** | **【提案】** | 探索事件、因果關係與量子振幅是否本身可由更底層的不變結構產生。目前沒有候選數學定義，僅作為基礎研究支線。 | `docs/foundations/invariant_projection_hypothesis.md` |
| **Smeared causal-set d'Alembertian benchmark** | **【已確認／Benchmark】** | $B_{\epsilon}^{(2)}$ 通過 1+1D 連續極限基準驗證，符合對應 mesoscale $\xi$ 下的波動算子極限，且波動係數隨 density 上升符合 $N^{-0.6}$ 左右之收斂速度；$B_{\epsilon}^{(3)}$ 通過獨立 2+1D 基準驗證，利用已發表 3D 係數在 past cone 上順利回復 $\Box$。 | `benchmarks/b_eps_2d.py`, `benchmarks/b_eps_3d.py` |
| **Momentum-space 2D continuum operator** | **【已確認】** | 已數值驗證 2D continuum averaged nonlocal d'Alembertian 的動量空間特徵：IR 極限下回復 continuum $\Box$，UV 極限下飽和為常數（$g \cdot \xi^2 \to -2$）。**追加確認**：此 UV 常數即 BBMM Eq.(4) 的 $a^{(2)}\rho$（$a^{(2)}=-2$），本專案獨立導出的 $g$ 與 BBMM Eq.(15)（取 $\gamma_2=1/2$）逐位吻合，subleading 係數 $b^{(2)}=8$。 | `analysis/gmom_2d.py`, `analysis/gmom_2d_bbmm.py` |
| **2015 spectral calculation 的 regularization / Wick rotation / P(s) 定義** | **【已確認／literature-faithful】** | 三者皆直接取自 BBMM (arXiv:1507.00330, PRD 93 044017)，未自行發明：(a) **regularization** = BBMM Eq.(5) $g_{\text{reg}} = a\rho^{2/d} g/(a\rho^{2/d}-g)$，源自 Aslanbeigi–Saravani–Sorkin (arXiv:1403.1622)，動機是 $g\to$ const 造成 Green function 在 coincidence limit 的 delta 發散，而離散理論本無 coincidence limit；(b) **Wick rotation** = BBMM Sec.II B：原算子為 retarded，$\Gamma_R$ 不可轉（會穿過奇點），須先解析延拓 $g$ 至全複平面改用 Feynman contour $\Gamma_F$。完整鏈條為 retarded $g$ → 解析延拓至全複平面 → Feynman prescription（$\Gamma_F$ 取代 $\Gamma_R$）→ Wick rotation $k^0\to-ik^0$ → Euclidean section $k^2>0$。**只有走完整條鏈之後**所有動量才皆為 spacelike，程式因而得以只在實數 $k^2>0$ 上求值（Bessel-$K$ 表示式單值實值的一側）。**警告**：看到 $k^2>0$ 本身不等於 Wick rotation 已完成；analytic continuation 與 contour prescription 是不可省略的載重步驟，嚴禁把 Lorentzian retarded $g$ 直接當成 Euclidean function 使用；(c) **$P(s)$** = BBMM Eq.(10) $P(s)=\int \frac{d^dk}{(2\pi)^d} e^{s g_{\text{reg}}}$，$d_s=-2\,\partial\ln P/\partial\ln s$（Eq.(8)）。 | `analysis/spectral_dim_2d.py`, `tests/test_spectral_dim_2d.py` |
| **2D spectral dimension 數值重現** | **【已確認】** | 通過五項 BBMM 自述之解析檢查：(C1) IR $g\to-k^2$；(C2) UV $g\to a\rho=-2$；(C3) $g_{\text{reg}}$ UV 斜率 $=-a^2/b=-0.5$；(C4) **未正則化時 $d_s = 4\rho s$ 嚴格成立**（BBMM Eq.(14)，數值比值 1.000000，為 $P(s)$ 定義與 Euclidean section 最銳利的驗證）；(C5) 正則化後 $d_s$ **曲線形狀**與 BBMM Fig.2 上圖一致：兩端皆 $\to 2$，中間出現 overshoot，由上方趨近 Hausdorff 維度。數值觀察到極大值 $\approx 2.26$ 位於 $s\approx 1.8$（$\rho=1$），但 **Fig.2 為圖形數值、其 caption 僅稱極大值位於 nonlocality scale 附近，故極大值的位置與高度只作數值觀察記錄，不作為文獻精確驗收條件**。注意 $d=2$ 因 UV 與 IR 同為二次而兩端同值，**不足以檢驗「普適降維至 2」**，該主張須待 $d=3,4$。 | `analysis/spectral_dim_2d.py`, `tests/test_spectral_dim_2d.py` |
| **2D operator 之精確閉式驗證** | **【已確認】** | ASS (arXiv:1403.1622) Eq.(2.5) 給出 $d=2$ 精確閉式 $\rho^{-1}g^{(2)}=-Ze^{Z/2}E_2(Z/2)$。本專案的 Eq.(15)（$\gamma_2=1/2$）求值與之在 $k^2\in[10^{-6},10^{3}]$ 吻合至機器精度（rel diff $\lesssim10^{-15}$）；其 $Z\to\infty$ 展開 $-2+8/Z$（ASS Eq.(2.8)）獨立確定 $a^{(2)}=-2$、$b^{(2)}=8$ 為精確值。此閉式解取代先前的數值交叉檢查，成為 2D 動量空間構造的最強驗收條件。 | `tests/test_spectral_dim_2d.py::test_closed_form_2d` |
| **4D spectral dimension（Track A / replication）** | **【已確認／replication】** | 以 ASS Eq.(2.12) 之 $a^{(4)}=-4/\sqrt6$、$b^{(4)}_{0..3}$ 與 $C_4=\pi/24$ 實作，通過 ASS Eq.(3.13) IR、Eq.(3.16) UV（$b_{UV}=2^{D-1}\pi^{D/2-1}\Gamma(D/2)b_0=32\pi/\sqrt6\approx41.0416$）、BBMM Eq.(6) 正則化 UV 斜率 $-a^2/b_{UV}\approx-0.064975$ 三項檢查。$d_s$ 由 UV 端 $2.003$ 流至 IR 端 $4.003$，中間於 $s\approx10$ 出現 overshoot 至 $4.17$（BBMM 稱 $d=3,4$ 極大值位於 $s\sim10\rho^{1/d}$，由上方趨近 Hausdorff）。**此為 replication benchmark，不得作為理論支柱**（見下兩列）。 | `analysis/spectral_dim_D.py` |
| **UV 降維與 non-positive spectral density 的關聯** | **【已知警告／未決物理解讀】** | BBMM 結論節指出：對 $d>2$，有證據顯示此類 causal-set-derived operator 的 Källén–Lehmann 譜函數 $\rho(\mu^2)=\mathrm{Im}(g)/|g|^2$ **非正定**，意味量子理論存在負模 (negative-norm states)；依 Weinberg 論證，propagator 在 UV 衰減快於 $1/k^2$ 與 spectral positivity 不相容。BBMM 並就此討論 spectral positivity 與 UV propagator 行為的關聯，提及 positivity-compatible generalized operators。**因此 $d_s\to2$ 不可視為天然正面的物理結論。** **來源歸屬警告**：arXiv:1502.01655 **本身並未計算 spectral dimension**；「positivity-preserving theory 之 $d_s^{UV}$ 維持 4」不得歸因為該論文的結論。對 Track B concrete operator，本專案已**解析預測**：$g$ 在 UV 為 $a+b/Z$（$a=-2,b=8$），若採與 Track A 同一 BBMM regularization（其動機——UV 常數飽和造成 coincidence-limit delta 發散——對 Track B 同樣成立，此為本專案推論），則 $g_{reg}\sim-Z/2\sim k^2$，兩端皆為二次，預期 $d_s^{UV}\to4$。**此預測待 Stage 4 數值驗證，程式算出什麼就記什麼。** 但 BBMM 自己的措辭是 natural question / possible linkage，**尚未證明二者必然因果等價**，本專案不得寫成「已證明降維源於負模」。 | BBMM Sec.IV–V |
| **Track B 工作框架（arXiv:1502.01655 concrete 4D operator）** | **【提案／進行中】** | 分階段：Stage 1 source-faithful operator → Stage 2 analytic structure + stability → Stage 3 spectral weight / positivity → Stage 4 才碰 $P(s)$ 與 $d_s$。來源表每項須同時記錄 equation number、dimension、$\Lambda$／$\rho$ 冪次約定、無因次變數定義、coefficient convention，再建立與 Track A notation 的 mapping；**不得預設 $a$ 值**。**驗收條件框架**：$d_s^{UV}\to4$ 僅為文獻啟發之預期，**不得作為驗收條件**；驗收條件是「operator 實作忠於原文、stability 與 positivity 重現原文」，$d_s$ 算出多少記多少。 | `analysis/track_b_4d.py` |
| **Track B Stage 1–2 完成** | **【已確認】** | Operator 定義取 Eq.(13)/(A7) + Eq.(11)/(A36)。$\delta_+$ 依原文 $\delta_+(u)=\lim_{\epsilon\to0^+}\delta(u-\epsilon)$ 與 $u=s^2$ 精確拆出，貢獻 $8/Z$（**不可用窄 Gaussian 近似**，其係數直接參與 IR 相消）。通過 A9（$k=0,1,2$）、A10、A11 moment 條件與 A8 IR 極限。**Stability**：以 argument principle 在割平面內部數零點得 $N=0$（$R=20\ldots300$），割線邊界另由 $\mathrm{Im}\,g\ne0$ 排除——此二分正是 A37 的實作而非窄化。附 planted-zero 對照測試確保計數器非恆回 0。 | `analysis/track_b_4d.py`, `analysis/track_b_4d_analytic.py`, `tests/test_track_b_4d.py`, `tests/test_track_b_4d_stage2.py` |
| **跨文獻解析識別：Track B 4D 與 ASS minimal 2D 共用同一 $g(Z)$** | **【已確認／本專案導出，非原文陳述】** | 1502.01655 的 4D concrete operator 與 ASS (arXiv:1403.1622) minimal **2D** operator 產生同一個無因次動量空間函數 $g(Z)=-Ze^{Z/2}E_2(Z/2)$。解析證明：$E_2(w)=e^{-w}-wE_1(w)$ 給 $g=-Z+\frac{Z^2}{2}e^{Z/2}E_1(Z/2)$，其割線不連續性給 $\mathrm{Im}\,g(-x-i0)=\frac\pi2x^2e^{-x/2}$，恰為 Eq.(A33) 主動指定並據以反建 kernel 的 $g_I$（數值吻合至 $10^{-26}$）。**分類註記**：1502.01655 全文不含 $E_2$，亦未明文說明其所選 $g$ 即 ASS 2D 那條；此識別為本專案獨立導出，**不得寫成原文陳述**。**措辭紀律**：「同一個 $g(Z)$」不等於「同一個理論」——維度 $D$ 仍經動量測度 $d^Dk/(2\pi)^D$ 獨立進入 Green function、spectral density 與 $d_s$。 | `analysis/track_b_4d_analytic.py` |
| **Track B physical branch prescription** | **【已確認／原文】** | 由 Eq.(12) $B(p)=\Lambda^2\lim_{\epsilon\to0^+}g((p+ip_\epsilon)^2/\Lambda^2)$ 直接定出：$p_\epsilon$ 為 infinitesimal future-directed timelike，原文用 $(-+++)$，故 future-directed timelike $p$ 有 $p\cdot p_\epsilon<0\Rightarrow\mathrm{Im}Z<0$，而 $p^2<0\Rightarrow\mathrm{Re}Z<0$。物理邊界為**下側** $Z=-x-i0$。與 Appendix A.3（割線下方 $\mathrm{Im}\,g>0$、上方為負）一致，數值亦重現。**注意**：此 prescription 取自 1502.01655 自身，不得從 ASS 進口——兩篇共用函數 $g$，但 contour prescription 各自陳述。 | `analysis/track_b_4d_analytic.py` |
| **深 IR catastrophic cancellation（已修）** | **【已確認／已封住】** | $g=a+8/Z+\int$ 形式在 $Z\to0$ 須讓兩個 $O(1/Z)$ 巨量相消到只剩 $O(Z)$，double precision 下必然失效：實測 $Z=10^{-6}$ 相對誤差 $6.8\times10^{-4}$，$Z\lesssim10^{-7}$ **回傳錯號正數且不拋錯**。修法用原文自身的 A9/A11 把相消移至解析層：$K_1$ 小宗量展開後，$1/x$ 項由 A9($k{=}0$) 與 $\delta_+$ 的 $8/Z$ 精確相消、$\ln\sqrt Z$ 與常數項由 A9($k{=}1$) 消去、$\ln s$ 項由 A11 與 $a=-2$ 相消，餘 $g(Z)=4\pi Z^{-1/2}\int ds\,s^2f_{\rm smooth}(s^2)R(\sqrt Zs)$。三層求值器有效範圍：直接積分 $Z\ge10^{-4}$（已加 `Z_MIN_DIRECT` 硬性拒絕，不再靜默出錯）、IR-safe 主項至 $10^{-10}$／修正項至 $10^{-8}$、閉式全域（已修 $Z\gtrsim1418$ 的 $e^{Z/2}$ 溢位）。**IR 修正律** $g/(-Z)-1=-\frac Z2(\ln\frac2Z-\gamma)$ 為真實解析修正（$Z=10^{-6}$ 時達 $7\times10^{-6}$），非求積誤差；要求精度優於此的測試會讓正確實作失敗。 | `analysis/track_b_4d_irsafe.py` |
| **Track B Stage 3：quantum spectral structure** | **【已確認／原文條件已重現】** | 來源：Eq.(55) $\tilde W=2\,\mathrm{Im}B\,\theta(p^0)/|B|^2$、Eq.(56) $\mathrm{sgn}\,\mathrm{Im}B=\mathrm{sgn}\,p^0$（**此為作者為使 two-point function 正定而另加的 quantum condition，非 Sec.II 六項 operator axioms 之一**）、Eq.(85) $\rho=\tilde W/2\pi$、Eq.(86) $\rho(\mu^2)=\delta(\mu^2)+\tilde\rho(\mu^2)$。**本專案由 Eq.(12)+(55)+(85) 組合導出**（原文未印出）：$\tilde\rho=\frac{1}{\pi\Lambda^2}\frac{g_I}{g_R^2+g_I^2}$，其中 $g_R(x)=x-\frac{x^2}{2}e^{-x/2}\mathrm{Ei}(x/2)$、$g_I(x)=\frac\pi2x^2e^{-x/2}>0$，$x=\mu^2/\Lambda^2$。故 positivity 解析可見：$\mu^2>0\Rightarrow g_I>0\Rightarrow\tilde\rho>0$。已通過 12 項驗收（Eq.(55) 定義、future/past bank 符號、$\tilde W\ge0$、$\tilde\rho>0$、$\rho=\tilde W/2\pi$、端點有限性、$\Lambda$ 冪次）。**massless $\delta(\mu^2)$ 未以函數表示**——不得用窄峰假造。 | `analysis/track_b_4d_spectral.py`, `tests/test_track_b_4d_spectral.py` |
| **連續譜總權重 $=b/a^2-1=1$** | **【本專案解析導出（用到 Stage-2 stability + IR residue + UV asymptotics）／非原文 sum rule／非文獻驗收條件】** | 數值：$\int_0^\infty d\mu^2\,\tilde\rho=1$（50 位精度，兩組獨立細分）。**解析來源**：令 $h(Z)=-1/g-1/Z-1/2$。**前提（易漏且承重）**：$h$ 在割平面外無極點，**依賴 Stage 2 的 stability 結果**——$g(Z)\ne0$ 對所有 $Z\ne0$ 成立；$g$ 若有任何額外零點即為 $1/g$ 的極點，論證立刻瓦解（$1/Z$ 減項處理的正是原點那個唯一存在的零點）。在此前提下：$g\simeq-Z$ 使 $-1/g$ 在原點留數為 1，大 $Z$ 端 $g=a+b/Z$ 給 $-1/g=-1/a+b/(a^2Z)$，$h$ 無窮遠趨零，Cauchy 得 $\int d\mu^2\tilde\rho=b/a^2-1$。**故此 sum rule 實為複合陳述**：IR 歸一化（$g\to-Z$）＋ UV 係數（$b/a^2$）＋ Stage 2 stability $\Rightarrow$ 連續譜權重 $=1$。**價值**：同時約束 IR、UV 與 stability，故為 Eq.(12)$\to$(55)$\to$(85) 歸一化鏈的強檢驗——鏈上任何多餘的 2 或 $\pi$ 都不會留下整數。**紀律警告**：1502.01655 **未**陳述任何 Källén–Lehmann sum rule，此結果**不得**作為忠於原文的驗收條件，僅作本專案自身算術的 regression lock。**推論**：完整 $\rho=\delta+\tilde\rho$ 積分為 **2 而非 1**，不得「修正」。 | `analysis/track_b_4d_spectral.py` |
| **positivity 對 stability 是承重而非裝飾** | **【本專案導出】** | $\mathrm{Re}\,g(-x-i0)$ 在 $x\to0^+$ 為 $+x>0$、$x\to\infty$ 趨 $-2$，故必在中間穿零：數值定於 $x_0=2.6943105$，即 $\mu=1.6414\Lambda$。**在該質量處 $\mathrm{Re}\,g=0$，$\mathrm{Im}\,g>0$ 是唯一阻止 $g$ 成為零的成分。** 故 A38–A42 的 positivity$\Rightarrow$stability 對此 operator 並非抽象蘊涵，而是在一個具體質量上實際承重。**主張範圍**：此陳述為條件式——若**保持 $g_R$ 結構不變**而將 $g_I$ 壓至零，首先會在 $x_0\simeq2.6943$ 產生 on-cut zero；它**不**主張任何對 $g_I$ 的修改都會在此處造成不穩定性，因為同時改動 $g_R$ 可使穿零點移位甚至消失。另註（**數值觀察／已鎖定 regression，非解析證明**）：在掃描範圍 $x\in[10^{-4},10^2]$ 內 $\tilde\rho$ 自端點 $1/(2\Lambda^2)$ 單調下降、未見共振峰（該處 $g_I=2.96$ 阻尼甚強）。**尚未證明** $d\tilde\rho/dx<0$ 對全部 $0<x<\infty$ 成立，不得改寫為全域單調性結果。 | `tests/test_track_b_4d_spectral.py` |
| **Sorkin–Johnston 交叉檢查（Eq.72–73）** | **【未實作／刻意保留】** | 原文以 SJ construction 獨立得到同一 $2\mathrm{Im}B/|B|^2$ 權重，作為兩種量子化途徑的一致性檢查。本專案**未**實作，因需另從原文抽出 SJ 公式；**嚴禁**由 Eq.(55) 端反推近似，那是循環論證。 | — |
| **Stage 4 通則：$d_s=D/\alpha$** | **【已確認／本專案解析導出】** | 若 Euclidean regularized eigenvalue 在某尺度區間滿足 $g_{\rm reg}(Z)\sim-cZ^\alpha$（$c>0,\alpha>0$），代換 $t=csZ^\alpha$ 於 $P(s)=\int dZ\,Z^{D/2-1}e^{sg_{\rm reg}}$ 得 $P\propto s^{-D/(2\alpha)}$，故 $d_s=D/\alpha$。**UV 為推論**：$u=a-g\sim-b/Z^\beta\Rightarrow g_{\rm reg}=ag/u\to-(a^2/b)Z^\beta$，即 $\alpha=\beta$。**IR 由同一式涵蓋**：兩 operator 共有 IR 條件 $g\to-Z$ 給 $g_{\rm reg}\to-Z$，即 $\alpha=1$，故 $d_s^{IR}=D$。（註：不可把 IR 寫成「$u\to a$ 常數即 $\beta=1$」——$u$ 在 IR 並非 $-b/Z^\beta$ 形式，該律必須寫在 $g_{\rm reg}$ 上才兩端統一。）以植入 $\alpha$ 的合成 operator 驗證（$\alpha=1,2,4$；$D=2,4$），驗的是管線本身而非任一物理 operator。 | `tests/test_stage4_comparison.py` |
| **BBMM「universal $d_s^{UV}\to2$」的代數來源** | **【已確認／本專案解析導出】** | ASS Eq.(3.16) 給 minimal GCB 族在**任意** $D$ 皆 $u\sim-b/Z^{D/2}$，即 $\beta=D/2$，代入通則得 $d_s^{UV}=D/(D/2)=2$ **恆成立**。故 BBMM 所述之 dimension-independent UV limiting value 2，在其 spectral-dimension prescription 內可代數追溯至該 $D/2$ 指數。**主張範圍**：此結果解釋 limiting value 2 的直接數學來源，**不判定該 exponent 本身是否具有更深物理起源**——「為何這族 causal-set operator 恰好給出 $D/2$」仍可能反映其構造或物理。**不得**改寫為「universal reduction 只是算術」。 | `tests/test_stage4_comparison.py` |
| **Stage 4 公平比較：Track A vs Track B** | **【已確認／本專案公平數值比較】** | 控制變因：兩 track 共用 `build_operator` 與 `d_s()`，相同 $z_{lo}=10^{-6}$、$z_{hi}=10^{6}$、$n_{pts}=801$、log-$Z$ 網格、cubic spline、內插法、BBMM Eq.(5)、$D=4$ 動量測度、$s$ 網格與求積設定；**唯一 operator-specific 輸入為 $a,u_{\rm raw},u_{IR},u_{UV}$**。結果：Track A（minimal GCB，$u\sim Z^{-2}$）得 $d_s^{UV}\to2$；Track B（1502.01655 concrete operator，$u\sim Z^{-1}$）得 $d_s^{UV}\to4$；兩者 $d_s^{IR}\to4$。**故最終對比是 Track A $4\to2$ vs Track B $4\to4$（帶中尺度 overshoot），而非「有無 overshoot」之別——兩者皆 overshoot，差別在 UV endpoint。** 差異可解析追溯至 UV subleading power，非 spline、網格或求積參數：Track B spline↔direct 之 $u$ 最大 rel err $2.372\times10^{-10}$、$d_s$ 最大絕對差 $1.862\times10^{-9}$；$n_{pts}=401/801/1601$ 僅動 $\sim10^{-8}$。 | `analysis/track_b_spectral_dim.py`, `analysis/spectral_dim_D.py`, `tests/test_stage4_comparison.py` |
| **「共用 asymptotic」不是公平控制變因** | **【已確認／executable counterexample】** | 把 Track A 的指數**連續銜接**到 Track B（取 $b=8z_{hi}$ 使 $-b/Z^2$ 在 $z_{hi}$ 接上 $-8/Z$），$d_s^{UV}$ 落在 **2.000000**——與 Track A 相同。spline 邊界以下 Track B 的 operator 一個位元未變，只換掉尾部，而 $s\to0$ 看到的正是尾部。**強制統一漸近行為等同更換 operator，非收緊控制變因。** 另記錄較粗糙版本（直接貼 Track A 的 $b_{UV}$、不做連續銜接）：留下五個數量級不連續，回傳 **0.0067**，既非 2 亦非 4——失效模式不總是「看似合理的錯答案」。 | `tests/test_stage4_comparison.py::test_forcing_track_A_asymptotics_onto_track_B_fakes_the_result` |
| **BBMM regularization 保留 Stage 3 spectral-weight factor** | **【已確認／本專案代數導出】** | $g_{\rm reg}=ag/(a-g)$ 且 $a$ 為實數 $\Rightarrow 1/g_{\rm reg}=1/g-1/a\Rightarrow\mathrm{Im}(1/g_{\rm reg})=\mathrm{Im}(1/g)$，故 $$\frac{\mathrm{Im}\,g_{\rm reg}}{|g_{\rm reg}|^2}=\frac{\mathrm{Im}\,g}{|g|^2}$$ **在兩側皆有定義之處**逐點成立（即避開分母之零點與極點 $g=0$、$g=a$；物理割線上兩者皆不發生——$g=0$ 由 Stage 2 stability 與 $\mathrm{Im}\,g>0$ 排除，$g=a$ 僅漸近達到）。50 位精度下差 $<10^{-40}$。此組合正是 Stage 3 的 $\tilde W=\frac{2}{\Lambda^2}\frac{\mathrm{Im}\,g}{|g|^2}$（Eq.55+Eq.12）與 Eq.(85) 譜密度所用因子。**此結果不證成「BBMM Eq.(5) 適用於 Track B」**（見下列），它排除的是該推論可能自我拆台的一種方式：Stage 4 所需之 regularization 未將 Stage 3 已確立的 positive spectral weight 改掉——保留的不只是符號，是數值本身。 | `tests/test_stage4_comparison.py` |
| **Stage 4 結論的上限：regularization 之適用性** | **【本專案推論／公平性上限】** | 對 Track B 套用 BBMM Eq.(5) 是**本專案推論**，依據為兩 operator 之 $g$ 在 UV 皆飽和至常數 $a=-2$，故 Green function 有相同的 coincidence-limit delta 發散，BBMM 的正則化動機原封不動適用。**arXiv:1502.01655 既未 regularize、亦未計算 spectral dimension。** 整個 Stage 4 比較的公平性以此推論為上限，已寫入 adapter 與測試 docstring。 | `analysis/track_b_spectral_dim.py` |
| **Track B 中尺度 overshoot** | **【數值觀察／非驗收條件】** | 連續搜尋得峰值 $d_s^{\max}=4.53655$ 於 $s_{\rm peak}=2.42149$（log 網格會讀成 4.531@$s{=}3.16$ 並錯過真峰）。**無文獻值可對**，且依賴上列 regularization 推論。峰值高度與位置**不得**引為與任何文獻之一致性。另註：Track A 峰在 $s\sim10$、Track B 在 $s\sim2.4$，測試已鎖定 Track B 峰位嚴格小於 Track A，以防日後有人因「兩者皆 overshoot」誤判行為類似。 | `tests/test_stage4_comparison.py` |
| **不得寫成已證明：positivity $\Rightarrow$ 不降維** | **【紀律／未決】** | 本專案證明的是：在這兩個 concrete operators 上，UV subleading power 不同（$Z^{-D/2}$ vs $Z^{-1}$），且此差異**伴隨**不同的 spectral-positivity 性質。**因果必然性尚未證明。** 不得由 Stage 4 結果推出「spectral positivity 已被證明造成 $d_s$ 不降維」。 | — |
| **minimal 4D operator 的不穩定性** | **【已知】** | ASS §2.2 與 §3.5：以 argument principle 數值計數，minimal 4D $\Box^{(4)}_\rho$ 的 $\tilde g(Z)$ 在複平面上存在**兩個非零的 unstable zeros**（虛部類時且指向未來），即存在指數增長模；2D 對應物則被解析證明穩定（$\tilde g$ 僅在 $Z=0$ 有零點）。ASS 亦稱未能找到任何穩定的 4D GCB 參數選擇。此為獨立於負模問題的**第二個病態**，且 BBMM 的 4D $d_s$ 正是建立在這個不穩定算子上。 | ASS §2.2, §3.5 |
| **Pure-order 診斷 (Myrheim-Meyer Profile)** | **【未證明增量價值／輔助診斷】** | 單一維度估算量不足以證明 manifold-likeness。KR 類結構的 global MM 維度可給出約 2.37 的漂亮數值，但結構非 manifold-like。scale-resolved/local MM profile 雖可做跨尺度穩定性診斷，但尚未證明其相較於 interval abundance 具有額外辨識價值。 | `benchmarks/order_bench.py`, `benchmarks/run_order_bench.py` |
| **Q_test squared diffusion recipe** | **【已否定作為 physical diffusion generator】** | 目前無物理推導支持 $L_Q = Q_{\text{test}}^2 - m^2 I$ 可直接解釋為 causal-set geometry 的 diffusion generator。此外該構造會使數值條件數平方，嚴重破壞低端譜的浮點解析。但 $Q_{\text{test}}$ 本身仍保留為 Gate A 結構診斷工具。 | `tests/test_gate_a_testbed.py` |
| **Hasse/link graph diffusion** | **【已否定作為目前的 continuum dimension probe】** | 全因果集 Hasse/link 圖上的擴散過程無法在閔考斯基撒點上可靠重現連續維度，此與 Lorentzian 因果集的固有非定域性相容，表明該 probe 本身不適用，而非撒點或因果集主線失敗。 | `benchmarks/order_bench.py`, `benchmarks/run_order_bench.py` |
| **Stage 5A：sector-pair quotient observable $\kappa(P)$** | **【已確認／本專案解析導出＋CI 窮舉驗證】** | 對 1+1D order-dimension-2 poset，定義 $\kappa(P)=|\mathcal R_2(P)/(\mathrm{Aut}(P)\times S_2)|$，其中 $\mathcal R_2(P)$ 為二元 realizer 集，$S_2$ 為全域 $U\leftrightarrow V$ 交換。將 realizer $(L_1,L_2)$ 編碼為 permutation diagram $\pi$：元素重新標號不改變 $\pi$；反之相同 $\pi$ 的 realizers 由等 $L_1$-rank 配對所誘導之 poset automorphism 相連；交換兩個 sectors 對應 $\pi\mapsto\pi^{-1}$。故 $\kappa$ 可由 $\pi$ 的 orbit 直接計算，無須顯式求 $\mathrm{Aut}(P)$。實作以 forcing/implication classes 列舉 transitive orientations，並以獨立 brute-force transitive-orientation + 全 automorphism + $\mathrm{Aut}\times S_2$ orbit 計數之小樣本 regression 交叉驗證；固定 $\kappa=1,2,3$ 例子皆鎖入測試。 | `analysis/stage5a_kappa.py`, `tests/test_stage5a_realizer.py` |
| **Stage 5A：1+1D global null-order sector pair 的 finite-$N$ canonicity** | **【本專案數值結果】** | 固定獨立 RNG stream 的 source-of-record：$P(\kappa=1)$ 在 $N=20,50,100,200,400$ 分別為 $153/200=0.765$、$136/150=0.907$、$77/80=0.963$、$40/40=1.000$、$39/40=0.975$；每個 $N$ 的 Clopper–Pearson 區間獨立報告，**不得**把不同 $N$ pooled 成一個共同機率，也**不得**寫成 asymptotically almost surely。單元素刪除之穩定性以 parent 為獨立統計單位：$N=50$ 為 29 個 eligible parents、145/145 children 保持 $\kappa=1$；$N=100$ 為 20 parents、100/100 children 保持；child counts 只作描述，不套 child-level binomial CI。**物理解讀上限**：所得只是 $(\mathcal C,\prec)\to\{U,V\}/S_2$ 的兩個 canonical **global** null orderings（candidate chiral precursor），**不得稱為 chirality**，更不得等同每個 event 的 local two-state spinor fiber。 | `analysis/stage5a_kappa.py`, `tests/test_stage5a_realizer.py` |
| **Stage 5A small-$N$ dimension-2 假陽性警告** | **【本專案數值警告】** | 以相同 Alexandrov interval/causal-diamond 幾何做 matched higher-dimensional negative controls，order-dimension-2 在很小 causet 上具有高假陽性：固定 source-of-record 於 $N=10$ 得 $D=2/3/4$ 比例 $1.000/0.825/0.958$，$N=20$ 為 $1.000/0.075/0.300$；到 $N=40,80$ 才在目前樣本中對 $D=3,4$ 皆降為 0。故 **$N\lesssim20$ 的 realizer/dimension-2 診斷不得當作 1+1D 特殊性的可靠證據**；目前清楚判別力只在較大 $N$ 出現。 | `analysis/stage5a_kappa.py` |
| **Stage 5B-2：三值 rank-based link channel $\chi\in\{U,V,\bot\}$** | **【本專案數值結果／診斷工具】** | 對 link $x\lessdot y$ 定義 $\Delta r_U=r_U(y)-r_U(x)$、$\Delta r_V=r_V(y)-r_V(x)$；$\Delta r_U>\Delta r_V$ 記 $U$、反之記 $V$、相等必須記 $\bot$。tie 若硬塞進任一 sector 會破壞全域 $U\leftrightarrow V$ covariance。固定 source-of-record（$N=300$, seed 55002）共有 1328 links、16 ties（1.20%）；非 tie 的 rank 診斷與 sealed continuum $\mathrm{sign}(\Delta u-\Delta v)$ 一致率約 97.4%。此結果只證明 $\chi$ 是有用的 **global order+number diagnostic**，不得稱為 local chirality。 | `analysis/stage5b_link_channel.py`, `tests/test_stage5b_link_channel.py` |
| **Stage 5B-2：rank-based $\chi$ 不是 microscopic link-local rule** | **【已確認／本專案構造性介入】** | link 的 open Alexandrov interval 依定義為空，但 $\Delta r_U,\Delta r_V$ 會計數 interval 外的 null-coordinate strips。修正版固定介入不再把「interval 外」與 `link_preserved` 當成兩項獨立證據，而另以純 order 量 $|I(w,y)\cap C_{\rm old}|$ 衡量新增點與端點之間的既有因果深度。source-of-record 只選擇每個新增點該深度皆 $\ge5$ 的 60 條 links：60/60 可翻轉 $\chi$，共加入 320 點、每 link 加入數中位 5.5；全部新增點之深度 min/median/max 為 $5/8/21$，且全部舊元素間 order relation 與原 $x\lessdot y$ link 均保持。故**此 rank-based $\chi$** 明確依賴 order-separated 的 link 外 population，不是 microscopic link-local observable。範圍限定：此結論**不主張任何形式的 local two-state internal space 都不可能存在**；先前「number 是體積量所以任何 order+number 構造必然非局域」之過強說法已撤回。 | `docs/STAGE5B_RESULT_B.md`, `analysis/stage5b_link_channel.py`, `tests/test_stage5b_link_channel.py` |
| **BHS 對 intrinsic nearest-neighbour / finite-valency construction 的限制** | **【已知／Stage 5B 設計約束】** | Bombelli–Henson–Sorkin, arXiv:gr-qc/0605006, Theorem 1：full Minkowski Poisson sprinkling 不存在到 spacetime direction 的 measurable Lorentz-equivariant map；論文並指出有限方向集合與 finite-valency graph 亦無法在保持 Lorentz invariance 下由 sprinkling intrinsic 地選出。因此「每個 event intrinsic 挑一個 $U$ 鄰居與一個 $V$ 鄰居」的 checkerboard 式 nearest-neighbour 主線撤回。**作用域**：定理嚴格針對 full Minkowski sprinkling；有限 diamond 可含 boundary-induced direction，不能把有限區域成功當成 intrinsic full-spacetime local rule 的證據。 | `docs/STAGE5B_RESULT_B.md` |
| **Stage 5C acceptance specification 審計** | **【已確認／規格需修訂】** | 已對 handoff v2.0 的 C0–C11 草案完成獨立審計。結論：研究方向正確，但尚非可執行的 pass/fail specification；五項阻塞為 `K` 物件類型未定、realizer orbit 被誤當成 canonical representative、量子 two-component scaffolding 未完整入帳、驗證流程可循環且無數值門檻，以及 C8 將物理敏感性與任意可區分性混同。審計未提出任何候選 kernel；正式 acceptance specification 必須先修復上述問題。 | `docs/STAGE5C_ACCEPTANCE_AUDIT.md`, `docs/handoff_v2.0.md` |
| **Stage 5C C0–C11 acceptance specification** | **【已確認／規格定稿；Freeze-1a 未完成】** | 審計後經 Claude／GPT 多輪獨立交叉審查，v0.9 已把 C0–C11 升級為具 test／pass threshold／failure meaning／evidence artifact 的驗收契約，並封住 object-type 切換、realizer orbit 任選、L2/L3 容量偷渡、oracle 回流、候選自訂 projector／test space、事後放寬容差、跨 batch 多重嘗試、C4/C8 循環與候選層／規格層過強 No-Go 等漏洞。v0.9 另修正 C3b 的型別錯誤：不具 sector capability 是 program／provenance class，不是 output linear subspace；任意 fixed endomorphism 與 scalar function 的有限和在固定 causet 上張成整個 output space，而單一 $A\otimes f$ 是 rank-one Segre cone、不能取 quotient。C3b 因此改為 source／capability preflight 與 rank-one blind-variety distance 兩個互不替代的必要軸。規格定稿**不等於 Freeze-1a**：附錄 D.1 九項仍須在單一 freeze commit 對接完成；九項完成前不得設計候選 kernel、接觸 holdout 或開始 Stage 5C-1 confirmatory evaluation。全程未設計候選 kernel，handoff §2.3 的候選材料未帶入。 | `docs/STAGE5C_ACCEPTANCE.md`, `docs/STAGE5C_ACCEPTANCE_AUDIT.md`, `docs/handoff_v2.0.md` |
| **Stage 5C C8.4 定義域內困難對照可構造性** | **【CONTROL-VIABLE／matchability 與 bounded residual discriminability 已確認；Freeze-1a 未完成】** | domain-internal control 的 dimension-$\le2$、$\kappa=1$、matching 與 continuum-oracle 可行性均已確認。依 commit `49b5cf32` 凍結的 reference probe 已一次執行：12 blocks 全過 cohort gates，Layer 1、P、N、Q 四 claims 全過 Holm；Q 在 $n=1014$ 得 $d=+0.8510$，N 在 $n=1140$ 得 $d=+0.0015$ 並證成 $\pm0.15$ 等效，adjudicator 判 **CONTROL-VIABLE**。可宣稱的範圍只是在明定 43 維 probe bank 下，matched cohort 仍有 order-only residual information；不得稱為 Dirac propagation、幾何辨識，亦不保證候選 $K$ 可見。全部 48 段 1.1B／1.2B seeds 已 burned。C6/C7/C8 統一 observable／selector／smearing／norm 與全域 multiplicity 仍待完成，故**不是 Freeze-1a 完成**。 | `docs/STAGE5C_C8_4_HARD_CONTROLS.md`, `docs/STAGE5C_D1_3_PROBE_RESULTS.md`, `analysis/stage5c_reference_probe.py`, `tests/test_stage5c_reference_probe.py`, `docs/stage5c_development_log.md` |
| **Stage 5C D.1-3 residual-discriminability reference probe** | **【已確認／CONTROL-VIABLE；前置判決完成，D.1 第 3 項仍 PENDING】** | Protocol 於 `49b5cf32` freeze 後才執行；reserved witness 一次揭露並永久 burned。Layer1 $n=1014,d=+0.3801$；P 每側 $2304,d=+1.1311$；N $n=1140,d=+0.0015$ 且 TOST 等效；Q $n=1014,d=+0.8510$，四 claims 全過 Holm。另做的 baseline-leakage diagnostics 未預登記，故隔離、不公開數值、不參與判決，也不得承重。Monte Carlo 的 $1/200001$ 是 zero-exceedance 下的最小可報估計，不是 underlying $p$ 的精確值或上界。runner 現以 `BlindedCase` API 隔離 feature extraction 並用可執行 adjudicator 覆蓋全部 gates；但此 firewall 只是 API／程序層，公開 seeds 與演算法使 calibration weights 理論上可被刻意重算，未來 construction 必須禁止 import／執行 probe module 並接受 C0 provenance audit。統一 evaluator contract 尚未寫，Freeze-1a 仍為 PENDING。 | `docs/STAGE5C_D1_3_REFERENCE_PROBE.md`, `docs/STAGE5C_D1_3_PROBE_RESULTS.md`, `analysis/stage5c_reference_probe.py`, `tests/test_stage5c_reference_probe.py` |
| **Stage 5C D.1-3 selector／endpoint contract 路線** | **【提案／v0.12 草案；6a-S plus arm `PROTOCOL-INVALID`、DEV-0012 dress rehearsal mechanically clean、attestation review PENDING】** | 1.3B plus 的 formal verdict 與永久 burned 狀態不變；1.4B 未 claim／未生成。Amendment-001 未改任何 S1/S5/S6 threshold。依 main `9504abf3` 一次執行的 3.1B plus-development rehearsal 已完成：768 claims／samples、11 selectors 與 198 block pairs 的完整 ledger 通過 hash-chain／schema 重驗，categorical adjudication 為 11/11 `6a-S PASS`、0 `PROTOCOL-INVALID`、0 `INCONCLUSIVE`。此結果只證 runner v2 mechanically clean，不是 target contrast、selector viability 或 replacement arm 結論；3.1B 全部永久 burned，raw ledger 未獲明確公開授權。DEV-0012、burn registry 與 attestation 須先經 CI、獨立 review／merge，1.5B replacement plus 才能解鎖；1.4B 仍須等待 DEV-0013。若四檔或 runtime 漂移只能走 AMEND-0002＋fresh dress profile／base。6a-E、active wrong-support、C6/C7 instances、D.1 第 3 項及 Freeze-1a 均維持 PENDING，未設計 $K$。 | `docs/STAGE5C_D1_3_OBSERVABLE_CONTRACT.md`, `docs/STAGE5C_SELECTOR_FAMILY.md`, `docs/STAGE5C_6A_S_PREREGISTRATION.md`, `docs/STAGE5C_6A_S_RUNNER_FREEZE.md`, `docs/STAGE5C_6A_S_EXECUTION_INCIDENT.md`, `docs/STAGE5C_6A_S_PROTOCOL_AMENDMENT_001.md`, `docs/stage5c_6a_s_burn_registry.json`, `docs/stage5c_6a_s_dress_rehearsal_attestation.json`, `docs/stage5c_development_log.md`, `docs/STAGE5C_E3_WRONG_DIRECTION.md`, `analysis/stage5c_measure_prereg.py`, `analysis/stage5c_6a_s_runner.py`, `tests/test_stage5c_6a_s_runner.py` |
| **Stage 5C C8 intrinsic selector family** | **【已確認之 candidate-independent 結構交付物／DEV-0012 clean、replacement pre-execution】** | $\Sigma_{C8}$ 的 11 點 family、selector 定義與 numerical gates 均未改。正式 1.3B plus ledger 維持五點單臂 PASS／六點 protocol-invalid，且不得外推為 selector viability。Amendment-001 只以事故前固定的無因次 ESS fraction contract 修正 adjudicator；3.1B end-to-end dress rehearsal 已一次執行且 11/11 categorical PASS、無 protocol-invalid／inconclusive，故 runner v2 的真實規模機械路徑 clean。該 development 結果不得用作 selector viability、門檻調整或 replacement input。跨臂 code/runtime identity、burn registry 與 committed attestations 仍強制 lifecycle；1.5B replacement plus 與 1.4B minus 尚未生成，沒有 target contrast 或 combined verdict。DEV-0012 commit 未經獨立 review／merge前不得續跑 reserved arms。 | `docs/STAGE5C_SELECTOR_FAMILY.md`, `docs/STAGE5C_6A_S_PREREGISTRATION.md`, `docs/STAGE5C_6A_S_RUNNER_FREEZE.md`, `docs/STAGE5C_6A_S_EXECUTION_INCIDENT.md`, `docs/STAGE5C_6A_S_PROTOCOL_AMENDMENT_001.md`, `docs/stage5c_6a_s_burn_registry.json`, `docs/stage5c_6a_s_dress_rehearsal_attestation.json`, `analysis/stage5c_selector_family.py`, `analysis/stage5c_measure_prereg.py`, `analysis/stage5c_6a_s_runner.py`, `tests/test_stage5c_6a_s_runner.py` |
| **Stage 5C D.1-3 primary invariant endpoint** | **【已確認之 candidate-independent 代數交付物／尚未 freeze】** | 原草案的 universal two-branch collision 命題為假：$Q/N^2-S/N^2$ 即可令 chiral／Jordan 兩支在共同極限外分居正負；四組正權重數值例不能證 universal claim。正確的一維下界來自至少三個連通 planted branches 在 blind 點形成的三叉拓撲。另原三分量只有 coordinate-deletion minimality，非全域極小；顯式二維端點 $\mathfrak I_G=((Q-2\lvert W\rvert)/N^2,S/N^2)$ 已以 `00/+0/-+/0+/++` 分離五個登記代數類別，故最小維度恰為二。兩分量 sharp bounds 為 $[-1,2]$ 與 $[0,1]$。wrong-direction、continuum mapping、thresholds 與 joint-law metric 仍 PENDING。 | `docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md`, `analysis/stage5c_primary_invariant.py`, `tests/test_stage5c_primary_invariant.py` |
| **Stage 5C E3 wrong-direction 邊界** | **【已確認／部分交付；active control PENDING】** | 全域 $\sigma_x$ sector swap 因 $\sigma_x\in G$ 是 gauge，正確用途為逐位元 invariance arm，不得要求 discrimination。原草案的 $X\notin G\cdot R\iff X$ 可作 discrimination class 為假：orbit 外只解除 gauge 禁制，既定二維 endpoint 未必分離；已用不在同軌道但 endpoint 完全碰撞的顯式矩陣鎖成 falsifier。真正 wrong direction 必須定義為固定 continuum frame／output legs、改動 support feeding 的 active typed intervention，再依序通過 orbit-admissibility 與完整凍結參數域的 endpoint-law separation。兩個 matrix-level proposals 只保留為非採納 algebraic stress witnesses，不偷渡為 C7/E3 controls。typed selector 尚未定案，故 active wrong-support、D.1 第 3 項與 Freeze-1a 仍 PENDING；未設計候選 $K$。 | `docs/STAGE5C_E3_WRONG_DIRECTION.md`, `docs/STAGE5C_D1_3_OBSERVABLE_CONTRACT.md`, `tests/test_stage5c_wrong_direction.py` |
| **Stage 5C §1.4 basis-group／invariant-family 分析** | **【已確認之代數分析／fork B、ambient norm、invariant algebra 與後續 primary 已交付；尚未 freeze】** | fixed-slot 群經一般 noncompact orbit-closure no-go 與 C0 最小 primitive 紀律定為 $h=p\mathbb 1$、$G=T^2\rtimes S_2$、$G_{\rm eff}=U(1)\rtimes S_2$；pairing／adjoint 是 L2，整體尺度才屬 L3 normalization。Frobenius norm 顯式 discharge ambient existence。後續 invariant-algebra review 補入 $Q=|a-d|^2$ 並完成 toric／second-Veronese 解析生成證明；primary 再由獨立交付物選為二維 real vector。C3b 未完成的 capability／calibration 項與 D.1 第 3 項整體仍 PENDING；未設計 $K$。 | `docs/STAGE5C_D1_4_BASIS_GROUP.md`, `docs/STAGE5C_D1_4_INVARIANT_ALGEBRA.md`, `docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md`, `tests/test_stage5c_basis_group.py`, `tests/test_stage5c_invariant_algebra.py` |
| **Stage 5C §1.4 fork-B invariant algebra** | **【已確認／完整生成與 relation ideal 已交付；後續 primary 已選】** | torus 半群 Hilbert basis 為 $u=|b|^2,v=|c|^2,W=bc,\bar W$，其 toric kernel 唯一關係 $uv=W\bar W$。取 swap 後，完整 complexified-real ring 由 $A,P,W,S,Q,R$ 及共軛生成；$Q$ 對 ring generation 必要、對點值 separation 不必要。final presentation 有六條 second-Veronese minors；上游 $uv=W\bar W$ 已在消去 $u,v$ 時吸收。625 點結構化格點的正確 unordered-pair 計數為全純 2950／跨完整 orbit 1000，實族 1950／跨完整 orbit 0；此只作 regression，不代替全域解析證明。E3 承重 primary 必須含實不變量；後續二維 endpoint 已符合此限制，但不倒推本文件曾選定它。 | `docs/STAGE5C_D1_4_INVARIANT_ALGEBRA.md`, `docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md`, `tests/test_stage5c_invariant_algebra.py` |
| **Stage 5C C3b blind-variety distance form** | **【已確認之 evaluator form／尚未 freeze】** | C3b 拆為兩個互不替代的必要軸：(i) program／source／capability preflight；(ii) value-level rank-one Segre blind variety $\mathcal B_1=\{A\otimes f\}$ 的 weighted Frobenius distance。把 $K$ 寫成 $4\times D$ 後，Eckart–Young 給 $d_{\mathcal B_1}^2=\sum_{i\ge2}\sigma_i^2$ 與 $\rho=d/\|K\|_w$；sharp 上界為 $\sqrt{1-1/\min(4,D)}$，不是固定 $\sqrt3/2$。row-major fiber action 是 $B\otimes\bar B$；pair columns 與 weights 必須共置換。精確 $K=0$ 因位於 $\mathcal B_1$ 直接 C3b FAIL；近零才可依事前 scale-aware nontriviality gate 記 INCONCLUSIVE。此 form 只排除 rank-one value degeneracy；rank $>1$ 不證明程式使用 sector，故 source audit 與 C4 仍獨立承重。具體 domain／weights、capability schema、effect-size／noise／continuum calibration 尚未固定，Freeze-1a 維持 PENDING。未設計候選 $K$。 | `docs/STAGE5C_C3B_BLIND_DISTANCE.md`, `analysis/stage5c_blind_distance.py`, `tests/test_stage5c_blind_distance.py` |

---

## 3. 模型演進歷史對照表

本專案經過多次修正，各階段的核心思想與修正原因如下：

| 版本代號 | 核心想法 | 留下的主要成果 | 被修正/否定的原因 |
| :--- | :--- | :--- | :--- |
| **v0 直覺期** | 光折返形成時間與質量。 | 提出了「以零方向重建物質」的基本問題意識。 | 沿路累積時間、客觀折返率等直覺被數學否定。 |
| **v1 Checkerboard** | 光速虛歷史疊加成有質量傳播。 | 釐清了端點類時間隔、質量為振幅耦合參數的物理本質。 | 承認該模型仍預設了連續時空與度規背景。 |
| **v2 因果相位集** | 偏序、計數與相位共同選出時空。 | 意識到 KR 熵問題與背景獨立的嚴格建模要求。 | 不能僅靠「隨機相位會相消」等口號。 |
| **v2.1 現階段** | 分開傳播核與動力算子。 | 抓到了三角行列式的退化漏洞，並設計了 Q_test 診斷算子。 | $Q_{\text{test}}$ 還不是真正的 Dirac 算子，缺乏自旋與手徵結構。 |

---

## 附錄 A ~ D 參考資料與速查手冊

### 附錄 A：關鍵公式與白話解讀

1. **量子機率相干疊加**
   $$P = \left|\sum_k A_k\right|^2$$
   *解讀*：先將所有可能路徑的複數振幅 $A_k$ 相加，再取絕對值平方。相位會決定路徑之間是增強還是相消。

2. **1+1 維有效端點間隔**
   $$\Delta\tau_{\text{eff}} = 2\delta t\sqrt{N_R N_L}$$
   *解讀*：起點到終點的整體類時間隔，由向右與向左行進的步數乘積決定。

3. **高維有效端點間隔（已預設時空）**
   $$\Delta\tau_{\text{eff}} = \delta t\sqrt{2\sum_{i<j}(1 - n_i \cdot n_j)}$$
   *解讀*：各步方向 $n_i$ 越不一致（夾角越大），端點的有效類時間隔越大。

4. **1+1 維手徵振幅翻轉**
   $$A_{\text{flip}} \approx -i\left(\frac{mc^2\delta t}{\hbar}\right)$$
   *解讀*：質量控制左右手徵通道之間的相干混合。

5. **KR 熵尺度**
   $$M_{\text{KR}} \approx \exp\left[\left(\frac{\ln 2}{4}\right)N^2\right]$$
   $$\text{隨機相消後剩餘振幅} \approx \sqrt{M_{\text{KR}}} = \exp\left[\left(\frac{\ln 2}{8}\right)N^2\right]$$
   *解讀*：非時空網絡數量隨 $N^2$ 指數增長，剩餘振幅依然巨大，必須尋求結構性壓制。

---

### 附錄 B：三角行列式失效原理

對任何無回路有限因果偏序集 $\mathcal{C}$，皆能進行拓撲排序（線性延伸），使得若 $j \prec i$，則 $j$ 的編號早於 $i$。在此排序下，若傳播矩陣 $D_C$ 只從過去傳到未來：
$$[D_C]_{ij} \neq 0 \implies j \prec i \implies j < i$$
這意味著 $D_C$ 為**嚴格下三角矩陣**。因此：
1. $D_C$ 的對角線元素全為 0。
2. $D_C$ 為 nilpotent 矩陣（即存在 $K$ 使得 $D_C^K = 0$），所有特徵值均為 0。
3. 當加入相同的質量塊 $-mI$ 後，行列式退化為：
   $$\det(D_C - mI) = (-m)^{rN}$$
此行列式不包含任何非對角元素（即具體的因果網絡關係），因此對鏈、反鏈或 KR 網絡輸出完全相同的定值，無法用於幾何選擇。

---

### 附錄 C：研究紀律與防走偏原則

- **先驗算，再詮釋**：矩陣若退化或不變量失效，再漂亮的物理故事也必須撤回。
- **先分層，再命名**：底層若沒有時空，禁止在底層使用「光線、速度、角度、波長」等宏觀物理詞彙。
- **先比較總量，再談抑制**：面對 KR 熵，必須證明非流形類的「總振幅」被壓低，而不是僅說「隨機相位會相消」。
- **先回復已知物理，再追求新預測**：任何候選算子必須能在合適流形極限下重現 Dirac 傳播與勞侖茲不變性。
- **清楚標示猜想**：「可能」、「我們提案」不得在下一段或下一個文件中悄悄變成「已證明」。
- **保留否證條件**：如果模型必須靠手動塞入幾何方向或人工調參才能成功，即代表該方案失敗。

---

### 附錄 D：白話名詞表

- **事件 (Event)**：底層最基本的一次發生，沒有預設的時空座標。
- **因果關係／偏序 (Partial Order)**：僅記錄事件間的先後影響關係，不能有時間回圈。
- **量子振幅 (Amplitude)**：帶大小與相位的複數權重；所有可能性先相加再平方產生機率。
- **波函數 (Wavefunction)**：在特定描述基底（如位置）下，將量子振幅整理成一個函數。
- **德布羅意物質波 (de Broglie Wave)**：有動量物質在既有時空中的相位規律；不是底層振幅 of same state.
- **虛歷史 (Virtual Histories)**：路徑積分中的數學可能性，不代表粒子真實走過的路。
- **固有時間 (Proper Time)**：跟著有質量物體的理想時鐘量到的時間；光狀路徑的固有時間為零。
- **端點類時間隔 (Proper Interval)**：起點與終點的時空位移長度，可非零，即便每一小段都是光狀。
- **手徵 (Chirality)**：Dirac 粒子的左右手徵性質，質量會相干混合這兩個通道。
- **Dirac 算子**：控制費米子傳播與質量耦合的核心數學算子。
- **譜 (Spectrum)**：矩陣的特徵值集合，用於不依賴事件編號地辨識因果結構。
- **KR 序 (Kleitman-Rothschild Orders)**：數量隨 $N^2$ 指數級增長、不具備時空特徵的三層偏序結構。
- **粗粒化 (Coarse-Graining)**：忽略極小尺度細節，只保留大量事件形成的穩定大尺度幾何規律。
- **背景獨立 (Background Independent)**：幾何本身是動態湧現的結果，不預先設定時空舞台。

---

## 5. 文獻地圖與引用衛生 (Reference Map)

本節用以釐清已確立研究與本專案猜想的邊界。

### 5.1 核心參考文獻
- **Foster & Jacobson**, *Spin on a 4D Feynman Checkerboard*, arXiv:1610.01142。
  *關聯*：高維 checkerboard、自旋投影與質量耦合，但仍在既有時空背景中。
- **Bombelli, Henson & Sorkin**, *Discreteness without symmetry breaking: a theorem*, gr-qc/0605006。
  *關聯*：證明 Poisson 灑點在離散化中不協變地挑出偏好方向。
- **Surya**, *Directions in Causal Set Quantum Gravity*, arXiv:1103.6272。
  *關聯*：因果集基本結構、非局域性與研究綜述。
- **Sorkin**, arXiv:0710.1675。
  *關聯*：宇宙常數裝落預測的啟發式成功論證。
- **Sverdlov**, *Spinor fields in Causal Set Theory*, arXiv:0808.2956。
  *關聯*：因果集上的 spinor 探索；其「費米子促使流形湧現」屬推測，非已證實的行列式抑制。
- **Noldus**, *Free Fermions on causal sets*, arXiv:1305.0443。
  *關聯*：因果集上自由費米子的另一種技術方案。
- **Finster**, *Causal Fermion Systems: Classical Gravity and Beyond*, arXiv:2109.05906。
  *關聯*：概念近親，但基本物理對象與作用量定義不同，不可與本專案直接混同。
- **Loomis & Carlip**, arXiv:1709.00064。
  *關聯*：因果集路徑積分中非流形結構（如 KR 序）的抑制問題。
- **Bernardini**, hep-th/0701091。
  *關聯*：手徵振盪與 Zitterbewegung 關係。
- **Entropy and the Link Action in the Causal Set Path-Sum**, arXiv:2009.07623。
  *關聯*：因果集路徑和中的熵與連結作用量，提及典型 KR 結構之層級分配。
- **Path Integral Suppression of Badly Behaved Causal Sets**, arXiv:2209.00327。
  *關聯*：因果集路徑積分中 Badly Behaved Causal Sets 被重力作用量強烈壓低，降低了單獨靠物質相位壓低 KR 的物理要求。
- **Eichhorn, Mack, Le & Wagner**, *Charting Causal Set Configuration Space with Graph Observables*, arXiv:2605.27514（2026）。
  *關聯*：因果集圖觀察量研究，提供以已發表之因果集算子（如 $B$、$i(B-B^\dagger)$、圖拉普拉斯譜）作為觀察基底的參照。
- **Yazdi, Letizia & Kempf**, *Lorentzian Spectral Geometry with Causal Sets*, arXiv:2008.02291。
  *關聯*：計算因果矩陣衍生算子（含區塊三角算子與伴隨算子組合）的譜，並在最多 9 個事件的所有因果集上測試其分類能力——方法論與 Gate A 現階段工作高度重疊，應優先精讀。
- **Yazdi & Kempf**, *Towards Spectral Geometry for Causal Sets*, arXiv:1611.09947。
  *關聯*：上一篇的前身論文，證明因果矩陣衍生算子的譜具有「重新標記不變性」(relabeling invariance)，與本專案 §9.3 的標籤不變性要求直接對應，是現成的學術先例。
- **Nicholas 2026**, arXiv:2606.25993。
  *關聯*：湧現運動學基準 (emergent kinematics benchmark)。注意其非 pre-spacetime 理論，因為已預設 $\mathbb{R}^n$ 與不變間隔函數 $D$。

### 5.2 已查明並修正之文獻錯配
請確保在後續討論或引用時，**不要混淆以下編號**：
- **arXiv:0910.0673** 是 Sorkin 的 *Light, Links and Causal Sets*，**不是** Foster–Jacobson 的 checkerboard 論文。
- **quant-ph/9503015** 是早期 *HyperDiamond* 模型，**不是** Foster–Jacobson。
- **Phys. Rev. D 87, 063515** 是 *Everpresent Lambda II*，**不是** Bombelli–Henson–Sorkin 的定域性/方向定理。
- **arXiv:1703.07556** **不是** Sorkin 原始的宇宙常數論證論文。
- **arXiv:2111.05659** **不是** Sverdlov 的 *Spinor fields in Causal Set Theory*（該論文為 **arXiv:0808.2956**）。
- **DOI 10.1007/s11005-021-01467-1** 對應因果費米子系統的熵 (entropy) 論文，**不是**一般性理論總覽。
- **arXiv:1611.09947** 是 Yazdi & Kempf 的 *Towards Spectral Geometry for Causal Sets*（2016），**不是** *Lorentzian Spectral Geometry with Causal Sets*；後者的正確編號是 **arXiv:2008.02291**（Yazdi, Letizia & Kempf, 2020）。
- **arXiv:1910.02780**：為 Dragan & Ekert 的 *Quantum principle of relativity*，**禁止**作為能量—動量關係的文獻依據。
- **arXiv:1507.00330 Eq.(15) 的 $\gamma_2$ 與三個獨立來源不一致**：該式印為 $\sqrt{\pi}/4\approx0.4431$，但 (i) 其自身通式 Eq.(3) 在 $d=2$ 給出 $\gamma_2=1/2$；(ii) 來源論文 ASS arXiv:1403.1622 Eq.(3.6) 給 $C_2=1/2$，且其 Appendix C 明文寫出 $\chi=2\int ds\,s\,e^{-\rho s^2/2}K_0(\cdot)$，即 $C_2=1/2$；(iii) ASS Eq.(2.5) 的**精確閉式解** $\rho^{-1}g^{(2)}=-Ze^{Z/2}E_2(Z/2)$ 與 $\gamma_2=1/2$ 的求值在九個數量級上吻合至機器精度，而 $\sqrt{\pi}/4$ 連 IR 符號都錯（$g\to+0.2555$）。**結論**：後續一律採 $\gamma_2=1/2$。此為**本專案的高信度 typo 判定**，數值與解析交叉檢查均支持；在作者發布正式 erratum 之前，**不得**寫成「作者已承認之印刷錯誤」。（見 `analysis/gmom_2d_bbmm.py`, `analysis/spectral_dim_D.py`）

### 版本核對規則

若 GitHub UI 或工具端 retrieval 顯示的內容與 commit SHA 不一致，一律以 GitHub API / raw / tarball 取得的 **main HEAD** 為準；提出「某檔案不存在」之前必須先重抓 HEAD 確認，不得以既有 checkout 為據。

---
*狀態頁更新記錄：*
*v1.39 (2026-09-04) - 依 main `9504abf3989a57a75ebb1359c872a36ba4190549` 與 runner v2 一次執行 3.1B plus-target full-arm development dress rehearsal。全部 768 seeds 均先 durable claim 再生成並永久 burned；外部 NDJSON 為 6,842,118 bytes、SHA-256 `cf5f3584f3a8e193f0ef49a812c8acd41c1250c982581acb256ae7cbe03e352c`，hash chain／schema 重驗通過。10,196 records 完整；categorical adjudication 為 11/11 `6a-S PASS`、0 `PROTOCOL-INVALID`、0 `INCONCLUSIVE`。header 的 protocol digest／start-registry hash 分別為 `1343eb8e…29707`／`cfea86cf…f2f2`，實際 runtime 為 Python 3.12.13 build string、NumPy 2.3.5、SciPy 1.17.0。此結果只證 runner v2 mechanically clean；未公開或討論 per-causet／block-pair 數值，不得形成 target contrast、selector viability、threshold feedback、primary endpoint 或候選 $K$。DEV-0012／registry／attestation 尚待 CI 與獨立 review／merge；之前不得 claim 1.5B，1.4B 亦未生成。*

*v1.38 (2026-09-04) - 3.1B 執行前 custody clarification：CI dependency pin 只驗證程式與測試，不等於 formal `run-arm` 的實際本機環境；DEV-0012 必須逐字記錄 ledger header 的 `sys.version`／NumPy／SciPy strings。3.1B→1.5B→1.4B 必須維持同一 runtime identity；rehearsal 後若四個承重 code files 或三個 runtime strings 任一漂移，均不得重跑 3.1B、改寫環境紀錄或直接進 1.5B，唯一出口為 AMEND-0002＋全新 dress profile／未使用 seed base。本次只補文件，四個 protocol-invariant files、digest、burn registry、S1/S5/S6 gates 與 manifests 均未改；未生成 seed、未形成 contrast、primary endpoint 或候選 $K$。*

*v1.37 (2026-09-03) - AMEND-0001 凍結 DEV-0011 後的 6a-S runner v2 與 fresh lifecycle；本 commit 不生成任何 seed。唯一有問題的 `kish_ess` 對 selected integer 之 $10^{-12}$ 有因次絕對比較已刪除，改沿用事故前既有的無因次 `ess_fraction` relation／$\varphi=1$ identity；coverage／normalization／signed-U transform 採 deterministic exact recomputation，三類 mismatch 保存不同 protocol reason。S1/S5/S6 floors、margins、selector family、smearing 與 sample grid 均未改。新增硬性順序：3.1B full-arm dress rehearsal 必須先 clean adjudicate 並以 DEV-0012＋committed hash attestation 封存，才能 claim 1.5B replacement plus；plus 再以 DEV-0013＋attestation 證明無 `PROTOCOL-INVALID`／`INCONCLUSIVE` 後，1.4B minus 才解鎖。每臂 header／attestation 保存四個承重 code files 的 protocol-invariant digest 與 `sys.version`／NumPy／SciPy versions，prerequisite 與兩臂 combine 都要求相同；CI dependencies 已 pin。claim 前另驗證 DEV-0011→0014 committed append-only burn-registry prefix 並拒絕已 burned profile／target；rehearsal 後若需改四檔只能另立 AMEND-0002＋fresh dress profile／base。3.1B 明禁與任何 minus ledger 配對或回流成 replacement input。1.3B formal verdict 不重判且永久 retired；未形成 contrast、primary endpoint 或候選 $K$。*

*v1.36 (2026-09-02) - DEV-0011 記錄依 runner freeze merge commit `3bdc062a` 首次執行 reserved 6a-S plus arm。全部 768 個 1.3B seeds 已 durable claim、生成並永久 burned；完整 ledger 經使用者明確授權公開，counts、SHA-256 hash chain 與重組 hashes 完整。凍結 adjudicator 因 uniform-weight Kish ESS roundoff（最大約 $1.86\times10^{-11}$）超過共用 $10^{-12}$ 絕對容差，正式輸出六點 `PROTOCOL-INVALID`、五點單臂 PASS。為避免 precedence 隱藏 scientific failure，另由 raw fields 對六點完整重算：S1／S5／S6 failures 全為 0，無 non-finite 或 S2／S3／S4 false row；因此 defect 位於 runner identity check，但不得據此事後改判。發現後停止，1.4B minus manifest 未 claim／未生成，沒有 combined verdict、target numerical contrast、primary endpoint 或候選 $K$。6a-S 未完成；下一步改為先做顯式 protocol amendment 與 fresh seed lifecycle。*

*v1.35 (2026-09-02) - DEV-0010 完成 6a-S runner freeze，reserved execution 仍 PENDING。外部 3.0B development-only audit 將 $N=64$ 的 `endpoint_depth_mass_band(0.8,1.0)` 登記為 $d_{\rm mean}$ binding cell：兩 targets null p99 約 0.122／0.123、p99.9 約 0.146／0.151、5000 draws maxima 0.172／0.171，未超過 0.20；不改 margin，正式超標仍 FAIL，3.0B segment 全部 burned。新增 one-arm-only runner、exclusive-create append-only NDJSON ledger、generator 前 append＋fsync burned claim、SHA256 hash chain、完整 per-causet／block-pair raw schema與 signed $\widehat E_U$、重算 S1–S6 的 adjudicator，以及只接收 categorical arm verdicts 的 cross-arm combiner。verdict precedence 固定為 `PROTOCOL-INVALID > FAIL > INCONCLUSIVE > PASS`；runner import／tests 未生成 1.3B／1.4B reserved samples，未形成 contrast、primary endpoint 或候選 $K$。*

*v1.34 (2026-09-02) - DEV-0009 收入 correction head 的獨立 2.9B development-only audit：全部 11 點 × 3 個 $N$ × 2 targets × 64 causets 共 4224 次逐 causet 檢查為 0 floor／coverage violations，確認 order-dual pair-mass family 已解除原 structural failure；2.9B segment 全部 burned。signed U-statistic 的 null bias 已歸零，但 cross-$N$ stress 顯示 $d_{\rm law}\le0.20$ 缺乏 law-difference power，故不改 threshold、只把 claim 限縮為 gross-breakage tripwire，通過不構成 law-stability 獨立證據。另事前登記 `interval_exact(4)`, $N=64$ 為 floor-binding cell：development minima 38／43，常態近似估正式 512 causets 至少一次觸底約 3%；若發生仍依原規格判 FAIL，不得改 floor、排除 sample 或轉為 INCONCLUSIVE。reserved 1.3B／1.4B 未生成，未形成 target contrast、primary endpoint 或候選 $K$。*

*v1.33 (2026-09-01) - PR #12 pre-execution 獨立審查確認三項承重問題，於 reserved 1.3B／1.4B streams 尚未生成時修正。DEV-0008 以獨立 2.7B／2.8B development-only streams 重現原 `source_depth_band` 的結構性 floor failure，改為 order-dual、pair-mass-balanced `endpoint_depth_mass_band`，capacity 仍為 11；S5 law metric 由帶 positive null bias 的 V-statistic 改為保留符號的 unbiased U-statistic；完整 80 shell 改存 40 complex／80 real nonredundant half-shell；並明定 S5 不驗證 $\epsilon=1/16$，Gaussian 只在 ambient $\mathbb R^4$ mass-preserving，scale 與 box-boundary leakage 留給 E4。外部 2.6B 與本輪 2.7B／2.8B development ranges 全部 burned；未碰 reserved streams、target contrast、primary endpoint 或候選 $K$。6a-S 仍未執行。*

*v1.32 (2026-09-01) - 完成 C8 smearing／normalization／6a-S numerical prereg，observable contract 升至 v0.12。固定 $\varphi=1$、$\mathcal N_C=|\Sigma(C)|$、$\epsilon=1/16$ mass-one Gaussian、80-mode Fourier signature、同 target mean／energy distances 各 0.20、selected pairs／Kish ESS 32、coverage 0.005、$N=64,96,128$、4 blocks × 64 causets 與 `1.3B/1.4B` 專屬 seed manifest。新增 executable primitives 與 10 項結構 regression。reserved streams 尚未生成，故 6a-S 仍未執行；6a-E、active wrong-support、C6/C7 instances、D.1 第 3 項及 Freeze-1a 仍 PENDING。未設計或接觸候選 $K$。*

*v1.31 (2026-09-01) - 收入 C8 intrinsic selector family 的 candidate-independent 結構交付物，observable contract 升至 v0.11。獨立審計裁決 active wrong-support 不要求 C8 selector sector-aware：E3 應使用獨立且事前登記的 L4 evaluator tuple，故 handoff §2.3 的 $\Delta r_U,\Delta r_V$ 不獲默示豁免。C8 family 固定為 11 個 ordered parameter points 並關閉 capacity；修正原草案裸 ndarray API、relabel inverse、無 provenance coverage cap、concentration 必要條件與 reference-probe-derived member。新增 13 項純結構 regression；$\varphi/\mathcal N$、measure／ESS、數值門檻與 seeds 尚未固定，未執行也不得宣稱 6a-S PASS。D.1 第 3 項及 Freeze-1a 仍 PENDING，未設計候選 $K$。*
*v1.30 (2026-08-31) - 收入 E3 wrong-direction 邊界的部分交付，observable contract 升至 v0.10、basis-group 文件升至 v0.7。全域 sector swap 確認為 $G$-gauge invariance arm；獨立 review 撤回原草案「軌道外 iff 可作 discrimination class」與「方向在 smearing 後完全不可見」兩個過強命題。修正版把 Gate O orbit-admissibility 與 Gate E endpoint-law separation 分帳，並以軌道不同但二維 endpoint 完全碰撞的矩陣作 executable falsifier。真正方向控制改為完整 typed evaluator tuple 上的 active wrong-support intervention；兩個 matrix proposals 不採納、不偷渡進 C7/E3。新增 7 項 regression；selector／continuum mapping／完整參數域／joint-law regions／power 仍 PENDING，故 D.1 第 3 項及 Freeze-1a 未完成；未設計候選 $K$。*
*v1.29 (2026-08-31) - primary endpoint provenance 補強：修正 sharp-bound 公式遺漏的 `\\qquad`；明定第一分量 $Q-2\lvert W\rvert$ 的係數 $2$ 是 O(1) evaluator convention，不由 invariant algebra 或 planted separation 推導。任意 $c>0$ 對五個已登記代數類別保留同一符號樣式；選 $c=2$ 只為使 sharp lower bound 為 $-1$、與第二分量上界對齊，日後更改須走 protocol amendment。另明禁把第一分量正／負號解讀為物理傳播方向或用來預判 wrong-direction E3；其餘 Freeze-1a blockers 不變。未設計候選 $K$。*
*v1.28 (2026-08-31) - 收入 D.1-3 primary invariant endpoint，observable contract 升至 v0.9。獨立 review 否定原草案兩項承重結論：兩支共享極限不推出任意連續純量必在兩支非零參數處碰撞，$Q/N^2-S/N^2$ 是直接反例；三個原座標各自不可刪也只證該三向量的 coordinate-deletion minimality，不證全域三維下界。正確的一維 no-go 改由至少三個 connected planted branches 在 blind 點形成的三叉拓撲證明；並構造更小的二維 real invariant endpoint $((Q-2|W|)/N^2,S/N^2)$，以 `00/+0/-+/0+/++` 分離五個已登記代數類別，sharp bounds 為 $[-1,2]\times[0,1]$。新增 source-of-record 與 10 項 regression；wrong-direction E3、selector／smearing／normalization、continuum mapping、joint-law metric 與門檻仍 PENDING，故 D.1 第 3 項及 Freeze-1a 尚未完成；未設計候選 $K$。*
*v1.27 (2026-08-30) - 收入 C3b blind-variety distance evaluator form，observable contract 升至 v0.8、acceptance specification 升至 v0.9。獨立 review 修正九個承重問題：program／API blindness 不是 output linear subspace；任意 fixed endomorphism 有限和在固定 causet 上張成整個 output space；單一 $A\otimes f$ 是 rank-one Segre cone、不能取 quotient；純 fiber／pair 線性作用皆保持 rank one，只有不可分離 slot–pair weighting 會破壞；row-major fiber action 為 $B\otimes\bar B$；relabel 時 columns 與 weights 必須共置換；$\rho$ 上界依 $D$ 為 $\sqrt{1-1/\min(4,D)}$；精確零 kernel 位於 blind variety、直接 C3b FAIL；非零 noise null 只有在事前 planted family 與 discretizer 下才有定義。新增 source-of-record evaluator 與 12 項 regression。具體 domain／weights、capability schema、nontriviality／effect-size／noise／continuum calibration 仍 PENDING，故 C3b 與 Freeze-1a 尚未完成；未設計候選 $K$。*
*v1.26 (2026-08-30) - 收入固定 fork B 的完整 invariant-algebra 交付物，observable contract 升至 v0.7、basis-group 文件升至 v0.5。獨立 review 修正三個承重問題：其一，$uv=W\bar W$ 是消去前 torus presentation 的 relation，不是 final generating set 的第七條 syzygy；final ideal 由 symmetric rank-one $3\times3$ matrix 的六個 $2\times2$ minors 生成，並補 toric height-one 與 second-Veronese 的完整性證明。其二，holomorphic-only endpoint 只是在 invariant-information 層退化成與 fork C complexification 相同的 quotient，不會真的改變 basis group，也不會使已構造的 Frobenius norm 消失。其三，原格點表的 550／525／200 是 excess-entry counts，不是 pairs；改為逐 unordered pair 的 2950／1950，跨完整 $G$-orbit 為 1000／0，並證明 full $G$ 在該格點的 orbit intersection 由 finite $C_4\rtimes S_2$ subgroup 完整實現。新增 8 項 regression；primary $\mathfrak I_G$、當時所稱 C3b quotient contract 與 D.1 第 3 項仍 PENDING（C3b 命名與型別已由 v1.27 修正），未設計候選 $K$。*

*v1.25 (2026-08-29) - fork B 的 ambient invariant norm 由顯式 Frobenius 見證構造性 discharge：$\|M\|_F=\sqrt{\operatorname{tr}(MM^\dagger)}$ 在 $G=T^2\rtimes S_2$ 下因 unitary conjugation 與 trace cyclicity 保持不變，且在完整 $M_2(\mathbb C)$ 上連續、正定。新增 deterministic regression 鎖住 identity、relative phases、swap 及非零／零 cases。作用域明確限為 ambient-norm existence；當時所稱 sector-blind quotient／projection、aggregate norm 與 effect-size threshold 尚未完成（其 quotient 型別已由 v1.27 撤回），故不得宣稱 C3b 或 D.1 第 3 項已交付。另於下一輪 invariant-algebra brief 預先標出：$a+d,ad,bc,|b|^2+|c|^2,(a-d)(|b|^2-|c|^2)$ 及共軛即使能作 orbit-separating family，也不足以生成完整實不變量環；ring-generation proof 還須處理 $|a-d|^2$。未設計候選 $K$。*

*v1.24 (2026-08-29) - §1.4 basis-group fork B 定案，observable contract 升至 v0.5。決議具名採兩項現行 acceptance 前提：C3b 的 norm 是完整 object domain 上連續正定的 invariant norm；C0 最小 primitive 紀律要求只宣告 norm 所需結構並取完整 stabilizer。review 的 closed-subgroup 簡化清單不完整，故改以一般非緊軌道閉包論證排除所有非緊有效對角子群；再證明 swap-compatible Hermitian form 的非零 cross term 會加入 Stage 5A 未導出的 relative-phase primitive，故 $h=p\mathbb 1$、$G=T^2\rtimes S_2$、$G_{\rm eff}=U(1)\rtimes S_2$。依 frozen provenance table，$h/\mathbb R_{>0}$ 登記為 declared L2 pairing scaffold；整體尺度吸收進 L3 normalization，不列 L4。新增 3 項 regression；未選 primary invariant、未設計候選 $K$，D.1 第 3 項與 Freeze-1a 仍 PENDING。*

*v1.23 (2026-08-28) - 收入 §1.4 basis-group／invariant-family 的 PENDING-fork 交付物，observable contract 同步升至 v0.4。獨立 review 修正四個實質問題：區分一般被動 $GL(2)$ 換基與 fixed-slot stabilizer；撤回「A/B/C 窮盡所有 fork」及「C 只稍弱」；以 orbit-closure no-go 指出非緊 C 在完整 domain 不存在 continuous positive invariant norm；並把 $\Delta$ 的 C3b 邏輯改為「非零是非純量的充分 witness，而非 non-degeneracy 必要條件」。另修正 planted-class 表：monomial 全純 invariants 無法把 blind／chiral 代表與單側 triangular degeneration 分離。新增 13 項無額外 dependency 的代數 regression；未選 $G$、未設計候選 $K$。*

*v1.22 (2026-08-28) - observable contract 升至 v0.3。E3 明定 oracle-built planted controls 只驗 evaluator、對 order-only $K$ 存在性零蘊涵；E2 等效性 power 與 detection power 分帳並須反推獨立 cohort floor；6a-S 限為同 target、contrast-free batch prefilter，6a-E 才能讀 target contrast 並受序列 FPTP／fresh confirmation／family-wise spending 管制。另以完整 candidate-independent induced-measure law $\Pi_{\theta,g}$ 固定 continuum target，只有 theorem 條件成立才容許 invariant-of-mean 簡化，封住 Freeze-2a 依候選 concentration 靜默換端點的循環。Freeze-1a 九項仍無完整 DELIVERED 項目；未設計候選 $K$。*

*v1.21 (2026-08-28) - 收入 D.1 第 3 項 observable contract v0.2 草案。獨立 review 撤回 trace／determinant 的過強 invariant claim、pointwise nonlinear operation on distributions、$\mu$ divergence 必要性與 constant-conformal-factor 不可觀測說，並補 global/local basis 型別分流、weighted test measure、C8 matched-cohort joint law、selector 成員容量帳、fresh confirmation，以及候選前的完整 endpoint／planted-alternative feasibility；新增兩項代數 regression 鎖住 invariant／cross-fiber 反例。草案仍缺多項 candidate-independent form 與數值預登記，不是 Freeze-1a 交付完成；未設計候選 $K$。*

*v1.20 (2026-08-28) - 補上 post-hoc falsification 的不對稱例外：與 verdict 相容的未登記診斷仍隔離，不得作 `NO-CONFLICT` 正面佐證；一旦診斷與 verdict 的必要前提衝突，必須只公開 `POSTHOC-CONFLICT`、暫停 verdict 承重並以 fresh protocol／fresh seeds 解決。D.1 第 3 項暫採 distributional selector 起草路線，但明確不由 reference probe 推出合格 $\Sigma$ 存在，也不把固定端點路線誤寫成 no-go；selector feasibility 仍是 Freeze-1a blocker。未設計候選 $K$。*

*v1.19 (2026-08-28) - 依 commit `49b5cf32` 的 frozen protocol 執行 D.1-3 reference probe，12 blocks 與 Layer1/P/N/Q 四 claims 全部通過，adjudicator 判 CONTROL-VIABLE；48 段 1.1B／1.2B seeds 全部 burned。獨立審計補正 Monte Carlo floor 的語意，補上 `BlindedCase` payload boundary 與全 gate adjudicator；確定性重跑逐項重現。兩項事後 baseline diagnostics 因不在預登記公開輸出內而隔離，不得承重。此結果只證明明定 bank 下存在 order-only residual information，不是 Dirac／幾何 claim，也不完成 D.1 第 3 項的統一 evaluator contract。未設計或接觸任何候選 $K$。*

*v1.18 (2026-08-27) - 完成 D.1-3 執行前 power audit。like-for-like 比較更正了「matching 大量吃掉 local contrast」的錯誤：三個 burned development blocks 上 oracle effect 平均僅衰減約 $1.4\%$；原 $0.552$ unpaired Cohen's $d$ 與 $0.386$ paired $d$ 的跨尺度比較作廢。Layer-1 $\widehat L$ 因低 counts／Jeffreys smoothing 相對 $L_\theta$ 向零收縮約 $38\%$，只許作 diagnostic。Arm N 在 $n=576,\delta_N=0.15$ 的最保守 TOST power 僅約 $0.572$，故新增 $n_N\ge900$ gate（約 $0.910$ power），不放寬 equivalence margin。新增 DEV-0005；未執行 probe，1.1B／1.2B reserved ranges 完全未動。*

*v1.17 (2026-08-27) - 完成 D.1 第 3 項 residual-discriminability reference probe 的執行前預登記，未執行 probe。修正草案的四類缺口：刪除會縮小候選搜尋空間的 binary 回流；精確固定 Layer-1 box kernel、boundary correction 與 zero-count handling；把 P/Q/N 的資料生成、calibration/witness split、ridge score、未匹配與配對 randomization、N 等效性、Holm family、power floor、seed ranges 與 Monte Carlo streams 全部釘死；將所有失敗限制為 control/protocol 層判決，不得轉嫁為候選 FAIL。Freeze-1a 仍為 PENDING，候選設計禁令不變。*

*v1.16 (2026-08-27) - 修正 C8.4 證據 provenance：曾用於選擇 raw pool 768 的 `910–943M` blocks 降級為 exploratory，改由設計固定後才抽取的三組 `960–983M` out-of-sample blocks 承重，且全部通過 matching gates。匹配前 signed-SMD 稽核推翻「global matching 不會吃 local signal」的過強推論：local density 差異會洩漏進 height／interval statistics，故目前只確認 matchability，residual discriminability 必須在任何候選前另以已凍結的 candidate-independent reference probe 檢驗。新增 DEV-0004；新 seeds 全部 burned。未執行 reference probe、未設計候選 kernel、未接觸 candidate holdout。*

*v1.15 (2026-08-27) - Stage 5C C8.4 獨立 robustness review：確認原 $\kappa=1$ 256-pool 負結論被 pool size 混淆，且 512 source run 跨 seed 不穩（僅 2/5 blocks 同時通過 pairs／coverage）。在不改 $N$、$\theta$、11 維 baseline、calipers 或門檻下把 raw pool 提升為 768，source-of-record 與四組獨立 replications 全數通過；$\kappa=1$ 的 512／768 filter-then-match 亦通過。Acceptance spec 升至 v0.8，新增 global-scalar／provenance／power-preservation qualification，禁止用 local target proxy 合法殺掉 Axis B。C8.4 對照族可構造性已確認；D.1 第 3 項 basis-invariant evaluator mapping 與第 6 項 multiplicity 整合仍待完成，Freeze-1a 保持 PENDING。未設計候選 kernel、未接觸 confirmatory holdout。*
*v1.14 (2026-08-26) - 完成 Stage 5C C8.4 最高風險項的第一段 candidate-independent 可行性驗證：解析構造兩個皆位於 order-dimension-$\le2$ 的 conformal-volume controls，精確匹配總體積、marginals 與 ordering-fraction expectation，並以固定 11 維 C8.1 nuisance vector（含 $H/\sqrt N$ 絕對高度尺度）、maximum-cardinality optimal matching、power 下界及 RNG/hash manifest 驗證完整 dim-$\le2$ domain 的低階匹配可行。核心 control family 已找到，故不觸發 bounded-search exhaustion；但 $\kappa=1$ 限縮 domain 的小池 audit 未達 matching gate，另有 C6/C7/C8 basis-invariant primary-observable mapping 與全域 multiplicity rule 尚待整合，Freeze-1a 仍為 PENDING。新增 development log；未設計候選 kernel、未接觸 holdout。*
*v1.13 (2026-08-26) - Stage 5C C0–C11 acceptance specification v0.7 定稿（`docs/STAGE5C_ACCEPTANCE.md`）。經多輪交叉審查後，完成 verdict／object／provenance／continuum／statistical contracts，加入 candidate-independent Freeze-1a 與 candidate-specific Freeze-2a、quantum/mixing 的 staged freeze、全域 confirmatory budget、development／protocol-amendment logs、immutable C9/C10 core，以及防 projector／test-space／tolerance 吞掉 core 的規則。規格定稿不等於 Freeze-1a；附錄 D.1 九項仍待完成，故候選設計與 confirmatory evaluation 仍禁止。未設計候選 kernel。*
*v1.0 (2026-08-23) - 初始化狀態總表與附錄速查。*
*v1.1 (2026-08-24) - 新增 Gate 0 運動學選擇狀態與 Nicholas 2026 文獻、修正 arXiv:1910.02780 引用錯配。*
*v1.2 (2026-08-24) - 修正 arXiv:1611.09947 / 2008.02291 引用錯置（見附錄 5.2）；為「物質選幾何核心假說」補上因 Q_test 相位固定而受限的範圍註記。*
*v1.3 (2026-08-24) - 解除 Gate B 阻塞：以 BBMM (arXiv:1507.00330) 原始處方確立 regularization / Wick rotation / P(s)，完成 2D spectral dimension 並通過五項文獻自述檢查。*
*v1.12 (2026-08-26) - 完成 Stage 5C C0–C11 acceptance-specification 獨立審計（`docs/STAGE5C_ACCEPTANCE_AUDIT.md`）。判決為「規格需修訂」而非物理 No-Go：確認五項阻塞、七條循環驗證路徑與隱藏 primitive 類別；尤其要求先固定 `K` 的物件類型、對 realizer orbit 而非任選代表下降、把 C8 拆為 universality 與 sensitivity、並在 mass mixing 後重新執行量子可行性驗收。全程未設計候選 kernel，handoff §2.3 的候選材料未帶入規格架構。*
*v1.11 (2026-08-26) - 補入 Stage 5C 準備狀態與 `docs/handoff_v2.0.md` 索引；明確標示 C0–C11 尚為待獨立審查草案、替代 primitive 評估只作交接記錄，且「待評估候選材料」不得進入 acceptance specification 或提前成為 kernel 設計。同步將 handoff 檔頭改為歷史快照式表述，避免 HEAD／檔案數自我指涉過期。*
*v1.10 (2026-08-26) - Stage 5B-2 封存 limited Result B：將 link-channel 診斷改為 $U/V/\bot$ 三值以保持 sector-swap covariance；固定 $N=300$ source-of-record 顯示 rank-based $\chi$ 為高相關 global diagnostic，但修正版構造性介入以 $|I(w,y)\cap C_{\rm old}|\ge5$ 作獨立 order-depth 門檻；60/60 可翻轉 $\chi$ 且保持舊 order relation 與 link 本身不變，故此 $\chi$ 不是 microscopic link-local rule。共形論證之作用域收窄為「metric link-direction 不是 pure-order data，需 number/volume 補足」，不再誤寫成 channel 概念不存在。另正式記入 BHS full-Minkowski no-direction / finite-valency 約束，checkerboard nearest-neighbour 主線撤回；明確不宣稱任何 local two-state internal fiber 皆不可能。*
*v1.9 (2026-08-26) - Stage 5A 完成：以 $\kappa(P)=|\mathcal R_2(P)/(\mathrm{Aut}(P)\times S_2)|$ 取代過強的 labelled-UPO 唯一性，解析建立 permutation-diagram 計算法並以獨立 brute-force orbit regression 驗證。1+1D finite-$N$ sprinkling 顯示 global null-order sector pair 在商掉 automorphism 與全域交換後高度 canonical，但仍有 finite-$N$ 反例；單元素刪除以 parent-level 統計高度穩定。matched higher-dimensional controls 同時鎖定 small-$N$ 假陽性警告。所得僅為 candidate chiral precursor，明確不等同 local chirality。*
*v1.8 (2026-08-25) - Stage 4 完成：Track A vs Track B 公平 spectral-dimension 比較。新增通則 $d_s=D/\alpha$（寫在 $g_{\rm reg}$ 上，兩端統一）、BBMM universal 2 之代數來源（ASS Eq.3.16 的 $D/2$ 指數，措辭已收窄）、「共用 asymptotic 非公平控制」之 executable counterexample、regularization 保留 spectral-weight factor 之代數恆等式。`spectral_dim_D.py` 重構為 `build_operator`（Track A 行為數值不變）。全庫 90 passed。*
*v1.7 (2026-08-24) - 外部審閱修訂：(1) sum rule 證明補上其對 Stage-2 no-extra-zeros 的依賴；(2) positivity 承重之主張收窄為條件式；(3) $\tilde\rho$ 單調性降級為掃描範圍內之數值觀察；(4) 修正 $d_s^{UV}\to4$ 的來源歸屬——1502.01655 未計算 spectral dimension，該預期為本專案解析預測，待 Stage 4 驗證。*
*v1.6 (2026-08-24) - Track B Stage 3 完成：Eq.(55)/(56)/(85)/(86) quantum positivity 與 continuum spectral density 重現，$\tilde\rho>0$ 解析可見。新增三項本專案導出結果（總權重 $b/a^2-1$、positivity 承重點 $x_0=2.6943$、$\tilde\rho$ 單調性），皆明標非原文陳述。SJ 交叉檢查刻意未實作。*
*v1.5 (2026-08-24) - Track B Stage 1–2 完成：source-faithful operator、physical branch prescription（Eq.12）、A37 stability（argument principle $N=0$ + 割線 $\mathrm{Im}\,g\ne0$）、深 IR catastrophic cancellation 修復並封住。新增跨文獻解析識別一列（本專案導出，非原文陳述）。*
*v1.4 (2026-08-24) - 外部審閱回饋修訂：(1) $\gamma_2$ 改記為「三方來源不一致 + 本專案高信度 typo 判定」，並補入 ASS Appendix C 與 Eq.(2.5) 閉式解佐證；(2) Wick rotation 補回完整 analytic continuation + Feynman prescription 鏈條；(3) Fig.2 極大值降級為數值觀察，非驗收條件；(4) 降維與負模關係改記為【已知警告／未決】。新增 4D Track A replication 與 ASS 4D 不穩定性兩列。*
