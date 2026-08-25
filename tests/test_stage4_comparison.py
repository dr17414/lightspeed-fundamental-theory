"""Stage 4: fair Track A vs Track B spectral-dimension comparison.

THE CONTROL VARIABLE, stated once.  Both tracks go through
analysis.spectral_dim_D.build_operator and d_s() with the SAME zlo, zhi, npts,
spline, interpolation, BBMM Eq.(5) regularization, D = 4 momentum measure, s
grid and quadrature settings.  The only per-operator inputs are a, u_raw, u_ir
and u_uv -- the operator itself.

Forcing the two to share asymptotics would not be a stricter control; it would
replace one operator with the other.  build(D, ...) hard-codes u ~ -b/Z^(D/2),
which is right for the minimal GCB family and wrong for Track B (u ~ -8/Z);
routing Track B through it would manufacture d_s^UV -> 2.  See
test_forcing_track_A_asymptotics_onto_track_B_fakes_the_result.

CAVEAT carried from the adapter: applying BBMM Eq.(5) to Track B is a PROJECT
INFERENCE (the UV constant saturation, hence the coincidence-limit divergence,
is common to both operators).  1502.01655 neither regularizes nor computes a
spectral dimension.  The comparison is only as fair as that inference.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.spectral_dim_D import (                     # noqa: E402
    COEFFS, b_uv, build, build_operator, d_s,
)
from analysis.track_b_spectral_dim import (               # noqa: E402
    A_B, B_UV_B, BETA_UV_B, Z_SERIES_SWITCH, build_track_b, g_direct,
    g_reg_direct, u_raw_B, u_series, u_uv_B,
)

ZLO, ZHI, NPTS = 1e-6, 1e6, 801
D = 4


@pytest.fixture(scope="module")
def tracks():
    _, _, gA = build(D, ZLO, ZHI, NPTS)
    _, uB, gB = build_track_b(ZLO, ZHI, NPTS)
    return gA, gB, uB


# ------------------------------------------------------- the general law

@pytest.mark.parametrize("alpha,Dm", [(1.0, 4), (2.0, 4), (1.0, 2), (4.0, 4)])
def test_ds_equals_D_over_alpha(alpha, Dm):
    """THE GENERAL LAW, stated on the regularized eigenvalue so that BOTH ends
    are covered by one statement.

    If in some scale regime  g_reg(Z) ~ -c Z^alpha  with c > 0, alpha > 0, then
    substituting t = c s Z^alpha in P(s) = int dZ Z^(D/2-1) e^(s g_reg) gives
    P(s) ~ s^(-D/(2 alpha)), hence

        d_s = D / alpha.

    UV is the corollary: u ~ -b/Z^beta gives g_reg = a g/u -> -(a^2/b) Z^beta,
    i.e. alpha = beta, so d_s^UV = D/beta.

    IR is the SAME statement, and this is why the law belongs on g_reg rather
    than on u: in the IR u -> a, a constant, which is not of the form -b/Z^beta
    at all -- writing "beta = 1" there was an abuse of notation.  What is true
    is that g_reg -> -Z, i.e. alpha = 1, giving d_s^IR = D.  Both operators
    share this, which is why both tracks tend to 4 in the IR.

    Tested on SYNTHETIC operators with planted alpha, so it checks the pipeline
    itself rather than either physical operator.
    """
    a, b = -2.0, 8.0
    op = build_operator(a,
                        lambda Z: -b / Z ** alpha,
                        lambda Z: a + Z,
                        lambda Z: -b / Z ** alpha,
                        1e-8, 1e8, 401)
    assert d_s(op[2], 1e-8, Dm) == pytest.approx(Dm / alpha, abs=2e-3)


@pytest.mark.parametrize("Dm,lo,hi", [(2, 1e-8, 1e8), (4, 1e-6, 1e6)])
def test_ir_end_follows_the_same_law_with_alpha_one(Dm, lo, hi):
    """IR: g_reg -> -Z for every operator satisfying the shared IR condition
    g -> -Z, so alpha = 1 and d_s^IR = D.  One law, both ends."""
    _, _, greg = build(Dm, lo, hi, 401)
    Z = np.array([lo * 10, lo * 100])
    assert np.all(np.abs(greg(Z) / (-Z) - 1.0) < 1e-2)


def test_minimal_GCB_gives_two_in_every_dimension():
    """CONSEQUENCE of the law, and the whole content of BBMM's 'universal'
    reduction: ASS Eq.(3.16) gives the minimal family u ~ -b/Z^(D/2) in EVERY
    dimension, i.e. beta = D/2, so d_s^UV = D/(D/2) = 2 identically.

    SCOPE OF THIS CLAIM.  Within BBMM's regularized spectral-dimension
    prescription, the dimension-independent limiting value 2 is traced
    algebraically to the exponent D/2 in ASS Eq.(3.16).  That explains where the
    number 2 comes from.  It does NOT establish that the exponent D/2 is itself
    without deeper origin -- why this family of causal-set operators produces
    exactly D/2 may well reflect something about their construction.  Do not
    restate this as "the universal reduction is merely arithmetic".

    Track B escapes the value 2 only because its subleading power is Z^-1
    rather than Z^(-D/2).
    """
    for Dm, (lo, hi) in [(2, (1e-8, 1e8)), (4, (1e-6, 1e6))]:
        _, _, greg = build(Dm, lo, hi, 401)
        assert d_s(greg, 1e-8, Dm) == pytest.approx(2.0, abs=1e-3)


# ------------------------------------------------------- Track B operator

def test_u_series_matches_an_independent_high_precision_reference():
    """The asymptotic evaluator against 80-digit mpmath -- NOT against g_direct.

    An earlier version of this test compared u_series(Z) with A_B - g_direct(Z)
    at Z > Z_SERIES_SWITCH, where g_direct is DEFINED as A_B - u_series(Z).  It
    therefore asserted u_series == a - (a - u_series) and checked nothing.  The
    reference has to come from outside the module.

    Measured truncation error at the switch Z = 200:
        6 terms 1.9e-08 | 12 terms 3.9e-14 | 16 terms 1.8e-16
    """
    mp = pytest.importorskip("mpmath")
    mp.mp.dps = 80

    def u_ref(Z):
        Z = mp.mpf(Z)
        g = -Z + (Z ** 2 / 2) * mp.exp(Z / 2) * mp.e1(Z / 2)
        return -2 - g

    for Z in [Z_SERIES_SWITCH, 300.0, 1e3, 1e4]:
        ref = u_ref(Z)
        got = mp.mpf(float(u_series(np.array([Z]))[0]))
        assert float(abs(got - ref) / abs(ref)) < 1e-12


def test_series_precision_does_not_set_the_floor_on_the_spline_check():
    """The evaluator must be more accurate than the interpolation error it is
    used to measure, or the spline-vs-direct number is an artefact of the
    evaluator.  With 6 terms it was (1.4e-9 reported, 2.4e-10 real)."""
    mp = pytest.importorskip("mpmath")
    mp.mp.dps = 80
    Z = Z_SERIES_SWITCH
    g = -mp.mpf(Z) + (mp.mpf(Z) ** 2 / 2) * mp.exp(mp.mpf(Z) / 2) * mp.e1(mp.mpf(Z) / 2)
    ref = -2 - g
    got = mp.mpf(float(u_raw_B(np.array([Z * 1.0001]))[0]))
    _ = got  # continuity is checked elsewhere; the point is the bound below
    err = float(abs(mp.mpf(float(u_series(np.array([Z]))[0])) - ref) / abs(ref))
    assert err < 1e-11


def test_u_series_is_asymptotic_not_convergent():
    """(n+1)! 2^(n+1) eventually beats Z^-n, so more terms is not more accurate
    at small Z.  Guards against anyone lowering Z_SERIES_SWITCH or raising the
    term count on the assumption that the series converges."""
    Z = np.array([5.0])
    errs = [abs(float(u_series(Z, n)[0]) - float(u_raw_B(np.array([5.0]))[0]))
            for n in (4, 8, 16, 24)]
    assert errs[-1] > errs[0]                      # diverging, not converging
    assert Z_SERIES_SWITCH >= 100.0


def test_u_is_negative_and_g_stays_in_the_regularization_domain():
    """a < g < 0 for all Z > 0, so the Eq.(5) denominator never vanishes."""
    Z = np.logspace(-18, 18, 2000)
    u = u_raw_B(Z)
    g = g_direct(Z)
    # u is what the Eq.(5) denominator actually uses, and it is computed from
    # the series, so it is strictly negative everywhere and never vanishes.
    assert np.all(u < 0.0)
    assert np.all(g < 0.0)
    assert np.all(g >= A_B)
    # g approaches a only asymptotically, so g > a is strict only while the gap
    # is representable: |u| = 8/Z falls below the ulp of 2 (4.4e-16) at
    # Z ~ 1.8e16, above which g == a in double precision.  That is float
    # saturation, not a domain violation -- u carries the gap, and u is fine.
    near = Z < 1e15
    assert np.all(g[near] > A_B)


def test_g_direct_does_not_cancel_at_large_Z():
    """REGRESSION.  -Z + (Z^2/2) e^{Z/2} E_1(Z/2) is -Z + Z(1 - 2/Z + ...); above
    Z ~ 5e16 the leading terms cancel to noise and g_reg comes out POSITIVE,
    which silently overflows the exp in d_s.  g_direct must switch to a - u_series
    there.  Caught only because the spline/direct d_s cross-check blew up to 6e23.
    """
    Z = np.array([1e17, 1e18, 1e19])
    assert np.all(g_direct(Z) < 0.0)
    assert np.all(g_direct(Z) == pytest.approx(A_B, abs=1e-15))
    assert np.all(g_reg_direct(Z) < 0.0)


def test_track_B_uv_exponent_is_one():
    """beta = 1, against the minimal family's beta = D/2 = 2.  This single
    exponent is the entire origin of the 4-vs-2 difference."""
    assert BETA_UV_B == 1.0
    for Z in [1e6, 1e8]:
        assert float(u_uv_B(np.array([Z]))[0]) * Z == pytest.approx(-B_UV_B)
    assert b_uv(4) / COEFFS[4]['a'] ** 2 != pytest.approx(B_UV_B / A_B ** 2)


# ------------------------------------------------- interpolation is not the cause

def test_track_B_spline_reproduces_direct_u(tracks):
    _, _, uB = tracks
    Z = np.logspace(np.log10(ZLO), np.log10(ZHI), 500)
    assert np.abs(uB(Z) / u_raw_B(Z) - 1.0).max() < 1e-8


def test_track_B_spline_reproduces_direct_ds(tracks):
    """The comparison's main methodological risk was Track A on a spline against
    Track B without one.  Routing Track B through the SAME spline changes
    d_s by ~1e-9, so interpolation cannot explain the 4-vs-2 result."""
    _, gB, _ = tracks
    worst = max(abs(d_s(gB, s, D) - d_s(g_reg_direct, s, D))
                for s in np.logspace(-4, 4, 9))
    assert worst < 1e-7


@pytest.mark.parametrize("npts", [401, 1601])
def test_result_is_insensitive_to_the_shared_grid(npts):
    _, _, gB = build_track_b(ZLO, ZHI, npts)
    _, _, gB0 = build_track_b(ZLO, ZHI, NPTS)
    for s in [1e-2, 1.0, 1e2]:
        assert d_s(gB, s, D) == pytest.approx(d_s(gB0, s, D), abs=1e-5)


def test_uv_splice_error_follows_the_six_over_Z_law():
    """u = -(8/Z)(1 - 6/Z + ...), so truncating at the leading term at the
    spline's upper edge leaves a relative error of 6/zhi: 6e-5 at 1e5, 6e-6 at
    1e6.  Confirms zhi = 1e6 puts Track B's splice error at a few ppm, far below
    the 2-vs-4 effect being measured."""
    for zhi, expected in [(1e5, 6e-5), (1e6, 6e-6), (1e7, 6e-7)]:
        rel = abs(float(u_uv_B(np.array([zhi]))[0])
                  / float(u_raw_B(np.array([zhi]))[0]) - 1.0)
        assert rel == pytest.approx(expected, rel=0.1)


# ------------------------------------------------------------ the comparison

def test_track_A_reduces_to_two_and_track_B_does_not(tracks):
    """The Stage 4 result.  Same pipeline, same grid, only the operator differs."""
    gA, gB, _ = tracks
    assert d_s(gA, 1e-4, D) == pytest.approx(2.0, abs=5e-3)
    assert d_s(gB, 1e-4, D) == pytest.approx(4.0, abs=5e-3)
    assert d_s(gA, 1e4, D) == pytest.approx(4.0, abs=5e-3)
    assert d_s(gB, 1e4, D) == pytest.approx(4.0, abs=5e-3)


def test_forcing_track_A_asymptotics_onto_track_B_fakes_the_result():
    """The trap this refactor exists to prevent.

    Routing Track B through the minimal family's UV branch (u ~ -b/Z^2) instead
    of its own (u ~ -8/Z) drives d_s^UV to 2 -- not because the operators agree
    but because Track B's physics was overwritten above the spline edge.  Shared
    asymptotics is not a tighter control variable; it is a different operator.
    """
    src = lambda Z: float(u_raw_B(np.array([Z]))[0])

    # (a) Splice Track A's exponent on continuously (b chosen so -b/Z^2 meets
    #     Track B's -8/Z at zhi).  Track B's own operator below zhi, Track A's
    #     beta above it -- and d_s^UV lands on 2, exactly the answer Track A
    #     gives.  Nothing about Track B's operator changed below the spline
    #     edge; only the tail was overwritten, and the tail is what s -> 0 sees.
    faked = build_operator(A_B, src, lambda Z: A_B + Z,
                           lambda Z: -(8.0 * ZHI) / Z ** 2, ZLO, ZHI, NPTS)
    assert d_s(faked[2], 1e-10, D) == pytest.approx(2.0, abs=1e-3)

    _, _, honest = build_track_b(ZLO, ZHI, NPTS)
    assert d_s(honest, 1e-10, D) == pytest.approx(4.0, abs=1e-3)

    # (b) The cruder version -- pasting Track A's b_uv(4) on without matching --
    #     leaves a five-order discontinuity at zhi and returns neither 2 nor 4
    #     but a meaningless small number.  Worth recording: the failure mode is
    #     not always a plausible-looking wrong answer.
    crude = build_operator(A_B, src, lambda Z: A_B + Z,
                           lambda Z: -b_uv(4) / Z ** 2, ZLO, ZHI, NPTS)
    assert d_s(crude[2], 1e-8, D) < 0.1


def test_track_B_overshoot_is_recorded_as_observation_only(tracks):
    """[NUMERICAL OBSERVATION -- NOT a literature acceptance criterion]

    Track B is not a flat 4 -> 4: it overshoots the Hausdorff dimension in
    mid-range, peaking near d_s = 4.537 at s = 2.42 (continuous search; a
    log-spaced grid reads 4.531 at s = 3.16 and misses the true peak).

    No published value exists to check this against, and it depends on applying
    BBMM Eq.(5) to Track B, which is our inference.  Bounds are therefore loose,
    and the peak's height and location must not be quoted as agreement with any
    source.  Note also that overshoot is NOT what distinguishes the tracks --
    both overshoot, Track A near s ~ 10 and Track B near s ~ 2.4.  The ENDPOINTS
    are the difference.
    """
    gA, gB, _ = tracks
    ss = np.logspace(-0.5, 1.5, 12)
    dsB = np.array([d_s(gB, s, D) for s in ss])
    dsA = np.array([d_s(gA, s, D) for s in ss])
    assert dsB.max() > 4.4
    assert dsA.max() > 4.0
    assert ss[int(np.argmax(dsB))] < ss[int(np.argmax(dsA))]


# ------------------------------------- regularization vs the Stage 3 weight

def test_regularization_preserves_the_spectral_weight_factor_exactly():
    """BBMM Eq.(5) leaves Im g / |g|^2 pointwise INVARIANT.

    Because g_reg = a g / (a - g) with a real,

        1/g_reg = (a - g)/(a g) = 1/g - 1/a,

    and 1/a is real, so Im(1/g_reg) = Im(1/g).  Since Im(1/w) = -Im w / |w|^2,

        Im g_reg / |g_reg|^2  =  Im g / |g|^2

    wherever both sides are defined -- i.e. away from the zeros and poles of the
    denominators involved (g = 0, g = a).  On the physical timelike cut neither
    occurs: g = 0 is excluded by the stage-2 stability result together with
    Im g > 0, and g = a only asymptotically.  Stated this way so the algebraic
    identity is not read as a global claim that includes its own singularities.

    That combination is exactly the factor carrying the Stage 3 quantum spectral
    weight, Wtilde = (2/Lambda^2) Im g / |g|^2 (Eq. 55 + Eq. 12), and hence the
    continuum spectral density of Eq.(85).

    WHY THIS MATTERS FOR STAGE 4.  Applying BBMM's regularization to Track B is
    a project inference, not a step either paper takes.  This does not justify
    that inference.  What it does rule out is one specific way the inference
    could have been self-defeating: the regularization needed for the spectral
    dimension is not quietly destroying the positive spectral weight established
    in Stage 3.  It preserves not just the sign but the value.

    Note the identity is algebraic and holds for any real a, so it is checked on
    the complex plane including the timelike cut, not only on Z > 0.
    """
    mp = pytest.importorskip("mpmath")
    mp.mp.dps = 50
    a = mp.mpf(A_B)

    def g_mp(Z):
        Z = mp.mpc(Z)
        return -Z + (Z ** 2 / 2) * mp.exp(Z / 2) * mp.e1(Z / 2)

    pts = [mp.mpc(0.5, 0.3), mp.mpc(3, -4), mp.mpc(-0.7, 0.2),
           mp.mpc(-2, -mp.mpf("1e-30")), mp.mpc(-8, -mp.mpf("1e-30")),
           mp.mpc(12, 0)]
    for Z in pts:
        g = g_mp(Z)
        greg = a * g / (a - g)
        lhs = mp.im(greg) / mp.fabs(greg) ** 2
        rhs = mp.im(g) / mp.fabs(g) ** 2
        assert float(abs(lhs - rhs)) < 1e-40
        # 1/g_reg = 1/g - 1/a, the identity the above follows from
        assert float(abs(1 / greg - (1 / g - 1 / a))) < 1e-40


def test_regularization_keeps_the_lower_bank_positive():
    """Corollary on the physical bank: since the factor is invariant and Track B
    has Im g > 0 there (Stage 3), g_reg inherits Im g_reg > 0."""
    mp = pytest.importorskip("mpmath")
    mp.mp.dps = 40
    a = mp.mpf(A_B)
    for x in [0.1, 1.0, 2.6943105, 8.0, 30.0]:
        Z = mp.mpc(-x, -mp.mpf("1e-30"))
        g = -Z + (Z ** 2 / 2) * mp.exp(Z / 2) * mp.e1(Z / 2)
        greg = a * g / (a - g)
        assert mp.im(g) > 0
        assert mp.im(greg) > 0

