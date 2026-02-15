from src.basket_pricer.models.basket import Basket
from src.basket_pricer.models.basket_item import BasketItem
from src.basket_pricer.models.catalogue import Catalogue
from src.basket_pricer.models.money import Money
from src.basket_pricer.models.product import Product
from src.basket_pricer.offers.buy_x_get_cheapest_free_offer import (
    BuyXGetCheapestFreeOffer,
)
from src.basket_pricer.offers.buy_x_get_y_free import BuyXgetYfree
from src.basket_pricer.offers.percentage_discount import PercentageOffer
from src.basket_pricer.pricer.basket_pricer import BasketPricer

pro1 = Product(sku=1, name="Baked Beans", price=Money("0.99"))
pro2 = Product(sku=2, name="Biscuits", price=Money("1.20"))
pro3 = Product(sku=3, name="Sardines", price=Money("1.89"))
pro4 = Product(sku=4, name="Shampoo (small)", price=Money("2.00"))
pro5 = Product(sku=5, name="Shampoo (medium)", price=Money("2.50"))
pro6 = Product(sku=6, name="Shampoo (large)", price=Money("3.50"))

catalogue = Catalogue([pro1, pro2, pro3, pro4, pro5, pro6])

basket = Basket(
    [
        BasketItem(product=pro4, qty=3),
        BasketItem(product=pro5, qty=1),
        BasketItem(product=pro6, qty=3),
    ]
)

offers = [
    PercentageOffer(id="percentage_10", name="10% Off", sku=5, percentage=10.0),
    PercentageOffer(id="percentage_10", name="10% Off", sku=6, percentage=10.0),
    BuyXgetYfree(id="buy2get1free", name="Buy 2 Get 1 Free", sku=4, buy=2, free=1),
    BuyXGetCheapestFreeOffer(
        id="buy3getcheapestfree",
        name="Buy 3 Get Cheapest free",
        product_skus=[4, 5, 6],
        quantity=3,
    ),
]
pricer = BasketPricer(catalogue=catalogue, offers=offers)

summary = pricer.calculate(basket)
print(summary)
