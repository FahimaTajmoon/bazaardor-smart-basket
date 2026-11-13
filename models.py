"""Data model classes for BazaarDor."""

# Fixed options are stored in tuples because they never change.
UNITS = ("kg", "litre", "dozen", "piece")
CATEGORIES = ("Grain", "Vegetable", "Protein", "Oil", "Spice", "Other")


class PriceRecord:
    """One price of one item at one bazaar on one date."""

    def __init__(self, record_id, item, bazaar, price, unit, category, date):
        self.record_id = record_id
        self.item = item.strip().title()      # "rice " -> "Rice"
        self.bazaar = bazaar.strip().title()
        self.price = float(price)
        self.unit = unit
        self.category = category
        self.date = date                      # text in YYYY-MM-DD format

    def to_dict(self):
        """Convert the object to a dictionary so it can be saved as JSON."""
        return {
            "record_id": self.record_id,
            "item": self.item,
            "bazaar": self.bazaar,
            "price": self.price,
            "unit": self.unit,
            "category": self.category,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a PriceRecord from a dictionary loaded from JSON."""
        return cls(
            data["record_id"], data["item"], data["bazaar"], data["price"],
            data["unit"], data["category"], data["date"],
        )

    def __str__(self):
        return (f"[{self.record_id}] {self.item} at {self.bazaar}: "
                f"{self.price:.2f} Tk per {self.unit} ({self.date})")


class Basket:
    """A shopping list: item name mapped to quantity."""

    def __init__(self, name, items=None):
        self.name = name.strip()
        self.items = items if items is not None else {}

    def add_item(self, item, quantity):
        """Add an item, or increase its quantity if it is already there."""
        item = item.strip().title()
        self.items[item] = self.items.get(item, 0) + quantity

    def remove_item(self, item):
        """Remove an item. Returns True if removed, False if not found."""
        item = item.strip().title()
        if item in self.items:
            del self.items[item]
            return True
        return False

    def to_dict(self):
        return {"name": self.name, "items": self.items}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["items"])