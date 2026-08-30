# Stage 5C §1.4 續 — 固定 $G$ 下的 invariant algebra

狀態：**【已確認之代數交付物／v0.2；尚未 freeze】** — primary endpoint 已由後續獨立交付物選定。

前置：fork B 已定案，$h=p\mathbb 1$、$G=T^2\rtimes S_2$、$G_{\rm eff}=U(1)\rtimes S_2$。
驗證於 main `753d9ea`：54 檔、integrity 通過、147 passed。（歷史快照。）

本文件本身**不選定** primary $\mathfrak I_G$，只交付 invariant algebra、其關係，以及一條對
$\mathfrak I_G$ 的**強制限制**。後續選定見
`docs/STAGE5C_D1_3_PRIMARY_INVARIANT.md`；不得把後續結果倒寫成本文件的代數前提。

---

## 1. 作用

$B=\mathrm{diag}(e^{i\varphi},e^{i\psi})$ 為 $h$-unitary，故 $B^{-1}=B^\dagger$，
$M\mapsto BMB^\dagger$。寫 $M=\begin{pmatrix}a&b\\c&d\end{pmatrix}$、$\theta=\varphi-\psi$：

$$a\mapsto a,\quad d\mapsto d,\quad b\mapsto e^{i\theta}b,\quad c\mapsto e^{-i\theta}c,$$

$\sigma_x$ 則交換 $a\leftrightarrow d$、$b\leftrightarrow c$。

**$a$ 與 $d$ 完全不變（複數，非僅模）**；相位作用只約化 off-diagonal。這使不變量理論
分解為「對角部分不受約化」$\otimes$「off-diagonal 的相位不變量」。

---

## 2. $T^2$ 層：Hilbert basis

實不變量以 $(a,\bar a,d,\bar d,b,\bar b,c,\bar c)$ 為變數。單項式
$b^p\bar b^{\,q}c^r\bar c^{\,s}$ 的權重為 $\theta(p-q-r+s)$，故不變 $\iff p+s=q+r$。

> **命題 IA-1.** 半群 $\{(p,q,r,s)\in\mathbb Z_{\ge0}^4:p+s=q+r\}$ 的 Hilbert basis 恰為
> $$u=|b|^2,\qquad v=|c|^2,\qquad w=bc,\qquad \bar w=\bar b\bar c,$$
> 且唯一關係為 $uv=w\bar w$。
>
> *證明.* 設非零 $(p,q,r,s)$ 在半群中且不可分解。若 $p>0,q>0$ 可減 $u$；$r>0,s>0$ 可減
> $v$；$p>0,r>0$ 可減 $w$；$q>0,s>0$ 可減 $\bar w$。若四者皆不成立：$p>0$ 迫使 $q=r=0$，
> 則 $p+s=0$，矛盾；$p=0$ 時 $q+r=s$，$q>0$ 迫使 $s=0$ 故 $q+r=0$ 矛盾，於是 $q=0,r=s$，
> 而 $r>0$ 又迫使 $s=0$，故全零。$\square$
> 回歸：degree $\le4$ 的窮舉列出不可分解元恰四個。

「唯一關係」另需證明，不能只由 Hilbert-basis 枚舉推出。令
$\Phi:\mathbb C[U,V,W,\widetilde W]\to
\mathbb C[b,\bar b,c,\bar c]$ 送
$(U,V,W,\widetilde W)\mapsto(b\bar b,c\bar c,bc,\bar b\bar c)$。
其像的 exponent lattice rank 為 $3$，故 prime toric ideal $\ker\Phi$ 的 height 為 $1$；
$UV-W\widetilde W$ 是其中不可約 binomial，因此生成整個 kernel。把
$\widetilde W$ 依 reality involution 記為 $\bar W$，即得 $uv=W\bar W$。

故下式是**實多項式不變量環的複化表示**（barred symbols 在代數證明中先視為獨立變數，
最後再施加 complex-conjugation reality involution）：

$$R_{T^2}=\mathbb C[a,\bar a,d,\bar d,u,v,w,\bar w]\big/(uv-w\bar w).$$

