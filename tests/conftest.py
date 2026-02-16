import pytest

# Import all components
from src.basket_pricer.models import Basket, BasketItem, Catalogue, Money, Product
from src.basket_pricer.offers import (
    BuyXGetCheapestFreeOffer,
    BuyXgetYfree,
    PercentageOffer,
)
from src.basket_pricer.offers.offers_factory import OffersFactory

# ------- MONEY FIXTURES ----------


@pytest.fixture
def zero_money() -> Money:
    """Fixture for zero money amount."""
    return Money.zero()


@pytest.fixture
def standard_price() -> Money:
    """Fixture for standard test price (£10.00)."""
    return Money("10.00")


# ------- PRODUCT FIXTURES -------


@pytest.fixture
def beans_product() -> Product:
    """Fixture for Baked Beans product."""
    return Product(sku=1, name="Baked Beans", price=Money("0.99"))


@pytest.fixture
def biscuits_product() -> Product:
    """Fixture for Biscuits product."""
    return Product(sku=2, name="Biscuits", price=Money("1.20"))


@pytest.fixture
def sardines_product() -> Product:
    """Fixture for Sardines product."""
    return Product(sku=3, name="Sardines", price=Money("1.89"))


@pytest.fixture
def shampoo_small() -> Product:
    """Fixture for Small Shampoo product."""
    return Product(sku=4, name="Shampoo (Small)", price=Money("2.00"))


@pytest.fixture
def shampoo_medium() -> Product:
    """Fixture for Medium Shampoo product."""
    return Product(sku=5, name="Shampoo (Medium)", price=Money("2.50"))


@pytest.fixture
def shampoo_large() -> Product:
    """Fixture for Large Shampoo product."""
    return Product(sku=6, name="Shampoo (Large)", price=Money("3.50"))


# ------- BASKET ITEM FIXTURE -------


@pytest.fixture
def basket_item_beans_qty3(beans_product: Product) -> BasketItem:
    """basket item 1 fixture"""
    return BasketItem(product=beans_product, qty=3)


@pytest.fixture
def basket_item_beans_qty6(beans_product: Product) -> BasketItem:
    """basket item 1 fixture"""
    return BasketItem(product=beans_product, qty=6)


@pytest.fixture
def basket_item2(biscuits_product: Product) -> BasketItem:
    """basket item 2 fixture"""
    return BasketItem(product=biscuits_product, qty=1)


@pytest.fixture
def basket_item_sardiness_qty1(sardines_product: Product) -> BasketItem:
    """basket item 3 fixture"""
    return BasketItem(product=sardines_product, qty=1)


@pytest.fixture
def basket_item_sardiness_qty3(sardines_product: Product) -> BasketItem:
    """basket item 3 fixture"""
    return BasketItem(product=sardines_product, qty=3)


@pytest.fixture
def basket_item_shampoo_small_qty2(shampoo_small: Product) -> BasketItem:
    """basket item 3 fixture"""
    return BasketItem(product=shampoo_small, qty=2)


@pytest.fixture
def basket_item_shampoo_medium_qty1(shampoo_medium: Product) -> BasketItem:
    """basket item 3 fixture"""
    return BasketItem(product=shampoo_medium, qty=1)


@pytest.fixture
def basket_item_shampoo_large_qty3(shampoo_large: Product) -> BasketItem:
    """basket item 3 fixture"""
    return BasketItem(product=shampoo_large, qty=3)


# ------- BASKET FIXTURES -------


@pytest.fixture
def empty_basket() -> Basket:
    """Fixture for empty basket."""
    return Basket()


@pytest.fixture
def basket_with_beans(
    empty_basket: Basket, basket_item_beans_qty3: BasketItem
) -> Basket:
    """Fixture for basket with 3 Baked Beans."""
    empty_basket.add_item(basket_item_beans_qty3)
    return empty_basket


@pytest.fixture
def basket_with_beans_qty6(
    empty_basket: Basket, basket_item_beans_qty6: BasketItem
) -> Basket:
    """Fixture for basket with 3 Baked Beans."""
    empty_basket.add_item(basket_item_beans_qty6)
    return empty_basket


