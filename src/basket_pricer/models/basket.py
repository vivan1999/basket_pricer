from typing import Dict, Optional

from src.basket_pricer.models.catalogue import Catalogue
from src.basket_pricer.models.basket_item import BasketItem
from src.basket_pricer.models.money import Money

from src.basket_pricer.utils.exceptions import PricerException
import logging

logger = logging.getLogger(__name__)

class Basket:

    def __init__(self, items: Optional[list[BasketItem]]= None):
        self._items : Dict[int, BasketItem] = {} # [{sku, BasketItem}]
        if items:
            for item in items:
                self.add_item(item)
        logger.debug(f"Created Basket with total {len(self._items)} distinct products.")
    
    def calculate_subtotal(self, catalogue: Catalogue):
        sub_total = Money("0")
        for sku, basketItem in self._items.items():
            if not catalogue.has_product(sku):
                logger.error(f"Product '{basketItem.product.name}' from basket is not present in the catalogue")
                raise PricerException(f"Product {sku} not in the catalogue")
            item_price = catalogue.fetch_price(sku)
            basket_item_total = item_price * basketItem.qty
            sub_total = basket_item_total + sub_total
        return sub_total
    
    def add_item(self, basket_item : BasketItem)-> "Basket":
        if not isinstance(basket_item, BasketItem):
            logger.error(f"Must be of basket Item type and got {type(basket_item).__name__}")
            raise TypeError("Must be of Basket Item type.")
        if basket_item.qty<=0:
            logger.error("Product quantity must be greater than 0")
            raise ValueError("Quantity must be positive and greater than 0")
        if basket_item.product.sku in self._items:
            new_qty = self._items[basket_item.product.sku].qty + basket_item.qty
            self._items[basket_item.product.sku] = BasketItem(product=basket_item.product, qty=new_qty)
            logger.info("item with sku is already present and hence updated the quantity in the basket")
        else:
            self._items[basket_item.product.sku] = basket_item
            logger.info(f"item with sku {basket_item.product.sku} added in the basket")
        logger.debug(f"Added '{basket_item.product.name}' in Basket and now total {len(self._items)} distinct products are present in basket")
    
    def has_product(self, sku):
        return sku in self._items
    
    def fetch_quantity(self, sku):
        basket_item = self._items.get(sku, None)
        return basket_item.qty
    
    def is_empty(self):
        return len(self._items) == 0
    
    def __str__(self):
        if self.is_empty():
            return f"Basket(items=0)"
        return f"Basket(items={len(self._items)}"

    def __repr__(self):
        return f"Basket(items={len(self._items)})"


