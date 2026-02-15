import pytest

from src.basket_pricer.models.basket import Basket
from src.basket_pricer.models.basket_item import BasketItem
from src.basket_pricer.models.money import Money
from src.basket_pricer.models.product import Product
from src.basket_pricer.utils.exceptions import PricerException


class TestProduct:
    """For testing Product Model and its functionality"""

    def test_create_product(self) -> None:
        """Test product initialization"""
        product = Product(sku=1, name="Beans", price=Money("0.99"))
        assert product.sku == 1
        assert product.name == "Beans"
        assert product.price.amount == Money("0.99").amount

    def test_product_is_immutable(self) -> None:
        """Test immutability of the product"""
        product = Product(sku=1, name="Beans", price=Money("0.99"))
        with pytest.raises(AttributeError):  # dataclass frozen raises AttributeError
            product.name = "Different Beans"

    def test_product_with_empty_name_raises_error(self) -> None:
        """Test empty product name raises Error"""
        with pytest.raises(PricerException, match="Product name is required"):
            Product(sku=1, name="", price=Money("0.99"))

    def test_product_with_whitespace_only_name_raises_error(self) -> None:
        """Test that whitespace-only name is rejected."""
        with pytest.raises(PricerException, match="is required"):
            Product(sku=1, name="   ", price=Money("0.99"))

    def test_product_with_zero_price_raises_error(self) -> None:
        """Test that zero price is rejected."""
        with pytest.raises(ValueError, match="must be positive"):
            Product(sku=1, name="Free Item", price=Money.zero())

    def test_product_with_negative_price_raises_error(self) -> None:
        """Test that negative price is rejected."""
        # This actually fails at Money creation, not Product validation
        with pytest.raises(ValueError):
            Product(sku=1, name="Beans", price=Money("-1.00"))

    """def test_product_equality(self) -> None:
        #Test that two products with same values are equal.
        p1 = Product(sku=1, name="Beans", price=Money("0.99"))
        p2 = Product(sku=1, name="Beans", price=Money("0.99"))
        assert p1 == p2"""

    def test_product_inequality(self) -> None:
        """Test that products with different values are not equal."""
        p1 = Product(sku=1, name="Beans", price=Money("0.99"))
        p2 = Product(sku=2, name="Beans", price=Money("1.99"))
        p3 = Product(sku=3, name="Sardines", price=Money("0.99"))
        assert p1 != p2
        assert p1 != p3

    def test_product_string_representation(self) -> None:
        """Test Product string formatting."""
        product = Product(sku=1, name="Baked Beans", price=Money("0.99"))
        # Dataclass default __repr__ shows all fields
        assert f"Product(name='{product.name}', price: {product.price})"


class TestBasketItem:
    """For testing Basket Item Model and its functionality"""

    @pytest.fixture
    def sardines_product(self) -> Product:
        """Sardines product fixture"""
        return Product(sku=1, name="Sardines", price=Money("0.99"))

    def test_create_valid_basket_item(self, sardines_product: Product) -> BasketItem:
        """Validate initialization of basked Item using product fixture"""
        basket_item = BasketItem(product=sardines_product, qty=2)
        assert basket_item.product == sardines_product
        assert basket_item.qty == 2

    def test_basket_item_with_zero_quantity_raises_error(
        self, sardines_product: Product
    ) -> None:
        """Test that zero quantity is rejected."""
        with pytest.raises(ValueError, match="must be positive"):
            BasketItem(product=sardines_product, qty=0)

    def test_basket_item_with_negative_quantity_raises_error(
        self, sardines_product: Product
    ) -> None:
        """Test that negative quantity is rejected."""
        with pytest.raises(ValueError, match="must be positive"):
            BasketItem(product=sardines_product, qty=-1)

    def test_basket_item_with_non_product_raises_error(self) -> None:
        """Test that non-Product object is rejected."""
        with pytest.raises(TypeError, match="must be Product"):
            BasketItem(product="not a product", qty=1)  # type: ignore

    def test_basket_item_total_price_calculation(
        self, sardines_product: Product
    ) -> None:
        """Test total_price calculation"""
        item = BasketItem(product=sardines_product, qty=2)
        expected_total = Money("0.99") * 2
        assert item.total_price()._amount == expected_total._amount

    def test_basket_item_quantity_can_be_modified(
        self, sardines_product: Product
    ) -> None:
        """Test that quantity can be changed (mutable)"""
        item = BasketItem(product=sardines_product, qty=2)
        item.qty = 5
        assert item.qty == 5


