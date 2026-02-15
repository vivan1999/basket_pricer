from dataclasses import dataclass
from typing import List
from src.basket_pricer.models.money import Money
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class OfferApplied:
    offer_name : str
    products_effected: List[str]
    discount : Money

    def __post_init__(self):
        if not self.offer_name:
            logger.error("Offer applied must have name")
            raise ValueError("Offer Applied must have a name")
        if not self.products_effected:
            logger.error("List of products required")
            raise ValueError("List of products required on which the offer is applied")
        if self.discount<Money("0"):
            raise ValueError("Discount must be greater than 0")
    
    def __str__(self):
        items_str = ", ".join(self.products_effected)
        return f"{self.offer_name}: -{self.discount} ({items_str})"
        