@pytest.fixture
def basket_with_sardiness_qty1(
    empty_basket: Basket, basket_item_sardiness_qty1: BasketItem
) -> Basket:
    """Fixture for basket with 3 Baked Beans."""
    empty_basket.add_item(basket_item_sardiness_qty1)
    return empty_basket


@pytest.fixture
def basket_with_sardiness_qty3(
    empty_basket: Basket, basket_item_sardiness_qty3: BasketItem
) -> Basket:
    """Fixture for basket with 3 Baked Beans."""
    empty_basket.add_item(basket_item_sardiness_qty3)
    return empty_basket


@pytest.fixture
def basket_with_shampoo_small_qty2(
    empty_basket: Basket, basket_item_shampoo_small_qty2: BasketItem
) -> Basket:
    """Fixture for basket with mixed items."""
    empty_basket.add_item(basket_item_shampoo_small_qty2)
    return empty_basket


@pytest.fixture
def basket_with_mixed_items(
    empty_basket: Basket,
    basket_item2: BasketItem,
    basket_item_sardiness_qty1: BasketItem,
    basket_item_beans_qty3: BasketItem,
) -> Basket:
    """Fixture for basket with mixed items."""
    empty_basket.add_item(basket_item_beans_qty3)
    empty_basket.add_item(basket_item_sardiness_qty1)
    return empty_basket


@pytest.fixture
def basket_with_shampoo_scenario(
    empty_basket: Basket,
    basket_item_shampoo_large_qty3: BasketItem,
    basket_item_shampoo_medium_qty1: BasketItem,
    basket_item_shampoo_small_qty2: BasketItem,
) -> Basket:
    """Fixture for basket with 3 Baked Beans."""
    empty_basket.add_item(basket_item_shampoo_large_qty3)
    empty_basket.add_item(basket_item_shampoo_medium_qty1)
    empty_basket.add_item(basket_item_shampoo_small_qty2)
    return empty_basket


# ------- CATALOGUE FIXTURES -------


@pytest.fixture
def basic_products(
    beans_product: Product, biscuits_product: Product, sardines_product: Product
) -> list[Product]:
    """Fixture for list of basic products."""
    return [beans_product, biscuits_product, sardines_product]


@pytest.fixture
def shampoo_products(
    shampoo_small: Product, shampoo_medium: Product, shampoo_large: Product
) -> list[Product]:
    """Fixture for list of shampoo products."""
    return [shampoo_small, shampoo_medium, shampoo_large]


@pytest.fixture
def basic_catalogue(basic_products: list[Product]) -> Catalogue:
    """Fixture for catalogue with basic products."""
    return Catalogue(basic_products)


@pytest.fixture
def shampoo_catalogue(shampoo_products: list[Product]) -> Catalogue:
    """Fixture for catalogue with shampoo products."""
    return Catalogue(shampoo_products)


@pytest.fixture
def full_catalogue(
    basic_products: list[Product], shampoo_products: list[Product]
) -> Catalogue:
    """Fixture for catalogue with all products."""
    return Catalogue(basic_products + shampoo_products)


# ---------- Offers Fixture ----------


@pytest.fixture
def beans_buy_2_get_1_free() -> BuyXgetYfree:
    """Fixture for Buy 2 Get 1 Free offer on Beans."""
    return OffersFactory.create_buy_x_get_y_free(
        101, "Buy 2 Get 1 Free", buy=2, free=1, sku=1
    )


@pytest.fixture
def sardines_25_percent_off() -> PercentageOffer:
    """Fixture for 25% off Sardines offer."""
    return OffersFactory.create_percentage_offer(
        102, "25 percent off on sardiness", sku=3, percentage=25
    )


@pytest.fixture
def shampoo_buy_3_cheapest_free() -> BuyXGetCheapestFreeOffer:
    """Fixture for Buy 3 Get Cheapest Free on Shampoos."""
    return OffersFactory.create_buy_x_get_cheapest_free(
        id=103, name="Buy 3 get cheapest free", product_skus=[4, 5, 6], quantity=3
    )


@pytest.fixture
def basic_offers(
    beans_buy_2_get_1_free: BuyXgetYfree, sardines_25_percent_off: PercentageOffer
) -> list:
    """Fixture for list of basic offers."""
    return [beans_buy_2_get_1_free, sardines_25_percent_off]
