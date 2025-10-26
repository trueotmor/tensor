from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TensorAboutPage(BasePage):
    WORKING_IMAGES = (By.CSS_SELECTOR, "img.tensor_ru-About__block3-image")

    def __init__(self, driver):
        super().__init__(driver)

    def find_working_images(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.WORKING_IMAGES)
        )
        images = self.driver.find_elements(*self.WORKING_IMAGES)
        return images