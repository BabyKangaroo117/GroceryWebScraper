from wegmans_webscraper import WegmansWebScraper
from shoprite_webscraper import ShopriteWebScraper
from GroceryScraper.groceryscraper.grocery_list import GroceryList

# wegmans_webscrape = WegmansWebScraper()
# wegmans_webscrape.retrieve_webpage()
grocery_list = GroceryList()
# wegmans_webscrape.scrape_wegmans(grocery_list.grocery_list, 18976)

shoprite_webscrape = ShopriteWebScraper()
shoprite_webscrape.scrape_shoprite(grocery_list.grocery_list[1:3], 18976)
# shoprite_webscrape.retrieve_webpage()
# for item in grocery_list.grocery_list[1:5]:
#     shoprite_webscrape.scrape_website(item)


