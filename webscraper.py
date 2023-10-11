import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class WebScraper:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--disable-javascript")
        # chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)

        # self.uc_options = uc.ChromeOptions()
        # self.uc_options.add_argument("--start-maximized")
        # self.uc_options.add_experimental_option("prefs", {"credentials_enable_service": False,
        #                                              "profile.password_manager_enabled": False})

        # self.uc_driver = uc.Chrome(options=self.uc_options)
    def scrape_wegmans(self, item):
        """
        Retrieve the name, price and jpg of items on a webpage from giant
        :return: Return a dictionary with a num as the key and a value that's a dictionary with the name, price and jpg
        """
        wegmans_data = {}
        self.driver.get(f"https://shop.wegmans.com/search?search_term={item}&search_is_autocomplete=true")

        # Click Wegman's in store button
        time.sleep(3)
        in_store_button = self.driver.find_element(By.XPATH, value='//*[@id="shopping-selector-shop-context-intent-instore"]')
        in_store_button.click()

        # Click the reload button
        time.sleep(2)
        reload_button = self.driver.find_element(By.XPATH, value='//*[@id="react"]/div[2]/div/button')
        reload_button.click()

        # Find all the item names, images on webpage
        # Need to scroll down for more items
        time.sleep(3)
        items = self.driver.find_elements(By.CLASS_NAME, value="css-131yigi")
        print(f"Items {len(items)}")
        prices = self.driver.find_elements(By.CLASS_NAME, value="css-zqx11d")
        print(f"prices {len(prices)}")
        images = self.driver.find_elements(By.CLASS_NAME, value="css-15zffbe")
        print(f"images {len(images)}")

        # Strip price and convert to float
        int_prices = [float(price.text.replace('$', "").replace(" /ea", "")) for price in prices]


        # Make sure index won't go out of range
        length = len(items) if (len(items) < len(prices)) and (len(items) < len(images)) else len(images)

        for num in range(length):
            wegmans_data[num] = {"name": items[num].text,
                                 "price": int_prices[num],
                                 "image": images[num].get_attribute("src")}
        
        print(wegmans_data)

    def scrape_walmart(self, item):
        """
        Retrieve the name, price and jpg of items on a webpage from giant
        :return: Return a dictionary with a num as the key and a value that's a dictionary with the name, price and jpg
        """
        walmart_data = {}
        self.uc_driver.get("https://www.google.com/")
        google_search = self.uc_driver.find_element(By.CLASS_NAME, value='gLFyf')
        google_search.send_keys("Walmart")
        time.sleep(2)
        search_button = self.uc_driver.find_element(By.CLASS_NAME, value='gNO89b')
        search_button.click()
        time.sleep(3)
        # walmart_link = self.uc_driver.find_element(By.CLASS_NAME, value='LC20lb MBeuO DKV0Md')
        # walmart_link.click()
        # items = self.uc_driver.find_element(By.CLASS_NAME, value="absolute w-100 h-100 z-1 hide-sibling-opacity")

        # prices = []
        # images = []
        # for item in items:
        #     item.click()
        #     time.sleep(2)
        #     prices.append(self.uc_driver.find_element(By.XPATH, value = '//*[@id="maincontent"]/section/main/div[2]/div[2]/div/div[2]/div/div[2]/div/div/span[1]/span[2]/span'))
        #     images.append(self.uc_driver.find_element(By.XPATH, value = '//*[@id="maincontent"]/section/main/div[2]/div[2]/div/div[1]/div/div/section[1]/div[2]/div[1]/div/div/div/img'))
        #     self.uc_driver.back()
        #     time.sleep(2)
        #
        # # Strip price and convert to float
        # int_prices = [float(price.text.replace('$', "").strip()) for price in prices]
        #
        # for num in range(len(items)):
        #     walmart_data[num] = {"name": items[num].get_attribute('href'),
        #                          "price": int_prices[num],
        #                          "image": images[num].get_attribute("src")}
        #
        # print(walmart_data)

        time.sleep(50000)

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
        length = len(items) if (len(items) < len(prices)) and (len(items) < len(images)) else len(images)

        for num in range(length):
            shoprite_data[num] = {"name": items[num].text,
                                 "price": int_prices[num],
                                 "image": images[num].get_attribute("src")}

        print(shoprite_data)
    def close_browser(self):
        self.driver.quit()



