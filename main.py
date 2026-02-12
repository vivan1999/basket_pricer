from src.basket_pricer.models.basket import Basket
from src.basket_pricer.models.basket_item import BasketItem
from src.basket_pricer.models.catalogue import Catalogue
from src.basket_pricer.models.product import Product
from decimal import Decimal
from src.basket_pricer.pricer.basket_pricer import BasketPricer
from src.basket_pricer.offers.percentage_discount import PercentageOffer
from src.basket_pricer.offers.buy_x_get_y_free import BuyXgetYfree

basket = Basket([
    BasketItem(sku =1, qty = 2),
    BasketItem(sku = 2, qty = 9)
])

catalogue = Catalogue([
    Product(sku = 1, name ="Baked Beans", price=Decimal("0.99"), stock=5),
    Product(sku = 2, name = "Biscuits", price=Decimal("1"), stock=10),
])
offers = [
    #PercentageOffer(2, 10.0),
    BuyXgetYfree(sku= 2,x=2,y=1)
]
pricer = BasketPricer()

summary = pricer.price(basket, catalogue, offers)
print(summary)
