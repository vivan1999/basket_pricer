import logging
from dataclasses import dataclass
from decimal import Decimal

from src.basket_pricer.utils import exceptions

from .money import Money

logger = logging.getLogger(__name__)


@dataclass
class Product:
    sku: int
    name: str
    price: int | str | float | Decimal | Money

    def __post_init__(self):
        if not self.name or not self.name.strip():
            logger.error("Product name cannot be empty.")
            raise exceptions.PricerException(
                f"Product name is required and cannot be empty for sku: {self.sku}"
            )
        if not isinstance(self.price, Money):
            logger.info("Price entered is not of type Money")
            self.price = Money(amount=self.price)

        if not self.price.is_positive():
            logger.error("Product price must be positive.")
            raise ValueError(f"Price must be positive: sku {self.sku}")

        logger.debug(f"Product created {self.name} with price {self.price}")

    def __str__(self):
        return f"Product {self.name} : {self.price}"

    def __repr__(self):
        return f"Product(name='{self.name}', price: {self.price})"
