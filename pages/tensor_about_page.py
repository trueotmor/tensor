from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class TensorAboutPage(BasePage):
    WORKING_IMAGES = (By.CSS_SELECTOR, "img.tensor_ru-About__block3-image")

    def __init__(self, driver):
        super().__init__(driver)

    def find_working_images(self):
        self.logger.info("✅ 11. Поиск изображений в разделе 'Работаем'")
        images = self.driver.find_elements(*self.WORKING_IMAGES)
        self.logger.info(f"Найдено изображений: {len(images)}")
        return images

    def verify_images_same_size(self):
        self.logger.info("✅ 12. Сравниваем размеры изображений в разделе 'Работаем'")
        
        # Ищем изображения
        images = self.find_working_images()
        
        if len(images) < 2:
            self.logger.error("⚠️ Меньше 2 изображений, проверка бессмысленна")
            return False
            
        # Проверяем размеры
        first_size = images[0].size
                
        for i, img in enumerate(images, 1):
            img_size = img.size
            alt = img.get_attribute("alt") or "no alt"
            self.logger.info(f"Размер изображения {i} : {img_size} - \"{alt}\"")
            
            if img_size['width'] != first_size['width'] or img_size['height'] != first_size['height']:
                self.logger.error(f"❌ Изображение {i} имеет другой размер")
                return False
        
        self.logger.info("✅ Все изображения одинакового размера")
        return True