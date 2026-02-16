import pytest

from src.basket_pricer.models import Catalogue, Product
from src.basket_pricer.utils.exceptions import CatalogueError


class TestCatalogueCreation:
    """Tests for Catalogue creation."""

    def test_create_empty_catalogue(self):
        """Test creating empty catalogue."""
        catalogue = Catalogue()
        assert len(catalogue._products) == 0

    def test_create_with_products(self, basic_products: list[Product]):
        """Test creating catalogue with products."""
        catalogue = Catalogue(basic_products)
        assert len(catalogue._products) == 3

    def test_create_with_fixture(self, basic_catalogue: Catalogue):
        """Test using catalogue fixture."""
        assert len(basic_catalogue._products) == 3


class TestCatalogueOperations:
    """Tests for Catalogue CRUD operations."""

    def test_add_product(self, beans_product: Product):
        """Test adding product."""
        catalogue = Catalogue()
        catalogue.add_product(beans_product)

        assert len(catalogue._products) == 1
        assert catalogue.has_product(1)

    def test_add_duplicate_raises_error(self, beans_product: Product):
        """Test adding duplicate raises error."""
        catalogue = Catalogue([beans_product])

        with pytest.raises(CatalogueError):
            catalogue.add_product(beans_product)

    def test_has_product(self, basic_catalogue: Catalogue):
        """Test checking product existence."""
        assert basic_catalogue.has_product(1)
