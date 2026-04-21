"""Surge pricing strategy — weekend and peak-season premiums."""

from datetime import date
from decimal import Decimal

from app.strategies.base_strategy import BasePricingStrategy

# Peak months (June–August, December)
PEAK_MONTHS = {6, 7, 8, 12}

WEEKEND_MULTIPLIER = Decimal("1.15")   # +15% on weekends
PEAK_MONTH_MULTIPLIER = Decimal("1.25") # +25% in peak months


class SurgePricingStrategy(BasePricingStrategy):
    """
    Applies surge pricing for weekends and peak travel months.

    Both conditions can stack (weekend in peak month = both applied).
    """

    def calculate(
        self,
        base_price: Decimal,
        check_in: date,
        check_out: date,
        occupancy_rate: float = 0.0,
    ) -> Decimal:
        price = base_price

        # Weekend surcharge (Friday=4, Saturday=5)
        if check_in.weekday() in (4, 5):
            price = (price * WEEKEND_MULTIPLIER).quantize(Decimal("0.01"))

        # Peak season surcharge
        if check_in.month in PEAK_MONTHS:
            price = (price * PEAK_MONTH_MULTIPLIER).quantize(Decimal("0.01"))

        return price
