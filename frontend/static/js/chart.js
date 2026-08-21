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

function resetChartData() {
    if (candleSeries) {
        candleSeries.setData([]);
    }
   
    if (volumeSeries) {
        volumeSeries.setData([]);
    }

    if (sma20Series) {
        sma20Series.setData([])
    }

    if (sma50Series) {
        sma50Series.setData([]);
    }

    if (ema20Series) {
        ema20Series.setData([]);
    }

    if (bollingerMiddleSeries) {
        bollingerMiddleSeries.setData([]);
    }

    if (bollingerUpperSeries) {
        bollingerUpperSeries.setData([]);
    }

    if (bollingerLowerSeries) {
        bollingerLowerSeries.setData([]);
    }
}


    container.innerHTML = "";


    /* ========================================================
       MAIN CHART
        re======================================================== */

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

                        return new Intl
                            .NumberFormat(
                                "en-US",
                                {
                                    maximumFractionDigits:
                                        2,
                                }
                            )
                            .format(
                                price
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


    resizeChart();


    window.addEventListener(
        "resize",
        resizeChart
    );
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
        !candles ||
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
                     * Lightweight Charts
                     * expects Unix seconds.
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


    uniqueData.sort(
        (
            a,
            b
        ) =>
            a.time - b.time
    );


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


                    return {

                        time:
                            timestamp,

                        value:
                            volume,

                        color:
                            Number(
                                candle.close
                            )
                            >=
                            Number(
                                candle.open
                            )
                                ? "#26a69a"
                                : "#ef5350",
                    };
                }
            )
            .filter(
                item => item !== null
            );


    if (
        volumeSeries &&
        volumeData.length
    ) {

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
       FIT CONTENT
       ======================================================== */

    priceChart
        .timeScale()
        .fitContent();

    priceChart
        .priceScale("right")
        .applyOptions({
            autoScale: true,
        });
}


/* ============================================================
   INDICATOR SERIES
   ============================================================ */

function updateIndicatorSeries(
    candles,
    indicators
) {

    if (!indicators) {
        return;
    }


    const movingAverages =
        indicators
            .moving_averages;


    const volatility =
        indicators
            .volatility;


    if (!movingAverages) {
        return;
    }


    /* ========================================================
       MOVING AVERAGE DATA
       ======================================================== */

    const maSeries =
        movingAverages.series;


    if (!maSeries) {
        return;
    }


    /* ========================================================
       SMA 20
       ======================================================== */

    setLineSeriesData(
        sma20Series,
        candles,
        maSeries.sma_20
    );


    /* ========================================================
       SMA 50
       ======================================================== */

    setLineSeriesData(
        sma50Series,
        candles,
        maSeries.sma_50
    );


    /* ========================================================
       EMA 20
       ======================================================== */

    setLineSeriesData(
        ema20Series,
        candles,
        maSeries.ema_20
    );


    /* ========================================================
       BOLLINGER BANDS
       ======================================================== */

    if (
        volatility &&
        volatility.bollinger_bands
    ) {

        const bollinger =
            volatility
                .bollinger_bands;


        const series =
            bollinger.series;


        if (series) {

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


    series.setData(
        data
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


    priceChart.resize(
        container.clientWidth,
        container.clientHeight
    );
                   }
