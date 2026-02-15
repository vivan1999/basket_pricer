from dataclasses import dataclass
from src.basket_pricer.models.money import Money
from src.basket_pricer.pricer.offer_summary import OfferApplied
from typing import List

@dataclass(frozen=True)
class PriceSummary:
    sub_total : Money
    discount : Money
    total_amount : Money
    applied_offers: List[OfferApplied] = None

    def __post_init__(self):
        # sub total should be positive
        if self.sub_total< Money.zero():
            raise ValueError(f"Sub-total cannot be negative: {self.sub_total}")
        
        # discount must be greater than or equal to 0
        if self.discount < Money.zero():
            raise ValueError(f"Discount cannot be negative: {self.discount}")
        
        # discount can't exceed sub-total
        if self.discount > self.sub_total:
            raise ValueError(
                f"Discount ({self.discount}) cannot exceed sub-total ({self.sub_total})"
            )
        
        # total amount must be non-negative
        if self.total_amount < Money.zero():
            raise ValueError(f"Total cannot be negative: {self.total_amount}")
        
        # total amount must equal sub_total - discount
        expected_total = self.sub_total - self.discount
        if self.total_amount != expected_total:
            raise ValueError(
                f"Total amount must equal to {expected_total} but got {self.total_amount}")
        
    def has_discounts(self):
        return not self.discount.is_zero()
    
    def __repr__(self):
        return (f"\nSub total : {self.sub_total}\n"
                f"Discount : {self.discount}\n"
                f"Total: {self.total_amount}\n")
    
    def __str__(self):
        result = (
            "\nBill Summary:\n"
            f"Sub total : {self.sub_total}\n"
            f"Discount : {self.discount}\n"
            f"Total: {self.total_amount}\n")
        if self.applied_offers:
            result += f"Offers applied: {len(self.applied_offers)}\n"
            for offer_app in self.applied_offers:
                result += f"    - {offer_app}\n"
        else:
            result += "Offers applied: None\n"

        return result

def no_discount_summary(sub_total: Money) -> PriceSummary:
    return PriceSummary(
        sub_total=sub_total,
        discount=Money.zero(),
        total_amount=sub_total,
        applied_offers=[],
    )

def zero_summary() -> PriceSummary:
    zero = Money.zero()
    return PriceSummary(
        sub_total=zero,
        discount=zero,
        total=zero,
        applied_offers=[],
    )