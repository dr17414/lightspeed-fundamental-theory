"""Item-7 v0.2 implementation, pending resource qualification and closeout.

The historical v0.1 module and its custody pins remain intact. Only the
combined enclosure/tolerance amendment and report semantics are changed here.
This module has no runner, generator, seed, ledger, or candidate-K entrypoint.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from math import hypot

import numpy as np
from scipy import integrate

from analysis.stage5c_continuum_pairing import (
    conformal_volume_density,
    pair_retarded_gauss_legendre,
)
from analysis.stage5c_e4_wellposedness import (
    CubatureRun,
    E4ProtocolError,
    E4Status,
    LeakageDiagnostics,
    PairingEnclosure as _V01PairingEnclosure,
    E4_CUBATURE_RTOL,
    E4_DENSITY_CHUNK_SIZE,
    E4_GAUSS_ORDER,
    E4_LEAKAGE_ID,
    E4_MAX_ATOMS,
    E4_MAX_SUBDIVISIONS,
    E4_TOPOLOGY_ID,
    _budget,
    _level_pairing_enclosure,
    _mixture_density,
    _up,
    _validated_mixture,
    _validated_theta,
    leakage_diagnostics,
)
from analysis.stage5c_numerical_certification import (
    CertificationResult,
    CertificationStatus,
    ImplementationEstimate,
    certify_pairing,
)


E4_CONTRACT_ID = "stage5c-6a-e-e4-wellposedness-v0.2"
E4_GAUSS_IMPLEMENTATION_ID = "gauss-legendre-32-with-cell-enclosure-v0.2"
E4_ADAPTIVE_IMPLEMENTATION_ID = "adaptive-genz-malik-scale-aware-with-cell-enclosure-v0.2"
E4_ENCLOSURE_ID = "positive-gaussian-characteristic-cell-enclosure-v0.2"
E4_ENCLOSURE_LEVELS = (64, 128, 256)
E4_CUBATURE_ATOL_CAP = 2.0**-30


class E4Reason(str, Enum):
    CERTIFIED = "CERTIFIED"
    STRUCTURAL_LEAKAGE_INVALID = "STRUCTURAL_LEAKAGE_INVALID"
    ADAPTIVE_TOLERANCE_UNDEFINED = "ADAPTIVE_TOLERANCE_UNDEFINED"
    NONFINITE_BACKEND = "NONFINITE_BACKEND"
    ADAPTIVE_RESOURCE_CAP = "ADAPTIVE_RESOURCE_CAP"
    NUMERICAL_CERTIFICATION_INCONCLUSIVE = "NUMERICAL_CERTIFICATION_INCONCLUSIVE"


@dataclass(frozen=True)
class PairingEnclosure(_V01PairingEnclosure):
    """The unchanged finite/ordered invariant with v0.2 level metadata."""

    levels: tuple[int, ...] = E4_ENCLOSURE_LEVELS
    enclosure_id: str = E4_ENCLOSURE_ID


@dataclass(frozen=True)
class E4Report:
    status: E4Status
    leakage: LeakageDiagnostics
    gauss: ImplementationEstimate
    enclosure: PairingEnclosure
    effective_atol: float | None
    adaptive: ImplementationEstimate | None
    adaptive_run: CubatureRun | None
    certification: CertificationResult | None
    reason: E4Reason
    topology_id: str = E4_TOPOLOGY_ID
    contract_id: str = E4_CONTRACT_ID

    def __post_init__(self) -> None:
        optional = (self.effective_atol, self.adaptive, self.adaptive_run, self.certification)
        skipped = self.reason in (
            E4Reason.STRUCTURAL_LEAKAGE_INVALID,
            E4Reason.ADAPTIVE_TOLERANCE_UNDEFINED,
        )
        if skipped:
            if self.status is not E4Status.INCONCLUSIVE or any(v is not None for v in optional):
                raise E4ProtocolError("skipped adaptive requires INCONCLUSIVE and null fields")
        elif any(v is None for v in optional):
            raise E4ProtocolError("executed adaptive requires complete report fields")

    @property
    def clean(self) -> bool:
        return bool(
            self.status is E4Status.CLEAN
            and self.leakage.structurally_admissible
            and self.certification is not None
            and self.certification.status is CertificationStatus.CLEAN
        )


def _down_binary64(value: Fraction) -> float:
    rounded = float(value)
    if Fraction.from_float(rounded) > value:
        rounded = float(np.nextafter(rounded, 0.0))
    return rounded


def effective_atol(enclosure: PairingEnclosure) -> float | None:
    """Derive the exact-dyadic, downward-rounded row tolerance; no fallback."""

    scale = float(np.max(enclosure.upper))
    if not np.isfinite(scale) or scale < 0.0:
        raise E4ProtocolError("pairing enclosure must be finite and non-negative")
    exact = Fraction.from_float(scale) * Fraction.from_float(E4_CUBATURE_RTOL)
    result = min(E4_CUBATURE_ATOL_CAP, _down_binary64(exact))
    return result if result > 0.0 else None


def pairing_enclosure(
    pair_coordinates: np.ndarray, probability_weights: np.ndarray, theta: float
) -> PairingEnclosure:
    theta = _validated_theta(theta)
    atoms, weights = _validated_mixture(pair_coordinates, probability_weights)
    bounds = [
        _level_pairing_enclosure(atoms, weights, theta, level)
        for level in E4_ENCLOSURE_LEVELS
    ]
    lower = np.stack([item[0] for item in bounds])
    upper = np.stack([item[1] for item in bounds])
    return PairingEnclosure(
        lower=np.max(lower, axis=0),
        upper=np.min(upper, axis=0),
        level_lower=lower,
        level_upper=upper,
        levels=E4_ENCLOSURE_LEVELS,
        enclosure_id=E4_ENCLOSURE_ID,
    )


def evaluate_e4_wellposedness(
    pair_coordinates: np.ndarray, probability_weights: np.ndarray, theta: float
) -> E4Report:
    """Evaluate only the reviewed combined v0.2 candidate, with no tunables."""

    theta = _validated_theta(theta)
    atoms, weights = _validated_mixture(pair_coordinates, probability_weights)
    leakage = leakage_diagnostics(atoms, weights)
    fixed = pair_retarded_gauss_legendre(_mixture_density(atoms, weights), theta, order=E4_GAUSS_ORDER)
    enclosure = pairing_enclosure(atoms, weights, theta)
    gauss = ImplementationEstimate(
        fixed.matrix, _budget(enclosure.error_for(fixed.matrix)), E4_GAUSS_IMPLEMENTATION_ID
    )
    common = dict(leakage=leakage, gauss=gauss, enclosure=enclosure)
    skipped = dict(effective_atol=None, adaptive=None, adaptive_run=None, certification=None)
    if not leakage.structurally_admissible:
        return E4Report(
            status=E4Status.INCONCLUSIVE, reason=E4Reason.STRUCTURAL_LEAKAGE_INVALID,
            **common, **skipped,
        )
    atol = effective_atol(enclosure)
    if atol is None:
        return E4Report(
            status=E4Status.INCONCLUSIVE, reason=E4Reason.ADAPTIVE_TOLERANCE_UNDEFINED,
            **common, **skipped,
        )
    gm = _cubature_pairing(atoms, weights, theta, "genz-malik", atol=atol)
    finite_matrix = bool(np.all(np.isfinite(gm.matrix)))
    finite_output = finite_matrix and bool(np.isfinite(gm.error))
    adaptive = ImplementationEstimate(
        gm.matrix, _budget(enclosure.error_for(gm.matrix) if finite_matrix else 0.0),
        E4_ADAPTIVE_IMPLEMENTATION_ID,
    )
    certification = certify_pairing(gauss, adaptive)
    if not finite_output:
        reason = E4Reason.NONFINITE_BACKEND
    elif not gm.converged:
        reason = E4Reason.ADAPTIVE_RESOURCE_CAP
    elif certification.status is not CertificationStatus.CLEAN:
        reason = E4Reason.NUMERICAL_CERTIFICATION_INCONCLUSIVE
    else:
        reason = E4Reason.CERTIFIED
    return E4Report(
        status=E4Status.CLEAN if reason is E4Reason.CERTIFIED else E4Status.INCONCLUSIVE,
        reason=reason, effective_atol=atol, adaptive=adaptive, adaptive_run=gm,
        certification=certification, **common,
    )
def _cubature_pairing(
    atoms: np.ndarray, weights: np.ndarray, theta: float, rule: str, *, atol: float
) -> CubatureRun:
    """Integrate both characteristic sectors in one rule-specific traversal."""

    density = _mixture_density(atoms, weights)

    def integrand(cube_points: np.ndarray) -> np.ndarray:
        cube_points = np.asarray(cube_points, dtype=float)
        a, s, transverse = cube_points.T
        right_points = np.stack((a, transverse, a * s, transverse), axis=-1)
        left_points = np.stack((transverse, a, transverse, a * s), axis=-1)

        def entry(points: np.ndarray) -> np.ndarray:
            px = conformal_volume_density(points[:, 0], points[:, 1], theta)
            py = conformal_volume_density(points[:, 2], points[:, 3], theta)
            biweight = np.asarray(px * py, dtype=float) ** -0.25
            return a * biweight * density(points)

        right = entry(right_points)
        left = entry(left_points)
        zeros = np.zeros_like(right)
        return np.stack((right, zeros, left, zeros), axis=-1)

    result = integrate.cubature(
        integrand,
        np.zeros(3),
        np.ones(3),
        rule=rule,
        atol=atol,
        rtol=E4_CUBATURE_RTOL,
        max_subdivisions=E4_MAX_SUBDIVISIONS,
    )
    estimate = np.asarray(result.estimate, dtype=float)
    errors = np.abs(np.asarray(result.error, dtype=float))
    if estimate.shape != (4,) or errors.shape != (4,):
        raise RuntimeError(f"E4 {rule} cubature returned an invalid live error record")
    matrix = np.diag(
        [complex(estimate[0], estimate[1]), complex(estimate[2], estimate[3])]
    )
    return CubatureRun(
        matrix=matrix,
        error=(
            np.inf
            if not np.all(np.isfinite(errors))
            else _up(hypot(*(float(value) for value in errors)))
        ),
        rule=rule,
        subdivisions=int(result.subdivisions),
        solver_status=str(result.status),
    )

