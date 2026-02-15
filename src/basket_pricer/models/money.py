import logging
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Union

logger = logging.getLogger(__name__)


class Money:
    _amount: Decimal = Decimal("0")

    def __init__(self, amount: Union[int, str, float, Decimal]):
        try:
            decimal_amount = self.to_decimal(amount)
        except (ValueError, InvalidOperation) as e:
            logger.error("Invalid amount")
            logger.info(
                "only accepts number as a str, float, int, and decimal as the amount."
            )
            raise ValueError(f"Cannot convert {amount} to money (decimal)")

        if decimal_amount < 0:
            logger.error(f"The amount {decimal_amount} cannot be negative.")
            raise ValueError(f"Money {decimal_amount} cannot be negative.")

        self._amount = decimal_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        logger.debug(f"Money created (decimal conversion done) : {self._amount}")

    @property
    def amount(self):
        return self._amount

    @classmethod
    def zero(cls):
        return cls("0")

    def to_decimal(
        self, value: Union[int, str, float, Decimal]
    ) -> Decimal:  # handling all possible types of values
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    def is_positive(self):
        return self._amount > Decimal("0")

    def is_zero(self):
        return self._amount == Decimal("0")

    # important Arithmetic operations
    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise TypeError(f"Cannot add Money and {type(other).__name__}")
        return Money(self._amount + other._amount)

    def __sub__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise TypeError(f"Cannot subtract Money and {type(other).__name__}")
        return Money(self._amount - other._amount)

    def __mul__(self, multiplier: Union[int, float, str, Decimal]):
        if not isinstance(multiplier, (int, float, str, Decimal)):
            raise TypeError(f"Cannot multiply Money by {type(multiplier).__name__}")
        return Money(self._amount * self.to_decimal(multiplier))

    # Cmparison Operators
    def __eq__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            raise TypeError(f"Cannot compare Money and {type(other).__name__}")
        return self._amount == other._amount

    def __gt__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            raise TypeError(f"Cannot compare Money and {type(other).__name__}")
        return self._amount > other._amount

    def __lt__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            raise TypeError(f"Cannot compare Money and {type(other).__name__}")
        return self._amount < other._amount

    # representation of money
    def __str__(self):
        return f"£{self._amount:.2f}"

    def __repr__(self):
        pass
