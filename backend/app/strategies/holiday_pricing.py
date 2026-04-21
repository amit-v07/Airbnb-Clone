"""Holiday pricing strategy — increases price during public holidays."""

from datetime import date
from decimal import Decimal
from typing import Set

from app.strategies.base_strategy import BasePricingStrategy


# A simplified set of US/global holidays (month, day)
HOLIDAYS: Set[tuple[int, int]] = {
    (1, 1),   # New Year's Day
    (7, 4),   # Independence Day (US)
    (12, 24), # Christmas Eve
    (12, 25), # Christmas Day
    (12, 31), # New Year's Eve
    (11, 25), # Thanksgiving (approximate)
    (2, 14),  # Valentine's Day
    (10, 31), # Halloween
}

DEFAULT_HOLIDAY_MULTIPLIER = Decimal("1.30")  # +30% on holidays


class HolidayPricingStrategy(BasePricingStrategy):
    """Applies a premium multiplier when check-in falls on a public holiday."""

    def __init__(self, multiplier: Decimal = DEFAULT_HOLIDAY_MULTIPLIER) -> None:
        self.multiplier = multiplier

    def calculate(
        self,
        base_price: Decimal,
        check_in: date,
        check_out: date,
        occupancy_rate: float = 0.0,
    ) -> Decimal:
        if (check_in.month, check_in.day) in HOLIDAYS:
            return (base_price * self.multiplier).quantize(Decimal("0.01"))
        return base_price
