from typing import Callable, Awaitable

from stablecoin_rates.scraper.ftx import get_ftx_rates
from stablecoin_rates.scraper.model import LendingRate

SCRAPER_METHODS: list[Callable[[], Awaitable[list[LendingRate]]]] = [
    get_ftx_rates,
]

__all__ = ["SCRAPER_METHODS", "get_ftx_rates"]
