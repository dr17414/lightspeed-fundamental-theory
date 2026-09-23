"""Check authorization custody only; never run the screen or claim seeds."""

from hashlib import sha1
import json
from pathlib import Path

from analysis import stage5c_e5_screen as screen


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_AUTHORIZATION = Path(
    "docs/stage5c_e5_screen_authorization.candidate.json"
)
ATTESTATION = Path("docs/stage5c_e5_screen_attestation.json")


def _candidate():
    return json.loads((ROOT / CANDIDATE_AUTHORIZATION).read_text(encoding="utf-8"))


def test_trigger_authorization_matches_reviewed_candidate_byte_for_byte():
    assert (ROOT / screen.AUTHORIZATION).read_bytes() == (
        ROOT / CANDIDATE_AUTHORIZATION
    ).read_bytes()


def test_attested_authorization_blob_and_still_frozen_sources():
    auth = _candidate()
    attestation = json.loads((ROOT / ATTESTATION).read_text(encoding="utf-8"))
    live_content = (ROOT / screen.AUTHORIZATION).read_bytes()
    live_sha = sha1(
        b"blob " + str(len(live_content)).encode("ascii") + b"\0" + live_content
    ).hexdigest()
    assert live_sha == attestation["authorization_checks"]["authorization_blob_sha1"]
    assert set(auth) == {
        "state", "blob_shas", "sys_version", "seed_range", "resource_limits", "output_paths"
    }
    assert auth["state"] == "AUTHORIZED"
    pinned = auth["blob_shas"]
    assert set(pinned) == {screen.RUNNER, screen.PROTOCOL, *screen.FROZEN_BLOBS}
    for path in (screen.PROTOCOL, *screen.FROZEN_BLOBS):
        expected_sha = pinned[path]
        content = (ROOT / path).read_bytes()
        actual_sha = sha1(
            b"blob " + str(len(content)).encode("ascii") + b"\0" + content
        ).hexdigest()
        assert actual_sha == expected_sha, path
        if path in screen.FROZEN_BLOBS:
            assert expected_sha == screen.FROZEN_BLOBS[path], path


def test_authorization_dimensions_match_proposal_without_exec():
    auth = _candidate()
    archived = json.loads(
        (ROOT / "docs/stage5c_6a_s_replacement_plus_attestation.json").read_text("utf-8")
    )["runtime_environment"]
    assert auth["sys_version"] == archived["python"]
    assert (archived["numpy"], archived["scipy"]) == ("2.3.5", "1.17.0")
    assert auth["seed_range"] == [screen.SEED_BASE, screen.SEED_LAST]
    assert len({screen.SEED_BASE + 8 * i + 4 * t + r
                for i in range(3) for t in range(2) for r in range(4)}) == 24
    assert auth["resource_limits"] == {
        "cpu_seconds": screen.MAX_CPU_SECONDS,
        "e4_wall_seconds": screen.MAX_E4_WALL_SECONDS,
        "rss_bytes": screen.MAX_RSS_BYTES,
    }
    paths = auth["output_paths"]
    assert set(paths) == {"burn_log", "report"}
    burn, report = (Path(paths[name]) for name in ("burn_log", "report"))
    assert burn != report
    for path in (burn, report):
        assert path.is_absolute() and path.resolve() == path
        assert ROOT not in path.parents and ROOT != path
