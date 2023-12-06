# def test_scrape_wegmans():
#     webscrape = WebScraper()
#     webscrape.retrieve_webpage()
#     grocery_list = GroceryList()
#     for item in grocery_list.grocery_list:
#         names, prices, unit_prices, images = webscrape.scrape_website(item)
#
#         assert (len(names) == len(prices) == len(images) == len(unit_prices))

# def test_item_block_html():
#     webscrape = WebScraper()
#     webscrape.retrieve_webpage()
#     grocery_list = GroceryList()
#     print(webscrape.item_block_html(grocery_list.grocery_list[0]))


# def test_process_item_block():
#     webscrape = WebScraper()
#     webscrape.retrieve_webpage()
#     grocery_list = GroceryList()
#     item = webscrape.item_block_html(grocery_list.grocery_list[0])
#     webscrape.process_item_block(item)
#
# def test_item_block_html():
#     webscrape = WebScraper()
#     webscrape.retrieve_webpage()
#     grocery_list = GroceryList().grocery_list
#     for item in grocery_list:
#         print(item)
#         item_block = webscrape.item_block_html(item)
#     assert item_block
#