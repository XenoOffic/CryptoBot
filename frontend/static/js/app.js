document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeChart();

        setupControls();

        loadAnalysis();

    }
);


function setupControls() {

    const analyzeButton =
        document.getElementById(
            "analyze-button"
        );

    const symbolInput =
        document.getElementById(
            "symbol-input"
        );

    analyzeButton.addEventListener(
        "click",
        () => {

            const symbol =
                symbolInput.value
                    .trim()
                    .toUpperCase();

            if (!symbol) {
                return;
            }

            AppState.symbol =
                symbol;

            loadAnalysis();

        }
    );


    document
        .querySelectorAll(
            "[data-days]"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        document
                            .querySelectorAll(
                                "[data-days]"
                            )
                            .forEach(
                                item =>
                                    item.classList
                                        .remove(
                                            "active"
                                        )
                            );

                        button.classList.add(
                            "active"
                        );

                        AppState.days =
                            Number(
                                button.dataset.days
                            );

                        loadAnalysis();

                    }
                );

            }
        );
}


async function loadAnalysis() {

    if (AppState.loading) {
        return;
    }

    AppState.loading = true;

    setLoading(
        true
    );

    try {

        const data =
            await fetchAnalysis(
                AppState.symbol,
                AppState.days
            );

        AppState.market =
            data.market;

        AppState.candles =
            data.candles;

        AppState.indicators =
            data.indicators;

        renderMarket(
            data.market
        );

        renderIndicators(
            data.indicators
        );

        updateChart(
            data.candles
        );

        setLoading(
            false,
            `${data.candles.length} candles loaded`
        );

    } catch (error) {

        console.error(
            error
        );

        setLoading(
            false,
            error.message
        );

    } finally {

        AppState.loading =
            false;

    }
}


function renderMarket(
    market
) {

    document.getElementById(
        "market-symbol"
    ).textContent =
        `${market.symbol} / USD`;

    document.getElementById(
        "price"
    ).textContent =
        formatPrice(
            market.price
        );

    document.getElementById(
        "change"
    ).textContent =
        formatPercent(
            market.change_24h
        );

    document.getElementById(
        "market-cap"
    ).textContent =
        formatLargeNumber(
            market.market_cap
        );

    document.getElementById(
        "volume"
    ).textContent =
        formatLargeNumber(
            market.volume_24h
        );
}


function renderIndicators(
    indicators
) {

    const movingAverages =
        indicators.moving_averages;

    const momentum =
        indicators.momentum;

    const volatility =
        indicators.volatility;


    document.getElementById(
        "rsi"
    ).textContent =
        formatNumber(
            momentum.rsi_14
        );

    document.getElementById(
        "sma20"
    ).textContent =
        formatPrice(
            movingAverages.sma_20
        );

    document.getElementById(
        "sma50"
    ).textContent =
        formatPrice(
            movingAverages.sma_50
        );

    document.getElementById(
        "ema20"
    ).textContent =
        formatPrice(
            movingAverages.ema_20
        );

    document.getElementById(
        "atr"
    ).textContent =
        formatPrice(
            volatility.atr_14
        );

    document.getElementById(
        "trend"
    ).textContent =
        indicators.trend;
}


function setLoading(
    loading,
    message = "Ready"
) {

    const element =
        document.getElementById(
            "loading-status"
        );

    if (!element) {
        return;
    }

    element.textContent =
        loading
            ? "Loading..."
            : message;
}


function formatPrice(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {
        return "—";
    }

    return new Intl.NumberFormat(
        "en-US",
        {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 2,
        }
    ).format(value);
}


function formatNumber(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {
        return "—";
    }

    return Number(value)
        .toFixed(2);
}


function formatPercent(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {
        return "—";
    }

    const sign =
        value >= 0
            ? "+"
            : "";

    return (
        `${sign}${Number(value).toFixed(2)}%`
    );
}


function formatLargeNumber(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {
        return "—";
    }

    return new Intl.NumberFormat(
        "en-US",
        {
            notation: "compact",
            maximumFractionDigits: 2,
        }
    ).format(value);
        }
