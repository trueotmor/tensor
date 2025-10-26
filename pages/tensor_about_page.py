from selenium.webdriver.common.by import By
from .base_page import BasePage

class TensorAboutPage(BasePage):
    WORKING_IMAGES = (By.CSS_SELECTOR, "img.tensor_ru-About__block3-image")

    def __init__(self, driver):
        super().__init__(driver)

    def find_working_images(self):
        images = self.driver.find_elements(*self.WORKING_IMAGES)
        return images