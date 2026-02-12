from decimal import Decimal, ROUND_HALF_UP

twoplaces_decimal = Decimal("0.01") # for two places decimal

def to_decimal(value: float| str | Decimal) -> Decimal: # handling all possible types of values
    if isinstance(value,Decimal):
        return value
    return Decimal(str(value))

def round_amount(value: Decimal) -> Decimal:
    return value.quantize(twoplaces_decimal, rounding=ROUND_HALF_UP)

def zero() -> Decimal:
    return Decimal("0")