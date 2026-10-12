"""In-memory sample data. Replaces a database for the workshop."""
from datetime import UTC, date, datetime
from decimal import Decimal as D

# token -> sales rep id
TOKENS = {
    "token-ana": "rep-ana",
    "token-bruno": "rep-bruno",
}

SALES_REPS = {
    "rep-ana": "Ana Costa",
    "rep-bruno": "Bruno Silva",
}

# customer id -> (name, sales rep id)
CUSTOMERS = {
    "C001": ("Atlântico Foods", "rep-ana"),
    "C002": ("Douro Tools", "rep-ana"),
    "C003": ("Minho Textiles", "rep-bruno"),
}


def _utc(y, m, d, h=12, mi=0):
    return datetime(y, m, d, h, mi, tzinfo=UTC)


# Orders: amounts in the order currency. net = without taxes.
ORDERS = [
    # id,      customer, created (UTC),           currency, net,            tax,           status
    ("O-1001", "C001", _utc(2026, 9, 3),           "EUR", D("1200.00"), D("276.00"), "shipped"),
    ("O-1002", "C001", _utc(2026, 9, 15),          "USD", D("500.00"),  D("0.00"),   "shipped"),
    ("O-1003", "C001", _utc(2026, 9, 20),          "EUR", D("800.00"),  D("184.00"), "cancelled"),
    # 2026-09-30 23:30 UTC is already 1 October 00:30 in Lisbon (WEST, UTC+1)
    ("O-1004", "C001", _utc(2026, 9, 30, 23, 30),  "EUR", D("300.00"),  D("69.00"),  "open"),
    ("O-1005", "C001", _utc(2026, 10, 2),          "USD", D("1000.00"), D("0.00"),   "open"),
    ("O-1006", "C001", _utc(2026, 10, 5),          "EUR", D("150.00"),  D("34.50"),  "open"),
    ("O-1007", "C001", _utc(2026, 8, 28),          "EUR", D("999.00"),  D("229.77"), "shipped"),
    ("O-2001", "C002", _utc(2026, 9, 10),          "EUR", D("2000.00"), D("460.00"), "shipped"),
    ("O-2002", "C002", _utc(2026, 10, 1, 8),       "EUR", D("400.00"),  D("92.00"),  "cancelled"),
    ("O-3001", "C003", _utc(2026, 10, 3),          "EUR", D("750.00"),  D("172.50"), "open"),
]

# EUR per 1 unit of foreign currency, by date (European Central Bank style reference rates).
FX_RATES = {
    "USD": {
        date(2026, 8, 28): D("0.9150"),
        date(2026, 9, 1): D("0.9100"),
        date(2026, 9, 15): D("0.9000"),
        date(2026, 9, 30): D("0.8950"),
        date(2026, 10, 1): D("0.8900"),
        date(2026, 10, 2): D("0.8800"),
    },
}