---

## 3. $S_2$ 層：生成集

$\sigma_x$ 在 $R_{T^2}$ 上作用為**同時交換三對**：$(a,d)$、$(\bar a,\bar d)$、$(u,v)$，
並固定 $w,\bar w$。

令 $s_i=x_i+y_i$、$\delta_i=x_i-y_i$。座標變換後作用為 $s_i\mapsto s_i$、
$\delta_i\mapsto-\delta_i$，故不變量恰為對 $\delta$ 整體偶次者：

> **命題 IA-2.** 該 $\mathbb Z_2$ 作用的不變環由
> $$\{s_1,s_2,s_3\}\ \cup\ \{\delta_i\delta_j:1\le i\le j\le3\}\ \cup\ \{w,\bar w\}$$
> 生成。
>
> *證明.* sign action 下的不變單項式恰有偶數個 $\delta$ factors；任一偶次單項式都可把
> factors 兩兩分組，故由 $\delta_i\delta_j$ 生成。$s_i,w,\bar w$ 固定。torus relation
> $uv-w\bar w=0$ 對 swap 穩定；在 characteristic $0$，有限群的 Reynolds operator 使
> invariants functor exact，故先取上述生成元再通過該 invariant quotient 不會漏掉生成元。
> $\square$

化簡兩個冗餘項：$\delta_1^2=(a+d)^2-4ad$ 由 $\{a+d,ad\}$ 表出；
$\delta_3^2=(u+v)^2-4uv=(u+v)^2-4w\bar w$ 由 $\{u+v,w,\bar w\}$ 表出。
$\delta_2^2$ 為 $\delta_1^2$ 的共軛。**但 $\delta_1\delta_2$ 不可化簡**（§5）。

### 生成集（修正版）

$$\boxed{\ \{\,A,\ P,\ W,\ S,\ Q,\ R\,\}\ \text{及其共軛}\ \{\bar A,\bar P,\bar W,\bar R\}\ }$$

$$A=a+d,\quad P=ad,\quad W=bc,\quad S=|b|^2+|c|^2,$$
$$Q=|a-d|^2=\delta_1\delta_2,\qquad R=(a-d)\bigl(|b|^2-|c|^2\bigr)=\delta_1\delta_3 .$$

$S,Q$ 為實。**$Q$ 是先前草案漏掉的生成元**；漏掉的成因是同時把 $\delta_1^2$ 與
$\delta_3^2$ 判為冗餘後，未檢查混合項 $\delta_1\delta_2$。

---

## 4. 完整關係（final presentation 的六條 syzygies）

記 $z_1=A^2-4P=\delta_1^2$、$z_2=\bar A^2-4\bar P=\delta_2^2$、
$z_3=S^2-4W\bar W=\delta_3^2$。final generating set 的全部關係為六條：

$$Q^2=z_1z_2,\qquad R^2=z_1z_3,\qquad \bar R^2=z_2z_3,$$
$$R\bar R=Q\,z_3,\qquad Q\bar R=z_2\,R,\qquad QR=z_1\bar R,$$

**完整性證明.** 令 $q_{ij}=\delta_i\delta_j$。對稱矩陣

$$
\mathcal Q=
\begin{pmatrix}
z_1&Q&R\\
Q&z_2&\bar R\\
R&\bar R&z_3
\end{pmatrix}
=
\begin{pmatrix}\delta_1\\\delta_2\\\delta_3\end{pmatrix}
\begin{pmatrix}\delta_1&\delta_2&\delta_3\end{pmatrix}
$$

的像是 symmetric rank-$\le1$ cone（second Veronese cone）；其 defining ideal 由
$\mathcal Q$ 的全部 $2\times2$ minors 生成。上列六式正是這六個不同 minors。
原 torus relation $uv=W\bar W$ 已用
$u+v=S$、$(u-v)^2=S^2-4W\bar W=z_3$ **消去** $u,v$，所以它是上游 presentation 的
relation，不是 final generating set 的「第七條 syzygy」。同理
$z_1=A^2-4P$ 與 $z_2=\bar A^2-4\bar P$ 是可逆的座標替換。故消去後沒有遺漏額外
relation，六個 minors 給出完整 final relation ideal。

