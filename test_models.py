from models import PriceRecord, Basket

r = PriceRecord("R001", "rice", "karwan bazar", 72, "kg", "Grain", "2026-11-13")
print(r)

b = Basket("Weekly")
b.add_item("rice", 5)
print(b.to_dict())