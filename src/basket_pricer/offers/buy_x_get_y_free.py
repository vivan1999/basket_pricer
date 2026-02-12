from offers.abc_offer import AbstractBaseOffer
from src.basket_pricer.models.basket import Basket
from src.basket_pricer.models.catalogue import Catalogue

class BuyXgetYfree(AbstractBaseOffer):
    def __init__(self, x: int, y: int, basket: Basket, catalogue: Catalogue):
        pass
    
    def calculate_discount(self, basket, catalogue):
        return super().calculate_discount(basket, catalogue)