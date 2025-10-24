from selenium.webdriver.common.by import By
from .base_page import BasePage

class SabyContactsPage(BasePage):
    CONTACTS_LINK = (By.LINK_TEXT, "Контакты")
    TENSOR_BANNER = (By.XPATH, "//img[contains(@alt, 'Тензор')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://saby.ru"

    def open_contacts(self):
        self.driver.get(self.url)
        self.click_element(self.CONTACTS_LINK)

    def click_tensor_banner(self):
        self.click_element(self.TENSOR_BANNER)