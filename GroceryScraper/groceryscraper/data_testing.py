import json
from shoprite_webscraper import ShopriteWebScraper


from wegmans_webscraper import WegmansWebScraper
# with open("grocery_data.json", "r") as file:
#     data = json.load(file)
#
#
# items = data['18976']['Wegmans']["Items"]
#
# for key, value in items.items():
#     print(key)
#     for key_2, value_2 in value.items():
#         print(value_2["name"])
#         print(value_2["price"])
#         print(value_2["price_per_ounce"])
#         print()

# webscrape = WegmansWebScraper()
# with open("../grocery_data.json", "r") as file:
#     data = json.load(file)
#
# items = data['18976']['Wegmans']["Items"]
# unit_prices = []
# for key, value in items.items():
#     for key_2, value_2 in value.items():
#         unit_prices.append(value_2["price_per_ounce"])
#
#
# print(webscrape.process_unit_price_data(unit_prices))

def update_items_shoprite():
    with open("shoprite_grocery_data_copy.json") as file:
        data = file.read()

    json_data = json.loads(data)
    websraper = ShopriteWebScraper()
    data = websraper.scrape_shoprite("medium salsa", 18976)
    json_data["18976"]["Shoprite"]["Items"]["Medium-spicy salsa"] = data

    with open("shoprite_grocery_data_copy.json", 'w') as file:
        json_data_2 = json.dumps(json_data)
        file.write(json_data_2)

def update_item_wegmans():
    with open("wegmans_grocery_data.json") as file:
        data = file.read()

    json_data = json.loads(data)
    websraper = WegmansWebScraper()
    data = websraper.scrape_wegmans("Vanilla ice cream", 18976)
    json_data["18976"]["Wegmans"]["Items"]["Vanilla ice cream"] = data

    with open("wegmans_grocery_data.json", 'w') as file:
        json_data_2 = json.dumps(json_data)
        file.write(json_data_2)

update_item_wegmans()