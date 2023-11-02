from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.remote.webelement import WebElement
import time
import json
from shoprite_process_prices import ShopriteProcessPrices
import re

class ShopriteWebScraper:
    def __init__(self):
        self.driver = ""
        # self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument("--disable-javascript")
        # # self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_experimental_option("detach", True)
        # self.driver = webdriver.Chrome(options=self.chrome_options)

    def create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-javascript")
        # self.chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def retrieve_webpage(self):
        """
        Retrieve webpage and get past initial website command
        :return:
        """
        try:
            self.driver.get("https://www.shoprite.com/sm/pickup/rsid/3000/")
        except Exception as e:
            print(f"Error occurred while retrieving the webpage: {e}")

        time.sleep(2)

    def set_store_location(self, zipcode):
        """Set the store location"""
        location_button = self.driver.find_element(By.CLASS_NAME, value='sc-dlnjPT')
        self.driver.execute_script("arguments[0].click();", location_button)
        time.sleep(1)
        set_store_button = self.driver.find_element(By.CLASS_NAME, value='ChangeStoreButton--1p5tqv5')
        set_store_button.click()
        time.sleep(2)
        enter_zipcode = self.driver.find_element(By.ID, value='googleAutoInput')
        enter_zipcode.send_keys(zipcode)
        time.sleep(1)
        set_zipcode = self.driver.find_element(By.CLASS_NAME, value='AutoPickResultButton--5n7gju')
        self.driver.execute_script("arguments[0].click();", set_zipcode)
        time.sleep(2)
        select_store = self.driver.find_element(By.CLASS_NAME, value="SelectStoreButton--x69z79")
        select_store.click()
        time.sleep(2)
        captch = self.driver.find_element(By.CLASS_NAME, value="ctp-checkbox-label")
        captch.click()

    def scrape_shoprite(self, items: list, zipcode: str):
        #self._set_store_location(zipcode)

        data = {zipcode: {"Shoprite": {"Items": {}}}}
        for item in items:
            data[zipcode]["Shoprite"]["Items"][item] = self._process_data(item)

        json_data = json.dumps(data)
        with open("grocery_data_shoprite.json", 'w') as file:
            file.write(json_data)

    def item_block_html(self, item):

        self.driver = self.create_driver()
        time.sleep(1)
        self.driver.get(f"https://www.shoprite.com/sm/pickup/rsid/439/results?q={item}")
        # Get html block that contains html name, price, unit price, image url
        # Scroll down a number of times to scrape more items
        items = []
        scrolls = 1
        time.sleep(2)
        for i in range(scrolls):
            print(1)
            items.extend(self.driver.find_elements(By.CLASS_NAME, value="ColListing--1fk1zey"))
            self.driver.find_element(By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        print(items)

        return items

    def process_item_block(self, item_objects: list[WebElement]):
        names = []
        prices = []
        unit_prices = []
        image_urls = []
        print(len(item_objects))
        for item in item_objects:
            # If html block is an item. If name is "" then not an item
            if item.find_element(By.CLASS_NAME, value="ProductCardNameWrapper--g2y3vm").text.split("\n")[0] != "":
                try:
                    names.append(item.find_element(By.CLASS_NAME, value="ProductCardNameWrapper--g2y3vm").text.split("\n")[0])
                except NoSuchElementException:
                    names.append("Not found")

                try:
                    prices.append(item.find_element(By.CLASS_NAME, value="ProductPrice--w5mr9b").text)
                except NoSuchElementException:
                    prices.append("Not found")

                try:
                    unit_prices.append(item.find_element(By.CLASS_NAME, value="ProductUnitPrice--slbqgg").text)
                except NoSuchElementException:
                    unit_prices.append("Not found")

                try:
                    image_urls.append(item.find_element(By.CLASS_NAME, value="Image--v39pjb").get_attribute("src"))
                except NoSuchElementException:
                    image_urls.append("Not found")


        # names = [name for name in names if name != ""]
        # prices = [price for price in prices if price != ""]
        # unit_prices = [unit_price for unit_price in unit_prices if unit_price != ""]

        print(len(names), names)
        print(len(prices), prices)
        print(len(unit_prices), unit_prices)
        print(len(image_urls), image_urls)
        self.driver.quit()
        del self.driver
        # assert len(names) == len(prices) == len(unit_prices) == len(image_urls)
        return names, prices, unit_prices, image_urls

    def scrape_website(self, item):

        html_block = self.item_block_html(item)
        name, price, unit_price, image = self.process_item_block(html_block)
        return name, price, unit_price, image


    def _process_data(self, item: str):
        shoprite_data = []
        process_price = ShopriteProcessPrices()
        items, prices, unit_prices, images = self.scrape_website(item)
        # Extract strings from selenium unit price objects. Makes unit testing following functions easier
        # Process unit price data
        processed_unit_prices = []
        for price in unit_prices:
            processed_unit_prices.append(process_price.process_unit_price(price))
        # process individual price date
        processed_prices = []
        for price in prices:
            processed_prices.append(process_price.process_individual_price(price))

        # Make sure index won't go out of range
        length = len(items)

        # Set to five items for now
        for num in range(length):
            try:
                shoprite_data[num] = {"name": items[num],
                                     "price": processed_prices[num],
                                     "price_per_ounce": processed_unit_prices[num],
                                     "image": images[num].get_attribute("src")}
            except IndexError:
                with open("item_issues", "a") as file:
                    file.write(item)


        # Currently set to return one item which is the cheapest by unit of ounces
        #cheapest_item = self._find_cheapest_item(wegmans_data)
        return shoprite_data


    def _find_cheapest_item(self, items: dict):
        """Find the cheapest item of the scraped data"""
        smallest = items[0]
        for key, value in items.items():
            if value["price_per_ounce"] < smallest["price_per_ounce"]:
                smallest = value
        return smallest

    def close_browser(self):
        self.driver.quit()