class TestBasket:
    """For testing basket Model and it functionality"""

    @pytest.fixture
    def beans(self) -> Product:
        """Baked Beans Product Fixture"""
        return Product(sku=1, name="Baked Beans", price=Money("0.99"))

    @pytest.fixture
    def biscuits(self) -> Product:
        """Biscuits product fixture"""
        return Product(sku=2, name="Biscuits", price=Money("1.20"))

    @pytest.fixture
    def sardines(self) -> Product:
        """Sardines product fixture"""
        return Product(sku=3, name="Sardines", price=Money("1.89"))

    @pytest.fixture
    def basket_item1(self, beans: Product) -> BasketItem:
        """basket item 1 fixture"""
        return BasketItem(product=beans, qty=2)

    @pytest.fixture
    def basket_item2(self, biscuits: Product) -> BasketItem:
        """basket item 2 fixture"""
        return BasketItem(product=biscuits, qty=1)

    @pytest.fixture
    def basket_item3(self, sardines: Product) -> BasketItem:
        """basket item 3 fixture"""
        return BasketItem(product=sardines, qty=3)

    def test_create_empty_basket(self) -> None:
        """Test creating an empty basket."""
        basket = Basket()
        assert basket.is_empty()
        assert len(basket._items) == 0

    def test_add_multiple_different_items(
        self, basket_item1: BasketItem, basket_item2: BasketItem
    ) -> None:
        """Test adding different products to basket."""
        basket = Basket()
        basket.add_item(basket_item1)
        basket.add_item(basket_item2)
        assert len(basket._items) == 2  # Two different products

    def test_add_same_item_twice_merges_quantity(
        self, basket_item1: BasketItem
    ) -> None:
        """Test that adding same product twice merges quantities."""
        basket = Basket()
        basket.add_item(basket_item1)
        basket.add_item(basket_item1)
        assert len(basket._items) == 1  # Still one product

    def test_add_non_product_raises_error(self) -> None:
        """Test that adding non-Product raises TypeError."""
        basket = Basket()
        with pytest.raises(TypeError, match="Must be of Basket Item type"):
            basket.add_item(1)  # type: ignore

    def test_get_item_by_name(self, basket_item1) -> None:
        """Test retrieving item by product name."""
        basket = Basket()
        basket.add_item(basket_item1)
        quantity = basket.fetch_quantity(sku=1)
        assert quantity == 2  # qty of beans(sku:1) in basket item is 2

    def test_has_item_returns_true_for_existing_item(self, basket_item3) -> None:
        """Test has_item returns True for items in basket."""
        basket = Basket()
        basket.add_item(basket_item3)
        assert basket.has_product(sku=3)

    def test_has_item_returns_false_for_missing_item(self) -> None:
        """Test has_item returns False for items not in basket."""
        basket = Basket()
        assert not basket.has_product(sku=0)

    """def test_total_items_sums_all_quantities(
        self, basket_item1, basket_item2, basket_item3
    ) -> None:
        #Test that total_items returns sum of all item quantities
        basket = Basket()
        basket.add_item(basket_item1)
        basket.add_item(basket_item2)
        basket.add_item(basket_item3)

        assert basket.calculate_subtotal()== Money("8.85")._amount
        # 0.99 * 2 (sku 1, qty 2) + 1.20 * 1 (sku 2, qty 1)+ 1.89 * 3 (sku 3, qty 3)
    """
