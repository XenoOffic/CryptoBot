/* ============================================================
   CRYPTOLYTICS — CHART CONTROLLER
   ============================================================ */


/* ============================================================
   CHART STATE
   ============================================================ */

let priceChart = null;

let candleSeries = null;
let volumeSeries = null;

let sma20Series = null;
let sma50Series = null;
let ema20Series = null;

let bollingerMiddleSeries = null;
let bollingerUpperSeries = null;
let bollingerLowerSeries = null;


/* ============================================================
   INITIALIZE CHART
   ============================================================ */

function initializeChart() {

    const container =
        document.getElementById(
            "chart-container"
        );


    if (!container) {
        return;
    }


    /* --------------------------------------------------------
       CHECK LIGHTWEIGHT CHARTS
       -------------------------------------------------------- */

    if (
        typeof LightweightCharts ===
        "undefined"
    ) {

        container.innerHTML = "";

        const error =
            document.createElement(
                "div"
            );

        error.className =
            "chart-placeholder";

        error.textContent =
            "Chart library unavailable.";

        container.appendChild(
            error
        );

        return;
    }


    /* --------------------------------------------------------
       CLEAR CONTAINER
       -------------------------------------------------------- */

    container.innerHTML = "";


    /* ========================================================
       MAIN CHART
       ======================================================== */

    priceChart =
        LightweightCharts.createChart(
            container,
            {

                layout: {

                    background: {
                        color: "#0a0e15",
                    },

                    textColor: "#8c97a8",
                },


                grid: {

                    vertLines: {
                        color: "#151b25",
                    },

                    horzLines: {
                        color: "#151b25",
                    },
                },


                crosshair: {

                    mode:
                        LightweightCharts
                            .CrosshairMode
                            .Normal,
                },


                rightPriceScale: {

                    borderColor:
                        "#252d3b",

                    autoScale:
                        true,

                    scaleMargins: {

                        top: 0.08,

                        bottom: 0.22,
                    },
                },


                timeScale: {

                    borderColor:
                        "#252d3b",

                    timeVisible: true,

                    secondsVisible: false,

                    rightOffset: 5,

                    barSpacing: 8,
                },


                localization: {

                    priceFormatter: (
                        price
                    ) => {

                        if (
                            !Number.isFinite(
                                Number(price)
                            )
                        ) {

                            return "";
                        }


                        const numericPrice =
                            Number(price);


                        let maximumFractionDigits =
                            2;


                        /*
                         * Low-priced cryptocurrencies
                         * such as DOGE need more decimals.
                         */

                        if (
                            numericPrice > 0 &&
                            numericPrice < 1
                        ) {

                            maximumFractionDigits =
                                6;
                        }


                        return new Intl
                            .NumberFormat(
                                "en-US",
                                {
                                    maximumFractionDigits:
                                        maximumFractionDigits,
                                }
                            )
                            .format(
                                numericPrice
                            );
                    },
                },
            }
        );


    /* ========================================================
       CANDLESTICKS
       ======================================================== */

    candleSeries =
        priceChart.addSeries(
            LightweightCharts
                .CandlestickSeries,
            {

                upColor:
                    "#26a69a",

                downColor:
                    "#ef5350",

                borderVisible:
                    false,

                wickUpColor:
                    "#26a69a",

                wickDownColor:
                    "#ef5350",
            }
        );


    /* ========================================================
       SMA 20
       ======================================================== */

    sma20Series =
        priceChart.addSeries(
            LightweightCharts
                .LineSeries,
            {

                lineWidth: 2,

                color: "#f5c451",

                priceLineVisible:
                    false,

                lastValueVisible:
                    false,
            }
        );


    /* ========================================================
       SMA 50
       ======================================================== */

    sma50Series =
        priceChart.addSeries(
            LightweightCharts
                .LineSeries,
            {

                lineWidth: 2,

                color: "#8b7cff",

                priceLineVisible:
                    false,

                lastValueVisible:
                    false,
            }
        );


    /* ========================================================
       EMA 20
       ======================================================== */

    ema20Series =
        priceChart.addSeries(
            LightweightCharts
                .LineSeries,
            {

                lineWidth: 2,

                color: "#4da3ff",

                priceLineVisible:
                    false,

                lastValueVisible:
                    false,
            }
        );


    /* ========================================================
       BOLLINGER MIDDLE
       ======================================================== */

    bollingerMiddleSeries =
        priceChart.addSeries(
            LightweightCharts
                .LineSeries,
            {

                lineWidth: 1,

                color: "#707b8f",

                priceLineVisible:
                    false,

                lastValueVisible:
                    false,
            }
        );


    /* ========================================================
       BOLLINGER UPPER
       ======================================================== */

    bollingerUpperSeries =
        priceChart.addSeries(
            LightweightCharts
                .LineSeries,
            {

                lineWidth: 1,

                color: "#5f6878",

                priceLineVisible:
                    false,

                lastValueVisible:
                    false,
            }
        );


    /* ========================================================
       BOLLINGER LOWER
       ======================================================== */

    bollingerLowerSeries =
        priceChart.addSeries(
            LightweightCharts
                .LineSeries,
            {

                lineWidth: 1,

                color: "#5f6878",

                priceLineVisible:
                    false,

                lastValueVisible:
                    false,
            }
        );


    /* ========================================================
       VOLUME
       ======================================================== */

    volumeSeries =
        priceChart.addSeries(
            LightweightCharts
                .HistogramSeries,
            {

                priceFormat: {

                    type: "volume",
                },

                priceScaleId:
                    "volume",
            }
        );


    /* --------------------------------------------------------
       VOLUME SCALE
       -------------------------------------------------------- */

    priceChart
        .priceScale("volume")
        .applyOptions(
            {

                scaleMargins: {

                    top: 0.82,

                    bottom: 0,
                },
            }
        );


    /* --------------------------------------------------------
       INITIAL RESIZE
       -------------------------------------------------------- */

    resizeChart();


    /* --------------------------------------------------------
       WINDOW RESIZE
       -------------------------------------------------------- */

    window.addEventListener(
        "resize",
        resizeChart
    );
}


