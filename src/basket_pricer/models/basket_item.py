from dataclasses import dataclass

@dataclass
class BasketItem:
    sku: int
    qty : int

    def __post_init__(self):
        if self.qty<=0:
            raise ValueError(f"Basket item quantity must be positive, got : {self.qty}")
