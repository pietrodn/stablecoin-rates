from decimal import Decimal
from typing import Any

from stablecoin_rates.model import LendingRate
import httpx

OKX_ASSETS = {"USDC", "USDT", "UST", "TUSD"}


async def get_okx_rates() -> list[LendingRate]:
    url = "https://www.okx.com/v2/asset/balance/project-currency"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        json_response = response.json(parse_float=Decimal, parse_int=Decimal)

    return parse_okx_rates(json_response)


def parse_okx_rates(response: dict[str, Any]) -> list[LendingRate]:
    platform = "OKX"

    projects_by_currency = response["data"]
    rate_data = [
        LendingRate(
            asset=projects_dict["currencyName"],
            platform=platform,
            apy=r["rateRangeMaxCompar"] / 100,
            duration=f"{r['period']}" if r["period"] != "Flexible" else None,
            project_name=okx_project_name(r["projectName"]),
        )
        for projects_dict in projects_by_currency
        for r in projects_dict["projectList"]
        if projects_dict["currencyName"] in OKX_ASSETS
        and r["matchCapitalType"] == 0
        and r["projectName"] not in ("lending", "DUAL_CURRENCY_DEPOSIT")
        and r["productStatus"]
    ]

    return rate_data


def okx_project_name(raw_project_name: str) -> str:
    return {
        "lockMiningTime": "Staking",
        "financial": "Savings",
        "lending": "P2P loan",
    }.get(raw_project_name, raw_project_name)
