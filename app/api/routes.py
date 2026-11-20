from fastapi import APIRouter, Depends, HTTPException, status

from app.config import get_settings
from app.domain.models import AnalysisResult, AnalyzeRequest
from app.providers.gemini import GeminiProvider
from app.services.analyzer import SupportAnalyzer


router = APIRouter()


async def get_analyzer() -> SupportAnalyzer:
    settings = get_settings()
    provider = GeminiProvider(settings) if settings.gemini_api_key else None
    return SupportAnalyzer(provider)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/api/analyze", response_model=AnalysisResult)
async def analyze(
    payload: AnalyzeRequest,
    analyzer: SupportAnalyzer = Depends(get_analyzer),
) -> AnalysisResult:
    try:
        return analyzer.analyze(payload)
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="El proveedor generativo no devolvió una respuesta válida.",
        ) from error
