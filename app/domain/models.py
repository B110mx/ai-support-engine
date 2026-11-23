from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Category(str, Enum):
    ACCESS = "ACCESS"
    BUG = "BUG"
    FEATURE = "FEATURE"
    SECURITY = "SECURITY"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AnalysisMode(str, Enum):
    TRADITIONAL = "traditional"
    GENERATIVE = "generative"


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    message: str = Field(min_length=3, max_length=5_000)
    mode: AnalysisMode


class EngineResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    category: Category
    priority: Priority
    response: str = Field(min_length=1, max_length=2_000)
    requiresHumanReview: bool


class AnalysisResult(EngineResult):
    mode: AnalysisMode
