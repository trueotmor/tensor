from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class SabyContactsPage(BasePage):
    """Page Object для страницы контактов Saby.ru"""
    
    # Селекторы для навигации
    CONTACTS_BUTTON = (By.CSS_SELECTOR, ".sbisru-Header-ContactsMenu__title span")  # Кнопка "Контакты" в шапке
    CONTACTS_LINK = (By.CSS_SELECTOR, ".sbisru-Header-ContactsMenu__items-visible a[href='/contacts']")  # Ссылка на контакты в меню
    TENSOR_BANNER = (By.CSS_SELECTOR, "a.sbisru-Contacts__logo-tensor")  # Баннер Tensor на странице контактов
    
    # Селекторы для регионов
    CURRENT_REGION = (By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text")  # Текущий выбранный регион
    REGION_DIALOG = (By.CSS_SELECTOR, ".sbis_ru-Region-Panel")  # Диалог выбора региона
    REGION_ITEMS = (By.CSS_SELECTOR, ".sbis_ru-Region-Panel__item")  # Элементы списка регионов
    REGION_TITLE = (By.CSS_SELECTOR, "span[title]")  # Название региона в элементе
    
    # Селекторы для партнеров
    PARTNERS_CONTAINER = (By.CSS_SELECTOR, "[data-qa='items-container']")  # Контейнер со списком партнеров
    PARTNER_ITEMS = (By.CSS_SELECTOR, ".sbisru-Contacts-List__item")  # Элементы партнеров
    PARTNER_NAME = (By.CSS_SELECTOR, ".sbisru-Contacts-List__name")  # Название партнера
    PARTNER_ADDRESS = (By.CSS_SELECTOR, ".sbisru-Contacts-List__address")  # Адрес партнера

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://saby.ru"

    def open_page(self):
        """Открывает главную страницу Saby.ru"""
        self.driver.get(self.url)
        self.wait_for_page_loaded()

    def click_contacts_button(self):
        """Клик по кнопке 'Контакты' в шапке"""
        self.click_element(self.CONTACTS_BUTTON)
        self.wait_visible(self.CONTACTS_LINK, timeout=10)

    def click_contacts_link(self):
        """Клик по ссылке на страницу контактов"""
        self.click_element(self.CONTACTS_LINK)
        self.wait_for_url_contains("/contacts", timeout=10)

    def click_tensor_banner(self):
        """Клик по баннеру Tensor и переключение на новую вкладку"""
        self.click_element(self.TENSOR_BANNER)
        WebDriverWait(self.driver, 10).until(
            lambda driver: len(driver.window_handles) > 1
        )
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait_for_page_loaded()

    def get_current_region(self):
        """Получение названия текущего региона"""
        region_element = self.find_element(self.CURRENT_REGION, timeout=10)
        return region_element.text.strip()

    def get_partners(self):
        """Получение списка всех видимых партнеров"""
        try:
            self.find_element(self.PARTNERS_CONTAINER, timeout=10)
            partner_elements = self.driver.find_elements(*self.PARTNER_ITEMS)
            return [partner for partner in partner_elements if partner.is_displayed()]
        except Exception as e:
            self.logger.warning(f"Не удалось найти партнеров: {e}")
            return []

    def get_partners_info(self):
        """Получение информации обо всех партнерах (название и адрес)"""
        partners_info = []
        try:
            partner_elements = self.driver.find_elements(*self.PARTNER_ITEMS)
            for i, partner in enumerate(partner_elements):
                if partner.is_displayed():
                    partner_info = self._extract_partner_info(partner, i + 1)
                    if partner_info:
                        partners_info.append(partner_info)
        except Exception as e:
            self.logger.warning(f"Ошибка при получении информации о партнерах: {e}")
        return partners_info

    def _extract_partner_info(self, partner_element, number):
        """Извлечение информации о партнере"""
        try:
            name = partner_element.find_element(*self.PARTNER_NAME).text
            address = partner_element.find_element(*self.PARTNER_ADDRESS).text
            return {'number': number, 'name': name, 'address': address}
        except Exception as e:
            self.logger.warning(f"Не удалось получить данные партнера #{number}: {e}")
            return {'number': number, 'name': 'Не удалось получить данные', 'address': ''}

    def open_region_chooser(self):
        """Открывает диалог выбора региона"""
        self.click_element(self.CURRENT_REGION)
        self.wait_visible(self.REGION_DIALOG, timeout=10)
        self.logger.info("Диалог выбора региона открыт")

    def select_region_by_name(self, region_name):
        """Выбирает регион по названию"""
        self.logger.info(f"Ищем регион: {region_name}")
        
        region_elements = self.driver.find_elements(*self.REGION_ITEMS)
        self.logger.info(f"Найдено регионов в списке: {len(region_elements)}")
        
        target_region = self._find_region_element(region_elements, region_name)
        
        if target_region:
            self._click_and_wait_for_close(target_region, region_name)
        else:
            raise Exception(f"Регион '{region_name}' не найден в списке")

    def _find_region_element(self, region_elements, region_name):
        """Поиск элемента региона по названию"""
        for region in region_elements:
            try:
                region_text = region.text.strip()
                region_title = region.find_element(*self.REGION_TITLE).get_attribute("title")
                
                if region_name in region_text or region_name in region_title:
                    self.logger.info(f"Найден регион: {region_text}")
                    return region
            except Exception as e:
                self.logger.warning(f"Ошибка при проверке региона: {e}")
        return None

    def _click_and_wait_for_close(self, target_region, region_name):
        """Клик по региону и ожидание закрытия диалога"""
        target_region.click()
        self.logger.info(f"Выбран регион: {region_name}")
        
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.REGION_DIALOG)
        )
        self.wait_for_page_loaded()

    def select_kamchatka_region(self):
        """Выбирает Камчатский край"""
        return self.select_region_by_name("Камчатский край")

    def get_page_title(self):
        """Получение title страницы"""
        return self.driver.title

    def wait_for_region_changed(self, expected_region, timeout=10):
        """Ожидание смены региона"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: expected_region.lower() in self.get_current_region().lower()
        )

    def wait_for_partners_updated(self, timeout=10):
        """Ожидание обновления списка партнеров"""
        self.find_element(self.PARTNERS_CONTAINER, timeout=timeout)
