from app.domain.models import (
    AnalysisMode,
    AnalyzeRequest,
    Category,
    GenerativeResult,
    Priority,
)
from app.services.analyzer import SupportAnalyzer


class StubProvider:
    def analyze(self, message: str) -> GenerativeResult:
        return GenerativeResult(
            category=Category.SECURITY,
            priority=Priority.HIGH,
            response="Escalaremos el incidente.",
            requiresHumanReview=False,
        )


def test_service_enforces_human_review_for_security():
    result = SupportAnalyzer(StubProvider()).analyze(
        AnalyzeRequest(message="Posible phishing", mode=AnalysisMode.GENERATIVE)
    )
    assert result.mode is AnalysisMode.GENERATIVE
    assert result.requiresHumanReview is True
