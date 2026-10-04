"""Unit tests for tri9cog core (no external files)."""

import pytest

from tri9cog.annotate import validate_coordinate, to_digits, from_digits, make_template
from tri9cog.fingerprint import encode, decode, fingerprint, entropy
from tri9cog.replicate import build_blueprint, verify_story


class TestEncodeDecode:
    def test_known_code_red_chamber_ch1(self):
        # Chapter 1 of Dream of the Red Chamber
        assert encode("221-221-220") == 18924

    def test_min_code(self):
        assert encode("000-000-000") == 0

    def test_max_code(self):
        assert encode("222-222-222") == 19682

    def test_roundtrip(self):
        for c in (0, 987, 1484, 12392, 18952, 19682):
            assert encode(decode(c)) == c

    def test_range(self):
        with pytest.raises(ValueError):
            decode(19683)


class TestCoordinate:
    def test_validate_dashed(self):
        assert validate_coordinate("020-112-201")

    def test_validate_flat(self):
        assert validate_coordinate("020112201")

    def test_invalid(self):
        assert not validate_coordinate("221-221-2200")
        assert not validate_coordinate("221-221-22")
        assert not validate_coordinate("321-000-000")

    def test_digits_roundtrip(self):
        assert from_digits(to_digits("020-112-201")) == "020-112-201"


class TestEntropy:
    def test_uniform_three_states(self):
        # log2(3) = 1.585
        assert abs(entropy([1, 1, 1]) - 1.58496) < 1e-4

    def test_single_state(self):
        assert entropy([5, 0, 0]) == 0.0


class TestFingerprint:
    def _rows(self):
        # 5 hand-made nodes; includes a known mirror pair
        return [
            {"node": "n1", "coordinate": "221-221-220", "title": ""},
            {"node": "n2", "coordinate": "000-000-000", "title": ""},
            {"node": "n3", "coordinate": "222-222-222", "title": ""},
            {"node": "n4", "coordinate": "000-000-000", "title": ""},
            {"node": "n5", "coordinate": "121-222-222", "title": ""},
        ]

    def test_node_count_and_codes(self):
        fp = fingerprint(self._rows(), top_turns=5)
        assert fp["nodes"] == 5
        assert fp["unique_codes"] == 4
        assert fp["code_range"] == [0, 19682]

    def test_entropy_bounds(self):
        fp = fingerprint(self._rows(), top_turns=5)
        assert 0.0 <= fp["entropy_total"] <= 1.585

    def test_turning_points_sorted(self):
        fp = fingerprint(self._rows(), top_turns=5)
        vals = [t["dims_changed"] for t in fp["turning_points"]]
        assert vals == sorted(vals, reverse=True)
        # n1->n2 changes all 9? 221-221-220 vs 000-000-000 -> 8 dims differ (3rd char same 0)
        assert fp["turning_points"][0]["dims_changed"] in (8, 9)


class TestReplicate:
    def _fp(self):
        rows = [
            {"node": "n1", "coordinate": "000-000-000", "title": ""},
            {"node": "n2", "coordinate": "000-000-000", "title": ""},
            {"node": "n3", "coordinate": "221-221-220", "title": ""},
        ]
        return fingerprint(rows, top_turns=0)

    def test_isomorphic_preserves_path(self):
        fp = self._fp()
        blue = build_blueprint(fp, strategy="isomorphic", seed=1)
        assert [b["coordinate"] for b in blue] == ["000-000-000", "000-000-000", "221-221-220"]

    def test_mirror_flips(self):
        fp = self._fp()
        blue = build_blueprint(fp, strategy="mirror", seed=1)
        assert blue[0]["coordinate"] == "222-222-222"
        assert blue[2]["coordinate"] == "001-001-002"

    def test_verify_perfect_match(self):
        fp = self._fp()
        blue = build_blueprint(fp, strategy="isomorphic", seed=1)
        rows = [{"node": b["node"], "coordinate": b["coordinate"], "title": ""} for b in blue]
        report = verify_story(rows, blue)
        assert report["matched"] == len(rows)
        assert report["mean_hamming"] == 0.0

    def test_verify_mismatch_detected(self):
        fp = self._fp()
        blue = build_blueprint(fp, strategy="isomorphic", seed=1)
        rows = [{"node": b["node"], "coordinate": "111-111-111", "title": ""} for b in blue]
        report = verify_story(rows, blue)
        assert report["matched"] == 0
        assert report["mean_hamming"] > 0