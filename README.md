# BazarDor Smart Basket (বাজার দর)

It compares local bazaar prices and finds the cheapest bazaar for a shopping basket (Tkinter + NumPy).

CSC 4162 Programming in Python, Section C, Fall 2026-27, mid-term group project.

## Team

| Member | Student ID | Name | Files | Branch |
|--------|------------|------|-------|--------|
| 1 | | | `models.py`, `validation.py`, `storage.py` | `feature/models-storage` |
| 2 | | | `manager.py`, `analysis.py` | `feature/manager` |
| 3 | | | `gui_records.py`, `main.py` | `feature/gui-records` |
| 4 | 21-44625-1 | Minhazul Abedin | `gui_basket.py`, `data/prices.json`, `README.md` | `feature/gui-basket` |

## How to run

You need Python 3 with Tkinter (it comes with Python on Windows and macOS).

```bash
pip install numpy
python main.py
```

`main.py` is the file to run.

## Screens

- **Price Records:** add, update, delete and search price records (item, bazaar, date, price).
- **Smart Basket:** build a basket with quantities, see each item's cheapest bazaar and what
  the basket costs at average prices, and rank every bazaar by the cost of the whole basket.

Records are saved to `data/prices.json` after every change and loaded at start.

## Files

| File | What it contains |
|------|------------------|
| `main.py` | The window; puts the two screens together |
| `models.py` | `PriceRecord` and `Basket` classes, the `ITEMS` dictionary and the `MARKETS` tuple |
| `validation.py` | Input checks for date, item, bazaar, price and quantity |
| `storage.py` | Save and load the records as JSON |
| `manager.py` | `BazaarManager`: add, search, update and delete records |
| `analysis.py` | NumPy calculations: cheapest bazaar per item, basket totals, cost at each bazaar |
| `gui_records.py` | The Price Records screen |
| `gui_basket.py` | The Smart Basket screen and the bazaar ranking |
| `data/prices.json` | 50 sample price records |

## Sample data

`data/prices.json` holds 50 **sample** records: all 8 items at all 5 Dhaka bazaars on
15 October 2026, plus 5 items at 2 bazaars a week earlier. The prices are realistic
examples for demonstration, not official prices.
