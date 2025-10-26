from selenium.webdriver.common.by import By
from .base_page import BasePage

class TensorMainPage(BasePage):
    POWER_BLOCK = (By.XPATH, "//p[@class='tensor_ru-Index__card-title tensor_ru-pb-16' and contains(text(), 'Сила в людях')]")
    DETAILS_LINK = (By.XPATH, "//a[@href='/about' and contains(text(), 'Подробнее')]")

    def __init__(self, driver):
        super().__init__(driver)

    def find_power_block(self):
        return self.find_element(self.POWER_BLOCK, timeout=5)

    def click_details(self):
        self.click_element(self.DETAILS_LINK)
        self.wait_for_url_contains("/about", timeout=10)