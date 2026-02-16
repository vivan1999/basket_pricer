import logging
from dataclasses import dataclass, field
from typing import List, Optional

from src.basket_pricer.models import Basket, BasketItem, Money
from src.basket_pricer.offers import AbstractBaseOffer
from src.basket_pricer.utils.exceptions import InvalidOfferConfigError

logger = logging.getLogger(__name__)


@dataclass
class BuyXGetCheapestFreeOffer(AbstractBaseOffer):
    product_skus: List[int] = field(default_factory=list)
    quantity: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()

        if not self.product_skus:
            raise InvalidOfferConfigError("product sku cannot be empty")

        # Validate no duplicate product skus
        if len(self.product_skus) != len(set(self.product_skus)):
            raise InvalidOfferConfigError(
                "product sku's list must not contain duplicates"
            )
        if self.quantity < 0:
            raise ValueError("quantity must be positive")

        # Need at least 2 products in set for "cheapest free"
        if len(self.product_skus) < 2:
            raise InvalidOfferConfigError(
                f"Multi-product offer needs at least 2 products, got {len(self.product_skus)}"
            )
        logger.debug("BuyXGetCheapestFree Offer Created")

    def is_applicable(self, basket: Basket) -> bool:
        total_eligible, _ = self.get_eligible_basket_items(basket)
        is_applicable = total_eligible >= self.quantity
        if not is_applicable:
            logger.debug("Insufficient Items in basket for buyXGetCheapestFree Offer")
        return is_applicable

    def get_eligible_basket_items(
        self, basket: Basket
    ) -> Optional[tuple[int, List[BasketItem]]]:
        total_eligible: int = 0
        eligible_product_names: List[str] = []

        basket_items = basket.get_items_list()  # [(sku, BasketItem),..]
        for sku, basket_item in basket_items.items():
            if sku in self.product_skus:
                total_eligible += basket_item.qty
                eligible_product_names.append(basket_item.product.name)

        return total_eligible, eligible_product_names

    def calculate_discount(self, basket: Basket) -> Money:
        all_eligible_items: List[tuple[int, Money]] = []  # (sku, price)
        free_items: List[tuple[int, Money]] = []  # Form groups and calculate discount
        total_discount = Money.zero()

        basket_items = basket.get_items_list()  # returns [(sku, BasketItem),..]

        # Adding each eligible unit individually in form of (sku, price), for sorting on price
        # Example: 3 Large Shampoos will have 3 entries of (Large, 3.50)
        for sku, basket_item in basket_items.items():
            if sku in self.product_skus:
                for _ in range(basket_item.qty):
                    all_eligible_items.append(
                        (basket_item.product.sku, basket_item.product.price)
                    )

        # If not enough items, no discount
        if len(all_eligible_items) < self.quantity:
            return Money.zero()

        # Sorting by price DESCENDING (expensive first) so that
        # expensive items are "bought", cheap ones are "free"
        all_eligible_items.sort(key=lambda x: x[1], reverse=True)

        # total groups can be formed
        num_groups = len(all_eligible_items) // self.quantity

        for group_idx in range(num_groups):
            # Get items for this group
            start = group_idx * self.quantity
            end = start + self.quantity
            group = all_eligible_items[start:end]

            # After sorting descending, last item is cheapest
            cheapest_item = group[-1]  # Last item in group
            free_items.append(cheapest_item)
            total_discount = (
                total_discount + cheapest_item[1]
            )  # cheapest_item[1] will give the unit price of the item

        logger.debug("Calculated discount of BuyXGetCheapestOffer discount.")

        return total_discount

    def __str__(self) -> str:
        products_str = ", ".join(self.product_skus)
        return f"Buy {self.quantity} Get Cheapest Free from sku's : [{products_str}] "

    def _get_affected_items(self, basket: Basket):
        _, prod_names = self.get_eligible_basket_items(basket)
        return prod_names
