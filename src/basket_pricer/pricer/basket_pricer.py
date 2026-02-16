import logging
from typing import List, Optional

from src.basket_pricer.models import Basket, Catalogue, Money, BasketItem
from src.basket_pricer.offers import AbstractBaseOffer
from src.basket_pricer.offers.offer_resolver import OfferResolver
from src.basket_pricer.pricer.offer_summary import OfferApplied
from src.basket_pricer.pricer.price_summary import (
    PriceSummary,
    no_discount_summary,
    zero_summary,
)
from src.basket_pricer.utils.exceptions import CatalogueError, PricingException

logger = logging.getLogger(__name__)


class BasketPricer:
    def __init__(self, catalogue: Catalogue, offers: Optional[List[AbstractBaseOffer]]):
        if not isinstance(catalogue, Catalogue):
            raise TypeError(
                f"catalogue must be Catalogue, got {type(catalogue).__name__}"
            )
        self.catalogue = catalogue
        self.offers = offers or []
        self.offer_resolver = OfferResolver(self.offers)
        for offer in self.offers:
            if not isinstance(offer, AbstractBaseOffer):
                raise TypeError(
                    f"All offers must be AbstractBaseOffer, but got {type(offer).__name__}"
                )
        logger.debug("Basket Pricer Created")

    def calculate(self, basket: Basket) -> PriceSummary:
        if not isinstance(basket, Basket):
            raise TypeError(f"Expected Basket Type and got {type(basket).__name__}")
        if basket.is_empty():
            logger.info("Basket is empty.")
            return zero_summary()

        sub_total = self.calculate_subtotal_basket(basket)

        if not self.offers:
            logger.info("No offers Available")
            return no_discount_summary(sub_total)

        total_discount, applied_offers = self._apply_offers(basket=basket)
        if total_discount < Money("0"):
            raise PricingException("Total discount must be poitive")

        if total_discount > sub_total:
            total_discount = sub_total  # making items free and no negative

        total = sub_total - total_discount  # final amount to be paid by the customer

        if total < Money("0"):
            logger.error("Negative total calculated and must be positive")
            raise PricingException(
                f"Discount ({total_discount}) exceeds sub-total ({sub_total}), "
                f"resulting in negative total ({total})"
            )

        result = PriceSummary(
            sub_total=sub_total,
            discount=total_discount,
            total_amount=total,
            applied_offers=applied_offers,
        )
        logger.debug("calculated final bill summary")
        return result

    def calculate_subtotal_basket(self, basket: Basket) -> Money:
        sub_total = Money("0")
        basket_items = basket.get_items_list()  # (sku, BasketItem)
        for sku, basket_item in basket_items.items():
            if not self.catalogue.has_product(sku):
                logger.error(
                    f"Product '{basket_item.product.name}' from basket not present in catalogue"
                )
                raise CatalogueError(f"Product {sku} not in the catalogue")
            item_price = self.catalogue.fetch_price(sku)
            basket_item_total = item_price * basket_item.qty
            sub_total = basket_item_total + sub_total
        logger.debug(f"calculated basket subtotal: {sub_total}")
        return sub_total
    
    def _get_applicable_offers(self, basket_item: BasketItem) -> AbstractBaseOffer:
        """Get all offers And resolve if there are more than one offer applicable on a product
        and finally return a final maximum discount offer applicable on that item"""
        applicable = []
        for offer in self.offers:
            # Check if offer is applicable to this item
            if hasattr(offer, 'sku') and offer.sku == basket_item.product.sku:
                applicable.append(offer)
            elif hasattr(offer, 'product_skus') and basket_item.product.sku in offer.product_skus:
                applicable.append(offer)
        return applicable

    def _apply_offers(self, basket: Basket) -> tuple[Money, List[OfferApplied]]:
        total_discount = Money.zero()
        applied_offers: List[OfferApplied] = []

        # Spliting offers into single‑SKU and multi‑SKU offers
        # helpful for resolving the conflicts
        single_sku_offers: List[AbstractBaseOffer] = []
        multi_sku_offers: List[AbstractBaseOffer] = []

        for offer in self.offers:
            if hasattr(offer, "sku"):
                single_sku_offers.append(offer)
            elif hasattr(offer, "product_skus"):
                multi_sku_offers.append(offer)
            else:
                # fallback: treating as basket‑level / multi‑sku
                multi_sku_offers.append(offer)

        # Apply multi‑SKU offers ONCE at basket level
        for offer in multi_sku_offers:
            result = offer.apply_to_basket(basket)
            if result is None:
                logger.debug("Offer not applied")
                continue

            discount, affected_items = result
            if discount.is_zero():
                continue

            applied_offers.append(
                OfferApplied(
                    offer_name=offer.name,
                    discount=discount,
                    products_effected=affected_items,
                )
            )
            total_discount = total_discount + discount
            logger.info("multi-sku offer applied to basket")

        # Resolve conflicts between single‑SKU offers per item
        resolver = OfferResolver(single_sku_offers)

        for sku, basket_item in basket.get_items_list().items():
            choice = resolver.resolve_best_offer_for_item(basket, basket_item)
            if choice is None:
                continue

            applied_offers.append(
                OfferApplied(
                    offer_name=choice.offer.name,
                    discount=choice.discount,
                    products_effected=choice.affected_items,
                )
            )
            total_discount = total_discount + choice.discount
            logger.info("single-sku offer applied to basket item")

        return total_discount, applied_offers