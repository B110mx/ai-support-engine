from app.domain.models import (
    AnalysisMode,
    AnalyzeRequest,
    Category,
    EngineResult,
    Priority,
)
from app.services.analyzer import SupportAnalyzer


class SecurityEngine:
    def analyze(self, message: str) -> EngineResult:
        return EngineResult(
            category=Category.SECURITY,
            priority=Priority.HIGH,
            response=f"Se revisará el incidente: {message}",
            requiresHumanReview=False,
        )


def test_analyzer_selects_mode_and_enforces_security_review() -> None:
    analyzer = SupportAnalyzer({AnalysisMode.TRADITIONAL: SecurityEngine()})

    result = analyzer.analyze(
        AnalyzeRequest(message="Posible phishing", mode="traditional")
    )

    assert result.mode is AnalysisMode.TRADITIONAL
    assert result.category is Category.SECURITY
    assert result.requiresHumanReview is True
