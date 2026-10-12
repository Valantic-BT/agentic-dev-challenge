def test_missing_token_is_401(client):
    assert client.get("/customers").status_code == 401


def test_invalid_token_is_401(client):
    assert client.get("/customers", headers={"Authorization": "Bearer nope"}).status_code == 401


def test_rep_sees_only_own_customers(client, ana):
    ids = [c["id"] for c in client.get("/customers", headers=ana).json()]
    assert ids == ["C001", "C002"]
