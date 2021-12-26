from typing import Callable, Awaitable

from stablecoin_rates.model import LendingRate
from stablecoin_rates.scraper.anchor import get_anchor_rates
from stablecoin_rates.scraper.ftx import get_ftx_rates
from stablecoin_rates.scraper.huobi import (
    get_huobi_flexible_rates,
    get_huobi_fixed_rates,
    get_huobi_featured_rates,
)
from stablecoin_rates.scraper.okex import get_okex_rates

SCRAPER_METHODS: list[Callable[[], Awaitable[list[LendingRate]]]] = [
    get_ftx_rates,
    get_okex_rates,
    get_huobi_flexible_rates,
    get_huobi_fixed_rates,
    get_huobi_featured_rates,
    get_anchor_rates,
]

__all__ = [
    "SCRAPER_METHODS",
    "get_ftx_rates",
    "get_okex_rates",
    "get_huobi_flexible_rates",
    "get_huobi_fixed_rates",
    "get_huobi_featured_rates",
    "get_anchor_rates",
]
