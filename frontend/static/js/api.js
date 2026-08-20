/* ============================================================
   CRYPTOLYTICS — API CLIENT
   ============================================================ */


/* ============================================================
   CONFIGURATION
   ============================================================ */

const API_CONFIG = {

    baseUrl: "",

    timeout: 20000,

};


/* ============================================================
   GENERIC REQUEST
   ============================================================ */

async function apiRequest(
    url,
    options = {}
) {

    const controller =
        new AbortController();


    const timeoutId =
        setTimeout(
            () => {
                controller.abort();
            },
            API_CONFIG.timeout
        );


    try {

        const response =
            await fetch(
                url,
                {
                    ...options,

                    signal:
                        controller.signal,

                    headers: {
                        Accept:
                            "application/json",

                        ...(options.headers || {}),
                    },
                }
            );


        clearTimeout(
            timeoutId
        );


        /*
         * HTTP error
         */

        if (!response.ok) {

            let message =
                `Request failed (${response.status}).`;


            try {

                const data =
                    await response.json();


                if (
                    data &&
                    data.detail
                ) {

                    message =
                        data.detail;

                }

            } catch {

                /*
                 * Server did not return
                 * a valid JSON error body.
                 */

            }


            throw new Error(
                message
            );

        }


        /*
         * Validate JSON response.
         */

        const contentType =
            response.headers.get(
                "content-type"
            );


        if (
            !contentType ||
            !contentType.includes(
                "application/json"
            )
        ) {

            throw new Error(
                "Server returned an invalid response."
            );

        }


        return await response.json();


    } catch (error) {

        clearTimeout(
            timeoutId
        );


        /*
         * Request timeout.
         */

        if (
            error.name ===
            "AbortError"
        ) {

            throw new Error(
                "Request timed out. Check your connection and try again."
            );

        }


        /*
         * Network/server connection
         * problem.
         */

        if (
            error instanceof
            TypeError
        ) {

            throw new Error(
                "Unable to connect to the Cryptolytics server."
            );

        }


        /*
         * Preserve our custom errors.
         */

        throw error;

    }

}


/* ============================================================
   FETCH FULL ANALYSIS
   ============================================================ */

async function fetchAnalysis(
    symbol,
    days = 30
) {

    if (
        !symbol ||
        typeof symbol !== "string"
    ) {

        throw new Error(
            "Cryptocurrency symbol is required."
        );

    }


    const normalizedSymbol =
        symbol
            .trim()
            .toUpperCase();


    if (!normalizedSymbol) {

        throw new Error(
            "Cryptocurrency symbol is required."
        );

    }


    /*
     * Keep the client-side range
     * within the backend limits.
     */

    const normalizedDays =
        Math.min(
            Math.max(
                Number(days) || 30,
                1
            ),
            365
        );


    const url =
        `${API_CONFIG.baseUrl}/api/analysis/` +
        `${encodeURIComponent(
            normalizedSymbol
        )}` +
        `?days=${normalizedDays}`;


    return await apiRequest(
        url
    );

}


/* ============================================================
   FETCH MARKET SNAPSHOT
   ============================================================ */

async function fetchMarket(
    symbol
) {

    if (
        !symbol ||
        typeof symbol !== "string"
    ) {

        throw new Error(
            "Cryptocurrency symbol is required."
        );

    }


    const normalizedSymbol =
        symbol
            .trim()
            .toUpperCase();


    if (!normalizedSymbol) {

        throw new Error(
            "Cryptocurrency symbol is required."
        );

    }


    const url =
        `${API_CONFIG.baseUrl}/api/market/` +
        `${encodeURIComponent(
            normalizedSymbol
        )}`;


    return await apiRequest(
        url
    );

}


/* ============================================================
   FETCH SYSTEM STATUS
   ============================================================ */

async function fetchSystemStatus() {

    return await apiRequest(
        "/api/system"
    );

}


/* ============================================================
   FETCH HEALTH
   ============================================================ */

async function fetchHealth() {

    return await apiRequest(
        "/api/health"
    );

}
