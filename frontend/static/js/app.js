/* ============================================================
   CRYPTOLYTICS — APPLICATION CONTROLLER
   ============================================================ */


/* ============================================================
   START APPLICATION
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeChart();

        setupControls();

        setActivePeriod(
            AppState.days
        );

        loadAnalysis();

    }
);


/* ============================================================
   UI CONTROLS
   ============================================================ */

function setupControls() {

    const analyzeButton =
        document.getElementById(
            "analyze-button"
        );

    const symbolInput =
        document.getElementById(
            "symbol-input"
        );


    /* --------------------------------------------------------
       ANALYZE BUTTON
       -------------------------------------------------------- */

    if (analyzeButton) {

        analyzeButton.addEventListener(
            "click",
            () => {

                analyzeSymbol();

            }
        );

    }


    /* --------------------------------------------------------
       ENTER KEY
       -------------------------------------------------------- */

    if (symbolInput) {

        symbolInput.addEventListener(
            "keydown",
            event => {

                if (
                    event.key === "Enter"
                ) {

                    analyzeSymbol();

                }

            }
        );

    }


    /* --------------------------------------------------------
       SIDEBAR TIME BUTTONS
       -------------------------------------------------------- */

    document
        .querySelectorAll(
            ".time-buttons [data-days]"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        const days =
                            Number(
                                button.dataset.days
                            );


                        AppState.days =
                            days;


                        setActivePeriod(
                            days
                        );


                        loadAnalysis();

                    }
                );

            }
        );


    /* --------------------------------------------------------
       CHART TIME BUTTONS
       -------------------------------------------------------- */

    document
        .querySelectorAll(
            ".chart-controls [data-days]"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        const days =
                            Number(
                                button.dataset.days
                            );


                        AppState.days =
                            days;


                        setActivePeriod(
                            days
                        );


                        loadAnalysis();

                    }
                );

            }
        );

}


/* ============================================================
   ANALYZE SYMBOL
   ============================================================ */

function analyzeSymbol() {

    const symbolInput =
        document.getElementById(
            "symbol-input"
        );


    if (!symbolInput) {
        return;
    }


    const symbol =
        symbolInput.value
            .trim()
            .toUpperCase();


    /* --------------------------------------------------------
       VALIDATE SYMBOL
       -------------------------------------------------------- */

    if (!symbol) {

        setLoading(
            false,
            "Enter a cryptocurrency symbol."
        );

        return;
    }


    /* --------------------------------------------------------
       CHECK WHETHER CRYPTO CHANGED
       -------------------------------------------------------- */

    const previousSymbol =
        AppState.symbol;


    AppState.symbol =
        symbol;


    /*
     * When switching from one cryptocurrency
     * to another, immediately remove the old
     * market data from the chart and state.
     *
     * This is especially important for assets
     * with very different prices, for example:
     *
     * BTC  ~ $100,000
     * DOGE ~ $0.07
     */

    if (
        previousSymbol !== symbol
    ) {

        if (
            typeof resetChartData ===
            "function"
        ) {

            resetChartData();

        }


        AppState.market =
            null;


        AppState.candles =
            [];


        AppState.indicators =
            null;

    }


    /* --------------------------------------------------------
       LOAD NEW MARKET
       -------------------------------------------------------- */

    loadAnalysis();

}


/* ============================================================
   ACTIVE PERIOD
   ============================================================ */

function setActivePeriod(
    days
) {

    const normalizedDays =
        String(days);


    /*
     * Update BOTH sidebar and
     * chart controls.
     */

    document
        .querySelectorAll(
            "[data-days]"
        )
        .forEach(
            button => {

                button.classList.toggle(
                    "active",
                    String(
                        button.dataset.days
                    ) === normalizedDays
                );

            }
        );

}


/* ============================================================
   LOAD ANALYSIS
   ============================================================ */

