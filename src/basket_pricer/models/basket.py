from typing import Dict
from decimal import Decimal

from src.basket_pricer.models.catalogue import Catalogue
from src.basket_pricer.models.basket_item import BasketItem

from src.basket_pricer.utils.exceptions import PriceException

class Basket:
    _items : Dict[int, int] = {} # [{sku, qty}]

    def __init__(self, items: list[BasketItem]):
        for item in items:
            if item.sku in self._items:
                self._items[item.sku] += item.qty
            else:
                self._items[item.sku] = item.qty
    
    def calculate_subtotal(self, catalogue: Catalogue):
        subTotal = Decimal("0")
        for sku, qty in self._items.items():
            if not catalogue.has_product(sku):
                raise PriceException(f"Product {sku} not in the catalogue")
            item_price = catalogue.fetch_price(sku)
            subTotal += item_price * qty
        return subTotal
    
    def has_product(self, sku):
        return sku in self._items
    
    def fetch_quantity(self, sku):
        return self._items.get(sku,0)


