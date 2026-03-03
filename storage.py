import json
import os

FILE = "wardrobe.json"

def load_items():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)

def save_items(new_items):
    items = load_items()
    items.extend(new_items)

    with open(FILE, "w") as f:
        json.dump(items, f, indent=4)