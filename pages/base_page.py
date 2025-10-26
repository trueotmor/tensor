from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import logging

class BasePage:
    """Базовый класс для всех Page Object"""
    
    MAX_STALE_RETRIES = 3
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def _create_wait(self, timeout=10):
        """Создание объекта WebDriverWait"""
        return WebDriverWait(self.driver, timeout)

    def find_element(self, locator, timeout=10):
        """Поиск элемента по локатору"""
        return self._create_wait(timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click_element(self, locator, timeout=10):
        """Клик по элементу с обработкой StaleElementReferenceException"""
        for attempt in range(self.MAX_STALE_RETRIES):
            try:
                element = self._create_wait(timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == self.MAX_STALE_RETRIES - 1:
                    raise
                self.logger.warning(f"StaleElementReferenceException, попытка {attempt + 1}")
                continue
    
    def get_element_size(self, locator):
        """Получение размера элемента"""
        element = self.find_element(locator)
        return element.size

    def get_current_url(self):
        """Получение текущего URL"""
        return self.driver.current_url

    def wait_for_url_contains(self, text, timeout=10):
        """Ожидание появления текста в URL"""
        self._create_wait(timeout).until(EC.url_contains(text))

    def wait_visible(self, locator, timeout=10):
        """Ожидание видимости элемента"""
        return self._create_wait(timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=10):
        """Ожидание кликабельности элемента"""
        return self._create_wait(timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_page_loaded(self, timeout=15):
        """Ожидание полной загрузки страницы"""
        self._create_wait(timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element_invisible(self, locator, timeout=10):
        """Ожидание исчезновения элемента"""
        self._create_wait(timeout).until(
            EC.invisibility_of_element_located(locator)
        )
