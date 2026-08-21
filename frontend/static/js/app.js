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

                        setActivePeriod(
                            button.dataset.days
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

                        setActivePeriod(
                            button.dataset.days
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


    if (!symbol) {

        setLoading(
            false,
            "Enter a cryptocurrency symbol."
        );

        return;
    }


    AppState.symbol =
        symbol;


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

        const data =
            await fetchAnalysis(
                AppState.symbol,
                AppState.days
            );


        /*
         * Validate response.
         */

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

        AppState.indicators =
            data.indicators || {};


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
            data.indicators
        );


        /* ----------------------------------------------------
           UPDATE CHART
           ---------------------------------------------------- */

        updateChart(
            data.candles || []
            data.indicators || null
        );


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


    if (symbolElement) {

        symbolElement.textContent =
            `${market.symbol} / USD`;

    }


    if (priceElement) {

        priceElement.textContent =
            formatPrice(
                market.price
            );

    }


    if (changeElement) {

        changeElement.textContent =
            formatPercent(
                market.change_24h
            );


        /*
         * Visual indication of
         * positive / negative movement.
         */

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


    if (marketCapElement) {

        marketCapElement.textContent =
            formatLargeNumber(
                market.market_cap
            );

    }


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

    if (!indicators) {
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


    if (rsiElement) {

        rsiElement.textContent =
            formatNumber(
                momentum.rsi_14
            );

    }


    if (sma20Element) {

        sma20Element.textContent =
            formatPrice(
                movingAverages.sma_20
            );

    }


    if (sma50Element) {

        sma50Element.textContent =
            formatPrice(
                movingAverages.sma_50
            );

    }


    if (ema20Element) {

        ema20Element.textContent =
            formatPrice(
                movingAverages.ema_20
            );

    }


    if (atrElement) {

        atrElement.textContent =
            formatPrice(
                volatility.atr_14
            );

    }


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
     * Crypto prices can have
     * many decimals, especially
     * for low-priced assets.
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
