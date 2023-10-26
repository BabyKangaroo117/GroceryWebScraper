import os,  sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from process_prices import ProcessPrices
from webscraper import WebScraper
from grocery_list import GroceryList

# def test_scrape_wegmans():
#     webscrape = WebScraper()
#     webscrape.retrieve_webpage()
#     grocery_list = GroceryList()
#     for item in grocery_list.grocery_list:
#         items, prices, images, unit_prices = webscrape.scrape_website(item)
#
#         assert (len(items) == len(prices) == len(images) == len(unit_prices))
#

# def test_item_block_html():
#     webscrape = WebScraper()
#     webscrape.retrieve_webpage()
#     grocery_list = GroceryList()
#     print(webscrape.item_block_html(grocery_list.grocery_list[0]))

def test_process_item_block():
    webscrape = WebScraper()
    webscrape.retrieve_webpage()
    grocery_list = GroceryList()
    item = webscrape.item_block_html(grocery_list.grocery_list[0])
    webscrape.process_item_block(item)