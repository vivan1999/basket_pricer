from src.basket_pricer.offers.abc_offer import AbstractBaseOffer
from src.basket_pricer.models.money import Money
from dataclasses import dataclass

@dataclass
class BuyXgetYfree(AbstractBaseOffer):
    sku: int # sku of the product on which this discount is valid
    x: int # number of product should be bought to avail this offer
    y: int # number of prod

    def calculate_discount(self, basket, catalogue):
        if not basket.has_product(self.sku):
            return Money.zero()
        quantity = basket.fetch_quantity(self.sku) # fetch total items present in the basket of this sku
        if quantity == 0:
            return Money.zero()
        unitPrice = catalogue.fetch_price(self.sku)
        minItems = self.x + self.y # minimum elements required for availing the offer
        groups = quantity // minItems
        group_amount = unitPrice * groups
        final_discount = group_amount * self.y
        return final_discount