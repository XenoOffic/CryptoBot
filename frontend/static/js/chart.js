let priceChart = null;
let candleSeries = null;


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


    container.innerHTML = "";


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
                },

                timeScale: {
                    borderColor:
                        "#252d3b",

                    timeVisible: true,

                    secondsVisible: false,
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


    candleSeries =
        priceChart.addSeries(
            LightweightCharts
                .CandlestickSeries,
            {
                upColor: "#26a69a",

                downColor: "#ef5350",

                borderVisible: false,

                wickUpColor: "#26a69a",

                wickDownColor: "#ef5350",
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
    candles
) {

    if (
        !candleSeries ||
        !candles ||
        !candles.length
    ) {
        return;
    }


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
                     *
                     * CoinGecko may return
                     * milliseconds.
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
                        time: timestamp,

                        open: Number(
                            candle.open
                        ),

                        high: Number(
                            candle.high
                        ),

                        low: Number(
                            candle.low
                        ),

                        close: Number(
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


    /*
     * Remove duplicate timestamps.
     */

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


    priceChart
        .timeScale()
        .fitContent();
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
