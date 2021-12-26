from decimal import Decimal
from typing import Any

import httpx

from stablecoin_rates.model import LendingRate

HUOBI_ASSETS = {"USDC", "USDT", "UST"}
FEATURED_URL = "https://www.huobi.com/-/x/hbg/v1/saving/mining/index/limitTime/list"
FIXED_URL = "https://www.huobi.com/-/x/hbg/v1/saving/mining/index/fixed/list"
FLEXIBLE_URL = "https://www.huobi.com/-/x/hbg/v1/saving/mining/index/active/list"


async def get_huobi_flexible_rates() -> list[LendingRate]:
    async with httpx.AsyncClient() as client:
        flexible_rates_response = await client.get(FLEXIBLE_URL)
        flexible_rates_json_response = flexible_rates_response.json(
            parse_float=Decimal, parse_int=Decimal
        )

    return parse_huobi_flexible_rates(flexible_rates_json_response)


def parse_huobi_flexible_rates(response: dict[str, Any]) -> list[LendingRate]:
    data = response["data"]

    rates = [
        LendingRate(
            asset=rate["currency"],
            platform="Huobi",
            apr=rate["day7YearRate"],
            project_name="Flexible",
        )
        for rate in data
        if rate["currency"] in HUOBI_ASSETS
    ]

    return rates


async def get_huobi_fixed_rates() -> list[LendingRate]:
    async with httpx.AsyncClient() as client:
        fixed_rates_response = await client.get(FIXED_URL)
        fixed_rates_json_response = fixed_rates_response.json(
            parse_float=Decimal, parse_int=Decimal
        )

    return parse_huobi_fixed_rates(fixed_rates_json_response)


def parse_huobi_fixed_rates(response: dict[str, Any]) -> list[LendingRate]:
    data = response["data"]

    rates = [
        LendingRate(
            asset=currency_projects["currency"],
            platform="Huobi",
            apr=Decimal(rate["viewYearRate"]),
            project_name="Fixed",
            duration=rate["term"],
        )
        for currency_projects in data
        for rate in currency_projects["projects"]
        if currency_projects["currency"] in HUOBI_ASSETS and rate["allowBuy"]
    ]

    return rates


async def get_huobi_featured_rates() -> list[LendingRate]:
    async with httpx.AsyncClient() as client:
        featured_rates_response = await client.get(FEATURED_URL)
        featured_rates_json_response = featured_rates_response.json(
            parse_float=Decimal, parse_int=Decimal
        )

    return parse_huobi_featured_rates(featured_rates_json_response)


def parse_huobi_featured_rates(response: dict[str, Any]) -> list[LendingRate]:
    data = response["data"]

    rates = [
        LendingRate(
            asset=rate["currency"],
            platform="Huobi",
            apr=Decimal(rate["viewYearRate"]),
            project_name="Featured",
            duration=rate["term"],
        )
        for rate in data
        if rate["currency"] in HUOBI_ASSETS and rate["projectStatus"] == 1
    ]

    return rates
