import json
from pathlib import Path

import pytest

from app.engines.traditional import analyze_traditional


CASES = json.loads(
    (Path(__file__).parents[1] / "data" / "test_cases.json").read_text(
        encoding="utf-8"
    )
)


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_comparative_cases_match_traditional_expectations(case: dict) -> None:
    result = analyze_traditional(case["message"])

    assert result.category.value == case["expectedCategory"]
    assert result.priority.value == case["expectedPriority"]
