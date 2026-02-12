from src.basket_pricer.models.product import Product
from typing import Dict
from src.basket_pricer.utils.exceptions import PriceException
from decimal import Decimal

class Catalogue:
    _products: Dict[int, Product] = {} # [{sku, Product}]

    def __init__(self, products: list[Product]):
        for item in products:
            if item.sku in self._products:
                raise PriceException(f"SKU {item.sku} for {item.name} is already present in Catalogue")
            self._products[item.sku] = item

    def fetch_price(self, sku: int) -> Decimal:
        if sku not in self._products:
            raise PriceException(f"Product with sku {sku} not found.")
        return self._products[sku].price
    
    def has_product(self, sku: int) -> bool:
        return sku in self._products