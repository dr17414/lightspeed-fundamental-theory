"""Frozen development inputs/method checks; no timing, RNG, screen, or K."""
from __future__ import annotations

import base64
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/stage5c_e4_v02_resource_characterization.json"
GRID = (0.9, 1.0, 1.1, 1.25)
MAXITER = 10000
RANK_RTOL = 2.0 ** -40
REFERENCE_RTOL = 1e-8
REFERENCE_ATOL = 1e-10
MODEL_RESIDUAL_LIMIT = 0.10
STRATA = {
    "total_order": ("chain",),
    "layered": ("two_layers", "four_layers", *(f"interval_bridge_{i}" for i in range(1, 5))),
    "dispersed": ("bit_reversal", "modular_5", "modular_17", "modular_31"),
}


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def array_bytes(array, dtype):
    import numpy as np
    return np.asarray(array, dtype=dtype, order="C").tobytes(order="C")


def array_hash(array, dtype):
    return sha256(array_bytes(array, dtype)).hexdigest()


def build_fixtures():
    """Select by counts/lexical ties before any new production cost observation."""
    import numpy as np
    from benchmarks.stage5c_e4_v02_resource_characterization import geometry_fixtures
    from analysis.stage5c_hard_controls import BlindedCase, order_from_uv
    from analysis.stage5c_selector_family import apply_selector, evaluation_order
    from analysis.stage5c_e5_screen import build_production_atoms
    inventory = json.loads(EVIDENCE.read_text())["selector_count_rows"]
    members = list(evaluation_order())
    coordinates, selected = {}, {}
    for n in (64, 96, 128):
        geometries = geometry_fixtures(n)
        for name in sorted(geometries):
            data = array_bytes(geometries[name], "<f8")
            coordinates[f"{n}:{name}"] = {
                "shape": [n, 2], "dtype": "<f8", "order": "C",
                "base64": base64.b64encode(data).decode(), "sha256": sha256(data).hexdigest(),
            }
        for name, parameters in members:
            rows = [r for r in inventory if r["N"] == n and r["selector"] == name
                    and r["parameters"] == list(parameters) and r["category"] == "SELECTED"]
            winner = min(rows, key=lambda r: (-r["selected_pairs"], r["fixture"]))
            key = (n, winner["fixture"], name, tuple(parameters))
            selected.setdefault(key, []).append("max_count_per_member")
        for stratum, names in STRATA.items():
            rows = [r for r in inventory if r["N"] == n and r["selector"] == "all_relations"
                    and r["fixture"] in names and r["category"] == "SELECTED"]
            winner = min(rows, key=lambda r: (-r["selected_pairs"], r["fixture"]))
            key = (n, winner["fixture"], "all_relations", ())
            selected.setdefault(key, []).append("stratum:" + stratum)
    cases = []
    member_index = {item: i for i, item in enumerate(members)}
    for n, fixture, name, parameters in sorted(selected, key=lambda x: (x[0], x[1], member_index[(x[2], x[3])])):
        payload = coordinates[f"{n}:{fixture}"]
        uv = np.frombuffer(base64.b64decode(payload["base64"]), dtype="<f8").reshape(n, 2)
        order = order_from_uv(uv)
        pairs = apply_selector(name, parameters, BlindedCase("RESOURCE-FIXTURE-ONLY", order))
        atoms, weights = build_production_atoms(SimpleNamespace(coordinates=uv), pairs)
        cases.append({"N": n, "fixture": fixture, "selector": name, "parameters": list(parameters),
                      "selection_reasons": selected[(n, fixture, name, parameters)],
                      "coordinate_key": f"{n}:{fixture}", "selected_count": len(pairs),
                      "pairs_sha256_le_i8": array_hash(pairs, "<i8"),
                      "atoms_sha256_le_f8": array_hash(atoms, "<f8"),
                      "weights_sha256_le_f8": array_hash(weights, "<f8")})
    return {"state": "FIXED-DEVELOPMENT-INPUTS", "coordinates": coordinates, "cases": cases,
            "stress": {"base_atoms_hex": [[float(x).hex() for x in row] for row in
                         ((.72, .81, .31, .22), (.61, .58, .24, .19), (.43, .67, .11, .37))],
                       "theta_hex": (.4).hex(), "recipe": "base[np.arange(a)%3], production uniform weights"}}


