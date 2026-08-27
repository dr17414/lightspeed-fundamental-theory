"""Machinery tests for the frozen D.1 item 3 reference probe.

These cover reproducibility and the pre-registered definitions.  They do not
re-run the sealed witness revelation, which is a one-shot source-of-record.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.stage5c_hard_controls import (  # noqa: E402
    BlindedCase,
    CONTROL_THETA,
    baseline_features,
    sprinkle_control,
)
from analysis.stage5c_reference_probe import (  # noqa: E402
    BANK_EIGENVALUES,
    EQUIVALENCE_MARGIN,
    NULL_BASE,
    POOL_SIZE,
    PQ_BASE,
    adjudicate,
    claim_stream,
    fit_probe,
    holm,
    oracle_contrast,
    order_feature_bank,
    paired_signflip,
    segment_seeds,
    tost_equivalence,
)


def test_bank_has_the_frozen_dimension_and_is_deterministic():
    sample = sprinkle_control(48, CONTROL_THETA, 400_000_001)
    case = BlindedCase("test", sample.order.copy())
    first = order_feature_bank(case)
    assert first.shape == (43,)
    assert np.all(np.isfinite(first))
    assert np.array_equal(first, order_feature_bank(case))


def test_bank_is_label_invariant():
    sample = sprinkle_control(48, CONTROL_THETA, 400_000_002)
    rng = np.random.default_rng(11)
    perm = rng.permutation(48)
    relabelled = sample.order[np.ix_(perm, perm)]
    assert np.allclose(
        order_feature_bank(BlindedCase("a", sample.order.copy())),
        order_feature_bank(BlindedCase("b", relabelled)),
        atol=1e-9,
    )


def test_bank_eigenvalues_are_sorted_descending():
    sample = sprinkle_control(48, CONTROL_THETA, 400_000_003)
    tail = order_feature_bank(BlindedCase("test", sample.order.copy()))[-BANK_EIGENVALUES:]
    assert np.all(np.diff(tail) <= 1e-12)


def test_segment_seed_reservation_matches_the_pre_registration():
    assert segment_seeds(PQ_BASE, 0, 0)[0] == 1_100_000_000
    assert segment_seeds(PQ_BASE, 5, 3)[0] == 1_153_000_000
    assert segment_seeds(NULL_BASE, 0, 0)[0] == 1_200_000_000
    assert len(segment_seeds(PQ_BASE, 2, 1)) == POOL_SIZE
    seen = {
        segment_seeds(base, b, j)[0]
        for base in (PQ_BASE, NULL_BASE)
        for b in range(6)
        for j in range(4)
    }
    assert len(seen) == 48


def test_claim_streams_are_frozen_and_distinct():
    first = claim_stream("Q").random(4)
    assert np.array_equal(first, claim_stream("Q").random(4))
    assert not np.array_equal(first, claim_stream("P").random(4))


def test_oracle_contrast_detects_a_planted_density_ratio():
    dense = np.column_stack(
        [np.full(64, 0.05), np.full(64, 0.05)]
    )  # all mass at s, none at t
    assert oracle_contrast(dense) > 0.0
    sparse = np.column_stack([np.full(64, 0.50), np.full(64, 0.05)])
    assert oracle_contrast(sparse) < 0.0


def test_frozen_probe_does_not_refit_on_new_data():
    rng = np.random.default_rng(5)
    bank = rng.normal(size=(60, 43))
    base = rng.normal(size=(60, 11))
    labels = np.where(np.arange(60) < 30, 1.0, -1.0)
    probe = fit_probe(bank, base, labels)
    other_bank = rng.normal(size=(20, 43))
    other_base = rng.normal(size=(20, 11))
    first = probe.score(other_bank, other_base)
    assert np.array_equal(first, probe.score(other_bank, other_base))


def test_fit_probe_rejects_zero_variance_column():
    rng = np.random.default_rng(6)
    bank = rng.normal(size=(40, 43))
    bank[:, 7] = 0.0
    base = np.zeros((40, 11))
    labels = np.where(np.arange(40) < 20, 1.0, -1.0)
    with pytest.raises(ValueError):
        fit_probe(bank, base, labels)


def test_paired_signflip_is_null_on_symmetric_data():
    rng = np.random.default_rng(3)
    deltas = rng.normal(size=800)
    _, _, p = paired_signflip(deltas, "Q")
    assert p > 0.01


def test_tost_declares_equivalence_only_when_effect_is_small():
    tight = np.full(1000, 0.0) + np.random.default_rng(4).normal(scale=1.0, size=1000)
    effect, p = tost_equivalence(tight)
    assert abs(effect) < EQUIVALENCE_MARGIN
    assert p < 0.01
    shifted = tight + 0.6
    _, p_shifted = tost_equivalence(shifted)
    assert p_shifted > 0.01


def test_holm_controls_the_family_and_is_monotone():
    verdict = holm({"a": 0.0001, "b": 0.002, "c": 0.004, "d": 0.5})
    assert verdict["a"] and verdict["b"] and verdict["c"]
    assert not verdict["d"]
    assert not holm({"a": 0.004, "b": 0.004, "c": 0.004, "d": 0.004})["a"]


def test_baseline_and_bank_are_disjoint_in_interval_orders():
    sample = sprinkle_control(48, CONTROL_THETA, 400_000_004)
    assert baseline_features(sample.order).shape == (11,)
    assert order_feature_bank(BlindedCase("test", sample.order.copy())).shape == (43,)


def test_feature_bank_rejects_non_blinded_payloads():
    sample = sprinkle_control(24, CONTROL_THETA, 400_000_005)
    with pytest.raises((AttributeError, TypeError, ValueError)):
        order_feature_bank(sample.order)  # type: ignore[arg-type]


def _synthetic_results() -> dict:
    claims = {
        name: {
            "n": 1000,
            "observed": 0.5,
            "effect": 0.8,
            "holm_significant": True,
        }
        for name in ("layer1", "P", "Q")
    }
    claims["N"] = {"n": 1000, "effect": 0.0, "holm_significant": True}
    claims["blocks"] = {"b": {"gate_ok": True}}
    return claims


def test_adjudicator_enforces_every_verdict_branch():
    passing = _synthetic_results()
    assert adjudicate(passing) == "CONTROL-VIABLE"

    weak_q = _synthetic_results()
    weak_q["Q"]["effect"] = 0.29
    assert adjudicate(weak_q) == "CONTROL-UNFAIR-RISK"

    dead = _synthetic_results()
    dead["layer1"]["effect"] = 0.29
    assert adjudicate(dead) == "CONTROL-DEAD"

    bad_instrument = _synthetic_results()
    bad_instrument["P"]["effect"] = 0.29
    assert adjudicate(bad_instrument) == "INCONCLUSIVE"

    underpowered_null = _synthetic_results()
    underpowered_null["N"]["n"] = 899
    assert adjudicate(underpowered_null) == "INCONCLUSIVE"
