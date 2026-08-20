const form = document.getElementById(
    "analysis-form"
);

const symbolInput = document.getElementById(
    "symbol-input"
);

const analyzeButton = document.getElementById(
    "analyze-button"
);

const loading = document.getElementById(
    "loading"
);

const errorBox = document.getElementById(
    "error-box"
);

let priceChart = null;


/* ==========================================================
   HELPERS
========================================================== */

function formatNumber(
    value,
    decimals = 2
) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(value)
    ) {
        return "—";
    }

    return Number(value).toLocaleString(
        "en-US",
        {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals,
        }
    );
}


function formatPrice(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "—";
    }

    return "$" + Number(value).toLocaleString(
        "en-US",
        {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }
    );
}


function formatCompact(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "—";
    }

    const number = Number(value);

    if (number >= 1e12) {
        return "$" + (
            number / 1e12
        ).toFixed(2) + "T";
    }

    if (number >= 1e9) {
        return "$" + (
            number / 1e9
        ).toFixed(2) + "B";
    }

    if (number >= 1e6) {
        return "$" + (
            number / 1e6
        ).toFixed(2) + "M";
    }

    if (number >= 1e3) {
        return "$" + (
            number / 1e3
        ).toFixed(2) + "K";
    }

    return "$" + number.toFixed(2);
}


