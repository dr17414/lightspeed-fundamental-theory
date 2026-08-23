"""
test_gate_a_testbed.py
=======================
關卡 A｜有限因果網測試台 (Finite Causal Set Testbed) - 修正版
對應 docs/STATUS.md 與 docs/handoff_v1.0.md 的最新修訂要求。

主要更新：
1. 將 U_ij 從數字 ID 抽樣中分離，改為獨立的模型附加相位場資料 U，隨時空重新排列時一同進行置換，以滿足真正的「標籤不變性」。
2. 修正 KR-like 生成器，將三層事件比例調整為標準典型比例（1/4, 1/2, 1/4）。
3. 引入「相同事件數、相同連結密度」的隨機因果集對照組，排除僅由連結數量引起的結構敏感假象。
"""

import numpy as np


# ---------------------------------------------------------------------
# 1. 因果集與附加物理場產生器
# ---------------------------------------------------------------------

def chain(n):
    order = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            order[i, j] = True
    return order


def antichain(n):
    return np.zeros((n, n), dtype=bool)


def kr_like(n, p=0.5, seed=None):
    """三層 Kleitman-Rothschild 型結構：L1-L2、L2-L3 獨立以機率 p 連結，
    L1:L2:L3 事件數量依典型比例（1/4, 1/2, 1/4）分配。"""
    rng = np.random.default_rng(seed)
    s1 = n // 4
    s2 = n // 2
    s3 = n - s1 - s2
    sizes = [s1, s2, s3]
    bounds = np.cumsum([0] + sizes)
    L1 = range(bounds[0], bounds[1])
    L2 = range(bounds[1], bounds[2])
    L3 = range(bounds[2], bounds[3])
    
    order = np.zeros((n, n), dtype=bool)
    for a in L1:
        for b in L2:
            if rng.random() < p:
                order[a, b] = True
    for b in L2:
        for c in L3:
            if rng.random() < p:
                order[b, c] = True
    for a in L1:
        for c in L3:
            for b in L2:
                if order[a, b] and order[b, c]:
                    order[a, c] = True
                    break
    return order


def poisson_sprinkle_1p1(n, seed=None):
    """1+1 維因果菱形中的 Poisson sprinkling，藉由零座標 u, v 生成偏序關係。"""
    rng = np.random.default_rng(seed)
    u = rng.random(n)
    v = rng.random(n)
    perm = np.argsort(u + v)
    u, v = u[perm], v[perm]
    order = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if u[i] < u[j] and v[i] < v[j]:
                order[i, j] = True
    return order


def random_matching_density_set(n, target_relations, seed=None):
    """生成一個隨機因果集（經遞移閉包），其關係數量（連結數）盡量接近 target_relations。"""
    if target_relations == 0:
        return np.zeros((n, n), dtype=bool)
    max_relations = n * (n - 1) // 2
    if target_relations >= max_relations:
        return chain(n)
        
    rng = np.random.default_rng(seed)
    best_order = None
    best_diff = float('inf')
    
    # 在概率空間中搜尋以逼近目標連結數
    for p in np.linspace(0.01, 0.99, 30):
        order = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p:
                    order[i, j] = True
        # 進行遞移閉包 (transitive closure)
        changed = True
        while changed:
            changed = False
            for i in range(n):
                for j in range(n):
                    if order[i, j]:
                        for k in range(n):
                            if order[j, k] and not order[i, k]:
                                order[i, k] = True
                                changed = True
        rels = np.sum(order)
        diff = abs(rels - target_relations)
        if diff < best_diff:
            best_diff = diff
            best_order = order
            
    return best_order


def generate_U_field(order, r=1, seed=None):
    """為因果關係網路生成獨立的物理相位場 U (形狀為 n x n x r x r)，
    僅在具有因果偏序關係（j ≺ i）的邊上賦予隨機複數值。"""
    n = order.shape[0]
    rng = np.random.default_rng(seed)
    U = np.zeros((n, n, r, r), dtype=complex)
    for j in range(n):
        for i in range(n):
            if order[j, i]:
                U[j, i] = rng.normal(size=(r, r)) + 1j * rng.normal(size=(r, r))
    return U


