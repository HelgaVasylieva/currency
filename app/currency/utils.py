from decimal import Decimal


def to_decimal(value: str, precision: int = 3) -> Decimal:
    """
    TODO
    """
    return round(Decimal(value), precision)
