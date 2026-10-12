"""Legacy reports, kept for the reporting team. Not used by the API."""
from decimal import Decimal

from . import orders


def legacy_customer_total(customer_id: str) -> Decimal:
    """Gross total of all non-cancelled orders, in order currency, without conversion.

    Deprecated: mixes currencies. Kept until the reporting team migrates.
    """
    return sum(
        (o.gross_amount for o in orders.orders_for_customer(customer_id) if o.status != "cancelled"),
        Decimal("0"),
    )
