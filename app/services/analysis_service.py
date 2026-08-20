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

from app.analysis.support_resistance import (
    analyze_market_structure,
    find_support_resistance,
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

    # ========================================================
    # MARKET
    # ========================================================

    market = await get_market_snapshot(
        symbol
    )

    # ========================================================
    # HISTORICAL DATA
    # ========================================================

    candles = await get_historical_data(
        symbol,
        days=30,
    )

    if not candles:

        raise ValueError(
            "No historical data available."
        )

    # ========================================================
    # TECHNICAL INDICATORS
    # ========================================================

    indicators = calculate_indicators(
        candles
    )

    # ========================================================
    # TREND
    # ========================================================

    (
        trend_score,
        trend_label,
        trend_observations,
    ) = analyze_trend(
        market.price,
        indicators,
    )

    # ========================================================
    # MOMENTUM
    # ========================================================

    (
        momentum_score,
        momentum_label,
        momentum_observations,
    ) = analyze_momentum(
        indicators,
    )

    # ========================================================
    # VOLATILITY
    # ========================================================

    (
        volatility_score,
        volatility_label,
        volatility_observations,
    ) = analyze_volatility(
        market.price,
        indicators,
    )

    # ========================================================
    # MARKET STRUCTURE
    # ========================================================

    (
        structure_score,
        structure_label,
        structure_observations,
    ) = analyze_market_structure(
        candles
    )

    # ========================================================
    # SUPPORT / RESISTANCE
    # ========================================================

    support_resistance = (
        find_support_resistance(
            candles,
            market.price,
        )
    )

    # ========================================================
    # SCORING
    # ========================================================

    score = build_score(

        trend_score,
        trend_label,
        trend_observations,

        momentum_score,
        momentum_label,
        momentum_observations,

        volatility_score,
        volatility_label,
        volatility_observations,

        structure_score,
        structure_label,
        structure_observations,
    )

    # ========================================================
    # REPORT
    # ========================================================

    report = generate_report(
        symbol=market.symbol,
        price=market.price,
        score=score,
    )

    # ========================================================
    # RESULT
    # ========================================================

    return {
        "market": market,
        "indicators": indicators,
        "structure": {
            "score": structure_score,
            "label": structure_label,
            "observations": structure_observations,
        },
        "support_resistance": support_resistance,
        "score": score,
        "report": report,
        "candles": candles,
    }
