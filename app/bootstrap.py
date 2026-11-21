from app.domain.models import AnalysisMode
from app.domain.ports import SupportEngine
from app.services.analyzer import SupportAnalyzer


def build_analyzer() -> SupportAnalyzer:
    """Compose the application.

    Each engine branch will register its implementation here during integration.
    """
    engines: dict[AnalysisMode, SupportEngine] = {}
    return SupportAnalyzer(engines)
