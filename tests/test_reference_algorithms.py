import subprocess
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def reference_programs(tmp_path_factory):
    build_dir = tmp_path_factory.mktemp("reference-programs")
    programs = {}
    for name in ("spancount", "rootcount"):
        source = PROJECT_ROOT / "algorithm" / name / "program" / f"{name}.cpp"
        executable = build_dir / name
        subprocess.run(
            ["g++", "-std=c++11", "-O2", str(source), "-o", str(executable)],
            check=True,
        )
        programs[name] = executable
    return programs


def run_program(executable, input_data):
    completed = subprocess.run(
        [str(executable)],
        input=input_data,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (
            "4 5 2 2\n1 2\n2 3\n2 4\n3 2\n4 3\n",
            "5 3 2",
        ),
        (
            "5 8 6 3\n3 4\n1 4\n3 5\n1 3\n2 5\n2 4\n1 2\n1 5\n",
            "45 21 24",
        ),
    ],
)
def test_spanning_tree_counts_are_exact(reference_programs, input_data, expected):
    assert run_program(reference_programs["spancount"], input_data) == expected


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (
            "5 12 1 8 11\n"
            "1 2\n1 4\n1 5\n2 3\n2 4\n2 5\n"
            "3 1\n3 5\n4 1\n4 2\n4 3\n5 2\n",
            "23 16 12",
        ),
        (
            "2 2 1 2 2\n1 2\n2 1\n",
            "1 1 0",
        ),
    ],
)
def test_rooted_tree_counts_are_exact(reference_programs, input_data, expected):
    assert run_program(reference_programs["rootcount"], input_data) == expected
