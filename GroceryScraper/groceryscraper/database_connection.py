import requests

class Database:
    def __init__(self):
        self.server_name = "https://frugl-server.database.windows.net"

    def post_area_item(self):
        post_items = "/api/AreaItems"
        payload = {
          "postalCode": 0,
          "itemId": 0,
          "shopriteUnitPrice": 0,
          "wegmansUnitPrice": 0,
          "shopriteItem": "string",
          "wegmansItem": "string",
          "itemUnits": "string",
          "item": {
            "itemId": 0,
            "itemName": "string"
          },
          "postalCodeNavigation": {
            "postalCode1": 0
          }
        }

        response = requests.post(self.server_name + post_items, json=payload)

        if response.status_code == 200:
            print("Request successful!")
            data = response.json()  # If the response is JSON
            print(data)
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)

