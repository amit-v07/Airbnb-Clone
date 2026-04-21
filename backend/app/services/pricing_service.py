"""Pricing service — composes multiple pricing strategies."""

from datetime import date
from decimal import Decimal
from typing import List

from app.strategies.base_strategy import BasePricingStrategy
from app.strategies.holiday_pricing import HolidayPricingStrategy
from app.strategies.occupancy_pricing import OccupancyPricingStrategy
from app.strategies.surge_pricing import SurgePricingStrategy
from app.strategies.urgency_pricing import UrgencyPricingStrategy


class PricingService:
    """
    Applies a chain of pricing strategies to calculate the final price per night.

    Strategies are applied in order; each one receives the output of the previous.
    The final total is then multiplied by the number of nights.
    """

    DEFAULT_STRATEGIES: List[BasePricingStrategy] = [
        HolidayPricingStrategy(),
        SurgePricingStrategy(),
        OccupancyPricingStrategy(),
        UrgencyPricingStrategy(),
    ]

    def __init__(
        self, strategies: List[BasePricingStrategy] | None = None
    ) -> None:
        self.strategies = strategies or self.DEFAULT_STRATEGIES

    def calculate_nightly_rate(
        self,
        base_price: Decimal,
        check_in: date,
        check_out: date,
        occupancy_rate: float = 0.0,
    ) -> Decimal:
        """Apply all strategies and return the final nightly rate."""
        price = base_price
        for strategy in self.strategies:
            price = strategy.calculate(price, check_in, check_out, occupancy_rate)
        return price.quantize(Decimal("0.01"))

    def calculate_total(
        self,
        base_price: Decimal,
        check_in: date,
        check_out: date,
        occupancy_rate: float = 0.0,
    ) -> Decimal:
        """Calculate the total price for the full booking duration."""
        nights = (check_out - check_in).days
        if nights <= 0:
            return Decimal("0.00")
        nightly_rate = self.calculate_nightly_rate(
            base_price, check_in, check_out, occupancy_rate
        )
        return (nightly_rate * nights).quantize(Decimal("0.01"))
