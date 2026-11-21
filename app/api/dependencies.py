from functools import lru_cache

from app.bootstrap import build_analyzer
from app.services.analyzer import SupportAnalyzer


@lru_cache
def get_analyzer() -> SupportAnalyzer:
    """Return the shared application service used by the API."""
    return build_analyzer()
