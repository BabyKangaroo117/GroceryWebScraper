from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
import time
import json
from GroceryScraper.groceryscraper.processing_prices.wegmans_process_prices import WegmansProcessPrices


class WegmansWebScraper:
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
        with open("../grocery_data/wegmans_grocery_data.json", 'w') as file:
            file.write(json_data)

    def item_block_html(self, item):
        print(item)
        self.driver.get(f"https://shop.wegmans.com/search?search_term={item}&search_is_autocomplete=true")
        time.sleep(4)

        # Get html block that contains html name, price, unit price, image url
        # Scroll down a number of times to scrape more items
        items = []
        scrolls = 3
        for i in range(scrolls):
            items.extend(self.driver.find_elements(By.CLASS_NAME, value="css-1u1k9gp"))
            self.driver.find_element(By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
        print(items)
        return items

    def process_item_block(self, item_objects: list[WebElement]):
        name = []
        price = []
        unit_price = []
        image_url = []
        for item in item_objects:
            try:
                name.append(item.find_element(By.CLASS_NAME, value="css-60bqrp").text)
            except NoSuchElementException:
                name.append("Not found")

            try:
                price.append(item.find_element(By.CLASS_NAME, value="css-zqx11d").text)
            except NoSuchElementException:
                price.append("Not found")

            try:
                unit_price.append(item.find_element(By.CLASS_NAME, value="css-1kh7mkb").text)
            except NoSuchElementException:
                unit_price.append("Not found")

            try:
                image_url.append(item.find_element(By.CLASS_NAME, value="css-15zffbe").get_attribute("src"))
            except NoSuchElementException:
                image_url.append("Not found")

        return name, price, unit_price, image_url

    def scrape_website(self, item):

        html_block = self.item_block_html(item)
        name, price, unit_price, image = self.process_item_block(html_block)
        return name, price, unit_price, image

    def _process_data(self, item: str):
        wegmans_data = []
        process_price = WegmansProcessPrices()
        items, prices, unit_prices, images = self.scrape_website(item)
        # Extract strings from selenium unit price objects. Makes unit testing following functions easier
        # Process unit price data
        units = []
        unit_prices_processed = []
        count = 0
        for unit_price in unit_prices:
            print(items[count])
            print(unit_price)
            if unit_price != "Not found":
                units.append(process_price.convert_unit_type(process_price.find_units(unit_price)[0]))
                unit_prices_processed.append(process_price.process_price_converted(unit_price))
            else:
                units.append("Not Found")
                unit_prices_processed.append(10000)

            # processed_unit_prices.append(process_price.process_price_converted(unit_price))
            count+=1

        # process individual price data
        prices = [float(price.replace('$', "").replace(" /ea", "").replace(" /lb", "")) if price != "Not found" else 10000 for price in prices]

        # Make sure index won't go out of range
        length = len(items)

        # Set to five items for now
        for num in range(length):
            try:
                wegmans_data.append({"name": items[num],
                                     "price": prices[num],
                                     "unit_price": unit_prices_processed[num],
                                     "units": units[num],
                                     "image": images[num]})
            except IndexError:
                with open("../item_issues", "a") as file:
                    file.write(item + "\n")


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
        process_price = WegmansProcessPrices()
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

    def close_browser(self):
        self.driver.quit()



