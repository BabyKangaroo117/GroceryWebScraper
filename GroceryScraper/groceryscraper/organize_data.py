import json


def wegmans_grocery_items() -> dict:
    with open("wegmans_grocery_data.json") as file:
        data = file.read()

    json_data = json.loads(data)

    grocery_items = json_data["18976"]["Wegmans"]["Items"]

    return grocery_items


def shoprite_grocery_items() -> dict:
    with open("shoprite_grocery_data_copy.json") as file:
        data = file.read()

    json_data = json.loads(data)

    grocery_items = json_data["18976"]["Shoprite"]["Items"]

    return grocery_items


def find_cheapest_price_wegmans() -> list[dict]:
    grocery_items = wegmans_grocery_items()
    cheapest_items = []

    for item_name, item_data in grocery_items.items():
        sorted_item_unit_prices = sorted(item_data, key=lambda x: x['unit_price'])
        print(sorted_item_unit_prices)
        cheapest_items.append(sorted_item_unit_prices[0])

    return cheapest_items


def get_numeric_value(item):
    """Set items that are not found to 10000 so that they are at the end of the sorted list"""
    # Try to convert to float, return 0 for non-numeric values
    try:
        return float(item['unit_price'])
    except ValueError:
        return 10000


def find_cheapest_price_shoprite() -> list[dict]:
    grocery_items = shoprite_grocery_items()
    cheapest_items = []

    for item_name, item_data in grocery_items.items():

        sorted_item_unit_prices = sorted(item_data, key=get_numeric_value)
        print(sorted_item_unit_prices)
        cheapest_items.append(sorted_item_unit_prices[0])
        print(sorted_item_unit_prices[0]["unit_price"])
    return cheapest_items


def format_for_sql_insert():
    """Print data so that it can be inserted into database through azure data studio """
    cheapest_wegmans = find_cheapest_price_wegmans()
    cheapest_shoprite = find_cheapest_price_shoprite()
    item_entries = []
    for num in range(len(cheapest_shoprite)):
        # Hardcoded zipcode because this is a temporary fix to getting around API issue
        postal_code = 18976
        # Item id is a foreign key to item name in the grocery list. In order of grocery list.
        item_id = num + 1
        shoprite_unit_price = cheapest_shoprite[num]["unit_price"]
        wegmans_unit_price = cheapest_wegmans[num]["unit_price"]
        shoprite_item = cheapest_shoprite[num]["name"]
        wegmans_item = cheapest_wegmans[num]["name"]
        item_units = cheapest_wegmans[num]["units"]

        entry = (postal_code, item_id, shoprite_unit_price, wegmans_unit_price, shoprite_item, wegmans_item, item_units)
        item_entries.append(entry)

    return item_entries

# find_cheapest_price_shoprite()
print(format_for_sql_insert())
print(len("Campbell's Condensed Chicken Noodle Soup, 10.75 OZ Can (Pack of 4)"))

