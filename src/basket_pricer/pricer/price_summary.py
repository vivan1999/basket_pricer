from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class PriceSummary:
    sub_total : Decimal
    discount : Decimal
    total_amount : Decimal

    def __repr__(self):
        return (f"\nsub total : {self.sub_total}\n"
                f"discount : {self.discount}\n"
                f"total: {self.total_amount}")
    