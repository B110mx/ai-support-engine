import pytest
from pydantic import ValidationError

from app.domain.models import AnalysisMode, AnalyzeRequest


def test_request_strips_message_whitespace() -> None:
    request = AnalyzeRequest(message="  No puedo ingresar  ", mode="traditional")

    assert request.message == "No puedo ingresar"
    assert request.mode is AnalysisMode.TRADITIONAL


@pytest.mark.parametrize(
    "payload",
    [
        {"message": "x", "mode": "traditional"},
        {"message": "Mensaje válido", "mode": "manual"},
        {"message": "Mensaje válido", "mode": "traditional", "extra": True},
    ],
)
def test_request_rejects_invalid_payloads(payload: dict) -> None:
    with pytest.raises(ValidationError):
        AnalyzeRequest.model_validate(payload)
