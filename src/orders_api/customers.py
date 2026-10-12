"""Customers module: customers and their assignment to sales reps."""
from dataclasses import dataclass

from . import data


@dataclass(frozen=True)
class Customer:
    id: str
    name: str
    sales_rep_id: str

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "salesRepId": self.sales_rep_id}


def get_customer(customer_id: str) -> Customer | None:
    row = data.CUSTOMERS.get(customer_id)
    return Customer(customer_id, *row) if row else None


def customers_for_rep(rep_id: str) -> list[Customer]:
    return [Customer(cid, name, rep) for cid, (name, rep) in data.CUSTOMERS.items() if rep == rep_id]


def is_assigned(customer_id: str, rep_id: str) -> bool:
    customer = get_customer(customer_id)
    return customer is not None and customer.sales_rep_id == rep_id
