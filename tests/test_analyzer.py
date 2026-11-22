import pytest

from app.domain.errors import EngineExecutionError
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


class ControlledFailureEngine:
    def analyze(self, message: str) -> EngineResult:
        raise EngineExecutionError("Fallo conocido")


def test_analyzer_selects_mode_and_enforces_security_review() -> None:
    analyzer = SupportAnalyzer({AnalysisMode.TRADITIONAL: SecurityEngine()})

    result = analyzer.analyze(
        AnalyzeRequest(message="Posible phishing", mode="traditional")
    )

    assert result.mode is AnalysisMode.TRADITIONAL
    assert result.category is Category.SECURITY
    assert result.requiresHumanReview is True


def test_analyzer_preserves_controlled_engine_errors() -> None:
    analyzer = SupportAnalyzer(
        {AnalysisMode.GENERATIVE: ControlledFailureEngine()}
    )

    with pytest.raises(EngineExecutionError, match="Fallo conocido"):
        analyzer.analyze(
            AnalyzeRequest(message="Mensaje válido", mode="generative")
        )