回歸測試只鎖住六式的代數恆等；「六式生成全部 ideal」由上述 second-Veronese
解析證明承擔，不得以有限殘差測試代替。

---

## 5. Ring generation $\ne$ orbit separation

這兩件事必須分開陳述，混用會導致錯誤結論。

> **命題 IA-3（$Q$ 是真生成元）.** $Q$ 不能由 $\{A,P,\bar A,\bar P\}$ 多項式生成。
>
> *證明.* $Q=|\delta_1|^2=|\delta_1^2|=|z_1|$，而 $z_1=A^2-4P$ 已是不變量。若存在
> $F(A,P,\bar A,\bar P)=Q$，限制到 $A=\bar A=0$、$P=-z/4$、$\bar P=-\bar z/4$
> 便得到多項式 $p(z,\bar z)=F(0,-z/4,0,-\bar z/4)=|z|$。再限制到實 $z=t$，
> $p(t,t)$ 在 $t>0$ 時須等於 $t$，
> $t<0$ 時須等於 $-t$。同一多項式不能同時滿足兩者。$\square$

> **命題 IA-4（$Q$ 在點值上冗餘）.** $Q=|z_1|$ 由 $z_1$ 的值唯一決定，故
> $\{A,P,\bar A,\bar P\}$ 的**點值**已決定 $Q$。

命題 IA-3 與 IA-4 並存：$Q$ 對**生成**是必要的，對**分離**不是。

**後果**：任何以「這組量能分離全部軌道」為由宣稱「已得到完整生成集」的論證都是無效的。
反向亦然：生成集的完整性不保證某個子集足以分離。$\mathfrak I_G$ 的選定必須分別論證
這兩件事。

**方法學註記**：命題 IA-3 是解析陳述，**原則上無法以逐點數值測試證明**——任何點值測試都
只能觸及命題 IA-4。回歸測試因此只鎖住命題 IA-4（$Q=|z_1|$）與 §4 的代數恆等式，
並在測試中明記命題 IA-3 由解析證明承擔。這與「不得用隨機零碰撞作完整性證據」是同一條紀律。

---

## 6. $\mathfrak I_G$ **必須**包含實不變量

> **命題 IA-5.** 若 primary $\mathfrak I_G$ 只由全純不變量（僅含 $a,b,c,d$，不含共軛）
> 構成，則它無法支撐 E3 對下列 degeneration pairs 的分離，亦不得單獨充作 C3b witness。
>
> *證明.* 全純單項式 $a^pd^qb^r c^s$ 在 $T^2$ 下權重為 $\theta(r-s)$，不變 $\iff r=s$；
> 再取 $S_2$ 不變得
> $$\mathbb C[a+d,\ ad,\ bc].$$
> 對 $fI$ 與 $fI+\lambda E_{12}$：兩者 $a=d=f$、$bc=0$，三個生成元全同，故不可分離。
> 對 $\mathrm{diag}(m_U,m_V)$ 與其上三角退化亦然。這正是 observable contract v0.7 §5
> 所指的兩組退化對。$\square$

> **命題 IA-6（為何這是結構性的而非偏好）.** 緊群 $T^2$ 的**全純**不變量與其複化
> $(\mathbb C^\times)^2$ 的不變量**完全相同**（權重條件 $r=s$ 不變；解析延拓）。
> 因此在 fork B 下只取全純族，會使**該 observable 所保留的 invariant information**退化為
> 與 fork C 相同的 holomorphic quotient；它繼承非閉軌道的 holomorphic indistinguishability
> 與上述退化對盲點。

這不是「真的重新選擇 fork C」：basis group 仍是 fork B，命題 6 的 Frobenius norm 仍存在，
完整 real invariant ring 也沒有消失。正確推論是：**holomorphic-only endpoint 會主動丟棄
當初選 fork B 才得到的分離資訊**，所以不能承擔 E3 的 degeneration discrimination；不是
fork B 本身突然失去正定 invariant norm。

