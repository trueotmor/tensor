from selenium.webdriver.common.by import By
from .base_page import BasePage

class TensorAboutPage(BasePage):
    POWER_IN_PEOPLE_BLOCK = (By.XPATH, "//*[contains(text(), 'Сила в людях')]")
    DETAILS_LINK = (By.XPATH, "//a[contains(text(), 'Подробнее')]")
    WORKING_SECTION = (By.XPATH, "//h2[contains(text(), 'Работаем')]/..")
    WORKING_IMAGES = (By.XPATH, "//h2[contains(text(), 'Работаем')]/..//img")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://tensor.ru"

    def open(self):
        self.driver.get(self.url)

    def is_power_in_people_displayed(self):
        try:
            return self.find_element(self.POWER_IN_PEOPLE_BLOCK).is_displayed()
        except:
            return False

    def click_details(self):
        self.click_element(self.DETAILS_LINK)

    def get_working_images_sizes(self):
        images = self.driver.find_elements(*self.WORKING_IMAGES)
        return [img.size for img in images]