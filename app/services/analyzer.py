from collections.abc import Mapping

from app.domain.errors import EngineExecutionError, EngineUnavailableError
from app.domain.models import (
    AnalysisMode,
    AnalysisResult,
    AnalyzeRequest,
    Category,
)
from app.domain.ports import SupportEngine


class SupportAnalyzer:
    def __init__(self, engines: Mapping[AnalysisMode, SupportEngine]) -> None:
        self._engines = dict(engines)

    def analyze(self, request: AnalyzeRequest) -> AnalysisResult:
        engine = self._engines.get(request.mode)
        if engine is None:
            raise EngineUnavailableError(
                f"El motor '{request.mode.value}' todavía no está disponible."
            )

        try:
            result = engine.analyze(request.message)
        except EngineExecutionError:
            raise
        except Exception as error:
            raise EngineExecutionError("El motor produjo un error inesperado.") from error

        if result.category is Category.SECURITY and not result.requiresHumanReview:
            result = result.model_copy(update={"requiresHumanReview": True})

        return AnalysisResult(
            **result.model_dump(),
            mode=request.mode,
        )
