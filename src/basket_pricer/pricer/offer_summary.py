from dataclasses import dataclass
from typing import List
from src.basket_pricer.models.money import Money
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class OfferApplied:
    name : str
    products_effected: List[str]
    discount : Money

    def __post_init__(self):
        if not self.name:
            logger.error("Offer applied must have name")
            raise ValueError("Offer Applied must have a name")
        