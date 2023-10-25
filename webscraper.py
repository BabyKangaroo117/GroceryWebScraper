from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
from process_prices import ProcessPrices


class WebScraper:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--disable-javascript")
        self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def retrieve_webpage(self):
        """
        Retrieve webpage and get past initial website command
        :return:
        """
        self.driver.get("https://shop.wegmans.com/search?search_term=chicken&search_is_autocomplete=true")

        # Click Wegman's in store button
        time.sleep(2)
        in_store_button = self.driver.find_element(By.XPATH,
                                                   value='//*[@id="shopping-selector-shop-context-intent-instore"]')
        in_store_button.click()

        # Click the reload button
        time.sleep(2)
        reload_button = self.driver.find_element(By.XPATH, value='//*[@id="react"]/div[2]/div/button')
        reload_button.click()
        time.sleep(2)

    def scrape_wegmans(self, items: list, zipcode: str):
        self._set_store_location(zipcode)

        data = {zipcode: {"Wegmans": {"Items": {}}}}
        for item in items:
            data[zipcode]["Wegmans"]["Items"][item] = self._process_data(item)

        json_data = json.dumps(data)
        with open("grocery_data.json", 'w') as file:
            file.write(json_data)

    def scrape_website(self, item):
        """
                Scrape wegmans website for an item
                :param item: Item to be searched
                :return:
                """

        self.driver.get(f"https://shop.wegmans.com/search?search_term={item}&search_is_autocomplete=true")
        time.sleep(2)

        # Find all the item names, images on webpage
        # Scroll down a number of times to scrape more items
        scrolls = 3
        items = []
        prices = []
        images = []
        unit_prices = []
        print(item)

        for i in range(scrolls):
            items.extend(self.driver.find_elements(By.CLASS_NAME, value="css-131yigi"))
            prices.extend(self.driver.find_elements(By.CLASS_NAME, value="css-zqx11d"))
            images.extend(self.driver.find_elements(By.CLASS_NAME, value="css-15zffbe"))
            unit_prices.extend(self.driver.find_elements(By.CLASS_NAME, value="css-1kh7mkb"))
            self.driver.find_element(By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
        print(len(items))
        print(len(prices))
        print(len(unit_prices))

        return items, prices, images, unit_prices

    def _process_data(self, item: str):
        wegmans_data = []
        process_price = ProcessPrices()
        items, prices, images, unit_prices = self.scrape_website(item)
        # Extract strings from selenium unit price objects. Makes unit testing following functions easier
        unit_price_str = [price.text for price in unit_prices]
        # Process unit price data
        unit_prices = process_price(unit_price_str)
        # process individual price data
        prices = [float(price.text.replace('$', "").replace(" /ea", "")) for price in prices]

        # Make sure index won't go out of range
        length = len(items) if (len(items) < len(prices)) and (len(items) < len(images)) else len(images)

        # Set to five items for now
        for num in range(length):
            try:
                wegmans_data[num] = {"name": items[num],
                                     "price": prices[num],
                                     "price_per_ounce": unit_prices[num],
                                     "image": images[num].get_attribute("src")}
            except IndexError:
                with open("item_issues", "a") as file:
                    file.write(item)


        # Currently set to return one item which is the cheapest by unit of ounces
        #cheapest_item = self._find_cheapest_item(wegmans_data)
        return wegmans_data

    def _set_store_location(self, zipcode):
        """Set the store location"""
        location_button = self.driver.find_element(By.XPATH, value='//*[@id="sticky-react-header"]/div/div[2]/div[1]/div/div[3]/button')
        self.driver.execute_script("arguments[0].click();", location_button)
        time.sleep(3)
        enter_zipcode = self.driver.find_element(By.XPATH, value='//*[@id="shopping-selector-search-cities"]')
        enter_zipcode.send_keys(zipcode)
        enter_zipcode.send_keys(Keys.ENTER)
        time.sleep(1)
        set_store_button = self.driver.find_elements(By.CLASS_NAME, value='button')
        set_store_button[1].click()

    def process_unit_price_data(self, unit_prices: list):
        """Process the text from selenium and format into an integer with unit ounces"""
        process_price = ProcessPrices()
        processed_unit_prices = []
        # Process unit price
        for price in unit_prices:
            processed_unit_prices = process_price(price)

        return processed_unit_prices

    def _find_cheapest_item(self, items: dict):
        """Find the cheapest item of the scraped data"""
        smallest = items[0]
        for key, value in items.items():
            if value["price_per_ounce"] < smallest["price_per_ounce"]:
                smallest = value
        return smallest

    def scrape_shoprite(self, item):
        """
        Retrieve the name, price and jpg of items on a webpage from shoprite
        :return: Return a dictionary with a num as the key and a value that's a dictionary with the name, price and jpg
        """
        shoprite_data = {}
        self.driver.get(f"https://www.shoprite.com/sm/pickup/rsid/3000/results?q={item}")

        items = self.driver.find_elements(By.CLASS_NAME, value='boGWcY')
        print(f"Items {len(items)}")
        prices = self.driver.find_elements(By.CLASS_NAME, value="bOJorN")
        print(f"prices {len(prices)}")
        images = self.driver.find_elements(By.CLASS_NAME, value="kKApVr")
        print(f"images {len(images)}")

        # Strip price and convert to float
        int_prices = [float(price.text.replace('$', "").replace("/lb", "").replace(" avg/ea", "")) for price in prices]

        # Make sure index won't go out of range
        length = len(items) if (len(items) < len(prices)) and (len(items) < len(images)) else len(prices)

        for num in range(length):
            shoprite_data[num] = {"name": items[num].text,
                                 "price": int_prices[num],
                                 "image": images[num].get_attribute("src")}

        print(shoprite_data)
    def close_browser(self):
        self.driver.quit()



