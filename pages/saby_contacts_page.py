from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class SabyContactsPage(BasePage):
    CONTACTS_BUTTON = (By.CSS_SELECTOR, ".sbisru-Header-ContactsMenu__title span")
    CONTACTS_LINK = (By.CSS_SELECTOR, ".sbisru-Header-ContactsMenu__items-visible a[href='/contacts']")
    TENSOR_BANNER = (By.CSS_SELECTOR, "a.sbisru-Contacts__logo-tensor")
    
    CURRENT_REGION = (By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text")
    REGION_CHOOSER = (By.CSS_SELECTOR, ".sbis_ru-Region-Chooser")
    PARTNERS_LIST = (By.CSS_SELECTOR, ".sbisru-Contacts-List__item")

    REGION_DIALOG = (By.CSS_SELECTOR, ".sbis_ru-Region-Panel")
    REGION_ITEMS = (By.CSS_SELECTOR, ".sbis_ru-Region-Panel__item")

    PARTNERS_CONTAINER = (By.CSS_SELECTOR, "[data-qa='items-container']")
    PARTNER_ITEMS = (By.CSS_SELECTOR, ".sbisru-Contacts-List__item")
    PARTNER_CITIES = (By.CSS_SELECTOR, ".sbisru-Contacts-List__city")

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

    def get_current_region(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CURRENT_REGION)
        )
        region_element = self.find_element(self.CURRENT_REGION, timeout=10)
        return region_element.text.strip()

    def get_partners(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PARTNERS_CONTAINER)
            )
            partner_elements = self.driver.find_elements(*self.PARTNER_ITEMS)
            partners = [partner for partner in partner_elements if partner.is_displayed()]
            return partners
            
        except Exception as e:
            self.logger.warning(f"Не удалось найти сертифицированных партнеров: {e}")
            return []

    def get_partners_info(self):
        partners_info = []
        try:
            partner_elements = self.driver.find_elements(*self.PARTNER_ITEMS)
            for i, partner in enumerate(partner_elements):
                if partner.is_displayed():
                    try:
                        name = partner.find_element(By.CSS_SELECTOR, ".sbisru-Contacts-List__name").text
                        address = partner.find_element(By.CSS_SELECTOR, ".sbisru-Contacts-List__address").text
                        partners_info.append({
                            'number': i + 1,
                            'name': name,
                            'address': address
                        })
                    except:
                        partners_info.append({'number': i + 1, 'name': 'Не удалось получить данные'})
        except Exception as e:
            self.logger.warning(f"Ошибка при получении информации о партнерах: {e}")
        
        return partners_info

    def open_region_chooser(self):
        self.click_element(self.CURRENT_REGION)
        
        # Ждем появления диалога выбора региона
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.REGION_DIALOG)
        )
        self.logger.info("Диалог выбора региона открыт")

    def select_region_by_name(self, region_name):
        self.logger.info(f"Ищем регион: {region_name}")
        
        # Ищем все элементы регионов
        region_elements = self.driver.find_elements(*self.REGION_ITEMS)
        self.logger.info(f"Найдено регионов в списке: {len(region_elements)}")
        
        # Ищем регион по названию
        target_region = None
        for region in region_elements:
            try:
                # Получаем текст региона
                region_text = region.text.strip()
                # Получаем title региона
                region_title = region.find_element(By.CSS_SELECTOR, "span[title]").get_attribute("title")
                
                self.logger.debug(f"Проверяем регион: text='{region_text}', title='{region_title}'")
                
                if region_name in region_text or region_name in region_title:
                    target_region = region
                    self.logger.info(f"Найден регион: {region_text}")
                    break
            except Exception as e:
                self.logger.warning(f"Ошибка при проверке региона: {e}")
                continue
        
        if target_region:
            target_region.click()
            self.logger.info(f"Выбран регион: {region_name}")
            
            # Ждем закрытия диалога и обновления страницы
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.REGION_DIALOG)
            )
            self.wait_for_page_loaded()
        else:
            raise Exception(f"Регион '{region_name}' не найден в списке")

    def select_kamchatka_region(self):
        return self.select_region_by_name("Камчатский край")

    def get_page_title(self):
        return self.driver.title

    def wait_for_region_changed(self, expected_region, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: expected_region.lower() in self.get_current_region().lower()
        )

    def wait_for_partners_updated(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.PARTNERS_CONTAINER)
        )