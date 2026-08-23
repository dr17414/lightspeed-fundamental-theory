"""
test_gate_a_testbed.py
=======================
關卡 A｜有限因果網測試台 (Finite Causal Set Testbed)
對應 docs/handoff_v1.0.md §9.3、§10.3（關卡 A）、§10.4（下一個最小工作包）。

本檔案做四件 handoff 明確要求、但 test_appendix_b.py 尚未涵蓋的事：

1. 建立四類可重現的有限偏序樣本：
   chain、antichain、三層 KR-like、1+1 維 Poisson sprinkling
   （對應 §10.4 第 1 項）。

2. 明確分開 R_C（延遲傳播核，天生下三角）與 Q_C（§9.2 診斷算子），
   並修正一個既有程式碼裡的具體缺口：build_DC 過去把隨機的 U_ij
   綁在「矩陣位置」而不是「事件身分」上，導致標籤不變性從未被真正
   測試過（§9.3 第 1 項要求：重新編號不能改變特徵值/行列式，但舊測
   試裡 chain/antichain 的構造方式剛好不會觸發這個問題，所以沒被
   抓到）。這裡改成用事件的持久身分 (id) 決定 U_ij，讓「隨機重新
   編號」變成一個對同一組物理關係的真正重新標籤，而不是重新抽樣。

3. 檢查重新標記後，特徵值、trace(Q^k)、det 是否真正不變
   （§9.3 第 1 項 / §10.4 第 3 項）。

4. 在固定 N 下比較四類結構的譜/行列式是否真的不同（§9.3 第 2 項），
   並用同類多個隨機種子估計「類內」變異，避免把隨機噪聲誤讀成結構
   訊號；同時觀察 log|det Q_test| 隨 N 的成長（§10.4 第 4、5 項），
   這是為了 Gate C 的「總量比較」鋪路，本檔案本身不宣稱解決 Gate C。

狀態標記（依 STATUS.md 慣例）：本檔案全部結果屬於【提案／數值探索】，
Q_test 仍缺自旋、手徵、局域對稱結構（§9.4），不能因為譜非平凡或標籤
不變就宣稱找到了真正的 Dirac 算子或幾何選擇機制。

Run with: python3 tests/test_gate_a_testbed.py
或 pytest tests/test_gate_a_testbed.py -v
"""

import numpy as np


# ---------------------------------------------------------------------
# 1. 四類有限因果集生成器
#    全部回傳 (order, ids)：
#      order[i, j] == True 表示「位置 i 的事件 ≺ 位置 j 的事件」
#      ids[i] = 該位置上事件的持久身分（初始等於位置本身）
#    註：與 test_appendix_b.py 不同，這裡的 order 存的是「i ≺ j」
#    （j 在後），下方 build_RC 據此判斷方向，不預設位置一定要遞增。
# ---------------------------------------------------------------------

def chain(n):
    order = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            order[i, j] = True
    ids = np.arange(n)
    return order, ids


def antichain(n):
    order = np.zeros((n, n), dtype=bool)
    ids = np.arange(n)
    return order, ids


