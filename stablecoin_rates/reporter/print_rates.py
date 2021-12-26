import asyncio

from stablecoin_rates.reporter.formatter import format_lending_rate_table
from stablecoin_rates.scraper import SCRAPER_METHODS


async def main() -> None:
    results = await asyncio.gather(*(method() for method in SCRAPER_METHODS))
    rates = [r for rates in results for r in rates]

    formatted_text = format_lending_rate_table(rates)
    print(formatted_text)


if __name__ == "__main__":
    asyncio.run(main())
