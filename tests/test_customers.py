from orders_api import customers


def test_assignment():
    assert customers.is_assigned("C001", "rep-ana")
    assert not customers.is_assigned("C003", "rep-ana")
    assert not customers.is_assigned("C999", "rep-ana")


def test_other_reps_customer_is_403(client, ana):
    assert client.get("/customers/C003", headers=ana).status_code == 403


def test_unknown_customer_is_404(client, ana):
    assert client.get("/customers/C999", headers=ana).status_code == 404
