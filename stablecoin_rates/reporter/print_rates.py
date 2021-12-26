import asyncio

from stablecoin_rates.scraper import SCRAPER_METHODS


async def main() -> None:
    results = await asyncio.gather(*(method() for method in SCRAPER_METHODS))
    rates = [r for rates in results for r in rates]

    rates = sorted(rates, key=lambda r: (r.asset, r.platform))

    for rate in rates:
        duration = f"{rate.duration}" if rate.duration else "Flexible"
        print(
            f"{rate.asset:>4} — {rate.platform:<6} {rate.project_name:<16} {duration:<8}: {rate.apr * 100:.2f}% APR"
        )


if __name__ == "__main__":
    asyncio.run(main())
