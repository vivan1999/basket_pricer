import logging
from typing import Dict, Optional

from src.basket_pricer.utils.exceptions import CatalogueError

from .money import Money
from .product import Product

logger = logging.getLogger(__name__)


class Catalogue:

    def __init__(self, products: Optional[list[Product]] = None):
        self._products: Dict[int, Product] = {}  # [{sku, Product}]

        if products:
            for product in products:
                self.add_product(product=product)
        logger.debug(f"Catalogue with {len(self._products)} products created.")

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError(f"Expected product type, but got {type(product).__name__}")

        if product.sku in self._products:
            logger.error(f"'{product.name}' is already present in Catalogue")
            raise CatalogueError(
                f"SKU {product.sku} for {product.name} is already present in Catalogue"
            )

        self._products[product.sku] = product
        logger.info(f"Product '{product.name}' is added to the catalogue")

    def fetch_price(self, sku: int) -> Money:
        if sku not in self._products:
            logger.error(f"Product with sku {sku} not found in the catalogue")
            raise ValueError(f"Sku {sku} not found in catalogue")
        return self._products[sku].price

    def has_product(self, sku: int) -> bool:
        return sku in self._products

    def __str__(self):
        if not self._products:
            return "Catalogue(empty)"
        return f"Catalogue : {len(self._products)} Products"
