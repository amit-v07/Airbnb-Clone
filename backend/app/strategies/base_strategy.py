"""Abstract base pricing strategy."""

from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal


class BasePricingStrategy(ABC):
    """
    Abstract base class for all pricing strategies.
    
    Each strategy takes the current price and booking context,
    and returns a potentially modified price.
    """

    @abstractmethod
    def calculate(
        self,
        base_price: Decimal,
        check_in: date,
        check_out: date,
        occupancy_rate: float = 0.0,
    ) -> Decimal:
        """
        Apply the pricing strategy.

        Args:
            base_price: The current price per night before this strategy.
            check_in: Check-in date.
            check_out: Check-out date.
            occupancy_rate: Hotel occupancy as a 0.0–1.0 float.

        Returns:
            Modified price per night.
        """
        ...

    def __repr__(self) -> str:
        return f"<PricingStrategy: {self.__class__.__name__}>"
