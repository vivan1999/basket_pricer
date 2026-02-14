from src.basket_pricer.models.money import Money
from decimal import Decimal,ROUND_HALF_UP
import pytest 

@pytest.mark.parametrize("amount, output",[
     (2,Decimal("2.00")), 
     ("2",Decimal("2.00")), 
     (2.045,Decimal("2.05")), 
     (Decimal("2.09"),Decimal("2.09"))
     ])
def test_money_creation(amount,output):
    """Initialization of money (decimal) using int, string, float and decimal
    Total 4 test cases"""
    money = Money(amount)
    assert money.amount == output

# Validating if -nagative amount is passed in, so should be raising a Value Error with matching exception message
def test_money_validation():
    with pytest.raises(ValueError, match = "Money -1.00 cannot be negative."):
        Money("-1.00")

def test_rounding_money():
    """Validating rounding off to two decimal places"""
    m1 = Money("1.05459")
    assert m1.amount == Decimal("1.05")
    m2 = Money("1.456")
    assert m2.amount == Decimal("1.46")

def test_invalid_string_money():
    """Validate if it raises ValueError on invalid string input"""
    with pytest.raises(ValueError):
        Money("hello")

def test_none_raises_error() -> None:
    """Validate if None is rejected."""
    with pytest.raises(ValueError):
        Money(None)
