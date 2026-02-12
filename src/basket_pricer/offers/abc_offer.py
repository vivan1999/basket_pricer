from abc import ABC, abstractmethod
from src.basket_pricer.models.basket import Basket
from src.basket_pricer.models.catalogue import Catalogue
from decimal import Decimal

class AbstractBaseOffer(ABC):

    @abstractmethod
    def calculate_discount(self, basket: Basket, catalogue: Catalogue)-> Decimal:
        pass