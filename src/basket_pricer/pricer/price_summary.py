from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class PriceSummary:
    subTotal : Decimal
    discount : Decimal
    totalAmount : Decimal
    