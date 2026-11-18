from models import PriceRecord, UNITS, CATEGORIES
from validation import (
    validate_text,
    validate_price,
    validate_date,
    validate_choice,
    validate_unique_id,
)


class BazaarManager:

    def __init__(self, records=None):
        self.records = list(records) if records is not None else []

    def records_for(self, item):
        item_key = str(item).strip().casefold()
        return [record for record in self.records
                if record.item.strip().casefold() == item_key]

    def add_record(self, record):
        if not isinstance(record, PriceRecord):
            raise TypeError("record must be a PriceRecord")
        record.record_id = validate_unique_id(record.record_id, self._used_ids())
        self.records.append(record)
        return record

    def search_records(self, keyword):
        keyword = str(keyword).strip().casefold()
        if not keyword:
            return []
        return [record for record in self.records
                if keyword in record.item.casefold()
                or keyword in record.bazaar.casefold()]

    def update_record(self, record_id, **changes):
        record = self.get_record(record_id)
        if record is None:
            return None
        allowed = {"item", "bazaar", "price", "unit", "category", "date"}
        unknown = set(changes) - allowed
        if unknown:
            raise ValueError(f"Unsupported field(s): {', '.join(sorted(unknown))}")
        cleaned = {}
        for field, value in changes.items():
            if field in {"item", "bazaar"}:
                text = "" if value is None else str(value)
                cleaned[field] = validate_text(text, field.title()).title()
            elif field == "price":
                cleaned[field] = validate_price(value)
            elif field == "unit":
                cleaned[field] = validate_choice(value, UNITS, "Unit")
            elif field == "category":
                cleaned[field] = validate_choice(value, CATEGORIES, "Category")
            elif field == "date":
                date_text = "" if value is None else str(value)
                cleaned[field] = validate_date(date_text)
        for field, value in cleaned.items():
            setattr(record, field, value)
        return record

    def delete_record(self, record_id):
        record = self.get_record(record_id)
        if record is not None:
            self.records.remove(record)
        return record

    def get_record(self, record_id):
        wanted = str(record_id).strip().casefold()
        return next((record for record in self.records
                     if record.record_id.casefold() == wanted), None)

    def _used_ids(self):
        return {record.record_id.upper() for record in self.records}
