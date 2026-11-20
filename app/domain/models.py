from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Category(StrEnum):
    ACCESS = "ACCESS"
    BUG = "BUG"
    FEATURE = "FEATURE"
    SECURITY = "SECURITY"


class Priority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AnalysisMode(StrEnum):
    TRADITIONAL = "traditional"
    GENERATIVE = "generative"


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    message: str = Field(min_length=3, max_length=5_000)
    mode: AnalysisMode

    @field_validator("message")
    @classmethod
    def reject_blank_message(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("message no puede estar vacío")
        return value


class AnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Category
    priority: Priority
    response: str = Field(min_length=1, max_length=2_000)
    requiresHumanReview: bool
    mode: AnalysisMode


class GenerativeResult(BaseModel):
    """Contrato estricto que debe devolver el modelo generativo."""

    model_config = ConfigDict(extra="forbid")

    category: Category
    priority: Priority
    response: str = Field(min_length=1, max_length=2_000)
    requiresHumanReview: bool