/* ============================================================
   RESET CHART DATA
   ============================================================ */

/*
 * Clears all current market data from the chart.
 *
 * This is intentionally outside initializeChart()
 * so app.js can call it when the cryptocurrency changes.
 */

function resetChartData() {

    if (candleSeries) {

        candleSeries.setData(
            []
        );
    }


    if (volumeSeries) {

        volumeSeries.setData(
            []
        );
    }


    if (sma20Series) {

        sma20Series.setData(
            []
        );
    }


    if (sma50Series) {

        sma50Series.setData(
            []
        );
    }


    if (ema20Series) {

        ema20Series.setData(
            []
        );
    }


    if (bollingerMiddleSeries) {

        bollingerMiddleSeries.setData(
            []
        );
    }


    if (bollingerUpperSeries) {

        bollingerUpperSeries.setData(
            []
        );
    }


    if (bollingerLowerSeries) {

        bollingerLowerSeries.setData(
            []
        );
    }


    if (priceChart) {

        priceChart
            .timeScale()
            .fitContent();

        priceChart
            .priceScale("right")
            .applyOptions({
                autoScale: true,
            });
    }
}


/* ============================================================
   UPDATE CHART
   ============================================================ */

function updateChart(
    candles,
    indicators = null
) {

    if (
        !priceChart ||
        !candleSeries ||
        !Array.isArray(candles) ||
        !candles.length
    ) {

        return;
    }


    /* ========================================================
       CANDLE DATA
       ======================================================== */

    const chartData =
        candles
            .map(
                candle => {

                    let timestamp =
                        Number(
                            candle.timestamp
                        );


                    /*
                     * Lightweight Charts expects
                     * Unix timestamps in seconds.
                     */

                    if (
                        timestamp >
                        10_000_000_000
                    ) {

                        timestamp =
                            Math.floor(
                                timestamp / 1000
                            );
                    }


                    return {

                        time:
                            timestamp,

                        open:
                            Number(
                                candle.open
                            ),

                        high:
                            Number(
                                candle.high
                            ),

                        low:
                            Number(
                                candle.low
                            ),

                        close:
                            Number(
                                candle.close
                            ),
                    };
                }
            )
            .filter(
                candle =>

                    Number.isFinite(
                        candle.time
                    )

                    &&

                    Number.isFinite(
                        candle.open
                    )

                    &&

                    Number.isFinite(
                        candle.high
                    )

                    &&

                    Number.isFinite(
                        candle.low
                    )

                    &&

                    Number.isFinite(
                        candle.close
                    )
            );


    /* ========================================================
       REMOVE DUPLICATES
       ======================================================== */

    const uniqueData = [];

    const seen =
        new Set();


    for (
        const candle of chartData
    ) {

        if (
            seen.has(
                candle.time
            )
        ) {

            continue;
        }


        seen.add(
            candle.time
        );


        uniqueData.push(
            candle
        );
    }


    /* --------------------------------------------------------
       CHRONOLOGICAL ORDER
       -------------------------------------------------------- */

    uniqueData.sort(
        (
            a,
            b
        ) =>
            a.time - b.time
    );


    /* --------------------------------------------------------
       SET CANDLES
       -------------------------------------------------------- */

    candleSeries.setData(
        uniqueData
    );


    /* ========================================================
       VOLUME
       ======================================================== */

    const volumeData =
        candles
            .map(
                candle => {

                    let timestamp =
                        Number(
                            candle.timestamp
                        );


                    if (
                        timestamp >
                        10_000_000_000
                    ) {

                        timestamp =
                            Math.floor(
                                timestamp / 1000
                            );
                    }


                    const volume =
                        Number(
                            candle.volume
                        );


                    if (
                        !Number.isFinite(
                            timestamp
                        )
                        ||
                        !Number.isFinite(
                            volume
                        )
                    ) {

                        return null;
                    }


                    const open =
                        Number(
                            candle.open
                        );

                    const close =
                        Number(
                            candle.close
                        );


                    return {

                        time:
                            timestamp,

                        value:
                            volume,

                        color:
                            close >= open
                                ? "#26a69a"
                                : "#ef5350",
                    };
                }
            )
            .filter(
                item =>
                    item !== null
            );


    if (volumeSeries) {

        volumeSeries.setData(
            volumeData
        );
    }


    /* ========================================================
       INDICATORS
       ======================================================== */

    if (indicators) {

        updateIndicatorSeries(
            candles,
            indicators
        );

    } else {

        /*
         * If indicators are unavailable,
         * clear old indicator lines.
         */

        clearIndicatorSeries();
    }


    /* ========================================================
       FIT NEW MARKET DATA
       ======================================================== */

    /*
     * This is important when switching from
     * BTC (~100,000 USD) to DOGE (~0.07 USD).
     *
     * The chart recalculates its visible range
     * using the new asset's actual price.
     */

    priceChart
        .priceScale("right")
        .applyOptions({
            autoScale: true,
        });


    priceChart
        .timeScale()
        .fitContent();
}


