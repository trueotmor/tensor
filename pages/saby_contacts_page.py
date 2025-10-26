from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class SabyContactsPage(BasePage):
    # Простые селекторы
    CONTACTS_BUTTON = (By.XPATH, "//*[contains(text(), 'Контакты')]")
    CONTACTS_LINK = (By.XPATH, "//a[contains(@href, '/contacts') and contains(., 'офиса в регионе')]")
    TENSOR_BANNER = (By.CSS_SELECTOR, "a.sbisru-Contacts__logo-tensor")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://saby.ru"

    def open_page(self):
        self.driver.get(self.url)
        self.wait_for_page_loaded()

    def click_contacts_button(self):
        self.click_element(self.CONTACTS_BUTTON)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CONTACTS_LINK)
        )

    def click_contacts_link(self):
        self.click_element(self.CONTACTS_LINK)
        self.wait_for_url_contains("/contacts", timeout=10)

    def click_tensor_banner(self):
        self.click_element(self.TENSOR_BANNER)
        WebDriverWait(self.driver, 10).until(
            lambda driver: len(driver.window_handles) > 1
        )
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait_for_page_loaded()