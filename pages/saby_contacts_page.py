from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class SabyContactsPage(BasePage):
    # Простые селекторы
    CONTACTS_BUTTON = (By.XPATH, "//*[contains(text(), 'Контакты')]")
    CONTACTS_LINK = (By.XPATH, "//a[contains(@href, '/contacts') and contains(., 'офиса в регионе')]")
    TENSOR_BANNER = (By.CSS_SELECTOR, "a.sbisru-Contacts__logo-tensor")


    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://saby.ru"

    def open_contacts_page(self):
        """Простой метод открытия страницы контактов"""
        print("1. Открываем saby.ru")
        self.driver.get(self.url)
        time.sleep(2)
        
        print("2. Кликаем на 'Контакты'")
        self.click_element(self.CONTACTS_BUTTON)
        time.sleep(2)
        
        print("3. Кликаем на ссылку в меню")
        self.click_element(self.CONTACTS_LINK)
        time.sleep(2)
        
        print(f"4. Текущий URL: {self.driver.current_url}")
        return self.driver.current_url

    def click_tensor_banner(self):
        """Кликаем на баннер Тензор"""
        print("5. Ищем и кликаем на баннер Тензор")
        self.click_element(self.TENSOR_BANNER)
        time.sleep(3)
        
        # Переключаемся на новую вкладку если открылась
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print(f"6. Переключились на новую вкладку: {self.driver.current_url}")