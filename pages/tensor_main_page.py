from selenium.webdriver.common.by import By
from .base_page import BasePage

class TensorMainPage(BasePage):
    """Page Object для главной страницы Tensor"""

    POWER_BLOCK = (By.CSS_SELECTOR, ".tensor_ru-Index__card-title")  # Блок "Сила в людях"
    DETAILS_LINK = (By.CSS_SELECTOR, "a.tensor_ru-link[href='/about']")  # Ссылка "Подробнее"

    def __init__(self, driver):
        super().__init__(driver)

    def find_power_block(self):
        """Поиск блока 'Сила в людях'"""
        return self.find_element(self.POWER_BLOCK, timeout=10)

    def click_details(self):
        """Клик по ссылке 'Подробнее'"""
        self.click_element(self.DETAILS_LINK)
        self.wait_for_url_contains("/about", timeout=10)