# ---------------------------------------------------------------------
# 2. 算子構建與置換
# ---------------------------------------------------------------------

def interval_size(order, i, j):
    return int(np.sum(order[i, :] & order[:, j]))


def build_RC(order, U, r=1):
    """(R_C psi)_i = sum_{j: j≺i} f(|I(j,i)|) U_ij psi_j，U_ij 為獨立輸入場。"""
    n = order.shape[0]
    N = n * r
    R = np.zeros((N, N), dtype=complex)
    for i in range(n):
        for j in range(n):
            if order[j, i]:  # j ≺ i
                s = interval_size(order, j, i)
                f = 1.0 + s + 0.3 * s ** 2
                R[i * r:(i + 1) * r, j * r:(j + 1) * r] = f * U[j, i]
    return R


def build_Qtest(order, U, r, m):
    """Q_test = [[mI, R_C], [R_C^†, -mI]]。"""
    Rc = build_RC(order, U, r=r)
    N = Rc.shape[0]
    top = np.hstack([m * np.eye(N), Rc])
    bot = np.hstack([Rc.conj().T, -m * np.eye(N)])
    return np.vstack([top, bot])


def relabel(order, U, rng):
    """置換事件的位置索引，order 與物理場 U 一同置換。"""
    n = order.shape[0]
    perm = rng.permutation(n)
    order2 = order[np.ix_(perm, perm)]
    # 置換 U 矩陣的前兩個維度 (j, i)
    U2 = U[perm][:, perm]
    return order2, U2


# ---------------------------------------------------------------------
# 3. 測試 1：標籤不變性與場變異測試
# ---------------------------------------------------------------------

def test_label_invariance():
    rng = np.random.default_rng(0)
    n, r, m = 12, 1, 0.5
    
    # 測試四類結構
    generators = {
        "chain": lambda: chain(n),
        "antichain": lambda: antichain(n),
        "kr_like": lambda: kr_like(n, seed=42),
        "poisson_1p1": lambda: poisson_sprinkle_1p1(n, seed=42),
    }
    
    for name, gen in generators.items():
        order = gen()
        U = generate_U_field(order, r, seed=42)
        
        Q1 = build_Qtest(order, U, r, m)
        
        # 1. 執行重新標記（同時置換 order 與 U）
        order2, U2 = relabel(order, U, rng)
        Q2 = build_Qtest(order2, U2, r, m)
        
        ev1 = np.sort_complex(np.linalg.eigvals(Q1))
        ev2 = np.sort_complex(np.linalg.eigvals(Q2))
        
        assert np.allclose(ev1, ev2, atol=1e-8), f"{name}: 標籤置換後特徵值改變"
        assert np.isclose(np.linalg.det(Q1), np.linalg.det(Q2), atol=1e-6), f"{name}: 標籤置換後 det 改變"
        
        # 2. 場變異測試：物理因果關係完全不變，但更換 U 相位場，特徵值必須隨之改變（證明 U 是物理場，非 ID 衍生量）
        if name != "antichain": # antichain 邊數為 0，U 恆為 0
            U_other = generate_U_field(order, r, seed=999)
            Q_other = build_Qtest(order, U_other, r, m)
            ev_other = np.sort_complex(np.linalg.eigvals(Q_other))
            assert not np.allclose(ev1, ev_other, atol=1e-6), f"{name}: 更換相位場後特徵值卻沒有改變"


# ---------------------------------------------------------------------
# 4. 測試 2：特徵值對稱性與固定相位驗證
# ---------------------------------------------------------------------

