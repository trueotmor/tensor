from selenium.webdriver.common.by import By
from .base_page import BasePage

class TensorMainPage(BasePage):
    POWER_BLOCK = (By.XPATH, "//p[@class='tensor_ru-Index__card-title tensor_ru-pb-16' and contains(text(), 'Сила в людях')]")
    DETAILS_LINK = (By.XPATH, "//a[@href='/about' and contains(text(), 'Подробнее')]")

    def __init__(self, driver):
        super().__init__(driver)

    def is_power_block_displayed(self):
        """Проверяем наличие блока 'Сила в людях'"""
        self.logger.info("✅ 8. Проверяем блок 'Сила в людях'")
        try:
            element = self.find_element(self.POWER_BLOCK, timeout=10)
            is_displayed = element.is_displayed()
            self.logger.info(f"Блок 'Сила в людях' найден и видим: {is_displayed}")
            return is_displayed
        except Exception as e:
            self.logger.error(f"❌ Блок 'Сила в людях' не найден: {e}")
            return False

    def click_details(self):
        self.logger.info("✅ 9. Кликаем на 'Подробнее'")
        self.click_element(self.DETAILS_LINK)
        
        self.wait_for_url_contains("/about", timeout=15)
        self.logger.info("✅ 10. Успешно перешли на страницу about")