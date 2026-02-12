from src.basket_pricer.models.basket import Basket
from src.basket_pricer.models.basket_item import BasketItem
from src.basket_pricer.models.catalogue import Catalogue
from src.basket_pricer.models.product import Product
from decimal import Decimal
from src.basket_pricer.pricer.basket_pricer import BasketPricer
from src.basket_pricer.offers.percentage_discount import PercentageOffer

basket = Basket([
    BasketItem(1, 2),
    BasketItem(2, 1)
])

catalogue = Catalogue([
    Product(1, "Baked Beans", Decimal("0.99"), 2),
    Product(2, "Biscuits", Decimal("1.20"), 4),
])
offers = [
    PercentageOffer(2, 10.0)
]
pricer = BasketPricer()

summary = pricer.price(basket, catalogue, offers)
print(summary)
