from fastapi.testclient import TestClient

from app.api.dependencies import get_analyzer
from app.domain.models import (
    AnalysisMode,
    Category,
    EngineResult,
    Priority,
)
from app.main import app
from app.services.analyzer import SupportAnalyzer


class FakeEngine:
    def analyze(self, message: str) -> EngineResult:
        return EngineResult(
            category=Category.ACCESS,
            priority=Priority.MEDIUM,
            response=f"Solicitud recibida: {message}",
            requiresHumanReview=False,
        )


class ExplodingEngine:
    def analyze(self, message: str) -> EngineResult:
        raise RuntimeError("Fallo interno simulado")


def override_analyzer() -> SupportAnalyzer:
    return SupportAnalyzer({AnalysisMode.TRADITIONAL: FakeEngine()})


def override_failing_analyzer() -> SupportAnalyzer:
    return SupportAnalyzer({AnalysisMode.GENERATIVE: ExplodingEngine()})


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_registered_traditional_engine_works_without_override() -> None:
    response = client.post(
        "/api/analyze",
        json={"message": "No puedo iniciar sesión", "mode": "traditional"},
    )

    assert response.status_code == 200
    assert response.json()["category"] == "ACCESS"
    assert response.json()["mode"] == "traditional"


def test_analyze_uses_common_contract() -> None:
    app.dependency_overrides[get_analyzer] = override_analyzer
    try:
        response = client.post(
            "/api/analyze",
            json={"message": "No puedo iniciar sesión", "mode": "traditional"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "category": "ACCESS",
        "priority": "MEDIUM",
        "response": "Solicitud recibida: No puedo iniciar sesión",
        "requiresHumanReview": False,
        "mode": "traditional",
    }


def test_analyze_returns_503_for_unregistered_engine() -> None:
    response = client.post(
        "/api/analyze",
        json={"message": "Necesito ayuda", "mode": "generative"},
    )

    assert response.status_code == 503
    assert "todavía no está disponible" in response.json()["detail"]


def test_analyze_hides_internal_engine_errors() -> None:
    app.dependency_overrides[get_analyzer] = override_failing_analyzer
    try:
        response = client.post(
            "/api/analyze",
            json={"message": "Necesito ayuda", "mode": "generative"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json() == {
        "detail": "El motor seleccionado no pudo completar el análisis."
    }


def test_analyze_rejects_invalid_body() -> None:
    response = client.post(
        "/api/analyze",
        json={"message": "x", "mode": "traditional", "extra": "no permitido"},
    )

    assert response.status_code == 422
