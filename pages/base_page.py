from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info("BasePage initialized")

    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:    
            self.logger.error(f"Element not found: {locator}")
            raise

    def click_element(self, locator):   
        element = self.find_element(locator)
        element.click()

    def get_element_size(self, locator):
        element = self.find_element(locator)
        return element.size

    def get_current_url(self):
        return self.driver.current_url