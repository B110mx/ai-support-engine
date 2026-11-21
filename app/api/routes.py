from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_analyzer
from app.domain.errors import EngineExecutionError, EngineUnavailableError
from app.domain.models import AnalysisResult, AnalyzeRequest
from app.services.analyzer import SupportAnalyzer

router = APIRouter()


@router.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/api/analyze",
    response_model=AnalysisResult,
    tags=["analysis"],
)
def analyze(
    payload: AnalyzeRequest,
    analyzer: SupportAnalyzer = Depends(get_analyzer),
) -> AnalysisResult:
    try:
        return analyzer.analyze(payload)
    except EngineUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except EngineExecutionError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="El motor seleccionado no pudo completar el análisis.",
        ) from error
