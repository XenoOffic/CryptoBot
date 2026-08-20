async function fetchAnalysis(
    symbol,
    days
) {

    const url =
        `/api/analysis/${encodeURIComponent(
            symbol
        )}?days=${days}`;

    const response =
        await fetch(url);

    if (!response.ok) {

        let message =
            "Unable to retrieve analysis.";

        try {

            const data =
                await response.json();

            if (data.detail) {
                message = data.detail;
            }

        } catch {
            // Ignore invalid error body.
        }

        throw new Error(
            message
        );
    }

    return response.json();
}
