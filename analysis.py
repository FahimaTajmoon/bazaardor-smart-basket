# Basket price analysis per market.

import numpy as np


# Return latest valid (bazaar, price) pairs for an item.
def _item_prices(manager, item):
    records = manager.records_for(item)
    # Keep newest record per bazaar.
    latest = {}
    for record in records:
        market = record.bazaar
        previous = latest.get(market)
        if previous is None or record.date >= previous.date:
            latest[market] = record
    return [(market, float(record.price)) for market, record in latest.items()
            if np.isfinite(record.price) and record.price > 0]


# Return cheapest-per-item basket estimate and totals.
def shopping_estimate(manager, items):
    lines = []
    missing = []
    cheapest_costs = []
    average_costs = []

    for item, quantity in items.items():
        quantity = float(quantity)
        if not np.isfinite(quantity) or quantity <= 0:
            raise ValueError(f"Quantity for {item} must be greater than zero")
        prices = _item_prices(manager, item)
        if not prices:
            missing.append(item)
            continue

        markets = [market for market, _ in prices]
        values = np.array([price for _, price in prices], dtype=float)
        lowest_index = int(np.argmin(values))
        cheapest = float(values[lowest_index] * quantity)
        average = float(np.mean(values) * quantity)
        lines.append({
            "item": item,
            "quantity": quantity,
            "market": markets[lowest_index],
            "cheapest_cost": cheapest,
            "average_cost": average,
        })
        cheapest_costs.append(cheapest)
        average_costs.append(average)

    total_cheapest = float(np.sum(cheapest_costs))
    total_average = float(np.sum(average_costs))
    return {
        "lines": lines,
        "missing": missing,
        "total_cheapest": total_cheapest,
        "total_average": total_average,
        "saving": total_average - total_cheapest,
    }


# Return total basket cost for bazaars carrying all items.
def cost_by_market(manager, items):
    if not items:
        return {}

    cleaned_items = []
    for item, quantity in items.items():
        quantity = float(quantity)
        if not np.isfinite(quantity) or quantity <= 0:
            raise ValueError(f"Quantity for {item} must be greater than zero")
        cleaned_items.append((item, quantity))

    totals = None
    for item, quantity in cleaned_items:
        prices = dict(_item_prices(manager, item))
        if not prices:
            return {}
        if totals is None:
            totals = {market: price * quantity for market, price in prices.items()}
        else:
            totals = {
                market: totals[market] + prices[market] * quantity
                for market in totals
                if market in prices
            }

    return {market: float(total) for market, total in (totals or {}).items()}
