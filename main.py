from webscraper import WebScraper
from grocery_list import GroceryList

webscraper = WebScraper()
webscraper.retrieve_webpage()
grocery_list = GroceryList()

webscraper.scrape_wegmans(grocery_list.grocery_list, "18976")



