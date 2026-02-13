from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Union
import logging

logger = logging.getLogger(__name__)

class Money:
    _amount : Decimal = Decimal("0")

    def __init__(self, amount: Union[int, str, float, Decimal]):
        try:
            decimal_amount = self.to_decimal(amount)
        except (ValueError,InvalidOperation) as e:
            logger.error("Invalid amount")
            logger.info("only accepts str, float, int, and decimal as amount.")
            raise ValueError(f"Cannot convert {amount} to money (decimal)")

        if decimal_amount<0:
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

    def to_decimal(value: Union[int, str, float, Decimal]) -> Decimal: # handling all possible types of values
        if isinstance(value,Decimal):
            return value
        return Decimal(str(value))
    
    def is_positive(self):
        return self.amount > Decimal("0")
    
    def is_zero(self):
        return self.amount == Decimal("0")
    
    def __str__(self):
        return f"£{self._amount:.2f}"
    
    def __repr__(self):
        pass