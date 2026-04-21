"""Occupancy-based pricing strategy — higher price at high occupancy."""

from datetime import date
from decimal import Decimal

from app.strategies.base_strategy import BasePricingStrategy


class OccupancyPricingStrategy(BasePricingStrategy):
    """
    Applies a tiered multiplier based on the hotel occupancy rate.

    Tiers:
        < 50%  — no adjustment
        50–75% — +10%
        75–90% — +20%
        > 90%  — +40%
    """

    def calculate(
        self,
        base_price: Decimal,
        check_in: date,
        check_out: date,
        occupancy_rate: float = 0.0,
    ) -> Decimal:
        if occupancy_rate >= 0.90:
            multiplier = Decimal("1.40")
        elif occupancy_rate >= 0.75:
            multiplier = Decimal("1.20")
        elif occupancy_rate >= 0.50:
            multiplier = Decimal("1.10")
        else:
            multiplier = Decimal("1.00")

        return (base_price * multiplier).quantize(Decimal("0.01"))