/* ============================================================
   INDICATOR SERIES
   ============================================================ */

function updateIndicatorSeries(
    candles,
    indicators
) {

    if (!indicators) {

        clearIndicatorSeries();

        return;
    }


    const movingAverages =
        indicators
            .moving_averages;


    const volatility =
        indicators
            .volatility;


    /* ========================================================
       MOVING AVERAGES
       ======================================================== */

    if (
        movingAverages &&
        movingAverages.series
    ) {

        const maSeries =
            movingAverages.series;


        /* ----------------------------------------------------
           SMA 20
           ---------------------------------------------------- */

        setLineSeriesData(
            sma20Series,
            candles,
            maSeries.sma_20
        );


        /* ----------------------------------------------------
           SMA 50
           ---------------------------------------------------- */

        setLineSeriesData(
            sma50Series,
            candles,
            maSeries.sma_50
        );


        /* ----------------------------------------------------
           EMA 20
           ---------------------------------------------------- */

        setLineSeriesData(
            ema20Series,
            candles,
            maSeries.ema_20
        );

    } else {

        if (sma20Series) {

            sma20Series.setData(
                []
            );
        }


        if (sma50Series) {

            sma50Series.setData(
                []
            );
        }


        if (ema20Series) {

            ema20Series.setData(
                []
            );
        }
    }


    /* ========================================================
       BOLLINGER BANDS
       ======================================================== */

    if (
        volatility &&
        volatility.bollinger_bands &&
        volatility
            .bollinger_bands
            .series
    ) {

        const series =
            volatility
                .bollinger_bands
                .series;


        /* ----------------------------------------------------
           MIDDLE
           ---------------------------------------------------- */

        setLineSeriesData(
            bollingerMiddleSeries,
            candles,
            series.middle
        );


        /* ----------------------------------------------------
           UPPER
           ---------------------------------------------------- */
                                       
