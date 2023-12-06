import requests


class DatabaseConnection:
    def __init__(self):
        self.server_name = "https://frugl-server.database.windows.net"

    def post_area_item(self, postal, item_id, shoprite_unit_price, wegmans_unit_price, shoprite_item, wegmans_item, units):
        post_items = "/api/AreaItems"
        payload = {
          "postalCode": postal,
          "itemId": item_id,
          "shopriteUnitPrice": shoprite_unit_price,
          "wegmansUnitPrice": wegmans_unit_price,
          "shopriteItem": shoprite_item,
          "wegmansItem": wegmans_item,
          "itemUnits": units,
          "item": None,
          "postalCodeNavigation": None
        }

        response = requests.post(self.server_name + post_items, json=payload)

        if response.status_code == 200:
            print("Request successful!")
            data = response.json()  # If the response is JSON
            print(data)
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)