def load_case(fixtures, index):
    import numpy as np
    from analysis.stage5c_hard_controls import BlindedCase, order_from_uv
    from analysis.stage5c_selector_family import apply_selector
    from analysis.stage5c_e5_screen import build_production_atoms
    case = fixtures["cases"][index]
    data = fixtures["coordinates"][case["coordinate_key"]]
    raw = base64.b64decode(data["base64"], validate=True)
    if sha256(raw).hexdigest() != data["sha256"]:
        raise ValueError("coordinate bytes changed")
    uv = np.frombuffer(raw, dtype="<f8").reshape(data["shape"])
    pairs = apply_selector(case["selector"], tuple(case["parameters"]),
                           BlindedCase("RESOURCE-FIXTURE-ONLY", order_from_uv(uv)))
    atoms, weights = build_production_atoms(SimpleNamespace(coordinates=uv), pairs)
    for value, dtype, key in ((pairs, "<i8", "pairs_sha256_le_i8"),
                              (atoms, "<f8", "atoms_sha256_le_f8"),
                              (weights, "<f8", "weights_sha256_le_f8")):
        if array_hash(value, dtype) != case[key]:
            raise ValueError("selector/adapter bytes changed")
    return atoms, weights


def fit_nnls(design, observations):
    import numpy as np
    from scipy.optimize import nnls
    a, y = np.asarray(design, dtype=np.float64), np.asarray(observations, dtype=np.float64)
    singular = np.linalg.svd(a, compute_uv=False)
    if len(singular) < a.shape[1] or singular[-1] <= RANK_RTOL * singular[0]:
        raise ValueError("NOT-IDENTIFIED")
    # SciPy 1.17's atol is unused; omit it, never claim it sets solver accuracy.
    coefficient, norm = nnls(a, y, maxiter=MAXITER)
    predicted = a @ coefficient
    return {"coefficients_hex": [float(x).hex() for x in coefficient],
            "active_positive": [bool(x > 0) for x in coefficient],
            "prediction_hex": [float(x).hex() for x in predicted],
            "residual_hex": [float(x).hex() for x in y - predicted],
            "rnorm_hex": float(norm).hex(), "rank": a.shape[1],
            "residual_df": len(y) - a.shape[1]}


def method_reference():
    """Only fit the ten already public rows; never consume held-out records."""
    import numpy as np
    import scipy
    import scipy.optimize._nnls as module
    if np.__version__ != "2.3.5" or scipy.__version__ != "1.17.0":
        raise ValueError("numerical version pin mismatch")
    evidence = json.loads(EVIDENCE.read_text())
    stress = [r for r in evidence["probes"] if r["stage"] == "adaptive_stress"]
    enclosure = [r for r in evidence["probes"] if r["stage"] == "enclosure"]
    if len(stress) != 7 or any(r["outcome"] != "FORCED-BUDGET-EXHAUSTED" for r in stress):
        raise ValueError("training rows changed")
    a = np.array([r["atoms"] for r in stress], dtype=np.float64)
    s = np.array([r["subdivision_budget"] for r in stress], dtype=np.float64)
    e = np.array([r["atoms"] for r in enclosure], dtype=np.float64)
    output = {"state": "METHOD-VERIFICATION-TRAINING-ONLY", "new_measurements": 0,
              "numpy": np.__version__, "scipy": scipy.__version__,
              "nnls_wrapper_sha256": sha256(Path(module.__file__).read_bytes()).hexdigest(),
              "stress_training_order": [[int(x), int(y)] for x, y in zip(a, s)],
              "enclosure_training_order": [int(x) for x in e], "fits": {}}
    for clock in ("cpu_seconds", "wall_seconds"):
        y = [r[clock] for r in stress]
        designs = {"stress_affine": np.column_stack((np.ones(7), a/8192, s/4096, a*s/(8192*4096)))}
        for p in GRID:
            for q in GRID:
                designs[f"stress_power_p{p}_q{q}"] = np.column_stack((np.ones(7), (a/8192)**p*(s/4096)**q))
        for name, design in designs.items():
            output["fits"][f"{clock}:{name}"] = fit_nnls(design, y)
        y = [r[clock] for r in enclosure]
        designs = {"enclosure_affine": np.column_stack((np.ones(3), e/8192))}
        designs.update({f"enclosure_power_p{p}": np.column_stack((np.ones(3), (e/8192)**p)) for p in GRID})
        for name, design in designs.items():
            output["fits"][f"{clock}:{name}"] = fit_nnls(design, y)
    return output