def kr_like(n, p=0.5, seed=None):
    """三層 Kleitman-Rothschild 型結構：L1-L2、L2-L3 獨立以機率 p 連結，
    L1-L3 的關係由「是否存在 L2 中介點」決定（這正是 KR 序數量爆炸的
    來源，見 STATUS.md 附錄 A 第 5 點）。不額外添加 L1-L3 隨機直接關
    係，以維持與文獻中 KR 結構定義一致。"""
    rng = np.random.default_rng(seed)
    sizes = [n // 3 + (1 if i < n % 3 else 0) for i in range(3)]
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
    ids = np.arange(n)
    return order, ids


def poisson_sprinkle_1p1(n, seed=None):
    """1+1 維因果菱形 (causal diamond) 中的 Poisson sprinkling，用零方向
    座標 u=t+x, v=t-x 取代直接放入 Minkowski 度規：均勻灑點在單位正方
    形 (u,v) 上，等價於均勻灑點在因果菱形內；a≺b 當且僅當 u_a<u_b 且
    v_a<v_b（Alexandrov interval 的乘積序，天生遞移，不需要另外做遞
    移閉包）。位置依 t=u+v 排序，即為一個合法的線性延伸。"""
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
    ids = np.arange(n)
    return order, ids


CLASSES = {
    "chain": lambda n, seed: chain(n),
    "antichain": lambda n, seed: antichain(n),
    "kr_like": lambda n, seed: kr_like(n, seed=seed),
    "poisson_1p1": lambda n, seed: poisson_sprinkle_1p1(n, seed=seed),
}


# ---------------------------------------------------------------------
# 2. R_C（延遲傳播核）與 Q_test（§9.2 診斷算子），身分綁定版本
# ---------------------------------------------------------------------

def interval_size(order, i, j):
    """事件 i、j 之間的因果區間大小 |I(i,j)|，用於 f(|I|) 的耦合權重。"""
    n = order.shape[0]
    return int(np.sum(order[i, :] & order[:, j]))


def _pair_rng(id_a, id_b):
    """由一對事件的『身分』決定性地產生一個 RNG，取代舊版單一 seed
    依序抽樣：這樣同一對事件不論目前排在哪個位置，得到的 U_ij 永遠
    相同，重新標記才真正只是換位置、不是重新抽樣。"""
    seed = hash((int(id_a), int(id_b))) % (2**32)
    return np.random.default_rng(seed)


def build_RC(order, ids, r=1):
    """(R_C psi)_i = sum_{j: j≺i} f(|I(j,i)|) U_ij psi_j，U_ij 由事件身分
    決定，不由目前位置決定。"""
    n = order.shape[0]
    N = n * r
    R = np.zeros((N, N), dtype=complex)
    for i in range(n):
        for j in range(n):
            if order[j, i]:  # j ≺ i
                s = interval_size(order, j, i)
                f = 1.0 + s + 0.3 * s ** 2
                rng_ij = _pair_rng(ids[j], ids[i])
                Uij = rng_ij.normal(size=(r, r)) + 1j * rng_ij.normal(size=(r, r))
                R[i * r:(i + 1) * r, j * r:(j + 1) * r] = f * Uij
    return R


def build_Qtest(order, ids, r, m):
    """§9.2: Q_test = [[mI, R_C], [R_C^†, -mI]]。"""
    Rc = build_RC(order, ids, r=r)
    N = Rc.shape[0]
    top = np.hstack([m * np.eye(N), Rc])
    bot = np.hstack([Rc.conj().T, -m * np.eye(N)])
    return np.vstack([top, bot])


def relabel(order, ids, rng):
    """隨機重新排列事件的『位置』，身分(ids)跟著事件走。回傳的
    (order2, ids2) 描述完全相同的一組物理因果關係，只是換了編號。"""
    n = order.shape[0]
    perm = rng.permutation(n)
    order2 = order[np.ix_(perm, perm)]
    ids2 = ids[perm]
    return order2, ids2


# ---------------------------------------------------------------------
# 3. 測試 1：標籤不變性
# ---------------------------------------------------------------------

def test_label_invariance():
    """對四類因果集各跑一次隨機重新標記，Q_test 的特徵值(排序後)、
    trace、trace(Q^2)、det 必須在數值誤差內完全一致。"""
    rng = np.random.default_rng(0)
    n, r, m = 9, 1, 0.5
    for name, builder in CLASSES.items():
        order, ids = builder(n, seed=42)
        order2, ids2 = relabel(order, ids, rng)

        Q1 = build_Qtest(order, ids, r, m)
        Q2 = build_Qtest(order2, ids2, r, m)

        ev1 = np.sort_complex(np.linalg.eigvals(Q1))
        ev2 = np.sort_complex(np.linalg.eigvals(Q2))

        assert np.allclose(ev1, ev2, atol=1e-8), f"{name}: 特徵值在重新標記後改變了"
        assert np.isclose(np.trace(Q1), np.trace(Q2), atol=1e-8), f"{name}: trace 改變了"
        assert np.isclose(np.trace(Q1 @ Q1), np.trace(Q2 @ Q2), atol=1e-8), (
            f"{name}: trace(Q^2) 改變了"
        )
        assert np.isclose(np.linalg.det(Q1), np.linalg.det(Q2), atol=1e-6), (
            f"{name}: det 改變了"
        )


# ---------------------------------------------------------------------
# 4. 測試 2：結構敏感性（含類內變異對照）
# ---------------------------------------------------------------------

def _log_abs_det(order, ids, r, m):
    Q = build_Qtest(order, ids, r, m)
    sign, logdet = np.linalg.slogdet(Q)
    return logdet


def structure_sensitivity_report(n=12, r=1, m=0.5, n_seeds=10):
    """對每一類跑多個隨機種子，回報 log|det Q_test| 的平均與標準差，
    讓『類間差異』可以跟『類內變異』直接比較，而不是只看單一樣本。"""
    report = {}
    for name, builder in CLASSES.items():
        vals = []
        for seed in range(n_seeds):
            order, ids = builder(n, seed=seed)
            vals.append(_log_abs_det(order, ids, r, m))
        vals = np.array(vals)
        report[name] = (vals.mean(), vals.std())
    return report


def test_structure_sensitivity_beyond_naive_degeneracy():
    """最低標準：至少要比 Appendix B 的舊死路好——四類之中不能全部
    都給出完全相同的 log|det|（那樣就等於行列式仍然只看 N, m）。"""
    report = structure_sensitivity_report(n=9, n_seeds=1)
    means = [v[0] for v in report.values()]
    assert not np.allclose(means, means[0], atol=1e-6), (
        "Q_test 對四類因果結構給出相同的 log|det|，等於重新掉回 Appendix B 的退化"
    )


# ---------------------------------------------------------------------
# 5. N 尺度：log|det Q_test| 與譜半徑如何隨事件數成長
# ---------------------------------------------------------------------

def n_scaling_report(n_values, r=1, m=0.5, n_seeds=5):
    rows = []
    for n in n_values:
        for name, builder in CLASSES.items():
            logdets, radii = [], []
            for seed in range(n_seeds):
                order, ids = builder(n, seed=seed)
                Q = build_Qtest(order, ids, r, m)
                sign, logdet = np.linalg.slogdet(Q)
                logdets.append(logdet)
                radii.append(np.max(np.abs(np.linalg.eigvals(Q))))
            rows.append((n, name, np.mean(logdets), np.std(logdets),
                         np.mean(radii), np.std(radii)))
    return rows


if __name__ == "__main__":
    test_label_invariance()
    print("[PASS] 標籤不變性：四類因果集重新編號後，特徵值/trace/trace(Q^2)/det 皆不變。\n")

    test_structure_sensitivity_beyond_naive_degeneracy()
    print("[PASS] Q_test 沒有掉回 Appendix B 的『行列式只看 N,m』退化。\n")

    print("=== 結構敏感性（N=12，每類 10 個隨機種子的 log|det Q_test|）===")
    for name, (mean, std) in structure_sensitivity_report(n=12, n_seeds=10).items():
        print(f"  {name:14s}  mean={mean:9.4f}   std={std:7.4f}")
    print()

    print("=== N 尺度變化（每個 (N, 類別) 用 5 個隨機種子取平均） ===")
    print(f"{'N':>3} {'class':14} {'mean logdet':>12} {'std logdet':>11} "
          f"{'mean radius':>12} {'std radius':>11}")
    for n, name, mlog, slog, mrad, srad in n_scaling_report([6, 9, 12, 15, 18]):
        print(f"{n:>3} {name:14} {mlog:12.4f} {slog:11.4f} {mrad:12.4f} {srad:11.4f}")
