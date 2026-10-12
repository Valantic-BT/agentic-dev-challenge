"""FX module: converts amounts to EUR using the reference rate of a given date."""
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from . import data

BASE = "EUR"


class RateNotFound(LookupError):
    pass


def rate(currency: str, on: date) -> Decimal:
    """EUR per 1 unit of `currency` on `on`; uses the latest rate published on or before that date."""
    if currency == BASE:
        return Decimal("1")
    table = data.FX_RATES.get(currency)
    if not table:
        raise RateNotFound(f"No rates for {currency}")
    candidates = [d for d in table if d <= on]
    if not candidates:
        raise RateNotFound(f"No {currency} rate on or before {on.isoformat()}")
    return table[max(candidates)]


def to_eur(amount: Decimal, currency: str, on: date) -> Decimal:
    """Convert `amount` in `currency` to EUR at the rate of date `on`, rounded to cents."""
    return (amount * rate(currency, on)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
