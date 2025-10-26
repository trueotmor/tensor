import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.saby_contacts_page import SabyContactsPage
from pages.tensor_main_page import TensorMainPage
from pages.tensor_about_page import TensorAboutPage

def test_full_scenario():
    print("🚀 Запуск полного сценария")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # 1. Saby контакты
        saby_page = SabyContactsPage(driver)
        saby_page.open_contacts_page()
        
        # 2. Баннер Тензор
        saby_page.click_tensor_banner()
        
        # 3. Tensor главная
        tensor_main = TensorMainPage(driver)
        
        # 4. Проверка блока "Сила в людях"
        assert tensor_main.is_power_block_displayed(), "Блок 'Сила в людях' не найден"
        print("✅ Блок 'Сила в людях' найден")
        
        # 5. Переход в Подробнее
        tensor_main.click_details()
        
        # 6. Проверка URL about
        current_url = driver.current_url
        assert current_url == "https://tensor.ru/about", f"Ожидался https://tensor.ru/about, получен {current_url}"
        print("✅ Успешно перешли на страницу about")
        
        # 7. Проверка изображений
        tensor_about = TensorAboutPage(driver)
        assert tensor_about.verify_images_same_size(), "Изображения имеют разные размеры"
        print("✅ Все изображения одинакового размера")
        
        print("\n🎉 ВЕСЬ СЦЕНАРИЙ УСПЕШНО ВЫПОЛНЕН!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    test_full_scenario()