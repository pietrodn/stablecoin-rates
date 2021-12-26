from decimal import Decimal
from typing import NamedTuple, Optional


class LendingRate(NamedTuple):
    asset: str
    platform: str
    apr: Decimal
    duration: Optional[str] = None
