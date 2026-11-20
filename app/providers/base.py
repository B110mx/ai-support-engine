from typing import Protocol

from app.domain.models import GenerativeResult


class GenerativeProvider(Protocol):
    def analyze(self, message: str) -> GenerativeResult: ...
