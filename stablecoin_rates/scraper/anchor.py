from decimal import Decimal
from typing import Any

from stablecoin_rates.model import LendingRate
import httpx


# See https://github.com/Anchor-Protocol/anchor-earn/blob/master/src/facade/terra-anchor-earn.ts
BLOCKS_IN_YEAR = 4_656_810
ANCHOR_RATE_URL = "https://api.anchorprotocol.com/api/v2/deposit-rate"


async def get_anchor_rates() -> list[LendingRate]:

    async with httpx.AsyncClient() as client:
        response = await client.get(ANCHOR_RATE_URL)
        json_response = response.json(parse_float=Decimal, parse_int=Decimal)

    return parse_anchor_rate(json_response)


def parse_anchor_rate(response: list[dict[str, Any]]) -> list[LendingRate]:
    platform = "Anchor"
    rate = response[0]
    return [
        LendingRate(
            asset="UST",
            platform=platform,
            apy=Decimal(rate["deposit_rate"]) * BLOCKS_IN_YEAR,
            duration=None,
            project_name="Earn",
        )
    ]
