import pytest
from unittest.mock import patch, MagicMock
from app.engines.gemini_engine import GeminiSupportEngine, GeminiEngineError

@pytest.fixture
def engine():
    return GeminiSupportEngine(api_key="fake_test_key")

@patch("app.engines.gemini_engine.genai.Client")
def test_analyze_ticket_success(mock_client_class, engine):
    mock_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"category": "BUG", "priority": "HIGH", "suggested_response": "Reinicio necesario", "reasoning": "Fallo del sistema"}'
    mock_instance.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_instance
    
    engine.client = mock_instance

    resultado = engine.analyze_ticket("La pantalla se quedó en blanco al guardar.")
    assert "BUG" in resultado 

def test_empty_ticket(engine):
    with pytest.raises(GeminiEngineError, match="El ticket está vacío"):
        engine.analyze_ticket("   ")