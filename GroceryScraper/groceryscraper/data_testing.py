import json
from wegmans_webscraper import WegmansWebScraper
with open("grocery_data.json", "r") as file:
    data = json.load(file)


items = data['18976']['Wegmans']["Items"]

for key, value in items.items():
    print(key)
    for key_2, value_2 in value.items():
        print(value_2["name"])
        print(value_2["price"])
        print(value_2["price_per_ounce"])
        print()

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
