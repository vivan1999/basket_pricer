import pytest

from src.basket_pricer.models import Basket, BasketItem, Catalogue, Money, Product
from src.basket_pricer.offers.offers_factory import OffersFactory
from src.basket_pricer.pricer import BasketPricer


@pytest.mark.integration
class TestExamples:
    """Tests for exact examples."""

    def test_example_1(
        self,
        basket_with_mixed_items: Basket,
        basic_catalogue: Catalogue,
        beans_buy_2_get_1_free,
    ):
        """Test Example 1: Beans + Biscuits.

        Basket: Baked Beans x3 (0.99 per item), Sardiness x1 (1.89 per item)
        Offer: Buy 2 get 1 free on Beans
        Expected: sub-total £4.86, discount £0.99, total £3.87
        """
        pricer = BasketPricer(basic_catalogue, [beans_buy_2_get_1_free])
        result = pricer.calculate(basket_with_mixed_items)

        assert result.sub_total == Money("4.86")
        assert result.discount == Money("0.99")
        assert result.total_amount == Money("3.87")
        assert len(result.applied_offers) == 1

    def test_example_2(
        self,
        basket_with_shampoo_scenario: Basket,
        shampoo_catalogue: Catalogue,
        shampoo_buy_3_cheapest_free,
    ):
        """Test Example 2: Shampoo Multi-Buy.

        Basket: Large x3, Medium x1, Small x2
        Offer: Buy 3, cheapest free
        Expected: sub-total £17.00, discount £5.50, total £11.50
        """
        pricer = BasketPricer(shampoo_catalogue, [shampoo_buy_3_cheapest_free])
        result = pricer.calculate(basket_with_shampoo_scenario)

        assert result.sub_total == Money("17.00")
        assert result.discount == Money("5.50")
        assert result.total_amount == Money("11.50")
        assert len(result.applied_offers) == 1


@pytest.mark.integration
class TestCombinedOffers:
    """Tests for multiple offers applied together."""

    def test_multiple_offers_applied(
        self,
        empty_basket: Basket,
        basic_catalogue: Catalogue,
        basket_item_beans_qty6: BasketItem,
        basket_item_sardiness_qty1: BasketItem,
    ):
        """Test basket with multiple different offers."""
        # Create offers
        offers = [
            OffersFactory.create_buy_x_get_y_free(
                id=101, sku=1, name="Buy 2 Baked Beans Get 1 free", buy=2, free=1
            ),
            OffersFactory.create_percentage_offer(
                id=102, sku=3, name="25 off on Sardines", percentage=25.0
            ),
        ]

        # Build basket
        empty_basket.add_item(basket_item_beans_qty6)
        empty_basket.add_item(basket_item_sardiness_qty1)

        # Calculate
        pricer = BasketPricer(basic_catalogue, offers)
        result = pricer.calculate(empty_basket)

        # Beans: 6 * 0.99 = 5.94, discount 1.98
        # Sardines: 1 * 1.89 = 1.89, discount 0.47
        # Sub-total: 7.83, Discount: 2.45, Total: 5.38
        assert result.sub_total == Money("7.83")
        assert result.discount == Money("2.45")
        assert result.total_amount == Money("5.38")
        assert len(result.applied_offers) == 2


class TestConflictOffers:
    """Test conflicting offers, and should be returning maximum discount"""

    def test_conflict_offers_with_single_basket_item(
        self,
        basket_item_beans_qty3: BasketItem,
        beans_product: Product,
        empty_basket: Basket,
        beans_buy_2_get_1_free,
        beans_20_percent_off,
    ):
        catalogue = Catalogue([beans_product])
        empty_basket.add_item(basket_item_beans_qty3)
        offers = [beans_20_percent_off, beans_buy_2_get_1_free]
        # Calculate
        pricer = BasketPricer(catalogue=catalogue, offers=offers)
        result = pricer.calculate(empty_basket)
        # Beans: 3 * 0.99 = 2.97
        # discount 1: buy2 get 1: discount = 0.99, total amount = 1.98
        # discount 2: 20 % off: discount = 0.59, totalo amount = 2.38
        # and so maximum discount is 0.99 which is discount 1(buy2 get 1 free)
        assert result.sub_total == Money("2.97")
        assert result.discount == Money("0.99")
        assert result.total_amount == Money("1.98")
        assert len(result.applied_offers) == 1

    def test_conflict_offers_with_multiple_basket_item(
        self,
        basket_item_beans_qty3: BasketItem,
        basket_item_shampoo_large_qty3: BasketItem,
        basket_item_shampoo_medium_qty1: BasketItem,
        basket_item_shampoo_small_qty2: BasketItem,
        beans_product: Product,
        shampoo_large: Product,
        shampoo_medium: Product,
        shampoo_small: Product,
        empty_basket: Basket,
        beans_buy_2_get_1_free,
        beans_20_percent_off,
        shampoo_buy_3_cheapest_free,
        shampoo_large_25_percent_off,
    ):
        catalogue = Catalogue(
            [beans_product, shampoo_medium, shampoo_large, shampoo_small]
        )
        empty_basket.add_item(basket_item_beans_qty3)
        empty_basket.add_item(basket_item_shampoo_large_qty3)
        empty_basket.add_item(basket_item_shampoo_medium_qty1)
        empty_basket.add_item(basket_item_shampoo_small_qty2)
        # all 3 offers with offers
        offers = [
            beans_20_percent_off,
            beans_buy_2_get_1_free,
            shampoo_buy_3_cheapest_free,
            shampoo_large_25_percent_off,
        ]

        # Calculate
        pricer = BasketPricer(catalogue=catalogue, offers=offers)
        result = pricer.calculate(empty_basket)
        # Beans: 3 * 0.99 = 2.97
        # shampoo SMALL: 2 * 2 = 4
        # shampoo medium : 1 * 2.50 = 2.50
        # shampoo large : 3 * 3.50 = 10.50
        # discount 1: beans buy2 get 1: discount = 0.99, total amount = 1.98
        # discount 2: 20 % off: discount = 0.59, total amount = 2.38
        # discount 3: discount = 5.50
        # discount 4: discount = 2.62
        # and so maximum discount is 0.99 + 2.63 + 5.50
        assert result.sub_total == Money("19.97")
        assert result.discount == Money("9.12")
        assert result.total_amount == Money("10.85")
        assert len(result.applied_offers) == 3
