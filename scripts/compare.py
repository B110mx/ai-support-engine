import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from app.config import get_settings
from app.domain.models import AnalysisMode, AnalyzeRequest
from app.providers.gemini import GeminiProvider
from app.services.analyzer import SupportAnalyzer


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise SystemExit("Configura GEMINI_API_KEY para ejecutar la comparación real.")

    cases = json.loads((ROOT / "data" / "test_cases.json").read_text(encoding="utf-8"))
    analyzer = SupportAnalyzer(GeminiProvider(settings))
    rows: list[dict] = []

    for case in cases:
        for mode in AnalysisMode:
            try:
                result = analyzer.analyze(
                    AnalyzeRequest(message=case["message"], mode=mode)
                )
                valid_format = True
                error = ""
            except Exception as exception:  # Se registra para la evidencia comparativa.
                result = None
                valid_format = False
                error = str(exception)

            actual_category = result.category.value if result else ""
            actual_priority = result.priority.value if result else ""
            correct = (
                valid_format
                and actual_category == case["expectedCategory"]
                and actual_priority == case["expectedPriority"]
            )
            rows.append({
                "caseId": case["id"],
                "message": case["message"],
                "mode": mode.value,
                "expectedCategory": case["expectedCategory"],
                "expectedPriority": case["expectedPriority"],
                "category": actual_category,
                "priority": actual_priority,
                "validFormat": valid_format,
                "correct": correct,
                "error": error,
            })

    output_dir = ROOT / "results"
    output_dir.mkdir(exist_ok=True)
    with (output_dir / "comparison.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    accuracy = {}
    for mode in AnalysisMode:
        subset = [row for row in rows if row["mode"] == mode.value]
        accuracy[mode.value] = round(
            100 * sum(row["correct"] for row in subset) / len(subset), 2
        )

    summary = {
        "generatedAt": datetime.now(UTC).isoformat(),
        "totalCasesPerEngine": len(cases),
        "accuracy": accuracy,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
