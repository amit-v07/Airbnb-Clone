"""Urgency pricing strategy — last-minute discounts or premiums."""

from datetime import date
from decimal import Decimal

from app.strategies.base_strategy import BasePricingStrategy

LAST_MINUTE_DAYS = 3     # Booking within 3 days
LAST_MINUTE_MULTIPLIER = Decimal("1.20")  # +20% urgency premium

ADVANCE_DAYS = 30        # Booking >30 days ahead
EARLY_BIRD_MULTIPLIER = Decimal("0.90")   # -10% early bird discount


class UrgencyPricingStrategy(BasePricingStrategy):
    """
    Adjusts price based on how far in advance the booking is made.

    - Last-minute (≤3 days): +20% urgency premium
    - Early bird (≥30 days): -10% discount
    - Otherwise: no adjustment
    """

    def calculate(
        self,
        base_price: Decimal,
        check_in: date,
        check_out: date,
        occupancy_rate: float = 0.0,
    ) -> Decimal:
        days_until_checkin = (check_in - date.today()).days

        if days_until_checkin <= LAST_MINUTE_DAYS:
            return (base_price * LAST_MINUTE_MULTIPLIER).quantize(Decimal("0.01"))

        if days_until_checkin >= ADVANCE_DAYS:
            return (base_price * EARLY_BIRD_MULTIPLIER).quantize(Decimal("0.01"))

        return base_price
