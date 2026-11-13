

import json
import os

from models import PriceRecord, Basket

DATA_FOLDER = "data"
PRICES_FILE = os.path.join(DATA_FOLDER, "prices.json")
BASKETS_FILE = os.path.join(DATA_FOLDER, "baskets.json")


def read_json(path):
    
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []        # first run: the file does not exist yet
    except (ValueError, OSError):
        print(f"Warning: could not read {path}. Starting with empty data.")
        return []
    if not isinstance(data, list):
        return []
    return data


def write_json(path, data):

    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError:
        return False


def load_records(path=PRICES_FILE):
   
    records = []
    for row in read_json(path):
        try:
            records.append(PriceRecord.from_dict(row))
        except (KeyError, ValueError, TypeError, AttributeError):
            continue
    return records


def save_records(records, path=PRICES_FILE):
    
    return write_json(path, [record.to_dict() for record in records])


def load_baskets(path=BASKETS_FILE):
   
    baskets = []
    for row in read_json(path):
        try:
            baskets.append(Basket.from_dict(row))
        except (KeyError, ValueError, TypeError, AttributeError):
            continue
    return baskets


def save_baskets(baskets, path=BASKETS_FILE):
    
    return write_json(path, [basket.to_dict() for basket in baskets])