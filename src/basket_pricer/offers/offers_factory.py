from typing import List

from src.basket_pricer.offers import (
    BuyXGetCheapestFreeOffer,
    BuyXgetYfree,
    PercentageOffer,
)


class OffersFactory:
    def create_buy_x_get_y_free(
        id: int,
        name: str,
        sku: int,
        buy: int,
        free: int = 1,
    ) -> BuyXgetYfree:
        # generate ID if not provided
        if id is None:
            id = f"buy_{buy}_get_{free}_free_{name.lower().replace(' ', '_')}"

        return BuyXgetYfree(id=id, name=name, buy=buy, free=free, sku=sku)

    def create_buy_x_get_cheapest_free(
        id: int, name: str, product_skus: List[int], quantity: int
    ) -> BuyXGetCheapestFreeOffer:

        if id is None:
            id = f"buy_{quantity}_get_cheapest_free_{name.lower().replace(' ', '_')}"

        return BuyXGetCheapestFreeOffer(
            id=id, name=name, product_skus=product_skus, quantity=quantity
        )

    def create_percentage_offer(
        id: int, name: str, sku: int, percentage: float
    ) -> PercentageOffer:

        if id is None:
            id = f"{percentage}_off_on_sku_{sku}"

        return PercentageOffer(id=id, name=name, sku=sku, percentage=percentage)
