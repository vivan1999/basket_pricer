from src.basket_pricer.models.money import Money
from src.basket_pricer.utils import exceptions
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Product:
    sku : int
    name : str
    price : Money
    _stock : int # optional (for future use)
    
    def __post_init__(self):
        if not self.name:
            logger.error("Product name cannot be empty.")
            raise exceptions.PriceException(f"Product name is required for product id : {self.sku}")
        if not self.price.is_positive():
            logger.error("Product price should be positive.")
            raise exceptions.PriceException(f"Price cannot be negative: sku {self.sku}")
        if self._stock < 0:
            raise ValueError(f"Stock cannot be negative {self.sku}")
        
        logger.debug(f"Product created {self.name} with price {self.price}")

    @property
    def stock(self):
        return self._stock

    def __str__(self):
        return f"Product {self.name} : {self.price}"

    def __repr__(self):
        return (
            f"Product(name='{self.name}', price: {self.product.price!r}), "
            f"stock={self.stock})"
        )