import os

from dotenv import load_dotenv

from app.domain.models import AnalysisMode
from app.domain.ports import SupportEngine
from app.engines.gemini import GeminiSupportEngine
from app.engines.traditional import TraditionalEngine
from app.services.analyzer import SupportAnalyzer


def build_analyzer() -> SupportAnalyzer:
    """Compose the application.

    Each engine branch will register its implementation here during integration.
    """
    load_dotenv()
    engines: dict[AnalysisMode, SupportEngine] = {
        AnalysisMode.TRADITIONAL: TraditionalEngine(),
    }
    if api_key := os.getenv("GEMINI_API_KEY"):
        engines[AnalysisMode.GENERATIVE] = GeminiSupportEngine(api_key=api_key)
    return SupportAnalyzer(engines)
