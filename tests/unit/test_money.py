from src.basket_pricer.models.money import Money
from decimal import Decimal

def test_money_creation():
    m1 = Money("1.03")
    assert m1.amount == Decimal("1.03")