from src.basket_pricer.offers.abc_offer import AbstractBaseOffer
from src.basket_pricer.utils import amount
from dataclasses import dataclass

@dataclass
class BuyXgetYfree(AbstractBaseOffer):
    sku: int # sku of the product on which this discount is valid
    x: int # number of product should be bought to avail this offer
    y: int # number of prod

    def calculate_discount(self, basket, catalogue):
        if not basket.has_product(self.sku):
            return amount.zero()
        quantity = basket.fetch_quantity(self.sku) # fetch total items present in the basket of this sku
        if quantity == 0:
            return amount.zero()
        unitPrice = catalogue.fetch_price(self.sku)
        minItems = self.x + self.y # minimum elements required for availing the offer
        groups = quantity // minItems
        return self.y * groups * unitPrice