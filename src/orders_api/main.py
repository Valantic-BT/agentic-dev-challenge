"""HTTP API (FastAPI)."""
from fastapi import Depends, FastAPI, HTTPException

from . import customers, orders
from .auth import current_rep

app = FastAPI(title="Orders API", version="1.2.0")


def _assigned_customer(customer_id: str, rep: str) -> customers.Customer:
    customer = customers.get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.sales_rep_id != rep:
        raise HTTPException(status_code=403, detail="Customer not assigned to you")
    return customer


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/customers")
def list_my_customers(rep: str = Depends(current_rep)) -> list[dict]:
    return [c.to_dict() for c in customers.customers_for_rep(rep)]


@app.get("/customers/{customer_id}")
def get_customer(customer_id: str, rep: str = Depends(current_rep)) -> dict:
    return _assigned_customer(customer_id, rep).to_dict()


@app.get("/customers/{customer_id}/orders")
def list_customer_orders(customer_id: str, rep: str = Depends(current_rep)) -> list[dict]:
    _assigned_customer(customer_id, rep)
    return [o.to_dict() for o in orders.orders_for_customer(customer_id)]
