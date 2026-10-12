from datetime import date
from decimal import Decimal

import pytest

from orders_api import fx


def test_eur_is_identity():
    assert fx.to_eur(Decimal("10.00"), "EUR", date(2026, 9, 1)) == Decimal("10.00")


def test_uses_rate_of_the_date():
    assert fx.to_eur(Decimal("100"), "USD", date(2026, 10, 2)) == Decimal("88.00")


def test_falls_back_to_previous_published_rate():
    # no rate on 2026-09-20: uses 2026-09-15
    assert fx.rate("USD", date(2026, 9, 20)) == Decimal("0.9000")


def test_unknown_currency_raises():
    with pytest.raises(fx.RateNotFound):
        fx.rate("GBP", date(2026, 9, 1))
