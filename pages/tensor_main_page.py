from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TensorMainPage(BasePage):
    POWER_BLOCK = (By.XPATH, "//p[@class='tensor_ru-Index__card-title tensor_ru-pb-16' and contains(text(), 'Сила в людях')]")
    DETAILS_LINK = (By.XPATH, "//a[@href='/about' and contains(text(), 'Подробнее')]")

    def __init__(self, driver):
        super().__init__(driver)

    def find_power_block(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.POWER_BLOCK)
        )
        return self.driver.find_element(*self.POWER_BLOCK)

    def click_details(self):
        self.click_element(self.DETAILS_LINK)
        self.wait_for_url_contains("/about", timeout=10)