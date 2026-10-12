from orders_api import orders


def test_orders_sorted_oldest_first():
    ids = [o.id for o in orders.orders_for_customer("C001")]
    assert ids[0] == "O-1007"
    assert len(ids) == 7


def test_gross_is_net_plus_tax():
    o = orders.get_order("O-1001")
    assert o.gross_amount == o.net_amount + o.tax_amount


def test_api_lists_orders_of_assigned_customer(client, ana):
    r = client.get("/customers/C002/orders", headers=ana)
    assert r.status_code == 200
    assert {o["id"] for o in r.json()} == {"O-2001", "O-2002"}


def test_api_denies_orders_of_other_reps_customer(client, bruno):
    assert client.get("/customers/C001/orders", headers=bruno).status_code == 403