async function loadAnalysis() {

    /*
     * Prevent duplicate requests.
     */

    if (AppState.loading) {
        return;
    }


    AppState.loading =
        true;


    setLoading(
        true,
        "Loading market data..."
    );


    try {

        /* ----------------------------------------------------
           REQUEST FULL ANALYSIS
           ---------------------------------------------------- */

        const data =
            await fetchAnalysis(
                AppState.symbol,
                AppState.days
            );


        /* ----------------------------------------------------
           VALIDATE RESPONSE
           ---------------------------------------------------- */

        if (
            !data ||
            !data.market
        ) {

            throw new Error(
                "Invalid market data received."
            );

        }


        /* ----------------------------------------------------
           SAVE STATE
           ---------------------------------------------------- */

        AppState.market =
            data.market;


        AppState.candles =
            data.candles || [];


        /*
         * Keep indicators as null when
         * the API does not provide them.
         */

        AppState.indicators =
            data.indicators || null;


        /* ----------------------------------------------------
           RENDER MARKET
           ---------------------------------------------------- */

        renderMarket(
            data.market
        );


        /* ----------------------------------------------------
           RENDER INDICATORS
           ---------------------------------------------------- */

        renderIndicators(
            data.indicators || null
        );


        /* ----------------------------------------------------
           UPDATE CHART
           ---------------------------------------------------- */

        updateChart(
            data.candles || [],
            data.indicators || null
        );


        /* ----------------------------------------------------
           FIT NEW CRYPTO SCALE
           ---------------------------------------------------- */

        /*
         * updateChart() already enables automatic
         * price scaling.
         *
         * requestAnimationFrame gives Lightweight
         * Charts one rendering cycle before the final
         * visible range is fitted.
         */

        if (
            typeof priceChart !==
            "undefined"
            &&
            priceChart
        ) {

            requestAnimationFrame(
                () => {

                    priceChart
                        .priceScale("right")
                        .applyOptions({
                            autoScale: true,
                        });


                    priceChart
                        .timeScale()
                        .fitContent();

                }
            );

        }


        /* ----------------------------------------------------
           SUCCESS STATUS
           ---------------------------------------------------- */

        setLoading(
            false,
            `${data.candles?.length || 0} candles loaded`
        );


    } catch (error) {

        console.error(
            "[CRYPTOLYTICS]",
            error
        );


        setLoading(
            false,
            getErrorMessage(
                error
            )
        );


    } finally {

        AppState.loading =
            false;

    }

}


/* ============================================================
   MARKET RENDERING
   ============================================================ */

function renderMarket(
    market
) {

    if (!market) {
        return;
    }


    const symbolElement =
        document.getElementById(
            "market-symbol"
        );

    const priceElement =
        document.getElementById(
            "price"
        );

    const changeElement =
        document.getElementById(
            "change"
        );

    const marketCapElement =
        document.getElementById(
            "market-cap"
        );

    const volumeElement =
        document.getElementById(
            "volume"
        );


    /* --------------------------------------------------------
       SYMBOL
       -------------------------------------------------------- */

    if (symbolElement) {

        symbolElement.textContent =
            `${market.symbol} / USD`;

    }


    /* --------------------------------------------------------
       PRICE
       -------------------------------------------------------- */

    if (priceElement) {

        priceElement.textContent =
            formatPrice(
                market.price
            );

    }


    /* --------------------------------------------------------
       24H CHANGE
       -------------------------------------------------------- */

    if (changeElement) {

        changeElement.textContent =
            formatPercent(
                market.change_24h
            );


        changeElement.classList.remove(
            "positive",
            "negative"
        );


        if (
            Number(
                market.change_24h
            ) > 0
        ) {

            changeElement.classList.add(
                "positive"
            );

        } else if (
            Number(
                market.change_24h
            ) < 0
        ) {

            changeElement.classList.add(
                "negative"
            );

        }

    }


    /* --------------------------------------------------------
       MARKET CAP
       -------------------------------------------------------- */

    if (marketCapElement) {

        marketCapElement.textContent =
            formatLargeNumber(
                market.market_cap
            );

    }


    /* --------------------------------------------------------
       VOLUME
       -------------------------------------------------------- */

    if (volumeElement) {

        volumeElement.textContent =
            formatLargeNumber(
                market.volume_24h
            );

    }

}


/* ============================================================
   INDICATORS RENDERING
   ============================================================ */

