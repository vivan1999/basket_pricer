from src.basket_pricer.models.basket import Basket
from src.basket_pricer.models.basket_item import BasketItem
from src.basket_pricer.models.catalogue import Catalogue
from src.basket_pricer.models.product import Product
from src.basket_pricer.models.money import Money
from src.basket_pricer.pricer.basket_pricer import BasketPricer
from src.basket_pricer.offers.percentage_discount import PercentageOffer
from src.basket_pricer.offers.buy_x_get_y_free import BuyXgetYfree

pro1 = Product(sku = 1, name ="Baked Beans", price=Money("0.99"))
pro2 = Product(sku = 1, name ="Biscuits", price=Money("1.20"))
pro3 = Product(sku = 3, name ="Sardines", price=Money("1.89"))
pro4 = Product(sku = 4, name ="Shampoo (small)", price=Money("2.00"))
pro5 = Product(sku = 5, name ="Shampoo (medium)", price=Money("2.50"))
pro6 = Product(sku = 6, name ="Shampoo (large)", price=Money("3.50"))

catalogue = Catalogue([pro1, pro2, pro3, pro4, pro5,pro6
])

basket = Basket([
    BasketItem(product= pro1, qty = 2),
    BasketItem(product= pro2, qty = 3)
])

offers = [
    #PercentageOffer(2, 10.0),
    BuyXgetYfree(sku= 2,x=2,y=1)
]
pricer = BasketPricer()

summary = pricer.price(basket, catalogue, offers)
print(summary)