**結論**：依本 contract 對 primary endpoint 的 E3 要求，$\mathfrak I_G$ **必須**至少含一個
涉及 $M^\dagger$ 的實不變量。$S=|b|^2+|c|^2$ 可分離上述兩組特定退化對
（$0$ vs $|\lambda|^2$）；這不表示單獨的 $S$ 已足以分離全部 planted classes 或全部
$G$-orbits。

$Q$ 與 $R$ 在此同樣是實不變量家族的成員，於選定 $\mathfrak I_G$ 時一併可用。

---

## 7. 結構化分離證據（非隨機）

在對子群 $\{\mathrm{diag}(i^k,1)\}\rtimes S_2$ **封閉**的格點
$\{0,\pm1,\pm i\}^4$（625 個矩陣）上窮舉：

| 族 | 相異族值 | 同族值的 unordered pairs | **跨完整 $G$-orbit pairs** |
| :--- | ---: | ---: | ---: |
| 全純 $\{A,P,W\}$ | 75 | 2950 | **1000** |
| 實族 $\{A,P,W,S,Q,R\}$ | 100 | 1950 | **0** |

原草案的 550／525 是「每個 bucket 扣掉首代表後的 excess entries」，200 是「不在首代表
subgroup orbit 的 excess entries」，**不是 pair counts**；表頭稱「碰撞對」因而錯誤。上表改為
逐一枚舉 unordered pairs 後的正確數字。

還需證明這個 finite subgroup 的 orbit test 在格點上等於完整 $G$-orbit test，不能只靠
「格點對 subgroup 封閉」。若兩個格點矩陣由完整 relative phase $e^{i\theta}$ 相連，且至少
一個 off-diagonal entry 非零，所需 phase 是兩個非零格點值之商，必屬
$\{1,i,-1,-i\}$；若 $b=c=0$，torus 作用本來就平凡。swap branch 同理。故完整 $G$-orbit
與 finite subgroup orbit 在此格點的交恰相同。

格點因此把碰撞**刻意逼出**，不是隨機零碰撞。全純族的 1000 個跨完整軌道 pairs 是
命題 IA-5 的量化見證。

實族在此格點上零跨軌道碰撞，與 basis-group 文件命題 5（緊群軌道皆閉 $\Rightarrow$ 實多項式不變量分離
軌道）及 §3–§4 的完整生成證明一致；但**格點結果不構成一般分離性證明**，一般性由解析
invariant-ring 證明與 compact-group separation theorem 承擔。

---

## 8. 尚未完成

- primary $\mathfrak I_G$ 已由後續交付物選定為二維 real invariant vector；本文件仍只承重
  可用族與 §6 的強制限制，其選定證明與推論上限由該交付物承擔。
- C3b 的 program／source capability schema，以及 rank-one blind-variety contract 的具體
  domain／weights、nontriviality／effect-size／noise／continuum calibration 仍未完成。
  `docs/STAGE5C_C3B_BLIND_DISTANCE.md` 只固定 SVD distance form；本文件只提供 ambient
  invariant algebra，兩者皆不能代替其餘 contract。
- 生成集的**極小性**未證（只證了生成性與 $Q$ 的不可約化）。
- 全部結論限 **1+1D**（C11），且依賴 fork B 的 L2 宣告；撤回該宣告則 §6 起全部失效。

---

## 附錄 — 回歸測試對應

`tests/test_stage5c_invariant_algebra.py` 鎖住：命題 IA-1 的 Hilbert basis 窮舉、
§4 的六條 final syzygy identities、命題 IA-4 的 $Q=|z_1|$、命題 IA-5 的兩組退化對、
§7 的格點 unordered-pair 計數（全純跨完整 orbit 1000／實族 0）。Hilbert-basis 的全次數
證明、toric kernel 的唯一關係、six-minor ideal 的完整性與命題 IA-3 均由解析證明承擔；
有限測試只作 regression。

**命題 IA-3 由解析證明承擔，不設點值測試**——理由見 §5 的方法學註記。
