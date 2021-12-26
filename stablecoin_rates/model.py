from decimal import Decimal
from typing import NamedTuple, Optional


class LendingRate(NamedTuple):
    asset: str
    platform: str
    apr: Decimal
    project_name: str = ""
    duration: Optional[str] = None
