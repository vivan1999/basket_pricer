from src.basket_pricer.offers.base_offer import AbstractBaseOffer
from src.basket_pricer.models.money import Money
from src.basket_pricer.models.basket import Basket
from src.basket_pricer.utils.exceptions import InvalidOfferConfigError
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class BuyXgetYfree(AbstractBaseOffer):
    sku: int # sku of the product on which this discount is valid
    buy: int = 0 # number of product should be bought to avail this offer
    free: int = 0 # number of prod

    def __post_init__(self):
        super().__post_init__() # call the parents validations first
        if not self.sku:
            raise InvalidOfferConfigError("Product sku's must be provided in the config of Offer's")
        if self.buy < 0 or self.free < 0:
            raise InvalidOfferConfigError(f"X and Y in {self.name} must be positive")
        logger.debug(f"Buy {self.buy} get {self.free} free offer created.")

    def is_applicable(self, basket: Basket):
        is_applicable : bool = False
        if not isinstance(basket,Basket):
            raise TypeError(f"Expected Basket Type, but got {type(basket).__name__}")
        
        min_req_qty = self.buy + self.free
        if basket.has_product(self.sku): # if required sku for the offer is peresent in the basket
            prod_qty = basket.fetch_quantity(self.sku)
            is_applicable = prod_qty >= min_req_qty # if minimum required items are present in basket
        if not is_applicable:
            logger.debug(f"Offer not valid on the basket, as minimum {min_req_qty} product requirements are not fullfilled.")
            
        return is_applicable
    
    def calculate_discount(self, basket):
        if not isinstance(basket,Basket):
            raise TypeError(f"Expected Basket Type, but got {type(basket).__name__}")
        if not basket.has_product(self.sku):
            return Money.zero() # already checked in is_applicable()
        quantity = basket.fetch_quantity(self.sku) # fetch total items present in the basket of this sku
        product = basket.fetch_product(self.sku)
        unit_price = product.price
        min_items = self.buy + self.free # minimum elements required for availing the offer
        groups = quantity // min_items
        group_amount = unit_price * groups
        final_discount = group_amount * self.free
        logger.debug(f"Discount Calculated for offer '{self.name}' : {final_discount}")
        return final_discount
    
    def __str__(self) -> str:
        return (
            f"Buy {self.buy} Get {self.free} Free Offer on product sku : {self.sku}"
        )