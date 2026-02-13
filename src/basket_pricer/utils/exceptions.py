from typing import Optional

# Base class 
class PricerException(Exception):
    "Base exception for all the errors"
    pass

# Basket Exceptions
class InvalidBasketError(PricerException):
    "Invalid Basket"
    pass

class EmptyBasketError(InvalidBasketError):
    "raised when basket is empty"
    pass

# Catalogue Errors
class CatalogueError(PricerException):
    "raised on any catalogue Errors"
    pass

class ProductNotFoundError(CatalogueError):
    def __init__(self, sku: int, product_name : str,  message : Optional[str] = None):
        self.product_name = product_name
        self.sku = sku
        if message is None:
            message = f"Product '{self.product_name}': sku {self.sku} not found in catalogue."
        super().__init__(message)

class DuplicateProductError(CatalogueError):
    def __init__(self, sku: int):
        self.sku = sku
        super().__init__(f"Product '{sku}' already exists in catalogue")

# Offer exceptions
