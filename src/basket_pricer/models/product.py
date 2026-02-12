from decimal import Decimal
from src.basket_pricer.utils import exceptions, amount

class Product:
    sku : int
    name : str
    price : int | float | str | Decimal
    _stock : int

    def __init__(self,sku , name, price, stock):
        self.sku = sku
        self.name = name
        self.price = amount.to_decimal(price)
        self._stock = stock

    def __repr__(self):
        return f"{self.sku} : {self.name}"
    
    def __post_init__(self):
        if not self.name:
            raise exceptions.PriceException(f"Product name is required for product id : {self.sku}")
        if self.price < 0:
            raise exceptions.PriceException(f"Price cannot be negative: sku {self.sku}")
        if self._stock < 0:
            raise ValueError(f"Stock cannot be negative of sku {self.sku}")
