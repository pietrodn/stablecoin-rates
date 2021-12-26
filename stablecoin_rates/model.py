from decimal import Decimal
from typing import NamedTuple, Optional


class LendingRate(NamedTuple):
    asset: str
    platform: str
    apy: Decimal
    project_name: str = ""
    duration: Optional[str] = None


def base_rate_to_apy(base_rate: Decimal, num_periods: int) -> Decimal:
    return (1 + base_rate) ** num_periods - 1