def test_eigenvalue_symmetry_and_fixed_phase():
    """驗證 Q_test 矩陣特徵值成對出現（±λ）以及其行列式相位固定（無可消量子相位）。"""
    n, r, m = 12, 1, 0.5
    order = poisson_sprinkle_1p1(n, seed=42)
    U = generate_U_field(order, r, seed=42)
    Q = build_Qtest(order, U, r, m)
    
    evs = np.linalg.eigvals(Q)
    
    # 1. 驗證對稱性：若有特徵值 λ，則必有 -λ 存在
    evs_sorted = np.sort(np.real(evs)) # Q 為 Hermitian，特徵值皆為實數
    evs_negative_mirror = np.sort(-evs_sorted)
    assert np.allclose(evs_sorted, evs_negative_mirror, atol=1e-8), "特徵值未能成對對稱出現 ±λ"
    
    # 2. 驗證 det 正負號/相位：由於特徵值皆為 ±λ_k，
    #    det(Q) = ∏_k (λ_k) * (-λ_k) = (-1)^N ∏_k λ_k^2
    #    其中 λ_k^2 = m^2 + σ_k^2 恆為正。故對於給定的 N=12，det(Q) 必定恆為正實數（無虛數相位且正負號固定）。
    det_val = np.linalg.det(Q)
    assert np.isclose(np.imag(det_val), 0.0, atol=1e-8), "det(Q) 含有非零虛數相位"
    assert np.real(det_val) > 0, "對於偶數 N，det(Q) 未能保持為正"


# ---------------------------------------------------------------------
# 5. 結構敏感性與相同密度控制組比較
# ---------------------------------------------------------------------

def structure_sensitivity_with_control_report(n=12, r=1, m=0.5, n_seeds=10):
    report = {}
    
    # 計算主類別
    for name in ["kr_like", "poisson_1p1"]:
        vals, vals_control = [], []
        gen = kr_like if name == "kr_like" else poisson_sprinkle_1p1
        
        for seed in range(n_seeds):
            # 1. 主樣本
            order = gen(n, seed=seed)
            U = generate_U_field(order, r, seed=seed)
            Q = build_Qtest(order, U, r, m)
            sign, logdet = np.linalg.slogdet(Q)
            vals.append(logdet)
            
            # 2. 相同連結密度的隨機因果集控制組
            num_rels = np.sum(order)
            order_ctrl = random_matching_density_set(n, num_rels, seed=seed + 100)
            U_ctrl = generate_U_field(order_ctrl, r, seed=seed)
            Q_ctrl = build_Qtest(order_ctrl, U_ctrl, r, m)
            _, logdet_ctrl = np.linalg.slogdet(Q_ctrl)
            vals_control.append(logdet_ctrl)
            
        vals = np.array(vals)
        vals_control = np.array(vals_control)
        report[name] = (vals.mean(), vals.std(), vals_control.mean(), vals_control.std())
        
    return report


if __name__ == "__main__":
    test_label_invariance()
    print("[PASS] 標籤不變性：四類因果集在重新標記 (置換 order 與 U) 後，特徵值與 det 皆保持不變。")
    print("[PASS] 場變異驗證：保持因果偏序不變，僅改變附加物理場 U 時，特徵值產生變化（無 labels 殘留）。\n")
    
    test_eigenvalue_symmetry_and_fixed_phase()
    print("[PASS] 特徵值對稱性與固定相位：特徵值對稱成對 ±λ，對於固定 N 其行列式相位固定（無抵消相角）。\n")
    
    # 輸出結構敏感度與同密度對照組結果
    print("=== 結構敏感度與相同密度對照組（N=12，每類 10 個隨機種子） ===")
    print(f"{'Class Name':15s}  {'Sample log|det| (std)':25s} | {'Control log|det| (std)':25s}")
    print("-" * 75)
    report = structure_sensitivity_with_control_report(n=12, n_seeds=10)
    for name, (m_val, s_val, m_ctrl, s_ctrl) in report.items():
        print(f"{name:15s}  mean={m_val:7.3f} (std={s_val:5.3f})   | mean={m_ctrl:7.3f} (std={s_ctrl:5.3f})")
    print("\n*註：若主樣本與相同密度控制組的 log|det| 差異顯著，說明算子確實敏感於拓撲結構，而非僅測量連結數量。")
