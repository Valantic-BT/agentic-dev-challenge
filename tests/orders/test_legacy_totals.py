"""Legacy report test (reporting team).

Fails since order O-1006 was added to the sample data in v1.2.
Owner: reporting team. Do not change without talking to them.
"""
from decimal import Decimal

from orders_api.reports import legacy_customer_total


def test_legacy_customer_total_c001():
    assert legacy_customer_total("C001") == Decimal("4573.77")
