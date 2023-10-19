from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

class WebScraper:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--disable-javascript")
        # chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def retrieve_webpage(self):
        """
        Retrieve webpage and get past initial website command
        :return:
        """
        self.driver.get("https://shop.wegmans.com/search?search_term=chicken&search_is_autocomplete=true")


        # Click Wegman's in store button
        time.sleep(3)
        in_store_button = self.driver.find_element(By.XPATH,
                                                   value='//*[@id="shopping-selector-shop-context-intent-instore"]')
        in_store_button.click()

        # Click the reload button
        time.sleep(2)
        reload_button = self.driver.find_element(By.XPATH, value='//*[@id="react"]/div[2]/div/button')
        reload_button.click()
        time.sleep(3)

    def _set_store_location(self, zipcode):
        """Set the store location"""
        location_button = self.driver.find_element(By.XPATH, value='//*[@id="sticky-react-header"]/div/div[2]/div[1]/div/div[3]/button')
        self.driver.execute_script("arguments[0].click();", location_button)
        # actions = ActionChains(self.driver)
        # actions.move_to_element(location_button).click().perform()
        time.sleep(3)
        enter_zipcode = self.driver.find_element(By.XPATH, value='//*[@id="shopping-selector-search-cities"]')
        enter_zipcode.send_keys(zipcode)
        enter_zipcode.send_keys(Keys.ENTER)
        time.sleep(1)
        set_store_buttons = self.driver.find_elements(By.CLASS_NAME, value='button')
        set_store_buttons[1].click()

    def scrape_wegmans(self, items: list, zipcode: str):
        self._set_store_location(zipcode)

        data = {zipcode: {"Wegmans": {"Items": {}}}}
        for item in items:
            data[zipcode]["Wegmans"]["Items"][item] = self._scrape_wegmans(item)[0]

        json_data = json.dumps(data)
        with open("grocery_data.json", 'w') as file:
            file.write(json_data)

    def _scrape_wegmans(self, item: str):
        """
        Scrape wegmans website for an item
        :param item: Item to be searched
        :return:
        """

        self.driver.get(f"https://shop.wegmans.com/search?search_term={item}&search_is_autocomplete=true")
        time.sleep(2)
        wegmans_data = {}

        # Find all the item names, images on webpage
        # Need to scroll down for more items
        items = self.driver.find_elements(By.CLASS_NAME, value="css-131yigi")
        print(f"Items {len(items)}")
        prices = self.driver.find_elements(By.CLASS_NAME, value="css-zqx11d")
        print(f"prices {len(prices)}")
        images = self.driver.find_elements(By.CLASS_NAME, value="css-15zffbe")
        print(f"images {len(images)}")
        unit_prices = self.driver.find_elements(By.CLASS_NAME, value="css-1kh7mkb")
        print(len(unit_prices))

        # Process unit price data
        unit_prices = self._process_unit_price_data(unit_prices)

        # process individual price data
        prices = [float(price.text.replace('$', "").replace(" /ea", "")) for price in prices]

        # Make sure index won't go out of range
        length = len(items) if (len(items) < len(prices)) and (len(items) < len(images)) else len(images)

        # Set to five items for now
        for num in range(1):
            wegmans_data[num] = {"name": items[num].text,
                                 "price": prices[num],
                                 "price_per_ounce": unit_prices[num],
                                 "image": images[num].get_attribute("src")}
        return wegmans_data
    def _process_unit_price_data(self, unit_prices: list):
        """Process the text from selenium and format into an integer with unit ounces"""
        processed_unit_prices = []
        # Process unit price
        for price in unit_prices:
            if "gal" in price.text:
                processed: str = (price.text.
                                  replace("gal", "").
                                  replace("(", "").
                                  replace(")", "").
                                  replace("/", "").
                                  replace("$", "")
                                  )

                split_processed = processed.split(" ")
                # Remove empty strings
                split_processed = [item for item in split_processed if item]
                print(split_processed)
                unit_price = round(float(split_processed[1]) / 64, 2)
                processed_unit_prices.append(unit_price)

            elif "qt" in price.text:
                processed: str = (price.text.
                                  replace("qt", "").
                                  replace("(", "").
                                  replace(")", "").
                                  replace("/", "").
                                  replace("$", "")
                                  )

                split_processed = processed.split(" ")
                # Remove empty strings
                split_processed = [item for item in split_processed if item]
                print(split_processed)
                unit_price = round(float(split_processed[1]) / 32, 2)
                processed_unit_prices.append(unit_price)

            elif "oz" in price.text:
                processed: str = (price.text.
                                  replace("oz", "").
                                  replace("(", "").
                                  replace(")", "").
                                  replace("/", "").
                                  replace("$", "").
                                  replace("fl", "")
                                  )

                # Ex processed format is "16 0.60" which is "(num ounces) (price per ounce)
                split_processed = processed.split(" ")
                # Remove empty strings
                split_processed = [item for item in split_processed if item]
                print(split_processed)
                try:
                    unit_price = round(float(split_processed[1]), 2)
                    processed_unit_prices.append(unit_price)
                except ValueError:
                    print("Item not processed correctly")

            elif "lb" in price.text:
                processed = float(price.text.replace("lb", "").replace("/", "").replace("$", ""))
                ounces = processed / 16
                processed_unit_prices.append(ounces)

            elif "ct" in price.text:
                processed: str = (price.text.
                                  replace("ct", "").
                                  replace("(", "").
                                  replace(")", "").
                                  replace("/", "").
                                  replace("$", "").
                                  replace("fl", "")
                                  )

                # Ex processed format is "16 0.60" which is "(num ounces) (price per ounce)
                split_processed = processed.split(" ")
                # Remove empty strings
                split_processed = [item for item in split_processed if item]
                unit_price = round(float(split_processed[1]), 2)
                processed_unit_prices.append(unit_price)
            break
        return processed_unit_prices

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



