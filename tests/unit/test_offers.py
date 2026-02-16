import pytest

from src.basket_pricer.models import Basket, Money


class TestBuyXGetYFreeOffer:
    """Tests for Buy X Get Y Free offer."""

    def test_buy_2_get_1_free_basic(
        self, beans_buy_2_get_1_free, basket_with_beans: Basket
    ):
        """Test basic buy 2 get 1 free."""

        assert beans_buy_2_get_1_free.is_applicable(basket_with_beans)
        discount = beans_buy_2_get_1_free.calculate_discount(basket_with_beans)
        print(discount)
        assert discount == Money("0.99")

    def test_buy_2_get_1_free_six_items(
        self, beans_buy_2_get_1_free, basket_with_beans_qty6: Basket
    ):
        """Test with 6 items (2 complete sets)."""
        assert beans_buy_2_get_1_free.is_applicable(basket_with_beans_qty6)
        discount = beans_buy_2_get_1_free.calculate_discount(basket_with_beans_qty6)
        assert discount == Money("1.98")  # 2 free items

    def test_insufficient_items(self, beans_buy_2_get_1_free, empty_basket: Basket):
        """Test with insufficient items."""
        assert not beans_buy_2_get_1_free.is_applicable(empty_basket)


class TestPercentageDiscountOffer:
    """Tests for Percentage Discount offer."""

    def test_25_percent_off_one_item(
        self, sardines_25_percent_off, basket_with_sardiness_qty1: Basket
    ):
        """Test 25% off one item."""
        assert sardines_25_percent_off.is_applicable(basket_with_sardiness_qty1)
        discount = sardines_25_percent_off.calculate_discount(
            basket_with_sardiness_qty1
        )
        assert discount == Money("0.47")  # 25% of 1.89

    def test_25_percent_off_three_items(
        self, sardines_25_percent_off, basket_with_sardiness_qty3: Basket
    ):
        """Test 25% off three items."""
        assert sardines_25_percent_off.is_applicable(basket_with_sardiness_qty3)
        discount = sardines_25_percent_off.calculate_discount(
            basket_with_sardiness_qty3
        )
        print(discount)
        assert discount == Money("1.42")  # 25% of 3.78

    def test_not_applicable(self, sardines_25_percent_off, basket_with_beans: Basket):
        """Test when product not in items."""
        assert not sardines_25_percent_off.is_applicable(basket_with_beans)


class TestBuyXGetCheapestFreeOffer:
    """Tests for Buy X Get Cheapest Free offer."""

    def test_scenario(self, shampoo_buy_3_cheapest_free, basket_with_shampoo_scenario):
        """Test exact assignment example."""

        assert shampoo_buy_3_cheapest_free.is_applicable(basket_with_shampoo_scenario)
        discount = shampoo_buy_3_cheapest_free.calculate_discount(
            basket_with_shampoo_scenario
        )
        print(discount)
        assert discount == Money("5.50")  # 1 large + 1 small free

    def test_insufficient_items(
        self, shampoo_buy_3_cheapest_free, basket_with_shampoo_small_qty2: Basket
    ):
        """Test with insufficient items."""
        assert not shampoo_buy_3_cheapest_free.is_applicable(
            basket_with_shampoo_small_qty2
        )
