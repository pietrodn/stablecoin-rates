from stablecoin_rates.model import LendingRate
import termtables  # type: ignore
import termtables.styles  # type: ignore


def format_lending_rate_table(rates: list[LendingRate]) -> str:
    """Format the list of lending rates to be printed to the terminal."""

    rates = sorted(
        rates, key=lambda r: (r.platform, r.asset, r.project_name, r.duration)
    )

    formatted_rates = []

    for rate in rates:
        duration = str(rate.duration) if rate.duration is not None else "-"
        row = (
            rate.platform,
            rate.asset,
            rate.project_name,
            duration,
            f"{rate.apr*100:.1f}%",
        )
        formatted_rates.append(row)

    return termtables.to_string(
        formatted_rates,
        header=("Platform", "Asset", "Project", "Duration (days)", "APY"),
    )
