from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def find_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )   

    def click_element(self, locator, timeout=10):
        for attempt in range(3):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                break
            except StaleElementReferenceException:
                if attempt == 2:
                    raise
                self.logger.warning(f"StaleElementReferenceException, попытка {attempt + 1}")
                WebDriverWait(self.driver, 2).until(
                    lambda driver: False
                )
    
    def get_element_size(self, locator):
        element = self.find_element(locator)
        return element.size

    def get_current_url(self):
        return self.driver.current_url

    def wait_for_url_contains(self, text, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
        )

    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
        )

    def wait_for_page_loaded(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    