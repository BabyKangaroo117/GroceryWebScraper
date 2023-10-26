from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
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
        try:
            self.driver.get("https://shop.wegmans.com/search?search_term=chicken&search_is_autocomplete=true")
        except Exception as e:
            print(f"Error occurred while retrieving the webpage: {e}")

        time.sleep(2)
        try:
            # Click Wegman's in store button
            in_store_button = self.driver.find_element(By.XPATH,
                                                       value='//*[@id="shopping-selector-shop-context-intent-instore"]')
            in_store_button.click()
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Error occurred while clicking in store button: {e}")

        time.sleep(2)

        try:
            # Click the reload button
            reload_button = self.driver.find_element(By.XPATH, value='//*[@id="react"]/div[2]/div/button')
            reload_button.click()
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Error occurred while clicking reload button: {e}")

        time.sleep(2)
    def scrape_wegmans(self, items: list, zipcode: str):
        self._set_store_location(zipcode)

        data = {zipcode: {"Wegmans": {"Items": {}}}}
        for item in items:
            data[zipcode]["Wegmans"]["Items"][item] = self._process_data(item)

        json_data = json.dumps(data)
        with open("grocery_data.json", 'w') as file:
            file.write(json_data)

    def _item_block_html(self, item):
        self.driver.get(f"https://shop.wegmans.com/search?search_term={item}&search_is_autocomplete=true")
        time.sleep(3)

        # Find all the item names, images on webpage
        # Scroll down a number of times to scrape more items
        items = []
        scrolls = 3
        for i in range(scrolls):
            items.extend(self.driver.find_elements(By.CLASS_NAME, value="css-1u1k9gp"))
            self.driver.find_element(By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
        print(items)
        return items

    def _process_item_block(self, item_objects: list[WebElement]):
        name = []
        price = []
        unit_price = []
        image_url = []
        for item in item_objects:
            name.append(item.find_element(By.CLASS_NAME, value="css-131yigi").text)
            price.append(item.find_element(By.CLASS_NAME, value="css-zqx11d").text)
            unit_price.append(item.find_element(By.CLASS_NAME, value="css-1kh7mkb").text)
            image_url.append(item.find_element(By.CLASS_NAME, value="css-15zffbe").get_attribute("src"))

        return name, price, unit_price, image_url

    def scrape_website(self, item):

        html_block = self._item_block_html(item)
        name, price, unit_price, image = self._process_item_block(html_block)
        return name, price, unit_price, image


    def _process_data(self, item: str):
        wegmans_data = []
        process_price = ProcessPrices()
        items, prices, unit_prices, images = self.scrape_website(item)
        # Extract strings from selenium unit price objects. Makes unit testing following functions easier
        # Process unit price data
        processed_unit_prices = []
        for price in unit_prices:
            processed_unit_prices.append(process_price.process_price(price))
        # process individual price data
        prices = [float(price.text.replace('$', "").replace(" /ea", "")) for price in prices]

        # Make sure index won't go out of range
        length = len(items)

        # Set to five items for now
        for num in range(length):
            try:
                wegmans_data[num] = {"name": items[num],
                                     "price": prices[num],
                                     "price_per_ounce": processed_unit_prices[num],
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
            try:
                processed_unit_prices.append(process_price(price))
            except Exception as e:
                print("Didn't process unit price")
                processed_unit_prices.append("")

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



