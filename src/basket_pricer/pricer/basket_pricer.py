from src.basket_pricer.models.basket import Basket
from src.basket_pricer.models.catalogue import Catalogue
from src.basket_pricer.offers.abc_offer import AbstractBaseOffer
from src.basket_pricer.pricer.price_summary import PriceSummary
from src.basket_pricer.models.money import Money

from typing import List

class BasketPricer:
    def price(self, basket: Basket, catalogue: Catalogue, offers: List[AbstractBaseOffer]) -> PriceSummary:
        subTotal = basket.calculate_subtotal(catalogue)
        total_discount = Money("0")
        for offer in offers:
            discount = offer.calculate_discount(basket=basket, catalogue=catalogue)
            if discount > Money("0"):
                total_discount = total_discount + discount
        
        if total_discount > subTotal:
            total_discount = subTotal # making free and no negative 

        total = subTotal - total_discount
        
        return PriceSummary(sub_total=subTotal, 
                            discount=total_discount, 
                            total_amount=total)

