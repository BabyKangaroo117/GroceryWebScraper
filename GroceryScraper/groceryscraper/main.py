from wegmans_webscraper import WegmansWebScraper
from GroceryScraper.groceryscraper.grocery_list import GroceryList

webscraper = WegmansWebScraper()
webscraper.retrieve_webpage()
grocery_list = GroceryList()

webscraper.scrape_wegmans(grocery_list.grocery_list, 18976)
# webscraper.scrape_wegmans(grocery_list.grocery_list, "18976")



