from models import UNITS
from validation import (validate_price, validate_date,
                        validate_choice, validate_unique_id)

print(validate_price("72.5"))
print(validate_date("2026-1-5"))
print(validate_unique_id("r002", {"R001"}))

tests = [
    lambda: validate_price("abc"),
    lambda: validate_price("-10"),
    lambda: validate_date("13/11/2026"),
    lambda: validate_choice("gram", UNITS, "Unit"),
    lambda: validate_unique_id("r001", {"R001"}),
]
for test in tests:
    try:
        test()
    except ValueError as error:
        print("Error:", error)
