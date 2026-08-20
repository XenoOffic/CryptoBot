from app.analysis.indicators import (
    calculate_indicators,
)

from app.analysis.trend import (
    analyze_trend,
)

from app.analysis.momentum import (
    analyze_momentum,
)

from app.analysis.volatility import (
    analyze_volatility,
)

from app.analysis.scoring import (
    build_score,
)

from app.analysis.report import (
    generate_report,
)

from app.data.market_data import (
    get_historical_data,
    get_market_snapshot,
)


async def analyze_crypto(
    symbol: str,
):

    market = await get_market_snapshot(
        symbol
    )

    candles = await get_historical_data(
        symbol,
        days=30,
    )

    indicators = calculate_indicators(
        candles
    )

    trend_score, trend_label, trend_obs = (
        analyze_trend(
            market.price,
            indicators,
        )
    )

    momentum_score, momentum_label, momentum_obs = (
        analyze_momentum(
            indicators,
        )
    )

    volatility_score, volatility_label, volatility_obs = (
        analyze_volatility(
            market.price,
            indicators,
        )
    )

    # Struttura temporaneamente neutrale.
    # La sostituiremo con il vero motore
    # support/resistance.
    structure_score = 50.0
    structure_label = "NEUTRAL"
    structure_obs = [
        "Advanced market structure analysis "
        "will be added next."
    ]

    score = build_score(

        trend_score,
        trend_label,
        trend_obs,

        momentum_score,
        momentum_label,
        momentum_obs,

        volatility_score,
        volatility_label,
        volatility_obs,

        structure_score,
        structure_label,
        structure_obs,
    )

    report = generate_report(
        symbol=market.symbol,
        price=market.price,
        score=score,
    )

    return {
        "market": market,
        "indicators": indicators,
        "report": report,
        "candles": candles,
    }
