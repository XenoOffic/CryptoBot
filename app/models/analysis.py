from pydantic import BaseModel, Field


class AnalysisComponent(BaseModel):
    score: float = Field(ge=0, le=100)
    label: str
    explanation: str


class AnalysisScore(BaseModel):
    overall: float = Field(ge=0, le=100)
    label: str

    trend: AnalysisComponent
    momentum: AnalysisComponent
    volatility: AnalysisComponent
    structure: AnalysisComponent


class AnalysisReport(BaseModel):
    symbol: str
    price: float

    market_bias: str
    confidence: str

    score: AnalysisScore

    summary: str
    strengths: list[str]
    risks: list[str]
    observations: list[str]
