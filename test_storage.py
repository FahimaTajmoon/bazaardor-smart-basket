from models import PriceRecord, Basket
from storage import save_records, load_records, save_baskets, load_baskets

records = [
    PriceRecord("R001", "rice", "karwan bazar", 72, "kg", "Grain", "2026-11-13"),
    PriceRecord("R002", "rice", "new market", 75, "kg", "Grain", "2026-11-13"),
]
print("Saved:", save_records(records, "data/test_prices.json"))
for record in load_records("data/test_prices.json"):
    print(record)

basket = Basket("Weekly")
basket.add_item("rice", 5)
print("Saved:", save_baskets([basket], "data/test_baskets.json"))
print(load_baskets("data/test_baskets.json")[0].to_dict())

print("Missing file gives:", load_records("data/no_such_file.json"))