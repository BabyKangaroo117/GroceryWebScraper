from wegmans_webscraper import WegmansWebScraper
from shoprite_webscraper import ShopriteWebScraper
from GroceryScraper.groceryscraper.grocery_list import GroceryList
import organize_data
from database_connection import DatabaseConnection

# wegmans_webscrape = WegmansWebScraper()
# wegmans_webscrape.retrieve_webpage()
# grocery_list = GroceryList()
# wegmans_webscrape.scrape_wegmans(grocery_list.grocery_list, 18976)


# shoprite_webscrape = ShopriteWebScraper()
# grocery_list = GroceryList()
# shoprite_webscrape.scrape_shoprite(grocery_list.grocery_list, 18976)


area_items = organize_data.format_for_sql_insert()
database_connection = DatabaseConnection()
for item in area_items:
    database_connection.post_area_item(item[0], item[1], item[2], item[3], item[4], item[5], item[6])



