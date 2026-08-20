const form = document.getElementById("analysis-form");
const input = document.getElementById("symbol-input");

const quickButtons =
    document.querySelectorAll("[data-symbol]");


function normalizeSymbol(value) {
    return value
        .trim()
        .toUpperCase();
}


function showMessage(symbol) {

    const placeholder =
        document.getElementById(
            "analysis-placeholder"
        );

    placeholder.innerHTML = `
        <div class="placeholder-icon">
            ◈
        </div>

        <h2>
            ${symbol} selected
        </h2>

        <p>
            Analysis engine is being connected.
        </p>
    `;
}


form.addEventListener("submit", function(event) {

    event.preventDefault();

    const symbol =
        normalizeSymbol(input.value);

    if (!symbol) {
        input.focus();
        return;
    }

    showMessage(symbol);

    console.log(
        `Requested analysis for ${symbol}`
    );
});


quickButtons.forEach(function(button) {

    button.addEventListener(
        "click",
        function() {

            const symbol =
                button.dataset.symbol;

            input.value = symbol;

            showMessage(symbol);
        }
    );

});
