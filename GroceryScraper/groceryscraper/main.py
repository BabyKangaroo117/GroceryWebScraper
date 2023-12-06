from GroceryScraper.groceryscraper.database import organize_data
from GroceryScraper.groceryscraper.database.database_connection import DatabaseConnection
from GroceryScraper.groceryscraper.webscrapers.shoprite_webscraper import ShopriteWebScraper
from GroceryScraper.groceryscraper.webscrapers.wegmans_webscraper import WegmansWebScraper
from GroceryScraper.groceryscraper.grocery_data.grocery_list import GroceryList
from GroceryScraper.groceryscraper.database.organize_data import format_for_sql_insert

#Run Wegmans webscraper
wegmans_webscrape = WegmansWebScraper()
wegmans_webscrape.retrieve_webpage()
grocery_list = GroceryList()
wegmans_webscrape.scrape_wegmans(grocery_list.grocery_list, 18976)

#Run Shoprite webscraper
shoprite_webscrape = ShopriteWebScraper()
grocery_list = GroceryList()
shoprite_webscrape.scrape_shoprite(grocery_list.grocery_list, 18976)


# Run this once data has been collected and saved in json files
print(format_for_sql_insert())


# Insert into database. Currently not working

# area_items = organize_data.format_for_sql_insert()
# database_connection = DatabaseConnection()
# for item in area_items:
#     database_connection.post_area_item(item[0], item[1], item[2], item[3], item[4], item[5], item[6])



