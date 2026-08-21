/* ============================================================
   CRYPTOLYTICS — APPLICATION STATE
   ============================================================ */

const AppState = {

    /* ========================================================
       MARKET
       ======================================================== */

    symbol: "BTC",

    days: 30,

    market: null,

    candles: [],


    /* ========================================================
       TECHNICAL ANALYSIS
       ======================================================== */

    indicators: {

        current_price: null,

        moving_averages: {
            sma_20: null,
            sma_50: null,
            ema_20: null,
        },

        momentum: {

            rsi_14: null,

            macd: {
                macd: null,
                signal: null,
                histogram: null,
            },

        },

        volatility: {

            atr_14: null,

            bollinger_bands: {
                middle: null,
                upper: null,
                lower: null,
                width: null,
            },

        },

        volume: {

            current: null,
            average: null,
            ratio: null,

        },

        trend: "insufficient_data",

    },


    /* ========================================================
       SIGNAL ENGINE
       ======================================================== */

    signal: {

        direction: "neutral",

        strength: 0,

        score: 0,

        confidence: 0,

        reasons: [],

    },


    /* ========================================================
       CHART SETTINGS
       ======================================================== */

    chart: {

        initialized: false,

        type: "candlestick",

        showSMA20: true,

        showSMA50: true,

        showEMA20: true,

        showBollingerBands: false,

        showVolume: false,

        showRSI: false,

    },


    /* ========================================================
       UI STATE
       ======================================================== */

    loading: false,

    error: null,

    lastUpdated: null,

};