def verify_reference(actual, expected):
    import numpy as np
    for key in ("numpy", "scipy", "nnls_wrapper_sha256", "stress_training_order", "enclosure_training_order"):
        if actual[key] != expected[key]:
            raise ValueError("method identity drift: " + key)
    if actual["fits"].keys() != expected["fits"].keys():
        raise ValueError("model set changed")
    for name, fit in actual["fits"].items():
        ref = expected["fits"][name]
        if fit["active_positive"] != ref["active_positive"] or fit["rank"] != ref["rank"]:
            raise ValueError("active-set/rank drift: " + name)
        for key in ("coefficients_hex", "prediction_hex", "residual_hex", "rnorm_hex"):
            x, y = fit[key], ref[key]
            x = [x] if isinstance(x, str) else x
            y = [y] if isinstance(y, str) else y
            if not np.allclose([float.fromhex(v) for v in x], [float.fromhex(v) for v in y],
                               rtol=REFERENCE_RTOL, atol=REFERENCE_ATOL):
                raise ValueError("numerical reference drift: " + name)


def residual_verdict(observed, prediction, *, censored=False):
    """A fixed 10% two-sided rule; never silently omit censored input."""
    if not (observed >= 0 and prediction >= 0):
        return "INSUFFICIENT-EVIDENCE"
    excess = observed - prediction
    threshold = MODEL_RESIDUAL_LIMIT * max(1.0, observed)
    if censored:
        return "MODEL-INVALID" if excess > threshold else "INSUFFICIENT-EVIDENCE"
    return "MODEL-INVALID" if abs(excess) > threshold else "POINTWISE-MODEL-CHECK-PASS"


def predict_stress(reference, clock, model, a, s):
    import numpy as np
    x = np.array([float.fromhex(v) for v in reference["fits"][f"{clock}:{model}"]["coefficients_hex"]])
    if model == "stress_affine":
        row = np.array([1., a/8192, s/4096, a*s/(8192*4096)])
    else:
        suffix = model.removeprefix("stress_power_p").split("_q")
        p, q = map(float, suffix)
        row = np.array([1., (a/8192)**p*(s/4096)**q])
    return float(row @ x)


def model_agreement_possible(reference, clock, a, s):
    """Check existence of any nonnegative observation passing every frozen model.

    Below 1 second the rule is absolute +/-0.1; above it is relative +/-10%.
    This uses training coefficients only; no new timing or prediction artifact.
    """
    predictions = [predict_stress(reference, clock, k.split(":", 1)[1], a, s)
                   for k in reference["fits"] if k.startswith(clock+":stress_")]
    low_absolute = max([0.] + [p - MODEL_RESIDUAL_LIMIT for p in predictions])
    high_absolute = min([1.] + [p + MODEL_RESIDUAL_LIMIT for p in predictions])
    low_relative = max([1.] + [p/(1+MODEL_RESIDUAL_LIMIT) for p in predictions])
    high_relative = min(p/(1-MODEL_RESIDUAL_LIMIT) for p in predictions)
    return low_absolute <= high_absolute or low_relative <= high_relative


