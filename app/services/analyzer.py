from app.domain.models import AnalysisMode, AnalysisResult, AnalyzeRequest, Category
from app.domain.traditional import analyze_traditional
from app.providers.base import GenerativeProvider


class SupportAnalyzer:
    def __init__(self, generative_provider: GenerativeProvider | None = None) -> None:
        self._generative_provider = generative_provider

    def analyze(self, request: AnalyzeRequest) -> AnalysisResult:
        if request.mode is AnalysisMode.TRADITIONAL:
            return analyze_traditional(request.message)
        if self._generative_provider is None:
            raise RuntimeError("El motor generativo no está configurado")

        generated = self._generative_provider.analyze(request.message)
        return AnalysisResult(
            category=generated.category,
            priority=generated.priority,
            response=generated.response,
            requiresHumanReview=(
                True if generated.category is Category.SECURITY
                else generated.requiresHumanReview
            ),
            mode=AnalysisMode.GENERATIVE,
        )
