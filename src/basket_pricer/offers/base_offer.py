import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from src.basket_pricer.models import Basket, Money
from src.basket_pricer.utils.exceptions import InvalidOfferConfigError

logger = logging.getLogger(__name__)


@dataclass
class AbstractBaseOffer(ABC):
    id: str
    name: str

    def __post_init__(self):
        if not self.id:
            raise InvalidOfferConfigError(f"Offer {self.name} must have an Id.")
        if not self.name or not self.name.split():
            raise InvalidOfferConfigError(f"Offer {self.name} must have a Name.")
        logger.debug(f"Created Offer : {self.name} with id : '{self.id}'")

    @abstractmethod
    def calculate_discount(self, basket: Basket) -> Money:
        raise NotImplementedError(
            "Subclasses must implement calculate_discount function"
        )

    @abstractmethod
    def is_applicable(self, basket: Basket):
        raise NotImplementedError("Subclasses must implement is_applicable function")

    def _get_affected_items(self, basket: Basket) -> List[str]:
        """For basic, and can be override"""
        basket_items = basket.get_items_list()
        item = basket_items[self.sku]
        product_name = item.product.name
        return [product_name]

    def apply_to_basket(self, basket: Basket) -> Optional[tuple[Money, List[str]]]:
        """Apply offer to basket items"""
        # check basket is empty or not
        if basket.is_empty():
            return None

        # check if APPLICABLE
        if not self.is_applicable(basket):
            logger.debug(f"offer {self.name} not applicable on the current basket")
            return None

        discount = self.calculate_discount(basket)
        if discount.is_zero():
            logger.debug("Offer applicable but zero discount")
            return None

        # names of affected items
        affected_items = self._get_affected_items(basket)
        logger.info(f"offer {self.name} applied")

        return discount, affected_items
