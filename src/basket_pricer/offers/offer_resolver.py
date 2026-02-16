import logging
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

from src.basket_pricer.models import Basket, BasketItem, Money
from src.basket_pricer.offers import AbstractBaseOffer

logger = logging.getLogger(__name__)


@dataclass
class OfferChoice:
    offer: AbstractBaseOffer
    discount: Money
    affected_items: List[str]


class OfferResolver:
    """
    Resolve conflicts when more than one offer is applicable
    to the same BasketItem / basket, by choosing the maximum discount.
    """

    def __init__(self, offers: Iterable[AbstractBaseOffer]) -> None:
        self.offers: List[AbstractBaseOffer] = list(offers)

    def get_applicable_single_sku_offers(
        self, basket_item: BasketItem
    ) -> List[AbstractBaseOffer]:
        """
        Filter offers that are applicable to this particular basket item
        (based on sku or product_skus).
        """
        applicable: List[AbstractBaseOffer] = []
        sku = basket_item.product.sku

        for offer in self.offers:
            # single‑SKU offers only
            if hasattr(offer, "sku") and getattr(offer, "sku") == sku:
                applicable.append(offer)

        return applicable

    def resolve_best_offer_for_item(
        self, basket: Basket, basket_item: BasketItem
    ) -> Optional[OfferChoice]:
        """
        Among all applicable offers for this specific item, return the one
        that gives the maximum discount on the current basket.
        If none yield a positive discount, return None.
        """
        applicable_offers = self.get_applicable_single_sku_offers(basket_item)
        if not applicable_offers:
            return None

        best_choice: Optional[OfferChoice] = None

        for offer in applicable_offers:
            result: Optional[Tuple[Money, List[str]]] = offer.apply_to_basket(basket)
            if result is None:
                continue

            discount, affected_items = result
            if discount.is_zero():
                continue

            if best_choice is None or discount > best_choice.discount:
                best_choice = OfferChoice(
                    offer=offer, discount=discount, affected_items=affected_items
                )

        return best_choice
