from fastapi.testclient import TestClient

from app.api.routes import get_analyzer
from app.domain.models import Category, GenerativeResult, Priority
from app.main import app
from app.services.analyzer import SupportAnalyzer


class StubProvider:
    def analyze(self, message: str) -> GenerativeResult:
        return GenerativeResult(
            category=Category.ACCESS,
            priority=Priority.MEDIUM,
            response="Verifique sus credenciales.",
            requiresHumanReview=False,
        )


async def override_analyzer() -> SupportAnalyzer:
    return SupportAnalyzer(StubProvider())


client = TestClient(app)


def test_traditional_endpoint_contract():
    response = client.post(
        "/api/analyze",
        json={"message": "No puedo iniciar sesión", "mode": "traditional"},
    )
    assert response.status_code == 200
    assert set(response.json()) == {
        "category", "priority", "response", "requiresHumanReview", "mode"
    }


def test_generative_endpoint_contract():
    app.dependency_overrides[get_analyzer] = override_analyzer
    try:
        response = client.post(
            "/api/analyze",
            json={"message": "No puedo iniciar sesión", "mode": "generative"},
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["mode"] == "generative"


def test_rejects_invalid_requests():
    response = client.post(
        "/api/analyze",
        json={"message": "x", "mode": "manual"},
    )
    assert response.status_code == 422
