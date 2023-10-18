from webscraper import WebScraper

webscraper = WebScraper()
# webscraper.scrape_wegmans("small pork chops")
webscraper.retrieve_webpage()
lst = ["chicken", "bread"]
webscraper.scrape_wegmans(lst, "18976")