function setText(
    id,
    value
) {

    const element =
        document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


function show(id) {

    document
        .getElementById(id)
        ?.classList
        .remove("hidden");
}


function hide(id) {

    document
        .getElementById(id)
        ?.classList
        .add("hidden");
}


/* ==========================================================
   SCORE BAR
========================================================== */

function setScore(
    scoreId,
    labelId,
    barId,
    component
) {

    const score =
        Number(component?.score ?? 0);

    setText(
        scoreId,
        formatNumber(score, 1)
    );

    setText(
        labelId,
        component?.label ?? "—"
    );

    const bar =
        document.getElementById(barId);

    if (bar) {

        bar.style.width =
            `${Math.max(
                0,
                Math.min(100, score)
            )}%`;

    }
}


/* ==========================================================
   CHART
========================================================== */

function renderChart(
    candles
) {

    const canvas =
        document.getElementById(
            "price-chart"
        );

    if (!canvas || !candles?.length) {
        return;
    }

    const labels = candles.map(
        candle => {

            const date =
                new Date(
                    candle.timestamp
                );

            return date.toLocaleDateString(
                "en-US",
                {
                    month: "short",
                    day: "numeric",
                }
            );

        }
    );


    const prices = candles.map(
        candle => candle.close
    );


    if (priceChart) {

        priceChart.destroy();

    }


    priceChart =
        new Chart(
            canvas,
            {
                type: "line",

                data: {

                    labels,

                    datasets: [
                        {
                            label: "Price",

                            data: prices,

                            borderWidth: 2,

                            pointRadius: 0,

                            tension: 0.25,

                            fill: true,

                            backgroundColor:
                                "rgba(124, 92, 255, 0.08)",

                            borderColor:
                                "#8f78ff",
                        }
                    ],

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    interaction: {
                        intersect: false,
                        mode: "index",
                    },

                    plugins: {

                        legend: {
                            display: false,
                        },

                    },

                    scales: {

                        x: {

                            grid: {
                                display: false,
                            },

                            ticks: {
                                color: "#687284",
                                maxTicksLimit: 7,
                            },

                        },

                        y: {

                            grid: {
                                color:
                                    "rgba(255,255,255,0.05)",
                            },

                            ticks: {

                                color:
                                    "#687284",

                                callback: value =>
                                    "$" +
                                    Number(
                                        value
                                    ).toLocaleString(
                                        "en-US"
                                    ),

                            },

                        },

                    },

                },

            }
        );

}


/* ==========================================================
   LEVELS
========================================================== */

function renderLevels(
    containerId,
    levels,
    prefix
) {

    const container =
        document.getElementById(
            containerId
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (!levels?.length) {

        container.innerHTML =
            `<div class="level">
                <span>No significant levels detected</span>
                <strong>—</strong>
            </div>`;

        return;
    }


    levels.forEach(
        (level, index) => {

            const element =
                document.createElement(
                    "div"
                );

            element.className =
                "level";

            element.innerHTML = `
                <span>
                    ${prefix}${index + 1}
                </span>

                <strong>
                    ${formatPrice(level)}
                </strong>
            `;

            container.appendChild(
                element
            );

        }
    );

}


/* ==========================================================
   INSIGHTS
========================================================== */

function renderList(
    containerId,
    items,
    emptyText
) {

    const container =
        document.getElementById(
            containerId
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (!items?.length) {

        const li =
            document.createElement(
                "li"
            );

        li.textContent =
            emptyText;

        container.appendChild(
            li
        );

        return;
    }


    items.forEach(
        item => {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                item;

            container.appendChild(
                li
            );

        }
    );

}


/* ==========================================================
   RENDER ANALYSIS
========================================================== */

function renderAnalysis(
    data
) {

    const market =
        data.market;

    const indicators =
        data.indicators;

    const score =
        data.score;

    const report =
        data.report;

    const structure =
        data.structure;

    const levels =
        data.support_resistance;


    /* ------------------------------------------------------
       ASSET
    ------------------------------------------------------ */

    setText(
        "asset-symbol",
        market.symbol
    );

    setText(
        "asset-name",
        market.name
    );

    setText(
        "asset-price",
        formatPrice(
            market.price
        )
    );


    const changeElement =
        document.getElementById(
            "asset-change"
        );


    const change =
        Number(
            market.change_24h ?? 0
        );


    changeElement.textContent =
        `${change >= 0 ? "+" : ""}${formatNumber(
            change,
            2
        )}%`;


    changeElement.className =
        "asset-change " +
        (
            change >= 0
                ? "positive"
                : "negative"
        );


    setText(
        "market-cap",
        formatCompact(
            market.market_cap
        )
    );

    setText(
        "volume",
        formatCompact(
            market.volume_24h
        )
    );


    /* ------------------------------------------------------
       SCORE
    ------------------------------------------------------ */

    setText(
        "overall-score",
        formatNumber(
            score.overall,
            1
        )
    );

    setText(
        "overall-label",
        score.label
    );


    const overallBar =
        document.getElementById(
            "overall-bar"
        );


    if (overallBar) {

        overallBar.style.width =
            `${score.overall}%`;

    }


    setScore(
        "trend-score",
        "trend-label",
        "trend-bar",
        score.trend
    );


    setScore(
        "momentum-score",
        "momentum-label",
        "momentum-bar",
        score.momentum
    );


    setScore(
        "volatility-score",
        "volatility-label",
        "volatility-bar",
        score.volatility
    );


    setScore(
        "structure-score",
        "structure-label",
        "structure-bar",
        score.structure
    );


    /* ------------------------------------------------------
       REPORT
    ------------------------------------------------------ */

    setText(
        "market-bias",
        report.market_bias
    );

    setText(
        "confidence",
        report.confidence
    );

    setText(
        "summary-text",
        report.summary
    );


    /* ------------------------------------------------------
       INDICATORS
    ------------------------------------------------------ */

    setText(
        "rsi",
        formatNumber(
            indicators.rsi,
            2
        )
    );

    setText(
        "macd",
        formatNumber(
            indicators.macd,
            4
        )
    );

    setText(
        "ema20",
        formatPrice(
            indicators.ema_20
        )
    );

    setText(
        "ema50",
        formatPrice(
            indicators.ema_50
        )
    );

    setText(
        "ema200",
        formatPrice(
            indicators.ema_200
        )
    );

    setText(
        "atr",
        formatPrice(
            indicators.atr
        )
    );


    /* ------------------------------------------------------
       LEVELS
    ------------------------------------------------------ */

    renderLevels(
        "resistance-list",
        levels?.resistance,
        "R"
    );

    renderLevels(
        "support-list",
        levels?.support,
        "S"
    );


    /* ------------------------------------------------------
       INSIGHTS
    ------------------------------------------------------ */

    renderList(
        "strengths-list",
        report.strengths,
        "No major strengths detected."
    );

    renderList(
        "risks-list",
        report.risks,
        "No major risks detected."
    );


    /* ------------------------------------------------------
       CHART
    ------------------------------------------------------ */

    renderChart(
        data.candles
    );


    /* ------------------------------------------------------
       SHOW
    ------------------------------------------------------ */

    show("asset-header");
    show("score-grid");
    show("analysis-content");
    show("indicators-panel");
    show("levels-panel");
    show("insights-panel");

}


/* ==========================================================
   API
========================================================== */

async function analyze(
    symbol
) {

    const cleanSymbol =
        symbol
            .trim()
            .toUpperCase();


    if (!cleanSymbol) {

        throw new Error(
            "Enter a cryptocurrency symbol."
        );

    }


    hide("error-box");

    show("loading");

    hide("asset-header");
    hide("score-grid");
    hide("analysis-content");
    hide("indicators-panel");
    hide("levels-panel");
    hide("insights-panel");


    analyzeButton.disabled =
        true;


    analyzeButton.textContent =
        "Analyzing...";


    try {

        const response =
            await fetch(
                `/api/analysis/${encodeURIComponent(
                    cleanSymbol
                )}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Analysis failed."
            );

        }


        renderAnalysis(
            data
        );


    } catch (error) {

        const box =
            document.getElementById(
                "error-box"
            );

        box.textContent =
            error.message;

        show("error-box");


    } finally {

        hide("loading");

        analyzeButton.disabled =
            false;

        analyzeButton.innerHTML =
            `Analyze <span>→</span>`;

    }

}


/* ==========================================================
   FORM
========================================================== */

form.addEventListener(
    "submit",
    event => {

        event.preventDefault();

        analyze(
            symbolInput.value
        );

    }
);


/* ==========================================================
   INITIAL LOAD
========================================================== */

window.addEventListener(
    "DOMContentLoaded",
    () => {

        analyze("BTC");

    }
);
