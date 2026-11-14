
from datetime import date

from models import PriceRecord, UNITS, CATEGORIES
from validation import (validate_text, validate_price, validate_date,
                        validate_unique_id)
from storage import load_records, save_records

MENU = (
    "Add a price record",
    "View all records",
    "Search by item or bazaar",
    "Update a price",
    "Delete a record",
    "Price summary for an item",
    "Exit",
)


def ask(prompt, validator, *extra):
    """Keep asking until the input passes the given validation function."""
    while True:
        try:
            return validator(input(prompt), *extra)
        except ValueError as error:
            print("  Error:", error)


def read_number(prompt, lowest, highest):
    """Keep asking until the user types a whole number in the given range."""
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print(f"  Error: enter a number from {lowest} to {highest}.")
            continue
        if lowest <= number <= highest:
            return number
        print(f"  Error: enter a number from {lowest} to {highest}.")


def choose_option(title, options):
    """Show the options of a tuple as a numbered list and return the choice."""
    print(f"  {title}:")
    for number, option in enumerate(options, start=1):
        print(f"    {number}. {option}")
    return options[read_number("  Choose a number: ", 1, len(options)) - 1]


def date_or_today(value):
    """An empty answer means today's date."""
    if value.strip() == "":
        return date.today().isoformat()
    return validate_date(value)


def find_record(records, record_id):
    """Return the record with this ID, or None if it does not exist."""
    for record in records:
        if record.record_id == record_id.strip().upper():
            return record
    return None


def show_table(records):
    """Print records as a simple table."""
    if not records:
        print("  No records to show.")
        return
    print(f"  {'ID':<6}{'Item':<14}{'Bazaar':<18}{'Price':>9}  {'Unit':<7}"
          f"{'Category':<11}{'Date'}")
    print("  " + "-" * 75)
    for record in records:
        print(f"  {record.record_id:<6}{record.item:<14}{record.bazaar:<18}"
              f"{record.price:>9.2f}  {record.unit:<7}{record.category:<11}"
              f"{record.date}")
    print(f"  Total: {len(records)} record(s)")


def save_changes(records):
    """Save after every change so no data is lost."""
    if save_records(records):
        print("  Saved.")
    else:
        print("  Warning: could not save the file.")


def add_record(records, used_ids):
    record_id = ask("  Record ID (e.g. R001): ", validate_unique_id, used_ids)
    item = ask("  Item name: ", validate_text, "Item name")
    bazaar = ask("  Bazaar name: ", validate_text, "Bazaar name")
    price = ask("  Price (Tk): ", validate_price)
    unit = choose_option("Unit", UNITS)
    category = choose_option("Category", CATEGORIES)
    record_date = ask("  Date YYYY-MM-DD (press Enter for today): ",
                      date_or_today)

    records.append(PriceRecord(record_id, item, bazaar, price, unit,
                               category, record_date))
    used_ids.add(record_id)
    print("  Record added.")
    save_changes(records)


def search_records(records):
    keyword = ask("  Item or bazaar to search: ", validate_text, "Search text")
    keyword = keyword.lower()
    matches = [record for record in records
               if keyword in record.item.lower()
               or keyword in record.bazaar.lower()]
    show_table(matches)


def update_price(records):
    record = find_record(records, input("  Record ID to update: "))
    if record is None:
        print("  Error: no record with that ID.")
        return
    print("  Current:", record)
    record.price = ask("  New price (Tk): ", validate_price)
    print("  Price updated.")
    save_changes(records)


def delete_record(records, used_ids):
    record = find_record(records, input("  Record ID to delete: "))
    if record is None:
        print("  Error: no record with that ID.")
        return
    print("  Found:", record)
    if input("  Type y to confirm delete: ").strip().lower() == "y":
        records.remove(record)
        used_ids.discard(record.record_id)
        print("  Record deleted.")
        save_changes(records)
    else:
        print("  Delete cancelled.")


def price_summary(records):
    item = ask("  Item name: ", validate_text, "Item name").title()
    matches = [record for record in records if record.item == item]
    if not matches:
        print(f"  No prices recorded for {item}.")
        return

    prices = [record.price for record in matches]
    cheapest = min(matches, key=lambda record: record.price)
    costliest = max(matches, key=lambda record: record.price)
    average = sum(prices) / len(prices)

    print(f"  {item}: {len(prices)} price(s) recorded")
    print(f"  Cheapest : {cheapest.price:.2f} Tk at {cheapest.bazaar}")
    print(f"  Highest  : {costliest.price:.2f} Tk at {costliest.bazaar}")
    print(f"  Average  : {average:.2f} Tk")
    if costliest.price > cheapest.price:
        saving = (costliest.price - cheapest.price) / costliest.price * 100
        print(f"  Buying at {cheapest.bazaar} saves {saving:.1f}%")


def main():
    records = load_records()
    used_ids = {record.record_id for record in records}  
    print("=" * 40)
    print("  BazaarDor: Local Market Price Book")
    print("=" * 40)
    print(f"  Loaded {len(records)} record(s).")

    while True:
        print()
        for number, label in enumerate(MENU, start=1):
            print(f"  {number}. {label}")
        choice = read_number("  Choose an option: ", 1, len(MENU))
        print()

        if choice == 1:
            add_record(records, used_ids)
        elif choice == 2:
            show_table(records)
        elif choice == 3:
            search_records(records)
        elif choice == 4:
            update_price(records)
        elif choice == 5:
            delete_record(records, used_ids)
        elif choice == 6:
            price_summary(records)
        else:
            print("  Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Program closed.")