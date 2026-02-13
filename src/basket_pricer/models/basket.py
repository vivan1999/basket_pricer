from typing import Dict
from decimal import Decimal

from src.basket_pricer.models.catalogue import Catalogue
from src.basket_pricer.models.basket_item import BasketItem

from src.basket_pricer.utils.exceptions import PriceException
import logging

logger = logging.getLogger(__name__)

class Basket:
    _items : Dict[int, BasketItem] = {} # [{sku, BasketItem}]

    def __init__(self, items: list[BasketItem]):
        for item in items:
            if item.product.sku in self._items:
                logger.info("item with sku is already present and hence updated the quantity in the basket")
                self._items[item.product.sku] += item.qty
            else:
                logger.info(f"item with sku {item.product.sku} added in the basket")
                self._items[item.product.sku] = item.qty
        logger.debug(f"Created Basket with total {len(self._items)} distinct products.")
    
    def calculate_subtotal(self, catalogue: Catalogue):
        sub_total = Decimal("0")
        for sku, basketItem in self._items.items():
            if not catalogue.has_product(sku):
                logger.error(f"Product '{basketItem.product.name}' from basket is not present in the catalogue")
                raise PriceException(f"Product {sku} not in the catalogue")
            item_price = catalogue.fetch_price(sku)
            sub_total += item_price * basketItem.qty
        return sub_total
    
    def has_product(self, sku):
        return sku in self._items
    
    def fetch_quantity(self, sku):
        return self._items.get(sku,0)
    
    def is_empty(self):
        return len(self._items) == 0
    
    def __str__(self):
        if self.is_empty():
            return f"Basket(items=0)"
        return f"Basket(items={len(self._items)}"

    def __repr__(self):
        return f"Basket(items={len(self._items)})"


