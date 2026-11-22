from __future__ import annotations

import csv
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from app.bootstrap import build_analyzer
from app.domain.models import AnalysisMode, AnalyzeRequest


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data" / "test_cases.json"
RESULTS_DIR = ROOT / "results"


def main() -> None:
    if not os.getenv("GEMINI_API_KEY"):
        raise SystemExit(
            "Configura GEMINI_API_KEY antes de generar evidencia real."
        )

    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    analyzer = build_analyzer()
    rows: list[dict[str, str | bool]] = []

    for case in cases:
        for mode in AnalysisMode:
            error = ""
            try:
                result = analyzer.analyze(
                    AnalyzeRequest(message=case["message"], mode=mode)
                )
                actual_category = result.category.value
                actual_priority = result.priority.value
                response = result.response
                human_review = result.requiresHumanReview
                valid_format = True
            except Exception as exception:  # Recorded as comparative evidence.
                actual_category = ""
                actual_priority = ""
                response = ""
                human_review = False
                valid_format = False
                error = str(exception)

            correct = (
                valid_format
                and actual_category == case["expectedCategory"]
                and actual_priority == case["expectedPriority"]
            )
            rows.append(
                {
                    "caseId": case["id"],
                    "type": case["type"],
                    "message": case["message"],
                    "mode": mode.value,
                    "expectedCategory": case["expectedCategory"],
                    "expectedPriority": case["expectedPriority"],
                    "category": actual_category,
                    "priority": actual_priority,
                    "response": response,
                    "requiresHumanReview": human_review,
                    "validFormat": valid_format,
                    "correct": correct,
                    "error": error,
                }
            )

    RESULTS_DIR.mkdir(exist_ok=True)
    with (RESULTS_DIR / "comparison.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    accuracy: dict[str, float] = {}
    for mode in AnalysisMode:
        subset = [row for row in rows if row["mode"] == mode.value]
        accuracy[mode.value] = round(
            100 * sum(bool(row["correct"]) for row in subset) / len(subset),
            2,
        )

    summary = {
        "generatedAt": datetime.now(UTC).isoformat(),
        "totalCasesPerEngine": len(cases),
        "totalRows": len(rows),
        "accuracy": accuracy,
    }
    (RESULTS_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