def build_plan(fixtures):
    jobs = [{"id": "direct-8128-4096", "kind": "stress", "atoms": 8128, "s": 4096,
             "wall_cap": 4500, "cpu_cap": 5000, "role": "held_out_cell"}]
    for i in range(len(fixtures["cases"])):
        for theta in (-.4, .4):
            jobs.append({"id": f"reach-{i:02d}-{theta:+.1f}", "kind": "production",
                         "case_index": i, "theta_hex": theta.hex(), "wall_cap": 1020,
                         "e4_wall_cap": 900, "setup_allowance": 120,
                         "cpu_cap": 1100, "role": "reachability_only_not_model_validation"})
    for s in (128, 256, 512, 1024):
        for repetition in range(4096//s):
            jobs.append({"id": f"cycle-s{s}-{repetition:02d}", "kind": "stress", "atoms": 8128,
                         "s": s, "wall_cap": 900, "cpu_cap": 1000,
                         "role": "held_out_cell" if s in (128, 1024) else "seen_cell_repeat"})
    return jobs


def assess_held_out(manifest, reference, records):
    """Retain every planned held-out row; never refit or select a winning subset."""
    latest = {r["job_id"]: r for r in records if "job_id" in r}
    result = {}
    jobs = [j for j in manifest["jobs"] if j["role"] == "held_out_cell"]
    for clock, field in (("cpu_seconds", "phase_cpu_seconds"), ("wall_seconds", "phase_wall_seconds")):
        names = [key.split(":", 1)[1] for key in reference["fits"]
                 if key.startswith(clock+":stress_")]
        for name in names:
            rows = []
            for job in jobs:
                record = latest.get(job["id"], {})
                prediction = predict_stress(reference, clock, name, job["atoms"], job["s"])
                observed = record.get(field)
                bound = record.get(field.removesuffix("_seconds") + "_lower_bound_seconds")
                censored = record.get("outcome") in ("WALL-CAP-CENSORED", "CPU-CAP-CENSORED")
                if censored and bound is not None:
                    verdict = residual_verdict(bound, prediction, censored=True)
                elif record.get("outcome") != "FORCED-BUDGET-EXHAUSTED" or observed is None:
                    verdict = "INSUFFICIENT-EVIDENCE"
                else:
                    verdict = residual_verdict(observed, prediction)
                rows.append({"job_id": job["id"], "prediction": prediction, "observed": observed,
                             "censored_lower_bound": bound if censored else None,
                             "outcome": record.get("outcome", "NOT-RUN"), "verdict": verdict})
            verdicts = {r["verdict"] for r in rows}
            summary = ("MODEL-INVALID" if "MODEL-INVALID" in verdicts else
                       "INSUFFICIENT-EVIDENCE" if "INSUFFICIENT-EVIDENCE" in verdicts else
                       "POINTWISE-MODEL-CHECK-PASS")
            result[clock+":"+name] = {"verdict": summary, "rows": rows}
    return {"model_set_verdict": "POINTWISE-ONLY-NO-DOMAIN-BOUND" if all(
                r["verdict"] == "POINTWISE-MODEL-CHECK-PASS" for r in result.values())
            else "INSUFFICIENT-EVIDENCE", "models": result,
            "primary_model": "stress_affine",
            "scenario_models": "all 16 power forms; no post-result model selection",
            "wall_comparability": "CROSS-PROFILE-DIAGNOSTIC-ONLY; orchestration differs from training",
            "all_models_agreement_possible": {clock: [model_agreement_possible(reference, clock, 8128, s)
                for s in (4096, 128, 1024)] for clock in ("cpu_seconds", "wall_seconds")},
            "new_count_or_mixture_domain_validation": False, "qualification": False}
