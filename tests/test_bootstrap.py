from app import bootstrap
from app.domain.models import (
    AnalysisMode,
    AnalyzeRequest,
    Category,
    EngineResult,
    Priority,
)


class FakeGeminiEngine:
    def __init__(self, api_key: str) -> None:
        assert api_key == "fake-key"

    def analyze(self, message: str) -> EngineResult:
        return EngineResult(
            category=Category.FEATURE,
            priority=Priority.LOW,
            response="Solicitud registrada.",
            requiresHumanReview=False,
        )


def test_build_analyzer_registers_gemini_when_key_exists(monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    monkeypatch.setattr(bootstrap, "GeminiSupportEngine", FakeGeminiEngine)

    analyzer = bootstrap.build_analyzer()
    result = analyzer.analyze(
        AnalyzeRequest(message="Agregar modo oscuro", mode="generative")
    )

    assert result.mode is AnalysisMode.GENERATIVE
    assert result.category is Category.FEATURE
