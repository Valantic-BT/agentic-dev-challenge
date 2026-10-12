# Architecture

## Modules (`src/orders_api/`)

| Module | Responsibility |
|---|---|
| `data.py` | In-memory sample data: sales reps and tokens, customers, orders, FX rates |
| `auth.py` | Bearer token → sales rep (`current_rep` dependency, 401 if missing or invalid) |
| `customers.py` | Customers and their assignment to a sales rep |
| `orders.py` | Order model (net, tax, gross, status, created_at in UTC) and read access |
| `fx.py` | Conversion to EUR at the rate of a given date (latest rate on or before that date) |
| `reports.py` | Legacy report for another team (not used by the API) |
| `main.py` | HTTP API |

## Endpoints

| Method and path | Auth | Notes |
|---|---|---|
| `GET /health` | no | |
| `GET /customers` | yes | customers of the authenticated sales rep |
| `GET /customers/{id}` | yes | 403 if not assigned, 404 if unknown |
| `GET /customers/{id}/orders` | yes | all orders, any status; 403 if not assigned |

Sample tokens: `token-ana` (customers C001, C002) and `token-bruno` (customer C003).

## Things worth knowing

- Timestamps are stored in UTC. Business months are in Europe/Lisbon.
- Amounts are `Decimal`, rounded to cents with ROUND_HALF_UP.
- Order statuses: `open`, `shipped`, `cancelled`.
