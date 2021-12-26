from decimal import Decimal
from typing import Any

import pytest as pytest

from stablecoin_rates.model import LendingRate
from stablecoin_rates.scraper.ftx import get_ftx_rates, parse_ftx_rates, FTX_ASSETS


@pytest.mark.asyncio
async def test_ftx_scraping() -> None:
    rates = await get_ftx_rates()
    assert len(rates) == len(FTX_ASSETS)

    assert {r.asset for r in rates} == FTX_ASSETS
    assert all(isinstance(r.apy, Decimal) for r in rates)


@pytest.mark.parametrize(
    "response, parsed",
    [
        (
            {
                "success": True,
                "result": [
                    {
                        "coin": "1INCH",
                        "previous": Decimal("0.00000456"),
                        "estimate": Decimal("0.00000456"),
                    },
                    {
                        "coin": "AAPL",
                        "previous": Decimal("0.000001"),
                        "estimate": Decimal("0.000001"),
                    },
                    {
                        "coin": "USDT",
                        "previous": Decimal("0.000001"),
                        "estimate": Decimal("0.000002"),
                    },
                ],
            },
            [
                LendingRate(
                    asset="USDT",
                    apy=Decimal("0.000001") * 24 * 365,
                    platform="FTX",
                    project_name="Margin lending",
                )
            ],
        )
    ],
)
def test_parse_ftx_response(
    response: dict[str, Any], parsed: list[LendingRate]
) -> None:
    assert parse_ftx_rates(response) == parsed