function renderIndicators(
    indicators
) {

    /*
     * If indicators are unavailable,
     * clear the visible indicator values
     * instead of keeping old crypto data.
     */

    if (!indicators) {

        clearIndicatorDisplay();

        return;
    }


    const movingAverages =
        indicators.moving_averages || {};


    const momentum =
        indicators.momentum || {};


    const volatility =
        indicators.volatility || {};


    const rsiElement =
        document.getElementById(
            "rsi"
        );

    const sma20Element =
        document.getElementById(
            "sma20"
        );

    const sma50Element =
        document.getElementById(
            "sma50"
        );

    const ema20Element =
        document.getElementById(
            "ema20"
        );

    const atrElement =
        document.getElementById(
            "atr"
        );

    const trendElement =
        document.getElementById(
            "trend"
        );


    /* --------------------------------------------------------
       RSI
       -------------------------------------------------------- */

    if (rsiElement) {

        rsiElement.textContent =
            formatNumber(
                momentum.rsi_14
            );

    }


    /* --------------------------------------------------------
       SMA 20
       -------------------------------------------------------- */

    if (sma20Element) {

        sma20Element.textContent =
            formatPrice(
                movingAverages.sma_20
            );

    }


    /* --------------------------------------------------------
       SMA 50
       -------------------------------------------------------- */

    if (sma50Element) {

        sma50Element.textContent =
            formatPrice(
                movingAverages.sma_50
            );

    }


    /* --------------------------------------------------------
       EMA 20
       -------------------------------------------------------- */

    if (ema20Element) {

        ema20Element.textContent =
            formatPrice(
                movingAverages.ema_20
            );

    }


    /* --------------------------------------------------------
       ATR
       -------------------------------------------------------- */

    if (atrElement) {

        atrElement.textContent =
            formatPrice(
                volatility.atr_14
            );

    }


    /* --------------------------------------------------------
       TREND
       -------------------------------------------------------- */

    if (trendElement) {

        trendElement.textContent =
            indicators.trend || "—";


        trendElement.classList.remove(
            "positive",
            "negative"
        );


        const trend =
            String(
                indicators.trend || ""
            ).toLowerCase();


        if (
            trend.includes("bull")
            ||
            trend.includes("up")
            ||
            trend.includes("positive")
        ) {

            trendElement.classList.add(
                "positive"
            );

        } else if (
            trend.includes("bear")
            ||
            trend.includes("down")
            ||
            trend.includes("negative")
        ) {

            trendElement.classList.add(
                "negative"
            );

        }

    }

}


/* ============================================================
   CLEAR INDICATOR DISPLAY
   ============================================================ */

function clearIndicatorDisplay() {

    const ids = [

        "rsi",

        "sma20",

        "sma50",

        "ema20",

        "atr",

        "trend",

    ];


    ids.forEach(
        id => {

            const element =
                document.getElementById(
                    id
                );


            if (element) {

                element.textContent =
                    "—";

                element.classList.remove(
                    "positive",
                    "negative"
                );

            }

        }
    );

}


/* ============================================================
   LOADING STATE
   ============================================================ */

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


    if (loading) {

        element.textContent =
            message || "Loading...";


        element.setAttribute(
            "aria-busy",
            "true"
        );

    } else {

        element.textContent =
            message;


        element.setAttribute(
            "aria-busy",
            "false"
        );

    }

}


/* ============================================================
   ERROR HANDLING
   ============================================================ */

function getErrorMessage(
    error
) {

    if (!error) {

        return (
            "Unable to load market data."
        );

    }


    if (
        error.message
    ) {

        return error.message;

    }


    return (
        "Unable to load market data."
    );

}


/* ============================================================
   PRICE FORMATTER
   ============================================================ */

function formatPrice(
    value
) {

    if (
        value === null ||
        value === undefined ||
        !Number.isFinite(
            Number(value)
        )
    ) {

        return "—";

    }


    const numericValue =
        Number(value);


    /*
     * Crypto prices can have very
     * different magnitudes.
     *
     * BTC:
     *     ~100000
     *
     * DOGE:
     *     ~0.07
     *
     * Cheap assets therefore need
     * additional decimal precision.
     */

    let maximumFractionDigits =
        2;


    if (
        numericValue > 0 &&
        numericValue < 1
    ) {

        maximumFractionDigits =
            6;

    }


    return new Intl.NumberFormat(
        "en-US",
        {
            style: "currency",

            currency: "USD",

            maximumFractionDigits:
                maximumFractionDigits,
        }
    ).format(
        numericValue
    );

}


/* ============================================================
   NUMBER FORMATTER
   ============================================================ */

function formatNumber(
    value
) {

    if (
        value === null ||
        value === undefined ||
        !Number.isFinite(
            Number(value)
        )
    ) {

        return "—";

    }


    return Number(value)
        .toFixed(2);

}


/* ============================================================
   PERCENT FORMATTER
   ============================================================ */

function formatPercent(
    value
) {

    if (
        value === null ||
        value === undefined ||
        !Number.isFinite(
            Number(value)
        )
    ) {

        return "—";

    }


    const numericValue =
        Number(value);


    const sign =
        numericValue >= 0
            ? "+"
            : "";


    return (
        `${sign}${numericValue.toFixed(2)}%`
    );

}


/* ============================================================
   LARGE NUMBER FORMATTER
   ============================================================ */

function formatLargeNumber(
    value
) {

    if (
        value === null ||
        value === undefined ||
        !Number.isFinite(
            Number(value)
        )
    ) {

        return "—";

    }


    return new Intl.NumberFormat(
        "en-US",
       {
            notation: "compact",

            maximumFractionDigits: 2,
       }
    ).format(
        Number(value)
    );
}
