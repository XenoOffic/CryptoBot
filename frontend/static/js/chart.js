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
                         * Low-priced assets such as
                         * DOGE need additional decimals.
                         */

                        if (
                            numericPrice > 0 &&
                            numericPrice < 1
                        ) {

                            maximumFractionDigits =
                                6;

                        } else if (
                            numericPrice > 0 &&
                            numericPrice < 100
                        ) {

                            maximumFractionDigits =
                                4;
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


    clearIndicatorSeries();


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


    /*
     * Clear previous indicator data first.
     *
     * This is important when switching from
     * BTC to DOGE or from DOGE back to BTC.
     */

    clearIndicatorSeries();


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


    if (!chartData.length) {

        return;
    }


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


    /* ========================================================
       CHRONOLOGICAL ORDER
       ======================================================== */

    uniqueData.sort(
        (
            a,
            b
        ) =>
            a.time - b.time
    );


    /* ========================================================
       SET CANDLES
       ======================================================== */

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


                    const open =
                        Number(
                            candle.open
                        );

                    const close =
                        Number(
                            candle.close
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
    }


    /* ========================================================
       AUTO SCALE
       ======================================================== */

    priceChart
        .priceScale("right")
        .applyOptions({
            autoScale: true,
        });


    /* ========================================================
       FIT CONTENT
       ======================================================== */

    priceChart
        .timeScale()
        .fitContent();


    /*
     * Apply autoscale once more after the
     * visible range has changed.
     */

    requestAnimationFrame(
        () => {

            if (!priceChart) {
                return;
            }


            priceChart
                .priceScale("right")
                .applyOptions({
                    autoScale: true,
                });
        }
    );
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


        setLineSeriesData(
            sma20Series,
            candles,
            maSeries.sma_20
        );


        setLineSeriesData(
            sma50Series,
            candles,
            maSeries.sma_50
        );


        setLineSeriesData(
            ema20Series,
            candles,
            maSeries.ema_20
        );

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


        setLineSeriesData(
            bollingerMiddleSeries,
            candles,
            series.middle
        );


        setLineSeriesData(
            bollingerUpperSeries,
            candles,
            series.upper
        );


        setLineSeriesData(
            bollingerLowerSeries,
            candles,
            series.lower
        );
    }
}


/* ============================================================
   CLEAR INDICATOR SERIES
   ============================================================ */

function clearIndicatorSeries() {

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
}


/* ============================================================
   GENERIC LINE SERIES HELPER
   ============================================================ */

function setLineSeriesData(
    series,
    candles,
    values
) {

    if (
        !series ||
        !Array.isArray(candles) ||
        !Array.isArray(values)
    ) {

        return;
    }


    const data = [];


    const length =
        Math.min(
            candles.length,
            values.length
        );


    for (
        let index = 0;
        index < length;
        index++
    ) {

        const value =
            values[index];


        if (
            value === null ||
            value === undefined
        ) {

            continue;
        }


        const numericValue =
            Number(value);


        if (
            !Number.isFinite(
                numericValue
            )
        ) {

            continue;
        }


        let timestamp =
            Number(
                candles[index]
                    .timestamp
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


        if (
            !Number.isFinite(
                timestamp
            )
        ) {

            continue;
        }


        data.push({

            time:
                timestamp,

            value:
                numericValue,
        });
    }


    /*
     * Lightweight Charts expects
     * chronological and unique timestamps.
     */

    const uniqueData = [];

    const seen =
        new Set();


    for (
        const item of data
    ) {

        if (
            seen.has(
                item.time
            )
        ) {

            continue;
        }


        seen.add(
            item.time
        );


        uniqueData.push(
            item
        );
    }


    uniqueData.sort(
        (
            a,
            b
        ) =>
            a.time - b.time
    );


    series.setData(
        uniqueData
    );
}


/* ============================================================
   RESIZE
   ============================================================ */

function resizeChart() {

    if (!priceChart) {
        return;
    }


    const container =
        document.getElementById(
            "chart-container"
        );


    if (!container) {
        return;
    }


    const width =
        container.clientWidth;


    const height =
        container.clientHeight;


    if (
        width <= 0 ||
        height <= 0
    ) {

        return;
    }


    priceChart.resize(
        width,
        height
    );
}
