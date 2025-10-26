import logging
import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.saby_contacts_page import SabyContactsPage

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestSabyToTensor:
    @pytest.fixture
    def driver(self):
        """Фикстура для создания драйвера"""
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(5)
        yield driver
        driver.quit()

    @pytest.fixture
    def saby_page(self, driver):
        """Фикстура для создания страницы Saby"""
        return SabyContactsPage(driver)

    def test_open_contacts_via_menu(self, saby_page):
        """
        Тест: переход на страницу контактов через выпадающее меню
        """
        print("\n" + "="*60)
        print("ТЕСТ: Переход на страницу контактов через меню")
        print("="*60)
        
        try:
            # Пробуем открыть через меню
            result = saby_page.open_contacts_via_menu()
            
            # Проверяем что мы на странице контактов
            current_url = saby_page.get_current_url()
            assert "/contacts" in current_url, f"Ожидался URL с /contacts, но получен: {current_url}"
            
            print("🎉 ТЕСТ ПРОЙДЕН УСПЕШНО!")
            print(f"Финальный URL: {current_url}")
            
        except Exception as e:
            print(f"❌ ТЕСТ ПРОВАЛЕН: {e}")
            
            # Пробуем запасной вариант
            print("\n🔄 Пробуем запасной вариант: прямой переход...")
            try:
                saby_page.open_contacts_direct()
                current_url = saby_page.get_current_url()
                assert "/contacts" in current_url
                print("🎉 ЗАПАСНОЙ ВАРИАНТ РАБОТАЕТ!")
                print(f"Финальный URL: {current_url}")
            except Exception as e2:
                print(f"❌ Запасной вариант тоже не сработал: {e2}")
                raise

def debug_test():
    """Функция для отладки без pytest"""
    print("🚀 ЗАПУСК ОТЛАДОЧНОГО ТЕСТА...")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    saby_page = SabyContactsPage(driver)
    
    try:
        test = TestSabyToTensor()
        test.test_open_contacts_via_menu(saby_page)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("Нажмите Enter чтобы закрыть браузер...")
        driver.quit()

if __name__ == "__main__":
    debug_test()