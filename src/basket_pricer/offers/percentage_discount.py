from src.basket_pricer.offers.base_offer import AbstractBaseOffer
from dataclasses import dataclass
from src.basket_pricer.models.money import Money
from src.basket_pricer.models.basket import Basket
from src.basket_pricer.utils.exceptions import InvalidOfferConfigError
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

@dataclass
class PercentageOffer(AbstractBaseOffer):
    sku : int
    percentage: float = 0.0

    def __post_init__(self):
        super().__post_init__() # call the parents validations first
        if not self.sku:
            raise InvalidOfferConfigError("Product sku's must be provided in the config of Offer's")
        if self.percentage < 0:
            raise InvalidOfferConfigError(f"Percentage must be positive")
        logger.debug(f"{self.name} offer is created.")

    def is_applicable(self, basket: Basket):
        if not isinstance(basket,Basket):
            raise TypeError(f"Expected Basket Type, but got {type(basket).__name__}")
        is_applicable = basket.has_product(self.sku) # check if offer sku is present in the basket
        if not is_applicable:
            logger.debug(f"Offer not valid on the basket, it is only valid on SKU:{self.sku}")
        return is_applicable
    
    def calculate_discount(self, basket):
        if not isinstance(basket,Basket):
            raise TypeError(f"Expected Basket Type, but got {type(basket).__name__}")
        if not basket.has_product(self.sku):
            return Money.zero()
        product = basket.fetch_product(self.sku)
        total = product.price * basket.fetch_quantity(sku=self.sku)
        percentage_decimal = Decimal(str(self.percentage)) / Decimal("100") # precise decimal percentage
        discount = total * percentage_decimal
        logger.debug(f"Calculated discount for offer '{self.name}', total discount: {discount}")
        return discount
    
    def __str__(self) -> str:
        return (
            f"{self.name} Offer on product sku : {self.sku}"
        )