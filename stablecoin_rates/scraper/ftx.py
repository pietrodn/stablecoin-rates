from decimal import Decimal
from typing import Any

from stablecoin_rates.model import LendingRate
import httpx

FTX_ASSETS = {"USD", "USDT", "EUR"}


async def get_ftx_rates() -> list[LendingRate]:
    url = "https://ftx.com/api/spot_margin/lending_rates"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        json_response = response.json(parse_float=Decimal, parse_int=Decimal)

    return parse_ftx_rates(json_response)


def parse_ftx_rates(response: dict[str, Any]) -> list[LendingRate]:
    platform = "FTX"
    rates = response["result"]
    rates_by_asset = {
        rate["coin"]: LendingRate(
            asset=rate["coin"],
            platform=platform,
            apr=rate["previous"] * 24 * 365,
            duration=None,
            project_name="Margin lending",
        )
        for rate in rates
        if rate["coin"] in FTX_ASSETS
    }

    return list(rates_by_asset.values())
