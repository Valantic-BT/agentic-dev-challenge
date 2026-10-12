# Client answers

Open this file only after writing your own questions.

| Question | Client answer |
|---|---|
| Which customers? | Only customers assigned to the authenticated sales rep; any other customer returns 403. |
| Which value? | Net value, excluding taxes. |
| Which currencies? | EUR and USD; convert to EUR at the order-date rate (existing FX module). |
| Which orders count? | All, except cancelled ones. |
| Which month? | Calendar month, in the Europe/Lisbon time zone. |
| Where is it used? | API: `GET /customers/{id}/order-totals` → `{currentMonth, previousMonth, currency}`. |
| Out of scope | Screen, export, history beyond two months. |
