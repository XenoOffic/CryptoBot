from app.models.analysis import (
    AnalysisComponent,
    AnalysisScore,
)


def build_score(
    trend_score: float,
    trend_label: str,
    trend_observations: list[str],

    momentum_score: float,
    momentum_label: str,
    momentum_observations: list[str],

    volatility_score: float,
    volatility_label: str,
    volatility_observations: list[str],

    structure_score: float,
    structure_label: str,
    structure_observations: list[str],
):
    overall = (
        trend_score * 0.35
        + momentum_score * 0.30
        + volatility_score * 0.15
        + structure_score * 0.20
    )

    overall = round(
        max(0, min(100, overall)),
        2,
    )

    if overall >= 75:
        overall_label = "STRONGLY BULLISH"

    elif overall >= 60:
        overall_label = "BULLISH"

    elif overall >= 45:
        overall_label = "NEUTRAL"

    elif overall >= 30:
        overall_label = "BEARISH"

    else:
        overall_label = "STRONGLY BEARISH"

    return AnalysisScore(
        overall=overall,
        label=overall_label,

        trend=AnalysisComponent(
            score=trend_score,
            label=trend_label,
            explanation=" ".join(
                trend_observations
            ),
        ),

        momentum=AnalysisComponent(
            score=momentum_score,
            label=momentum_label,
            explanation=" ".join(
                momentum_observations
            ),
        ),

        volatility=AnalysisComponent(
            score=volatility_score,
            label=volatility_label,
            explanation=" ".join(
                volatility_observations
            ),
        ),

        structure=AnalysisComponent(
            score=structure_score,
            label=structure_label,
            explanation=" ".join(
                structure_observations
            ),
        ),
    )
