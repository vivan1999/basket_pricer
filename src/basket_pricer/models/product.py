import logging
from dataclasses import dataclass

from src.basket_pricer.models.money import Money
from src.basket_pricer.utils import exceptions

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Product:
    sku: int
    name: str
    price: Money

    def __post_init__(self):
        if not self.name or not self.name.strip():
            logger.error("Product name cannot be empty.")
            raise exceptions.PricerException(
                f"Product name is required and cannot be empty for sku: {self.sku}"
            )
        if not self.price.is_positive():
            logger.error("Product price must be positive.")
            raise ValueError(f"Price must be positive: sku {self.sku}")

        logger.debug(f"Product created {self.name} with price {self.price}")

    def __str__(self):
        return f"Product {self.name} : {self.price}"

    def __repr__(self):
        return f"Product(name='{self.name}', price: {self.price})"
