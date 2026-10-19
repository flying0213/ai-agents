"""独立的公开证据：不要求特定随机库，不断言随机误差单调下降。"""

import csv
import math
from pathlib import Path
import subprocess
import sys

import pytest

import experiment


DEFAULT_SIZES = (1000, 10000, 100000)
FIELDS = (
    "seed", "n", "crossings", "pi_estimate", "needle_length", "line_spacing"
)


@pytest.mark.parametrize(
    ("distance", "angle", "expected"),
    [
        (0.4, math.pi / 2, False),  # 针的一半长为 0.25，够不到线。
        (0.1, math.pi / 2, True),
        (0.25, math.pi / 2, True),  # 针尖恰好触线，也算相交。
        (0.1, 0.0, False),         # 与线平行，中心又不在线上。
        (0.0, 0.0, True),          # 在线上的平行针。
    ],
)
def test_crossing_known_positions(distance, angle, expected):
    assert experiment.crosses_line(distance, angle) is expected


def test_equal_length_and_spacing_is_allowed():
    assert experiment.crosses_line(0.5, math.pi / 2, length=1.0, spacing=1.0)


def test_estimator_has_a_hand_calculable_answer():
    # N=100，K=32，L=0.5，d=1；手算结果为 100/32。
    assert experiment.estimate_pi(100, 32) == pytest.approx(3.125)
    # 同样的相交数，针长变化后结果也要随公式变化。
    assert experiment.estimate_pi(100, 32, length=1.0) == pytest.approx(6.25)


@pytest.mark.parametrize(
    ("distance", "angle", "length", "spacing"),
    [(-0.01, 0.0, 0.5, 1.0), (0.51, 0.0, 0.5, 1.0),
     (0.1, -0.1, 0.5, 1.0), (0.1, math.pi, 0.5, 1.0),
     (0.1, 0.0, 0.0, 1.0), (0.1, 0.0, 1.1, 1.0),
     (0.0, 0.0, 0.5, 0.0)],
)
def test_invalid_geometry_is_not_silently_corrected(distance, angle, length, spacing):
    with pytest.raises(ValueError):
        experiment.crosses_line(distance, angle, length=length, spacing=spacing)


@pytest.mark.parametrize(("n", "crossings"), [(0, 0), (100, 0), (100, -1), (100, 101)])
def test_invalid_estimate_is_not_reported_as_a_number(n, crossings):
    with pytest.raises(ValueError):
        experiment.estimate_pi(n, crossings)


def test_same_seed_and_parameters_reproduce_the_run():
    first = experiment.simulate(1000, seed=42)
    second = experiment.simulate(1000, seed=42)
    assert first == second
    assert first["seed"] == 42
    assert first["n"] == 1000
    assert first["needle_length"] == pytest.approx(0.5)
    assert first["line_spacing"] == pytest.approx(1.0)
    assert isinstance(first["crossings"], int)
    assert 0 < first["crossings"] <= 1000
    expected = 2 * first["needle_length"] * first["n"] / (
        first["line_spacing"] * first["crossings"]
    )
    assert first["pi_estimate"] == pytest.approx(expected)


def test_default_csv_matches_the_actual_simulations(tmp_path):
    # 在临时目录运行，不覆盖你项目中的真实 results.csv。
    project_dir = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, str(project_dir / "experiment.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    with (tmp_path / "results.csv").open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == list(FIELDS)
        rows = list(reader)
    # 保留初始三组，维护时可以新增更大的 N、换入口 seed。
    assert set(DEFAULT_SIZES) <= {int(row["n"]) for row in rows}
    for row in rows:
        n = int(row["n"])
        seed = int(row["seed"])
        length = float(row["needle_length"])
        spacing = float(row["line_spacing"])
        result = experiment.simulate(n, seed=seed, length=length, spacing=spacing)
        assert seed == result["seed"]
        assert n == result["n"]
        assert int(row["crossings"]) == result["crossings"]
        assert float(row["needle_length"]) == pytest.approx(result["needle_length"])
        assert float(row["line_spacing"]) == pytest.approx(result["line_spacing"])
        estimate = 2 * length * n / (spacing * int(row["crossings"]))
        assert float(row["pi_estimate"]) == pytest.approx(estimate)
        assert float(row["pi_estimate"]) == pytest.approx(result["pi_estimate"])
