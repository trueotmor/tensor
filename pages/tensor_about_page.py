import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class TensorAboutPage(BasePage):
    WORKING_SECTION = (By.XPATH, "//*[contains(text(), 'Работаем')]")
    WORKING_IMAGES = (By.XPATH, "//img[contains(@src, 'work') or contains(@alt, 'работа') or contains(@class, 'work')]")

    def __init__(self, driver):
        super().__init__(driver)

    def verify_images_same_size(self):
        """Проверяем что все изображения одинакового размера"""
        print("9. Проверяем размеры изображений в разделе 'Работаем'")
        
        # Даем время для полной загрузки страницы
        time.sleep(3)   
        
        # Ищем изображения
        images = self.driver.find_elements(*self.WORKING_IMAGES)
        print(f"Найдено изображений: {len(images)}")
        
        if len(images) < 2:
            print("⚠️ Меньше 2 изображений, проверка бессмысленна")
            return True
            
        # Выводим информацию о размерах для отладки
        first_size = images[0].size
        print(f"Размер первого изображения: {first_size}")
        
        for i, img in enumerate(images[1:], 1):
            img_size = img.size
            print(f"Размер изображения {i+1}: {img_size}")
            if img_size['width'] != first_size['width'] or img_size['height'] != first_size['height']:
                print(f"❌ Изображение {i+1} имеет другой размер")
                return False
        
        print("✅ Все изображения одинакового размера")
        return True