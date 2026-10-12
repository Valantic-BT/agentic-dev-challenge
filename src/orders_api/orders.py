"""Orders module: order model and read access."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from . import data

STATUSES = ("open", "shipped", "cancelled")


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    created_at: datetime  # timezone-aware, UTC
    currency: str
    net_amount: Decimal  # without taxes
    tax_amount: Decimal
    status: str

    @property
    def gross_amount(self) -> Decimal:
        return self.net_amount + self.tax_amount

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customerId": self.customer_id,
            "createdAt": self.created_at.isoformat(),
            "currency": self.currency,
            "netAmount": str(self.net_amount),
            "taxAmount": str(self.tax_amount),
            "status": self.status,
        }


def _all() -> list[Order]:
    return [Order(*row) for row in data.ORDERS]


def get_order(order_id: str) -> Order | None:
    return next((o for o in _all() if o.id == order_id), None)


def orders_for_customer(customer_id: str) -> list[Order]:
    """All orders of a customer, any status, oldest first."""
    return sorted((o for o in _all() if o.customer_id == customer_id), key=lambda o: o.created_at)
