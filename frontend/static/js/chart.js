let priceChart = null;
let candleSeries = null;


function initializeChart() {

    const container =
        document.getElementById(
            "chart-container"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    /*
     * The actual chart library will be
     * connected in the next step.
     *
     * Keeping chart initialization
     * isolated here allows us to change
     * the visualization layer without
     * touching the API layer.
     */

    const placeholder =
        document.createElement("div");

    placeholder.className =
        "chart-placeholder";

    placeholder.textContent =
        "Candlestick engine ready";

    container.appendChild(
        placeholder
    );
}


function updateChart(candles) {

    if (!candles || !candles.length) {
        return;
    }

    console.log(
        "Received candles:",
        candles.length
    );
}
