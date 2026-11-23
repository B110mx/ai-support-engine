from typing import Protocol

from app.domain.models import EngineResult


class SupportEngine(Protocol):
    """Contract implemented by traditional and generative engines."""

    def analyze(self, message: str) -> EngineResult:
        """Analyze one validated support request."""
        ...
