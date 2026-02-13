from dataclasses import dataclass
from src.basket_pricer.models.product import Product
import logging
logger = logging.getLogger(__name__)

@dataclass
class BasketItem:
    product: Product
    qty : int

    def __post_init__(self):
        if not isinstance(self.product, Product):
            logger.error(f"product must be of type Product but recieved : {type(self.product).__name__}")
            raise TypeError(f"product must be of type Product but recieved : {type(self.product).__name__}")
        if self.qty<=0:
            logger.error(f"Quantity should be positive but recived: {self.qty}")
            raise ValueError(f"Basket item quantity must be positive but recieved : {self.qty}")
        
        logger.debug(f"Added {self.qty} items of {self.product.name} in the basket.")

    def total_price(self):
        return self.product.price * self.qty
    
    def __str__(self):
        return f"{self.product.name} x {self.qty} ({self.total_price()})"
    
    def __repr__(self) -> str:
        return (
            f"BasketItem(product=Product('{self.product.name}', {self.product.price!r}), "
            f"quantity={self.qty})"
        )
