from decimal import Decimal
from typing import Any

import httpx

from stablecoin_rates.model import LendingRate

RATES_URL = "https://blockfi.com/page-data/rates/page-data.json"
ASSETS = {"USDC (Tier 1)", "USDT (Tier 1)"}


async def get_blockfi_rates() -> list[LendingRate]:
    async with httpx.AsyncClient() as client:
        response = await client.get(RATES_URL)
        json_response = response.json(parse_float=Decimal, parse_int=Decimal)

    return parse_blockfi_rate(json_response)


def parse_blockfi_rate(response: dict[str, Any]) -> list[LendingRate]:
    platform = "BlockFi"
    rates = response["result"]["data"]["allContentfulPageRates"]["nodes"][0][
        "interestAccountRates"
    ]["rates"]

    # [
    #     {
    #         "currency": "USDC (Tier 1)",
    #         "amount": "0 - 40,000 USDC",
    #         "apy": "9%"
    #     },
    #     {
    #         "currency": "USDC (Tier 2)",
    #         "amount": "> 40,000 USDC",
    #         "apy": "8%"
    #     },
    #     {
    #         "currency": "USDT (Tier 1)",
    #         "amount": "0 - 40,000 USDT",
    #         "apy": "9.5%"
    #     },
    # ]

    return [
        LendingRate(
            asset=rate["currency"],
            platform=platform,
            apy=Decimal(rate["apy"].replace("%", "")) / 100,
            duration=None,
            project_name="Interest Account",
        )
        for rate in rates
        if rate["currency"] in ASSETS
    ]
