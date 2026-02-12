from src.basket_pricer.offers.abc_offer import AbstractBaseOffer
from dataclasses import dataclass
from src.basket_pricer.utils import amount
from decimal import Decimal

@dataclass
class PercentageOffer(AbstractBaseOffer):
    product_sku : int
    percentage: float = 0.0

    def calculate_discount(self, basket, catalogue):
        if not basket.has_product(self.product_sku):
            return amount.zero()
        
        total = catalogue.fetch_price(self.product_sku) * basket.fetch_quantity(sku=self.product_sku)
        percentage_decimal = Decimal(str(self.percentage)) / Decimal("100") # precise decimal percentage
        discount = total * percentage_decimal
        return discount
    
    
