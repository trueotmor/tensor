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

    def open_contacts_page(self):
        self.logger.info("✅ 1. Открываем saby.ru")
        self.driver.get(self.url)
        self.wait_for_page_loaded()
                
        self.logger.info("✅ 2. Кликаем на 'Контакты'")
        self.click_element(self.CONTACTS_BUTTON)
        
        self.logger.info("✅ 3. Ждем появления ссылки в выпадающем меню")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CONTACTS_LINK)
        )

        self.logger.info("✅ 4. Кликаем на ссылку в меню")
        self.click_element(self.CONTACTS_LINK)
        
        self.wait_for_url_contains("/contacts", timeout=15)
        current_url = self.get_current_url()
        self.logger.info(f"✅ 5. Страница контактов загружена: {current_url}")
        return current_url

    def click_tensor_banner(self):

        self.logger.info("✅ 6. Ищем и кликаем на баннер Тензор")
        self.click_element(self.TENSOR_BANNER)
        
        # Ждем открытия новой вкладки
        WebDriverWait(self.driver, 10).until(
            lambda driver: len(driver.window_handles) > 1
        )
        
        # Переключаемся на новую вкладку
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait_for_page_loaded()
        self.logger.info(f"✅ 7. Переключились на tensor.ru: {self.driver.current_url}")