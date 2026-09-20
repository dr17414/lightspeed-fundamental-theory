"""Pure structural checks: no test calls sprinkle_control or claims a seed."""

from contextlib import nullcontext
from fractions import Fraction
from types import SimpleNamespace

import numpy as np
import pytest

from analysis import stage5c_e5_screen as screen


@pytest.mark.parametrize(
    ("boundary", "lower", "upper"),
    [
        (Fraction(1, 160), "CLEAN-LOW", "CLEAN-MID"),
        (Fraction(1, 80), "CLEAN-MID", "CLEAN-NEAR"),
        (Fraction(1, 40), "CLEAN-NEAR", "CLEAN-OVER"),
    ],
)
def test_bands_use_exact_binary64_rationals(boundary, lower, upper):
    # Test the two representable numbers straddling each exact rational cut.
    below = float(boundary)
    if Fraction.from_float(below) >= boundary:
        below = np.nextafter(below, -np.inf)
    above = np.nextafter(below, np.inf)
    assert Fraction.from_float(float(below)) < boundary <= Fraction.from_float(float(above))
    assert screen._category(np.array((0.0, below)), clean=True) == lower
    assert screen._category(np.array((0.0, above)), clean=True) == upper
    assert screen._category(np.array((0.0, 0.0)), clean=True) == "CLEAN-LOW"


def test_exact_coord_one_division_and_nonclean_short_circuit():
    # The raw first coordinate has width 3; division before the Fraction
    # comparison would introduce a further binary64 rounding.
    error = np.array((0.075, 0.0))
    assert screen._category(error, clean=True) == "CLEAN-NEAR"
    assert screen._category(error, clean=False) == "E4-OR-ITEM3-NONCLEAN"
    assert screen._category(np.array((float("nan"), 0.0)), clean=True) == (
        "E4-OR-ITEM3-NONCLEAN"
    )


def test_selector_boundary_evaluator_coordinates_and_uniform_weights(monkeypatch):
    sample = SimpleNamespace(
        order=np.array([[False, True], [False, False]]),
        coordinates=np.array(((0.8, 0.7), (0.2, 0.1))),
        theta=0.4,
    )

    def select(name, params, case):
        assert name == "all_relations" and params == ()
        assert isinstance(case, screen.BlindedCase)
        assert set(vars(case)) == {"case_id", "order"}
        assert case.case_id == "AUDIT-ONLY"
        return np.array(((0, 1),), dtype=np.int64)

    def evaluate(atoms, weights, theta):
        assert atoms.tolist() == [[0.8, 0.7, 0.2, 0.1]]
        assert weights.tolist() == [1.0]
        assert theta == 0.4
        return SimpleNamespace(
            clean=True,
            certification=SimpleNamespace(endpoint_error=np.array((0.0, 0.0))),
        )

    monkeypatch.setattr(screen, "apply_selector", select)
    monkeypatch.setattr(screen, "evaluate_e4_wellposedness", evaluate)
    monkeypatch.setattr(screen, "_e4_deadline", nullcontext)
    assert screen._one_member(sample, "all_relations", ()) == "CLEAN-LOW"


def test_absent_committed_authorization_rejects_before_generator(monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        raise AssertionError("generator must never be touched")

    monkeypatch.setattr(screen, "sprinkle_control", forbidden)
    root = tmp_path / "repo"
    root.mkdir()
    burn, report = tmp_path / "burn.ndjson", tmp_path / "report.json"
    with pytest.raises(screen.ScreenNotAuthorized, match="authorization is absent"):
        screen.run_screen(root, burn, report)
    assert not burn.exists() and not report.exists()
